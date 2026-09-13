#!/usr/bin/env python3
"""
GetHookd URL Resolver — Shared utility for all replicator pipelines.

Accepts a GetHookd share URL or ad ID, fetches the ad metadata via API,
downloads the video to a local cache, and returns the local path + metadata.

Usage:
    from tools.gethookd_resolver import resolve_video_input

    video_path, metadata = resolve_video_input(user_input, cache_dir="/tmp/gethookd-cache")
    # video_path = local .mp4 file path (either the original local path or downloaded)
    # metadata = dict with ad info (brand, title, score, etc.) or None if local file
"""

import json
import os
import re
import sys
import time
import requests

API_KEY = "[REDACTED_SECRET]"
BASE = "https://app.gethookd.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

DEFAULT_CACHE_DIR = os.path.expanduser("~/Documents/marketing brain/gethookd-cache")


def is_gethookd_url(input_str):
    """Check if input is a GetHookd URL or ad ID (not a local file path)."""
    if not input_str:
        return False
    # GetHookd share URL patterns
    if "gethookd.ai" in input_str:
        return True
    # Pure numeric ad ID (8+ digits)
    if re.match(r"^\d{7,}$", input_str.strip()):
        return True
    return False


def extract_ad_id(input_str):
    """Extract ad ID from a GetHookd URL or raw ID string."""
    input_str = input_str.strip()

    # Pure numeric ID
    if re.match(r"^\d+$", input_str):
        return input_str

    # Share URL: https://app.gethookd.ai/share/ad/86606845?signature=[REDACTED_SECRET]
    match = re.search(r"gethookd\.ai/share/ad/(\d+)", input_str)
    if match:
        return match.group(1)

    # Dashboard URL: https://app.gethookd.ai/ads/86606845 or similar
    match = re.search(r"gethookd\.ai/(?:ads?|swipefile|brandspy)/.*?(\d{7,})", input_str)
    if match:
        return match.group(1)

    # Fallback: any 7+ digit number in the URL
    match = re.search(r"(\d{7,})", input_str)
    if match:
        return match.group(1)

    return None


def fetch_ad_metadata(ad_id):
    """Fetch ad metadata from GetHookd API.

    Tries multiple API endpoints to find the ad.
    """
    # Try the share endpoint first (works with ad IDs directly)
    endpoints = [
        f"{BASE}/ads/{ad_id}",
        f"{BASE}/swipefile/{ad_id}",
    ]

    for url in endpoints:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if not data.get("errors"):
                    ad_data = data.get("data", data)
                    if isinstance(ad_data, dict) and ad_data.get("id"):
                        return ad_data
        except Exception:
            continue

    # If direct endpoints fail, search the swipe file for it
    try:
        page = 1
        while page <= 10:  # Search up to 10 pages
            url = f"{BASE}/swipefile?page={page}&per_page=100"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                break
            data = resp.json()
            ads = data.get("data", [])
            if not ads:
                break
            for ad in ads:
                if str(ad.get("id")) == str(ad_id):
                    return ad
            page += 1
            time.sleep(0.3)
    except Exception:
        pass

    return None


def get_video_url(ad_data):
    """Extract the best video URL from ad metadata."""
    media = ad_data.get("media", [])
    # Find the first video with a URL
    for m in media:
        if m.get("type") == "video" and m.get("url"):
            return m["url"]
    return None


