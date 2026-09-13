"""Tests for adengine.dr against a LocalStore under a temp dir.

Env is pinned before adengine is imported so settings pick it up; the fixture
also swaps the store singleton and auth context explicitly so the suite is
independent of import order when other test modules run first.
"""
import asyncio
import os
import tempfile

_DATA_DIR = tempfile.mkdtemp(prefix="adengine-dr-test-")
os.environ["ADENGINE_DATA_DIR"] = _DATA_DIR
os.environ["ADENGINE_DEV_WORKSPACE"] = "ws_test"
os.environ["ADENGINE_AUTH"] = "dev"

import pytest  # noqa: E402

from adengine.core import store as store_mod  # noqa: E402
from adengine.core.auth import AuthContext, _ctx, set_auth_context  # noqa: E402
from adengine.core.errors import Forbidden  # noqa: E402
from adengine.core.store import LocalStore  # noqa: E402
from adengine.dr import artifacts, boards, context, lawgate, server, tracker  # noqa: E402

WS = "ws_test"
OWNER = AuthContext(workspace_id=WS, member_id="m_owner", role="owner")
AGENT = AuthContext(workspace_id=WS, member_id="m_agent", role="agent")


@pytest.fixture
def st(tmp_path):
    local = LocalStore(str(tmp_path))
    store_mod._store = local
    token = set_auth_context(OWNER)
    try:
        yield local
    finally:
        _ctx.reset(token)
        store_mod._store = None


@pytest.fixture
def brand(st):
    return st.create("brand", WS, "brd", slug="acme", name="Acme Goods", code="ACM",
                     brief={"positioning": "the quiet luxury tote"},
                     house_laws=[{"law": "house: never say 'synergy'", "severity": "blocker",
                                  "regex": r"(?i)\bsynergy\b"}])


def _assets(st, n):
    out = []
    for i in range(n):
        a = st.create("asset", WS, "ast", kind="image", mime="image/jpeg",
                      storage_key=f"frames/f{i}.jpg", url=None, meta={"width": 1080, "height": 1920}, job_id=None)
        out.append(a["id"])
    return out


def _spec(assets, title="Acme tote storyboard"):
    ref_beats = [{"t": f"0:0{i}", "script": f"ref line {i}", "visual": "creator holds bag",
                  "emotion": "curiosity"} for i in range(3)]
    our_beats = [{"t": f"0:0{i}", "script": f"our line {i}", "frame": assets[i],
                  "visual": "bag on counter", "emotion": "relief"} for i in range(3)]
    return {"title": title, "summary": "Mirror the reference beat for beat.",
            "timelines": [{"label": "REFERENCE CREATIVE", "source": "tiktok 1.2M", "beats": ref_beats},
                          {"label": "OUR VERSION", "beats": our_beats}],
            "notes": [{"title": "DO", "text": "keep the product on screen"}]}


# ---------------------------------------------------------------------------

def test_load_brand_and_unknown(st, brand):
    out = context.load_brand("acme")
    assert out["brand"] == "acme" and out["brief"]["positioning"].startswith("the quiet")
    assert out["house_laws"][0]["severity"] == "blocker"
    assert out["products"] == [] and out["angle_bank"] is None
    assert context.load_brand("nope")["available"] == ["acme"]


def test_lawgate_combines_global_and_house(st, brand):
    res = lawgate.check("Pure synergy — right here.", brand_slug="acme")
    laws = {b["law"] for b in res["blockers"]}
    assert any("em dash" in l for l in laws)
    assert any("synergy" in l for l in laws)
    assert res["ok"] is False
    assert lawgate.check("Plain sentence.")["ok"] is True


def test_artifact_save_passes_and_versions(st, brand):
    r1 = artifacts.save_artifact("acme", "voc-index", "Customers say the strap digs in.")
    assert r1["saved"] and r1["version"] == 1
    assert r1["frontmatter"]["brand"] == "acme" and r1["frontmatter"]["artifact"] == "voc-index"
    assert set(r1["frontmatter"]) == {"brand", "artifact", "generated_by", "updated", "sources"}
    r2 = artifacts.save_artifact("acme", "voc-index", "Updated body.", sources=["survey-1"])
    assert r2["version"] == 2 and r2["id"] == r1["id"]
    read = artifacts.read_artifact("acme", "voc-index")
    assert read["body"] == "Updated body." and read["version"] == 2
    inv = artifacts.list_artifacts("acme")["artifacts"]
    assert len(inv) == 1 and inv[0]["version"] == 2


