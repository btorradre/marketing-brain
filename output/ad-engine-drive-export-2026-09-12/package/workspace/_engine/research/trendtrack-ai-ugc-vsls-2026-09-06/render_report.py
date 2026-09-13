import json,pathlib,re,html,markdown
root=pathlib.Path(__file__).resolve().parent
cases=json.load(open(root/'evidence-index.json'));cm={c['caseId']:c for c in cases};coverage=json.load(open(root/'coverage.json'))
visual=[]
for name in ['video-manifest.json','video-manifest-extra.json']:
 visual+=json.load(open(root/'visual-review'/name))
vm={x['ad']['adId']:x for x in visual if not x.get('error')}
thumbs=json.load(open(root/'visual-review/thumbnail-manifest.json'));tm={x['ad']['adId']:x for x in thumbs if 'path' in x}
def link(cid):return '['+cid+': media]('+cm[cid]['mediaUrl']+')'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(str(v).replace('|','/') for v in row)+' |\n' for row in rows)
intro=[]
for cid in ['N1','N2','N3','R1','R3','L1','L2','G2','Z1','Z2','C1','A1','E1','S1']:
 c=cm[cid];intro.append([c['brand'],c['title'],c['wordCount'],str(round(c['firstNamedProductWordFraction']*100))+'%',link(cid)])
coverage_rows=[]
for c in coverage:
 coverage_rows.append([c['brand'],c['activeAds'],c['availableGroups'],c['retrievedDistinctGroups'],', '.join(link(cid) for cid in c['cases']) or 'No eligible completed transcript returned'])
evidence=[]
for c in cases:
 evidence.append([c['caseId'],c['brand']+' — '+c['title'],c.get('usageCount') if c.get('usageCount') is not None else 'not a grouped row',c['longestRunning'],c.get('individualStatus','not individually checked'),link(c['caseId'])+' / [thumbnail]('+c['thumbnailUrl']+')'])
scans=[]
for c in cases:
 if 'individualScanVerdict' in c:scans.append([c['brand'],c['caseId'],c['individualStatus'],c['individualScanVerdict'].replace('**',''),link(c['caseId'])])
