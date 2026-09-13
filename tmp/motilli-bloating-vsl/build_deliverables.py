from pathlib import Path
import re, math, json, shutil

root = Path('/Users/brooksorradre2/Documents/marketing brain')
out = root / 'brands/motilli/creative/MOT-BLOAT-NUORA-01'
out.mkdir(parents=True, exist_ok=True)
(out/'edit').mkdir(exist_ok=True)
(out/'evidence').mkdir(exist_ok=True)

# Exact proposed spoken copy; each microsegment receives its own editorial job.
rows = [
('Hook','Visual qualification',"If your stomach looks like this on a GLP-1, watch this. Especially if you're eating less, but feeling more bloated.",'H01: Illustrative adult woman, clothed side profile in bedroom mirror, palm lightly resting on waistband; neutral expression, no exaggerated swelling.','Immediate recognition; the word this has a visible referent.','User hook; original illustrative staging'),
('Recognition','Small meal, big discomfort',"You sit down to a small meal. A few bites later, your stomach feels stretched and tight. And you wonder how so little food can leave you feeling so full.",'H02: Overhead lunch plate; woman puts fork down beside a modest meal.','Name the contradiction that earns the explanation.','Audience scenario, not a testimonial'),
('Recognition','Clothing consequence',"By the afternoon, you're loosening your waistband. The outfit you felt good in this morning is suddenly the one you want to change out of.",'H03: Seated three-quarter office view; discreet waistband adjustment beneath desk.','Move from symptom to daily consequence.','Original scenario informed by local bloating research'),
('Recognition','Emotional cost',"You wanted to feel more comfortable in your body. Now you're checking your stomach before you leave the house and wondering how you'll feel after dinner.",'H04: Hallway wide shot; woman pauses with handbag and keys, glances toward mirror.','Establish the desired outcome: comfort and participation.','Original scenario; not a measured audience prevalence claim'),
('Failed attempts','Trial and error',"Maybe you've tried peppermint tea, cut out a favorite food, or picked up another digestive supplement. And you're still trying to work out what actually sets the bloating off.",'H05: Kitchen overhead; hand moves handwritten food diary beside plain tea mug. No remedy stack or discarded medication.','Acknowledge effort without declaring treatments ineffective.','Conditional audience recognition'),
('Reframe','The missing question',"That is the frustrating part. You keep looking for something you ate, when a change in how your digestion works could also be part of the picture.",'P01: Presenter medium shot, direct eye contact; quiet pause after first sentence.','Shift from food blame to a broader explanation.','Qualified explanation; does not diagnose the viewer'),
('Mechanism','Medication context',"GLP-1 medicines such as Wegovy can slow how quickly your stomach empties. Bloating is also a listed side effect. So this deserves more attention than simply blaming your last meal.",'S01: Authentic prescribing-information excerpt with restrained highlights on stomach emptying and bloating.','Introduce external factual authority without inventing a clinician.','Wegovy official prescribing information'),
('Mechanism','Explain the movement',"Your stomach does more than hold food. Its muscles mix what you eat and gradually move it into your small intestine. That process takes time.",'S02: Isolated stomach-to-duodenum educational model showing mixing and measured passage; no medicine or product in frame.','Explain the process in ordinary language.','General anatomy; schematic illustration, not diagnostic imagery'),
('Mechanism','Connect back to fullness',"When your stomach empties more slowly, that lingering fullness can make more sense. The amount on your plate is only one part of the story.",'S03: Simple clock-and-meal schematic showing elapsed time and lingering fullness label; no accumulating sludge or complete blockage.','Return the explanation to the opening small-meal experience.','Qualified context; no universal causal attribution'),
('Mechanism','Separate contributors',"Gas and constipation can contribute to bloating too. That is why the same swollen feeling does not always have the same explanation, even for people taking the same medication.",'S04: Distinct colon schematic with modest gas pockets and separate constipation label; no stomach cutaway reuse.','Avoid forcing every symptom into one cause.','NIDDK gas symptoms and causes'),
('Failed attempts','Why random additions confuse',"And adding more to your routine isn't automatically the answer. Some people get more gas with extra fiber. The type, the amount, and your own response all matter.",'S05: Two neutral fiber ingredient cards beside measuring-spoon silhouette; no product efficacy comparison.','Explain why selection and individual tolerance matter.','NIDDK diet and gas'),
('Solution criteria','Change the decision',"So the useful question becomes: what belongs in a daily digestive routine for you? Something with clear ingredients, a manageable daily serving, and a routine you can actually keep up with.",'P02: Presenter holds blank three-item card; editor adds Ingredients / Directions / Personal fit.','Establish honest selection criteria before the brand.','Original purchasing criteria'),
('Ingredient reveal','Introduce the combination',"One combination you'll see is celery juice powder, prebiotic fiber, and chlorophyll. Three different ingredients, which are worth understanding before you decide whether to add them to your day.",'I01: Three tabletop ingredient stations, celery powder, fiber sample and green pigment reference, separately labeled.','Introduce the actual listed ingredients without unproven treatment claims.','Current Motilli product page; ingredient identity is seller-reported'),
('Ingredient reveal','Give prebiotic its meaning',"Prebiotic fiber provides food for bacteria in your gut. That's its role. Your own tolerance still matters, especially when bloating is the reason you're looking at digestive support.",'I02: Microscopic-style schematic of bacteria using fiber substrate; no good-versus-evil characters or instant gas disappearance.','Give the technical term a job and retain the relevant limitation.','General prebiotic role; not evidence of Motilli bloating efficacy'),
('Ingredient reveal','Explain the other names',"Celery juice powder is the plant ingredient. Chlorophyll is the green pigment found in plants; supplements may use a related form called chlorophyllin. Those names tell you what's included.",'I03: Celery stalk macro transitions at Chlorophyll to distinct leaf-pigment macro with chlorophyllin label.','Clarify names without inventing a prokinetic or gas-neutralizing action.','Current ingredient list names sodium copper chlorophyllin'),
('Product bridge','Brand reveal',"Motilli brings those ingredients together in a daily digestive-support gummy. The practical difference is having them in one simple routine, with the ingredients and directions available to review before you buy.",'PR01: First verified Motilli bottle reveal on bedside surface; real label readable, camera settles.','Match product to the criteria already introduced.','Current seller-listed formula and format; no proof of disease-specific efficacy'),
('Product','Why a gummy',"And if you're tired of swallowing another capsule or mixing another drink, the gummy format may be the part you appreciate first. You simply chew it.",'PR02: Hands open verified bottle and place gummies on clean palm; no swallowing simulation.','Answer format objection through convenience rather than absorption superiority.','Gummy format; hypothetical preference'),
('Product','Concrete routine',"Motilli's directions are two gummies before bed with a full glass of water. That gives you a straightforward routine to discuss with your prescriber alongside anything else you're taking.",'PR03: Bedside overhead, exactly two current-reference gummies and full water glass; hand sets bottle beside them.','Make use understandable without asserting universal medication compatibility.','Current product directions; advise individual discussion'),
('Expectations','How to assess fit',"If you decide to try it, pay attention to how you actually feel. Keep track of your bloating and comfort, so you can evaluate your own experience.",'H06: Close-up simple symptom journal being filled in; no fabricated improving scores or guaranteed timeline.','Replace borrowed week-by-week testimonial with a realistic evaluation.','No timed outcome promise'),
('Payoff','Return to the opening',"Because the goal is easy to picture: getting dressed without planning around your waistband, enjoying a meal without spending the evening focused on your stomach, and feeling present when you're out.",'F01: Original imagined-life scene: wide dining table, woman engaged in conversation. Small Imagine everyday comfort label; no before/after transformation.','Resolve opening concerns as an aspiration, not a treatment result.','Explicit aspirational framing'),
('Offer','Available next step',"If you'd like to take a closer look, the link below takes you to Motilli. You can review the formula, the daily routine, and the available bottle options there.",'PR04: Verified live product-page screen capture showing formula and bottle options; no price unless freshly checked.','Make click destination specific and useful.','Current product destination'),
('Guarantee','Risk reversal',"Motilli also offers a ninety-day money-back guarantee, starting when your order arrives. It covers opened bottles too, so opening the bottle doesn't end your chance to request a refund.",'PR05: Real bottle with editor-rendered guarantee card: 90 days from delivery / Opened bottles included / Terms apply.','State the actual risk reversal; no guaranteed result or no-return claim.','Live refund policy checked 2026-09-09'),
('CTA','Close the loop',"If you're ready to explore a simpler digestive routine, tap below to see Motilli. Start with the details, and decide whether it belongs in your routine.",'PR06: Clean verified bottle and two gummies, See Motilli button graphic; stable final frame.','One clear next action with no invented scarcity.','Brand action; no medical outcome guarantee'),
]

