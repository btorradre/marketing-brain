from pathlib import Path
import json, re, math, shutil

out=Path('/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/MOT-BLOAT-NUORA-01')
previous=json.loads((out/'microsegments.json').read_text())
archive=out/'versions/v1'
archive.mkdir(parents=True,exist_ok=True)
for name in ['script-and-beat-map.md','script.txt','microsegments.json','README.md']:
    if not (archive/name).exists(): shutil.copy2(out/name,archive/name)
if not (archive/'editing-plan.md').exists(): shutil.copy2(out/'edit/editing-plan.md',archive/'editing-plan.md')

copy=[
"If your stomach looks like this on a GLP-1, mine does too. I'm eating less, but some days I feel more bloated than ever.",
"I can sit down to a small lunch, eat a few bites, and already feel that tightness across my stomach. I look at what's left on my plate and think, how am I this full?",
"The worst part is getting dressed in the morning and feeling good in something, then wanting to peel it off by the afternoon because the waistband is digging into me.",
"I wanted to feel comfortable in my clothes again. Instead, I'm standing sideways in the mirror before we go out, deciding whether I need a looser top.",
"I've tried peppermint tea. I've gone back over what I ate, wondering whether it was the dairy, or the meal before that. Some days, it feels like every food becomes a suspect.",
"And I keep coming back to the same question: if I'm eating so much less, why does my stomach still feel this uncomfortable? I wanted an explanation I could actually understand.",
"Then I read that GLP-1 medicines such as Wegovy can slow how quickly the stomach empties. Bloating is listed as a side effect too. That gave me something more useful to ask about.",
"The way I understand it now, my stomach has to mix the food and gradually move it into my small intestine. It takes muscular movement, and it takes time.",
"So a smaller meal doesn't necessarily mean that full feeling disappears quickly. How long my stomach takes to empty can matter too. That was the connection I'd been missing.",
"I also learned that gas and constipation can contribute to bloating. So I couldn't look at my stomach in the mirror and know exactly what was causing it.",
"Even the advice to add more fiber had more to it than I realized. Some people get more gas with extra fiber. I needed to pay attention to the type and my own response.",
"I wanted to understand what I was taking before I added another thing. Clear ingredients, simple directions, and something I could realistically fit into my day. Those became my starting points.",
"One formula I looked at combined celery juice powder, prebiotic fiber, and chlorophyll. I recognized celery, but I wanted to understand the other ingredients before deciding how I felt about the combination.",
"I learned that prebiotic fiber provides food for bacteria in the gut. That helped me understand its purpose, while remembering that my own tolerance still mattered when I was already feeling bloated.",
"Chlorophyll was another name I recognized once I read about it: the green pigment in plants. This formula lists a related form called chlorophyllin, alongside the celery juice powder and fiber.",
"That formula is Motilli. It's a daily digestive-support gummy. What interested me was having those ingredients together, with a routine I could understand and discuss with my prescriber.",
"And honestly, I liked the idea of a gummy. When I'm already feeling full, another drink to mix or a capsule to swallow doesn't sound appealing. Chewing something felt more manageable.",
"The directions are two gummies before bed with a full glass of water. That's a routine I can picture fitting into my evening, alongside brushing my teeth and getting ready for bed.",
"What I care about is how I actually feel. I'd want to keep track of the bloating and my comfort, so I could judge my own experience instead of guessing.",
"I want to put on an outfit and leave it on. I want to enjoy dinner without quietly loosening my jeans underneath the table. Mostly, I want an evening where my stomach isn't taking up all my attention.",
"I've put the Motilli page below if you want to look at it too. You can see the ingredients, the directions, and the bottle options in one place.",
"The guarantee caught my attention as well. It's ninety days from delivery, and it includes opened bottles. So opening it doesn't take away the option to request a refund.",
"If you're doing the same thing I am, checking your stomach and second-guessing every meal, you'll understand why I'm looking into this. Tap below to take a look at Motilli.",
]
assert len(copy)==len(previous['segments'])
rows=previous['segments']; t=0
def clock(s):return f'{s//60:02d}:{s%60:02d}'
for r,s in zip(rows,copy):
    r['copy']=s;r['words']=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",s))
    r['duration']=math.ceil(r['words']*60/160+0.5);r['start']=t;t+=r['duration'];r['end']=t
    if r['id'] not in ['M07','M08','M09','M10','M11','M14','M15','M18','M22']:
        r['evidence']='Fictional first-person dramatization; no actual customer account or Motilli use/result supplied. '+r['evidence']
