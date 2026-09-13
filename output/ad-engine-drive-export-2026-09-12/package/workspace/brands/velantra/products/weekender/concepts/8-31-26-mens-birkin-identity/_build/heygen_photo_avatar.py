"""Create a HeyGen photo avatar from a greenscreen keyframe and return its look id.
Order matters (MENSGS-01 lesson): upload asset -> create avatar -> THEN render with engine avatar_v.

  python3 heygen_photo_avatar.py <image.png> "<name>"   -> prints JSON {asset_id, look_id, group_id, engines}
"""
import json, os, subprocess, sys
VAULT="/Users/brooksorradre2/Documents/marketing brain"
def env(k):
    for line in open(os.path.join(VAULT,".env")):
        line=line.strip()
        if line and not line.startswith("#") and "=" in line:
            a,b=line.split("=",1)
            if a.strip()==k: return b.strip().strip('"').strip("'")
    raise KeyError(k)
KEY=env("HEYGEN_API_KEY")
def curl(args):
    out=subprocess.run(["curl","-s"]+args,capture_output=True,text=True,timeout=180).stdout
    try: return json.loads(out)
    except Exception: return {"_raw":out[:300]}
img, name = sys.argv[1], sys.argv[2]
assert os.path.exists(img), img
a=curl(["-X","POST","https://api.heygen.com/v3/assets","-H",f"X-Api-Key: {KEY}","-F",f"file=@{img}"])
asset_id=(a.get("data") or {}).get("asset_id") or (a.get("data") or {}).get("id")
if not asset_id:
    a=curl(["-X","POST","https://upload.heygen.com/v1/asset","-H",f"X-Api-Key: {KEY}","-H","Content-Type: image/png","--data-binary",f"@{img}"])
    asset_id=(a.get("data") or {}).get("id") or (a.get("data") or {}).get("asset_id")
if not asset_id: print(json.dumps({"error":"asset upload failed","resp":a})); sys.exit(1)
b=curl(["-X","POST","https://api.heygen.com/v3/avatars","-H",f"X-Api-Key: {KEY}","-H","Content-Type: application/json",
        "-d",json.dumps({"type":"photo","name":name,"file":{"type":"asset_id","asset_id":asset_id}})])
d=b.get("data") or {}
item=d.get("avatar_item") or d
out={"asset_id":asset_id,"look_id":item.get("id"),"group_id":(d.get("avatar_group") or {}).get("id") or item.get("group_id"),
     "engines":item.get("supported_api_engines"),"status":item.get("status"),"raw":b if not item.get("id") else None}
print(json.dumps(out,indent=1))