def words(s): return len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",s))
def clock(s): return f'{int(s)//60:02d}:{int(s)%60:02d}'
t=0
for i,(macro,beat,copy,visual,purpose,evidence) in enumerate(rows):
    n=words(copy)
    # 160 wpm plus a half-second thought break, rounded up for reviewable whole-second allocations.
    d=math.ceil(n*60/160+0.5)
    rows[i]={'id':f'M{i+1:02d}','macro':macro,'beat':beat,'copy':copy,'visual':visual,'purpose':purpose,'evidence':evidence,'words':n,'duration':d,'start':t,'end':t+d}
    t+=d
total=t+3
count=sum(r['words'] for r in rows)

intro=f'''# Motilli bloating VSL — Nuora framework — V1

Date: 2026-09-09. Concept: MOT-BLOAT-NUORA-01. Status: script and editorial planning draft; no media production requested or performed.

Audience: problem-aware adults on a GLP-1 who recognize bloating, especially women represented in the existing Motilli audience research. Main pain: eating less while feeling uncomfortably full and tight around the waistband. Emotional payoff: comfort, getting dressed, meals and being present with others.

Format assumption: one warm, informed female brand presenter speaking directly to camera, with original illustrative B-roll. No fabricated customer experience, clinician identity, endorsement or result. Vertical 9:16 is provisional. This is not a customer testimonial.

Timing: {count} spoken words. Planning delivery is 160 words/minute, with segment-level thought breaks and rounding. Allocated narration: {clock(t)}; 3-second final hold; total {clock(total)}. Timings are provisional until selected voice is recorded and aligned. These are original allocations, not measurements or runtime shares extracted from Nuora.

Nuora transfer: recognition → attempted fixes → new explanatory context → solution criteria → ingredient introduction → product fit → practical expectations → emotional callback → guarantee → CTA. Its fabricated-or-unverified testimonial timeline, secret-research device and scarcity are not imported. Authority here comes from identifiable prescribing information. Product proof is limited to verifiable format and seller-listed ingredients, not established bloating efficacy.

Evidence limitation: older internal briefs conflict and the August product-development brief records earlier fabricated label amounts. The current site is a source for what the seller lists, not independent confirmation of composition or clinical efficacy. No product-specific human evidence establishing reversal of GLP-1 delayed emptying was found in the reviewed materials. This draft therefore uses the narrower daily digestive-support positioning and convenience bridge. A stronger treatment-mechanism passage needs finished-product substantiation; none has been invented. Numeric ingredient doses, testimonial results, review counts, special processing, gas-neutralization and medication-interaction assurances are excluded.
'''

