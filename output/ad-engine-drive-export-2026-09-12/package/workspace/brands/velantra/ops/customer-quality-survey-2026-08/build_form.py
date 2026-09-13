#!/usr/bin/env python3
"""Create the Velantra customer quality survey in Google Forms.

Two passes, because branching needs section item IDs that only exist after the
sections do:
  pass 1  create every section and question in order
  pass 2  read back the item IDs and patch the three branching questions

Every branch jumps FORWARD over a section. That is deliberate: the Forms API
exposes no navigation on a page break, so the only way to skip a block is for
the last question of the preceding section to name its target. Sections are
ordered so that each "skip" path lands on a section the natural flow also
reaches.

Auth: btorradre@gmail.com, drive.file scope (the Forms API accepts it).
"""
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TOKEN = ROOT / "_engine" / "oauth credentials" / "btorradre_gmail_gdrive_token.json"

TITLE = "How did we do? (Velantra)"
DESCRIPTION = (
    "Thanks for doing this. It takes about two minutes and there is no wrong answer. "
    "If you are annoyed with us, that is the response I most want to read.\n\n"
    "Brooks, Founder"
)

# Section keys, in the order they appear in the form. Branch targets below refer
# to these keys.
S_EXPECT = "S_EXPECT"
S_MISMATCH = "S_MISMATCH"
S_QUALITY = "S_QUALITY"
S_DELIVERY = "S_DELIVERY"
S_SUPPORT_GATE = "S_SUPPORT_GATE"
S_SUPPORT_YES = "S_SUPPORT_YES"
S_SUPPORT_NO = "S_SUPPORT_NO"
S_TRUST = "S_TRUST"
S_FORWARD = "S_FORWARD"


def short(title, desc=None, required=False, key=None):
    return {"kind": "q", "key": key, "title": title, "description": desc,
            "required": required, "q": {"textQuestion": {"paragraph": False}}}


def para(title, desc=None, required=False, key=None):
    return {"kind": "q", "key": key, "title": title, "description": desc,
            "required": required, "q": {"textQuestion": {"paragraph": True}}}


def radio(title, options, desc=None, required=False, key=None, branches=None):
    return {"kind": "q", "key": key, "title": title, "description": desc,
            "required": required, "branches": branches,
            "q": {"choiceQuestion": {"type": "RADIO",
                                     "options": [{"value": o} for o in options]}}}


def checks(title, options, desc=None, required=False, key=None):
    return {"kind": "q", "key": key, "title": title, "description": desc,
            "required": required,
            "q": {"choiceQuestion": {"type": "CHECKBOX",
                                     "options": [{"value": o} for o in options]}}}


def scale(title, low, high, low_label, high_label, desc=None, required=False, key=None):
    return {"kind": "q", "key": key, "title": title, "description": desc,
            "required": required,
            "q": {"scaleQuestion": {"low": low, "high": high,
                                    "lowLabel": low_label, "highLabel": high_label}}}


def section(key, title, desc=None):
    return {"kind": "section", "key": key, "title": title, "description": desc}


def text(title, desc):
    return {"kind": "text", "title": title, "description": desc}


