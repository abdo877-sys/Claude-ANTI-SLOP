# Quality gate — before calling the work done

Run all four layers. Record results in `templates/quality-report.md` format.

## Layer 1 — static scan
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slop_scan.py . --compare .anti-slop/before.json
```
Pass: overall ≥ 90 (new builds) or ≥ +25 vs before (existing code), **zero
critical**, function = 100, accessibility ≥ 90. Any remaining finding is
either fixed or justified in one sentence (e.g. "3-column grid kept: pricing has exactly three plans").

## Layer 2 — rendered page
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/page_check.py <url> --out .anti-slop/after
```
Pass: no horizontal overflow at any viewport, no broken images, no console
errors, no low-contrast text, every focus stop visibly focused, dominant font
is not a stock default. If no browser is available: write "Layer 2 not run" in the report.

## Layer 3 — functionality
Complete `checklists/functionality.md`. Pass: every item checked or listed as a known gap.

## Layer 4 — rubric
Score `evaluation/rubric.md`. Pass: no dimension below 3; Originality and
Functionality at 3+; total ≥ 36/44.

## Redesign trigger
If **Originality < 3** or the blur test fails, do not polish — go back to the
direction step. Decorating a template doesn't make it not a template.

## Honesty line (always include in the final report)
"Verified: <layers run, routes, viewports>. Not verified: <what and why>."
