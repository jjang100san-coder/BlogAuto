# -*- coding: utf-8 -*-
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame
BASE = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=os.path.join(BASE,"chrome_profile"), channel="chrome",
        headless=False, args=["--disable-blink-features=AutomationControlled"],
        viewport={"width":1400,"height":950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/baiyan_novembre?Redirect=Write",
              wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page)
    fr.locator(".se-content").click()
    time.sleep(1)
    fr.locator("button.se-table-toolbar-button").first.click()
    time.sleep(2)
    print("--- 표 패널 구조 ---")
    html = fr.evaluate("""() => {
        const el = document.querySelector('[class*=table-layer], [class*=table-panel], .se-table-create-layer, [class*=se-table]');
        return el ? el.outerHTML.slice(0, 2500) : 'NOT FOUND';
    }""")
    print(html[:2500])
    print("\n--- 셀 후보 개수 ---")
    for sel in ["[class*=table-create] td","[class*=table] td","[class*=grid] td",
                "td[data-row]","[class*=cell]","button[class*=table]"]:
        try: print("  %-28s %d" % (sel, fr.locator(sel).count()))
        except Exception: pass
    page.screenshot(path=os.path.join(BASE,"table_panel.png"))
    ctx.close()
