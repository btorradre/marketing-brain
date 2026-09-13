"""Pluggable lip-sync conform pass.

For talking-head segments the mouth must match the ElevenLabs waveform, NOT
Veo's discarded native speech. A backend takes (silent_video, audio, out) and
returns a lip-synced video whose audio IS the ElevenLabs stem.

For pure b-roll segments (talking_head=False) we skip lip-sync entirely and the
caller just muxes the VO over the visuals.

Backends are registered in BACKENDS. Add your own by registering a callable
`fn(video_path, audio_path, out_path) -> out_path`. Shipped backends:

  * "fal"      — Sync.so lip-sync hosted on fal.ai (DEFAULT). Uses FAL_API_KEY
                 from the vault .env; no local ML, no SDK. This is the one that
                 actually drives the mouth out of the box.
  * "omni"     — Google Omni audio-conditioned avatar, IF a CLI is wired via
                 env UGC_OMNI_CMD (template with {video} {audio} {out}).
  * "wav2lip"  — wav2lip-style model, IF a CLI is wired via env UGC_WAV2LIP_CMD.
  * "none"     — plain mux only (no mouth driving).

If a real backend is unavailable or errors mid-run, we fall back to a plain mux
so the correct audio is always present and duration-synced, and we LOG that
mouths won't be driven — never silently pretend lip-sync happened.
"""
import os
import shlex
import subprocess

from util import log
from video_ops import conform_video_to_audio, mux_audio
from util import ffprobe_duration


def _run_template(template, video, audio, out):
    cmd = template.format(video=shlex.quote(str(video)),
                          audio=shlex.quote(str(audio)),
                          out=shlex.quote(str(out)))
    log(f"lipsync exec: {cmd.split()[0]} ...")
    subprocess.run(cmd, shell=True, check=True)
    return str(out)


def _mux_fallback(video, audio, out, *, why):
    log(f"lipsync fallback (mux only): {why}. Mouth will not be driven by audio.")
    dur = ffprobe_duration(audio)
    conformed = str(out) + ".silent.mp4"
    conform_video_to_audio(video, dur, conformed)
    mux_audio(conformed, audio, out)
    try:
        os.remove(conformed)
    except OSError:
        pass
    return str(out)


def fal_backend(video, audio, out):
    if not os.environ.get("FAL_API_KEY"):
        return _mux_fallback(video, audio, out, why="FAL_API_KEY not set")
    try:
        import lipsync_fal
        return lipsync_fal.lipsync(video, audio, out)
    except SystemExit:
        raise
    except Exception as e:
        return _mux_fallback(video, audio, out, why=f"fal lipsync error: {e}")


def omni_backend(video, audio, out):
    tmpl = os.environ.get("UGC_OMNI_CMD")
    if not tmpl:
        return _mux_fallback(video, audio, out, why="UGC_OMNI_CMD not set")
    return _run_template(tmpl, video, audio, out)


def wav2lip_backend(video, audio, out):
    tmpl = os.environ.get("UGC_WAV2LIP_CMD")
    if not tmpl:
        return _mux_fallback(video, audio, out, why="UGC_WAV2LIP_CMD not set")
    return _run_template(tmpl, video, audio, out)


BACKENDS = {
    "fal": fal_backend,
    "omni": omni_backend,
    "wav2lip": wav2lip_backend,
    "none": lambda v, a, o: _mux_fallback(v, a, o, why="backend=none (mux requested)"),
}


def lipsync_conform(video, audio, out, *, backend="fal"):
    fn = BACKENDS.get(backend)
    if not fn:
        raise SystemExit(f"[ugc-forge] Unknown lip-sync backend {backend!r}. "
                         f"Choices: {', '.join(BACKENDS)}")
    return fn(video, audio, out)
