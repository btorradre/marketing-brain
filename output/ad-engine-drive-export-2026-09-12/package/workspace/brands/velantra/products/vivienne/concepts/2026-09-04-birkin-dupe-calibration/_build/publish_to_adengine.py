#!/usr/bin/env python3
"""Publish the current storyboard into the productized ad-engine Store.

This uses the same workspace-scoped asset, reference, artifact, concept and
board records the hosted app uses. It never approves its own keyframes.
"""

from __future__ import annotations

import copy
import base64
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETING_BRAIN = ROOT.parents[5]
APP = MARKETING_BRAIN.parent / "marketing-apps" / "adengine"
APP_DATA = APP / "data" / "local"
WORKSPACE = "velantra-studio"

os.environ.setdefault("ADENGINE_DATA_DIR", str(APP_DATA))
os.environ.setdefault("ADENGINE_DEV_WORKSPACE", WORKSPACE)
os.environ.setdefault("ADENGINE_PUBLIC_URL", "http://localhost:3000")
sys.path.insert(0, str(APP / "services" / "engine"))

from adengine.core import get_store  # noqa: E402
from adengine.core.auth import AuthContext, set_auth_context  # noqa: E402
from adengine.dr import artifacts, boards, tracker  # noqa: E402
from adengine.gen import registry as registry  # noqa: E402


SOURCE_URL = "https://www.instagram.com/reel/DckbXyGt785/"
MASTER = (
    MARKETING_BRAIN
    / "brands/velantra/products/vivienne/product-images/master/VIVIENNE-MASTER-chocolate-front.png"
)
SOURCE_VIDEO = MARKETING_BRAIN / "_engine/mcp/ad-engine/data/downloads/job_5e513b03bc63/source.mp4"
WATCH_DIR = MARKETING_BRAIN / "_engine/mcp/ad-engine/data/watch/job_cc6efc9d4bef"


def image_meta(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
         "-of", "json", str(path)], capture_output=True, text=True, check=True,
    )
    stream = json.loads(out.stdout)["streams"][0]
    return {"width": stream["width"], "height": stream["height"]}


def ensure_asset(store, path: Path, key: str, *, role: str, extra: dict | None = None) -> dict:
    source_path = str(path)
    meta = {"source_path": source_path, "role": role, **(extra or {})}
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        meta.update(image_meta(path))
    existing = next(
        (a for a in store.find("asset", WORKSPACE) if (a.get("meta") or {}).get("source_path") == source_path),
        None,
    )
    if existing:
        store.put_blob(WORKSPACE, existing["storage_key"], path.read_bytes(), mime=existing["mime"])
        return store.update("asset", WORKSPACE, existing["id"], meta=meta)
    return registry.put_file_asset(store, WORKSPACE, str(path), key, meta=meta)


def ensure_brand(store) -> dict:
    rows = store.find("brand", WORKSPACE, slug="velantra")
    fields = {
        "name": "Velantra",
        "code": "VEL",
        "brief": {
            "positioning": "Understated handbags with visible design detail and practical purchase information.",
            "creator_voice": "Natural customer language grounded in authenticated experience.",
        },
        "house_laws": [
            "No current offer amounts or price badges in ads.",
            "Use Google Omni for video generation and GPT Image 2 for image production.",
            "Use the internal video editor for actual editing.",
            "HyperFrames and Remotion are banned.",
            "Preserve product identity from the approved product reference.",
        ],
    }
    if rows:
        return store.update("brand", WORKSPACE, rows[0]["id"], **fields)
    return store.create("brand", WORKSPACE, "brand", slug="velantra", **fields)


def ensure_product(store, brand: dict, master_asset_id: str) -> dict:
    rows = store.find("product", WORKSPACE, brand_id=brand["id"], slug="vivienne")
    truth = {
        "display_name": "The Vivienne Top Handle Bag",
        "catalog_handle": "velantra-vivienne",
        "shopify_product_id": "8050561876033",
        "selected_variant": "Chocolate",
        "reference_asset_ids": [master_asset_id],
        "source_status": "owner-selected generated design target dated 2026-09-03; not physically measured",
        "visual_locks": [
            "wide soft slouch",
            "grainy dark-chocolate matte/satin body",
            "smoother warmer-cognac trim",
            "braided upper edge",
            "two upright rolled handles",
            "left hanging key bell",
            "reinforced corner caps",
            "horizontal oval antique-gold center fitting with two rivets and central post",
            "parallel antique-gold side bars",
            "both belt tails falling inward with slotted gold ends",
            "raised-flap state",
            "no front logo",
        ],
        "unknown_or_forbidden_inference": [
            "rear, interior, base and closure mechanism",
            "capacity and laptop fit",
            "long-strap implementation",
            "measured physical scale",
        ],
        "nominal_dimensions_cm": {"width": 38, "height": 27, "depth": 20, "status": "owner-approved/inferred"},
    }
    fields = {"name": "The Vivienne Top Handle Bag", "code": "VIV", "truth": truth}
    if rows:
        return store.update("product", WORKSPACE, rows[0]["id"], **fields)
    return store.create("product", WORKSPACE, "prod", brand_id=brand["id"], slug="vivienne", **fields)


