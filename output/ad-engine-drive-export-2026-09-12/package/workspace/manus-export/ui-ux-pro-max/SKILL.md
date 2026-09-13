---
name: ui-ux-pro-max
description: Comprehensive UI/UX design intelligence for web and mobile — a prioritized rulebook covering accessibility, touch/interaction, performance, style selection, layout, typography/color, animation, forms, navigation, and charts, backed by a database of 84 named styles, 161 color palettes, 73 font pairings, 161 product-type design-system recommendations, and 25 chart-type mappings. Use when designing new pages or apps, creating or refactoring UI components, choosing a color/typography/style system, reviewing existing UI for accessibility or consistency, implementing navigation/animation/responsive behavior, or doing a pre-launch UI quality pass. Applies across common frontend stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, plain HTML/CSS).
---

# UI/UX Pro Max — Design Intelligence

A prioritized rulebook for UI structure, visual design decisions, interaction patterns, and user-experience quality control. It combines a set of hard numeric/technical rules (contrast ratios, touch-target sizes, timing values, breakpoints) with a searchable design-system database (styles, color palettes, font pairings, product-type recommendations, chart types).

## When to apply this

Use this guidance when:
- Designing new pages (landing page, dashboard, admin panel, SaaS product, mobile app).
- Creating or refactoring UI components (buttons, modals, forms, tables, charts, etc.).
- Choosing color schemes, typography systems, spacing standards, or layout systems.
- Reviewing UI code for user experience, accessibility, or visual consistency.
- Implementing navigation structures, animations, or responsive behavior.
- Making product-level design decisions (style, information hierarchy, brand expression).
- Improving the perceived quality, clarity, or usability of an interface.

Also apply it when the UI "looks unprofessional" but the reason is unclear, when there's feedback on usability, before a launch as a quality pass, when aligning design across web/iOS/Android, or when building a design system or reusable component library.

Skip it for pure backend logic, API/database design, non-visual performance work, infrastructure/DevOps, or non-visual scripts. Decision rule: if the task changes how a feature **looks, feels, moves, or is interacted with**, apply this guidance.

## How to use this

### 1. Analyze the requirements

Extract from the request: the product type (entertainment — social/video/music/gaming; tool — scanner/editor/converter; productivity — task manager/notes/calendar; or a hybrid), the target audience (age group, usage context — commute, leisure, work), style keywords (playful, vibrant, minimal, dark mode, content-first, immersive, etc.), and the target technology stack.

### 2. Establish a design system before writing any component

Before building individual components, decide and write down (even briefly) a coherent design system for the whole project: an overall visual pattern/style, a color palette, a typography pairing, and a set of visual effects (shadows, blur, radius) — all chosen to match the product type and audience, with explicit anti-patterns to avoid for that style. Don't let color, font, and component style get decided ad hoc, component by component — that's what produces an inconsistent, "not quite professional" result.

Use `references/product-design-system.md` to drive this: look up the product type (or the closest match) to get a primary style recommendation, a landing-page pattern, a color-palette focus, and the decision rules / anti-patterns for that category. Then pull the actual style details from `references/style-catalog.md`, the font pairing from `references/typography-pairings.md`, and the palette hex values from `references/color-palettes.md`.

For larger projects, maintain one master design-system document (colors, type scale, spacing scale, component conventions, anti-patterns) as the single source of truth, and only create a page-specific override document when a particular page deliberately deviates from the master (e.g. a checkout page with a stripped-down nav). When building any specific page, check for a page-level override first; fall back to the master rules if none exists. This keeps a large multi-page build visually consistent without forcing every page to be identical.

### 3. Apply the detailed rule checklists

Work through the ten rule categories below, prioritized 1 (most critical) to 10 (least critical) — treat 1-3 as non-negotiable baseline quality, 4-6 as strongly expected, 7-10 as refinement:

| Priority | Category | Impact | Reference file |
|---|---|---|---|
| 1 | Accessibility | CRITICAL | `references/accessibility.md` |
| 2 | Touch & Interaction | CRITICAL | `references/touch-targets.md` |
| 3 | Performance | HIGH | `references/performance.md` |
| 4 | Style Selection | HIGH | `references/style.md` (+ `style-catalog.md`) |
| 5 | Layout & Responsive | HIGH | `references/layout.md` |
| 6 | Typography & Color | MEDIUM | `references/typography.md` (+ `typography-pairings.md`, `color-palettes.md`) |
| 7 | Animation | MEDIUM | `references/animation.md` |
| 8 | Forms & Feedback | MEDIUM | `references/forms.md` |
| 9 | Navigation Patterns | HIGH | `references/navigation.md` |
| 10 | Charts & Data | LOW | `references/charts.md` |

### 4. Run a pre-delivery check before calling any UI work finished

**Visual quality**
- No emoji used as icons (SVG instead); one consistent icon family and style throughout.
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
- Primary text contrast ≥4.5:1, secondary text contrast ≥3:1, in both light and dark mode.
- Dividers/borders and interaction states are distinguishable in both modes.
- Modal/drawer scrim opacity is strong enough to preserve foreground legibility (~40-60% black).
- Both themes are actually tested before delivery — never inferred from a single theme.

