from pathlib import Path
import json, re, math, shutil

out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/MOT-BLOAT-NUORA-01')
data=json.loads((out/'microsegments.json').read_text())
oldplan=(out/'edit/editing-plan.md').read_text()
archive=out/'versions/v4';archive.mkdir(parents=True,exist_ok=True)
for name in ['script-and-beat-map.md','script.txt','microsegments.json','README.md']:
    if not (archive/name).exists():shutil.copy2(out/name,archive/name)
if not (archive/'editing-plan.md').exists():shutil.copy2(out/'edit/editing-plan.md',archive/'editing-plan.md')

insert=[
dict(macro='Discovery',beat='Facebook support-group scroll',copy="One night, I was scrolling through a Facebook GLP-1 support group when I noticed a gastroenterologist's comment under a post about bloating.",visual='F01: Over-shoulder view of woman scrolling an illustrative support-group feed. Persistent prominent Dramatized example—not a real post. No real group name, personal profile, identity, likes or fabricated verification.',purpose='Deliver the user-requested quick discovery context before the solution mechanism.'),
dict(macro='Solution mechanism setup',beat='Fictional gastroenterologist comment',copy="He wrote, 'If slow stomach emptying is the problem, you need to ask about supporting stomach motility—the movement that carries food into the intestine.'",visual='F02: Readable illustrative comment card with the exact conditional wording; role label Fictional gastroenterologist. Same prominent Dramatized example—not a real post disclosure. No Motilli branding or product recommendation.',purpose='Introduce stomach movement as the relevant solution target. This is invented dramatic dialogue, not a sourced clinician quotation or endorsement.'),
dict(macro='UMS setup',beat='Name the solution criterion before the brand',copy="That was what I'd been missing: a solution aimed at the movement itself. I started looking into motility support.",visual='F03: Return to woman at kitchen table, phone lowered; editor label Motility = movement. Fresh narrator delivery, no replayed stomach anatomy or product footage.',purpose='Make the mechanism she is investigating explicit before any Motilli mention. Motility support is a category, not proof of product uniqueness or efficacy.'),
dict(macro='Product introduction',beat='Motilli after mechanism setup',copy="While looking into that, I came across Motilli. It combines celery juice powder, prebiotic fiber, and chlorophyll in a daily gummy—a formula I could review with my prescriber.",visual='PR01: First verified Motilli product-page reveal, then distinct actual bottle with ingredient labels. Hard internal cut at It combines. Remove fictional doctor and group UI before brand appears.',purpose='Introduce Motilli as a product for evaluation after the desired mechanism has been explained; no doctor-product endorsement or demonstrated prokinetic effect.'),
]
rows=data['segments'][:5]+insert+data['segments'][7:]
def clock(s):return f'{s//60:02d}:{s%60:02d}'
t=0
for i,r in enumerate(rows):
    r['id']=f'M{i+1:02d}'
    r['words']=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",r['copy']))
    r['duration']=math.ceil(r['words']*60/150+0.5);r['start']=t;t+=r['duration'];r['end']=t
