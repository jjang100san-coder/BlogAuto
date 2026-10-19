# -*- coding: utf-8 -*-
"""발행된 글을 다시 읽어 수정본 md 와 대조한다. 아무것도 고치지 않는다.

update_text.py 는 에디터 DOM 만 보고 검증하므로, 저장이 실제로 반영됐는지는
확인하지 못한다. 이 스크립트는 사용자가 [수정] 을 누른 뒤 발행된 글을 직접
열어서 본문 블록을 순서까지 맞춰본다.

사용:
    python verify_published.py <ops.json>

읽기 전용이다. 로그인도 필요 없다(공개 글이라 빈 브라우저로 연다).
몇 번을 돌려도 글에 영향이 없다.
"""
import sys, os, io, json, time, difflib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from md_parser import parse

BASE = os.path.dirname(os.path.abspath(__file__))

def log(m): print(m); sys.stdout.flush()

def norm(s):
    s = (s or "").replace("​", "").replace(" ", " ")
    return " ".join(s.split()).strip()

# 발행 화면의 본문을 컴포넌트 순서대로 훑는다. 캡션은 본문 문단이 아니라서 뺀다.
JS_BLOCKS = """() => {
  const box = document.querySelector('.se-main-container');
  if (!box) return null;
  const out = [];
  for (const c of box.querySelectorAll(':scope > .se-component')) {
    if (c.classList.contains('se-text')) {
      for (const p of c.querySelectorAll('.se-text-paragraph')) {
        out.push({t: 'text', v: p.innerText || ''});
      }
    } else if (c.classList.contains('se-image')) {
      const img = c.querySelector('img');
      let name = '';
      try {
        const d = JSON.parse(img.getAttribute('data-linkdata') || '{}');
        name = d.fileName || '';
      } catch (e) {}
      if (!name && img) {
        name = decodeURIComponent((img.getAttribute('src') || '').split('?')[0]
               .split('/').pop() || '');
      }
      const cap = c.querySelector('.se-caption');
      out.push({t: 'img', v: name, cap: cap ? (cap.innerText || '') : ''});
    } else if (c.classList.contains('se-horizontalLine')) {
      out.push({t: 'hr', v: ''});
    } else if (c.classList.contains('se-table')) {
      out.push({t: 'table', v: String(c.querySelectorAll('tr').length)});
    } else if (c.classList.contains('se-quotation')) {
      out.push({t: 'quote', v: c.innerText || ''});
    }
  }
  // 제목은 감싸는 요소를 잡으면 카테고리·작성일까지 딸려온다. 좁은 것부터 본다.
  let title = '';
  for (const s of ['.se-title-text .se-text-paragraph',
                   '.se-documentTitle .se-text-paragraph',
                   '.se-title-text', '.itemSubjectBoldfont', '.pcol1']) {
    const e = document.querySelector(s);
    const t = e ? (e.innerText || '').trim() : '';
    if (t && t.length < 200) { title = t; break; }
  }
  return {title, blocks: out};
}"""

def expected_blocks(md_path):
    """수정본 md 를 발행 화면과 같은 모양의 블록 목록으로 바꾼다."""
    d = parse(md_path)
    out = []
    for k, v in d["blocks"]:
        if k == "text":
            out.append(("text", norm(v.replace("**", ""))))
        elif k == "img":
            out.append(("img", v[0]))
        elif k == "hr":
            out.append(("hr", ""))
        elif k == "table":
            out.append(("table", str(len(v))))
        elif k == "quote":
            out.append(("quote", norm(v)))
        elif k == "link":
            # 링크는 발행 화면에서 그냥 문단이다. 안 세면 멀쩡한 글도 블록수가 하나 모자란다.
            out.append(("text", norm((v[1] + v[2]).replace("**", ""))))
        # tags 는 일부러 세지 않는다 — 네이버는 해시태그를 .se-main-container
        # 바깥에 렌더링해서 발행 블록 목록에 안 들어온다. 여기서 세면 도리어 어긋난다.
        elif k == "tags":
            out.append(("text", norm(v)))   # 해시태그 줄도 본문 문단으로 발행된다
        # blank 만 뺀다
    return d, out

def read_published(blog_id, post_no):
    url = "https://blog.naver.com/%s/%s" % (blog_id, post_no)
    log("여는 중: %s" % url)
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)      # 프로필 안 씀 - 에디터 창과 안 부딪힌다
        pg = br.new_context(viewport={"width": 1280, "height": 900}).new_page()
        pg.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        got = None
        for _ in range(10):                        # 본문은 iframe#mainFrame 안에 있다
            for f in pg.frames:
                try:
                    r = f.evaluate(JS_BLOCKS)
                except Exception:
                    r = None
                if r and r["blocks"]:
                    got = r; break
            if got: break
            time.sleep(2)
        br.close()
    if not got:
        raise RuntimeError("본문을 읽지 못했습니다. 글이 공개 상태인지 확인하세요.")
    return got

