from pathlib import Path
import json,os,shutil,hashlib,zipfile
R=Path(__file__).resolve().parent;P=R.parent;dest=P/'final-nine-ads-r4';dest.mkdir(exist_ok=True)
manifest=json.loads((R/'resolve/manifest.json').read_text());qa=json.loads((R/'qa/final/report.json').read_text());rows=[]
folders={'H1':('01-Old-Money-Style','Old-Money-Style'),'H2':('02-Outfit-Transformation','Outfit-Transformation'),'H3':('03-Travel-Style','Travel-Style')}
for ad in manifest:
 folder,label=folders[ad['hook']];d=dest/folder;d.mkdir(exist_ok=True);source=R/'exports'/(ad['name']+'.mp4');target=d/(label+'-Presenter-'+ad['avatar']+'-R4.mp4')
 if not target.exists():os.link(source,target)
 sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha==qa[ad['name']]['sha256']
 text=json.loads((P/'voice'/ad['hook']/'request.json').read_text())['text'];assert ' '.join(x['verbatim'] for x in ad['captions'])==' '.join(text.split())
 (d/'FULL-SCRIPT.txt').write_text(text+'\n')
 rows.append({'ad':ad['name'],'file':str(target.relative_to(dest)),'duration_seconds':ad['duration_frames']/30,'sha256':sha,'voice_speed':1.1,'full_hook_bridge_body_cta':True})
shutil.copy2(R/'exports/Eleanor-OldMoney-R4.drp',dest/'Eleanor-OldMoney-R4.drp')
(dest/'NINE-AD-COVERAGE.json').write_text(json.dumps(rows,indent=2))
(dest/'START-HERE.md').write_text('''# Eleanor Weekender — all nine ads, R4

Start with **01-Old-Money-Style**. Each folder contains all three approved presenter variations and the complete script.

- New four-woman grids: different white women, old-money outfits and distinct carried bags.
- Bold, larger captions with dark backing. Hook placement keeps the bags visible.
- H1 cuts to the Weekender at 5.300 seconds on “This one gives you that classic.” H2 cuts at “Just swap this in” and H3 at “That's where this one comes in.”
- Voice and presenter run together at 1.1× with pitch preserved. Long quiet pauses removed; all narration and CTAs retained.
- Nine MP4s: 1080×1920, 30fps, H.264/AAC. H1 44.700s; H2 47.833s; H3 45.267s.

[Updated Cut Room storyboard](https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard)

The editable Resolve project contains nine timelines. Its media remains in this workspace's production folders; the DRP does not embed those source files. Previous R3 exports remain intact.

QA: full exports decoded; no black frames or detected quiet intervals >220ms at −44dB. Speech timing checked against the actual rendered audio; 95% of word starts within 42ms of plan. Pitch median ratio 1.000. All scene composites reviewed; A1 caption/cut boundary sheets reviewed per hook; source/presenter correspondence and empty keyed-background regions checked. This is not a claim every moving frame was individually viewed.
''')
archive=P/'Eleanor-OldMoney-All-9-Ads-R4.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
 for f in sorted(dest.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(dest.parent)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
(R/'qa/package-verification.json').write_text(json.dumps({'directory':str(dest),'zip':str(archive),'zip_bytes':archive.stat().st_size,'zip_crc_passed':True,'ads':rows},indent=2))
print(dest);print(archive);print('9 full ads; hashes and archive CRC verified')
