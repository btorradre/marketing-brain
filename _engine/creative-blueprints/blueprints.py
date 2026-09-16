#!/usr/bin/env python3
"""Portable, standard-library lookup and validation for the concept library."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
ROUTER = 'skills/creative-diversity-router'
DEFINITIONS = f'{ROUTER}/references/profiles.json'
CONTRACTS = [f'{ROUTER}/references/production-contract.md',
             f'{ROUTER}/references/profile-contract.md']
BEAT_FIELDS = ['id', 'communication_job', 'visual_action', 'style_id',
               'placement_entry_exit_return', 'proposed_dwell_handoff', 'rationale']
STYLE_FIELDS = ['id', 'visual_treatment_and_source_route', 'placement_and_purpose']


def local(relative):
    path = (ROOT / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(ROOT):
        raise ValueError(f'Path leaves the bundle: {relative}')
    return path


def read_json(relative):
    return json.loads(local(relative).read_text(encoding='utf-8'))


def records():
    return read_json('manifest.json')['concepts']


def selected(profile_id):
    for record in records():
        if record['id'] == profile_id:
            return record
    raise ValueError(f'Unknown profile: {profile_id}. Use list to see available IDs.')


def definition(profile_id):
    data = next(p for p in read_json(DEFINITIONS)['concepts'] if p['id'] == profile_id)
    return {**data,
            'beats': [dict(zip(BEAT_FIELDS, beat)) for beat in data['beats']],
            'styles': [dict(zip(STYLE_FIELDS, style)) for style in data['styles']]}


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def validate():
    manifest = read_json('manifest.json')
    concepts = read_json(DEFINITIONS)['concepts']
    indexed = records()
    if manifest['schema_version'] != 1 or not indexed:
        raise ValueError('Expected schema 1 and a nonempty concept library')
    if len({r['id'] for r in indexed}) != len(indexed):
        raise ValueError('Duplicate profile IDs')
    if {p['id'] for p in concepts} != {r['id'] for r in indexed}:
        raise ValueError('Manifest and definitions disagree')
    study = [r for r in indexed if r.get('source_kind', 'reference-audit') == 'reference-audit']
    expected_refs = set(manifest.get('reference_study_refs', [f'R{i:02}' for i in range(1, 15)]))
    if {r['source_ref'] for r in study} != expected_refs or len(study) != len(expected_refs):
        raise ValueError('Original reference-study coverage has changed')
    total_frames = 0
    workspace_cases = 0
    for record in indexed:
        item = definition(record['id'])
        if (item['skill'], item['ref'], item['title']) != (
                record['family'], record['source_ref'], record['title']):
            raise ValueError(f'Manifest metadata drift: {record["id"]}')
        for key in ('skill', 'blueprint', 'editing_profile', 'source_analysis',
                    'provenance', 'coverage'):
            if not local(record[key]).is_file():
                raise ValueError(f'Missing {key}: {record["id"]}')
        for relative in record.get('additional_context', []):
            if not local(relative).is_file():
                raise ValueError(f'Missing additional context: {relative}')
        source = read_json(record['provenance'])
        coverage = read_json(record['coverage'])
        if source['url'] != record['source_url']:
            raise ValueError(f'Source URL drift: {record["id"]}')
        kind = record.get('source_kind', 'reference-audit')
        if kind == 'reference-audit':
            if coverage['unreviewed_ranges'] or coverage['reviewed_frames'] != coverage['total_frames']:
                raise ValueError(f'Incomplete recorded coverage: {record["source_ref"]}')
            if coverage['total_frames'] != source['specs']['frame_count']:
                raise ValueError(f'Frame count mismatch: {record["source_ref"]}')
            total_frames += coverage['total_frames']
        elif kind == 'workspace-synthesis':
            if not coverage.get('review_scope') or not coverage.get('inspected_evidence'):
                raise ValueError(f'Missing workspace review scope: {record["source_ref"]}')
            if source.get('source_kind') != kind or coverage.get('source_kind') != kind:
                raise ValueError(f'Workspace provenance kind mismatch: {record["source_ref"]}')
            for evidence in coverage['inspected_evidence']:
                path = local(evidence['path'])
                if hashlib.sha256(path.read_bytes()).hexdigest() != evidence['sha256']:
                    raise ValueError(f'Evidence hash mismatch: {evidence["path"]}')
            workspace_cases += 1
        else:
            raise ValueError(f'Unsupported source kind: {kind}')
    links = 0
    files = [p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    for path in files:
        if path.is_symlink():
            raise ValueError(f'Bundle must contain real files: {path.relative_to(ROOT)}')
        if path.suffix not in ('.md', '.json', '.yaml', '.py'):
            continue
        content = path.read_text(encoding='utf-8')
        if re.search(r'/(?:Users|home)/[^\s/]+/', content):
            raise ValueError(f'Nonportable home path in {path.relative_to(ROOT)}')
        if path.suffix != '.md':
            continue
        for target in re.findall(r'\]\(([^)]+)\)', content):
            target = target.strip().strip('<>')
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                raise ValueError(f'Broken/nonportable link in {path.relative_to(ROOT)}: {target}')
            links += 1
    result = subprocess.run([sys.executable, str(local(f'{ROUTER}/scripts/render_profiles.py')),
                             '--check'], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or result.stdout.strip())
    emit({'status': 'valid', 'concept_variants': len(indexed),
          'families': len({r['family'] for r in indexed}),
          'skills': len(list((ROOT / 'skills').glob('*/SKILL.md'))),
          'paired_documents': len(indexed) * 2, 'local_links_checked': links,
          'workspace_syntheses': workspace_cases,
          'recorded_reviewed_frames': total_frames,
          'evidence_limit': 'Frame total covers reference-audit records only; workspace samples remain separate. Validation does not re-inspect media.'})


def install(destination):
    destination = Path(destination).expanduser().resolve()
    sources = sorted(p.parent for p in (ROOT / 'skills').glob('*/SKILL.md'))
    pending = []
    for source in sources:
        target = destination / source.name
        if target.resolve() == source.resolve():
            continue
        if target.exists() or target.is_symlink():
            raise ValueError(f'Existing skill preserved; choose another directory: {target}')
        pending.append((source, target))
    destination.mkdir(parents=True, exist_ok=True)
    for source, target in pending:
        target.symlink_to(source, target_is_directory=True)
    emit({'skills_dir': str(destination), 'created': len(pending),
          'already_linked': len(sources) - len(pending),
          'note': 'Keep the bundle at this location; refresh the host skill catalog if needed.'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    listing = commands.add_parser('list', help='List all concept variants')
    listing.add_argument('--json', action='store_true')
    showing = commands.add_parser('show', help='Read a pair member or structured definition')
    showing.add_argument('profile_id')
    showing.add_argument('--format', choices=['json', 'blueprint', 'profile'], default='json')
    context = commands.add_parser('context', help='Print the complete Markdown reading packet')
    context.add_argument('profile_id')
    commands.add_parser('validate', help='Check coverage records, portable links and generated docs')
    installing = commands.add_parser('install', help='Register all library skill links without overwrites')
    installing.add_argument('--skills-dir', required=True)
    args = parser.parse_args()
    if args.command == 'list':
        if args.json:
            emit(records())
        else:
            for record in records():
                print(f'{record["id"]}\t{record["source_ref"]}\t{record["title"]}')
    elif args.command == 'show':
        record = selected(args.profile_id)
        if args.format == 'json':
            emit({'paths_relative_to_bundle': record,
                  'required_contracts': CONTRACTS,
                  'definition': definition(args.profile_id)})
        else:
            key = 'editing_profile' if args.format == 'profile' else 'blueprint'
            print(local(record[key]).read_text(encoding='utf-8'))
    elif args.command == 'context':
        record = selected(args.profile_id)
        paths = [*CONTRACTS, record['skill'], record['blueprint'],
                 record['editing_profile'], record['source_analysis'],
                 *record.get('additional_context', []),
                 'support/Ad-Editing-Plan-First-SOP.md',
                 'support/Copywriting-Structure-and-Specificity-SOP.md']
        print(f'# Reading packet: {record["title"]}\n\nAll paths are relative to the bundle. '
              'Current user instructions take precedence; resolve image links from their source file.\n')
        for path in paths:
            print(f'\n---\n\nSource file: `{path}`\n\n{local(path).read_text(encoding="utf-8")}')
    elif args.command == 'validate':
        validate()
    else:
        install(args.skills_dir)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
