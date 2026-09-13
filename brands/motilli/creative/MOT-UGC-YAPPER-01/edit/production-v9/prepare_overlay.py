from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json
O=Path(__file__).resolve().parent;A=O.parent.parent/'assets/images-v9'
source=Image.open(A/'apigenin-research-page.png').convert('RGB')
crop=source.crop((0,120,1700,1940));crop.save(A/'apigenin-research-crop.png')
canvas=Image.new('RGB',(1080,1920),'#f1f3f5');d=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',32)
bold=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',36)
d.text((44,96),'In vitro microbiota study',fill='#233c55',font=bold)
d.text((44,148),'PMC • Molecules • 2017',fill='#66727d',font=font)
canvas.paste(crop.resize((1032,round(crop.height*1032/crop.width)),Image.Resampling.LANCZOS),(24,220))
canvas.save(A/'apigenin-research-overlay.png')
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(A/'apigenin-research-overlay.png'),'-frames:v','132','-an','-c:v','qtrle','-pix_fmt','argb','-threads','1',str(O/'apigenin-research-overlay.mov')],check=True)
(O/'overlay-layout.json').write_text(json.dumps({'source_crop':[0,120,1700,1940],'source_unmodified_text':True,'canvas':[1080,1920],'paper_position':[24,220],'paper_width':1032,'label':'In vitro microbiota study','caption_position':'Unchanged; below paper ending at1325px','timeline_frames':[4619,4751]},indent=2))
