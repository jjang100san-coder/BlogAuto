# -*- coding: utf-8 -*-
r"""초안 검사 — 마스터 지침 2-11 (2026-10-12 본인 지시: 「강제해」).

초안은 작업 메모의 「🧭 지침 경유표」를 다 채우고, 아래 검사를 통과해야 끝난 것이다.
fill_editor.py 는 새 글을 넣기 전에 이 검사를 부르고, 실패하면 실행하지 않는다.

사용:  python draft_lint.py <초안.md> [<초안2.md> ...]
결과:  ❌ 실패(자동 입력 막힘) / ⚠ 경고(알리고 진행). 실패가 하나라도 있으면 종료 코드 1.

검사 항목(마스터 절):
  ❌ 구조   — [[TITLE:]]·[[CATEGORY:]]·경계선 두 줄 (템플릿 1·2-1)
  ❌ 2-11  — 「🧭 지침 경유표」 표가 있고 모든 칸이 채워져 있다(빈칸·…·□·TODO 금지)
  ❌ 10-8  — 제목 검색어 점검표(「월 검색량」 머리글이 있는 표)가 작업 메모에 있다
  ❌ 10-6  — 제목에 구분선 「|」, 뒤 문장이 있다
  ❌ 2-10  — 본문 2,000자 이상(공백·표·마커·태그 제외)
           · 인포그래픽 예외(2026-10-12): 캡션에 「직접 만든 그림」「직접 만든 도해」「인포그래픽」이 있는 IMG 가 3장 이상이면 면제
  ❌ 2장   — 본문에 마크다운 헤딩·목록·코드블록·[텍스트](url) 링크 없음, 표 3열 이하
  ❌ 5-1   — [[IMG:]] 는 단독 줄, 파일이 images 폴더(또는 초안 폴더)에 실제로 있다
  ❌ 2-7   — 해시태그 8~10개
  ❌ 2-11  — 제목 숫자 대조: 제목에 쓴 숫자가 본문에 그대로(또는 반올림 전 값으로) 있다 (2026-10-12 추가)
  ⚠ 4-1   — 섹션마다 볼드 1~2개
  ⚠ 10-8 규칙 4 — 앞 검색어 낱말이 파이프 뒤에서 되풀이되는지
  ⚠ 3-1   — 쉬는 말(metaphor_words.json rest)이 본문에 2번 이상 + 장부: 지켜보는 말을 이 글·최근 글들이 함께 많이 씀 (2026-10-16 추가, 말 그대로의 뜻일 수 있어 경고만)
  ❌/⚠ 2-7-1 — 말투 리듬(2026-10-19, 「TTS 같다」 피드백 · 같은 날 강제: 경유표 「말투」 칸 + 아래 핵심 넷 ❌, 나머지 ⚠): 「~어./~야.」 50% 넘음 · 같은 끝맺음 3연속 3곳 이상 · 질문 부족 · 12자 이하 8% 미만 · 숫자 3개 이상 든 문장(날짜는 하나로) · 「그런데·그래서」 첫머리 · 정형구
"""
import io, os, re, sys
try:
    import sys as _sys; _sys.stdout.reconfigure(encoding='utf-8'); _sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

SEP_A = "===== ✂️ 여기부터 복사 ====="
SEP_B = "===== ✂️ 여기까지 ====="
PASS_ROWS = ("분야 지침", "유입 꼴", "10-8 점검표", "10-6 ① 앞 검색어", "10-6 ② 내 숫자·장면",
             "10-6 ③ 꼴", "10-6 ④ 첫 문단의 답", "16-3 검색 화면", "제목 숫자 대조", "사실·숫자·영상", "썸네일", "말투", "발행 전 검증")
EMPTY = re.compile(r"^\s*(|…|\.\.\.|□|-|TODO|todo|미정|\(.*채울.*\))\s*$")
TEMPLATE_PH = ("어느 지침의 몇 장을 봤나", "검색형 / 홈판형 + 이유", "날짜 · 씨앗 · 고른 앞 검색어", "고른 말 (+ 소주제 명사는",
               "내가 재거나 본 것 하나", "발견형 / 질문형(10-5: 누를 사람", "제목이 약속한 답이 첫 문단 어디에",
               "직접 계산 숫자 여부 · 영상 인용은", "무엇을, 왜", "①요약+궁금증 ○/△/✕", "전체 글 목록에 같은 글 없음 · 하루 발행 수",
               "날짜 · 앞 검색어로 실제 블로그 탭 상위 글", "제목의 숫자마다 본문 표의 원래 값")


def body_text_len(body):
    t = re.sub(r"\[\[[^\]]*\]\]", "", body)
    t = re.sub(r"^\|.*\|\s*$", "", t, flags=re.M)
    t = re.sub(r"^---\s*$", "", t, flags=re.M)
    t = re.sub(r"#\S+", "", t)
    return len(re.sub(r"\s", "", t))


