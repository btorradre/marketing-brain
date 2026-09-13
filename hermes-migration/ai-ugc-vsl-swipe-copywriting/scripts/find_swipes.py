#!/usr/bin/env python3
"""Search the packaged corpus without network access or third-party dependencies."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query', default='')
    parser.add_argument('--pattern', default='')
    parser.add_argument('--brand', default='')
    parser.add_argument('--case', default='')
    parser.add_argument('--nuora-id', default='', help='Retrieve a Nuora study ID, including noncurated texts')
    parser.add_argument('--all', action='store_true', help='Include noncurated transcripts')
    parser.add_argument('--limit', type=int, default=8)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 50:
        parser.error('--limit must be between 1 and 50')
    root = Path(__file__).resolve().parents[1] / 'references'
    cases = json.loads((root / 'cases.json').read_text())
    patterns = json.loads((root / 'patterns.json').read_text())
    if args.pattern and args.pattern not in {p['id'] for p in patterns}:
        parser.error('Unknown pattern. Available: ' + ', '.join(p['id'] for p in patterns))
    if args.case and args.case.upper() not in {c['caseId'] for c in cases}:
        parser.error('Unknown case ID')
    by_transcript = {}
    for case in cases:
        by_transcript.setdefault(case['transcriptId'], []).append(case)
    results = []
    for line in (root / 'transcripts.jsonl').read_text().splitlines():
        row = json.loads(line)
        linked = by_transcript.get(row['transcriptId'], [])
        if not args.all and not args.nuora_id and not linked:
            continue
        if args.nuora_id and row.get('nuoraStudyId') != args.nuora_id.upper():
            continue
        if args.case:
            linked = [c for c in linked if c['caseId'] == args.case.upper()]
            if not linked:
                continue
        if args.pattern:
            linked = [c for c in linked if args.pattern in c['patterns']]
            if not linked:
                continue
        if args.brand.casefold() not in row['brand'].casefold():
            continue
        haystack = (row['fullText'] + ' ' + row['brand'] + ' ' + row.get('nuoraStudyId', '') + ' ' + row.get('executionFamily', '') + ' ' + json.dumps(linked)).casefold()
        words = args.query.casefold().split()
        if not all(word in haystack for word in words):
            continue
        results.append({
            'transcriptId': row['transcriptId'], 'brand': row['brand'],
            'caseIds': [c['caseId'] for c in linked],
            'patterns': sorted({p for c in linked for p in c['patterns']}),
            'wordCount': row['wordCount'],
            'nuoraStudyId': row.get('nuoraStudyId'),
            'executionFamily': row.get('executionFamily'),
            'reviewLevel': row.get('reviewLevel', 'See original case analysis and coverage'),
            'opening': ' '.join(row['fullText'].split()[:45]),
            'transcriptFile': str(root / row['transcriptPath']),
            'analysisFiles': [str(root / c['analysisPath']) for c in linked],
            'sourceAds': row['sources'],
        })
    print(json.dumps({'matches': len(results), 'returned': min(args.limit, len(results)),
                      'results': results[:args.limit]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
