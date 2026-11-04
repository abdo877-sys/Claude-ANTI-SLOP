# Frontend engineering standards

## 0. Respect the project
- Detect and use the existing framework, router, styling approach, component
  library, lint/format config, and naming conventions. Read 2–3 existing
  components before writing a new one and match them.
- Smallest change that achieves the brief. Don't migrate frameworks, CSS
  systems or state libraries to restyle a page.
- New dependency only if it removes more code/complexity than it adds; say why.
  Prefer platform features (CSS Grid, `<dialog>`, View Transitions, container queries).
- Never modify files unrelated to the task.

## 1. Semantic HTML
- Landmarks: `header`, `nav`, `main#main`, `footer`, `aside` where real.
- Heading levels in order, one `h1`.
- Lists are `ul/ol`, tables are `table`, buttons are `button`, links are `a`.
- `lang` (and `dir="rtl"` for Arabic/Hebrew) on `<html>`.

## 2. CSS
- Tokens as custom properties; components reference tokens only.
- Logical properties (`margin-inline`, `padding-block`, `inset-inline-start`) so RTL works for free.
- Layout with Grid/Flex; `clamp()` for fluid type/space; container queries for components.
- Cascade layers (`@layer reset, tokens, base, components, utilities`) in plain-CSS projects.
- Tailwind: extend the theme with tokens; keep arbitrary values (`[...]`) rare;
  extract repeated class sets into components, not `@apply` soup.

## 3. Components and TypeScript
- Components small, single-purpose, props typed explicitly; no `any`.
- `strict: true`; discriminated unions for variants (`variant: "primary" | "secondary"`).
- Separate data fetching from presentation where the framework allows.
- Handle `loading | error | empty | success` explicitly (a union, not booleans).

## 4. Performance budget (targets, mobile, 4G)
LCP < 2.5s · INP < 200ms · CLS < 0.1 · JS on landing page < 150KB gz where feasible.
- **Images:** framework image component or `<img srcset sizes width height loading="lazy" decoding="async">`;
  AVIF/WebP; the LCP image is *not* lazy and gets `fetchpriority="high"`.
- **Fonts:** see `typography.md` § loading; ≤2 families, subset, preload the voice face.
- **Code splitting:** route-level by default; dynamic import heavy widgets
  (charts, editors, maps, 3D) and load them on interaction or visibility.
- **Animation:** transform/opacity only; no layout thrash; pause offscreen.
- **Third parties:** defer analytics; no blocking scripts in `<head>`.
- Measure if possible (Lighthouse CI, `npx unlighthouse`, browser Performance panel). Report only measured numbers.

## 5. SEO fundamentals
- Unique `<title>` (≤60 chars) and meta description per page; canonical URL.
- Open Graph/Twitter image and text that reflect the real page.
- Semantic headings, descriptive link text, `alt` on content images.
- `sitemap.xml`, `robots.txt`, structured data (JSON-LD) where it fits the content type
  (Organization, Product, Article, BreadcrumbList).
- Content must render without client JS for marketing pages (SSR/SSG).

## 6. Error handling
- Error boundaries (React) / error pages per route. User-facing messages, logged details.
- Network: timeouts, retry for idempotent requests, offline message.
- Never swallow errors silently; never show stack traces to users.

## 7. Browser compatibility
- Target the project's browserslist; default to last 2 versions + Safari iOS.
- Feature-detect modern CSS (`@supports`) and provide acceptable fallbacks
  (OKLCH → hex, `text-wrap` → normal, View Transitions → none).
- Test in Chromium and at least reason about WebKit quirks (100vh → `100dvh`, sticky inside overflow).

## 8. Maintainability
- No magic numbers in components; no duplicated token values.
- Delete dead code you replace. Keep diffs reviewable.
- Leave `DESIGN.md` updated when you add or change a token.