ITEMS = [
    # ---- opening section (no page break; this is the form's first page) ----
    short("Your order number",
          "We filled this in for you. Please leave it as it is.",
          key="ORDER"),
    short("The bag you are telling us about",
          "We filled this in for you. Please leave it as it is.",
          key="BAG"),
    scale("How happy are you with your Velantra bag?", 1, 5,
          "Not happy", "Very happy", required=True, key="Q1"),
    radio("Are you still using it?",
          ["I use it regularly",
           "I have it, but I barely use it",
           "I sent it back, or asked to",
           "Tracking says it was delivered but I never actually got it"],
          required=True, key="Q3",
          branches={"Tracking says it was delivered but I never actually got it": S_DELIVERY}),

    # ---- expectation gap ----
    section(S_EXPECT, "Opening the box"),
    radio("When you opened the box, how did the bag compare to what you expected "
          "from our website?",
          ["Much better than I expected", "Better", "About what I expected",
           "Worse", "Much worse"],
          required=True, key="Q4",
          branches={"Much better than I expected": S_QUALITY,
                    "Better": S_QUALITY,
                    "About what I expected": S_QUALITY}),

    section(S_MISMATCH, "What was different?",
            "Sorry. This is the part we most need to hear."),
    checks("What was different from what you pictured?",
           ["Smaller than I pictured", "Bigger than I pictured", "The colour",
            "How the material feels", "The weight", "Too floppy", "Too stiff",
            "Details like hardware or stitching", "It had a smell", "Something else"],
           key="Q5"),
    para("Tell me what you saw when you opened it.", key="Q6"),

    # ---- the bag itself ----
    section(S_QUALITY, "The bag itself"),
    scale("Overall, how would you rate the quality of the bag?", 1, 5,
          "Poor", "Excellent", required=True, key="Q7"),
    checks("Anything on it that let you down?",
           ["Nothing, it is well made", "The material", "The stitching",
            "The hardware (zips, clasps, feet)", "The zipper",
            "The lining or inside", "The handles or straps",
            "It does not hold its shape", "The smell", "Something else"],
           key="Q8"),
    radio("Has anything gone wrong with it since it arrived?",
          ["No, it has held up", "It arrived already damaged",
           "Something broke or came apart",
           "Something wore out faster than I expected"],
          key="Q9"),
    para("If something did go wrong: what happened, and how long had you had it?",
         key="Q9B"),

    # ---- delivery ----
    section(S_DELIVERY, "Getting it to you"),
    radio("How did delivery compare to what you expected when you ordered?",
          ["Faster than expected", "About what I expected", "Slower",
           "A lot slower", "It never arrived"],
          required=True, key="Q10"),
    radio("While you were waiting, how clear were we about where your order was?",
          ["Very clear", "Clear enough", "Vague", "You told me nothing at all"],
          key="Q11"),
    radio("How did the package itself turn up?",
          ["Perfect", "Outer box was beaten up, bag was fine",
           "The bag itself was damaged", "The packaging felt cheap for the price",
           "Wrong item"],
          key="Q12"),

    # ---- support gate ----
    section(S_SUPPORT_GATE, "Talking to us"),
    radio("Did you ever email or message us?", ["Yes", "No"],
          required=True, key="Q13", branches={"No": S_SUPPORT_NO}),

    section(S_SUPPORT_YES, "When you got in touch"),
    checks("What was it about?",
           ["Where my order was", "A return or exchange",
            "A refund or cancellation", "Something damaged or faulty",
            "A sizing or product question", "Changing my order", "Something else"],
           key="Q14"),
    radio("How long did it take to hear back?",
          ["Same day", "1 to 2 days", "3 to 6 days", "Over a week",
           "I never got a reply"],
          key="Q15"),
    para("How did dealing with us make you feel? Say it however you want.", key="Q17"),
    radio("Did it get sorted out?",
          ["Yes, fully", "Partly", "No", "I gave up"],
          key="Q16",
          branches={"Yes, fully": S_TRUST, "Partly": S_TRUST,
                    "No": S_TRUST, "I gave up": S_TRUST}),

    section(S_SUPPORT_NO, "One thing about getting in touch"),
    radio("Was there ever a moment you wanted to get in touch and did not?",
          ["No", "Yes"], key="Q18"),
    para("If yes, what stopped you?", key="Q18B"),

    # ---- trust ----
    section(S_TRUST, "Straight question"),
    radio("Did you ever think about cancelling, returning, or disputing the charge?",
          ["No, never", "I thought about it", "I asked for a refund or return",
           "I disputed it with my bank"],
          key="Q19"),
    para("If you did think about it, what pushed you there?", key="Q19B"),
    para("Before you bought, was there anything you wanted to know that our site "
         "did not tell you?", key="Q20"),

    # ---- forward ----
    section(S_FORWARD, "Last few"),
    scale("How likely are you to buy from us again?", 0, 10,
          "Not a chance", "Definitely", key="Q21"),
    scale("How likely are you to recommend Velantra to a friend?", 0, 10,
          "Not a chance", "Definitely", key="Q22"),
    para("If we fixed one thing, what should it be?", key="Q23"),
    para("Anything you genuinely loved?", key="Q24"),
    radio("Can I follow up with you personally if I have a question?",
          ["Yes, by email", "Yes, by phone", "No thanks"], key="Q25"),
    short("If yes, the best email or number to reach you on", key="Q25B"),
    text("Your 15% off code: THANKYOU15",
         "Use it on your next order at velantrafashion.com. Thank you for doing this, "
         "I read every one of these myself.\n\nBrooks"),
]


