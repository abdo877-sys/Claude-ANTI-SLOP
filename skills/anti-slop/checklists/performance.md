# Performance checklist

Targets (mobile): LCP < 2.5s · INP < 200ms · CLS < 0.1. Report only measured values.

## Images
- [ ] Modern formats (AVIF/WebP) with fallbacks; responsive `srcset`/`sizes` or framework image component
- [ ] Intrinsic `width`/`height` or `aspect-ratio` on every image
- [ ] LCP image: not lazy, `fetchpriority="high"`, preloaded if discovered late
- [ ] Below-the-fold images `loading="lazy" decoding="async"`

## Fonts
- [ ] ≤ 2 families, WOFF2, subset to used scripts
- [ ] Framework loader or self-hosted; `font-display: swap`; no CSS `@import` of remote fonts
- [ ] Voice face preloaded; metric-matched fallback to limit CLS

## JavaScript
- [ ] Route-level code splitting; heavy widgets (charts, maps, editors, 3D) dynamically imported
- [ ] No unused dependencies added; bundle checked if tooling exists
- [ ] Marketing content renders without client JS (SSR/SSG)
- [ ] Third-party scripts deferred/async

## CSS and animation
- [ ] Only transform/opacity animated; no `transition: all`
- [ ] No large fixed widths; no layout thrash on scroll
- [ ] Offscreen animations/videos paused

## Measurement
- [ ] Lighthouse (or `npx unlighthouse` / Lighthouse CI) run on key routes if available — paste real numbers
- [ ] If not measurable here: say "performance not measured" and list the static checks done
