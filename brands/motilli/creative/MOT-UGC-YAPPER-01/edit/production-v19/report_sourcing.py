from pathlib import Path
import json
O=Path(__file__).resolve().parent;J=O/'tiktok-sourcing';meta={}
for l in (J/'candidates_meta.jsonl').read_text().splitlines():
 m=json.loads(l);meta[m['video_id']]=m
rows=[]
for vfile in sorted((J/'candidates/B17').glob('*.mp4')):
 f=J/'verdicts'/(vfile.stem+'.json');v=json.loads(f.read_text()) if f.exists() else {'match':False,'status':'model response pending','direct_screening':'Text-bearing kitchen/pantry action, wrong toilet context.'};m=meta.get(vfile.stem,{});rows.append({'id':vfile.stem,'url':m.get('url'),'creator':m.get('author'),'source_query':m.get('source_key'),'local_file':str(vfile),'visual_review':v,'reuse_rights':'unverified'})
assert len(rows)==70;assert not any(r['visual_review'].get('match') for r in rows)
(J/'sourcing-ledger.json').write_text(json.dumps(rows,indent=2));closest=next(r for r in rows if r['id']=='7586638932775849238');(O/'closest-captioned-source.json').write_text(json.dumps(closest,indent=2));model_count=len(list((J/'verdicts').glob('*.json')))
report=f'''# V19 toilet-cramping sourcing — no clean selection

Target: B17, “Backed up, uncomfortable, just waiting.” V18 frames 2779–2856, 92.633333–95.200000 seconds. Latest V18 Michelle voice, alignment and final ad remain unchanged.

Three search rounds, eight query families, 70 distinct downloaded TikToks. Every candidate submitted to the Gemini motion gate; {model_count} responses saved at report time. All 70 inspected directly via four sampled frames per candidate on 13 contact pages. No verified match meeting the action, intensity, rawness and clean 2.566667-second interval requirements. No every-frame clean certification claimed for any clip.

Closest action lead: https://www.tiktok.com/@holly_swindale/video/7586638932775849238

The woman is visibly seated in a bathroom stall, hunched forward with a tightly pinched expression; model review identifies abdomen bracing and sustained distress around 1–5 seconds. Full-resolution frame at 2.5 seconds directly inspected. Persistent “POV you have IBS and the cramps are cramping” text plus a smaller caption and visible clothing lettering fail the no-text requirement. Entry EV 5, peak EV 5 and rawness 5 are editorial model ratings, not a diagnosis or authenticity claim. Source retained as a decision lead, not a qualified selection. Rights unverified.

No source text cropped, covered, blurred or inpainted. No generated substitute. No V19 timeline, final export or selected Cut Room replacement created. Resolve live access succeeded and V18 was verified as 9,431 frames with 26 covering scenes. To proceed requires a clean source or user direction allowing original TikTok captions for this insert.

Full rejected-candidate record: tiktok-sourcing/sourcing-ledger.json. Original files and source metadata retained.
''';(O/'sourcing-report.md').write_text(report)
(O/'production-status.json').write_text(json.dumps({'status':'awaiting_source_or_text_preference','latest_completed_version':18,'requested_beat':'B17','timeline_frames':[2779,2856],'candidates_directly_screened':70,'model_responses':model_count,'qualified_clean_sources':0,'closest_captioned_source':closest['url'],'edit_changed':False,'final_export_created':False},indent=2))
f=O.parent/'editing-plan.md';s=f.read_text();marker='V19 sourcing result: three rounds / eight search terms'
if marker not in s:s+='\n\n'+marker+f' yielded 70 distinct downloaded sources. All were submitted for model motion review ({model_count} responses saved at report time) and directly screened through four sampled frames each. No verified clean match. Closest real toilet-cramping source is @holly_swindale/7586638932775849238, but persistent captions and clothing lettering fail the clean-source requirement. Full-resolution 2.5-second frame reviewed; source retained as a decision lead, not selected. No V19 edit/export or Cut Room replacement claimed. V18 unchanged. Native Resolve baseline access verified. Continue with a clean source or user direction accepting source text. Detailed ledger and report saved in production-v19.\n';f.write_text(s)
print('70 sources screened;',model_count,'model responses; zero clean matches; V18 unchanged.')
