#!/usr/bin/env python3
"""
angle_map.py — the mechanics behind the angle mapper.

Turns pages of avatar research into a tree of angles (the core problem) and
micro-angles (the same problem at higher resolution, aimed at one cohort), then
polices that tree so nothing unsourced, unspecific, or un-buyable reaches a brief.

  chunk    split a pile of research into extraction-sized passes with line refs
  add      append one candidate record, auto-allocating its ID
  lint     schema + gate + structure check over every candidate
  verify   prove every source_quote exists verbatim in the research (Law 2)
  matrix   coverage grid: core angles x context vectors, and the empty cells
  queue    ranked production queue of what to brief next
  render   assemble angle-map.md, the artifact the rest of the DR OS reads
  bank     emit angle-bank-ready YAML for records that passed every gate

The map lives at brands/<brand>/research/dr-os/angle-map/ :
  candidates.jsonl   one JSON record per line, the working set
  chunks/            extraction passes written by `chunk`
  manifest.json      what was chunked, from where

Usage
-----
  python3 angle_map.py chunk  --map <dir> --in <file-or-dir> ... [--words 6000]
  python3 angle_map.py add    --map <dir> --json '<record>'      # or --file r.json
  python3 angle_map.py lint   --map <dir>
  python3 angle_map.py verify --map <dir> --sources <file-or-dir> ...
  python3 angle_map.py matrix --map <dir>
  python3 angle_map.py queue  --map <dir> [--limit 10]
  python3 angle_map.py render --map <dir> --out <angle-map.md>
  python3 angle_map.py bank   --map <dir>
"""
from __future__ import annotations
import argparse, json, re, sys, unicodedata
from collections import Counter, defaultdict, OrderedDict
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- vocabulary

# The ten ways a core problem narrows into a cohort. Niche-agnostic on purpose:
# these are the axes a person's life varies along, not features of any category.
VECTORS = [
    "occasion",       # the specific event the product gets used in
    "identity",       # job or role: nurse, contractor, new mum, grad student
    "life-stage",     # transition: postpartum, divorce, first apartment, retirement
    "constraint",     # money, space, time, body, rules they must obey
    "failure-moment", # the scene where the problem cost or humiliated them
    "incumbent",      # what they use now and exactly how it fails them
    "relational",     # who else the problem touches: partner, kids, clients, staff
    "frequency",      # the heavy user vs the once-a-year user
    "environment",    # climate, geography, commute, home type
    "objection",      # the blocker itself as the problem: burned before, sceptical
]

LEVELS = {1: "core angle", 2: "contextual micro-angle", 3: "situational micro-angle"}

GATES = ["layer", "rewrite", "self_id", "population", "product_truth", "swap", "brand_law"]

REQUIRED = [
    "id", "level", "brand", "avatar", "name", "problem", "golden_nugget",
    "source_quote", "source", "source_type", "grounding", "awareness",
    "emotional_trigger", "priority", "status",
]
MICRO_REQUIRED = ["parent_id", "cohort", "vector", "self_id_line"]

AWARENESS = {"unaware", "problem", "solution", "product", "most"}
GROUNDING = {"sourced", "inferred"}
PRIORITY = {"HIGH", "MEDIUM", "LOW"}
STATUS = {"fresh", "active", "fatigued", "retired"}
SHELF = {"evergreen", "seasonal-wrapper", "dated"}

TEXT_SUFFIXES = {".md", ".txt", ".csv", ".jsonl", ".json", ".yaml", ".yml"}

# A claim wearing an angle's clothes. These openings mean a hook got filed as a problem.
CLAIM_TELLS = re.compile(
    r"^\s*(it'?s not\b|the real reason\b|why your\b|the truth about\b|"
    r"most people don'?t\b|doctors? (?:won'?t|don'?t)\b|this is why\b|"
    r"here'?s why\b|the secret\b|nobody tells you\b)", re.I)


# ---------------------------------------------------------------- plumbing

