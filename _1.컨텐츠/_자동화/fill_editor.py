# -*- coding: utf-8 -*-
"""
초안 md → 네이버 스마트에디터 본문 채우기 (발행/저장 안 함).
사용: python fill_editor.py <md경로>
"""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup
from md_parser import parse, split_bold

BASE, PROFILE = os.path.dirname(os.path.abspath(__file__)), None
PROFILE = os.path.join(BASE, "chrome_profile")
BLOG_ID, IMG_SUB = "baiyan_novembre", "클로드"

BTN_IMG   = "button.se-image-toolbar-button"
BTN_HR    = "button.se-document-toolbar-icon-select-button[data-name=horizontal-line]"
BTN_TABLE = "button.se-table-toolbar-button"
ADD_BTN   = ".se-cell-add-button"
DEL_BTN   = ".se-context-menu-button-delete"
ALL_CELLS = ".se-cell-select-all-button"
ALIGN_DD  = "button[data-name='align-drop-down-with-justify']"
ALIGN_OPT = "button.se-toolbar-option-icon-button"
# 열 선택 버튼 위에 크기조절 핸들이 겹쳐 클릭을 가로챈다. 잠깐 통과시킨다.
SIZEBAR = "(v) => document.querySelectorAll('.se-cell-size-controlbar').forEach(e => e.style.pointerEvents = v)"

BTN_BOTTOM = "button.se-canvas-bottom-button"
BTN_LINK   = "button.se-link-toolbar-button"
BTN_QUOTE  = "button.se-insert-quotation-default-toolbar-button"
LINK_APPLY = ".se-custom-layer-link-apply-button"

def go_to_end(fr, page):
    """문서 맨 끝에 새 문단을 만들고 커서를 옮긴다.
    .se-content 중앙 클릭은 글이 길어지면 표/이미지 안을 찍어 커서가 갇힌다."""
    try:
        b = fr.locator(BTN_BOTTOM)
        if b.count():
            b.first.click(timeout=5000); time.sleep(0.4); return True
    except Exception:
        pass
    try:                                     # 예비: 마지막 문단 클릭
        fr.locator(".se-text-paragraph").last.click(timeout=4000)
        page.keyboard.press("Control+End")
    except Exception:
        pass
    return False

def log(m): print(m); sys.stdout.flush()

VS16 = chr(0xFE0F)                 # 이형 선택자(눈에 안 보이는 글자라 코드로 쓴다)

def _vs_split(s):
    """'⚠️ 주의' -> [('⚠️',True), (' 주의',False)]. 기본문자+U+FE0F 쌍만 True."""
    out, buf, i = [], "", 0
    while i < len(s):
        # 중복은 '기본 다국어 평면' 문자(⚠ ✈ ▶ ✂)에서만 생긴다.
        # 🍽️ 처럼 코드포인트가 큰 이모지는 VS16이 붙어도 멀쩡하니 건드리지 않는다.
        if i + 1 < len(s) and s[i+1] == VS16 and ord(s[i]) < 0x10000:
            if buf: out.append((buf, False)); buf = ""
            out.append((s[i:i+2], True)); i += 2
        else:
            buf += s[i]; i += 1
    if buf: out.append((buf, False))
    return out

def type_text(page, s, delay=6):
    """네이버 에디터는 기본문자+U+FE0F 이모지를 받으면 홑문자를 앞에 남긴다(⚠⚠️).
    이모지 한 쌍을 친 직후 ←/Backspace/→ 로 그 홑문자만 지운다."""
    if VS16 not in s:
        page.keyboard.type(s, delay=delay); return
    for seg, is_emoji in _vs_split(s):
        page.keyboard.type(seg, delay=delay)
        if is_emoji:
            time.sleep(0.25)
            page.keyboard.press("ArrowLeft");  time.sleep(0.1)
            page.keyboard.press("Backspace");  time.sleep(0.1)
            page.keyboard.press("ArrowRight"); time.sleep(0.1)

def do_text(page, line):
    for seg, bold in split_bold(line):
        if not seg: continue
        if bold: page.keyboard.press("Control+b")
        type_text(page, seg)
        if bold: page.keyboard.press("Control+b")

