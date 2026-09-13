import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
beats = json.loads((ROOT / 'script-beats.json').read_text())
shots = [
 (0,'Kitchen presenter; large SOS bottle foreground','Hook: medication conflict; product visible immediately','Static wide'),
 (60,'Same presenter in close-up','Continue hook','Hard cut closer'),
 (128,'Wide kitchen and bottle','Promise explanation','Hard cut wider'),
 (158,'Presenter leans toward foreground bottle','Explanation setup','Hard cut closer'),
 (193,'Bottle and capsules beauty shot','GLP-1 explanation begins; visual product reminder','Horizontal blur transition'),
 (230,'Male torso with glowing digestive anatomy','Slower digestive-system claim','Hard cut; camera pushes inward'),
 (292,'Woman demonstrates loose jeans','Weight-loss benefit','Hard cut; hands pull waistband'),
 (327,'Transparent torso and food particle','Slower food movement','Hard cut; internal particle movement'),
 (356,'Woman declines food at restaurant','Fullness','Hard cut; hand gesture'),
 (390,'Woman on couch, hand on abdomen','Agitate heaviness','Hard cut; restrained body movement'),
 (451,'Transparent torso with active stomach','Stomach emptying claim','Hard cut; internal glow'),
 (493,'Close bowel anatomy','Intestinal-movement claim','Hard cut; camera tracks bowel'),
 (534,'Colon section with food-like material','Fermentation claim','Hard cut; material moves'),
 (576,'Man reacts with hand to mouth','Sulfur-burp symptom','Hard cut; reaction action'),
 (619,'Colon with backed-up material','Waste-backup claim','Warm light-leak / white-flash transition; outgoing light begins earlier'),
 (686,'Presenter pushes laxative boxes away','Failed solutions','Hard cut; emphatic hand movement'),
 (740,'Bowel muscle with fiery contraction','Stimulant-laxative explanation','Hard cut; moving anatomical camera'),
 (805,'Woman holds injection pen at abdomen','Medication counterforce claim','Hard cut; injection-related action'),
 (891,'Woman in red glasses drinks water','Continue conflict; introduce fiber','Hard cut; glass movement'),
 (947,'Large fiber-like mass in digestive cross-section','Bulk claim','Hard cut; internal camera movement'),
 (979,'Bowel lumen with mass and MOVEMENT title','Bulk-needs-movement claim','Hard cut to internal viewpoint'),
 (1028,'Silver-haired woman addresses camera','Claim viewer lacks movement','Hard cut; emphatic gesture'),
 (1060,'OTC containers; red X appears','Wrong-mechanism conclusion','Hard cut; graphic X animates'),
 (1106,'Red-glasses woman standing','Absolution: failed attempts make sense','Hard cut; presenter gesture'),
 (1142,'Dark-haired woman in coral top','Solution requirement','Hard cut; raised finger'),
 (1231,'Red-haired woman crosses arms','Contrast against medication','Hard cut; X gesture'),
 (1252,'Kitchen presenter picks up SOS bottle','Spoken branded ingredient introduction','Hard cut; bottle pickup'),
 (1329,'Blue water particles enter bowel illustration','Magnesium / water explanation','Horizontal blur transition'),
 (1397,'Red-glasses woman with palms out','No-contractions reassurance','Hard cut; calming gesture'),
 (1425,'Same woman, hand on abdomen','Comfort promise','Hard cut; relaxed expression'),
 (1475,'Hand holds ginger root','Second ingredient','Hard cut; rotating object close-up'),
 (1500,'Stomach with orange particles / lower bowel','Ginger study and emptying claim','Hard cut; camera travels along anatomy'),
 (1580,'Bottle and clear capsules close-up','Connect ingredient explanation to product','Hard cut; beauty-shot camera movement'),
 (1649,'Kitchen woman in pink blouse','Sulfur-burp outcome claim','Hard cut; open-hand gesture'),
 (1691,'Inside bowel with food particles','Food empties before fermentation claim','Hard cut; forward camera movement'),
 (1749,'Warm morning coffee portrait','Three-day testimonial result','Hard cut; cup held'),
 (1807,'Blue simplified pelvis','No-cramping reassurance','Hard cut; anatomy insert'),
 (1827,'Hand at exposed abdomen','No-urgency reassurance','Hard cut; live-body-style detail'),
 (1854,'Woman gets out of bed','No-emergency reassurance','Hard cut; full-body movement'),
 (1888,'Hand circles calendar date','Day-two marker','Hard cut; pen action'),
 (1905,'Woman eating restaurant salad','Burps stopped / energy return','Hard cut; eating action'),
 (1971,'Woman stretches in bed','Morning routine restored','Hard cut; stretching action'),
 (2018,'Kitchen coffee sip','Coffee and regularity testimonial','Hard cut; cup action'),
 (2051,'Woman exits home','Predictability / freedom','Hard cut; walking action'),
 (2083,'Brunch group selfie','Social-life restoration','Hard cut; shared laughter'),
 (2133,'Two capsules picked up beside dinner','Easy routine','Hard cut; hand close-up'),
 (2168,'Bottle with 60-day guarantee seal','Risk reversal','Warm flash; white frame at 2167, incoming bottle at 2168'),
 (2218,'Kitchen presenter, open palms','Nothing-to-lose reassurance','Hard cut; gesture'),
 (2257,'Woman holds capsule to sunlight','Transparency proof','Hard cut; capsule inspection'),
 (2311,'Floating capsule reveals oversized herbs','Ingredient-visibility demonstration','Hard cut; capsule changes appearance within same shot'),
 (2398,'Presenter holds bottle','Closing slogan callback','Hard cut; bottle presentation'),
 (2434,'Product end card with stars, 55,000+ users, URL','Visual social proof and CTA; speech ends before card','Horizontal blur transition; card held to end'),
]
audit = ROOT / 'edit' / 'reference-analysis'
with (audit / 'verified-shot-map.csv').open('w', newline='') as f:
    w=csv.writer(f);w.writerow(['shot','start_frame_25fps','start_sec','end_sec','duration_sec','visual','narration_function','transition_camera_action'])
    for i,(frame,visual,narration,movement) in enumerate(shots):
        end=shots[i+1][0]/25 if i+1<len(shots) else 103.92
        w.writerow([i+1,frame,f'{frame/25:.2f}',f'{end:.2f}',f'{end-frame/25:.2f}',visual,narration,movement])

