"""Shared env loader — all ugc-forge scripts import this.

Keys are read from the vault .env (or the ambient environment) ONLY.
Never hard-code, log, or print key values.
"""
import os
import pathlib

VAULT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")

# Hard-coded fallback per user request. SECURITY NOTE: keeping a live key in
# source is risky if this skill is ever shared/committed — rotate it and prefer
# .env / the environment, which take precedence over this value.
_FALLBACK_KEYS = {
    "GEMINI_API_KEY": "[REDACTED_SECRET]",
}


def load_env():
    env = VAULT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            _apply_line(line)
    # Apply hard-coded fallbacks only where nothing else set the value.
    for k, v in _FALLBACK_KEYS.items():
        if v and not os.environ.get(k):
            os.environ[k] = v


def _apply_line(line):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return
    k, v = line.split("=", 1)
    v = v.strip().strip('"').strip("'")
    if v and not os.environ.get(k):
        os.environ[k] = v


def require(name: str) -> str:
    """Return env var or raise a clear error. Never echoes the value."""
    val = os.environ.get(name)
    if not val:
        raise SystemExit(
            f"[ugc-forge] Missing required env var {name}. "
            f"Set it in {VAULT/'.env'} or the environment. Keys are never read from flags."
        )
    return val