def main(spec_path):
    spec = json.loads(io.open(spec_path, encoding="utf-8").read())
    md = spec.get("revised_md")
    if not md or not os.path.exists(md):
        sys.exit("ops.json 의 revised_md 경로가 없습니다: %r" % md)
    d, want = expected_blocks(md)

    got = read_published(spec["blog_id"], spec["post_no"])
    # 발행 화면은 블록 사이마다 빈 문단을 하나씩 깔아둔다. md 에는 없으니 뺀다.
    have = [(b["t"], norm(b["v"]) if b["t"] != "img" else b["v"])
            for b in got["blocks"]]
    have = [(t, v) for t, v in have if not (t == "text" and not v)]
    log("")

    fail = []

    # ---------- 1. 제목 ----------
    t_got, t_want = norm(got["title"]), norm(spec["title"])
    log("[1] 제목")
    log("    발행: %s" % t_got)
    if t_got == t_want:
        log("    확인 — 새 제목")
    else:
        log("    !! 다름. 기대: %s" % t_want)
        if t_got == norm(spec.get("title_old", "")):
            log("    (아직 옛 제목입니다 — [수정] 버튼을 안 누르셨을 수 있습니다)")
        fail.append("제목")

    # ---------- 2. 바꾼 문장 개수 ----------
    log("\n[2] 바꾼 문장 개수 (새 문장 1건 / 옛 문장 0건)")
    texts = [v for t, v in have if t == "text"]
    def cnt(s): return sum(1 for x in texts if x == norm(s.replace("**", "")))  # 굵게 표시는 화면 글자에 없다 (2026-10-01)
    moved = {norm(b["v"]) for o in spec["ops"] if o["type"] == "insert_before"
             for b in o["blocks"] if b["t"] == "text"}
    for n, o in enumerate(spec["ops"], 1):
        if o["type"] == "replace":
            a, b = cnt(o["find"]), cnt(o["text"])
            ok = (a == 0 and b == 1)
            log("    %d) 새 %d건 / 옛 %d건  %s  %s"
                % (n, b, a, "확인" if ok else "!!", o["text"][:28]))
            if not ok: fail.append("op%d" % n)
        elif o["type"] == "delete_range":
            # 문단을 '옮기는' 수정이면 지운 문장이 insert 로 다시 들어온다.
            # 그건 0건이 아니라 1건이 맞다. 되살아난 문장은 insert 쪽에서 센다.
            ok = True
            for key in ("from", "to"):
                want_n = 1 if norm(o[key]) in moved else 0
                c = cnt(o[key])
                if c != want_n: ok = False
                log("    %d) 지운 문단 %d건 (기대 %d건)  %s  %s"
                    % (n, c, want_n, "확인" if c == want_n else "!!", o[key][:24]))
            if not ok: fail.append("op%d" % n)
        elif o["type"] == "insert_before":
            for blk in o["blocks"]:
                if blk["t"] != "text": continue
                c = cnt(blk["v"])
                log("    %d) 넣은 문단 %d건  %s  %s"
                    % (n, c, "확인" if c == 1 else "!!", blk["v"][:28]))
                if c != 1: fail.append("op%d" % n)

    # ---------- 3. 블록 순서 ----------
    log("\n[3] 블록 순서 (수정본 md 와 그대로 맞는지)")
    log("    수정본 %d블록 / 발행 %d블록" % (len(want), len(have)))
    diffs = [x for x in difflib.SequenceMatcher(None, want, have).get_opcodes()
             if x[0] != "equal"]
    if not diffs:
        log("    확인 — 순서·내용 완전 일치")
    else:
        for tag, i1, i2, j1, j2 in diffs:
            log("    !! %s  md[%d:%d] <-> 발행[%d:%d]" % (tag, i1, i2, j1, j2))
            for t, v in want[i1:i2]: log("       기대 [%s] %s" % (t, v[:56]))
            for t, v in have[j1:j2]: log("       실제 [%s] %s" % (t, v[:56]))
        fail.append("블록순서")

    # ---------- 4. 사진 ----------
    log("\n[4] 사진 (재업로드 없이 그대로인지)")
    w_img = [v for t, v in want if t == "img"]
    h_img = [v for t, v in have if t == "img"]
    log("    수정본 %d장 / 발행 %d장" % (len(w_img), len(h_img)))
    for i, fn in enumerate(h_img):
        mark = "확인" if i < len(w_img) and fn == w_img[i] else "!!"
        log("    %d. %s  %s" % (i + 1, fn or "(파일명 못 읽음)", mark))
    if len(w_img) != len(h_img) or any(
            i >= len(w_img) or fn != w_img[i] for i, fn in enumerate(h_img)):
        fail.append("사진")

    # ---------- 5. 구분선 ----------
    log("\n[5] 구분선")
    w_hr = sum(1 for t, _ in want if t == "hr")
    h_hr = sum(1 for t, _ in have if t == "hr")
    log("    수정본 %d개 / 발행 %d개  %s" % (w_hr, h_hr, "확인" if w_hr == h_hr else "!!"))
    if w_hr != h_hr: fail.append("구분선")

    log("\n" + "=" * 56)
    if fail:
        log("대조 실패 %d건: %s" % (len(fail), ", ".join(dict.fromkeys(fail))))
        log("발행 화면에서 해당 부분을 직접 확인하세요.")
    else:
        log("대조 완료 — 발행된 글이 수정본과 일치합니다.")
    log("이 스크립트는 글을 고치지 않습니다.")
    log("=" * 56)
    return 1 if fail else 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("사용: python verify_published.py <ops.json>")
    sys.exit(main(sys.argv[1]))
