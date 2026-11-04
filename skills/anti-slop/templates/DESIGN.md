# DESIGN.md — <product>

> Source of truth for UI decisions. Humans and AI agents changing the UI must
> follow this file. Values not defined here must not be introduced.
> Created with ANTI-SLOP; update it when a token changes.

## Direction
<Family> · <material metaphor>. <One sentence: why this fits the product and its users.>

## Tokens (where they live: `<path/to/tokens>`)
| Token | Light | Dark | Use |
|---|---|---|---|
| paper | | | page background |
| surface | | | raised areas, inputs |
| ink | | | primary text |
| ink-muted | | | secondary text (≥4.5:1 on paper) |
| rule | | | borders, dividers |
| accent | | | primary action, key data, focus ring |
| accent-ink | | | text on accent |
| positive / warning / danger | | | states |

- Voice face: <font> · Reading face: <font> · Data face: <font>
- Type scale: <steps> · Measure: <ch>
- Spacing scale: <steps>
- Shape: <philosophy> — container <x>, control <x>, chip <x>
- Depth: <model and exact values>
- Motion: fast <ms>, base <ms>, slow <ms>, curve <…>; reduced-motion: <behavior>

## Signature move
<What it is>. Used in: <places>. Never on: <places>.

## Do
- <specific rules>

## Don't
- No gradients, glass, blobs, glow, emoji icons, gradient text (unless listed above with a reason)
- No centered hero + three feature cards
- No literals in components — tokens only
- <product-specific refusals>
