"""Audio source resolution.

The per-segment audio stems can come from one of three sources; the rest of the
pipeline (conform video -> audio duration, lip-sync, mux) is identical regardless:

  1. SYNTHESIZE  — ElevenLabs API from a voice_id (the default).
  2. UPLOAD DIR  — one pre-made VO file per segment (you already rendered them in
                   ElevenLabs). Mapped to beats in sorted filename order.
  3. UPLOAD ONE  — a single full-ad VO file, split into per-segment stems on
                   silence at sentence gaps.

Uploaded audio is copied (never re-encoded) into work/audio/seg_NNN.<ext> so it
stays the authoritative stem; the audio is never stretched/trimmed/pitch-shifted.
Count must equal the script segment count or we STOP and report (no guessing).
"""
import glob
import os
import re
import shutil
import subprocess

from util import RetryableError, ffprobe_duration, log, sha1_file

AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")


def _copy_stem(src, work_audio_dir, idx):
    ext = os.path.splitext(src)[1].lower() or ".mp3"
    dst = os.path.join(work_audio_dir, f"seg_{idx:03d}{ext}")
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    return dst


def from_dir(audio_dir, n, work_audio_dir, segments):
    files = sorted(f for f in glob.glob(os.path.join(audio_dir, "*"))
                   if os.path.splitext(f)[1].lower() in AUDIO_EXTS)
    if len(files) != n:
        raise SystemExit(
            f"[ugc-forge] Uploaded audio count ({len(files)}) != script segment "
            f"count ({n}). Provide exactly one VO file per beat (sorted order), or "
            "adjust your segmentation. Refusing to guess the mapping."
        )
    meta = []
    for i, src in enumerate(files):
        dst = _copy_stem(src, work_audio_dir, i)
        dur = ffprobe_duration(dst)
        meta.append({"path": dst, "dur": dur,
                     "text_hash": sha1_file(dst),
                     "applied": segments[i]["line"]})
        log(f"audio seg {i}: uploaded {os.path.basename(src)} ({dur:.2f}s)")
    return meta


def _silence_cut_points(vo_path, noise_db, min_gap):
    """Return a sorted list of cut timestamps at the MIDDLE of each detected
    silence gap (where we slice between spoken beats)."""
    proc = subprocess.run(
        ["ffmpeg", "-i", vo_path, "-af",
         f"silencedetect=noise={noise_db}dB:d={min_gap}", "-f", "null", "-"],
        text=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL,
    )
    starts, ends = [], []
    for line in proc.stderr.splitlines():
        ms = re.search(r"silence_start:\s*([0-9.]+)", line)
        me = re.search(r"silence_end:\s*([0-9.]+)", line)
        if ms:
            starts.append(float(ms.group(1)))
        if me:
            ends.append(float(me.group(1)))
    cuts = []
    for s, e in zip(starts, ends):
        cuts.append((s + e) / 2.0)
    return sorted(cuts)


def from_voiceover(vo_path, n, work_audio_dir, segments, *, noise_db=-30, min_gap=0.35):
    total = ffprobe_duration(vo_path)
    cuts = _silence_cut_points(vo_path, noise_db, min_gap)
    # We need exactly n-1 internal cut points to make n chunks.
    if len(cuts) + 1 != n:
        raise SystemExit(
            f"[ugc-forge] Splitting the voiceover found {len(cuts)+1} spoken chunks "
            f"but the script has {n} beats. Tune --vo-noise-db / --vo-min-gap, or "
            "upload one VO file per beat with --audio-dir. Refusing to guess."
        )
    bounds = [0.0] + cuts + [total]
    ext = os.path.splitext(vo_path)[1].lower() or ".mp3"
    meta = []
    for i in range(n):
        start, end = bounds[i], bounds[i + 1]
        dst = os.path.join(work_audio_dir, f"seg_{i:03d}{ext}")
        # Stream-copy the slice — no re-encode, audio untouched.
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", vo_path,
             "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-c", "copy", dst],
            check=True,
        )
        dur = ffprobe_duration(dst)
        meta.append({"path": dst, "dur": dur,
                     "text_hash": sha1_file(dst),
                     "applied": segments[i]["line"]})
        log(f"audio seg {i}: split {start:.2f}-{end:.2f}s ({dur:.2f}s)")
    return meta