plan=intro+'''
## Inputs and reference findings

- User's Nuora transcript/breakdown supplied as a four-page screenshot PDF in Downloads; all four pages visually inspected during this conversation. Transcript structure and annotations are available. No original Nuora video was supplied, so source shot boundaries, consecutive-frame cuts, camera movements, captions, music and delivery are unobserved. No frame audit is claimed. The schedule below is original Motilli editorial direction, not replication of an inspected video.
- Latest request: bloating, problem-aware, hook beginning If your stomach looks like this on a GLP-1.
- Local context: Motilli_Product_Context.md (March; historical), custom-formulation-brief-2026-08-11.md (development proposal, not current SKU), bloating sub-avatar-profile.md (research synthesis, not clinical proof).
- Current product page and refund policy fetched live 2026-09-09; see evidence/sources.md.

## Overall editing strategy

Open with a clothed illustrative abdomen in the first frame so “this” has a referent. Do not use a before/after or imply that body shape establishes a diagnosis. Let the daily-life details establish recognition, then move into a clearly sourced explanation. The prescriber-information insert introduces authority; one stomach anatomy view explains movement; the subsequent timing schematic and colon view explain separate ideas. Ingredient footage changes scale and subject each time. Reveal the brand only when the copy reaches product fit. Close on an imagined social-life payoff and the real guarantee.

Use straight cuts at the exact next segment's first word, with continuous narration. Where a microsegment contains two shots, cut at the specified sentence cue, not a guessed timestamp; final word alignment locates that cut. No decorative transitions, repeated footage, zoom-only variants, or symptom-to-flat-stomach visual claims. Presenter coverage can remain consistent but is captured as continuous delivery, not a loop.

## Shot and line schedule

All scene IDs below identify planned assets, not existing files. Current bottle/gummy references must be visually checked before production. Each row has an asset gap; no source reuse is selected at this phase. Local libraries have not been visually audited for selection.

| ID / beat | Exact narration | Provisional time | Visual / visible action | Source or asset gap | Incoming / outgoing transition and cut cue | Movement / captions / sound | Editorial purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    transition=('Cold open on first phoneme; ' if i==0 else 'Straight cut on first word; ')+('hold into silent tail.' if i==len(rows)-1 else 'straight cut at next row’s first word.')
    gap='Source verified product photography or create from current approved references.' if r['visual'].startswith('PR') else ('Capture authentic source page; redact irrelevant navigation.' if r['id']=='M07' else 'Original scene required; source or generate after copy selection.')
    movement='Locked or restrained practical camera; phrase captions, maximum two lines; continuous VO.'
    if r['id']=='M15': transition+=' Internal cut on “Chlorophyll”.'
    if r['id']=='M01': movement+=' Neutral illustrative label; no music during hook.'
    if r['id']=='M20': movement+=' Maintain “Imagine everyday comfort” to distinguish aspiration.'
    if r['id']=='M07': movement+=' Source citation stays legible; no fake journal graphics.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])} ({r['duration']}s) | {r['visual']} | {gap} | {transition} | {movement} | {r['purpose']} |\n"

plan+=f'''
Final hold: {clock(t)}–{clock(total)}, three seconds on PR06 with brand, See Motilli and guarantee terms reference. No additional spoken words.

