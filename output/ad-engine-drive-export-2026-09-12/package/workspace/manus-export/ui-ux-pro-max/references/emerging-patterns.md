# Emerging & Situational UX Patterns

These are additional UX-guideline categories in the source database that sit outside the 10 core priority categories — smaller in rule count, but still concrete, verbatim rules worth checking for the right project (AI-driven interfaces, spatial/VisionOS UI, content formatting, onboarding, sustainability, and app-specific state/anti-pattern rules).

## Content, Onboarding, AI Interaction, Spatial UI, Sustainability (from `ux-guidelines.csv`)

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 84 | Content | Truncation | All | Handle long content gracefully | `Truncate with ellipsis and expand option` | `Overflow or broken layout` | `line-clamp-2 with expand` | `Overflow or cut off` | Medium |
| 85 | Content | Date Formatting | All | Use locale-appropriate date formats | `Use relative or locale-aware dates` | `Ambiguous date formats` | `2 hours ago or locale format` | `01/02/03` | Low |
| 86 | Content | Number Formatting | All | Format large numbers for readability | `Use thousand separators or abbreviations` | `Long unformatted numbers` | `1.2K or 1,234` | `1234567` | Low |
| 87 | Content | Placeholder Content | All | Show realistic placeholders during dev | `Use realistic sample data` | `Lorem ipsum everywhere` | `Real sample content` | `Lorem ipsum` | Low |
| 88 | Onboarding | User Freedom | All | Users should be able to skip tutorials | `Provide Skip and Back buttons` | `Force linear unskippable tour` | `Skip Tutorial button` | `Locked overlay until finished` | Medium |
| 92 | AI Interaction | Disclaimer | All | Users need to know they talk to AI | `Clearly label AI generated content` | `Present AI as human` | `AI Assistant label` | `Fake human name without label` | High |
| 93 | AI Interaction | Streaming | All | Waiting for full text is slow | `Stream text response token by token` | `Show loading spinner for 10s+` | `Typewriter effect` | `Spinner until 100% complete` | Medium |
| 94 | Spatial UI | Gaze Hover | VisionOS | Elements should respond to eye tracking before pinch | `Scale/highlight element on look` | `Static element until pinch` | `hoverEffect()` | `onTap only` | High |
| 95 | Spatial UI | Depth Layering | VisionOS | UI needs Z-depth to separate content from environment | `Use glass material and z-offset` | `Flat opaque panels blocking view` | `.glassBackgroundEffect()` | `bg-white` | Medium |
| 96 | Sustainability | Auto-Play Video | Web | Video consumes massive data and energy | `Click-to-play or pause when off-screen` | `Auto-play high-res video loops` | `playsInline muted preload='none'` | `autoplay loop` | Medium |
| 97 | Sustainability | Asset Weight | Web | Heavy 3D/Image assets increase carbon footprint | `Compress and lazy load 3D models` | `Load 50MB textures` | `Draco compression` | `Raw .obj files` | Medium |
| 98 | AI Interaction | Feedback Loop | All | AI needs user feedback to improve | `Thumps up/down or 'Regenerate'` | `Static output only` | `Feedback component` | `Read-only text` | Low |

## State & Anti-Pattern (from `app-interface.csv`)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 12 | State | Preserve Screen State | navigation preserve state | iOS/Android/React Native | Returning to a screen should restore its scroll and form state | `Keep components mounted or persist state` | `Reset list scroll and form inputs on every visit` | `<Tab.Navigator screenOptions={{ unmountOnBlur: false }}>` | `<Tab.Screen options={{ unmountOnBlur: true }} />` | Medium |
| 30 | Anti-Pattern | No Gesture-Only Actions | gesture only hidden controls | iOS/Android/React Native | Don't rely solely on hidden gestures for core actions | `Provide visible buttons in addition to gestures` | `Rely on swipe/shake only with no UI affordance` | `Swipe to delete + visible Delete button` | `Only shake device to undo with no UI` | Critical |
