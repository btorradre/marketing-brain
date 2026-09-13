"""The only subprocess surface in the engine: ffmpeg, ffprobe, yt-dlp and curl,
resolved through settings. Nothing else is ever executed."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

from adengine.core.errors import ProviderError
from adengine.core.settings import settings


def run(cmd: list[str], timeout: int = 300, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=check)


def run_bytes(cmd: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, timeout=timeout)


def curl_json(args: list[str], timeout: int = 180) -> dict:
    out = run([settings.curl, "-s", *args], timeout=timeout)
    try:
        return json.loads(out.stdout, strict=False)
    except ValueError:
        raise ProviderError(f"non-JSON response: {(out.stdout or out.stderr)[:300]}")


def curl_download(url: str, dest: str, timeout: int = 600) -> str:
    """Download `url` to `dest` with curl -sL. Raises on an empty file."""
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    run([settings.curl, "-sL", "--fail", "-o", dest, url], timeout=timeout, check=True)
    if not os.path.exists(dest) or os.path.getsize(dest) == 0:
        raise ProviderError(f"downloaded 0 bytes from {url[:120]}")
    return dest


def workdir(prefix: str = "job") -> str:
    """A scratch directory on the data volume (never the OS temp dir of the host)."""
    base = os.path.join(settings.data_dir, "tmp")
    os.makedirs(base, exist_ok=True)
    return tempfile.mkdtemp(prefix=f"{prefix}-", dir=base)
