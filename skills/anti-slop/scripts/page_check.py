#!/usr/bin/env python3
"""
page_check.py — audit a RENDERED page in a real browser (Playwright/Chromium).

What it measures, per viewport (mobile 390, tablet 820, desktop 1440):
  * horizontal overflow and the elements causing it
  * tap targets smaller than 44x44 CSS px (mobile)
  * broken images (naturalWidth == 0) and images without alt
  * links that go nowhere (href="#", "", javascript:)
  * buttons that are not disabled but have no form/handler hint
  * keyboard: tabs through the first N focusables and checks a visible focus style
  * console errors and failed requests
  * the fonts and colors actually rendered (to catch Inter / stock indigo at runtime)
  * text contrast of visible text nodes vs their effective background (WCAG AA)
and saves full-page screenshots.

Usage:
    python3 page_check.py http://localhost:3000            # report
    python3 page_check.py ./dist/index.html --out shots/   # local file
    python3 page_check.py URL --json > page.json

Requires:  pip install playwright && python3 -m playwright install chromium
It never claims more than it measured: if a check cannot run, it says so.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VIEWPORTS = {"mobile": (390, 844), "tablet": (820, 1180), "desktop": (1440, 900)}
STOCK_FONTS = {"inter", "poppins", "roboto", "montserrat", "open sans", "arial", "helvetica"}
STOCK_RGB = {  # Tailwind indigo/violet/purple/blue 500-700 and Material purple
    (99, 102, 241), (79, 70, 229), (67, 56, 202), (139, 92, 246), (124, 58, 237), (109, 40, 217),
    (168, 85, 247), (147, 51, 234), (59, 130, 246), (37, 99, 235), (29, 78, 216), (98, 0, 238),
}

PROBE_JS = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const out = {overflow: [], smallTargets: [], brokenImages: [], imgNoAlt: 0, deadLinks: [],
               suspectButtons: [], fonts: {}, colors: {}, lowContrast: [], scrollWidth: document.documentElement.scrollWidth, vw};
  const visible = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const label = el => (el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '')).slice(0, 80);
  for (const el of document.body.querySelectorAll('*')) {
    if (!visible(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') out.overflow.push(label(el));
  }
  out.overflow = [...new Set(out.overflow)].slice(0, 12);
  for (const el of document.querySelectorAll('a[href], button, [role=button], input, select, textarea')) {
    if (!visible(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 44 || r.height < 44) {
      const inline = el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.closest('p,li');
      if (!inline) out.smallTargets.push(`${label(el)} ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
  }
  out.smallTargets = out.smallTargets.slice(0, 15);
  for (const img of document.images) {
    if (!img.hasAttribute('alt')) out.imgNoAlt++;
    if (img.complete && img.naturalWidth === 0 && img.src) out.brokenImages.push(img.src.slice(0, 120));
  }
  for (const a of document.querySelectorAll('a')) {
    const h = (a.getAttribute('href') || '').trim();
    if (h === '' || h === '#' || h.startsWith('javascript:')) out.deadLinks.push((a.textContent || label(a)).trim().slice(0, 50));
  }
  for (const b of document.querySelectorAll('button')) {
    if (b.disabled || b.closest('form') || b.getAttribute('aria-controls') || b.getAttribute('aria-expanded') !== null) continue;
    if (!b.onclick && !b.getAttribute('onclick') && !b.dataset.action) out.suspectButtons.push((b.textContent || label(b)).trim().slice(0, 50));
  }
  // fonts and colors actually rendered on text
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).map(Number); return p; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const bgOf = el => { for (let e = el; e; e = e.parentElement) { const p = parse(getComputedStyle(e).backgroundColor);
      if (p && (p.length < 4 || p[3] > 0.9)) return p; } return [255, 255, 255]; };
  let checked = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode; const el = t.parentElement;
    if (!el || !t.textContent.trim() || !visible(el)) continue;
    const s = getComputedStyle(el);
    const fam = s.fontFamily.split(',')[0].replace(/["']/g, '').trim();
    out.fonts[fam] = (out.fonts[fam] || 0) + t.textContent.trim().length;
    const fg = parse(s.color), bg = bgOf(el);
    if (fg) {
      const key = fg.slice(0, 3).join(',');
      out.colors[key] = (out.colors[key] || 0) + 1;
      if (checked < 400 && !getComputedStyle(el).backgroundImage.includes('gradient')) {
        checked++;
        const L1 = lum(fg), L2 = lum(bg); const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
        const size = parseFloat(s.fontSize); const bold = +s.fontWeight >= 700;
        const need = (size >= 24 || (bold && size >= 18.66)) ? 3 : 4.5;
        if (ratio < need) out.lowContrast.push(`${t.textContent.trim().slice(0, 30)} — ${ratio.toFixed(2)}:1 (needs ${need})`);
      }
    }
  }
  for (const el of document.body.querySelectorAll('*')) {
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    const p = parse(cs.backgroundColor);
    if (p && (p.length < 4 || p[3] > 0.5)) { const key = 'bg:' + p.slice(0, 3).join(','); out.colors[key] = (out.colors[key] || 0) + 1; }
    for (const g of (cs.backgroundImage.match(/rgba?\([^)]+\)/g) || [])) {
      const q = parse(g); if (q) { const key = 'bg:' + q.slice(0, 3).join(','); out.colors[key] = (out.colors[key] || 0) + 1; } }
  }
  out.lowContrast = [...new Set(out.lowContrast)].slice(0, 12);
  out.deadLinks = out.deadLinks.slice(0, 12); out.suspectButtons = out.suspectButtons.slice(0, 12);
  return out;
}
"""

