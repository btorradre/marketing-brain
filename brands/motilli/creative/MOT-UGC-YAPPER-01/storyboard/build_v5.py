"""Exact updated-script storyboard; saves the editing plan before image production."""
from pathlib import Path
import json, re, hashlib

ROOT = Path(__file__).resolve().parents[1]
OLD = json.loads((ROOT/'versions/v4-before-updated-script/storyboard/cutroom-spec.json').read_text())
SOURCE = (ROOT/'script/user-updated-v5.txt').read_text()
paras = [' '.join(l for l in p.splitlines() if not l.isupper()).strip() for p in SOURCE.split('\n\n')]
paras = [p for p in paras if p]
V1 = ROOT/'assets/images-v1'
V2 = ROOT/'assets/images-v2'
V3 = ROOT/'assets/images-v3'
V3.mkdir(exist_ok=True)
P = str(V1/'P01-presenter-base.png')
assets = {
 'presenter':P,
 'stomach':str(V1/'I03-stomach-emptying.png'),
 'celery':str(V1/'I06-celery.png'),
 'chlorophyllin':str(V1/'I07-chlorophyllin.png'),
 'fiber':str(V2/'B14-low-bulk-fiber-overlay.png'),
 'ingredients':str(V2/'B15-diy-ingredients-overlay.png'),
 'product':str(V2/'B17-Motilli-product-overlay.png'),
 'routine':str(V2/'B18-iphone-gummies-water.png'),
 'dinner':str(V1/'I10-dinner.png'),
 'mirror':str(V2/'B21-mirror-smile.png'),
 'clearing':str(V2/'B22-candid-plate-clearing.png'),
 'leaving':str(V2/'B24-candid-heading-out.png'),
}
for a in ['unfinished-dinner','loose-jeans','kitchen-wait','fiber-stirring','morning-heavy','pharmacy','research','river','gas-diagram','group-post','cta']:
 assets[a]=str(V3/(a+'.png'))