def find_img_dirs(md):
    # fill_editor.pick_img_dir 와 같은 범위를 본다 — 초안 폴더 + 하위 2단계(클로드·photos·사진 폴더 등).
    # 2026-10-12: 처음엔 images/img/photos 만 봐서 「클로드\」 에 사진을 둔 초안이 전부 ❌(파일 없음)로 막혔다.
    d = os.path.dirname(os.path.abspath(md))
    out = [os.path.join(d, "images"), d, os.path.join(d, "img"), os.path.join(d, "photos")]
    try:
        for n in sorted(os.listdir(d)):
            d1 = os.path.join(d, n)
            if not os.path.isdir(d1): continue
            out.append(d1)
            try:
                out += [os.path.join(d1, m) for m in sorted(os.listdir(d1)) if os.path.isdir(os.path.join(d1, m))]
            except OSError:
                pass
    except OSError:
        pass
    return out


STOCK = ("셈이야", "셈이고", "답부터 말하면", "이 글은", "따라가 봐", "직접 세어 봤", "한번 볼게", "정리해 볼게")


def tone_sentences(body):
    """본문 문장만 — IMG·태그·구분선·표·소제목 줄(이모지로 시작) 제외."""
    keep = []
    for line in body.splitlines():
        st = line.strip()
        if not st or st.startswith(("[[", "#", "|", "---", "=====")): continue
        if re.match(r"^[^\w「『(\[]", st) and len(st) < 60: continue   # 이모지 소제목
        keep.append(st.replace("**", ""))
    return [x.strip() for x in re.split(r"(?<=[.?!])\s+", " ".join(keep)) if len(x.strip()) >= 2]


