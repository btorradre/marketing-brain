#!/usr/bin/env python3
"""One-time builder for the Velantra Creative Tracker Google Sheet.

Creates the spreadsheet with two tabs (Active Creatives, Net New Concepts),
fills Active Creatives from the Triple Whale roster pulls in the scratchpad,
formats headers, shares with btorradre@gmail.com, and saves the spreadsheet id
to sheet_config.json. Re-running rebuilds the Active Creatives tab in place.
"""
import json
import sys
from pathlib import Path

from sheets_common import CONFIG, HERE, drive_service, sheets_service

SCRATCH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/"
    "a6bf2018-f030-4ff5-b385-3835bce35a80/scratchpad")

TITLE = "Velantra Creative Tracker"
SHARE_WITH = "btorradre@gmail.com"

ACTIVE_HEADERS = ["Ad Name", "Product", "Concept", "Angle", "Thesis", "Format",
                  "Campaign", "Spend 30d", "Conv 30d", "CPA", "ROAS",
                  "Winner / Loser", "Ads Manager Link", "Creative Preview"]
NETNEW_HEADERS = ["Date Added", "Product", "Concept Name", "Angle", "Thesis",
                  "Format", "Type", "Source", "Status", "Ad ID (once live)",
                  "Notes"]

# name-prefix -> (product, concept, angle, thesis)
CONCEPT_MAP = [
    ("founder h", "Weekender", "Founder story to camera",
     "Brooks tells the founding story, 2/3 face + 1/3 b-roll; h1-h4 = hook variants",
     "Founder credibility + story converts cold traffic better than faceless UGC; the format carve-out that beat the no-founder rule"),
    ("velantra weekender intro", "Weekender", "Product intro film",
     "Straightforward 'meet the bag' feature tour",
     "A new product captures existing demand fastest with a clean introduction before clever angles"),
    ("general travel", "Weekender", "Travel VO b-roll",
     "Faceless travel-aspiration b-roll with a single seamless VO",
     "Faceless VO sidesteps creator discontinuity and lets travel aspiration carry the sell"),
    ("fall travel", "Weekender", "Travel VO b-roll",
     "Fall-trip variant of the travel VO concept",
     "Season-pegged variant of the proven faceless travel VO structure"),
    ("VEL-CARRYON-", "Weekender", "Carry-on dynamics",
     "Trip-pegged practical hooks: friday flight / packs 3 days / rides on your carry-on",
     "Trip planners buy on practical compliance; personal-item fit is the hardest RTB we own"),
    ("VEL-CLAY-", "Weekender", "Claymation brand film",
     "Whimsical claymation travel vignette",
     "Hard pattern interrupt in a feed of lookalike UGC; brand warmth without creator cost"),
    ("VEL-WEEKENDER-ONROUTE-", "Weekender", "Onroute replication",
     "NYC in-transit POV, competitor structure ported",
     "The onroute structure is proven; porting it with our bag as hero inherits its retention curve"),
    ("VEL-WEEKENDER-BUILT-CRAFT-", "Weekender", "Built craft film",
     "Construction/materials craft story",
     "Craft justifies price; hooks are elite (52%+) so the close is the variable being fixed"),
    ("VEL-BACKINSTOCK-eleanor", "Eleanor", "Back-in-stock static",
     "Scarcity restock announcement per colorway",
     "Restock scarcity converts warm demand that missed the colorway the first time"),
    ("eleanor-girl-math", "Eleanor", "Girl-math UGC",
     "Cost-per-wear rationalization in trend-native voice; hooks b/c = variants",
     "Trend-native math gives permission to buy; redirect of a swiped mechanism onto our product"),
    ("VEL-ELEANOR-MOF-REVIEW-", "Eleanor", "MOF review static",
     "Real customer review quote over product shot",
     "Verbatim review language is the strongest MOF proof for warm retargeting"),
    ("a-preorder-open", "Colette", "Preorder open announcement",
     "Preorder is open + honest ship date",
     "Launch announcement converts the earliest warm demand; no review ports on a preorder product"),
    ("b-manifesto", "Colette", "Fall manifesto",
     "Editorial seasonal brand manifesto",
     "Seasonal identity piece primes the fall wardrobe purchase before urgency angles run"),
    ("c-feels-like-a-coat", "Colette", "Feels like a coat",
     "'Feels like your favorite fall coat' emotional comparison",
     "Familiar-comfort metaphor transfers existing fall-coat affection onto the bag"),
    ("d-one-bag", "Colette", "One bag",
     "The one bag for all of fall",
     "Decision-fatigue relief for the capsule-wardrobe shopper"),
    ("e-everything-bag", "Colette", "Everything bag",
     "Fits everything capacity claim",
     "Capacity is the most repeated purchase driver in bag VOC; lead with it plainly"),
    ("f-first-bag-of-fall", "Colette", "First bag of fall",
     "Seasonal newness ritual",
     "'First X of fall' taps the season-turn shopping ritual moment"),
]


