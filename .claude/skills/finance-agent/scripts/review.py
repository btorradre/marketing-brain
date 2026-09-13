#!/usr/bin/env python3
"""
Review loop — the human/Claude ruling step for anything the rulebook couldn't settle.

  python3 review.py --show                      # queue as markdown (grouped by merchant), also saved to data/review.md
  python3 review.py --set <id> <category> [--brand Velantra] [--note "..."]
  python3 review.py --set-merchant "<regex>" <category> [--brand X] [--learn --name "Rule name"]
  python3 review.py --apply decisions.json      # batch: [{"ids":[...]} | {"merchant_regex":"..."}, "category":..., "brand":..., "learn":true, "name":"..."}]
  python3 review.py --accept-all                # accept every proposed category as-is (locks them)

Every decision locks the rows (cat_source=manual) and, with --learn, appends a rule to
config/vendor_rules.json so the same vendor never comes back. Re-run categorize.py afterwards.
"""
import os, re, sys, json, argparse, datetime as dt
from collections import defaultdict, Counter
from fin_common import *  # noqa


def show(queue):
    items = queue.get("items", [])
    groups = defaultdict(list)
    for it in items:
        key = re.sub(r"\d+", "", (it["merchant"] or it["description"]).lower()).strip()[:32]
        groups[key].append(it)
    lines = [f"# Review queue — {len(items)} transactions in {len(groups)} vendor groups", "",
             f"Generated {queue.get('generated_at')} · threshold {queue.get('threshold')}", "",
             "Rule with: `python3 review.py --set-merchant \"<regex>\" <category> --learn --name \"<rule>\"`", ""]
    pol = defaultdict(list)
    for it in items:
        if it.get("policy"): pol[it["policy"]].append(it)
    if pol:
        lines += ["## Policy questions — answer ONCE, settles every row tagged with it", "",
                  "| policy | txns | $ | currently booked as | settle with |", "|---|---:|---:|---|---|"]
        for pname, its in sorted(pol.items(), key=lambda kv: -sum(x["amount"] for x in kv[1])):
            cats = Counter(x["proposed"] for x in its).most_common(1)[0][0]
            lines.append(f"| {pname} | {len(its)} | ${sum(x['amount'] for x in its):,.0f} | {cats} | `python3 review.py --policy {pname} <category>` |")
        lines += ["", "personal_looking → `owner_draw` (excluded from profit) or `other_opex` (keep as company cost). "
                  "people_payments → `contractors_agency` or `owner_draw`. unknown_transfer → rule each wire by id.", ""]
    for key, its in sorted(groups.items(), key=lambda kv: -sum(abs(x['amount']) for x in kv[1])):
        tot = sum(x["amount"] for x in its)
        prop = its[0]["proposed"] or "—"
        lines.append(f"## {its[0]['merchant'][:48]}  ·  {len(its)} txn · ${tot:,.2f}  ·  proposed **{prop}** ({its[0].get('confidence') or 0:.2f})")
        lines.append(f"_{its[0].get('reason')}_")
        so = its[0].get("second_opinion")
        if so and so.get("category") != its[0].get("proposed"):
            lines.append(f"_GPT 5.6 Sol says **{so['category']}** ({so.get('confidence', 0):.2f}): {so.get('reason')}_")
        for x in sorted(its, key=lambda x: x["date"])[:6]:
            lines.append(f"- `{x['id']}` {x['date']} ${x['amount']:,.2f} {x['account']} — {x['description'][:90]}")
        if len(its) > 6: lines.append(f"- … {len(its) - 6} more")
        lines.append("")
    md = "\n".join(lines)
    open(os.path.join(DATA, "review.md"), "w").write(md)
    print(md)


