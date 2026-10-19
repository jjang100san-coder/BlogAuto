# -*- coding: utf-8 -*-
"""발행글에 링크 한 줄만 넣는다 (수정 화면에서 앵커 문단 바로 앞에). 사진·다른 문단은 건드리지 않는다.

사용: python add_link.py <spec.json>
spec: {"blog_id", "post_no", "title_old", "anchor_startswith" 또는 "after_startswith", "url", "text"}
  text 는 초안 [[LINK:]] 와 같은 규칙(md_parser.split_link_label): 「머리말 | 제목」 이면 머리말은 일반 글자, 제목에만 링크.
  after_startswith 를 주면 그 문단(기존 링크 줄) 바로 아래에 빈 줄 없이 붙인다(2026-10-16 본인 지적).
발행(수정 반영) 버튼은 누르지 않는다. 창을 열어둔 채 대기한다.
"""
import sys, os, io, json, time, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame
from fill_editor import type_text, BTN_LINK, LINK_APPLY, do_link
from md_parser import split_link_label

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
PARA = ".se-content .se-text-paragraph"
JS_FIND = """([needle, exact]) => {
  const norm = s => (s||'').replace(/\\u200B/g,'').replace(/\\u00A0/g,' ').replace(/\\s+/g,' ').trim();
  const t = norm(needle), hits = [];
  const ps = [...document.querySelectorAll('%s')];
  ps.forEach((p, i) => { const x = norm(p.innerText); if (exact ? x === t : x.startsWith(t)) hits.push(i); });
  return {n: ps.length, hits};
}""" % PARA
JS_LINK = """(url) => [...document.querySelectorAll('.se-content a')].filter(a => (a.getAttribute('href')||'').includes(url)).map(a => a.innerText.trim())"""


def log(m):
    print(m); sys.stdout.flush()


