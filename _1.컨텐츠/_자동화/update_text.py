# -*- coding: utf-8 -*-
"""발행글 텍스트만 고친다 (제목·소제목·문단). 사진은 건드리지 않는다.

fill_editor.py 의 --post 수정 모드는 본문을 통째로 비우고 다시 채우기 때문에
사진 8장이 재업로드된다. 수정본 작업 메모의 '🚫 이미지를 다시 올리지 말 것'을
지키려면 이미 올라가 있는 문단만 찾아서 바꿔야 한다. 그래서 따로 만들었다.

사용:
    python update_text.py <ops.json> [--dry]

--dry 를 주면 문단을 찾기만 하고 한 글자도 고치지 않는다. 먼저 이걸로
8개 앵커가 전부 잡히는지 확인한 뒤 본 실행한다.

발행(수정 반영) 버튼은 누르지 않는다. 창을 열어둔 채 대기한다.
"""
import sys, os, io, json, time, difflib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from editor_util import get_editor_frame, dismiss_restore_popup
from fill_editor import type_text, do_text, BTN_HR, BTN_IMG

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
PARA = ".se-content .se-text-paragraph"

def log(m): print(m); sys.stdout.flush()

# 에디터는 문단 안에 제로폭 문자와 nbsp 를 섞어 넣는다. 그대로 비교하면 안 맞는다.
NORM = ("s => (s||'').replace(/\\u200B/g,'').replace(/\\u00A0/g,' ')"
        ".replace(/\\s+/g,' ').trim()")

JS_FIND = """(needle) => {
  const norm = %s;
  const ps = [...document.querySelectorAll('%s')];
  const t = norm(needle);
  const hits = [];
  ps.forEach((p, i) => { if (norm(p.innerText) === t) hits.push(i); });
  return {n: ps.length, hits};
}""" % (NORM, PARA)



def find_one(fr, text, what, nth=None, expect=None):
    """문단을 하나만 찾는다. 0개나 2개 이상이면 멈춘다 — 엉뚱한 곳을 고치면 안 된다.
    nth: 같은 글자 문단이 여럿일 때(표 칸 등) 위에서 몇 번째(0부터)인지 고른다.
    expect 로 일치 개수까지 맞춰야 고른다 (2026-10-07)."""
    text = text.replace("**", "")                  # 굵게 표시는 화면 글자에 없다
    r = fr.evaluate(JS_FIND, text)
    if nth is not None:
        if expect is not None and len(r["hits"]) != expect:
            raise LookupError("%s: 문단 %d개 일치, 기대 %d개 — %r"
                              % (what, len(r["hits"]), expect, text[:40]))
        if len(r["hits"]) > nth:
            return r["hits"][nth]
    elif len(r["hits"]) == 1:
        return r["hits"][0]
    raise LookupError("%s: 문단 %d개 일치 (전체 %d개) — %r"
                      % (what, len(r["hits"]), r["n"], text[:40]))

def gone(fr, text):
    return len(fr.evaluate(JS_FIND, text.replace("**", ""))["hits"]) == 0

# ---------- 작업별 처리 ----------
def op_replace(page, fr, o, dry):
    nth = o.get("nth")
    before_n = len(fr.evaluate(JS_FIND, o["find"].replace("**", ""))["hits"])
    i = find_one(fr, o["find"], "replace 대상", nth, o.get("expect"))
    log("    문단 #%d 발견%s" % (i, "" if nth is None else " (%d개 중 %d번째)" % (before_n, nth + 1)))
    if dry: return True
    fr.locator(PARA).nth(i).click(click_count=3)   # 문단 통째 선택
    time.sleep(0.5)
    if "**" in o["text"]:
        page.keyboard.press("Delete"); time.sleep(0.3)   # 선택을 먼저 지워야 Ctrl+B 가 새 글자에만 먹는다
        do_text(page, o["text"])
    else:
        type_text(page, o["text"], delay=8)
    time.sleep(0.8)
    if nth is not None:                            # 같은 글자 문단이 하나 줄었는지로 본다
        left = len(fr.evaluate(JS_FIND, o["find"].replace("**", ""))["hits"])
        return left == before_n - 1
    if not gone(fr, o["find"]):
        return False
    return len(fr.evaluate(JS_FIND, o["text"].replace("**", ""))["hits"]) == 1

