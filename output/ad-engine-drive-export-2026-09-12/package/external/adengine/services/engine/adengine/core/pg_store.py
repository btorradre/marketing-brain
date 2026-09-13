"""PostgresStore: the Store API on the real tables in packages/schema/migrations.

Design
------
Each Store collection maps 1:1 onto a table (``approval`` -> ``card_approval``).
For every table we know the set of real columns (``COLUMNS``). On ``put`` the
record is split: keys that are columns become column values, everything else is
packed into the ``data jsonb`` column. On read the two halves are merged back
into one flat record, so callers never see the split.

Timestamps: the Store contract uses ``created`` / ``updated`` as epoch floats
(LocalStore). The tables use ``created_at`` / ``updated_at`` timestamptz. The
mapping is done here, both directions.

Connections: psycopg3, opened lazily on first use, so this module imports and
builds SQL without a database (the unit test only checks the SQL text). Every
query is workspace-scoped by the caller (``workspace_id`` argument); the engine
connects as the service role which bypasses RLS, so this scoping is the tenant
boundary. Never build a query here without ``workspace_id = %s``.

The queue and Store lifecycle are exercised by test_postgres_integration.py.
claim_job is the explicit worker-only exception to single-workspace queries.
"""
from __future__ import annotations
import datetime as dt
import json
from typing import Any, Iterable

from .errors import NotFound
from .store import Store, Record

# collection name -> table name. Everything else is identity.
TABLE_FOR = {"approval": "card_approval"}

# Real columns per table, excluding id / workspace_id / created_at / updated_at / data,
# which every tenant table has. Keep in sync with packages/schema/migrations/0001_init.sql.
COLUMNS: dict[str, tuple[str, ...]] = {
    "credential":     ("provider", "ciphertext", "last_verified", "balance_cache"),
    "brand":          ("slug", "name", "brief", "house_laws"),
    "product":        ("brand_id", "slug", "name", "truth"),
    "artifact":       ("brand_id", "kind", "name", "body", "frontmatter", "version", "generated_by"),
    "reference":      ("brand_id", "source", "asset_id", "manifest", "status"),
    "board":          ("brand_id", "slug", "title", "lanes", "cards", "edges", "version", "status"),
    "lane":           ("board_id", "name", "position"),
    "card":           ("board_id", "lane_id", "type", "position", "size", "content", "asset_id"),
    "card_approval":  ("board_id", "card_id", "member_id", "state", "note", "at"),
    "board_version":  ("board_id", "version", "snapshot", "created_by"),
    "comment":        ("board_id", "card_id", "member_id", "body", "resolved"),
    "job":            ("kind", "provider", "status", "input", "output", "cost", "parent_id"),
    "asset":          ("kind", "mime", "storage_key", "url", "meta", "job_id", "duration_ms", "width", "height"),
    "cost":           ("job_id", "provider", "units", "unit_name", "usd"),
    "concept":        ("brand_id", "product_id", "asset_code", "fields"),
    "timeline":       ("brand_id", "doc", "version"),
    "render":         ("timeline_id", "timeline_version", "preset", "status", "output_asset_id", "job_id", "cost"),
    "style":          ("brand_id", "doc"),
    "ad":             ("brand_id", "concept_id", "naming_id", "concept_family", "axis", "status"),
    "ad_metric":      ("ad_id", "source", "period_start", "period_end", "spend", "roas", "cpa", "hook_rate", "hold_rate"),
    "playbook_entitlement": ("playbook_id", "tier", "granted_at", "expires_at"),
}

# jsonb columns need json-encoded parameters.
JSON_COLUMNS = {"brief", "house_laws", "truth", "frontmatter", "manifest", "lanes", "cards", "edges",
                "position", "size", "content", "snapshot", "input", "output", "meta", "fields", "doc",
                "balance_cache", "data"}
# timestamptz columns that the Store sees as epoch floats.
TS_COLUMNS = {"created_at", "updated_at", "last_verified", "at", "granted_at", "expires_at"}
BASE_COLUMNS = ("id", "workspace_id", "created_at", "updated_at", "data")


def table_for(collection: str) -> str:
    t = TABLE_FOR.get(collection, collection)
    if t not in COLUMNS:
        raise ValueError(f"unknown collection {collection!r}")
    return t


def _ts(v: Any) -> Any:
    if v is None or isinstance(v, dt.datetime):
        return v
    return dt.datetime.fromtimestamp(float(v), tz=dt.timezone.utc)


def _epoch(v: Any) -> Any:
    return v.timestamp() if isinstance(v, dt.datetime) else v


