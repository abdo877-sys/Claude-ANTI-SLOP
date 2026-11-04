# Scenario 03-portfolio

- **Workflow under test:** `workflows/portfolio.md`
- **Seed project:** `none` (empty directory)

## Prompt
```
Build a portfolio site for Amina, a documentary photographer working in the Horn of Africa. She has 6 photo series. Use placeholder image files I will replace (put them in /public/series/...). Editors and NGOs hire her.
```

## Expected results
- Work visible in first viewport on mobile and desktop
- Series pages vary in layout to suit the photographs
- Image pipeline responsive with width/height; no stock image URLs
- Contact path works

## Failure cases (any one = scenario fails)
- Hero portrait + 'Hi, I'm Amina' + skill bars
- Unsplash/picsum URLs
- Every series page identical template

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