def op_delete_range(page, fr, o, dry):
    i1 = find_one(fr, o["from"], "delete 시작")
    i2 = find_one(fr, o["to"], "delete 끝")
    log("    문단 #%d ~ #%d" % (i1, i2))
    if i2 < i1:
        raise LookupError("delete_range: 끝 문단이 시작보다 앞에 있습니다")
    if dry: return True
    # JS 로 Range 를 잡으면 안 된다. 에디터가 자기 선택 모델과 동기화하지 않아서
    # Delete 가 엉뚱한 곳(문단 사이 빈 줄)에만 먹는다. 실제 마우스 선택을 쓴다.
    a, b = fr.locator(PARA).nth(i1), fr.locator(PARA).nth(i2)
    a.click(position={"x": 3, "y": 5})             # 첫 문단 첫 줄 왼쪽
    page.keyboard.press("Home"); time.sleep(0.3)
    box = b.bounding_box()
    if not box:
        return False
    b.click(modifiers=["Shift"],                   # 끝 문단 마지막 줄까지 확장
            position={"x": max(box["width"] - 3, 3),
                      "y": max(box["height"] - 5, 3)})
    time.sleep(0.3)
    page.keyboard.press("Shift+End"); time.sleep(0.3)
    page.keyboard.press("Delete")                  # 빈 문단 하나가 남는다 (정상)
    time.sleep(0.9)
    dismiss_restore_popup(fr)
    return gone(fr, o["from"]) and gone(fr, o["to"])

def op_insert_before(page, fr, o, dry):
    i = find_one(fr, o["anchor"], "insert 앵커")
    log("    앵커 문단 #%d 앞에 %d블록" % (i, len(o["blocks"])))
    if dry: return True
    # 캐럿도 JS 로 옮기면 안 된다(delete_range 주석 참고). 앵커 첫 줄 왼쪽을
    # 실제로 클릭하고 Home 을 눌러야 에디터가 문단 맨 앞으로 인식한다.
    fr.locator(PARA).nth(i).click(position={"x": 3, "y": 5})
    page.keyboard.press("Home"); time.sleep(0.4)
    for b in o["blocks"]:
        if b["t"] == "text":
            do_text(page, b["v"])                  # **굵게** 지원 (2026-10-01)
            page.keyboard.press("Enter")           # 친 글이 앞 문단으로 떨어진다
            time.sleep(0.5)
        elif b["t"] == "hr":
            page.keyboard.press("Enter"); time.sleep(0.4)
            page.keyboard.press("ArrowUp"); time.sleep(0.3)
            fr.locator(BTN_HR).first.click(); time.sleep(1.0)
        elif b["t"] == "img":
            if not op_image_here(page, fr, b, o["anchor"]):
                return False
        else:
            raise ValueError("모르는 블록: %r" % b["t"])
    ok = True
    for b in o["blocks"]:
        if b["t"] == "text" and len(fr.evaluate(JS_FIND, b["v"].replace("**", ""))["hits"]) != 1:
            ok = False
    return ok


