"""Storyboard boards as Store records, plus the human approval gate.

layout(spec) is the app's deterministic storyboard layout engine: a
semantic spec (title, summary, timelines[{label, source, role, beats[{t,
script, frame, visual, emotion, note}]}], notes, moodboard) becomes
{lanes, cards, edges} with pixel positions. Frames are ASSET IDS (a string, or
{"asset_id", "width", "height"}); no PIL, no files. Unknown frame dimensions
default to a 16:9 card.

Board record: id, workspace_id, brand_id, slug, title, summary, project,
lanes, cards, edges, spec, version, warnings.
Approval record: id, workspace_id, board_id, card_id, asset_id, member_id,
state (approved|rejected), note, at.

Card ids are semantic (l{lane}-b{beat}-frame ...) so a re-push keeps them
stable; an approval only counts while the card still carries the asset it
was approved with, so swapping a keyframe re-opens the gate automatically.
"""
from __future__ import annotations

from adengine.core.auth import require_write

import copy
import hashlib
import html
import json
import math
import re
import time
from typing import Any

from adengine.core.auth import current
from adengine.core.errors import Forbidden, NotFound
from adengine.core.settings import settings
from adengine.core.store import Store

from .deps import brand_by_slug, store, ws

COL_W = 260          # beat column width
COL_GAP = 28
LANE_PAD = 36
LANE_GAP = 70
STACK_GAP = 12

COLOR_SCRIPT = "#fdf3c9"   # warm yellow
COLOR_EMOTION = "#f3dce8"  # soft pink
COLOR_NOTE = "#f7f5ee"     # off-white

DEFAULT_FRAME_ASPECT = 16 / 9
APPROVAL_STATES = ("approved", "rejected")
OURS_LABEL = re.compile(r"\b(our|ours|adaptation)\b", re.I)


# ---------------------------------------------------------------------------
# pure layout
# ---------------------------------------------------------------------------

def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9\-_ ]", "", (s or "").lower().strip())
    return re.sub(r"[\s_]+", "-", s)[:60] or "board"


def text_h(text: str | None, title: str | None = None, width: int = COL_W) -> int:
    """Rough height estimate for a note card."""
    chars_per_line = max(18, int((width - 30) / 7.0))
    lines = 0
    for para in (text or "").split("\n"):
        lines += max(1, math.ceil(max(1, len(para)) / chars_per_line))
    h = 26 + lines * 19
    if title:
        h += 24
    return max(48, h)


def frame_ref(value: Any, fallback_w: Any = None, fallback_h: Any = None) -> dict[str, Any] | None:
    """Normalise a frame reference to {asset_id, width, height} or None."""
    if not value:
        return None
    if isinstance(value, str):
        ref: dict[str, Any] = {"asset_id": value}
    elif isinstance(value, dict) and value.get("asset_id"):
        ref = {"asset_id": value["asset_id"], "width": value.get("width"), "height": value.get("height")}
        if value.get("src"):
            ref["src"] = value["src"]
    else:
        return None
    if not ref.get("width"):
        ref["width"] = fallback_w
    if not ref.get("height"):
        ref["height"] = fallback_h
    return ref


def image_dims(ref: dict[str, Any] | None, width: int = COL_W) -> tuple[int, int]:
    w = (ref or {}).get("width")
    h = (ref or {}).get("height")
    try:
        if w and h and float(w) > 0 and float(h) > 0:
            return width, max(60, round(width * float(h) / float(w)))
    except (TypeError, ValueError):
        pass
    return width, max(60, round(width / DEFAULT_FRAME_ASPECT))


def lane_role(tl: dict[str, Any], index: int, count: int) -> str:
    """Explicit role > label regex > (last of many lanes = ours; single lane = ours)."""
    role = (tl.get("role") or "").lower()
    if role in ("ours", "reference"):
        return role
    if OURS_LABEL.search(tl.get("label") or ""):
        return "ours"
    if count == 1 or index == count - 1:
        return "ours"
    return "reference"


