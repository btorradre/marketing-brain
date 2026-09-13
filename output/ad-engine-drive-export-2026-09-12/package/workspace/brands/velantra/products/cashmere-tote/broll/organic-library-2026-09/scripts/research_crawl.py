#!/usr/bin/env python3
"""Organic TikTok research crawl for the Colette wool tote B-roll library.
Commands: crawl | select | download | frames
Data lands in ../research/ (raw json, tiktok_reference_dataset.csv, videos/, frames/)."""
import csv, json, os, subprocess, sys, time, random
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "research")
RAW = os.path.join(RES, "raw"); VID = os.path.join(RES, "videos"); FRM = os.path.join(RES, "frames")
for d in (RAW, VID, FRM): os.makedirs(d, exist_ok=True)
ENV = {}
for l in open(os.path.expanduser("~/Documents/marketing brain/.env")):
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1); ENV[k] = v.strip().strip('"').strip("'")
TOK = ENV["APIFY_API_TOKEN"]
ACTOR = "clockworks~free-tiktok-scraper"

# Derived from the product's visual class: women's soft wool/felt east-west carry-all tote,
# leather trim, gold disc caps, no logo, fall/quiet-luxury register.
QUERIES = [
 "handbag", "leather handbag", "everyday handbag", "quiet luxury bag", "tote bag",
 "work tote bag", "tote bag outfit", "what's in my bag", "whats in my bag tote",
 "bag review", "handbag unboxing", "purse collection", "grwm handbag", "handbag styling",
 "bag close up", "bag details", "handbag recommendation", "fall bag", "fall handbag",
 "wool tote", "felt tote bag", "suede tote bag", "big tote bag", "everything bag",
 "carry all tote", "old money bag", "loro piana tote", "bag haul", "new bag",
 "bag that fits laptop", "mom bag tote", "airport tote bag", "packing my bag",
 "bag in car", "mirror outfit check bag", "cafe tote bag", "shoulder tote outfit",
 "designer inspired bag", "purse", "handbag outfit",
]
PER_QUERY = 40

def start_run(queries):
    payload = {"searchQueries": queries, "resultsPerPage": PER_QUERY, "searchSection": "/video",
               "shouldDownloadVideos": False, "shouldDownloadCovers": False}
    r = requests.post(f"https://api.apify.com/v2/acts/{ACTOR}/runs?token=[REDACTED_SECRET]", json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["data"]["id"]

def wait_run(run_id):
    while True:
        d = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}?token=[REDACTED_SECRET]", timeout=60).json()["data"]
        if d["status"] in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            return d
        time.sleep(15)

def fetch_items(dataset_id):
    items, offset = [], 0
    while True:
        r = requests.get(f"https://api.apify.com/v2/datasets/{dataset_id}/items?token=[REDACTED_SECRET]&offset={offset}&limit=1000", timeout=120)
        r.raise_for_status(); batch = r.json()
        items += batch
        if len(batch) < 1000: return items
        offset += 1000