def creds():
    c = Credentials.from_authorized_user_file(str(TOKEN))
    if not c.valid:
        c.refresh(Request())
        TOKEN.write_text(c.to_json())
    return c


def build_requests():
    reqs = []
    for i, it in enumerate(ITEMS):
        item = {"title": it["title"]}
        if it.get("description"):
            item["description"] = it["description"]
        if it["kind"] == "section":
            item["pageBreakItem"] = {}
        elif it["kind"] == "text":
            item["textItem"] = {}
        else:
            q = json.loads(json.dumps(it["q"]))
            q["required"] = it["required"]
            item["questionItem"] = {"question": q}
        reqs.append({"createItem": {"item": item, "location": {"index": i}}})
    return reqs


def main():
    svc = build("forms", "v1", credentials=creds(), cache_discovery=False)

    # --form-id <id> resumes against a form that already has its items, so a
    # failure in the entry-ID scrape never costs a duplicate form.
    existing = None
    if "--form-id" in sys.argv:
        existing = sys.argv[sys.argv.index("--form-id") + 1]

    if existing:
        fid = existing
        print(f"resuming against existing form {fid}")
    else:
        form = svc.forms().create(body={"info": {
            "title": TITLE,
            "documentTitle": "Velantra Customer Quality Survey"}}).execute()
        fid = form["formId"]
        print(f"created form {fid}")

        svc.forms().batchUpdate(formId=fid, body={"requests": [
            {"updateFormInfo": {"info": {"description": DESCRIPTION},
                                "updateMask": "description"}}]}).execute()

        svc.forms().batchUpdate(formId=fid, body={"requests": build_requests()}).execute()
        print(f"pass 1: {len(ITEMS)} items created")

    # -------- pass 2: resolve section item IDs, patch branching --------
    live = svc.forms().get(formId=fid).execute()
    section_ids, by_index = {}, {}
    for idx, item in enumerate(live["items"]):
        by_index[idx] = item
        if "pageBreakItem" in item:
            spec = ITEMS[idx]
            section_ids[spec["key"]] = item["itemId"]

    patches = []
    for idx, spec in enumerate(ITEMS):
        if spec["kind"] != "q" or not spec.get("branches"):
            continue
        item = by_index[idx]
        q = json.loads(json.dumps(item["questionItem"]["question"]))
        for opt in q["choiceQuestion"]["options"]:
            target = spec["branches"].get(opt["value"])
            if target:
                opt["goToSectionId"] = section_ids[target]
            else:
                opt["goToAction"] = "NEXT_SECTION"
        q["choiceQuestion"]["options"] = q["choiceQuestion"]["options"]
        patches.append({"updateItem": {
            "item": {"itemId": item["itemId"],
                     "title": item["title"],
                     "questionItem": {"question": q}},
            "location": {"index": idx},
            "updateMask": "questionItem.question"}})

    svc.forms().batchUpdate(formId=fid, body={"requests": patches}).execute()
    print(f"pass 2: {len(patches)} branching questions patched")

    final = svc.forms().get(formId=fid).execute()
    responder = final["responderUri"]

    # -------- entry IDs for the prefilled links --------
    html = urllib.request.urlopen(
        responder, timeout=30, context=SSL_CTX).read().decode("utf-8", "replace")
    blob = re.search(r"FB_PUBLIC_LOAD_DATA_ = (.*?);</script>", html, re.S)
    entries = {}
    if blob:
        data = json.loads(blob.group(1))
        for entry in data[1][1]:
            label, fields = entry[1], entry[4]
            if fields:
                entries[label] = fields[0][0]

    keymap = {}
    for spec in ITEMS:
        if spec["kind"] == "q" and spec.get("key"):
            eid = entries.get(spec["title"])
            if eid:
                keymap[spec["key"]] = {"entry": f"entry.{eid}", "title": spec["title"]}

    out = {
        "formId": fid,
        "editUri": f"https://docs.google.com/forms/d/{fid}/edit",
        "responderUri": responder,
        "sections": section_ids,
        "entries": keymap,
    }
    (HERE / "form.json").write_text(json.dumps(out, indent=1))

    print("\nedit:     ", out["editUri"])
    print("responder:", responder)
    print("\nprefill entry IDs:")
    for k in ("ORDER", "BAG", "Q1"):
        print(f"  {k:6s} {keymap.get(k, {}).get('entry', 'NOT FOUND')}")
    print(f"\nwrote {HERE / 'form.json'}")


if __name__ == "__main__":
    main()