def op_image_here(page, fr, b, anchor):
    """캐럿이 있는 문단 '앞'에 사진이 들어간다(2026-10-01 빈 글 시험으로 확인).
    올린 뒤 캡션을 달고, 캐럿을 다시 앵커 문단 맨 앞으로 돌려놓는다."""
    before = fr.locator(".se-component.se-image").count()
    with page.expect_file_chooser(timeout=30000) as fc:
        fr.locator(BTN_IMG).first.click()
    fc.value.set_files([b["path"]])
    for _ in range(90):
        time.sleep(1)
        if fr.locator(".se-component.se-image").count() > before:
            break
    else:
        log("    !! 사진 업로드 확인 실패: %s" % os.path.basename(b["path"]))
        return False
    time.sleep(1.5)
    log("    사진 업로드 %s" % os.path.basename(b["path"]))
    if b.get("caption"):
        # 새 사진은 '마지막' 사진이 아니다. 앵커 문단 바로 앞 컴포넌트를 찾는다.
        idx = fr.evaluate("""(anchorText) => {
          const norm = %s;
          const comps = [...document.querySelectorAll('.se-content .se-component')]
              .filter(c => !(c.parentElement && c.parentElement.closest('.se-component')));
          let imgs = 0, last = -1;
          for (const c of comps) {
            if (c.classList.contains('se-image')) { last = imgs; imgs++; continue; }
            const t = [...c.querySelectorAll('.se-text-paragraph')].map(p => norm(p.innerText)).join(' ');
            if (t.includes(norm(anchorText))) return last;
          }
          return -1;
        }""" % NORM, anchor)
        try:
            comp = fr.locator(".se-component.se-image").nth(idx)
            comp.click(timeout=4000); time.sleep(0.6)
            cap = comp.locator(".se-module-text").last
            if cap.count() and cap.is_visible():
                cap.click(timeout=3000); time.sleep(0.3)
                type_text(page, b["caption"], delay=8)
                log("    캡션 입력")
            else:
                log("    !! 캡션 칸이 열리지 않음 — 사진은 들어갔음")
        except Exception as e:
            log("    !! 캡션 입력 실패(%s) — 사진은 들어갔음" % str(e)[:60])
    i = find_one(fr, anchor, "insert 앵커(사진 뒤 복귀)")
    fr.locator(PARA).nth(i).click(position={"x": 3, "y": 5})
    page.keyboard.press("Home"); time.sleep(0.4)
    return True

def op_img_replace(page, fr, o, dry):
    """앵커 문단 '바로 앞' 사진을 지우고 새 사진을 같은 자리에 넣는다 (2026-10-01).
    빈 글 시험: 사진 컴포넌트를 클릭하고 Delete 를 누르면 그 사진만 빠진다."""
    i = find_one(fr, o["anchor"], "img_replace 앵커")
    idx = fr.evaluate(JS_IMG_BEFORE, o["anchor"].replace("**", ""))
    if idx < 0:
        raise LookupError("img_replace: 앵커 바로 앞이 사진이 아닙니다")
    log("    앵커 문단 #%d 바로 앞 사진(%d번째) 교체" % (i, idx + 1))
    if dry: return True
    before = fr.locator(".se-component.se-image").count()
    fr.locator(".se-component.se-image").nth(idx).click(); time.sleep(0.6)
    page.keyboard.press("Delete"); time.sleep(1.0)
    dismiss_restore_popup(fr)
    if fr.locator(".se-component.se-image").count() != before - 1:
        log("    !! 사진 삭제 확인 실패"); return False
    log("    기존 사진 삭제")
    j = find_one(fr, o["anchor"], "img_replace 앵커(삭제 뒤)")
    fr.locator(PARA).nth(j).click(position={"x": 3, "y": 5})
    page.keyboard.press("Home"); time.sleep(0.4)
    return op_image_here(page, fr, {"path": o["path"], "caption": o.get("caption")}, o["anchor"])

JS_IMG_BEFORE = """(anchorText) => {
  const norm = %s;
  const comps = [...document.querySelectorAll('.se-content .se-component')]
      .filter(c => !(c.parentElement && c.parentElement.closest('.se-component')));
  let imgs = 0, prevImg = -1, prevWasImg = false;
  for (const c of comps) {
    if (c.classList.contains('se-image')) { prevImg = imgs; imgs++; prevWasImg = true; continue; }
    const ps = [...c.querySelectorAll('.se-text-paragraph')].map(p => norm(p.innerText)).filter(Boolean);
    if (ps.length && ps[0] === norm(anchorText)) return prevWasImg ? prevImg : -1;
    if (ps.length || c.classList.contains('se-horizontalLine')) prevWasImg = false;
  }
  return -1;
}""" % NORM

