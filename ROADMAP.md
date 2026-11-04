# Roadmap

Priorities are set by evidence: what the benchmark and issue reports show matters most.

## Next (1.1)
- [ ] Publish the first benchmark run (≥3 runs per arm per scenario, blind rubric scores, losses included).
- [ ] `page_check.py --routes` to crawl internal links and check every page in one run.
- [ ] Interactive checks in `page_check.py`: open/close disclosure widgets via keyboard, submit forms empty.
- [ ] Optional axe-core integration when `@axe-core/cli` is available.
- [ ] Scanner: Vue/Svelte-specific handler patterns; CSS-in-JS (styled-components, emotion) color literals.

## Later
- [ ] Lighthouse CI recipe and budget file template.
- [ ] Direction-family worked examples contributed from more domains (health, public sector, education, music).
- [ ] RTL-specific checks in `page_check.py` (mirrored icons, logical properties).
- [ ] Claude Code plugin packaging (marketplace install).
- [ ] Localised references (French, Arabic, Spanish).

## Not planned
- A style catalogue of ready-made themes — it would recreate the averaging problem this skill exists to fix.
- Automatic "beauty scores" from screenshots — we score with evidence and humans, not vibes.