def die(msg: str, code: int = 1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def map_dir(a) -> Path:
    d = Path(a.map)
    d.mkdir(parents=True, exist_ok=True)
    return d


def cand_path(d: Path) -> Path:
    return d / "candidates.jsonl"


def load(d: Path) -> list[dict]:
    p = cand_path(d)
    if not p.exists():
        return []
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            die(f"{p}:{i} is not valid JSON — {e}")
    return out


def save(d: Path, records: list[dict]):
    cand_path(d).write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
        encoding="utf-8")


def expand(paths: list[str]) -> list[Path]:
    """Files given directly, or every text file under a directory given."""
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out += sorted(f for f in p.rglob("*")
                          if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES)
        elif p.is_file():
            out.append(p)
        else:
            die(f"no such path: {raw}")
    return out


def norm(s: str) -> str:
    """Fold a quote to its comparable core: no smart quotes, no case, no run-on space."""
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"[^a-z0-9' ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def by_level(records: list[dict]) -> tuple[list[dict], list[dict]]:
    return ([r for r in records if int(r.get("level", 1)) == 1],
            [r for r in records if int(r.get("level", 1)) > 1])


def gates_of(r: dict) -> dict:
    return r.get("gates", {}) or {}


def gate_failures(r: dict) -> list[str]:
    g = gates_of(r)
    bad = [k for k in GATES if str(g.get(k, "")).lower() not in ("pass", "n/a")]
    if str(g.get("shelf_life", "")).lower() == "dated":
        bad.append("shelf_life")
    return bad


def passed(r: dict) -> bool:
    return not gate_failures(r) and str(g_shelf(r)).lower() in ("evergreen", "seasonal-wrapper")


def g_shelf(r: dict) -> str:
    return gates_of(r).get("shelf_life", "")


# ---------------------------------------------------------------- chunk

def cmd_chunk(a):
    d = map_dir(a)
    outdir = d / "chunks"
    outdir.mkdir(exist_ok=True)
    for old in outdir.glob("chunk-*.md"):
        old.unlink()

    files = expand(a.inputs)
    if not files:
        die("nothing to chunk")

    manifest, n, total_words = [], 0, 0
    for f in files:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception as e:
            print(f"  skipped {f}: {e}", file=sys.stderr)
            continue

        buf: list[str] = []
        buf_words = 0
        start = 1
        for idx, line in enumerate(lines, 1):
            buf.append(line)
            buf_words += len(line.split())
            # Break on a blank line once we are past target, so a paragraph is never split.
            if buf_words >= a.words and (not line.strip() or idx == len(lines)):
                n += 1
                total_words += buf_words
                _write_chunk(outdir, n, f, start, idx, buf)
                manifest.append({"chunk": n, "source": str(f), "lines": [start, idx],
                                 "words": buf_words})
                buf, buf_words, start = [], 0, idx + 1
        if buf and any(l.strip() for l in buf):
            n += 1
            total_words += buf_words
            _write_chunk(outdir, n, f, start, len(lines), buf)
            manifest.append({"chunk": n, "source": str(f), "lines": [start, len(lines)],
                             "words": buf_words})

    (d / "manifest.json").write_text(
        json.dumps({"generated": date.today().isoformat(), "target_words": a.words,
                    "files": len(files), "chunks": n, "words": total_words,
                    "passes": manifest}, indent=2), encoding="utf-8")

    print(f"{len(files)} file(s), {total_words:,} words -> {n} extraction pass(es)")
    print(f"chunks:   {outdir}")
    print(f"manifest: {d / 'manifest.json'}")
    if n:
        print("\nRun one extraction pass per chunk. One pass over everything gives you a "
              "thin read of all of it instead of a deep read of any of it.")


def _write_chunk(outdir: Path, n: int, src: Path, start: int, end: int, buf: list[str]):
    header = (f"<!-- CHUNK {n:03d} | source: {src} | lines {start}-{end}\n"
              f"     Cite anything you pull from here as {src}#L<line>. -->\n\n")
    (outdir / f"chunk-{n:03d}.md").write_text(header + "\n".join(buf) + "\n",
                                              encoding="utf-8")