class _Builder:
    def __init__(self):
        self.cards: list[dict[str, Any]] = []
        self.lanes: list[dict[str, Any]] = []

    def add(self, **kw) -> dict[str, Any]:
        for k in ("x", "y", "w", "h"):
            kw[k] = round(kw.get(k, 0))
        self.cards.append(kw)
        return kw

    def lane(self, **kw) -> dict[str, Any]:
        for k in ("x", "y", "w", "h"):
            kw[k] = round(kw.get(k, 0))
        self.lanes.append(kw)
        return kw


def layout(spec: dict[str, Any]) -> dict[str, Any]:
    """Semantic spec -> {lanes, cards, edges}. Pure: no store, no files."""
    title = spec.get("title") or "Untitled brief"
    b = _Builder()
    x0, y = 0, 0

    # ---- header
    b.add(id="hdr-title", type="label", lane_id=None, x=x0, y=y, w=1200, h=52, text=title.upper(), size=34)
    y += 66
    if spec.get("summary"):
        h = text_h(spec["summary"], title="CONCEPT", width=760)
        b.add(id="hdr-summary", type="note", lane_id=None, x=x0, y=y, w=760, h=h, title="CONCEPT",
              text=spec["summary"], color=COLOR_NOTE)
        y += h + 30
    y += 20

    # ---- timelines
    timelines = [tl for tl in (spec.get("timelines") or []) if tl.get("beats")]
    for li, tl in enumerate(timelines):
        beats = tl.get("beats") or []
        lane_id = f"lane-{li}"
        lane_x, lane_y = x0, y
        col_x = lane_x + LANE_PAD
        max_bottom = lane_y + LANE_PAD + 10

        for bi, beat in enumerate(beats):
            cy = lane_y + LANE_PAD + 10
            cid = f"l{li}-b{bi}"
            if beat.get("t"):
                b.add(id=f"{cid}-t", type="label", lane_id=lane_id, beat=bi, x=col_x, y=cy, w=COL_W, h=24,
                      text=beat["t"], size=15, color="#8fa0b3")
                cy += 32
            if beat.get("script"):
                h = text_h(beat["script"], title="SCRIPT")
                b.add(id=f"{cid}-script", type="note", lane_id=lane_id, beat=bi, x=col_x, y=cy, w=COL_W, h=h,
                      title="SCRIPT", text=beat["script"], color=COLOR_SCRIPT)
                cy += h + STACK_GAP
            ref = frame_ref(beat.get("frame"), beat.get("frame_width"), beat.get("frame_height"))
            if ref:
                w, h = image_dims(ref)
                cap = beat.get("visual") or ""
                if cap:
                    h += 14 + min(3, math.ceil(len(cap) / 40)) * 15
                b.add(id=f"{cid}-frame", type="image", lane_id=lane_id, beat=bi, x=col_x, y=cy, w=w, h=h,
                      asset_id=ref["asset_id"], src=ref.get("src"), text=cap)
                cy += h + STACK_GAP
            elif beat.get("visual"):
                h = text_h(beat["visual"], title="VISUAL")
                b.add(id=f"{cid}-visual", type="note", lane_id=lane_id, beat=bi, x=col_x, y=cy, w=COL_W, h=h,
                      title="VISUAL", text=beat["visual"], color=COLOR_NOTE)
                cy += h + STACK_GAP
            emo = beat.get("emotion") or ""
            if beat.get("note"):
                emo = (emo + "\n\n" + beat["note"]).strip()
            if emo:
                h = text_h(emo, title="EMOTION")
                b.add(id=f"{cid}-emotion", type="note", lane_id=lane_id, beat=bi, x=col_x, y=cy, w=COL_W, h=h,
                      title="EMOTION", text=emo, color=COLOR_EMOTION)
                cy += h + STACK_GAP
            max_bottom = max(max_bottom, cy)
            col_x += COL_W + COL_GAP

        lane_w = max(600, col_x - lane_x - COL_GAP + LANE_PAD)
        lane_h = max_bottom - lane_y + LANE_PAD - STACK_GAP
        label = tl.get("label") or "TIMELINE"
        lane_title = label + ("  ·  " + tl["source"] if tl.get("source") else "")
        b.lane(id=lane_id, type="lane", label=label, source=tl.get("source"),
               role=lane_role(tl, li, len(timelines)), x=lane_x, y=lane_y, w=lane_w, h=lane_h,
               title=lane_title, beat_count=len(beats))
        y = lane_y + lane_h + LANE_GAP

    # ---- free notes
    notes = spec.get("notes") or []
    if notes:
        b.add(id="notes-title", type="label", lane_id=None, x=x0, y=y, w=600, h=36, text="NOTES", size=22)
        y += 48
        nx, row_h = x0, 0
        for i, n in enumerate(notes):
            h = text_h(n.get("text", ""), title=n.get("title"), width=300)
            if nx + 300 > x0 + 1360:
                nx = x0
                y += row_h + 20
                row_h = 0
            b.add(id=f"note-{i}", type="note", lane_id=None, x=nx, y=y, w=300, h=h,
                  title=n.get("title", ""), text=n.get("text", ""), color=n.get("color", COLOR_NOTE))
            nx += 320
            row_h = max(row_h, h)
        y += row_h + LANE_GAP

    # ---- moodboard
    mood = [(m, frame_ref(m.get("image") or m.get("asset_id"), m.get("width"), m.get("height")))
            for m in (spec.get("moodboard") or [])]
    mood = [(m, r) for m, r in mood if r]
    if mood:
        b.add(id="mood-title", type="label", lane_id=None, x=x0, y=y, w=600, h=36, text="MOODBOARD", size=22)
        y += 48
        nx, row_h = x0, 0
        for i, (m, ref) in enumerate(mood):
            w, h = image_dims(ref, width=240)
            if m.get("caption"):
                h += 26
            if nx + w > x0 + 1360:
                nx = x0
                y += row_h + 20
                row_h = 0
            b.add(id=f"mood-{i}", type="image", lane_id=None, x=nx, y=y, w=w, h=h,
                  asset_id=ref["asset_id"], src=ref.get("src"), text=m.get("caption", ""))
            nx += w + 20
            row_h = max(row_h, h)
        y += row_h

    return {"lanes": b.lanes, "cards": b.cards, "edges": list(spec.get("edges") or [])}


