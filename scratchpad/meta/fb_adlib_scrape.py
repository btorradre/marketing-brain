#!/usr/bin/env python3
"""Unauthenticated Meta Ads Library scrape via the async search endpoint."""
import json, re, sys, urllib.parse, urllib.request, http.cookiejar

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def scrape(query, count=60):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [("User-Agent", UA), ("Accept-Language", "en-US,en;q=0.9")]

    seed_url = ("https://www.facebook.com/ads/library/?active_status=active&ad_type=all"
                f"&country=US&q={urllib.parse.quote(query)}&search_type=keyword_unordered"
                "&media_type=all")
    html = opener.open(seed_url, timeout=60).read().decode("utf-8", "replace")

    lsd = None
    m = re.search(r'"LSD",\[\],{"token":"([^"]+)"', html)
    if m: lsd = m.group(1)
    if not lsd:
        m = re.search(r'name="lsd" value="([^"]+)"', html)
        if m: lsd = m.group(1)
    if not lsd:
        print(f"[{query}] no lsd token; page len {len(html)}", file=sys.stderr)
        return None

    params = {
        "q": query, "count": str(count), "active_status": "active",
        "ad_type": "all", "countries[0]": "US",
        "search_type": "keyword_unordered", "media_type": "all",
        "session_id": "", "collation_token": "",
    }
    body = urllib.parse.urlencode({"lsd": lsd, **params}).encode()
    req = urllib.request.Request(
        "https://www.facebook.com/ads/library/async/search_ads/?" + urllib.parse.urlencode(params),
        data=body, method="POST")
    req.add_header("User-Agent", UA)
    req.add_header("X-FB-LSD", lsd)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("Referer", seed_url)
    try:
        raw = opener.open(req, timeout=60).read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        print(f"[{query}] async HTTP {e.code}", file=sys.stderr)
        return None
    raw = raw.replace("for (;;);", "", 1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"[{query}] non-JSON response, first 200: {raw[:200]}", file=sys.stderr)
        return None

if __name__ == "__main__":
    q = sys.argv[1]
    out = sys.argv[2]
    data = scrape(q)
    if data:
        json.dump(data, open(out, "w"))
        print(f"[{q}] OK -> {out}")
    else:
        sys.exit(1)
