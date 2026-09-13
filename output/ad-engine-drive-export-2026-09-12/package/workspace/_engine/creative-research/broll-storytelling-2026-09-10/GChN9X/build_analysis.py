from pathlib import Path
import json,csv,statistics
p=Path(__file__).parent
# Semantic image events personally reviewed. Same-setup presenter pickups stay in their containing beat.
data='''0|human|Woman on toilet folds arms over abdomen, leans forward and winces; elevated doorway view|recognition hook|Make discomfort legible before any explanation
56|human|Close couch selfie with palm against forehead|agitation|Add another recognizable lived symptom
100|presenter|Seated blonde presenter in gray top by window|warning bridge|Give the warning a human speaker
136|mechanism|Pink intestinal tunnel with white worm-like forms and glowing deposits|invisible-threat teaser|Introduce the proposed hidden cause before naming it
238|human|Dim bedroom wide; woman throws covers aside and gets out of bed|symptom|Show interrupted sleep as an action
296|presenter|Seated presenter gestures|common explanation|Voice the viewer's existing interpretation
343|human|Woman rubs shoulder and grimaces in black top|symptom|Locate the specific discomfort
398|human|Woman lying sideways in same dim bedroom setup|common explanation|Illustrate sleeping posture rather than repeat shoulder rubbing
439|human|Woman parts hair at scalp close to camera|symptom|Make hair concern physically inspectable
480|presenter|Seated presenter|common explanation|Attribute symptom to an assumed cause
506|human|Woman closes eyes and presses both temples|symptom|Visual shorthand for difficulty concentrating
595|human|Side angle of gray-shirt woman seated and smiling then looking down|self-dismissal|Embody joking or embarrassment
634|human|Waist and torso side view in close-fitting tan dress; hand at hip|symptom|Show clothing/body concern concretely
720|presenter|Seated presenter|reframe setup|Connect the symptoms and challenge normalization
799|human|Fast recap of bedroom getting-up shot with blur/bright entry|recap|Recall the first symptom
809|human|Fast shoulder-pain recap with bright entry|recap|Gather apparently separate issues
819|human|Fast hair-parting recap with bright entry|recap|Continue visual enumeration
829|human|Fast temple-pressure recap with bright entry|recap|Continue visual enumeration
839|human|Fast tan-dress abdomen recap|recap|Complete the symptom set
855|presenter|Blurred lateral return to seated presenter, settling by frame858|cause bridge|Presenter delivers the unifying interpretation
961|mechanism|Circular endoscopic-looking intestinal image on black|cause naming|Give the named cause an immediate image
994|presenter|Seated presenter|authority setup|Introduce numeric research claim
1016|document-inset|Highlighted article-like screenshot over presenter's chest; red caption box|claimed proof|Borrow document authority while retaining speaker; source authenticity unverified
1165|presenter|Screenshot disappears; presenter fills frame|exposure bridge|Introduce everyday exposure examples
1207|object|Hand presses raw meat on yellow plate with white string-like material|exposure example|Literal food-related referent
1236|object|Bathroom faucet runs brown liquid into sink, bright/blur entry|exposure example|Literal water-related referent
1266|object|First-person hand turns silver doorknob, bright/blur entry|exposure example|Show the contact action
1297|human|Woman seated in armchair cuddles small black-and-white pet|exposure example|Connect proposed exposure to normal affection
1323|mechanism|Cool-blue microscopic organism/appendage animation|scale change|Travel conceptually from everyday world to inside body
1369|presenter|Seated presenter|explanatory emphasis|State the next process
1391|mechanism|Endoscopic-style worm within pink intestinal tunnel|process|Show an internal resident at the process cue
1447|presenter|Seated presenter|definition bridge|Introduce plain-language explanation
1464|mechanism-inset|Simple labeled blue-red biofilm illustration on white over chest|definition|Let a small schematic annotate an unfamiliar term
1562|mechanism|Spherical sacs filled with worm-like forms in brown tissue; moving close view|process escalation|Visualize protected multiplication
1658|mechanism|Purple particles around branching fibrous structures|process escalation|Vary microscopic scale for spreading language
1715|presenter|Seated presenter|objection bridge|Connect mechanism story to a frustrating clinical experience
1746|human|Woman in white coat and stethoscope holds clipboard, adjusts glasses|authority reenactment|Represent the claimed doctor interaction, not verified medical authority
1781|document|Full-frame printed lab-style report; camera moves down paper|claimed proof|Make the test-result topic tangible
1820|document|Same report darkened with oval highlight; red arrow subsequently appears|claimed proof emphasis|Direct attention to a specific result area; authenticity unverified
1878|presenter|Seated presenter|consequence setup|Move from proposed invisibility to daily effects
1971|mechanism|Worm-like forms reach food material inside intestinal tunnel|cause|Illustrate proposed nutrient interception
2058|human|Woman at laptop slumps and rubs head beside window blinds|consequence|Translate invisible nutrient story into observable fatigue
2133|presenter|Seated presenter|interpretation|Land the energy consequence verbally
2167|mechanism|Red blood cells travel through vessel as green cloud spreads|cause|Illustrate proposed bloodstream transport
2227|mechanism|Brain image dissolves over vessel, isolated by frame2236|cause destination|Visually connect transport to destination rather than reset with unrelated image
2271|presenter|Seated presenter|interpretation|Connect brain image back to experience
2300|human|Side-view gray-shirt woman pauses, closes eyes and looks down|consequence|Represent trouble recalling words
2336|mechanism|Worm-like forms among white sugar-like material in gut|cause|Show proposed feeding process
2393|object|Open box of doughnuts in ordinary room|consequence|Move to recognizable food craving cue
2440|presenter|Seated presenter|reassurance/reframe|Deliver interpretation about failed willpower
2541|mechanism|Red irritated spots on inner gut wall|specific system|Locate the named gut process
2561|mechanism|Blue human upper-body diagram with highlighted red joints|specific system|Change the scientific view for joint language
2588|presenter|Seated presenter, direct eye contact|emotional accumulation|Hold face for blame, aging and lost-time argument
2797|human|Woman plays blocks beside child in living room|stakes|Show a valuable activity at risk
2838|human-effect|Same setting but woman slumps, grayscale and large red STOLEN|loss contrast|Turn desired activity into denied activity at consequence cue
2863|human|Woman smiles and gestures in car selfie|stakes|Show easy conversation as another valued ability
2894|human-effect|Car image becomes grayscale; red STOLEN appears while the expression subsequently changes|loss contrast|Turn social ease into denied ability
2930|human|Close waist in white top and pale trousers, hand moves near side|stakes|Represent familiar body/clothing relationship
2980|human-effect|Different tighter abdomen view in dark top, grayscale and red STOLEN|loss contrast|Create body-recognition loss contrast; not calibrated before/after evidence
3007|presenter|Seated presenter|hope bridge|Move from loss toward agency before naming ingredient
3170|ingredient|Hand holds wooden plate of green oregano and clear oil jar outdoors|solution ingredient|Show recognizable raw material before claimed function
3263|mechanism|Microscope-looking threadlike forms with oil-droplet arrows; radial zoom entry|solution action|Connect ingredient to process; lab authenticity and efficacy not verified
3381|mechanism|Golden liquid pours across worm-filled sacs and bubbles in tissue|solution action|Animate the script's barrier-break action in the previously established environment
3513|mechanism|Microscope-looking organism changes shape/loses structure|solution action|Use close action to depict loss of attachment
3586|mechanism|Different microscope-looking segmented organism disintegrates|solution action|Switch visible subject for multiplication language
3656|ingredient|Lateral blur into hand-held plate of black seeds and dark oil outdoors|second ingredient|Introduce distinct raw material using matching ingredient setup
3723|presenter|Seated presenter|role explanation|Explain second ingredient's job
3797|mechanism|Dark stream moves through intestinal tunnel amid small white forms|solution action|Depict flushing/movement
3904|mechanism|Clean stylized orange intestinal tunnel with particles|solution action|Change to calmer gut illustration
3948|mechanism-metaphor|Tiny worker figures spray/support joint tissue|solution action metaphor|Use a different anatomical site and repair metaphor for joints
3976|mechanism|Glowing green outline of whole body|system summary|Zoom conceptually out to whole-system language
4009|mechanism|Worm-filled translucent sac deflates in gut tunnel|role recap|Recall first ingredient's proposed job
4069|mechanism-metaphor|Tiny workers spray blue streams over glowing damaged tissue|role recap|Different action for the second ingredient's cooling metaphor
4138|ingredient|Both seed/herb piles and two oil jars share wooden board outdoors|combination|Put both ingredients in one frame when discussing their combination
4214|mechanism|Microscope-style organism inside cracking shell-like membrane|role recap|Literalize barrier metaphor; avoid treating animation as proof
4248|mechanism|Fade through black into luminous green digestive torso|role recap|Shift from breaking to calming action
4293|ingredient|Warm flare reveals two amber oil bottles in golden light|combination|Reunite ingredient pair with a hopeful visual tone
4335|presenter|Seated presenter|benefit bridge|Presenter interprets and hands off to life outcomes
4378|human|Warm flash into woman working at laptop in pink shirt|benefit|Restore competence at a concrete everyday task
4441|human|Woman at table in blue sweatshirt, relaxed expression and hand at cheek|benefit|Show more comfortable mental engagement
4494|human|Older woman speaks outside in selfie composition|benefit|Make remembering/conversation visible
4544|human|Woman smiles and turns in fitted black dress in hallway|benefit|Return to clothing comfort using new footage
4604|presenter|Seated presenter|benefit interpretation|Carry the temporal qualification on face
4642|human|Woman wakes in daylight bed, sits up and stretches both arms|benefit callback|Answer earlier night waking with a distinct positive scene
4715|human|Woman in blue top dances/raises arms in kitchen|benefit|Make energy a visible action
4747|presenter|Seated presenter|qualification|Keep verbal distinction on speaker
4803|human|Grandparent and family watch small child play indoors|emotional payoff|Return to family participation
4842|human|Older woman sits by/in river in swimwear|emotional payoff|Give retirement an active, specific scene
4869|human|Older couple walk side by side outside building|emotional payoff|Show shared daily life beyond symptom removal
4897|presenter|Seated presenter|selection objection|Reset attention to choosing among options
4925|object|Crowded shelf of oil/supplement bottles in cupboard|alternatives|Show category clutter
4975|presenter|Seated presenter|selection criterion|Explain the claimed distinction
5008|object|Hand holds competing oregano bottle in shop aisle|comparison|Make comparison object legible
5017|object-effect|Competing bottle turns grayscale with large red X|comparison emphasis|Encode rejection visually; comparative claim unverified
5055|mechanism|Microscope view with intact organism, briefly red X|failure explanation|Recall the mechanism criterion before product recommendation
5111|presenter|Seated presenter|selection bridge|State criterion and recommended brand
5231|product|Hand holds white Resilia oil-of-oregano pouch outdoors|brand reveal|First clear branded product after lengthy mechanism and benefit sequence
5257|document|Pouch behind printed branded stability-report page|claimed proof|Attach claimed concentration to document
5286|document|Closer graph crop on printed report|claimed proof emphasis|Focus attention on one claimed numeric criterion
5315|origin|Workers in branded shirts harvest herbs on mountain slope|origin story|Make stated sourcing location and harvesting action visible; provenance unverified
5362|origin|Branded-shirt workers operate metal equipment indoors|manufacturing story|Depict stated production process; provenance unverified
5440|offer|Finger points at guarantee area on laptop product page|risk reversal|Show where the stated policy can be found
5523|presenter|Seated presenter|reassurance|Let speaker deliver refund reassurance personally
5629|presenter-cta|Seated presenter plus downward red arrow|action cue|Indicate the action location
5693|product-cta|Hand holds Resilia pouch by window; arrow persists|action cue|Connect click request with recognizable purchase object
5739|product-cta|Pouch tips golden softgels into palm|format/use|Make physical product form tangible during closing line
5791|product-cta|Palm of golden softgels in window light|format/use|Hold material detail and keep arrow readable
5841|presenter-cta|Return to presenter with downward arrow through final frame|closing appeal|End on human invitation and action direction'''
entries=[]
for line in data.splitlines():
 f,kind,visual,role,purpose=line.split('|');entries.append(dict(start_frame=int(f),visual_class=kind,visual=visual,story_role=role,purpose_inferred=purpose))
