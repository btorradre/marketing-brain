#!/usr/bin/env python3
"""
Send all winning video ads to Gemini for creative type analysis.
Classifies each video into creative types, analyzes scene structure,
identifies DR + viral organic principles at work.
"""
import json, os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from pathlib import Path
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "[REDACTED_SECRET]")
MODEL = "gemini-2.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY)

VIDEO_DIR = os.path.expanduser("~/Documents/marketing brain/gethookd-research/videos")
OUTPUT_DIR = os.path.expanduser("~/Documents/marketing brain/gethookd-research/analysis")
os.makedirs(OUTPUT_DIR, exist_ok=True)

ANALYSIS_PROMPT = """You are an expert direct response creative strategist analyzing winning Facebook/Meta video ads.

Analyze this video ad and provide a detailed JSON response with the following structure:

{
  "creative_type": "one of: talking_head_ugc | ai_ugc | animated_3d | claymation | motion_graphics | product_demo | slideshow | mixed_format | podcast_clip | car_yapper | doctor_talking_head | testimonial_compilation | other",
  "creative_type_confidence": 0.0-1.0,
  "sub_types": ["list of sub-types if mixed, e.g. 'talking_head_with_broll', 'animated_with_text_overlays'"],
  
  "scene_breakdown": [
    {
      "scene_number": 1,
      "timestamp_start": "0:00",
      "timestamp_end": "0:05",
      "scene_type": "one of: hook_visual | talking_head | broll_action | broll_science | broll_product | text_overlay | before_after | statistical_diagram | research_screenshot | animated_sequence | product_shot | testimonial | cta",
      "description": "what's happening visually",
      "audio_type": "one of: voiceover | on_camera_speech | music_only | sound_effects | silence",
      "text_on_screen": "any text overlays visible",
      "motion_type": "one of: static | slow_pan | zoom_in | zoom_out | fast_cut | smooth_transition | animated"
    }
  ],
  
  "visual_style": {
    "overall_aesthetic": "description of the visual style",
    "color_palette": "dominant colors",
    "production_quality": "one of: raw_ugc | polished_ugc | semi_professional | professional | high_end_animation",
    "aspect_ratio": "9:16 | 1:1 | 16:9 | 4:5",
    "text_overlay_style": "description of how text is used",
    "is_ai_generated": true/false,
    "ai_generation_tells": ["list of signs it's AI-generated, if any"]
  },
  
  "dr_elements": {
    "hook_type": "what kind of hook opens the ad",
    "hook_text": "the actual opening text/speech",
    "problem_agitation": "how the problem is presented",
    "mechanism_education": "how the solution mechanism is explained",
    "social_proof_type": "how social proof is shown",
    "cta_type": "what call to action is used",
    "urgency_scarcity": "any urgency/scarcity elements",
    "belief_shifts": ["list of belief shifts attempted"]
  },
  
  "viral_organic_elements": {
    "native_feel": 0.0-1.0,
    "scroll_stopping_technique": "what makes someone stop scrolling",
    "curiosity_gap": "how curiosity is created",
    "pattern_interrupt": "any pattern interrupts used",
    "emotional_triggers": ["list of emotions targeted"],
    "storytelling_arc": "how the story unfolds"
  },
  
  "broll_segments": [
    {
      "timestamp": "start-end",
      "type": "action_lifestyle | product_shot | science_mechanism | text_graphic | nature_abstract | testimonial_social | before_after | animated_sequence | statistical_diagram | research_screenshot",
      "description": "what the broll shows",
      "could_be_replicated_with": "AI tool or method to replicate this (e.g. 'Kling 3.0 animation', 'Nano Banana 2 image-to-image', 'Veo 3.1 text-to-video', 'stock footage', 'manual product shot')"
    }
  ],
  
  "duration_seconds": total video duration,
  "estimated_cpm_tier": "low | medium | high",
  "key_takeaway": "the single most important lesson from this ad for replication"
}

Be thorough and specific. Focus on what makes this ad a WINNER — it has the highest performance score on the platform."""

