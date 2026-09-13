#!/usr/bin/env python3
"""VEL-MARGOT-BEST-01 — talking-head PIP chain via Seedance 2.0 on kie.ai.

  avatar_chain.py run       generate all segments sequentially (last-frame chained)
  avatar_chain.py stitch    concat segments -> take-1.mp4 (native audio kept for
                            reference) + take-1-vo.mp4 (audio replaced with the
                            seamless ElevenLabs VO, the shipping audio law)
  avatar_chain.py status

Why this shape: Higgsfield session is expired (interactive re-auth), so the
skill's --audio lip-sync path is unavailable. kie Seedance cannot take
first_frame_url AND reference_audio_urls together (HTTP 422). So each segment
carries its chunk's dialogue in the prompt — Seedance mouths the actual words —
and the per-clip audio is dropped at stitch, replaced by the ONE seamless
ElevenLabs track (feedback_vo_single_seamless_cut). At PIP cutout scale the
approximate sync reads like every screen-recorded reaction PIP on IG.
If hard lip-sync is wanted: `hf auth login`, then re-run via aiugc-longform's
render_segment.sh with --audio per chunk.

Sequential by necessity (chaining) — expect 40-70 min with top-up waits.
"""
import json, os, re, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
AV = os.path.join(ASSETS, "avatars")
STATE_PATH = os.path.join(HERE, "avatar_state.json")
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
VID_MODEL = "bytedance/seedance-2"          # std only
REF = os.path.join(AV, "creator-ref.png")
SCRIPT = os.path.normpath(os.path.join(HERE, "..", "VEL-MARGOT-BEST-01-VO-script.txt"))
KEY = None

MAX_WORDS = 30          # per segment; ~10s at the fast-creator read
DUR = 10


def chunks():
    text = re.sub(r"\s+", " ", open(SCRIPT).read()).strip()
    sents = re.split(r"(?<=[.?!]) ", text)
    out, cur = [], ""
    for s in sents:
        cand = (cur + " " + s).strip()
        if cur and len(cand.split()) > MAX_WORDS:
            out.append(cur)
            cur = s
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


def seg_prompt(line):
    return (
        "UGC iPhone selfie video, handheld with subtle natural sway, real-time pacing. The same woman as the "
        "reference image, exact same face, hair, cream linen shirt and bright kitchen, no setting change, no "
        "face morphing. She is mid conversation, talking animatedly straight into the front camera like "
        "FaceTiming her best friend about bags she tested, natural hand gestures, expressive intonation, "
        "energy holds through the final word, never monotone. She says: \"" + line + "\" No other people. "
        "No cuts. No zooms. No music. No text overlays. Vertical 9:16. ONE CONTINUOUS SHOT.")


def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def load_key():
    global KEY
    for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if line.startswith("KIE_API_KEY="):
            KEY = line.strip().split("=", 1)[1]
    assert KEY, "KIE_API_KEY not found"


def credits():
    req = urllib.request.Request("https://api.kie.ai/api/v1/chat/credit",
                                 headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, context=ctx(), timeout=60) as r:
        return json.loads(r.read().decode(), strict=False).get("data")


def state():
    return json.load(open(STATE_PATH)) if os.path.exists(STATE_PATH) else {"uploads": {}, "segs": {}}


def save(st):
    json.dump(st, open(STATE_PATH, "w"), indent=1)


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        return json.loads(r.read().decode(), strict=False)


def upload_file(path):
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(10 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_URL,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=velantra-margot-best1",
             "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            last = out.stdout or out.stderr
            continue
        if resp.get("data", {}).get("downloadUrl"):
            return resp["data"]["downloadUrl"]
        last = out.stdout
    raise RuntimeError(f"upload failed for {path}: {last[:300]}")


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out = subprocess.run(["curl", "-sL", "--fail", "-A", "Mozilla/5.0", "-o", dest, url],
                         capture_output=True, text=True)
    if out.returncode != 0 or not os.path.getsize(dest):
        raise RuntimeError(f"download failed for {url}")


def wait_task(task_id, timeout_s=40 * 60):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        d = (api(f"/recordInfo?taskId={task_id}").get("data") or {})
        if d.get("state") == "success":
            res = json.loads(d.get("resultJson") or "{}", strict=False)
            urls = res.get("resultUrls") or []
            return urls[0] if urls else None
        if d.get("state") == "fail":
            raise RuntimeError(f"task {task_id} failed: {d.get('failMsg')}")
        time.sleep(15)
    raise RuntimeError(f"task {task_id} timed out")


def last_frame(mp4, png):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.25", "-i", mp4,
                    "-frames:v", "1", png], check=True)


