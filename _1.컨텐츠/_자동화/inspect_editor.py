# -*- coding: utf-8 -*-
"""스마트에디터 ONE 구조 파악 (읽기만, 아무것도 입력하지 않음)."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
BLOG_ID = "baiyan_novembre"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE, channel="chrome", headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/%s?Redirect=Write" % BLOG_ID,
              wait_until="domcontentloaded", timeout=45000)

    fr = None
    for _ in range(30):                      # 에디터 iframe + 본문 로딩 대기
        time.sleep(2)
        for f in page.frames:
            if "PostWriteForm" in f.url:
                fr = f; break
        if fr:
            try:
                if fr.locator(".se-content, .se-component").count() > 0:
                    break
            except Exception:
                pass
    print("에디터 프레임:", "OK" if fr else "못 찾음")
    time.sleep(3)

    # 작성 중이던 글 복구 팝업 확인
    for sel in [".se-popup-container", ".se-popup", "[class*=popup]"]:
        try:
            n = fr.locator(sel).count()
            if n: print("  팝업 후보 %s : %d개" % (sel, n))
        except Exception: pass

    print("\n--- 핵심 요소 탐색 ---")
    targets = {
      "제목 영역"      : ".se-documentTitle, .se-title-text, [class*=documentTitle]",
      "본문 영역"      : ".se-component-content, .se-text-paragraph, .se-content",
      "사진 버튼"      : "button.se-image-toolbar-button, [data-name=image], button[class*=image]",
      "표 버튼"        : "button.se-table-toolbar-button, [data-name=table], button[class*=table]",
      "구분선 버튼"    : "[data-name=horizontalLine], button[class*=horizontalLine]",
      "파일 input"     : "input[type=file]",
    }
    for label, sel in targets.items():
        try:
            n = fr.locator(sel).count()
            print("  %-10s %s  (%s)" % (label, ("%d개" % n) if n else "없음", sel.split(",")[0]))
        except Exception as e:
            print("  %-10s 오류 %s" % (label, type(e).__name__))

    print("\n--- 상단 툴바 버튼 목록 ---")
    try:
        btns = fr.locator("button")
        for i in range(min(btns.count(), 45)):
            b = btns.nth(i)
            t = (b.get_attribute("data-name") or b.get_attribute("aria-label")
                 or (b.inner_text() or "").strip().replace("\n"," ") or "")[:28]
            cls = (b.get_attribute("class") or "")[:38]
            if t: print("  %-28s | %s" % (t, cls))
    except Exception as e:
        print("  오류:", e)

    page.screenshot(path=os.path.join(BASE, "editor_loaded.png"))
    print("\n스크린샷 저장됨")
    ctx.close()