def split_record(collection: str, record: Record) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """(table, column values, leftover data) for a record. Store timestamps map to *_at."""
    table = table_for(collection)
    cols = set(COLUMNS[table]) | set(BASE_COLUMNS) - {"data"}
    rec = dict(record)
    if "created" in rec:
        rec["created_at"] = rec.pop("created")
    if "updated" in rec:
        rec["updated_at"] = rec.pop("updated")
    values: dict[str, Any] = {}
    data: dict[str, Any] = {}
    for k, v in rec.items():
        if k in cols:
            values[k] = v
        elif k == "data" and isinstance(v, dict):
            data.update(v)
        else:
            data[k] = v
    return table, values, data


def _param(col: str, v: Any) -> Any:
    if col in JSON_COLUMNS:
        return json.dumps(v, default=str)
    if col in TS_COLUMNS:
        return _ts(v)
    return v


def build_put(collection: str, record: Record) -> tuple[str, list[Any]]:
    """INSERT ... ON CONFLICT (id) DO UPDATE for one record."""
    table, values, data = split_record(collection, record)
    if table == "job" and values.get("cost") is None:
        values["cost"] = 0
    if "id" not in values or "workspace_id" not in values:
        raise ValueError("record needs id and workspace_id")
    values["data"] = data
    cols = list(values)
    placeholders = ", ".join("%s::uuid" if c == "workspace_id" else "%s" for c in cols)
    updates = ", ".join(f"{c} = excluded.{c}" for c in cols if c not in ("id", "workspace_id", "created_at"))
    sql = (f"insert into {table} ({', '.join(cols)}) values ({placeholders}) "
           f"on conflict (id) do update set {updates} "
           f"where {table}.workspace_id = excluded.workspace_id returning *")
    return sql, [_param(c, values[c]) for c in cols]


def build_find(collection: str, workspace_id: str, eq: dict[str, Any]) -> tuple[str, list[Any]]:
    """SELECT * scoped by workspace. Column filters compare the column; other keys filter data->>key."""
    table = table_for(collection)
    cols = set(COLUMNS[table]) | {"id"}
    where = ["workspace_id = %s::uuid"]
    params: list[Any] = [workspace_id]
    for k, v in eq.items():
        if k in cols:
            if k in JSON_COLUMNS:
                where.append(f"{k} = %s::jsonb"); params.append(json.dumps(v, default=str))
            else:
                where.append(f"{k} = %s"); params.append(v)
        else:
            if not k.replace("_", "").isalnum():
                raise ValueError(f"bad filter key {k!r}")
            if isinstance(v, (dict, list)):
                where.append(f"data -> %s = %s::jsonb"); params.extend([k, json.dumps(v, default=str)])
            else:
                where.append("data ->> %s = %s"); params.extend([k, str(v)])
    sql = f"select * from {table} where {' and '.join(where)} order by updated_at desc"
    return sql, params


def build_get(collection: str, workspace_id: str, id: str) -> tuple[str, list[Any]]:
    table = table_for(collection)
    return f"select * from {table} where workspace_id = %s::uuid and id = %s", [workspace_id, id]


def build_delete(collection: str, workspace_id: str, id: str) -> tuple[str, list[Any]]:
    table = table_for(collection)
    return f"delete from {table} where workspace_id = %s::uuid and id = %s", [workspace_id, id]


def row_to_record(row: dict[str, Any]) -> Record:
    """Merge columns + data back into one flat Store record (epoch floats for created/updated)."""
    rec: Record = {}
    data = row.get("data") or {}
    if isinstance(data, str):
        data = json.loads(data)
    rec.update(data)
    for k, v in row.items():
        if k == "data":
            continue
        if k in JSON_COLUMNS and isinstance(v, str):
            v = json.loads(v)
        if k in TS_COLUMNS:
            v = _epoch(v)
        if k == "created_at":
            k = "created"
        elif k == "updated_at":
            k = "updated"
        if isinstance(v, dt.date) and not isinstance(v, dt.datetime):
            v = v.isoformat()
        if v is None and k not in ("created", "updated", "id", "workspace_id"):
            continue  # unset nullable columns stay absent, as in LocalStore
        rec[k] = v
    rec["workspace_id"] = str(rec["workspace_id"])
    return rec


