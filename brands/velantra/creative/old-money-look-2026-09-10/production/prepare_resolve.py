"""Align approved beats and author Resolve OTIO assemblies without rendering media.

These are offline assemblies. Background removal and live Resolve import/render
must be verified before they can be considered completed ads.
"""
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent
FPS = 30
OUT = HERE / 'resolve'
OUT.mkdir(exist_ok=True)
sequences = json.loads((CONCEPT / 'storyboard/sequence-manifest.json').read_text())
body = {x['id']: x for x in json.loads((CONCEPT / 'storyboard/body-beats.json').read_text())}
matrix = json.loads((CONCEPT / 'storyboard/nine-ad-assembly.json').read_text())
selections = json.loads((HERE / 'voice/selection.json').read_text())

def norm(t):
    return ''.join(c.lower() for c in t if c.isalnum())

def rt(n, rate=FPS):
    return {'OTIO_SCHEMA': 'RationalTime.1', 'value': n, 'rate': rate}

def tr(start, dur):
    return {'OTIO_SCHEMA': 'TimeRange.1', 'start_time': rt(start), 'duration': rt(dur)}

def probe(path):
    return json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                                      '-of', 'json', str(path)], capture_output=True, text=True, check=True).stdout)

def gap(n):
    return {'OTIO_SCHEMA': 'Gap.1', 'metadata': {}, 'source_range': tr(0, n),
            'effects': [], 'markers': [], 'enabled': True}

def clip(path, src, dur, meta=None):
    available = dur + src
    if path.exists() and path.suffix != '.jpg':
        available = max(available, float(probe(path)['format']['duration']) * FPS)
    return {'OTIO_SCHEMA': 'Clip.2', 'name': path.name, 'metadata': meta or {},
            'source_range': tr(src, dur), 'effects': [], 'markers': [], 'enabled': True,
            'active_media_reference_key': 'DEFAULT_MEDIA',
            'media_references': {'DEFAULT_MEDIA': {'OTIO_SCHEMA': 'ExternalReference.1',
                'name': path.name, 'metadata': {}, 'target_url': str(path),
                'available_range': tr(0, available), 'available_image_bounds': None}}}

def track(name, kind, items, end):
    children = []; cursor = 0
    for start, item in sorted(items, key=lambda x: x[0]):
        assert start >= cursor, (name, start, cursor)
        if start > cursor: children.append(gap(start - cursor))
        children.append(item); cursor = start + item['source_range']['duration']['value']
    if cursor < end: children.append(gap(end - cursor))
    return {'OTIO_SCHEMA': 'Track.1', 'name': name, 'kind': kind, 'metadata': {},
            'source_range': tr(0, end), 'effects': [], 'markers': [], 'enabled': True, 'children': children}

aligned = {}
for hook, beats in sequences.items():
    audio = HERE / selections[hook]['path']
    alignment = json.loads((audio.parent / 'alignment.json').read_text())['alignment']
    raw = ''.join(alignment['characters'])
    mapping = [i for i, c in enumerate(raw) if c.isalnum()]
    normalized = norm(raw); cursor = 0; rows = []
    for beat in beats:
        line = beat['script']; needle = norm(line); pos = normalized.find(needle, cursor)
        assert pos >= 0, (hook, beat['beat_id'], line)
        first = mapping[pos]; last = mapping[pos + len(needle) - 1]
        start = alignment['character_start_times_seconds'][first]
        stop = alignment['character_end_times_seconds'][last]
        rows.append({**beat, 'speech_start': start, 'speech_end': stop,
                     'start_frame': round(start * FPS), 'speech_end_frame': math.ceil(stop * FPS)})
        cursor = pos + len(needle)
    for i, row in enumerate(rows):
        row['end_frame'] = rows[i + 1]['start_frame'] if i + 1 < len(rows) else row['speech_end_frame']
    speech_end = rows[-1]['speech_end_frame']; end = speech_end + 36
    windows = [{'id': hook + '-GRID', 'start': 0, 'end': rows[1]['start_frame'],
                'path': str(HERE / 'hooks' / hook / 'hook-native.mp4'), 'source_in_frames': 0,
                'reason': rows[0]['emotion']}]
    for row in rows:
        b = body.get(row['beat_id'])
        if not b or not b.get('source'): continue
        maximum = math.floor((b['source_out'] - b['source_in']) * FPS)
        duration = min(maximum, row['end_frame'] - row['start_frame'])
        windows.append({'id': b['id'], 'start': row['start_frame'], 'end': row['start_frame'] + duration,
                        'path': b['source'], 'source_in_frames': b['source_in'] * FPS, 'reason': b['why']})
    # Freeze an extracted source frame for the approved product-only end hold.
    cta = windows[-1]; source_sec = (cta['source_in_frames'] + cta['end'] - cta['start']) / FPS
    last_still = OUT / (hook + '-end-hold.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(max(0, source_sec - 1/24)), '-i', cta['path'],
                    '-frames:v', '1', '-y', str(last_still)], check=True)
    windows.append({'id': 'END-HOLD', 'start': cta['end'], 'end': end,
                    'path': str(last_still), 'source_in_frames': 0,
                    'reason': 'Preserve the last reviewed product image through the spoken CTA tail and 1.2 seconds after the final word.'})
    assert len({w['path'] for w in windows}) == len(windows), 'Unintended source repeat'
    aligned[hook] = {'fps': FPS, 'audio_path': str(audio), 'audio_duration': float(probe(audio)['format']['duration']),
                     'speech_end_frame': speech_end, 'end_frame': end, 'beats': rows, 'background_windows': windows,
                     'timing_method': 'Provider character alignment; rounded to nearest 30fps frame. Final lip-sync/render validation pending.'}

