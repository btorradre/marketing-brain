"""Assemble exact original cut windows in HyperFrames using retouched video plates."""
import argparse,html,json,shutil,math
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('family');p.add_argument('--index',action='store_true');a=p.parse_args()
row=next(r for r in json.loads(Path('shots.json').read_text()) if r['family']==a.family)
source=Path('assets')/a.family/'original.mp4'
if not source.exists():shutil.copy2(row['video'],source)
clips=[]
for shot in row['shots']:
    # Decimal rounding must never move a cut beyond its exact frame timestamp.
    # Start infinitesimally early and cover the full last intended frame.
    start=math.floor(shot['start']/24*1e9)/1e9
    duration=math.ceil((shot['end']-shot['start'])/24*1e9)/1e9
    if shot['retouch']:
        src=Path('plates')/a.family/f"shot-{shot['number']:02d}"/'shot.mp4'
        if not src.exists():raise RuntimeError(f'Missing repaired shot {src}')
        media_start=0
    else:
        src=source;media_start=start
    clips.append(f'<video id="{a.family}-{shot["number"]:02d}" class="clip" src="{html.escape(str(src))}" data-start="{start:.9f}" data-duration="{duration:.9f}" data-media-start="{media_start:.9f}" data-track-index="0" muted playsinline preload="auto"></video>')
duration=row['frames']/24
document=f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<title>Velantra {a.family.title()} — surface correction</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>*{{box-sizing:border-box;margin:0}}html,body{{width:1920px;height:1080px;overflow:hidden;background:#000}}#root{{position:relative;width:1920px;height:1080px;overflow:hidden}}.clip{{position:absolute;inset:0;width:1920px;height:1080px;object-fit:contain}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.9f}" data-width="1920" data-height="1080">
{chr(10).join(clips)}
</div><script>window.__timelines=window.__timelines||{{}};const timeline=gsap.timeline({{paused:true}});timeline.to({{}},{{duration:{duration:.9f}}});window.__timelines.main=timeline;</script></body></html>
'''
Path('assembly').mkdir(exist_ok=True)
Path('assembly',f'{a.family}.html.txt').write_text(document)
Path('index.html').write_text(document)
print(json.dumps({'family':a.family,'shots':len(row['shots']),'frames':row['frames'],'duration':duration,'composition':'index.html','archived_composition':f'assembly/{a.family}.html.txt'}))