plan='''# Motilli — GLP-1 late product reveal: editing plan

Status: writing and planning complete; no media generation, voiceover, timeline assembly or export performed. Original Motilli direction derived from an inspected reference. Timings are provisional until final voice alignment.

## Editorial intent

One consistent female AI presenter leads a roughly two-minute VSL. The sequence is recognition → explanation → failed-attempt reframe → purchase criteria → ingredient category → Motilli → simple routine → guarantee → explicit CTA. The reference's personal-results testimony becomes factual product demonstration because no documented Motilli outcome proof was supplied or found. This changes the strength of the proof section; it is not equivalent to clinical validation.

**Reveal lock:** no Motilli logo, bottle, packaging, gummy, product page or branded caption before the spoken word “Motilli” in beat 7. At the current 150-wpm planning rate, beat 7 starts at 78 seconds; the brand follows its short introductory phrase at roughly 80 seconds. First visibility must align to that word after voice alignment. No capsule prop or silhouette teaser beforehand. Unbranded ingredient-category education is allowed.

**Format:** 9:16, proposed 1080×1920, approximately 116 seconds speech plus four-second end hold. 289 words; 145–155 wpm gives about 112–120 seconds speech. Do not speed up the narration to match the reference's approximately 177-wpm spoken delivery.

## Observed reference and limits

Source: supplied 104.04-second SOS MP4, video track 103.92 seconds, 25 fps. See [reference analysis](../reference-breakdown.md), [shot map](reference-analysis/verified-shot-map.csv), five boundary sheets and five half-second overview sheets. Fifty-two editorial shot units were mapped. All candidate boundaries were inspected as consecutive source-frame pairs; duplicate scene detections were removed. The missed guarantee transition was checked across consecutive frames 2150–2175: outgoing scene flashes white at 86.68 seconds and incoming bottle appears at 86.72. Blurred/flash transitions are intervals, not clean single-frame cuts. Full-video every-frame inspection was not performed; this is a cut-boundary audit with half-second coverage between boundaries.

The source alternates short presenter shots, anatomical explanations, symptom illustrations and lifestyle relief scenes, generally around two seconds each; its final product card holds about 6.5 seconds. Main caption style is bold black text in compact white rectangles. The first several seconds add a large red/black headline. Major blur transitions occur around 7.72, 53.16 and 97.36 seconds; warm flashes around 24.7 and 86.7 seconds. Narration sometimes anticipates or trails the visible cut, so transcript phrase starts and shot starts must not be conflated.

Audio was separately assessed by a video-capable model: consistent mature female narration, light continuous instrumental bed, possible transition and action effects. Exact SFX and music timing remain unverified. Its generated end-of-speech estimate conflicts with the timed transcript; use the transcript's approximately 99.76-second speech endpoint, not that model estimate. Proposed audio below is original direction, not a certified recreation of the source mix.

## Voice, captions and mix

Warm, matter-of-fact female voice; inquisitive opening; empathetic agitation; clear explanation; practical close. She is an AI brand presenter, with a discreet readable disclosure, not a doctor or claimed customer. No invented clinical practice, personal weight loss, treatment result or patient anecdote. Keep contractions and connected phrases; allow a pause after the hook and before the brand.

Captions: two lines maximum, semantic phrases, large readable type, avoid covering face/product and platform UI. Emphasize the question, the three criteria, product name, serving directions and guarantee. Word timing follows final voice; no improvised stronger claims in captions. Body mechanisms carry “Illustration”. Avoid fake study screenshots, user comments, review cards, certificates or before/after footage.

Mix: voice is dominant; one restrained instrumental bed, ducked below narration. Proposed output approximately −14 LUFS integrated with true peak at or below −1 dBTP, then listen on phone speakers. Gentle transitions only at the explanation and reveal. No bodily comedy effects or claim-emphasizing medical alarms. Fade music during the end hold.

## Beat-to-edit map

All assets below are gaps. P01/P02 are consistent presenter coverage; each B-roll ID is a new composition and action. Use Google Omni for generated video and GPT Image 2 for any image assets. Use the current documented internal editor only if production is later requested; resolve its entry point then. No HyperFrames or Remotion.

| Beat / provisional time | Spoken copy | Specific visual / asset gap | Cut cue and purpose | Incoming → outgoing transition | Proof |
|---|---|---|---|---|---|
'''
for b in beats:
    plan+=f"| {b['beat']} / {b['start']:.1f}–{b['end']:.1f}s | {b['copy']} | {b['visual']} | {b['cut']} Purpose: {b['purpose']} | Hard cut in → hard cut out; spoken phrases guide inserts. Final CTA holds 4s after voice. | {b['proof']} |\n"
