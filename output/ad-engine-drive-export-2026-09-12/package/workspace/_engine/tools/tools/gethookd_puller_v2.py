#!/usr/bin/env python3
"""Pull all winning (5-star) video ads from GetHookd brand spy + swipe file. v2 with correct score mapping."""
import json, sys, time, requests, os
from collections import Counter

API_KEY = "[REDACTED_SECRET]"
BASE = "https://app.gethookd.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

# Score mapping: 91 = Winning (5 stars), 81 = Optimized (4 stars)
MIN_WINNING_SCORE = 91  # 5 stars only

BRANDS = {
    "Nutravive": 150589,
    "Alicia Darling": 134264, 
    "GLP-1 SOS Supplements": 3846867,
    "Dr Gundry Energy and Health": 2552,
}

def get_all_brand_ads(brand_id, brand_name):
    """Pull all ads for a brand, paginated."""
    all_ads = []
    page = 1
    per_page = 100
    retries = 0
    while True:
        url = f"{BASE}/brandspy/{brand_id}?page={page}&per_page={per_page}"
        resp = requests.get(url, headers=HEADERS)
        
        if resp.status_code == 429:
            retries += 1
            wait = min(60, 5 * retries)
            print(f"  Rate limited, waiting {wait}s (retry {retries})...")
            time.sleep(wait)
            continue
        
        data = resp.json()
        if data.get("errors"):
            print(f"  ERROR: {data.get('message')}")
            if retries < 3:
                retries += 1
                time.sleep(10)
                continue
            break
        
        retries = 0
        ads_data = data["data"]["ads"]
        ads = ads_data.get("data", [])
        total = ads_data.get("total", 0)
        all_ads.extend(ads)
        
        # Count winning on this page
        winning_on_page = sum(1 for a in ads if (a.get("performance_score") or 0) >= MIN_WINNING_SCORE)
        print(f"  [{brand_name}] Page {page}/{ads_data.get('last_page',1)}: {len(ads)} ads ({winning_on_page} winning) | total collected: {len(all_ads)}/{total}")
        
        if page >= ads_data.get("last_page", 1):
            break
        page += 1
        time.sleep(0.3)  # rate limit
    return all_ads

def get_swipe_file():
    """Pull all ads from swipe file."""
    all_ads = []
    page = 1
    per_page = 100
    while True:
        url = f"{BASE}/swipefile?page={page}&per_page={per_page}"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 429:
            time.sleep(10)
            continue
        data = resp.json()
        if data.get("errors"):
            print(f"  ERROR: {data.get('message')}")
            break
        ads = data.get("data", [])
        if not ads:
            break
        all_ads.extend(ads)
        print(f"  [Swipe File] Page {page}: {len(ads)} ads (collected: {len(all_ads)})")
        if len(ads) < per_page:
            break
        page += 1
        time.sleep(0.3)
    return all_ads

def filter_winning_video(ads):
    """Filter for 5-star (Winning) video ads."""
    return [ad for ad in ads if (ad.get("performance_score") or 0) >= MIN_WINNING_SCORE and ad.get("display_format") == "VIDEO"]

def main():
    output_dir = os.path.expanduser("~/Documents/marketing brain/gethookd-research")
    os.makedirs(output_dir, exist_ok=True)
    
    all_results = {}
    all_winning_videos = []
    
    for name, brand_id in BRANDS.items():
        print(f"\n=== {name} (brand_id={brand_id}) ===")
        ads = get_all_brand_ads(brand_id, name)
        winning = filter_winning_video(ads)
        print(f"  >> {len(winning)} WINNING video ads out of {len(ads)} total")
        
        # Score distribution
        scores = Counter((a.get("performance_score"), a.get("performance_score_title")) for a in ads)
        print(f"  Score distribution: {dict(scores)}")
        
        all_results[name] = {
            "brand_id": brand_id,
            "total_ads": len(ads),
            "winning_video_count": len(winning),
        }
        all_winning_videos.extend(winning)
        
        # Save per-brand
        safe_name = name.replace(" ", "_").lower()
        with open(os.path.join(output_dir, f"{safe_name}_winning_video.json"), "w") as f:
            json.dump(winning, f, indent=2)
    
    # Swipe file
    print(f"\n=== Swipe File ===")
    swipe = get_swipe_file()
    winning_swipe = filter_winning_video(swipe)
    # Also get ALL swipe file ads regardless of score (user saved them for a reason)
    swipe_video = [ad for ad in swipe if ad.get("display_format") == "VIDEO"]
    print(f"  >> {len(winning_swipe)} WINNING video ads / {len(swipe_video)} total video ads / {len(swipe)} total in swipe file")
    
    all_results["Swipe File"] = {
        "total_ads": len(swipe),
        "video_ads": len(swipe_video),
        "winning_video_count": len(winning_swipe),
    }
    
    with open(os.path.join(output_dir, "swipe_file_winning_video.json"), "w") as f:
        json.dump(winning_swipe, f, indent=2)
    with open(os.path.join(output_dir, "swipe_file_all_video.json"), "w") as f:
        json.dump(swipe_video, f, indent=2)
    
    # Master file with ALL winning videos
    with open(os.path.join(output_dir, "all_winning_videos.json"), "w") as f:
        json.dump(all_winning_videos, f, indent=2)
    
    # Summary with video URLs for download
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    total = 0
    for name, r in all_results.items():
        print(f"  {name}: {r.get('winning_video_count', 0)} winning video ads / {r['total_ads']} total")
        total += r.get("winning_video_count", 0)
    print(f"\n  TOTAL WINNING VIDEO ADS: {total}")
    
    # List all winning video URLs for download
    print(f"\n  Video URLs for download:")
    for ad in all_winning_videos:
        media = ad.get("media", [])
        for m in media:
            if m.get("type") == "video" and m.get("url"):
                print(f"    {m['url']}")
                break
    
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nFiles saved to: {output_dir}")

if __name__ == "__main__":
    main()
