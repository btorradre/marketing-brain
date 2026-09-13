from pathlib import Path
import json,os,shutil,hashlib,zipfile
R=Path(__file__).resolve().parent;P=R.parent;dest=P/'final-nine-ads-r5';dest.mkdir(exist_ok=True)
manifest=json.loads((R/'resolve/manifest.json').read_text());qa=json.loads((R/'qa/final/report.json').read_text());rows=[]
folders={'H1':('01-Old-Money-Style','Old-Money-Style'),'H2':('02-Outfit-Transformation','Outfit-Transformation'),'H3':('03-Travel-Style','Travel-Style')}
for ad in manifest:
 folder,label=folders[ad['hook']];d=dest/folder;d.mkdir(exist_ok=True);source=R/'exports'/(ad['name']+'.mp4');target=d/(label+'-Presenter-'+ad['avatar']+'-R5.mp4')
 if not target.exists():os.link(source,target)
 sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha==qa[ad['name']]['sha256']
 text=json.loads((P/'voice'/ad['hook']/'request.json').read_text())['text'];assert ' '.join(x['verbatim'] for x in ad['captions'])==' '.join(text.split())
 (d/'FULL-SCRIPT.txt').write_text(text+'\n')
 rows.append({'ad':ad['name'],'file':str(target.relative_to(dest)),'duration_seconds':ad['duration_frames']/30,'sha256':sha,'voice_speed':1.1,'full_hook_bridge_body_cta':True})
shutil.copy2(R/'exports/Eleanor-OldMoney-R5.drp',dest/'Eleanor-OldMoney-R5.drp')
(dest/'NINE-AD-COVERAGE.json').write_text(json.dumps(rows,indent=2))
(dest/'START-HERE.md').write_text("""# Eleanor Weekender — all nine ads, R5

Start with **01-Old-Money-Style**. Each folder contains the three presenter variations and complete approved script.

- White sentence-case captions with close black outlines around individual letters. No black boxes, backing panels or shadows.
- Caption appearance and bottom-center placement matched against the actual Nuamore reference. Source font metadata is unavailable; Arial Regular is the visual reconstruction.
- R4 footage, exact narration, 1.1× synchronized voice/presenter, pitch preservation and quiet-pause trims retained.
- Weekender reveal retained: H1 at 5.300 seconds on “This one gives you that classic”; H2 at 5.867s; H3 at 8.967s.
- Nine MP4s, 1080×1920, 30fps, H.264/AAC. H1 44.700s; H2 47.833s; H3 45.267s.

[Updated Cut Room storyboard](https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard)

The editable Resolve project contains nine timelines. The DRP references source media in this workspace and does not embed it. Previous R4 exports remain intact.

QA: every export fully decoded with no black frames; durations, caption wording/timing and outline-only native graphs verified. Rendered audio checked against corresponding R4 exports. Actual scene and caption composites visually reviewed, including light and dark backgrounds. This does not claim every moving frame was individually viewed.
""")

archive=P/'Eleanor-OldMoney-All-9-Ads-R5.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
 for f in sorted(dest.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(dest.parent)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
(R/'qa/package-verification.json').write_text(json.dumps({'directory':str(dest),'zip':str(archive),'zip_bytes':archive.stat().st_size,'zip_crc_passed':True,'ads':rows},indent=2))
print(dest);print(archive);print('9 full ads; hashes and archive CRC verified')
