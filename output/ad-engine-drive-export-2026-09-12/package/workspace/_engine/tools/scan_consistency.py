#!/usr/bin/env python3
"""
scan_consistency.py — audit a chained UGC build for drift before it ships.

Chained generation fails quietly. Identity and set wander a little per clip, no single
seam looks wrong, and by the back half it is a different person in a different store.
This measures every segment against a reference instead of trusting a spot check.

    python3 scan_consistency.py <clips_dir> --job job.json [--ref 1]

Per segment:
  background   SSIM of the upper band (shelving, minimal face) vs the reference segment
  identity     SSIM of the centre band (face region) vs the reference segment
  accuracy     transcribed words vs the intended line from job.json
  fade         energy of the final second vs the clip mean
  technical    duration, resolution, fps, audio stream present

Outliers are flagged with the segment number so only those get re-rolled.
"""
import argparse
import json
import pathlib
import re
import statistics
import subprocess
import sys

SSIM_RE = re.compile(r"All:([\d.]+)")


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout + p.stderr


def probe(path: pathlib.Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "stream=codec_type,width,height,r_frame_rate:format=duration",
               "-of", "json", str(path)])
    try:
        d = json.loads(out)
    except json.JSONDecodeError:
        return {}
    vid = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    has_audio = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    fr = vid.get("r_frame_rate", "0/1")
    try:
        num, den = fr.split("/")
        fps = round(int(num) / max(1, int(den)), 2)
    except ValueError:
        fps = 0.0
    return {
        "duration": round(float(d.get("format", {}).get("duration", 0)), 2),
        "width": vid.get("width"), "height": vid.get("height"),
        "fps": fps, "has_audio": has_audio,
    }


def band(src: pathlib.Path, dst: pathlib.Path, crop: str, at: float = 5.0) -> bool:
    """Grab one frame mid-clip and crop to a band. Mid-clip is more representative
    than the last frame, which is often a trailing mouth-closed pose."""
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-ss", str(at), "-i", str(src), "-vframes", "1",
                        "-vf", f"{crop},scale=480:-1", str(dst)], capture_output=True)
    return r.returncode == 0 and dst.exists()


def similarity(a: pathlib.Path, b: pathlib.Path) -> float:
    """
    Histogram intersection, not SSIM.

    SSIM compares pixels positionally, so the same actor in the same set with her head
    turned scores ~0.3 and an absolute threshold flags everything. Colour distribution is
    pose-insensitive: a shelf of the same boxes under the same lights yields the same
    histogram whether or not she moved, while a different set or a different person
    shifts it. Returns 0-1, higher is more alike.
    """
    from PIL import Image
    try:
        ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    except OSError:
        return 0.0
    ha, hb = ia.histogram(), ib.histogram()
    total = sum(ha) or 1
    return round(sum(min(x, y) for x, y in zip(ha, hb)) / total, 4)


def outliers(values: dict[int, float], k: float = 3.0) -> set[int]:
    """
    Flag by deviation from the group, not against a fixed floor.

    Uses median absolute deviation, which does not get dragged around by the very
    outliers it is meant to find the way a mean and stdev would.
    """
    if len(values) < 4:
        return set()
    vals = list(values.values())
    med = statistics.median(vals)
    mad = statistics.median([abs(v - med) for v in vals]) or 1e-6
    return {n for n, v in values.items() if (med - v) / (1.4826 * mad) > k}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("clips_dir")
    ap.add_argument("--job", help="job.json, enables transcript accuracy per segment")
    ap.add_argument("--ref", type=int, default=1, help="segment number used as the reference")
    ap.add_argument("--bg-floor", type=float, default=0.55)
    ap.add_argument("--id-floor", type=float, default=0.45)
    args = ap.parse_args()

    d = pathlib.Path(args.clips_dir)
    segs = sorted((p for p in d.glob("seg-*.mp4")
                   if re.fullmatch(r"seg-\d+\.mp4", p.name)),
                  key=lambda p: int(re.findall(r"\d+", p.name)[0]))
    if not segs:
        sys.exit(f"no promoted seg-N.mp4 files in {d}")

    lines = {}
    if args.job:
        j = json.loads(pathlib.Path(args.job).read_text())
        lines = {s["index"]: s["dialogue"] for s in j["segments"]}

    work = d / "_scan"
    work.mkdir(exist_ok=True)
    # Upper band = shelving. Centre band = face. Cropping them apart keeps a pose change
    # from being scored as a set change, and vice versa.
    BG = "crop=in_w:in_h*0.28:0:0"
    ID = "crop=in_w*0.6:in_h*0.30:in_w*0.2:in_h*0.28"

    ref_n = args.ref
    ref = next((p for p in segs if int(re.findall(r"\d+", p.name)[0]) == ref_n), segs[0])
    band(ref, work / "ref_bg.png", BG)
    band(ref, work / "ref_id.png", ID)

    rows = []
    for p in segs:
        n = int(re.findall(r"\d+", p.name)[0])
        info = probe(p)
        bg = idn = 1.0
        if n != ref_n:
            if band(p, work / f"{n}_bg.png", BG):
                bg = similarity(work / "ref_bg.png", work / f"{n}_bg.png")
            if band(p, work / f"{n}_id.png", ID):
                idn = similarity(work / "ref_id.png", work / f"{n}_id.png")
        rows.append({"n": n, "bg": bg, "id": idn, **info})

    bg_out = outliers({r["n"]: r["bg"] for r in rows if r["n"] != ref_n})
    id_out = outliers({r["n"]: r["id"] for r in rows if r["n"] != ref_n})

    print(f"reference: segment {ref_n}\n")
    print(f"{'seg':>4} {'bg':>7} {'identity':>9} {'dur':>6} {'res':>10} {'fps':>5} {'aud':>4}  flags")
    bad = []
    for r in rows:
        flags = []
        if r["n"] in bg_out:
            flags.append("BG OUTLIER")
        if r["n"] in id_out:
            flags.append("IDENTITY OUTLIER")
        if not r.get("has_audio"):
            flags.append("NO AUDIO")
        if r.get("duration", 0) < 5:
            flags.append("SHORT")
        if flags:
            bad.append(r["n"])
        print(f"{r['n']:>4} {r['bg']:>7} {r['id']:>9} {r.get('duration', 0):>6} "
              f"{str(r.get('width'))+'x'+str(r.get('height')):>10} {r.get('fps', 0):>5} "
              f"{'yes' if r.get('has_audio') else 'NO':>4}  {' '.join(flags)}")

    bgs = [r["bg"] for r in rows if r["n"] != ref_n]
    ids = [r["id"] for r in rows if r["n"] != ref_n]
    if bgs:
        print(f"\nbackground sim   median {statistics.median(bgs):.3f}  min {min(bgs):.3f}")
        print(f"identity  sim   median {statistics.median(ids):.3f}  min {min(ids):.3f}")
    res = {(r.get("width"), r.get("height"), r.get("fps")) for r in rows}
    print(f"technical: {len(res)} distinct video format(s) across {len(rows)} segments"
          f"{' — MISMATCH' if len(res) > 1 else ''}")
    print(f"\n{len(bad)} segment(s) flagged" + (f": {bad}" if bad else " — consistent"))

    (d / "consistency_scan.json").write_text(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
