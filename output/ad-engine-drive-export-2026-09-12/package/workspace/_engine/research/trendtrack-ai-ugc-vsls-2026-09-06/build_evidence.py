import json,pathlib,hashlib,re,html
root=pathlib.Path(__file__).resolve().parent;r=root/'raw';brands=json.load(open(r/'brands.json'));bm={b['name']:b for b in brands}
def get(name,kind,ix):
 p=r/('nivara-transcripts-usage.json' if name=='Nivara Official' and kind=='usage' else bm[name]['id']+'-'+kind+'.json')
 a=json.load(open(p))['result']['structuredContent']['data'][ix]
 if kind=='current-video':
  t=a['content'].get('transcript') or ''
  try:j=json.loads(t);t=j.get('text') or ' '.join(q['text'] for q in j.get('segments',[]))
  except:pass
  return dict(fullText=t,sampleAd=dict(adId=a['id'],**a['media']),usageCount=None,longestRunning=a['daysRunning'],status=a['status'],rank=a.get('rank'))
 return a
spec=[
('N1','Nivara Official','usage',1,'Normal labs versus lived symptoms','ferravital'),('N2','Nivara Official','usage',8,'Heavy-period refill problem','ferrivital'),('N3','Nivara Official','usage',12,'Postpartum nurse advocate','ferrovital'),('N4','Nivara Official','longest',0,'Long-running ferritin-normal-range variant','ferravital'),('N5','Nivara Official','usage',4,'Turn-the-bottle-over buying guide','ferravital'),
('R1','Resilia','usage',0,'Expert dosing tutorial','resilia'),('R2','Resilia','usage',2,'Reverse-warning testimonial','resilia'),('R3','Resilia','usage',3,'Household discovery story','resilia'),('R4','Resilia','usage',5,'Profane transformation timeline','resilia'),
('L1','Lanural','usage',1,'Expert biofilm explanation','wanol'),('L2','Lanural','usage',3,'Incomplete-emptying personal story','la noral'),('L3','Lanural','usage',0,'Accidental garlic discovery','loneril'),
('G1','GLP-1 SOS Supplements','usage',1,'Failed-remedy expense ledger',None),('G2','GLP-1 SOS Supplements','usage',0,'Keep the weight loss; resolve the side effect','dlp-1 sos'),('G3','GLP-1 SOS Supplements','usage',6,'Grandmother restores daily life','glp-1 sos'),
('Z1','blog.zafiraorganics.com','longest',0,'Receptor-versus-supply explanation','zafira'),('Z2','blog.zafiraorganics.com','longest',1,'Weight-loss success with lost joy','zephira'),('Z3','blog.zafiraorganics.com','usage',0,'Six-side-effect article bridge',None),('Z4','blog.zafiraorganics.com','usage',2,'Personified cortisol explanation','zafira organics'),
('C1','CAVAÉ','usage',0,'Absorption-route argument','caviar melt'),('C2','CAVAÉ','longest',0,'Runner identity story',None),
('A1','avaRoot','usage',0,'Four rejected UTI remedies','avarut'),('A2','avaRoot','longest',2,'Sister-founded solution story','avaroot'),
('E1','Elvera','usage',0,'6:17 a.m. bathroom scene','elvera'),('E2','Elvera','usage',3,'Expert bacterial-signal argument',None),
('S1','Sculptique','usage',3,'Expert interview on kidney drainage','sculpteek'),('S2','Sculptique','usage',0,'Six-stage fear ladder','sculpteek'),
('U1','Nuora','usage',0,'Ingredient characters assemble a formula','nuora'),('U2','Nuora','usage',2,'Apology turns into discount reveal','nuara'),('U3','Nuora','current-video',0,'Patient-expert questions on recurring odor','nuora'),
('H1','Lymphoria','usage',5,'Social-reaction dialogue','lymphoria'),('H2','Lymphoria','longest',4,'Intimacy-and-cellulite narrative song','lymphoria'),
('P1','PiPi Tea','usage',0,'Practitioner fatigue explanation','ppt'),('P2','PiPi Tea','usage',1,'Partner retells practitioner explanation','ppt'),
('AR1','Arctic Goddess','usage',2,'Maternal identity restoration','arctic minerals'),('AR2','Arctic Goddess','longest',6,'Postpartum self-discovery','arctic goddess'),
('B1','go.blymeskinsystems.com','usage',0,'Ex-husband reunion curiosity story',None),('B2','go.blymeskinsystems.com','usage',2,'Wedding-photo identity restoration','balmy prime elixir'),
('SA1','Sanlava','usage',0,'Three formulation barriers','sanlava'),('NH1','Neural Health Report','usage',0,'Cracked-heel myth correction','sakureva'),('AU1','AuraVanna','usage',0,'Throat-lining character explains delivery route','esovera'),
('F1','ZEDE Paris','usage',4,'Travel capacity with polished appearance','zd paris'),('F2','Verano Hill','usage',1,'Luxury-price challenge and product demo','verano hill'),('F3','Vellatini','usage',0,'One-bag everyday usefulness',None),('F4','VESTIRSI','usage',3,'Three-year durability comparison','vestersi'),('F5','Bellaucci','usage',0,'Restock plus personal meaning','bella ucci'),('F6','Sarah & Stone','usage',4,'Vacation purchase becomes everyday bag','sarah and stone'),('F7','Nuamōre','usage',0,'Social-status watch framing','oceana'),('F8','Lux Boat Tote','usage',0,'Seasonal discovery and desire',None)
]
scans={}
for p in list(r.glob('*-scan.json'))+list(r.glob('*-scan2.json')):
 s=json.load(open(p))['result'].get('structuredContent',{});scans[s.get('adId')]=s
