from pathlib import Path
import json,re,math,shutil

out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/MOT-BLOAT-NUORA-01')
data=json.loads((out/'versions/v6-evidence-slot/microsegments.json').read_text())
oldplan=(out/'edit/editing-plan.md').read_text()
archive=out/'versions/v6-evidence-slot';archive.mkdir(parents=True,exist_ok=True)
for f in ['script-and-beat-map.md','script.txt','microsegments.json','README.md']:
    if not (archive/f).exists():shutil.copy2(out/f,archive/f)
if not (archive/'editing-plan.md').exists():shutil.copy2(out/'edit/editing-plan.md',archive/'editing-plan.md')
rows=data['segments']
rows[0].update(copy="If your stomach looks like this on a GLP-1, this was mine before—and this is mine now. I can finally get through dinner without unbuttoning my jeans. Give me thirty seconds to explain what changed.",visual='H01: User-planned before/after occupies the opening itself. Before appears at this was mine before; direct cut to same subject after at this is mine now. Return to narrator on dinner payoff. Treat source as pending genuine same-customer evidence; no synthetic transformation.',evidence='Conditional customer outcome; footage/account not provided. Visual payoff does not independently prove Motilli caused the change.')
rows[1].update(copy="I was scrolling through a Facebook GLP-1 group when a gastroenterologist's comment caught my attention.")
rows[2].update(copy="He wrote, 'GLP-1s can slow stomach emptying, so food stays longer. If that's causing the fullness, ask about motility support—helping food move through the stomach.'",visual='F02: Concise illustrative comment with full conditional wording; label Dramatized example—not a real post if no actual comment. No Motilli branding or implied expert endorsement.')
rows[3].update(macro='Product bridge',beat='Name product after solution target',copy="That led me to Motilli.",visual='PR00: First current Motilli product-page reveal; entirely separate from doctor/group UI.',evidence='Conditional narrative discovery; no asserted product effect on stomach movement.',reserved_seconds=0)
# No separate narrated result block: the user's opening visual carries the claimed transformation.
rows=[r for i,r in enumerate(rows) if i not in [4,7]]
rows[-1]['copy']="I've linked Motilli below so you can see the ingredients and directions for yourself. If this sounds familiar, tap below and take a look."
def clock(s):return f'{s//60:02d}:{s%60:02d}'
t=0
for i,r in enumerate(rows):
    r['id']=f'M{i+1:02d}';r['words']=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",r['copy']))
    r['reserved_seconds']=0;r['duration']=math.ceil(r['words']*60/150+0.5);r['start']=t;t+=r['duration'];r['end']=t
