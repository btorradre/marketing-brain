import sys,json,time,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[5];sys.path.insert(0,str(ROOT/'_engine/mcp/ad-engine'))
from engines import kie
import db
requests=[
('stool-softening','Vertical 9:16 scientific medical educational 3D illustration, clean smooth non-graphic anatomical teaching model. Tight diagonal longitudinal cutaway of a SHORT distal colon segment, pink layered wall framing a pale tan compact porous cylinder representing dry stool in the lumen. Small translucent blue water beads at its surface penetrate its outer porous layer, clear focus on hydration softening the contents. Camera at lumen level with a slight overhead angle, wall forms a diagonal channel from lower left to upper right. No stomach, no whole torso, no text, arrows, labels or UI. Dark deep navy background. High quality restrained realistic science animation first frame. No fecal realism, no gore, no cartoon faces.'),
('gastric-muscles','Vertical 9:16 scientific anatomical 3D illustration. Oblique BACK-SIDE view of an isolated anatomically recognizable stomach, muscular wall layers exposed in a small rectangular anatomical dissection window. Distinct circular and longitudinal muscle fiber bands wrap the lower antrum and narrow distal outlet, the bands contracting sequentially are the visual focus. Organ occupies center 75 percent of frame, inlet tube upper right and outlet curving lower left; clean coral and burgundy muscular bands, small translucent section hints at beige liquid contents. Deep navy background. NO big open stomach bowl, no colon, no torso, no labels, arrows, text or UI. Elegant realistic medical teaching model, non-graphic, no blood. First frame for a short animation about muscular propulsion as a different mechanism from stool hydration.'),
('gastric-retention','Vertical 9:16 clean realistic scientific 3D teaching model. High overhead three-quarter view down into an isolated anatomically recognizable stomach chamber with the upper wall partially transparent, retained pale golden semi-liquid contents visible beneath the transparent surface. The chamber lies diagonally across the composition, large fundus in upper left and very narrow pyloric outlet at lower right leading into a short duodenum. Majority of contents stay pooled in the body while only a tiny trickle can leave the narrow outlet. Emphasize the entire chamber and volume retained, not a close-up of the outlet. Smooth pink tissue with gentle ridges, dark navy background. No text, arrows, labels, torso, colon, gore or UI. Distinct high-angle mechanism first frame, restrained realistic medical educational visualization.')]
(P/'science-prompts.json').write_text(json.dumps(requests,indent=2))
for key,prompt in requests:
 receipt=P/(key+'-job.json')
 if not receipt.exists():
  assert kie.balance()>50
  job=kie.generate('gpt-image-2-text-to-image',{'prompt':prompt,'aspect_ratio':'9:16'},brand='motilli',concept='podcast-DVHp-v6');receipt.write_text(json.dumps(job,indent=2));print(key,'submitted',flush=True)
for key,prompt in requests:
 receipt=P/(key+'-job.json');job=json.loads(receipt.read_text())
 while job['status'] not in ['success','fail']:
  time.sleep(6);job=kie.status(job.get('job_id') or job['id']);receipt.write_text(json.dumps(job,indent=2))
 if job['status']=='success':
  with db.get_conn() as conn:a=conn.execute('SELECT path FROM assets WHERE job_id=?',(job.get('job_id') or job['id'],)).fetchone()
  shutil.copy2(a['path'],P/'assets'/(key+'.png'))
 print(key,job['status'],flush=True)
