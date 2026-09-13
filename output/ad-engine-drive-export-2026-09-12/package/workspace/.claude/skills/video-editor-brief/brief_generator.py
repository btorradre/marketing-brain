#!/usr/bin/env python3
"""
Video Editor Brief Generator
==============================
Takes a script + replicator output directory, uses Gemini to match each script
segment to the best-fitting scene, and produces a comprehensive video editor brief.

Usage:
    python3 brief_generator.py \
        --script "/path/to/script.txt" \
        --replicator-dir "./replicator-output" \
        --brand "Motilli" \
        --title "GLP-1 Claymation Ad" \
        --drive-folder "FOLDER_ID" \
        --output "./editor-brief.md"

    # Or inline script:
    python3 brief_generator.py \
        --script-text "Line 1 of script here..." \
        --replicator-dir "./replicator-output" \
        --brand "Motilli"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[!] Missing google-genai. Run: pip install google-genai")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config (reuses replicator's keys)
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "[REDACTED_SECRET]")
GEMINI_MODEL = "gemini-3-flash-preview"

# Google Drive OAuth2 (reuses replicator's token)
GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser("~/.claude/skills/video-scene-replicator/gdrive_token.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(stage, msg):
    print(f"[{stage}] {msg}")


def load_json(path):
    """Load a JSON file, return empty list if missing."""
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def scan_files(directory, extension):
    """Scan a directory for files with a given extension, return sorted list."""
    if not os.path.isdir(directory):
        return []
    return sorted([
        f for f in os.listdir(directory)
        if f.lower().endswith(extension)
    ])


# ---------------------------------------------------------------------------
# Stage 1: Load Replicator Output
# ---------------------------------------------------------------------------

def load_replicator_output(replicator_dir):
    """Load all outputs from a previous video-scene-replicator run."""
    log("Load", f"Reading replicator output from: {replicator_dir}")

    # Scene analysis
    analysis_path = os.path.join(replicator_dir, "analysis", "scene_analysis.json")
    analyses = load_json(analysis_path)
    log("Load", f"Scene analyses: {len(analyses)}")

    # Image prompts
    prompts_path = os.path.join(replicator_dir, "prompts", "image_prompts.json")
    prompts = load_json(prompts_path)
    log("Load", f"Image prompts: {len(prompts)}")

    # Animated clips inventory
    anim_dir = os.path.join(replicator_dir, "animated")
    animated_files = scan_files(anim_dir, ".mp4")
    log("Load", f"Animated clips: {len(animated_files)}")

    # Generated stills inventory
    gen_dir = os.path.join(replicator_dir, "generated")
    generated_files = scan_files(gen_dir, ".png")
    log("Load", f"Generated stills: {len(generated_files)}")

    # Reference keyframes
    scenes_dir = os.path.join(replicator_dir, "scenes")
    keyframe_files = scan_files(scenes_dir, ".png")
    log("Load", f"Reference keyframes: {len(keyframe_files)}")

    # Build a unified scene inventory
    scenes = []
    for i, analysis in enumerate(analyses):
        scene_num = analysis.get("scene_number", i + 1)
        num_str = f"{scene_num:03d}"

        scene = {
            "scene_number": scene_num,
            "analysis": analysis,
            "prompt": prompts[i] if i < len(prompts) else {},
            "animated_file": f"scene_{num_str}_animated.mp4" if f"scene_{num_str}_animated.mp4" in animated_files else None,
            "generated_file": f"scene_{num_str}_brand.png" if f"scene_{num_str}_brand.png" in generated_files else None,
            "keyframe_file": f"scene_{num_str}.png" if f"scene_{num_str}.png" in keyframe_files else None,
        }
        scenes.append(scene)

    log("Load", f"Total scenes assembled: {len(scenes)}")
    return scenes


# ---------------------------------------------------------------------------
# Stage 2: Parse Script
# ---------------------------------------------------------------------------

def parse_script(script_text):
    """Parse a script into logical segments.
    Splits on double newlines, scene markers, or numbered lines."""
    # Clean up
    script_text = script_text.strip()

    # Try splitting by scene markers first (e.g., [SCENE 1], SCENE:, etc.)
    scene_pattern = r'(?:^|\n)\s*(?:\[?SCENE\s*\d*\]?|SHOT\s*\d*|CUT\s+TO|---+)\s*'
    if re.search(scene_pattern, script_text, re.IGNORECASE):
        segments = re.split(scene_pattern, script_text, flags=re.IGNORECASE)
        segments = [s.strip() for s in segments if s.strip()]
        if len(segments) > 1:
            return segments

    # Try splitting by double newlines
    segments = [s.strip() for s in script_text.split("\n\n") if s.strip()]
    if len(segments) > 1:
        return segments

    # Try splitting by single newlines (each line is a segment)
    segments = [s.strip() for s in script_text.split("\n") if s.strip()]
    return segments


# ---------------------------------------------------------------------------
# Stage 3: Match Script Segments → Scenes via Gemini
# ---------------------------------------------------------------------------

def match_script_to_scenes(script_segments, scenes, brand, title):
    """Use Gemini to intelligently match script segments to scenes."""
    client = genai.Client(api_key=GEMINI_API_KEY)

    log("Match", f"Matching {len(script_segments)} script segments to {len(scenes)} scenes...")

    # Build scene summaries for Gemini
    scene_summaries = []
    for s in scenes:
        a = s["analysis"]
        scene_summaries.append({
            "scene_number": s["scene_number"],
            "description": a.get("description", ""),
            "composition": a.get("composition", ""),
            "style": a.get("style", ""),
            "motion": a.get("motion", ""),
            "mood": a.get("mood", ""),
            "key_elements": a.get("key_elements", []),
            "text_overlays": a.get("text_overlays", ""),
            "duration": a.get("duration", 0),
            "timestamp": a.get("timestamp", 0),
            "has_animated_clip": s["animated_file"] is not None,
        })

    # Build numbered script segments
    numbered_segments = []
    for i, seg in enumerate(script_segments):
        numbered_segments.append(f"SEGMENT {i+1}: {seg}")

    prompt = f"""You are a video editor's assistant creating a production brief.