HANDLERS = {"replace": op_replace, "delete_range": op_delete_range,
            "insert_before": op_insert_before, "img_replace": op_img_replace}

# ---------- 블록 순서 검증 ----------
# 문단이 '있다'는 것만으로는 부족하다. 사진·구분선 기준으로 어느 자리에 있는지
# 봐야 한다. 지우고 남은 빈 문단은 md 에 없으니 세지 않는다.
JS_OUTLINE = """() => {
  const box = document.querySelector('.se-content');
  if (!box) return [];
  // 수정 화면은 .se-content 와 .se-component 사이에 래퍼가 한 겹 더 있다.
  // ':scope > .se-component' 로 잡으면 0개가 나온다(2026-09-23 실측).
  // 깊이에 상관없이 '가장 바깥쪽 컴포넌트'만 고른다.
  const tops = [...box.querySelectorAll('.se-component')]
      .filter(c => !(c.parentElement && c.parentElement.closest('.se-component')));
  const out = [];
  for (const c of tops) {
    if (c.classList.contains('se-documentTitle')) continue;
    if (c.classList.contains('se-text')) {
      for (const p of c.querySelectorAll('.se-text-paragraph')) {
        const v = (p.innerText || '').replace(/\\u200B/g, '').trim();
        if (v) out.push({t: 'text', v});
      }
    } else if (c.classList.contains('se-image')) {
      const img = c.querySelector('img');
      let n = '';
      try { n = JSON.parse(img.getAttribute('data-linkdata') || '{}').fileName || ''; }
      catch (e) {}
      out.push({t: 'img', v: n});
    } else if (c.classList.contains('se-horizontalLine')) {
      out.push({t: 'hr', v: ''});
    } else if (c.classList.contains('se-table')) {
      out.push({t: 'table', v: String(c.querySelectorAll('tr').length)});
    } else if (c.classList.contains('se-quotation')) {
      out.push({t: 'quote', v: (c.innerText || '').trim()});
    }
  }
  return out;
}"""

def _norm(s):
    return " ".join((s or "").replace("​", "").replace(" ", " ").split())

def check_order(fr, md_path):
    """수정본 md 의 블록 나열과 에디터 안 나열을 순서까지 맞춰본다."""
    from md_parser import parse as _parse
    want = []
    for k, v in _parse(md_path)["blocks"]:
        if k == "text":    want.append(("text", _norm(v.replace("**", ""))))
        elif k == "img":   want.append(("img", v[0]))
        elif k == "hr":    want.append(("hr", ""))
        elif k == "table": want.append(("table", str(len(v))))
        elif k == "quote": want.append(("quote", _norm(v)))
        # 링크와 해시태그는 에디터에서 그냥 문단이다. 여기서 안 세면
        # md 쪽 블록이 모자라서 멀쩡한 글에도 "블록순서" 실패가 뜬다.
        elif k == "link":  want.append(("text", _norm((v[1] + v[2]).replace("**", ""))))
        elif k == "tags":  want.append(("text", _norm(v)))
    have = [(b["t"], _norm(b["v"]) if b["t"] != "img" else b["v"])
            for b in fr.evaluate(JS_OUTLINE)]
    # 사진은 에디터에서 파일명을 못 읽는 경우가 있다. 못 읽으면 비교에서 뺀다.
    if all(not v for t, v in have if t == "img"):
        want = [(t, "" if t == "img" else v) for t, v in want]
    log("    수정본 %d블록 / 에디터 %d블록" % (len(want), len(have)))
    ops = [x for x in difflib.SequenceMatcher(None, want, have).get_opcodes()
           if x[0] != "equal"]
    for tag, i1, i2, j1, j2 in ops:
        log("    !! %s  md[%d:%d] <-> 에디터[%d:%d]" % (tag, i1, i2, j1, j2))
        for t, v in want[i1:i2]: log("       기대 [%s] %s" % (t, v[:52]))
        for t, v in have[j1:j2]: log("       실제 [%s] %s" % (t, v[:52]))
    return not ops

