"""Thin task runner using the existing Kie engine; no custom API endpoints."""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
sys.path.insert(0, str(REPO / "_engine/mcp/ad-engine"))
import db
from engines import kie


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["submit", "poll"])
    args = parser.parse_args()
    path = ROOT / "prompts-and-provenance.json"
    manifest = json.loads(path.read_text())
    db.init_db()

    def save():
        path.write_text(json.dumps(manifest, indent=2) + "\n")

    if args.action == "submit":
        if not manifest.get("uploaded_source_url"):
            manifest["uploaded_source_url"] = kie.upload(
                manifest["source"]["path"], upload_path="velantra-craftsmanship-2026-09-05"
            )
            save()
        for panel in manifest["panels"]:
            if panel["status"] != "planned":
                continue
            source_url = manifest["uploaded_source_url"]
            if panel.get("source_crop"):
                source_url = kie.upload(panel["source_crop"]["path"], upload_path="velantra-craftsmanship-2026-09-05")
                panel["source_crop"]["uploaded_url"] = source_url
                save()
            balance = kie.balance()
            if balance is None or balance < 100:
                raise RuntimeError(f"Cannot submit: available credits {balance}")
            panel["credits_before_submission"] = balance
            result = kie.generate(
                manifest["model"],
                {"prompt": panel["prompt"], "input_urls": [source_url],
                 "aspect_ratio": manifest["aspect_ratio"], "resolution": manifest["resolution"]},
                brand="velantra", concept="craftsmanship-followup-2026-09-05",
            )
            panel["submission"] = result
            panel["status"] = result["status"]
            save()
            print(panel["id"], result, flush=True)
        return

    for panel in manifest["panels"]:
        if panel["status"] != "running":
            continue
        result = kie.status(panel["submission"]["job_id"])
        panel["status"] = result["status"]
        (ROOT / "receipts").mkdir(exist_ok=True)
        (ROOT / "receipts" / (panel["id"] + ".json")).write_text(json.dumps(result, indent=2) + "\n")
        if result["status"] == "success":
            assets = db.list_assets(job_id=panel["submission"]["job_id"], limit=10)
            asset = next(a for a in assets if a.get("path"))
            (ROOT / "final").mkdir(exist_ok=True)
            dest = ROOT / "final" / (panel["id"] + ".png")
            shutil.copy2(asset["path"], dest)
            panel["output"] = str(dest)
            panel["output_sha256"] = hashlib.sha256(dest.read_bytes()).hexdigest()
            panel["provider_asset"] = asset
        save()
        print(panel["id"], panel["status"], panel.get("output", ""), flush=True)


if __name__ == "__main__":
    main()
