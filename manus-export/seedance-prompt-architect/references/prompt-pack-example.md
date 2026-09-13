# Example prompt-pack shape

The finished document should look roughly like this (abbreviated example):

```
# PROMPT PACK — <Brand> / <Product> · ref: <reference name>

Reference: <filename> · 41.8s · 6 cuts → 6 segments
Product tag used throughout: [product reference]. Aspect: 9:16.

Segment table:
| Seg | Time | Dur | Cut in | Beat (one line) |
|----|------|-----|--------|-----------------|
| 1 | 00:00–00:07 | 7.0s | open | Creator holds product to camera, hook line |
| 2 | 00:07–00:12 | 5.0s | hard | Reaction close-up |
| 3 | 00:12–00:21 | 9.0s | hard | Story beat, product on shoulder |
| 4 | 00:21–00:29 | 8.0s | hard | Hands open the product, show capacity |
| 5 | 00:29–00:36 | 7.0s | hard | Walking, product on shoulder |
| 6 | 00:36–00:41 | 5.0s | hard | Close, call to action |

## ASSET PROMPTS (generate first, reuse)
[avatar prompt] ... [product keyframe A prompt] ... [product keyframe B prompt] ...

## SEGMENTS
### SEG 1 · 00:00–00:07 (7.0s) · cut in: open
Reference beat: [description]
Start frame: Product keyframe A
Video prompt: [full prompt]
Continuity: Start of chain. Export Seg 1's last frame for Seg 2.

### SEG 2 · ...
[continues for every segment]

## OPERATOR NOTES
- Generate avatar + product keyframes first, then segments in order (some chain off
  the prior clip's last frame — those are marked).
- Iterate on draft quality; regenerate keepers on the best quality setting for clean
  label + hands.
- Watch any 8+ second creator shot for face drift; split or tighten the camera if it wobbles.
- Keep the product reference/tag consistent on every product shot.
```
