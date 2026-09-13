#!/usr/bin/env python3
"""
harvest_media.py, resolve every link on an application, download the videos,
and explode them into frames + transcripts so the screening agent can actually
watch them.

Two extraction profiles, because a Loom and a portfolio ad need opposite things:

  loom : the applicant talking about their workflow for 5-8 minutes.
         Transcript is the payload. Frames are a sanity check (is it really them,
         is there a screen share). Sparse frames, mandatory transcript.

  ad   : a finished ad. Frames are the payload. The first 3 seconds are sampled
         densely at 4fps because the rubric weights the hook heavier than
         anything else, then scene-change detection covers the rest of the cut.

Usage
  python3 harvest_media.py --run <run_dir> [--max-videos 5] [--only <applicant_id>]

Reads  <run_dir>/applicants.json   (written by the browser harvest step)
Writes <run_dir>/media/<applicant_id>/…   frames, transcripts, media.json
       <run_dir>/media/index.json         roll-up of what landed and what failed
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------- link routing

VIDEO_HOSTS = (
    "loom.com", "youtube.com", "youtu.be", "vimeo.com", "tiktok.com",
    "instagram.com", "facebook.com", "fb.watch", "dailymotion.com",
    "streamable.com", "wistia.com", "wistia.net", "veed.io", "dropbox.com",
)
# Pages that hold videos but that yt-dlp cannot enumerate on its own.
# These get flagged for the browser pass instead of being silently dropped.
BROWSER_HOSTS = (
    "drive.google.com", "behance.net", "notion.site", "notion.so",
    "canva.com", "wix.site", "wixsite.com", "carrd.co", "framer.website",
    "myportfolio.com", "squarespace.com", "linktr.ee", "beacons.ai",
)
DEAD_HOSTS = ("linkedin.com", "upwork.com", "onlinejobs.ph", "mailto:")

URL_RE = re.compile(r"https?://[^\s<>\"'\)\]]+", re.I)
MEDIA_EXT = (".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi")


def classify(url: str) -> str:
    u = url.lower().rstrip(".,);]")
    if any(h in u for h in DEAD_HOSTS):
        return "ignore"
    if "loom.com" in u:
        return "loom"
    # A direct file link off someone's own domain or a CDN is the single most
    # common way a reel arrives, and no host list will ever cover it.
    if any(u.split("?")[0].endswith(e) for e in MEDIA_EXT):
        return "video"
    if "drive.google.com/file/" in u:
        return "video"          # yt-dlp handles a single Drive file
    if "drive.google.com/drive/folders" in u:
        return "browser"        # a folder has to be enumerated first
    if any(h in u for h in VIDEO_HOSTS):
        return "video"
    if any(h in u for h in BROWSER_HOSTS):
        return "browser"
    return "unknown"


def extract_links(applicant: dict) -> list:
    """Pull every URL out of whatever text fields the harvest produced."""
    blob = " ".join(
        str(applicant.get(k) or "")
        for k in ("cover_letter", "message", "body", "portfolio", "loom", "links", "raw_text")
    )
    found = [u.rstrip(".,);]'\"") for u in URL_RE.findall(blob)]
    for u in applicant.get("links") or []:
        if isinstance(u, str) and u.startswith("http"):
            found.append(u.rstrip(".,);]'\""))
    seen, out = set(), []
    for u in found:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


# ---------------------------------------------------------------- shell helpers

def run(cmd, timeout=900):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"
    except FileNotFoundError as e:
        return 127, "", str(e)


def probe_duration(path: Path) -> float:
    rc, out, _ = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(path)
    ], timeout=60)
    try:
        return float(out.strip())
    except (ValueError, AttributeError):
        return 0.0


# ---------------------------------------------------------------- download

def download(url: str, dest_dir: Path, kind: str) -> dict:
    """yt-dlp a single video. Returns a result dict; never raises."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    tmpl = str(dest_dir / "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp", "--no-playlist", "--no-warnings", "--quiet",
        "--max-filesize", "600M",
        "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
        "--merge-output-format", "mp4",
        "--write-auto-subs", "--write-subs", "--sub-langs", "en.*,en",
        "--sub-format", "vtt",
        "--convert-subs", "vtt",
        "-o", tmpl, url,
    ]
    rc, _, err = run(cmd, timeout=900)
    vids = sorted(
        [p for p in dest_dir.glob("*") if p.suffix.lower() in (".mp4", ".mkv", ".webm", ".mov")],
        key=lambda p: p.stat().st_mtime,
    )
    if not vids:
        return {"url": url, "kind": kind, "ok": False,
                "error": (err or "no file produced").strip()[-400:]}
    video = vids[-1]
    subs = sorted(dest_dir.glob("*.vtt"), key=lambda p: p.stat().st_mtime)
    return {
        "url": url, "kind": kind, "ok": True,
        "file": str(video),
        "duration": round(probe_duration(video), 2),
        "vtt": str(subs[-1]) if subs else None,
    }


