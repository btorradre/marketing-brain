#!/usr/bin/env python3
"""
Gemini B-Roll Match Gate
========================
Visually analyzes EVERY downloaded TikTok candidate against the exact script
line / emotional beat it was sourced for. Nothing reaches the editor without
passing this gate.

For each candidate in <job>/candidates/<slot_id>/:
  1. Upload the video to Gemini
  2. Ask for a structured verdict against the slot spec (script line, emotion,
     action, brand context)
  3. Verdict → verdicts.json; passing clips get their best segment trimmed via
     ffmpeg into <job>/matched/<slot_id>/rankNN_<id>.mp4
  4. Human-readable sourcing report → <job>/match_report.md

Usage:
  venv/bin/python analyze.py --plan sourcing_plan.json --output ./job-dir
  venv/bin/python analyze.py --plan plan.json --output ./job --slot S02   # one slot
  venv/bin/python analyze.py ... --threshold 70 --keep-flagged
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

VAULT_ENV = os.path.expanduser("~/Documents/marketing brain/.env")


def load_env_file(path):
    if not os.path.exists(path):
        return
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


load_env_file(VAULT_ENV)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_VIDEO_MODEL", "gemini-3-flash-preview")
DEFAULT_HARD_FLAGS = {"TALKING_TO_CAMERA", "BURNED_CAPTIONS", "WATERMARK", "COMPETITOR_PRODUCT"}

try:
    from google import genai
except ImportError:
    print("[!] Missing google-genai in this venv")
    sys.exit(1)


VERDICT_PROMPT = """You are a B-roll sourcing QA agent for direct-response video ads.

We need footage for this exact moment in an ad script:

SCRIPT LINE: {script_line}
EMOTION REQUIRED ON SCREEN: {emotion}
ACTION / VISUAL REQUIRED: {action}
BRAND / PRODUCT CONTEXT: {brand_context}
NEEDED CLIP LENGTH: at least {duration_needs_s} seconds of continuously usable footage
ADDITIONAL SOURCING NOTES (these override the default judging rules where they
conflict): {notes}

Watch this TikTok video carefully, moment by moment. Decide whether ANY
continuous segment of it works as B-roll under a voiceover saying the script
line above. The footage must SHOW the emotion and action — the viewer will
never hear the TikTok's own audio.

A video that is MOSTLY talking-to-camera can still be a match: many usable
moments live inside longer talking videos (the creator pauses to demonstrate —
injects the pen, pinches their stomach, pours the powder). Mine the whole
timeline for that moment. What matters is that the BEST SEGMENT itself is
clean: the required action fills the frame, the subject is not visibly
speaking to camera during it, and no burned-in text sits over it.

THE VISUAL SUBJECT TEST — this is the decisive test. Imagine the best segment
muted, with no captions, shown to a stranger with zero context. The stranger
must be able to say "I am literally looking at [the required action] right
now." If they would instead say "I'm looking at a person talking", "a face",
"someone reacting", or "something related to the topic", it is NOT a match —
no matter how on-topic the video is. Footage ABOUT the subject is worthless;
only footage OF the required action counts.

Automatic non-matches (match=false, confidence under 20):
- A talking head discussing the topic with NO segment anywhere in the video
  where the required action is performed on screen.
- A face filling the frame while the required action happens off-screen or
  not at all.
- Someone HOLDING or DISPLAYING an object to the camera when the spec asks for
  an action performed WITH the object.
- Comedy skits, POV memes, and performed reactions about the topic.

Judge strictly:
- The required action must be physically visible and prominent in frame for at
  least the needed clip length. Confidence = how literally and prominently the
  required action fills the screen (100 = the action IS the frame).
- The emotion on screen must match the required emotion (not just the topic).
- When match is true, best_segment is REQUIRED and must be the exact
  timestamps where the action is on screen.
- Flag anything that makes a clip unusable in a paid ad.

Return ONLY valid JSON (no markdown fences):
{{
  "match": true or false,
  "confidence": 0-100,
  "best_segment": {{"start": "MM:SS", "end": "MM:SS"}},
  "alt_segments": [{{"start": "MM:SS", "end": "MM:SS"}}],
  "emotion_read": "the emotion actually visible on screen",
  "action_read": "what is actually happening on screen",
  "flags": [],
  "why": "one or two sentences on the verdict"
}}

