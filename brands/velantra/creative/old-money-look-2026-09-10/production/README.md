# Eleanor Weekender — nine completed ads

All nine 1080×1920, 30fps H.264 MP4s are rendered from DaVinci Resolve in `exports/`, together with the editable `Eleanor-OldMoney-9Ads.drp` project. Voice: Woman Over 40, Eleven V3 Creative. All approved spoken words and normal speech speed preserved. No authored on-screen text.

H1: 51.3 seconds, H2: 54.8 seconds, H3: 51.7 seconds. Each hook is crossed with A1 Anna, A2 eurofall-weekender-C3 and A3 mer-oldmoney-C1. Nine/ eight/ thirteen deep-silence intervals were removed per hook respectively, synchronized with avatar footage and all visual cues. Natural louder breaths remain; long post-speech dead space was removed. Source audio was decoded to lossless WAV to eliminate Resolve's MP3 decoding offset.

Native Resolve Lua scripting was used because external Python is unavailable on this installed edition. The isolated project is `VEL_Eleanor_OldMoney_9Ads_2026-09-11`; the previous project was saved and preserved. A2/A3 use native Fusion keying; A1 uses a source-preserving person matte. Final compositing, edits and exports are Resolve operations. The DRP references existing source files in this workspace.

QA: all 14,202 video frames decoded and scanned at reduced resolution with no black-frame or green-screen flags. All 54 final audio comparison windows have zero measured source offset and correlation above 0.99999. Presenter source-frame correspondence was checked across five holds per ad. Full audio/video machine reviews and direct inspection of representative/flagged frames are documented in `qa/final/`; several inconsistent model flags were adjudicated against actual pixels and byte-identical audio. This is machine-assisted QA, not human listening approval or exhaustive full-resolution frame review.

Cut Room contains verified actual final-render previews: https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard

Native provider outputs, pre-trim assemblies, first renders and QA history are retained. Do not regenerate paid assets.
