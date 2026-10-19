# -*- coding: utf-8 -*-
"""링크 3줄 연속 삽입 재현 + 각 단계 포커스/href 진단. 저장·발행 안 함."""
import sys, os, time, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
BLOG_ID = "baiyan_novembre"
BTN_BOTTOM = "button.se-canvas-bottom-button"
BTN_LINK   = "button.se-link-toolbar-button"
LINK_APPLY = ".se-custom-layer-link-apply-button"

LINKS = [("https://blog.naver.com/baiyan_novembre/224396513000", "1편 아내는 평생 소원이라 했고, 나는 숫자를 댔어"),
         ("https://blog.naver.com/baiyan_novembre/224396528324", "3편 깎아달라고 했다가 2.5% 더 주고 샀어"),
         ("https://blog.naver.com/baiyan_novembre/224396551334", "4편 증명서 다섯 가지 떼어 갔는데 한 장도 안 냈어")]

ACTIVE = """() => { const a=document.activeElement; return a? (a.tagName+'|'+(a.className||'').slice(0,60)+'|ph='+(a.getAttribute&&a.getAttribute('placeholder')||'')) : 'none'; }"""
HREFS  = """() => [...document.querySelectorAll('.se-content a')].map(a=>a.getAttribute('href')+' :: '+(a.textContent||'').trim().slice(0,20))"""
TEXTS  = """() => [...document.querySelectorAll('.se-text-paragraph')].map(p=>(p.textContent||'').trim()).filter(t=>t)"""

def log(m): print(m); sys.stdout.flush()

def go_to_end(fr, page):
    try:
        b = fr.locator(BTN_BOTTOM)
        if b.count(): b.first.click(timeout=5000); time.sleep(0.4); return
    except Exception: pass
    fr.locator(".se-text-paragraph").last.click(timeout=4000)
    page.keyboard.press("Control+End")

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE, channel="chrome", headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/%s?Redirect=Write" % BLOG_ID,
              wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=log)
    dismiss_restore_popup(fr)
    log("에디터 준비 완료")

    fr.locator(".se-documentTitle").click(); time.sleep(0.6)
    page.keyboard.type("링크 연속삽입 진단", delay=8)
    fr.locator(".se-content").click(); time.sleep(0.6)
    go_to_end(fr, page)
    page.keyboard.type("앞 본문 한 줄.", delay=8); page.keyboard.press("Enter")

    for i, (url, text) in enumerate(LINKS, 1):
        log("\n===== 링크 %d =====" % i)
        log("  [전] active=%s" % fr.evaluate(ACTIVE))
        page.keyboard.type(text, delay=6)
        for _ in range(len(text)): page.keyboard.press("Shift+ArrowLeft")
        time.sleep(0.6)
        log("  [선택후] active=%s" % fr.evaluate(ACTIVE))

        fr.locator(BTN_LINK).first.click(); time.sleep(1.2)
        inp = fr.locator("input[placeholder*='URL']")
        log("  [링크바] input=%d active=%s" % (inp.count(), fr.evaluate(ACTIVE)))
        if inp.count():
            inp.first.click(); time.sleep(0.3)
            page.keyboard.type(url, delay=4); time.sleep(0.5)
            log("  [URL입력후] active=%s" % fr.evaluate(ACTIVE))
            ap = fr.locator(LINK_APPLY)
            log("  [적용버튼] count=%d" % ap.count())
            if ap.count(): ap.first.click(); time.sleep(1.5)
        log("  [적용후] active=%s" % fr.evaluate(ACTIVE))
        log("  [적용후] hrefs=%s" % json.dumps(fr.evaluate(HREFS), ensure_ascii=False))
        page.screenshot(path=os.path.join(BASE, "dbg4_%d_applied.png" % i))

        go_to_end(fr, page)     # 문서 포커스 복귀 시도
        log("  [복귀후] active=%s" % fr.evaluate(ACTIVE))
        page.keyboard.type("X", delay=6)   # 커서가 문서에 있는지 표식
        log("  [복귀후] 문단=%s" % json.dumps(fr.evaluate(TEXTS)[-3:], ensure_ascii=False))
        page.keyboard.press("Backspace")

    log("\n최종 hrefs=%s" % json.dumps(fr.evaluate(HREFS), ensure_ascii=False))
    log("최종 문단=%s" % json.dumps(fr.evaluate(TEXTS), ensure_ascii=False))
    page.screenshot(path=os.path.join(BASE, "dbg4_final.png"))
    log("\n저장/발행 안 함. 창 닫으면 종료.")
    while not page.is_closed(): time.sleep(2)