# ---------- 링크 ----------
def do_link(page, fr, url, head, text, warn):
    """head(머리말)는 그냥 치고, text만 선택해 링크를 덮는다(카드형 미리보기 방지).
    뒤에서부터 글자 수만큼 선택하므로 앞의 머리말은 링크에 안 들어간다."""
    if head: type_text(page, head)
    type_text(page, text)
    for _ in range(len(text)): page.keyboard.press("Shift+ArrowLeft")
    time.sleep(0.6)
    ok = False
    try:
        fr.locator(BTN_LINK).first.click(timeout=5000); time.sleep(1.2)
        inp = fr.locator("input[placeholder*='URL']")
        if not inp.count(): raise RuntimeError("URL 입력칸 없음")
        inp.first.click(); time.sleep(0.3)
        type_text(page, url, delay=4); time.sleep(0.5)
        fr.locator(LINK_APPLY).first.click(); time.sleep(1.5)
        ok = True
    except Exception:
        warn.append("링크 적용 실패(텍스트만 남음): %s" % text[:24])
    # 적용 직후에도 링크 텍스트가 선택된 채로 남는다.
    # 이 상태에서 Enter를 치면 선택 영역이 통째로 지워지므로 먼저 선택을 푼다.
    page.keyboard.press("ArrowRight")               # 선택 해제 + 커서를 링크 끝으로
    page.keyboard.press("End")
    time.sleep(0.2)
    page.keyboard.press("Enter")
    return ok

# ---------- 사진 ----------
def do_image(page, fr, path, caption, warn):
    # 업로드가 빠르면 set_files 뒤에 세는 사이 이미 1장 늘어나 있다.
    # 그러면 영영 before 를 못 넘겨 멀쩡히 올라간 사진을 실패로 보고, 캡션도 건너뛴다.
    before = fr.locator(".se-component.se-image").count()
    with page.expect_file_chooser(timeout=30000) as fc:
        fr.locator(BTN_IMG).first.click()
    fc.value.set_files([path])
    for _ in range(90):                                  # 업로드 완료 대기
        time.sleep(1)
        if fr.locator(".se-component.se-image").count() > before: break
    else:
        warn.append("사진 업로드 확인 실패: %s" % os.path.basename(path)); return
    time.sleep(1.2)
    if not caption: return
    try:                                                 # 캡션은 실패해도 진행
        comp = fr.locator(".se-component.se-image").last
        comp.click(timeout=4000); time.sleep(0.6)
        cap = comp.locator(".se-module-text").last
        if cap.count() and cap.is_visible():
            cap.click(timeout=3000); time.sleep(0.3)
            type_text(page, caption)
        else:
            warn.append("캡션 칸이 열리지 않음: %s" % caption[:24])
    except Exception:
        warn.append("캡션 입력 실패: %s" % caption[:24])

# ---------- 표 ----------
def _vis(fr, sel):
    """표가 둘 이상이면 이전 표의 핸들이 hidden 인 채로 DOM 에 남는다.
    .first 가 그걸 잡아 클릭이 타임아웃난다. 보이는 것만 고른다."""
    return fr.locator(sel).filter(visible=True)


def _dims(fr):
    t = fr.locator("table").last
    return t.locator("tr").count(), t.locator("tr").first.locator("td,th").count()

def _add_handles(fr):
    """⊕ 핸들을 (행추가용, 열추가용)으로 분류해 좌표순 반환."""
    a = _vis(fr, ADD_BTN)
    items = []
    for i in range(a.count()):
        b = a.nth(i).bounding_box()
        if b: items.append((i, b["x"], b["y"]))
    if not items: return [], []
    minx = min(t[1] for t in items)
    rows = sorted([t for t in items if abs(t[1]-minx) < 12], key=lambda t: t[2])
    cols = sorted([t for t in items if abs(t[1]-minx) >= 12], key=lambda t: t[1])
    return rows, cols

def _handles_dump(fr):
    """실패 시점의 표 핸들 상태. 어느 표의 핸들이 잡혔는지 보려는 것."""
    out = []
    try: out.append("table=%d" % fr.locator("table").count())
    except Exception: out.append("table=?")
    for name, sel in (("all_cells", ALL_CELLS), ("del", DEL_BTN),
                      ("colsel", ".se-cell-select-button")):
        try:
            loc = fr.locator(sel); n = loc.count()
            vis = sum(1 for i in range(n) if loc.nth(i).is_visible())
            txt = ""
            if name == "colsel":
                txt = "[" + ",".join(
                    "%s%s" % ((loc.nth(i).inner_text() or "").strip()[:8],
                              "" if loc.nth(i).is_visible() else "(hidden)")
                    for i in range(min(n, 10))) + "]"
            out.append("%s=%d/vis%d%s" % (name, n, vis, txt))
        except Exception:
            out.append("%s=err" % name)
    return " ".join(out)


