"""Flag abrupt motion introduced inside a shot; preserve original hard cuts."""
import json
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent

def differences(path):
    capture = cv2.VideoCapture(str(path))
    result = [0.0]
    previous = None
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        small = cv2.GaussianBlur(cv2.resize(frame, (320, 180)), (0, 0), 1).astype(np.float32)
        if previous is not None:
            result.append(float(np.abs(small - previous).mean()))
        previous = small
    capture.release()
    return result

report = []
for family in json.loads((ROOT / 'shots.json').read_text()):
    original = differences(family['video'])
    revised = differences(ROOT / 'exports' / f"{family['family']}-surface-clean.mp4")
    assert len(original) == len(revised) == family['frames']
    shots = []
    for shot in family['shots']:
        indices = range(shot['start'] + 1, shot['end'])
        flags = [{'frame': i, 'original_mae': original[i], 'revised_mae': revised[i]}
                 for i in indices if revised[i] > 7 and revised[i] > original[i] * 3 + 3]
        peak = max(indices, key=lambda i: revised[i])
        shots.append({'shot': shot['number'], 'peak_frame': peak,
                      'peak_revised_mae': revised[peak], 'original_mae_at_peak': original[peak],
                      'flags': flags})
    row = {'family': family['family'], 'shots': shots, 'flags': sum(len(s['flags']) for s in shots)}
    report.append(row)
    print(json.dumps({'family': row['family'], 'flags': row['flags']}), flush=True)
(ROOT / 'qa/motion-continuity.json').write_text(json.dumps(report, indent=2) + '\n')
if any(row['flags'] for row in report):
    raise SystemExit(1)
