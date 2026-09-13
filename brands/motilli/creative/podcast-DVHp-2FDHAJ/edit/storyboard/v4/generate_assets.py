"""V4 storyboard images through the concept's authorized Kie integration."""
import json, sys, shutil
from pathlib import Path

V = Path(__file__).resolve().parent
ROOT = next(p for p in V.parents if (p / '_engine/mcp/ad-engine').exists())
sys.path.insert(0, str(ROOT / '_engine/mcp/ad-engine'))
from engines import kie
import db

SCI = ('Create ONE vertical 9:16 first frame for a scientific educational animation, '
       'a detailed realistic medical 3D illustration, non-gory. Deep dark navy blue backdrop #081b35, '
       'natural pink tissue, subtle teal rim light, warm contents. The requested anatomical subject fills '
       'the central 75% of the frame. Absolutely NO text, labels, arrows, numbers, logos, captions, '
       'panels, inset diagrams, white background, glowing magic or face. Not a clinical recording. ')
PHONE = ('Create ONE candid vertical 9:16 iPhone video first frame, as if casually recorded in 30 seconds '
         'by a friend for TikTok. Available room/daylight, deep smartphone depth of field, slight framing '
         'imperfection, ordinary lived-in environment, natural wrinkles and skin texture, relatable woman '
         'in her early-to-mid 50s, no commercial lighting, cinematic bokeh, glamour retouching, posed stock '
         'photography, text, watermark, branding, before/after layout or exaggerated acting. ')
