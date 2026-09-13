#!/usr/bin/env python3
"""supabase_store.py — Cutroom's cloud backend on Supabase Storage.

Local files stay the fast working copy; everything write-through syncs to the
private `cutroom` bucket so the whole workspace (projects, boards, assets) is
cloud-backed and restorable on any machine.

Bucket layout:
    projects.json            — project index
    boards/<slug>.json       — one object per board
    assets/<board>/<file>    — board images

CLI:
    python3 supabase_store.py push     # push everything local → cloud
    python3 supabase_store.py pull     # download anything missing locally
    python3 supabase_store.py status   # counts local vs cloud
"""
import json
import mimetypes
import os
import sys
import threading

import httpx

ROOT = os.path.dirname(os.path.abspath(__file__))
BOARDS = os.path.join(ROOT, "boards")
ASSETS = os.path.join(ROOT, "assets")
PROJECTS_FILE = os.path.join(ROOT, "projects.json")
ENV_FILE = os.path.join(os.path.dirname(ROOT), ".env")
BUCKET = "cutroom"


def _env(name):
    if os.environ.get(name):
        return os.environ[name]
    if os.path.isfile(ENV_FILE):
        for line in open(ENV_FILE):
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    return None


_client = None
_lock = threading.Lock()


def client():
    global _client
    with _lock:
        if _client is None:
            url = _env("SUPABASE_URL")
            key = _env("SUPABASE_SECRET_KEY")
            if not url or not key:
                raise RuntimeError("SUPABASE_URL / SUPABASE_SECRET_KEY missing from .env")
            _client = httpx.Client(
                base_url=url.rstrip("/") + "/storage/v1",
                headers={"apikey": key, "Authorization": f"Bearer {key}"},
                timeout=60,
            )
        return _client


def ensure_bucket():
    r = client().get(f"/bucket/{BUCKET}")
    if r.status_code == 200:
        return
    client().post("/bucket", json={"id": BUCKET, "name": BUCKET, "public": False})


def upload(path, data, ctype=None):
    ctype = ctype or mimetypes.guess_type(path)[0] or "application/octet-stream"
    r = client().post(
        f"/object/{BUCKET}/{path}", content=data,
        headers={"Content-Type": ctype, "x-upsert": "true"},
    )
    r.raise_for_status()


def download(path):
    r = client().get(f"/object/{BUCKET}/{path}")
    r.raise_for_status()
    return r.content


def delete(paths):
    if isinstance(paths, str):
        paths = [paths]
    client().request("DELETE", f"/object/{BUCKET}", json={"prefixes": paths})


def list_remote(prefix=""):
    """Recursively list object paths under a prefix. Returns {path: updated_epoch}."""
    import datetime
    out = {}
    r = client().post(
        f"/object/list/{BUCKET}",
        json={"prefix": prefix, "limit": 1000, "offset": 0,
              "sortBy": {"column": "name", "order": "asc"}},
    )
    r.raise_for_status()
    for entry in r.json():
        name = (prefix + "/" if prefix else "") + entry["name"]
        if entry.get("id") is None:  # folder
            out.update(list_remote(name))
        else:
            ts = 0.0
            stamp = entry.get("updated_at") or entry.get("created_at")
            if stamp:
                try:
                    ts = datetime.datetime.fromisoformat(
                        stamp.replace("Z", "+00:00")).timestamp()
                except ValueError:
                    ts = 0.0
            out[name] = ts
    return out


# ---- high-level sync ---------------------------------------------------

def push_board(slug):
    p = os.path.join(BOARDS, slug + ".json")
    if os.path.isfile(p):
        upload(f"boards/{slug}.json", open(p, "rb").read(), "application/json")
        try:
            mirror_board(slug)
        except Exception:
            pass


def delete_board(slug):
    delete([f"boards/{slug}.json"])
    remote_assets = [p for p in list_remote(f"assets/{slug}")]
    if remote_assets:
        delete(remote_assets)


def push_asset(rel):
    """rel is relative to assets/, e.g. 'my-board/frame1.jpg'."""
    p = os.path.join(ASSETS, rel)
    if os.path.isfile(p):
        upload(f"assets/{rel}", open(p, "rb").read())


def push_projects():
    if os.path.isfile(PROJECTS_FILE):
        upload("projects.json", open(PROJECTS_FILE, "rb").read(), "application/json")