def classify(name):
    for prefix, product, concept, angle, thesis in CONCEPT_MAP:
        if name.lower().startswith(prefix.lower()):
            return product, concept, angle, thesis
    return "", "UNMAPPED", "", ""


def verdict(spend, conv, roas):
    if conv >= 2 and roas >= 2.5:
        return "WINNER"
    if (spend >= 90 and conv == 0) or (spend >= 150 and roas < 1.5):
        return "LOSER"
    return "TESTING"


def main():
    roster = json.loads((SCRATCH / "tw_active_roster.json").read_text())
    stats30 = {r["ad_name"]: r for r in
               json.loads((SCRATCH / "tw_meta_conv_30d.json").read_text())}
    active = [r for r in roster if r["ad_status"] == "ACTIVE"
              and r["adset_status"] == "ACTIVE" and r["campaign_status"] == "ACTIVE"]
    active.sort(key=lambda r: -float(r["spend"] or 0))

    rows = []
    for r in active:
        name = r["ad_name"]
        product, concept, angle, thesis = classify(name)
        s30 = stats30.get(name, {})
        sp = float(s30.get("spend") or r["spend"] or 0)
        cv = float(s30.get("conv") or r["conv"] or 0)
        rev = float(s30.get("rev") or r["rev"] or 0)
        roas = rev / sp if sp else 0
        fmt = {"image": "Static", "video": "Video", "dynamic": "Dynamic"}.get(
            r["ad_type"] or "", r["ad_type"] or "")
        preview = r.get("video_url") or r.get("image_url") or ""
        rows.append([
            name, product, concept, angle, thesis, fmt, r["campaign"] or "",
            round(sp, 2), int(cv), round(sp / cv, 2) if cv else "",
            round(roas, 2), verdict(sp, cv, roas),
            r.get("ad_manager_url") or "", preview,
        ])

    svc = sheets_service()

    if CONFIG.exists():
        sid = json.loads(CONFIG.read_text())["spreadsheet_id"]
    else:
        created = svc.spreadsheets().create(body={
            "properties": {"title": TITLE},
            "sheets": [{"properties": {"title": "Active Creatives"}},
                       {"properties": {"title": "Net New Concepts"}}],
        }).execute()
        sid = created["spreadsheetId"]
        CONFIG.write_text(json.dumps({
            "spreadsheet_id": sid,
            "url": created["spreadsheetUrl"],
        }, indent=2))
        drive_service().permissions().create(
            fileId=sid, sendNotificationEmail=False,
            body={"type": "user", "role": "writer",
                  "emailAddress": SHARE_WITH}).execute()

    svc.spreadsheets().values().clear(
        spreadsheetId=sid, range="Active Creatives!A:N").execute()
    svc.spreadsheets().values().update(
        spreadsheetId=sid, range="Active Creatives!A1",
        valueInputOption="USER_ENTERED",
        body={"values": [ACTIVE_HEADERS] + rows}).execute()

    existing = svc.spreadsheets().values().get(
        spreadsheetId=sid, range="Net New Concepts!A1:A1").execute()
    if not existing.get("values"):
        svc.spreadsheets().values().update(
            spreadsheetId=sid, range="Net New Concepts!A1",
            valueInputOption="USER_ENTERED",
            body={"values": [NETNEW_HEADERS]}).execute()

    meta = svc.spreadsheets().get(spreadsheetId=sid).execute()
    gids = {s["properties"]["title"]: s["properties"]["sheetId"]
            for s in meta["sheets"]}
    fmt_reqs = []
    for tab, ncols in (("Active Creatives", len(ACTIVE_HEADERS)),
                       ("Net New Concepts", len(NETNEW_HEADERS))):
        gid = gids[tab]
        fmt_reqs += [
            {"repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True},
                    "backgroundColor": {"red": 0.9, "green": 0.89, "blue": 0.86}}},
                "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
            {"updateSheetProperties": {
                "properties": {"sheetId": gid,
                               "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount"}},
        ]
    fmt_reqs.append({"autoResizeDimensions": {"dimensions": {
        "sheetId": gids["Active Creatives"], "dimension": "COLUMNS",
        "startIndex": 0, "endIndex": 3}}})
    svc.spreadsheets().batchUpdate(
        spreadsheetId=sid, body={"requests": fmt_reqs}).execute()

    url = json.loads(CONFIG.read_text())["url"]
    unmapped = [r[0] for r in rows if r[2] == "UNMAPPED"]
    print(f"Sheet ready: {url}\n{len(rows)} active ads written.")
    if unmapped:
        print("UNMAPPED ads (add to CONCEPT_MAP):", unmapped)


if __name__ == "__main__":
    main()
