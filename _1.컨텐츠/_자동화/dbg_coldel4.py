# -*- coding: utf-8 -*-
"""열 선택('N열 선택' 버튼) → 삭제 버튼 실제 클릭 시도."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup

BASE = os.path.dirname(os.path.abspath(__file__))
def log(m): print(m); sys.stdout.flush()

def dims(fr):
    t = fr.locator("table").last
    return t.locator("tr").count(), t.locator("tr").first.locator("td,th").count()

def cells(fr):
    return fr.locator("table").last.inner_text().replace("\n", "|")[:60]

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
    log("삽입 직후 dims=%s  내용=%s" % (dims(fr), cells(fr)))

    # 마지막 열(=2열) 선택 버튼을 텍스트로 정확히 집는다
    last = dims(fr)[1] - 1
    btn = fr.locator(".se-cell-select-button").filter(has_text="%d열 선택" % last)
    log("'%d열 선택' 버튼 %d개" % (last, btn.count()))
    t.locator("td").nth(last).hover(); time.sleep(0.5)     # 핸들 활성화
    btn.first.click(); time.sleep(1.2)
    log("열 선택 후 dims=%s" % (dims(fr),))
    page.screenshot(path=os.path.join(BASE, "cd4_1_selected.png"))

    dele = fr.locator(".se-context-menu-button-delete")
    log("삭제 버튼 %d개 / 보임=%s" % (dele.count(), dele.first.is_visible() if dele.count() else "-"))
    if dele.count():
        dele.first.click(); time.sleep(1.5)                # 실제 클릭
    log("삭제 후 dims=%s  내용=%s" % (dims(fr), cells(fr)))
    page.screenshot(path=os.path.join(BASE, "cd4_2_deleted.png"))
    log("\n테스트 끝. 창 닫으면 종료.")
    while not page.is_closed(): time.sleep(2)
