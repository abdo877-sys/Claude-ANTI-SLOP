# Layout and composition

## 1. Start from content priority, not sections
List what the page must communicate, ranked. Rank 1 gets the most space and
the strongest position. A layout is a ranking made visible. If you can't rank,
you don't understand the page yet.

## 2. Grids
- **12-column** for marketing/editorial (flexible spans: 7/5, 8/4, 5/7 — avoid 4/4/4).
- **Modular** grids (repeating module height) for catalogs and dashboards.
- **Editorial** grids: a narrow text column + wide media column + margin column for notes.
- Use CSS Grid with named lines; `minmax()` and `clamp()` for fluid gutters:
```css
.page { display: grid; grid-template-columns:
  [full-start] minmax(1rem, 1fr) [content-start] minmax(0, 72rem) [content-end] minmax(1rem, 1fr) [full-end]; }
.page > * { grid-column: content; }
.page > .bleed { grid-column: full; }
```

## 3. Asymmetry and tension
- Prefer unequal splits (5/7, 3/9) over halves.
- Anchor one element off-center per view; let one element break the grid
  (bleed, overlap, hang into the margin) once per page, on purpose.
- Vary density: a spacious statement next to a dense data block.

## 4. Spacing system
One scale, used everywhere, e.g. `4 8 12 16 24 32 48 72 112` (px or rem).
Proximity encodes grouping: space *within* a group < space *between* groups,
by at least 1.5–2×. If everything has the same gap, nothing is grouped.

## 5. Layout moves (replacements for template sections)

| Template | Replace with (choose by content) |
|---|---|
| Centered hero + gradient + 2 buttons | **Statement + proof** (left-aligned headline, the real product or real numbers beside it) · **Specimen hero** (the core object at full size, headline annotates it) · **Question hero** (headline is the user's question, the next block answers it) |
| 3 feature cards with icons | **Lead + list** (one feature large with real visual, others as a ruled two-column list) · **Numbered sequence** (if features are steps) · **Ledger rows** (name / description / concrete figure) · **Before/after** pairs |
| Logo wall "Trusted by" | Only with real, permitted logos. Otherwise a single concrete quote or a metric the user supplied. |
| Testimonial carousel | One large real quote, or a dense wall of short quotes. None if none exist. |
| Pricing: 3 identical cards | Comparison table with the recommended plan emphasized by position and one accent, not a gradient border |
| Uniform card grid | Mixed sizes by importance; rows + rules where items are compared |
| Footer with 5 link columns | Only the links that exist; one line of real contact; maybe a closing statement |
| Mobile: everything stacked | Re-rank for mobile: primary action within thumb reach, secondary content collapsed with real disclosure |

## 6. Responsive composition
- Design mobile first for apps; for content sites design the hardest
  breakpoint first (often mobile), then let it grow.
- Recompose, don't just stack: change order, spans and density per breakpoint.
- Container queries (`@container`) for components that live in different widths.
- Test 320, 390, 768, 1024, 1440 and one ultra-wide; nothing scrolls sideways.

## 7. Whitespace is intentional
Whitespace is earned by hierarchy. Huge empty space around a weak headline is
not minimalism, it's an absence. Every large gap should frame something important.