t=json.loads((p/'transcript.json').read_text());words=[w for s in t['segments'] for w in s.get('words',[])]
rows=[]
for j,e in enumerate(entries):
 end=entries[j+1]['start_frame'] if j+1<len(entries) else 5900
 st=e['start_frame']/25;et=end/25
 transition='Direct cut / appearance' if j else 'Cold open'
 if e['start_frame'] in [799,809,819,829,839,1236,1266,1297]:transition='Cut with brief bright/blurred incoming treatment'
 if e['start_frame'] in [855,3656]:transition='Brief lateral blur handoff'
 if e['start_frame']==3263:transition='Radial zoom-blur handoff'
 if e['start_frame']==2227:transition='Cross-dissolve begins f2227; isolated brain by f2236'
 if e['start_frame']==4248:transition='Fade through black f4247 into torso from f4248'
 if e['start_frame'] in [4293,4378]:transition='Warm flare / white flash handoff; incoming image visible at this frame'
 if e['visual_class'].endswith('effect'):transition='Within-beat edit/effect event; not necessarily a new source clip'
 row=dict(event=f'E{j+1:03}',**e,end_frame_exclusive=end,start_seconds=st,end_seconds=et,duration_seconds=round(et-st,3),narration_asr_approx=' '.join(w['word'].strip() for w in words if w['start']<et and w['end']>st),incoming=transition,outgoing='End of source' if j+1==len(entries) else 'To '+entries[j+1]['visual'],evidence=f'frames/{e["start_frame"]:05}.jpg',timing_basis='Image event manually checked; speech uses approximate MLX Whisper timestamps')
 rows.append(row)
