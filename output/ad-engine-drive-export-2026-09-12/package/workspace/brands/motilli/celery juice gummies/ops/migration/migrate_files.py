"""
Migrate files from old to new Shopify store using fileCreate with URL pull.
Builds an old_url -> new_url map for downstream HTML rewriting.
"""
import json, urllib.request, urllib.parse, time, sys, os
from urllib.error import HTTPError

OLD_TOKEN="[REDACTED_SECRET]"
NEW_TOKEN="[REDACTED_SECRET]"
OLD_SHOP="sthgu4-xa.myshopify.com"
NEW_SHOP="y9t3s8-ns.myshopify.com"

def gql(shop, token, q, variables=None):
    body = json.dumps({"query": q, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        f"https://{shop}/admin/api/2025-01/graphql.json",
        data=body,
        headers={"X-Shopify-Access-Token": token, "Content-Type":"application/json"}
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError("retry exhausted")

# Load source URLs
files = json.load(open('files/old_urls.json'))
print(f"Migrating {len(files)} files...")

# Read existing map if resuming
url_map = {}
if os.path.exists('files/url_map.json'):
    url_map = json.load(open('files/url_map.json'))
    print(f"Resuming: already have {len(url_map)} mapped URLs")

# Helper: filename from URL (without ?v=)
def fname(url):
    base = url.split('?')[0]
    return base.split('/')[-1]

# Submit in batches of 25
remaining = [f for f in files if f['url'] not in url_map]
print(f"Need to submit: {len(remaining)} files")

BATCH = 10
new_file_ids = {}  # alt or original_src -> id (for poll matching)
# We will key by the source URL we submit. fileCreate returns the file with no original URL exposed; we'll use alt as a tag carrying the old url stripped of ?v=

submitted = json.load(open('files/submitted.json')) if os.path.exists('files/submitted.json') else {}
# submitted: { old_url: new_file_gid }

q_create = """
mutation fileCreate($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files { id alt fileStatus
      ... on MediaImage { image { url } mimeType }
      ... on GenericFile { url mimeType }
    }
    userErrors { field message code }
  }
}
"""

todo = [f for f in remaining if f['url'] not in submitted]
print(f"Submitting {len(todo)} new files in batches of {BATCH}...")

for i in range(0, len(todo), BATCH):
    chunk = todo[i:i+BATCH]
    # Use the alt field to carry the old filename for matching
    inputs = []
    for f in chunk:
        old_url_clean = f['url'].split('?')[0]
        marker = f"MIGR::{old_url_clean}"
        # If alt was set, preserve original but prepend marker  
        alt_combined = marker
        if f.get('alt'):
            alt_combined = f"{marker}::{f['alt'][:200]}"
        inputs.append({
            "originalSource": f['url'],
            "alt": alt_combined,
            "contentType": "IMAGE" if "image" in f['url'].lower() or any(f['url'].lower().split('?')[0].endswith(ext) for ext in ['.png','.jpg','.jpeg','.webp','.gif','.svg']) else "FILE"
        })
    data = gql(NEW_SHOP, NEW_TOKEN, q_create, {"files": inputs})
    if 'errors' in data:
        print(f"GraphQL errors batch {i}: {data['errors']}")
        time.sleep(2); continue
    result = data['data']['fileCreate']
    if result['userErrors']:
        print(f"userErrors batch {i}: {result['userErrors']}")
    created = result['files']
    for j, fobj in enumerate(created):
        old_url = chunk[j]['url']
        submitted[old_url] = fobj['id']
    print(f"  batch {i}-{i+len(chunk)}: {len(created)} created, throttle...")
    with open('files/submitted.json','w') as f:
        json.dump(submitted, f)
    time.sleep(0.5)

print(f"Submitted total: {len(submitted)}")