def main(spec_path, dry):
    spec = json.loads(io.open(spec_path, encoding="utf-8").read())
    url = ("https://blog.naver.com/PostWriteForm.naver"
           "?blogId=%s&logNo=%s&redirect=Update"
           % (spec["blog_id"], spec["post_no"]))
    log("글번호 %s / 작업 %d건%s\n" % (spec["post_no"], len(spec["ops"]),
                                      "  [DRY RUN — 고치지 않음]" if dry else ""))

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE, channel="chrome", headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1400, "height": 950})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        fr = get_editor_frame(page, log=log)
        log("에디터 준비 완료")

        cur = (fr.locator(".se-documentTitle").inner_text() or "").strip()
        log("현재 제목: %s" % cur)
        if spec.get("title_old") and cur.replace("​", "") != spec["title_old"]:
            log("\n!! 열린 글의 제목이 원본과 다릅니다. 글번호를 확인하세요.")
            log("   기대: %s" % spec["title_old"])
            while not page.is_closed(): time.sleep(2)
            return
        log("원본 제목 확인됨\n")

        fail = []
        # 본문을 먼저 고치고 제목은 마지막에 — 제목이 앵커 검증 기준이라서다.
        for n, o in enumerate(spec["ops"], 1):
            log("[%d/%d] %s" % (n, len(spec["ops"]), o["type"]))
            try:
                ok = HANDLERS[o["type"]](page, fr, o, dry)
            except LookupError as e:
                ok = False; log("    !! %s" % e)
            log("    %s" % ("확인" if ok else "!! 실패 — 직접 확인 필요"))
            if not ok:
                fail.append("%d. %s" % (n, o["type"]))
                if not dry:
                    log("\n!! 한 건이라도 어긋나면 이어서 고치지 않습니다.")
                    break
            time.sleep(0.4)

        if not fail and not dry:
            log("\n[제목] 교체")
            fr.locator(".se-documentTitle").click(click_count=3); time.sleep(0.5)
            page.keyboard.press("Control+a"); time.sleep(0.2)
            type_text(page, spec["title"], delay=10)
            time.sleep(0.6)
            got = (fr.locator(".se-documentTitle").inner_text() or "").strip()
            log("    %s" % got)
            if got.replace("​", "") != spec["title"]:
                fail.append("제목")

            md = spec.get("revised_md")
            if md and os.path.exists(md):
                log("\n[순서] 블록 나열 대조")
                if check_order(fr, md):
                    log("    확인 — 순서·내용 완전 일치")
                else:
                    fail.append("블록순서")
            else:
                log("\n[순서] 건너뜀 — ops.json 에 revised_md 경로가 없습니다")

        page.screenshot(path=os.path.join(BASE, "update_result.png"), full_page=True)
        log("\n" + "=" * 56)
        if dry:
            log("DRY RUN 끝 — 앵커 %d건 중 %d건 실패" % (len(spec["ops"]), len(fail)))
        elif fail:
            log("실패 %d건: %s" % (len(fail), ", ".join(fail)))
            log("저장하지 말고 창에서 직접 확인하세요.")
        else:
            log("텍스트 교체 완료 — 사진은 건드리지 않았습니다.")
            log("저장도 발행도 하지 않았습니다.")
            log("")
            log("  다 확인하신 뒤 [발행] 버튼을 눌러 주세요.")
            log("  누르신 다음 '발행했어, 검토해줘' 라고 알려주시면")
            log("  발행된 글을 다시 읽어 수정본과 한 번 더 대조하겠습니다.")
            log("")
            log("  (직접 돌리실 때: python verify_published.py \"%s\")" % spec_path)
        log("=" * 56)
        if dry:                       # 프로필을 붙잡고 있으면 본 실행이 막힌다
            ctx.close(); log("DRY RUN 이므로 창을 닫습니다.")
            return
        while not page.is_closed():
            time.sleep(2)
        log("창이 닫혔습니다.")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--dry"]
    if not a:
        sys.exit("사용: python update_text.py <ops.json> [--dry]")
    main(a[0], "--dry" in sys.argv[1:])
