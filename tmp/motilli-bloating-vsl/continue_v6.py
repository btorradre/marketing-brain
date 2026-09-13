from pathlib import Path
import json,re,math,shutil

out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/MOT-BLOAT-NUORA-01')
prior=(out/'edit/editing-plan.md').read_text()
archive=out/'versions/v5';archive.mkdir(parents=True,exist_ok=True)
for name in ['script-and-beat-map.md','script.txt','microsegments.json','README.md']:
    if not (archive/name).exists():shutil.copy2(out/name,archive/name)
if not (archive/'editing-plan.md').exists():shutil.copy2(out/'edit/editing-plan.md',archive/'editing-plan.md')

items=[
('Hook','Conditional transformation and promise',"If your stomach looks like this on a GLP-1, this was mine before, and this is mine now. I can finally get through dinner without unbuttoning my jeans. In the next thirty seconds, I'll explain the gut slowdown no one explained to me—and what helped me feel comfortable again.",'H01: Genuine same-customer before, cut to genuine after on this is mine now, distinct dinner-comfort detail then customer to camera.','Requires actual customer transformation and outcome evidence; none supplied.',None),
('Discovery','Quick Facebook scene',"I was scrolling through a Facebook GLP-1 group when a gastroenterologist's comment caught my attention.",'F01: Phone scroll to clearly illustrative comment; prominent Dramatized example—not a real post unless genuine source supplied.','Invented scene device, not a real group/doctor source.',None),
('Problem and solution mechanism','Doctor explains the target before product',"He wrote, 'GLP-1s can slow stomach emptying. If that slowdown is contributing to your symptoms, ask about supporting stomach motility—the movement that carries food onward.'",'F02: Exact conditional text as readable illustrative comment, then one simple stomach-to-intestine movement schematic. No brand or treatment-result animation.','Invented doctor dialogue; broad medical context from sources already checked; not a Motilli recommendation.',None),
('Product-to-result bridge','Required actual customer action and result','[Insert one verified customer sentence naming the approach she actually used and the improvement she can truthfully report. Approximately 12–16 spoken words.]','P01: Actual customer to camera and supported evidence asset; first brand appearance allowed only after mechanism.','REQUIRED EVIDENCE SLOT. Not narration, not a claim ready to record.',8),
('Mechanism clarification','One plain-language explanation',"That helped me understand why I could eat a small lunch and still feel so full afterward. My stomach had to mix the food and move it along. The amount I ate was only part of the picture.",'S01: Distinct meal-and-elapsed-time schematic; then return to narrator, no repeat stomach model.','Conditional personal understanding, not a clinical diagnosis.',None),
('Product detail','Actual listed formula',"Motilli combines celery juice powder, prebiotic fiber, and chlorophyll in a daily gummy. The prebiotic fiber provides food for bacteria in the gut. I wanted to understand the ingredients before making it part of my routine.",'PR01: Current approved bottle, separate ingredient labels; fiber illustration distinct from stomach animation.','Seller-listed ingredients; no claim that celery accelerates emptying or chlorophyll removes bloating.',None),
('Routine','Practical use',"The directions are two gummies before bed with a full glass of water. I liked that the routine was easy to understand, and that I could review the formula with my prescriber.",'PR02: Actual current directions, then separate full water glass and two gummies; no consumption until real customer use verified.','Seller-listed directions; personal statements remain conditional on actual account.',None),
('Payoff','Resolve the opening once',"Being able to enjoy dinner without thinking about my waistband is the part that matters to me. That was the everyday comfort I wanted back.",'H02: Genuine customer describes supported outcome; everyday dinner footage only if truthful and correctly contextualized.','Conditional outcome already introduced in hook; no new quantitative or timed recovery claim.',None),
('Guarantee','Verified risk reversal',"Motilli offers a ninety-day money-back guarantee from delivery, including opened bottles. You can review the full terms on the product page before deciding whether to try it.",'PR03: Current product plus 90 days from delivery / Opened bottles included / Terms apply.','Refund policy checked this conversation; no no-return-required claim.',None),
('CTA','One next step',"I've linked Motilli below so you can see the ingredients and directions for yourself. If this sounds familiar, take a look and discuss whether it fits your routine with your prescriber.",'PR04: Current product, See Motilli, real page destination; end hold.','Product-page CTA; no product efficacy or prescription-change guarantee.',None),
]
def clock(s):return f'{s//60:02d}:{s%60:02d}'
rows=[];t=0
for i,(macro,beat,copy,visual,evidence,reserve) in enumerate(items):
    n=0 if reserve else len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",copy))
    duration=reserve or math.ceil(n*60/150+0.5)
    rows.append(dict(id=f'M{i+1:02d}',macro=macro,beat=beat,copy=copy,visual=visual,evidence=evidence,words=n,reserved_seconds=reserve or 0,start=t,end=t+duration,duration=duration));t+=duration
