# -*- coding: utf-8 -*-
"""발행글 수정 화면의 실제 주소와 프레임 구조를 확인한다. 아무것도 고치지 않는다."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
BLOG_ID = "baiyan_novembre"
LOG_NO = sys.argv[1] if len(sys.argv) > 1 else "224419499878"

CANDS = [
    "https://blog.naver.com/%s/%s?Redirect=Update" % (BLOG_ID, LOG_NO),
    "https://blog.naver.com/PostWriteForm.naver?blogId=%s&Redirect=Update&logNo=%s" % (BLOG_ID, LOG_NO),
    "https://blog.naver.com/PostWriteForm.naver?blogId=%s&logNo=%s&redirect=Update" % (BLOG_ID, LOG_NO),
]

def probe(page, url, tag):
    print("\n" + "=" * 70)
    print("[%s] 요청: %s" % (tag, url))
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e:
        print("  goto 실패:", type(e).__name__, str(e)[:120]); return
    time.sleep(5)
    print("  최종 URL :", page.url)
    print("  문서 title:", (page.title() or "")[:80])
    for f in page.frames:
        try:
            n_content = f.locator(".se-content").count()
            n_title = f.locator(".se-documentTitle").count()
        except Exception:
            n_content = n_title = -1
        print("   - frame name=%r url=%s" % (f.name, (f.url or "")[:90]))
        print("       .se-content=%s  .se-documentTitle=%s" % (n_content, n_title))
    page.screenshot(path=os.path.join(BASE, "dbg_update_%s.png" % tag), full_page=False)
    print("  스크린샷: dbg_update_%s.png" % tag)

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE, channel="chrome", headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    # 0) 먼저 글 보기 화면에서 '수정' 링크의 실제 주소를 캐낸다
    view = "https://blog.naver.com/%s/%s" % (BLOG_ID, LOG_NO)
    print("[view] %s" % view)
    page.goto(view, wait_until="domcontentloaded", timeout=45000)
    time.sleep(4)
    for f in page.frames:
        try:
            hrefs = f.evaluate(
                "() => [...document.querySelectorAll('a')]"
                ".map(a => a.getAttribute('href') || '')"
                ".filter(h => /Update|WriteForm|Modify/i.test(h))")
        except Exception:
            hrefs = []
        for h in hrefs[:10]:
            print("   수정링크 후보:", h[:140])

    for i, u in enumerate(CANDS, 1):
        probe(page, u, "cand%d" % i)

    print("\n확인 끝. 창을 닫습니다.")
    ctx.close()