plan+='''
## Variety, product fidelity and delivery QA

Before generation, compare proposed B01–B10: calendar; dining action; side-section stomach; overhead meal; tabletop categories; microscopic microbes; bottle/ingredient composition; palm with gummies; bedside routine; label macro. These are distinct views and actions. Presenter returns are intentional continuity, not recycled B-roll. Do not use multiple translucent torsos. No ingredient-to-bowel “repair” or before/after motion implies an unproved product mechanism.

Before any product generation, locate approved current bottle and heart-shaped gummy references, confirm current label with the supplier/brand, and compare against the live SKU. No invented dosages or changes to packaging. Ingredient amounts in older workspace files are not reliable. Generated label text must be checked against actual references; use accurate typesetting where necessary.

Before export: update this plan to final voice alignment; check every line, caption and source; verify reveal frame against the first spoken brand word; audit the entire timeline for exact source reuse and visually similar B-roll; inspect faces, hands and product identity; check explicit illustrative/AI labeling; verify the live guarantee and CTA destination; review audio on phone speakers; ensure full end hold and no cutoff words. A real outcome testimonial or product trial, if later supplied, requires revising the script and this plan before production. No output video has been created in this task.
'''
(ROOT/'edit'/'editing-plan.md').write_text(plan)

outline='# Motilli VSL outline\n\nOriginal adaptation on the inspected reference skeleton. 289 words; approximately 120 seconds including end hold at the planning pace. Product reveal around 80 seconds, about two-thirds through. All timings provisional.\n\n| Beat | Target duration | What to say / purpose | Proof element | Draft copy |\n|---|---:|---|---|---|\n'
for b in beats:
    outline+=f"| {b['beat']} | {b['duration']:.1f}s | {b['purpose']} | {b['proof']} | {b['copy']} |\n"
outline+='\nEnd hold: four additional seconds. The product demonstration is deliberately factual; it does not stand in for an unavailable finished-product study or customer result.\n'
(ROOT/'outline.md').write_text(outline)
print('Wrote editing plan, outline and 52-shot reference map.')