def test_artifact_em_dash_blocked_then_forced(st, brand):
    body = "The hook — then the payoff."
    blocked = artifacts.save_artifact("acme", "brief", body, name="2026-09-02 test brief")
    assert blocked["saved"] is False and blocked["lawgate"]["blockers"]
    assert artifacts.read_artifact("acme", "brief", name="2026-09-02 test brief").get("error")
    forced = artifacts.save_artifact("acme", "brief", body, name="2026-09-02 test brief", force=True)
    assert forced["saved"] and forced["forced"] and forced["name"] == "2026-09-02-test-brief"
    listing = artifacts.read_artifact("acme", "brief")
    assert listing["available"] == ["2026-09-02-test-brief"]
    assert artifacts.save_artifact("acme", "brief", "x").get("error")  # collection needs a name


def test_layout_is_pure_and_default_16_9():
    laid = boards.layout({"title": "T", "timelines": [{"label": "OUR VERSION",
                                                        "beats": [{"t": "0:00", "frame": "ast_x"}]}]})
    frame = next(c for c in laid["cards"] if c["type"] == "image")
    assert frame["asset_id"] == "ast_x" and frame["w"] == 260 and frame["h"] == 146
    assert laid["lanes"][0]["role"] == "ours"
    laid2 = boards.layout({"title": "T", "timelines": [
        {"label": "A", "beats": [{"frame": {"asset_id": "a", "width": 1080, "height": 1920}}]},
        {"label": "B", "beats": [{"script": "x"}]}]})
    assert [l["role"] for l in laid2["lanes"]] == ["reference", "ours"]
    assert next(c for c in laid2["cards"] if c["type"] == "image")["h"] == 462


def test_push_board_and_approval_gate(st, brand):
    assets = _assets(st, 3)
    pushed = boards.push_board("acme", _spec(assets))
    assert pushed["version"] == 1 and pushed["card_count"] > 0 and pushed["warnings"] == []
    assert pushed["url"].endswith("/b/acme-tote-storyboard")
    slug = pushed["slug"]

    again = boards.push_board("acme", _spec(assets))
    assert again["board_id"] == pushed["board_id"] and again["version"] == 2

    board = boards.get_board("acme", slug)
    frames = [c for c in board["cards"] if c["type"] == "image"]
    assert len(frames) == 3 and all(c["src"] and c["asset_id"] for c in frames)
    assert all(c["approval"] is None for c in frames)
    assert board["lanes"][1]["role"] == "ours"

    status = boards.approval_status(st, WS, slug)
    assert (status["approved"], status["total"], status["approved_count"]) == (False, 3, 0)
    assert len(status["pending"]) == 3

    a1 = boards.approve_card(slug, frames[0]["id"], "approved")
    assert a1["member_id"] == "m_owner" and a1["at"] > 0
    boards.approve_card(slug, frames[1]["id"], "approved", note="good")
    status = boards.approval_status(st, WS, slug)
    assert status["approved"] is False and status["approved_count"] == 2 and len(status["pending"]) == 1

    boards.approve_card(slug, frames[2]["id"], "rejected", note="wrong colorway")
    status = boards.approval_status(st, WS, slug)
    assert status["approved"] is False and status["rejected"][0]["note"] == "wrong colorway"

    boards.approve_card(slug, frames[2]["id"], "approved")
    status = boards.approval_status(st, WS, slug)
    assert status["approved"] is True and status["approved_count"] == 3 and status["pending"] == []

    # swapping the keyframe on an approved card re-opens the gate
    new_asset = _assets(st, 1)[0]
    spec = _spec(assets)
    spec["timelines"][1]["beats"][2]["frame"] = new_asset
    boards.push_board("acme", spec)
    status = boards.approval_status(st, WS, slug)
    assert status["approved"] is False and status["pending"][0]["stale"] is True

    html = boards.export_board(slug)
    assert html.startswith("<!doctype html>") and "ACME TOTE STORYBOARD" in html and new_asset in html


def test_agent_role_cannot_approve(st, brand):
    assets = _assets(st, 1)
    slug = boards.push_board("acme", _spec(assets + assets + assets), slug="gate")["slug"]
    token = set_auth_context(AGENT)
    try:
        with pytest.raises(Forbidden):
            boards.approve_card(slug, "l1-b0-frame", "approved")
        assert server.approve_card("gate", "l1-b0-frame", "approved")["error"] == "Forbidden"
    finally:
        _ctx.reset(token)
    assert boards.approval_status(st, WS, slug)["approved_count"] == 0


