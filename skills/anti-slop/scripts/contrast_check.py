#!/usr/bin/env python3
"""
contrast_check.py — validate a palette against WCAG 2.2 contrast.

Usage:
    python3 contrast_check.py "#1B1A17" "#F4EFE6"            # one pair
    python3 contrast_check.py --pairs palette.json            # many pairs

palette.json format:
    {"pairs": [["ink", "#1B1A17", "paper", "#F4EFE6", "text"],
               ["accent", "#C2410C", "paper", "#F4EFE6", "large"],
               ["accent", "#C2410C", "paper", "#F4EFE6", "ui"]]}
The 5th item is the use: "text" (4.5:1), "large" (3:1), "ui" (3:1).
"""
import argparse
import json
import sys

REQ = {"text": 4.5, "large": 3.0, "ui": 3.0}


def lum(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 8:  # AARRGGBB (Flutter style) -> drop alpha
        h = h[2:]
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def ch(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ratio(a: str, b: str) -> float:
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fg", nargs="?")
    ap.add_argument("bg", nargs="?")
    ap.add_argument("--pairs")
    a = ap.parse_args()

    rows = []
    if a.pairs:
        data = json.load(open(a.pairs, encoding="utf-8"))
        rows = data["pairs"]
    elif a.fg and a.bg:
        rows = [["fg", a.fg, "bg", a.bg, "text"]]
    else:
        ap.error("give FG BG or --pairs file")

    failed = 0
    for fg_name, fg, bg_name, bg, use in rows:
        r = ratio(fg, bg)
        need = REQ.get(use, 4.5)
        ok = r >= need
        failed += not ok
        mark = "PASS" if ok else "FAIL"
        print(f"{mark}  {fg_name:<12} {fg:<9} on {bg_name:<12} {bg:<9} {r:5.2f}:1  (needs {need}:1 for {use})")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