# ---------------------------------------------------------------- add

def _used_ids(d: Path, records: list[dict]) -> set[str]:
    """Every ID already spoken for, here and in the sibling angle bank."""
    used = {r.get("id", "") for r in records}
    bank = d.parent / "angle-bank.md"
    if bank.exists():
        used |= set(re.findall(r"\b([A-Z]{3}-A-\d+(?:\.\d+)?)\b",
                               bank.read_text(encoding="utf-8", errors="replace")))
    return {u for u in used if u}


def _allocate(d: Path, records: list[dict], rec: dict) -> str:
    used = _used_ids(d, records)
    parent = rec.get("parent_id")
    if parent:
        m = re.match(r"^([A-Z]{3}-A-\d+)", parent)
        if not m:
            die(f"parent_id '{parent}' is not a core angle ID like VEL-A-014")
        stem = m.group(1)
        i = 1
        while f"{stem}.{i}" in used:
            i += 1
        return f"{stem}.{i}"
    prefix = (rec.get("prefix") or rec.get("brand", "")[:3]).upper()
    if not re.fullmatch(r"[A-Z]{3}", prefix):
        die("cannot derive a 3-letter brand prefix; pass \"prefix\": \"VEL\"")
    nums = [int(m.group(1)) for u in used
            if (m := re.fullmatch(rf"{prefix}-A-(\d+)", u))]
    return f"{prefix}-A-{max(nums, default=0) + 1:03d}"


def cmd_add(a):
    d = map_dir(a)
    records = load(d)

    raw = Path(a.file).read_text(encoding="utf-8") if a.file else a.json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        die(f"input is not valid JSON — {e}")
    incoming = payload if isinstance(payload, list) else [payload]

    today = date.today().isoformat()
    added = []
    for rec in incoming:
        if not isinstance(rec, dict):
            die("each record must be a JSON object")
        rec.setdefault("level", 2 if rec.get("parent_id") else 1)
        rec["level"] = int(rec["level"])
        if not rec.get("id"):
            rec["id"] = _allocate(d, records + added, rec)
        elif rec["id"] in _used_ids(d, records + added):
            die(f"id {rec['id']} is already used")
        rec.pop("prefix", None)
        rec.setdefault("status", "fresh")
        rec.setdefault("asset_ids", [])
        rec.setdefault("hook_seeds", [])
        rec.setdefault("verdict", "")
        rec.setdefault("first_seen", today)
        rec["last_touched"] = today
        g = rec.setdefault("gates", {})
        g.setdefault("shelf_life", "")
        for k in GATES:
            g.setdefault(k, "")
        added.append(rec)

    save(d, records + added)
    for r in added:
        kind = LEVELS.get(r["level"], "micro-angle")
        print(f"+ {r['id']:<14} L{r['level']} {kind:<26} {r.get('name','')}")
    print(f"\n{len(records) + len(added)} record(s) in {cand_path(d)}")
    print("Next: python3 angle_map.py lint --map " + str(d))


# ---------------------------------------------------------------- lint