def ensure_reference(store, brand: dict, video_asset: dict, frame_assets: dict[str, dict]) -> dict:
    watch = json.loads((ROOT / "reference" / "watch.json").read_text())
    old_manifest = watch["output"]["manifest"]
    manifest = {
        "source": video_asset["id"],
        "transcript_source": old_manifest.get("transcript_source"),
        "overall": old_manifest.get("overall"),
        "beats": [],
        "provenance": "migrated from successful watch job_cc6efc9d4bef",
    }
    for beat in old_manifest.get("beats", []):
        name = Path(beat["frame"]).name
        item = {k: v for k, v in beat.items() if k not in {"frame", "clip"}}
        item["frame_asset_id"] = frame_assets[name]["id"]
        item["frame_url"] = frame_assets[name]["url"]
        manifest["beats"].append(item)
    rows = store.find("reference", WORKSPACE, source=SOURCE_URL)
    if rows:
        return store.update(
            "reference", WORKSPACE, rows[0]["id"], brand_id=brand["id"], asset_id=video_asset["id"],
            manifest=manifest, status="watched", watch_job_id="job_cc6efc9d4bef",
        )
    return registry.create_reference(
        store, WORKSPACE, SOURCE_URL, asset_id=video_asset["id"], status="watched",
        brand_id=brand["id"], manifest=manifest,
    )


def replace_frames(spec: dict, assets_by_path: dict[str, dict]) -> dict:
    out = copy.deepcopy(spec)
    for timeline in out.get("timelines", []):
        for beat in timeline.get("beats", []):
            asset = assets_by_path[beat["frame"]]
            beat["frame"] = {"asset_id": asset["id"], **image_meta(Path((asset.get("meta") or {})["source_path"]))}
    for mood in out.get("moodboard", []):
        asset = assets_by_path[mood["image"]]
        mood["image"] = {"asset_id": asset["id"], **image_meta(Path((asset.get("meta") or {})["source_path"]))}
    return out


