from pathlib import Path
import json,csv,statistics,hashlib,re,subprocess
p=Path('brands/motilli/creative/MOT-UGC-YAPPER-01/edit/reference-analysis')
trans=json.loads((p/'reference-transcript.json').read_text())
# Full-frame changes manually confirmed on the adjacent-frame contact sheets.
# Caption-only changes, within-shot motion, overlays and page scrolling excluded.
events=[(0,'Presenter: car selfie'),(122,'Dresses on shop mannequins'),(158,'Presenter'),(198,'Couple portrait'),(234,'Presenter'),(266,'Engagement-party couple'),(315,'Presenter'),(367,'Woman with microphone at event'),(437,'Presenter'),(636,'Seated woman / claimed prior condition'),(697,'Presenter'),(774,'Salad and drink'),(810,'Woman climbing stairs'),(852,'Woman looking at abdomen'),(928,'Presenter'),(971,'Two-woman outdoor portrait'),(1026,'Presenter'),(1182,'Nuora bottle in hand'),(1231,'Presenter'),(1264,'Abdomen mirror image: before-style'),(1294,'Abdomen mirror image: after-style'),(1323,'Presenter'),(1340,'Fitting / clothing-rack scene'),(1419,'Presenter'),(1479,'Science: estrogen torso'),(1541,'Presenter with later inset'),(1648,'Science: illuminated digestive torso'),(1696,'Presenter with later inset'),(1788,'Science: bloodstream'),(1858,'Presenter'),(1894,'Science: digestive tract'),(1967,'Presenter'),(2006,'Science: cortisol torso'),(2065,'Science: changing abdomen model'),(2122,'Presenter'),(2281,'Science: fat-cell view'),(2341,'Presenter with ingredient inset'),(2462,'Science: intestinal wall animation'),(2614,'Presenter with intermittent insets'),(2814,'Science: intestinal tunnel'),(2858,'Presenter'),(2889,'Nuora bottle and supplement label'),(3019,'Presenter holding bottle'),(3152,'Loose waistband detail'),(3210,'Presenter'),(3265,'Abdomen / waistband result'),(3325,'Presenter'),(3425,'Navy dress mirror scene'),(3553,'Presenter'),(3574,'Floral dress mirror scene'),(3680,'Presenter'),(3701,'Two women at reception'),(3803,'Presenter'),(3890,'Two women discussing at table'),(4003,'Presenter'),(4170,'Wedding group photo'),(4238,'Presenter'),(4278,'Woman holding drink at event'),(4358,'Presenter'),(4402,'Loose waistband detail reused'),(4468,'Presenter'),(4520,'Presenter pickup / face reset'),(4653,'Nuora product-page scroll'),(4695,'Presenter'),(4862,'Navy dress event scene'),(4968,'Presenter'),(5012,'Open supplement bottle'),(5055,'Presenter'),(5081,'Woman in pale activewear'),(5137,'Presenter'),(5211,'Presenter holding bottle: closing pickup')]
duration=5266/30
rows=[]
for i,(f,label) in enumerate(events):
 end=events[i+1][0] if i+1<len(events) else 5266
 st=f/30;et=end/30
 # ASR word timestamps supply approximate narration overlap, independent of exact image boundaries.
 words=[w['word'].strip() for s in trans['segments'] for w in s.get('words',[]) if w['start']<et and w['end']>st]
 rows.append(dict(shot=f'S{i+1:02}',start_frame=f,end_frame_exclusive=end,start_seconds=st,end_seconds=et,duration_seconds=et-st,visual=label,narration=' '.join(words),incoming='Cold open' if i==0 else 'Direct cut / presenter pickup; adjacent source frames reviewed',outgoing='End of source' if i==len(events)-1 else 'Direct cut to '+events[i+1][1],timing_basis='Image frames measured; narration ASR approximate'))