def cmd_lint(a):
    d = map_dir(a)
    records = load(d)
    if not records:
        die("no candidates yet")

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    ids = {r.get("id") for r in records}

    for r in records:
        rid = r.get("id", "<no id>")
        lvl = int(r.get("level", 1))

        for f in REQUIRED:
            if not str(r.get(f, "")).strip():
                errors.append(f"{rid}: missing required field `{f}`")
        if lvl > 1:
            for f in MICRO_REQUIRED:
                if not str(r.get(f, "")).strip():
                    errors.append(f"{rid}: micro-angle missing `{f}`")

        if rid in seen_ids:
            errors.append(f"{rid}: duplicate ID")
        seen_ids.add(rid)

        if lvl > 1:
            parent = r.get("parent_id")
            if parent and parent not in ids:
                errors.append(f"{rid}: parent_id {parent} is not in the map")
            if parent and not rid.startswith(parent.split(".")[0]):
                errors.append(f"{rid}: ID does not descend from parent {parent}")
        elif r.get("parent_id"):
            errors.append(f"{rid}: level 1 record cannot have a parent_id")

        v = r.get("vector")
        if lvl > 1 and v not in VECTORS:
            errors.append(f"{rid}: vector '{v}' is not one of {', '.join(VECTORS)}")

        if r.get("awareness") not in AWARENESS:
            errors.append(f"{rid}: awareness '{r.get('awareness')}' invalid")
        if r.get("grounding") not in GROUNDING:
            errors.append(f"{rid}: grounding must be sourced|inferred")
        if r.get("priority") not in PRIORITY:
            errors.append(f"{rid}: priority must be HIGH|MEDIUM|LOW")
        if r.get("status") not in STATUS:
            errors.append(f"{rid}: status must be one of {', '.join(sorted(STATUS))}")
        shelf = g_shelf(r)
        if shelf and shelf not in SHELF:
            errors.append(f"{rid}: gates.shelf_life '{shelf}' invalid")

        # The angle-is-a-problem law, mechanically.
        prob = str(r.get("problem", ""))
        if CLAIM_TELLS.match(prob):
            errors.append(f"{rid}: `problem` opens like a claim — that is a hook. "
                          f"Move it to hook_seeds and write the problem it argues about.")
        if prob and len(prob.split()) < 6:
            warnings.append(f"{rid}: `problem` is {len(prob.split())} words — too thin to "
                            f"recognise as hers")
        if str(r.get("golden_nugget", "")).strip().lower() == prob.strip().lower():
            errors.append(f"{rid}: golden_nugget repeats the problem — that is the topic, "
                          f"not the motive")

        if lvl > 1 and str(r.get("self_id_line", "")) and \
                "you" not in str(r.get("self_id_line", "")).lower():
            warnings.append(f"{rid}: self_id_line never addresses her — nobody will "
                            f"self-select into it")

        blank = [k for k in GATES if not str(gates_of(r).get(k, "")).strip()]
        if blank:
            warnings.append(f"{rid}: gates not run: {', '.join(blank)}")
        if not str(g_shelf(r)).strip():
            warnings.append(f"{rid}: gates.shelf_life not set")

        fails = gate_failures(r)
        if fails and r.get("priority") == "HIGH":
            errors.append(f"{rid}: HIGH priority with failing gate(s): {', '.join(fails)}")
        if r.get("grounding") == "inferred" and r.get("priority") == "HIGH":
            errors.append(f"{rid}: inferred cohort cannot be HIGH — confirm it in the "
                          f"research or cap it at MEDIUM")
        if int(r.get("evidence_count", 0) or 0) >= 3 and r.get("grounding") == "inferred":
            warnings.append(f"{rid}: {r['evidence_count']} pieces of evidence but marked "
                            f"inferred — promote it to sourced?")

    # An avatar with one angle is not a campaign; an angle with no micro-angles is untargeted.
    kids = Counter(r.get("parent_id") for r in records if int(r.get("level", 1)) > 1)
    for r in records:
        if int(r.get("level", 1)) == 1 and kids.get(r.get("id"), 0) == 0:
            warnings.append(f"{r.get('id')}: core angle with zero micro-angles — one cohort "
                            f"only, so nothing to expand into")
    per_avatar = Counter(r.get("avatar") for r in records if int(r.get("level", 1)) == 1)
    for av, c in per_avatar.items():
        if c < 3:
            warnings.append(f"avatar '{av}': {c} core angle(s) — under 3 is not yet a campaign")

    for w in warnings:
        print(f"  warn  {w}")
    for e in errors:
        print(f"  FAIL  {e}")
    print(f"\n{len(records)} record(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


# ---------------------------------------------------------------- verify

def cmd_verify(a):
    d = map_dir(a)
    records = load(d)
    if not records:
        die("no candidates yet")

    sources = a.sources or [str(d / "chunks")]
    files = expand(sources)
    if not files:
        die("no source files to verify against")

    haystack = " ||| ".join(
        norm(f.read_text(encoding="utf-8", errors="replace")) for f in files)

    bad = []
    for r in records:
        q = str(r.get("source_quote", "")).strip()
        if not q:
            bad.append((r.get("id"), "<empty quote>"))
            continue
        if norm(q) not in haystack:
            bad.append((r.get("id"), q))

    print(f"checked {len(records)} quote(s) against {len(files)} file(s)")
    if bad:
        print("\nNOT FOUND VERBATIM:")
        for rid, q in bad:
            print(f"  {rid}: {q[:110]}")
        print("\nA quote that is not in the research is a fabricated citation. Replace it "
              "with a real line or delete the record.")
        sys.exit(1)
    print("all quotes verified verbatim")


# ---------------------------------------------------------------- matrix

def cmd_matrix(a):
    d = map_dir(a)
    records = load(d)
    if not records:
        die("no candidates yet")
    core, micro = by_level(records)
    core_by_id = {r["id"]: r for r in core}

    grid = defaultdict(list)
    for m in micro:
        grid[(m.get("parent_id"), m.get("vector"))].append(m)

    label_w = max([len(f"{r['id']} {r.get('name','')}") for r in core] + [18])
    label_w = min(label_w, 46)
    head = " " * (label_w + 2) + " ".join(f"{v[:4]:>4}" for v in VECTORS)
    print("COVERAGE — core angles x context vectors")
    print(head)
    print(" " * (label_w + 2) + " ".join("----" for _ in VECTORS))

    for c in core:
        lbl = f"{c['id']} {c.get('name','')}"[:label_w].ljust(label_w)
        cells = []
        for v in VECTORS:
            got = grid.get((c["id"], v), [])
            if not got:
                cells.append("   .")
            else:
                mark = "*" if any(m.get("grounding") == "inferred" for m in got) else " "
                cells.append(f"{len(got):>3}{mark}")
        print(f"  {lbl} " + " ".join(cells))

    print("\n  legend: number = micro-angles on that vector, * = includes inferred "
          "cohorts, . = empty cell")

    gaps = [(c, v) for c in core for v in VECTORS if not grid.get((c["id"], v))]
    print(f"\n{len(micro)} micro-angle(s) across {len(core)} core angle(s). "
          f"{len(gaps)} empty cell(s).")

    if gaps:
        print("\nEMPTY CELLS — each one is a cohort nobody has written to yet:")
        for c, v in gaps[: a.limit]:
            print(f"  {c['id']:<12} x {v:<15} {c.get('name','')}")
        if len(gaps) > a.limit:
            print(f"  ... and {len(gaps) - a.limit} more (--limit to see them)")

    coh = Counter(m.get("cohort") for m in micro if m.get("cohort"))
    print(f"\nCOHORTS ADDRESSED: {len(coh)}")
    for name, n in coh.most_common(12):
        print(f"  {n:>2}  {name}")

    aw = Counter(r.get("awareness") for r in records)
    print("\nAWARENESS SPREAD: " + ", ".join(
        f"{k} {aw.get(k,0)}/{len(records)}" for k in
        ["unaware", "problem", "solution", "product", "most"]))
    trig = Counter(r.get("emotional_trigger") for r in records)
    print("EMOTIONAL SPREAD: " + ", ".join(f"{k} {n}" for k, n in trig.most_common()))
    unparented = [m for m in micro if m.get("parent_id") not in core_by_id]
    if unparented:
        print(f"\norphaned micro-angles: {', '.join(m['id'] for m in unparented)}")


# ---------------------------------------------------------------- queue

def _rank(r: dict) -> tuple:
    pri = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(r.get("priority"), 3)
    ground = 0 if r.get("grounding") == "sourced" else 1
    ev = -int(r.get("evidence_count", 0) or 0)
    untested = 0 if not r.get("asset_ids") else 1
    hooks = 0 if r.get("hook_seeds") else 1
    return (untested, pri, ground, ev, hooks, r.get("id", ""))


def cmd_queue(a):
    d = map_dir(a)
    records = [r for r in load(d)
               if r.get("status") in ("fresh", "active") and passed(r)]
    if not records:
        die("nothing has passed the gates yet — run lint and fill the gate fields")
    records.sort(key=_rank)

    print("PRODUCTION QUEUE — briefed top-down\n")
    for i, r in enumerate(records[: a.limit], 1):
        lvl = int(r.get("level", 1))
        tag = "CORE " if lvl == 1 else f"MICRO"
        print(f"{i:>2}. [{tag}] {r['id']}  {r.get('name','')}   "
              f"({r.get('priority')}, {r.get('grounding')}, "
              f"evidence x{r.get('evidence_count', 0)})")
        print(f"    avatar:  {r.get('avatar','')}")
        if lvl > 1:
            print(f"    cohort:  {r.get('cohort','')}  [{r.get('vector','')}]")
            print(f"    self-ID: {r.get('self_id_line','')}")
        print(f"    problem: {str(r.get('problem','')).strip()}")
        seeds = r.get("hook_seeds") or []
        print(f"    hooks:   " + (seeds[0] if seeds else
                                  "none yet — run dr-hook-lab on this record"))
        if r.get("notes"):
            print(f"    NOTE:    {r['notes']}")
        print(f"    formats: {', '.join(r.get('formats', []) or ['-'])}   "
              f"awareness: {r.get('awareness','')}\n")

    if len(records) > a.limit:
        print(f"... {len(records) - a.limit} more passing record(s)")
    print("Reminder: you do NOT have to test each micro-angle separately. One concept can "
          "lead with the strongest micro-angle's hook and carry two or three others in the "
          "body — split them into their own ad sets only once the parent angle proves out.")


# ---------------------------------------------------------------- render

def _y(v, indent=2) -> str:
    """Minimal YAML scalar/sequence emitter — no dependency, no surprises."""
    pad = " " * indent
    if isinstance(v, list):
        if not v:
            return "[]"
        return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in v) + "]"
    s = str(v)
    if "\n" in s or len(s) > 88:
        body = "\n".join(pad + "  " + l.strip() for l in s.strip().splitlines() if l.strip())
        return ">\n" + body
    if s == "" or re.search(r"[:#\-{}\[\],&*?|<>=!%@`\"']", s) or s.strip() != s:
        return json.dumps(s, ensure_ascii=False)
    return s