# Each tuple gives sentence count, selected picture, visible action, cut cue and dramatic purpose.
rows = [
 [(1,'presenter','Same car presenter, close eye-level frame; direct eye contact.','Open immediately on I was; no title pre-roll.','Recognition — identify the weight-loss/discomfort contradiction.'),
  (2,'presenter','Hold the same presenter and let the invitation breathe.','Continue performance through Because nobody told me; no forced cut.','Curiosity — promise the missing explanation.')],
 [(2,'presenter','Small acknowledging nod; no scale numbers or weight-loss montage.','Keep voice conversational on actually working.','Credibility — acknowledge the shot was working.'),
  (2,'presenter','Presenter describes the heaviness with understated discomfort.','Stay on face for concrete; no literal concrete inside anatomy.','Agitation — make the persistent feeling recognizable.'),
  (3,'unfinished-dinner','Table-level candid view: fork set down beside a meal with only a few bites taken; body turns away.','Cut on a few bites at dinner for 3s; return on And it did not matter, following actual wording.','Agitation — show why even a small dinner feels difficult.')],
 [(1,'loose-jeans','Waist-level detail: mature hand lightly checks extra room at denim waistband; tee stays over abdomen.','Cut on My jeans for 2s; return for leaving the dinner table early.','Contradiction — clothes improve while comfort does not.'),
  (1,'kitchen-wait','Side/rear kitchen wide: same woman rests both hands on counter and waits, gaze toward window.','Straight cut on stand in the kitchen; hold about 3s, then back.','Isolation — make waiting after meals tangible.'),
  (1,'presenter','Same presenter admits she could not explain it.','Return before And I could not explain it, aligned to exact words.','Empathy — vulnerability belongs on her face.')],
 [(3,'presenter','Reflective, slight pause after That was the thing.','Continuous face coverage; no numerical scale shot.','Open loop — weight loss was the wrong expectation.')],
 [(2,'presenter','Matter-of-fact delivery of the advice.','Stay on My doctor; do not invent a clinician scene.','Prior solution — establish she followed advice.'),
  (1,'fiber-stirring','Overhead domestic action: one hand stirs cloudy water, plain powder container and breakfast bowl nearby.','Cut on mixing fiber powder for 3s; return before following every piece of advice.','Effort — show the morning routine distinctly from the later ingredient image.'),
  (4,'presenter','Steady presenter, small pauses between Weeks and Then a couple of months.','Let the brief sentence fragments create pacing; no invented calendar graphic.','Frustration — effort and time without the desired feeling.'),
  (1,'morning-heavy','Dim bedroom side angle: same woman sits on bed edge at dawn, quiet tired posture, gaze down.','Cut on waking up every morning for 3s; straight return.','Persistence — the problem starts before breakfast.')],
 [(1,'pharmacy','Over-shoulder pharmacy aisle: same woman hesitates near digestive-care shelves, face turned from camera.','Cut on went to the pharmacy for 3s; captions carry MiraLAX, no invented readable packaging.','Escalation — an ordinary pharmacy visit becomes an emotional low point.'),
  (2,'presenter','Face carries embarrassment without a staged crying reaction.','Back on And that felt; hold through gone wrong.','Vulnerability — explain why the purchase mattered.'),
  (3,'presenter','Same setup, lower intensity; slight pause before I just wanted to feel okay.','Keep these thoughts together; avoid another aisle insert.','Empathy — land the human need.')],
 [(4,'presenter','Measured delivery: acknowledge partial help, then disappointment.','Hold face through Something was definitely still missing.','Open loop — acknowledge experience without a fake comparison graphic.')],
 [(3,'research','Overhead evening desk: laptop with indistinct article layout, handwritten notes, mug and reading glasses; mature hand on trackpad.','Insert on thirty different articles for 3s; continuous narration.','Search — show effort without inventing an authoritative quotation.'),
  (1,'presenter','Presenter introduces what she read.','Return before gastroenterologist; no fake doctor portrait or credentials.','Discovery — bridge from search to explanation.')],
 [(1,'presenter','Small natural reset before the explanation.','Brief hold on He explained it like this.','Orientation — invite the viewer into a simple explanation.'),
  (3,'stomach','Single educational stomach cutaway; later motion is gentle wall contraction/churning, not a blocked valve.','Cut on stomach is basically a muscle; cover about 4s, return or hold as aligned.','Mechanism — establish the organ and movement once.'),
  (2,'river','Overhead shallow river view: broad upstream pool feeding a narrow gentle trickle, a few floating leaves.','Straight cut on Think of a river; hold 4s. A metaphor, never a clinical before/after.','Understanding — translate slowed flow into the script’s metaphor.'),
  (4,'gas-diagram','Flat gut-lumen schematic: contents and several gas pockets within a soft tube; no full torso or repeated stomach.','Cut on Food backs up for 3s; return before all that pressure lands.','Mechanism — give gas/pressure a separate visual vocabulary.'),
  (3,'presenter','Return to direct eye contact; slight release on It was the gut slowdown.','Hard return on It was not a diet problem, using the exact spoken words.','Relief — remove self-blame and close the first loop.')],
 [(2,'presenter','Same presenter, curiosity rather than a sales pivot.','Hold the question through slowdown itself.','Second loop — what addresses it?')],
 [(3,'group-post','Flat illustrated social-group post card, clearly labeled Illustrative recreation; no phone video.','Overlay on GLP-1 support group for 4s, then return; keep mouth and captions clear.','Discovery — move from research to the peer account.')],
 [(3,'celery','Distinct close view of celery stalks and juice; neutral ingredient image.','Overlay on apigenin from celery juice for 3s; return for the receptor statement.','Ingredient 1 — give an unfamiliar name a concrete anchor; no simulated proof.')],
 [(1,'chlorophyllin','Dark-green ingredient sample with its existing chlorophyllin label, separate from celery.','Overlay on Second for 3s; return for clinical wording.','Ingredient 2 — visually separate the second ingredient without an efficacy animation.')],
 [(2,'fiber','Small fine powder portion beside mixed water, existing category image.','Overlay on soluble prebiotic fiber for 3s; face for wrong kind qualifier.','Ingredient 3 — make the type distinction legible.')],
 [(2,'presenter','Same presenter recounts the other woman’s experience.','Stay on face; no invented gym testimonial or transformation.','Peer story — retain the anecdote without creating false proof.')],
 [(2,'presenter','Skeptical recollection; slight head tilt on 2019.','Hold I almost kept scrolling and prior celery-juice experience.','Objection — voice the viewer’s skepticism.'),
  (2,'presenter','Continue the reply in her own conversational voice.','Hold on all three together; no formula ratio numbers added.','Answer — keep the stated distinction clear.')],
 [(1,'ingredients','Separate named ingredient samples on a domestic table.','Overlay on tried them separately for 3s; remove before So I found.','Selection — show why she looked for a combined blend.'),
  (2,'product','Exact approved Motilli cutout overlays the unchanged presenter, below/right of face.','Reveal on So I found the same one for 4s; no extra spoken brand line.','Product reveal — introduce Motilli visually while preserving the new script.')],
 [(1,'routine','Candid bedside palm with exactly two forest-green heart gummies and a full glass of water.','Full-frame insert on two gummies for about 3s; direct return.','Demonstration — make the nightly action immediately understandable.')],
 [(3,'presenter','Disappointment followed by a modest decision to persist.','Keep the first-week admission on face; no promise of instant results.','Expectation — allow uncertainty.')],
 [(2,'dinner','Warm close dinner-table detail with her relaxed hand and companion’s hand; ordinary meal.','Insert on dinner with my husband for 3s, then return.','Payoff — a normal dinner is the emotional center.'),
  (3,'presenter','Hold her face; allow Just fine its own small pause.','Continuous close performance through I had not felt that in months.','Relief — emphasize ordinary comfort, not a dramatic transformation.')],
 [(3,'mirror','Morning mirror action: same woman looks at her own reflected eyes and smiles privately.','Insert on my mornings felt different for 3s; return for the waking-up callback.','Progress — a new morning action, not reused bed footage.')],
 [(2,'leaving','Rear three-quarter action: woman picks up keys and heads outside, gaze toward door.','Insert on had not thought about my stomach for 3s; face for That was new.','Freedom — attention returns to normal life.')],
 [(2,'presenter','Same current presenter; no split-screen body before/after.','Hold This is me now with quiet certainty.','Present tense — bring the story back to today.')],
 [(2,'clearing','Side/rear dining view: calmly clears a used plate, looking at the task.','Cut on I get through dinner for 3s; return for the pressure statement.','Practical payoff — distinct action and angle from the earlier dinner insert.'),
  (1,'presenter','Relaxed, conversational presenter.','Stay on not mapping my whole day; do not repeat doorway B-roll.','Freedom — state the broader consequence.')],
 [(2,'presenter','Direct and warm; no product prop in her hands.','Hold the distinction between weight loss and feeling like a person.','Meaning — explain why she is sharing.'),
  (3,'presenter','Keep sustained eye contact through nobody told me either.','No insert over the final empathetic lines.','Identification — close the opening promise.')],
 [(1,'presenter','Same presenter, optional exact product cutout below/right.','Link below is conversational, no forced downward gesture.','CTA — a simple next step.'),
  (1,'cta','Clean static offer card: 90-day money-back guarantee and Link below, alongside unchanged product cutout.','Show on ninety days; keep as separate overlay, not a new avatar scene.','Reassurance — visualize only the supplied guarantee.'),
  (1,'presenter','Same presenter with product and CTA overlays retained.','Hold final composition 3s after the last word.','Close — leave time to act.')]
]