BRAND: {brand}
VIDEO TITLE: {title}

SCRIPT SEGMENTS (in order):
{chr(10).join(numbered_segments)}

AVAILABLE SCENES (from reference video, with brand-adapted B-roll already generated):
{json.dumps(scene_summaries, indent=2)}

YOUR TASK:
Match each script segment to the best-fitting scene from the available scenes. Consider:
1. Narrative alignment — does the scene's mood/description match what the script segment is saying?
2. Visual relevance — do the key_elements match what the script describes?
3. Pacing — maintain the flow of the video. The script goes in order; scenes should generally follow the reference timeline.
4. If a script segment is a hook/opening line, match it to an attention-grabbing scene.
5. If a script segment mentions the product, match it to a scene that has the product in key_elements.
6. A scene CAN be reused for multiple segments if needed, but prefer 1:1 matches.
7. If there are more script segments than scenes, some segments can share a scene (the editor will cut between them).
8. If there are more scenes than segments, note which scenes are unmatched as "extra B-roll".

Return a JSON array where each object has:
{{
  "segment_number": <int>,
  "segment_text": "<the script text>",
  "matched_scene": <int scene_number>,
  "confidence": "high" | "medium" | "low",
  "editor_notes": "<brief direction for the editor on how to use this scene with this script line>"
}}

Also add a final object with "unmatched_scenes" listing any scene numbers not used.

