import pathlib,json,csv,hashlib,collections,statistics
p=pathlib.Path(__file__).parent
# Manually assessed starts from six consecutive decoded frames per detector candidate.
# Cue text is a paraphrase; never medical validation.
raw='''0|Curiosity promise: show where parasites live|mechanism+presenter|Endoscope-like camera enters pink mouth/throat; man's keyed bust bottom-left; red/yellow hook banner|Forward glide|Set destination and curiosity; commentator promises access to hidden scene
91|What you will see changes how you view symptoms|mechanism+presenter|New deeper pink intestinal tunnel with raised wall nodules; same keyed commentator and hook|Forward glide|Continue visual journey before revealing named antagonist
192|These here are parasites|mechanism+presenter|Brown/yellow damaged-looking gut interior with worm forms; keyed commentator points|Zoom-blur entry then drifting macro view|Name the thing after first showing it; deictic cue directs attention
240|Attached to intestinal wall|mechanism|Circular scope crop of coiled gut with elongated worms attached to wall; presenter disappears|Slow push|Give unobstructed view of location/attachment
288|Hiding behind a biofilm shield|mechanism|Tighter circular scope wall view with bulbous yellow-coated forms|Macro drift|Make protection/barrier spatially visible
336|Immune system cannot see it|mechanism|Single shielded lump with floating small bright particles passing nearby|Macro drift/particle motion|Represent failed contact between immune particles and protected target
402|Fermenting food|mechanism|Pale foaming mass around worm forms on gut wall|Bubbling action|Render the named process as visible change
468|Pumping inflammatory waste|mechanism|Gut tunnel with green liquid running over walls|Liquid flow|Switch from agent to its proposed output
515|Back into gut|anatomical-system|External semi-transparent torso/intestinal system|Slow anatomical drift|Briefly restore whole-organ orientation after many internal macros
544|Nightly bloating|human-problem|Phone-style overhead close shot of woman touching/pinching exposed abdomen while reclining|Hand action; small handheld drift|Translate invisible story into recognizable bodily discomfort
616|Look at these eggs|mechanism+presenter|Scope wall with translucent eggs and small worms; commentator keyed lower-left|Slow push; presenter pointing|Reset attention and introduce second antagonist/lifecycle objection
658|Hundreds of eggs|mechanism|Wide circular gut tunnel crowded with pale dots near lower wall|Slow forward drift|Show extent before macro detail
699|Embedded in gut lining|mechanism|Angled gut wall close-up containing translucent ovals and small worm forms|Macro drift|Show location rather than merely repeating egg quantity
744|Each egg hatches within two weeks|mechanism|Extreme macro of clustered pearl-like eggs; interiors/worm forms develop|Visible hatching animation|Animate lifecycle consequence that explains recurrence
827|Why previous cleanse failed|mechanism|Scope tunnel; white cleansing fluid rushes through dirty wall scene|Fluid surge|Introduce attempted solution and set up limitation
874|Killed some adults|mechanism|Remaining yellow-brown tunnel/worm material after fluid pass|Slow push|Separate partial effect from complete resolution
919|Eggs remain waiting|mechanism+overlay|Tight eggs on gut fold while white fluid passes; curved white arrow targets eggs|Fluid pass; fixed attention arrow|Show the missed target; arrow identifies the important residual detail
1019|Watch food pass|mechanism+presenter|Dark lumen with food matter and worms; keyed commentator returns|Forward drift; pointing|Announce a new mechanism chapter
1041|Food arrives and parasites eat first|mechanism|Same dark lumen/food scene with presenter layer removed|Food movement; slow push|Clear viewing area at the demonstration action; layout change, not a new underlying clip
1108|Nutrients the body needs|mechanism|Cleaner pink intestinal tunnel containing small gold particles|Forward drift|Establish normal desired flow before interception
1161|Zinc, iron, amino acids, vitamins|mechanism|Brown tunnel with four large colored nutrient-like shapes suspended inside|Colored pieces move toward viewer|One grouped view supports a list of related entities without a cut per noun
1255|Intercepted before body receives them|mechanism|Close intestinal folds with coated blobs and bright particle below|Macro drift|Begin interception sequence
1279|Intercepted before body receives them|mechanism|Villus-level red tissue, worms and large colored nutrient objects clustered at center|Macro particle convergence|Move to finer scale to show where interception happens
1324|Eating clean|human-attempt|Young man eating from plate at a table in everyday room; vertical phone composition|Fork-to-mouth action|Recognizable good habit becomes a failed-attempt example
1359|Taking supplements|human-attempt|Woman in kitchen selfie framing with several pills in open mouth|Mouth/swallow action|Concrete supplement behavior supports second attempted solution
1395|Still deficient|human-problem|Older man seated on bed in undershirt, rubbing abdomen and grimacing|Hand-to-abdomen action|Show the unresolved human consequence; symptoms do not prove deficiency
1432|They steal nutrients|mechanism|Wide interior with thin worms and drifting colored particles|Worm/particle motion|Return from habit examples to proposed reason they fail
1488|This is the vagus nerve|mechanism+presenter|Internal wall with long pale branching nerve-like structure; commentator lower-left points up|Slow push; pointing|Introduce a new named structure using guide plus visible referent
1542|Gut-to-brain connection|anatomical-system|Transparent upper torso/back of head with blue impulses running toward brain|Camera tracks upward along pulses|Show route at whole-system scale
1617|Clustered around nerve|mechanism+presenter|Return to inside wall and pale branching strand with small surrounding forms|Macro drift; presenter pointing|Reconnect whole-body route to localized claimed trigger
1671|Chemical signals|mechanism|Blue neuron-like branching web above lumpy microscopic landscape with moving cyan streaks|Fast electrical streaks; micro camera glide|Use a distinct microscopic vocabulary for signaling
1717|Signals trigger sugar cravings|anatomical-system|Frontal transparent torso with lit nerve path/brain and sugar/bread pictograms|Light pulses rise; food insets static|Integrate route and behavioral destination in one diagram
1779|Midnight trip to kitchen|human-problem|Wide dim home kitchen; woman approaches and opens refrigerator|Walking/refrigerator door action|Externalize abstract craving as a specific familiar behavior and time-of-day setting
1825|Cannot stop eating sweets|human-problem|Closer same kitchen/person holding ice-cream tub and spoon|Spoon-to-mouth action|Complete action chain from seeking food to eating it
1874|Signal started here|mechanism+presenter|Gut wall with worms and expanding purple rings; commentator points|Pulsing rings|Return human behavior to claimed source and visually mark origin
1923|What has been living inside you|mechanism|Close coated, dirty-looking intestinal fold|Slow macro glide|Re-establish antagonist before symptom recap
1969|Bloating|human-problem|Seated blonde woman struggles with waistband then exposes stomach|Pulling waistband/body reaction|Fast list montage gives symptom a distinct visible action
2001|Brain fog|human-problem|Young woman in robe at table presses forehead, eyes closed|Forehead hold/slumped pose|Switch face/body cue and environment to depict cognitive difficulty
2029|Fatigue|human-problem|Wide living room; person lies stretched out on sofa|Mostly still collapsed posture|Sub-second exhaustion insert; change shot scale and location
2051|Sugar cravings|human-problem|Close woman holding Nutella container and heaped sweet-filled spoon|Food held close to lens|Exaggerated food action gives craving an immediately legible image
2081|2 a.m. wake-ups|human-problem|Man lying on side in bed, eyes opening/looking aside|Small head/eye motion|Use sleep environment and restless expression for this symptom
2120|Joint pain|human-problem|Woman on edge of bed grips/rubs knee and leans back|Knee-rubbing and grimace|Specific joint and action instead of generic discomfort
2150|Skin breakouts|human-problem|Phone close-up of woman's visibly red facial skin, head angled toward lens|Head tilt|Surface-level symptom is best shown directly at close scale
2183|All one root cause|mechanism|Dark red crowded tissue with shiny worm/parasite-like forms|Slow dense organic motion|Collapse diverse symptom montage back into singular cause claim
2243|Behind biofilm|mechanism|Close wall with stacked yellow-coated bulbs|Slow macro push|Recall previously established barrier rather than introducing unrelated symbol
2301|No doctor told you|professional-context|Person in white coat working at a lab bench with microscope, monitors, test tubes|Seated bench work|Visual professional context for omission claim; image does not substantiate it
2356|Take two softgels before bed|product-use+presenter|Robe-wearing person's hands hold golden softgels near bed; commentator keyed below|Picking up capsule; hand rises to mouth|Show simple regimen at the solution pivot
2469|Wild oregano ingredient|ingredient|Green leafy plant macro outdoors|Gentle handheld/foliage motion|Move from scary interior to fresh tangible ingredient source
2546|85% carvacrol|ingredient|Yellow liquid droplet at pipette above amber glass bottle|Drop forms/falls|Switch from raw plant to concentrated liquid form on strength claim
2600|Paired with black seed oil|ingredient|Black seeds pour into white bowl|Pour accumulation|Introduce second ingredient with distinct color, texture and action
2678|Rich in thymoquinone|ingredient|Spoon scoops black seeds from white bowl|Scoop/lift|Closer tactile insert sustains second ingredient while naming active
2719|Two powerful compounds|presenter|Same male presenter full-frame in home, carved wood cabinet background|Conversational face/hand gesture|Human explanation synthesizes ingredient pair before demonstration
2821|Both arrive at once|mechanism|Inside mouth/throat with two golden capsules landing on tongue|Capsules tumble|Bridge recognizable dose to internal treatment path
2896|Watch first compound|mechanism|Golden liquid surges through intestinal tunnel onto coated material|Pour/flow|First ingredient receives distinct gold visual identity and action
2937|Hits biofilm|mechanism|Closer angle on stream striking bulbous shield surface|Impact/dissolution action|Advance from delivery to contact at target
2974|Shield cracks open|mechanism|Cut to coated structures splitting/opening along gut wall|Shell separation and debris|Visible before-to-after action carries barrier-removal claim
3056|Protection gone|presenter|Full-frame commentator in same room|Emphatic expression|Interpret prior action and pause before stage two
3165|Second compound finishes job|mechanism|Gut with worm forms; thick black fluid rushes in and washes through|Large continuous fluid surge; camera tracks|Second ingredient uses contrasting black color and sequential action; hold long enough to see completion
3351|Eggs survived previous cleanses|mechanism|Pale scope tunnel with clusters of white eggs; green liquid washes through|Fluid passes eggs|Reprise failed alternative to frame remaining objection
3437|Cheap oregano bounces off casings|mechanism|Dark bulb-like egg casing; cream spheres strike/bounce around it|Repeated sphere impacts|Different action explains proposed failure at barrier
3520|Weak black seed oil cannot crack|mechanism|Pale intestinal tunnel packed with eggs; black fluid passes over them|Black liquid flow|Show second solo ingredient's alleged insufficiency using same code
3582|Dissolved; contents wiped out|mechanism|Clean pink gut wall with translucent eggs fading/breaking down|Gradual disappearance|Pay off egg objection with visible change, then cleaner surface
3645|No next generation; previous cleanse failed|presenter|Full-frame commentator|Direct delivery|State conclusion after demonstration; reset visual load
3745|Shelf products are weak|retail-context|Long aisle of supplement bottles on store shelves|Shallow-focus lateral drift|Make comparison category tangible without inventing a named competitor
3813|Weak amounts / wrong origin|presenter|Full-frame commentator|Direct delivery|Carry verbal differentiation that footage cannot directly verify
3944|Second active barely does anything|mechanism|Black liquid between pink folds while clusters remain visible|Liquid stream around eggs|Recall inadequate standalone effect visually
4014|Need both at full strength together|presenter|Same full-frame commentator|Counting/emphatic hand gestures|Combine two-stage lesson into simple selection criterion
4122|Gut after three weeks|mechanism|Smooth pale-pink clean tunnel with a few softly glowing particles|Calm forward glide|Visual after-state contrasts earlier dirty, crowded texture
4194|Bloating gone|human-benefit|Woman standing in jeans turns then smiles with top lifted above abdomen|Body turn/smile|Mirror problem category with positive lived outcome; different person, not verified before/after
4242|Brain fog lifts|human-benefit|Woman seated on bed working at laptop in bright room|Typing/attentive posture|Show functioning behavior rather than another symptom pose
4293|Sugar cravings stop|human-benefit|POV hands throw decorated cake into trash bin|Clear discard action|A decisive behavior makes reduced desire visible
4345|Sleep through night|human-benefit|Person peacefully asleep on pillow under blanket|Still/restful pose|Quiet sustained image resolves restless-bed problem category
4408|Cause is gone|mechanism|Golden fluid washes worms from red intestinal tunnel|Fluid flush with moving organisms|Return benefit montage to shared cause and recap removal
4489|Resilia is the brand|product|Hand holds labeled white/green pouch in sunlit bedroom|Handheld pack display|First extended branding passage turns mechanism story into identifiable item
4538|Sourcing oregano|ingredient|Overhead bowl of fresh green leaves on stone tabletop|Subtle overhead drift|Recall tangible ingredient with composition different from first plant macro
4581|Mediterranean mountains / altitude|origin-context|Wide green alpine valley and jagged peaks|Slow landscape drift|Give provenance language geographic scale; actual source location not verified
4669|Ethiopian black seed oil|ingredient|Glass jar of black seeds with small gold spoon, overhead|Scoop/stir action|Match second ingredient with fresh composition and material identity
4750|Volcanic soil|origin-context|Ground-level close-up of dark cracked soil and small roots|Low close camera drift|Translate soil claim literally and change scale from landscape
4790|High-altitude origin|origin-context|Lush steep mountain with visible paths/valley|Aerial-like landscape drift|Return from soil micro-detail to geography/altitude
4827|Two oils|comparison-overlay|Split screen of golden and brown oil jars on bright tabletop|Subtle jar/lighting motion|Compress two inputs side-by-side in one glance
4852|Two countries|comparison-overlay|Split screen of earlier two mountain landscapes|Slow landscape motion|Parallel composition reinforces two-source formulation; repeats source landscapes
4878|One softgel|product-detail|Fingertips hold one translucent golden capsule against softly lit interior|Small hand/camera movement|Converge two-source story into one easy unit
4910|Small weekly batches|presenter|Full-frame commentator|Conversational delivery|Human assertion introduces scarcity rationale
4972|Cannot scale wild mountainside oregano|origin-context|Low green herb plants/rocks with hillside houses in warm light|Slow forward drift|Make limited-source story imaginable; landscape is illustrative, not supply evidence
5056|When video takes off|presenter|Full-frame commentator|Direct address|Pivot from origin to popularity/availability narrative
5116|They sell out|social-proof-collage|Nine-panel grid of people and product pouches|Several inset clips move simultaneously|Brief collective-uptake cue; actual purchases/testimonials not verified
5140|Waiting weeks for next drop|purchase-context|Woman at table using laptop on product site|Over-shoulder to closer screen drift|Show shopping context and make delay relevant at point of purchase
5209|If link is working|presenter|Full-frame commentator|Direct address|Set conditional click instruction
5261|Still available|product|Hand holds labeled pouch outdoors against dark steps|Handheld tilt|Keep recognizable product on availability statement
5312|Tap now|presenter|Presenter leans forward and points down toward bottom of frame|Downward pointing gesture|Align visible action with click location
5335|Two softgels before bed|product|Pouch standing on light surface with two golden softgels in front|Push toward pack/capsules|Reduce regimen to pack plus counted dose at close
5386|Three weeks|product|Hands hold pouch over lap/table in home|Small hand movement|Brief pack reminder on duration promise
5407|Your body will tell you|presenter|Same full-frame commentator concludes|Direct eye-line and speech|Close on human conviction; no separate static logo end-card'''
rows=[]
for line in raw.splitlines():
 frame,cue,cls,visual,movement,purpose=line.split('|');rows.append(dict(start_frame=int(frame),cue_paraphrase=cue,visual_class=cls,observed_visual_action=visual,observed_motion=movement,editorial_role_inference=purpose))
