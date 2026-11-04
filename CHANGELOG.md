# Changelog

All notable changes are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: SemVer.

## [1.0.0] — 2026-11-04
### Added
- `SKILL.md` with core principles, mandatory 6-phase workflow and routing to 10 workflows.
- Workflows: new website, redesign, portfolio, SaaS app, e-commerce, agency, dashboard, improve UI, fix AI-generated, audit.
- References: creative direction engine (18 direction families with evidence for/against and failure modes),
  typography, color, layout, motion, components, engineering, research, browser testing, AI tells.
- Checklists: preflight, quality gate, functionality, accessibility, performance.
- `slop_scan.py`: 41 rules in 4 categories (identity, function, accessibility, performance) across web, Flutter, SwiftUI, Compose;
  JSON/Markdown output, before/after comparison, CI gate.
- `page_check.py`: Playwright audit at 390/820/1440 — overflow culprits, tap targets, rendered contrast, focus visibility,
  dead links, console errors, rendered fonts/colors, screenshots.
- `contrast_check.py`: WCAG 2.2 contrast validator.
- Evaluation: 11-dimension rubric, 10 benchmark scenarios, blind A/B harness (`bench/run_benchmark.py`).
- Example: Harbor Ledger before/after run with report and screenshots.
- Tests: positive case for every rule, false-positive guards, CLI tests; structure/link validator; GitHub Actions.
### Fixed during development (found by actually running the workflow)
- Form errors hidden on blur shifted layout under the pointer; rule added to components reference and functionality checklist.
