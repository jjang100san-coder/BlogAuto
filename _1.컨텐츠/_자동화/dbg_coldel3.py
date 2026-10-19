# -*- coding: utf-8 -*-
"""표 열 삭제 경로 탐색: 셀 클릭 / 열 선택 각 상태에서 보이는 버튼 전수 조사."""
import sys, os, time, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup

BASE = os.path.dirname(os.path.abspath(__file__))
def log(m): print(m); sys.stdout.flush()

# 프레임 안에서 "보이는" 버튼을 전부 긁는다
BTNS = """() => [...document.querySelectorAll('button,[role=button]')]
  .filter(b => b.offsetParent !== null)
  .map(b => ({cls:(b.className||'').toString().slice(0,60),
              name:b.getAttribute('data-name')||'',
              lbl:(b.getAttribute('aria-label')||'').slice(0,20),
              tx:(b.innerText||'').replace(/\s+/g,' ').trim().slice(0,16)}))"""

def dims(fr):
    t = fr.locator("table").last
    return t.locator("tr").count(), t.locator("tr").first.locator("td,th").count()

def dump(fr, tag, base=None):
    cur = fr.evaluate(BTNS)
    key = lambda b: (b['cls'], b['name'], b['lbl'], b['tx'])
    if base is not None:
        old = {key(b) for b in base}
        cur = [b for b in cur if key(b) not in old]
        log("\n--- %s (새로 나타난 것만 %d개) ---" % (tag, len(cur)))
    else:
        log("\n--- %s (%d개) ---" % (tag, len(cur)))
    for b in cur:
        log("   " + json.dumps(b, ensure_ascii=False))
    return cur

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=os.path.join(BASE, "chrome_profile"), channel="chrome",
        headless=False, args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/baiyan_novembre?Redirect=Write",
              wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=log)
    dismiss_restore_popup(fr)
    fr.locator(".se-content").click(); time.sleep(1)

    base = fr.evaluate(BTNS)                       # 표 없는 기본 상태
    fr.locator("button.se-table-toolbar-button").first.click(); time.sleep(2)
    log("표 삽입 직후 dims=%s" % (dims(fr),))
    t = fr.locator("table").last
    for i, txt in enumerate(["A1", "B1", "C1"]):
        t.locator("td").nth(i).click(); time.sleep(0.2); page.keyboard.type(txt, delay=6)

    t.locator("td").nth(2).click(); time.sleep(1.0)
    after_cell = dump(fr, "3번째 셀 클릭 상태", base)
    page.screenshot(path=os.path.join(BASE, "cd3_1_cell.png"))

    # 열 선택 핸들 좌표 파악
    sel = fr.locator(".se-cell-select-button")
    items = [(i, sel.nth(i).bounding_box()) for i in range(sel.count())]
    items = [(i, b) for i, b in items if b]
    log("\nse-cell-select-button %d개: %s" % (len(items),
        [(i, round(b['x']), round(b['y'])) for i, b in items]))
    if items:
        miny = min(b['y'] for _, b in items)
        cols = sorted([x for x in items if abs(x[1]['y'] - miny) <= 3], key=lambda x: x[1]['x'])
        log("열 선택 핸들(위쪽 가로줄) idx=%s" % [c[0] for c in cols])
        if cols:
            sel.nth(cols[-1][0]).click(force=True); time.sleep(1.2)
            log("맨오른쪽 열 선택 후 dims=%s" % (dims(fr),))
            dump(fr, "열 선택 상태", after_cell)
            page.screenshot(path=os.path.join(BASE, "cd3_2_colsel.png"))
    log("\n조사 끝. 창 닫으면 종료.")
    while not page.is_closed(): time.sleep(2)