# ---------------------------------------------------------------------------
# store-backed operations
# ---------------------------------------------------------------------------

def board_url(slug: str) -> str:
    return f"{settings.public_base_url.rstrip('/')}/b/{slug}"


def _asset_url(st: Store, workspace: str, asset: dict[str, Any]) -> str | None:
    if asset.get("url"):
        return asset["url"]
    if asset.get("storage_key"):
        return st.url(workspace, asset["storage_key"])
    return None


def _hydrate(spec: dict[str, Any], st: Store, workspace: str) -> tuple[dict[str, Any], list[str]]:
    """Resolve frame asset ids against the store: fill missing dims + url. Returns (spec, warnings)."""
    spec = copy.deepcopy(spec)
    warnings: list[str] = []
    cache: dict[str, dict[str, Any] | None] = {}

    def lookup(asset_id: str) -> dict[str, Any] | None:
        if asset_id not in cache:
            try:
                cache[asset_id] = st.get("asset", workspace, asset_id)
            except (NotFound, ValueError):
                cache[asset_id] = None
        return cache[asset_id]

    def enrich(holder: dict[str, Any], key: str, w_key: str = "width", h_key: str = "height"):
        ref = frame_ref(holder.get(key), holder.get(w_key), holder.get(h_key))
        if not ref:
            if holder.get(key):
                warnings.append(f"ignored non-asset frame value {holder.get(key)!r} (frames are asset ids)")
                holder[key] = None
            return
        asset = lookup(ref["asset_id"])
        if asset is None:
            warnings.append(f"asset {ref['asset_id']} not found in workspace; card placed without a url")
        else:
            meta = asset.get("meta") or {}
            ref.setdefault("width", None)
            if not ref.get("width") and meta.get("width"):
                ref["width"] = meta["width"]
            if not ref.get("height") and meta.get("height"):
                ref["height"] = meta["height"]
            ref["src"] = _asset_url(st, workspace, asset)
        holder[key] = ref

    for tl in spec.get("timelines") or []:
        for beat in tl.get("beats") or []:
            enrich(beat, "frame", "frame_width", "frame_height")
    for m in spec.get("moodboard") or []:
        if m.get("asset_id") and not m.get("image"):
            m["image"] = m.pop("asset_id")
        enrich(m, "image")
    return spec, warnings