cands=json.loads((p/'candidate-frames.json').read_text());tr=json.loads((p/'transcript-mlx.json').read_text())
for i,r in enumerate(rows):
 r['shot_id']=f'YIX-{i+1:03d}';r['start_s']=round(r['start_frame']/30,3);r['end_frame_exclusive']=rows[i+1]['start_frame'] if i+1<len(rows) else 5484;r['end_s']=round(r['end_frame_exclusive']/30,3);r['duration_s']=round((r['end_frame_exclusive']-r['start_frame'])/30,3)
 r['incoming_transition']='opening frame' if i==0 else ('zoom-blur transition' if r['start_frame']==192 else ('presenter overlay removed; underlying scene continues' if r['start_frame']==1041 else 'hard cut'))
 r['outgoing_transition']='source ends' if i==len(rows)-1 else ('zoom-blur transition' if rows[i+1]['start_frame']==192 else ('presenter overlay removed' if rows[i+1]['start_frame']==1041 else 'hard cut'))
 r['boundary_review']='first source frame' if i==0 else 'personally inspected source frames n-3 through n+2 at 180x320; consecutive frame evidence'
 if r['start_frame'] in cands:
  idx=cands.index(r['start_frame']);r['boundary_evidence']=f'boundaries-{idx//10+1:02d}.jpg row {idx%10+1}; split file boundaries-{idx//10+1:02d}-{1 if idx%10<5 else 2}.jpg'
 else:r['boundary_evidence']='dense-01.jpg opening'
 r['transcript_excerpt_asr_unverified']=' '.join(w['word'].strip() for s in tr['segments'] for w in s.get('words',[]) if w['start']<182.64 and r['start_s']<=((w['start']+w['end'])/2)<r['end_s'])
 r['caption_style_observed']='Small white sans-serif with dark outline, generally near mid-frame/lower middle; phrase replacements; hook banner additionally at top until 6.4s'
 r['source_provenance_status']='Finished reference only. Original human/stock/CGI origin and capture device not verified.'