class PostgresStore(Store):
    """Store on the packages/schema tables. Blobs are delegated to object storage (Phase 1)."""

    def __init__(self, dsn: str | None):
        if not dsn:
            raise ValueError("PostgresStore needs DATABASE_URL")
        self.dsn = dsn
        self._conn = None

    # ---- connection (lazy; psycopg imported here so the module loads without it)
    def conn(self):
        if self._conn is None or self._conn.closed:
            import psycopg
            from psycopg.rows import dict_row
            self._conn = psycopg.connect(self.dsn, row_factory=dict_row, autocommit=True)
        return self._conn

    def _run(self, sql: str, params: list[Any]):
        with self.conn().cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if cur.description else []

    def claim_job(self, kinds=None, workspace_ids=None) -> Record | None:
        """Worker-only fleet operation. Atomically claim one job across permitted workspaces.

        The parent join is tenant-scoped even when the worker serves all tenants.
        Failed/missing parents fail their children; pending parents remain queued.
        Each UPDATE holds the selected row lock through the state transition.
        """
        if workspace_ids == []:
            return None
        filters, params = ["j.status = 'queued'"], []
        if kinds:
            filters.append("j.kind = any(%s)")
            params.append(list(kinds))
        if workspace_ids is not None:
            filters.append("j.workspace_id = any(%s::uuid[])")
            params.append(list(workspace_ids))
        filters.append("(j.parent_id is null or p.id is null or p.status in ('completed', 'failed', 'cancelled'))")
        sql = f"""
            with candidate as (
                select j.id, j.workspace_id,
                       (j.parent_id is null or p.status = 'completed') is true as ready
                from job j left join job p
                  on p.id = j.parent_id and p.workspace_id = j.workspace_id
                where {' and '.join(filters)}
                order by j.created_at, j.id
                for update of j skip locked limit 1
            )
            update job j set
                status = case when c.ready then 'running' else 'failed' end,
                updated_at = now(),
                data = j.data || case when c.ready
                    then jsonb_build_object('started', extract(epoch from now()))
                    else jsonb_build_object('finished', extract(epoch from now()),
                         'error', 'parent job ' || j.parent_id || ' failed or is unavailable') end
            from candidate c where j.id = c.id and j.workspace_id = c.workspace_id
            returning j.*
        """
        while True:
            rows = self._run(sql, params)
            if not rows:
                return None
            record = row_to_record(rows[0])
            if record["status"] == "running":
                return record

    # ---- generic
    def put_once(self, collection: str, record: Record) -> Record:
        sql, params = build_put(collection, record)
        sql = sql.split(' on conflict (id)')[0] + ' on conflict (id) do nothing returning *'
        rows = self._run(sql, params)
        return row_to_record(rows[0]) if rows else self.get(collection, record['workspace_id'], record['id'])

    def retry_failed_job(self, workspace_id: str, job_id: str) -> Record:
        rows = self._run("""
            update job set status='queued', updated_at=now(),
                data=(data - 'error') || jsonb_build_object('failed_attempts',
                    coalesce(data->'failed_attempts', '[]'::jsonb) ||
                    jsonb_build_array(jsonb_build_object('error',data->'error','finished',data->'finished')))
            where workspace_id=%s::uuid and id=%s and status='failed'
                and (output is null or output='{}'::jsonb)
            returning *
        """, [workspace_id, job_id])
        return row_to_record(rows[0]) if rows else self.get('job',workspace_id,job_id)

    def put(self, collection: str, record: Record) -> Record:
        sql, params = build_put(collection, record)
        rows = self._run(sql, params)
        if not rows:
            # id exists in another workspace: the ON CONFLICT ... WHERE refused it
            raise NotFound(f"{collection}/{record['id']} not writable in workspace {record['workspace_id']}")
        return row_to_record(rows[0])

    def get(self, collection: str, workspace_id: str, id: str) -> Record:
        rows = self._run(*build_get(collection, workspace_id, id))
        if not rows:
            raise NotFound(f"{collection}/{id} not found in workspace {workspace_id}")
        return row_to_record(rows[0])

    def find(self, collection: str, workspace_id: str, **eq: Any) -> list[Record]:
        rows = self._run(*build_find(collection, workspace_id, eq))
        return [row_to_record(r) for r in rows]

    def delete(self, collection: str, workspace_id: str, id: str) -> None:
        self._run(*build_delete(collection, workspace_id, id))

    # ---- blobs: object storage lands in Phase 1 (OBJECT_STORE_URL). Signatures kept.
    def put_blob(self, workspace_id: str, key: str, data: bytes | Iterable[bytes], mime: str = "application/octet-stream") -> str:
        raise NotImplementedError("PostgresStore blobs are served by object storage (Phase 1)")

    def open_blob(self, workspace_id: str, key: str):
        raise NotImplementedError("PostgresStore blobs are served by object storage (Phase 1)")

    def blob_path(self, workspace_id: str, key: str) -> str:
        raise NotImplementedError("PostgresStore blobs are served by object storage (Phase 1)")

    def url(self, workspace_id: str, key: str) -> str:
        from .settings import settings
        base = settings.object_store_url or settings.public_base_url
        return f"{base.rstrip('/')}/{workspace_id}/{key}"


__all__ = ["PostgresStore", "build_put", "build_find", "build_get", "build_delete",
           "split_record", "row_to_record", "table_for", "COLUMNS", "TABLE_FOR"]
