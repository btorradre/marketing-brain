from pathlib import Path
import json,re,math,shutil

out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/MOT-BLOAT-NUORA-01')
archive=out/'versions/v6b';archive.mkdir(parents=True,exist_ok=True)
for f in ['script-and-beat-map.md','script.txt','microsegments.json','README.md']:
    if not (archive/f).exists():shutil.copy2(out/f,archive/f)
if not (archive/'editing-plan.md').exists():shutil.copy2(out/'edit/editing-plan.md',archive/'editing-plan.md')

items=[
('Hook','Transformation + mechanism tease',"If your stomach looks like this on a GLP-1, this was mine before—and this is mine now, after I finally understood the gut slowdown no one had explained to me.",'H01: Genuine same-customer before→after cut on this is mine now; short GLP-1 gut slowdown label.','Conditional on actual customer account/footage. Do not claim doctors deliberately conceal information.',None),
('Problem agitation','Small meal, waistband discomfort',"Some days, a few bites of lunch left me feeling so full I wanted to undo my jeans. I couldn't understand why eating less wasn't making that feeling go away.",'H02: Modest meal overhead; cut to distinct seated waistband detail on undo my jeans.','Preserves the concrete lunch/jeans frustration from the fuller V4 draft; personal experience conditional.',None),
('Twist the knife','Private everyday frustration',"I was eating less, but still choosing clothes around my stomach. And I didn't exactly want to explain that over dinner.",'H03: Wardrobe view; woman exchanges a fitted top for a looser one, then restrained look toward camera.','One short privacy/embarrassment beat. No fabricated prevalence or social-proof statistic.',None),
('Second curiosity loop','Renew hope before education',"But let me explain the part I was missing—and what changed the way I looked for help. I wanted to enjoy dinner without quietly undoing my jeans.",'H04: Narrator directly to camera, pause at let me explain; no anatomy or product yet.','Aspirational renewed promise follows agitation. Uses user-offered let me explain alternative; no inaccurate 30-second timer.',None),
('Discovery','Facebook messenger',"I was scrolling through a Facebook GLP-1 support group when a gastroenterologist's comment caught my attention.",'F01: Brief clearly illustrative support-group scroll; comment source pending.','Fictional scene/comment must be clearly dramatized unless actual source supplied; no real doctor endorsement.',None),
('UMP','Explain slowed stomach emptying',"He explained that GLP-1 medicines can slow stomach emptying. The stomach normally mixes food and moves it into the small intestine. When that takes longer, the full feeling can linger—even after a small meal.",'S01: Conditional educational comment→single stomach/duodenum model; movement then elapsed-time cue.','General medication/physiology context previously verified. Personal symptoms not diagnosed. No UMS or brand here.',None),
('Past solutions','Different job from stomach emptying',"Fiber can help bowel regularity, and MiraLAX softens stool by holding water in it. Those jobs are different from speeding up stomach emptying. That was the distinction I'd missed.",'S02: Separate colon/stool hydration illustration with accurate labels, then a small anatomical locator.','Functional comparison after UMP. Do not generalize to fiber/MiraLAX never helping GLP-1 symptoms or the colon being innocent.',None),
('Third curiosity loop','How do I address it?',"So my next question was: how do I address the slowdown? What should I actually look for? That became a three-part checklist.",'F02: Narrator at kitchen table; notebook with three empty rows, no bottle/brand.','Open solution question only after problem mechanism and prior-remedy distinction.',None),
('UMS 1','Celery-derived compound','First, a compound from celery juice, for [the verified action relevant to stomach movement].','I01: Celery juice/compound macro and a plain role card; no gastric effect animation until substantiated.','OPEN COPY SLOT: no reviewed human evidence establishes Motilli/apigenin accelerates stomach emptying. Do not fill with invented effect.',12),
('UMS 2','Chlorophyllin','Second, chlorophyllin, a plant-derived ingredient, for [the verified action relevant to gas or bloating].','I02: Distinct plant-pigment macro and ingredient form label; no gas disappearance or binding animation without matching support.','OPEN COPY SLOT: gas neutralization/bloating relief at this formula/dose not established by reviewed evidence.',12),
('UMS 3','Soluble prebiotic fiber',"Third, a soluble prebiotic fiber to feed bacteria in the gut. The type and amount matter, because more fiber can mean more gas for some people.",'I03: Distinct microscopic fiber-substrate view, restrained labels; no zero-bulk/guaranteed passage depiction.','Supported general prebiotic role and tolerance qualification. Not evidence that this FOS nudges stomach contents or treats delayed emptying.',None),
('Product introduction','Combine the three after explaining them',"Then I came across Motilli. It combines celery juice powder, chlorophyllin, and prebiotic fiber in one daily gummy, so I could review the whole formula together.",'PR01: First actual current Motilli bottle/page reveal; three previously introduced ingredient labels surround bottle.','Product identity seller-listed. Fit with the first two claimed jobs remains conditional on substantiating those exact UMS slots.',None),
('Routine','Easy daily format',"The directions are two gummies before bed with a full glass of water. I liked the simplicity of chewing something instead of swallowing another capsule.",'PR02: Current directions→distinct two-gummy/water demonstration.','Seller-listed directions checked; personal preference conditional. No faster absorption or prescriber endorsement invented.',None),
('Guarantee','Risk reversal',"Motilli offers a ninety-day money-back guarantee from delivery, including opened bottles. That gives you time to decide whether it's a routine you want to keep.",'PR03: Product and current 90 days from delivery / Opened bottles included / Terms apply card.','Verified policy; no result guarantee or blanket no-return claim.',None),
('CTA','One click',"I've put the link below so you can see the ingredients and directions for yourself. Tap below to take a look at Motilli.",'PR04: Stable product, See Motilli CTA, guarantee reference; end hold.','Single destination, no repeated identity arc or invented recovery timeline.',None),
]
def clock(s):return f'{s//60:02d}:{s%60:02d}'
rows=[];t=0
for i,(macro,beat,copy,visual,evidence,reserve) in enumerate(items):
    n=0 if reserve else len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",copy))
    duration=reserve or math.ceil(n*60/155+0.35)
    rows.append(dict(id=f'M{i+1:02d}',macro=macro,beat=beat,copy=copy,visual=visual,evidence=evidence,words=n,reserved_seconds=reserve or 0,start=t,end=t+duration,duration=duration));t+=duration
