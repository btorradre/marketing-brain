"""SQL-generation only. No database is available in Phase 0."""
import datetime as dt
import json
import os
import re

import pytest

from adengine.core import pg_store
from adengine.core.pg_store import PostgresStore, build_put, build_find, build_get, build_delete, row_to_record

WS = "00000000-0000-4000-8000-000000000001"
SQL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "packages", "schema", "migrations", "0001_init.sql")


def test_importable_without_connection():
    s = PostgresStore("postgresql://user:pw@localhost/db")
    assert s._conn is None
    with pytest.raises(ValueError):
        PostgresStore(None)


def test_put_splits_columns_and_data():
    rec = {"id": "brand_1", "workspace_id": WS, "slug": "acme", "name": "Acme",
           "brief": {"avatar": "x"}, "house_laws": [], "created": 1.0, "updated": 2.0, "extra": "kept"}
    sql, params = build_put("brand", rec)
    assert sql.startswith("insert into brand (")
    assert "on conflict (id) do update set" in sql
    assert "where brand.workspace_id = excluded.workspace_id" in sql
    assert sql.endswith("returning *")
    cols = re.search(r"insert into brand \((.*?)\) values", sql).group(1).split(", ")
    assert cols == ["id", "workspace_id", "slug", "name", "brief", "house_laws", "created_at", "updated_at", "data"]
    assert params[cols.index("brief")] == json.dumps({"avatar": "x"})
    assert json.loads(params[cols.index("data")]) == {"extra": "kept"}
    assert isinstance(params[cols.index("created_at")], dt.datetime)
    assert "created_at = excluded.created_at" not in sql   # creation time never overwritten
    assert "%s::uuid" in sql                                # workspace id cast


def test_approval_maps_to_card_approval():
    sql, _ = build_put("approval", {"id": "apr_1", "workspace_id": WS, "board_id": "b", "card_id": "c",
                                    "member_id": "m", "state": "approved", "at": 1700000000.0})
    assert sql.startswith("insert into card_approval (")


def test_find_scopes_workspace_and_filters():
    sql, params = build_find("job", WS, {"status": "queued", "concept": "VEL-01"})
    assert sql == ("select * from job where workspace_id = %s::uuid and status = %s and data ->> %s = %s "
                   "order by updated_at desc")
    assert params == [WS, "queued", "concept", "VEL-01"]


def test_find_without_filters_is_still_scoped():
    sql, params = build_find("asset", WS, {})
    assert "where workspace_id = %s::uuid" in sql and params == [WS]


def test_get_and_delete_scoped():
    sql, params = build_get("board", WS, "board_1")
    assert sql == "select * from board where workspace_id = %s::uuid and id = %s" and params == [WS, "board_1"]
    sql, params = build_delete("board", WS, "board_1")
    assert sql == "delete from board where workspace_id = %s::uuid and id = %s"


def test_unknown_collection_rejected():
    with pytest.raises(ValueError):
        build_find("secrets", WS, {})
    with pytest.raises(ValueError):
        build_find("job", WS, {"bad key; drop": 1})


def test_row_roundtrip():
    now = dt.datetime(2026, 9, 2, tzinfo=dt.timezone.utc)
    row = {"id": "job_1", "workspace_id": WS, "kind": "generate", "provider": "kie", "status": "done",
           "input": {"a": 1}, "output": {}, "cost": 0, "parent_id": None,
           "data": {"extra": True}, "created_at": now, "updated_at": now}
    rec = row_to_record(row)
    assert rec["created"] == now.timestamp() and rec["updated"] == now.timestamp()
    assert rec["extra"] is True and rec["input"] == {"a": 1}
    assert "parent_id" not in rec and "created_at" not in rec


def test_column_map_matches_migration():
    """Every column pg_store thinks exists must appear in the CREATE TABLE for that table."""
    sql = open(SQL_PATH, encoding="utf-8").read()
    for table, cols in pg_store.COLUMNS.items():
        m = re.search(rf"create table if not exists {table} \((.*?)\n\);", sql, re.S)
        assert m, f"table {table} missing from migration"
        body = m.group(1)
        for c in cols + pg_store.BASE_COLUMNS:
            assert re.search(rf"^\s+{c}\s", body, re.M), f"{table}.{c} not in migration"


def test_every_tenant_table_gets_rls():
    sql = open(SQL_PATH, encoding="utf-8").read()
    applied = re.search(r"adengine_apply_tenant_policies\(t::regclass\) from unnest\(array\[(.*?)\]\)", sql, re.S).group(1)
    names = set(re.findall(r"'(\w+)'", applied))
    assert names == set(pg_store.COLUMNS)
    assert "create or replace function workspace_member(ws uuid)" in sql
    assert "security definer" in sql


def test_put_once_uses_insert_without_overwrite(monkeypatch):
    store=PostgresStore('postgresql://unused');calls=[]
    record={'id':'job_review','workspace_id':WS,'kind':'grade_edit_style','status':'queued','input':{}}
    monkeypatch.setattr(store,'_run',lambda sql,params:(calls.append((sql,params)) or []))
    monkeypatch.setattr(store,'get',lambda collection,ws,rid:{**record,'status':'running'})
    result=store.put_once('job',record)
    assert 'on conflict (id) do nothing returning *' in calls[0][0]
    assert result['status']=='running'


def test_retry_failed_review_is_atomic_and_scoped(monkeypatch):
    store=PostgresStore('postgresql://unused');calls=[]
    monkeypatch.setattr(store,'_run',lambda sql,params:(calls.append((sql,params)) or []))
    monkeypatch.setattr(store,'get',lambda *args:{'status':'completed'})
    assert store.retry_failed_job(WS,'job_review')['status']=='completed'
    sql,params=calls[0]
    assert "status='failed'" in sql and 'workspace_id=%s::uuid' in sql
    assert params==[WS,'job_review'] and 'failed_attempts' in sql
