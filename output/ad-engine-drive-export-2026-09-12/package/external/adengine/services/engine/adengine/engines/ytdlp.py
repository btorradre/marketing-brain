"""yt-dlp download (TikTok / IG / YouTube / any supported URL) into a work dir.
Also fetches native captions (srt) so the watcher can prefer them over Whisper."""
from __future__ import annotations

import glob
import os
from urllib.parse import urlparse

from adengine.core.errors import ProviderError
from adengine.core.settings import settings
from adengine.engines import shell


def is_url(s: str | None) -> bool:
    if not s:
        return False
    p = urlparse(s)
    return p.scheme in {"http", "https"} and bool(p.netloc)


def download(url: str, work_dir: str) -> str:
    """Downloads `url` as <work_dir>/source.<ext> (mp4 preferred) plus any
    English subtitles as source.*.srt. Returns the video path."""
    os.makedirs(work_dir, exist_ok=True)
    out_template = os.path.join(work_dir, "source.%(ext)s")
    res = shell.run([
        settings.ytdlp,
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--write-auto-subs", "--write-subs",
        "--sub-lang", "en.*",
        "--convert-subs", "srt",
        "--no-playlist",
        "-o", out_template,
        url,
    ], timeout=900)
    if res.returncode != 0:
        raise ProviderError(f"yt-dlp failed: {(res.stderr or res.stdout)[-400:]}")
    for ext in ("mp4", "mkv", "webm", "mov"):
        candidate = os.path.join(work_dir, f"source.{ext}")
        if os.path.exists(candidate):
            return candidate
    raise ProviderError("yt-dlp finished but no source.* file was produced")


def subtitle_files(work_dir: str) -> list[str]:
    return sorted(glob.glob(os.path.join(work_dir, "source.*.srt"))
                  + glob.glob(os.path.join(work_dir, "source.*.vtt")))
