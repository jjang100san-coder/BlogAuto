# -*- coding: utf-8 -*-
"""수정한 do_table 검증: 6편의 4행2열 표를 그대로 넣어본다."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup
import fill_editor as F

BASE = os.path.dirname(os.path.abspath(__file__))
ROWS = [["구간", "걸린 시간"], ["사내 결재와 인감", "영업일 2일"],
        ["보유 상품 매도 결제", "영업일 8일"], ["현금화 완료 후 인출 처리", "영업일 2일"]]
def log(m): print(m); sys.stdout.flush()

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=F.PROFILE, channel="chrome", headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/%s?Redirect=Write" % F.BLOG_ID,
              wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=log)
    dismiss_restore_popup(fr)
    fr.locator(".se-documentTitle").click(); time.sleep(0.6)
    page.keyboard.type("표 열삭제 검증", delay=8)
    fr.locator(".se-content").click(); time.sleep(0.8)
    F.go_to_end(fr, page)

    warn = []
    F.do_table(page, fr, ROWS, warn)
    log("\n최종 dims=%s" % (F._dims(fr),))
    log("내용=%s" % fr.locator("table").last.inner_text().replace("\n", " / "))
    log("경고=%s" % (warn or "없음"))
    page.screenshot(path=os.path.join(BASE, "tbl4_result.png"))
    log("\n테스트 끝. 창 닫으면 종료.")
    while not page.is_closed(): time.sleep(2)