def cmd_crawl():
    chunks = [QUERIES[i:i+5] for i in range(0, len(QUERIES), 5)]
    allitems = []
    def one(ch):
        rid = start_run(ch); print("started", rid, ch, flush=True)
        d = wait_run(rid); print("finished", rid, d["status"], flush=True)
        items = fetch_items(d["defaultDatasetId"])
        json.dump(items, open(os.path.join(RAW, f"run_{rid}.json"), "w"))
        return items
    with ThreadPoolExecutor(max_workers=4) as ex:
        for f in as_completed([ex.submit(one, c) for c in chunks]):
            try: allitems += f.result()
            except Exception as e: print("chunk failed", e, flush=True)
    seen, rows = set(), []
    for it in allitems:
        vid = str(it.get("id") or ""); 
        if not vid or vid in seen: continue
        seen.add(vid)
        vm = it.get("videoMeta") or {}; am = it.get("authorMeta") or {}
        rows.append({
            "video_id": vid, "url": it.get("webVideoUrl"), "creator": am.get("name"), "creator_nick": am.get("nickName"),
            "caption": (it.get("text") or "").replace("\n", " ")[:600],
            "hashtags": " ".join("#" + h.get("name", "") for h in (it.get("hashtags") or [])),
            "views": it.get("playCount"), "likes": it.get("diggCount"), "comments": it.get("commentCount"),
            "shares": it.get("shareCount"), "duration_s": vm.get("duration"), "published": it.get("createTimeISO"),
            "thumbnail": vm.get("coverUrl"), "media_url": (it.get("mediaUrls") or [None])[0],
            "search_query": it.get("searchQuery"), "is_ad": it.get("isAd"), "is_slideshow": it.get("isSlideshow"),
            "width": vm.get("width"), "height": vm.get("height"),
        })
    with open(os.path.join(RES, "tiktok_reference_dataset.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"dataset: {len(allitems)} raw, {len(rows)} unique videos")

def load_rows():
    return list(csv.DictReader(open(os.path.join(RES, "tiktok_reference_dataset.csv"))))

def cmd_select(target=180):
    rows = load_rows(); random.seed(7)
    ok = [r for r in rows if r["is_ad"] != "True" and r["is_slideshow"] != "True"
          and r["duration_s"] and 4 <= float(r["duration_s"]) <= 120 and r["url"]]
    byq = {}
    for r in ok: byq.setdefault(r["search_query"], []).append(r)
    picks, seen = [], set()
    # round robin over queries, each query sorted by views desc but with light shuffle so we don't only get virals
    lists = []
    for q, lst in byq.items():
        lst.sort(key=lambda r: -int(float(r["views"] or 0)))
        top = lst[:12]; rest = lst[12:]; random.shuffle(rest)
        lists.append(top + rest)
    i = 0
    while len(picks) < target and any(lists):
        for lst in lists:
            if lst and len(picks) < target:
                r = lst.pop(0)
                if r["video_id"] not in seen:
                    seen.add(r["video_id"]); picks.append(r)
        i += 1
        if i > 100: break
    json.dump(picks, open(os.path.join(RES, "download_selection.json"), "w"), indent=1)
    print(f"selected {len(picks)} of {len(ok)} eligible ({len(rows)} total)")

def dl(r):
    out = os.path.join(VID, f"{r['video_id']}.mp4")
    if os.path.exists(out) and os.path.getsize(out) > 50000: return r["video_id"], True
    cmd = ["yt-dlp", "-q", "--no-warnings", "-f", "mp4/bv*+ba/b", "--no-playlist", "-o", out, r["url"]]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        return r["video_id"], p.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 50000
    except subprocess.TimeoutExpired:
        return r["video_id"], False

def cmd_download():
    picks = json.load(open(os.path.join(RES, "download_selection.json")))
    n_ok = 0
    with ThreadPoolExecutor(max_workers=4) as ex:
        for f in as_completed([ex.submit(dl, r) for r in picks]):
            vid, ok = f.result(); n_ok += ok
            print(vid, "ok" if ok else "FAIL", flush=True)
    print(f"downloaded {n_ok}/{len(picks)}")

def cmd_frames():
    """6-frame contact sheet per video (3x2), for the human-eye pattern pass."""
    for fn in sorted(os.listdir(VID)):
        if not fn.endswith(".mp4"): continue
        vid = fn[:-4]; out = os.path.join(FRM, f"{vid}.jpg")
        if os.path.exists(out): continue
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(VID, fn)], capture_output=True, text=True).stdout.strip() or 0)
        if dur <= 0: continue
        step = max(dur / 6.5, 0.3)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(VID, fn), "-vf",
                        f"fps=1/{step:.3f},scale=270:-2,tile=3x2", "-frames:v", "1", "-q:v", "4", out])
    print("frames done")

if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "crawl"
    {"crawl": cmd_crawl, "select": cmd_select, "download": cmd_download, "frames": cmd_frames}[c]()
