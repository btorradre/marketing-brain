import pathlib,json,html,csv
P=pathlib.Path(__file__).resolve().parent
cases=[
('878420788651528','Medical-crisis photo + spouse narrative','Strongest observed total reach','A bathroom mirror photo showing an abdominal scar and a medical pouch, paired with a 2,777-word story told by a husband. The copy moves from successful weight loss to digestive distress, failed remedies, research, product discovery, and a recovery timeline. The visual and narrative are advertiser material; their authenticity and causal implications are unverified.'),
('3291016807753829','Side-by-side body image + side-effect diary','Strong measured static example','A side-by-side full-body image with a short overlay about the cost of slimming injections, paired with 306 words of first-person copy. Structure: weight is coming off → constipation/nausea/fog → products tried → simple daily routine → still losing weight and feeling better. The comparison image does not independently prove a transformation.'),
('1604509631289921','Ordinary lifestyle photo + nurse-framed story','Strong measured static example','An ordinary garage/workbench photo carries no obvious product pitch. The 1,520-word primary text does the selling through a narrator claiming nursing experience, a list of failed alternatives, discovery, and product comparison. Credentials and treatment claims were not verified.'),
('24781784614835674','Selfie testimonial + product/routine demonstration','Longevity and reuse only','40.5-second vertical video. Sampled frames show a medication vial and syringe opener, a woman speaking to camera, a fiber pouch close-up, and an outdoor drinking shot. A completed TrendTrack transcript supports a side-effects → discovery → benefits → daily-routine structure.'),
('1313972990318526','Talking-head education + product overlays','Longevity and reuse only','68.4-second vertical video. Sampled frames show a woman speaking directly to camera, a constipation-on-GLP-1 headline, yellow subtitle cards, and nutrition product overlays. The copy sells a GLP-1 nutrition bundle. Treat this as an educational presentation, without inferring credentials from appearance.'),
('2835637713488990','Animated anatomy explainer + progress timeline','Early measured signal','111.8-second vertical video. Sampled frames show a clothed skeleton with visible digestive anatomy, a DAY 10 progress card, organ close-ups, and a product packshot. The production method is unverified. It has only 2,004 reported reach and 11 days running, so it is an emerging format rather than a demonstrated large-scale winner.'),
('789593897301120','Comment-reply expert presentation','Adjacent side-effect reference','70.7-second kitchen talking-head video with a viewer comment about dehydration, dizziness and nausea. The presenter identifies herself as a doctor and holds an electrolyte product. Constipation appears in the ad copy, but the sampled video is primarily an adjacent GLP-1 side-effect example.'),
('1654383312323364','Relatable routine clip → app/watch demo','Adjacent product; reuse only','22.7-second video: a woman drinking water, native-style on-screen diary text, watch app close-ups, and an end card. Promotes a GLP-1 tracker rather than constipation relief. Useful only as an adjacent execution reference; not included among the top direct-niche recommendations.')]
rows=[]
for id,title,tier,notes in cases:
 s=json.loads((P/'raw'/f'scan-{id}.json').read_text())['result']['structuredContent'];a=s['data'];m=a['metrics']
 rows.append(dict(id=id,title=title,tier=tier,notes=notes,brand=a['advertiser']['name'],reach=m['reach'],reach7d=m['reachDelta7d'],reach30d=m['reachDelta30d'],days=a['daysRunning'],duplicates=m['duplicates'],members=s['memberAdsCount'],active=s['activeAdsCount'],media=a['media']['mediaUrl'],landing=a['content']['landingPageUrl'] or a.get('links',{}).get('adLibraryUrl') or ('https://www.facebook.com/ads/library/?id='+id),countries=', '.join(a['audience']['targetedCountries'] or []),type=a['media']['type'],words=len(a['content']['body'].split())))