rows[0]['visual']='H01: Same fictional adult woman throughout; clothed side profile in her bedroom mirror, then looks toward phone camera. Show clear persistent “Dramatized story” disclosure; no before/after.'
rows[4]['visual']='H05: Kitchen close overhead; her hand rests beside peppermint tea and a food diary. No product-failure montage or discarded medication.'
rows[5]['visual']='P01: Same woman seated at kitchen table, talking directly to her phone; pause after her question, no professional presenter manner.'
rows[11]['visual']='P02: Over-shoulder view as she writes Ingredients / Directions / Fits my routine in a notebook; narration continues.'
rows[12]['visual']='I01: Three separate ingredient stations with labels; original illustrative insert representing the formula she is considering.'
rows[15]['visual']='PR01: Actual current Motilli product page on her phone, first brand reveal; finger scrolls from name to ingredients. No received-order or use implication.'
rows[16]['visual']='PR02: Verified bottle and gummy product demonstration on neutral surface; hands open bottle and show gummy texture. Clearly product demonstration, not a customer trial.'
rows[17]['visual']='PR03: Close-up verified printed or online directions at Two gummies, then distinct bedtime water-glass scene. Do not show narrator consuming product.'
rows[18]['visual']='H06: Blank symptom journal, headings Bloating and Comfort; hand sets pen alongside it. No invented outcome tracking or elapsed treatment timeline.'
rows[19]['visual']='F01: Imagined social dinner, woman engaged with friends, no belly transformation. Clearly mark “What I want to get back to”; never show as a Motilli result.'
rows[22]['purpose']='Return to the narrator’s ongoing problem and invite product-page review; no claim of recovery.'

words=sum(r['words'] for r in rows);total=t+3
intro=f'''# Motilli bloating VSL — V2, first-person woman

Date: 2026-09-09. Concept: MOT-BLOAT-NUORA-01. Status: first-person script draft and updated editing plan; no media generated.

Latest user direction: the narrator is a woman going through the problem. She speaks about her meals, clothing, frustration and search in first person. Problem-aware GLP-1 bloating remains the focus. The hook continues to address the viewer briefly, then immediately establishes “mine does too.” She has not claimed to have taken Motilli or recovered.

Narrator status: FICTIONAL DRAMATIZATION, not a verified customer testimonial. Personal events, research and consideration are written narrative devices. Show an unambiguous “Dramatized story” disclosure throughout any produced version and retain this note with scripts handed to collaborators. If a real customer will deliver it as her own experience, replace fictional events with her actual account before recording. Do not remove the disclosure and present the same invented account as authentic.

Timing: {words} spoken words at a planning pace of 160 wpm, plus per-segment thought breaks and rounding. Narration allocation {clock(t)}; final hold 3s; planned total {clock(total)}. All timing is provisional pending recorded delivery and word alignment. V1 is preserved under versions/v1/.

Framework: recognition → lived frustration → attempted explanations → discovery → understandable problem mechanism → buying criteria → ingredients → product consideration → routine → desired-life callback → guarantee → CTA. Desired relief is an aspiration. The actual customer-results beat is unavailable; no result has been invented to fill it.

Current product and guarantee details use the sources already checked in this conversation; see evidence/sources.md. Ingredient presence and format do not establish that Motilli treats GLP-1 bloating or reverses delayed stomach emptying. The revised voice does not expand the claims.
'''
old=(out/'edit/editing-plan.md').read_text()
reference=old[old.index('## Inputs and reference findings'):old.index('## Overall editing strategy')]
reference=reference.replace('- Latest request: bloating, problem-aware, hook beginning If your stomach looks like this on a GLP-1.','- Latest request: first-person perspective of a woman currently experiencing GLP-1 bloating; preserve problem awareness and the hook concept.')
plan=intro+'\n'+reference+'''
## Revision and editorial strategy

V2 replaces the educator presentation with a woman speaking from an ongoing problem and personal search. Use one consistent fictional woman and home environment. Her scientific understanding must sound learned, qualified and conversational. Avoid customer-success montage, received-order scenes, capsule superiority, clinical authority costume, product consumption or invented treatment timeline. Frame her social-life payoff as what she wants to regain, not what Motilli restored.

Keep every B-roll insert distinct: bedroom profile; meal overhead; office waistband; hallway wardrobe decision; tea and food diary; seated phone conversation; real prescribing-information excerpt; stomach mixing model; time schematic; colon diagram; fiber cards; notebook criteria; ingredient trio; bacteria-and-fiber schematic; celery and pigment macros; phone product-page discovery; gummy demonstration; directions and bedtime glass; blank journal; imagined social dinner; page options; guarantee card; final packshot. Scientific views are different by subject and composition. Planned reuse is limited to deliberate continuous narrator coverage; no repeated B-roll source selected. Final visual/source audit remains pending until assets exist.

Use hard cuts on the first spoken word of each row with uninterrupted voice audio. Additional internal cut cues are specified where needed. Natural physical movement, no ornamental crossfades or zoom variants masquerading as new scenes. This is original editorial direction derived from the supplied transcript, not an observed frame-by-frame replication of Nuora.

## Updated microsegment and visual schedule

| ID / beat | Exact narration | Provisional timing | Visual / action | Source or asset gap | Incoming / outgoing cut cue | Movement, captions and sound | Purpose |
|---|---|---|---|---|---|---|---|
'''
for i,r in enumerate(rows):
    cue=('Cold open; ' if i==0 else 'Hard cut at first word; ')+('hold into silent tail.' if i==len(rows)-1 else 'hard cut at next row’s first word.')
    if r['id']=='M15':cue+=' Cut from plant macro to exact ingredient name at “This formula”.'
    if r['id']=='M18':cue+=' Cut from directions to water glass at “That’s a routine”.'
    gap='Original scene or properly sourced footage needed; asset not selected.'
    if r['visual'].startswith('PR'):gap='Current approved bottle/gummy references or live page capture needed; actual media not selected.'
    if r['id']=='M07':gap='Use authentic official source capture; no fabricated expert or paper.'
    plan+=f"| {r['id']} / {r['beat']} | {r['copy']} | {clock(r['start'])}–{clock(r['end'])}, {r['duration']}s | {r['visual']} | {gap} | {cue} | Restrained physical movement; phrase captions, max 2 lines; persistent Dramatized story; uninterrupted narrator VO. | {r['purpose']} |\n"