def del_extra_cols(page, fr, need_c, warn):
    """네이버 기본 표는 3열이라 2열 표는 빈 열이 남는다. 오른쪽부터 지운다."""
    for _ in range(4):
        have_c = _dims(fr)[1]
        if have_c <= need_c: return
        last = have_c - 1
        try:
            fr.locator("table").last.locator("td").nth(last).click(timeout=4000)
            time.sleep(0.7)
            fr.evaluate(SIZEBAR, "none")
            (_vis(fr, ".se-cell-select-button")
               .filter(has_text="%d열 선택" % last).first.click(timeout=8000))
            time.sleep(1.0)
            fr.evaluate(SIZEBAR, "")
            _vis(fr, DEL_BTN).first.click(timeout=8000)
            time.sleep(1.2)
        except Exception as e:
            try: fr.evaluate(SIZEBAR, "")
            except Exception: pass
            log("      !! 열삭제 예외: %s | %s" % (
                type(e).__name__, str(e)[:200].replace("\n", " ")))
            log("      !! 핸들: " + _handles_dump(fr))
            break
        if _dims(fr)[1] >= have_c: break        # 안 줄면 즉시 중단
    if _dims(fr)[1] > need_c:
        warn.append("빈 열 삭제 실패 — 직접 삭제 필요")

def del_extra_rows(page, fr, need_r, warn):
    """네이버 기본 표는 3행이라 2행 표는 빈 행이 남는다. 아래부터 지운다."""
    for _ in range(4):
        have_r, have_c = _dims(fr)
        if have_r <= need_r: return
        last = have_r - 1
        try:
            fr.locator("table").last.locator("td").nth(last*have_c).click(timeout=4000)
            time.sleep(0.7)
            fr.evaluate(SIZEBAR, "none")
            (_vis(fr, ".se-cell-select-button")
               .filter(has_text="%d행 선택" % last).first.click(timeout=8000))
            time.sleep(1.0)
            fr.evaluate(SIZEBAR, "")
            _vis(fr, DEL_BTN).first.click(timeout=8000)
            time.sleep(1.2)
        except Exception as e:
            try: fr.evaluate(SIZEBAR, "")
            except Exception: pass
            log("      !! 행삭제 예외: %s | %s" % (
                type(e).__name__, str(e)[:200].replace(chr(10), " ")))
            log("      !! 핸들: " + _handles_dump(fr))
            break
        if _dims(fr)[0] >= have_r: break        # 안 줄면 즉시 중단
    if _dims(fr)[0] > need_r:
        warn.append("빈 행 삭제 실패 — 직접 삭제 필요")

def center_cells(page, fr, warn):
    """셀 전체 선택 → 정렬 드롭다운 → 가운데 정렬."""
    try:
        fr.locator("table").last.locator("td").first.click(timeout=4000)
        time.sleep(0.6)
        fr.evaluate(SIZEBAR, "none")               # 겹친 핸들 통과
        _vis(fr, ALL_CELLS).first.click(timeout=8000)
        time.sleep(0.9)
        fr.evaluate(SIZEBAR, "")
        _vis(fr, ALIGN_DD).first.click(timeout=6000)
        time.sleep(0.8)
        (_vis(fr, ALIGN_OPT).filter(has_text="가운데 정렬")
           .first.click(timeout=6000))
        time.sleep(0.8)
    except Exception as e:
        try: fr.evaluate(SIZEBAR, "")
        except Exception: pass
        log("      !! 정렬 예외: %s | %s" % (
            type(e).__name__, str(e)[:200].replace("\n", " ")))
        log("      !! 핸들: " + _handles_dump(fr))
        warn.append("표 가운데 정렬 실패 — 직접 지정 필요"); return
    al = fr.evaluate("() => { const t = [...document.querySelectorAll('table')].pop();"
                     "  return t ? [...t.querySelectorAll('td .se-text-paragraph')]"
                     "    .map(p => getComputedStyle(p).textAlign) : []; }")
    off = [a for a in al if a != "center"]
    log("      셀 가운데 정렬 %d/%d" % (len(al) - len(off), len(al)))
    if off: warn.append("표 가운데 정렬 일부 누락 (%d칸) — 직접 확인" % len(off))
    go_to_end(fr, page)                            # 셀 선택 해제 (안 풀면 다음 입력이 덮어쓴다)

