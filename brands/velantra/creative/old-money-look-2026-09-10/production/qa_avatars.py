"""Check all avatar files and audio synchronization without altering originals."""
import json
import subprocess
from pathlib import Path
import numpy as np
from scipy.signal import correlate, correlation_lags
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
matrix = json.loads((HERE.parent / 'storyboard/nine-ad-assembly.json').read_text())
selection = json.loads((HERE / 'voice/selection.json').read_text())

def pcm(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', '8000',
                        '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32)

def probe(path):
    return json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
                                    capture_output=True, text=True, check=True).stdout)

report = []
for ad in matrix:
    d = HERE / 'avatars' / ad['ad_id']; path = d / 'avatar-native.mp4'
    if not path.exists(): continue
    info = probe(path); (d / 'probe.json').write_text(json.dumps(info, indent=2))
    src = pcm(HERE / selection[ad['hook_id']]['path']); dst = pcm(path)
    pairs = []
    for seconds in [0, 20, 40]:
        i = seconds * 8000; n = min(80000, len(src) - i, len(dst) - i)
        x, y = src[i:i+n], dst[i:i+n]
        c = correlate(y, x, mode='full', method='fft'); lags = correlation_lags(len(y), len(x))
        valid = np.abs(lags) <= 2400; lag = int(lags[valid][np.argmax(c[valid])])
        if lag >= 0: xx, yy = x[:len(x)-lag], y[lag:]
        else: xx, yy = x[-lag:], y[:len(y)+lag]
        coeff = float(np.corrcoef(xx, yy)[0, 1])
        pairs.append({'window_start_seconds': seconds, 'audio_lag_seconds': lag / 8000,
                      'waveform_correlation': round(coeff, 5)})
    duration = float(info['format']['duration']); v = next(s for s in info['streams'] if s['codec_type']=='video')
    canvas = Image.new('RGB', (960,600), '#222222'); draw = ImageDraw.Draw(canvas)
    for i, t in enumerate([1, duration/2, duration-1]):
        f = d / f'qa-{i}.jpg'
        subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-y',str(f)],check=True)
        im = Image.open(f); im.thumbnail((318,565)); canvas.paste(im,(i*320,30))
        draw.text((i*320+3,8),f'{ad["ad_id"]} {t:.2f}s',fill='white')
    canvas.save(HERE/'qa'/f'{ad["ad_id"]}-sheet.jpg')
    result = {'ad_id': ad['ad_id'], 'duration': duration, 'width': v['width'], 'height': v['height'],
              'frame_rate': v['r_frame_rate'], 'audio_correspondence': pairs,
              'original_audio_preserved_in_edit': True,
              'limit': 'Waveform correlation verifies audio correspondence, not visible lip synchronization. Sampled frames need visual review; final keying and composed export QA remain.'}
    report.append(result)
    print(ad['ad_id'], pairs, flush=True)
(HERE/'qa/avatar-file-and-audio-checks.json').write_text(json.dumps(report,indent=2)+'\n')