PROMPTS = {
 'stomach-open': SCI + 'Three-quarter frontal view of ONE complete anatomically coherent stomach and short esophagus/duodenum. The front stomach wall is opened away to one side as a thin cutaway shell, revealing the rugae, modest tan chyme pool and narrow pyloric passage. Show the inside clearly: the open section is the main feature, not an exterior stomach. Starting state for a slow wall-opening reveal. No feces in stomach.',
 'contractions': SCI + 'Completely different composition: horizontal-oblique short section of SMALL INTESTINE shown longitudinally cut open, with muscular rings around the tube. One subtle shallow circular constriction behind soft chyme illustrates weak propulsion. The tubular intestinal muscle sleeve and interior lumen fill frame diagonally. No stomach, torso, food plate, or comparison diagram.',
 'appetite': SCI + 'Close sagittal slice through the UPPER STOMACH fundus/body from a side view, with a small meal retained inside and the gently distended muscular wall prominent. The folded interior wall and modest contents dominate the image, communicating lingering satiety after eating. Fine natural nerve fibers visible within the wall, not cartoon electrical icons. No whole digestive tract, brain, food plate, floating molecules or infographic.',
 'constipation': SCI + 'Oblique view of descending colon bending into sigmoid colon, with a longitudinal window through the near wall. Several dry compact brown stool pieces line up inside the colon lumen, showing slow backed-up passage. Clean textbook medical realism, no complete blockage, impaction, cancer, bleeding, feces outside the body, stomach or horror. This is constipation, not a stomach full of stool.',
 'colon-water': SCI + 'A single close longitudinal window into COLON, broad pink haustral tissue wall above and below one soft brown stool mass. Clear faint blue aqueous fluid is retained within the lumen around the stool, wetting its rough surface so it softens. The tissue, fluid and stool are the only subjects. No blue beads pouring through the wall, medical equipment, giant water drops, diagrams or text. Close internal camera distinct from a whole-colon anatomy view.',
 'bulk-fiber': SCI + 'Extreme macro view INSIDE the intestinal lumen. Pink curved intestinal tissue walls surround beige/tan psyllium husk fiber fragments immersed in fluid. The husk particles visibly have clear hydrated gel halos beginning to swell as they absorb surrounding water. A few unhydrated fragments remain alongside them in this one continuous scene, not comparison panels. Not a beaker, bowl, grain pile, roots or seaweed. Make fluid absorption into actual fiber material visually legible.',
 'pylorus': SCI + 'Close detailed oblique cutaway of the stomach ANTRUM narrowing into the PYLORIC SPHINCTER and the very beginning of duodenum. Only the outlet region is visible, not an entire stomach. One natural muscle squeeze advances a thin stream of tan liquid chyme through the open pyloric channel. Continuous anatomically connected lumen. Distinct from wide open-stomach shot and from intestinal muscle tube. No instant cure or dramatic before/after.',
 'fermentation': SCI + 'Camera INSIDE the stomach just above retained tan partially digested food. Pink rugae in the back and curved wall establish in-body stomach setting. A cluster of small gas bubbles forms locally at the surface of the retained food and rises through a small amount of fluid. Restrained illustrative fermentation concept, no microbial monsters, rotten food, green smoke, nose, face, floating odor cloud, sulfur symbols or food turning into feces. Macro low camera skimming the food surface, not a whole stomach cutaway.',
 'prebiotic-arrival': SCI + 'Microscopic angled surface view along a healthy COLON mucus layer: smooth coral mucosal terrain extends into depth, with a sparse friendly-looking but scientifically rendered community of naturally shaped rod and bifid bacteria. Dispersed fine soluble carbohydrate substrate moves in the fluid above and toward the microbial community. Substrate is small translucent off-white fragments, not grains or bulky tangled fibers. No text or stylized cartoon faces. First frame of substrate arriving, bacteria small within a wide microenvironment.',
 'prebiotic-uptake': SCI + 'Distinct close cross-sectional microscopic view at the COLON mucus boundary. Three to five rod/bifid bacterial cells dominate foreground, surrounded by tiny dispersed off-white soluble carbohydrate fragments, visibly clustered at bacterial surfaces for microbial utilization. Pink mucus/tissue boundary clearly behind them and navy negative space above. Not the same wide surface composition: a tight microcolony cross-section with different orientation and action. No bulky gel, symbols, magic, diagrams or text.',
 'fullness': PHONE + 'Medium candid view across her own kitchen table after lunch. Woman has shoulder-length chestnut hair with some gray, a muted sage everyday top and average body. Unfinished meal and fork on ordinary plate in foreground. She leans back slightly, one hand presses upper abdomen over clothing, brows pinched and mouth tense with uncomfortable fullness. Fully clothed, subtle convincing discomfort; not grabbing lower pelvis. Avoid smiling.',
 'burp': PHONE + 'Different woman in her late 50s with short dark curly hair and burgundy knit top, sitting in a parked car passenger seat, holding a hand lightly before her mouth immediately after a burp, embarrassed weary eyes looking aside. Daylight through window, parked suburban setting, seatbelt visible. No smell cloud or visual effects. Not driving, not vomiting.',
 'getting-dressed': PHONE + 'Woman in her early 50s with shoulder-length brown hair streaked with gray, ordinary average body, muted blue casual blouse and beige trousers. Medium-wide slightly low phone view in a lived-in bedroom with unmade bed and open wardrobe. She comfortably fastens the waist button of her trousers, shoulders relaxed, a small relieved smile. The ordinary action of getting dressed is clear. No weight-loss comparison, skinny reveal, underwear, mirror selfie phone in her hands, or fashion pose.',
 'lunch': PHONE + 'Two ordinary women in their early-to-mid 50s sharing lunch at a neighborhood cafe, captured informally from the third friend’s seat at the table. One brown-haired woman in a light blue everyday blouse looks attentively at her friend, who is mid-story with one natural hand gesture; both genuinely engaged in conversation. Casual sandwiches and soup, drinking water, window light, dishes slightly cluttered. Eye contact, comfortable posture and present attention; neither looks at camera or presses abdomen.',
 'afternoon': PHONE + 'Casual woman in her 50s with shoulder-length brown hair and a light blue shirt at her home doorway, slipping into a soft olive jacket and picking up keys from a crowded side table, ready to meet a friend. Three-quarter full-body phone framing from inside hallway, afternoon light through partly open door, relaxed face and easy movement. Ordinary freedom to go out, not a fashion campaign.',
 'celery': 'Create a photoreal ingredient overlay asset on a flat deep navy #081b35 background, vertical 9:16. Crisp fresh green celery stalks with leafy tops, cut ends visible, beside a small clear glass of freshly pressed celery juice. Large clear photographic cutout-like cluster in lower central half with uncluttered navy above. Natural botanical textures and soft edge separation. Not an infographic, molecule, drawing or illustration. NO words, labels, arrows, logos or captions.',
 'chlorophyll': 'Create a photoreal ingredient overlay asset on deep navy #081b35 background, vertical 9:16. Extreme detailed green leaf veins with small glass vial and a glass dropper holding one dark emerald green plant-pigment extract droplet. Actual photographed material appearance, not molecular schematic. Cluster of leaf, vial and dropper occupies lower central half with clean navy area above. No label on glass. NO text, formula, arrows, logos, green smoke or white background. This is a botanical ingredient visual, not a chemical identity assay.',
 'soluble-fiber': 'Create a photoreal dietary-supplement ingredient overlay asset on deep navy #081b35 background, vertical 9:16. A small precise measuring spoon of very fine off-white FOS soluble prebiotic supplement powder beside an open small clear glass supplement jar containing the same powder and a small glass of clear water. Fine powder is visibly a measured supplement serving, not flour sack, oats, wheat, roots, fiber strands or tangled fibers. Shot from close oblique top view, cluster in lower central half with clean navy above. No packaging brand, words, labels, arrows, infographic, or captions.',
}