(OUT / 'aligned-sequences.json').write_text(json.dumps(aligned, indent=2) + '\n')
manifest = []
for ad in matrix:
    seq = aligned[ad['hook_id']]; end = seq['end_frame']; speech_end = seq['beats'][-1]['start_frame']
    avatar = HERE / 'avatars' / ad['ad_id'] / 'avatar-native.mp4'
    windows = seq['background_windows']
    bgitems = [(w['start'], clip(Path(w['path']), w['source_in_frames'], w['end'] - w['start'],
                                {'beat_id': w['id'], 'why_here': w['reason']})) for w in windows]
    cuts = sorted({0, speech_end, *[min(speech_end, w[k]) for w in windows for k in ['start', 'end']]})
    presenter = []; layout = []
    for start, stop in zip(cuts, cuts[1:]):
        covering = next((w for w in windows if w['start'] <= start < w['end']), None)
        mode = 'overlay' if covering else 'presenter_hold'
        layout.append({'start': start, 'end': stop, 'mode': mode,
                       'scale': .34 if mode == 'overlay' else 1.0,
                       'position': 'center-lower over grid; position per product shot to keep bag hardware clear' if covering else 'center',
                       'background_removal': 'Anna subject mask' if ad['avatar_id'] == 'A1' else 'green-screen key',
                       'status': 'requires live Resolve compositing and visual validation'})
        presenter.append((start, clip(avatar, start, stop-start, layout[-1])))
    audio = Path(seq['audio_path']); adur = min(end, math.floor(seq['audio_duration'] * FPS))
    tracks = [track('Video 1', 'Video', bgitems, end), track('Video 2', 'Video', presenter, end),
              track('Audio 1', 'Audio', [(0, clip(audio, 0, adur))], end)]
    markers = [{'OTIO_SCHEMA': 'Marker.2', 'name': b['beat_id'], 'color': 'BLUE',
                'marked_range': tr(b['start_frame'], max(1, b['end_frame']-b['start_frame'])),
                'metadata': {'script': b['script'], 'why_here': b['emotion']}} for b in seq['beats']]
    doc = {'OTIO_SCHEMA': 'Timeline.1', 'name': ad['ad_id'], 'global_start_time': rt(0),
           'metadata': {'delivery': '1080x1920', 'status': 'offline unkeyed assembly; not final ad'},
           'tracks': {'OTIO_SCHEMA': 'Stack.1', 'name': 'tracks', 'metadata': {}, 'source_range': tr(0, end),
                      'effects': [], 'markers': markers, 'enabled': True, 'children': tracks}}
    (OUT / f'{ad["ad_id"]}.otio').write_text(json.dumps(doc, indent=2) + '\n')
    manifest.append({**ad, 'avatar_path': str(avatar), 'audio_path': str(audio), 'duration_frames': end,
                     'otio': str(OUT / f'{ad["ad_id"]}.otio'), 'presenter_layout': layout,
                     'avatar_ready': avatar.exists(), 'in_resolve': False, 'exported': False})
(OUT / 'nine-ad-production-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'aligned_hooks': len(aligned), 'offline_assemblies': len(manifest),
                  'avatars_ready': sum(x['avatar_ready'] for x in manifest), 'live_import': False,
                  'final_exports': 0}, indent=2))
