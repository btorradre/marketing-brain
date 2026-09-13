# Animation (Priority 7 — MEDIUM)

## Core rules

- Micro-interactions: 150-300ms. Complex transitions: up to ~400ms. Avoid anything over 500ms.
- Animate only `transform`/`opacity`; never animate `width`/`height`/`top`/`left` (causes layout thrashing).
- Show a skeleton or progress indicator once loading exceeds ~300ms.
- Animate at most 1-2 key elements per view — restraint reads as more polished, not less.
- Ease-out for elements entering, ease-in for elements exiting; avoid linear easing for UI transitions.
- Every animation should express a cause-effect relationship, not be purely decorative.
- State changes (hover/active/expanded/collapsed/modal) should animate smoothly, never snap instantly.
- Page/screen transitions should maintain spatial continuity (a shared element, a directional slide) rather than a jarring cut.
- Use parallax sparingly, and always respect reduced-motion settings — it must never cause disorientation.
- Prefer spring/physics-based motion curves over linear or generic cubic-bezier curves for a natural feel.
- Exit animations should be shorter than enter animations (roughly 60-70% of the enter duration) to feel responsive.
- Stagger list/grid item entrances by 30-50ms per item — avoid both an all-at-once reveal and a too-slow cascade.
- Use shared-element/hero transitions for visual continuity between screens where relevant.
- Animations must be interruptible — a user's tap or gesture should cancel an in-progress animation immediately.
- Never block user input during an animation; the UI must stay interactive throughout.
- Use crossfade for content replacement within the same container.
- Subtle scale (0.95-1.05) on press for tappable cards/buttons, restoring on release.
- Drag, swipe, and pinch gestures must give real-time visual response that tracks the finger, not a delayed jump.
- Use translate/scale direction to express hierarchy: entering from below reads as "deeper," exiting upward reads as "back."
- Unify duration/easing tokens globally so all animations share the same rhythm.
- Don't let a fading element linger below ~0.2 opacity — either fade it fully out or keep it visible.
- Modals/sheets should animate from their trigger source (scale+fade or slide-in) to preserve spatial context.
- Forward navigation animates left/up; backward navigates right/down — keep the direction logically consistent throughout the product.
- Animations must never cause layout reflow or shift — use `transform` for any position change, never layout properties.

## Full rule database (verbatim from source)

Source: `ux-guidelines.csv` Animation category (8 rows) and `app-interface.csv` Animation category (3 rows).

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 7 | Animation | Excessive Motion | All | Too many animations cause distraction and motion sickness | `Animate 1-2 key elements per view maximum` | `Animate everything that moves` | `Single hero animation` | `animate-bounce on 5+ elements` | High |
| 8 | Animation | Duration Timing | All | Animations should feel responsive not sluggish | `Use 150-300ms for micro-interactions` | `Use animations longer than 500ms for UI` | `transition-all duration-200` | `duration-1000` | Medium |
| 9 | Animation | Reduced Motion | All | Respect user's motion preferences | `Check prefers-reduced-motion media query` | `Ignore accessibility motion settings` | `@media (prefers-reduced-motion: reduce)` | `No motion query check` | High |
| 10 | Animation | Loading States | All | Show feedback during async operations | `Use skeleton screens or spinners` | `Leave UI frozen with no feedback` | `animate-pulse skeleton` | `Blank screen while loading` | High |
| 11 | Animation | Hover vs Tap | All | Hover effects don't work on touch devices | `Use click/tap for primary interactions` | `Rely only on hover for important actions` | `onClick handler` | `onMouseEnter only` | High |
| 12 | Animation | Continuous Animation | All | Infinite animations are distracting | `Use for loading indicators only` | `Use for decorative elements` | `animate-spin on loader` | `animate-bounce on icons` | Medium |
| 13 | Animation | Transform Performance | Web | Some CSS properties trigger expensive repaints | `Use transform and opacity for animations` | `Animate width/height/top/left properties` | `transform: translateY()` | `top: 10px animation` | Medium |
| 14 | Animation | Easing Functions | All | Linear motion feels robotic | `Use ease-out for entering ease-in for exiting` | `Use linear for UI transitions` | `ease-out` | `linear` | Low |

### App-interface rows (iOS/Android/React Native specific)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 23 | Animation | Duration & Easing | animation duration easing | iOS/Android/React Native | Micro-interactions should be 150–300ms with native-like easing | `Use ease-out for enter/ease-in for exit` | `Use long or linear animations for core UI` | `Animated.timing(..., { duration: 200, easing: Easing.out(Easing.quad) })` | `Animated.timing(..., { duration: 800, easing: Easing.linear })` | Medium |
| 24 | Animation | Respect Reduced Motion | reduced motion accessibility | iOS/Android/React Native | Respect OS reduced-motion accessibility setting | `Check reduceMotionEnabled and simplify animations` | `Ignore user motion preferences` | `if (reduceMotionEnabled) skipAnimation()` | `Always run complex parallax animations` | Critical |
| 25 | Animation | Limited Continuous Motion | loop animation loader | iOS/Android/React Native | Reserve infinite animations for loaders and live data | `Use looping only where necessary` | `Keep decorative elements looping forever` | `Animated.loop(loaderAnim) for ActivityIndicator` | `Animated.loop(bounceAnim) on background icons` | Medium |