def do_table(page, fr, rows, warn):
    need_r, need_c = len(rows), max(len(r) for r in rows)
    fr.locator(BTN_TABLE).first.click(); time.sleep(2)
    have_r, have_c = _dims(fr)

    for _ in range(60):                                  # 행 추가 (상한 있음)
        if have_r >= need_r: break
        rb, _c = _add_handles(fr)
        if not rb: break
        _vis(fr, ADD_BTN).nth(rb[-1][0]).click(); time.sleep(0.9)
        nr, nc = _dims(fr)
        if nr == have_r: break                           # 안 늘면 즉시 중단
        have_r, have_c = nr, nc

    for _ in range(10):                                  # 열 추가 (필요한 경우만)
        if have_c >= need_c: break
        _r, cb = _add_handles(fr)
        if not cb: break
        _vis(fr, ADD_BTN).nth(cb[-1][0]).click(); time.sleep(0.9)
        nr, nc = _dims(fr)
        if nc == have_c: break
        have_r, have_c = nr, nc

    del_extra_cols(page, fr, need_c, warn)      # 남는 빈 열 제거
    del_extra_rows(page, fr, need_r, warn)      # 남는 빈 행 제거
    have_r, have_c = _dims(fr)
    log("      표 요청 %d행%d열 → 생성 %d행%d열" % (need_r, need_c, have_r, have_c))
    if (have_r, have_c) != (need_r, need_c):
        warn.append("표 크기 불일치 (요청 %dx%d / 생성 %dx%d) — 직접 조정 필요"
                    % (need_r, need_c, have_r, have_c))
    tds = fr.locator("table").last.locator("td,th")
    for ri, row in enumerate(rows):
        if ri >= have_r: break
        for ci, cell in enumerate(row):
            if ci >= have_c or not cell: continue
            try:
                tds.nth(ri*have_c + ci).click(timeout=4000); time.sleep(0.12)
                type_text(page, cell, delay=4)
            except Exception:
                warn.append("표 셀 입력 실패 (%d,%d)" % (ri+1, ci+1))
    center_cells(page, fr, warn)                # 셀 내용 가운데 정렬

# ---------- 본체 ----------
def pick_img_dir(d):
    """사진 폴더를 찾는다. IMG_SUB → md와 같은 폴더 → 사진이 든 하위폴더 순."""
    want = {fn for k, v in d["blocks"] if k == "img" for fn in [v[0]]}
    base = d["img_dir"]
    cands = [os.path.join(base, IMG_SUB), base]
    # 'photos' 처럼 이름이 다른 하위폴더도 받아준다. 수정본 md 가 한 단계 위에
    # 놓이는 경우가 있어 손자 폴더(하위 2단계)까지 본다.
    try:
        for n in sorted(os.listdir(base)):
            d1 = os.path.join(base, n)
            if not os.path.isdir(d1):
                continue
            cands.append(d1)
            try:
                cands += [os.path.join(d1, m) for m in sorted(os.listdir(d1))
                          if os.path.isdir(os.path.join(d1, m))]
            except OSError:
                pass
    except OSError:
        pass
    for c in cands:
        if os.path.isdir(c) and want and want <= set(os.listdir(c)):
            return c
    return base