plan+=f'\nFinal silent hold: {clock(t)}–{clock(total)}. Stable product, See Motilli, and guarantee terms reference. Retain dramatization disclosure.\n'
finish=old[old.index('## Voice, captions and audio'):]
finish=finish[:finish.index('## Visual variety audit')]+finish[finish.index('## Production order and delivery QA'):]
finish=finish.replace('Warm, conversational, matter-of-fact female brand presenter; no clinician costume or impersonated testimonial.','Warm, candid first-person woman currently experiencing the problem; a clearly disclosed dramatization. Speak like a woman describing her evening to a friend. Let frustration appear in the specific details without theatrical distress. No clinician costume or impersonated real customer.')
finish=finish.replace('No music in opening;','Keep a legible “Dramatized story” disclosure separate from speech captions throughout. No music in opening;')
plan+='\n'+finish

# Update plan first; keep the exact new script and all current allocations synchronized.
(out/'edit/editing-plan.md').write_text(plan)
script=intro+'\n## Timed first-person script\n\n'
for r in rows:script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['macro']} / {r['beat']}\n\n{r['copy']}\n\n"
script+=f'End hold {clock(t)}–{clock(total)}: no narration.\n'
(out/'script-and-beat-map.md').write_text(script)
(out/'script.txt').write_text('[NON-SPOKEN PRODUCTION NOTE: Fictional dramatization. Retain a clear Dramatized story disclosure in any produced version. This is not an actual customer testimonial.]\n\n'+'\n\n'.join(copy)+'\n')
(out/'microsegments.json').write_text(json.dumps({'version':2,'date':'2026-09-09','narrator':'first-person woman, explicitly fictional dramatization','words':words,'planning_wpm':160,'spoken_allocation_seconds':t,'end_hold_seconds':3,'total_seconds':total,'timing_status':'provisional; no recorded alignment','segments':rows},indent=2))
(out/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V2\n\nFirst-person woman experiencing GLP-1 bloating; explicitly dramatized draft, no product-result claim.\n\n- [Current script and timed beat map](script-and-beat-map.md)\n- [Narration with required non-spoken provenance note](script.txt)\n- [Updated editing plan](edit/editing-plan.md)\n- [Sources](evidence/sources.md)\n- [V1 archive](versions/v1/)\n')
assert all(rows[i]['end']==rows[i+1]['start'] for i in range(len(rows)-1))
assert all(r['copy'] in plan for r in rows)
print(json.dumps({'words':words,'total':clock(total),'narration':clock(t),'segments':[(r['id'],clock(r['start'])+'–'+clock(r['end']),r['duration']) for r in rows]},indent=2))
