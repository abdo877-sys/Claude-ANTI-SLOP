# Typography

Type is where most of an identity lives. Decide it before color.

## 1. Roles, not fonts
Define two faces maximum (a third only for code/data):
- **Voice** — display, headlines, numbers, brand moments. Carries the direction.
- **Reading** — body, UI labels, forms. Carries legibility.
- **Data** (optional) — mono or tabular for code, prices, metrics.

## 2. Choosing faces from the direction
| Direction / metaphor | Voice candidates | Reading candidates |
|---|---|---|
| Editorial, manuscript, luxury | Fraunces, Newsreader, Instrument Serif, Playfair Display (sparingly), Cormorant, Source Serif 4 | Source Serif 4, Newsreader Text, IBM Plex Sans, Public Sans |
| Swiss, institutional, civic | Neue-Haas-like grotesks: Instrument Sans, Schibsted Grotesk, Hanken Grotesk, Geist | Public Sans, IBM Plex Sans, Geist |
| Technical, dev tools, data | JetBrains Mono, IBM Plex Mono, Geist Mono, Space Mono | IBM Plex Sans, Geist, Atkinson Hyperlegible |
| Industrial, signage, transit | Barlow Condensed, Archivo (width axis), Big Shoulders Display, Oswald (sparingly) | Archivo, Barlow, Public Sans |
| Neo-brutalist, playful-direct | Bricolage Grotesque, Space Grotesk, Darker Grotesque, Familjen Grotesk | Space Grotesk, DM Sans |
| Organic, craft, food | Fraunces (soft axis), Recoleta-like serifs (e.g. Gloock), Young Serif | Nunito Sans, Source Sans 3 |
| Playful, kids, games | Fredoka, Baloo 2, Gluten (display only), Bricolage Grotesque | Nunito, Lexend |
| Futuristic, deep tech | Space Grotesk, Unbounded, Michroma (display), Geist | Geist, IBM Plex Sans |

These are *candidates*. Choose by the metaphor: stamped → slab/grotesk with
character; engraved → high-contrast serif; terminal → mono; painted sign →
quirky grotesk. **Inter, Poppins, Roboto, Montserrat and Open Sans are never
the voice face** (they're the statistical default). They may remain as the
reading face if already established in the project.

Scripts: Arabic → IBM Plex Sans Arabic, Noto Naskh/Kufi Arabic, Tajawal,
Amiri (classical). CJK → Noto Sans/Serif JP/SC/TC. Devanagari → Noto Sans
Devanagari, Hind. Check every script your locales need **before** committing.

Licensing: Google Fonts / Fontsource / OFL are safe to ship. Never reference a
commercial font the project doesn't own.

## 3. Fluid scale
Use a ratio that matches the tension pairs: dense/technical → 1.2; balanced →
1.25; editorial/expressive → 1.333–1.5. Generate fluid steps with `clamp()`:

```css
:root {
  --step--1: clamp(0.83rem, 0.80rem + 0.15vw, 0.94rem);
  --step-0:  clamp(1.00rem, 0.95rem + 0.25vw, 1.13rem);  /* body: never < 16px */
  --step-1:  clamp(1.25rem, 1.14rem + 0.50vw, 1.50rem);
  --step-2:  clamp(1.56rem, 1.36rem + 0.95vw, 2.00rem);
  --step-3:  clamp(1.95rem, 1.60rem + 1.70vw, 2.83rem);
  --step-4:  clamp(2.44rem, 1.85rem + 2.90vw, 4.00rem);
  --step-5:  clamp(3.05rem, 2.05rem + 5.00vw, 6.00rem);   /* expressive display */
}
```
Use **fewer steps with more contrast** rather than many near-identical sizes.
A page should visibly use 3–5 sizes, not 9.

## 4. Readability rules
- Measure: 60–75ch for body (`max-width: 68ch`), 35–50ch for lead paragraphs.
- Line-height: body 1.5–1.65; headlines 1.0–1.15; tighter as size grows.
- Tracking: display sizes −0.01 to −0.03em; small caps/labels +0.04 to +0.08em.
- `font-variant-numeric: tabular-nums` wherever numbers are compared.
- `text-wrap: balance` for headlines; `text-wrap: pretty` for paragraphs.
- Left-align body text. Center only short standalone statements.
- Hanging punctuation for pull quotes where supported.

## 5. Variable fonts
Prefer variable files (one request, any weight). Use axes intentionally:
`opsz` for optical size at display vs text, `wdth` for condensed headlines,
`SOFT`/`WONK` in Fraunces for warmth. Animate axes only as a signature move.

## 6. Loading
- Framework loaders first (`next/font`, `@fontsource/*`, Astro fonts) — they
  self-host and set `font-display`.
- Otherwise: self-host WOFF2, `<link rel="preload" as="font" crossorigin>` for
  the voice face only, `font-display: swap`, subset to used scripts.
- Never `@import` Google Fonts inside CSS (render-blocking).
- Define metric-compatible fallbacks (`size-adjust`, `ascent-override`) to cut layout shift.

## 7. Hierarchy check
Squint at the page: you should see exactly one dominant element, then a clear
second level, then body. If three things shout, two must whisper.
