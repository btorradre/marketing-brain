# Asset resolution, reuse & memory

The general discipline of *not regenerating the same asset twice*, and of remembering confirmed preferences across projects — regardless of what specific tooling you have for it.

## The core principle

Check for a reusable asset before generating or fetching anything fresh — for background music, sound effects, images, icons, brand logos, voice, color grades, and LUTs alike.

Judging *semantic* fit ("this existing 'upbeat tech launch' track is close enough to my new 'energetic tech intro' request") is a judgment call you make yourself by reading descriptions. An automated system will only auto-reuse an *exact*, normalized match (same text, case/whitespace-insensitive); anything looser requires your explicit read-and-decide.

## A practical reuse workflow

1. Check your current project's own asset log/manifest for an exact or near-exact match on the same request — reuse automatically if found.
2. Scan for any already-downloaded/generated files that were never logged, in case something usable already exists unregistered.
3. Check any broader/cross-project asset cache you maintain for a semantically similar item — list candidates, read their descriptions, and decide yourself whether one fits.
4. Only if nothing fits: fetch fresh from a provider/catalog, or generate.
5. Whatever you end up using — reused or freshly produced — log it: an id, a short description, its file path, duration/dimensions if relevant, and where it came from. Also promote it into whatever broader reuse cache you maintain, so future projects benefit.

This is the same shape whether you're implementing it as an ad hoc manifest file, a small local database, or a one-off checklist you run by hand — the point is the order of operations (check → scan → check broader cache → fetch/generate → log), not the storage mechanism.

## Trust guardrail

A redundant fresh download/generation is cheap; shipping the *wrong* reused asset is not. When in doubt, resolve fresh rather than reuse on a loose match.

This is especially important for **brand- or entity-specific assets** (like a company logo): only reuse a cross-project brand asset when the entity matches *exactly*. A broad cross-project cache can easily surface a different client's or brand's asset on a loose semantic match, and using it by mistake is a real risk, not just an inefficiency.

## Adopting an existing project's assets

If a project already has a folder of loose media files that were never logged, walk that folder, probe each file for real duration/dimensions (a tool like `ffprobe` gives you this without opening the file in an editor), and register them into your asset log with best-guess descriptions — rather than leaving them invisible to future reuse checks.

## Remembered preferences (lightweight tier)

Confirmed brief answers a person actually gave you — a target aspect ratio, a language, a preferred voice, a style preset, etc. — are worth persisting so you don't re-ask on the next project.

Keep two tiers:
- **Project-level** — specific to the current project, inherited by anyone else working on it.
- **Personal/global** — applies across all future projects for that person.

A preference should only be promoted to the personal/global tier once it's been **independently confirmed in at least two different projects** — this stops a one-off choice on a single project from silently becoming everyone's global default.

Critically: only record what a person **actually confirmed** — never an inferred, guessed, or merely-defaulted value. When you do have a remembered preference available, surface it as a *recommended default with a visible reason* ("last time you picked X, want that again?") rather than silently applying it and skipping the question altogether.

## Frozen "recipes" (heavyweight tier)

For a fully-approved production run you expect to repeat (e.g. a recurring weekly promo format), it's worth freezing the whole approved structure as a reusable, named, versioned bundle:
- the storyboard/structure skeleton, with the specific content blanked out to per-run fill-ins
- any brief/spec skeleton
- the specific confirmed preference values that made that particular run work

Same two-tier split as preferences (project-level committed bundle vs. personal/global), except a frozen recipe promotes to the personal/global tier **immediately** on freezing — no two-project rule — because a deliberate freeze-and-approve action is already a much stronger confirmation signal than an ordinary preference answer.

Re-freezing an existing recipe name should bump its version number and archive the previous version rather than silently overwriting it.

Offer to freeze a recipe **once**, right after a final approval — not repeatedly, not unprompted mid-project. When a person picks an existing recipe to reuse, it's fine to skip re-asking the questions that recipe already answers — choosing to reuse the recipe **is** the confirmation for all of those.

## What to keep in an asset log, generally

- A machine-readable manifest: one record per asset, with id, type, path, description, and provenance (where it came from).
- A human/agent-readable index table summarizing the same (id, type, duration, dimensions, path, description) for quick scanning.
- Committed project-level preferences and any project-level frozen recipes (so a team inherits them).
- A separate, non-committed personal/global cache and personal/global preferences and recipes — ideally content-addressed by a hash of the file, so identical content is recognized even under a different filename.
- A local log of "misses" — resolve attempts that found nothing — useful for spotting gaps in your asset library over time.

### Illustrative shapes

Asset inventory table:

```
id         type   dur    dims        path                             description
bgm_001    bgm    25s    -           assets/audio/bgm/bgm_001.mp3     upbeat tech launch
sfx_001    sfx    0.6s   -           assets/audio/sfx/sfx_001.mp3     whoosh
image_001  image  -      1920x1080   assets/images/image_001.jpg      gradient tech background
icon_001   icon   -      200x200     assets/images/icon_001.png       rocket
```

Manifest record (one per line, machine-readable):

```json
{"id":"bgm_001","type":"bgm","path":"assets/audio/bgm/bgm_001.mp3","description":"upbeat tech launch","duration_s":25,"source":"catalog-retrieve","provider":"example-music-catalog"}
```