# ---------------------------------------------------------------- frames

def measure_cuts(video: Path, duration: float, thresh: float = 0.28) -> dict:
    """Real cut timestamps. Counting extracted frames does not work because the
    frame extractor caps at 24, which silently turns a fast 300s reel into a
    fake 12s average. Pacing is 2.0 of the 10 points, so it gets measured."""
    rc, _, err = run(["ffmpeg", "-v", "info", "-i", str(video),
                      "-vf", f"select='gt(scene,{thresh})',showinfo",
                      "-f", "null", "-"], timeout=900)
    cuts = [round(float(m), 2) for m in re.findall(r"pts_time:([0-9.]+)", err)]
    marks = [0.0] + cuts + [duration]
    shots = [round(marks[i + 1] - marks[i], 2) for i in range(len(marks) - 1)]
    shots = [s for s in shots if s > 0.05]
    return {
        "cut_count": len(cuts),
        "cut_times": cuts[:120],
        "avg_shot": round(sum(shots) / len(shots), 2) if shots else None,
        "median_shot": round(sorted(shots)[len(shots) // 2], 2) if shots else None,
        "first_cut_at": cuts[0] if cuts else None,
    }


def frames_ad(video: Path, out_dir: Path, duration: float) -> list:
    """Hook-dense + scene-change. The first 3s get 4fps because that is where
    the rubric's craft points are actually won or lost."""
    out_dir.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
         "-t", "3", "-vf", "fps=4,scale=640:-2", "-frames:v", "12",
         str(out_dir / "hook_%02d.jpg")], timeout=300)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
         "-vf", "select='gt(scene,0.3)',scale=640:-2", "-fps_mode", "vfr",
         "-frames:v", "24", str(out_dir / "scene_%02d.jpg")], timeout=600)

    scenes = sorted(out_dir.glob("scene_*.jpg"))
    # Flat-graded or single-take footage defeats scene detection. Fall back to a
    # uniform sweep so a slow-cut ad is not scored on three frames.
    if len(scenes) < 4 and duration > 4:
        for p in scenes:
            p.unlink(missing_ok=True)
        step = max(duration / 14.0, 0.4)
        run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
             "-vf", f"fps=1/{step:.3f},scale=640:-2", "-frames:v", "14",
             str(out_dir / "scene_%02d.jpg")], timeout=600)
    return sorted(str(p) for p in out_dir.glob("*.jpg"))


def frames_loom(video: Path, out_dir: Path, duration: float) -> list:
    """Sparse. One frame per ~45s, capped at 12. Enough to tell a real screen
    share from a static slide, not enough to waste a context window on it."""
    out_dir.mkdir(parents=True, exist_ok=True)
    step = max(duration / 12.0, 45.0) if duration else 45.0
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
         "-vf", f"fps=1/{step:.3f},scale=640:-2", "-frames:v", "12",
         str(out_dir / "loom_%02d.jpg")], timeout=600)
    return sorted(str(p) for p in out_dir.glob("*.jpg"))


# ---------------------------------------------------------------- transcript

def vtt_to_text(vtt_path: Path) -> str:
    lines, seen = [], set()
    for raw in vtt_path.read_text(errors="ignore").splitlines():
        s = raw.strip()
        if not s or s.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        if "-->" in s:
            continue
        s = re.sub(r"<[^>]+>", "", s)
        if s and s not in seen:
            seen.add(s)
            lines.append(s)
    return " ".join(lines)