total=t+3;words=sum(r['words'] for r in rows)
assert total<=180
intro=f'''# Motilli bloating VSL — V6 working continuation

Date: 2026-09-09. Scope: continue from the conditional transformation hook while retaining the user's stage-3 premise, problem-aware first-person woman, brief Facebook discovery, solution mechanism before product and ≤3-minute maximum.

Status: WORKING SCRIPT, NOT RECORD-READY. One explicit product-to-result evidence slot remains. User has been asked for the actual customer account and product mechanism support. No customer before/after, genuine gastroenterologist comment, personal treatment action or product-specific evidence has been supplied. The hook and personal outcome passages are conditional creative copy, not verified factual assertions. The Facebook/doctor scene is invented and must be plainly identified as dramatized unless replaced with an actual source. A dramatization label does not substantiate product efficacy.

Timing: {words} drafted spoken words plus one 8-second reserved evidence sentence. At 150 wpm with brief breaks/rounding, allocated total {clock(total)} including 3-second hold. This is a provisional schedule, not a finished word count or recorded runtime. Reserve approximately 12–16 words for the missing actual action/result; recalculate after evidence arrives. Hard final maximum 180 seconds.

Promise: mechanism and solution target arrive immediately after the hook, before Motilli. M02–M04 take {rows[3]['end']-rows[1]['start']} seconds after the hook. The actual benefit promised by the hook remains undelivered until M04 contains a truthful supported account. Measure the 30-second promise from its spoken onset in final alignment; compress the hook/continuation if necessary rather than claim the current estimates prove delivery. Do not leave the payoff at V5's old 1:32 product reveal.

UMS distinction: the doctor introduces stomach movement as the relevant target. That does not prove a unique Motilli solution mechanism. Any sentence asserting that Motilli restores stomach movement must have matching evidence. Do not fill the result slot by copying Nuora's results or inventing an effect for celery, fiber or chlorophyll.
'''
plan=intro+'''
## Reference, strategy and source boundaries

Read the existing V5 plan and V6 hook proposal before continuing. Nuora PDF/transcript was visually inspected earlier; no original reference video supplied and no frame-boundary audit claimed. New sequence is original direction. User requested continuation of the proposed hook, not image/video/voice production.

Open on actual transformation evidence if supplied, quickly show the requested group discovery, then the conditional doctor explanation of slowed emptying and movement. The one customer action/result sentence is the early payoff, followed by concise mechanism clarification, actual formula, directions and close. No identity ladder, extended failed-remedy story or invented recovery timeline. First Motilli mention occurs only after the solution target has been introduced.

## Microsegment and visual schedule

| ID / beat | Exact drafted line or explicit slot | Provisional time | Visual/action | Evidence or asset gap | Incoming/outgoing and internal cut cues | Captions/audio/movement | Purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    cue=('Cold open; ' if i==0 else 'Hard cut on first phrase; ')+('hold through silent tail.' if i==len(rows)-1 else 'hard cut on next row’s first phrase.')
    if i==0:cue+=' Internal cuts on this is mine now and get through dinner.'
    if i==2:cue+=' Comment to schematic on the movement; preserve full conditional wording.'
    treatments='Natural physical movement; continuous female narrator; phrase captions max 2 lines; high contrast.'
    if i in [1,2]:treatments+=' Clearly label invented group/comment as Dramatized example—not a real post.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])}, {r['duration']}s | {r['visual']} | {r['evidence']} All visual assets unselected. | {cue} | {treatments} | {r['macro']} |\n"
plan+=f'\nSilent hold {clock(t)}–{clock(total)}. No asset generation, narration, timeline or export performed.\n'
plan+='''
## Voice, variety and QA

