# adv2 deploy — 2026-08-03

## Status

| Piece | State |
|---|---|
| Vercel project `lunessa-a1` (team `bto-ec-ventures`) | **live** |
| https://lunessa-a1.vercel.app | **live, 200, images serving** |
| SSO Deployment Protection | disabled |
| Domain `a1.hearthealthblog.org` attached to project | done, `verified: true` |
| DNS CNAME for `a1` | **BLOCKED — not created** |

## The blocker

`hearthealthblog.org` is **not** on Namecheap like guthealthblog.org. It is:

- Registered at **GoDaddy** (created 2025-12-02, expires 2026-12-02)
- DNS on GoDaddy nameservers `ns69/ns70.domaincontrol.com`
- Apex currently served by **Netlify** (75.2.60.5), `www` CNAMEs to `adv6.netlify.app`
- Apex app is a React/Vite SPA titled "Heart Health Insider" with Microsoft Clarity (`ugd7r807e4`)

There are **no GoDaddy credentials** in `.env`, no GoDaddy browser profile in `auth/`, and no Netlify
CLI or token on this machine. The Namecheap API cannot touch this domain. So the final CNAME has to
be added by hand in the GoDaddy DNS panel.

## The one record to add

In GoDaddy DNS for `hearthealthblog.org`:

```
Type:  CNAME
Name:  a1
Value: f91eedf8d9f67e95.vercel-dns-016.com
TTL:   600
```

Fallback value if GoDaddy rejects the per-project host: `cname.vercel-dns.com`

This is purely additive. It does not touch the apex A record or the `www` CNAME, so the existing
Netlify site keeps serving exactly as it does now.

After the record propagates (~1 to 10 min on GoDaddy), confirm with:

```
dig +short a1.hearthealthblog.org
curl -s -o /dev/null -w "%{http_code}\n" -L https://a1.hearthealthblog.org
```

Vercel issues the certificate automatically once the CNAME resolves. If it races, re-add the domain:

```
TOKEN=$(python3 -c "import json;print(json.load(open('/Users/brooksorradre2/Library/Application Support/com.vercel.cli/auth.json'))['token'])")
curl -s -X POST "https://api.vercel.com/v10/projects/lunessa-a1/domains?teamId=team_PEAgDtA4cYo5pPIWohX7sw2G" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"a1.hearthealthblog.org"}'
```

## Redeploying the page

```
cd brands/lunessa/pages/advertorials/adv2-three-pathway
python3 _production/build_page.py          # rebuilds web/index.html from the template + body
cd web && vercel deploy --prod --yes --scope bto-ec-ventures
```

## Open items before this takes traffic

1. **The ad CTAs point at `go.shoplunessa.store/adv2`.** That host does not resolve right now
   (`shoplunessa.store` returned 000). The live store is **`trylunessa.co`**. Either point
   `go.shoplunessa.store` at this page or change the ad links to `a1.hearthealthblog.org`.
2. **Guarantee term is unverified.** The refund policy page is JS-rendered and could not be parsed,
   so the page says "Money-Back Guarantee" with no day count. If it is 90 days, say so explicitly.
3. **No ratings block.** The Motilli template's 4.9 / 4,217-ratings sidebar card was deliberately
   dropped rather than inventing numbers for Lunessa. Supply real review data to add it back.
4. **"AS SEEN ON" media logos dropped** (NBC/ABC/CBS/Fox) — fabricated media endorsement.
5. No analytics on the page. The apex runs Clarity `ugd7r807e4`; add the same tag if you want this
   subdomain in the same project.