cases=[]
for cid,name,kind,ix,title,brandword in spec:
 a=get(name,kind,ix);t=a['fullText'];entry=dict(caseId=cid,brand=name,kind=kind,index=ix,title=title,brandtrackerId=bm[name]['id'],adId=a['sampleAd']['adId'],mediaUrl=a['sampleAd'].get('mediaUrl'),thumbnailUrl=a['sampleAd'].get('thumbnailUrl'),usageCount=a.get('usageCount'),longestRunning=a['longestRunning'],wordCount=len(t.split()),fullText=t)
 if brandword:
  m=re.search(re.escape(brandword),t,re.I)
  if m:entry['firstNamedProductWordFraction']=round(len(t[:m.start()].split())/len(t.split()),3)
 if entry['adId'] in scans:
  s=scans[entry['adId']];entry['individualStatus']=s['data']['status'];entry['individualScanVerdict']=s.get('analysis',{}).get('verdict')
 elif a.get('status'):entry['individualStatus']=a['status']
 cases.append(entry)
(r/'cases-internal.json').write_text(json.dumps(cases,indent=2))
(root/'evidence-index.json').write_text(json.dumps([{k:v for k,v in c.items() if k!='fullText'} for c in cases],indent=2))
coverage=[];rawrows=0
for b in brands:
 seen=set();rows=[];available=0
 for kind in ['usage','longest']:
  p=r/('nivara-transcripts-usage.json' if b['name']=='Nivara Official' and kind=='usage' else b['id']+'-'+kind+'.json')
  if not p.exists():continue
  s=json.load(open(p))['result'].get('structuredContent',{});available=max(available,s.get('pagination',{}).get('total',0))
  for a in s.get('data',[]):
   rawrows+=1;h=hashlib.sha256(a['fullText'].encode()).hexdigest()
   if h in seen:continue
   seen.add(h);rows.append(a)
 coverage.append(dict(brand=b['name'],id=b['id'],activeAds=b['counts']['activeAds'],availableGroups=available,retrievedDistinctGroups=len(rows),cases=[c['caseId'] for c in cases if c['brand']==b['name']]))
(root/'coverage.json').write_text(json.dumps(coverage,indent=2))
print(json.dumps({'trackedEntries':len(brands),'groupRows':rawrows,'distinctGroups':sum(x['retrievedDistinctGroups'] for x in coverage),'caseStudies':len(cases),'firstNamedProductFractions':[{k:c[k] for k in ['caseId','wordCount','firstNamedProductWordFraction'] if k in c} for c in cases if c['caseId'] in ['N1','N2','N3','R1','R3','L1','L2','G2','Z1','Z2','E1','S1','A1','C1']]}))