words=sum(r['words'] for r in rows);total=t+3
slower=sum(math.ceil(r['words']*60/140+0.5) for r in rows)+3
assert total<=180 and slower<=180
intro=f'''# Motilli bloating VSL — V5, Facebook discovery before product

Date: 2026-09-09. Concept MOT-BLOAT-NUORA-01. Copy and planning only.

Current brief: problem-aware woman in first person, user's stage-3 sophistication premise, GLP-1 gut slowdown education, short Facebook support-group discovery with a gastroenterologist comment, solution mechanism/criterion before Motilli, total no more than 3 minutes.

Sequence: hook → one symptom scene → slowed stomach emptying → personal connection → Facebook discovery → gastroenterologist's conditional stomach-motility explanation → narrator names motility support → Motilli consideration → routine → payoff → guarantee → CTA.

Timing: {words} spoken words at 150 wpm with brief breaks and whole-second allocations. Narration {clock(t)}; final hold 3s; total {clock(total)}. Estimated at 140 wpm with the same allocation method: {clock(slower)}. All timings provisional until recorded voice alignment. Hard finished maximum 180 seconds. V4 archived under versions/v4/.

Provenance: FICTIONAL DRAMATIZATION. The narrator's experiences, Facebook post and gastroenterologist comment are invented scene-writing, not actual customer experience, a real professional's quote or a verified endorsement. Preserve clear Dramatized story labeling; prominently identify the group/comment scene as Dramatized example—not a real post. A real testimonial or real expert comment must use verified actual wording, identity and context. No actual Facebook group has been accessed, scraped or posted to.

UMS/evidence boundary: M07–M08 now introduce the desired solution target before the product. Motility support describes a general approach, not a proven proprietary Motilli mechanism. The hypothetical doctor does not recommend Motilli or its ingredients. Product-level evidence that this formula accelerates gastric emptying remains unavailable in reviewed material. M09 accordingly introduces a formula for consideration, not a clinically established match or a doctor's endorsed solution. Do not use the doctor scene or proximity editing to imply otherwise.
'''
reference=oldplan[oldplan.index('## Inputs and reference findings'):oldplan.index('## Editing strategy')]
reference=reference.replace('- Latest request: stage-3 premise, only necessary gut-slowdown education and solution introduction, first-person woman, three-minute maximum.','- Latest request: UMS before product, with a brief Facebook group scroll and gastroenterologist comment; retain first person and three-minute maximum.')
plan=intro+'\n'+reference+'''
## Editing strategy

Keep M01–M05 from V4. Replace its immediate brand transition with three compact shots: support-group scroll, illustrative doctor comment, narrator naming motility support. First brand appearance follows those beats. Hold the exact comment long enough to read, retaining its conditional clause. The same woman reads it in narration; no impersonated doctor voice. Her understanding supplies the bridge; the fictional doctor does not recommend a product.

The Facebook sequence is original direction from the user's latest request. No actual post or media reference supplied. Do not manufacture a supposedly authentic screenshot, real physician identity, clinic logo, credential badge, social-proof count or comment endorsement. No reference frame audit claimed. Keep ordinary straight cuts and continuous narration; avoid repeating mechanism education already delivered by M03–M05.

## Updated line and microsegment schedule

| ID / beat | Exact narration | Provisional time | Visual / action | Source or asset gap | Incoming / outgoing and internal cut cue | Captions, motion and audio | Purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    cue=('Cold open; ' if i==0 else 'Hard cut on first word; ')+('hold through silent tail.' if i==len(rows)-1 else 'hard cut on next segment’s first word.')
    if r['id']=='M02':cue+=' Internal cut at undo my jeans.'
    if r['id']=='M04':cue+=' Timing insert at When that process.'
    if r['id']=='M09':cue+=' Internal cut at It combines; doctor/group UI absent before product reveal.'
    if r['id']=='M10':cue+=' Cut from directions to gummy demonstration at I liked.'
    gap='Original scene or sourced media needed; none selected.'
    if r['visual'].startswith('PR'):gap='Actual current approved product reference or current page capture needed.'
    if r['id']=='M03':gap='Capture official medication information from existing cited source.'
    if r['id'] in ['M06','M07']:gap='Clearly illustrative feed/comment design needed. A real comment has not been supplied.'
    treatment='Natural physical movement; ≤2-line phrase captions; Dramatized story; continuous narrator VO.'
    if r['id'] in ['M06','M07']:treatment+=' Prominent Dramatized example—not a real post; do not let speech captions obscure disclosure or comment.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])}, {r['duration']}s | {r['visual']} | {gap} | {cue} | {treatment} | {r['purpose']} |\n"
plan+=f'\nEnd hold {clock(t)}–{clock(total)}; no speech; product, CTA and guarantee. Maximum final export 03:00.\n\n'
finish=oldplan[oldplan.index('## Voice, audio and captions'):]
finish=finish.replace('No expert costume, exaggerated distress or voiced research credentials.','No expert costume or impersonated physician voice. The woman reads the fictional comment as part of the explicitly dramatized narrative.')
finish=finish.replace('kitchen reflection; phone product discovery;','kitchen reflection; group scroll; comment card; narrator reaction; phone product discovery;')
plan+=finish
plan+='''
## V5 verification additions

Audit that M07–M08 precede all spoken/visible Motilli branding. Keep the doctor comment conditional and unbranded. Verify that viewer-facing disclosures make the fictional source clear; internal production notes alone are insufficient. The last product card must not imply the physician selected or endorsed Motilli. Recheck total runtime with the selected read; shorten copy if needed, do not accelerate the approved voice. Scientific education supports only general medication/stomach context, not efficacy of the advertised supplement.
'''
(out/'edit/editing-plan.md').write_text(plan)
script=intro+'\n## Timed first-person script\n\n'
for r in rows:script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['macro']} / {r['beat']}\n\n{r['copy']}\n\n"
script+=f'Silent end hold {clock(t)}–{clock(total)}.\n'
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('[NON-SPOKEN PRODUCTION NOTE: Fictional dramatization, including the Facebook group and gastroenterologist comment. Clearly label story and illustrative comment in any produced version. Not a real testimonial, quote or product endorsement. Maximum finished runtime 180 seconds.]\n\n'+'\n\n'.join(r['copy'] for r in rows)+'\n')
data.update(version=5,words=words,spoken_allocation_seconds=t,total_seconds=total,estimated_seconds_at_140wpm=slower,ums_status='General motility-support criterion introduced before product; proprietary Motilli physiological mechanism not substantiated',segments=rows)
(out/'microsegments.json').write_text(json.dumps(data,indent=2))
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V5\n\nBrief dramatized Facebook discovery; solution criterion before brand; first-person woman; stage-3 brief; ≤3-minute finished runtime.\n\n- [Script and beat map](script-and-beat-map.md)\n- [Narration and disclosure note](script.txt)\n- [Updated editing plan](edit/editing-plan.md)\n- [Evidence](evidence/sources.md)\n- [Previous drafts](versions/)\n')
source=out/'evidence/sources.md'
source.write_text(source.read_text()+'''\n## V5 source distinction\n\nThe Facebook post and gastroenterologist comment are explicitly fictional, not sourced from a real person or group. General clinical context checked at https://www.niddk.nih.gov/health-information/digestive-diseases/gastroparesis/treatment on 2026-09-09: clinicians may address delayed emptying using treatments that improve stomach muscle activity. This is not evidence for Motilli, not a narrator diagnosis, and not a source for the invented quoted wording.\n''')
assert all(r['copy'] in plan for r in rows)
assert all(rows[i]['end']==rows[i+1]['start'] for i in range(len(rows)-1))
print(json.dumps({'words':words,'total':clock(total),'at_140wpm':clock(slower),'changed':[(r['id'],clock(r['start'])+'–'+clock(r['end']),r['copy']) for r in rows[5:9]]},indent=2))