def find_board(st: Store, workspace: str, slug: str) -> dict[str, Any]:
    rows = st.find("board", workspace, slug=slug)
    if not rows:
        raise NotFound(f"board not found: {slug}")
    return rows[0]


@require_write
def push_board(brand_slug: str, spec: dict[str, Any], slug: str | None = None) -> dict[str, Any]:
    if not isinstance(spec, dict) or not spec.get("title"):
        return {"error": "spec must be a dict with at least a title"}
    brand = brand_by_slug(brand_slug)
    st, workspace = store(), ws()
    slug = slugify(slug or spec["title"])
    hydrated, warnings = _hydrate(spec, st, workspace)
    laid = layout(hydrated)

    fields = {"brand_id": brand["id"], "slug": slug, "title": spec["title"],
              "summary": spec.get("summary") or "", "project": spec.get("project") or brand_slug,
              "lanes": laid["lanes"], "cards": laid["cards"], "edges": laid["edges"],
              "spec": spec, "warnings": warnings}
    try:
        existing = find_board(st, workspace, slug)
    except NotFound:
        existing = None
    if existing is not None and existing.get("brand_id") not in (None, brand["id"]):
        return {"error": f"slug '{slug}' already belongs to another brand in this workspace; pass a different slug"}
    if existing is None:
        rec = st.create("board", workspace, "brd", version=1, **fields)
    else:
        rec = st.update("board", workspace, existing["id"], version=int(existing.get("version", 1)) + 1, **fields)
    return {"board_id": rec["id"], "slug": slug, "url": board_url(slug), "version": rec["version"],
            "card_count": len(laid["cards"]), "lane_count": len(laid["lanes"]),
            "lanes": [{"id": l["id"], "label": l["label"], "role": l["role"], "beats": l["beat_count"]}
                      for l in laid["lanes"]],
            "warnings": warnings,
            "next": "Hand the url to the editor. Keyframes on OUR VERSION cards need approve_card before animation."}


def latest_approvals(st: Store, workspace: str, board_id: str) -> dict[str, dict[str, Any]]:
    """card_id -> most recent approval record."""
    latest: dict[str, dict[str, Any]] = {}
    for a in st.find("approval", workspace, board_id=board_id):
        cur = latest.get(a["card_id"])
        if cur is None or a.get("at", 0) > cur.get("at", 0):
            latest[a["card_id"]] = a
    return latest


def card_fingerprint(board: dict, card: dict) -> str:
    """Bind approval to the beat's content, including script, not canvas placement."""
    keys = ("id", "type", "lane_id", "beat", "asset_id", "text", "title")
    siblings = [c for c in board.get("cards", [])
                if c.get("lane_id") == card.get("lane_id") and c.get("beat") == card.get("beat")]
    payload = [{k: c.get(k) for k in keys} for c in sorted(siblings, key=lambda c: c["id"])]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def _card_state(card: dict[str, Any], approval: dict[str, Any] | None,
                fingerprint: str) -> dict[str, Any] | None:
    """Legacy approvals without a content fingerprint require reapproval."""
    if approval is None:
        return None
    if (approval.get("asset_id") != card.get("asset_id")
            or approval.get("fingerprint") != fingerprint):
        return {"state": "stale", "previous": approval.get("state"), "member_id": approval.get("member_id"),
                "at": approval.get("at"), "note": approval.get("note")}
    return {"state": approval.get("state"), "member_id": approval.get("member_id"),
            "at": approval.get("at"), "note": approval.get("note")}


