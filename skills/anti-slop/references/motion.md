# Motion and interaction

## 1. Motion must explain something
Allowed jobs: show causality (this came from there), show state change,
direct attention once, give feedback, preserve spatial orientation during
navigation. If an animation does none of these, remove it.

## 2. Personality from the metaphor
| Metaphor quality | Duration | Curve |
|---|---|---|
| Paper — slides and settles | 180–240ms | `cubic-bezier(.2,.7,.2,1)` (ease-out) |
| Stamp — lands | 100–140ms | `cubic-bezier(.3,1.3,.6,1)` (≤3% overshoot) |
| Terminal — cuts | 0–80ms | `steps(3)` or linear |
| Fabric — drapes | 280–360ms | `cubic-bezier(.45,0,.2,1)` |
| Precise instrument | 120–200ms | `cubic-bezier(.2,0,0,1)` |

Tokens: `--dur-fast`, `--dur-base`, `--dur-slow`, `--ease-standard`,
`--ease-emphasis`. Use them everywhere; no ad-hoc durations.

## 3. Micro-interactions that earn their place
- Hover: reveal *information* (preview, underline that grows, cursor-follow
  label on media) — not just lift + shadow.
- Press: 1–2px translate or tone shift, under 120ms.
- Toggle/checkbox: a state change the eye can follow.
- Copy button: inline "Copied" confirmation, not a toast.
- Form: inline validation on blur, success state on submit.

## 4. Scroll
- Reveal-on-scroll only for content that benefits from sequence (steps, data
  stories). Not for every section. Never hide content until JS runs — content
  must be visible without JS and with reduced motion.
- Stagger ≤60ms per item, ≤6 items; beyond that reveal as a group.
- Use `IntersectionObserver` or CSS scroll-driven animations
  (`animation-timeline: view()`) with a fallback; avoid scroll listeners.

## 5. Page transitions
View Transitions API (`document.startViewTransition`, or framework support)
for shared-element continuity. Keep under 300ms. Skip for back/forward if it fights the browser.

## 6. Framer Motion (React)
Use it when the project already depends on it or when you need layout
animations / shared layout / gestures. Prefer `motion` + `LazyMotion` with
`domAnimation` to keep the bundle small. For simple fades and hovers, CSS is enough.

```tsx
import { LazyMotion, domAnimation, m, useReducedMotion } from "motion/react";
const reduce = useReducedMotion();
<LazyMotion features={domAnimation}>
  <m.li initial={reduce ? false : { opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2, ease: [0.2, 0.7, 0.2, 1] }} />
</LazyMotion>
```

## 7. Performance and safety
- Animate only `transform` and `opacity` (and `filter` sparingly). Never
  width/height/top/left on frequent animations.
- No infinite animations except genuine live status.
- Respect `prefers-reduced-motion`: replace movement with instant or opacity-only changes.
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
```
- Nothing flashes more than 3 times per second.
