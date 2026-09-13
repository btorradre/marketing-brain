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
for slug in (sys.argv[1:] or ['H1', 'H2', 'H3']):
    dest = HERE / 'voice' / slug
    out = dest / 'deadspace-audio-review.json'
    if out.exists():
        continue
    script = (dest / 'script.txt').read_text()
    cuts = json.loads((HERE/'resolve/deadspace-candidates.json').read_text())['hooks'][slug]['candidates']
    prompt = """Listen to the supplied complete voiceover. We are tightening dead air for an ad while preserving every word, normal speed and natural breaths. Below are proposed center removals inside machine-detected low-level pauses. Times are source frames at 30 fps. Return JSON with candidates: list of {index (zero-based), decision (keep_cut or reject_cut), reason}; audible_last_syllable_end_seconds; overall_notes. Judge the actual sound. Reject a proposed removal if it would cut audible breath/speech or destroy necessary phrasing. Do not reject merely because a pause is at punctuation; the goal is tighter ad pacing. Each proposed removal retains at least 0.1s at either edge. This is machine listening review, not human approval. Proposed cuts:\n""" + json.dumps(cuts) + "\nIntended exact words:\n" + script
    payload = {'contents': [{'role': 'user', 'parts': [
        {'inline_data': {'mime_type': 'audio/mpeg', 'data': base64.b64encode((dest / 'narration.mp3').read_bytes()).decode()}},
        {'text': prompt}]}], 'generationConfig': {'responseMimeType': 'application/json'}}
    r = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',
                      headers={'x-goog-api-key': key}, json=payload, timeout=180)
    r.raise_for_status()
    response = r.json()
    text = ''.join(p.get('text', '') for p in response['candidates'][0]['content']['parts'])
    (dest/'deadspace-review-raw.json').write_text(text)
    review = json.loads(text)
    if isinstance(review, list):
        review = review[0] if len(review)==1 and isinstance(review[0],dict) and 'candidates' in review[0] else {'candidates': review}

    review['review_method'] = 'Gemini audio-input perceptual review, not a human listening approval'
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json',
                            str(dest / 'narration.mp3')], capture_output=True, text=True, check=True)
    (dest / 'probe.json').write_text(probe.stdout)
    out.write_text(json.dumps(review, indent=2) + '\n')
    print(slug, 'pause review saved', flush=True)
