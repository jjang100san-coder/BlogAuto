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

    adds = fr.locator(".se-cell-add-button")
    boxes = []
    for i in range(adds.count()):
        b = adds.nth(i).bounding_box()
        if b: boxes.append((i, round(b['x']), round(b['y']), round(b['width']), round(b['height'])))
    print("\n⊕ 버튼 좌표 (idx, x, y, w, h):")
    for b in boxes: print("   ", b)

    # 세로로 길게 늘어선 것(같은 x, y가 다름) = 행 추가 후보 → x 최소 그룹
    minx = min(b[1] for b in boxes)
    row_btns = sorted([b for b in boxes if abs(b[1]-minx) < 12], key=lambda b: b[2])
    col_btns = sorted([b for b in boxes if abs(b[1]-minx) >= 12], key=lambda b: b[1])
    print("\n행 추가 후보(왼쪽 세로줄): idx", [b[0] for b in row_btns])
    print("열 추가 후보(위쪽 가로줄): idx", [b[0] for b in col_btns])

    if row_btns:
        tgt = row_btns[-1][0]                       # 가장 아래
        print("\n→ idx %d 클릭 (맨 아래 행 추가 시도)" % tgt)
        adds.nth(tgt).click(); time.sleep(1.5)
        print("   결과:", dims(fr))
        adds2 = fr.locator(".se-cell-add-button")
        bs = sorted([(i, adds2.nth(i).bounding_box()) for i in range(adds2.count())
                     if adds2.nth(i).bounding_box()], key=lambda t: t[1]['y'])
        cand = [t for t in bs if abs(t[1]['x']-minx) < 12]
        if cand:
            print("→ 재조회 후 맨 아래 idx %d 클릭" % cand[-1][0])
            adds2.nth(cand[-1][0]).click(); time.sleep(1.5)
            print("   결과:", dims(fr))
    page.screenshot(path=os.path.join(BASE,"table_dbg3.png"))
    ctx.close()