def clear_document(page, fr, warn):
    """수정 모드 전용 - 기존 제목과 본문을 지운다.

    덜 지워진 채로 채우면 발행된 글에 내용이 두 번 들어간다. 그래서 남은
    컴포넌트를 세서 확인하고, 안 비워졌으면 채우지 않고 멈춘다.
    """
    # 제목 칸(se-documentTitle)도 se-component 다. 본문만 세야 한다.
    CNT = ("() => document.querySelectorAll("
           "'.se-content .se-component:not(.se-documentTitle)').length")

    fr.locator(".se-documentTitle").click(); time.sleep(0.6)
    page.keyboard.press("Control+a"); time.sleep(0.2)
    page.keyboard.press("Delete"); time.sleep(0.5)

    left = -1
    for attempt in range(3):
        fr.locator(".se-content").click(); time.sleep(0.6)
        page.keyboard.press("Control+a"); time.sleep(0.3)
        page.keyboard.press("Delete"); time.sleep(1.0)
        dismiss_restore_popup(fr)
        try:
            left = fr.evaluate(CNT)
        except Exception:
            left = -1
        log("  비우기 %d회차 - 남은 본문 컴포넌트 %s개" % (attempt + 1, left))
        if left in (0, 1):                 # 빈 문단 하나는 정상이다
            return True
    warn.append("기존 본문을 비우지 못했습니다 (남은 본문 컴포넌트 %s개)" % left)
    return False


