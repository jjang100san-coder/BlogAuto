# -*- coding: utf-8 -*-
"""예약 발행 글의 문단을 고친다 (2026-10-11, 미국 체류기 2편으로 시험).

update_text.py 는 발행글을 글번호(logNo)로 연다. 예약 글은 글번호가 없고
글쓰기 화면 「예약 발행 N건」 팝업에서 제목을 눌러야 에디터에 실린다. 그래서
자동화 크롬(CDP 9334, 네이버 로그인된 chrome_profile)에 붙어 팝업 → 제목 클릭
→ update_text 의 교체 함수를 그대로 쓴다. 발행(예약 유지) 버튼은 누르지 않는다.

사용:
    python update_reserved.py <ops.json> [--dry]
ops.json: {"title": "예약 글 제목(일부)", "ops": [ {"type":"replace","find":"…","text":"…"}, … ]}
"""
import sys, os, io, json, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from update_text import HANDLERS, log, JS_FIND, find_one, PARA
from fill_editor import type_text, do_link

IMG = ".se-content .se-component.se-image"

def op_title(page, fr, o, dry):
    """제목 교체. 본문 작업 뒤 마지막에 둔다."""
    cur = (fr.locator(".se-documentTitle").inner_text() or "").replace("​", "").strip()
    log("    지금 제목: %s" % cur)
    if dry: return True
    fr.locator(".se-documentTitle").click(click_count=3); time.sleep(0.5)
    page.keyboard.press("Control+a"); time.sleep(0.2)
    type_text(page, o["text"], delay=10); time.sleep(0.6)
    got = (fr.locator(".se-documentTitle").inner_text() or "").replace("​", "").strip()
    log("    바뀐 제목: %s" % got)
    return got == o["text"]

def _img_names(fr):
    return fr.evaluate(r"""() => [...document.querySelectorAll('.se-content .se-component.se-image img')]
        .map(im => (im.getAttribute('src')||'').split('/').pop().split('?')[0])""")

def _img_index(fr, o):
    """index(0부터) 또는 file(파일명 일부)로 사진을 고른다. 지연 로딩이면 src 가 svg 라 먼저 스크롤한다."""
    if "file" in o:
        comps = fr.locator(IMG)
        for i in range(comps.count()):
            comps.nth(i).scroll_into_view_if_needed(); time.sleep(0.3)
        time.sleep(1.5)
        names = _img_names(fr)
        hits = [i for i, n in enumerate(names) if o["file"] in n]
        if len(hits) != 1:
            raise LookupError("사진 '%s' 일치 %d개 — %s" % (o["file"], len(hits), names))
        return hits[0]
    return int(o["index"])

def op_caption(page, fr, o, dry):
    """기존 사진의 캡션 칸에 글을 넣는다 (비어 있는 칸만)."""
    i = _img_index(fr, o)
    comp = fr.locator(IMG).nth(i)
    cur = comp.locator(".se-caption p").first.inner_text().strip().replace("​", "") if comp.locator(".se-caption p").count() else ""
    log("    사진 #%d 캡션 지금: %r" % (i, cur[:30]))
    if cur == o["text"]:
        log("    이미 같은 캡션"); return True
    if cur and cur != "사진 설명을 입력하세요." and not o.get("overwrite"):
        raise LookupError("캡션이 이미 있다 — overwrite 없이는 안 덮는다")
    if dry: return True
    comp.scroll_into_view_if_needed(); time.sleep(0.4)
    cap = None
    for attempt in range(3):                      # 첫 클릭에 캡션 칸이 안 열릴 때가 있다 (2026-10-11 5편)
        (comp.locator("img").first if attempt % 2 else comp).click(); time.sleep(0.8 + 0.4 * attempt)
        c = comp.locator(".se-module-text").last
        if c.count() and c.is_visible():
            cap = c; break
        page.keyboard.press("Escape"); time.sleep(0.4)
    if cap is None:
        log("    !! 캡션 칸이 안 열림"); return False
    cap.click(); time.sleep(0.3)
    if cur and o.get("overwrite"):
        page.keyboard.press("Control+a"); time.sleep(0.2)
    type_text(page, o["text"], delay=8); time.sleep(0.5)
    page.keyboard.press("Escape"); time.sleep(0.3)
    # 사진이 선택된 동안은 캡션 칸 안에 툴바 글자(「왼쪽 정렬」 등)가 끼어든다. 문단(p)만 읽는다.
    got = comp.locator(".se-caption p").first.inner_text().strip().replace("​", "")
    log("    캡션 결과: %r" % got[:40])
    return got == o["text"]

