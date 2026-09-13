import json,re,csv,hashlib,sqlite3,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'database';OUT.mkdir(exist_ok=True)
THEMES={
'new_brand':r'new brand|niche brand|underrated|under.rated|never heard|discover|gatekeep|gate.keep|lesser.known|brand.{0,15}know|where.{0,15}buy|what brand|which brand',
'founder':r'founder|founded|started.{0,20}brand|created.{0,15}bag|small business|small brand|business owner',
'designer_spend':r'overpric|over.pric|expensive|thousand|price|afford|cost|budget|money|worth|spend|paying|paid|dollar',
'old_money':r'old.money|timeless|classic|classy|elegan|quiet.luxury|sophisticat|rich aunt|look.{0,12}rich|wealth',
'european_style':r'europe|paris|parisian|milan|french|italian|scandinav|london|toteme|pol[eè]ne|moynat',
'euro_trip':r'paris|milan|london|europe|trip|travel|vacation|holiday|airport|suitcase|luggage|flight|flying|carry.on',
'outfit_upgrade':r'outfit|look.{0,16}expensive|elevat|polish|put.together|style|stylish|chic|wardrobe|dress',
'social_judgment':r'judg|approv|men |man |boyfriend|husband|attract|impress|compliment|confidence|confident|opinion|what.{0,12}think',
'markup_skepticism':r'scam|rip.off|ripoff|markup|mark.up|marketing|profit|manufactur|factor|cost.{0,12}mak|same.{0,15}factor|overpric|over.pric|price.hike',
'quality_material':r'quality|leather|suede|craft|stitch|material|durab|peel|scratch|heavy|weight|lining|zipper|zip|hardware|plastic|nylon|wool|vegan',
'logo_independence':r'logo|brand.name|no.brand|loud|understat|recogniz|recognis|quiet|same.{0,12}bag|every.{0,12}carrying|basic',
'seasonal_woven':r'raffia|woven|straw|summer|fall|autumn|winter|season|basket',
'work_polish':r'work.bag|office|laptop|commut|professional|briefcase|backpack|work tote|business trip',
'travel_scale':r'travel|trip|weekend|duff|carry.on|airport|luggage|suitcase|pack|big.bag|large.bag|oversiz|fit|size|space|spacious',
'gifting':r'gift|birthday|christmas|anniversary|present for|bought.{0,15}(wife|mum|mom|mother|husband)',
'purchase_trigger':r'sold.out|restock|stock|waitlist|new.colou?r|new.drop|new.arrival|limited|sale|discount|shipping|deliver|return|review|order|bought|buying'
}
def tags(s):return [k for k,p in THEMES.items() if re.search(p,s or '',re.I)]
def key(url,platform='instagram'):
 if platform=='instagram':
  m=re.search(r'/(?:p|reel|reels)/([^/?]+)',url or '');return 'ig:'+m.group(1) if m else ''
 m=re.search(r'/video/(\d+)',url or '');return 'tt:'+m.group(1) if m else ''
def read(name):
 p=ROOT/'raw'/name;return json.loads(p.read_text()) if p.exists() else []
