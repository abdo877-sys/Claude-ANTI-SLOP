# Color

## 1. Source the palette from the metaphor
Don't pick from a color wheel or a Tailwind swatch. Name the materials of the
metaphor and sample their colors: *receipt paper, carbon ink, rubber-stamp red*;
*rack black, LED green, amber warning*; *vellum, iron-gall ink, lapis*.

## 2. Roles (semantic tokens)
| Token | Role |
|---|---|
| `--paper` | page background |
| `--surface` / `--surface-2` | raised areas, inputs, sections (tone steps from paper) |
| `--ink` | primary text |
| `--ink-muted` | secondary text — must still pass 4.5:1 on paper |
| `--rule` | borders, dividers |
| `--accent` | THE signature color: primary actions, key data, focus ring |
| `--accent-ink` | text/icons on accent |
| `--positive` `--warning` `--danger` `--info` | states — tuned to the palette's temperature |

Rules:
- **One** saturated accent. Everything else is tinted neutral (neutrals carry
  the paper's temperature; never pure `#808080`).
- The accent is never a framework default at 500/600 (indigo, violet, blue,
  purple). Move it ≥8° in hue or ≥10% in chroma/lightness from the nearest default.
- State colors live in the same world: a ledger's red is brick, not `#EF4444`.
- Accent covers ≤10% of any screen. Rarity makes it work.

## 3. Use OKLCH for tokens where supported
OKLCH gives perceptually even lightness steps, which makes tone ramps and dark
mode predictable:
```css
:root {
  --paper: oklch(96% 0.015 85);  --surface: oklch(93% 0.018 85);
  --ink: oklch(22% 0.015 70);    --ink-muted: oklch(45% 0.02 70);
  --rule: oklch(86% 0.02 80);    --accent: oklch(55% 0.16 40);
  --accent-ink: oklch(98% 0.01 80);
}
```
Provide hex fallbacks if the project targets browsers without OKLCH.

## 4. Contrast
- Body text ≥ 4.5:1, large text (≥24px or ≥18.66px bold) ≥ 3:1,
  UI boundaries and focus indicators ≥ 3:1 against adjacent colors.
- Check every text/background pair you defined:
  `python3 ${CLAUDE_SKILL_DIR}/scripts/contrast_check.py --pairs palette.json`
- Never put text on photos without a solid or scrim layer that guarantees contrast.

## 5. Dark mode is a different material
Not an inversion. Decide what the metaphor looks like at night: paper becomes
deep warm black (not `#000`), ink becomes warm off-white (not `#FFF`), the
accent loses ~10% chroma and gains lightness to keep contrast. Surfaces get
*lighter* as they rise. Ship dark mode only if the brief justifies it or the
product is used at night; a half-made dark mode is worse than none.

```css
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { /* … */ } }
:root[data-theme="dark"] { /* same values, for the manual toggle */ }
```

## 6. Color carries meaning, not decoration
Use color to encode: state, category, selection, priority. If removing a color
removes no information, it was decoration — consider removing it.
Never encode meaning by color alone: pair with text, icon or pattern.
