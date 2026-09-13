"""Index reviewed native films without modifying any media."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
FAMILIES = ("weekender", "meridian", "camille", "colette", "delphine", "juliette")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


deliveries = []
pending = []
for family in FAMILIES:
    path = BASE / family / "delivery.json"
    if not path.exists():
        pending.append(family)
        continue
    delivery = json.loads(path.read_text())
    assert delivery["status"] == "approved", path
    assert sha256(delivery["video"]) == delivery["video_sha256"], path
    assert sha256(delivery["poster"]) == delivery["poster_sha256"], path
    assert Path(delivery["qa"]).is_file(), path
    for source in delivery["sources"]:
        assert sha256(source["path"]) == source["sha256"], source["path"]
    deliveries.append({"family": family, "manifest": str(path), **delivery})

result = {
    "updated_utc": datetime.now(timezone.utc).isoformat(),
    "target_families": list(FAMILIES),
    "approved_count": len(deliveries),
    "pending_families": pending,
    "all_native_video_and_poster_hashes_verified": True,
    "all_input_source_hashes_verified": True,
    "physical_scale": "Not measured or certified by generated media.",
    "hosting": "Root owns Shopify hosting and draft-theme assignments.",
    "films": deliveries,
}
(BASE / "delivery-index.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"approved": len(deliveries), "pending": pending,
                  "index": str(BASE / "delivery-index.json")}))
