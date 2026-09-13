# VEL-COLETTE-LOOKRICH-01 · build status

## DONE

**VO recorded and locked.** `vo/VO-lookrich-FINAL.mp3`

| | |
|---|---|
| Voice | **Woman Aged 40-65** `SkQqPDmEiASWjGhFSNZ3`, eleven_v3 Creative |
| Runtime | 43.04s, 136 words, 191 wpm |
| Dead air | **zero.** No lead-in, no tail, not one inter-word gap over 0.12s, so nothing to tighten |
| Loudness | -14.08 LUFS, TP -1.08 dBTP |
| STT gate | **PASS.** "Colette" correct, clean `Vel` onset, and "thirty dollars off" reads back as "$30 off" with no "percent" anywhere |

Take 1 on **Woman Over 40** (the 8/22 voice) came back at 38.3s / 215 wpm, too fast against the 189 wpm exemplar. Woman Aged 40-65 landed at 191 and also sits better against a creator who reads around 50. Kept at `vo/VO-lookrich-w4065-take2.mp3` pre-normalize.

**No atempo.** The read ships at its natural pace and the picture gets cut to it, per the men's-greenscreen law that atempo is what "robotic" sounds like.

**Shot map retimed to the recorded track.** Every beat in `../2026-08-29-VEL-COLETTE-LOOKRICH-01.md` §5 is now a measured timing off `vo/VO-lookrich-w4065-take2-words.json`, not an estimate. "Velantra" lands inside 3.81 to 6.61s, so the brand clears the 0:06 law.

The one-second silent breath beat is gone. The recorded read runs straight from the no-logo payoff into the proof, so there was no room for it.

## BLOCKED, needs one file

Brooks's creator photo is in the chat, not on disk, and chat attachments do not exist on this machine. **Save it to `creator/creator-anchor-brooks-pick.jpg` in this folder** and the HeyGen build runs start to finish.

## THEN, in order

1. Upload the photo to HeyGen, create the photo avatar, confirm the look reports `avatar_v` in `supported_api_engines`.
2. Upload `vo/VO-lookrich-FINAL.mp3` to `/v1/asset`, take the `id` as `audio_asset_id`.
3. `POST /v3/videos` with `engine.type = avatar_v`, 9:16, 1080p. HeyGen lip-syncs to that exact mp3, so no HeyGen voice and no re-read.
4. Key, comp against the shot map, burn captions, cut the PDP recording onto the tail.

## Gotchas already checked

- **HeyGen billing is a wallet, not a quota.** The legacy `api: 316` number lies. `GET /v3/users/me` reports **$5.27 remaining** with auto-reload on at $15 / $5 threshold, so we are sitting right on the trigger. The next render will probably fire the reload. If a job hard-fails `MOVIO_PAYMENT_INSUFFICIENT_CREDIT`, refire once before calling it blocked.
- **Chromakey similarity 0.08 to 0.10, blend 0.03.** At 0.15 the key bled alpha into a creator's torso and it only showed at full res. Test the key over a flat red card first.
- **Clamp caption cards** to `end = min(end + 0.12, next_start - 0.02)` or overlapping ranges stack two cards into garble.
- The capacity run is fast by design: 0.79s, 0.88s, 0.64s, one cut per noun.
- HeyGen photo avatars of a real person need the consent record on file. Worth having that sorted before this ships.
