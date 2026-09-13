import json,pathlib,html,csv
P=pathlib.Path(__file__).resolve().parent
r={x['label']:x for x in json.loads((P/'candidates.json').read_text())}
chosen=[('U1','Failed-remedy cost breakdown','Likely AI presenter and staged reenactments','77-second developed VSL. A woman lists previous products, prices and disappointing outcomes, then introduces a different explanation and a product designed for the situation. Alternates direct address, symptom scenes, product inserts and a clear offer. Strongest combined reuse/longevity candidate in the screened human-presenter set.'),('U3','Blunt car-selfie recommendation','Likely AI presenter and reenactments','50-second compact VSL. A man addresses the camera from his car, moves into a simple explanation with anatomy and ingredient inserts, then returns to an ordinary-life outcome and product/guarantee close. An identical media file is currently active under a newer ad ID.'),('U2','Close-camera peer explanation','Likely AI presenter and reenactments','42-second compact VSL. A man with a small microphone makes a direct problem callout, explains the product roles, demonstrates the routine and closes with a guarantee. It is a short complete sales argument, rather than a 2–5-minute VSL.'),('L20','Mechanism-first kitchen explanation','Likely AI presenter and staged inserts','104-second developed VSL. A woman at a kitchen counter introduces a conflict between previous remedies and the medication-altered situation. Anatomy inserts illustrate the explanation; product roles, daily-life outcomes, routine and guarantee complete the argument. Weaker reuse evidence than the top three.'),('L7','Outcome-first morning-routine story','Likely AI presenter; some inserts may be live-action','65-second VSL. Opens with a normal coffee-and-bathroom routine, rewinds into earlier discomfort, explains the discovery, then returns to the opening routine. Useful script reference, but end-to-end AI production is especially uncertain because of product footage.')]
intro='''# GLP-1 constipation: AI UGC VSL shortlist

Live TrendTrack MCP refresh: September 8, 2026. This replaces the previous recommendation scope with human-presenter video sales letters. Native image ads, standalone character animation, anatomical-only animation and generic live-action-looking testimonials are excluded from the recommendation shortlist.

**Start with the failed-remedy cost breakdown and blunt peer/car-selfie VSL.** They have the best combined historical reuse and longevity among the screened likely-AI human-presenter candidates. Mechanism-first education is a longer test direction with weaker deployment evidence.

**AI classification:** TrendTrack did not supply model, generation-job or production provenance. These are visually screened **likely-AI candidates**, not certified fully AI productions. The inference comes from synthetic-looking character staging, recurring presenter representations across reenactments, rendering/label irregularities and constructed explanatory inserts. Those cues do not establish that every frame or the voice was generated. The requested strictly verified end-to-end AI category cannot be established with this data.

**Performance classification:** transcript usage is ad reuse, not ROAS. Longest running is the longest observed ad associated with that transcript in its query window, not a whole-family continuous run. These examples expose no usable reach, spend or conversion history. They should be described as recurrent/durable deployment references, not proven profitable winners. Older sample-ad status is distinguished from newer active uses.

## Ranked execution references

| Execution | Duration | Transcript uses | Longest run | Original sample status | Media |
|---|---:|---:|---:|---|---|
'''
data=[]
for label,title,ai,notes in chosen:
 x=r[label];scan=json.loads((P/'raw'/('scan-'+label+'.json')).read_text())['result']['structuredContent'];a=scan['data'];dur=float(json.loads((P/'media'/(label+'-probe.json')).read_text())['format']['duration'])
 intro+=f"| {title} | {dur:.0f}s | {x['usageCount']} | {x['longestRunning']} days | {a['status']} | [Watch]({x['sampleAd']['mediaUrl']}) |\n"
 data.append(dict(label=label,format=title,duration_seconds=round(dur,1),transcript_uses=x['usageCount'],longest_run_days=x['longestRunning'],sample_status=a['status'],ai_assessment=ai,media=x['sampleAd']['mediaUrl'],notes=notes))
intro+='''
All five references above are GLP-1 SOS. This is a focused brand-level result, not evidence of market-wide format leadership. The first three usage counts use the six-month transcript query; the last two use the one-year longevity query. Counts across different windows or near-identical transcripts must not be added together.

## What is active now

'''
for label,parent in [('A1','U1'),('A2','U1'),('A3','U3')]:
 x=r[label];scan=json.loads((P/'raw'/('scan-'+label+'.json')).read_text())['result']['structuredContent'];a=scan['data'];dur=float(json.loads((P/'media'/(label+'-probe.json')).read_text())['format']['duration'])
 intro+=f"- **{label}: {dur:.0f}s; active {a['daysRunning']} days.** "+('A newer presenter execution of the failed-remedy cost-breakdown script. The transcript is nearly identical to the older U1 reference. Its current presenter/footage provenance remains uncertain, so it demonstrates current script reuse, not verified all-AI production.' if parent=='U1' else 'The exact same media URL as the historical U3 car-selfie reference, now running under a new individual ad ID. This establishes current reuse of that creative, not 125 uninterrupted active days.')+f" [Watch]({a['media']['mediaUrl']}) · ad `{a['id']}`.\n"