(p/'verified-shot-map.json').write_text(json.dumps(rows,indent=2))
with (p/'verified-shot-map.csv').open('w') as h:
 w=csv.DictWriter(h,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
presenter=sum(r['duration_seconds'] for r in rows if r['visual'].startswith('Presenter'))
stats=dict(source='https://app.trendtrack.io/share/ads/alicia-darling-LFj90I',ad_id='1833962050620738',video_seconds=duration,container_seconds=175.6561,fps=30,width=720,height=1280,frames=5266,source_sha256=hashlib.sha256((p/'alicia-darling-reference.mp4').read_bytes()).hexdigest(),reviewed_candidate_boundary_pairs=162,retained_fullframe_shots=len(rows),median_shot_seconds=statistics.median(r['duration_seconds'] for r in rows),presenter_base_percent=presenter/duration*100,asr_words=656,approx_wpm=656/175.6561*60)
(p/'source-metadata.json').write_text(json.dumps(stats,indent=2))
md=f'''# Alicia Darling reference: observed editing map

Source: https://app.trendtrack.io/share/ads/alicia-darling-LFj90I. Share metadata identifies Facebook ad **1833962050620738**, not the earlier inaccessible 880104018170915. Original media saved without alteration. Video is **720×1280, 30fps, 5,266 frames / 175.533 seconds**; container/audio tail lasts 175.656 seconds.

Review: all three 1fps overview sheets covering the whole video and **162 candidate before/after frame pairs** were visually inspected. Caption changes, motion and page scrolling were rejected as cuts. The retained map has **{len(rows)} full-frame shots/pickups**, median **{stats['median_shot_seconds']:.2f}s**. Small inset events are additional overlays, not double-counted as full-frame shots. This is a cut map, not a claim that every intervening frame was manually viewed. Complete transition spans would need extra inspection if a dissolve or other transition were suspected; reviewed retained cuts are abrupt frame changes. Ambiguous tiny presenter motion is not automatically counted as a cut.

## What to reproduce

- Base image: close, eye-level car selfie, denim shirt and visible seat belt; face fills much of the upper frame. Occasional mild reframing/pickups, gestures and changing facial expression. These identity/wardrobe details belong to the reference, not to the new Motilli character.
- Approximately **{stats['presenter_base_percent']:.1f}%** of the picture uses the presenter as its base, including moments with an inset graphic; the remainder is full-frame inserts. The woman returns repeatedly to carry reactions and interpretation.
- Captions: bold-looking black sans serif on tight white rectangular boxes, generally one or two short lines, centered around chest height. Exact font family is unknown. Caption styling persists across presenter and B-roll. This is materially different from the provisional white-text outline treatment.
- Typical inserts are brief and tied to nouns/actions: dress → wedding scene → emotional reaction; meal → stairs → abdomen; bottle when named. Science receives a denser sequence of full-frame illustrations and small image insets.
- Full-frame replacements use direct cuts. Inset images appear below the caption/face on some ingredient words. Avoid blanket push-ins, wipes, animated title cards or a mandatory new shot at every sentence.
- Source is fast: local ASR yields approximately **656 words / 224 wpm** over the file. ASR mishears Nuora and Akkermansia; retain raw output as machine evidence, not polished transcript. Word timestamps are approximate. This pace is a source observation, not permission to time-stretch approved narration.
- Audio contains a sustained female narration in the transcript across insert changes. Source waveform/transcription were processed locally. Music level, timbre, SFX and mix were not independently established by critical listening; do not claim exact sound matching yet. Preserve continuous voice and leave soundtrack decisions open.
- The loose-waistband B-roll around 105–107s returns around 146.7–148.9s. For Motilli, follow the user's current visual-variety instruction and use different scenes instead of copying that reuse.

## Narrative sequence versus the requested Motilli script

This ad opens with family drama, not the prior Nuora PDF hook. It names Nuora around 39–40s before its mechanism lesson, then uses another product/label insert at 96.3s. Its UMS discusses berberine and black pepper, not the earlier PDF's bromelain pairing. Transfer editing grammar only. Preserve the supplied Motilli opening, UMP/UMS order and later brand entry. No reference health claim or testimonial outcome becomes Motilli evidence.

## Source shot/narration map

Exact image cuts below use 30fps source frames. Narration is ASR-aligned and may straddle boundaries. The JSON/CSV includes outgoing handoffs. Captions and continuous narration apply throughout; scene-specific motion is visible in overview/boundary images.

| Shot | Frames [in,out) | Seconds | Picture | Approximate narration overlap |
|---|---:|---:|---|---|
'''
for r in rows:md+=f"| {r['shot']} | {r['start_frame']}–{r['end_frame_exclusive']} | {r['start_seconds']:.3f}–{r['end_seconds']:.3f} | {r['visual']} | {r['narration']} |\n"
md+='\n## Evidence files\n\nOriginal MP4; local audio WAV; raw ASR JSON; 1fps overview-01/02/03.jpg; boundaries-01 through boundaries-09.jpg; boundary-index.json; verified-shot-map.json/csv. The screenshot grid and reference footage are comparison evidence only and are not selected assets for the Motilli ad.\n'
(p/'reference-breakdown.md').write_text(md)
print(json.dumps(stats,indent=2))