(p/'shot-map.json').write_text(json.dumps(rows,indent=2))
with (p/'shot-map.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
true={r['start_frame'] for r in rows};ver=[dict(frame=f,time=round(f/30,3),decision='confirmed edit/layout boundary' if f in true else 'rejected: continuous within-shot motion',review='six consecutive frames inspected') for f in cands];(p/'boundary-review.json').write_text(json.dumps(ver,indent=2))
counts=collections.Counter();dur=collections.Counter()
for r in rows:counts[r['visual_class']]+=1;dur[r['visual_class']]+=r['duration_s']
stats={'segments':len(rows),'verified_boundaries':len(rows)-1,'candidate_boundaries':len(cands),'mean_segment_s':182.8/len(rows),'median_segment_s':statistics.median(r['duration_s'] for r in rows),'class_segment_counts':dict(counts),'class_seconds':dict(dur),'all_decoded_frames':5484,'dense_samples_reviewed':366};(p/'statistics.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
# Reference sha and bounded clean transcript preserve raw result and explicitly remove hallucinated tail.
j=json.loads((p/'provenance.json').read_text());j.update({'video_sha256':hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest(),'retrieved_date':'2026-09-10','video_frames':5484,'video_duration_s':182.8,'container_duration_s':182.925397,'review':'Visual research only; no media generated or edited into production'});(p/'provenance.json').write_text(json.dumps(j,indent=2))
clean=' '.join(s['text'].strip() for s in tr['segments'] if s['start']<182.64);(p/'transcript-readable.txt').write_text('ASR draft, not approved narration. Caption spelling: Resilia, carvacrol. Hallucinated tail after 182.64 seconds excluded; raw output retained.\n\n'+clean)
