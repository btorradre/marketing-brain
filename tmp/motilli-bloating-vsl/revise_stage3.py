from pathlib import Path
import json,re,math,shutil

out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/MOT-BLOAT-NUORA-01')
oldplan=(out/'edit/editing-plan.md').read_text()
archive=out/'versions/v3';archive.mkdir(parents=True,exist_ok=True)
for name in ['script-and-beat-map.md','script.txt','microsegments.json','README.md']:
    if not (archive/name).exists():shutil.copy2(out/name,archive/name)
if not (archive/'editing-plan.md').exists():shutil.copy2(out/'edit/editing-plan.md',archive/'editing-plan.md')

items=[
('Hook','Recognize her problem',"If your stomach looks like this on a GLP-1, mine does too. I'm eating smaller meals, but I still get that tight, bloated feeling.",'H01: Clothed side profile of the same fictional woman; she turns toward her phone camera, hand rests lightly on waistband.','Qualify the problem-aware viewer immediately.'),
('Problem','One concrete frustration',"Some days, a few bites of lunch leave me feeling so full I want to undo my jeans. I couldn't understand why eating less wasn't making that feeling go away.",'H02: Overhead modest lunch plate; fork set down. At “undo my jeans”, cut to a distinct seated waistband detail.','Give the explanation one specific experience to resolve.'),
('Problem mechanism','Introduce GLP-1 gut slowdown',"Then I learned about GLP-1 gut slowdown. Medicines like Wegovy can slow how quickly the stomach empties, which means food can stay there longer after a meal.",'S01: Authentic official medication information on tablet, highlight stomach emptying; short editor label GLP-1 gut slowdown.','Supply the central new explanation early.'),
('Problem mechanism','Explain the movement',"Normally, the muscles in my stomach mix the food and gradually move it into my small intestine. When that process slows down, the full feeling can last longer too.",'S02: One isolated stomach-to-duodenum model shows mixing and gradual passage, with restrained timing schematic at “slows down”. No complete blockage or product.','Explain the cause and immediate consequence once, in ordinary language.'),
('Belief shift','Connect it back to her meal',"That could help explain why even a small meal was leaving me uncomfortable. I'd been thinking about how much I ate, without thinking about how quickly my stomach was emptying.",'H03: Three-quarter kitchen shot, woman looks from meal notes toward camera; no repeated lunch insert.','Land amount-versus-movement as the one belief shift.'),
('Solution transition','Move directly to product consideration',"Once I understood that, I started looking into digestive support made with GLP-1 users in mind. That's how Motilli came onto my radar.",'PR01: First real current Motilli product-page reveal on phone; show positioning then product, no doctor endorsement.','Introduce the product as the next step in her search.'),
('Solution introduction','Combined formula',"Motilli combines celery juice powder, prebiotic fiber, and chlorophyll in a daily gummy. What interested me was having those ingredients together in one routine I could review with my prescriber.",'PR02: Verified bottle with three separately labeled ingredient references on tabletop. No faster-stomach-motion demonstration.','Introduce the actual formula and format. Ingredient combination is not proof of a prokinetic UMS.'),
('Product fit','Simple use',"And the routine is simple: two gummies before bed with a full glass of water. I liked being able to chew something instead of adding another capsule to my evening.",'PR03: Close-up current directions, then distinct neutral gummy demonstration beside water; narrator does not consume product.','Make the format and directions concrete without claiming better absorption.'),
('Payoff','One everyday outcome',"What I want is simple too: finish a meal and get on with my evening, without spending the next few hours focused on how tight my stomach feels.",'H04: Fictional woman talks from sofa in same home, hopeful but still describing a goal. No recovery montage or flat-belly transformation.','Use one short aspiration that closes the opening loop.'),
('Guarantee','Risk reversal',"Motilli has a ninety-day money-back guarantee from delivery, including opened bottles. That matters to me, because I'd want to judge my own experience before deciding whether to keep it in my routine.",'PR04: Current bottle and clear guarantee text: 90 days from delivery; Opened bottles included; Terms apply.','Use the verified offer without invented scarcity or results.'),
('CTA','One clear next step',"If this sounds like what you're dealing with, I've linked Motilli below. You can see the ingredients and directions, and decide whether it's something you want to look into too.",'PR05: Stable current packshot, See Motilli CTA, guarantee reference; retain through end hold.','One product-page action, no additional education or open loop.'),
]
def clock(s):return f'{s//60:02d}:{s%60:02d}'
rows=[];t=0
for i,(macro,beat,copy,visual,purpose) in enumerate(items):
    n=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",copy));duration=math.ceil(n*60/150+0.5)
    rows.append(dict(id=f'M{i+1:02d}',macro=macro,beat=beat,copy=copy,visual=visual,purpose=purpose,words=n,start=t,end=t+duration,duration=duration));t+=duration