def main(spec_path):
    spec = json.loads(io.open(spec_path, encoding="utf-8").read())
    url = ("https://blog.naver.com/PostWriteForm.naver?blogId=%s&logNo=%s&redirect=Update" % (spec["blog_id"], spec["post_no"]))
    log("글번호 %s 에 링크 추가" % spec["post_no"])
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(user_data_dir=PROFILE, channel="chrome", headless=False,
                                                   args=["--disable-blink-features=AutomationControlled"], viewport={"width": 1400, "height": 950})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        fr = get_editor_frame(page, log=log)
        log("에디터 준비 완료")
        cur = (fr.locator(".se-documentTitle").inner_text() or "").strip().replace("​", "")
        log("현재 제목: %s" % cur)
        ok = False
        if cur != spec["title_old"]:
            log("!! 열린 글의 제목이 기대와 다릅니다. 아무것도 고치지 않았습니다.")
        else:
            head, ltext = split_link_label(spec["text"])
            full = head + ltext
            after = bool(spec.get("after_startswith"))
            key = spec.get("after_startswith") or spec["anchor_startswith"]
            r = fr.evaluate(JS_FIND, [key, False])
            if len(fr.evaluate(JS_FIND, [ltext, False])["hits"]) or len(fr.evaluate(JS_FIND, [full, False])["hits"]):
                log("이미 같은 링크 문구가 본문에 있습니다. 아무것도 고치지 않았습니다.")
            elif len(r["hits"]) != 1:
                log("!! 기준 문단 %d개 일치 (전체 %d개) — 아무것도 고치지 않았습니다." % (len(r["hits"]), r["n"]))
            else:
                i = r["hits"][0]
                log("기준 문단 #%d (전체 %d개) %s 링크 입력 — 머리말 %r / 링크 %r" % (i, r["n"], "바로 아래에" if after else "앞에", head, ltext))
                warn = []
                n_before = fr.evaluate("document.querySelectorAll('%s').length" % PARA)
                # after 모드: 링크 줄 끝(End)에서 Enter 는 커서가 링크 끝으로 안 가 실패했다(10/16 실측).
                # → 기준 문단 「다음」 문단을 쓴다. 그 문단이 비어 있으면(링크 목록과 해시태그 사이 빈 줄) 그 자리에 바로 치고,
                #   비어 있지 않으면 그 문단 앞에 빈 문단을 만든다(Enter → ArrowUp).
                j = i + 1 if after else i
                nxt_txt = fr.evaluate("(k) => { const p = document.querySelectorAll('%s')[k]; return p ? p.innerText.replace(/\\u200B/g,'').trim() : null; }" % PARA, j)
                use_blank = after and nxt_txt == ""
                para = fr.locator(PARA).nth(j)
                para.scroll_into_view_if_needed(); time.sleep(0.5)
                para.click(position={"x": 3, "y": 5})      # 선택·캐럿은 실제 클릭/키로
                if not use_blank:   # 문단 앞에 빈 문단(Enter → ArrowUp) — 문단 맨 앞에 바로 치면 해시태그와 섞인다(10/02·10/04)
                    page.keyboard.press("Home"); time.sleep(0.4)
                    page.keyboard.press("Enter"); time.sleep(0.5)
                    page.keyboard.press("ArrowUp"); time.sleep(0.4)
                log("입력 자리: 문단 #%d %s" % (j, "(원래 있던 빈 줄을 씀)" if use_blank else "앞에 빈 문단을 만듦"))
                n_after = fr.evaluate("document.querySelectorAll('%s').length" % PARA)
                cur_txt = fr.evaluate("(()=>{const s=getSelection();const p=s&&s.anchorNode&&s.anchorNode.parentElement&&s.anchorNode.parentElement.closest('%s');return p?p.innerText.replace(/\u200B/g,'').trim():null})()" % PARA)
                log("빈 문단 삽입: 문단 %d → %d, 캐럿 문단 내용=%r" % (n_before, n_after, (cur_txt or '')[:30]))
                if n_after != n_before + (0 if use_blank else 1) or cur_txt:
                    log("!! 빈 문단이 만들어지지 않았거나 캐럿이 빈 문단에 있지 않습니다. 중단(저장 안 함).")
                    page.screenshot(path=os.path.join(BASE, "add_link_result.png"))
                    while not page.is_closed(): time.sleep(2)
                    return
                applied = do_link(page, fr, spec["url"], head, ltext, warn)   # 끝에 End+Enter 로 빈 문단이 하나 더 생긴다
                time.sleep(0.8)
                n_mid = fr.evaluate("document.querySelectorAll('%s').length" % PARA)
                if not use_blank and n_mid == n_before + 2:   # 새로 만든 자리면 do_link 가 만든 빈 문단을 지운다
                    page.keyboard.press("Backspace"); time.sleep(0.6)
                n_final = fr.evaluate("document.querySelectorAll('%s').length" % PARA)
                got = fr.evaluate("""(t) => [...document.querySelectorAll('.se-text-paragraph')].filter(p => p.querySelector('a,[class*=se-link]'))
                                      .map(p => (p.textContent||'').replace(/\\u200B/g,'').trim()).filter(x => x === t)""", full.strip())
                linked = fr.evaluate("""(t) => [...document.querySelectorAll('.se-content a, .se-content [class*=se-link]')].map(a => (a.innerText||'').replace(/\u200B/g,'').trim()).filter(x => x === t).slice(0,1)""", ltext)
                n_anchor = len(fr.evaluate(JS_FIND, [spec["anchor_startswith"], False])["hits"]) if spec.get("anchor_startswith") else 1
                ok = applied and len(got) == 1 and len(linked) == 1 and n_final == n_before + 1 and n_anchor == 1
                log("링크 적용 %s | 링크 문단 %d개 | 링크 걸린 글자 %r | 문단 수 %d → %d(+1 이어야) | 해시태그 문단 %d개 | 경고 %s"
                    % (applied, len(got), linked, n_before, n_final, n_anchor, warn))
                page.screenshot(path=os.path.join(BASE, "add_link_result.png"))
        log("=" * 56)
        log("결과: %s" % ("링크 추가 확인" if ok else "확인 필요 — 위 줄 참고"))
        log("발행(수정 반영)은 누르지 않았습니다. 창에서 확인 후 직접 눌러 주세요. 창을 닫으면 종료됩니다.")
        log("=" * 56)
        while not page.is_closed():
            time.sleep(2)
        log("창이 닫혔습니다.")


if __name__ == "__main__":
    main(sys.argv[1])
