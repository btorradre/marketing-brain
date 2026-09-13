#!/usr/bin/env python3
"""Install the reviewed swipe package into the existing Hermes shared skill route.

Run on the Hermes host. Dry run by default; pass --apply to install. Does not
change models, credentials, profile configuration, running services or messages.
Requires the PyYAML dependency already used by the prior Hermes migration.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

import yaml

NAME = 'ai-ugc-vsl-swipe-copywriting'
SHARED = '/opt/vault/agents/hermes/shared-skills'
START = '<!-- BTO-VSL-SWIPES:START -->'
END = '<!-- BTO-VSL-SWIPES:END -->'
ROUTE = f'''{START}
## Spoken AI UGC and VSL specialist

For AI UGC scripts, spoken VSLs, hook selection, psychological appeals, swipe
adaptation, product bridges, and video copy critique, load `{NAME}` from
`{SHARED}/{NAME}/SKILL.md`. It includes Brooks's September 6 cross-brand study,
September 7 Nuora expansion, full source transcripts, hook selection guidance,
and a local search helper. For current local source material and path mapping,
read `/opt/vault/marketing-brain/HERMES-KNOWLEDGE-INDEX.md` and its linked sources.
For fresh drafting or substantial adaptation, retrieve the closest relevant
case transcripts before writing. Keep current product evidence and this
operating system authoritative. Transfer structure, not competitor claims or
invented customer experiences. Preserve the user's requested scope and format.
{END}'''


def digest_tree(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(path.rglob('*')) if p.is_file()}


def validate_package(source):
    skill = (source / 'SKILL.md').read_text()
    front = yaml.safe_load(skill.split('---', 2)[1])
    if front.get('name') != NAME or not front.get('description'):
        raise RuntimeError('Invalid skill frontmatter')
    refs = source / 'references'
    manifest = json.loads((refs / 'corpus-manifest.json').read_text())
    rows = [json.loads(line) for line in (refs / 'transcripts.jsonl').read_text().splitlines()]
    cases = json.loads((refs / 'cases.json').read_text())
    if len(rows) != manifest['totalPackagedTranscripts'] or len(cases) != manifest['curatedCases']:
        raise RuntimeError('Corpus counts differ from manifest')
    for row in rows:
        data = (refs / row['transcriptPath']).read_bytes()
        if hashlib.sha256(data).hexdigest() != row['sha256'] or data.decode() != row['fullText']:
            raise RuntimeError('Transcript integrity failure: ' + row['transcriptId'])
    for case in cases:
        if not (refs / case['transcriptPath']).is_file() or not (refs / case['analysisPath']).is_file():
            raise RuntimeError('Broken case reference: ' + case['caseId'])
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parent / NAME)
    parser.add_argument('--system-root', type=Path, default=Path('/'), help='Fixture root for isolated verification')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    source = args.source.resolve()
    manifest = validate_package(source)
    root = args.system_root.resolve()
    shared = root / SHARED.lstrip('/')
    target = shared / NAME
    doctrine = shared / 'dtc-marketing-operating-system/SKILL.md'
    if not shared.is_dir() or not doctrine.is_file():
        raise RuntimeError('Existing shared marketing installation not found; inspect the live Hermes setup first')
    configs = set((root / 'root').glob('.hermes*/config.yaml'))
    configs.update((root / 'root/.hermes/profiles').glob('*/config.yaml'))
    if not configs:
        raise RuntimeError('No Hermes profiles found; inspect the live setup first')
    profiles = []
    for config in sorted(configs):
        data = yaml.safe_load(config.read_text()) or {}
        dirs = (data.get('skills') or {}).get('external_dirs') or []
        registered = SHARED in [str(d).rstrip('/') for d in dirs]
        shadows = []
        for local in (config.parent / 'skills').rglob('SKILL.md'):
            text = local.read_text()
            try:
                fm = yaml.safe_load(text.split('---', 2)[1]) or {}
            except (IndexError, yaml.YAMLError):
                continue
            if fm.get('name') == NAME:
                shadows.append(str(local))
        profiles.append({'profile': str(config.parent), 'sharedDirRegistered': registered, 'localShadows': shadows})
    print(json.dumps({'mode': 'apply' if args.apply else 'dry-run', 'target': str(target),
                      'transcripts': manifest['totalPackagedTranscripts'], 'cases': manifest['curatedCases'],
                      'profiles': profiles}, indent=2))
    if not all(p['sharedDirRegistered'] and not p['localShadows'] for p in profiles):
        raise RuntimeError('Profile discovery differs from the prior migration; inspect reported profiles before installation')
    old_doctrine = doctrine.read_text()
    if START in old_doctrine:
        if old_doctrine.count(START) != 1 or old_doctrine.count(END) != 1:
            raise RuntimeError('Ambiguous existing referral block')
        left, rest = old_doctrine.split(START)
        _, right = rest.split(END)
        updated_doctrine = left + ROUTE + right
    elif END in old_doctrine:
        raise RuntimeError('Unclosed existing referral block')
    else:
        updated_doctrine = old_doctrine.rstrip() + '\n\n' + ROUTE + '\n'
    payload_changed = not target.exists() or digest_tree(source) != digest_tree(target)
    route_changed = old_doctrine != updated_doctrine
    if not args.apply:
        print(json.dumps({'wouldInstallPayload': payload_changed, 'wouldAddSpecialistRoute': route_changed}))
        return
    if not payload_changed and not route_changed:
        print(json.dumps({'status': 'already-installed', 'integrityVerified': True}))
        return
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = root / 'root/hermes-migration-backups' / ('vsl-swipes-' + stamp)
    backup.mkdir(parents=True)
    shutil.copy2(doctrine, backup / 'dtc-marketing-operating-system-SKILL.md')
    if target.exists():
        shutil.copytree(target, backup / NAME)
    staging_parent = Path(tempfile.mkdtemp(prefix='.vsl-swipes-stage-', dir=shared))
    stage = staging_parent / NAME
    shutil.copytree(source, stage)
    validate_package(stage)
    if digest_tree(stage) != digest_tree(source):
        raise RuntimeError('Staged package differs from source')
    old_target = staging_parent / 'previous'
    published = False
    try:
        if payload_changed:
            if target.exists():
                target.rename(old_target)
            stage.rename(target)
            published = True
        if route_changed:
            temporary = doctrine.with_name('.SKILL.vsl-swipes.tmp')
            temporary.write_text(updated_doctrine)
            shutil.copymode(doctrine, temporary)
            os.replace(temporary, doctrine)
        validate_package(target)
        if digest_tree(target) != digest_tree(source):
            raise RuntimeError('Installed package differs from source')
    except Exception:
        if published and target.exists():
            shutil.rmtree(target)
        if old_target.exists():
            old_target.rename(target)
        shutil.copy2(backup / 'dtc-marketing-operating-system-SKILL.md', doctrine)
        raise
    finally:
        shutil.rmtree(staging_parent)
    receipt = {'status': 'installed', 'target': str(target), 'backup': str(backup),
               'configuredProfiles': len(profiles), 'integrityVerified': True,
               'runtimeDiscovery': 'Not tested by this installer; verify skills_list/skill_view in a fresh Hermes session',
               'manifest': manifest, 'fileHashes': digest_tree(target)}
    (backup / 'installation-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k not in ['manifest', 'fileHashes']}, indent=2))


if __name__ == '__main__':
    main()
