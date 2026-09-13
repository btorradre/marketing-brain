#!/usr/bin/env python3
"""Verify synced knowledge bytes against the local source snapshot manifests."""
from pathlib import Path
import hashlib
import json


def main():
    staging = Path(__file__).resolve().parent
    root = Path('/opt/vault/marketing-brain')
    manifests = ['manifest.json', 'memory-manifest.json']
    verified = 0
    failures = []
    seen = {}
    for name in manifests:
        for item in json.loads((staging / name).read_text()):
            if item['path'] in seen:
                if seen[item['path']] != item['sha256']:
                    failures.append({'path': item['path'], 'reason': 'conflicting snapshot manifests'})
                continue
            seen[item['path']] = item['sha256']
            target = root / item['path']
            if not target.is_file():
                failures.append({'path': item['path'], 'reason': 'missing'})
            elif hashlib.sha256(target.read_bytes()).hexdigest() != item['sha256']:
                failures.append({'path': item['path'], 'reason': 'hash mismatch'})
            else:
                verified += 1
    report = {'verifiedFiles': verified, 'failures': failures,
              'method': 'SHA-256 of each server file compared to the local document/data and memory snapshot',
              'scope': 'Knowledge documents/data and Markdown memory; excludes generated media, credentials, caches, and banned composition tooling.'}
    (staging / 'knowledge-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
