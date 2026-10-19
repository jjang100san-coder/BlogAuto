# -*- coding: utf-8 -*-
"""
네이버 로그인 전용 프로필 준비 스크립트.
크롬 창을 띄우고 사용자가 직접 로그인할 때까지 기다린다.
로그인 쿠키(NID_AUT/NID_SES)가 잡히면 성공 처리하고 종료.
비밀번호는 이 스크립트가 보지도 저장하지도 않는다 — 브라우저 프로필에만 남는다.
"""
import sys, time, os
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
WAIT_SEC = 300          # 최대 5분 대기
LOGIN_URL = "https://nid.naver.com/nidlogin.login"

def logged_in(ctx):
    names = {c["name"] for c in ctx.cookies() if "naver.com" in c.get("domain", "")}
    return {"NID_AUT", "NID_SES"} <= names

def main():
    os.makedirs(PROFILE, exist_ok=True)
    print("프로필 경로:", PROFILE)
    with sync_playwright() as p:
        kw = dict(
            user_data_dir=PROFILE,
            headless=False,
            args=["--disable-blink-features=AutomationControlled",
                  "--window-size=1280,900"],
            viewport={"width": 1280, "height": 900},
        )
        try:                                    # 설치된 실제 크롬 우선
            ctx = p.chromium.launch_persistent_context(channel="chrome", **kw)
            print("브라우저: 설치된 Chrome 사용")
        except Exception as e:
            ctx = p.chromium.launch_persistent_context(**kw)
            print("브라우저: 번들 Chromium 사용 (%s)" % type(e).__name__)

        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        if logged_in(ctx):
            print("\n[OK] 이미 로그인되어 있습니다.")
            ctx.close(); return 0

        page.goto(LOGIN_URL)
        print("\n" + "="*56)
        print("  크롬 창에서 네이버에 로그인해 주세요.")
        print("  (아이디/비밀번호는 이 스크립트가 다루지 않습니다)")
        print("  최대 %d분 대기합니다." % (WAIT_SEC // 60))
        print("="*56 + "\n")

        for i in range(WAIT_SEC // 3):
            time.sleep(3)
            try:
                if logged_in(ctx):
                    print("\n[OK] 로그인 확인됨! 세션이 프로필에 저장되었습니다.")
                    try:
                        page.goto("https://blog.naver.com", timeout=15000)
                        print("     블로그 접근 확인:", page.title())
                    except Exception:
                        pass
                    time.sleep(1)
                    ctx.close(); return 0
            except Exception:
                pass
            if i % 10 == 9:
                print("  ... 대기 중 (%d초 경과)" % ((i+1)*3))

        print("\n[TIMEOUT] 시간 내 로그인이 확인되지 않았습니다. 다시 실행해 주세요.")
        ctx.close(); return 1

sys.exit(main())
