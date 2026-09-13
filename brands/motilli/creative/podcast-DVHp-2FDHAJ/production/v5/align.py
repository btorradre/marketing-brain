import json, re, subprocess
from pathlib import Path

OUT=Path(__file__).resolve().parent
CONCEPT=OUT.parents[1]
pattern=re.compile(r"[\w]+(?:['’][\w]+)*")
def tokens(text):return [m.group().lower().replace('’',"'") for m in pattern.finditer(text)]
turns=json.loads((OUT/'dialogue-turns.json').read_text())
alignments={role:json.loads((OUT/f'{role}-paced-alignment.json').read_text())['alignment'] for role in ('host','guest')}
words=[];timeline_frame=0
for turn in turns:
    role=turn['speaker'];alignment=alignments[role]
    start=turn['source_char_start'];end=turn['source_char_end']
    assert ''.join(alignment['characters'][start:end])==turn['text']
    starts=alignment['character_start_times_seconds'];ends=alignment['character_end_times_seconds']
    source_start=max(0,round((starts[start]-.055)*30))
    source_end=round((ends[end-1]+.075)*30)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(OUT/f'{role}-avatar-master.mp4')]))
    source_end=min(source_end, int(float(probe['format']['duration'])*30))
    length=source_end-source_start
    turn.update({'source_start_frame':source_start,'source_end_frame_exclusive':source_end,'timeline_start_frame':timeline_frame,'timeline_end_frame_exclusive':timeline_frame+length,'fps':30})
    for match in pattern.finditer(turn['text']):
        i=start+match.start();j=start+match.end()-1
        words.append({'word':match.group(),'speaker':role,'source_start':starts[i],'source_end':ends[j],'start':timeline_frame/30+starts[i]-source_start/30,'end':timeline_frame/30+ends[j]-source_start/30})
    timeline_frame+=length
all_cards=json.loads((CONCEPT/'edit/storyboard/podcast-coverage.json').read_text())
cards=[c for c in all_cards if tokens(c['script_excerpt'])]
assert tokens(' '.join(c['script_excerpt'] for c in cards))==tokens(' '.join(w['word'] for w in words))
index=0
for i,card in enumerate(cards):
    count=len(tokens(card['script_excerpt']));subset=words[index:index+count]
    card['provisional_start']=card['start'];card['provisional_end']=card['end']
    card['start']=0 if i==0 else max(0,round(subset[0]['start']*30)/30)
    card['end']=round(subset[-1]['end']*30)/30
    card['word_index_start']=index;card['word_index_end']=index+count
    card['script_excerpt_timing']='ElevenLabs character timestamps, 1.1x source time, assembled in exact approved turn order; pending visual cut review'
    index+=count
for i,card in enumerate(cards):
    card['end']=cards[i+1]['start'] if i+1<len(cards) else timeline_frame/30+.7
    card['duration']=round(card['end']-card['start'],4)
    if card['mode'] not in ('Podcast · guest','Podcast · host','Podcast · female host TOP / guest BOTTOM'):
        card['insert_start']=card['start'];card['insert_end']=min(card['end'],card['start']+4)
        if card['id'] in ('S26-1','S26-2'):card['insert_end']=card['end']
    card['timing_qa']='pending final composed picture, lip-sync and caption review'
(OUT/'aligned-turns.json').write_text(json.dumps(turns,indent=2))
(OUT/'aligned-words.json').write_text(json.dumps(words,indent=2))
(OUT/'aligned-coverage.json').write_text(json.dumps(cards,indent=2))
(OUT/'alignment-qa.json').write_text(json.dumps({'exact_characters':True,'exact_coverage_word_order':True,'speaker_turns':len(turns),'coverage_cards':len(cards),'spoken_end_seconds':timeline_frame/30,'end_hold_seconds':.7,'status':'source timing complete; final video timing unverified'},indent=2))
print('Aligned',len(turns),'turns,',len(cards),'cards;',round(timeline_frame/30+.7,3),'seconds including end hold')
