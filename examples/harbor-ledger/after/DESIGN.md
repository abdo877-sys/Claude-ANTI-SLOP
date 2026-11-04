# DESIGN.md — Harbor Ledger

> Source of truth for UI decisions. Humans and AI agents changing the UI must
> follow this file. Values not defined here must not be introduced.
> Created with ANTI-SLOP; update it when a token changes.

## Direction
Swiss International + one Organic move · **the duplicate receipt book**
(carnet à souches). Shop owners already keep credit in a paper book behind the
counter; the site looks like the tool they trust, made clearer.

## Tokens (where they live: `styles.css` → `@layer tokens`)
| Token | Value | Use |
|---|---|---|
| paper | #F4F1E8 | page background (original sheet) |
| copy | #F2E6B4 | the specimen / emphasis surface (yellow carbon copy) |
| field | #FFFDF6 | input background |
| ink | #1D2433 | text (13.75:1 on paper) |
| ink-muted | #4F5566 | secondary text (6.58:1 on paper) |
| rule | #CFC7B2 | decorative form lines |
| rule-strong | #857C66 | input borders, table rules (3.67:1 on paper) |
| accent | #2C3E8F | carbon blue — primary action, kickers, step numbers, focus ring |
| accent-ink | #F4F1E8 | text on accent (8.48:1) |
| stamp | #A8322A | rubber-stamp red — overdue and form errors only |
| carbon | rgb(44 62 143 / .28) | the carbon-duplicate shadow |

- Voice: IBM Plex Sans Condensed 600 · Reading: IBM Plex Sans 400/600 · Data: IBM Plex Mono 500 (self-hosted WOFF2, OFL)
- Type steps: --step--1 … --step-4 (fluid, clamp)
- Spacing: --s-1 … --s-8 (4, 8, 12, 16, 24, 40, 64, 104 px)
- Shape: square containers; controls 2px
- Depth: flat + hairline rules + one tone step (copy). No shadows except the carbon duplicate.
- Motion: base 200ms, fast 120ms, ease-settle cubic-bezier(.2,.7,.2,1); the overdue stamp lands once. Reduced motion: none.

## Signature move
**The carbon duplicate** — a faint offset blue copy behind key figures
(`.carbon`). Used on: the specimen total, the step numbers. Never on body
text, buttons or headings.

## Do
- Show money as the core object: names, amounts in DJF, how long it's been open.
- Use mono + tabular figures for every amount.
- Keep copy polite and concrete; credit is a relationship.

## Don't
- No gradients, glass, blobs, glow, emoji, sparkles.
- No invented proof (user counts, uptime, logos, testimonials, pricing).
- No dark theme for marketing pages; no stock photos.
- No literals in component rules — tokens only.
