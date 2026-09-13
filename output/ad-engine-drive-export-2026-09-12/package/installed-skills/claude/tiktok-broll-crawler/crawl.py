#!/usr/bin/env python3
"""
TikTok B-Roll Crawler
=====================
Adapted from the vendored DAN3002/Tiktok-Crawler (crawler/), rebuilt as a
CLI slot-based sourcing tool. Reads a sourcing_plan.json (one "slot" per
script line / beat that needs B-roll), crawls TikTok per slot via TikTokApi
(hashtag / sound / user), downloads candidate videos, and writes metadata
for the Gemini analysis gate (analyze.py).

Modes:
  plan     — crawl every slot in a sourcing_plan.json          (default)
  hashtag  — one-off: crawl hashtags   --keys bloating,guthealth
  sound    — one-off: crawl a sound id --keys 7405366156447501057
  user     — one-off: crawl a username --keys somecreator
  urls     — download explicit TikTok URLs via yt-dlp (no API/MS_TOKEN
             needed; use for Apify-sourced or hand-picked URLs)

Usage:
  venv/bin/python crawl.py --plan sourcing_plan.json --output ./job-dir
  venv/bin/python crawl.py --mode hashtag --keys bloating,bloatedstomach \
      --count 10 --output ./job-dir --slot S01
  venv/bin/python crawl.py --mode urls --url-file urls.txt --output ./job-dir --slot S01

MS_TOKEN is read from env or from the marketing brain .env. Without it,
TikTokApi may still work but gets blocked more often — the skill's Apify
fallback (see SKILL.md) covers that case via `--mode urls`.
"""

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

VAULT_ENV = os.path.expanduser("~/Documents/marketing brain/.env")


def load_env_file(path):
    if not os.path.exists(path):
        return
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


load_env_file(VAULT_ENV)
MS_TOKEN = os.environ.get("MS_TOKEN") or None


def ensure_ms_token():
    """Harvest an anonymous msToken via get_ms_token.py if none is configured."""
    global MS_TOKEN
    if MS_TOKEN:
        return MS_TOKEN
    here = os.path.dirname(os.path.abspath(__file__))
    print("  [i] No MS_TOKEN set — harvesting anonymous msToken from tiktok.com...")
    try:
        r = subprocess.run(
            [os.path.join(here, "venv", "bin", "python"),
             os.path.join(here, "get_ms_token.py"), "--browser", "webkit"],
            capture_output=True, text=True, timeout=120,
        )
        for line in r.stdout.splitlines():
            if line.startswith("MS_TOKEN="):
                MS_TOKEN = line.split("=", 1)[1].strip()
                print("  [i] harvested msToken OK")
                return MS_TOKEN
    except Exception:
        pass
    print("  [!] msToken harvest failed — trying without (may be blocked)")
    return None
YTDLP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "yt-dlp")
if not os.path.exists(YTDLP):
    YTDLP = "yt-dlp"


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

def video_meta(v_dict):
    stats = v_dict.get("stats", {}) or {}
    author = v_dict.get("author", {}) or {}
    return {
        "video_id": str(v_dict.get("id", "")),
        "desc": v_dict.get("desc", ""),
        "author": author.get("uniqueId", ""),
        "author_name": author.get("nickname", ""),
        "duration_s": (v_dict.get("video", {}) or {}).get("duration", 0),
        "create_time": v_dict.get("createTime", 0),
        "plays": stats.get("playCount", 0),
        "likes": stats.get("diggCount", 0),
        "url": f"https://www.tiktok.com/@{author.get('uniqueId','_')}/video/{v_dict.get('id','')}",
    }


def append_meta(meta_path, record):
    with open(meta_path, "a") as f:
        f.write(json.dumps(record) + "\n")


def already_have(slot_dir):
    return {p.stem for p in Path(slot_dir).glob("*.mp4")}


# ---------------------------------------------------------------------------
# yt-dlp download (robust path — works watermark-free for most videos)
# ---------------------------------------------------------------------------

