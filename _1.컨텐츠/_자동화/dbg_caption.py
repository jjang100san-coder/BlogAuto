# -*- coding: utf-8 -*-
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame
BASE = os.path.dirname(os.path.abspath(__file__))
IMG = r"D:\Base_JBS\개인\네이버 블로그\260906_인왕산_등산글\260906\20260905_163738.jpg"
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=os.path.join(BASE,"chrome_profile"), channel="chrome",
        headless=False, args=["--disable-blink-features=AutomationControlled"],
        viewport={"width":1400,"height":950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/baiyan_novembre?Redirect=Write",
              wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=print)
    fr.locator(".se-content").click(); time.sleep(1)
    with page.expect_file_chooser(timeout=30000) as fc:
        fr.locator("button.se-image-toolbar-button").first.click()
    fc.value.set_files([IMG])
    for _ in range(60):
        time.sleep(1)
        if fr.locator(".se-image, .se-component-image").count(): break
    time.sleep(3)
    print("이미지 컴포넌트:", fr.locator(".se-image, .se-component-image").count())
    info = fr.evaluate("""() => {
        const c = document.querySelector('.se-component.se-image') || document.querySelector('.se-image');
        if(!c) return {err:'no component'};
        const out = [];
        c.querySelectorAll('*').forEach(e=>{
            const cl = typeof e.className==='string'?e.className:'';
            if(/caption|text|placeholder/i.test(cl))
                out.push({tag:e.tagName, cls:cl.slice(0,70),
                          ce:e.getAttribute('contenteditable'),
                          ph:(e.getAttribute('data-placeholder')||e.getAttribute('placeholder')||''),
                          vis:e.offsetParent!==null, tx:(e.innerText||'').trim().slice(0,30)});
        });
        return {n:out.length, items:out.slice(0,18)};
    }""")
    print("\n--- caption/text 후보 ---")
    if 'items' in info:
        for it in info['items']:
            print("  %-6s vis=%-5s ce=%-5s ph=%-22s | %s" % (it['tag'], it['vis'], it['ce'], it['ph'][:22], it['cls'][:50]))
    else: print(info)
    page.screenshot(path=os.path.join(BASE,"caption_dbg.png"))
    ctx.close()