total=t+3;words=sum(r['words'] for r in rows)
assert total<=180
assert next(i for i,r in enumerate(rows) if r['macro']=='UMP')<next(i for i,r in enumerate(rows) if r['macro']=='Past solutions')<next(i for i,r in enumerate(rows) if r['macro']=='UMS 1')<next(i for i,r in enumerate(rows) if r['macro']=='Product introduction')
intro=f'''# Motilli bloating VSL — V7, restored user-specified structure

Date: 2026-09-09. Latest explicit correction supersedes V6b's fast product jump. Preserve the fuller earlier script's lunch/jeans scene, one everyday emotional stake and the user's before/after hook. Required order: hook → short agitation → twist → second curiosity loop → messenger → UMP → prior-solution distinction → how do I address it? → three-part UMS unbranded → product → routine/guarantee/CTA. No Motilli naming or imagery before all three UMS rows.

Status: structurally complete WORKING SCRIPT with two clearly marked evidence-dependent ingredient-action lines. Those are the only spoken-copy slots, not optional permission gates. The reviewed materials do not establish celery/apigenin restores stomach movement or chlorophyllin neutralizes gas/bloating at Motilli's dose. These claims cannot be replaced by a generic ingredient list and called a UMS, nor asserted as fact without support. M09–M10 reserve the user's requested roles in the correct position. M11 states the supported prebiotic function and tolerance issue; it does not claim FOS mechanically nudges stomach food through. Personal transformation and discovery remain conditional on actual account; the invented doctor/group scene must be explicitly dramatized unless sourced.

Timing: {words} drafted words outside the two 12-second UMS slots. Plan approximately 25–28 spoken words per slot after claims are substantiated. At 155 wpm with brief breaks/rounding, total allocation {clock(total)}, including 3-second hold. This is provisional until finished copy and recorded word alignment. Hard measured delivery maximum ≤180 seconds; shorten nonessential copy if the final read exceeds it. No forced retiming of approved narration. Stage-3 sophistication is the user's brief premise; awareness remains problem-aware.

Second curiosity loop uses the user's alternative “let me explain,” so the opening no longer promises a complete fix thirty seconds before a deliberately later UMS. The mechanism is teased in the first line but explained only after agitation and renewed curiosity.
'''
reference='''
## Nuora reference reread — observed in supplied PDF

Re-inspected rendered PDF pages 1, 2 and 3 during this revision. On PDF page 2, the passage about stretchy joggers and a baggy shirt ends immediately before “But in the next thirty seconds, I'm gonna tell you what I found…” That passage promises movement from swimsuit embarrassment to buying cuter swimsuits, then references thousands of women quietly reclaiming themselves. “So let me show you how” is followed by another brief agitation passage before the forum practitioner and plaque analogy. The later “How do I stop it?” precedes the research/ingredient solution sequence. Page 3 contains bromelain/processing and berberine before the company recommendation.

Transfer: re-engage after the emotional stake, explain the problem before explaining the solution, give each ingredient its job before the brand. Do not import the research, thousands-of-women claim or medical conclusions. These are transcript/page observations; no original video, source timestamps, edit transitions or frame boundaries have been inspected. The user-described immediate before/after is the intended opening direction, not newly measured media evidence.

Useful source distinction: vitamins/minerals not getting through belongs to Nuora's claimed problem-mechanism explanation; its explicit probiotics/antibiotics failed-options passage comes later in the research story. The current Motilli order follows the user's requested adaptation, placing the fiber/MiraLAX distinction between UMP and UMS.
'''
plan=intro+reference+'''
## Editorial strategy

Opening is a visual before/after and a mechanism tease; no detailed science or product yet. One short lunch scene plus one wardrobe/privacy beat supplies agitation. Return to narrator for the second curiosity loop, then use the brief Facebook messenger to introduce the problem explanation only. Explain mixing and delayed emptying in one anatomy view. Follow with a distinct stool-hydration/colon view for the prior-remedy distinction. Ask the solution question, then show three distinct ingredient scenes. Only afterward reveal Motilli.

All source assets are unselected. Actual before/after must depict the same customer's genuine change in truthful context; it is not proof that the product caused the change. Do not generate, digitally flatten or deceptively pose a body to manufacture treatment evidence. Doctor/group scene is fictional unless actual source supplied: readable Dramatized example—not a real post labeling, no real credentials/identity or implied recommendation of Motilli. No clinical result, dose, week-by-week recovery or doctor concealment claim invented.

## Updated line and microsegment schedule

| ID / beat | Exact draft or marked evidence slot | Provisional timing | Visual/action | Source/claim gap | Incoming/outgoing and internal cut cue | Captions/motion/sound | Purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    cue=('Cold open; ' if i==0 else 'Straight cut at first word; ')+('hold into silent tail.' if i==len(rows)-1 else 'straight cut on next row’s first word.')
    if i==0:cue+=' Before→after cut exactly on this is mine now.'
    if i==1:cue+=' Meal→waistband cut at undo my jeans.'
    if r['macro']=='UMP':cue+=' Comment→anatomy at The stomach normally; pause at small meal.'
    if r['macro']=='Product introduction':cue+=' Product and brand appear for the first time here, after M09–M11.'
    treatment='Continuous first-person female VO; restrained physical motion; phrase captions ≤2 lines.'
    if r['macro'] in ['Discovery','UMP']:treatment+=' Fictional comment clearly identified; source-page authority is not a real doctor quote.'
    if r['reserved_seconds']:treatment+=' Do not record this row until the bracketed action is resolved; durations reserved.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])}, {r['duration']}s | {r['visual']} | {r['evidence']} Media gap: asset required. | {cue} | {treatment} | {r['macro']} |\n"
plan+=f'\nEnd hold {clock(t)}–{clock(total)} on product/CTA/guarantee. No further voice or identity material.\n'
plan+='''
## Voice, finish, variety and production QA