def ytdlp_download(url, out_path):
    cmd = [
        YTDLP, "-q", "--no-warnings",
        "-f", "mp4/bv*+ba/b",
        "--no-playlist",
        "-o", out_path,
        url,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        return r.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 50_000
    except subprocess.TimeoutExpired:
        return False


# ---------------------------------------------------------------------------
# TikTokApi crawl (hashtag / sound / user)
# ---------------------------------------------------------------------------

async def crawl_slot(mode, keys, count, slot_dir, meta_path, min_dur, max_dur):
    from TikTokApi import TikTokApi

    ensure_ms_token()
    os.makedirs(slot_dir, exist_ok=True)
    have = already_have(slot_dir)
    saved = 0

    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[MS_TOKEN] if MS_TOKEN else None,
            num_sessions=1,
            sleep_after=3,
            browser=os.environ.get("TIKTOK_BROWSER", "webkit"),
            headless=os.environ.get("TIKTOK_HEADLESS", "0") == "1",
        )

        for key in keys:
            print(f"  [{mode}] {key}: fetching up to {count} candidates...")
            try:
                if mode == "hashtag":
                    gen = api.hashtag(name=key).videos(count=count)
                elif mode == "sound":
                    gen = api.sound(id=key).videos(count=count)
                elif mode == "user":
                    gen = api.user(username=key).videos(count=count)
                else:
                    raise ValueError(f"bad mode {mode}")

                got_for_key = 0
                async for video in gen:
                    if got_for_key >= count:
                        break
                    meta = video_meta(video.as_dict)
                    vid = meta["video_id"]
                    if not vid or vid in have:
                        continue
                    dur = meta["duration_s"]
                    if dur and (dur < min_dur or dur > max_dur):
                        continue

                    out_path = os.path.join(slot_dir, f"{vid}.mp4")
                    ok = False
                    # Primary: TikTokApi bytes (same as vendored crawler)
                    try:
                        video_bytes = await video.bytes()
                        if video_bytes and len(video_bytes) > 50_000:
                            with open(out_path, "wb") as f:
                                f.write(video_bytes)
                            ok = True
                    except Exception:
                        ok = False
                    # Fallback: yt-dlp on the canonical URL
                    if not ok:
                        ok = ytdlp_download(meta["url"], out_path)

                    if ok:
                        meta["file"] = out_path
                        meta["source_key"] = key
                        append_meta(meta_path, meta)
                        have.add(vid)
                        got_for_key += 1
                        saved += 1
                        print(f"    saved {vid} ({meta['duration_s']}s, {meta['plays']} plays)")
                        await asyncio.sleep(1)
                    else:
                        print(f"    FAILED download {vid}")
            except Exception as e:
                print(f"  [!] {mode} '{key}' failed: {type(e).__name__}: {e}")
    return saved


# ---------------------------------------------------------------------------
# Apify engine (clockworks/free-tiktok-scraper) — discovery without MS_TOKEN
# ---------------------------------------------------------------------------

APIFY_ACTOR = os.environ.get("APIFY_TIKTOK_ACTOR", "clockworks~free-tiktok-scraper")


def _apify_run(mode, keys, count):
    import requests

    token = os.environ.get("APIFY_API_TOKEN")
    payload = {"resultsPerPage": count}
    if mode == "hashtag":
        payload["hashtags"] = keys
    elif mode == "search":
        payload["searchQueries"] = keys
        payload["searchSection"] = "/video"
    elif mode == "user":
        payload["profiles"] = keys
    else:
        raise ValueError(f"apify engine does not support mode '{mode}'")
    url = (f"https://api.apify.com/v2/acts/{APIFY_ACTOR}/"
           f"run-sync-get-dataset-items?token=[REDACTED_SECRET]&timeout=280")
    r = requests.post(url, json=payload, timeout=320)
    r.raise_for_status()
    return r.json()