def save(p,d): p.write_text(json.dumps(d,indent=2))

def prepare():
 reqs=[{'id':k,'model':'gpt-image-2-text-to-image','input':{'prompt':p,'aspect_ratio':'9:16'}} for k,p in PROMPTS.items()]
 # Existing host/guest references are already inspected. Preserve those exact faces.
 host=V.parent/'generated/host-gpt-image-2-5-kie.png'
 guest=V.parent/'generated/guest-gpt-image-2-5-kie.png'
 cache=V/'sources/uploads.json'
 urls=json.loads(cache.read_text()) if cache.exists() else {}
 for key,path in [('host',host),('guest',guest),('metamucil',V/'sources/metamucil-official.png')]:
  if key not in urls:
   urls[key]=kie.upload(str(path),upload_path='motilli-podcast-v4'); save(cache,urls)
 reqs += [
  {'id':'podcast-split','model':'gpt-image-2-image-to-image','input':{'input_urls':[urls['host'],urls['guest']],'aspect_ratio':'9:16','prompt':'Make a clean vertical 9:16 two-panel stacked podcast composition from these exact two supplied presenter references. TOP HALF must be the FEMALE HOST from image 1: preserve her exact face, long straight brown hair, navy hoodie, black microphone and warm beige studio. She listens thoughtfully. BOTTOM HALF must be the existing MALE SPEAKING GUEST from image 2: preserve his exact face, beard, olive cap, charcoal shirt and warm studio. Only these two people. Do NOT put any male cohost in top panel. Equal-height panels, eye lines natural, sharp clean horizontal boundary, no thick divider strip. Keep identity and wardrobes unchanged. Remove existing footer text and add NO text, subtitles, labels or logos. This is an AI storyboard concept, not an actual recording or endorsement.'}},
  {'id':'fiber-supplement','model':'gpt-image-2-image-to-image','input':{'input_urls':[urls['metamucil']],'aspect_ratio':'9:16','prompt':'Use the supplied actual Metamucil package as the exact identity reference. Create a casual vertical iPhone photograph of this real orange Metamucil psyllium fiber supplement tub on an ordinary slightly cluttered kitchen counter beside a glass of water, with a woman’s hand reaching for the lid. Preserve the recognizable Metamucil logo, orange cap, purple 4-in-1 fiber panel and turquoise sugar-free panel without redesign. Main brand and psyllium fiber supplement words legible. Unstaged ordinary window light, deep phone focus, off-center casual composition, no glossy campaign styling. No added labels or commentary, no extra product, not a generic fiber bowl. Normal intact safe use, no pouring a massive dose.'}}
 ]
 save(V/'image-requests.json',reqs)
 print('Prepared',len(reqs),'GPT Image 2 requests',flush=True)

def run(mode):
 requests=json.loads((V/'image-requests.json').read_text())
 for req in requests:
  rp=V/'receipts'/f"{req['id']}.json"
  if mode=='submit':
   if rp.exists():continue
   balance=kie.balance()
   if balance is None or balance<30: raise RuntimeError('Kie credit balance unavailable or below reserve.')
   job=kie.generate(req['model'],req['input'],brand='motilli',concept='podcast-DVHp-2FDHAJ-storyboard-v4')
   save(rp,{**req,'job':job}); print(req['id'],job.get('status'),job.get('error',''),flush=True)
  elif mode=='status' and rp.exists():
   rec=json.loads(rp.read_text()); job_id=rec['job'].get('job_id') or rec['job']['id']
   job=kie.status(job_id);rec['job']=job
   if job['status']=='success':
    with db.get_conn() as conn:
     assets=conn.execute('SELECT path,source_url FROM assets WHERE job_id=?',(job_id,)).fetchall()
    if assets and assets[0]['path']:
     dst=V/'assets'/f"{req['id']}.png"
     if not dst.exists():shutil.copy2(assets[0]['path'],dst)
     rec['output']=str(dst);rec['source_url']=assets[0]['source_url']
   save(rp,rec);print(req['id'],job['status'],job.get('error') or '',flush=True)

if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare()
 else:run(sys.argv[1])
