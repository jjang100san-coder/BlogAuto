# -*- coding: utf-8 -*-
"""아티팩트 HTML의 그림(figure)들을 블로그용 PNG로 뽑는다. 2배 해상도, 밝은 테마."""
import os, sys, pathlib
from playwright.sync_api import sync_playwright

HTML = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1100, "height": 900}, device_scale_factor=2, color_scheme="light")
    pg.goto(HTML.as_uri())
    pg.wait_for_timeout(2500)          # 구글 폰트 로드
    pg.evaluate("document.fonts && document.fonts.ready")
    pg.wait_for_timeout(800)
    figs = pg.locator("figure")
    n = figs.count()
    labels = [pg.locator("figure svg").nth(i).get_attribute("aria-label") or ("fig%02d" % (i+1)) for i in range(n)]
    for i in range(n):
        fig = figs.nth(i)
        fig.scroll_into_view_if_needed()
        safe = "".join(c for c in labels[i] if c not in '\\/:*?"<>|').strip()[:28]
        path = OUT / ("%02d_%s.png" % (i + 1, safe))
        fig.screenshot(path=str(path))
        print("saved", path.name)
    b.close()
print("total", n)