def apify_discover(mode, keys, count, min_dur, max_dur, chunk_size=4, workers=3):
    """Search TikTok via Apify. mode: hashtag | search | user. Returns meta list.
    Keys are chunked into separate parallel runs so no single run hits the
    sync-endpoint timeout."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    if not os.environ.get("APIFY_API_TOKEN"):
        print("  [!] APIFY_API_TOKEN not set — cannot use apify engine")
        return []
    chunks = [keys[i:i + chunk_size] for i in range(0, len(keys), chunk_size)]
    print(f"  [apify] {mode}: {len(keys)} terms in {len(chunks)} runs, {count}/term...")
    items = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_apify_run, mode, c, count): c for c in chunks}
        for fut in as_completed(futs):
            try:
                items.extend(fut.result())
            except Exception as e:
                print(f"  [!] apify chunk {futs[fut]} failed: {type(e).__name__}: {e}")
    out = []
    for it in items:
        vmeta = it.get("videoMeta") or {}
        dur = vmeta.get("duration", 0)
        if dur and (dur < min_dur or dur > max_dur):
            continue
        vid = str(it.get("id", ""))
        web_url = it.get("webVideoUrl")
        if not vid or not web_url:
            continue
        out.append({
            "video_id": vid,
            "desc": (it.get("text") or "")[:500],
            "author": (it.get("authorMeta") or {}).get("name", ""),
            "author_name": (it.get("authorMeta") or {}).get("nickName", ""),
            "duration_s": dur,
            "create_time": it.get("createTime", 0),
            "plays": it.get("playCount", 0),
            "likes": it.get("diggCount", 0),
            "url": web_url,
            "source_key": ",".join(keys),
        })
    print(f"  [apify] {len(out)} usable results")
    return out


def crawl_slot_apify(mode, keys, count, slot_dir, meta_path, min_dur, max_dur,
                     dl_workers=4):
    from concurrent.futures import ThreadPoolExecutor, as_completed

    os.makedirs(slot_dir, exist_ok=True)
    have = already_have(slot_dir)
    saved = 0
    metas = apify_discover(mode, keys, count, min_dur, max_dur)
    todo = []
    seen = set()
    for meta in metas:
        vid = meta["video_id"]
        if vid in have or vid in seen:
            continue
        seen.add(vid)
        todo.append(meta)

    def dl(meta):
        out_path = os.path.join(slot_dir, f"{meta['video_id']}.mp4")
        return meta, out_path, ytdlp_download(meta["url"], out_path)

    with ThreadPoolExecutor(max_workers=dl_workers) as ex:
        for fut in as_completed([ex.submit(dl, m) for m in todo]):
            meta, out_path, ok = fut.result()
            if ok:
                meta["file"] = out_path
                append_meta(meta_path, meta)
                saved += 1
                print(f"    saved {meta['video_id']} ({meta['duration_s']}s, "
                      f"{meta['plays']} plays)")
            else:
                print(f"    FAILED download {meta['video_id']}")
    return saved


def run_slot(mode, keys, count, slot_dir, meta_path, min_dur, max_dur, engine="auto"):
    """Dispatch one slot to the right engine. auto = tiktokapi when MS_TOKEN is
    set, apify otherwise; tiktokapi zero-result falls through to apify."""
    if engine == "tiktokapi" or (engine == "auto" and MS_TOKEN):
        try:
            saved = asyncio.run(
                crawl_slot(mode, keys, count, slot_dir, meta_path, min_dur, max_dur))
            if saved > 0 or engine == "tiktokapi":
                return saved
            print("  [i] tiktokapi returned nothing — falling back to apify")
        except Exception as e:
            if engine == "tiktokapi":
                raise
            print(f"  [i] tiktokapi failed ({type(e).__name__}) — falling back to apify")
    apify_mode = "search" if mode == "search" else mode
    return crawl_slot_apify(apify_mode, keys, count, slot_dir, meta_path, min_dur, max_dur)


# ---------------------------------------------------------------------------
# URL-list download (Apify fallback / hand-picked)
# ---------------------------------------------------------------------------

def crawl_urls(urls, slot_dir, meta_path):
    os.makedirs(slot_dir, exist_ok=True)
    saved = 0
    for url in urls:
        url = url.strip()
        if not url:
            continue
        m = re.search(r"/video/(\d+)", url)
        vid = m.group(1) if m else re.sub(r"\W+", "_", url)[-24:]
        out_path = os.path.join(slot_dir, f"{vid}.mp4")
        if os.path.exists(out_path):
            print(f"    have {vid}")
            continue
        if ytdlp_download(url, out_path):
            append_meta(meta_path, {"video_id": vid, "url": url, "file": out_path, "source_key": "urls"})
            saved += 1
            print(f"    saved {vid}")
        else:
            print(f"    FAILED {url}")
        time.sleep(1)
    return saved


# ---------------------------------------------------------------------------
# Plan runner
# ---------------------------------------------------------------------------

def norm_hashtag(term):
    return re.sub(r"[^a-z0-9]", "", term.lower())


def run_plan(plan_path, output_dir, engine="auto"):
    plan = json.loads(Path(plan_path).read_text())
    output_dir = Path(output_dir)
    cand_root = output_dir / "candidates"
    cand_root.mkdir(parents=True, exist_ok=True)
    meta_path = str(output_dir / "candidates_meta.jsonl")
    engine = plan.get("engine", engine)

    total = 0
    for slot in plan["slots"]:
        sid = slot["slot_id"]
        slot_dir = str(cand_root / sid)
        mode = slot.get("mode", "search")
        count = int(slot.get("per_term_count", 8))
        min_dur = int(slot.get("min_duration_s", 3))
        max_dur = int(slot.get("max_duration_s", 90))
        print(f"\n== Slot {sid}: {slot.get('script_line', '')[:70]}")

        if mode == "urls":
            total += crawl_urls(slot.get("urls", []), slot_dir, meta_path)
        elif mode == "sound":
            total += asyncio.run(
                crawl_slot(mode, slot.get("search_terms", []), count,
                           slot_dir, meta_path, min_dur, max_dur))
        else:
            keys = slot.get("search_terms", [])
            if mode == "hashtag":
                keys = [norm_hashtag(k) for k in keys]
            total += run_slot(mode, keys, count, slot_dir, meta_path,
                              min_dur, max_dur, engine)
    print(f"\nDone. {total} new candidate videos in {cand_root}")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", help="sourcing_plan.json path (plan mode)")
    ap.add_argument("--mode", choices=["search", "hashtag", "sound", "user", "urls"],
                    default="search")
    ap.add_argument("--engine", choices=["auto", "apify", "tiktokapi"], default="auto")
    ap.add_argument("--keys", help="comma-separated hashtags / sound id / username")
    ap.add_argument("--url-file", help="file with one TikTok URL per line (urls mode)")
    ap.add_argument("--urls", help="comma-separated TikTok URLs (urls mode)")
    ap.add_argument("--count", type=int, default=8, help="candidates per key")
    ap.add_argument("--slot", default="S01", help="slot id for one-off modes")
    ap.add_argument("--min-duration", type=int, default=3)
    ap.add_argument("--max-duration", type=int, default=90)
    ap.add_argument("--output", required=True, help="job output dir")
    args = ap.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    if args.plan:
        run_plan(args.plan, args.output, args.engine)
        return

    slot_dir = str(out / "candidates" / args.slot)
    meta_path = str(out / "candidates_meta.jsonl")
    if args.mode == "urls":
        urls = []
        if args.url_file:
            urls += Path(args.url_file).read_text().splitlines()
        if args.urls:
            urls += args.urls.split(",")
        crawl_urls(urls, slot_dir, meta_path)
    else:
        keys = [k.strip() for k in (args.keys or "").split(",") if k.strip()]
        if args.mode == "hashtag":
            keys = [norm_hashtag(k) for k in keys]
        if not keys:
            print("[!] --keys required")
            sys.exit(1)
        if args.mode == "sound":
            asyncio.run(
                crawl_slot(args.mode, keys, args.count, slot_dir, meta_path,
                           args.min_duration, args.max_duration))
        else:
            run_slot(args.mode, keys, args.count, slot_dir, meta_path,
                     args.min_duration, args.max_duration, args.engine)


if __name__ == "__main__":
    main()