intro+='\n## Sales structures and visual execution\n\n'
for label,title,ai,notes in chosen:
 intro+=f"### {title}\n\n{notes}\n\nAI assessment: {ai}; unverified. [Watch original]({r[label]['sampleAd']['mediaUrl']}) · [Inspected frame strip](media/{label}-sheet.jpg).\n\n"
intro+='''## Exclusions that matter

- The 40-use top transcript starts with a clay-style character. It is not human-presenter AI UGC and was excluded.
- The product-character and anatomical-only formats were excluded even when they had substantial reuse.
- The 148-second grandmother testimonial is active and has 13 uses in the six-month query, but its presenter looks like plausibly live-action footage. It was not used as evidence of purely AI UGC. A second hook variant reuses much of the same footage and was also excluded.
- The morning-routine reference includes footage that could be live action; retain it only as a script direction if fully synthetic production is a hard requirement.
- Glow&Conquer search results were mainly plateau/energy ads. They were not substituted for direct GLP-1 constipation evidence.

## Suggested test order

1. A 75–100-second failed-remedy breakdown, with a consistent AI presenter, specific attempts/costs, a supported product rationale, an ordinary-life outcome and a clear offer.
2. A 45–60-second blunt peer/car-selfie version of the same supported argument.
3. A 90–120-second mechanism-first kitchen VSL when the product has enough substantiated explanation to sustain it.

These are proposed test ranges informed by observed examples, not proven optimal lengths. Use verified product claims and truthful experience framing; the competitor transcripts contain strong medical claims that this research does not substantiate.

## Evidence and retrieval

Retrieved 50 transcript groups sorted by use in a six-month window, 30 sorted by longevity in a one-year window, and 30 from the live window. These are overlapping sets, not 110 unique VSLs. Screened 28 opening thumbnails, then inspected eight sampled frames and the full returned transcript for seven selected videos; three current executions were additionally sampled and individually scanned. Videos were not reviewed continuously end-to-end. Two current executions with identical historical media were not treated as new visual formats.

All source requests/responses, sampled frames, downloaded MP4s, transcripts and shortlist CSV are saved here. Search ranking behaved inconsistently: the current-rank requests returned descending positions despite requested ascending/best-rank semantics, so no current-rank winner claims are made. Current status was verified by individual scans. No generation workflow or model was invoked.
'''
(P/'REPORT.md').write_text(intro)
with (P/'shortlist.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI UGC VSL references</title><style>body{font:16px system-ui;background:#f7f8fa;color:#18222d;max-width:1180px;margin:40px auto;padding:0 20px}article{background:white;padding:22px;margin:22px 0;border-radius:12px}img{max-width:100%}p{line-height:1.6}a{color:#245ba0}video{max-height:600px;max-width:100%}</style><h1>GLP-1 constipation: AI UGC VSL candidates</h1><p>Likely AI production inferred from visual review; end-to-end production origin unverified. Historical deployment signals do not prove profitability. <a href="REPORT.md">Full report</a>.</p>']
for d in data:
 label=d['label'];parts.append(f'<article><h2>{html.escape(d["format"])}</h2><p>{d["duration_seconds"]}s · {d["transcript_uses"]} transcript uses · {d["longest_run_days"]} longest-running days · original ad {d["sample_status"]}</p><p>{html.escape(d["notes"])}</p><p><a href="{d["media"]}">Open original media</a></p><video controls preload="none" poster="media/{label}-frame0.jpg" src="media/{label}.mp4"></video><details><summary>Inspected frame strip</summary><img src="media/{label}-sheet.jpg" alt="Sampled video frames"></details></article>')
parts.append('<h2>Current script/media reuse</h2>')
for label in ['A1','A2','A3']:
 parts.append(f'<article><h3>{label}: active example</h3><p>Current production origin remains unverified. A3 reuses the exact historical car-selfie media.</p><a href="{r[label]["sampleAd"]["mediaUrl"]}">Open original media</a><p><video controls preload="none" poster="media/{label}-frame0.jpg" src="media/{label}.mp4"></video></p></article>')
parts.append('</html>');(P/'evidence.html').write_text('\n'.join(parts))
print('Created focused report, video gallery and CSV.')
