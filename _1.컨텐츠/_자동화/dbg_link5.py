# -*- coding: utf-8 -*-
"""수정한 do_link 검증: 본문 → 링크 3줄 → 빈 줄 → 해시태그. 저장·발행 안 함."""
import sys, os, time, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup
import fill_editor as F

BASE = os.path.dirname(os.path.abspath(__file__))
LINKS = [("https://blog.naver.com/baiyan_novembre/224396513000", "▶ 1편 아내는 평생 소원이라 했고, 나는 숫자를 댔어"),
         ("https://blog.naver.com/baiyan_novembre/224396521566", "▶2편: 2주를 차로만 돌았는데 남는 게 없었어"),
         ("https://blog.naver.com/baiyan_novembre/224396528324", "3편. 깎아달라고 했다가 2.5% 더 주고 샀어")]
TAGS = "#퇴직연금중도인출 #DC형퇴직연금 #내집마련"

# 문단별로 (텍스트, 링크걸린부분) 을 뽑는다
DUMP = """() => [...document.querySelectorAll('.se-text-paragraph')].map(p => ({
  t: (p.textContent||'').trim(),
  link: [...p.querySelectorAll('a,[class*="se-link"],[class*="link"]')].map(e=>(e.textContent||'').trim()).filter(x=>x)
}))"""

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
    page.keyboard.type("링크 수정본 검증", delay=8)
    fr.locator(".se-content").click(); time.sleep(0.6)
    F.go_to_end(fr, page)

    warn = []
    page.keyboard.type("너희는 언제부터 준비했어?", delay=6); page.keyboard.press("Enter")
    import md_parser as MP
    for u, lab in LINKS:
        mh = MP.RE_HEAD.match(lab)
        if mh:
            mark = (mh.group(1) + " ") if mh.group(1) else ""
            h, t = "%s%s편 : " % (mark, mh.group(2)), mh.group(3)
        else:
            h, t = "", lab
        log("링크: 머리말=%r 링크=%r → %s" % (h, t[:16],
            "OK" if F.do_link(page, fr, u, h, t, warn) else "실패"))
    page.keyboard.press("Enter")
    page.keyboard.type(TAGS, delay=6)

    log("\n--- 문단 덤프 ---")
    for d in fr.evaluate(DUMP): log("  " + json.dumps(d, ensure_ascii=False))
    log("\n경고: %s" % (warn or "없음"))
    page.screenshot(path=os.path.join(BASE, "dbg5_result.png"))
    log("\n검증 끝. 저장/발행 안 함. 창 닫으면 종료.")
    while not page.is_closed(): time.sleep(2)
