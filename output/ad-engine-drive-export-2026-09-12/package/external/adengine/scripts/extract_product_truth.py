#!/usr/bin/env python3
"""Seed packages/schema/seed/product_truth/ from the product-truth skills, ONCE.

Best-effort markdown parser over the per-product skills (velantra-weekender,
velantra-vivienne, velantra-straw-tote, velantra-boat-tote, velantra-meridian,
velantra-juliette, motilli, lunessa, ...). Emits one record per product in the
shape of services/engine/adengine/product_truth/schema.json and prints a
confidence report per field.

Heuristics (in order of trust):
  identity_block   heading containing IDENTITY -> first blockquote in the section (high);
                   else "Visual Description" bullets joined (low).
  mechanism_block  heading containing MECHANISM / FLAP / OPENING -> first blockquote (high).
  extra_blocks     other "VERBATIM ..." headings -> their first blockquote (high).
  colorways        "**Colorways:**" bullet (medium), a table under a heading containing
                   colorway/colors (medium), or a prose "Colorways ..." line with **bold** names (medium).
  banned_terms     lines containing never / banned / do not call / must not -> quoted terms (low-medium).
  dimensions       W x H x D patterns and "**Dimensions:**" bullets (medium).
  claims           "Claims:" / "claims safe to use:" / "Claims on label:" lines (medium).
  engine_notes     bullets under an Engine heading, grouped by sub-heading (medium).
  reference_assets image/video filenames in tables, joined to the nearest directory line (medium).
  qa_checklist     bullets / FAIL lines under QA, Pre-Flight, HARDWARE COUNT headings (medium).

Original image paths are kept verbatim in source_path_original; they get
re-uploaded and given asset ids later. Nothing here is imported by services/.

Usage:
  python scripts/extract_product_truth.py                # all product skills in ~/.claude/skills
  python scripts/extract_product_truth.py velantra-weekender motilli
  python scripts/extract_product_truth.py --skills-dir /path/to/skills --out packages/schema/seed/product_truth
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, re, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = os.path.join(REPO, "packages", "schema", "seed", "product_truth")
DEFAULT_SKILLS_DIR = os.path.expanduser("~/.claude/skills")
DEFAULT_SKILLS = ["velantra-weekender", "velantra-vivienne", "velantra-straw-tote", "velantra-boat-tote",
                  "velantra-meridian", "velantra-juliette", "motilli", "lunessa"]

sys.path.insert(0, os.path.join(REPO, "services", "engine"))

IMG_EXT = r"(?:jpe?g|png|webp|mp4|mov|heic)"
MATERIAL_WORDS = ["leather", "suede", "canvas", "twill", "straw", "brass", "gold hardware", "silver", "palladium",
                  "vegetable-tanned", "pebbled", "woven", "cotton", "nylon", "plastic", "glass"]


# ----------------------------------------------------------------- markdown helpers
def strip_frontmatter(text: str) -> tuple[dict, str]:
    fm = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip()
            text = text[end + 4:]
    return fm, text


def sections(lines: list[str]) -> list[dict]:
    """Split into {level, title, start, end, lines} by markdown headings, in document order."""
    heads = [(i, len(m.group(1)), m.group(2).strip()) for i, l in enumerate(lines)
             if (m := re.match(r"^(#{1,6})\s+(.*)$", l))]
    out = []
    for n, (i, level, title) in enumerate(heads):
        end = len(lines)
        for j, lvl, _ in heads[n + 1:]:
            if lvl <= level:
                end = j
                break
        out.append({"level": level, "title": title, "start": i, "end": end, "lines": lines[i + 1:end]})
    return out


def clean_title(t: str) -> str:
    t = re.sub(r"[\U0001F300-\U0001FAFF☀-➿⭐⚠️⏰-⏿\U0001F000-\U0001F2FF]", "", t)
    t = re.sub(r"[*_`]", "", t)
    return re.sub(r"\s+", " ", t).strip(" :-")


def first_blockquote(sec_lines: list[str]) -> str | None:
    buf, started = [], False
    for l in sec_lines:
        if l.startswith(">"):
            started = True
            buf.append(l[1:].lstrip() if l.startswith("> ") or l == ">" else l[1:])
        elif started:
            if l.strip() == "":
                break
            break
    if not buf:
        return None
    # Join wrapped lines the way the skills wrap them (hard wraps inside one paragraph).
    return "\n".join(buf).strip()


def blockquote_paragraph(text: str) -> str:
    """Re-flow a hard-wrapped blockquote into paragraphs (blank quote lines separate)."""
    paras, cur = [], []
    for l in text.split("\n"):
        if l.strip() == "":
            if cur:
                paras.append(" ".join(cur)); cur = []
        else:
            cur.append(l.strip())
    if cur:
        paras.append(" ".join(cur))
    return "\n\n".join(paras)


def unmd(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.strip()


def table_rows(sec_lines: list[str]) -> list[list[str]]:
    rows = []
    for l in sec_lines:
        if l.startswith("|") and not re.match(r"^\|\s*-{2,}", l):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def tables(sec_lines: list[str]) -> list[list[list[str]]]:
    """All tables in a section, each as [header, row, row...]."""
    out, cur = [], []
    for l in sec_lines + [""]:
        if l.startswith("|"):
            if re.match(r"^\|\s*:?-{2,}", l):
                continue
            cur.append([c.strip() for c in l.strip().strip("|").split("|")])
        elif cur:
            out.append(cur); cur = []
    return out


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "product"


# ----------------------------------------------------------------- extractors
class Extractor:
    def __init__(self, skill_name: str, path: str, text: str):
        self.skill = skill_name
        self.path = path
        self.fm, body = strip_frontmatter(text)
        self.lines = body.splitlines()
        self.secs = sections(self.lines)
        self.conf: OrderedDict[str, str] = OrderedDict()
        self.notes: list[str] = []
        self.sha = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # -- naming
    def name_and_slug(self) -> tuple[str, str, str, str]:
        m = next((re.search(r"\*\*Product:\*\*\s*(.+)", l) for l in self.lines
                  if re.search(r"\*\*Product:\*\*", l)), None)
        raw = m.group(1).strip() if m else next((l[2:] for l in self.lines if l.startswith("# ")), self.skill)
        name = re.split(r"\s+[—–-]{1,2}\s+", unmd(raw))[0].strip()
        name = name.split(",")[0].strip()
        parts = self.skill.split("-")
        brand = parts[0]
        if len(parts) > 1:
            slug = "-".join(parts[1:])
        else:
            slug = slugify(re.sub(rf"^{re.escape(brand)}\s+", "", name, flags=re.I))
        cat = next((unmd(re.search(r"\*\*Category:\*\*\s*(.+)", l).group(1)) for l in self.lines
                    if re.search(r"\*\*Category:\*\*", l)), None)
        if not cat:
            cat = self._guess_category(raw)
        self.conf["name"] = "high" if m else "medium"
        return name, slug, brand, cat

    def _guess_category(self, raw: str) -> str:
        t = (raw + " " + self.fm.get("description", "")).lower()
        for k, v in (("tote", "tote bag"), ("weekender", "travel bag"), ("top handle", "top handle bag"),
                     ("handbag", "handbag"), ("gumm", "supplement gummies"), ("bag", "bag")):
            if k in t:
                self.conf["category"] = "low"
                return v
        self.conf["category"] = "none"
        return "product"

    # -- bullets under "## Product Identity"
    def identity_bullets(self) -> dict[str, str]:
        out = {}
        for s in self.secs:
            if "product identity" in s["title"].lower():
                for l in s["lines"]:
                    m = re.match(r"^-\s+\*\*(.+?):?\*\*:?\s*(.*)$", l)
                    if m:
                        out[clean_title(m.group(1)).lower()] = m.group(2).strip()
                    m2 = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", l)
                    if m2:
                        out[clean_title(m2.group(1)).lower()] = m2.group(2).strip()
                break
        return out

    # -- verbatim blocks
    def verbatim_blocks(self) -> tuple[str | None, str | None, list[dict]]:
        """identity = IDENTITY heading; mechanism = best of MECHANISM > OPENING > FLAP headings
        (never CLOSURE / OCCLUSION); extras = every other VERBATIM/BLOCK heading with a blockquote."""
        cands = []
        for s in self.secs:
            t = s["title"].upper()
            if not ("VERBATIM" in t or "BLOCK" in t):
                continue
            bq = first_blockquote(s["lines"])
            if not bq:
                continue
            cands.append((s, t, blockquote_paragraph(bq)))
        identity, mechanism, extras = None, None, []
        ident = next((c for c in cands if "IDENTITY" in c[1]), None)
        if ident:
            identity = ident[2]; self.conf["identity_block"] = "high"
        mech = None
        for key in ("MECHANISM", "OPENING", "FLAP"):
            mech = next((c for c in cands if key in c[1] and "CLOSURE" not in c[1] and "OCCLUSION" not in c[1]
                         and "IDENTITY" not in c[1]), None)
            if mech:
                break
        if mech:
            mechanism = mech[2]; self.conf["mechanism_block"] = "high"
        for c in cands:
            if c is ident or c is mech:
                continue
            m = re.search(r"\((.*)\)", clean_title(c[0]["title"]))
            name = clean_title(re.sub(r"\(.*\)", "", c[0]["title"]))
            name = re.sub(r"^VERBATIM\s+", "", name, flags=re.I).replace(" BLOCK", "").strip()
            extras.append({"name": name.lower(), "text": c[2], "when": m.group(1).strip() if m else None})
        if identity is None:
            identity = self.visual_description_fallback()
        if mechanism is None:
            self.conf["mechanism_block"] = "none"
            self.notes.append("no MECHANISM/FLAP/OPENING block found; mechanism_block=null")
        self.conf["extra_blocks"] = "high" if extras else "none"
        return identity, mechanism, extras

    def visual_description_fallback(self) -> str | None:
        for s in self.secs:
            if "visual description" in s["title"].lower():
                bullets = [unmd(re.sub(r"^-\s+", "", l)) for l in s["lines"] if l.startswith("- ")]
                if bullets:
                    self.conf["identity_block"] = "low"
                    self.notes.append("no VERBATIM IDENTITY BLOCK; identity_block assembled from Visual Description bullets")
                    return "\n".join(bullets)
        self.conf["identity_block"] = "none"
        self.notes.append("no identity block found")
        return None

    # -- colorways
    def colorways(self, ib: dict[str, str]) -> list[dict]:
        out: list[dict] = []
        seen = set()

        def add(name, desc="", hexv=None, hero=False, ref=None):
            key = name.strip().lower()
            if not key or key in seen or len(key) > 40:
                return
            seen.add(key)
            entry = OrderedDict(name=name.strip(), description=unmd(desc).strip(" .;"))
            if hexv:
                entry["hex"] = hexv
            if hero:
                entry["hero"] = True
            if ref:
                entry["reference"] = ref
            out.append(entry)

        # 1. tables under a colorway-ish heading
        for s in self.secs:
            if re.search(r"colorway|colou?rs\b", s["title"], re.I):
                for tbl in tables(s["lines"]):
                    hdr = [h.lower() for h in tbl[0]]
                    if not any("colorway" in h or "color" in h for h in hdr):
                        continue
                    ci = next(i for i, h in enumerate(hdr) if "colorway" in h or "color" in h)
                    hi = next((i for i, h in enumerate(hdr) if "hex" in h), None)
                    ni = next((i for i, h in enumerate(hdr) if "note" in h or "body" in h or "desc" in h), None)
                    ri = next((i for i, h in enumerate(hdr) if "ref" in h or "file" in h or "image" in h), None)
                    ti = next((i for i, h in enumerate(hdr) if "strap" in h or "trim" in h), None)
                    for row in tbl[1:]:
                        if len(row) <= ci:
                            continue
                        name = unmd(row[ci])
                        desc = " ".join(x for x in [unmd(row[ni]) if ni is not None and ni < len(row) else "",
                                                     ("straps/trim: " + unmd(row[ti])) if ti is not None and ti < len(row) else ""] if x)
                        hexv = None
                        if hi is not None and hi < len(row):
                            hm = re.search(r"#[0-9a-fA-F]{6}", row[hi]); hexv = hm.group(0) if hm else None
                        ref = unmd(row[ri]) if ri is not None and ri < len(row) and re.search(IMG_EXT, row[ri]) else None
                        add(name, desc, hexv, ref=ref)
                    self.conf["colorways"] = "medium"
        # 2. "**Colorways:**" bullet
        cw = ib.get("colorways")
        if cw:
            head = re.split(r"\.\s|\*\*", cw)[0]
            for part in head.split(","):
                part = part.strip(" .")
                m = re.match(r"([\w\- ]+?)\s*(?:\((.*?)\))?$", part)
                if m:
                    add(m.group(1).title() if m.group(1).islower() else m.group(1), m.group(2) or "",
                        hero="hero" in (m.group(2) or "").lower())
            self.conf.setdefault("colorways", "medium")
        # 3. prose line: "Colorways (...): **light chocolate** (...), **army green** (...)"
        for l in self.lines:
            if re.match(r"^\s*Colorways\b", l) and "**" in l:
                for m in re.finditer(r"\*\*([^*]+)\*\*\s*\(([^)]*)\)", l):
                    add(m.group(1).title(), m.group(2), hero="hero" in m.group(2).lower())
                self.conf.setdefault("colorways", "medium")
        # hero from "X is the HERO"
        for l in self.lines:
            m = re.match(r"^\s*(\w[\w ]*?) is the HERO", l)
            if m:
                for c in out:
                    if c["name"].lower() == m.group(1).lower():
                        c["hero"] = True
        if not out:
            self.conf["colorways"] = "none"
        return out

    # -- banned terms
    NEG_BEFORE = re.compile(r"(?:\bnever\b|\bbanned\b|\bno\b|\bnot\b|\bdo not\b|\bdon't\b|\bmust not\b|\bnor\b)(?:\s+\S+){0,6}\s*$", re.I)
    NEG_AFTER = re.compile(r"^[^.;]*?(?:\b(?:is|are)\s+banned\b|\bnever\s+appears?\b|\bmust\s+never\s+appear\b|\bbanned\s+from\b)", re.I)
    QUOTE = re.compile(r"[\"\u201c\u201d]")

    def banned_terms(self, name: str) -> list[dict]:
        """Quoted terms inside a negated clause: 'never write "X"', 'no "X"', '"X" is banned', '"X" never appears'.

        Quotes are paired by splitting on quote characters (odd segments are quoted), so a long
        quoted sentence earlier on the line cannot swallow the opening quote of a later term."""
        out, seen = [], set()
        lname = name.lower()
        for l in self.lines:
            if l.startswith("|") or l.startswith(">"):
                continue
            if not re.search(r"\b(never|banned|do not|must not|not allowed|no)\b", l, re.I):
                continue
            plain = unmd(l)
            segs = self.QUOTE.split(plain)
            for i in range(1, len(segs), 2):
                term = segs[i].strip()
                low = term.lower()
                if not (4 <= len(term) <= 40) or low in seen or len(term.split()) > 5 or low in lname:
                    continue
                if re.search(IMG_EXT + r"$", term) or low.startswith(("never ", "no ", "not ")):
                    continue
                before = re.split(r"[.;:]\s", "".join(segs[:i]))[-1]
                after = "".join(segs[i + 1:])
                if not (self.NEG_BEFORE.search(before) or self.NEG_AFTER.search(after)):
                    continue
                seen.add(low)
                reason = re.sub(r"\s+", " ", plain)[:220]
                scope = "prompt" if re.search(r"prompt", plain, re.I) else ("copy" if re.search(r"copy|customer|brief", plain, re.I) else "any")
                out.append(OrderedDict(term=term, reason=reason, scope=scope))
        self.conf["banned_terms"] = "medium" if out else "none"
        return out

    # -- dimensions
    def dimensions(self, ib: dict[str, str]) -> dict:
        d: dict = {}
        pat = re.compile(r"(\d+(?:\.\d+)?)\s*(?:\"|in(?:ches)?)?\s*W\s*[x×]\s*(\d+(?:\.\d+)?)\s*(?:\"|in(?:ches)?)?\s*H\s*[x×]\s*(\d+(?:\.\d+)?)\s*(?:\"|in(?:ches)?)?\s*D", re.I)
        for l in self.lines:
            m = pat.search(l)
            if m:
                d.update(width_in=float(m.group(1)), height_in=float(m.group(2)), depth_in=float(m.group(3)), raw=unmd(m.group(0)))
                break
        dim_line = ib.get("dimensions")
        if dim_line and "raw" not in d:
            d["raw"] = unmd(dim_line)
            m = re.search(r"(\d+(?:\.\d+)?)\s*cm\s*\((\d+(?:\.\d+)?)\s*in\)", dim_line)
            if m:
                d["width_cm"] = float(m.group(1)); d["width_in"] = float(m.group(2)); d["note"] = "width only"
        for l in self.lines:
            m = re.search(r"\*\*Count:\*\*\s*(.+)", l)
            if m:
                d["count"] = unmd(m.group(1))
        self.conf["dimensions"] = "medium" if d else "none"
        return d

    # -- materials
    def materials(self, identity: str | None) -> list[str]:
        """Material words in the identity block, ignoring negated mentions ('no canvas', 'never silver')."""
        text = (identity or "").lower()
        found = []
        for w in MATERIAL_WORDS:
            hits = [m for m in re.finditer(re.escape(w), text)]
            pos = [m for m in hits if not re.search(r"\b(?:no|not|never|without|nor|or)\s+(?:\w+\s+){0,2}$", text[max(0, m.start() - 24):m.start()])]
            if pos:
                found.append(w)
        self.conf["materials"] = "low" if found else "none"
        return found

    # -- claims
    def claims(self) -> list[dict]:
        out = []
        for i, l in enumerate(self.lines):
            src = f"{self.path}#L{i + 1 + self._fm_offset()}"
            m = re.search(r"claims safe to use:\s*([^.]+)\.", l, re.I)
            if m:
                for c in m.group(1).split(","):
                    out.append(OrderedDict(claim=unmd(c).strip(), verified=True, source=src))
            m = re.search(r"\*\*Claims:\*\*\s*OK\s*[—–-]+\s*(.+?)\.\s*BANNED", l)
            if m:
                for c in m.group(1).split(","):
                    out.append(OrderedDict(claim=unmd(c).strip(), verified=True, source=src))
            m = re.search(r"\*\*Claims on label:\*\*\s*(.+)$", l)
            if m:
                for c in re.findall(r"\"([^\"]+)\"", m.group(1)):
                    out.append(OrderedDict(claim=c.strip(), verified=True, source=src))
        self.conf["claims"] = "medium" if out else "none"
        return [c for c in out if c["claim"]]

    def _fm_offset(self) -> int:
        raw = open(self.path, encoding="utf-8").read()
        return raw.count("\n", 0, len(raw) - len("\n".join(self.lines))) if raw.startswith("---") else 0

    # -- engine notes
    def engine_notes(self) -> list[dict]:
        out = []
        for s in self.secs:
            if not re.search(r"\bengine", s["title"], re.I):
                continue
            subs = [x for x in self.secs if s["start"] < x["start"] < s["end"] and x["level"] == s["level"] + 1]
            if subs:
                for sub in subs:
                    engine = clean_title(sub["title"])
                    for l in sub["lines"]:
                        if l.startswith("- "):
                            note = unmd(l[2:])
                            out.append(OrderedDict(engine=engine, note=note[:600]))
            else:
                for l in s["lines"]:
                    if l.startswith("- "):
                        m = re.match(r"^-\s+\*\*(.+?)\*\*\s*[—–-]*\s*(.*)$", l)
                        engine = clean_title(m.group(1)) if m else "general"
                        note = unmd(m.group(2) if m else l[2:])
                        out.append(OrderedDict(engine=engine, note=note[:600]))
        self.conf["engine_notes"] = "medium" if out else "none"
        return out[:40]

    # -- reference assets
    def _first_dir(self) -> str | None:
        for l in self.lines:
            m = re.match(r"^\s*`?((?:~|/|brands/)[^`|]*?/)`?\s*$", l)
            if m:
                return m.group(1).strip()
        return None

    @staticmethod
    def _join(cur_dir: str | None, f: str) -> str:
        if f.startswith(("/", "~", "brands/")) or not cur_dir:
            return f
        base = cur_dir.rstrip("/")
        head = f.split("/")[0]
        if base.endswith("/" + head) or base == head:      # `colors/` + `colors/Navy/07.jpg`
            base = base[: -len(head) - 1] if base != head else ""
        joined = (base + "/" + f) if base else f
        return os.path.normpath(joined) if not joined.startswith("~") else "~" + os.path.normpath(joined[1:])

    def reference_assets(self) -> list[dict]:
        out, seen = [], set()
        cur_dir = None
        fallback_dir = self._first_dir()
        dir_pat = re.compile(r"^\s*`?((?:~|/|brands/)[^`|]*?/)`?\s*$")
        inline_dir = re.compile(r"`((?:~|/|brands/)[^`]*?/)`")
        for l in self.lines:
            m = dir_pat.match(l)
            if m:
                cur_dir = m.group(1).strip()
            else:
                ms = inline_dir.findall(l)
                if ms:
                    cur_dir = ms[-1].strip()
            if not l.startswith("|"):
                continue
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) < 2 or re.match(r"^:?-{2,}", cells[0]):
                continue
            desc = unmd(" ".join(cells[1:]))
            low = desc.lower()
            # directory rows ("| `brands/.../product-references/` | canonical i2i seeds |")
            dm = re.match(r"^`((?:~|/|brands/)[^`]*?/)`$", cells[0])
            if dm:
                if re.search(r"read only|competitor", low) or dm.group(1) in seen:
                    continue
                seen.add(dm.group(1))
                role = "master_seed" if "seed" in low and not any(a["role"] == "master_seed" for a in out) else "angle"
                out.append(OrderedDict(role=role, asset_id=None, source_path_original=dm.group(1), note=desc[:200] or None, colorway=None))
                continue
            files = re.findall(r"`([^`]+\." + IMG_EXT + r")`", cells[0])
            if not files:
                continue
            if re.search(r"\b(hero|primary|default)\b", low) and not any(a["role"] == "master_seed" for a in out):
                role = "master_seed"
            elif re.search(r"macro|detail|hardware|label|close-up|interior|texture|gummy\b", low):
                role = "detail"
            elif re.search(r"lifestyle|model|hand|woman|holding|carry|scale", low):
                role = "lifestyle"
            else:
                role = "angle"
            for f in files:
                if f in seen:
                    continue
                seen.add(f)
                path = self._join(cur_dir or fallback_dir, f)
                mcw = re.search(r"colors/([^/]+)/", f)
                out.append(OrderedDict(role=role, asset_id=None, source_path_original=path,
                                       note=desc[:200] or None, colorway=mcw.group(1) if mcw else None))
        # hardcoded PRIMARY absolute path lines
        for l in self.lines:
            m = re.match(r"^\s*(/[^`\s]+(?:\s[^`\s]+)*\." + IMG_EXT + r")\s*$", l)
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                for a in out:
                    if a["role"] == "master_seed":
                        a["role"] = "angle"
                out.insert(0, OrderedDict(role="master_seed", asset_id=None, source_path_original=m.group(1),
                                          note="hardcoded primary reference", colorway=None))
        self.conf["reference_assets"] = "medium" if out else "none"
        if out and any(not a["source_path_original"].startswith(("/", "~", "brands/")) for a in out):
            self.conf["reference_assets"] = "low"
            self.notes.append("some reference filenames could not be joined to a directory")
        elif out and any(a["source_path_original"].startswith(fallback_dir or "\0") for a in out) and not cur_dir:
            self.conf["reference_assets"] = "low"
        return out

    def attach_colorway_refs(self, colorways: list[dict], refs: list[dict]) -> None:
        """Colorway table refs (e.g. colors/Navy/07.jpg) become angle assets and get absolute-ish paths."""
        cur = None
        for l in self.lines:
            ms = re.findall(r"`((?:~|/|brands/)[^`]*?colors/)`", l)
            if ms:
                cur = ms[-1]; break
        have = {a["source_path_original"] for a in refs}
        for c in colorways:
            ref = c.get("reference")
            if not ref:
                continue
            path = self._join(cur, ref)
            c["reference"] = path
            if path not in have:
                refs.append(OrderedDict(role="angle", asset_id=None, source_path_original=path,
                                        note=f"canonical {c['name']} reference", colorway=c["name"]))
                have.add(path)

    # -- QA checklist
    def qa_checklist(self) -> list[str]:
        out = []
        for s in self.secs:
            t = s["title"]
            if not re.search(r"\bQA\b|pre-?flight|hardware count|fail on sight|frame qa", t, re.I) or re.search(r"\bLAW\b", t):
                continue
            for l in s["lines"]:
                if re.match(r"^\s*(?:[-*]|\d+[a-z]?\.)\s+", l):
                    out.append(unmd(re.sub(r"^\s*(?:[-*]|\d+[a-z]?\.)\s+", "", l))[:300])
                elif re.match(r"^(CORRECT|FAIL)\b", l):
                    out.append(unmd(l)[:300])
                elif l.startswith("|") and not re.match(r"^\|\s*:?-{2,}", l):
                    cells = [unmd(c.strip()) for c in l.strip().strip("|").split("|")]
                    if cells and cells[0].lower() not in ("fitting", "file", "path"):
                        out.append(" | ".join(cells)[:300])
        for l in self.lines:
            m = re.match(r"^\*\*FAIL on sight:\*\*\s*(.+)$", l)
            if m:
                out.extend(unmd(x).strip() for x in m.group(1).split("\u00b7"))
        self.conf["qa_checklist"] = "medium" if out else "none"
        return out[:30]

    # -- required phrases
    def required_phrases(self) -> list[str]:
        out = []
        for l in self.lines:
            for m in re.finditer(r"(?:must pin|Paste|add to VOICE|say)[:\s]+\*?[\"“*]([^\"”*]{12,400})[\"”*]", l):
                out.append(m.group(1).strip())
        self.conf["required_phrases"] = "low" if out else "none"
        return out[:10]

    # -- assemble
    def record(self) -> dict:
        name, slug, brand, cat = self.name_and_slug()
        ib = self.identity_bullets()
        identity, mechanism, extras = self.verbatim_blocks()
        rec = OrderedDict()
        rec["name"] = name
        rec["slug"] = slug
        rec["brand_slug"] = brand
        rec["category"] = cat
        pos = ib.get("positioning") or ib.get("positioning (internal)")
        rec["positioning"] = unmd(pos) if pos else None
        price = ib.get("price") or next((m.group(1) for l in self.lines if (m := re.search(r"\*\*Price:\*\*\s*(\$[\d.,]+)", l))), None)
        rec["price"] = price
        rec["identity_block"] = identity or ""
        rec["mechanism_block"] = mechanism
        rec["extra_blocks"] = extras
        rec["colorways"] = self.colorways(ib)
        rec["dimensions"] = self.dimensions(ib)
        rec["materials"] = self.materials(identity)
        rec["banned_terms"] = self.banned_terms(name)
        rec["required_phrases"] = self.required_phrases()
        rec["claims"] = self.claims()
        rec["engine_notes"] = self.engine_notes()
        rec["reference_assets"] = self.reference_assets()
        self.attach_colorway_refs(rec["colorways"], rec["reference_assets"])
        rec["qa_checklist"] = self.qa_checklist()
        rec["version"] = 1
        rec["extracted_from"] = OrderedDict(path=self.path, sha256=self.sha,
                                            extracted_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                            extractor="scripts/extract_product_truth.py")
        rec["extraction"] = OrderedDict(confidence=self.conf, notes=self.notes)
        return rec


def discover(skills_dir: str) -> list[str]:
    names = []
    for n in sorted(os.listdir(skills_dir)):
        p = os.path.join(skills_dir, n, "SKILL.md")
        if not os.path.isfile(p) or n.endswith("-concept"):
            continue
        head = open(p, encoding="utf-8").read(1500)
        if re.search(r"description:.*\bproduct scale\b", head, re.I):
            names.append(n)
    return names


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skills", nargs="*", help="skill folder names (default: discover product-scale skills)")
    ap.add_argument("--skills-dir", default=DEFAULT_SKILLS_DIR)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--no-validate", action="store_true")
    args = ap.parse_args()

    names = args.skills or discover(args.skills_dir) or DEFAULT_SKILLS
    os.makedirs(args.out, exist_ok=True)
    validate = None
    if not args.no_validate:
        try:
            from adengine.product_truth import validate  # type: ignore
        except Exception as e:  # pragma: no cover
            print(f"WARN: schema validation unavailable ({e})", file=sys.stderr)

    ok = 0
    for n in names:
        path = os.path.join(args.skills_dir, n, "SKILL.md")
        if not os.path.isfile(path):
            print(f"SKIP {n}: no SKILL.md at {path}")
            continue
        text = open(path, encoding="utf-8").read()
        rec = Extractor(n, path, text).record()
        if validate:
            try:
                validate(rec)
            except Exception as e:
                print(f"INVALID {n}: {e}")
                continue
        out = os.path.join(args.out, f"{rec['brand_slug']}-{rec['slug']}.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2, ensure_ascii=False); f.write("\n")
        ok += 1
        conf = rec["extraction"]["confidence"]
        summary = ", ".join(f"{k}={v}" for k, v in conf.items())
        print(f"OK {n} -> {os.path.relpath(out, REPO)}")
        print(f"   {summary}")
        for note in rec["extraction"]["notes"]:
            print(f"   note: {note}")
    print(f"{ok}/{len(names)} records written to {os.path.relpath(args.out, REPO)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