words=sum(r['words'] for r in rows);total=t+3
slower=sum(math.ceil(r['words']*60/140+0.5) for r in rows)+3
assert total<180 and slower<180
intro=f'''# Motilli bloating VSL — V4, stage-3 brief, maximum 3 minutes

Date: 2026-09-09. Concept MOT-BLOAT-NUORA-01. Copy and editorial planning only.

Latest user direction governs: use the user's stage-3 market-sophistication premise, problem-aware audience, first-person woman, GLP-1 gut slowdown explanation and UMS introduction; maximum 180 seconds. Market sophistication and audience awareness are separate brief inputs. The user's premise is accepted as creative direction, not presented as independently established market research. Nuora remains a reference for causal progression, not a required length or identity/objection checklist.

Argument: recognizable bloating → medication can slow stomach emptying → slower movement can prolong fullness → Motilli consideration and combined formula → simple routine → brief payoff, guarantee and CTA. Removed extended identity scenes, failed-remedy ladder, repeated mechanism paragraphs, ingredient definitions, diary/evaluation section and repeated product-page invitations.

Timing: {words} spoken words. Conversational planning pace 150 wpm plus brief thought breaks and rounding. Narration allocation {clock(t)}, end hold 3s, total {clock(total)}. At 140 wpm with the same break allocation, estimated total {clock(slower)}. Both fit the 3-minute maximum. These are estimates; actual voice and final export must be measured ≤180 seconds. Recut/rewrite before export if necessary; do not rush or silently retime the voice. Product first named at M06, {clock(rows[5]['start'])}–{clock(rows[5]['end'])}. Previous drafts remain under versions/.

Narrator provenance: fictional dramatization, not a supplied real testimonial. Keep explicit Dramatized story identification in any produced version; use actual personal events for any real customer adaptation. She is considering the product and does not claim to have taken it, improved, received an endorsement or completed a recovery timeline.

UMS boundary: the user requested a unique solution mechanism introduction. Reviewed evidence establishes seller-listed ingredients and format, but not that Motilli or its celery ingredient restores stomach movement, neutralizes gas or reverses medication effects. M07 introduces the actual combination and format. This is a product/formula introduction; it is not a substantiated physiological UMS. A stronger mechanism claim remains dependent on product evidence. Do not silently relabel an ingredient list as proof of how the product resolves the slowdown.
'''
reference=oldplan[oldplan.index('## Inputs and reference findings'):oldplan.index('## Revision and editorial strategy')]
reference=reference.replace('- Latest request: first-person perspective of a woman currently experiencing GLP-1 bloating; preserve problem awareness and the hook concept; use GLP-1 gut slowdown as the central mechanism.','- Latest request: stage-3 premise, only necessary gut-slowdown education and solution introduction, first-person woman, three-minute maximum.')
plan=intro+'\n'+reference+'''
## Editing strategy

Keep the hook and one lunch/waistband scene concise; introduce slowdown immediately afterward. Let one real source insert and one stomach model carry the education. Move to Motilli as soon as the portion-versus-emptying distinction lands. The product sequence demonstrates actual formula, format and directions; the final payoff is a single desired everyday activity. All transitions are direct cuts on speech cues; narration remains continuous. No extended identity montage or invented research-discovery scene.

Reference limitation: PDF/transcript inspected earlier; no original Nuora video supplied, no frame boundaries, camera motion, sound or caption rhythm measured. This plan is original direction, not a claimed source-media frame audit.

## Line and microsegment schedule

| ID / beat | Exact narration | Provisional timing | Visual / visible action | Source or asset gap | Incoming / outgoing cut and internal cue | Movement / captions / audio | Editorial purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    cue=('Cold open; ' if i==0 else 'Hard cut on first word; ')+('hold into silent end card.' if i==len(rows)-1 else 'hard cut at next segment’s first word.')
    if r['id']=='M02':cue+=' Internal cut at “undo my jeans”.'
    if r['id']=='M04':cue+=' Introduce timing schematic at “When that process”.'
    if r['id']=='M08':cue+=' Cut to gummy demonstration at “I liked”.'
    gap='New original scene or source footage required; no asset selected.'
    if r['visual'].startswith('PR'):gap='Current verified product references/live page required; no asset selected.'
    if r['id']=='M03':gap='Capture authentic official prescribing information from cited source.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])}, {r['duration']}s | {r['visual']} | {gap} | {cue} | Restrained physical movement; ≤2-line phrase captions; clear Dramatized story; uninterrupted first-person voice. | {r['purpose']} |\n"
plan+=f'\nEnd hold {clock(t)}–{clock(total)}: no speech, steady product and CTA, guarantee reference. Hard delivery maximum 03:00.\n'
plan+='''
## Voice, audio and captions