def test_push_concept_increments(st, brand):
    st.create("product", WS, "prd", brand_id=brand["id"], slug="tote", name="Tote", code="TOTE", truth={})
    c1 = tracker.push_concept("acme", "Tote", "Founder Story", "A1 strap pain", "the strap is the hook")
    c2 = tracker.push_concept("acme", "Tote", "Founder Story", "A1 strap pain", "second cut")
    assert c1["asset_code"] == "ACM-TOTE-FOUNDERSTORY-VID01"
    assert c2["asset_code"] == "ACM-TOTE-FOUNDERSTORY-VID02"
    img = tracker.push_concept("acme", "Tote", "Founder Story", "A1", "static", format="image")
    assert img["asset_code"] == "ACM-TOTE-FOUNDERSTORY-IMG01"
    assert tracker.push_concept("acme", "Tote", "x", "a", "t", format="gif").get("error")


def test_ingest_reference_queues_job_and_status(st, brand):
    job = server.ingest_reference("https://example.com/ad.mp4", brand_slug="acme")
    assert job["status"] == "queued" and job["job_id"].startswith("job_")
    assert st.get("job", WS, job["job_id"])["input"]["url"] == "https://example.com/ad.mp4"
    assert server.ingest_reference("/Users/someone/ad.mp4").get("error")
    s = server.status()
    assert s["workspace"] == WS and s["counts"]["job"] == 1 and s["counts"]["brand"] == 1
    assert s["store_backend"] == "local" and "adengine.laws" in s["packages"]


def test_playbook_step_aliases_when_registry_present():
    lp = context.list_playbooks()
    if lp.get("error"):
        pytest.skip(lp["error"])
    assert lp["pipeline_steps"]["strategize"]["playbook"] == "strategize-ad-adaptation"
    got = context.get_playbook("strategize")
    assert got.get("resolved") == "strategize-ad-adaptation" and got["content"]
    laws = context.get_playbook("laws")
    assert laws.get("file") == "modules/laws.md" and laws["content"]
    assert context.get_playbook("no-such-playbook").get("error")


def test_server_tool_registration():
    tools = asyncio.run(server.mcp.list_tools())
    names = {t.name for t in tools}
    expected = {"pipeline_guide", "load_brand", "load_product", "list_playbooks", "get_playbook",
                "lawgate", "list_artifacts", "read_artifact", "save_artifact", "push_board",
                "get_board", "list_boards", "approve_card", "board_approval_status", "export_board",
                "push_concept", "ingest_reference", "status"}
    assert expected <= names, expected - names
    guide = server.pipeline_guide()
    assert "Brooks" not in guide and "localhost" not in guide and "/Users/" not in guide
    flat = " ".join(guide.split())
    assert "animate_scenes verifies the board's approval state server-side" in flat


def test_authmw_oauth_mode_sets_context():
    from starlette.testclient import TestClient
    from adengine.core.auth import current
    from adengine.dr import authmw

    async def app(scope, receive, send):
        body = current().workspace_id.encode()
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})

    client = TestClient(authmw.AuthMiddleware(app, mode="oauth"))
    assert client.get("/mcp").status_code == 401                                   # no token
    assert client.get("/mcp", headers={"Authorization": "Bearer abc"}).status_code == 403  # stub resolver
    original = authmw.resolve_token
    authmw.set_token_resolver(lambda tok: AuthContext(workspace_id=f"ws_{tok}", member_id="m1", role="editor"))
    try:
        r = client.get("/mcp", headers={"Authorization": "Bearer abc"})
        assert r.status_code == 200 and r.text == "ws_abc"
    finally:
        authmw.set_token_resolver(original)
    assert TestClient(authmw.AuthMiddleware(app, mode="dev")).get("/mcp").text == WS  # dev passthrough


def test_server_tools_lawgate_and_product_blocks(st):
    """Regression: the `lawgate` tool must not shadow the lawgate module, and
    load_product must render the truth record's identity block verbatim."""
    from adengine.dr import server
    ws = WS; store = st
    b = store.create("brand", ws, "brand", slug="acme", name="Acme", code="ACM", brief={}, house_laws=[
        {"id": "no-foo", "law": "never say foo", "severity": "blocker", "regex": r"\bfoo\b", "flags": ["i"]}])
    store.create("product", ws, "prod", brand_id=b["id"], brand_slug="acme", slug="tote", name="Acme Tote",
                 truth={"name": "Acme Tote", "slug": "tote", "brand_slug": "acme", "identity_block": "a plain canvas tote, verbatim", "version": 1})
    g = server.lawgate("Foo is great", brand_slug="acme")
    assert [h["id"] for h in g["blockers"]] == ["no-foo"]
    p = server.load_product("acme", "tote")
    assert p.get("error") is None, p
    assert "a plain canvas tote, verbatim" in p["blocks"]
