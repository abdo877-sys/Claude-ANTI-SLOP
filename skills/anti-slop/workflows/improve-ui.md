# Workflow — improve an existing UI (no full redesign)

The user wants it better, not different. Keep the direction (or the implicit
one); raise the craft.

## 1. Baseline
`slop_scan.py` + `page_check.py` on the affected screens. Screenshot before.

## 2. Find the highest-leverage fixes (in this order)
1. **Broken things** — dead links, no-op buttons, overflow, console errors.
2. **Accessibility** — focus, contrast, labels, keyboard traps.
3. **Hierarchy** — one focal point per screen; demote competing elements.
4. **Consistency** — collapse near-duplicate values into tokens
   (e.g. 7 greys → 3 roles, 5 radii → 1 philosophy).
5. **Spacing rhythm** — one scale; grouping by proximity.
6. **Typography** — fewer sizes, more contrast, proper measure and line-height.
7. **States** — add empty/loading/error where missing.
8. **Details** — hover/focus/pressed states, transitions via tokens.

## 3. Implement in small, reviewable steps
One category per commit/change set. Don't touch layout structure unless a
hierarchy problem requires it. If you find the identity itself is generic,
tell the user and suggest `workflows/fix-ai-generated.md` instead of silently expanding scope.

## Quality checks
- [ ] Zero new scan findings; function/accessibility categories improved
- [ ] Before/after screenshots show clearer hierarchy
- [ ] No behavior change except fixes the user can see listed in the report
