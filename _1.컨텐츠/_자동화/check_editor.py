# -*- coding: utf-8 -*-
"""저장된 프로필로 글쓰기 화면까지 도달하는지만 확인 (아무것도 쓰지 않음)."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
SHOT = os.path.join(BASE, "editor_check.png")
BLOG_ID = "baiyan_novembre"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE, channel="chrome", headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    names = {c["name"] for c in ctx.cookies() if "naver.com" in c.get("domain","")}
    print("로그인 쿠키:", "OK" if {"NID_AUT","NID_SES"} <= names else "없음")

    url = "https://blog.naver.com/%s?Redirect=Write" % BLOG_ID
    print("\n이동:", url)
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    time.sleep(6)

    print("현재 URL :", page.url)
    print("페이지 제목:", page.title())

    # 스마트에디터는 iframe 안에 있는 경우가 많음
    frames = [f for f in page.frames if f != page.main_frame]
    print("iframe 개수:", len(frames))
    for f in frames[:6]:
        print("   -", (f.name or "(무명)"), "|", f.url[:90])

    page.screenshot(path=SHOT, full_page=False)
    print("\n스크린샷:", SHOT)
    ctx.close()
