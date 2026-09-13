from pathlib import Path
import json,re,math,shutil

out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/MOT-BLOAT-NUORA-01')
data=json.loads((out/'microsegments.json').read_text())
oldplan=(out/'edit/editing-plan.md').read_text()
archive=out/'versions/v2';archive.mkdir(parents=True,exist_ok=True)
for name in ['script-and-beat-map.md','script.txt','microsegments.json','README.md']:
    if not (archive/name).exists():shutil.copy2(out/name,archive/name)
if not (archive/'editing-plan.md').exists():shutil.copy2(out/'edit/editing-plan.md',archive/'editing-plan.md')

changes={
'M06':('Discovery — GLP-1 gut slowdown',"What finally made me look at this differently was learning about GLP-1 gut slowdown. My shot could be changing how quickly food moved through my stomach.",'P01: Same woman speaks to phone at kitchen table. At “GLP-1 gut slowdown”, add that exact short label; no diagnosis or medical costume.','Introduce the selected mechanism as the answer to her unresolved question.'),
'M07':('Medication effect — slower stomach emptying',"I'd been focused on how little I was eating. But medicines such as Wegovy can slow stomach emptying. That means food can stay in the stomach longer after a meal.",'S01: Authentic Wegovy source on tablet, highlight slowed stomach emptying. First-person narration continues across source insert.','Give the mechanism an identifiable factual source.'),
'M08':('Normal movement — mix and move',"Normally, the muscles in my stomach mix the food and gradually move it into my small intestine. So digestion depends on that movement happening, even when the meal is small.",'S02: Single isolated stomach-to-duodenum model with normal mixing and gradual passage. No total blockage, product, rotten food or shutdown.','Explain the necessary physical process in ordinary language.'),
'M09':('Slowdown — lingering fullness',"When the stomach takes longer to empty, that full feeling can hang around too. That could help explain why a small lunch was leaving me feeling so uncomfortable afterward.",'S03: Distinct time-and-fullness schematic; one small-meal icon with elapsed-time indicator. No invented hourly measurements.','Connect the mechanism to the small-lunch opening without diagnosing the narrator.'),
'M10':('Belief shift — amount and movement',"That was the part I'd been missing. Eating less and moving food through my stomach are two different things. I was watching the portion size without thinking about the slowdown.",'H07: Side-on kitchen scene; woman looks from partly eaten meal to notes on tablet. No anatomy reuse or visual recovery.','Land the belief shift once, using the opening lived detail.'),
'M11':('Failed attempts — reconsider food blame',"It also changed how I thought about all those foods I'd been blaming. Changing what was on my plate didn't tell me whether slower stomach emptying was contributing to the bloating.",'H08: Macro food diary; hand adds the question “Could stomach emptying matter?” beside existing meal notes. Distinct from tea overhead.','Explain the limit of her prior investigation without claiming dietary approaches never work.'),
'M12':('Solution search — relevant next question',"So I had a better question for my prescriber: could the slowdown be part of what I was feeling, and what digestive support would actually make sense alongside my medication?",'P02: Over-shoulder phone note with that prescriber question. She writes it; no fabricated consultation, recommendation or endorsement.','Turn understanding into a relevant solution search; do not imply a supplement reverses medication effects.'),
'M13':('Ingredient reveal — during her search',"During that search, I looked at a formula with celery juice powder, prebiotic fiber, and chlorophyll. I wanted to understand what was in it before adding another thing to my routine.",'I01: Three distinct labeled ingredient stations. Actual seller-listed ingredients; no product-induced stomach contractions.','Connect ingredient consideration to the ongoing search.'),
'M16':('Product reveal — Motilli consideration',"That formula is Motilli, a daily digestive-support gummy marketed for people on a GLP-1. It gave me a specific ingredient list and routine to review with my prescriber.",'PR01: Actual current Motilli product page on phone; first spoken/visible brand reveal, then ingredients and directions. No prescriber endorsement implied.','Introduce a concrete product for consideration; no proven prokinetic claim.'),
}
rows=data['segments'];t=0
def clock(s):return f'{s//60:02d}:{s%60:02d}'
for r in rows:
    if r['id'] in changes:
        r['beat'],r['copy'],r['visual'],r['purpose']=changes[r['id']]
        r['evidence']='V3 first-person fictional dramatization. Official Wegovy stomach-emptying context and NIDDK general stomach movement; not evidence of Motilli efficacy.' if r['id'] in ['M06','M07','M08','M09','M10','M11','M12'] else 'Seller-listed product facts; dramatized consideration, no claimed use or result.'
    r['words']=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",r['copy']))
    r['duration']=math.ceil(r['words']*60/160+0.5);r['start']=t;t+=r['duration'];r['end']=t
