# Workflow — fix a generic AI-generated design

The signature workflow of this skill. The site looks like every other
AI-built site; make it look like *this* product, without breaking anything.

## 1. Measure the slop
```bash
mkdir -p .anti-slop
python3 ${CLAUDE_SKILL_DIR}/scripts/slop_scan.py . --json > .anti-slop/before.json
python3 ${CLAUDE_SKILL_DIR}/scripts/slop_scan.py .
python3 ${CLAUDE_SKILL_DIR}/scripts/page_check.py <url> --out .anti-slop/before   # if it runs
```
Read the `ai-tells.md` entries for rules that fired. List the visual tells
you see in the screenshots.

## 2. Find what's actually specific
Generic sites usually hide the real product under template copy. Dig: what's
in the data models, the real feature names, the user's own words in issues or
docs? Rewrite the one-sentence positioning concretely before any visual work.

## 3. Direction
Full creative-direction process. The divergence check is strict here: the new
direction may match the default look on **at most two** axes, and it must
pass the sibling test.

## 4. Replace, in this order
1. **Copy:** hero, section titles, CTAs — concrete, specific, true. Remove
   invented proof (fake logos, invented user counts) unless the user confirms.
2. **Tokens:** new palette/type/shape/depth/motion; remap the framework theme
   (Tailwind config, shadcn CSS variables).
3. **Delete decoration:** gradients, blobs, glow, glass, sparkles, floating shapes, emoji icons.
4. **Recompose the template sections** with `layout.md` § moves:
   hero → statement+proof/specimen; 3 cards → lead+list/sequence/ledger rows;
   logo wall/testimonials → real or removed; pricing cards → comparison table.
5. **Signature move** in 3–5 places.
6. **Make it work:** dead links → real targets; no-op buttons → real behavior or
   removed; forms → wired with states.
7. **States and responsive recomposition.**

## 5. Verify
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slop_scan.py . --compare .anti-slop/before.json --md .anti-slop/scan.md
python3 ${CLAUDE_SKILL_DIR}/scripts/page_check.py <url> --out .anti-slop/after
```
Then `checklists/quality-gate.md`. Put before/after screenshots side by side
and run the blur test on both.

## Quality checks
- [ ] Identity category ≥ 90; zero critical findings
- [ ] Function category 100 (no dead/fake UI)
- [ ] ≤2 axes match the default look; sibling test written in the brief
- [ ] Every removed claim/asset listed for the user
- [ ] DESIGN.md + agent rule line in place so it doesn't regress
