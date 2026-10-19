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

    # 셀에 표식 입력 (삭제 후 남은 데이터 확인용)
    t = fr.locator("table").last
    for i, txt in enumerate(["A1","B1","C1"]):
        t.locator("td").nth(i).click(); time.sleep(0.2); page.keyboard.type(txt, delay=6)

    # 맨 오른쪽 열 선택 → 삭제
    sel = fr.locator(".se-cell-select-button")
    items = [(i, sel.nth(i).bounding_box()) for i in range(sel.count())]
    items = [(i, b) for i, b in items if b]
    minx = min(b['x'] for _, b in items)          # 왼쪽 세로줄 = 행 선택
    cols = sorted([x for x in items if abs(x[1]['x'] - minx) > 3], key=lambda x: x[1]['x'])
    rows = sorted([x for x in items if abs(x[1]['x'] - minx) <= 3], key=lambda x: x[1]['y'])
    print("열 선택 idx:", [c[0] for c in cols], " 행 선택 idx:", [r[0] for r in rows])
    sel.nth(cols[-1][0]).click(force=True); time.sleep(1)
    print("열 선택 후 dims:", dims(fr))

    dele = fr.locator(".se-context-menu-button-delete")
    print("삭제 버튼 %d개 — DOM 클릭 시도" % dele.count())
    dele.first.evaluate("b => b.click()")
    time.sleep(1.5)
    print("삭제 후 dims:", dims(fr))
    print("남은 내용:", fr.locator("table").last.inner_text().replace("\n","|")[:40])
    page.screenshot(path=os.path.join(BASE,"coldel_test.png"))
    ctx.close()
