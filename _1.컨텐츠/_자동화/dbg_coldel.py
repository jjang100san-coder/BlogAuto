# -*- coding: utf-8 -*-
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame
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
    print("삽입 직후:", dims(fr))

    # 3열째 셀 클릭 후 나타나는 셀 메뉴 버튼 조사
    t = fr.locator("table").last
    t.locator("td").nth(2).click(); time.sleep(1)
    info = fr.evaluate("""() => Array.from(document.querySelectorAll('.se-cell-context-menu-button, [class*=context-menu-button]'))
        .map(b=>({cls:(b.className||'').slice(0,70),
                  tip:(b.querySelector('[class*=tooltip]')||{}).innerText||'',
                  tx:(b.innerText||'').trim().slice(0,20),
                  vis:b.offsetParent!==null}))""")
    print("\n--- 셀 컨텍스트 메뉴 버튼 ---")
    for b in info:
        print("  vis=%-5s tip=%-14s tx=%-12s %s" % (b['vis'], b['tip'].replace('\n',' ')[:14], b['tx'].replace('\n',' '), b['cls']))

    # 열 선택 버튼(상단 se-cell-select-button) 조사
    sel = fr.locator(".se-cell-select-button")
    print("\nse-cell-select-button 개수:", sel.count())
    boxes=[]
    for i in range(sel.count()):
        b = sel.nth(i).bounding_box()
        if b: boxes.append((i, round(b['x']), round(b['y'])))
    print("  좌표:", boxes)
    page.screenshot(path=os.path.join(BASE,"colmenu.png"))
    ctx.close()