## Voice, captions and audio

Warm, conversational, matter-of-fact female brand presenter; no clinician costume or impersonated testimonial. Deliver complete thoughts with brief pauses; primary pace 160 wpm. GLP-1 is spoken “G L P one”; ninety-day is spoken naturally; confirm brand pronunciation from an approved brand voice sample before VO selection. Scientific passages are explanatory, not alarmist.

Continuous voice recording across cuts. No music in opening; optional unobtrusive instrumental bed enters under M02, stays substantially below speech (initial planning offset around -24 dB relative to narration), with a short fade into final hold. No heartbeat, ominous impact, flushing, gas sounds or sound implying instant relief. Adjust by listening; provisional delivery target -16 to -14 LUFS integrated and true peak no higher than -1 dBTP.

Phrase captions, maximum two lines, edited from final word alignment; white text with dark backing when required for contrast. Safe areas planned for 1080×1920: keep captions away from bottom 300px and rightmost 140px; verify placement against final platform UI. Short emphasis labels only when they aid understanding. Never add outcome claims through captions that the spoken copy does not support.

## Visual variety audit — planned stage

Distinct scenes: bedroom side profile; overhead meal; office seated detail; hallway wide; food diary and tea; presenter; authentic medication information; stomach model; clock schematic; colon model; fiber cards; presenter criteria; ingredient stations; microbial substrate view; celery macro and pigment macro; product bedside hero; bottle-opening hands; bedtime overhead; symptom journal; social dining wide; live product-page capture; guarantee card; final packshot. Repeated product presence has different actions and framing for distinct editorial jobs. No exact B-roll source selected or reused. The final source-and-composition audit remains required after assets exist; filenames alone do not demonstrate variety.

## Production order and delivery QA

This phase delivers script and plan only. If production is requested: first update this plan for accepted copy; locate the current documented internal-editor entry point; verify actual product references, label and claim support; choose/source each distinct scene; use GPT Image 2 for image production and Google Omni for generated video; inspect outputs; record/select voice; obtain fresh word alignment; recalculate boundaries and caption timing; assemble in the user's internal editor; inspect the complete final cut and exact transition spans; verify all assets, offer text, captions, audio and three-second end hold. HyperFrames and Remotion are prohibited. No editor was invoked or entry point assumed in this planning phase.

