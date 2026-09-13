# UI/UX Design Intelligence

This document is a comprehensive design guide for web and mobile applications — a prioritized rulebook covering accessibility, touch/interaction, performance, style selection, layout, typography, color, animation, forms, navigation, and charts/data visualization, applicable across common frontend stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, plain HTML/CSS). Use it whenever a task involves UI structure, visual design decisions, interaction patterns, or user-experience quality control.

## When to apply this

Use this guidance when:
- Designing new pages (landing page, dashboard, admin panel, SaaS product, mobile app).
- Creating or refactoring UI components (buttons, modals, forms, tables, charts, etc.).
- Choosing color schemes, typography systems, spacing standards, or layout systems.
- Reviewing UI code for user experience, accessibility, or visual consistency.
- Implementing navigation structures, animations, or responsive behavior.
- Making product-level design decisions (style, information hierarchy, brand expression).
- Improving the perceived quality, clarity, or usability of an interface.

Also consider it when the UI "looks unprofessional" but the reason is unclear, when there's feedback on usability, before a launch as a quality pass, when aligning design across web/iOS/Android, or when building a design system or reusable component library.

Skip it for pure backend logic, API/database design, non-visual performance work, infrastructure/DevOps, or non-visual scripts. Decision rule: if the task changes how a feature **looks, feels, moves, or is interacted with**, apply this guidance.

## How to use this

### 1. Analyze the requirements

Extract from the request: the product type (entertainment — social/video/music/gaming; tool — scanner/editor/converter; productivity — task manager/notes/calendar; or a hybrid), the target audience (age group, usage context — commute, leisure, work), style keywords (playful, vibrant, minimal, dark mode, content-first, immersive, etc.), and the target technology stack.

### 2. Establish a design system before writing any component

Before building individual components, decide and write down (even briefly) a coherent design system for the whole project: an overall visual pattern/style, a color palette, a typography pairing, and a set of visual effects (shadows, blur, radius) — all chosen to match the product type and audience, with explicit anti-patterns to avoid for that style. Don't let color, font, and component style get decided ad hoc, component by component — that's what produces an inconsistent, "not quite professional" result.

A good practice for larger projects: maintain one master design-system document (colors, type scale, spacing scale, component conventions, anti-patterns) as the single source of truth, and only create a page-specific override document when a particular page deliberately deviates from the master (e.g. a checkout page with a stripped-down nav). When building any specific page, check for a page-level override first; fall back to the master rules if none exists. This keeps a large multi-page build visually consistent without forcing every page to be identical.

### 3. Apply the detailed rule checklists

Work through the ten rule categories below, prioritized 1 (most critical) to 10 (least critical) — treat 1-3 as non-negotiable baseline quality, 4-6 as strongly expected, 7-10 as refinement:

| Priority | Category | Impact |
|---|---|---|
| 1 | Accessibility | CRITICAL |
| 2 | Touch & Interaction | CRITICAL |
| 3 | Performance | HIGH |
| 4 | Style Selection | HIGH |
| 5 | Layout & Responsive | HIGH |
| 6 | Typography & Color | MEDIUM |
| 7 | Animation | MEDIUM |
| 8 | Forms & Feedback | MEDIUM |
| 9 | Navigation Patterns | HIGH |
| 10 | Charts & Data | LOW |

### 4. Run a pre-delivery check before calling any UI work finished

- Run through the CRITICAL and HIGH categories (1-3, plus 5 and 9) as a final review before delivery.
- Test at a small-phone width (375px) and in landscape orientation.
- Verify behavior with reduced-motion enabled and with text scaled to its largest supported size.
- Check dark-mode contrast independently — never assume light-mode color values will also pass in dark mode.
- Confirm all touch targets are at least 44×44pt and nothing is hidden behind device safe areas (notch, home indicator, status/nav bars).

## Rules & standards

### 1. Accessibility (CRITICAL)

- Minimum 4.5:1 contrast ratio for normal text (3:1 for large text).
- Visible focus rings (2-4px) on every interactive element — never remove them.
- Descriptive alt text for meaningful images.
- `aria-label` (or platform-native accessibility label) for icon-only buttons.
- Tab order matches visual order; full keyboard support.
- Use a real `<label>` associated with its input via a `for`/`htmlFor` attribute.
- Provide a "skip to main content" link for keyboard users.
- Sequential heading hierarchy (h1→h6), never skip a level.
- Never convey information by color alone — pair it with an icon or text.
- Support system text-size scaling; avoid truncating text as it grows.
- Respect "reduced motion" settings — reduce or disable animations when the user has requested it.
- Provide meaningful accessibility labels/hints and a logical reading order for screen readers.
- Provide a cancel/back path in every modal and multi-step flow.
- Preserve system and accessibility keyboard shortcuts; offer a keyboard alternative to any drag-and-drop interaction.