words=sum(r['words'] for r in rows);total=t+3
intro=f'''# Motilli bloating VSL — V3, GLP-1 gut slowdown

Date: 2026-09-09. Concept: MOT-BLOAT-NUORA-01. Script/planning phase only.

User-selected mechanism: GLP-1 gut slowdown, explained specifically as delayed stomach emptying. Preserve a problem-aware woman speaking in first person, Nuora's argument progression, and the bloated-stomach hook. Narrative spine: small meals and lingering discomfort → GLP-1 can slow stomach emptying → movement as well as portion size matters → relevant digestive-support questions → Motilli consideration → everyday comfort aspiration → verified guarantee and CTA.

Voice/provenance: fictional dramatization of an ongoing problem and search; no verified customer account or product result supplied. Retain clear “Dramatized story” identification in any produced version. Adapt personal events to actual experience before using as a real customer's testimonial. Clinical explanation remains qualified: no assertion that every GLP-1 user's bloating has one cause, no gastroparesis diagnosis, and no claim that Motilli reverses medication-induced slowing.

Timing: {words} spoken words; planning pace 160 wpm plus thought breaks and whole-second allocations. Narration {clock(t)}, final hold 3s, total {clock(total)}. Provisional until final voice alignment. V1 and V2 preserved under versions/.

V3 changes: M06–M12 now carry one coherent slowdown explanation; gas/constipation and extra-fiber detours removed from that passage. M13 and M16 reconnect product consideration to her search. M14 retains individual tolerance in its ingredient explanation. Other copy remains as in V2; all downstream timing recalculated.
'''
reference=oldplan[oldplan.index('## Inputs and reference findings'):oldplan.index('## Revision and editorial strategy')]
reference=reference.replace('preserve problem awareness and the hook concept.','preserve problem awareness and the hook concept; use GLP-1 gut slowdown as the central mechanism.')
plan=intro+'\n'+reference+'''
## Revision and editorial strategy

Keep one fictional woman and a continuous first-person account. In the mechanism passage use the narrator, real prescribing information, one stomach-movement model, then a separate elapsed-time schematic, a kitchen reflection scene and a food-diary detail. Remove the prior colon/gas schematic and fiber-comparison cards from this passage. These are distinct views with different editorial purposes, not variations of a repeated anatomical torso. Source video was not supplied: this is original direction, not an observed Nuora frame audit.

The stomach animation demonstrates general digestion only. No gummy or ingredient triggers faster emptying, no restored squeeze, no instant flat stomach, no food rotting/fermenting in the stomach, no dead or paralyzed organ, and no total blockage. The desired future dinner remains an aspiration. Product consideration and current directions are distinct from clinical proof. No actual customer trial or efficacy evidence has been supplied.

## Updated microsegment and visual schedule

Every scene remains an asset gap: no media generation, voice production or timeline assembly has occurred. Use straight cuts at the next row's opening phrase with continuous narration; after final voice selection align every boundary and caption anew.

| ID / beat | Exact narration | Provisional time | Visual and visible action | Source / asset gap | Incoming / outgoing cut cue | Movement / captions / sound | Purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    cue=('Cold open; ' if i==0 else 'Straight cut on first word; ')+('hold into silent tail.' if i==len(rows)-1 else 'straight cut at next row’s first word.')
    if r['id']=='M15':cue+=' At “This formula”, cut to exact chlorophyllin ingredient label.'
    if r['id']=='M18':cue+=' At “That’s a routine”, cut from directions to bedtime glass.'
    gap='Original illustrative scene required; no footage selected.'
    if r['visual'].startswith('PR'):gap='Current approved product reference or authentic current-page capture required.'
    if r['id']=='M07':gap='Capture the real official Wegovy source; verify excerpt on screen.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])}, {r['duration']}s | {r['visual']} | {gap} | {cue} | Restrained physical motion, phrase captions ≤2 lines, clear Dramatized story, continuous VO. | {r['purpose']} |\n"
plan+=f'\nSilent end hold: {clock(t)}–{clock(total)}, current product, See Motilli, guarantee reference and dramatization disclosure.\n\n'
plan+=oldplan[oldplan.index('## Voice, captions and audio'):]
plan+='''
## V3 planned visual variety check

No exact source reuse selected. Continuous narrator coverage is intentional. Mechanism views: real source page, stomach model, elapsed-time schematic, kitchen scene and diary detail. Each teaches a different idea. Product frames use distinct actions: phone discovery, gummy demonstration, instructions, options, guarantee, end hold. Verify visual similarity and exact source reuse after assets exist and again before export. The current internal-editor entry point is to be located only if actual production is requested; no stale route has been assumed. GPT Image 2 and Google Omni remain the production models; HyperFrames and Remotion are prohibited.
'''
(out/'edit/editing-plan.md').write_text(plan)
script=intro+'\n## Timed script\n\n'
for r in rows:script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['beat']}\n\n{r['copy']}\n\n"
script+=f'Final silent hold {clock(t)}–{clock(total)}.\n'
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('[NON-SPOKEN PRODUCTION NOTE: Fictional dramatization, not an actual customer testimonial. Retain clear Dramatized story identification in production.]\n\n'+'\n\n'.join(r['copy'] for r in rows)+'\n')
data.update(version=3,words=words,spoken_allocation_seconds=t,total_seconds=total,mechanism='GLP-1 gut slowdown, specifically delayed stomach emptying',segments=rows)
(out/'microsegments.json').write_text(json.dumps(data,indent=2))
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V3\n\nFirst-person woman; problem-aware GLP-1 bloating; central mechanism: GLP-1 gut slowdown / delayed stomach emptying. Explicitly dramatized draft.\n\n- [Script and timings](script-and-beat-map.md)\n- [Narration](script.txt)\n- [Editing plan](edit/editing-plan.md)\n- [Sources](evidence/sources.md)\n- [Previous versions](versions/)\n')
sources=out/'evidence/sources.md'
sources.write_text(sources.read_text()+'''\n## V3 mechanism verification\n\nRechecked 2026-09-09: https://www.wegovy.com/prescribing-information.html supports slower stomach emptying and lists bloating. https://www.niddk.nih.gov/health-information/digestive-diseases/gastroparesis/definition-facts explains stomach-muscle movement and slow-emptying context; not used to diagnose the narrator with gastroparesis. Mechanism is presented as a possible contributor, not a proven personal diagnosis or a Motilli treatment claim.\n''')
assert all(r['copy'] in plan for r in rows)
assert all(rows[i]['end']==rows[i+1]['start'] for i in range(len(rows)-1))
print(json.dumps({'words':words,'narration':clock(t),'total':clock(total),'changed':[(r['id'],clock(r['start'])+'–'+clock(r['end']),r['duration'],r['copy']) for r in rows if r['id'] in changes]},indent=2))
