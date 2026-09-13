import base64
import sys
import json
import subprocess
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '.env').exists())
env = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines()
           if '=' in line and not line.startswith('#'))
key = env['GEMINI_API_KEY'].strip().strip('"').strip("'")
for slug in ['selected']:
    dest = HERE / 'voice'
    out = dest / 'audio-review.json'
    if out.exists():
        continue
    script = (HERE.parent / 'script-v1.txt').read_text()
    prompt = '''Listen to this entire supplied audio file. Review the actual sound, not just the supplied intended copy.
Return JSON: heard_transcript (literal words heard), matches_intended_words, missing_or_added_words,
pronunciation (Eleanor Weekender, Velantra, Birkin), delivery_naturalness_1_to_5,
delivery_observations (specific audible cadence, breaths, unnatural pauses, robotic patterns),
clipped_or_distorted, concerns_with_seconds, usable_for_raw_conversational_fashion_ad.
Be critical; do not pass the audio just because the intended copy is supplied. This is machine perceptual review, not human approval.
Intended exact copy:\n''' + script
    payload = {'contents': [{'role': 'user', 'parts': [
        {'inline_data': {'mime_type': 'audio/mpeg', 'data': base64.b64encode((dest / 'narration-native-1.1x.mp3').read_bytes()).decode()}},
        {'text': prompt}]}], 'generationConfig': {'responseMimeType': 'application/json'}}
    r = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',
                      headers={'x-goog-api-key': key}, json=payload, timeout=180)
    r.raise_for_status()
    response = r.json()
    text = ''.join(p.get('text', '') for p in response['candidates'][0]['content']['parts'])
    review = json.loads(text)
    review['review_method'] = 'Gemini audio-input perceptual review, not a human listening approval'
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json',
                            str(dest / 'narration-native-1.1x.mp3')], capture_output=True, text=True, check=True)
    (dest / 'probe.json').write_text(probe.stdout)
    out.write_text(json.dumps(review, indent=2) + '\n')
    print(slug, json.dumps(review), flush=True)