def main() -> None:
    set_auth_context(AuthContext(workspace_id=WORKSPACE, member_id="root-creative-author", role="agent"))
    store = get_store()
    brand = ensure_brand(store)

    registered: dict[str, dict] = {}
    master = ensure_asset(store, MASTER, "velantra/vivienne/product-master-chocolate.png", role="product-master")
    registered[str(MASTER)] = master
    product = ensure_product(store, brand, master["id"])

    video_asset = ensure_asset(store, SOURCE_VIDEO, "references/DckbXyGt785/source.mp4", role="reference-video")
    frame_assets: dict[str, dict] = {}
    for p in sorted((WATCH_DIR / "frames").glob("beat_*.jpg")):
        asset = ensure_asset(store, p, f"references/DckbXyGt785/frames/{p.name}", role="reference-frame")
        frame_assets[p.name] = asset
        registered[str(p)] = asset
    reference = ensure_reference(store, brand, video_asset, frame_assets)

    for p in sorted((ROOT / "visuals" / "storyboard").glob("[0-9][0-9]-*.jpg")):
        registered[str(p)] = ensure_asset(
            store, p, f"velantra/vivienne/birkin-dupe/storyboard/{p.name}", role="storyboard-keyframe",
            extra={"generated": True, "approval_state": "pending"},
        )
    for p in sorted((ROOT / "visuals" / "generated").glob("*.png")):
        registered[str(p)] = ensure_asset(
            store, p, f"velantra/vivienne/birkin-dupe/generated/{p.name}", role="generated-plate",
            extra={"generated": True, "model_workflow": "GPT Image 2"},
        )
    anna_path = ROOT / "visuals" / "presenter" / "anna-keyed.png"
    registered[str(anna_path)] = ensure_asset(
        store, anna_path, "velantra/vivienne/birkin-dupe/presenter/anna-keyed.png", role="presenter-reference",
        extra={"provider": "heygen", "avatar_name": "Anna", "look_id": "abb163c6fe0d4880863c30a2323394ca"},
    )

    local_spec = json.loads((ROOT / "storyboard-v5.json").read_text())
    app_spec = replace_frames(local_spec, registered)
    board = boards.push_board("velantra", app_spec, slug="vivienne-birkin-inspired-ai-ugc")

    # The hosted board UI is not in this repository yet. Keep a self-contained
    # export beside the concept so the exact app record is still reviewable.
    board_html = boards.export_board(board["slug"])
    board_rec = store.one("board", WORKSPACE, slug=board["slug"])
    for card in board_rec.get("cards") or []:
        if card.get("type") != "image" or not card.get("asset_id"):
            continue
        asset = store.get("asset", WORKSPACE, card["asset_id"])
        path = Path(store.blob_path(WORKSPACE, asset["storage_key"]))
        data_uri = f"data:{asset['mime']};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
        board_html = board_html.replace(asset["url"], data_uri)
    board_export = ROOT / "adengine-board.html"
    board_export.write_text(board_html)

    adaptation = {
        "golden_nugget": "A recognizable designer shape becomes trustworthy when a real frustration leads to visible product proof and an authenticated use story.",
        "reference_id": reference["id"],
        "reference_watch_job": "job_cc6efc9d4bef",
        "mirror_contract": "Stable vertical product background; presenter lower right; bold headline; speech captions; quick find/reveal/proof/CTA sequence.",
        "forced_deviations": [
            "No price or offer amount appears.",
            "Longer authenticated personal narrative extends the runtime from 19.3s to a provisional 33.75s.",
            "CTA uses the link below because comment automation is not verified.",
        ],
        "continuity_groups": {
            "anna": {"provider": "heygen", "look_id": "abb163c6fe0d4880863c30a2323394ca", "member_beats": [f"V{i:02d}" for i in range(1, 9)]},
            "hero_plate": {"member_beats": ["V01", "V02", "V03", "V04", "V07", "V08"]},
            "detail_plate": {"member_beats": ["V05"]},
            "daily_driver_plate": {"member_beats": ["V06"]},
        },
        "authenticity": {"presenter": "AI avatar explicitly directed by user", "product": "generated stills locked to approved master", "action_broll": "none"},
    }
    saved_plan = artifacts.save_artifact(
        "velantra", "adaptation-plan", json.dumps(adaptation, indent=2), name="vivienne-birkin-inspired-ai-ugc",
        sources=[SOURCE_URL, reference["id"]], generated_by="adengine-storyboard-run",
    )
    saved_brief = artifacts.save_artifact(
        "velantra", "brief", json.dumps(local_spec, indent=2), name="vivienne-birkin-inspired-ai-ugc",
        speaker="creator", sources=[SOURCE_URL, reference["id"], master["id"]], generated_by="adengine-storyboard-run",
    )
    if not saved_plan.get("saved") or not saved_brief.get("saved"):
        raise RuntimeError(json.dumps({"plan": saved_plan, "brief": saved_brief}, indent=2))

    existing_concept = next(
        (c for c in store.find("concept", WORKSPACE, brand_id=brand["id"])
         if (c.get("fields") or {}).get("concept") == "Birkin-inspired personal find"),
        None,
    )
    if existing_concept:
        concept = {"ok": True, "concept_id": existing_concept["id"], "asset_code": existing_concept["asset_code"], "reused": True}
    else:
        concept = tracker.push_concept(
            "velantra", "vivienne", "Birkin-inspired personal find",
            "A01 designer-shape without designer friction",
            "Authenticated frustration plus visible Vivienne details makes the familiar silhouette feel credible and desirable.",
            format="video", type="net-new", source=SOURCE_URL,
            notes="AI UGC greenscreen; Anna; Woman Over 40; no current offer amount; board approval required.",
        )

    result = {
        "workspace": WORKSPACE,
        "data_dir": str(APP_DATA),
        "brand_id": brand["id"],
        "product_id": product["id"],
        "reference_id": reference["id"],
        "board": board,
        "board_export": str(board_export),
        "approval": boards.approval_status(store, WORKSPACE, board["slug"]),
        "adaptation_plan": {k: saved_plan.get(k) for k in ("id", "name", "version", "saved")},
        "brief": {k: saved_brief.get(k) for k in ("id", "name", "version", "saved")},
        "concept": concept,
        "registered_asset_count": len(registered) + 1,
        "next": "A human owner/editor approves every OUR VERSION image card in the app before VO, avatar animation, Google Omni motion, or final editing.",
    }
    (ROOT / "adengine-run.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
