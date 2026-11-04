# Workflow — new website from scratch

## 1. Brief (mandatory file)
Copy `templates/creative-brief.md` to `.anti-slop/brief.md` and fill it
(`references/creative-direction.md`). Get the user's answers to ≤3 questions.
Collect real content now: copy, photos, logos, numbers. If none exists, write
honest draft copy from the brief and list what the user must supply.

## 2. Stack
Use what the user asked for. If unspecified: content site → Astro or Next.js
(SSG); app-like → Next.js/React Router/SvelteKit; one page → plain HTML+CSS.
TypeScript strict. No UI kit unless the product needs complex widgets
(then an accessible primitive library: Radix, React Aria, Ark).

## 3. Information architecture
- List pages and, per page, the ranked content (rank 1 = biggest, highest).
- Write the primary action per page. Each page has exactly one.
- Sketch sections as text first: `[statement+proof] [how it works: numbered] [one real quote] [closing CTA]`.
  Reject any section that exists only because "landing pages have one".

## 4. Tokens + DESIGN.md
Implement tokens (type scale, palette, spacing, radius, depth, motion) in the
stack's native mechanism. Write `DESIGN.md` from `templates/DESIGN.md`.
Add the DESIGN.md rule line to `CLAUDE.md`/`AGENTS.md`.

## 5. Build one screen end to end
The homepage (or the most important screen), desktop and mobile, with real
copy, working links, all states. Show it to the user. Adjust direction now —
it's cheapest here.

## 6. Build the rest
Reuse components; add a component only when a pattern appears twice.
Every route gets: title/meta, OG image, 404 handling, error state.

## 7. Engineering pass
`references/engineering.md`: images, fonts, code splitting, SEO files
(sitemap, robots), JSON-LD where relevant, favicon/manifest.

## Quality checks
- [ ] `slop_scan.py` ≥ 90, zero critical, zero function/accessibility majors
- [ ] `page_check.py` on every route: no overflow, no dead links, focus visible, contrast passes
- [ ] `checklists/functionality.md` complete — every link and button clicked
- [ ] Rubric (`evaluation/rubric.md`) ≥ 3 on every dimension, originality ≥ 3
- [ ] Blur test passes; sibling test passes
- [ ] Final report lists what content is still placeholder and needs the user