def get_board(brand_slug: str, slug: str) -> dict[str, Any]:
    brand = brand_by_slug(brand_slug)
    st, workspace = store(), ws()
    rec = find_board(st, workspace, slug)
    if rec.get("brand_id") != brand["id"]:
        raise NotFound(f"board '{slug}' does not belong to brand '{brand_slug}'")
    latest = latest_approvals(st, workspace, rec["id"])
    cards = []
    for c in rec.get("cards") or []:
        c = dict(c)
        c["approval"] = _card_state(c, latest.get(c["id"]), card_fingerprint(rec, c))
        cards.append(c)
    return {"board_id": rec["id"], "slug": slug, "url": board_url(slug), "title": rec.get("title"),
            "summary": rec.get("summary"), "project": rec.get("project"), "version": rec.get("version"),
            "updated": rec.get("updated"), "lanes": rec.get("lanes") or [], "cards": cards,
            "edges": rec.get("edges") or [], "warnings": rec.get("warnings") or [],
            "approval": approval_status(st, workspace, slug)}


def list_boards(brand_slug: str | None = None) -> list[dict[str, Any]]:
    st, workspace = store(), ws()
    rows = st.find("board", workspace, **({"brand_id": brand_by_slug(brand_slug)["id"]} if brand_slug else {}))
    return [{"board_id": r["id"], "slug": r["slug"], "title": r.get("title"), "project": r.get("project"),
             "version": r.get("version"), "url": board_url(r["slug"]),
             "updated": time.strftime("%Y-%m-%d %H:%M", time.gmtime(r.get("updated", 0)))} for r in rows]


def approve_card(slug: str, card_id: str, state: str, note: str | None = None) -> dict[str, Any]:
    """The human gate. Requires an approver (owner/editor); an agent role is refused."""
    ctx = current()
    if not ctx.can_approve():
        raise Forbidden(f"role '{ctx.role}' cannot approve; an approver with editor rights must approve on the board")
    if state not in APPROVAL_STATES:
        return {"error": f"state must be one of {list(APPROVAL_STATES)}"}
    st, workspace = store(), ws()
    rec = find_board(st, workspace, slug)
    card = next((c for c in rec.get("cards") or [] if c.get("id") == card_id), None)
    if card is None:
        return {"error": f"card '{card_id}' not on board '{slug}'",
                "cards": [c["id"] for c in rec.get("cards") or []]}
    approval = st.create("approval", workspace, "apr", board_id=rec["id"], card_id=card_id,
                         asset_id=card.get("asset_id"), member_id=ctx.member_id, state=state,
                         note=note or "", at=time.time(), fingerprint=card_fingerprint(rec, card))
    return {"approval_id": approval["id"], "board_id": rec["id"], "slug": slug, "card_id": card_id,
            "asset_id": card.get("asset_id"), "state": state, "member_id": ctx.member_id,
            "at": approval["at"], "board": approval_status(st, workspace, slug)}