def main(md_path, post_no=None):
    # 마스터 2-11 (2026-10-12): 새 글은 지침 경유표 + draft_lint 통과 전에는 넣지 않는다. 건너뛰는 옵션은 없다.
    import draft_lint
    _f, _w = draft_lint.lint(md_path)
    for _x in _w: log("  ⚠ 초안 검사: " + _x)
    if _f:
        log("=" * 56)
        log("초안 검사(draft_lint) 실패 — 자동 입력을 하지 않습니다 (마스터 2-11)")
        for _x in _f: log("  ❌ " + _x)
        log("=" * 56)
        if not post_no:
            sys.exit(2)
        log("[수정 모드] 기존 글 수정이라 경고만 하고 진행합니다")
    d = parse(md_path)
    img_dir = pick_img_dir(d)
    log("사진 폴더: %s" % img_dir)
    log("제목: %s\n블록: %d개\n" % (d["title"], len(d["blocks"])))

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE, channel="chrome", headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1400, "height": 950})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        if post_no:
            # 대문자 Redirect 나 /<id>/<logNo> 형태는 에디터가 안 뜬다.
            # 소문자 redirect + PostWriteForm.naver 만 동작한다 (dbg_update_url.py 로 확인).
            url = ("https://blog.naver.com/PostWriteForm.naver"
                   "?blogId=%s&logNo=%s&redirect=Update" % (BLOG_ID, post_no))
            log("[수정 모드] 기존 글 %s 을 엽니다" % post_no)
        else:
            url = "https://blog.naver.com/%s?Redirect=Write" % BLOG_ID
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        fr = get_editor_frame(page, log=log)
        log("에디터 준비 완료\n")

        warn = []
        if post_no:
            log("[수정 모드] 기존 제목·본문을 지웁니다")
            if not clear_document(page, fr, warn):
                log("")
                log("=" * 56)
                log("!! 기존 내용을 비우지 못해 채우기를 중단합니다.")
                log("   그대로 채우면 발행된 글에 내용이 두 번 들어갑니다.")
                log("   창을 열어 두었으니 직접 비운 뒤 다시 실행하세요.")
                log("=" * 56)
                while not page.is_closed():
                    time.sleep(2)
                return

        # 제목은 눈으로 확인한다. 예전에는 타이핑만 하고 "입력 완료"를 찍었는데,
        # 복구 팝업이 포커스를 가로채면 한 글자도 안 들어간 채 성공으로 기록됐다
        # (2026-09-26 실측: 본문 89블록은 정상인데 제목만 비어서 발행 직전에 발견).
        title_ok = False
        for attempt in (1, 2, 3):
            fr.locator(".se-documentTitle").click(); time.sleep(0.8)
            page.keyboard.press("Control+a"); time.sleep(0.2)
            type_text(page, d["title"], delay=10)
            time.sleep(0.6)
            got = (fr.locator(".se-documentTitle").inner_text() or "")
            got = got.replace("​", "").replace(" ", " ").strip()
            if got == d["title"].strip():
                log("[제목] 입력 완료 — 확인됨")
                title_ok = True
                break
            log("[제목] 안 맞음 (%d/3) — 읽은 값: %r" % (attempt, got[:60]))
            dismiss_restore_popup(fr, log)       # 복구 팝업이 원인인 경우가 많다
            time.sleep(0.5)
        if not title_ok:
            log("!! 제목 입력 실패. 본문은 계속 채우니 제목만 직접 넣으세요:")
            log("   %s" % d["title"])

        fr.locator(".se-content").click(); time.sleep(0.8)
        go_to_end(fr, page)

        n_img, t0 = 0, time.time()
        for idx, (kind, val) in enumerate(d["blocks"]):
            try:
                dismiss_restore_popup(fr)
                if kind == "text":
                    do_text(page, val); page.keyboard.press("Enter")
                elif kind == "quote":
                    # '>' 표식은 떼고, 연속된 인용구 줄은 한 덩어리로 묶는다
                    prev_k = d["blocks"][idx-1][0] if idx else None
                    next_k = d["blocks"][idx+1][0] if idx+1 < len(d["blocks"]) else None
                    if prev_k == "quote":
                        page.keyboard.press("Enter")
                    else:
                        fr.locator(BTN_QUOTE).first.click(); time.sleep(1.2)
                        log("  [%3d] 인용구" % idx)
                    do_text(page, val)
                    if next_k != "quote":
                        go_to_end(fr, page)
                elif kind == "blank":
                    page.keyboard.press("Enter")
                elif kind == "hr":
                    fr.locator(BTN_HR).first.click(); time.sleep(1.0)
                    go_to_end(fr, page)
                elif kind == "img":
                    fn, cap = val
                    fp = os.path.join(img_dir, fn)
                    if not os.path.exists(fp):
                        warn.append("사진 파일 없음: %s" % fn); continue
                    n_img += 1
                    log("  [%3d] 사진 %2d  %s" % (idx, n_img, fn))
                    do_image(page, fr, fp, cap, warn)
                    go_to_end(fr, page)
                elif kind == "table":
                    log("  [%3d] 표 삽입" % idx)
                    do_table(page, fr, val, warn)
                    go_to_end(fr, page)
                elif kind == "link":
                    u, h, t = val
                    log("  [%3d] 링크 %s%s" % (idx, h, t[:24]))
                    do_link(page, fr, u, h, t, warn)
                elif kind == "tags":
                    # 네이버는 본문 #태그를 그대로 태그로 인식한다
                    do_text(page, val); page.keyboard.press("Enter")
                    log("  [%3d] 태그 %d개 입력" % (idx, len(val.split())))
            except Exception as e:
                warn.append("[%d] %s 실패: %s" % (idx, kind, type(e).__name__))
                log("      !! %s 실패: %s" % (kind, str(e)[:90]))

        # 링크 검증 — 문단에 실제로 링크가 걸렸는지 센다
        LINKQ = ("() => [...document.querySelectorAll('.se-text-paragraph')]"
                 ".filter(p=>p.querySelector('a,[class*=se-link]'))"
                 ".map(p=>(p.textContent||'').trim().slice(0,30))")
        try:
            got = fr.evaluate(LINKQ)
            need = sum(1 for k, _ in d["blocks"] if k == "link")
            log("")
            log("링크 %d/%d 적용됨" % (len(got), need))
            for g in got: log("  · " + g)
            if len(got) < need:
                warn.append("링크 누락 (%d/%d) — 직접 확인 필요" % (len(got), need))
        except Exception:
            warn.append("링크 검증 실패 — 직접 확인 필요")

        page.screenshot(path=os.path.join(BASE, "filled_result.png"), full_page=True)
        log("\n" + "="*56)
        log("본문 입력 완료 — 사진 %d장 / 소요 %d초" % (n_img, time.time()-t0))
        if warn:
            log("\n확인 필요 %d건:" % len(warn))
            for w in warn[:25]: log("  - " + w)
        log("\n브라우저에서 검토하세요. 창을 닫으면 종료됩니다.")
        if post_no:
            log("수정 반영(발행) 버튼은 누르지 않았습니다.")
        else:
            log("발행도 저장도 하지 않았습니다.")
        log("="*56)
        while not page.is_closed():
            time.sleep(2)
        log("창이 닫혔습니다.")

if __name__ == "__main__":
    # 사용: python fill_editor.py <md경로> [--post <글번호>]
    #   --post 를 주면 새 글이 아니라 그 글을 수정 모드로 연다.
    args = sys.argv[1:]
    post = None
    if "--post" in args:
        i = args.index("--post")
        post = args[i + 1]
        del args[i:i + 2]
    if not args:
        sys.exit("사용: python fill_editor.py <md경로> [--post <글번호>]")
    main(args[0], post)