Planned export if requested: 1080×1920 H.264 MP4, 30 fps, AAC audio, clean master and captioned version. Reconfirm target platform before final export. QA must reject invented results, body transformations presented as product evidence, unsupported causal medical animations, repeated B-roll, stale product labels and guarantee wording that promises no returns are ever required.
'''

# Plan is written first, before any production artifacts; script is a separate reviewable deliverable.
(out/'edit/editing-plan.md').write_text(plan)
script=intro+'\n## Timed script\n\n'
for r in rows:
    script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['macro']} / {r['beat']}\n\n{r['copy']}\n\n"
script+=f'Final silent end hold: {clock(t)}–{clock(total)}.\n'
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('\n\n'.join(r['copy'] for r in rows)+'\n')
(out/'microsegments.json').write_text(json.dumps({'version':1,'date':'2026-09-09','words':count,'planning_wpm':160,'spoken_allocation_seconds':t,'end_hold_seconds':3,'total_seconds':total,'timing_status':'provisional, no recorded alignment','segments':rows},indent=2))
sources='''# Sources and claim boundaries — 2026-09-09

1. Current seller product page: https://getmotilli.com/products/motilli-3-bottle-90day-reset — fetched successfully with requests 2026-09-09. Listed ingredients and directions; not independent formula testing or proof of efficacy. Snapshot: live-product-page.txt.
2. Current refund policy: https://getmotilli.com/policies/refund-policy — fetched successfully 2026-09-09. 90 days from receipt; opened bottles count; return may be requested; prepaid return instructions if so; approval and requested return precede refund. Policy contact differs from PDP; use policy email support@trymotilli.co in any later on-screen instructions. No “no questions asked” or “no return required” blanket claim.
3. Wegovy official prescribing information: https://www.wegovy.com/prescribing-information.html — browsed 2026-09-09. Supports slowed stomach emptying and bloating as a listed side effect. Does not establish that every GLP-1 user's bloating is caused by slowed emptying or that Motilli treats it.
4. NIDDK gas symptoms and causes: https://www.niddk.nih.gov/health-information/digestive-diseases/gas-digestive-tract/symptoms-causes — browsed 2026-09-09. Supports distinctions among gas, bloating, digestive conditions and bacterial carbohydrate breakdown.
5. NIDDK gas and diet: https://www.niddk.nih.gov/health-information/digestive-diseases/gas-digestive-tract/eating-diet-nutrition — browsed 2026-09-09. Some people have more gas with excess fiber. Does not establish that Motilli's FOS reduces bloating.
6. Local product-dev/custom-formulation-brief-2026-08-11.md: records earlier fabricated label amounts and limitations of celery evidence. It is a proposed new formulation; do not mistake proposed ginger, artichoke, magnesium, kiwi or powder format for the current gummy SKU.
7. User's Nuora PDF: /Users/brooksorradre2/Downloads/screencapture-docs-google-document-d-1Fwe1k2Pk-Kv7SnOkODk8iNjGmqf0hSwfH0mMiRaDw6g-edit-2026-09-09-12_59_27.pdf. All four PDF pages inspected in conversation. No source video timestamps or observed editing asserted.

Script limits: no product clinical outcomes, customer testimonial, review statistic, instant result, timed recovery, prokinetic claim, absorption superiority, zero-bulk claim, gas-neutralization claim, weight-loss preservation guarantee or manufactured scarcity. The absence of these is an evidence boundary, not a declaration that the product is ineffective.
'''
(out/'evidence/sources.md').write_text(sources)
shutil.copyfile(root/'tmp/motilli-bloating-vsl/live-product-page.txt',out/'evidence/live-product-page.txt')
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01\n\nProblem-aware GLP-1 bloating VSL; script and planning phase.\n\n- [Script and timed beat map](script-and-beat-map.md)\n- [Clean narration](script.txt)\n- [Editing plan](edit/editing-plan.md)\n- [Sources and claim boundaries](evidence/sources.md)\n- [Machine-readable microsegments](microsegments.json)\n')
print(json.dumps({'folder':str(out),'words':count,'narration_seconds':t,'total_seconds':total,'microsegments':len(rows),'ranges':[(r['id'],clock(r['start'])+'–'+clock(r['end']),r['duration'],r['beat']) for r in rows]},indent=2))