with (P/'shortlist.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
intro='''# GLP-1 constipation creative formats — TrendTrack MCP, September 8, 2026

The strongest measured examples found were static images paired with personal narratives. For video, selfie testimonials with product demonstrations and talking-head education had substantial reported longevity and reuse, but no reported reach. Animated anatomy was an early signal with a much smaller measured audience.

## Scope and interpretation

Research used the live authenticated TrendTrack MCP endpoint (`tools/list`, `search_ads`, `scan_ad`). Searches covered GLP-1, GLP1, Mounjaro, Ozempic, Wegovy (in results), semaglutide, tirzepatide, and weight-loss-jab language alongside constipation/constipated. Results were active English-language Meta creatives, without a country restriction. This is a targeted shortlist, not an exhaustive census or a causal comparison of formats. Eight shortlisted creatives were deep-scanned; three stills and six sampled frames from each of five videos were visually inspected. Videos were not reviewed continuously end-to-end.

The strict GLP-1 + constipation query returned 544 matching creative groups; its video subset returned 128 under duplication sorting. These totals are not unique across searches, are not counts of proven winners, and include off-topic mentions. Drug sellers, hair-loss ads, broad clinical-study recruitment and incidental mentions were excluded from direct-niche recommendations. An exploratory `keyword_mode=any` batch expanded into unrelated results; it was not used as evidence of niche prevalence and was replaced with intersecting keyword queries.

Metrics describe creative groups where collation IDs were supplied. A representative ad may itself be inactive while another group member remains active. Reported days running describe the returned group, not verified uninterrupted spend. The `duplicates` field does not consistently equal member count minus one, so both values are preserved in the CSV. Null/zero reported reach is not evidence of zero delivery, especially outside EU/UK transparency coverage. No ROAS, CPA, conversion rate, sales or actual campaign budgets were available. Estimated spend was omitted because it is derived from reach and an assumed CPM.

TrendTrack uses “reach” as an impressions-style metric where available: [official API documentation](https://docs.trendtrack.io/en/docs/reference/api/ads). EU/UK coverage is described on [TrendTrack pricing](https://app.trendtrack.io/en/pricing). The Cloud example reports 59,874 seven-day growth but only 21,728 thirty-day growth, an inconsistent relationship for straightforward cumulative delivery. Glissé also reports identical one-day, seven-day and thirty-day deltas. Raw values are preserved; neither is treated as a clean daily-delivery series or used to calculate growth rates. Total reported reach and longevity anchor the measured shortlist.

## Direct-niche shortlist

| Format | Example | Reported reach | Days running | Evidence strength |
|---|---|---:|---:|---|
'''
for r in rows[:6]:intro+=f"| {r['title']} | {r['brand']} · [media]({r['media']}) | {r['reach']:,}"+(' (unreported/zero)' if not r['reach'] else '')+f" | {r['days']} | {r['tier']} |\n"
intro+='\n## What the executions actually contain\n\n'
for r in rows:
 intro+=f"### {r['title']} — {r['brand']}\n\n{r['notes']}\n\nReported: {r['reach']:,} reach; {r['days']} days; duplicates field {r['duplicates']}; {r['members']} group members, {r['active']} currently active. [Original media]({r['media']}) · [Destination]({r['landing']}) · [Raw MCP scan](raw/scan-{r['id']}.json).\n\n"
intro+='''## Test priority inferred from this evidence

1. Start with the side-effect diary static: a recognizable GLP-1 context, an ordinary personal image, and concise first-person narrative. It is supported by measured reach and has a simpler execution than the long crisis story.
2. Test a 35–45-second selfie testimonial with product use shown. That duration is a suggested production range anchored by the observed 40.5-second SoWell example, not a proven optimum.
3. Test a 60–75-second talking-head educational video with readable captions and relevant product demonstration. Again, this is an inferred range anchored by the observed 68.4-second Formulite example.
4. Keep the ordinary-photo long-copy story as a separate copy test. The photo alone does not explain performance; landing page, offer, audience and media buying are confounders.
5. Treat animated anatomy as an exploratory test. The observed measured evidence is too small to give it the same confidence as the leading statics.

A recurring message is that the audience wants to preserve its weight-loss progress while feeling comfortable and able to live normally. This is an inference from the observed ads. Competitors make strong medical-mechanism, remedy-dismissal and treatment claims that this research does not substantiate. Borrow the narrative and visual structures; use documented product claims, genuine experiences and verified credentials in any execution.

All raw requests/responses, the shortlist CSV, original downloaded media, and video sample frames are saved beside this report. The visual evidence gallery links the original media and displays the inspected frames.
'''
(P/'REPORT.md').write_text(intro)
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GLP-1 constipation creative evidence</title><style>body{font:16px system-ui;max-width:1120px;margin:40px auto;padding:0 20px;color:#17212c;background:#f7f8fa}article{background:white;padding:24px;margin:24px 0;border-radius:12px}img{max-width:100%;max-height:800px;display:block}p{line-height:1.6}a{color:#1c57a5}.meta{color:#55616d}</style><h1>GLP-1 constipation: creative evidence</h1><p>Live TrendTrack MCP · September 8, 2026. Observed performance proxies, not verified profitability. Still images and sampled video frames were inspected. <a href="REPORT.md">Full methodology and report</a>.</p>']
for r in rows:
 src=f"media/{r['id']}"+('-sheet.jpg' if r['type']=='video' else '.jpg')
 parts.append(f'<article><h2>{html.escape(r["title"])}</h2><p class="meta">{html.escape(r["brand"])} · {r["reach"]:,} reported reach · {r["days"]} days · {html.escape(r["tier"])}</p><p>{html.escape(r["notes"])}</p><p><a href="{html.escape(r["media"])}">Open original media</a> · <a href="{html.escape(r["landing"])}">Landing page</a></p><img src="{src}" alt="Inspected creative or sampled video frames"></article>')
parts.append('</html>');(P/'evidence.html').write_text('\n'.join(parts))
print('Created REPORT.md, shortlist.csv, evidence.html; 8 cases.')