### 2. Touch & Interaction (CRITICAL)

- Minimum touch target: 44×44pt (Apple) / 48×48dp (Material) — extend the hit area beyond the visual bounds if the icon itself is smaller.
- Minimum 8px/8dp gap between adjacent touch targets.
- Use click/tap for primary interactions; never rely on hover alone (hover doesn't exist on touch devices).
- Disable a button during an async operation and show a spinner or progress indicator.
- Clear error messages placed near the problem, not just at the top of the page.
- Add a pointer cursor to clickable elements on web.
- Avoid horizontal swipe gestures on main content; prefer vertical scroll.
- Use `touch-action: manipulation` on web to reduce the ~300ms tap delay.
- Use platform-standard gestures consistently; don't redefine swipe-back, pinch-zoom, etc.
- Don't block OS-level system gestures (Control Center, edge-swipe-back, etc.).
- Provide visual feedback on press (ripple or highlight).
- Use haptic feedback for confirmations and important actions — but don't overuse it.
- Never rely on gesture-only interactions for critical actions; always provide a visible control as well.
- Keep primary touch targets away from the notch, dynamic island, gesture bar, and screen edges.
- Avoid requiring pixel-perfect taps on small icons or thin edges.
- Swipe actions must show a clear affordance or hint (a chevron, a label, a one-time tutorial).
- Use a movement threshold before starting a drag, to avoid accidental drags from an imprecise tap.

### 3. Performance (HIGH)

- Use modern image formats (WebP/AVIF), responsive images, and lazy-load non-critical assets.
- Declare image width/height (or use `aspect-ratio`) to prevent layout shift.
- Use `font-display: swap` or `optional` to avoid invisible text while a webfont loads; reserve space to reduce shift.
- Preload only genuinely critical fonts — don't preload every variant.
- Prioritize above-the-fold CSS.
- Lazy-load non-hero components via dynamic import or route-level code splitting.
- Split code by route/feature to reduce initial load size and time-to-interactive.
- Load third-party scripts async/deferred; regularly audit and remove unnecessary ones.
- Avoid frequent layout reads/writes in a row; batch DOM reads, then batch writes.
- Reserve space for async content so it doesn't cause a layout jump when it arrives.
- Use native lazy-loading for below-the-fold images and heavy media.
- Virtualize lists with 50+ items for memory efficiency and scroll performance.
- Keep per-frame work under ~16ms to sustain 60fps; move heavy work off the main thread.
- Use skeleton screens/shimmer instead of a long blocking spinner for operations over ~1 second.
- Keep input latency under ~100ms for taps/scrolls; give visual feedback within 100ms of a tap.
- Debounce/throttle high-frequency events (scroll, resize, input).
- Provide offline-state messaging and a basic fallback where relevant.
- Offer a degraded mode for slow networks (lower-res images, fewer animations).

### 4. Style Selection (HIGH)

- Match the visual style to the product type, and use one style consistently across every page.
- Use real vector icons (e.g. Phosphor, Heroicons, Lucide, or a platform-native icon set), never emoji, for structural/navigational icons — emoji are font-dependent, render inconsistently across platforms, and can't be controlled by design tokens. If a suitable icon isn't in whatever curated set is being used, pull a more semantically accurate one from the full icon library rather than forcing a near-miss; only fall back to a different icon family if truly necessary, and keep stroke width/fill style consistent with the rest of the interface if so.
- Choose the color palette deliberately from the product's category/industry.
- Keep shadows, blur, and corner radius aligned with the chosen style (glass, flat, clay, etc.) — don't mix effect languages randomly.
- Respect platform idioms (iOS Human Interface Guidelines vs. Material Design) for navigation, controls, typography, and motion when building for a specific platform.
- Make hover/pressed/disabled states visually distinct while staying on-style.
- Use one consistent elevation/shadow scale for cards, sheets, and modals — avoid arbitrary one-off shadow values.
- Design light and dark variants together so brand, contrast, and style stay consistent across both.
- Use one icon set/visual language (stroke width, corner radius) across the entire product.
- Prefer native/system controls over fully custom ones; only build a custom control when branding genuinely requires it.
- Use blur to indicate that something (a modal, a sheet) sits above and dismisses the background — not as pure decoration.
- Give each screen exactly one primary call-to-action; make secondary actions visually subordinate.

### 5. Layout & Responsive (HIGH)

- `width=device-width, initial-scale=1` in the viewport meta tag — never disable zoom.
- Design mobile-first, then scale up to tablet and desktop.
- Use a systematic, consistent set of breakpoints (e.g. 375 / 768 / 1024 / 1440).
- Minimum 16px body text on mobile (smaller triggers unwanted auto-zoom on iOS Safari).
- Line length: roughly 35-60 characters on mobile, 60-75 on desktop.
- No horizontal scroll on mobile — content must fit the viewport width.
- Use an incremental spacing system (4pt/8dp) rather than arbitrary spacing values.
- Keep component spacing comfortable for touch — not so cramped it causes mis-taps.
- Use a consistent max-width container on desktop.
- Define an explicit, layered z-index scale (e.g. 0/10/20/40/100/1000) rather than ad hoc values.
- A fixed navbar or bottom bar must reserve safe padding so it never covers underlying content.
- Avoid nested scroll regions that fight with the main page scroll.
- Prefer a dynamic viewport height unit over a flat 100vh on mobile (address-bar resize issues).
- Keep the layout readable and operable in landscape orientation, not just portrait.
- Show core content first on mobile; fold or hide secondary content behind disclosure.
- Establish visual hierarchy through size, spacing, and contrast — never color alone.

### 6. Typography & Color (MEDIUM)

- Line-height 1.5-1.75 for body text.
- Line length 65-75 characters.
- Pair heading and body fonts whose personalities match (not fighting each other).
- Use a consistent type scale (e.g. 12/14/16/18/24/32).
- Use noticeably darker text on light backgrounds (e.g. a near-black on white, not mid-gray).
- Use a platform type-role system (iOS Dynamic Type styles / Material type roles — display, headline, title, body, label) rather than ad hoc sizes.
- Use font-weight to reinforce hierarchy: bold headings (600-700), regular body (400), medium labels (500).
- Define semantic color tokens (primary, secondary, error, surface, on-surface) rather than scattering raw hex values through component code.
- In dark mode use desaturated/lighter tonal variants, not simply inverted colors — and test contrast in dark mode separately from light mode.
- Foreground/background pairs must meet at least 4.5:1 contrast (AA) or 7:1 (AAA) — verify with a contrast-checking tool.
- Functional colors (error red, success green) must be paired with an icon or text, never rely on color alone to convey meaning.
- Prefer text wrapping over truncation; when truncation is unavoidable, use an ellipsis and provide the full text via a tooltip or expand affordance.
- Respect the platform's default letter-spacing; avoid tight tracking on body text.
- Use tabular/monospaced figures for data columns, prices, and timers, to prevent digits from causing layout shift as they change.
- Use whitespace intentionally to group related items and separate sections — avoid visual clutter.

### 7. Animation (MEDIUM)

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

### 8. Forms & Feedback (MEDIUM)

- A visible label per input — never rely on a placeholder as the only label.
- Show validation errors directly below the related field.
- Show a loading state, then a success/error state, on submit.
- Mark required fields clearly (e.g. an asterisk).
- Show a helpful message and an available action for any empty state.
- Auto-dismiss toast notifications after 3-5 seconds.
- Confirm before any destructive action.
- Provide persistent helper text below complex inputs, not just a placeholder.
- Disabled elements should use reduced opacity (~0.38-0.5) plus a cursor change plus the semantic disabled attribute — all three, not just a visual cue.
- Reveal complex options progressively; don't overwhelm the user with every option up front.
- Validate on blur, not on every keystroke — show an error only after the user has finished with that field.
- Use semantic input types (email, tel, number) so mobile devices show the correct keyboard.
- Provide a show/hide toggle on password fields.
- Use autocomplete/content-type attributes so the OS/browser can autofill correctly.
- Allow undo for destructive or bulk actions (e.g. an "Undo delete" toast).
- Confirm completed actions with brief visual feedback (a checkmark, a toast, a color flash).
- Error messages must include a clear recovery path (retry, edit, a help link) — not just a statement that something went wrong.
- Multi-step flows should show a step indicator or progress bar, and allow navigating back.
- Long forms should auto-save drafts to prevent data loss on an accidental dismissal.
- Confirm before dismissing a sheet/modal that has unsaved changes.
- Error messages must state both the cause and how to fix it — never just "Invalid input."
- Group related fields logically (a fieldset/legend, or clear visual grouping).
- A read-only state should look and behave distinctly from a disabled state.
- After a failed submit, auto-focus the first invalid field.
- For multiple simultaneous errors, show a summary at the top with anchor links to each field.
- Mobile input height should be at least 44px to meet touch-target requirements.
- Destructive actions should use a semantic danger color (red) and be visually separated from primary actions.
- Toasts must never steal keyboard focus; use a polite live-region announcement for screen readers.
- Form errors should use a live region or alert role so screen readers announce them.
- Error and success state colors must meet 4.5:1 contrast.
- A request timeout must show clear feedback with a retry option.

### 9. Navigation Patterns (HIGH)

- Bottom navigation: maximum 5 items, each with both a label and an icon.
- Use a drawer/sidebar for secondary navigation, not for primary actions.
- Back navigation must be predictable and consistent, and preserve scroll position/state.
- Every key screen should be reachable via a deep link/URL, for sharing and for notifications.
- On iOS, use a bottom tab bar for top-level navigation; on Android, a top app bar with a navigation icon.
- Navigation items need both an icon and a text label — icon-only navigation hurts discoverability.
- The current location must be visually highlighted (color, weight, an indicator) within the navigation.
- Keep primary navigation (tabs/bottom bar) clearly separated from secondary navigation (drawer/settings).
- Modals and sheets must offer a clear close/dismiss affordance; support swipe-down-to-dismiss on mobile.
- Search should be easily reachable (a top bar or a tab) and offer recent/suggested queries.
- On web, use breadcrumbs for hierarchies three or more levels deep.
- Navigating back must restore the previous scroll position, filter state, and any in-progress input.
- Support system gesture navigation (iOS swipe-back, Android predictive back) without conflicting with it.
- Use badges on nav items sparingly, to indicate unread/pending state, and clear them once visited.
- When actions exceed available space, use an overflow/"more" menu rather than cramming everything in.
- Bottom navigation is for top-level screens only — never nest sub-navigation inside it.
- On large screens (≥1024px) prefer a sidebar; on small screens use bottom/top nav.
- Never silently reset the navigation stack or unexpectedly jump the user back to home.
- Keep navigation placement consistent across every page — don't vary it by page type.
- Don't mix tab navigation, a sidebar, and bottom navigation at the same hierarchy level.
- Never use a modal for a primary navigation flow — it breaks the user's sense of place.
- After a page transition, move keyboard/screen-reader focus to the main content region.
- Keep core navigation reachable from deep pages — don't hide it entirely inside a sub-flow.
- Keep dangerous actions (delete account, log out) visually and spatially separated from normal nav items.
- If a nav destination is temporarily unavailable, explain why rather than silently hiding it.

### 10. Charts & Data (LOW)

- Match chart type to data type: trend → line, comparison → bar, proportion → pie/donut.
- Use accessible color palettes; avoid a red/green-only pairing (fails for colorblind users).
- Provide a table alternative — charts alone aren't screen-reader friendly.
- Supplement color with patterns, textures, or shapes so data is distinguishable without relying on color.
- Always show a legend, positioned near the chart, not detached below a scroll fold.
- Provide tooltips/data labels on hover (web) or tap (mobile) showing exact values.
- Label axes with units and a readable scale; avoid truncated or rotated labels on mobile.
- Charts must reflow or simplify on small screens (e.g. switch to horizontal bars, fewer ticks).
- Show a meaningful empty state ("No data yet" + guidance) rather than a blank chart when there's no data.
- Use a skeleton/shimmer placeholder while chart data loads — never an empty axis frame.
- Chart entrance animations must respect reduced-motion settings; data should be readable immediately regardless.
- For 1,000+ data points, aggregate or sample, and provide drill-down for detail rather than rendering everything at once.
- Use locale-aware formatting for numbers, dates, and currencies on axes and labels.
- Interactive chart elements (points, segments) need at least a 44pt tap area, or should expand on touch.
- Avoid pie/donut charts for more than 5 categories — switch to a bar chart for clarity.
- Data lines/bars vs. background: at least 3:1 contrast; data text labels: at least 4.5:1.
- Legends should be clickable to toggle series visibility.
- For small datasets, label values directly on the chart to reduce eye travel.
- Tooltip content must be keyboard-reachable, not hover-only.
- Data tables must support sorting, with the current sort state announced (e.g. via `aria-sort`).
- Axis ticks must not be cramped — keep spacing readable and auto-skip labels on small screens.
- Limit information density per chart to avoid cognitive overload; split into multiple charts if needed.
- Emphasize the data trend over decoration — avoid heavy gradients/shadows that obscure the data itself.
- Grid lines should be low-contrast so they don't compete visually with the data.
- Interactive chart elements must be keyboard-navigable.
- Provide a text summary or accessible description of the chart's key insight, for screen readers.
- A data-load failure must show an error message with a retry action, not a broken/empty chart.
- For data-heavy products, offer a CSV/image export of the chart data.
- Drill-down interactions must maintain a clear back-path and hierarchy breadcrumb.
- Time-series charts must clearly label the time granularity (day/week/month) and allow switching it.

## Common rules for professional-feeling app UI

These are frequently overlooked issues that make an interface look unprofessional. (This section is scoped to app UI — iOS/Android/React Native/Flutter — rather than desktop-web interaction patterns.)

### Icons & visual elements

| Rule | Standard | Avoid | Why it matters |
|---|---|---|---|
| No emoji as structural icons | Use vector-based icons (Phosphor, Heroicons, a platform icon library). | Emoji (🎨 🚀 ⚙️) for navigation, settings, or system controls. | Emoji are font-dependent, render inconsistently across platforms, and can't be controlled via design tokens. |
| Vector-only assets | SVG or platform vector icons that scale cleanly and support theming. | Raster PNG icons that blur or pixelate. | Ensures scalability, crisp rendering, and dark/light-mode adaptability. |
| Stable interaction states | Color, opacity, or elevation transitions for press states, without changing layout bounds. | Layout-shifting transforms that move surrounding content or trigger visual jitter. | Prevents unstable interactions and preserves perceived quality on mobile. |
| Correct brand logos | Official brand assets, following their usage guidelines (spacing, color, clear space). | Guessing logo paths, recoloring unofficially, or distorting proportions. | Prevents brand misuse and legal/platform compliance issues. |
| Consistent icon sizing | Icon sizes as design tokens (e.g. icon-sm/md/lg = fixed values). | Mixing arbitrary values (20pt/24pt/28pt) randomly. | Maintains rhythm and visual hierarchy. |
| Stroke consistency | One consistent stroke width within a visual layer. | Mixing thick and thin strokes arbitrarily. | Inconsistent strokes reduce perceived polish. |
| Filled vs. outline discipline | One icon style per hierarchy level. | Mixing filled and outline icons at the same hierarchy level. | Maintains semantic clarity and stylistic coherence. |
| Touch target minimum | At least 44×44pt interactive area (expand the hit area if the icon itself is smaller). | Small icons with no expanded tap area. | Meets accessibility and usability standards. |
| Icon alignment | Aligned to the text baseline, with consistent padding. | Misaligned icons or inconsistent spacing around them. | Prevents subtle visual imbalance. |
| Icon contrast | WCAG contrast: 4.5:1 for small elements, 3:1 minimum for larger glyphs. | Low-contrast icons that blend into the background. | Ensures accessibility in both light and dark modes. |

### Interaction (app)

| Rule | Do | Don't |
|---|---|---|
| Tap feedback | Clear pressed feedback (ripple/opacity/elevation) within 80-150ms | No visual response on tap |
| Animation timing | Micro-interactions around 150-300ms with platform-native easing | Instant transitions or slow (>500ms) animations |
| Accessibility focus | Screen-reader focus order matches visual order; descriptive labels | Unlabeled controls, confusing focus traversal |
| Disabled state clarity | Semantic disabled state, reduced emphasis, no tap action | Controls that look tappable but do nothing |
| Touch target minimum | ≥44×44pt (iOS) / ≥48×48dp (Android); expand hit area for small icons | Tiny tap targets or icon-only hit areas without padding |
| Gesture conflict prevention | One primary gesture per region; avoid nested tap/drag conflicts | Overlapping gestures causing accidental actions |
| Semantic native controls | Native interactive primitives with proper accessibility roles | Generic containers used as primary controls with no semantics |

### Light/dark mode contrast

| Rule | Do | Don't |
|---|---|---|
| Surface readability (light) | Cards/surfaces clearly separated from background via opacity/elevation | Overly transparent surfaces that blur hierarchy |
| Text contrast (light) | Body text contrast ≥4.5:1 against light surfaces | Low-contrast gray body text |
| Text contrast (dark) | Primary text ≥4.5:1, secondary text ≥3:1, on dark surfaces | Dark-mode text that blends into the background |
| Border/divider visibility | Separators visible in both themes | Theme-specific borders that disappear in one mode |
| State contrast parity | Pressed/focused/disabled states equally distinguishable in both themes | Interaction states defined for only one theme |
| Token-driven theming | Semantic color tokens mapped per theme across surfaces/text/icons | Hardcoded per-screen hex values |
| Scrim and modal legibility | Modal scrim strong enough to isolate foreground content (~40-60% black) | Weak scrim that leaves the background visually competing |

### Layout & spacing

| Rule | Do | Don't |
|---|---|---|
| Safe-area compliance | Respect top/bottom safe areas for fixed headers, tab bars, CTA bars | Fixed UI placed under the notch, status bar, or gesture area |
| System bar clearance | Spacing for status/nav bars and the gesture home indicator | Tappable content colliding with OS chrome |
| Consistent content width | Predictable content width per device class | Mixing arbitrary widths between screens |
| 8dp spacing rhythm | Consistent 4/8dp spacing system for padding/gaps/section spacing | Random spacing increments with no rhythm |
| Readable text measure | Long-form text stays readable on large devices | Edge-to-edge paragraphs on tablets |
| Section spacing hierarchy | Clear vertical rhythm tiers (e.g. 16/24/32/48) by hierarchy | Similar UI levels with inconsistent spacing |
| Adaptive gutters by breakpoint | Larger horizontal insets on wider widths and in landscape | Same narrow gutter on every device size/orientation |
| Scroll and fixed-element coexistence | Bottom/top content insets so lists aren't hidden behind fixed bars | Scroll content obscured by sticky headers/footers |

## Pre-delivery checklist

Before delivering UI code, verify all of the following. (Scoped to app UI — iOS/Android/React Native/Flutter.)

**Visual quality**
- No emoji used as icons (SVG instead).
- All icons come from one consistent icon family and style.
- Official brand assets used with correct proportions and clear space.
- Pressed-state visuals don't shift layout bounds or cause jitter.
- Semantic theme tokens used consistently — no ad hoc per-screen hardcoded colors.

**Interaction**
- All tappable elements provide clear pressed feedback (ripple/opacity/elevation).
- Touch targets meet the minimum size (≥44×44pt iOS, ≥48×48dp Android).
- Micro-interaction timing stays in the 150-300ms range with native-feeling easing.
- Disabled states are visually clear and non-interactive.
- Screen-reader focus order matches visual order, and interactive labels are descriptive.
- Gesture regions avoid nested/conflicting interactions (tap/drag/back-swipe conflicts).

**Light/dark mode**
- Primary text contrast ≥4.5:1 in both light and dark mode.
- Secondary text contrast ≥3:1 in both light and dark mode.
- Dividers/borders and interaction states are distinguishable in both modes.
- Modal/drawer scrim opacity is strong enough to preserve foreground legibility (~40-60% black).
- Both themes are actually tested before delivery — never inferred from a single theme.

**Layout**
- Safe areas respected for headers, tab bars, and bottom CTA bars.
- Scroll content is not hidden behind fixed/sticky bars.
- Verified on a small phone, a large phone, and a tablet (portrait + landscape).
- Horizontal insets/gutters adapt correctly by device size and orientation.
- 4/8dp spacing rhythm maintained across component, section, and page levels.
- Long-form text measure remains readable on larger devices (no edge-to-edge paragraphs).

**Accessibility**
- All meaningful images/icons have accessibility labels.
- Form fields have labels, hints, and clear error messages.
- Color is never the only indicator of meaning or state.
- Reduced motion and dynamic text size are supported without breaking the layout.
- Accessibility traits/roles/states (selected, disabled, expanded) are announced correctly.

## Common sticking points and where to look

| Problem | What to check |
|---|---|
| Can't decide on style/color | Revisit the product type and audience, and try a different combination of style keywords |
| Dark-mode contrast issues | Typography & Color: dark-mode desaturation + accessible-pair contrast rules |
| Animations feel unnatural | Animation: spring-physics curves + easing direction + exit-faster-than-enter |
| Form UX is poor | Forms & Feedback: inline validation timing + error clarity + focus management |
| Navigation feels confusing | Navigation: primary/secondary nav separation + bottom-nav item limit + predictable back behavior |
| Layout breaks on small screens | Layout & Responsive: mobile-first + consistent breakpoints |
| Performance/jank | Performance: list virtualization + main-thread budget + debounce/throttle |
</content>
