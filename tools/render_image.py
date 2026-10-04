"""Render an HTML page (element #stage) to PNG.
Usage: python3 tools/render_image.py page.html out.png --w 1080 --h 1350"""
import argparse, os
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("out")
ap.add_argument("--w", type=int, default=1080); ap.add_argument("--h", type=int, default=1350)
a = ap.parse_args()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": a.w, "height": a.h})
    pg.goto("file://" + os.path.abspath(a.html)); pg.wait_for_timeout(1200)
    pg.locator("#stage").screenshot(path=a.out); b.close()
print("ok", a.out)