seeds=json.loads((ROOT/'seeds.json').read_text());seedmap={key(x['url'],x['platform']):x for x in seeds if x['platform'] in ['instagram','tiktok']}
posts={};errors=[]
for f in sorted((ROOT/'raw').glob('*items.json')):
 if 'comment' in f.name:continue
 for i,r in enumerate(json.loads(f.read_text())):
  platform='tiktok' if 'tiktok' in f.name else 'instagram';url=r.get('url') or r.get('webVideoUrl') or r.get('inputUrl') or '';pk=key(url,platform)
  if not pk and r.get('shortCode'):pk='ig:'+r['shortCode'];url='https://www.instagram.com/p/'+r['shortCode']+'/'
  if not pk or not (r.get('shortCode') or r.get('id')):errors.append({'file':f.name,'row':i,'input':r.get('inputUrl') or r.get('url'),'error':r.get('error'),'description':r.get('errorDescription')});continue
  p=posts.setdefault(pk,{'post_id':pk,'platform':platform,'url':url,'caption':'','transcript':'','creator':'','published_at':'','likes':0,'comments_reported':0,'views':0,'waves':[],'raw_refs':[],'seed_id':seedmap.get(pk,{}).get('seed_id',''),'seed_notes':seedmap.get(pk,{}).get('notes','')})
  p['waves'].append(f.name.split('-items')[0]);p['raw_refs'].append(f'raw/{f.name}#row={i}')
  if r.get('caption') or r.get('text'):p['caption']=r.get('caption') or r.get('text')
  if r.get('transcript'):p['transcript']=str(r['transcript'])
  p['creator']=r.get('ownerUsername') or r.get('authorMeta',{}).get('name') or p['creator'];p['published_at']=r.get('timestamp') or r.get('createTimeISO') or p['published_at']
  p['likes']=r.get('likesCount',r.get('diggCount',p['likes'])) or 0;p['comments_reported']=r.get('commentsCount',r.get('commentCount',p['comments_reported'])) or 0;p['views']=r.get('videoPlayCount',r.get('playCount',p['views'])) or 0
  p['media_type']=r.get('type','Video');p['paid_partnership']=bool(r.get('paidPartnership') or r.get('isSponsored') or r.get('isAd'))
  p['input_url']=r.get('inputUrl') or r.get('searchQuery') or p.get('input_url','')
for p in posts.values():
 s=p['caption']+' '+p['transcript'];p['theme_tags']=tags(s)
 p['category']='handbag_context' if re.search(r'\b(bags?|handbags?|purses?|totes?|weekenders?|duffels?|duffles?|birkin|herm[eè]s|luggage|backpack|satchel|briefcase)\b',s,re.I) else 'adjacent_fashion_or_other'
 p['category_method']='lexical screening of creator caption/transcript; review source before bag-specific claims'
 p['transcript_status']='automatic_unverified' if p['transcript'] else 'not_available';p['retrieved_at']='2026-09-11'
comments={}
def add(r,f,i,pk=None,embedded=False):
 platform='tiktok' if 'tiktok' in f else 'instagram';url=r.get('postUrl') or r.get('videoWebUrl') or r.get('submittedVideoUrl') or '';pk=pk or key(url,platform)
 if not pk or not r.get('text'):return
 cid=str(r.get('id') or r.get('cid') or hashlib.sha256((pk+r['text']).encode()).hexdigest()[:20]);cid=('ttc:' if platform=='tiktok' else 'igc:')+cid
 author=r.get('ownerUsername') or r.get('uniqueId') or '';p=posts.get(pk,{})
 if cid in comments:
  comments[cid]['raw_refs'].append(f'raw/{f}#row={i}'+('#latestComments' if embedded else ''));comments[cid]['waves']=sorted(set(comments[cid]['waves']+[f.split('-items')[0]]));return
 txt=r['text'];words=re.findall(r'[\w]+',txt.lower());clean=' '.join(words)
 link_vocab={'link','links','bag','bags','shop','shopping','please','pls','plz','me','send','can','you','the','a','to','i','want','need','it','now','for','this','these','thank','thanks','fall','summer','accessories','cool','clothes','outfits','outfit','info','details','dm','yes','winter','travel','fashion','finds','europe','euro','european','all','and','of','them','would','love','get','have','your','collection','elites','elite','set'}
 if not words:signal='emoji_only'
 elif len(words)<=12 and set(words)<=link_vocab:signal='link_request_or_prompt_keyword'
 elif len(words)<=3:signal='short_reaction'
 elif re.search(r'check.{0,12}(profile|bio)|dm.{0,15}(promot|collab)|promot.{0,10}it',txt,re.I):signal='possible_promotion'
 elif re.search(r'@[\w.]+',txt) and re.search(r'recommend|got mine|bought|quality|shipping|customer support|check out|follow|support',txt,re.I):signal='possible_commercial_promotion'
 elif re.search(r'support.{0,30}(following|liking)|my page|check out our|small side journey',txt,re.I):signal='possible_commercial_promotion'
 else:signal='substantive_candidate'
 own=author.lower()==p.get('creator','').lower() and bool(author)
 comments[cid]={'comment_id':cid,'post_id':pk,'platform':platform,'text':txt,'author':author,'source_url':r.get('commentUrl') or p.get('url') or url,'locator_type':'comment_permalink' if r.get('commentUrl') else 'post_url_plus_comment_id','published_at':r.get('timestamp') or r.get('createTimeISO') or '', 'likes':r.get('likesCount',r.get('diggCount',0)) or 0,'signal_class':signal,'evidence_role':'creator_reply' if own else 'audience_comment_purchase_unverified','theme_tags':tags(txt),'context_tags':p.get('theme_tags',[]),'category':p.get('category','unknown'),'seed_id':p.get('seed_id',''),'waves':[f.split('-items')[0]],'raw_refs':[f'raw/{f}#row={i}'+('#latestComments' if embedded else '')],'self_reported_purchase':bool(re.search(r'\b(i bought|i own|i have|my bag|ordered mine|purchased)\b',txt,re.I)),'retrieved_at':'2026-09-11'}
