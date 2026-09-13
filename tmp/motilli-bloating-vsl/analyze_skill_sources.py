from pathlib import Path
import json,re
out=Path('_engine/research/vsl-structure-voice-2026-09-09')
count=lambda s:len(re.findall(r"\b\w+(?:['’’-]\w+)*\b",s))
rows=json.loads((out/'motilli-sections.json').read_text())
mot=[r.copy() for r in rows if r['beat'] not in ['H2','H3']]
groups={'H1':'Hook','AGITATION':'Agitation / twist','TWIST':'Agitation / twist','CURIOSITY LOOP':'Renewed curiosity','DISCOVERY':'Discovery / authority','UMP':'UMP','PRIOR SOLUTIONS':'Prior solutions','DM BEAT':'Solution search / criteria','DOC RESPONSE':'Solution search / criteria','BACK TO GROUP':'Solution search / criteria',"WOMAN'S RECOMMENDATION":'Solution search / criteria','UMS 1':'UMS','UMS 2':'UMS','UMS 3':'UMS','MYTH-BUST':'Formulation / selection','NO COMPANY HAD DONE IT':'Formulation / selection','PRODUCT REVEAL':'Product / brand','ROUTINE':'Routine','FUTURE PACING':'Outcome / emotional payoff','SCARCITY':'Scarcity','GUARANTEE + CTA':'Offer / guarantee / CTA'}
for r in mot:r['group']=groups[r['beat']]
# Split the user's long outcome section into its actual changes in thought.
fp=next(r for r in mot if r['beat']=='FUTURE PACING')
anchors=[('Initial disappointment','And the first week'),('First everyday improvement','Then around week two'),('Morning improvement','By week three'),('Practical test','And the real test'),('Before/now callback','So that was me two months'),('Restored everyday life','I get through dinner'),('Meaning and reason to share','And I know the shot')]
idx=mot.index(fp)
parts=[]
for i,(name,a) in enumerate(anchors):
 start=fp['copy'].index(a)
 end=fp['copy'].index(anchors[i+1][1]) if i+1<len(anchors) else len(fp['copy'])
 copy=fp['copy'][start:end].strip()
 parts.append(dict(beat=name,group=fp['group'],copy=copy,words=count(copy)))
mot[idx:idx+1]=parts
n=(out/'nuora-ocr-working.txt').read_text()
# Repair obvious OCR errors only. Mask genuinely obscured words rather than invent them.
n=n.replace('iteralvrafusing','literally refusing').replace('Ifyou','If you').replace('gut, © 4 ~ othing to','gut, [obscured] to').replace('biofilm =" = tee gut','biofilm [obscured] gut')
n=re.sub(r'Itwas always me, but just slipping intott.*?So that was me three months', '[obscured sentence about clothing and meals] So that was me three months', n)
n=n.replace("So I'l drop", "So I'll drop")
n=n.replace('to be She sent a link' ,'to be [obscured]. She sent a link').replace(' +','')
(out/'nuora-transcript-working.txt').write_text('OCR-derived working transcription; some source words obscured. Not an exact audio transcript.\n\n'+n+'\n')
na=[
('Transformation and hidden-layer hook',"Here's how I went",'Hook'),
('Private stakes, prior attempts and twist',"So last year's",'Agitation / twist'),
('Second promise and social-proof claim','But in the next thirty seconds','Renewed curiosity'),
('Renewed concrete embarrassment','But before I do','Agitation / twist'),
('Forum practitioner discovery','So, of course','Discovery / authority'),
('Plaque analogy and causal explanation','If you take your tongue','UMP'),
('Recognition and solution question','So my mind started racing','Solution search / criteria'),
('Milan research authority','She explained that a research team','Solution search / criteria'),
('Tested-alternatives rejection','Probiotics?','Prior solutions'),
('Pineapple and bromelain role','You know the tingly','UMS'),
('Practical dose obstacle and processing','But there was a problem','Formulation / selection'),
('Remaining symptom and berberine role','I was thinking','UMS'),
('Why other formulations miss a piece','So most companies skip','Formulation / selection'),
('Others recover everyday activities','But the women that know','Outcome / emotional payoff'),
('Unnamed company / product route','She sent a link','Product / brand'),
('Expectation setting','But this isn\'t a magic pill','Outcome / emotional payoff'),
('Skepticism, purchase and first-week disappointment','I brushed it off','Outcome / emotional payoff'),
('First small changes and later practical results','Then week two','Outcome / emotional payoff'),
('Before/now and reason to share','So that was me three months','Outcome / emotional payoff'),
('First spoken brand name','So the company from the forum','Product / brand'),
('Directions',"It's two capsules",'Routine'),
('Batch availability and spare bottles','The only problem is the freeze','Scarcity'),
('Invitation, guarantee and CTA',"So I'll drop",'Offer / guarantee / CTA')]
nu=[]
for i,(beat,a,g) in enumerate(na):
 start=n.index(a)
 end=n.index(na[i+1][1]) if i+1<len(na) else len(n)
 copy=n[start:end].strip()
 words=count(re.sub(r'\[[^]]*\]','',copy))
 nu.append(dict(beat=beat,group=g,copy=copy,words=words))
