# -*- coding: utf-8 -*-
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup
BASE = os.path.dirname(os.path.abspath(__file__))

def dims(fr):
    t = fr.locator("table").last
    return t.locator("tr").count(), t.locator("tr").first.locator("td,th").count()

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
    fr.locator("button.se-table-toolbar-button").first.click(); time.sleep(2)
    print("삽입 직후 (행,열):", dims(fr))

    t = fr.locator("table").last
    t.locator("td").last.click(); time.sleep(0.6)
    page.keyboard.press("Tab"); time.sleep(1.5)
    print("마지막셀 Tab 후  :", dims(fr))

    print("\n--- 표 선택 상태에서 나타난 버튼 ---")
    btns = fr.evaluate("""() => Array.from(document.querySelectorAll('button'))
      .filter(b=>b.offsetParent!==null)
      .map(b=>({dn:b.getAttribute('data-name')||'', tt:(b.querySelector('.se-toolbar-tooltip')||{}).innerText||'',
                cls:(b.className||'').slice(0,55)}))
      .filter(o=>/table|row|col|cell/i.test(o.dn+o.cls) || /행|열|셀|표/.test(o.tt))""")
    for b in btns: print("  tip=%-16s dn=%-22s %s" % (b['tt'][:16].replace('\n',' '), b['dn'], b['cls']))

    print("\n--- 표 위 ⊕ 핸들(a/span/div) ---")
    h = fr.evaluate("""() => {
      const out=new Set();
      document.querySelectorAll('div,span,a,button').forEach(e=>{
        const c=typeof e.className==='string'?e.className:'';
        if(/se-(cell|table|row|col).*(add|insert|plus|handle)|(add|insert).*(row|col)/i.test(c) && e.offsetParent!==null)
          out.add(e.tagName+'.'+c.slice(0,65));});
      return [...out].slice(0,20);}""")
    for s in h: print("  ", s)
    page.screenshot(path=os.path.join(BASE,"table_dbg2.png"))
    ctx.close()
