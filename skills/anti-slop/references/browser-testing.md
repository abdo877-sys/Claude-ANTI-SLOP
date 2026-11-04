# Rendered-page testing protocol

Static code review misses most real defects. When the page can run, test it
in a real browser. **Only report checks you actually performed.**

## 1. Get it running
Use the project's dev/preview command (`npm run dev`, `pnpm preview`, `vite`,
`next dev`, `astro dev`, `python -m http.server` for static output). Note the URL.

## 2. Automated pass (Playwright — works in any shell)
```bash
pip install playwright && python3 -m playwright install chromium   # once
python3 ${CLAUDE_SKILL_DIR}/scripts/page_check.py http://localhost:3000 --out .anti-slop/screens
```
It renders at 390 / 820 / 1440px and reports: horizontal overflow (with the
culprit elements), tap targets <44px, broken images, missing alt, dead links,
buttons with no visible handler, keyboard focus visibility over 20 Tab stops,
text contrast, console errors, failed requests, and the fonts and colors
actually rendered. It saves full-page screenshots.

Run it per important route (home, a detail page, a form page, an app screen).

## 3. Look at the screenshots (you, not the script)
Open each PNG and judge what tools can't:
- Is there one focal point? Does hierarchy read in under 3 seconds?
- Does the mobile layout *recompose*, or just stack?
- Spacing rhythm, alignment to the grid, orphaned words in headlines.
- Does it pass the blur test (`ai-tells.md`)?
- Does anything still look like a template section?

## 4. Interactive pass
With an interactive browser tool (Claude in Chrome, the built-in browser, or a
Playwright script), actually operate the UI:
- Every nav link and button on the page — does something correct happen?
- Open and close each menu, modal, dropdown with mouse *and* keyboard (Enter, Space, Esc, arrows).
- Submit each form empty, invalid, and valid. Check messages, focus, and that input survives errors.
- Search and filters: results change, empty result state exists, URL reflects state if shareable.
- Resize across breakpoints while a menu is open.
- `prefers-reduced-motion` and dark mode (if supported): emulate and re-check.

Playwright snippet for emulation:
```python
ctx = browser.new_context(reduced_motion="reduce", color_scheme="dark")
```

## 5. Fix → re-run → repeat
Fix every critical and major issue, re-run the automated pass and re-open the
screenshots. Stop when no critical/major issues remain, or explain clearly
which remain and why.

## 6. What to write in the final report
"Rendered at 390/820/1440 with page_check.py on `/`, `/pricing`, `/contact`;
tabbed 20 stops on `/`; submitted the contact form invalid and valid." —
precise and true. If no browser was available, say: "Not visually tested:
no browser in this environment. Static scan only."