beats=[]; cursor=0
for pi, entries in enumerate(rows):
 sentences=re.split(r'(?<=[.!?])\s+',paras[pi]); offset=0
 for n,key,visual,cue,purpose in entries:
  script=' '.join(sentences[offset:offset+n]);offset+=n
  assert script
  duration=len(script.split())/205*60+0.20
  b={'id':f'B{len(beats)+1:02d}','paragraph':pi,'script':script,'asset':key,'frame':assets[key],
    'start':round(cursor,2),'end':round(cursor+duration,2),'duration':round(duration,2),
    'visual':visual,'cue':cue,'emotion':purpose,'type':'presenter' if key=='presenter' else ('overlay' if key in ['group-post','celery','chlorophyllin','fiber','ingredients','product','cta','gas-diagram'] else 'broll')}
  beats.append(b);cursor+=duration
 assert offset==len(sentences),(pi,offset,len(sentences),sentences)
assert ' '.join(b['script'] for b in beats)==' '.join(paras)
def tc(t):return f'{int(t)//60:02d}:{t%60:04.1f}'
words=len(' '.join(paras).split())
summary=f'Updated supplied script, verbatim: {words} words across {len(beats)} editorial beats. Estimated {tc(cursor+3)} at 205 wpm including pauses and a 3-second end hold; timing is provisional until final narration. One consistent car presenter, separate static overlays and unique candid B-roll. The product appears visually at “So I found the same one”; no extra narration is added.'
plan=f'''# MOT-UGC-YAPPER-01 — editing plan v5 · updated supplied script

Date: 2026-09-09. Supersedes v4 narration and all prior hook alternatives. Earlier plan, board, selected assets and exact prior script are preserved in version history.

## Brief and inputs

{summary}

Source copy: `../script/user-updated-v5.txt`, copied unchanged from the latest attachment. Audience: women with the GLP-1 discomfort experience described in the script. Objective: build recognition, explain the story's slowdown idea, introduce the blend, show an ordinary routine and close with the supplied guarantee. This phase delivers the Cut Room storyboard and selected first image set. 9:16 composition, eventual 1080×1920. Existing P01 presenter, olive shirt, ivory tee, mature face and parked car remain the identity reference. Exact Motilli product PNG and two dark-green heart gummies remain the product references.

## Reference evidence and revision scope

Recovered Alicia Darling source analysis remains applicable to editing grammar only. See `reference-analysis/reference-breakdown.md` and `verified-shot-map.json`: 30fps source, 71 retained shots/pickups, mostly straight cuts, captions in black on compact white boxes, noun/action-linked inserts, repeated returns to presenter. This revision re-inspected all three overview sheets and adjacent-frame boundary evidence; the prior detailed audit is retained, not represented as a new exhaustive watch. Source narration alignment is approximate. Music and SFX matching were not established by critical listening. Competitor media stays in a separate reference lane and supplies no Motilli proof.

## Editing strategy

Open directly on the fixed car presenter. Make the expanded frustration sequence concrete with a barely eaten meal, loose jeans, waiting at the counter, stirring fiber, dawn discomfort and the pharmacy aisle. Each is one unique setting/action. The vulnerable lines remain on the face. Research gets an overhead desk view. The mechanism changes visual language from one stomach cutaway to the river metaphor to a simple gut-lumen/gas diagram, then returns to her realization. The support-group material is one clearly labeled static illustrative card. Neutral ingredient images anchor the three names; do not turn unverified ingredient claims into simulated clinical results. Product cutout appears over the existing presenter when she says she found the same blend. Routine, relaxed dinner, mirror, leaving home and clearing the table are separate scenes. Close with face, exact product and the supplied guarantee.

All insert durations below are windows within their thought beat. V1 presenter remains continuous underneath; V2 inserts and overlays cover the specified phrase, then reveal V1. Each scene appears once, except intentional same-presenter coverage and product identification at close. No crops/mirrors masquerading as unique scenes. No automatic cut on every sentence. No dissolves, swooshes or blanket zooms. Straight cuts in/out; static overlays appear/disappear on named cues. Later video motion should be a small real action within the first-frame composition. Do not animate flat screenshots as phone scenes.

## Voice, captions and sound

Conversational first-person delivery, candid and quick but intelligible; one continuous performance. Prior saved direction used one HeyGen avatar; this still-only revision preserves that visual setup and does not invoke any voice/video provider. Current workspace provider rule governs any later generation: Google Omni; editing in DaVinci Resolve. 205 wpm is inherited planning pace, not approved recorded audio or a request to accelerate speech. Preserve every word, contractions and sequence. Pause lightly at Weeks, Just fine and That was new. Pronunciations need checking against the selected final read. No new VO produced here.

Captions: exact spoken copy in short 2–6 word chunks, black Inter-like semibold text on snug white rectangles, 1–2 lines. At 1080×1920 keep within x=100–900 and y=1050–1470; verify against final face and platform UI. Overlay cards live below the mouth and above captions, with readable recreation labels. Keep captions separate from the raw images. No new unsupported benefit badges. Clean continuous narration/room tone; music optional and 20–24dB below voice if later selected, no emotional stingers. Proposed final loudness around -14 LUFS, ceiling -1dBTP; verify actual export. Fresh final word alignment controls all cuts/captions, never provisional beat times.

## Visual schedule — provisional

| Beat | Exact narration | Time / duration | Visual / visible action | Source / gap | Cut in / out | Movement / captions / sound | Purpose |
|---|---|---|---|---|---|---|---|
'''
for b in beats:
 source=('Selected existing GPT Image 2 asset' if Path(b['frame']).exists() else 'Generate GPT Image 2 first frame') if b['asset']!='product' else 'Exact approved transparent product PNG'
 plan+='| '+' | '.join([b['id'],b['script'],f"{tc(b['start'])}–{tc(b['end'])} / {b['duration']}s",b['visual'],source+' · '+b['asset'],b['cue'], 'Continuous voice; exact captions. Static overlay.' if b['type']=='overlay' else 'Continuous voice; exact captions. Natural small action; no automatic zoom.',b['emotion']])+' |\n'
