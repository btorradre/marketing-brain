# Ad Library Link → Gemini Analysis → Brief Pipeline

When a user pastes a Meta Ad Library URL, execute this automated pipeline. The user pastes a link, you handle everything else, and deliver a full Gemini visual analysis + video editor brief.

---

## Step 1: Detect the URL Format

Meta Ad Library URLs come in 3 formats. Parse accordingly:

**Format A: Keyword Search**
```
https://www.facebook.com/ads/library/?...&q=balmbare.com&search_type=keyword_unordered&...
```
→ Scrapes all ads matching the keyword. Filter for video ads, take top 5 by impressions.

**Format B: Page-Level**
```
https://www.facebook.com/ads/library/?...&view_all_page_id=663571616828831&...
```
→ Scrapes all ads from a specific advertiser page. Filter for video ads, take top 5.

**Format C: Single Ad ID**
```
https://www.facebook.com/ads/library/?id=4093398267656797
```
→ Scrapes that single ad. If it's a video, analyze it directly.

---

## Step 2: Scrape with Apify

Use the `meta-ad-scraper` Apify actor (ID: `JHGi3kAzHO1t3Fxrb`) to scrape the Ad Library page.

```python
from apify_client import ApifyClient
import json, os, subprocess, time

APIFY_KEY = '[REDACTED_SECRET]'
client = ApifyClient(APIFY_KEY)

def scrape_ad_library(url):
    """Scrape a Meta Ad Library URL and return video ads."""
    run = client.actor('JHGi3kAzHO1t3Fxrb').call(run_input={
        'targetUrl': url,
        'maxConcurrency': 3
    })

    items = list(client.dataset(run['defaultDatasetId']).iterate_items())

    # Filter for video ads only
    video_ads = [item for item in items if item.get('videos') and len(item['videos']) > 0]

    print(f"Total ads scraped: {len(items)}")
    print(f"Video ads found: {len(video_ads)}")

    return video_ads
```

---

## Step 3: Download Videos

```python
def download_video(video_ad, output_dir='/sessions/dazzling-tender-pascal/videos'):
    """Download a video ad and return the local file path."""
    os.makedirs(output_dir, exist_ok=True)

    vid = video_ad['videos'][0]
    url = vid['url'] if isinstance(vid, dict) else vid

    library_id = video_ad.get('libraryID', 'unknown')
    filename = f"{output_dir}/ad_{library_id}.mp4"

    subprocess.run(
        ['wget', '-q', '-O', filename, '--timeout=30', url],
        capture_output=True, text=True, timeout=60
    )

    if os.path.exists(filename) and os.path.getsize(filename) > 10000:
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"Downloaded: {filename} ({size_mb:.1f}MB)")
        return filename
    else:
        print(f"Failed to download ad {library_id}")
        return None
```

---

## Step 4: Gemini Frame-by-Frame Analysis

Upload each video to Gemini and run the analysis prompt.

```python
from google import genai

GEMINI_KEY = '[REDACTED_SECRET]'
gemini_client = genai.Client(api_key=GEMINI_KEY)

GEMINI_ANALYSIS_PROMPT = """You are analyzing a direct response video ad from Facebook/Meta. Perform a THOROUGH frame-by-frame analysis covering:

1. **VISUAL PACING TIMELINE**: Break the video into segments (every 5-10 seconds). For each segment note:
   - What's on screen (talking head, b-roll, overlay, text, product shot)
   - Camera angle/framing changes
   - Any text overlays or captions
   - Visual transitions (cuts, zooms, etc.)

2. **SCRIPT-VISUAL SYNC**: How do the visuals support what's being said? When does the speaker appear vs. when do we see supporting visuals? What's the ratio of speaker-on-screen vs. b-roll/overlays?

3. **ORGANIC FEEL ASSESSMENT**: Rate 1-10 how organic/native this feels (vs. "produced ad"). What specific techniques make it feel native? (lighting, camera work, setting, wardrobe, audio quality, etc.)

4. **PACING ANALYSIS**:
   - How often do visual interrupts happen? (count cuts per minute)
   - Average duration of each visual segment
   - Where are the visual "beats" that keep attention?
   - What's the speaker-to-camera hold duration for trust-building moments?

5. **HOOK VISUALS (first 5 seconds)**: What's happening visually? What text appears? How does the visual support the spoken hook?

6. **PRODUCT INTRODUCTION VISUALS**: When does the product first appear? How is it framed? How much screen time does it get?

7. **FULL TRANSCRIPT**: Transcribe the complete spoken audio word-for-word. Include timestamps where possible.

8. **VISUAL LAYER BREAKDOWN**: Categorize all visual elements into these layers and estimate % of total screen time for each:
   - Speaker-to-camera (talking head)
   - Floating overlays (images/diagrams over speaker)
   - Full-screen b-roll (speaker disappears)
   - Full-screen animations/diagrams
   - Credential props (phone/paper held to camera)
   - Product sequence (product shots)

Be extremely detailed and specific about timestamps."""


def analyze_video_with_gemini(video_path):
    """Upload video to Gemini and get frame-by-frame analysis."""
    print(f"Uploading {video_path} to Gemini...")
    uploaded = gemini_client.files.upload(file=video_path)

    # Wait for processing
    while uploaded.state.name == 'PROCESSING':
        time.sleep(5)
        uploaded = gemini_client.files.get(name=uploaded.name)

    print(f"Analyzing with Gemini (model: gemini-2.5-flash)...")
    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[uploaded, GEMINI_ANALYSIS_PROMPT]
    )

    return response.text
```