FOCUS_JS = r"""
() => { const el = document.activeElement; if (!el || el === document.body) return null;
  const s = getComputedStyle(el);
  const visible = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || (s.boxShadow && s.boxShadow !== 'none');
  return {tag: el.tagName.toLowerCase(), text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40), visible}; }
"""


def run(target: str, out_dir: Path, tabs: int) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"error": "playwright not installed: pip install playwright && python3 -m playwright install chromium"}
    if not target.startswith(("http://", "https://", "file://")):
        p = Path(target).resolve()
        if not p.exists():
            return {"error": f"not found: {target}"}
        target = p.as_uri()
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"target": target, "viewports": {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name, (w, h) in VIEWPORTS.items():
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                      is_mobile=(name == "mobile"), has_touch=(name == "mobile"))
            page = ctx.new_page()
            errors, failed = [], []
            page.on("console", lambda m: errors.append(m.text[:160]) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)[:160]))
            page.on("requestfailed", lambda r: failed.append(r.url[:120]))
            try:
                page.goto(target, wait_until="networkidle", timeout=30000)
            except Exception as e:  # noqa: BLE001
                report["viewports"][name] = {"error": f"could not load: {e}"[:200]}
                ctx.close()
                continue
            page.wait_for_timeout(400)
            data = page.evaluate(PROBE_JS)
            focus = []
            if name == "desktop":
                for _ in range(tabs):
                    page.keyboard.press("Tab")
                    f = page.evaluate(FOCUS_JS)
                    if f:
                        focus.append(f)
            shot = out_dir / f"{name}.png"
            page.screenshot(path=str(shot), full_page=True)
            data.update({"consoleErrors": errors[:10], "failedRequests": failed[:10], "screenshot": str(shot)})
            if focus:
                data["focus"] = {"tabbed": len(focus), "withoutVisibleFocus": [f"{f['tag']} {f['text']}" for f in focus if not f["visible"]][:10]}
            report["viewports"][name] = data
            ctx.close()
        browser.close()
    report["summary"] = summarize(report)
    return report


def summarize(rep: dict) -> dict:
    issues = []
    fonts, colors = {}, {}
    for name, v in rep["viewports"].items():
        if "error" in v:
            issues.append(("critical", f"{name}: {v['error']}"))
            continue
        if v["scrollWidth"] > v["vw"] + 1:
            issues.append(("major", f"{name}: horizontal overflow ({v['scrollWidth']}px > {v['vw']}px) — {', '.join(v['overflow'][:4])}"))
        if name == "mobile" and v["smallTargets"]:
            issues.append(("minor", f"mobile: {len(v['smallTargets'])} tap targets < 44px — e.g. {v['smallTargets'][0]}"))
        if v["brokenImages"]:
            issues.append(("major", f"{name}: {len(v['brokenImages'])} broken images"))
        if v["lowContrast"]:
            issues.append(("major", f"{name}: {len(v['lowContrast'])} low-contrast text nodes — e.g. {v['lowContrast'][0]}"))
        if v["consoleErrors"]:
            issues.append(("major", f"{name}: {len(v['consoleErrors'])} console errors — {v['consoleErrors'][0]}"))
        for k, n in v["fonts"].items():
            fonts[k] = fonts.get(k, 0) + n
        for k, n in v["colors"].items():
            colors[k] = colors.get(k, 0) + n
        if "focus" in v and v["focus"]["withoutVisibleFocus"]:
            issues.append(("major", f"keyboard: {len(v['focus']['withoutVisibleFocus'])}/{v['focus']['tabbed']} focus stops have no visible focus style"))
    d = rep["viewports"].get("desktop", {})
    if d.get("deadLinks"):
        issues.append(("major", f"{len(d['deadLinks'])} dead links — {', '.join(d['deadLinks'][:4])}"))
    if d.get("suspectButtons"):
        issues.append(("minor", f"{len(d['suspectButtons'])} buttons with no visible handler/form (verify by clicking) — {', '.join(d['suspectButtons'][:4])}"))
    if d.get("imgNoAlt"):
        issues.append(("major", f"{d['imgNoAlt']} images without alt"))
    top_font = max(fonts, key=fonts.get) if fonts else None
    if top_font and top_font.lower() in STOCK_FONTS:
        issues.append(("major", f"dominant font-family on visible text is a stock default: {top_font}"))
    stock_hits = sum(n for k, n in colors.items()
                     if tuple(int(x) for x in k.replace("bg:", "").split(",")[:3]) in STOCK_RGB)
    if stock_hits:
        issues.append(("major", f"stock indigo/violet/blue rendered on {stock_hits} elements"))
    return {"issues": [{"severity": s, "message": m} for s, m in issues],
            "fonts_by_characters": dict(sorted(fonts.items(), key=lambda x: -x[1])[:5])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="URL or path to an HTML file")
    ap.add_argument("--out", default=".anti-slop/screens")
    ap.add_argument("--tabs", type=int, default=20, help="how many Tab presses to test")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rep = run(a.target, Path(a.out), a.tabs)
    if "error" in rep:
        print(rep["error"], file=sys.stderr)
        sys.exit(2)
    if a.json:
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return
    print(f"\nANTI-SLOP page check — {rep['target']}")
    print(f"primary font-family on visible text (by characters): {rep['summary']['fonts_by_characters']}")
    for v, d in rep["viewports"].items():
        if "screenshot" in d:
            print(f"screenshot {v}: {d['screenshot']}")
    issues = rep["summary"]["issues"]
    if not issues:
        print("\nNo rendered-page issues detected by the automated checks.")
        print("Now look at the screenshots yourself: hierarchy, rhythm, originality are not measurable here.\n")
        return
    print()
    for i in issues:
        print(f"[{i['severity'][:4].upper()}] {i['message']}")
    print()


if __name__ == "__main__":
    main()
