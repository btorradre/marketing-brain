#!/usr/bin/env python3
"""Standalone keyframe fixer — regenerates ONE keyframe WITHOUT touching state.json.

Usage: python3 qa_fix.py FILM K_INDEX

Composes the prompt from the current orchestrate.py spec (so it picks up any
mechanism-block edits), uploads refs fresh under a separate upload path, creates
a GPT Image 2 task, polls, downloads over the old K<idx>.png, and re-crops the
9:16 frame. Safe to run while the main orchestrator is generating videos —
no shared state is read or written.

NOTE for the video stage: after fixing a keyframe, the main state.json still
holds the OLD upload URL for its -916 crop and possibly an old seg task. Before
re-running `orchestrate.py videos <FILM>` for the affected segment, delete the
seg mp4 AND pop both state["tasks"]["<FILM>_S<idx>"] and
state["uploads"]["<abs path to K<idx>-916.png>"] (only when the main run is idle).
"""
import json, os, subprocess, sys, time
import orchestrate as o


def upload(path, key):
    for attempt in range(4):
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", o.UPLOAD_API,
             "-H", f"Authorization: Bearer {key}",
             "-F", f"file=@{path}", "-F", "uploadPath=velantra-clay-qa",
             "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try:
            r = json.loads(out.stdout)
        except ValueError:
            time.sleep(20); continue
        u = r.get("data", {}).get("downloadUrl")
        if u:
            return u
        time.sleep(20)
    sys.exit("upload failed " + path)


def fix_seg(film_name, idx):
    key = o.env_key()
    film = o.F[film_name]
    flags = film["kf"][idx - 1][1]
    has_bag = "styleonly" not in flags
    prompt = o.compose_seg(film, film["seg"][idx - 1], has_bag, "forming" in flags)
    kf = os.path.join(o.CAMP, film["dir"], "keyframes", f"K{idx}-916.png")
    url = upload(kf, key)
    resp = o.api("POST", f"{o.API}/jobs/createTask", key,
                 {"model": o.VID_MODEL, "input": {
                     "prompt": prompt, "first_frame_url": url,
                     "aspect_ratio": "9:16", "resolution": "720p",
                     "duration": 5, "generate_audio": True}})
    if resp.get("code") != 200:
        sys.exit(f"createTask failed: {resp}")
    tid = resp["data"]["taskId"]
    print("task", tid, flush=True)
    while True:
        d = o.api("GET", f"{o.API}/jobs/recordInfo?taskId={tid}", key).get("data", {})
        if d.get("state") == "success":
            res = json.loads(d.get("resultJson") or "{}", strict=False)
            break
        if d.get("state") == "fail":
            sys.exit(f"FAILED {d.get('failCode')} {d.get('failMsg')}")
        time.sleep(15)
    dest = os.path.join(o.CAMP, film["dir"], "output", f"seg_{idx:02d}.mp4")
    o.download(res["resultUrls"][0], dest)
    print("done", dest, f"({d.get('creditsConsumed')} cr)")


def main():
    if sys.argv[1] == "seg":
        fix_seg(sys.argv[2].upper(), int(sys.argv[3]))
        return
    film_name, idx = sys.argv[1].upper(), int(sys.argv[2])
    key = o.env_key()
    film = o.F[film_name]
    refs, flags, scene = film["kf"][idx - 1]
    has_bag = "styleonly" not in flags
    prompt = o.compose_kf(film, scene, flags, has_bag)
    urls = [upload(r, key) for r in refs]
    resp = o.api("POST", f"{o.API}/jobs/createTask", key,
                 {"model": o.IMG_MODEL, "input": {
                     "prompt": prompt, "input_urls": urls,
                     "aspect_ratio": "2:3", "resolution": "2K"}})
    if resp.get("code") != 200:
        sys.exit(f"createTask failed: {resp}")
    tid = resp["data"]["taskId"]
    print("task", tid, flush=True)
    while True:
        d = o.api("GET", f"{o.API}/jobs/recordInfo?taskId={tid}", key).get("data", {})
        if d.get("state") == "success":
            res = json.loads(d.get("resultJson") or "{}", strict=False)
            break
        if d.get("state") == "fail":
            sys.exit(f"FAILED {d.get('failCode')} {d.get('failMsg')}")
        time.sleep(12)
    dest = os.path.join(o.CAMP, film["dir"], "keyframes", f"K{idx}.png")
    o.download(res["resultUrls"][0], dest)
    o.crop_916(dest, dest.replace(".png", "-916.png"))
    print("done", dest, f"({d.get('creditsConsumed')} cr)")


if __name__ == "__main__":
    main()
