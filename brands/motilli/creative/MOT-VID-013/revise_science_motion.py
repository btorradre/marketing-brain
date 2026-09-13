import json
from concurrent.futures import ThreadPoolExecutor
import produce_motion as m
m.OUT=m.HERE/'output/science-v2/motion/revisions';m.OUT.mkdir(parents=True,exist_ok=True)
m.MOTION={
'S12':'Slow camera push toward the existing stomach cutaway. The meal remains resting inside the stomach with every visible plant strand lying flat in its original place. Only a faint natural stomach-wall contraction and liquid surface shimmer. Keep every solid food piece and fiber strand fixed in size and position; no rising strands, sprouting, swelling, floating fibers or new material.',
'S22':'Macro scientific material animation in clear moving water: the existing fine translucent strands drift together gently from left to right, and several small water bubbles travel upward past the foreground strands. Clear visible relative motion, not a frozen still. Preserve strand thickness and length throughout. They remain separate dispersed strands, never clumping or turning into gel. Camera stays fixed.'}
plan=json.loads((m.HERE/'production-plan-science-v2.json').read_text())
with ThreadPoolExecutor(max_workers=2) as pool:
 for r in pool.map(m.generate,[s for s in plan['shots'] if s['id'] in m.MOTION]):print(r['shot'],r['status'],flush=True)
