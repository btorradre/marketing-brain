# Accessibility (Priority 1 — CRITICAL)

Accessibility is the single most critical rule category. Contrast, focus states, labels, and keyboard support are non-negotiable baseline quality on every screen, not a pass applied at the end.

## Core rules

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

## Full rule database (verbatim from source)

Source: `ux-guidelines.csv` (cross-platform, 11 rows) and `app-interface.csv` (iOS/Android/React Native specific, 5 rows).

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 36 | Accessibility | Color Contrast | All | Text must be readable against background | `Minimum 4.5:1 ratio for normal text` | `Low contrast text` | `#333 on white (7:1)` | `#999 on white (2.8:1)` | High |
| 37 | Accessibility | Color Only | All | Don't convey information by color alone | `Use icons/text in addition to color` | `Red/green only for error/success` | `Red text + error icon` | `Red border only for error` | High |
| 38 | Accessibility | Alt Text | All | Images need text alternatives | `Descriptive alt text for meaningful images` | `Empty or missing alt attributes` | `alt='Dog playing in park'` | `alt='' for content images` | High |
| 39 | Accessibility | Heading Hierarchy | Web | Screen readers use headings for navigation | `Use sequential heading levels h1-h6` | `Skip heading levels or misuse for styling` | `h1 then h2 then h3` | `h1 then h4` | Medium |
| 40 | Accessibility | ARIA Labels | All | Interactive elements need accessible names | `Add aria-label for icon-only buttons` | `Icon buttons without labels` | `aria-label='Close menu'` | `<button><Icon/></button>` | High |
| 41 | Accessibility | Keyboard Navigation | Web | All functionality accessible via keyboard | `Tab order matches visual order` | `Keyboard traps or illogical tab order` | `tabIndex for custom order` | `Unreachable elements` | High |
| 42 | Accessibility | Screen Reader | All | Content should make sense when read aloud | `Use semantic HTML and ARIA properly` | `Div soup with no semantics` | `<nav> <main> <article>` | `<div> for everything` | Medium |
| 43 | Accessibility | Form Labels | All | Inputs must have associated labels | `Use label with for attribute or wrap input` | `Placeholder-only inputs` | `<label for='email'>` | `placeholder='Email' only` | High |
| 44 | Accessibility | Error Messages | All | Error messages must be announced | `Use aria-live or role=alert for errors` | `Visual-only error indication` | `role='alert'` | `Red border only` | High |
| 45 | Accessibility | Skip Links | Web | Allow keyboard users to skip navigation | `Provide skip to main content link` | `No skip link on nav-heavy pages` | `Skip to main content link` | `100 tabs to reach content` | Medium |
| 99 | Accessibility | Motion Sensitivity | All | Parallax/Scroll-jacking causes nausea | `Respect prefers-reduced-motion` | `Force scroll effects` | `@media (prefers-reduced-motion)` | `ScrollTrigger.create()` | High |

### App-interface rows (iOS/Android/React Native specific)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Accessibility | Icon Button Labels | icon button accessibilityLabel | iOS/Android/React Native | Icon-only buttons must expose an accessible label | `Set accessibilityLabel or label prop on icon buttons` | `Icon buttons without accessible names` | `<Pressable accessibilityLabel="Close"><XIcon /></Pressable>` | `<Pressable><XIcon /></Pressable>` | Critical |
| 2 | Accessibility | Form Control Labels | form input label accessibilityLabel | iOS/Android/React Native | All inputs must have a visible label and an accessibility label | `Pair Text label with input and set accessibilityLabel` | `Inputs with placeholder only` | `<View><Text>Email</Text><TextInput accessibilityLabel="Email address" /></View>` | `<TextInput placeholder="Email" /></View>` | Critical |
| 3 | Accessibility | Role & Traits | accessibilityRole accessibilityTraits | iOS/Android/React Native | Interactive elements must expose correct roles/traits | `Use accessibilityRole/button/link/checkbox etc.` | `Rely on generic views with no roles` | `<Pressable accessibilityRole="button">Submit</Pressable>` | `<View onTouchStart={submit}>Submit</View>` | High |
| 4 | Accessibility | Dynamic Updates | accessibilityLiveRegion announce | iOS/Android/React Native | Async status updates should be announced to screen readers | `Use accessibilityLiveRegion or announceForAccessibility` | `Update text silently with no announcement` | `<Text accessibilityLiveRegion="polite">{status}</Text>` | `<Text>{status}</Text>` | Medium |
| 5 | Accessibility | Decorative Icons | accessible={false} importantForAccessibility | iOS/Android/React Native | Decorative icons should be hidden from screen readers | `Mark decorative icons as not accessible` | `Have screen reader read every icon` | `<Icon accessible={false} importantForAccessibility="no" />` | `<Icon />` | Medium |