total=t+3;words=sum(r['words'] for r in rows)
prefix=rows[0]['copy'].split('Give me thirty seconds')[0]
promise_start_estimate=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",prefix))*60/150
assert total<180
intro=f'''# Motilli bloating VSL — V6b, immediate visual payoff

Date: 2026-09-09. Latest user clarification: before/after appears immediately and creates the question “how did she solve this?” Let the images establish the claimed outcome; do not insert a separate narrated recovery block into the middle. Retain first-person woman, user stage-3 premise, problem awareness, brief Facebook discovery, gut slowdown and solution-target introduction before Motilli. Hard maximum 3 minutes.

This is a complete conditional creative script, not a verified customer testimonial. The before/after and dinner-comfort claim require the same actual customer's truthful account and genuine material. The visual change itself does not establish causation by Motilli. The Facebook/doctor exchange remains fictional unless an actual source is supplied, and must be clearly identified as such. No images or outcomes have been generated. Product evidence and source provenance remain dependencies outside the spoken copy, rather than an invented recovery story or an empty spoken result slot.

Timing: {words} spoken words. At 150 wpm with short breaks/rounding: narration {clock(t)}, final hold 3s, total {clock(total)}. All timing provisional; measured final export ≤180s. The promise begins approximately {promise_start_estimate:.1f}s into the hook; mechanism/solution target ends {clock(rows[2]['end'])}, product bridge ends {clock(rows[3]['end'])}. These allocations put the explanatory reveal within thirty seconds of that estimated promise onset. They do not substantiate the claimed personal result or prove the provider/recorded voice timing. Final alignment must verify the exact interval.

Narrative order: visible claimed outcome → how question → Facebook discovery → slow-emptying explanation and motility-support target → Motilli → actual formula/routine → guarantee/CTA. Motility support is the solution category; it is not evidence that this formula accelerates stomach emptying. No doctor-product endorsement, invented treatment timeline, fabricated study or alleged medical concealment is introduced.
'''
plan=intro+'''
## Reference and editing strategy

Read the existing V6 plan, V6 conditional hook and earlier Nuora transcript analysis before this update. Only the PDF/transcript and user's description of the visual opening were available; no original Nuora video or actual transformation footage supplied. Do not claim an observed source-video cut audit. This is original editorial direction implementing the user's stated visual logic.

Show before and after immediately on their exact spoken cues. Keep the before/after physically faithful to the same subject, with truthful context and no generative treatment proof, digital slimming or deceptive posture changes. The remaining question is how; immediately move to the brief support-group scene, then the solution target before brand. No additional result-story slot in the middle. At product reveal remove the fictional doctor/group card so its proximity does not imply endorsement.

## Updated schedule

| ID / beat | Exact conditional copy | Provisional time | Visual/action | Evidence/asset gap | Incoming/outgoing cut cue | Caption, motion and sound | Purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    cue=('Cold open; ' if i==0 else 'Hard cut on first phrase; ')+('hold into silent tail.' if i==len(rows)-1 else 'hard cut at next row’s first phrase.')
    if i==0:cue+=' Cut before→after exactly on this is mine now; narrator/dinner detail on I can finally.'
    if i==2:cue+=' Preserve entire conditional comment; no cropped-out if clause.'
    if i==3:cue+=' Doctor/group UI absent before brand.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])}, {r['duration']}s | {r['visual']} | {r['evidence']} Source assets unselected. | {cue} | Natural movement, continuous woman VO, phrase captions max 2 lines. Fictional group/comment plainly labeled. | {r['macro']} |\n"
plan+=f'\nSilent product/CTA hold {clock(t)}–{clock(total)}. No additional result narration.\n\n'
finish=oldplan[oldplan.index('## Voice, variety and QA'):]
finish=finish.replace('actual customer proof;','')
finish=finish.replace('obtain the missing true account and matched claim evidence, resolve the conditional hook/result,','obtain the true account and matched claim evidence, substantiate the conditional visual hook,')
finish=finish.replace('The evidence slot prevents this from being represented as a complete record-ready testimonial.','The conditional transformation claim and unsupplied genuine source account prevent this from being represented as a verified, record-ready testimonial. There is no longer a placeholder in the spoken copy.')
plan+=finish
(out/'edit/editing-plan.md').write_text(plan)
script=intro+'\n## Timed conditional script\n\n'
for r in rows:script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['beat']}\n\n{r['copy']}\n\n"
script+=f'Final hold {clock(t)}–{clock(total)}.\n'
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('[NON-SPOKEN NOTE: Conditional creative script. Personal transformation and dinner outcome require genuine customer evidence; the invented Facebook/doctor scene must be clearly identified as dramatized unless sourced. No product-to-result causation has been verified.]\n\n'+'\n\n'.join(r['copy'] for r in rows)+'\n')
(out/'microsegments.json').write_text(json.dumps(dict(version='6b',date='2026-09-09',status='complete conditional copy; source/claim evidence outstanding',spoken_words=words,planning_wpm=150,total_seconds=total,max_finished_seconds=180,promise_start_estimated_seconds=promise_start_estimate,promise_target='explanation and solution target followed by product reveal; personal result remains unverified',segments=rows),indent=2))
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V6b\n\nBefore/after supplies immediate visual payoff. Conditional full copy, no spoken placeholder. Genuine customer/source/claim evidence still outstanding.\n\n- [Current script and timings](script-and-beat-map.md)\n- [Current editing plan](edit/editing-plan.md)\n- [Sources](evidence/sources.md)\n- [Previous versions](versions/)\n')
assert all(r['copy'] in plan for r in rows)
assert all(rows[i]['end']==rows[i+1]['start'] for i in range(len(rows)-1))
print(json.dumps(dict(words=words,total=clock(total),promise_start=promise_start_estimate,segments=[(r['id'],clock(r['start'])+'–'+clock(r['end']),r['copy']) for r in rows]),indent=2))
