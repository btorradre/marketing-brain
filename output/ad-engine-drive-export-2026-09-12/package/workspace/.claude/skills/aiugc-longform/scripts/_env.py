"""Shared env loader — all aiugc-longform Python scripts import this."""
import os, pathlib

VAULT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")

def load_env():
    env = VAULT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip('"').strip("'")
        if v and not os.environ.get(k):
            os.environ[k] = v
