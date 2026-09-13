#!/usr/bin/env python3
"""
factory.py — the internal UGC factory. Script in, finished captioned ad out, resumable.

Blueprint: _engine/pipelines/BLUEPRINT-internal-ugc-factory.md
Laws baked in, not optional:
  ONE-TAKE AUDIO   The ad's audio is one continuous ElevenLabs take. Video clips are
                   lip-synced to slices of it, then the ORIGINAL take is laid back over
                   the assembled video. Per-clip audio is always discarded.
  KEYFRAME-FIRST   Every scene renders from its authored keyframe. No clip ever seeds
                   from another clip's last frame.
  SENTENCE-SAFE    Audio chunks end on sentence boundaries. An under-filled chunk is
                   fine; a severed sentence is not.

Usage:
  python3 factory.py run <job.json> [--until vo|align|chunks|render|qa|assemble|captions]
  python3 factory.py status <job.json>

Job shape:
{
  "job_id": "MOT-WRONGSIGNAL-F1",
  "workdir": "/abs/path",                    # all artifacts + state live here
  "script": "full spoken script...",          # or "script_file": "/abs/path.txt"
  "voice_id": "nSzdVDjK1sQkrCshCsUT",
  "keyframe": "/abs/actor.png",              # dialogue-scene keyframe (talking head)
  "engine": "seedance",                      # dialogue engine: seedance | omni+fal
  "aspect_ratio": "9:16", "resolution": "720p",
  "identity_line": "same woman as the reference image, ...",
  "max_chunk_seconds": 13.8, "max_inflight": 3,
  "captions": true
}

State: <workdir>/factory.db (sqlite) records step status/attempts for observability;
artifacts on disk are authoritative — a step whose artifact exists and passes its check
is skipped, so any crash resumes with `run` and never re-spends.
"""
import argparse
import json
import math
import os
import pathlib
import re
import sqlite3
import ssl
import subprocess
import sys
import time
import urllib.request

import certifi

ROOT = pathlib.Path(__file__).resolve().parents[1]          # _engine/
VAULT = ROOT.parent                                          # marketing brain/
SSL_CTX = ssl.create_default_context(cafile=certifi.where())

KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
EL_API = "https://api.elevenlabs.io/v1"
SEEDANCE_MODEL = "bytedance/seedance-2"
SEEDANCE_CR_PER_SEC = 69          # ~414cr/6s observed (reference_seedance_askme_run_learnings)

SENT_END = re.compile(r"(?<=[.!?])\s+")


# ----------------------------------------------------------------------------- utilities
def env_key(name):
    if os.environ.get(name):
        return os.environ[name]
    envf = VAULT / ".env"
    for line in envf.read_text().splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"{name} not found in {envf}")


def http_json(method, url, headers=None, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as r:
        return json.loads(r.read())


def sh(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:4])}... failed:\n{p.stderr[-1200:]}")
    return p.stdout


def media_duration(path):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
              "-of", "default=nw=1:nk=1", str(path)]).strip()
    return float(out.splitlines()[0])


def load_tool(name):
    """Import a sibling tool script (pick_take etc.) as a module."""
    import importlib.util
    p = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class State:
    """Step ledger. Disk artifacts are authoritative; this is the observable record."""

    def __init__(self, workdir):
        self.db = sqlite3.connect(workdir / "factory.db")
        self.db.execute("CREATE TABLE IF NOT EXISTS steps("
                        "key TEXT PRIMARY KEY, status TEXT, detail TEXT, "
                        "attempts INT DEFAULT 0, updated TEXT)")
        self.db.commit()

    def set(self, key, status, detail=""):
        self.db.execute(
            "INSERT INTO steps(key,status,detail,attempts,updated) VALUES(?,?,?,1,datetime('now')) "
            "ON CONFLICT(key) DO UPDATE SET status=excluded.status, detail=excluded.detail, "
            "attempts=attempts+1, updated=excluded.updated", (key, status, str(detail)[:500]))
        self.db.commit()

    def rows(self):
        return self.db.execute("SELECT key,status,attempts,updated FROM steps ORDER BY key").fetchall()