(p/'shot-map.json').write_text(json.dumps(rows,indent=2))
with (p/'shot-map.csv').open('w') as h:
 writer=csv.DictWriter(h,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
md='''# GChN9X: symptom recognition → hidden cause → regained retirement

Source: https://app.trendtrack.io/share/ads/resilia-GChN9X. Original retained as source.mp4. 720×1280, 25 fps, 5,900 image frames / 236.000 seconds; container/audio tail 236.116 seconds. User identifies the reference as high-converting; conversion metrics were not supplied.

## Actual review coverage

All 5,900 frames decoded and differenced. Personally inspected 472 chronological frames at alternating 0.48/0.52-second spacing, all 202 candidate consecutive-frame pairs in 11 boundary sheets, and 213 additional consecutive frames across selected transition spans in six transition sheets, plus ten frames checking loss-label onset (sheets/loss-label-check.jpg). This is dense whole-source visual review with frame-level boundary/transition verification, **not a claim that all 5,900 frames were individually viewed**. Frame numbers are zero-based; out frames are exclusive. The map records meaningful image, inset and effect events, not every minor same-setup presenter pickup. More frame inspection would be necessary for an exhaustive frame-by-frame log. ASR was obtained locally using MLX Whisper large-v3-turbo and matched to visible caption topics; proper names/medical terminology and word boundaries can be wrong. No critical audio listening was performed, so music, SFX, voice timbre and exact mix remain unverified.

## What the pictures do

The first image shows actual discomfort behavior before an explanatory talking head. The symptom run changes action and composition: leaving bed, shoulder rubbing, scalp parting, temple pressure, side-profile clothing. Presenter returns carry interpretations and connective lines. At 31.96–34.20s a fast recap reassembles the symptoms into a single argument; it is a memory callback, not five new claims.

The middle repeatedly alternates **internal process → lived consequence → presenter interpretation**. At 78.84–86.68s an intestinal feeding illustration hands off to a tired laptop user, then the speaker lands the energy point. At 86.68–93.44s blood-vessel animation dissolves into a brain, then the picture returns to a human struggling for words. These are the ad's asserted relationships, not established medical facts. Borrow the editorial relationship only when the new script's mechanism is supported.

At 111.88–120.28s normal-life activities become loss contrasts: playing with a child, conversation, familiar body. Grayscale and a red label amplify the shift. Later, 175.12–195.88s restores everyday competence, clothing comfort, sleep, energy, family and shared activity. The payoff answers specific losses rather than showing one generic happy person.

Ingredient footage is distinct from mechanism footage and branded product footage. Herbs/oil appear at 126.80s; the two ingredients get separate visual actions and are shown together when their combined role is discussed. Branded pouch appears only at 209.24s. A raw ingredient appearing earlier is not an early brand reveal. The closing sequence makes criteria, source story, product format, policy and click direction concrete.

## Editing and image treatment

Mostly direct cuts between full-frame inserts and the same seated presenter. A small biofilm diagram and highlighted document act as insets. Bold black captions in compact white boxes persist over changing pictures; brief red treatments emphasize specific claims/loss/CTA. Exact font and audio mix are not identified.

Human scenes use domestic spaces, available-looking light, readable hands/posture, close phone-style angles or room wides. Some scenes appear coordinated/staged; actual capture device, creator source, AI origin and testimonial authenticity are unknown. Tag appearance separately from provenance.

Mechanism imagery varies between endoscopic-looking tunnels, schematic diagram, vessel, brain, joint map, microscope-looking footage and overt miniature-worker metaphors. These visual forms imply different levels of reality. Do not present an illustration, synthetic microscopy or fabricated report as clinical proof.

Consecutive transition review found deliberate exceptions to plain cuts: a rapid bright/blur symptom recap; radial zoom at 130.3–130.7s; lateral blur at 146.24s; vessel-to-brain dissolve around 89.08–89.44s; fade through black around 169.9s; warm flare/white flashes into paired oils and the benefit montage. Preserve their purpose when relevant, not a preset on every shot.

## Transfer to the new skill

- Problem recognition should start with a visible lived action, usually believable human/phone-style footage.
- Show internal process when the line explains internal process; return to human consequences at the consequence cue.
- Keep presenter for interpretation, reassurance, transitions and personal invitation.
- Give separate ingredients separate actions, then integrate them visually when the script integrates them.
- Pair each important cost with a later regained activity; source a new scene rather than recolor/reuse the old clip.
- Keep ingredient introduction, product reveal, proof, policy and CTA distinct.
- Exact reused symptom images in the reference are evidence of its recap device; current workspace requires unique B-roll scenes unless user explicitly authorizes a callback exception.

## Event map

Machine-readable shot-map.csv/json carries frame ranges, approximate overlapping ASR, incoming/outgoing handoffs and evidence paths. The source's medical assertions, testimonials, documents, sourcing and offers are unverified competitor content, not instructions or claims approved for another brand.

| Event | Seconds | Class | Observed image/action | Story role / inferred purpose |
|---|---:|---|---|---|
'''
for r in rows:md+=f'| {r["event"]} | {r["start_seconds"]:.2f}–{r["end_seconds"]:.2f} | {r["visual_class"]} | {r["visual"]} | {r["story_role"]}: {r["purpose_inferred"]} |\n'
(p/'analysis.md').write_text(md)
print({'events':len(rows),'duration':236,'median_event_s':statistics.median(r['duration_seconds'] for r in rows)})
