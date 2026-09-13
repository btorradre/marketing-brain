#!/usr/bin/env python3
"""ugc-forge — consistent, correctly-voiced UGC video ads from a single script.

Solves two recurring failures:
  1) visual drift between independently-generated clips  -> FRAME CHAINING
  2) mispronounced generated speech                      -> ElevenLabs + lexicon

Pipeline: parse -> segment(<=8s) -> ElevenLabs TTS (lexicon, measure durations)
-> Veo 3 image-to-video sequentially with frame-chaining (native audio OFF,
conform each clip to its audio) -> lip-sync conform (talking heads) + mux VO
untouched -> concat -> outputs + run manifest.

Keys: GEMINI_API_KEY, ELEVENLABS_API_KEY (env only — never flags, never printed).
"""
import argparse
import os
import pathlib
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _env
import audio_source
import faces
import lexicon as lex
import manifest as mf
import prompts
import segmenter
import tts_elevenlabs as tts
import veo
import video_ops as vops
from lipsync import lipsync_conform
from util import dump_json, load_json, log

FIXED_SEED = 777  # one fixed seed reused on every Veo call (consistency safeguard)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args(argv):
    p = argparse.ArgumentParser(prog="ugc-forge", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_argument_group("inputs")
    src.add_argument("--script", help="raw ad script (.txt) to auto-segment")
    src.add_argument("--manifest", help="pre-segmented input JSON {segments:[{line,visual,talking_head}]}")
    src.add_argument("--avatar", action="append", default=[],
                     help="creator reference still (repeatable -> --variations)")
    src.add_argument("--voice", help="ElevenLabs voice_id to SYNTHESIZE from (omit if uploading audio)")
    src.add_argument("--audio-dir", help="use pre-made VO: one audio file per beat (sorted order)")
    src.add_argument("--voiceover", help="use one full-ad VO file, auto-split on silence into beats")
    src.add_argument("--vo-noise-db", type=int, default=-30, help="silence threshold for --voiceover split")
    src.add_argument("--vo-min-gap", type=float, default=0.35, help="min silence gap (s) for --voiceover split")
    src.add_argument("--lexicon", help="pronunciation lexicon JSON (synthesis only)")
    src.add_argument("--settings", help="optional settings JSON (style anchor overrides etc.)")

    out = p.add_argument_group("output")
    out.add_argument("--out", required=True, help="final MP4 path (9:16 master)")
    out.add_argument("--aspect", default="9:16", help="master aspect (default 9:16)")
    out.add_argument("--also-aspect", action="append", default=[],
                     help="extra aspect output, e.g. 4:5 or 16:9 (repeatable)")

    ctrl = p.add_argument_group("drift control")
    ctrl.add_argument("--reanchor-every", type=int, default=0,
                      help="re-seed from the ORIGINAL reference every N segments (0=never)")
    ctrl.add_argument("--reanchor-on-segment", default="",
                      help="comma list of 0-based indices to force a clean re-anchor")
    ctrl.add_argument("--auto-drift", action="store_true",
                      help="also re-anchor when luma drift from the original ref is detected")

    eng = p.add_argument_group("engine")
    eng.add_argument("--veo-model", default=veo.DEFAULT_MODEL)
    eng.add_argument("--tts-model", default=tts.DEFAULT_MODEL)
    eng.add_argument("--lipsync-backend", default="fal", choices=["fal", "omni", "wav2lip", "none"])
    eng.add_argument("--face-index", type=int, default=None,
                     help="which face to lock if the reference has multiple")

    rer = p.add_argument_group("re-run economy")
    rer.add_argument("--regen", default="",
                     help="comma list of 0-based segment indices to force re-render "
                          "(frame-chain dependents auto-included)")
    rer.add_argument("--run-manifest", help="path to the run manifest (default: <out>.manifest.json)")
    rer.add_argument("--resegment", action="store_true",
                     help="allow segment count to differ from a prior run manifest")
    rer.add_argument("--variations", action="store_true",
                     help="run identical script + identical audio across every --avatar")
    p.add_argument("--plan-only", action="store_true",
                   help="segment + preview prompts/lexicon WITHOUT any API calls (free)")
    return p.parse_args(argv)


def _parse_idx(s):
    return [int(x) for x in s.split(",") if x.strip() != ""]


# --------------------------------------------------------------------------- #
# Pipeline
# --------------------------------------------------------------------------- #
def main(argv):
    args = parse_args(argv)
    _env.load_env()

    out_path = pathlib.Path(args.out).resolve()
    work = out_path.with_suffix("")
    work = work.parent / (work.name + ".ugcforge")
    (work / "audio").mkdir(parents=True, exist_ok=True)
    run_manifest_path = args.run_manifest or str(out_path.with_suffix(".manifest.json"))

    settings = load_json(args.settings) if args.settings else {}
    style = prompts.load_style(settings)
    lexicon = lex.load_lexicon(args.lexicon)
    use_ssml = lex.uses_ssml(lexicon)

    # 1) Segment ------------------------------------------------------------- #
    segments, source = segmenter.load_segments(script_path=args.script, manifest_path=args.manifest)
    n = len(segments)
    log(f"segmented into {n} beats (<=8s each) from {source} input")

    # Free preview path: segmentation + lexicon + prompt plan, NO API calls. #
    if args.plan_only:
        return _write_plan(segments, style, lexicon, args, out_path, run_manifest_path)

    uploaded_audio = bool(args.audio_dir or args.voiceover)
    _env.require("GEMINI_API_KEY")
    if not uploaded_audio:
        _env.require("ELEVENLABS_API_KEY")
        if not args.voice:
            raise SystemExit("[ugc-forge] Provide --voice to synthesize, or upload audio "
                             "with --audio-dir / --voiceover.")
    if args.audio_dir and args.voiceover:
        raise SystemExit("[ugc-forge] Use either --audio-dir or --voiceover, not both.")
    if not args.avatar:
        raise SystemExit("[ugc-forge] At least one --avatar reference image is required.")

    prev = mf.load(run_manifest_path)
    if prev and len(prev.get("segments", [])) != n and not args.resegment:
        raise SystemExit(
            f"[ugc-forge] Segment count changed ({len(prev['segments'])} -> {n}). "
            "Re-run with --resegment to accept the new segmentation (prior video "
            "artifacts may not line up), or restore the original script. Refusing to guess."
        )

    # 2) Audio — synthesize OR use uploaded VO; shared across all avatars ----- #
    audio_dir = work / "audio"
    if args.audio_dir:
        log(f"audio source: uploaded stems from {args.audio_dir}")
        audio_meta = audio_source.from_dir(args.audio_dir, n, str(audio_dir), segments)
    elif args.voiceover:
        log(f"audio source: splitting voiceover {args.voiceover}")
        audio_meta = audio_source.from_voiceover(
            args.voiceover, n, str(audio_dir), segments,
            noise_db=args.vo_noise_db, min_gap=args.vo_min_gap)
    else:
        log("audio source: ElevenLabs synthesis")
        audio_settings_key = mf.sha1_text_key(args.voice, args.tts_model)
        audio_meta = []  # per seg: {path, dur, text_hash, applied}
        for i, seg in enumerate(segments):
            applied = lex.apply_lexicon(seg["line"], lexicon)
            thash = mf.segment_text_hash(seg["line"], applied)
            apath = str(audio_dir / f"seg_{i:03d}.mp3")
            reuse = mf.reusable(prev, i, text_hash=thash, settings_key=audio_settings_key,
                                require_keys=("audio_path",))
            if reuse and os.path.exists(reuse["audio_path"]) and reuse["audio_path"] == apath:
                dur = reuse["audio_duration"]
                log(f"audio seg {i}: reuse ({dur:.2f}s)")
            else:
                dur = tts.synthesize(applied, voice_id=args.voice, out_path=apath,
                                     model_id=args.tts_model, ssml=use_ssml)
            audio_meta.append({"path": apath, "dur": dur, "text_hash": thash, "applied": applied})

    # Guardrail: audio count must equal script count.
    if len(audio_meta) != n:
        raise SystemExit(f"[ugc-forge] Audio/script segment mismatch ({len(audio_meta)} vs {n}). Stopping.")

    # 3) Drift-control anchors ---------------------------------------------- #
    forced = _parse_idx(args.reanchor_on_segment) if args.reanchor_on_segment else []
    anchors = mf.reanchor_indices(n, every=args.reanchor_every, forced=forced)
    log(f"re-anchor segments (seed from original reference): {sorted(anchors)}")

    # Which segments must be (re)rendered for the master avatar.
    forced_regen = set(_parse_idx(args.regen)) if args.regen else set()
    auto_changed = set()
    for i, seg in enumerate(segments):
        vkey = video_key(segments[i], style, args, anchor=(i in anchors))
        reuse = mf.reusable(prev, i, text_hash=audio_meta[i]["text_hash"],
                            settings_key=vkey, require_keys=("final_path",))
        if not reuse:
            auto_changed.add(i)
    regen_set = set(mf.expand_regen_set(forced_regen | auto_changed, n, anchors))
    log(f"segments to render (master): {sorted(regen_set)}; reused: {sorted(set(range(n)) - regen_set)}")

    # 4-6) Video per avatar -------------------------------------------------- #
    variation_avatars = args.avatar if (args.variations or len(args.avatar) > 1) else args.avatar[:1]
    out_manifest = mf.new_manifest(run_settings={
        "aspect": args.aspect, "veo_model": args.veo_model, "tts_model": args.tts_model,
        "lipsync_backend": args.lipsync_backend, "reanchor_every": args.reanchor_every,
        "reanchor_on_segment": forced, "auto_drift": args.auto_drift, "fixed_seed": FIXED_SEED,
        "negative_prompt": veo.NEGATIVE_PROMPT, "voice_id_used": True, "source": source,
    })
    out_manifest["segments"] = [None] * n
    variations_out = []

    for vi, avatar in enumerate(variation_avatars):
        avatar = str(pathlib.Path(avatar).resolve())
        faces.guard_single_face(avatar, face_index=args.face_index)
        is_master = (vi == 0)
        label = pathlib.Path(avatar).stem
        seg_dir = work / f"avatar_{vi:02d}_{label}"
        (seg_dir / "frames").mkdir(parents=True, exist_ok=True)
        log(f"=== avatar {vi} ({label}) {'[master]' if is_master else '[variation]'} ===")

        finished = []           # final per-seg mp4 paths, in order, skips excluded
        last_frame = None       # png path for chaining
        for i, seg in enumerate(segments):
            audio = audio_meta[i]
            final_path = str(seg_dir / f"seg_{i:03d}.mp4")
            last_png = str(seg_dir / "frames" / f"seg_{i:03d}_last.png")

            # Reuse (master only) ----------------------------------------- #
            if is_master and i not in regen_set:
                reuse = mf.reusable(prev, i, text_hash=audio["text_hash"],
                                    settings_key=video_key(seg, style, args, anchor=(i in anchors)),
                                    require_keys=("final_path",))
                if reuse and os.path.exists(reuse["final_path"]):
                    log(f"seg {i}: reuse video {os.path.basename(reuse['final_path'])}")
                    if reuse["final_path"] != final_path:
                        shutil.copyfile(reuse["final_path"], final_path)
                    if reuse.get("last_frame") and os.path.exists(reuse["last_frame"]):
                        if reuse["last_frame"] != last_png:
                            shutil.copyfile(reuse["last_frame"], last_png)
                        last_frame = last_png
                    finished.append(final_path)
                    out_manifest["segments"][i] = {**reuse, "final_path": final_path,
                                                   "last_frame": last_png}
                    continue

            # Choose start frame (frame chaining vs re-anchor) ------------- #
            anchor = i in anchors or last_frame is None
            if not anchor and args.auto_drift and last_frame:
                if vops.drift_detected(avatar, last_frame):
                    anchor = True
            start_frame = avatar if anchor else last_frame
            source_kind = "reference" if start_frame == avatar else "prev_frame"
            if i in anchors and start_frame == avatar and i != 0:
                source_kind = "reanchor"

            prompt = prompts.build_prompt(seg["visual"], style, talking_head=seg["talking_head"])

            # Generate with safety-retry -> rework -> skip ---------------- #
            raw_mp4 = str(seg_dir / f"seg_{i:03d}.raw.mp4")
            gen = _generate_with_recovery(prompt=prompt, start_frame=start_frame,
                                          out_path=raw_mp4, aspect=args.aspect,
                                          model=args.veo_model)
            if gen is None:
                log(f"seg {i}: SKIPPED (safety/empty after retries) — excluded from final")
                out_manifest["segments"][i] = {
                    "index": i, "line": seg["line"], "skipped": True,
                    "reason": "safety_filtered_or_empty", "audio_path": audio["path"],
                    "audio_duration": audio["dur"],
                }
                continue

            # Conform video to audio; lip-sync (talking head) or mux ------ #
            conformed = str(seg_dir / f"seg_{i:03d}.conf.mp4")
            vops.conform_video_to_audio(raw_mp4, audio["dur"], conformed)
            if seg["talking_head"]:
                lipsync_conform(conformed, audio["path"], final_path,
                                backend=args.lipsync_backend)
            else:
                vops.mux_audio(conformed, audio["path"], final_path)

            vops.extract_last_frame(raw_mp4, last_png)
            last_frame = last_png
            finished.append(final_path)

            seg_record = {
                "index": i, "line": seg["line"], "applied_text": audio["applied"],
                "visual": seg["visual"], "talking_head": seg["talking_head"],
                "prompt": prompt, "seed": gen["seed"], "veo_model": gen["model"],
                "start_frame_source": source_kind, "audio_path": audio["path"],
                "audio_duration": audio["dur"], "final_path": final_path,
                "last_frame": last_png, "watermark": gen["watermark"],
                "text_hash": audio["text_hash"],
                "settings_key": video_key(seg, style, args, anchor=(i in anchors)),
            }
            if is_master:
                out_manifest["segments"][i] = seg_record

            for tmp in (raw_mp4, conformed):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

        # Concat this avatar's finished segments ------------------------- #
        avatar_out = out_path if is_master else out_path.with_name(
            f"{out_path.stem}__{label}{out_path.suffix}")
        vops.concat(finished, avatar_out, seg_dir)
        log(f"avatar {vi}: -> {avatar_out}")

        alt_outputs = []
        for asp in args.also_aspect:
            alt = avatar_out.with_name(f"{avatar_out.stem}.{asp.replace(':','x')}{avatar_out.suffix}")
            vops.make_aspect(avatar_out, alt, asp)
            alt_outputs.append({"aspect": asp, "path": str(alt)})
        variations_out.append({"avatar": avatar, "label": label, "output": str(avatar_out),
                               "alt_aspects": alt_outputs, "segments_rendered": len(finished),
                               "master": is_master})

    # 7) Manifest ------------------------------------------------------------ #
    out_manifest["segments"] = [s for s in out_manifest["segments"] if s is not None]
    out_manifest["variations"] = variations_out
    out_manifest["output"] = str(out_path)
    dump_json(out_manifest, run_manifest_path)
    log(f"manifest -> {run_manifest_path}")
    log("done.")


def _generate_with_recovery(*, prompt, start_frame, out_path, aspect, model):
    """Generate a segment; on safety-filter/empty, retry once reworded, then give
    up (return None) so the batch continues rather than crashing."""
    try:
        return veo.generate_segment(prompt=prompt, start_image_path=start_frame,
                                    out_path=out_path, aspect=aspect, seed=FIXED_SEED,
                                    model=model)
    except veo.SafetyFiltered as e:
        log(f"safety/empty: {e}; retrying with reworded prompt")
    try:
        return veo.generate_segment(prompt=veo.rework_prompt(prompt),
                                    start_image_path=start_frame, out_path=out_path,
                                    aspect=aspect, seed=FIXED_SEED, model=model)
    except veo.SafetyFiltered as e:
        log(f"safety/empty again: {e}; skipping segment")
        return None


def _write_plan(segments, style, lexicon, args, out_path, run_manifest_path):
    """Free preview: segmentation + lexicon + prompt for each beat. No API calls."""
    forced = _parse_idx(args.reanchor_on_segment) if args.reanchor_on_segment else []
    anchors = mf.reanchor_indices(len(segments), every=args.reanchor_every, forced=forced)
    plan = {"tool": "ugc-forge", "mode": "plan-only", "segments": []}
    for i, seg in enumerate(segments):
        applied = lex.apply_lexicon(seg["line"], lexicon)
        plan["segments"].append({
            "index": i, "line": seg["line"], "applied_text": applied,
            "est_seconds": round(segmenter.estimate_seconds(seg["line"]), 1),
            "talking_head": seg["talking_head"], "visual": seg["visual"],
            "start_frame_source": "reference" if i in anchors else "prev_frame",
            "prompt": prompts.build_prompt(seg["visual"], style, talking_head=seg["talking_head"]),
        })
        log(f"plan seg {i}: ~{plan['segments'][i]['est_seconds']}s "
            f"th={seg['talking_head']} :: {seg['line'][:60]}")
    dump_json(plan, run_manifest_path)
    log(f"plan -> {run_manifest_path} ({len(segments)} beats, NO API calls made)")
    return


def video_key(seg, style, args, *, anchor):
    """Hash of everything that, if changed, requires a video re-render."""
    prompt = prompts.build_prompt(seg["visual"], style, talking_head=seg["talking_head"])
    blob = "|".join([
        prompt, args.aspect, str(FIXED_SEED), args.veo_model,
        args.lipsync_backend, str(seg["talking_head"]), str(anchor),
    ])
    return mf.sha1_text(blob)


if __name__ == "__main__":
    main(sys.argv[1:])