def download_video(video_url, ad_id, cache_dir):
    """Download video to cache directory. Returns local path."""
    os.makedirs(cache_dir, exist_ok=True)
    filename = f"gethookd_{ad_id}.mp4"
    local_path = os.path.join(cache_dir, filename)

    # Skip if already cached
    if os.path.exists(local_path) and os.path.getsize(local_path) > 10000:
        print(f"  [GetHookd] Using cached video: {local_path}")
        return local_path

    print(f"  [GetHookd] Downloading video from: {video_url[:80]}...")
    resp = requests.get(video_url, stream=True, timeout=120)
    resp.raise_for_status()

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0

    with open(local_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                pct = downloaded / total * 100
                mb = downloaded / 1024 / 1024
                print(f"\r  [GetHookd] Downloading: {mb:.1f}MB ({pct:.0f}%)", end="", flush=True)

    file_size = os.path.getsize(local_path) / 1024 / 1024
    print(f"\n  [GetHookd] Downloaded: {local_path} ({file_size:.1f}MB)")

    # Save metadata alongside the video
    return local_path


def build_metadata(ad_data):
    """Build a clean metadata dict from ad data for Gemini context injection."""
    return {
        "ad_id": ad_data.get("id"),
        "brand": ad_data.get("brand", {}).get("name", "Unknown") if isinstance(ad_data.get("brand"), dict) else "Unknown",
        "title": ad_data.get("title", ""),
        "body": ad_data.get("body", ""),
        "score": ad_data.get("performance_score"),
        "score_title": ad_data.get("performance_score_title", ""),
        "days_active": ad_data.get("days_active"),
        "landing_page": ad_data.get("landing_page", ""),
        "platform": ad_data.get("platform", ""),
        "start_date": ad_data.get("start_date", ""),
        "cta_type": ad_data.get("cta_type", ""),
        "share_url": ad_data.get("share_url", ""),
        "video_length": None,
    }


def resolve_video_input(input_str, cache_dir=None):
    """Main entry point. Resolves a video input (local path or GetHookd URL) to a local file.

    Args:
        input_str: Either a local file path or a GetHookd URL/ad ID
        cache_dir: Where to cache downloaded videos (default: ~/Documents/marketing brain/gethookd-cache/)

    Returns:
        tuple: (local_video_path, metadata_dict_or_None)
            - If local file: returns (path, None)
            - If GetHookd URL: returns (downloaded_path, metadata_dict)

    Raises:
        ValueError: If the URL can't be resolved or video can't be downloaded
        FileNotFoundError: If local file doesn't exist
    """
    if cache_dir is None:
        cache_dir = DEFAULT_CACHE_DIR

    # Check if it's a GetHookd URL/ID
    if not is_gethookd_url(input_str):
        # It's a local file path
        expanded = os.path.expanduser(input_str)
        if not os.path.exists(expanded):
            raise FileNotFoundError(f"Video file not found: {expanded}")
        return expanded, None

    # --- GetHookd resolution ---
    print(f"  [GetHookd] Resolving: {input_str}")

    ad_id = extract_ad_id(input_str)
    if not ad_id:
        raise ValueError(f"Could not extract ad ID from: {input_str}")

    print(f"  [GetHookd] Ad ID: {ad_id}")

    # Check if already cached
    cached_path = os.path.join(cache_dir, f"gethookd_{ad_id}.mp4")
    cached_meta = os.path.join(cache_dir, f"gethookd_{ad_id}_meta.json")

    if os.path.exists(cached_path) and os.path.getsize(cached_path) > 10000:
        print(f"  [GetHookd] Found cached video: {cached_path}")
        metadata = None
        if os.path.exists(cached_meta):
            with open(cached_meta) as f:
                metadata = json.load(f)
        return cached_path, metadata

    # Fetch metadata from API
    print(f"  [GetHookd] Fetching ad metadata from API...")
    ad_data = fetch_ad_metadata(ad_id)

    if not ad_data:
        # Try direct video download from share URL as fallback
        if "gethookd.ai/share/ad/" in input_str:
            # The share page may have the video URL embedded — try scraping it
            raise ValueError(
                f"Could not fetch ad metadata for ID {ad_id}. "
                f"The ad may not be in your swipe file or brand spy. "
                f"Try adding it to your swipe file on GetHookd first."
            )
        raise ValueError(f"Could not find ad with ID {ad_id} in GetHookd API")

    # Extract video URL
    video_url = get_video_url(ad_data)
    if not video_url:
        raise ValueError(f"Ad {ad_id} has no video media attached")

    # Download
    local_path = download_video(video_url, ad_id, cache_dir)

    # Build and save metadata
    metadata = build_metadata(ad_data)

    # Get video length from media if available
    for m in ad_data.get("media", []):
        if m.get("type") == "video" and m.get("video_length"):
            metadata["video_length"] = m["video_length"]
            break

    # Cache metadata
    with open(cached_meta, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"  [GetHookd] Resolved: {ad_data.get('brand', {}).get('name', '?')} — \"{ad_data.get('title', '?')[:50]}\"")
    print(f"  [GetHookd] Score: {metadata['score']} ({metadata['score_title']}) | {metadata['days_active']} days active")

    return local_path, metadata


# --- CLI for standalone testing ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gethookd_resolver.py <url_or_path_or_ad_id>")
        print("\nExamples:")
        print("  python3 gethookd_resolver.py https://app.gethookd.ai/share/ad/86606845?signature=[REDACTED_SECRET]")
        print("  python3 gethookd_resolver.py 86606845")
        print("  python3 gethookd_resolver.py /path/to/local/video.mp4")
        sys.exit(1)

    path, meta = resolve_video_input(sys.argv[1])
    print(f"\nResolved path: {path}")
    if meta:
        print(f"Metadata: {json.dumps(meta, indent=2)}")