def _local_files():
    files = {}
    if os.path.isfile(PROJECTS_FILE):
        files["projects.json"] = PROJECTS_FILE
    if os.path.isdir(BOARDS):
        for f in os.listdir(BOARDS):
            if f.endswith(".json"):
                files[f"boards/{f}"] = os.path.join(BOARDS, f)
    if os.path.isdir(ASSETS):
        for base, _dirs, names in os.walk(ASSETS):
            for n in names:
                if n.startswith("."):
                    continue
                full = os.path.join(base, n)
                rel = os.path.relpath(full, ASSETS).replace(os.sep, "/")
                files[f"assets/{rel}"] = full
    return files


SKEW = 5  # seconds of clock slack before we call one side "newer"


def _dest_for(remote):
    if remote == "projects.json":
        return PROJECTS_FILE
    if remote.startswith("boards/"):
        return os.path.join(BOARDS, remote[len("boards/"):])
    if remote.startswith("assets/"):
        return os.path.join(ASSETS, remote[len("assets/"):])
    return None


def push_all():
    """Upload local files that are missing remotely or newer than the cloud copy."""
    ensure_bucket()
    remote = list_remote("")
    pushed = 0
    for rpath, local in _local_files().items():
        if rpath not in remote or os.path.getmtime(local) > remote[rpath] + SKEW:
            upload(rpath, open(local, "rb").read())
            pushed += 1
    return pushed


def pull_missing():
    """Download cloud objects that are missing locally or newer than the local copy."""
    ensure_bucket()
    local = _local_files()
    pulled = 0
    for rpath, rts in list_remote("").items():
        dest = _dest_for(rpath)
        if dest is None:
            continue
        if rpath in local and os.path.getmtime(local[rpath]) + SKEW >= rts:
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(download(rpath))
        pulled += 1
    return pulled


def sync():
    """Two-way, newer-wins in both directions (web edits survive local restarts)."""
    pulled = pull_missing()
    pushed = push_all()
    return {"pulled": pulled, "pushed": pushed}


# ---- optional relational mirror (tables created via supabase/migrations/) ----

_tables_ok = None


def _rest():
    url = _env("SUPABASE_URL").rstrip("/") + "/rest/v1"
    key = _env("SUPABASE_SECRET_KEY")
    return url, {"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "application/json",
                 "Prefer": "resolution=merge-duplicates"}


def tables_exist():
    global _tables_ok
    if _tables_ok is None:
        url, headers = _rest()
        r = httpx.get(f"{url}/cutroom_boards?select=id&limit=1", headers=headers, timeout=15)
        _tables_ok = r.status_code == 200
    return _tables_ok


def mirror_board(slug):
    """Best-effort upsert of a board row into cutroom_boards (if tables exist)."""
    if not tables_exist():
        return False
    p = os.path.join(BOARDS, slug + ".json")
    if not os.path.isfile(p):
        return False
    b = json.load(open(p))
    url, headers = _rest()
    httpx.post(f"{url}/cutroom_boards", headers=headers, timeout=30, json={
        "id": slug, "title": b.get("title", slug),
        "project": b.get("project", "general"),
        "cards": b.get("cards", []), "edges": b.get("edges", []),
    })
    return True


def migrate_to_tables():
    """Populate cutroom_projects/cutroom_boards from current data. Re-runnable."""
    if not tables_exist():
        return ("Tables not found. Push to main (or run the "
                "'Deploy Supabase migrations' workflow) to apply supabase/migrations/ first.")
    url, headers = _rest()
    projects = json.load(open(PROJECTS_FILE)) if os.path.isfile(PROJECTS_FILE) else {}
    projects.setdefault("general", {"name": "General"})
    rows = [{"id": s, "name": p.get("name", s)} for s, p in projects.items()]
    httpx.post(f"{url}/cutroom_projects", headers=headers, json=rows, timeout=30).raise_for_status()
    n = 0
    for f in os.listdir(BOARDS):
        if f.endswith(".json") and mirror_board(f[:-5]):
            n += 1
    return f"migrated {len(rows)} projects, {n} boards into tables"


def fire_and_forget(fn, *args):
    """Run a sync op in a daemon thread; log failures, never block the request."""
    def run():
        try:
            fn(*args)
        except Exception as e:
            print(f"[supabase sync] {fn.__name__}{args} failed: {e}", file=sys.stderr)
    threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "push":
        print(f"pushed {push_all()} objects")
    elif cmd == "pull":
        print(f"pulled {pull_missing()} objects")
    elif cmd == "sync":
        print(sync())
    elif cmd == "migrate":
        print(migrate_to_tables())
    else:
        ensure_bucket()
        print(f"local: {len(_local_files())} files, cloud: {len(list_remote(''))} objects")
