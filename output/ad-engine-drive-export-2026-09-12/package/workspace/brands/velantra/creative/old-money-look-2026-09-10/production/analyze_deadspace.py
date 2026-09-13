"""Prepare conservative, source-time silence candidates; never modify media."""
import json
import math
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30
result = {
    'updated_at': datetime.now(timezone.utc).isoformat(),
    'status': 'machine candidates; listening and Resolve application pending',
    'applied': False,
    'detector': {'noise_dbfs': -38, 'minimum_seconds': 0.30},
    'retained_edge_seconds': 0.10,
    'instructions': [
        'Review candidates and all shorter gaps by ear; protect words and breaths.',
        'Cut identical source-time intervals from narration and corresponding avatars.',
        'Ripple visuals and markers; preserve reveal timing and original speech speed.',
        'Remove unused head/tail and blank frames; finish about 0.15s after final audible syllable.',
        'Existing OTIO files are pre-trim bases; do not claim candidate cuts are applied.',
    ],
    'hooks': {},
}
for hook in ['H1', 'H2', 'H3']:
    source = HERE / 'voice' / hook / 'narration.mp3'
    scan = subprocess.run([
        'ffmpeg', '-hide_banner', '-i', str(source), '-af',
        'silencedetect=noise=-38dB:d=0.3', '-f', 'null', '-'
    ], capture_output=True, text=True, check=True)
    (HERE / 'voice' / hook / 'silence-scan.log').write_text(scan.stderr)
    intervals = []
    start = None
    for line in scan.stderr.splitlines():
        found = re.search(r'silence_start: ([\d.]+)', line)
        if found:
            start = float(found[1])
        found = re.search(r'silence_end: ([\d.]+)', line)
        if found and start is not None:
            end = float(found[1])
            left = math.ceil((start + 0.10) * FPS)
            right = math.floor((end - 0.10) * FPS)
            intervals.append({
                'quiet_start_seconds': start, 'quiet_end_seconds': end,
                'proposed_remove_start_frame': left,
                'proposed_remove_end_frame_exclusive': right,
                'proposed_removed_seconds': round(max(0, right-left)/FPS, 6),
                'listening_review': 'pending', 'applied': False,
            })
            start = None
    result['hooks'][hook] = {
        'source': str(source), 'fps': FPS,
        'applies_to_ads': [f'VEL-OM-{hook}-A{i}' for i in range(1, 4)],
        'candidates': intervals,
        'potential_internal_reduction_seconds': round(sum(
            x['proposed_removed_seconds'] for x in intervals), 3),
    }
out = HERE / 'resolve' / 'deadspace-candidates.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: {
    'candidates': len(v['candidates']),
    'potential_seconds': v['potential_internal_reduction_seconds']
} for k, v in result['hooks'].items()}, indent=2))