def apply_decision(store, queue, d, learn_rules):
    T = store["transactions"]
    cat = norm_category(d["category"])
    if not cat:
        print(f"  unknown category {d['category']!r}"); return 0
    ids = set(d.get("ids") or [])
    rx = re.compile(d["merchant_regex"], re.I) if d.get("merchant_regex") else None
    n = 0
    for t in T:
        hit = t["id"] in ids or (rx and (rx.search(t["merchant"]) or rx.search(t["description"])) and not t.get("locked"))
        if not hit: continue
        t["category"], t["cat_source"], t["confidence"], t["locked"], t["needs_review"] = cat, "manual", 1.0, True, False
        t["reason"] = d.get("note") or "ruled in review"
        if d.get("brand"): t["brand"] = d["brand"]
        n += 1
    queue["items"] = [it for it in queue.get("items", []) if it["id"] not in ids and not (rx and (rx.search(it["merchant"]) or rx.search(it["description"])))]
    if d.get("learn") and rx:
        learn_rules.append({"name": d.get("name") or f"learned: {d['merchant_regex'][:30]}", "pattern": d["merchant_regex"],
                            "category": cat, **({"brand": d["brand"]} if d.get("brand") else {}),
                            "note": d.get("note") or "learned from review"})
    print(f"  {cat:22} ← {n} rows  ({d.get('merchant_regex') or f'{len(ids)} ids'})")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--set", nargs=2, metavar=("ID", "CATEGORY"))
    ap.add_argument("--set-merchant", nargs=2, metavar=("REGEX", "CATEGORY"))
    ap.add_argument("--brand"); ap.add_argument("--note"); ap.add_argument("--name")
    ap.add_argument("--learn", action="store_true", help="append a vendor rule for --set-merchant")
    ap.add_argument("--apply", help="decisions JSON file")
    ap.add_argument("--accept-all", action="store_true")
    ap.add_argument("--policy", nargs=2, metavar=("POLICY", "CATEGORY"), help="settle every row + rule tagged with this policy")
    args = ap.parse_args()

    store = load_json(TXNS, {"transactions": []})
    queue = load_json(QUEUE, {"items": []})
    if args.policy:
        pname, cat = args.policy[0], norm_category(args.policy[1])
        if not cat: print(f"unknown category {args.policy[1]!r}"); return
        ids = [t["id"] for t in store["transactions"] if t.get("policy") == pname and not t.get("locked")]
        rules = load_json(RULES, {"rules": []}); n_r = 0
        for r in rules["rules"]:
            if r.get("policy") == pname:
                r["category"] = cat; r.pop("review", None); r["note"] = (r.get("note") or "") + f" · policy settled {dt.date.today().isoformat()} → {cat}"; n_r += 1
        save_json(RULES, rules)
        d = {"ids": ids, "category": cat, "note": f"policy {pname} → {cat}", "policy": pname}
        n = apply_decision(store, queue, d, [])
        log = load_json(DECISIONS, {"decisions": []}); log["decisions"].append({**d, "ids": len(ids), "at": now_iso()}); save_json(DECISIONS, log)
        store["updated_at"] = now_iso(); save_json(TXNS, store); save_json(QUEUE, queue)
        print(f"policy {pname} → {cat}: {n} rows locked, {n_r} rules updated (review flag removed). Now run: python3 categorize.py")
        return
    if args.show or not any([args.set, args.set_merchant, args.apply, args.accept_all]):
        show(queue); return

    decisions = []
    if args.set:
        decisions.append({"ids": [args.set[0]], "category": args.set[1], "brand": args.brand, "note": args.note})
    if args.set_merchant:
        decisions.append({"merchant_regex": args.set_merchant[0], "category": args.set_merchant[1], "brand": args.brand,
                          "note": args.note, "learn": args.learn, "name": args.name})
    if args.apply:
        d = load_json(os.path.expanduser(args.apply), [])
        decisions.extend(d if isinstance(d, list) else d.get("decisions", []))
    if args.accept_all:
        by = defaultdict(list)
        for it in queue.get("items", []):
            if it["proposed"]: by[it["proposed"]].append(it["id"])
        for cat, ids in by.items():
            decisions.append({"ids": ids, "category": cat, "note": "accepted proposed category"})

    learned = []
    total = sum(apply_decision(store, queue, d, learned) for d in decisions)
    if learned:
        rules = load_json(RULES, {"rules": []})
        # learned rules go BEFORE the generic tail (meals/retail) but after the excluded/ads block: insert at index of first "airlines" rule
        idx = next((i for i, r in enumerate(rules["rules"]) if r["name"] == "airlines"), len(rules["rules"]))
        for r in learned: rules["rules"].insert(idx, r); idx += 1
        save_json(RULES, rules); print(f"  +{len(learned)} rule(s) learned → {RULES}")
    log = load_json(DECISIONS, {"decisions": []}); log["decisions"].extend({**d, "at": now_iso()} for d in decisions); save_json(DECISIONS, log)
    store["updated_at"] = now_iso(); save_json(TXNS, store); save_json(QUEUE, queue)
    print(f"{total} rows ruled · {len(queue.get('items', []))} left in queue. Now run: python3 categorize.py")


if __name__ == "__main__":
    main()
