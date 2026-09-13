import json, os, sys, requests
ENV={}
for l in open(os.path.expanduser("~/Documents/marketing brain/.env")):
    l=l.strip()
    if "=" in l and not l.startswith("#"):
        k,v=l.split("=",1); ENV[k]=v.strip().strip('"').strip("'")
tok=ENV["APIFY_API_TOKEN"]
actor="clockworks~free-tiktok-scraper"
payload={"searchQueries":["handbag","what's in my bag"],"resultsPerPage":6,"searchSection":"/video","shouldDownloadVideos":False,"shouldDownloadCovers":False}
r=requests.post(f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?token=[REDACTED_SECRET]&timeout=240",json=payload,timeout=300)
print("status",r.status_code)
items=r.json()
print("n items",len(items))
out=os.path.join(os.path.dirname(__file__),"..","research","raw","probe.json")
json.dump(items,open(out,"w"),indent=1)
if items:
    it=items[0]
    print("keys:",sorted(it.keys()))
    for k in ["id","text","webVideoUrl","videoMeta","authorMeta","playCount","diggCount","commentCount","shareCount","createTimeISO","hashtags","mediaUrls","searchQuery","isAd","isSponsored"]:
        v=it.get(k)
        s=json.dumps(v)[:300] if v is not None else None
        print(f"  {k}: {s}")