def cmd_run():
    st = state()
    lines = chunks()
    print(f"{len(lines)} segments x {DUR}s")
    if not st["uploads"].get("ref"):
        st["uploads"]["ref"] = upload_file(REF)
        save(st)
    seed_url = st["uploads"]["ref"]
    RE_ANCHOR_FROM = 7      # chained last frames accumulate compression noise by
    # mid-chain; from here every segment re-anchors to the ORIGINAL creator ref.
    # Pose jumps between segments are fine: the PIP crop repositions every beat.
    for i, line in enumerate(lines, 1):
        sid = f"seg_{i:02d}"
        if i >= RE_ANCHOR_FROM:
            seed_url = st["uploads"]["ref"]
        dest = os.path.join(AV, "segments", f"{sid}.mp4")
        rec = st["segs"].get(sid, {})
        # Brooks pulls finished segments into his edit mid-run — a recorded
        # success with a cached last-frame upload counts as done even if the
        # local file is gone. Never regenerate what he already took.
        if rec.get("state") == "success" and st["uploads"].get(f"lf::{sid}"):
            print(f"{sid}: recorded success, seeding from cached last frame")
            seed_url = st["uploads"][f"lf::{sid}"]
            continue
        if os.path.exists(dest):
            print(f"{sid}: exists, skipping")
            fp = os.path.join(AV, "segments", f"{sid}_last.png")
            if not os.path.exists(fp):
                last_frame(dest, fp)
            key = f"lf::{sid}"
            if not st["uploads"].get(key):
                st["uploads"][key] = upload_file(fp)
                save(st)
            seed_url = st["uploads"][key]
            continue
        if rec.get("taskId") and rec.get("state") not in ("success", "fail"):
            # a task from a prior run may have finished after our poll timed out
            d = (api(f"/recordInfo?taskId={rec['taskId']}").get("data") or {})
            if d.get("state") == "success":
                res = json.loads(d.get("resultJson") or "{}", strict=False)
                urls = res.get("resultUrls") or []
                if urls:
                    download(urls[0], dest)
                    rec["state"] = "success"
                    save(st)
                    fp = os.path.join(AV, "segments", f"{sid}_last.png")
                    last_frame(dest, fp)
                    st["uploads"][f"lf::{sid}"] = upload_file(fp)
                    save(st)
                    seed_url = st["uploads"][f"lf::{sid}"]
                    print(f"{sid}: prior task finished, downloaded -> {dest}")
                    continue
        # Auto-top-up stalls for long stretches. Size each segment to what the
        # balance can pre-authorise (130 cr/s), floor 5s, cap DUR. Wait only if
        # even 5s does not fit.
        waited = 0
        while credits() < 130 * 5:
            print(f"balance {credits()} < {130 * 5} (5s floor), waiting 120s for top-up...")
            time.sleep(120)
            waited += 120
        dur = max(5, min(DUR, int(credits() // 130)))
        print(f"{sid}: balance {credits()} -> duration {dur}s")
        payload = {"model": VID_MODEL, "input": {
            "prompt": seg_prompt(line),
            "first_frame_url": seed_url,
            "aspect_ratio": "9:16",
            "resolution": "720p",
            "duration": dur,
            "generate_audio": True}}
        # Moderation sometimes false-positives the real-footage ref frame
        # ("may contain real person"). Retry once, then fall back to the
        # previous successful segment's GENERATED last frame.
        url = None
        for attempt in range(3):
            if attempt == 2:
                prev_lfs = [st["uploads"][k] for k in sorted(st["uploads"]) if k.startswith("lf::seg_")]
                if prev_lfs:
                    payload["input"]["first_frame_url"] = prev_lfs[-1]
                    print(f"{sid}: falling back to previous segment's last frame as seed")
            r = api("/createTask", payload)
            if r.get("code") != 200:
                raise RuntimeError(f"{sid} CREATE FAIL: {r}")
            tid = r["data"]["taskId"]
            st["segs"][sid] = {"taskId": tid, "state": "created", "line": line}
            save(st)
            print(f"{sid} task {tid} ({len(line.split())}w, attempt {attempt + 1})")
            try:
                url = wait_task(tid)
                break
            except RuntimeError as e:
                if "real person" in str(e) and attempt < 2:
                    print(f"{sid}: moderation false-positive, retrying ({e})")
                    continue
                raise
        download(url, dest)
        st["segs"][sid]["state"] = "success"
        save(st)
        fp = os.path.join(AV, "segments", f"{sid}_last.png")
        last_frame(dest, fp)
        st["uploads"][f"lf::{sid}"] = upload_file(fp)
        save(st)
        seed_url = st["uploads"][f"lf::{sid}"]
        print(f"{sid} DONE -> {dest}")
    print("ALL SEGMENTS DONE")


def cmd_stitch():
    segs = sorted(f for f in os.listdir(os.path.join(AV, "segments")) if re.match(r"seg_\d+\.mp4$", f))
    lst = os.path.join(HERE, "avatar_concat.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.join(AV, 'segments', s)}'\n")
    raw = os.path.join(AV, "take-1.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", raw], check=True)
    vo = os.path.join(ASSETS, "vo", "VEL-MARGOT-BEST-01-vo-full.mp3")
    out = os.path.join(AV, "take-1-vo.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-i", vo,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", out], check=True)
    print(f"stitched {len(segs)} segs -> {raw} and {out}")


def cmd_status():
    st = state()
    print(f"credits: {credits()}")
    for sid, rec in sorted(st["segs"].items()):
        print(f"  {sid}: {rec.get('state')}")


if __name__ == "__main__":
    load_key()
    {"run": cmd_run, "stitch": cmd_stitch, "status": cmd_status}.get(
        sys.argv[1] if len(sys.argv) > 1 else "status", cmd_status)()