for f in sorted((ROOT/'raw').glob('*comment*-items.json')):
 for i,r in enumerate(json.loads(f.read_text())):add(r,f.name,i)
for f in sorted((ROOT/'raw').glob('*items.json')):
 if 'comment' in f.name or 'tiktok' in f.name:continue
 for i,r in enumerate(json.loads(f.read_text())):
  pk=key(r.get('url') or r.get('inputUrl') or '')
  for c in r.get('latestComments',[]) or []:add(c,f.name,i,pk,True)
# Exact textual repeats are a separate warning, never counted as distinct phrasing.
freq=collections.Counter(re.sub(r'\s+',' ',x['text'].strip().lower()) for x in comments.values())
for c in comments.values():c['same_text_count']=freq[re.sub(r'\s+',' ',c['text'].strip().lower())]
for p in posts.values():
 cs=[c for c in comments.values() if c['post_id']==p['post_id']];p['comments_collected']=len(cs);p['substantive_candidates']=sum(c['signal_class']=='substantive_candidate' and c['evidence_role']!='creator_reply' for c in cs)

def export(name,rows):
 (OUT/(name+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 if rows:
  with (OUT/(name+'.csv')).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)
export('posts',list(posts.values()));export('comments',list(comments.values()));export('collection_errors',errors)
status=[]
for s in seeds:
 p=posts.get(key(s['url'],s['platform']),{});status.append({**s,'status':'retrieved' if p else 'not_retrieved','post_id':p.get('post_id',''),'actual_creator':p.get('creator',''),'category':p.get('category',''),'comments_collected':p.get('comments_collected',0),'transcript_status':p.get('transcript_status','not_available')})
export('seed_register',status)
export('discovered_posts',[p for p in posts.values() if not p['seed_id']])
con=sqlite3.connect(OUT/'velantra-voc.sqlite')
for name,rows in [('posts',list(posts.values())),('comments',list(comments.values())),('seed_register',status)]:
 con.execute('DROP TABLE IF EXISTS '+name)
 if not rows:continue
 fields=list(rows[0]);con.execute('CREATE TABLE '+name+' ('+','.join('"'+k+'" TEXT' for k in fields)+')')
 con.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in fields)+')',[[json.dumps(r.get(k),ensure_ascii=False) if isinstance(r.get(k),(list,dict)) else r.get(k) for k in fields] for r in rows])
con.execute('CREATE INDEX IF NOT EXISTS comment_post_idx ON comments(post_id)');con.commit();con.close()
stats={'posts':len(posts),'posts_by_platform':dict(collections.Counter(p['platform'] for p in posts.values())),'comments':len(comments),'comments_by_platform':dict(collections.Counter(c['platform'] for c in comments.values())),'signal_classes':dict(collections.Counter(c['signal_class'] for c in comments.values())),'categories':dict(collections.Counter(p['category'] for p in posts.values())),'transcripts':sum(bool(p['transcript']) for p in posts.values()),'audience_substantive_bag_candidates':sum(c['signal_class']=='substantive_candidate' and c['category']=='handbag_context' and c['evidence_role']!='creator_reply' for c in comments.values()),'seed_retrieved':sum(s['status']=='retrieved' for s in status)}
(OUT/'summary.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
(ROOT/'taxonomy.json').write_text(json.dumps(THEMES,indent=2))
