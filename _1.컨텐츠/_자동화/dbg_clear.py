# -*- coding: utf-8 -*-
"""수정 화면에서 '비우기' 후 무엇이 남는지 확인한다. 발행/저장은 하지 않는다."""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
BLOG_ID = "baiyan_novembre"
LOG_NO = sys.argv[1] if len(sys.argv) > 1 else "224419499878"
URL = ("https://blog.naver.com/PostWriteForm.naver"
       "?blogId=%s&logNo=%s&redirect=Update" % (BLOG_ID, LOG_NO))

DUMP = """() => {
  const out = {};
  const box = document.querySelector('.se-content');
  out.content_components = [...document.querySelectorAll('.se-content .se-component')]
      .map(e => e.className.split(/\\s+/).slice(0, 4).join(' '));
  out.all_components = document.querySelectorAll('.se-component').length;
  out.text_len = box ? (box.innerText || '').trim().length : -1;
  out.title = (document.querySelector('.se-documentTitle') || {}).innerText || '';
  return out;
}"""

def show(fr, tag):
    d = fr.evaluate(DUMP)
    print("\n[%s]" % tag)
    print("  .se-content 안 컴포넌트 %d개, 전체 %d개" %
          (len(d["content_components"]), d["all_components"]))
    for c in d["content_components"]:
        print("     -", c)
    print("  본문 글자수:", d["text_len"])
    print("  제목:", (d["title"] or "").strip()[:60])
    return d

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE, channel="chrome", headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 950})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=45000)
    fr = get_editor_frame(page, log=lambda m: print(m))
    print("에디터 준비 완료")

    show(fr, "비우기 전")

    fr.locator(".se-documentTitle").click(); time.sleep(0.6)
    page.keyboard.press("Control+a"); time.sleep(0.2)
    page.keyboard.press("Delete"); time.sleep(0.6)
    show(fr, "제목 지운 뒤")

    fr.locator(".se-content").click(); time.sleep(0.6)
    page.keyboard.press("Control+a"); time.sleep(0.3)
    page.keyboard.press("Delete"); time.sleep(1.2)
    dismiss_restore_popup(fr)
    show(fr, "본문 Ctrl+A Delete 1회")

    page.keyboard.press("Control+a"); time.sleep(0.3)
    page.keyboard.press("Delete"); time.sleep(1.2)
    show(fr, "한 번 더")

    page.screenshot(path=os.path.join(BASE, "dbg_clear.png"), full_page=False)
    print("\n스크린샷: dbg_clear.png")
    print("저장/발행 안 함. 창을 닫습니다.")
    ctx.close()
