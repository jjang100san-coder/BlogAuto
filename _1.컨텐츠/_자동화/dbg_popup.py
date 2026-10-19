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
    time.sleep(8)
    el = page.wait_for_selector("iframe#mainFrame", timeout=20000)
    fr = el.content_frame()
    info = fr.evaluate("""() => {
        const ps = document.querySelectorAll('.se-popup, [data-group=popupLayer]');
        return Array.from(ps).map(pp => ({
            name: pp.getAttribute('data-name')||'',
            vis : pp.offsetParent !== null,
            text: (pp.innerText||'').trim().slice(0,160),
            btns: Array.from(pp.querySelectorAll('button')).map(b=>({
                tx:(b.innerText||'').trim().slice(0,20), cls:(b.className||'').slice(0,60)}))
        }));
    }""")
    for pp in info:
        if not pp['vis']: continue
        print("팝업 name=%s" % pp['name'])
        print("  본문: %s" % pp['text'].replace("\n"," / "))
        for b in pp['btns']:
            print("   버튼 [%s]  %s" % (b['tx'], b['cls']))
        print()
    page.screenshot(path=os.path.join(BASE,"popup_dbg.png"))
    ctx.close()