def approval_status(store_: Store, workspace: str, slug: str) -> dict[str, Any]:
    """Plain function (no auth context needed) so the gen server can gate animation on it.
    Every beat in OUR VERSION needs media, and every media card needs current approval."""
    rec = find_board(store_, workspace, slug)
    ours = {l["id"] for l in rec.get("lanes") or [] if l.get("role") == "ours"}
    latest = latest_approvals(store_, workspace, rec["id"])
    gated = [c for c in rec.get("cards") or []
             if c.get("lane_id") in ours and c.get("type") == "image" and c.get("asset_id")]
    approved, rejected, pending = [], [], []
    missing = []
    for lane in rec.get("lanes") or []:
        if lane["id"] not in ours:
            continue
        for beat in range(lane.get("beat_count", 0)):
            if not any(c.get("lane_id") == lane["id"] and c.get("beat") == beat for c in gated):
                missing.append({"lane_id": lane["id"], "beat": beat, "reason": "missing media"})
    for c in gated:
        s = _card_state(c, latest.get(c["id"]), card_fingerprint(rec, c))
        entry = {"card_id": c["id"], "asset_id": c.get("asset_id"), "beat": c.get("beat"), "lane_id": c.get("lane_id")}
        try:
            store_.get("asset", workspace, c["asset_id"])
        except (NotFound, ValueError):
            pending.append({**entry, "reason": "asset not found in workspace"})
            continue
        if s and s["state"] == "approved":
            approved.append(entry)
        elif s and s["state"] == "rejected":
            rejected.append({**entry, "note": s.get("note")})
        else:
            pending.append({**entry, "stale": bool(s and s["state"] == "stale")})
    return {"slug": slug, "board_id": rec["id"], "version": rec.get("version"),
            "approved": bool(gated) and not rejected and not pending and not missing,
            "total": len(gated) + len(missing), "approved_count": len(approved),
            "approved_cards": approved, "missing": missing,
            "rejected": rejected, "pending": pending,
            "note": ("No OUR VERSION card carries an asset yet; push keyframes first." if not gated
                     else "animate_scenes verifies this state server-side before rendering.")}


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------