Return ONLY the JSON array, no markdown fences."""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        text = response.text.strip()
        # Clean markdown fences
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        matches = json.loads(text)
        log("Match", f"Gemini returned {len(matches)} matches")
        return matches

    except Exception as e:
        log("Match", f"ERROR: Gemini matching failed: {e}")
        # Fallback: sequential 1:1 matching
        log("Match", "Falling back to sequential matching...")
        matches = []
        for i, seg in enumerate(script_segments):
            scene_idx = min(i, len(scenes) - 1)
            matches.append({
                "segment_number": i + 1,
                "segment_text": seg,
                "matched_scene": scenes[scene_idx]["scene_number"],
                "confidence": "low",
                "editor_notes": "Auto-matched sequentially (Gemini unavailable)"
            })
        return matches


# ---------------------------------------------------------------------------
# Stage 4: Generate the Brief
# ---------------------------------------------------------------------------

def generate_brief(matches, scenes, script_segments, brand, title, replicator_dir):
    """Generate the full video editor brief as markdown."""
    log("Brief", "Generating editor brief...")

    # Build scene lookup
    scene_map = {s["scene_number"]: s for s in scenes}

    # Calculate total duration
    total_duration = sum(s["analysis"].get("duration", 0) for s in scenes)

    date_str = datetime.now().strftime("%Y-%m-%d")

    lines = []

    # --- Header ---
    lines.append(f"# Video Editor Brief — {brand} {title}")
    lines.append(f"**Brand:** {brand} | **Date:** {date_str} | **Scenes:** {len(scenes)} | **Script Segments:** {len(script_segments)} | **Est. Duration:** ~{total_duration:.0f}s")
    lines.append("")
    lines.append(f"**Replicator Output:** `{os.path.abspath(replicator_dir)}`")
    lines.append("")

    # --- Timeline Table ---
    lines.append("## Timeline")
    lines.append("")
    lines.append("| # | Time | Dur | Script | B-Roll | Still | Confidence |")
    lines.append("|---|------|-----|--------|--------|-------|------------|")

    # Filter out the unmatched_scenes entry
    segment_matches = [m for m in matches if "segment_number" in m]
    unmatched_entry = next((m for m in matches if "unmatched_scenes" in m), None)

    for m in segment_matches:
        seg_num = m["segment_number"]
        scene_num = m.get("matched_scene", 0)
        scene = scene_map.get(scene_num, {})
        analysis = scene.get("analysis", {})

        ts = f"{analysis.get('timestamp', 0):.1f}s"
        dur = f"{analysis.get('duration', 0):.1f}s"
        script_preview = m.get("segment_text", "")[:60]
        if len(m.get("segment_text", "")) > 60:
            script_preview += "..."
        broll = scene.get("animated_file", "—") or "—"
        still = scene.get("generated_file", "—") or "—"
        conf = m.get("confidence", "—")

        lines.append(f"| {seg_num} | {ts} | {dur} | {script_preview} | {broll} | {still} | {conf} |")

    lines.append("")

    # --- Scene-by-Scene Direction ---
    lines.append("## Scene-by-Scene Direction")
    lines.append("")

    for m in segment_matches:
        seg_num = m["segment_number"]
        scene_num = m.get("matched_scene", 0)
        scene = scene_map.get(scene_num, {})
        analysis = scene.get("analysis", {})

        ts = analysis.get("timestamp", 0)
        dur = analysis.get("duration", 0)

        lines.append(f"### Segment {seg_num} → Scene {scene_num} — {ts:.1f}s ({dur:.1f}s)")
        lines.append(f"**Script:** \"{m.get('segment_text', '')}\"")
        lines.append(f"**Visual:** {analysis.get('description', 'N/A')}")
        lines.append(f"**Composition:** {analysis.get('composition', 'N/A')}")
        lines.append(f"**Motion:** {analysis.get('motion', 'N/A')}")
        lines.append(f"**Mood:** {analysis.get('mood', 'N/A')}")
        lines.append(f"**Style:** {analysis.get('style', 'N/A')}")

        if analysis.get("text_overlays") and analysis["text_overlays"] != "None":
            lines.append(f"**Text Overlays:** {analysis['text_overlays']}")

        lines.append(f"**B-Roll:** `animated/{scene.get('animated_file', 'N/A')}`")
        lines.append(f"**Still:** `generated/{scene.get('generated_file', 'N/A')}`")
        lines.append(f"**Editor Notes:** {m.get('editor_notes', 'N/A')}")
        lines.append(f"**Match Confidence:** {m.get('confidence', 'N/A')}")
        lines.append("")

    # --- Unmatched Scenes (Extra B-Roll) ---
    if unmatched_entry and unmatched_entry.get("unmatched_scenes"):
        lines.append("## Extra B-Roll (Unmatched Scenes)")
        lines.append("")
        lines.append("These scenes from the reference were not matched to any script segment. The editor can use them as cutaways, transitions, or filler.")
        lines.append("")

        for scene_num in unmatched_entry["unmatched_scenes"]:
            scene = scene_map.get(scene_num, {})
            analysis = scene.get("analysis", {})
            lines.append(f"- **Scene {scene_num}** ({analysis.get('timestamp', 0):.1f}s, {analysis.get('duration', 0):.1f}s): {analysis.get('description', 'N/A')} | `animated/{scene.get('animated_file', 'N/A')}`")

        lines.append("")

    # --- Pacing Notes ---
    lines.append("## Pacing Guide")
    lines.append("")
    lines.append(f"- **Total estimated duration:** ~{total_duration:.0f}s")
    lines.append(f"- **Number of scenes:** {len(scenes)}")
    lines.append(f"- **Number of script segments:** {len(script_segments)}")
    avg_dur = total_duration / max(len(scenes), 1)
    lines.append(f"- **Average scene duration:** ~{avg_dur:.1f}s")
    lines.append("")
    if avg_dur < 2:
        lines.append("*Fast-paced edit — quick cuts, high energy. Keep transitions tight.*")
    elif avg_dur < 4:
        lines.append("*Medium pace — standard ad pacing. Allow moments to breathe between cuts.*")
    else:
        lines.append("*Slower pace — let scenes develop. Use smooth transitions.*")
    lines.append("")

    # --- Asset Manifest ---
    lines.append("## Asset Manifest")
    lines.append("")
    lines.append("### Animated B-Roll Clips")
    anim_dir = os.path.join(replicator_dir, "animated")
    for f in scan_files(anim_dir, ".mp4"):
        lines.append(f"- `animated/{f}`")

    lines.append("")
    lines.append("### Generated Stills (thumbnails / fallback)")
    gen_dir = os.path.join(replicator_dir, "generated")
    for f in scan_files(gen_dir, ".png"):
        lines.append(f"- `generated/{f}`")

    lines.append("")
    lines.append("### Reference Keyframes (from original video)")
    scenes_dir = os.path.join(replicator_dir, "scenes")
    for f in scan_files(scenes_dir, ".png"):
        lines.append(f"- `scenes/{f}`")

    lines.append("")

    # --- Full Script ---
    lines.append("## Full Script")
    lines.append("")
    lines.append("```")
    for i, seg in enumerate(script_segments):
        lines.append(f"[{i+1}] {seg}")
    lines.append("```")
    lines.append("")

    brief_text = "\n".join(lines)
    log("Brief", f"Brief generated: {len(brief_text)} chars, {len(lines)} lines")
    return brief_text


# ---------------------------------------------------------------------------
# Stage 5: Google Drive Upload (optional)
# ---------------------------------------------------------------------------

def upload_brief_to_drive(brief_path, drive_folder_id, brand, title):
    """Upload the brief to Google Drive using the replicator's OAuth2 token."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        log("Drive", "Google Drive packages not installed. Skipping upload.")
        return None

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    creds = None
    if os.path.exists(GDRIVE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GDRIVE_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_config = {
                "installed": {
                    "client_id": GDRIVE_CLIENT_ID,
                    "client_secret": GDRIVE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(GDRIVE_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    filename = os.path.basename(brief_path)
    file_metadata = {"name": filename, "parents": [drive_folder_id]}
    media = MediaFileUpload(brief_path, mimetype="text/markdown", resumable=True)
    uploaded = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    log("Drive", f"Uploaded brief to Drive: {filename} (id: {uploaded.get('id')})")
    return uploaded.get("id")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Video Editor Brief Generator")
    parser.add_argument("--script", default="", help="Path to script file (.txt, .md)")
    parser.add_argument("--script-text", default="", help="Inline script text (alternative to --script)")
    parser.add_argument("--replicator-dir", required=True, help="Path to video-scene-replicator output directory")
    parser.add_argument("--brand", default="", help="Brand name (for header)")
    parser.add_argument("--title", default="Video Ad", help="Video title (for header)")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID to upload brief")
    parser.add_argument("--output", default="", help="Output path for the brief .md file")
    parser.add_argument("--notion", action="store_true", help="Publish brief to Notion after generating")
    parser.add_argument("--notion-page", default="334c96bf-9982-8053-b6b6-f47e5897590b", help="Notion parent page ID for briefs (default: Briefs page)")
    parser.add_argument("--notion-db", default="", help="[DEPRECATED] Use --notion-page instead")
    parser.add_argument("--angle", default="", help="Creative angle (for Notion metadata)")
    parser.add_argument("--format-type", default="", help="Format type: UGC, Claymation, Talking Head, etc. (for Notion metadata)")

    args = parser.parse_args()

    # Load script
    if args.script and os.path.exists(args.script):
        with open(args.script, "r", encoding="utf-8") as f:
            script_text = f.read()
        log("Input", f"Loaded script from: {args.script}")
    elif args.script_text:
        script_text = args.script_text
        log("Input", f"Using inline script ({len(script_text)} chars)")
    else:
        print("ERROR: Provide --script (file path) or --script-text (inline)")
        sys.exit(1)

    # Validate replicator dir
    if not os.path.isdir(args.replicator_dir):
        print(f"ERROR: Replicator directory not found: {args.replicator_dir}")
        sys.exit(1)

    # Default output path
    if not args.output:
        date_str = datetime.now().strftime("%Y-%m-%d")
        brand_slug = args.brand.lower().replace(" ", "-") if args.brand else "brand"
        args.output = os.path.join(args.replicator_dir, f"editor_brief_{brand_slug}_{date_str}.md")

    print("=" * 60)
    print("VIDEO EDITOR BRIEF GENERATOR")
    print("=" * 60)
    print(f"Brand:          {args.brand or '(unspecified)'}")
    print(f"Title:          {args.title}")
    print(f"Replicator Dir: {args.replicator_dir}")
    print(f"Output:         {args.output}")
    print("=" * 60)

    # Stage 1: Load replicator output
    scenes = load_replicator_output(args.replicator_dir)
    if not scenes:
        print("ERROR: No scenes found in replicator output. Run video-scene-replicator first.")
        sys.exit(1)

    # Stage 2: Parse script
    script_segments = parse_script(script_text)
    log("Parse", f"Script split into {len(script_segments)} segments")
    for i, seg in enumerate(script_segments):
        preview = seg[:80] + "..." if len(seg) > 80 else seg
        log("Parse", f"  [{i+1}] {preview}")

    # Stage 3: Match script → scenes
    matches = match_script_to_scenes(script_segments, scenes, args.brand, args.title)

    # Stage 4: Generate brief
    brief_text = generate_brief(
        matches, scenes, script_segments,
        args.brand, args.title, args.replicator_dir
    )

    # Write brief
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(brief_text)
    log("Output", f"Brief saved to: {args.output}")

    # Stage 5: Upload to Drive
    if args.drive_folder:
        upload_brief_to_drive(args.output, args.drive_folder, args.brand, args.title)
    else:
        log("Drive", "No Drive folder specified — skipping upload")

    # Save matches JSON (for Notion publisher and future reference)
    matches_path = os.path.join(args.replicator_dir, "matches.json")
    with open(matches_path, "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=2)
    log("Output", f"Matches saved to: {matches_path}")

    # Stage 6: Publish to Notion (optional)
    notion_url = None
    if args.notion:
        try:
            from notion_brief import publish_to_notion
        except ImportError:
            # Try importing from same directory
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "notion_brief",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "notion_brief.py")
            )
            notion_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(notion_mod)
            publish_to_notion = notion_mod.publish_to_notion

        log("Notion", "Publishing brief to Notion...")
        result = publish_to_notion(
            replicator_dir=args.replicator_dir,
            matches=matches,
            script_segments=script_segments,
            scenes=scenes,
            parent_page_id=args.notion_page,
            brand=args.brand,
            title=args.title,
            angle=args.angle,
            format_type=args.format_type,
            drive_folder_id=args.drive_folder or None,
        )
        if result:
            notion_url = result.get("page_url", "")

    # Summary
    print("\n" + "=" * 60)
    print("BRIEF GENERATED")
    print("=" * 60)
    print(f"Script segments:  {len(script_segments)}")
    print(f"Scenes matched:   {len([m for m in matches if 'segment_number' in m])}")
    print(f"Brief saved to:   {args.output}")
    if notion_url:
        print(f"Notion page:      {notion_url}")
    print("=" * 60)


if __name__ == "__main__":
    main()