**Layout**
- Safe areas respected for headers, tab bars, and bottom CTA bars; scroll content not hidden behind fixed/sticky bars.
- Verified on a small phone, a large phone, and a tablet (portrait + landscape).
- 4/8dp spacing rhythm maintained across component, section, and page levels.
- Long-form text measure remains readable on larger devices (no edge-to-edge paragraphs).

**Accessibility**
- All meaningful images/icons have accessibility labels; form fields have labels, hints, and clear error messages.
- Color is never the only indicator of meaning or state.
- Reduced motion and dynamic text size are supported without breaking the layout.
- Accessibility traits/roles/states (selected, disabled, expanded) are announced correctly.

Run through the CRITICAL and HIGH categories (1-3, 5, 9) as a final review before delivery. Test at a small-phone width (375px) and in landscape orientation. Verify behavior with reduced-motion enabled and with text scaled to its largest supported size. Check dark-mode contrast independently — never assume light-mode color values will also pass in dark mode. Confirm all touch targets are at least 44×44pt and nothing is hidden behind device safe areas (notch, home indicator, status/nav bars).

## Reference file index

Each file below preserves the full, verbatim numeric/technical rule set for its category — exact pixel sizes, contrast ratios, timing values, breakpoints, and (where the source has them) concrete Do/Don't pairs with code examples. Don't paraphrase these values when applying them; read the relevant file and cite the exact number.

- **`references/accessibility.md`** — Contrast ratios, focus rings, ARIA/labels, keyboard nav, screen-reader rules. CRITICAL, check first on every UI task.
- **`references/touch-targets.md`** — Minimum tap sizes, spacing, gesture rules, press feedback timing. CRITICAL.
- **`references/performance.md`** — Image/font loading, code splitting, list virtualization, main-thread budget, plus the full React/Next.js performance rule set (async waterfalls, rerenders, bundle size).
- **`references/style.md`** — How to pick and stay consistent with a visual style; icon system rules. Points to `style-catalog.md` for the full 84-style database (colors, effects, best-for/avoid-for, framework compatibility, ready-to-use AI prompt keywords).
- **`references/style-catalog.md`** — The 84-entry style catalog itself (Minimalism, Glassmorphism, Claymorphism, Brutalism, Neumorphism, Bento Grid, Skeuomorphism, etc.).
- **`references/layout.md`** — Breakpoints, spacing scale, z-index scale, safe areas, viewport rules.
- **`references/typography.md`** — Type scale, line-height/length, semantic color tokens, dark-mode contrast rules. Points to `typography-pairings.md` (73 font pairings with ready CSS/Tailwind) and `color-palettes.md` (161 product-type hex palettes).
- **`references/typography-pairings.md`** — The 73 curated heading/body font-pairing database.
- **`references/color-palettes.md`** — The 161 product-type semantic color-token database (all as hex values).
- **`references/animation.md`** — Duration/easing values, what to animate vs never animate, stagger timing, reduced-motion handling.
- **`references/forms.md`** — Label/validation/error rules, toast timing, disabled-state styling, multi-step flow rules.
- **`references/navigation.md`** — Bottom-nav limits, back-behavior, deep linking, platform-specific nav idioms.
- **`references/charts.md`** — Chart UI rules (legends, tooltips, accessible color) plus the 25-entry chart-type selection database (which chart for which data, with accessibility grades and library recommendations).
- **`references/product-design-system.md`** — The design-system generation database: ~161 product types → style/pattern/color recommendations, 34 landing-page structure patterns, and the machine-readable decision-rule/anti-pattern reasoning layer used to resolve style choices for a given product type.
- **`references/emerging-patterns.md`** — Smaller, situational rule sets outside the 10 core categories: content formatting, onboarding, AI-interaction UX (disclosure, streaming, feedback loops), spatial/VisionOS UI, sustainability (auto-play, asset weight), and app-specific state-preservation/anti-pattern rules.

Not reproduced in this reference set (present in the original source vault but out of scope for a precision rules doc): a raw catalog of ~1,900 individual Google Fonts (`google-fonts.csv`, use the 73 curated pairings first), and per-framework implementation-detail notes for 16 stacks (React, Next.js, Vue, Svelte, Astro, SwiftUI, React Native, Flutter, Nuxt.js, Nuxt UI, HTML+Tailwind, shadcn/ui, Jetpack Compose, Three.js, Angular, Laravel).

## Common sticking points and where to look

| Problem | What to check |
|---|---|
| Can't decide on style/color | Revisit the product type and audience in `references/product-design-system.md`, and try a different combination of style keywords against `references/style-catalog.md` |
| Dark-mode contrast issues | `references/typography.md`: dark-mode desaturation + accessible-pair contrast rules |
| Animations feel unnatural | `references/animation.md`: spring-physics curves + easing direction + exit-faster-than-enter |
| Form UX is poor | `references/forms.md`: inline validation timing + error clarity + focus management |
| Navigation feels confusing | `references/navigation.md`: primary/secondary nav separation + bottom-nav item limit + predictable back behavior |
| Layout breaks on small screens | `references/layout.md`: mobile-first + consistent breakpoints |
| Performance/jank | `references/performance.md`: list virtualization + main-thread budget + debounce/throttle |
| Charts look inaccessible or wrong type | `references/charts.md`: chart-type-to-data-type mapping + accessibility grade + fallback requirement |