One woman's first-person voice, 150 wpm planning pace, warm and direct. She reads the comment; no cloned/imitation doctor voice. No music under hook; optional unobtrusive music under later scenes well below narration, short ending fade. Initial voice priority mix -16 to -14 LUFS integrated, true peak ≤-1 dBTP, all verified only after actual export. Caption timing comes from fresh word alignment; critical text kept out of lower 300px/right 140px in provisional 1080×1920 layout.

Distinct planned scenes: genuine transformation material; independent dinner detail; group scroll; comment card; one stomach model; actual customer proof; separate meal/time diagram; product ingredient tableau; fiber view; directions; bedtime glass; real customer reflection; guarantee; final packshot. No exact B-roll source reuse selected. Audit source reuse and visually similar compositions after sourcing and before export. Do not digitally create or enhance a claimed body transformation, use an actor's body as real customer proof, or animate ingredients restarting the stomach.

Before any production: obtain the missing true account and matched claim evidence, resolve the conditional hook/result, update this plan, verify current product references and guarantee, choose distinct assets, use GPT Image 2 for images and Google Omni for video, inspect results, record voice, align the actual words, and assemble using the user's internal editor after locating its current documented entry point. HyperFrames and Remotion prohibited. Proposed export only if requested: 1080×1920 H.264 30fps AAC; ≤180s measured, including final hold. Verify actual 30-second promise, full captions, audio, cuts, source provenance and visual variety. The evidence slot prevents this from being represented as a complete record-ready testimonial.
'''
(out/'edit/editing-plan.md').write_text(plan)
script=intro+'\n## Timed working script\n\n'
for r in rows:script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['beat']}\n\n{r['copy']}\n\n"
script+=f'Final hold {clock(t)}–{clock(total)}.\n'
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('[NON-SPOKEN NOTE: Conditional working script, not record-ready. Transformation and outcome require true customer evidence. The Facebook/doctor scene is invented and must be clearly dramatized. M04 is an explicit missing-evidence slot, not narration.]\n\n'+'\n\n'.join(r['copy'] for r in rows)+'\n')
(out/'microsegments.json').write_text(json.dumps(dict(version=6,date='2026-09-09',status='working, evidence-dependent',drafted_spoken_words=words,evidence_slot_seconds=8,planning_wpm=150,total_seconds=total,max_finished_seconds=180,timing_status='provisional; evidence line and actual voice outstanding',segments=rows),indent=2))
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V6 working draft\n\nContinuation from transformation hook. One explicit customer action/result slot needs evidence; not record-ready.\n\n- [Working script and timings](script-and-beat-map.md)\n- [Updated editing plan](edit/editing-plan.md)\n- [Conditional hook](hook-v6.md)\n- [Sources](evidence/sources.md)\n- [Earlier versions](versions/)\n')
assert all(r['copy'] in plan for r in rows)
assert all(rows[i]['end']==rows[i+1]['start'] for i in range(len(rows)-1))
print(json.dumps(dict(words=words,total=clock(total),first_payoff=clock(rows[3]['end']),seconds_after_hook=rows[3]['end']-rows[0]['end'],segments=[(r['id'],clock(r['start'])+'–'+clock(r['end'])) for r in rows]),indent=2))
