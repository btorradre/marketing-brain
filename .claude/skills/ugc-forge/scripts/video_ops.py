"""ffmpeg/ffprobe glue: last-frame extraction, conform-to-audio, mux, concat,
aspect outputs, and lightweight drift detection.

Hard rule: AUDIO is authoritative. Video is conformed to the audio duration.
Audio is never stretched, trimmed, pitch-shifted, or re-encoded.
"""
import os
import subprocess

from util import ffprobe_duration, log, run


def extract_last_frame(video_path, out_png):
    """Write the FINAL frame of `video_path` to `out_png` (for frame chaining)."""
    dur = ffprobe_duration(video_path)
    # Seek slightly before the end to dodge a black/partial trailing frame.
    ts = max(0.0, dur - 0.05)
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", f"{ts:.3f}", "-i", str(video_path),
        "-frames:v", "1", "-q:v", "2", str(out_png),
    ])
    return str(out_png)


def conform_video_to_audio(video_path, audio_dur, out_path):
    """Make the SILENT video exactly `audio_dur` long.

    Longer than target -> trim. Shorter -> freeze the last frame (tpad) to fill.
    The video is re-encoded; the audio is untouched (added later in mux).
    """
    vid_dur = ffprobe_duration(video_path)
    if vid_dur >= audio_dur:
        vf = None
        trim = ["-t", f"{audio_dur:.3f}"]
    else:
        pad = audio_dur - vid_dur
        vf = f"tpad=stop_mode=clone:stop_duration={pad:.3f}"
        trim = ["-t", f"{audio_dur:.3f}"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path), "-an"]
    if vf:
        cmd += ["-vf", vf]
    cmd += trim + ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(out_path)]
    run(cmd)
    return str(out_path)


def mux_audio(video_path, audio_path, out_path):
    """Mux ElevenLabs audio over the (already conformed) video. Audio copied as
    AAC without altering timing; video stream copied."""
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(video_path), "-i", str(audio_path),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(out_path),
    ])
    return str(out_path)


def concat(segment_paths, out_path, workdir):
    """Concatenate finished segments into one continuous MP4.

    Re-encode through concat filter to be robust to minor stream differences.
    """
    if not segment_paths:
        raise SystemExit("[ugc-forge] No segments to concatenate.")
    inputs = []
    filt = []
    for i, p in enumerate(segment_paths):
        inputs += ["-i", str(p)]
        filt.append(f"[{i}:v:0][{i}:a:0]")
    filter_complex = "".join(filt) + f"concat=n={len(segment_paths)}:v=1:a=1[v][a]"
    run([
        "ffmpeg", "-y", "-loglevel", "error", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        str(out_path),
    ])
    return str(out_path)


def make_aspect(src_mp4, out_path, aspect):
    """Produce an alternate aspect via center-crop/pad. 9:16 is the master."""
    # Map aspect -> target WxH (1080-wide family).
    targets = {"9:16": (1080, 1920), "4:5": (1080, 1350), "16:9": (1920, 1080)}
    if aspect not in targets:
        raise SystemExit(f"[ugc-forge] Unsupported aspect {aspect}")
    w, h = targets[aspect]
    vf = (
        f"scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{h}"
    )
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src_mp4),
        "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "copy", str(out_path),
    ])
    return str(out_path)


def mean_luma(image_or_video):
    """Average luminance (0-255) via ffmpeg signalstats. Used for drift detection."""
    proc = subprocess.run(
        [
            "ffmpeg", "-i", str(image_or_video),
            "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG",
            "-frames:v", "1", "-f", "null", "-",
        ],
        text=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL,
    )
    val = None
    for line in proc.stderr.splitlines():
        if "YAVG" in line and "=" in line:
            try:
                val = float(line.rsplit("=", 1)[1].strip())
            except ValueError:
                pass
    return val


def drift_detected(reference_png, current_png, threshold=18.0):
    """True if the chained frame's luma has drifted from the original reference
    by more than `threshold` (a proxy for accumulated color/exposure drift)."""
    a, b = mean_luma(reference_png), mean_luma(current_png)
    if a is None or b is None:
        return False
    delta = abs(a - b)
    if delta > threshold:
        log(f"drift detected: luma delta {delta:.1f} > {threshold}")
        return True
    return False
