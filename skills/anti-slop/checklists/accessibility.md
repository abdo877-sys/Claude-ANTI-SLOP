# Accessibility checklist (WCAG 2.2 AA baseline)

## Structure
- [ ] `lang` on `<html>`; `dir="rtl"` for RTL locales
- [ ] Landmarks: header, nav, main (with id for skip link), footer
- [ ] One `h1`; headings in order; no heading used just for size
- [ ] Skip link is the first focusable element and works

## Keyboard
- [ ] Everything interactive reachable and operable with keyboard only
- [ ] Focus order follows visual order; no positive `tabindex`
- [ ] `:focus-visible` style clearly visible (≥3:1 against adjacent colors), never removed
- [ ] No keyboard traps; modals trap intentionally and release on close
- [ ] Focus not obscured by sticky headers (`scroll-margin-top`)

## Semantics
- [ ] Buttons are `<button>`, links are `<a href>`; no clickable divs
- [ ] Icon-only controls have accessible names
- [ ] Form fields have visible labels; errors linked with `aria-describedby`
- [ ] Images: meaningful `alt`, or `alt=""` for decoration; SVG icons `aria-hidden` when decorative
- [ ] Dynamic updates announced (`aria-live="polite"`) for toasts, validation summaries, async results

## Visual
- [ ] Text contrast ≥ 4.5:1 (≥3:1 large); UI component contrast ≥ 3:1
- [ ] Information not conveyed by color alone
- [ ] Text resizes to 200% without loss; layout reflows at 320px without horizontal scroll
- [ ] Pinch-zoom not disabled
- [ ] Touch targets ≥ 44×44 (WCAG minimum 24×24, aim for 44)

## Motion and media
- [ ] `prefers-reduced-motion` respected; no essential info only in animation
- [ ] Nothing flashes > 3 times/second
- [ ] Video has captions when it contains speech; autoplay is muted and pausable

Tools: `page_check.py` covers contrast, focus visibility, alt, targets. For a
deeper pass, run axe (`npx @axe-core/cli <url>`) if available, and report its real output.
