from pathlib import Path
import json, math, re, shutil

root = Path('brands/motilli/creative/MOT-BLOAT-NUORA-01')
data = json.loads((root/'microsegments.json').read_text())
assert data['version'] == 7
archive = root/'versions/v7-before-podcast-ump'
archive.mkdir(parents=True, exist_ok=True)
for name in ['microsegments.json','script-and-beat-map.md','script.txt','edit/editing-plan.md','README.md']:
    dest = archive/name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root/name, dest)
oldrows = json.loads(json.dumps(data['segments']))
rows = data['segments']
ump = rows[5]
ump['copy'] = "He explained there were a couple of things going on. GLP-1s slow stomach emptying and can slow the contractions that move food along. Then your appetite decreases. You're eating less, so you may get less fiber too. Put those together, and you've got a recipe for constipation—and that backed-up, bloated feeling."
ump['beat'] = 'Slower movement + lower intake → constipation and bloating'
ump['visual'] = 'S01a: Narrator recounts explanation; S01b: stomach/duodenum movement illustration; S01c: distinct side-view smaller meal and fiber-containing foods; S01d: return to narrator on bloated feeling.'
ump['evidence'] = 'Podcast supplies conversational sequence, not a real Facebook quote. GLP-1 motility evidence supports general explanation. Lower fiber intake is a possibility, not universal or the first nutrient everyone cuts. No diagnosis or claim that all bloating has this cause.'
ump['microbeats'] = [
    {'offset_start':0,'offset_end':4,'cue':'He explained','action':'Narrator; conversational lead-in'},
    {'offset_start':4,'offset_end':11,'cue':'GLP-1s slow','action':'Stomach/duodenum illustration; show slower movement without total blockage'},
    {'offset_start':11,'offset_end':17,'cue':'Then your appetite decreases','action':'New smaller-meal composition; show possibility of reduced fiber intake'},
    {'offset_start':17,'offset_end':21,'cue':'Put those together','action':'Narrator; land on constipation and bloated feeling'},
]
rows[8]['evidence'] += ' V8 review: apigenin is a flavone, not an enzyme. Mouse-colon inflammatory and motor findings do not establish human GLP-1 gastric-emptying benefit; current product apigenin dose is unspecified. See evidence/ingredient-mechanism-review-v8.md.'
rows[9]['evidence'] += ' V8 review: odor endpoints are distinct from fermentation, gas volume, or bloating; controlled odor evidence is mixed. No established fermentation-stopping role at seller-listed 0.54 mg/day. See ingredient review.'
t=0
for r in rows:
    r['words'] = 0 if r['reserved_seconds'] else len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",r['copy']))
    r['duration'] = r['reserved_seconds'] or math.ceil(r['words']*60/155+0.35)
    r['start'],r['end'] = t,t+r['duration']
    t=r['end']
total=t+3
def clock(n): return f'{n//60:02}:{n%60:02}'
assert total <= 180
assert rows[6]['copy'] == oldrows[6]['copy']
assert all(rows[i]['copy']==oldrows[i]['copy'] for i in range(len(rows)) if i !=5)

plan=(root/'edit/editing-plan.md').read_text()
plan=plan.replace('V7, restored user-specified structure','V8, targeted podcast UMP revision')
plan=plan.replace('337 drafted words','354 drafted words').replace('02:49','02:56')
plan=plan.replace('Explain mixing and delayed emptying in one anatomy view.','Explain slowed emptying and contractions, then reduced appetite and potentially less fiber; finish with constipation/bloating. Use distinct anatomy and smaller-meal views.')
newlines=[]
for line in plan.splitlines():
    m=re.match(r'\| (M\d+) / ',line)
    if m:
        i=next(i for i,r in enumerate(rows) if r['id']==m[1])
        old,new=oldrows[i],rows[i]
        line=line.replace(old['copy'],new['copy']).replace(old['beat'],new['beat']).replace(old['visual'],new['visual']).replace(old['evidence'],new['evidence'])
        line=re.sub(r'\| \d\d:\d\d–\d\d:\d\d, \d+s \|', f"| {clock(new['start'])}–{clock(new['end'])}, {new['duration']}s |",line)
        if i==5:
            line=line.replace('Comment→anatomy at The stomach normally; pause at small meal.','Anatomy on GLP-1s slow; new meal view on Then your appetite decreases; narrator on Put those together. Microbeats: 4s / 7s / 6s / 4s; align final cut points to recorded words.')
    newlines.append(line)
plan='\n'.join(newlines)+'\n'
plan=re.sub(r'End hold \d\d:\d\d–\d\d:\d\d',f'End hold {clock(t)}–{clock(total)}',plan)
plan+='\n## V8 revision scope and ingredient findings\n\nOnly M06 spoken copy changed. All other spoken lines, including M07 fiber/MiraLAX, remain verbatim. Downstream times shift seven seconds. M06 is 52 words allocated 21 seconds. Full provisional runtime 2:56 including both 12-second ingredient slots and 3-second end hold. Four seconds remain under the hard cap; final copy and voice alignment must fit. The podcast is a supplied text reference, not inspected audiovisual footage.\n\nIngredient research is documented in [the V8 evidence review](../evidence/ingredient-mechanism-review-v8.md). It does not substantiate the proposed apigenin stomach-restart or chlorophyllin anti-fermentation claims. Those two spoken slots remain unresolved for that factual reason; no generic support phrase has been substituted to imply an established solution. The latest user request supersedes the canonical document’s older instruction against naming apigenin.\n'
# Update plan before the related script artifacts.
(root/'edit/editing-plan.md').write_text(plan)
script=(root/'script-and-beat-map.md').read_text()
script=script.split('## Timed working script')[0]
script=script.replace('V7, restored user-specified structure','V8, targeted podcast UMP revision').replace('337 drafted words','354 drafted words').replace('02:49','02:56')
script+='## Timed working script\n\n'
for r in rows:
    script+=f"### {r['id']} · {clock(r['start'])}–{clock(r['end'])} · {r['duration']}s · {r['macro']}\n\n{r['copy']}\n\n"
script+='V8 changes M06 only; all other spoken text is preserved. Ingredient findings: [evidence review](evidence/ingredient-mechanism-review-v8.md). Ingredient slots remain unsubstantiated, so this is a working script, not finished recording copy.\n'
(root/'script-and-beat-map.md').write_text(script)
txt=(root/'script.txt').read_text().replace(oldrows[5]['copy'],ump['copy'])
(root/'script.txt').write_text(txt)
data.update(version=8,status='podcast UMP revised; ingredient research complete, two proposed efficacy claims unsubstantiated',drafted_words_excluding_slots=sum(r['words'] for r in rows),total_seconds=total)
(root/'microsegments.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(root/'README.md').write_text('# MOT-BLOAT-NUORA-01 — V8\n\nTargeted podcast UMP revision. All other spoken copy preserved, including fiber/MiraLAX. Provisional allocation 2:56, with two unresolved 12-second ingredient-action slots and 3-second end hold.\n\n- [Script and timings](script-and-beat-map.md)\n- [Editing plan](edit/editing-plan.md)\n- [Ingredient evidence findings](evidence/ingredient-mechanism-review-v8.md)\n- [Previous drafts](versions/)\n')
assert all(r['copy'] in plan and r['copy'] in script and r['copy'] in txt for r in rows)
print(json.dumps({'version':8,'changed_spoken_rows':['M06'],'UMP_seconds':ump['duration'],'total_seconds':total,'words_excluding_slots':data['drafted_words_excluding_slots'],'fiber_MiraLAX_preserved':True}))