def op_img_delete(page, fr, o, dry):
    """사진 한 장을 지운다. 지우기 전 파일명을 로그에 남긴다."""
    i = _img_index(fr, o)
    names = _img_names(fr)
    log("    사진 #%d 삭제 대상: %s (전체 %d장)" % (i, names[i] if i < len(names) else "?", len(names)))
    if dry: return True
    before = fr.locator(IMG).count()
    fr.locator(IMG).nth(i).scroll_into_view_if_needed(); time.sleep(0.4)
    fr.locator(IMG).nth(i).click(); time.sleep(0.6)
    page.keyboard.press("Delete"); time.sleep(1.2)
    return fr.locator(IMG).count() == before - 1

def op_link_before(page, fr, o, dry):
    """앵커 문단 앞에 빈 문단을 만들고 그 안에 「머리말 + 링크 글자」를 넣는다 (add_link.py 방식)."""
    i = find_one(fr, o["anchor"], "link 앵커")
    log("    앵커 문단 #%d 앞에 링크: %s%s" % (i, o.get("head", ""), o["text"]))
    if dry: return True
    para = fr.locator(PARA).nth(i)
    para.scroll_into_view_if_needed(); time.sleep(0.4)
    para.click(position={"x": 3, "y": 5}); page.keyboard.press("Home"); time.sleep(0.4)
    n0 = fr.locator(PARA).count()
    page.keyboard.press("Enter"); time.sleep(0.5)
    page.keyboard.press("ArrowUp"); time.sleep(0.4)
    if fr.locator(PARA).count() != n0 + 1:
        log("    !! 빈 문단이 안 생김"); return False
    warn = []
    ok = do_link(page, fr, o["url"], o.get("head", ""), o["text"], warn)
    time.sleep(1.0)
    # 에디터는 링크를 <a> 가 아니라 span.se-link[data-href] 로 든다 (2026-10-11 실측)
    got = fr.evaluate(r"""(u) => [...document.querySelectorAll('.se-content a, .se-content [class*=se-link]')].filter(a => ((a.getAttribute('href')||a.getAttribute('data-href'))||'').includes(u)).map(a => a.innerText.trim())""", o["url"])
    log("    링크 적용 %s / 본문 속 링크 %s / 경고 %s" % (ok, got, warn))
    return bool(ok) and got == [o["text"]]

def op_bold(page, fr, o, dry):
    """글자는 그대로 두고 굵게만 바꾸는 교체. update_text 의 replace 는 글자가 같으면 실패로 보니 따로 둔다."""
    from update_text import do_text
    i = find_one(fr, o["find"], "bold 대상")
    log("    문단 #%d 발견" % i)
    if dry: return True
    para = fr.locator(PARA).nth(i)
    para.scroll_into_view_if_needed(); time.sleep(0.3)
    para.click(click_count=3); time.sleep(0.5)
    page.keyboard.press("Delete"); time.sleep(0.3)
    do_text(page, o["text"]); time.sleep(0.8)
    r = fr.evaluate(JS_FIND, o["text"].replace("**", ""))
    if len(r["hits"]) != 1: return False
    return fr.evaluate("(i) => !!document.querySelectorAll('.se-content .se-text-paragraph')[i].querySelector('b, strong')", r["hits"][0])

def op_plain(page, fr, o, dry):
    """굵게를 풀고 같은 글자를 보통 글씨로 다시 친다 (볼드가 섹션에 너무 많을 때)."""
    i = find_one(fr, o["find"], "plain 대상")
    log("    문단 #%d 발견" % i)
    if dry: return True
    para = fr.locator(PARA).nth(i)
    para.scroll_into_view_if_needed(); time.sleep(0.3)
    para.click(click_count=3); time.sleep(0.5)
    page.keyboard.press("Delete"); time.sleep(0.3)
    # 선택을 지운 뒤에도 굵게 상태가 남을 수 있어 Ctrl+B 를 한 번 눌러 끄고 확인한다
    type_text(page, o["find"][:1], delay=8); time.sleep(0.3)
    had = fr.evaluate("(i) => !!document.querySelectorAll('.se-content .se-text-paragraph')[i].querySelector('b, strong')", i)
    page.keyboard.press("Backspace"); time.sleep(0.2)
    if had: page.keyboard.press("Control+b"); time.sleep(0.2)
    type_text(page, o["find"], delay=8); time.sleep(0.8)
    r = fr.evaluate(JS_FIND, o["find"])
    if len(r["hits"]) != 1: return False
    return not fr.evaluate("(i) => !!document.querySelectorAll('.se-content .se-text-paragraph')[i].querySelector('b, strong')", r["hits"][0])