_EXPORT_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#1e2126;color:#e8eaed}
#viewport{position:absolute;inset:0;overflow:hidden;cursor:grab;background-image:radial-gradient(#2b2f36 1.2px, transparent 1.2px);background-size:26px 26px}
#world{position:absolute;top:0;left:0;transform-origin:0 0}
.card{position:absolute;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.35)}
.card.note{background:#f7f5ee;color:#26282c;padding:12px 14px;overflow:hidden}
.card.note .ctitle{font-weight:700;font-size:13px;margin-bottom:6px}
.card.note .ctext{font-size:12.5px;line-height:1.45;white-space:pre-wrap;word-wrap:break-word}
.card.image{background:#111;overflow:hidden;display:flex;flex-direction:column}
.card.image img{flex:1;width:100%;object-fit:cover;min-height:0}
.card.image .cap{background:#15171b;color:#cfd5dc;font-size:11px;padding:6px 9px;line-height:1.35}
.card.image .cap:empty{display:none}
.card.image .badge{position:absolute;top:6px;right:6px;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:2px 7px;border-radius:6px;background:#3a4049;color:#e8eaed}
.card.image .badge.approved{background:#2e7d4f}.card.image .badge.rejected{background:#a33a3a}.card.image .badge.stale{background:#8a6d1f}
.card.label{background:transparent;box-shadow:none;color:#e8eaed;font-weight:800;display:flex;align-items:flex-end;padding:4px 2px}
.card.lane{background:rgba(255,255,255,.028);border:1px dashed #444b56;box-shadow:none;border-radius:14px}
.card.lane .lane-title{position:absolute;top:-11px;left:18px;background:#1e2126;padding:2px 10px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#9aa3ad}
#bar{position:fixed;top:12px;left:14px;z-index:10;background:rgba(38,42,49,.9);border:1px solid #3a4049;border-radius:10px;padding:8px 14px;font-size:13px;font-weight:600}
</style></head><body>
<div id="bar">__TITLE__ · v__VERSION__ · scroll to pan, pinch/ctrl-scroll to zoom</div>
<div id="viewport"><div id="world"></div></div>
<script>
const board = __BOARD__;
const world = document.getElementById('world'), viewport = document.getElementById('viewport');
let view = {x:60, y:60, s:1};
const order = {lane:0,label:1,image:2,note:3};
[...board.cards].sort((a,b)=>(order[a.type]??2)-(order[b.type]??2)).forEach(c=>{
  const el = document.createElement('div');
  el.className = 'card '+c.type;
  el.style.cssText = `left:${c.x}px;top:${c.y}px;width:${c.w}px;height:${c.h}px`;
  if(c.type==='note'){
    el.style.background = c.color||'#f7f5ee';
    const t=document.createElement('div'); t.className='ctitle'; t.textContent=c.title||'';
    const x=document.createElement('div'); x.className='ctext'; x.textContent=c.text||'';
    if(c.title) el.appendChild(t); el.appendChild(x);
  } else if(c.type==='image'){
    const im=document.createElement('img'); if(c.src) im.src=c.src; im.alt=c.asset_id||'';
    const cap=document.createElement('div'); cap.className='cap'; cap.textContent=c.text||'';
    el.appendChild(im); el.appendChild(cap);
    if(c.approval&&c.approval.state){ const b=document.createElement('div'); b.className='badge '+c.approval.state; b.textContent=c.approval.state; el.appendChild(b); }
  } else if(c.type==='label'){
    el.style.fontSize=(c.size||22)+'px'; if(c.color) el.style.color=c.color;
    el.textContent=c.text||'';
  } else if(c.type==='lane'){
    const t=document.createElement('div'); t.className='lane-title'; t.textContent=c.title||'';
    el.appendChild(t);
  }
  world.appendChild(el);
});
function apply(){ world.style.transform=`translate(${view.x}px,${view.y}px) scale(${view.s})`; }
function fit(){
  if(!board.cards.length) return apply();
  const xs=board.cards.map(c=>c.x), ys=board.cards.map(c=>c.y);
  const xe=board.cards.map(c=>c.x+c.w), ye=board.cards.map(c=>c.y+c.h);
  const minX=Math.min(...xs)-60, minY=Math.min(...ys)-60;
  const w=Math.max(...xe)-minX+60, h=Math.max(...ye)-minY+60;
  const r=viewport.getBoundingClientRect();
  const s=Math.min(1.6, Math.min(r.width/w, r.height/h));
  view={s, x:(r.width-w*s)/2-minX*s, y:(r.height-h*s)/2-minY*s}; apply();
}
viewport.addEventListener('pointerdown', e=>{
  const sx=e.clientX, sy=e.clientY, ox=view.x, oy=view.y;
  const mv = ev=>{ view.x=ox+ev.clientX-sx; view.y=oy+ev.clientY-sy; apply(); };
  const up = ()=>{ window.removeEventListener('pointermove',mv); window.removeEventListener('pointerup',up); };
  window.addEventListener('pointermove',mv); window.addEventListener('pointerup',up);
});
viewport.addEventListener('wheel', e=>{
  e.preventDefault();
  if(e.ctrlKey||e.metaKey){
    const ns=Math.min(2.5,Math.max(.08,view.s*Math.exp(-e.deltaY*.01)));
    const r=viewport.getBoundingClientRect();
    const px=(e.clientX-r.left-view.x)/view.s, py=(e.clientY-r.top-view.y)/view.s;
    view.s=ns; view.x=e.clientX-r.left-px*ns; view.y=e.clientY-r.top-py*ns; apply();
  } else { view.x-=e.deltaX; view.y-=e.deltaY; apply(); }
},{passive:false});
window.addEventListener('resize', fit);
fit();
</script></body></html>"""


def export_board(slug: str) -> str:
    """Self-contained read-only HTML. Images reference their asset urls (no base64)."""
    st, workspace = store(), ws()
    rec = find_board(st, workspace, slug)
    latest = latest_approvals(st, workspace, rec["id"])
    cards = [{"id": l["id"], "type": "lane", "x": l["x"], "y": l["y"], "w": l["w"], "h": l["h"],
              "title": l.get("title")} for l in rec.get("lanes") or []]
    for c in rec.get("cards") or []:
        c = dict(c)
        c["approval"] = _card_state(c, latest.get(c["id"]), card_fingerprint(rec, c))
        cards.append(c)
    board = {"id": slug, "title": rec.get("title"), "version": rec.get("version"), "cards": cards,
             "edges": rec.get("edges") or []}
    payload = json.dumps(board).replace("</", "<\\/")
    return (_EXPORT_TEMPLATE
            .replace("__TITLE__", html.escape(rec.get("title") or slug))
            .replace("__VERSION__", str(rec.get("version", 1)))
            .replace("__BOARD__", payload))
