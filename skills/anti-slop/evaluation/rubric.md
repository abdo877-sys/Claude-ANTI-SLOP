# Scoring rubric — 11 dimensions × 0–4 (max 44)

Score from evidence only: a file:line, a screenshot, a measured value, or an
action you performed. If you can't gather evidence for a dimension, mark it
**N/A — not assessed** and exclude it from the total (report the denominator).

For benchmark comparisons, score **blind**: the scorer must not know which
output was produced with the skill.

| # | Dimension | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|
| 1 | **Visual originality** | Indistinguishable from the default look (≥6 default axes) | A recolored template (4–5 axes) | Some intentional choices, template structure remains (3 axes) | Distinct direction, ≤2 default axes, passes blur test | Unmistakably this product; signature move memorable; passes sibling test |
| 2 | **Design coherence** | Decisions contradict each other | Several unrelated styles mixed | One direction, inconsistently applied | Consistent system; few exceptions | Every element traceable to the brief; refusals respected |
| 3 | **Typography** | Defaults, no hierarchy | Hierarchy weak or too many sizes | Reasonable but generic pairing | Pairing fits direction; clear 3-level hierarchy; good measure | Expressive and legible; fluid scale; numerals/scripts handled |
| 4 | **Layout composition** | Broken or chaotic | Template sections stacked | Some recomposition | Content-ranked, asymmetric where useful, clear focal point per view | Composition itself communicates the product; deliberate grid breaks |
| 5 | **Spacing** | Random | Many near-duplicate values | A scale exists but grouping unclear | Consistent scale; proximity groups content | Rhythm varies intentionally; every large gap frames something |
| 6 | **Color consistency** | Clashing / defaults | Default palette with tweaks | Custom palette, inconsistent roles | Semantic tokens, one accent, contrast passes | Palette from the metaphor; dark mode (if present) is designed, not inverted |
| 7 | **Responsive behavior** | Breaks/overflows on mobile | Stacks with issues | Works but just stacks | Recomposes per breakpoint, no overflow 320–1440 | Each breakpoint feels designed; primary action ideally placed |
| 8 | **Accessibility** | Major barriers (no keyboard, contrast fails widely) | Many issues | Basic semantics, some failures | AA checks pass in tools + keyboard walk | Plus thoughtful details: skip link, live regions, reduced motion, RTL |
| 9 | **Interaction quality** | Dead or fake UI | Many controls without states | Works, generic states | All states designed; meaningful feedback | Interactions express the direction; motion tokens; delightful but restrained |
| 10 | **Performance** | Unusable (huge assets, blocking) | Obvious problems | Acceptable, unoptimised | Images/fonts/code split handled; no CLS issues seen | Measured within budgets (LCP/INP/CLS) |
| 11 | **Code quality** | Unmaintainable | Literals everywhere, duplication | Mixed | Tokens, typed components, matches project conventions | Minimal, idiomatic, DESIGN.md in sync, no unnecessary deps |

## Mapping to automated evidence
| Dimension | Automated signal (supporting, not sufficient) |
|---|---|
| 1, 2, 6 | `slop_scan` identity category; `page_check` rendered fonts/colors |
| 7 | `page_check` overflow per viewport; screenshots |
| 8 | `slop_scan` accessibility category; `page_check` contrast, focus, alt, targets |
| 9 | `slop_scan` function category; `page_check` dead links/suspect buttons; manual clicks |
| 10 | `slop_scan` performance category; Lighthouse if run |
| 11 | `slop_scan` hard-coded values; code review |

## Thresholds
- **Gate (skill output):** no dimension < 3; total ≥ 36/44 (or ≥ 82% of assessed).
- **Redesign trigger:** Originality < 3 or Coherence < 3.
- **Benchmark win:** with-skill total > baseline total on ≥ 8/10 scenarios **and**
  no dimension regresses on average.