def _record_yaml(r: dict) -> str:
    order = ["id", "parent_id", "level", "avatar", "name", "cohort", "vector",
             "status", "priority", "problem", "self_id_line", "golden_nugget",
             "source_quote", "source", "source_url", "source_type", "evidence_count",
             "grounding", "awareness", "sophistication", "emotional_trigger",
             "formats", "hook_seeds", "notes", "asset_ids", "verdict", "first_seen",
             "last_touched"]
    lines = ["```yaml"]
    for k in order:
        if k not in r or r.get(k) in (None, ""):
            continue
        lines.append(f"{k}: {_y(r[k])}")
    g = gates_of(r)
    if g:
        lines.append("gates:")
        for k in GATES + ["shelf_life"]:
            if g.get(k):
                lines.append(f"  {k}: {_y(g[k], 4)}")
    lines.append("```")
    return "\n".join(lines)


def cmd_render(a):
    d = map_dir(a)
    records = load(d)
    if not records:
        die("no candidates yet")
    core, micro = by_level(records)
    brand = (records[0].get("brand") or "unknown")
    out = Path(a.out) if a.out else d.parent / "angle-map.md"

    kids = defaultdict(list)
    for m in micro:
        kids[m.get("parent_id")].append(m)

    srcs = sorted({r.get("source", "").split("#")[0] for r in records if r.get("source")})
    L = []
    L.append("---")
    L.append(f"brand: {brand}")
    L.append("artifact: angle-map")
    L.append("generated_by: dr-angle-mapper")
    L.append(f"updated: {date.today().isoformat()}")
    L.append("sources:")
    for s in srcs:
        L.append(f"  - {s}")
    L.append("---\n")
    L.append("# Angle Map\n")
    L.append(f"{len(core)} core angle(s), {len(micro)} micro-angle(s), "
             f"{len(set(m.get('cohort') for m in micro if m.get('cohort')))} cohort(s) "
             f"addressed.\n")
    L.append("A core angle is the problem. A micro-angle is that same problem at higher "
             "resolution, narrowed onto one cohort by one context vector. Both pass the "
             "ad-set test; the micro-angle just names a smaller room.\n")

    avatars = OrderedDict()
    for c in core:
        avatars.setdefault(c.get("avatar", "unassigned"), []).append(c)

    for avatar, angles in avatars.items():
        L.append(f"\n## Avatar — {avatar}\n")
        for c in sorted(angles, key=_rank):
            L.append(f"### {c['id']} — {c.get('name','')}  "
                     f"({c.get('priority')}, {c.get('status')})\n")
            L.append(_record_yaml(c) + "\n")
            ms = sorted(kids.get(c["id"], []), key=_rank)
            if not ms:
                L.append("_No micro-angles yet. This angle speaks to one undifferentiated "
                         "room._\n")
                continue
            L.append(f"**Micro-angles ({len(ms)})**\n")
            for m in ms:
                L.append(f"#### {m['id']} — {m.get('name','')}  "
                         f"[{m.get('vector')}] {m.get('priority')}, {m.get('grounding')}\n")
                L.append(f"> {m.get('self_id_line','')}\n")
                L.append(_record_yaml(m) + "\n")

    L.append("\n## Coverage matrix\n")
    L.append("```")
    L.append(_matrix_text(core, micro))
    L.append("```\n")

    ready = [r for r in records if r.get("status") in ("fresh", "active") and passed(r)]
    ready.sort(key=_rank)
    L.append("## Production queue\n")
    if not ready:
        L.append("_Nothing has cleared every gate yet._\n")
    for i, r in enumerate(ready[:15], 1):
        who = r.get("cohort") or r.get("avatar")
        L.append(f"{i}. **{r['id']} {r.get('name','')}** — {who}. "
                 f"{str(r.get('problem','')).strip()}")
    L.append("\nYou do NOT have to test each micro-angle separately. One concept can lead "
             "with the strongest micro-angle and carry the next two in the body. Split into "
             "separate ad sets once the parent angle proves out.\n")

    L.append("## Media buying map\n")
    L.append("```")
    for avatar, angles in avatars.items():
        L.append(f"CBO Campaign — Avatar: {avatar}")
        for c in angles:
            ms = kids.get(c["id"], [])
            L.append(f"├── Ad set — {c['id']} {c.get('name','')}  "
                     f"[{len(c.get('hook_seeds') or [])} hook seeds]")
            for m in ms:
                L.append(f"│   ├── Ad  — {m['id']} {m.get('name','')} "
                         f"({m.get('cohort','')})")
    L.append("```\n")
    L.append("Promote a micro-angle to its own ad set when it earns budget separation: two "
             "or more hooks written, and a parent angle already proving out.\n")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {out}  ({len(core)} core, {len(micro)} micro)")


