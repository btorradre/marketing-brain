#!/usr/bin/env python3
"""Delphine b-roll v4 — Omni animation for the real-seed rebuild (board: delphine-broll-v4-rebuild).

    python3 animate_v4.py run     # launch everything missing, then poll until done

Same Omni engine and motion constants as build_library.py / scenes_delphine.py.
Constant-distance motions ONLY — push-ins inflate the 25cm bag (see README).
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
STILLS = os.path.join(HERE, "stills")
CLIPS = os.path.join(HERE, "clips")
STATE = os.path.join(HERE, "_library", "state_v4.json")
os.makedirs(os.path.dirname(STATE), exist_ok=True)

GEM_KEY = next(l.split("=", 1)[1].strip().strip('"').strip("'")
               for l in open(os.path.join(VAULT, ".env")) if l.startswith("GEMINI_API_KEY="))
OMNI = "https://generativelanguage.googleapis.com/v1beta/interactions"

sys.path.insert(0, HERE)
from scenes_delphine import HOLD, DRIFT, OVERHEAD, WALK_AWAY, WALK_BY, CARRY, MACRO, HANDS

MOTIONS = {
    "p1-street-walkaway": WALK_AWAY, "p2-chair-seat": HOLD, "p3-bench-coffee": HOLD,
    "p4-ag-table-control": HOLD, "p5-grab-off-chair": HANDS, "p6-mirror-check": CARRY,
    "002r-street-coffee-crossing-DC": WALK_BY, "003-street-crossing-brick-LC": WALK_BY,
    "004-street-walkaway-cars-DC": WALK_AWAY, "005-street-crouch-curb-LC": HANDS,
    "006r-street-brickdrive-AG": WALK_BY, "007r-street-coffee-car-LC": CARRY,
    "008-street-friends-LC": WALK_AWAY, "009-street-trench-DC": WALK_AWAY,
    "010-street-shopfront-AG": CARRY, "011-checkout-counter-DC": CARRY,
    "012-street-cafedoor-LC": WALK_BY, "013-cafe-window-table-LC": HOLD,
    "014-cafe-window-angle-DC": DRIFT, "015-cafe-icedcoffees-AG": HOLD,
    "016-checkout-window-LC": DRIFT, "021-car-lipstick-LC": HANDS,
    "022-car-dooropen-DC": CARRY, "023-car-stepping-LC": CARRY,
    "024-car-seat-pouch-AG": HANDS, "027-home-table-side-AG": DRIFT,
    "028-home-turnlock-hand-AG": HANDS, "030r-home-bag-couch-LC": HOLD,
    "031-home-chair-wide-LC": DRIFT, "032r-home-counter-pouch-LC": HANDS,
    "033-home-counter-close-DC": HANDS, "034r-home-strap-fasten-LC": HANDS,
    "035-home-lipoil-AG": HANDS, "038-chair-items-pack-LC": HOLD,
    "039r-chair-pouch-in-LC": HANDS, "040-bench-hands-open-LC": HANDS,
    "042-open-topdown-AG": OVERHEAD, "043-open-couch-interior-LC": HOLD,
    "046-flatlay-fur-LC": OVERHEAD, "047-flatlay-fur-DC": OVERHEAD,
    "049-macro-side-buckle-AG": MACRO, "050-macro-turnlock-AG": MACRO,
    "051-macro-feet-AG": MACRO, "052-macro-leather-grain-LC": MACRO,
    "053-macro-canvas-seam-AG": MACRO, "054-macro-handle-base-LC": MACRO,
    "055-macro-clochette-AG": MACRO, "056-macro-corner-feet-AG": MACRO,
    "058-street-curb-pickup-DC": HANDS,
}


def curl_json(args, timeout=300):
    out = subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout
    try:
        return json.loads(out)
    except Exception:
        return {"_raw": out[:300]}


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}


def save_state(s):
    json.dump(s, open(STATE, "w"), indent=1)


def launch():
    st = load_state()
    for f in sorted(os.listdir(STILLS)):
        if not f.endswith(".png"):
            continue
        key = f[:-4]
        if key in st or os.path.exists(os.path.join(CLIPS, key + ".mp4")):
            continue
        if key not in MOTIONS:
            print(f"no motion for {key}", flush=True); continue
        payload = {"model": "models/gemini-omni-flash-preview",
                   "input": [{"type": "image",
                              "data": base64.b64encode(open(os.path.join(STILLS, f), "rb").read()).decode(),
                              "mime_type": "image/png"},
                             {"type": "text",
                              "text": MOTIONS[key] + " No people speaking, natural ambient sound only. "
                                                     "Vertical 9:16."}],
                   "background": True, "generation_config": {"video_config": {}}}
        p = os.path.join(HERE, "_library", ".payload_v4.json")
        open(p, "w").write(json.dumps(payload))
        d = curl_json(["curl", "-s", "-X", "POST", f"{OMNI}?key={GEM_KEY}",
                       "-H", "Content-Type: application/json", "--data-binary", f"@{p}"])
        if "id" in d:
            st[key] = d["id"]; print(f"launched {key}", flush=True)
        else:
            print(f"LAUNCH FAILED {key}: {json.dumps(d)[:160]}", flush=True)
        save_state(st); time.sleep(1)


def poll_once():
    st = load_state(); done = pend = failed = 0
    for key, iid in st.items():
        out = os.path.join(CLIPS, key + ".mp4")
        if os.path.exists(out) and os.path.getsize(out) > 100_000:
            done += 1; continue
        d = curl_json(["curl", "-s", f"{OMNI}/{iid}?key={GEM_KEY}"])
        if d.get("status") == "completed":
            vid = None
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video":
                        vid = c.get("data")
            if vid:
                open(out, "wb").write(base64.b64decode(vid)); done += 1
                print(f"landed {key}", flush=True)
        elif d.get("status") in ("failed", "error"):
            failed += 1; print(f"FAILED {key}", flush=True)
        else:
            pend += 1
    print(f"[poll] {done} landed, {pend} pending, {failed} failed", flush=True)
    return pend


def drift_qa():
    """First-vs-last frame edge-energy check: all-negative deltas = locked-off law held."""
    qa = os.path.join(HERE, "_library", "qa_v4"); os.makedirs(qa, exist_ok=True)
    report = []
    for f in sorted(os.listdir(CLIPS)):
        if not f.endswith(".mp4"):
            continue
        k = f[:-4]
        a = os.path.join(qa, k + "-first.jpg"); b = os.path.join(qa, k + "-last.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(CLIPS, f),
                        "-vf", "select=eq(n\\,0)", "-frames:v", "1", a])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.5",
                        "-i", os.path.join(CLIPS, f), "-frames:v", "1", b])
        try:
            from PIL import Image, ImageFilter
            import statistics
            def energy(p):
                im = Image.open(p).convert("L").resize((256, 455)).filter(ImageFilter.FIND_EDGES)
                px = list(im.getdata()); return statistics.mean(px)
            d = energy(b) - energy(a)
            report.append((k, round(d, 2)))
        except Exception as e:
            report.append((k, f"err {e}"))
    open(os.path.join(qa, "drift_report.txt"), "w").write(
        "\n".join(f"{k}\t{v}" for k, v in report))
    inflated = [k for k, v in report if isinstance(v, float) and v > 8]
    print(f"[drift] {len(report)} clips checked, suspect push-in: {inflated or 'none'}", flush=True)


if __name__ == "__main__":
    launch()
    while True:
        time.sleep(90)
        # re-launch anything that failed at launch time, then poll
        launch()
        if poll_once() == 0:
            break
    drift_qa()
    n = len([f for f in os.listdir(CLIPS) if f.endswith('.mp4')])
    print(f"DONE: {n} clips in clips/", flush=True)
