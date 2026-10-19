# -*- coding: utf-8 -*-
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
BASE = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=os.path.join(BASE,"chrome_profile"), channel="chrome",
        headless=False, args=["--disable-blink-features=AutomationControlled"],
        viewport={"width":1400,"height":950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/baiyan_novembre?Redirect=Write",
              wait_until="domcontentloaded", timeout=45000)
    for t in (3, 8, 15):
        time.sleep(t if t==3 else t-3)
        print("\n=== %ds 경과 : 프레임 %d개 ===" % (t, len(page.frames)))
        for i, f in enumerate(page.frames):
            print("  [%d] name=%r" % (i, f.name))
            print("      url=%s" % f.url[:110])
            for sel in (".se-documentTitle", ".se-content", "button"):
                try: print("      %-18s %d" % (sel, f.locator(sel).count()), end="")
                except Exception as e: print("      %-18s ERR" % sel, end="")
            print()
    ctx.close()