plan+='''
## Production, delivery and QA

Plan saved before generating v5 images. Generate missing first frames with GPT Image 2 using P01 for the woman’s identity and the approved product references where applicable. Inspect each selected image for candid gaze, anatomy/hands, readable typography, composition variety and fidelity. Reuse existing selected images only where the new words still fit. Remove the old eight-month member reply, doctor-comment group image, old narration, spare-jar/scarcity scene and previous hook alternatives from the current storyboard. Archive unchanged original evidence separately.

Build using `cutroom/board_builder.py` in the existing Motilli project, same stable board URL; no additional approval gate. Every planned insert gets its actual selected first frame. Presenter-only cards show P01; overlay assets and product remain separate. Verify full source-to-board narration equality, all image URLs, board project, cloud sync and visual variety. Store manifests and QA in this concept. Proposed future edit: isolated Resolve project/timeline; verify current connection before claiming any editor operation. Final delivery would require actual narration alignment, generated motion inspection, accurate subtitles, full playback, sound/caption checks and export QA. No Resolve operation, motion generation or export is part of this storyboard phase.

Copy dependencies remain separate: do not present generated group UI as captured testimony or fabricate medical citations/charts. Preserve the supplied narration; publication substantiation, actual narrator representation, directions and guarantee terms remain production checks. The board does not certify these claims. No added dose, ratio, result percentage, weight-loss amount or availability assertion.
'''
(ROOT/'edit/editing-plan.md').write_text(plan)
(ROOT/'storyboard/beat-cards-v5.json').write_text(json.dumps(beats,indent=2))
(ROOT/'storyboard/assets-v5.json').write_text(json.dumps(assets,indent=2))
print(json.dumps({'words':words,'beats':len(beats),'estimated_runtime':tc(cursor+3),'missing':[k for k,v in assets.items() if not Path(v).exists()]},indent=2))

