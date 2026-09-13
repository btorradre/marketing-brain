"""Store: the only persistence boundary. Every record carries workspace_id and every
query is scoped by it. LocalStore keeps JSON documents on disk under
ADENGINE_DATA_DIR for dev and tests; PostgresStore (packages/schema) is the hosted backend.

Record kinds (collection name -> required fields):
  brand         id, workspace_id, slug, name, brief (dict), house_laws (list[rule])
  product       id, workspace_id, brand_id, slug, name, truth (dict; see product_truth.schema)
  artifact      id, workspace_id, brand_id, kind, name, body, frontmatter (dict), version
  reference     id, workspace_id, brand_id, source, asset_id, manifest (dict), status
  board         id, workspace_id, brand_id, slug, title, lanes (list), cards (list), edges (list), version
  approval      id, workspace_id, board_id, card_id, member_id, state, note, at
  job           id, workspace_id, kind, provider, status, input, output, cost, parent_id, created, updated
  asset         id, workspace_id, kind, mime, storage_key, url, meta (dict), job_id
  cost          id, workspace_id, job_id, provider, units, unit_name, usd
  credential    id, workspace_id, provider, ciphertext, last_verified
  concept       id, workspace_id, brand_id, asset_code, fields (dict)
  timeline      id, workspace_id, brand_id, doc (dict), version
  style         id, workspace_id, brand_id, doc (dict)
"""
from __future__ import annotations
import json, os, threading, time
from typing import Any, Iterable
from .settings import settings
from .errors import NotFound
from .ids import new_id

Record = dict[str, Any]


class Store:
    # ---- generic
    def put(self, collection: str, record: Record) -> Record: raise NotImplementedError
    def put_once(self, collection: str, record: Record) -> Record:
        """Atomically insert or return the existing workspace-scoped record."""
        raise NotImplementedError
    def retry_failed_job(self, workspace_id: str, job_id: str) -> Record:
        """Atomically requeue a failed, ungraded job while retaining attempt errors."""
        raise NotImplementedError
    def get(self, collection: str, workspace_id: str, id: str) -> Record: raise NotImplementedError
    def find(self, collection: str, workspace_id: str, **eq: Any) -> list[Record]: raise NotImplementedError
    def delete(self, collection: str, workspace_id: str, id: str) -> None: raise NotImplementedError

    # ---- blobs (media). Returns a storage key; url() makes it fetchable.
    def put_blob(self, workspace_id: str, key: str, data: bytes | Iterable[bytes], mime: str = "application/octet-stream") -> str: raise NotImplementedError
    def open_blob(self, workspace_id: str, key: str): raise NotImplementedError
    def blob_path(self, workspace_id: str, key: str) -> str:
        """Local filesystem path for workers that need one (ffmpeg). Never returned to a tool caller."""
        raise NotImplementedError
    def url(self, workspace_id: str, key: str) -> str: raise NotImplementedError

    # ---- helpers
    def create(self, collection: str, workspace_id: str, prefix: str, **fields: Any) -> Record:
        now = time.time()
        rec = {"id": new_id(prefix), "workspace_id": workspace_id, "created": now, "updated": now, **fields}
        return self.put(collection, rec)

    def update(self, collection: str, workspace_id: str, id: str, **fields: Any) -> Record:
        rec = self.get(collection, workspace_id, id)
        rec.update(fields); rec["updated"] = time.time()
        return self.put(collection, rec)

    def one(self, collection: str, workspace_id: str, **eq: Any) -> Record:
        rows = self.find(collection, workspace_id, **eq)
        if not rows:
            raise NotFound(f"{collection} not found: {eq}")
        return rows[0]


class LocalStore(Store):
    """JSON-on-disk store. One file per record: <data_dir>/<workspace>/<collection>/<id>.json"""

    def __init__(self, root: str | None = None):
        self.root = root or settings.data_dir
        self._lock = threading.RLock()
        os.makedirs(self.root, exist_ok=True)

    def _dir(self, workspace_id: str, collection: str) -> str:
        p = os.path.join(self.root, _safe(workspace_id), _safe(collection))
        os.makedirs(p, exist_ok=True)
        return p

    def put(self, collection: str, record: Record) -> Record:
        ws = record["workspace_id"]; rid = record["id"]
        path = os.path.join(self._dir(ws, collection), _safe(rid) + ".json")
        with self._lock:
            tmp = path + ".tmp"
            with open(tmp, "w") as f:
                json.dump(record, f, indent=1, default=str)
            os.replace(tmp, path)
        return record

    def put_once(self, collection: str, record: Record) -> Record:
        with self._lock:
            try:
                return self.get(collection, record['workspace_id'], record['id'])
            except NotFound:
                return self.put(collection, record)

    def retry_failed_job(self, workspace_id: str, job_id: str) -> Record:
        with self._lock:
            job = self.get('job', workspace_id, job_id)
            if job['status'] == 'failed' and not job.get('output'):
                attempts = list(job.get('failed_attempts', []))
                attempts.append({'error':job.get('error'), 'finished':job.get('finished')})
                return self.update('job',workspace_id,job_id,status='queued',error=None,
                                   failed_attempts=attempts)
            return job

    def get(self, collection: str, workspace_id: str, id: str) -> Record:
        path = os.path.join(self._dir(workspace_id, collection), _safe(id) + ".json")
        if not os.path.exists(path):
            raise NotFound(f"{collection}/{id} not found in workspace {workspace_id}")
        with open(path) as f:
            return json.load(f)

    def find(self, collection: str, workspace_id: str, **eq: Any) -> list[Record]:
        out = []
        d = self._dir(workspace_id, collection)
        for name in os.listdir(d):
            if not name.endswith(".json"):
                continue
            with open(os.path.join(d, name)) as f:
                rec = json.load(f)
            if all(rec.get(k) == v for k, v in eq.items()):
                out.append(rec)
        out.sort(key=lambda r: r.get("updated", 0), reverse=True)
        return out

    def delete(self, collection: str, workspace_id: str, id: str) -> None:
        path = os.path.join(self._dir(workspace_id, collection), _safe(id) + ".json")
        if os.path.exists(path):
            os.remove(path)

    # blobs
    def blob_path(self, workspace_id: str, key: str) -> str:
        p = os.path.join(self.root, _safe(workspace_id), "blobs", *[_safe(x) for x in key.split("/")])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    def put_blob(self, workspace_id, key, data, mime="application/octet-stream") -> str:
        p = self.blob_path(workspace_id, key)
        with open(p, "wb") as f:
            if isinstance(data, (bytes, bytearray)):
                f.write(data)
            else:
                for chunk in data:
                    f.write(chunk)
        return key

    def open_blob(self, workspace_id, key):
        return open(self.blob_path(workspace_id, key), "rb")

    def url(self, workspace_id, key) -> str:
        return f"{settings.public_base_url}/blobs/{workspace_id}/{key}"


def _safe(s: str) -> str:
    s = str(s)
    if not s or s in (".", "..") or "/" in s or "\\" in s or s.startswith("."):
        raise ValueError(f"unsafe id: {s!r}")
    return s


_store: Store | None = None


def get_store() -> Store:
    global _store
    if _store is None:
        if settings.store_backend == "postgres":
            from .pg_store import PostgresStore  # optional dependency
            _store = PostgresStore(settings.database_url)
        else:
            _store = LocalStore()
    return _store
