"""A clip review gallery, not a video compositor or export renderer."""
import json, shutil
from pathlib import Path
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SLUG='mot-vid-013-science-v2-motion'
ASSETS=ROOT/'cutroom/assets'/SLUG

def main():
 soup=BeautifulSoup((HERE/'MOT-VID-013-science-v2-storyboard.html').read_text(),'html.parser')
 timed={}
 for variant in ['A','B','C']:
  board=json.loads((HERE/'output/science-v2/editor'/f'MOT-VID-013-{variant}-board.json').read_text())
  timed.update({c['id']:c for c in board['lanes'][0]['cards']})
 def tc(t):return f'{int(t//60):02d}:{t%60:04.1f}'
 soup.title.string='Motilli · Motion review'
 soup.h1.clear();soup.h1.append('Science drives the explanation.');soup.h1.append(soup.new_tag('br'));soup.h1.append('Every shot follows the line.')
 soup.header.find('p').string='16 replacement scenes put anatomy and ingredient close-ups under the digestive explanation. People appear only for the normal-day activities. Same narration and three hooks; 41 Google Omni clips and three complete timeline drafts.'
 soup.select_one('.stats').clear()
 for value in ['41 motion clips','Google Omni','9:16 · 720p sources','~97s timeline drafts']:
  tag=soup.new_tag('span');tag.string=value;soup.select_one('.stats').append(tag)
 audio=soup.new_tag('audio',controls='',preload='metadata',src='narration.mp3');audio['id']='narration';soup.header.append(audio)
 note=soup.new_tag('p');note.string='Selected narration · Woman Over 40 · playback at the draft’s 1.22× pace';soup.header.append(note)
 links=soup.new_tag('p')
 for i,v in enumerate(['A','B','C']):
  filename=f'MOT-VID-013-{v}-timeline.json';shutil.copy2(HERE/'output/science-v2/editor'/filename,ASSETS/filename)
  link=soup.new_tag('a',href=filename,download=filename);link.string='Timeline '+v;links.append(link)
  if i<2:links.append(' · ')
 soup.header.append(links)
 for article in soup.select('section:not(.reference) .shot'):
  sid=article.select_one('.meta').get_text().split(' ')[0]
  card=timed[sid];article.select_one('.meta').string=f"{sid} · {tc(card['t'])}–{tc(card['t_end'])}"
  for paragraph in article.select('details p'):
   paragraph.string=paragraph.get_text().replace('GPT Image 2 keyframe. Google Omni motion follows visual review.','Google Omni source clip. Use the shown timeline window; source clips include extra handles.')
  picture=article.select_one('.picture');poster=picture.img['src']
  native=ASSETS/(sid+'.mp4')
  if native.exists():
   video=soup.new_tag('video',src=sid+'.mp4',poster=poster,controls='',muted='',playsinline='',preload='metadata')
   video['aria-label']='Play '+sid;video['style']='display:block;width:100%;aspect-ratio:9/16;background:#182019;object-fit:contain'
   picture.replace_with(video)
  else:
   warning=soup.new_tag('p');warning.string='Motion unavailable — provider rejected this shot.';warning['style']='padding:12px;background:#fff1d3;color:#664215;margin:0;font-weight:700';article.select_one('.meta').insert_after(warning)
 soup.select_one('.footer-inner').string='Native source clips are shown individually. These are not final exported ads. Timeline drafts contain the exact narration, timed captions, callouts and the planned end card. Final playback and export await the internal editor. Source-reference frames below are context only.'
 script=soup.new_tag('script');script.string="document.getElementById('narration').playbackRate=1.22;document.querySelectorAll('video').forEach(v=>{v.muted=true;v.addEventListener('play',()=>document.querySelectorAll('video').forEach(other=>{if(other!==v)other.pause()}))});"
 soup.body.append(script)
 page=str(soup)
 (ASSETS/'review.html').write_text(page)
 (HERE/'MOT-VID-013-science-v2-motion-review.html').write_text(page)
 print('Motion gallery: http://localhost:8765/assets/'+SLUG+'/review.html')

if __name__=='__main__':main()