---

## Step 5: Generate the Brief

Take the Gemini analysis and generate a video editor brief following the `brief-template.md` structure.

```python
BRIEF_GENERATION_PROMPT = """Based on the following Gemini frame-by-frame analysis of a reference video ad, generate a complete video editor brief.

The brief should follow this exact structure:

### YOUR #1 JOB
One sentence: replicate this reference ad's style and pacing for [Brand]'s script.

### ASSETS TABLE
| Asset | Link / Location |
|-------|----------------|
| Script (approved copy) | [to be provided] |
| Reference Ad | [Meta Ad Library link] |

### EDITING RULES
Based on what Gemini observed in the reference ad, specify:
- Rhythm (how often visual interrupts happen — use the actual frequency from the analysis)
- Overlays (how they're positioned — floating? full-screen? lower-third?)
- B-roll style (what types of b-roll were used, when they appear)
- Captions (style, color, position — match the reference)
- Transitions (cuts? zooms? swipes?)
- Sound (clean audio? ASMR b-roll? music?)

### VISUAL LAYER SYSTEM
Based on the Gemini visual layer breakdown, specify each layer with its approximate % of screen time:
1. Speaker-to-camera — X% (describe setting, framing, wardrobe)
2. Floating overlays — X% (describe type: stock photos, diagrams, screenshots)
3. Full-screen b-roll — X% (describe content: nature, lifestyle, medical)
4. Animations — X% (describe: 3D renders, infographics, diagrams)
5. Credential props — X% (describe: phone held up, papers, screenshots)
6. Product sequence — X% (describe: bottles, labels, website)

### VISUAL INTERRUPT TIMING
From the Gemini pacing analysis, specify:
- Cuts per minute
- Average segment duration
- Speaker hold duration for trust beats
- When product first appears

### ORGANIC FEEL NOTES
From the Gemini organic feel assessment, list the specific techniques that make this ad feel native (not produced). The editor should replicate these.

### DELIVERABLES
1. Final video: MP4, 9:16, 1080×1920, H.264, 30fps minimum
2. Project file (CapCut / Premiere / DaVinci)
3. Diagram/overlay assets as separate PNG/PSD files
4. Brief rationale: 3-5 sentences on editing choices

### EVALUATION CRITERIA
| Criteria | Weight |
|----------|--------|
| Reference fidelity | 30% |
| Pacing & visual interrupts | 20% |
| Diagram/overlay quality | 20% |
| B-roll integration | 15% |
| Platform nativeness | 15% |

---

Here is the Gemini analysis of the reference ad:

{gemini_analysis}

---

Here is the ad copy/metadata:

Brand: {brand}
Ad Library ID: {library_id}
Start Date: {start_date}
Primary Text: {body}
CTA: {cta}

Generate the complete brief now. Be specific — the editor should be able to produce the video from this brief alone without watching the reference ad."""
```

---

## Full Pipeline (Copy-Paste Ready)

Here's the complete pipeline that runs end-to-end when a user pastes a link:

```python
from apify_client import ApifyClient
from google import genai
import json, os, subprocess, time

# API Keys
APIFY_KEY = '[REDACTED_SECRET]'
GEMINI_KEY = '[REDACTED_SECRET]'

apify_client = ApifyClient(APIFY_KEY)
gemini_client = genai.Client(api_key=GEMINI_KEY)

def run_pipeline(ad_library_url, max_videos=5):
    """
    Full pipeline: Ad Library URL → Scrape → Download → Gemini Analysis → Brief

    Args:
        ad_library_url: Any Meta Ad Library URL (keyword, page, or single ad)
        max_videos: Max number of video ads to analyze (default 5)

    Returns:
        List of dicts, each containing: ad_metadata, gemini_analysis, brief
    """

    # --- SCRAPE ---
    print("Step 1: Scraping Ad Library...")
    run = apify_client.actor('JHGi3kAzHO1t3Fxrb').call(run_input={
        'targetUrl': ad_library_url,
        'maxConcurrency': 3
    })
    items = list(apify_client.dataset(run['defaultDatasetId']).iterate_items())
    video_ads = [item for item in items if item.get('videos') and len(item['videos']) > 0]
    print(f"  Found {len(video_ads)} video ads (of {len(items)} total)")

    results = []
    os.makedirs('/sessions/dazzling-tender-pascal/videos', exist_ok=True)

    for i, ad in enumerate(video_ads[:max_videos]):
        library_id = ad.get('libraryID', f'unknown_{i}')
        print(f"\n{'='*60}")
        print(f"Processing ad #{i+1}: {library_id}")

        # --- DOWNLOAD ---
        print("Step 2: Downloading video...")
        vid = ad['videos'][0]
        url = vid['url'] if isinstance(vid, dict) else vid
        filename = f'/sessions/dazzling-tender-pascal/videos/ad_{library_id}.mp4'

        subprocess.run(
            ['wget', '-q', '-O', filename, '--timeout=30', url],
            capture_output=True, text=True, timeout=60
        )

        if not (os.path.exists(filename) and os.path.getsize(filename) > 10000):
            print("  Download failed, skipping...")
            continue

        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"  Downloaded: {size_mb:.1f}MB")

        # --- GEMINI ANALYSIS ---
        print("Step 3: Uploading to Gemini for frame-by-frame analysis...")
        uploaded = gemini_client.files.upload(file=filename)
        while uploaded.state.name == 'PROCESSING':
            time.sleep(5)
            uploaded = gemini_client.files.get(name=uploaded.name)

        analysis_response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[uploaded, GEMINI_ANALYSIS_PROMPT]
        )
        gemini_analysis = analysis_response.text
        print(f"  Gemini analysis complete ({len(gemini_analysis)} chars)")

        # --- GENERATE BRIEF ---
        print("Step 4: Generating video editor brief...")
        brief_prompt = BRIEF_GENERATION_PROMPT.format(
            gemini_analysis=gemini_analysis,
            brand=ad.get('brand', 'Unknown'),
            library_id=library_id,
            start_date=ad.get('startDate', 'N/A'),
            body=(ad.get('body') or '')[:2000],
            cta=ad.get('ctaText', 'N/A')
        )

        brief_response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[brief_prompt]
        )
        brief = brief_response.text
        print(f"  Brief generated ({len(brief)} chars)")

        results.append({
            'library_id': library_id,
            'brand': ad.get('brand', 'Unknown'),
            'body': ad.get('body', ''),
            'start_date': ad.get('startDate', 'N/A'),
            'video_file': filename,
            'gemini_analysis': gemini_analysis,
            'brief': brief
        })

    return results
```

---

## How to Use in Practice

When the user pastes a link, execute the pipeline like this:

```python
# User pastes: https://www.facebook.com/ads/library/?id=4093398267656797
url = "https://www.facebook.com/ads/library/?id=4093398267656797"
results = run_pipeline(url, max_videos=1)  # Single ad = 1 video

# For keyword/page searches, analyze top 5:
# results = run_pipeline(url, max_videos=5)

# Output the results
for r in results:
    print(f"\n{'='*80}")
    print(f"AD: {r['library_id']} | Brand: {r['brand']}")
    print(f"\n--- GEMINI ANALYSIS ---")
    print(r['gemini_analysis'][:500] + "...")
    print(f"\n--- VIDEO EDITOR BRIEF ---")
    print(r['brief'])
```

---

## Output Format

After running the pipeline, present the user with:

1. **Ad metadata** (brand, library ID, start date, primary text preview)
2. **Gemini visual analysis** (the full frame-by-frame breakdown)
3. **Video editor brief** (production-ready, follows brief-template.md structure)

Save each brief to the workspace folder as a markdown file so the user can access it:
```python
output_path = f"/sessions/dazzling-tender-pascal/mnt/video ads obsidian/brief_{library_id}.md"
with open(output_path, 'w') as f:
    f.write(brief)
```

---

## Notes

- **Rate limits**: Gemini processes one video at a time. For 5 videos, expect ~5-10 minutes total
- **Video size**: Most Meta Ad Library videos are 1-15MB. Gemini handles up to 2GB
- **Apify costs**: The meta-ad-scraper actor charges per run. A single keyword search typically costs $0.01-0.05
- **Error handling**: If a video fails to download (Facebook CDN issues), skip it and try the next one
- **Single ad vs. search**: For single ad URLs (`?id=XXXXX`), set `max_videos=1`. For keyword/page searches, default to `max_videos=5`