Allowed flags: TALKING_TO_CAMERA (subject visibly speaking to camera DURING
the best segment — do not flag talking elsewhere in the video),
BURNED_CAPTIONS (text/captions burned into the frame DURING the best segment —
do not flag text elsewhere in the video), WATERMARK (TikTok or other watermark
visible in the best segment), COMPETITOR_PRODUCT (a visible
brand/product that isn't ours), LOW_QUALITY (blurry, dark, shaky),
AI_GENERATED (footage looks AI-generated), VERTICAL_CROP_RISK (key action at
frame edges), MINOR_ON_SCREEN (child prominently featured).
"""


def ts_to_seconds(ts):
    parts = str(ts).split(":")
    try:
        parts = [float(p) for p in parts]
    except ValueError:
        return 0.0
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]


def parse_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        raise ValueError("no JSON object in response")
    return json.loads(m.group(0))


def analyze_one(client, video_path, slot, retries=2):
    prompt = VERDICT_PROMPT.format(
        script_line=slot.get("script_line", ""),
        emotion=slot.get("emotion", ""),
        action=slot.get("action", ""),
        brand_context=slot.get("brand_context", slot.get("brand", "")),
        duration_needs_s=slot.get("duration_needs_s", 3),
        notes=slot.get("notes", "none"),
    )
    last_err = None
    for attempt in range(retries + 1):
        try:
            vfile = client.files.upload(file=video_path)
            while vfile.state.name == "PROCESSING":
                time.sleep(4)
                vfile = client.files.get(name=vfile.name)
            if vfile.state.name != "ACTIVE":
                raise RuntimeError(f"file state {vfile.state.name}")
            resp = client.models.generate_content(model=GEMINI_MODEL, contents=[vfile, prompt])
            verdict = parse_json(resp.text)
            try:
                client.files.delete(name=vfile.name)
            except Exception:
                pass
            return verdict
        except Exception as e:
            last_err = e
            time.sleep(8 * (attempt + 1))
    return {"match": False, "confidence": 0, "flags": ["ANALYSIS_ERROR"],
            "why": f"analysis failed: {type(last_err).__name__}: {last_err}"}


def trim_segment(src, dst, start_s, end_s, pad=0.25):
    start = max(0, start_s - pad)
    dur = max(1.0, (end_s - start_s) + 2 * pad)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.2f}", "-i", src,
           "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
           "-an", dst]
    r = subprocess.run(cmd, capture_output=True)
    return r.returncode == 0 and os.path.exists(dst)


def load_meta(job_dir):
    meta = {}
    p = Path(job_dir) / "candidates_meta.jsonl"
    if p.exists():
        for line in p.read_text().splitlines():
            try:
                rec = json.loads(line)
                meta[rec["video_id"]] = rec
            except Exception:
                pass
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--output", required=True, help="job dir (same as crawl.py --output)")
    ap.add_argument("--slot", help="only analyze this slot id")
    ap.add_argument("--threshold", type=int, default=65)
    ap.add_argument("--keep-flagged", action="store_true",
                    help="hard flags demote instead of reject")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-trim", action="store_true", help="copy full clips, don't cut segments")
    ap.add_argument("--pad", type=float, default=0.25, help="seconds of handle around best segment when trimming")
    args = ap.parse_args()

    if not GEMINI_API_KEY:
        print("[!] GEMINI_API_KEY not set")
        sys.exit(1)
    client = genai.Client(api_key=GEMINI_API_KEY)

    plan = json.loads(Path(args.plan).read_text())
    hard_flags = set(plan["hard_flags"]) if "hard_flags" in plan else DEFAULT_HARD_FLAGS
    job = Path(args.output)

    # Clips killed by Claude's frame audit — one "slot/video_id" per line.
    # These are permanent: a re-gate must never re-export them.
    rej_path = job / "audit_rejects.txt"
    audit_rejects = set()
    if rej_path.exists():
        audit_rejects = {ln.strip() for ln in rej_path.read_text().splitlines()
                         if ln.strip() and not ln.startswith("#")}
    meta = load_meta(job)
    verdicts_path = job / "verdicts.json"
    verdicts = json.loads(verdicts_path.read_text()) if verdicts_path.exists() else {}

    slots = [s for s in plan["slots"] if not args.slot or s["slot_id"] == args.slot]
    brand_context = plan.get("brand_context", plan.get("brand", ""))

    for slot in slots:
        sid = slot["slot_id"]
        slot.setdefault("brand_context", brand_context)
        cand_dir = job / "candidates" / sid
        vids = sorted(cand_dir.glob("*.mp4")) if cand_dir.exists() else []
        todo = [v for v in vids if f"{sid}/{v.stem}" not in verdicts]
        print(f"\n== Slot {sid}: {len(vids)} candidates ({len(todo)} to analyze)")

        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(analyze_one, client, str(v), slot): v for v in todo}
            for fut in as_completed(futs):
                v = futs[fut]
                verdict = fut.result()
                verdicts[f"{sid}/{v.stem}"] = verdict
                verdicts_path.write_text(json.dumps(verdicts, indent=2))
                tag = "MATCH" if verdict.get("match") else "no"
                print(f"    {v.stem}: {tag} conf={verdict.get('confidence',0)} "
                      f"flags={verdict.get('flags',[])}")

        # Rank + export matches
        slot_hard = set(slot["hard_flags"]) if "hard_flags" in slot else hard_flags
        scored = []
        for v in vids:
            verdict = verdicts.get(f"{sid}/{v.stem}", {})
            if not verdict.get("match"):
                continue
            conf = int(verdict.get("confidence", 0))
            hard = [f for f in verdict.get("flags", []) if f in slot_hard]
            if hard and not args.keep_flagged:
                continue
            if hard:
                conf -= 25
            if conf < args.threshold:
                continue
            scored.append((conf, v, verdict))
        scored.sort(key=lambda x: -x[0])

        # Permanent audit rejects (Claude's frame audit) never resurface
        scored = [t for t in scored if f"{sid}/{t[1].stem}" not in audit_rejects]

        matched_dir = job / "matched" / sid
        matched_dir.mkdir(parents=True, exist_ok=True)
        # Purge stale exports: re-ranking renames files, so anything not in the
        # new expected set is a leftover duplicate from a previous run.
        expected = {f"rank{r:02d}_c{c}_{v.stem}.mp4"
                    for r, (c, v, _) in enumerate(scored, 1)}
        for old in matched_dir.glob("*.mp4"):
            if old.name not in expected:
                old.unlink()
        for rank, (conf, v, verdict) in enumerate(scored, 1):
            dst = matched_dir / f"rank{rank:02d}_c{conf}_{v.stem}.mp4"
            if dst.exists():
                continue
            seg = verdict.get("best_segment") or {}
            s, e = ts_to_seconds(seg.get("start", 0)), ts_to_seconds(seg.get("end", 0))
            if args.no_trim or e <= s:
                shutil.copy(v, dst)
            elif not trim_segment(str(v), str(dst), s, e, pad=args.pad):
                shutil.copy(v, dst)
        print(f"    -> {len(scored)} matched clips in {matched_dir}")

    # Report
    lines = [f"# TikTok B-Roll Match Report", "",
             f"Job: `{job}`  ·  Model: `{GEMINI_MODEL}`  ·  Threshold: {args.threshold}", ""]
    for slot in slots:
        sid = slot["slot_id"]
        lines += [f"## {sid} — \"{slot.get('script_line','')}\"",
                  f"- Emotion: {slot.get('emotion','')}",
                  f"- Action: {slot.get('action','')}", ""]
        cand_dir = job / "candidates" / sid
        vids = sorted(cand_dir.glob("*.mp4")) if cand_dir.exists() else []
        rows = ["| clip | verdict | conf | best segment | flags | why |",
                "|---|---|---|---|---|---|"]
        for v in vids:
            verdict = verdicts.get(f"{sid}/{v.stem}", {})
            seg = verdict.get("best_segment") or {}
            src = (meta.get(v.stem) or {}).get("url", v.stem)
            rows.append(
                f"| [{v.stem}]({src}) | {'MATCH' if verdict.get('match') else 'reject'} "
                f"| {verdict.get('confidence','—')} | {seg.get('start','')}–{seg.get('end','')} "
                f"| {', '.join(verdict.get('flags',[]))} | {verdict.get('why','')} |")
        lines += rows + [""]
    (job / "match_report.md").write_text("\n".join(lines))
    print(f"\nReport: {job / 'match_report.md'}")
    print(f"Verdicts: {verdicts_path}")


if __name__ == "__main__":
    main()
