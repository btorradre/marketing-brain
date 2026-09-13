#!/usr/bin/env python3
"""Pull all 5-star video ads from GetHookd brand spy + swipe file."""
import json, sys, time, requests, os

API_KEY = "[REDACTED_SECRET]"
BASE = "https://app.gethookd.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

# Brand mapping: spied_brand_id -> brand_id (internal) -> name
BRANDS = {
    120715: {"brand_id": 150589, "name": "Nutravive"},
    95934:  {"brand_id": None, "name": "Alicia Darling"},  # need to find brand_id
    118401: {"brand_id": 3846867, "name": "GLP-1 SOS Supplements"},
    122428: {"brand_id": 2552, "name": "Dr Gundry Energy and Health"},
}

def get_all_brand_ads(brand_id, brand_name):
    """Pull all ads for a brand, paginated."""
    all_ads = []
    page = 1
    per_page = 100
    while True:
        url = f"{BASE}/brandspy/{brand_id}?page={page}&per_page={per_page}"
        resp = requests.get(url, headers=HEADERS)
        data = resp.json()
        if data.get("errors"):
            print(f"  ERROR for brand_id {brand_id}: {data.get('message')}")
            break
        ads_data = data["data"]["ads"]
        ads = ads_data.get("data", [])
        total = ads_data.get("total", 0)
        all_ads.extend(ads)
        print(f"  [{brand_name}] Page {page}: got {len(ads)} ads (total: {total}, collected: {len(all_ads)})")
        if page >= ads_data.get("last_page", 1):
            break
        page += 1
        time.sleep(0.25)  # rate limit
    return all_ads

def get_swipe_file():
    """Pull all ads from swipe file."""
    all_ads = []
    page = 1
    per_page = 100
    while True:
        url = f"{BASE}/swipefile?page={page}&per_page={per_page}"
        resp = requests.get(url, headers=HEADERS)
        data = resp.json()
        if data.get("errors"):
            print(f"  ERROR: {data.get('message')}")
            break
        ads = data.get("data", [])
        if not ads:
            break
        all_ads.extend(ads)
        print(f"  [Swipe File] Page {page}: got {len(ads)} ads (collected: {len(all_ads)})")
        # Check if there are more pages
        if len(ads) < per_page:
            break
        page += 1
        time.sleep(0.25)
    return all_ads

def filter_5star_video(ads):
    """Filter for 5-star performance score and video format."""
    return [ad for ad in ads if ad.get("performance_score") == 5 and ad.get("display_format") == "VIDEO"]

def main():
    output_dir = os.path.expanduser("~/Documents/marketing brain/gethookd-research")
    os.makedirs(output_dir, exist_ok=True)
    
    # First, get all spied brands to find brand_ids
    print("=== Getting spied brands list ===")
    all_brands = []
    for pg in range(1, 10):
        resp = requests.get(f"{BASE}/brandspy?page={pg}", headers=HEADERS)
        data = resp.json()
        brands = data.get("data", [])
        if not brands:
            break
        all_brands.extend(brands)
    
    # Build lookup: spied_brand_id -> brand_id
    brand_lookup = {}
    for b in all_brands:
        brand_lookup[b["id"]] = b["brand_id"]
        if b["id"] == 95934:
            BRANDS[95934]["brand_id"] = b["brand_id"]
            print(f"  Found brand_id for Alicia Darling (95934): {b['brand_id']}")
    
    print(f"  Total spied brands: {len(all_brands)}")
    
    all_results = {}
    
    # Pull ads from each brand
    for spied_id, info in BRANDS.items():
        brand_id = info["brand_id"] or brand_lookup.get(spied_id)
        name = info["name"]
        if not brand_id:
            print(f"\n=== SKIP {name} (spied_id={spied_id}) — no brand_id found ===")
            continue
        
        print(f"\n=== Pulling ads for {name} (brand_id={brand_id}) ===")
        ads = get_all_brand_ads(brand_id, name)
        five_star_video = filter_5star_video(ads)
        print(f"  RESULT: {len(five_star_video)} five-star video ads out of {len(ads)} total")
        
        all_results[name] = {
            "spied_brand_id": spied_id,
            "brand_id": brand_id,
            "total_ads": len(ads),
            "five_star_video_count": len(five_star_video),
            "five_star_video_ads": five_star_video,
        }
        
        # Save per-brand
        with open(os.path.join(output_dir, f"{name.replace(' ', '_').lower()}_5star_video.json"), "w") as f:
            json.dump(five_star_video, f, indent=2)
    
    # Pull swipe file
    print(f"\n=== Pulling Swipe File ===")
    swipe_ads = get_swipe_file()
    five_star_swipe = filter_5star_video(swipe_ads)
    print(f"  RESULT: {len(five_star_swipe)} five-star video ads out of {len(swipe_ads)} total in swipe file")
    
    all_results["Swipe File"] = {
        "total_ads": len(swipe_ads),
        "five_star_video_count": len(five_star_swipe),
        "five_star_video_ads": five_star_swipe,
    }
    
    with open(os.path.join(output_dir, "swipe_file_5star_video.json"), "w") as f:
        json.dump(five_star_swipe, f, indent=2)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    total_5star = 0
    for name, r in all_results.items():
        print(f"  {name}: {r['five_star_video_count']} five-star video ads / {r['total_ads']} total")
        total_5star += r["five_star_video_count"]
    print(f"\n  TOTAL FIVE-STAR VIDEO ADS: {total_5star}")
    
    # Save master summary
    summary = {k: {kk: vv for kk, vv in v.items() if kk != "five_star_video_ads"} for k, v in all_results.items()}
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nFiles saved to: {output_dir}")

if __name__ == "__main__":
    main()