Same fictional woman, warm candid voice, short complete thoughts, 150 wpm planning pace. No expert costume, exaggerated distress or voiced research credentials. Preserve natural pauses at the mechanism and product reveal. GLP-1 spoken G L P one; verify Motilli pronunciation from current brand voice source when selecting VO.

Hook begins with voice only. Optional subtle music enters under M02 and remains well below narration; no dramatic alarm, gas noises, heartbeat or relief sound. Brief fade during 3-second end hold. Start around -24 dB below voice and adjust by listening; planned integrated loudness -16 to -14 LUFS, true peak ≤-1 dBTP, verified only on eventual export.

Continuous phrase captions based on fresh recorded word alignment, maximum two lines, high contrast; keep clear of platform controls. Initial 1080×1920 safe-area plan excludes bottom 300px/right 140px for critical text. Do not caption outcomes or clinical claims absent from the script. Keep dramatization identification readable separately from speech captions.

## Visual variety and product fidelity

Distinct planned visuals: bedroom profile; lunch overhead; seated waistband detail; authentic source tablet; isolated stomach model with a simple timing insert; kitchen reflection; phone product discovery; ingredient-and-bottle tabletop; directions close-up; gummy demonstration; sofa aspiration; guarantee card; final packshot. Each insert has its own composition, subject and action. Product presence repeats for distinct jobs; no exact B-roll source reuse selected. Audit actual source reuse and visual similarity again after assets exist and before export. No stomach shutdown, rotting food, whole-gut blockage, or product-triggered restored contractions. No before/after body transformation. Product labels and gummies must match approved current references.

## Production and QA

No images, video, voiceover, timeline or export are authorized by this script-revision phase. If production is requested, first update accepted copy and this plan, resolve any stronger UMS evidence, verify actual product references, source/create the distinct scenes, record/select narration, align every word, and recalculate all cuts/captions. Use GPT Image 2 for image production, Google Omni for generated video, and the user's internal editor for editing after locating its current documented entry point. HyperFrames and Remotion are prohibited. No legacy editor route assumed.

Planned output if requested: vertical 1080×1920, H.264, 30 fps, AAC, clean and captioned masters. QA the complete video and transition spans; verify products, captions, narration, offer, sound, framing, scene variety and 3-second hold. Actual total duration must be ≤180 seconds. If the selected read exceeds the cap, shorten copy and update this plan rather than accelerating the approved voice. Script timing is not a measured recording.
'''
# The editing plan is the first current artifact updated; no asset production follows.
(out/'edit/editing-plan.md').write_text(plan)
script=intro+'\n## Timed first-person script\n\n'
for r in rows:script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['macro']} / {r['beat']}\n\n{r['copy']}\n\n"
script+=f'Silent end hold {clock(t)}–{clock(total)}.\n'
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('[NON-SPOKEN PRODUCTION NOTE: Fictional dramatization; not a verified customer testimonial. Clearly identify as Dramatized story in production. Maximum finished runtime 180 seconds.]\n\n'+'\n\n'.join(r['copy'] for r in rows)+'\n')
(out/'microsegments.json').write_text(json.dumps({'version':4,'date':'2026-09-09','market_sophistication':'stage 3, user-provided premise','awareness':'problem aware','narrator':'first-person woman; fictional dramatization','mechanism':'GLP-1 gut slowdown / delayed stomach emptying','ums_status':'formula introduction only; physiological Motilli mechanism unsubstantiated in reviewed evidence','words':words,'planning_wpm':150,'spoken_allocation_seconds':t,'end_hold_seconds':3,'total_seconds':total,'estimated_seconds_at_140wpm':slower,'max_finished_seconds':180,'timing_status':'provisional until recorded alignment','segments':rows},indent=2))
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V4\n\nUser stage-3 brief; problem-aware first-person bloating; gut-slowdown explanation and concise formula introduction. Maximum 3 minutes.\n\n- [Script and microsegment timings](script-and-beat-map.md)\n- [Narration](script.txt)\n- [Editing plan](edit/editing-plan.md)\n- [Evidence and claim limits](evidence/sources.md)\n- [Previous versions](versions/)\n')
assert all(r['copy'] in plan for r in rows)
assert all(rows[i]['end']==rows[i+1]['start'] for i in range(len(rows)-1))
print(json.dumps({'words':words,'narration':clock(t),'total':clock(total),'at_140_wpm':clock(slower),'segments':[(r['id'],clock(r['start'])+'–'+clock(r['end']),r['duration']) for r in rows]},indent=2))