def analyze_video(video_path, video_metadata):
    """Upload video to Gemini and analyze it."""
    filename = os.path.basename(video_path)
    analysis_path = os.path.join(OUTPUT_DIR, filename.replace(".mp4", "_analysis.json"))
    
    # Skip if already analyzed
    if os.path.exists(analysis_path):
        print(f"  SKIP (already analyzed): {filename}")
        with open(analysis_path) as f:
            return json.load(f)
    
    file_size = os.path.getsize(video_path) / 1024 / 1024
    print(f"  Uploading {filename} ({file_size:.1f}MB)...")
    
    try:
        # Upload file
        uploaded = client.files.upload(file=video_path)
        
        # Wait for processing
        while uploaded.state == "PROCESSING":
            time.sleep(2)
            uploaded = client.files.get(name=uploaded.name)
        
        if uploaded.state != "ACTIVE":
            print(f"  ERROR: File state = {uploaded.state}")
            return None
        
        print(f"  Analyzing...")
        
        # Add context about the ad
        context = f"""
Ad metadata:
- Brand: {video_metadata.get('brand', 'Unknown')}
- Title: {video_metadata.get('title', 'Unknown')}
- Performance Score: {video_metadata.get('score', 'Unknown')} (Winning = highest tier)
- Days Active: {video_metadata.get('days_active', 'Unknown')}
- Duration: {video_metadata.get('duration', 'Unknown')}s
"""
        
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_uri(file_uri=uploaded.uri, mime_type="video/mp4"),
                context + "\n" + ANALYSIS_PROMPT,
            ],
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=65000,
                response_mime_type="application/json",
            ),
        )

        # Parse JSON from response
        text = response.text
        # Extract JSON from markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        # Try to repair truncated JSON
        try:
            analysis = json.loads(text)
        except json.JSONDecodeError:
            # Try to fix common truncation issues
            import re
            # Remove trailing incomplete entries and close brackets
            text = text.rstrip()
            # Try progressively removing the last incomplete part
            for _ in range(10):
                try:
                    analysis = json.loads(text)
                    break
                except json.JSONDecodeError:
                    # Remove last incomplete array/object element
                    text = re.sub(r',\s*[{\["]?[^}\]]*$', '', text, flags=re.DOTALL)
                    # Close any open brackets
                    opens = text.count('{') - text.count('}')
                    text += '}' * max(0, opens)
                    opens = text.count('[') - text.count(']')
                    text += ']' * max(0, opens)
            else:
                raise
        analysis["_metadata"] = video_metadata
        analysis["_filename"] = filename
        
        # Save individual analysis
        with open(analysis_path, "w") as f:
            json.dump(analysis, f, indent=2)
        
        print(f"  ✓ {analysis.get('creative_type', 'unknown')} | {len(analysis.get('scene_breakdown', []))} scenes")
        
        # Clean up uploaded file
        try:
            client.files.delete(name=uploaded.name)
        except:
            pass
        
        return analysis
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def main():
    # Load video metadata
    meta_path = os.path.expanduser("~/Documents/marketing brain/gethookd-research/unique_winning_videos.json")
    with open(meta_path) as f:
        videos_meta = json.load(f)
    
    # Build metadata lookup by ad_id
    meta_lookup = {}
    for v in videos_meta:
        brand = v["brand"].replace(" ", "_").lower()
        filename = f"{brand}_{v['ad_id']}.mp4"
        meta_lookup[filename] = v
    
    # Get all video files, sorted by size (smallest first for faster initial results)
    video_files = sorted(
        [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")],
        key=lambda f: os.path.getsize(os.path.join(VIDEO_DIR, f))
    )
    print(f"Found {len(video_files)} video files to analyze")
    
    all_analyses = []
    for i, vf in enumerate(video_files, 1):
        video_path = os.path.join(VIDEO_DIR, vf)
        meta = meta_lookup.get(vf, {"brand": "Unknown", "ad_id": vf})
        
        print(f"\n[{i}/{len(video_files)}] {vf}")
        analysis = analyze_video(video_path, meta)
        if analysis:
            all_analyses.append(analysis)
        
        time.sleep(1)  # Rate limit
    
    # Save master analysis file
    master_path = os.path.join(OUTPUT_DIR, "all_analyses.json")
    with open(master_path, "w") as f:
        json.dump(all_analyses, f, indent=2)
    
    # Generate summary
    from collections import Counter
    type_counts = Counter(a.get("creative_type") for a in all_analyses)
    scene_type_counts = Counter()
    broll_type_counts = Counter()
    for a in all_analyses:
        for s in a.get("scene_breakdown", []):
            scene_type_counts[s.get("scene_type")] += 1
        for b in a.get("broll_segments", []):
            broll_type_counts[b.get("type")] += 1
    
    summary = {
        "total_analyzed": len(all_analyses),
        "creative_type_distribution": dict(type_counts.most_common()),
        "scene_type_distribution": dict(scene_type_counts.most_common(20)),
        "broll_type_distribution": dict(broll_type_counts.most_common(20)),
    }
    
    summary_path = os.path.join(OUTPUT_DIR, "analysis_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Analyzed: {len(all_analyses)}/{len(video_files)} videos")
    print(f"\nCreative Types:")
    for ct, count in type_counts.most_common():
        print(f"  {ct}: {count}")
    print(f"\nTop Scene Types:")
    for st, count in scene_type_counts.most_common(10):
        print(f"  {st}: {count}")
    print(f"\nTop B-Roll Types:")
    for bt, count in broll_type_counts.most_common(10):
        print(f"  {bt}: {count}")
    print(f"\nFiles saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
