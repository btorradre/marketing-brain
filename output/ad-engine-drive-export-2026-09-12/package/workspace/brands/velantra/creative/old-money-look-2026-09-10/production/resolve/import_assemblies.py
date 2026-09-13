"""Import nine prepared assemblies into a fresh isolated Resolve project.

Run with Resolve's Python only after scripting connects. No renders are started:
subject/background removal and presenter positioning need live visual finishing.
"""
import datetime
import json
from pathlib import Path
import DaVinciResolveScript

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE/'nine-ad-production-manifest.json').read_text())
missing = [m['avatar_path'] for m in manifest if not Path(m['avatar_path']).exists()]
if missing: raise RuntimeError('Missing avatar assets: ' + ', '.join(missing))
resolve = DaVinciResolveScript.scriptapp('Resolve')
if not resolve: raise RuntimeError('Resolve scripting is unavailable; nothing imported.')
pm = resolve.GetProjectManager()
current = pm.GetCurrentProject()
if current and not pm.SaveProject(): raise RuntimeError('Could not save existing project; leaving it open.')
listed = pm.GetProjectListInCurrentFolder()
names = set(listed.values() if isinstance(listed, dict) else listed)
base = 'VEL_Eleanor_OldMoney_9Ads_2026-09-11'
name = base; suffix = 2
while name in names:
    name = base + '_' + str(suffix); suffix += 1
project = pm.CreateProject(name)
if not project: raise RuntimeError('Could not create isolated project.')
settings = {'timelineResolutionWidth':'1080','timelineResolutionHeight':'1920','timelineFrameRate':'30'}
if hasattr(project, 'SetSettings'): project.SetSettings(settings)
else:
    for k,v in settings.items(): project.SetSetting(k,v)
pool = project.GetMediaPool()
report = {'project': name, 'imported': [], 'final_exports': [], 'compositing': 'pending'}
for ad in manifest:
    timeline = pool.ImportTimelineFromFile(ad['otio'], {'timelineName': ad['ad_id']})
    if not timeline: raise RuntimeError('Import failed for ' + ad['ad_id'])
    report['imported'].append({'name':timeline.GetName(), 'id':timeline.GetUniqueId()})
    pm.SaveProject()
    (HERE/'live-import-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
