# -*- coding: utf-8 -*-
import sys, os
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
    print("frame: OK\n")
    rows = fr.evaluate("""() => Array.from(document.querySelectorAll('button')).map(b => ({
        cls: b.className || '', dn: b.getAttribute('data-name') || '',
        al: b.getAttribute('aria-label') || '', tx: (b.innerText||'').trim().slice(0,18)
    }))""")
    print("--- 버튼 %d개 ---" % len(rows))
    for r in rows:
        if r['tx'] or r['al'] or r['dn']:
            print("  %-12s | dn=%-15s | al=%-14s | %s" % (r['tx'], r['dn'], r['al'], r['cls'][:44]))
    print("\n--- 요소 개수 ---")
    for sel in [".se-documentTitle", ".se-content", ".se-text-paragraph", "input[type=file]"]:
        print("  %-22s %d" % (sel, fr.locator(sel).count()))
    ctx.close()