HANDLERS = dict(HANDLERS, title=op_title, bold=op_bold, plain=op_plain, caption=op_caption, img_delete=op_img_delete, link_before=op_link_before)
CDP = "http://127.0.0.1:9334"
WRITE = "https://blog.naver.com/PostWriteForm.naver?blogId=baiyan_novembre"
POPUP, RESERVE_BTN = ".layer_popup__MFPwH", "button.reserve_btn__Yc1V8"

def load_reserved(page, title):
    """팝업을 열어 제목이 맞는 예약 글을 에디터에 싣는다. 이미 실려 있으면 그대로."""
    def _n(s): return " ".join((s or "").replace("​", "").replace(" ", " ").split())
    cur = _n(page.locator(".se-documentTitle").inner_text())
    if _n(title) in cur:
        log("이미 실려 있음: %s" % cur); return cur
    # 팝업이 이미 열려 있고 제목이 안 맞으면 먼저 닫는다 (Escape) — 열린 팝업이 클릭을 가로챈다
    pop0 = page.locator(POPUP + ".isShow__KPrZB")
    if pop0.count() and pop0.first.is_visible():
        page.keyboard.press("Escape"); time.sleep(1)
    pop = page.locator(POPUP)
    if not (pop.count() and pop.first.is_visible()):
        page.locator(RESERVE_BTN).first.click(); time.sleep(3)
    btn = page.locator(POPUP + " button.article_button__p0NRG", has_text=title)
    if btn.count() != 1:
        raise LookupError("예약 목록에서 '%s' 일치 %d건" % (title, btn.count()))
    log("예약 목록: %s" % btn.first.inner_text().replace("\n", " / "))
    btn.first.click(); time.sleep(4)
    page.wait_for_selector(".se-content", timeout=30000); time.sleep(2)
    cur = (page.locator(".se-documentTitle").inner_text() or "").replace("​", "").strip()
    if title not in cur:
        raise LookupError("실린 글 제목이 다름: %s" % cur)
    return cur

def main(spec_path, dry):
    spec = json.loads(io.open(spec_path, encoding="utf-8").read())
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        pages = [pg for pg in b.contexts[0].pages if "PostWriteForm" in pg.url]
        page = pages[0] if pages else b.contexts[0].new_page()
        if not pages:
            page.goto(WRITE, wait_until="domcontentloaded"); time.sleep(5)
        fr = page.main_frame                      # 예약 글은 최상위 프레임이 에디터
        cur = load_reserved(page, spec["title"])
        log("에디터 제목: %s%s\n" % (cur, "  [DRY RUN — 고치지 않음]" if dry else ""))
        fail = []
        for n, o in enumerate(spec["ops"], 1):
            log("[%d/%d] %s" % (n, len(spec["ops"]), o["type"]))
            try:
                ok = HANDLERS[o["type"]](page, fr, o, dry)
            except LookupError as e:
                ok = False; log("    !! %s" % e)
            log("    %s" % ("확인" if ok else "!! 실패 — 직접 확인 필요"))
            if not ok:
                fail.append("%d. %s" % (n, o["type"]))
                if not dry: break
        if not dry:
            for o in spec["ops"]:
                if o["type"] == "replace":
                    r = fr.evaluate(JS_FIND, o["text"].replace("**", ""))
                    if r["hits"]:
                        i = r["hits"][0]
                        bold = fr.evaluate("(i) => { const p = document.querySelectorAll('.se-content .se-text-paragraph')[i]; return !!p.querySelector('b, strong'); }", i)
                        log("    문단 #%d 굵게: %s — %s" % (i, bold, o["text"][:30]))
        log("\n결과: %s" % ("전부 확인" if not fail else "실패 " + ", ".join(fail)))
        log("발행(예약 유지) 버튼은 누르지 않았다. 에디터에서 확인 뒤 직접 누른다.")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    main(a[0], "--dry" in a)
