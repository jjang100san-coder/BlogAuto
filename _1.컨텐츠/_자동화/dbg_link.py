# -*- coding: utf-8 -*-
"""링크 덮기(텍스트 선택 → 링크 버튼 → URL) 가능 여부 셀렉터 조사."""
import sys, os, time, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
BLOG_ID = "baiyan_novembre"

DUMP = """() => [...document.querySelectorAll('button,input,a')]
  .filter(e => {
     const s = (e.className||'') + ' ' + (e.getAttribute('data-name')||'') + ' '
             + (e.getAttribute('aria-label')||'') + ' ' + (e.getAttribute('placeholder')||'')
             + ' ' + (e.textContent||'').slice(0,20);
     return /link|url|URL|\uB9C1\uD06C/i.test(s);
  })
  .map(e => ({tag:e.tagName, cls:e.className, name:e.getAttribute('data-name'),
              ph:e.getAttribute('placeholder'), aria:e.getAttribute('aria-label'),
              txt:(e.textContent||'').trim().slice(0,20),
              vis:!!(e.offsetWidth||e.offsetHeight)}))"""

def log(m): print(m); sys.stdout.flush()

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE, channel="chrome", headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/%s?Redirect=Write" % BLOG_ID,
              wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=log)
    log("에디터 준비 완료\n")

    fr.locator(".se-documentTitle").click(); time.sleep(0.6)
    page.keyboard.type("링크 테스트", delay=8)
    fr.locator(".se-content").click(); time.sleep(0.6)

    TEXT, LINKTEXT = "앞문장 ", "여기에링크"
    page.keyboard.type(TEXT + LINKTEXT + " 뒷문장", delay=8)
    # 뒷문장(4자+공백1) 만큼 왼쪽으로 이동 후, 링크 대상만 선택
    for _ in range(len(" 뒷문장")): page.keyboard.press("ArrowLeft")
    for _ in range(len(LINKTEXT)):  page.keyboard.press("Shift+ArrowLeft")
    time.sleep(0.8)

    log("--- 선택 상태에서 link/url 관련 요소 ---")
    for e in fr.evaluate(DUMP): log("  " + json.dumps(e, ensure_ascii=False))

    page.screenshot(path=os.path.join(BASE, "dbg_link_1_selected.png"))

    # --- 링크 버튼 클릭 ---
    fr.locator("button.se-link-toolbar-button").first.click(); time.sleep(1.0)
    log("\n--- 링크바 열린 뒤 보이는 input ---")
    for e in fr.evaluate("""() => [...document.querySelectorAll('input')]
        .map(e=>({cls:e.className, ph:e.getAttribute('placeholder'), type:e.type,
                  vis:!!(e.offsetWidth||e.offsetHeight)})).filter(e=>e.vis)"""):
        log("  " + json.dumps(e, ensure_ascii=False))
    log("--- 링크바 영역 버튼 ---")
    for e in fr.evaluate("""() => [...document.querySelectorAll('[class*=se-link] button, [class*=link-input] button, [class*=se-property-toolbar] button')]
        .map(e=>({cls:e.className, name:e.getAttribute('data-name'),
                  txt:(e.textContent||'').trim().slice(0,20), vis:!!(e.offsetWidth||e.offsetHeight)})).filter(e=>e.vis)"""):
        log("  " + json.dumps(e, ensure_ascii=False))
    page.screenshot(path=os.path.join(BASE, "dbg_link_2_bar.png"))

    # --- URL 입력 후 확정 ---
    URL = "https://blog.naver.com/baiyan_novembre"
    inp = fr.locator("input[placeholder*='URL']")
    log("\nURL input count=%d" % inp.count())
    inp.first.click(); time.sleep(0.3)
    page.keyboard.type(URL, delay=8); time.sleep(0.5)
    fr.locator(".se-custom-layer-link-apply-button").first.click(); time.sleep(1.5)
    page.screenshot(path=os.path.join(BASE, "dbg_link_3_applied.png"))

    # --- 결과 검증 ---
    JS_HTML = "() => [...document.querySelectorAll('.se-text-paragraph')].map(p=>p.outerHTML)"
    log("\n--- 본문 문단 HTML ---")
    for h in fr.evaluate(JS_HTML): log("  " + h)
    JS_LINK = ("() => [...document.querySelectorAll('.se-content *')]"
               ".filter(e=>e.hasAttribute('href')||/link/i.test(e.className||''))"
               ".map(e=>({tag:e.tagName, cls:e.className, href:e.getAttribute('href'),"
               " txt:(e.textContent||'').trim().slice(0,30)}))")
    res = fr.evaluate(JS_LINK)
    log("\n--- href/link 요소 ---")
    for a in res: log("  " + json.dumps(a, ensure_ascii=False))
    log("\n결과: %s" % ("링크 덮기 성공" if res else "링크 흔적 없음"))
    ctx.close()