def tone_check(body):
    """2-7-1 말투 리듬 (2026-10-19 본인 지시 — 지인 피드백 「TTS 같다」, 같은 날 「모든 글에 강하게」).
    핵심 넷(끝맺음 쏠림·3연속·질문·짧은 문장)은 ❌, 나머지(숫자·이음새·정형구)는 ⚠."""
    f, w = [], []
    ss = tone_sentences(body)
    if len(ss) < 15: return f, w
    last = [re.sub(r"[.?!」』\")]+$", "", s)[-1:] for s in ss]
    flat = sum(1 for s in ss if re.search(r"(어|야)\.$", s))
    if flat / len(ss) > 0.5:
        f.append("2-7-1: 「~어./~야.」 끝맺음 %d%% — 50%% 아래로(~더라·~거든·~잖아·~네·질문·명사 끝을 섞는다)" % round(flat / len(ss) * 100))
    runs = sum(1 for i in range(len(ss) - 2) if ss[i][-1] == ss[i + 1][-1] == ss[i + 2][-1] == "." and last[i] == last[i + 1] == last[i + 2])
    if runs >= 3: f.append("2-7-1: 같은 끝맺음 세 번 연달아 %d곳 — 셋째 문장의 끝을 바꾼다" % runs)
    q = sum(s.endswith("?") for s in ss)
    if q < max(2, len(ss) // 60): f.append("2-7-1: 질문 %d번(문장 %d개) — 소제목마다 독자에게 묻는 문장을 하나쯤" % (q, len(ss)))
    short = sum(len(s) <= 12 for s in ss)
    if short / len(ss) < 0.08: f.append("2-7-1: 12자 이하 짧은 문장 %d%% — 8%% 넘게(문단마다 한마디)" % round(short / len(ss) * 100))
    undate = lambda s: re.sub(r"(\d{4}년\s*)?\d{1,2}월\s*\d{1,2}일|\d{4}[.-]\d{1,2}[.-]\d{1,2}|\d{4}-\d{2}", "D", s)   # 날짜는 숫자 하나로
    many = [s for s in ss if len(re.findall(r"(?<![가-힣A-Za-z\d])\d[\d,.]*|D", undate(s))) >= 3]   # 「김연경2」 같은 이름 속 숫자는 빼고
    if many: w.append("2-7-1: 숫자 세 개 이상 든 문장 %d개 — 한 문장에 숫자 두 개까지(예: 「%s…」)" % (len(many), many[0][:24]))
    heads = sum(1 for s in ss if s.startswith(("그런데 ", "그래서 ")))
    if heads > max(3, len(ss) // 25): w.append("2-7-1: 문장 첫머리 「그런데·그래서」 %d번 — 빼거나 「근데·그러고 보니」로" % heads)
    st = [k for k in STOCK if body.count(k) >= 1]
    if len(st) >= 2: w.append("2-7-1: 정형구 %s — 돌려 쓴다" % "·".join("「%s」" % k for k in st))
    return f, w


def lint(md):
    fail, warn = [], []
    s = io.open(md, encoding="utf-8").read()
    if SEP_A not in s or SEP_B not in s:
        return ["구조: 경계선 두 줄이 없다(템플릿 1)"], warn
    head, rest = s.split(SEP_A, 1)
    body, memo = rest.split(SEP_B, 1)
    m = re.search(r"\[\[TITLE:\s*(.+?)\]\]", head)
    if not m: fail.append("구조: [[TITLE:]] 없음")
    if "[[CATEGORY:" not in head: fail.append("구조: [[CATEGORY:]] 없음")
    title = m.group(1).strip() if m else ""

    # 2-11 지침 경유표
    if "🧭 지침 경유표" not in memo:
        fail.append("2-11: 작업 메모에 「🧭 지침 경유표」가 없다 — 템플릿 5절 표를 붙이고 채운다")
    else:
        seg = memo.split("🧭 지침 경유표", 1)[1]
        rows = {}
        for line in seg.splitlines()[1:60]:
            if line.startswith("## ") or line.startswith("# "): break
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 2 and not set(c[0]) <= set("-: "): rows[c[0]] = "|".join(c[1:])
        for k in PASS_ROWS:
            v = next((rows[r] for r in rows if r.startswith(k)), None)
            if v is None: fail.append("2-11: 경유표 「%s」 칸이 없다" % k)
            elif EMPTY.match(v): fail.append("2-11: 경유표 「%s」 칸이 비어 있다" % k)
            elif any(v.startswith(ph) for ph in TEMPLATE_PH): fail.append("2-11: 경유표 「%s」 칸이 템플릿 설명 그대로다 — 이 글 내용으로 채운다" % k)
            elif k == "썸네일":   # 5-4 세 질문 (2026.10.15)
                marks = {n: re.search(n + r"\s*([○△✕xX])", v) for n in ("①", "②", "③")}
                miss = [n for n, mm in marks.items() if not mm]
                if miss: fail.append("5-4: 경유표 「썸네일」 칸에 세 질문 답이 없다(%s) — `①○ ②○ ③○ — 무엇을, 왜` 꼴로" % "".join(miss))
                else:
                    bad = [n for n, mm in marks.items() if mm.group(1) in "✕xX"]
                    if bad: fail.append("5-4: 썸네일 세 질문 중 %s 가 ✕ — 대표 이미지를 바꾼다" % "".join(bad))
                    tri = [n for n, mm in marks.items() if mm.group(1) == "△"]
                    if tri: warn.append("5-4: 썸네일 %s △ — 이유를 칸에 적었는지 확인" % "".join(tri))

    # 10-8 점검표
    if not re.search(r"^\s*\|\s*말\s*\|\s*월 검색량", memo, re.M):
        fail.append("10-8: 제목 검색어 점검표(title_check.py --md 표)가 작업 메모에 없다")

    # 10-6 제목 꼴
    if title and "|" not in title:
        fail.append("10-6: 제목에 구분선 「|」 와 뒤 문장이 없다")
    elif title:
        front, back = [x.strip() for x in title.split("|", 1)]
        if not back: fail.append("10-6: 구분선 뒤 문장이 비어 있다")
        toks = [w for w in re.findall(r"[가-힣A-Za-z0-9]{2,}", front)]
        rep = [w for w in toks[:2] if w in back]
        if rep: warn.append("10-8 규칙 4: 앞 검색어 「%s」 가 구분선 뒤에서 되풀이된다" % "·".join(rep))

    # 2-11 제목 숫자 대조 — 제목 숫자는 본문 숫자와 같거나 그 반올림이어야 한다(0-5·10-6 ④, 10/12 사용자 지시)
    if title:
        num = lambda x: float(x.replace(",", ""))
        body_nums = [num(x) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", body)]
        for tok in re.finditer(r"(?<![\d.,])(\d[\d,]*(?:\.\d+)?)(?![\d.,])(?!\s*[천만억])", title):
            t = num(tok.group(1))
            if any(abs(b - t) < 1e-9 or (t == int(t) and int(b + 0.5) == int(t) and b != int(b)) for b in body_nums):
                continue
            fail.append("2-11: 제목 숫자 「%s」 가 본문에 없다 — 본문 표의 원래 값과 반올림이 맞는지 본다" % tok.group(1))

    # 2-10 분량 — 인포그래픽 카드(캡션 「직접 만든 그림·도해」「인포그래픽」) 3장 이상이면 면제 (마스터 2-10, 2026-10-12)
    n = body_text_len(body)
    caps = re.findall(r"\[\[IMG:[^|\]]*\|([^\]]*)\]\]", body)
    cards = sum(1 for c in caps if re.search(r"직접 만든 (?:그림|도해)|인포그래픽", c))
    if n < 2000:
        if cards >= 3: warn.append("2-10 인포그래픽 예외 적용 — 카드 %d장, 본문 %d자 (❌ 아님, 알림)" % (cards, n))
        else: fail.append("2-10: 본문 %d자 — 2,000자 이상이어야 한다 (인포그래픽 카드 %d장, 3장 이상이면 면제)" % (n, cards))

    # 2장 금지 서식·표
    for i, line in enumerate(body.splitlines(), 1):
        st = line.strip()
        if re.match(r"^#{1,6}\s", st): fail.append("2장: 본문 %d줄 마크다운 헤딩 「%s」" % (i, st[:20]))
        if re.match(r"^[-*]\s+\S", st) and st != "---": fail.append("2장: 본문 %d줄 마크다운 목록 「%s」" % (i, st[:20]))
        if st.startswith("```"): fail.append("2장: 본문 %d줄 코드블록" % i)
        if re.search(r"\[[^\[\]]+\]\(https?://", st): fail.append("2장: 본문 %d줄 마크다운 링크(LINK 마커를 쓴다)" % i)
        if st.startswith("|") and st.endswith("|") and not set(st) <= set("|-: "):
            if st.count("|") - 1 > 3: fail.append("2장: 본문 %d줄 표가 3열을 넘는다" % i)
        if "[[IMG:" in st and not (st.startswith("[[IMG:") and st.endswith("]]")):
            fail.append("5-1: 본문 %d줄 IMG 마커가 단독 줄이 아니다" % i)

    # 5-1 이미지 파일
    for fn in re.findall(r"\[\[IMG:\s*([^|\]]+?)\s*(?:\||\]\])", body):
        if not any(os.path.exists(os.path.join(d, fn)) for d in find_img_dirs(md)):
            fail.append("5-1: 이미지 파일이 없다 — %s" % fn)

    # 2-7 태그
    tags = re.findall(r"(?<![\w&])#[^\s#]+", "\n".join(l for l in body.splitlines()[-6:]))
    if not 8 <= len(tags) <= 10: fail.append("2-7: 해시태그 %d개 — 8~10개" % len(tags))

    # 4-1 볼드
    for k, sec in enumerate(re.split(r"\n---\n", body)):
        b = sec.count("**") // 2
        name = sec.strip().splitlines()[0][:16] if sec.strip() else "(빈 섹션)"
        if sec.strip().startswith("#") or "[[LINK:" in sec and b == 0 and len(sec) < 400: continue
        if b == 0 and body_text_len(sec) > 150: warn.append("4-1: 「%s」 섹션에 볼드가 없다" % name)
        if b > 2: warn.append("4-1: 「%s」 섹션 볼드 %d개 — 1~2개" % (name, b))
    # 3-1 쉬는 말 — 같은 비유를 글마다 돌려 쓰지 않는다 (2026-10-16 본인 지시). 말 그대로의 뜻일 수 있어 ⚠ 만
    plain = "\n".join(l for l in body.splitlines() if not l.strip().startswith("[[IMG:") and not l.strip().startswith("#"))
    rest_words = {
        "문": r"(?<![가-힣])문(?:을|이|은|에|에서|으로|의|도|만|과|셋|넷|둘|들)?(?![가-힣])",
        "칸": r"칸(?!쿤)",
        "계단": r"계단",
        "뚜껑": r"뚜껑",
    }
    rest_n = 2
    try:   # 말 목록은 metaphor_words.json 이 원본(마스터 3-1 장부, 10/16) — 없으면 위 기본값
        import json
        _W = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "metaphor_words.json"), encoding="utf-8"))
        rest_words, rest_n = _W["rest"], _W.get("rest_per_post", 2)
    except Exception:
        pass
    for w, pat in rest_words.items():
        k = len(re.findall(pat, plain))
        if k >= rest_n: warn.append("3-1: 쉬는 말 「%s」 본문 %d번 — 비유면 바꾼다(한 글에 한 번까지), 말 그대로의 뜻이면 그대로" % (w, k))
    _tf, _tw = tone_check(body); fail.extend(_tf); warn.extend(_tw)
    try:   # 3-1 장부: 이 글에서 많이 쓴 지켜보는 말이 최근 글들에서도 많이 쓰였는지
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import metaphor_ledger
        warn.extend(metaphor_ledger.draft_check(md))
    except Exception as e:
        warn.append("3-1 장부: 확인 못 함(%s)" % e.__class__.__name__)
    return fail, warn


def main(paths):
    bad = 0
    for p in paths:
        f, w = lint(p)
        print("\n■ %s" % p)
        for x in f: print("  ❌ " + x)
        for x in w: print("  ⚠ " + x)
        if not f and not w: print("  ✅ 통과")
        elif not f: print("  ✅ 통과(경고만)")
        bad += bool(f)
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit("사용: python draft_lint.py <초안.md> [...]")
    sys.exit(main(sys.argv[1:]))
