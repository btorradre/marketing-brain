import json,re
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cohort-review'
qs=json.loads((ROOT/'report/quote-audit.json').read_text());cs={c['comment_id']:c for c in map(json.loads,(ROOT/'database/comments.jsonl').read_text().splitlines())};ps={p['post_id']:p for p in map(json.loads,(ROOT/'database/posts.jsonl').read_text().splitlines())}
doc=pymupdf.open(ROOT/'report/Velantra-Voice-of-Customer-100-Pages.pdf');text=[p.get_text() for p in doc]
records=[]
for i,q in enumerate(qs,1):
 c=cs[q['comment_id']];p=ps[c['post_id']];pages=[i+1 for i,t in enumerate(text) if q['comment_id'] in t]
 records.append({'review_id':f'Q{i:03}', 'comment_id':q['comment_id'],'post_id':q['post_id'],'report_pages':pages,'full_text':c['text'],'excerpt':q['excerpt'],'source_url':c['source_url'],'creator':p['creator'],'caption':p['caption'],'author':c['author'],'published_at':c['published_at']})
(OUT/'quote-review-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
for start in range(0,100,10):
 (OUT/f'report-pages-{start+1:03}-{start+10:03}.txt').write_text('\n\n'.join('PAGE '+str(i+1)+'\n'+text[i] for i in range(start,start+10)))
for start in range(0,len(records),60):
 packet=[]
 for r in records[start:start+60]:packet.append(f"{r['review_id']} | {r['comment_id']} | {r['post_id']} | pp {','.join(map(str,r['report_pages']))} | @{r['creator']}\nFULL COMMENT: {r['full_text']}\n")
 (OUT/f'quotes-{start+1:03}-{min(start+60,len(records)):03}.txt').write_text('\n'.join(packet))
print('Prepared 100 report pages and 603 full-comment records. No automatic cohort assignments.')