def timing(rs):
 total=sum(r['words'] for r in rs)
 t=0
 for r in rs:
  r.update(start_sec=t*60/155,duration_sec=r['words']*60/155,start_pct=t/total*100,share_pct=r['words']/total*100)
  t+=r['words']
 return total
mt,nt=timing(mot),timing(nu)
(out/'annotated-beats.json').write_text(json.dumps({'method':'Text-only estimates at 155 wpm, without pauses; Nuora OCR approximate; H1 only for Motilli; primary spans exclusive, proof may recur as secondary function.','motilli':mot,'nuora':nu},indent=2,ensure_ascii=False))
def clock(t):
 t=round(t);return f'{t//60}:{t%60:02}'
md='# Beat extraction: supplied Motilli and Nuora scripts\n\n'
md+='No five-ad cohort was retrieved. IM8 is a short beat summary, not a transcript, so it is excluded from timing. These are two related story examples, not independent evidence of a category-wide winning pattern. All seconds below are modeled from text at 155 wpm, with no pauses or visual-only holds. Nuora OCR has obscured words, so its counts are approximate. Comment timestamps in the PDF are reviewer posting times, not video times.\n\n'
md+=f'Motilli with H1: **{mt} words, {clock(mt*60/155)} modeled narration**. At 140–165 wpm: {clock(mt*60/165)}–{clock(mt*60/140)}, before pauses. H2 and H3 are alternatives, not sequential hooks. Nuora: **approximately {nt} legible words, {clock(nt*60/155)} modeled narration**.\n\n'
for title,rs in [('Motilli — supplied approved-style reference',mot),('Nuora — PDF narration, excluding annotations',nu)]:
 md+='## '+title+'\n\n| Beat | Start–end estimate | Seconds | Share | Opening words / source anchor |\n|---|---:|---:|---:|---|\n'
 for r in rs:
  md+=f"| {r['beat']} | {clock(r['start_sec'])}–{clock(r['start_sec']+r['duration_sec'])} | {r['duration_sec']:.1f} | {r['share_pct']:.1f}% | {' '.join(r['copy'].split()[:10])}… |\n"
 md+='\n'
md+='## A. Paired descriptive averages — n=2, estimated, not a target skeleton\n\nFirst onset is averaged only across examples containing the group. Shares sum all occurrences of that group in each script, including interleaved occurrences. An absent group has zero share; missing onset is excluded. Coverage prevents an absent beat being described as shared. Early Nuora failed attempts remain within its agitation span, while explicit research-stage alternatives get their own span; secondary functions are discussed in the report. Means alone hide this ordering.\n\n| Beat group | Mean first start (sec) | Mean first start (% position) | Mean share | Coverage | What the examples do |\n|---|---:|---:|---:|---:|---|\n'
jobs=['Promise an explanation or transformation','Make the unresolved feeling concrete and private','Renew the reason to listen after the stakes','Introduce an outside source inside the story','Give the symptom a causal explanation','Reinterpret what prior options do or allegedly miss','Turn understanding into a search for requirements','Assign each component a distinct job','Explain why form or combination affects selection','Introduce a purchasable option; spoken brand can occur later','Make use easy to picture','Describe small changes, callbacks and regained ordinary life','Attach availability to a production story','Invite a click and describe risk reversal']
for group,job in zip(dict.fromkeys(groups.values()),jobs):
 stats=[]
 for rs in [mot,nu]:
  rr=[r for r in rs if r['group']==group]
  stats.append((rr[0]['start_sec'] if rr else None,rr[0]['start_pct'] if rr else None,sum(r['share_pct'] for r in rr)))
 starts=[x[0] for x in stats if x[0] is not None]; positions=[x[1] for x in stats if x[1] is not None]
 md+=f"| {group} | {sum(starts)/len(starts):.1f} | {sum(positions)/len(positions):.1f}% | {sum(x[2] for x in stats)/2:.1f}% | {len(starts)}/2 | {job} |\n"
md+='\nAveraging first onset does not preserve a playable sequence. Use the ordered per-script tables to select an archetype, then allocate a new target budget. The supplied Motilli script places its named product before the outcome story; Nuora routes to an unnamed company first and names Nuora after most of the outcome story.\n'
(out/'beat-extraction.md').write_text(md)
print(json.dumps({'motilli_words':mt,'nuora_approx_words':nt,'motilli_seconds':mt*60/155,'nuora_seconds':nt*60/155,'motilli_UMP_share':sum(r['share_pct'] for r in mot if r['group']=='UMP'),'motilli_outcome_share':sum(r['share_pct'] for r in mot if r['group']=='Outcome / emotional payoff')},indent=2))