# ----------------------------------------------------------------------------- stage: vo
def stage_vo(job, wd, st):
    """One continuous take for the whole script. eleven_v3, stability 0.0
    (multilingual_v2 reads robotic — feedback_elevenlabs_v3_creative_vo)."""
    mp3, wav = wd / "vo_full.mp3", wd / "vo_full.wav"
    if wav.exists() and media_duration(wav) > 5:
        return
    key = env_key("ELEVENLABS_API_KEY")
    body = {"text": job["script"], "model_id": "eleven_v3",
            "voice_settings": {"stability": 0.0}}
    req = urllib.request.Request(
        f"{EL_API}/text-to-speech/{job['voice_id']}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900, context=SSL_CTX) as r:
        mp3.write_bytes(r.read())
    sh(["ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "48000", str(wav)])
    st.set("vo", "done", f"{media_duration(wav):.1f}s")
    print(f"[vo] {media_duration(wav):.1f}s one-take VO rendered")


# ----------------------------------------------------------------------------- stage: align
def stage_align(job, wd, st):
    """Word timestamps by transcribing our own VO — independent of TTS timestamp support."""
    out = wd / "alignment.json"
    if out.exists():
        return
    key = env_key("ELEVENLABS_API_KEY")
    wav = wd / "vo_full.mp3"
    boundary = "----factoryalign"
    body = bytearray()
    for k, v in {"model_id": "scribe_v1", "timestamps_granularity": "word"}.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"vo.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode()
    body += wav.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{EL_API}/speech-to-text", data=bytes(body),
        headers={"xi-api-key": key,
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=900, context=SSL_CTX) as r:
        out.write_bytes(r.read())
    st.set("align", "done")
    print("[align] word timestamps captured")


# ----------------------------------------------------------------------------- stage: chunks
def stage_chunks(job, wd, st):
    """Sentence-safe AUDIO chunks: group whole sentences to <= max seconds, slice the WAV."""
    manifest_f = wd / "chunks" / "manifest.json"
    if manifest_f.exists():
        return json.loads(manifest_f.read_text())
    (wd / "chunks").mkdir(exist_ok=True)

    words = [w for w in json.loads((wd / "alignment.json").read_text())["words"]
             if w.get("type") == "word"]
    sentences = [s.strip() for s in SENT_END.split(job["script"].strip()) if s.strip()]

    # Walk the aligned words across the sentences; VO was generated from this exact text
    # so counts line up modulo transcription quirks, absorbed by the running pointer.
    def norm(t):
        return re.sub(r"[^a-z0-9]", "", t.lower())
    spans, wi = [], 0
    for sent in sentences:
        n = len(sent.split())
        take = min(n, len(words) - wi)
        seg = words[wi:wi + take]
        # nudge the pointer if the transcriber merged/split tokens
        drift = len([w for w in seg if norm(w["text"])]) - n
        wi += take + (0 if abs(drift) > 3 else 0)
        if not seg:
            break
        spans.append({"text": sent, "start": seg[0]["start"], "end": seg[-1]["end"],
                      "seg": seg})
        wi = min(wi, len(words))

    # A single sentence longer than the cap gets split at the comma nearest its time
    # midpoint — the one place a beat may end mid-sentence, because a speaker already
    # pauses there. Without this, the clip container (15s max) runs shorter than the
    # audio chunk and the mouth cuts off before the words do.
    max_s = job.get("max_chunk_seconds", 13.8)

    def split_long(sp):
        if sp["end"] - sp["start"] <= max_s:
            return [sp]
        mid = (sp["start"] + sp["end"]) / 2
        commas = [(k, w) for k, w in enumerate(sp["seg"][:-1]) if w["text"].rstrip().endswith(",")]
        if not commas:
            return [sp]
        k, w = min(commas, key=lambda kw: abs(kw[1]["end"] - mid))
        nth = sum(1 for _, x in commas if x["end"] <= w["end"])
        parts = sp["text"].split(",")
        left_t = ",".join(parts[:nth]) + ","
        right_t = ",".join(parts[nth:]).strip()
        left = {"text": left_t.strip(), "start": sp["start"], "end": w["end"],
                "seg": sp["seg"][:k + 1]}
        right = {"text": right_t, "start": sp["seg"][k + 1]["start"], "end": sp["end"],
                 "seg": sp["seg"][k + 1:]}
        return split_long(left) + split_long(right)

    spans = [piece for sp in spans for piece in split_long(sp)]
    for sp in spans:
        sp.pop("seg", None)

    vo_len = media_duration(wd / "vo_full.wav")
    chunks, cur = [], None
    for sp in spans:
        if cur is None:
            cur = dict(sp)
        elif sp["end"] - cur["start"] <= max_s:
            cur["end"], cur["text"] = sp["end"], cur["text"] + " " + sp["text"]
        else:
            chunks.append(cur)
            cur = dict(sp)
    if cur:
        chunks.append(cur)
    # boundaries: end each chunk exactly where the next begins so concat == the VO
    for i, c in enumerate(chunks):
        c["start"] = chunks[i - 1]["end"] if i else 0.0
        if i == len(chunks) - 1:
            c["end"] = vo_len
        c["index"], c["duration"] = i + 1, round(c["end"] - c["start"], 3)
        f = wd / "chunks" / f"chunk_{i + 1:02d}.wav"
        sh(["ffmpeg", "-y", "-i", str(wd / "vo_full.wav"), "-ss", str(c["start"]),
            "-to", str(c["end"]), "-c", "pcm_s16le", str(f)])
        c["file"] = str(f)
    manifest_f.write_text(json.dumps(chunks, indent=1))
    st.set("chunks", "done", f"{len(chunks)} chunks")
    est = sum(min(15, math.ceil(c["duration"]) + 1) for c in chunks) * SEEDANCE_CR_PER_SEC
    print(f"[chunks] {len(chunks)} sentence-safe chunks, {vo_len:.0f}s total; "
          f"kie estimate ~{est:,} credits")
    return chunks


# ----------------------------------------------------------------------------- engines
def kie_upload(path, cache_f):
    cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
    if path in cache:
        return cache[path]
    key = env_key("KIE_API_KEY")
    for attempt in range(4):
        p = subprocess.run(["curl", "-sS", "-X", "POST", KIE_UPLOAD,
                            "-H", f"Authorization: Bearer {key}",
                            "-F", f"file=@{path}", "-F", "uploadPath=ugc-factory"],
                           capture_output=True, text=True)
        try:
            url = json.loads(p.stdout)["data"]["downloadUrl"]
            cache[path] = url
            cache_f.write_text(json.dumps(cache, indent=1))
            return url
        except (json.JSONDecodeError, KeyError, TypeError):
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"kie upload failed for {path}: {p.stdout[:300]}")


def seedance_prompt(job):
    return (
        "UGC iPhone selfie video, locked-off, real-time pacing. "
        f"{job['identity_line']} "
        "She is speaking straight into the front camera, animated and expressive like "
        "FaceTiming a friend about something she actually looked into, natural hand "
        "gestures, voice rising and falling. Subject lip-syncs to the provided audio, "
        "natural pauses, expressive intonation, energy held to the final word, never "
        "monotone. No cuts, no zooms, no transitions, no music, no captions. "
        f"Vertical {job.get('aspect_ratio', '9:16')}. ONE CONTINUOUS SHOT."
    )


def stage_render(job, wd, st, chunks):
    """Dialogue scenes on Seedance via kie: keyframe + audio chunk per scene, an in-flight
    pool, tasks.json resume so a crash never re-charges, and a smoke gate on scene 1."""
    clips_dir = wd / "clips"
    clips_dir.mkdir(exist_ok=True)
    cache_f, tasks_f = wd / "upload_cache.json", wd / "tasks.json"
    tasks = json.loads(tasks_f.read_text()) if tasks_f.exists() else {}
    key = env_key("KIE_API_KEY")
    keyframe_url = kie_upload(job["keyframe"], cache_f)
    prompt = seedance_prompt(job)

    def dest(i):
        return clips_dir / f"seg-{i}.mp4"

    def submit(c):
        i = str(c["index"])
        if i in tasks:
            return tasks[i]
        inp = {"prompt": prompt,
               "aspect_ratio": job.get("aspect_ratio", "9:16"),
               "resolution": job.get("resolution", "720p"),
               "duration": min(15, math.ceil(c["duration"]) + 1),
               "generate_audio": True,
               "reference_image_urls": [keyframe_url],
               "reference_audio_urls": [kie_upload(c["file"], cache_f)]}
        # kie returns {"data": null, "code": ..., "msg": ...} on throttle/errors — an
        # explicit null defeats .get(key, {}) — so surface msg and retry with backoff.
        last = None
        for attempt in range(5):
            r = http_json("POST", f"{KIE_API}/jobs/createTask",
                          {"Authorization": f"Bearer {key}"},
                          {"model": SEEDANCE_MODEL, "input": inp})
            tid = (r.get("data") or {}).get("taskId")
            if tid:
                tasks[i] = tid
                tasks_f.write_text(json.dumps(tasks, indent=1))
                st.set(f"render.{i}", "submitted", tid)
                return tid
            last = f"code={r.get('code')} msg={r.get('msg') or r.get('message')}"
            msg = (last or "").lower()
            if "credit" in msg or "balance" in msg:
                raise RuntimeError(f"seg {i}: OUT OF KIE CREDITS — {last}")
            st.set(f"render.{i}", "retry", last)
            time.sleep(20 * (attempt + 1))
        raise RuntimeError(f"seg {i}: createTask failed after 5 attempts — {last}")

    def check(c):
        i = str(c["index"])
        r = http_json("GET", f"{KIE_API}/jobs/recordInfo?taskId={tasks[i]}",
                      {"Authorization": f"Bearer {key}"})
        d = r.get("data", {})
        state = d.get("state") or d.get("status")
        if state in ("success", "SUCCESS"):
            res = d.get("resultJson")
            res = json.loads(res) if isinstance(res, str) else (res or d)
            url = ((res.get("resultUrls") or res.get("result_urls") or [None])[0])
            if not url:
                raise RuntimeError(f"seg {i}: success but no result url: {d}")
            sh(["curl", "-sS", "-L", "-o", str(dest(i)), url])
            tasks.pop(i, None)
            tasks_f.write_text(json.dumps(tasks, indent=1))
            st.set(f"render.{i}", "done")
            print(f"[render] seg {i} landed ({media_duration(dest(i)):.1f}s)")
            return True
        if state in ("fail", "FAIL", "failed"):
            tasks.pop(i, None)
            tasks_f.write_text(json.dumps(tasks, indent=1))
            st.set(f"render.{i}", "failed", d.get("failMsg", ""))
            raise RuntimeError(f"seg {i} failed on kie: {d.get('failMsg', d)}")
        return False

    todo = [c for c in chunks if not dest(c["index"]).exists()]
    if not todo:
        return
    # Smoke gate: land scene 1 alone before any fan-out.
    first = next((c for c in todo if c["index"] == 1), None)
    if first:
        submit(first)
        while not check(first):
            time.sleep(15)
        acc = qa_clip(job, wd, first)
        if acc is not None and acc < 0.80:
            raise RuntimeError(f"SMOKE GATE: seg 1 accuracy {acc} — inspect before fan-out")
        print(f"[render] smoke gate passed (seg 1 accuracy {acc})")
        todo = [c for c in todo if c["index"] != 1]

    inflight = []
    max_in = job.get("max_inflight", 3)
    while todo or inflight:
        while todo and len(inflight) < max_in:
            c = todo.pop(0)
            submit(c)
            inflight.append(c)
        time.sleep(15)
        for c in inflight[:]:
            if check(c):
                inflight.remove(c)


# ----------------------------------------------------------------------------- stage: qa
_PT = None


def qa_clip(job, wd, c):
    """Word accuracy of the clip's own (discarded) audio vs the chunk text — verifies the
    mouth performed the right words. Tolerant threshold: it is a re-speak, not our VO."""
    global _PT
    if _PT is None:
        _PT = load_tool("pick_take")
    clip = wd / "clips" / f"seg-{c['index']}.mp4"
    heard = _PT.transcribe(clip, env_key("ELEVENLABS_API_KEY"))
    if not heard:
        return None
    return round(_PT.word_accuracy(heard, c["text"]), 3)


def stage_qa(job, wd, st, chunks):
    report_f = wd / "qa_report.json"
    done = json.loads(report_f.read_text()) if report_f.exists() else {}
    bad = []
    for c in chunks:
        i = str(c["index"])
        if i not in done:
            done[i] = qa_clip(job, wd, c)
            report_f.write_text(json.dumps(done, indent=1))
        if done[i] is not None and done[i] < 0.80:
            bad.append((i, done[i]))
    st.set("qa", "done" if not bad else "flagged", str(bad))
    print(f"[qa] accuracy per scene: {done}")
    if bad:
        for i, _ in bad:
            (wd / "clips" / f"seg-{i}.mp4").rename(wd / "clips" / f"seg-{i}-rejected.mp4")
        raise RuntimeError(f"QA rejected scenes {bad} — re-run to regenerate them")


# ----------------------------------------------------------------------------- stage: assemble
def stage_assemble(job, wd, st, chunks):
    """Trim each clip's VIDEO to its chunk's exact length, concat video-only, then lay the
    original one-take VO over the whole assembly. This is the One-Take law in code."""
    final = wd / "final.mp4"
    if final.exists():
        return
    n = len(chunks)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for c in chunks:
        cmd += ["-i", str(wd / "clips" / f"seg-{c['index']}.mp4")]
    cmd += ["-i", str(wd / "vo_full.wav")]
    fc = "".join(f"[{i}:v]trim=0:{c['duration']},setpts=PTS-STARTPTS,"
                 f"scale=720:1280,fps=24[v{i}];" for i, c in enumerate(chunks))
    fc += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(final)]
    sh(cmd)
    st.set("assemble", "done", f"{media_duration(final):.1f}s")
    print(f"[assemble] final.mp4 {media_duration(final):.1f}s — one-take audio over {n} scenes")


# ----------------------------------------------------------------------------- stage: captions
def stage_captions(job, wd, st):
    """Burned captions from the SAME alignment the VO produced — in sync by construction.
    This ffmpeg has no drawtext, so cards are Pillow PNGs composited with overlay
    (reference_burned_caption_overlays), batched to keep filtergraphs sane."""
    if not job.get("captions", True):
        return
    out = wd / "final-captioned.mp4"
    if out.exists():
        return
    from PIL import Image, ImageDraw, ImageFont
    words = [w for w in json.loads((wd / "alignment.json").read_text())["words"]
             if w.get("type") == "word"]
    cards, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["text"].rstrip().endswith((".", "!", "?", ",")):
            cards.append({"text": " ".join(x["text"] for x in cur).strip(),
                          "start": cur[0]["start"], "end": cur[-1]["end"] + 0.12})
            cur = []
    if cur:
        cards.append({"text": " ".join(x["text"] for x in cur).strip(),
                      "start": cur[0]["start"], "end": cur[-1]["end"] + 0.12})

    cdir = wd / "caption_cards"
    cdir.mkdir(exist_ok=True)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 58)
    for i, c in enumerate(cards):
        img = Image.new("RGBA", (720, 130), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        t = c["text"].upper()
        wpx = d.textlength(t, font=font)
        x = (720 - wpx) / 2
        for dx in (-3, 3):
            for dy in (-3, 3):
                d.text((x + dx, 30 + dy), t, font=font, fill="black")
        d.text((x, 30), t, font=font, fill="white")
        img.save(cdir / f"c{i:04d}.png")

    src = wd / "final.mp4"
    BATCH = 40
    for b in range(0, len(cards), BATCH):
        batch = cards[b:b + BATCH]
        nxt = wd / f"_cap_{b}.mp4"
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src)]
        for i in range(len(batch)):
            cmd += ["-i", str(cdir / f"c{b + i:04d}.png")]
        fc, prev = "", "0:v"
        for i, c in enumerate(batch):
            lab = f"o{i}"
            fc += (f"[{prev}][{i + 1}:v]overlay=0:1010:"
                   f"enable='between(t,{c['start']:.2f},{c['end']:.2f})'[{lab}];")
            prev = lab
        cmd += ["-filter_complex", fc.rstrip(";"), "-map", f"[{prev}]", "-map", "0:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "copy", str(nxt)]
        sh(cmd)
        if src != wd / "final.mp4":
            src.unlink()
        src = nxt
    src.rename(out)
    for f in wd.glob("_cap_*.mp4"):
        f.unlink()
    st.set("captions", "done", f"{len(cards)} cards")
    print(f"[captions] {len(cards)} cards burned -> final-captioned.mp4")


# ----------------------------------------------------------------------------- alt engines
def omni_render(keyframe, prompt, out_mp4):
    """B-roll scenes ≤10s on Omni (no dialogue; VO carries over them). Interactions API
    via curl per reference_omni_interactions_api. Not exercised by dialogue-only jobs."""
    import base64
    key = env_key("GEMINI_API_KEY")
    payload = {"model": "models/gemini-omni-flash-preview", "background": True,
               "generation_config": {"video_config": {}},
               "input": [{"type": "image",
                          "data": base64.b64encode(pathlib.Path(keyframe).read_bytes()).decode(),
                          "mime_type": "image/png"},
                         {"type": "text", "text": prompt}]}
    pf = pathlib.Path(out_mp4).with_suffix(".payload.json")
    pf.write_text(json.dumps(payload))
    r = json.loads(sh(["curl", "-sS", "-X", "POST",
                       f"https://generativelanguage.googleapis.com/v1beta/interactions?key={key}",
                       "-H", "Content-Type: application/json", "--data-binary", f"@{pf}"]))
    iid = r["id"]
    while True:
        time.sleep(10)
        d = json.loads(sh(["curl", "-sS",
                           f"https://generativelanguage.googleapis.com/v1beta/interactions/{iid}?key={key}"]))
        if d.get("status") == "completed":
            for step in d.get("steps", []):
                for part in step.get("content", []):
                    if part.get("type") == "video":
                        pathlib.Path(out_mp4).write_bytes(base64.b64decode(part["data"]))
                        return out_mp4
            raise RuntimeError("omni completed without video part")
        if d.get("status") in ("failed", "cancelled"):
            raise RuntimeError(f"omni failed: {d}")


def fal_lipsync(video_url, audio_url, out_mp4):
    """Tier-2 lip-sync: re-render the mouth of an existing clip against a VO chunk.
    What makes Omni usable for talking shots. Not exercised by Seedance-dialogue jobs."""
    key = env_key("FAL_API_KEY")
    r = http_json("POST", "https://fal.run/fal-ai/sync-lipsync",
                  {"Authorization": f"Key {key}"},
                  {"video_url": video_url, "audio_url": audio_url}, timeout=1200)
    url = (r.get("video") or {}).get("url") or r.get("video_url")
    if not url:
        raise RuntimeError(f"fal lipsync returned no url: {r}")
    sh(["curl", "-sS", "-L", "-o", str(out_mp4), url])
    return out_mp4


# ----------------------------------------------------------------------------- driver
STAGES = ["vo", "align", "chunks", "render", "qa", "assemble", "captions"]


def run(job_path, until=None):
    job = json.loads(pathlib.Path(job_path).read_text())
    if "script_file" in job and "script" not in job:
        job["script"] = pathlib.Path(job["script_file"]).read_text().strip()
    wd = pathlib.Path(job["workdir"])
    wd.mkdir(parents=True, exist_ok=True)
    st = State(wd)
    stop = STAGES.index(until) if until else len(STAGES) - 1

    stage_vo(job, wd, st)
    if stop >= 1:
        stage_align(job, wd, st)
    chunks = stage_chunks(job, wd, st) if stop >= 2 else None
    if chunks is None and (wd / "chunks" / "manifest.json").exists():
        chunks = json.loads((wd / "chunks" / "manifest.json").read_text())
    if stop >= 3:
        stage_render(job, wd, st, chunks)
    if stop >= 4:
        stage_qa(job, wd, st, chunks)
    if stop >= 5:
        stage_assemble(job, wd, st, chunks)
    if stop >= 6:
        stage_captions(job, wd, st)
    print(f"[factory] complete through '{until or 'captions'}' -> {wd}")


def status(job_path):
    job = json.loads(pathlib.Path(job_path).read_text())
    for row in State(pathlib.Path(job["workdir"])).rows():
        print("  ".join(str(x) for x in row))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "status"])
    ap.add_argument("job")
    ap.add_argument("--until", choices=STAGES)
    a = ap.parse_args()
    (run(a.job, a.until) if a.cmd == "run" else status(a.job))
