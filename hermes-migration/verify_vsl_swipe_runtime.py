#!/usr/bin/env python3
"""Read-only skill discovery/retrieval checks using the installed Hermes runtime."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

CODE = """
import os
import json
from pathlib import Path
from tools.skills_tool import skills_list,skill_view
name='ai-ugc-vsl-swipe-copywriting'
listing=json.loads(skills_list())
assert any(s['name']==name for s in listing.get('skills',[])),listing.get('error','skill missing')
main=json.loads(skill_view(name,preprocess=False));assert main['success']
assert main['skill_dir']=='/opt/vault/agents/hermes/shared-skills/'+name
assert not main.get('setup_needed'),main.get('readiness_status')
case_id=os.environ.get('VSL_VERIFY_CASE','G2')
case=json.loads(skill_view(name,file_path='references/cases/'+case_id+'.md',preprocess=False));assert case['success']
root=Path(main['skill_dir'])
cases=json.loads((root/'references/cases.json').read_text());source=next(c for c in cases if c['caseId']==case_id)
transcript=json.loads(skill_view(name,file_path='references/'+source['transcriptPath'],preprocess=False))
assert transcript['success'];assert (root/'references'/source['transcriptPath']).read_text() in transcript['content']
if case_id.startswith('NU'):
 study=json.loads(skill_view(name,file_path='references/nuora-study/NUORA-ANALYSIS.md',preprocess=False));assert study['success']
 assert Path('/opt/vault/marketing-brain/HERMES-KNOWLEDGE-INDEX.md').is_file()
 assert json.loads((root/'references/corpus-manifest.json').read_text())['totalPackagedTranscripts']==392
print(json.dumps({'listed':True,'loaded':True,'caseLoaded':True,'transcriptLoaded':True,'noSetupRequired':True}))
"""


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',default='G2');args=parser.parse_args()
    profiles = sorted(set(p.parent for p in Path('/root').glob('.hermes*/config.yaml')) |
                      set(p.parent for p in Path('/root/.hermes/profiles').glob('*/config.yaml')))
    results = []
    for profile in profiles:
        env = os.environ.copy()
        env['HERMES_HOME'] = str(profile)
        env['VSL_VERIFY_CASE'] = args.case
        result = subprocess.run([sys.executable, '-c', CODE], env=env,
                                cwd='/root/.hermes/hermes-agent', capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(str(profile) + ': ' + result.stderr[-1500:] + result.stdout[-1000:])
        checks = json.loads(result.stdout.strip().splitlines()[-1])
        results.append({'profile': str(profile), **checks})
    report = {'verifiedProfiles': len(results), 'case': args.case, 'checks': results,
              'method': 'Installed Hermes skills_list and skill_view in fresh Python processes; no model inference or outbound messages.'}
    (Path(__file__).resolve().parent / 'runtime-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