One woman, candid conversational tone, 155 wpm planning assumption. The emotional stake comes from a specific private inconvenience, not theatrical shame. A short pause at let me explain and how do I address the slowdown marks the two narrative turns. She recounts the fictional comment; no impersonated expert voice. Optional unobtrusive music enters after hook, well below voice, with a brief fade into final hold. Initial mix goal -16 to -14 LUFS integrated, true peak ≤-1 dBTP, verify on actual export.

Fresh word alignment controls cuts and two-line phrase captions. Use high contrast and provisional 1080×1920 safe areas excluding bottom 300px/right 140px for essential text. Do not add efficacy claims in overlays beyond substantiated narration. No unsupported comparisons, gas disappearing, stomach restarting, gummy absorption superiority or before/after treatment animation.

Planned unique scenes: genuine transformation; meal overhead; seated waistband; wardrobe; narrator curiosity turn; group feed; comment; one stomach model; a distinct colon/stool-water view; three-item notebook; celery macro; chlorophyllin/pigment macro; microscopic prebiotic-substrate view; current product reveal; directions/two-gummy water scene; guarantee; final packshot. Deliberate continuous narrator coverage can recur; no exact B-roll reuse selected. Audit actual source duplication and similar compositions after sourcing and before export.

No asset production or export performed. Before future production, resolve the two exact ingredient-action claims and real testimonial/source provenance, update this plan, verify approved current product references and offer, create/source distinct scenes, use GPT Image 2 for images and Google Omni for video, inspect outputs, record/select voice, align words, and assemble in the user's internal editor after locating the current documented entry point. HyperFrames and Remotion prohibited. Planned delivery only if requested: 1080×1920 H.264, 30fps, AAC; clean/captioned versions; measured total ≤180 seconds. Verify full edit, caption alignment, source/claim accuracy, three-part UMS before first visible/spoken brand, offer, audio, transitions and hold. No new approval gate is introduced; factual dependencies remain factual dependencies.
'''
(out/'edit/editing-plan.md').write_text(plan)
script=intro+reference+'\n## Timed working script\n\n'
for r in rows:script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['macro']}\n\n{r['copy']}\n\n"
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('[NON-SPOKEN NOTE: Working conditional script. Two explicit ingredient-effect slots require substantiation before recording. Actual transformation/source account required; fictional group/doctor scene must be clearly dramatized unless sourced. Maximum finished duration 180s.]\n\n'+'\n\n'.join(r['copy'] for r in rows)+'\n')
(out/'microsegments.json').write_text(json.dumps(dict(version=7,date='2026-09-09',status='corrected structure; two evidence-dependent UMS lines',drafted_words_excluding_slots=words,slot_count=2,slot_seconds=24,planning_wpm=155,total_seconds=total,max_finished_seconds=180,segments=rows),indent=2))
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V7\n\nRestored fuller structure per latest explicit user correction. Hook → agitation → second loop → UMP → prior solutions → how do I stop it → three-part UMS → product. Maximum 3 minutes. Two ingredient-action lines require evidence.\n\n- [Working script and timings](script-and-beat-map.md)\n- [Editing plan and Nuora reread](edit/editing-plan.md)\n- [Sources](evidence/sources.md)\n- [Previous drafts](versions/)\n')
src=out/'evidence/sources.md'
src.write_text(src.read_text()+'''\n## V7 comparison verification\n\nhttps://medlineplus.gov/druginfo/meds/a603032.html and https://www.miralax.com/healthcare-professionals/about-constipation support polyethylene glycol retaining water with stool / stool softening. The copy compares that function with stomach emptying; it does not call MiraLAX/fiber useless or insist all bloating begins in one organ. Targeted primary-literature search did not establish the requested celery/apigenin prokinetic or chlorophyllin anti-bloating effect at this product's dose. Two exact UMS action slots remain unresolved; no false mechanism has been supplied.\n''')
assert all(r['copy'] in plan for r in rows)
assert not any('Motilli' in r['copy'] for r in rows[:11])
print(json.dumps(dict(drafted_words=words,reserved_seconds=24,total=clock(total),rows=[(r['id'],clock(r['start'])+'–'+clock(r['end']),r['duration'],r['macro']) for r in rows]),indent=2))
