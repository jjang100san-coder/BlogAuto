# -*- coding: utf-8 -*-
"""표 뒤에서 커서가 정말 빠져나오는지 검증."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame
from fill_editor import go_to_end
BASE = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=os.path.join(BASE,"chrome_profile"), channel="chrome",
        headless=False, args=["--disable-blink-features=AutomationControlled"],
        viewport={"width":1400,"height":950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://blog.naver.com/baiyan_novembre?Redirect=Write",
              wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=print)
    fr.locator(".se-content").click(); time.sleep(1)
    page.keyboard.type("표 앞 문단", delay=8); page.keyboard.press("Enter")

    fr.locator("button.se-table-toolbar-button").first.click(); time.sleep(2)
    t = fr.locator("table").last
    t.locator("td").nth(4).click(); time.sleep(0.3)      # 가운데 셀에 입력
    page.keyboard.type("셀안", delay=8)
    print("표 삽입 + 셀 입력 완료")

    ok = go_to_end(fr, page)
    print("go_to_end 버튼 사용:", ok)
    time.sleep(0.5)
    page.keyboard.type("표 뒤 문단 — 여기가 표 밖이어야 정상", delay=8)
    time.sleep(1)

    inside = fr.evaluate("""() => {
        const t=document.querySelectorAll('table');
        let hit=false;
        t.forEach(tb=>{ if(tb.innerText.includes('표 뒤 문단')) hit=true; });
        return {inTable:hit,
                bodyHas:document.querySelector('.se-content').innerText.includes('표 뒤 문단')};
    }""")
    print("\n결과 → 표 안에 있나?:", inside['inTable'], "/ 본문에 있나?:", inside['bodyHas'])
    print("판정:", "실패 (여전히 표 안)" if inside['inTable'] else "성공 (표 밖으로 나옴)")
    page.screenshot(path=os.path.join(BASE,"escape_test.png"))
    ctx.close()
