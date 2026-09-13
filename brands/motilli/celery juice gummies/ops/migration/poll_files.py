import json, urllib.request, time
from urllib.error import HTTPError

NEW_TOKEN="[REDACTED_SECRET]"
NEW_SHOP="y9t3s8-ns.myshopify.com"

def gql(q, variables=None):
    body = json.dumps({"query": q, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        f"https://{NEW_SHOP}/admin/api/2025-01/graphql.json",
        data=body,
        headers={"X-Shopify-Access-Token": NEW_TOKEN, "Content-Type":"application/json"}
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2**attempt); continue
            raise
    raise RuntimeError("retry exhausted")

submitted = json.load(open('files/submitted.json'))
# Reverse: gid -> old_url
gid_to_old = {gid: url for url, gid in submitted.items()}
print(f"Polling status for {len(gid_to_old)} files...")

# Query files by id in batches via nodes()
ids = list(gid_to_old.keys())
url_map = {}
not_ready = list(ids)

BATCH = 100
for attempt_round in range(20):
    if not not_ready:
        break
    print(f"Round {attempt_round}: {len(not_ready)} still pending")
    next_round = []
    for i in range(0, len(not_ready), BATCH):
        chunk = not_ready[i:i+BATCH]
        q = '''query($ids:[ID!]!){ nodes(ids:$ids) {
          ... on MediaImage { id fileStatus alt image { url } }
          ... on GenericFile { id fileStatus alt url }
          ... on Video { id fileStatus alt }
        } }'''
        data = gql(q, {"ids": chunk})
        if 'errors' in data:
            print(f"errors: {data['errors']}"); time.sleep(3); next_round.extend(chunk); continue
        for n in data['data']['nodes']:
            if not n: continue
            gid = n['id']
            status = n.get('fileStatus')
            if status == 'READY':
                u = (n.get('image') or {}).get('url') or n.get('url')
                if u:
                    url_map[gid_to_old[gid]] = u
                else:
                    print(f"WARN: ready but no url for {gid}")
            elif status == 'FAILED':
                print(f"FAILED file: {gid} (old={gid_to_old[gid]})")
            else:
                next_round.append(gid)
    not_ready = next_round
    print(f"  ready: {len(url_map)}/{len(submitted)}")
    if not_ready:
        time.sleep(8)

with open('files/url_map.json','w') as f:
    json.dump(url_map, f, indent=2)
print(f"\nFINAL: {len(url_map)} files mapped, {len(not_ready)} still pending/failed")
if not_ready:
    print("Pending GIDs:", not_ready[:5], "...")