s=(root/'report-draft.md').read_text();s=s.replace('{{INTRO_TABLE}}',table(['Brand','Example','Transcript words','First branded-name word position','Source'],intro));s=s.replace('{{COVERAGE_TABLE}}',table(['Tracked entry','Reported active ads','Available groups, six months','Distinct groups retrieved','Selected cases'],coverage_rows));s=s.replace('{{EVIDENCE_TABLE}}',table(['Case','Example','Grouped uses','Longest observed days','Individual status','Source'],evidence));s=s.replace('{{SCAN_TABLE}}',table(['Brand','Case','Status','TrendTrack individual-ad verdict','Source'],scans))
s=re.sub(r'\{([A-Z]+\d+)\}',lambda m:link(m.group(1)),s)
start=json.load(open(root/'raw/usage-start.json'))['credits']['totalRemaining'];end=json.load(open(root/'raw/usage-end.json'))['credits']['totalRemaining']
s+='\nAPI credit balance at start: '+str(start)+'. At completion: '+str(end)+'. This research used '+str(start-end)+' credits. The authentication key was held in memory and is not stored in these research artifacts.\n'
(root/'AI-UGC-VSL-BREAKDOWN.md').write_text(s)
css='''*{box-sizing:border-box}body{margin:0;background:#f5f3ee;color:#202722;font:17px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1120px;margin:auto;padding:48px 32px 80px}h1{font-size:42px;line-height:1.15;max-width:900px;color:#173b30}p{margin:20px 0}p>strong:first-child{color:#173b30}a{color:#195d7a;text-underline-offset:3px}table{width:100%;border-collapse:collapse;font-size:14px;background:white;margin:22px 0;display:block;overflow-x:auto}th{background:#173b30;color:white;text-align:left;white-space:nowrap}td,th{padding:12px 14px;border-bottom:1px solid #ddd;vertical-align:top}tr:nth-child(even){background:#f4f7f4}li{margin:12px 0}.nav{display:flex;gap:20px;flex-wrap:wrap;border-bottom:1px solid #c7cec7;padding-bottom:20px}.label{font-size:12px;text-transform:uppercase;letter-spacing:.15em;color:#496359}.card{background:white;border:1px solid #d5ddd7;border-radius:12px;padding:22px;margin:20px 0}.thumb{width:150px;max-height:230px;object-fit:contain;float:right;margin:0 0 15px 22px}.timeline{width:100%;height:auto;border-radius:5px;margin-top:16px}.meta{font-size:14px;color:#59645d}.card:after{content:"";display:block;clear:both}input{width:100%;padding:15px;font:inherit;border:1px solid #9eb5a8;border-radius:8px;background:white}button{font:inherit}details{margin:14px 0}summary{cursor:pointer;color:#195d7a}@media(max-width:650px){main{padding:28px 16px}h1{font-size:30px}.thumb{width:100px}table{font-size:12px}}@media print{body{background:white}main{padding:0}.nav,input{display:none}table{display:table;font-size:10px}a{color:inherit}.card{break-inside:avoid}}'''
def page(title,body,extra=''):
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+css+'</style></head><body><main><div class="label">TrendTrack research · September 6, 2026</div><nav class="nav"><a href="AI-UGC-VSL-BREAKDOWN.html">Full analysis</a><a href="evidence-gallery.html">49-case evidence gallery</a><a href="AI-UGC-VSL-BREAKDOWN.md">Markdown report</a></nav>'+body+'</main>'+extra+'</body></html>'
(root/'AI-UGC-VSL-BREAKDOWN.html').write_text(page('AI UGC VSL breakdown',markdown.markdown(s,extensions=['tables'])))
body='<h1>Ad evidence library</h1><p>49 selected examples from all 29 tracked entries. Search by brand, case, or structure. Grouped reuse and longevity are deployment signals, not proof of profitable scale. Speaker and AI-production provenance are unverified.</p><p class="meta">17 downloaded videos have five sampled frames each. Frame strips show composition at selected moments, not a continuous playback review.</p><input id="filter" type="search" aria-label="Filter evidence by brand or structure" placeholder="Search Nivara, expert, story, checklist…"><p id="count" class="meta">49 cases</p>'
for c in cases:
 cid=c['caseId'];v=vm.get(c['adId']);thumb=tm.get(c['adId']);img=str(pathlib.Path(thumb['path']).relative_to(root)) if thumb else c['thumbnailUrl'];title=cid+' · '+c['brand']+' · '+c['title'];status=c.get('individualStatus','not individually checked')
 body+='<article class="card" data-search="'+html.escape(title.lower(),quote=True)+'"><img class="thumb" loading="lazy" src="'+html.escape(img,quote=True)+'" alt="'+html.escape(c['brand']+' ad reference thumbnail',quote=True)+'"><strong>'+html.escape(title)+'</strong><p class="meta">Grouped uses: '+str(c.get('usageCount') if c.get('usageCount') is not None else 'n/a')+' · Longest observed run: '+str(c['longestRunning'])+' days · '+str(c['wordCount'])+' transcript words<br>Representative-ad status: '+html.escape(status)+'</p>'
 if 'individualScanVerdict' in c:body+='<p class="meta">'+html.escape(c['individualScanVerdict'].replace('**',''))+'</p>'
 body+='<p><a href="'+html.escape(c['mediaUrl'],quote=True)+'" target="_blank" rel="noopener">Open source video</a> · <a href="'+html.escape(c['thumbnailUrl'],quote=True)+'" target="_blank" rel="noopener">Source thumbnail</a></p>'
 if v:
  video=str(pathlib.Path(v['videoPath']).relative_to(root));timeline=str(pathlib.Path(v['timelinePath']).relative_to(root));body+='<p><a href="'+html.escape(video,quote=True)+'">Open preserved local video</a> · '+str(round(v['duration'],1))+' seconds</p><details><summary>Inspect five sampled frames</summary><img class="timeline" loading="lazy" src="'+html.escape(timeline,quote=True)+'" alt="Five sampled video frames with timestamps"></details>'
 body+='</article>'
js='''<script>const field=document.getElementById('filter');const cards=[...document.querySelectorAll('.card')];field.addEventListener('input',()=>{const q=field.value.trim().toLowerCase();let n=0;for(const c of cards){const show=c.dataset.search.includes(q);c.hidden=!show;if(show)n++;}document.getElementById('count').textContent=n+' cases';});</script>'''
(root/'evidence-gallery.html').write_text(page('VSL evidence gallery',body,js))
print(json.dumps({'reportWords':len(s.split()),'cases':len(cases),'scanCases':len(scans),'sampledVideos':len(vm),'creditsUsed':start-end,'files':['AI-UGC-VSL-BREAKDOWN.md','AI-UGC-VSL-BREAKDOWN.html','evidence-gallery.html']}))
