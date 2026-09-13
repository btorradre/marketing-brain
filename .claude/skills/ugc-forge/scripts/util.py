"""Shared utilities: logging, shell, ffprobe, hashing, backoff."""
import hashlib
import json
import subprocess
import sys
import time


def log(msg: str):
    print(f"[ugc-forge] {msg}", file=sys.stderr, flush=True)


def run(cmd, check=True, capture=False):
    """Run a subprocess. cmd is a list. Returns CompletedProcess."""
    return subprocess.run(
        cmd,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def ffprobe_duration(path) -> float:
    """Return media duration in seconds via ffprobe."""
    out = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True, text=True, stdout=subprocess.PIPE,
    ).stdout.strip()
    return float(out)


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def sha1_file(path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def with_backoff(fn, *, tries=6, base=2.0, max_sleep=90.0, retry_on=(), label="op"):
    """Call fn(); retry with exponential backoff when it raises a retry_on
    exception OR raises RetryableError. Re-raises the last error after `tries`.
    `sleeper` is module-level so tests can patch; uses time.sleep here."""
    last = None
    for attempt in range(tries):
        try:
            return fn()
        except RetryableError as e:
            last = e
            sleep = min(max_sleep, base ** attempt)
            log(f"{label}: retryable ({e}); backoff {sleep:.0f}s (attempt {attempt+1}/{tries})")
            time.sleep(sleep)
        except retry_on as e:  # type: ignore[misc]
            last = e
            sleep = min(max_sleep, base ** attempt)
            log(f"{label}: error ({e}); backoff {sleep:.0f}s (attempt {attempt+1}/{tries})")
            time.sleep(sleep)
    raise last if last else RuntimeError(f"{label} failed")


class RetryableError(Exception):
    """Raise to signal with_backoff that a retry is warranted (e.g. HTTP 429/5xx)."""


def load_json(path):
    with open(path) as f:
        return json.load(f)


def dump_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
