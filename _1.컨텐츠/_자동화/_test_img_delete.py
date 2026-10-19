# -*- coding: utf-8 -*-
"""update_text.py 에 사진 끼워넣기를 붙이기 전 시험 (2026-10-01).
빈 새 글 창에서: 문단 A/B/C 를 치고, C 문단 맨 앞에 캐럿을 둔 채 사진을 올린다.
사진이 B 와 C 사이에 들어가는지(= 캐럿 문단 '앞') 블록 순서로 확인한다. 저장·발행하지 않는다."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup
from fill_editor import type_text, BTN_IMG
from update_text import JS_OUTLINE, PARA, JS_FIND

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = sys.argv[1]

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(user_data_dir=os.path.join(BASE, "chrome_profile"),
        channel="chrome", headless=False, args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/PostWriteForm.naver?blogId=baiyan_novembre", wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=print)
    time.sleep(2)
    fr.locator(PARA).first.click(); time.sleep(0.5)
    for s in ("시험문단A", "시험문단B", "시험문단C"):
        type_text(page, s); page.keyboard.press("Enter"); time.sleep(0.3)
    r = fr.evaluate(JS_FIND, "시험문단C"); i = r["hits"][0]
    fr.locator(PARA).nth(i).click(position={"x": 3, "y": 5}); page.keyboard.press("Home"); time.sleep(0.4)
    with page.expect_file_chooser(timeout=30000) as fc:
        fr.locator(BTN_IMG).first.click()
    fc.value.set_files([IMG])
    for _ in range(60):
        time.sleep(1)
        if fr.locator(".se-component.se-image").count() > 0: break
    time.sleep(1.5)
    out = fr.evaluate(JS_OUTLINE)
    print("OUTLINE:", [(b["t"], b["v"][:12]) for b in out])
    # 사진 지우기 시험: 컴포넌트 클릭 → Delete
    comp = fr.locator(".se-component.se-image").first
    comp.click(); time.sleep(0.6)
    page.keyboard.press("Delete"); time.sleep(1.0)
    print("AFTER DELETE count:", fr.locator(".se-component.se-image").count())
    out = fr.evaluate(JS_OUTLINE)
    print("AFTER DELETE:", [(b["t"], b["v"][:12]) for b in out])
    page.screenshot(path=os.path.join(BASE, "_test_img_insert.png"))
    ctx.close()
    print("closed (저장 안 함)")
