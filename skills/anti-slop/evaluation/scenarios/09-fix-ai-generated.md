# Scenario 09-fix-ai-generated

- **Workflow under test:** `workflows/fix-ai-generated.md`
- **Seed project:** `seeds/generic-landing` (copied into the run directory before the prompt)

## Prompt
```
This landing page looks AI-generated. Fix it.
```

## Expected results
- Identity category ≥ 90, zero critical findings
- Function category 100
- Invented proof removed and listed for the user
- DESIGN.md created and agent rule added
- Passes sibling test as written in the brief

## Failure cases (any one = scenario fails)
- Replacing purple with another trend (neon, beige+serif) without evidence
- Keeping hero + 3 cards with new colors
- Dead links remain

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
