# Higgsfield Soul Character (Identity Training)

Trains a "Soul Character" — a personalized model of a specific person's face — that Higgsfield then uses for identity-faithful image and video generation of that person. Use this when the request is to create a Soul, train a face, make a digital twin, build an avatar, learn someone's appearance, create a character of a specific real person, set up identity for video, or put a real person's face into generated images/video going forward. This is a one-time training step: train once, get back a reference ID, then reuse that ID across many later generations.

This is NOT the right tool for a one-shot face swap on a single image (a direct image-reference edit is faster for that), or for a named/fictional character that isn't based on real photos of a real person (a plain text/image prompt covers that).

This skill wraps the Higgsfield CLI (`higgsfield soul-id create` / `wait` / `list` / `get`). On Manus, treat this as: call the Higgsfield API/CLI with these commands and parameters.

## How to use this

1. **Set up access.** If the `higgsfield` CLI isn't installed, install it (`curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh`). If account status shows a session/auth error, the user needs to log in (`higgsfield auth login`). Soul training additionally requires a paid plan (Basic tier or above) — check account status and tell the user up front if they're on a free plan, since training will fail.
2. **Get a name.** One word, used to reference this Soul later. Ask if not given.
3. **Get photos.** 5–20 face photos of the person, varied in angle and lighting (see photo guidance below). Local file paths or already-uploaded IDs both work.
4. **Pick a training variant:**
   - `--soul-2` — for image generation (default, use unless told otherwise)
   - `--soul-cinematic` — for cinematic/video work
   Choose based on the user's stated downstream use; default to `--soul-2` if unclear.
5. **Submit training:**
   ```
   higgsfield soul-id create --name "<name>" --soul-2 --image ./photo1.png --image ./photo2.png ...
   ```
   (paths auto-upload; the command returns a reference ID once accepted)
6. **Wait for training to finish.** `higgsfield soul-id wait <id>` — this can take several minutes; don't spam status updates while waiting, default timeout is 30 minutes.
7. **Deliver the result** simply: "Soul `<name>` ready." Don't expose the raw reference ID in casual conversation — just note that it's ready for use.
8. **Use the trained Soul in later generations** by passing its reference ID as the identity/soul parameter, e.g.:
   ```
   higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <ref_id> --quality 2k --wait
   higgsfield generate create soul_cinematic --prompt "..." --soul-id <ref_id> --quality 2k --wait
   ```
9. **List or look up existing Souls** if needed:
   ```
   higgsfield soul-id list                   # all references
   higgsfield soul-id get <id>               # one by id
   ```

## Rules & standards

1. Be concise — no raw IDs in casual chat; just confirm "Soul ready" with the name.
2. Detect the user's language and respond in it; CLI flags/commands stay in English.
3. Ask for only the minimum needed: name + photos. Pick a sensible training variant automatically rather than asking.
4. Training takes minutes — poll/wait silently rather than repeating status updates.
5. Training requires a paid plan (Basic tier or higher) — verify this before submitting and tell the user if they need to upgrade.

### Photo requirements for good training

- **Quantity:** minimum 5, maximum 20 photos — 8 to 12 is the sweet spot.
- **Content:** clear face with eyes visible; single person per photo; no heavy filters, no sunglasses.
- **Variety** (higher variety = better identity capture):
  - Multiple angles: front, 3/4 left, 3/4 right, slight up/down.
  - Different lighting: indoor, outdoor, soft, harsh.
  - Different expressions: neutral, smiling, talking.
  - Different distances: head shot, head-and-shoulders, full body.
- **Quality:** sharp and in focus; resolution ideally 1024×1024 or higher; JPEG or PNG.
- **Avoid:** group photos, heavy makeup the person doesn't normally wear, costumes/cosplay, hats covering the face, or the same pose repeated across every photo.

### Troubleshooting

- **"Minimum Basic plan required"** — Soul training needs a paid plan. Tell the user to upgrade.
- **"Training failed"** — common causes: too few photos (fewer than 5) or too uniform a set; heavy occlusion (sunglasses, hats); group photos confusing the identity; wrong upload type (must be image uploads, not video). Action: ask the user for better/more varied photos and retrain.
- **"Session expired"** — the user needs to log in again.
- **Slow training** — default timeout is 30 minutes; if still in progress, wait longer (e.g. up to 60 minutes) before treating it as failed.