if '--board' in __import__('sys').argv:
 missing=[v for v in assets.values() if not Path(v).exists()]
 assert not missing,missing
 timelines=[]
 for start in range(0,len(beats),8):
  group=beats[start:start+8]
  timelines.append({'label':f'UPDATED SCRIPT · {group[0]["id"]}–{group[-1]["id"]}','source':'Exact latest supplied narration · all timing provisional','beats':[
   {'t':f'{b["id"]} · {tc(b["start"])}–{tc(b["end"])}','script':b['script'],'frame':b['frame'],'visual':b['visual'],'emotion':b['emotion'],
    'note':b['cue']+' Straight cuts in/out. Continuous presenter/voice underneath. Final word alignment determines position.'} for b in group]})
 timelines.append({'label':'PRESENTER & PRODUCT · PRODUCTION SOURCES','beats':[
  {'t':'ONE BASE PRESENTER','frame':P,'visual':'Same face, olive shirt, ivory tee and car throughout.','note':'Use one continuous performance. No product holding or separate CTA avatar.'},
  {'t':'EXACT PRODUCT OVERLAY','frame':assets['product'],'visual':'Approved source cutout; independent overlay.','note':'Reveal at So I found the same one; return at CTA.'},
  {'t':'FINAL HOLD · 3s','frame':assets['cta'],'visual':'Offer overlay over the same presenter with separate product.','note':'Retain last composition for 3 seconds after narration.'}]})
 timelines.extend(t for t in OLD['timelines'] if t['label'].startswith('REFERENCE CREATIVE'))
 spec={'title':'MOT-UGC-YAPPER-01 — Updated script v5','project':'motilli','summary':summary,'timelines':timelines,'notes':[
  {'title':'READING ORDER','text':'Read each UPDATED SCRIPT row left to right, then move down. All supplied narration is included exactly once in these rows. Reference frames are in their own lane.'},
  {'title':'CURRENT SCRIPT','text':f'{words} words; {len(beats)} thought beats, not {len(beats)} video clips. One supplied opening; old hook alternatives removed. All timing provisional.'},
  {'title':'CAPTIONS & SOUND','text':'Black text on snug white boxes; 1–2 short lines. Continuous conversational voice across inserts. Keep face and captions clear. No music or SFX match is claimed.'},
  {'title':'PRODUCT ENTRY','text':'The new script never says Motilli aloud. Show the exact Motilli product on So I found the same one. Preserve the script; add no spoken brand sentence.'},
  {'title':'VISUAL VARIETY','text':'Every covering scene uses a distinct source and action. Dinner problem, dinner payoff and clearing plate are different compositions. Stomach, river and lumen diagram are distinct mechanism views.'},
  {'title':'FIRST ASSET SET','text':'Selected GPT Image 2 presenter, candid inserts and overlays attached. Prior compatible images retained; expanded scenes generated for this revision. These are storyboard stills, not finished video.'},
  {'title':'REFERENCE SCOPE','text':'Recovered Alicia Darling source and frame-level cut map retained. Transfer straight cuts, conversational presenter returns and caption style only. Reference frames are not Motilli assets or evidence.'},
  {'title':'COPY & REPRESENTATION','text':'Group UI is visibly labeled illustrative recreation. No invented clinician quote, proof chart, body before/after or treatment animation. Supplied narration preserved; existing substantiation and representation dependencies remain.'},
  {'title':'EDITOR HANDOFF','text':'Editing plan v5 is saved with the concept. Align cuts/captions to final voice; preserve performance speed. Future motion uses Google Omni and production editing uses DaVinci Resolve. No timeline or export created in this phase.'}
 ]}
 (ROOT/'storyboard/cutroom-spec.json').write_text(json.dumps(spec,indent=2))
 (ROOT/'storyboard/beat-cards.json').write_text(json.dumps(beats,indent=2))
 coverage=[{'beat':b['id'],'asset':b['asset'],'path':b['frame'],'type':b['type'],'sha256':hashlib.sha256(Path(b['frame']).read_bytes()).hexdigest()} for b in beats]
 (ROOT/'storyboard/asset-coverage.json').write_text(json.dumps(coverage,indent=2))
