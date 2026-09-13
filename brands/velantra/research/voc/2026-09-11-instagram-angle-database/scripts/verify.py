import json,re,sqlite3,collections,hashlib
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'database';R=ROOT/'report'
cs={c['comment_id']:c for c in map(json.loads,(DB/'comments.jsonl').read_text().splitlines())};ps={p['post_id']:p for p in map(json.loads,(DB/'posts.jsonl').read_text().splitlines())};qs=json.loads((R/'quote-audit.json').read_text());seeds=[json.loads(x) for x in (DB/'seed_register.jsonl').read_text().splitlines()]
assert len(cs)==16437 and len(ps)==643 and len(seeds)==167
assert all(c['post_id'] in ps for c in cs.values())
assert len(qs)==len({q['comment_id'] for q in qs})==603
assert all(q['exact_contiguous'] and q['excerpt'] in cs[q['comment_id']]['text'] and 0<q['words']<=24 for q in qs)
cache={};rawchecks=0
for q in qs:
 c=cs[q['comment_id']];ref=c['raw_refs'][0];m=re.match(r'(.*?)#row=(\d+)(.*)',ref);file=m[1];idx=int(m[2]);cache.setdefault(file,None)
 if cache[file] is None:cache[file]=json.loads((ROOT/file).read_text())
 raw=cache[file][idx]
 if '#latestComments' in ref:assert any(x.get('text')==c['text'] and str(x.get('id'))==c['comment_id'].split(':',1)[1] for x in raw.get('latestComments',[]))
 else:assert raw.get('text')==c['text']
 rawchecks+=1
con=sqlite3.connect(DB/'velantra-voc.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert con.execute('SELECT count(*) FROM comments').fetchone()[0]==len(cs);assert con.execute('SELECT count(*) FROM angles').fetchone()[0]==16
n=con.execute('SELECT count(*) FROM comment_search WHERE comment_search MATCH ?',('"never heard" OR leather',)).fetchone()[0];assert n>0;con.close()
doc=pymupdf.open(R/'Velantra-Voice-of-Customer-100-Pages.pdf');assert len(doc)==100
outside=[];links=0
for i,p in enumerate(doc):
 links+=len(p.get_links())
 for b in p.get_text('blocks'):
  if b[0]<40 or b[2]>572 or b[1]<20 or b[3]>775:outside.append({'page':i+1,'bbox':b[:4]})
assert not outside,outside[:3]
(R/'qa').mkdir(exist_ok=True)
for npage in [1,3,9,10,12,26,38,40,41,58,80,90,91,96,100]:doc[npage-1].get_pixmap(matrix=pymupdf.Matrix(1.2,1.2)).save(R/'qa'/f'page-{npage:03}.png')
manifest=json.loads((ROOT/'collection-manifest.json').read_text());assert all(x['status']=='SUCCEEDED' for x in manifest['runs'])
ver={'status':'passed','pdf_pages':len(doc),'pdf_words':sum(len(p.get_text().split()) for p in doc),'pdf_links':links,'out_of_bounds_text_blocks':outside,'distinct_report_quotes':len(qs),'exact_quote_checks':rawchecks,'comment_post_joins':'all resolve','sqlite_integrity':'ok','fts_sample_query_results':n,'seed_accounting':dict(collections.Counter(s['status'] for s in seeds)),'minimum_layout_scale':min(x['scale'] for x in json.loads((R/'layout-qa.json').read_text())),'reported_actor_usd':manifest['total_reported_actor_usd'],'limits':['Automatic transcripts not audio-verified','Lexical tags are candidates, not validated prevalence','No campaign conversion evidence','Two Instagram and two external seed links unavailable']}
(R/'verification.json').write_text(json.dumps(ver,indent=2));print(json.dumps(ver,indent=2))
with (ROOT/'checksums.sha256').open('w') as f:
 for p in sorted(ROOT.rglob('*')):
  if p.is_file() and p.suffix in ['.json','.jsonl','.csv','.sqlite','.pdf','.md','.html','.js'] and 'qa' not in p.parts:f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n')