def _matrix_text(core: list[dict], micro: list[dict]) -> str:
    grid = defaultdict(list)
    for m in micro:
        grid[(m.get("parent_id"), m.get("vector"))].append(m)
    label_w = min(max([len(f"{r['id']} {r.get('name','')}") for r in core] + [18]), 46)
    rows = [" " * (label_w + 2) + " ".join(f"{v[:4]:>4}" for v in VECTORS)]
    for c in core:
        lbl = f"{c['id']} {c.get('name','')}"[:label_w].ljust(label_w)
        cells = []
        for v in VECTORS:
            got = grid.get((c["id"], v), [])
            cells.append("   ." if not got else f"{len(got):>4}")
        rows.append(f"  {lbl} " + " ".join(cells))
    rows.append("")
    rows.append("  columns: " + ", ".join(VECTORS))
    return "\n".join(rows)


# ---------------------------------------------------------------- bank

def cmd_bank(a):
    """Emit angle-bank-ready records. Only what cleared every gate goes through."""
    d = map_dir(a)
    records = [r for r in load(d) if passed(r)]
    if not records:
        die("nothing has passed the gates — run lint first")
    blocked = [r for r in load(d) if not passed(r)]

    print("# Paste-ready for brands/<brand>/research/dr-os/angle-bank.md")
    print("# Every record below cleared layer, rewrite, self-ID, population,")
    print("# product-truth, swap, brand-law and shelf-life. dr-angle-bank still merges;")
    print("# it does not append blind.\n")
    for r in sorted(records, key=_rank):
        b = {
            "id": r["id"], "avatar": r.get("avatar"), "name": r.get("name"),
            "status": r.get("status", "fresh"), "problem": r.get("problem"),
            "golden_nugget": r.get("golden_nugget"),
            "source_quote": r.get("source_quote"), "source": r.get("source"),
            "source_url": r.get("source_url", ""), "source_type": r.get("source_type"),
            "persona": r.get("cohort") or r.get("persona", ""),
            "awareness": r.get("awareness"), "sophistication": r.get("sophistication", ""),
            "emotional_trigger": r.get("emotional_trigger"),
            "formats": r.get("formats", []),
            "priority": r.get("priority"), "shelf_life": g_shelf(r),
            "swap_test": gates_of(r).get("swap", ""),
            "brand_law_check": gates_of(r).get("brand_law", ""),
            "saturation": r.get("saturation", "fresh"), "notes": r.get("notes", ""),
            "first_seen": r.get("first_seen"), "last_touched": r.get("last_touched"),
        }
        print("- " + "\n  ".join(
            f"{k}: {_y(v, 4)}" for k, v in b.items() if v not in (None, "")))
        seeds = r.get("hook_seeds") or []
        print("  hooks:")
        if not seeds:
            print("    []   # run dr-hook-lab before briefing")
        for s in seeds:
            print(f"    - text: {_y(s, 6)}")
            print(f"      status: fresh")
            print(f"      asset_ids: []")
            print(f"      verdict: \"\"")
        print()

    if blocked:
        print(f"# HELD BACK ({len(blocked)}): " +
              ", ".join(f"{r['id']} ({', '.join(gate_failures(r)) or 'shelf_life'})"
                        for r in blocked))


# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("chunk", help="split research into extraction passes")
    c.add_argument("--map", required=True)
    c.add_argument("--in", dest="inputs", nargs="+", required=True)
    c.add_argument("--words", type=int, default=6000)
    c.set_defaults(f=cmd_chunk)

    ad = sub.add_parser("add", help="append candidate record(s)")
    ad.add_argument("--map", required=True)
    ad.add_argument("--json")
    ad.add_argument("--file")
    ad.set_defaults(f=cmd_add)

    li = sub.add_parser("lint", help="schema, structure and gate check")
    li.add_argument("--map", required=True)
    li.set_defaults(f=cmd_lint)

    v = sub.add_parser("verify", help="every quote must exist verbatim in the research")
    v.add_argument("--map", required=True)
    v.add_argument("--sources", nargs="+")
    v.set_defaults(f=cmd_verify)

    mx = sub.add_parser("matrix", help="coverage grid and empty cells")
    mx.add_argument("--map", required=True)
    mx.add_argument("--limit", type=int, default=25)
    mx.set_defaults(f=cmd_matrix)

    q = sub.add_parser("queue", help="ranked production queue")
    q.add_argument("--map", required=True)
    q.add_argument("--limit", type=int, default=10)
    q.set_defaults(f=cmd_queue)

    r = sub.add_parser("render", help="write angle-map.md")
    r.add_argument("--map", required=True)
    r.add_argument("--out")
    r.set_defaults(f=cmd_render)

    b = sub.add_parser("bank", help="emit angle-bank-ready YAML")
    b.add_argument("--map", required=True)
    b.set_defaults(f=cmd_bank)

    a = p.parse_args()
    if a.cmd == "add" and not (a.json or a.file):
        die("add needs --json or --file")
    a.f(a)


if __name__ == "__main__":
    main()
