# -*- coding: utf-8 -*-
"""표 셀 전체 선택 → 가운데 정렬 경로 탐색 + 적용."""
import sys, os, time, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup
import fill_editor as F

BASE = os.path.dirname(os.path.abspath(__file__))
ROWS = [["구간", "걸린 시간"], ["사내 결재와 인감", "영업일 2일"],
        ["보유 상품 매도 결제", "영업일 8일"], ["현금화 완료 후 인출 처리", "영업일 2일"]]
def log(m): print(m); sys.stdout.flush()

VIS = """() => [...document.querySelectorAll('button,[role=button],li,a')]
  .filter(b => b.offsetParent !== null && /정렬/.test(b.innerText||''))
  .map(b => ({tag:b.tagName, cls:(b.className||'').toString().slice(0,70),
              name:b.getAttribute('data-name')||'',
              tx:(b.innerText||'').replace(/\s+/g,' ').trim().slice(0,20)}))"""
ALIGN = """() => [...document.querySelectorAll('table td p, table td .se-text-paragraph')]
  .map(p => getComputedStyle(p).textAlign)"""

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
    page.keyboard.type("표 가운데정렬 검증", delay=8)
    fr.locator(".se-content").click(); time.sleep(0.8)
    F.go_to_end(fr, page)

    warn = []
    F.do_table(page, fr, ROWS, warn)
    log("표 완료 dims=%s / 정렬=%s" % (F._dims(fr), fr.evaluate(ALIGN)))

    # 셀 전체 선택
    allb = fr.locator(".se-cell-select-all-button")
    log("\n셀 전체 선택 버튼 %d개" % allb.count())
    fr.locator("table").last.locator("td").first.click(); time.sleep(0.6)
    fr.evaluate(F.SIZEBAR, "none")
    allb.first.click(timeout=8000); time.sleep(1.0)
    fr.evaluate(F.SIZEBAR, "")
    page.screenshot(path=os.path.join(BASE, "al_1_allsel.png"))

    log("\n--- '정렬' 들어간 보이는 요소 ---")
    for b in fr.evaluate(VIS): log("   " + json.dumps(b, ensure_ascii=False))

    # 정렬 드롭다운 열기
    dd = fr.locator("button[data-name='align-drop-down-with-justify']")
    log("\n정렬 드롭다운 %d개" % dd.count())
    if dd.count():
        dd.first.click(); time.sleep(1.0)
        log("--- 드롭다운 열린 뒤 ---")
        for b in fr.evaluate(VIS): log("   " + json.dumps(b, ensure_ascii=False))
        page.screenshot(path=os.path.join(BASE, "al_2_dropdown.png"))
    log("\n조사 끝. 창 닫으면 종료.")
    while not page.is_closed(): time.sleep(2)
