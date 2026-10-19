# -*- coding: utf-8 -*-
"""겹친 크기조절 핸들의 pointer-events를 끄고 열 선택 → 삭제."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup

BASE = os.path.dirname(os.path.abspath(__file__))
def log(m): print(m); sys.stdout.flush()

OFF = "() => document.querySelectorAll('.se-cell-size-controlbar').forEach(e => e.style.pointerEvents='none')"
ON  = "() => document.querySelectorAll('.se-cell-size-controlbar').forEach(e => e.style.pointerEvents='')"
SELCNT = "() => document.querySelectorAll('td[class*=selected],th[class*=selected],td.se-cell-selected').length"

def dims(fr):
    t = fr.locator("table").last
    return t.locator("tr").count(), t.locator("tr").first.locator("td,th").count()
def cells(fr):
    return fr.locator("table").last.inner_text().replace("\n", "").replace("\t", "|")[:40]

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
    fr.locator("button.se-table-toolbar-button").first.click(); time.sleep(2)

    t = fr.locator("table").last
    for i, txt in enumerate(["A1", "B1", "C1"]):
        t.locator("td").nth(i).click(); time.sleep(0.2); page.keyboard.type(txt, delay=6)
    log("삽입 직후 dims=%s 내용=%s" % (dims(fr), cells(fr)))

    last = dims(fr)[1] - 1
    t.locator("td").nth(last).click(); time.sleep(0.8)
    fr.evaluate(OFF)                                        # 겹친 핸들 통과
    btn = fr.locator(".se-cell-select-button").filter(has_text="%d열 선택" % last)
    btn.first.click(timeout=8000); time.sleep(1.2)
    fr.evaluate(ON)
    log("열 선택 후 dims=%s / 선택된 셀 %s개" % (dims(fr), fr.evaluate(SELCNT)))
    page.screenshot(path=os.path.join(BASE, "cd5_1_selected.png"))

    dele = fr.locator(".se-context-menu-button-delete")
    log("삭제 버튼 %d개 보임=%s" % (dele.count(), dele.first.is_visible() if dele.count() else "-"))
    try:
        dele.first.click(timeout=8000)
    except Exception as e:
        log("실제 클릭 실패(%s) → dispatch_event 시도" % type(e).__name__)
        dele.first.dispatch_event("click")
    time.sleep(1.5)
    log("삭제 후 dims=%s 내용=%s" % (dims(fr), cells(fr)))
    page.screenshot(path=os.path.join(BASE, "cd5_2_deleted.png"))
    log("\n테스트 끝. 창 닫으면 종료.")
    while not page.is_closed(): time.sleep(2)