def elevenlabs_stt(video: Path, out_dir: Path) -> str:
    """Fallback transcript. Loom and self-hosted files rarely carry captions."""
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return ""
    audio = out_dir / "audio.mp3"
    rc, _, _ = run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
                    "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k",
                    str(audio)], timeout=600)
    if rc != 0 or not audio.exists() or audio.stat().st_size > 24 * 1024 * 1024:
        return ""
    boundary = "----claudeharvest"
    body = bytearray()

    def field(name, value):
        body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode())

    field("model_id", "scribe_v1")
    body.extend(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
        f"filename=\"audio.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n".encode()
    )
    body.extend(audio.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/speech-to-text",
        data=bytes(body),
        headers={"xi-api-key": key,
                 "Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read().decode()).get("text", "")
    except Exception:
        return ""
    finally:
        audio.unlink(missing_ok=True)


# ---------------------------------------------------------------- per applicant

def harvest_one(applicant: dict, run_dir: Path, max_videos: int) -> dict:
    aid = str(applicant.get("id") or applicant.get("name") or "unknown")
    # Name first: OnlineJobs ids are opaque hashes, and a media tree full of
    # dpw4qrwb/ is unreadable when the hiring manager wants to check by hand.
    label = f"{applicant.get('name') or ''}-{aid}".strip("-")
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:70] or "unknown"
    base = run_dir / "media" / slug
    base.mkdir(parents=True, exist_ok=True)

    links = extract_links(applicant)
    routed = [(u, classify(u)) for u in links]
    unknown = [u for u, k in routed if k == "unknown"]
    # An unrecognised host is usually the applicant's own portfolio site, which
    # is exactly where the work lives. Queue it for the browser rather than
    # letting it fall off the end of the run.
    needs_browser = [u for u, k in routed if k == "browser"] + unknown
    targets = [(u, k) for u, k in routed if k in ("loom", "video")]

    # Loom first: it is the one required deliverable and it carries the
    # instruction-compliance signal.
    targets.sort(key=lambda t: 0 if t[1] == "loom" else 1)
    targets = targets[: max_videos + 2]

    items, videos_done = [], 0
    for url, kind in targets:
        if videos_done >= max_videos:
            break
        vdir = base / f"v{videos_done + 1:02d}"
        res = download(url, vdir, kind)
        if not res["ok"]:
            items.append(res)
            continue
        video = Path(res["file"])
        fdir = vdir / "frames"
        profile = "loom" if kind == "loom" else "ad"
        res["profile"] = profile
        res["frames"] = (frames_loom(video, fdir, res["duration"]) if profile == "loom"
                         else frames_ad(video, fdir, res["duration"]))
        if profile == "ad":
            res["pacing"] = measure_cuts(video, res["duration"])

        text = ""
        if res.get("vtt"):
            text = vtt_to_text(Path(res["vtt"]))
        if len(text) < 80 and profile == "loom":
            text = elevenlabs_stt(video, vdir)
        if text:
            (vdir / "transcript.txt").write_text(text)
            res["transcript"] = str(vdir / "transcript.txt")
            res["transcript_chars"] = len(text)
        # The mp4 is the biggest thing on disk and the frames are what get read.
        # Keep Looms (re-watchable on a callback), drop ad sources.
        if profile == "ad":
            video.unlink(missing_ok=True)
            res["file"] = None
        items.append(res)
        videos_done += 1

    manifest = {
        "id": aid, "slug": slug,
        "name": applicant.get("name"),
        "links_found": links,
        "needs_browser": needs_browser,
        "unclassified": unknown,
        "media": items,
        "videos_ok": sum(1 for i in items if i.get("ok")),
        "videos_failed": [i["url"] for i in items if not i.get("ok")],
        "total_frames": sum(len(i.get("frames") or []) for i in items),
        "has_loom": any(i.get("profile") == "loom" and i.get("ok") for i in items),
    }
    (base / "media.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="run directory")
    ap.add_argument("--max-videos", type=int, default=5)
    ap.add_argument("--only", help="single applicant id, for re-runs")
    args = ap.parse_args()

    run_dir = Path(args.run).expanduser().resolve()
    src = run_dir / "applicants.json"
    if not src.exists():
        sys.exit(f"missing {src}, run the browser harvest step first")
    for tool in ("yt-dlp", "ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"missing required binary: {tool}")

    applicants = json.loads(src.read_text())
    if isinstance(applicants, dict):
        applicants = applicants.get("applicants", [])
    if args.only:
        applicants = [a for a in applicants if str(a.get("id")) == args.only]

    index = []
    for n, a in enumerate(applicants, 1):
        name = a.get("name") or a.get("id")
        print(f"[{n}/{len(applicants)}] {name}", flush=True)
        try:
            index.append(harvest_one(a, run_dir, args.max_videos))
        except Exception as e:  # one bad application must not kill the batch
            print(f"    ERROR {e}", file=sys.stderr)
            index.append({"id": a.get("id"), "name": name, "error": str(e),
                          "videos_ok": 0, "total_frames": 0})

    (run_dir / "media").mkdir(parents=True, exist_ok=True)
    (run_dir / "media" / "index.json").write_text(json.dumps(index, indent=2))
    ok = sum(1 for i in index if i.get("videos_ok"))
    print(f"\ndone, {ok}/{len(index)} applicants with playable media, "
          f"{sum(i.get('total_frames', 0) for i in index)} frames total")
    stuck = [i for i in index if i.get("needs_browser")]
    if stuck:
        print(f"{len(stuck)} applicants have links only the browser can open "
              f"(Drive folders, portfolio sites), see needs_browser in media/index.json")


if __name__ == "__main__":
    main()
