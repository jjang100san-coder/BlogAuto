# -*- coding: utf-8 -*-
r"""비유·묶음말 장부 — 마스터 3-1 (2026-10-16 본인 지시).

「문」「칸」을 쉬게 하면 그 자리를 「조건」 같은 다른 말이 또 메운다. 그래서 말 목록(metaphor_words.json)의
쉬는 말·지켜보는 말이 최근 글들에서 몇 번 쓰였는지 센다. 목록에 없는 새 반복 후보도 찾는다.

사용:
  python metaphor_ledger.py                 최근 10편 장부를 화면에 + _문서\비유장부\비유장부_<날짜>.md 저장
  python metaphor_ledger.py --draft <초안.md>  이 초안의 말을 최근 10편과 나란히(저장 안 함)
  python metaphor_ledger.py --window 20      창 크기 바꾸기

세는 곳: 초안 본문(경계선 안, IMG 줄·해시태그 줄 제외) + 같은 폴더(또는 위 폴더)의 *_그림으로.html 글자(도해).
숫자는 말 그대로의 뜻(실제 문·표의 칸)도 함께 센 원래 횟수다 — 비유인지는 사람이 본다.
새 후보: 「○○ 셋/넷」 묶음, 「○○처럼」, 「○○라고 치면」 앞의 말을 모아, 창 안에서 3편 이상 나온 것.
"""
import io, os, re, sys, json, glob, argparse, datetime as dt
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # _1.컨텐츠
BLOG = os.path.dirname(ROOT)
OUT_DIR = os.path.join(BLOG, "_문서", "비유장부")
SEP_A = "===== ✂️ 여기부터 복사 ====="
SEP_B = "===== ✂️ 여기까지 ====="


def load_words():
    with io.open(os.path.join(HERE, "metaphor_words.json"), encoding="utf-8") as f:
        return json.load(f)


def body_of(md_text):
    if SEP_A in md_text and SEP_B in md_text:
        s = md_text.split(SEP_A, 1)[1].split(SEP_B, 1)[0]
    else:
        s = md_text.split("# 🚧 작업 메모")[0]
    keep = [l for l in s.splitlines() if not l.strip().startswith("[[IMG:") and not l.strip().startswith("#")]
    return "\n".join(keep)


def html_text(p):
    s = io.open(p, encoding="utf-8", errors="ignore").read()
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r'alt="([^"]*)"', r" \1 ", s)                 # 그림 설명도 센다
    s = re.sub(r"<[^>]+>", " ", s)
    return s


def post_date(path):
    for part in reversed(os.path.normpath(path).split(os.sep)):
        m = re.match(r"^(\d{6})", part)
        if m:
            try:
                return dt.datetime.strptime(m.group(1), "%y%m%d").date()
            except ValueError:
                pass
    return dt.date.fromtimestamp(os.path.getmtime(path))


def find_posts():
    seen, posts = set(), []
    pats = ["**/초안_*.md", "**/*_draft.md"]
    for pat in pats:
        for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
            low = p.replace("\\", "/")
            if "/_템플릿/" in low or "/base data/" in low or "/_raw/" in low or "백업" in low or "/_자동화/" in low:
                continue
            if p in seen:
                continue
            seen.add(p)
            posts.append(p)
    return posts


def figure_page(md_path):
    d = os.path.dirname(md_path)
    for dd in (d, os.path.dirname(d)):
        hs = glob.glob(os.path.join(dd, "*_그림으로.html"))
        if hs:
            return hs[0]
    return None


def count(text, words):
    return {w: len(re.findall(p, text)) for w, p in words.items()}


CAND_PATS = [
    r"([가-힣]{1,5}) (?:셋|넷|다섯)(?:은|이|을|으로|만|도)?(?![가-힣])",     # 문 셋, 조건 셋
    r"([가-힣]{1,5})처럼",                                                  # 로켓처럼
    r"([가-힣]{1,5})(?:이)?라고 치면",                                      # 냄비라고 치면
]
CAND_STOP = set("그 이 저 것 수 때 데 곳 거 게 걸 건 뭐 누구 우리 내 나 너 그것 이것 저것 사람 하루 오늘 지금 이번 다음 마지막 처음 모두 전부 아무 둘 셋 넷 혹시 정말 그렇게 이렇게 다른 같은 사실".split())


def candidates(text):
    out = {}
    for pat in CAND_PATS:
        for m in re.finditer(pat, text):
            w = m.group(1)
            if w in CAND_STOP or len(w) < 1:
                continue
            out[w] = out.get(w, 0) + 1
    return out


def analyse(window=None, extra_draft=None):
    W = load_words()
    win = window or W.get("window", 10)
    words = dict(W["rest"]); words.update(W["watch"])
    rows = []
    for p in find_posts():
        try:
            b = body_of(io.open(p, encoding="utf-8", errors="ignore").read())
        except Exception:
            continue
        fp = figure_page(p)
        f = html_text(fp) if fp else ""
        rows.append({"path": p, "date": post_date(p), "mtime": os.path.getmtime(p),
                     "body": count(b, words), "fig": count(f, words) if f else {},
                     "cand": candidates(b + "\n" + f)})
    rows.sort(key=lambda r: (r["date"], r["mtime"]))
    if extra_draft:
        ap = os.path.abspath(extra_draft)
        rows = [r for r in rows if os.path.abspath(r["path"]) != ap]
    recent = rows[-win:]
    return W, words, recent


def tally(W, words, recent):
    out = []
    for w in words:
        per = [(r["body"].get(w, 0) + r["fig"].get(w, 0)) for r in recent]
        posts = sum(1 for x in per if x > 0)
        heavy = sum(1 for x in per if x >= W["watch_per_post"])
        out.append({"word": w, "kind": "쉬는 말" if w in W["rest"] else "지켜보는 말",
                    "posts": posts, "heavy": heavy, "total": sum(per), "per": per})
    out.sort(key=lambda x: (-x["heavy"], -x["total"]))
    cand = {}
    known = set(words)
    for r in recent:
        for w, n in r["cand"].items():
            if w in known:
                continue
            c = cand.setdefault(w, [0, 0]); c[0] += 1; c[1] += n
    cands = sorted([(w, a, b) for w, (a, b) in cand.items() if a >= 3], key=lambda x: (-x[1], -x[2]))
    return out, cands


def name_of(p):
    rel = os.path.relpath(p, ROOT)
    parts = rel.split(os.sep)
    return (parts[-2] if len(parts) >= 2 else "") + "/" + parts[-1].replace("초안_", "").replace(".md", "")


def flag(t, W):
    if t["kind"] == "쉬는 말":
        return "🔴 쉬는 중" if t["total"] else "✅ 쉬는 중"
    if t["heavy"] >= W["watch_posts"]:
        return "🟠 쉬는 말 후보"
    if t["posts"] >= W["watch_posts"]:
        return "🟡 자주 보임"
    return ""


def report(window=None):
    W, words, recent = analyse(window)
    tl, cands = tally(W, words, recent)
    today = dt.date.today().isoformat()
    L = ["# 비유·묶음말 장부 — %s" % today, "",
         "> 마스터 3-1. 최근 %d편(폴더 날짜순) 초안 본문 + 도해 페이지에서 센 원래 횟수 — 말 그대로의 뜻도 섞여 있다. 목록 `_1.컨텐츠\\_자동화\\metaphor_words.json`(%s)." % (len(recent), W["updated"]),
         "> 🟠 쉬는 말 후보 = 한 편에 %d번 이상 쓴 글이 %d편 이상 · 🟡 자주 보임 = %d편 이상에서 보임 · 🔴 쉬는 중인데 아직 보임." % (W["watch_per_post"], W["watch_posts"], W["watch_posts"]), "",
         "## 최근 글", "", "| # | 날짜 | 글 |", "|---|---|---|"]
    for i, r in enumerate(recent, 1):
        L.append("| %d | %s | %s |" % (i, r["date"].strftime("%m/%d"), name_of(r["path"])))
    L += ["", "## 말별 횟수 (편마다: 본문+도해)", "", "| 말 | 종류 | 판정 | 쓴 편 | 많이 쓴 편 | 합계 | " + " | ".join(str(i) for i in range(1, len(recent) + 1)) + " |",
          "|---|---|---|---|---|---|" + "---|" * len(recent)]
    for t in tl:
        if t["total"] == 0 and t["kind"] != "쉬는 말":
            continue
        L.append("| %s | %s | %s | %d | %d | %d | %s |" % (t["word"], t["kind"], flag(t, W), t["posts"], t["heavy"], t["total"], " | ".join(str(x) if x else "·" for x in t["per"])))
    L += ["", "## 목록 밖 새 반복 후보 (「○○ 셋」「○○처럼」「○○라고 치면」, 3편 이상)", ""]
    if cands:
        L += ["| 말 | 나온 편 | 합계 |", "|---|---|---|"] + ["| %s | %d | %d |" % c for c in cands[:20]]
    else:
        L.append("없음")
    L += ["", "→ 🟠·새 후보는 사용자에게 보여 주고, 쉬는 말로 올릴지·지켜보는 말에 넣을지 정한다(마스터 3-1). 정하면 json 과 마스터 3-1 기록 표를 같이 고친다."]
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "비유장부_%s.md" % today)
    io.open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print("\n(저장: %s)" % out)


def draft_check(md, window=None):
    """draft_lint 가 부른다: 이 초안에서 많이 쓴 지켜보는 말이 최근 글에서도 많이 쓰였으면 경고 문장 목록."""
    W, words, recent = analyse(window, extra_draft=md)
    b = body_of(io.open(md, encoding="utf-8").read())
    fp = figure_page(md)
    f = html_text(fp) if fp else ""
    mine = count(b + "\n" + f, W["watch"])
    warns = []
    for w, n in mine.items():
        if n < W["watch_per_post"]:
            continue
        others = sum(1 for r in recent if r["body"].get(w, 0) + r["fig"].get(w, 0) >= W["watch_per_post"])
        if others + 1 >= W["watch_posts"]:
            warns.append("3-1 장부: 「%s」 이 글 %d번(본문+도해), 최근 %d편 중 %d편도 많이 씀 — 돌려 쓰는 말이 되고 있다, 맨말·이 글의 사물로" % (w, n, len(recent), others))
    return warns


def summary(window=None):
    """월요일 아침 보고용 짧은 글(카톡 --text, 마크다운 없음). 장부 md 도 같이 저장한다."""
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        report(window)
    W, words, recent = analyse(window)
    tl, cands = tally(W, words, recent)
    orange = [t for t in tl if t["kind"] != "쉬는 말" and t["heavy"] >= W["watch_posts"]]
    yellow = [t for t in tl if t["kind"] != "쉬는 말" and t["heavy"] < W["watch_posts"] and t["posts"] >= W["watch_posts"]]
    red = [t for t in tl if t["kind"] == "쉬는 말" and t["total"]]
    fmt = lambda t: "%s %d편%d회" % (t["word"], t["posts"], t["total"])
    L = ["[비유 장부] 최근 %d편 %s~%s" % (len(recent), recent[0]["date"].strftime("%m/%d"), recent[-1]["date"].strftime("%m/%d"))]
    L.append("쉬는 말 후보: " + (", ".join(fmt(t) for t in orange[:3]) if orange else "없음"))
    if yellow: L.append("자주 보임: " + ", ".join(fmt(t) for t in yellow[:3]))
    if red: L.append("쉬는 중인데 보임: " + ", ".join(fmt(t) for t in red[:3]))
    if cands: L.append("목록 밖 새 후보: " + ", ".join("%s %d편" % (w, a) for w, a, b in cands[:3]))
    if orange or cands:
        L.append("→ 쉬는 말로 올릴지 정해 주세요 (마스터 3-1)")
    else:
        L.append("→ 바꿀 것 없음")
    s = "\n".join(L)
    return s if len(s) <= 195 else s[:192] + "…"   # 카톡 글 200자 제한(kakao_send)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft")
    ap.add_argument("--window", type=int)
    ap.add_argument("--summary", action="store_true", help="월요일 아침 보고용 짧은 글")
    a = ap.parse_args()
    if a.summary:
        print(summary(a.window))
    elif a.draft:
        W, words, recent = analyse(a.window, extra_draft=a.draft)
        b = body_of(io.open(a.draft, encoding="utf-8").read())
        fp = figure_page(a.draft)
        f = html_text(fp) if fp else ""
        mine = count(b + "\n" + f, words)
        tl, _ = tally(W, words, recent)
        print("말 | 이 글 | 최근 %d편 중 쓴 편 | 합계" % len(recent))
        for t in tl:
            if mine.get(t["word"]) or t["total"]:
                print("%s | %d | %d | %d %s" % (t["word"], mine.get(t["word"], 0), t["posts"], t["total"], flag(t, W)))
        for x in draft_check(a.draft, a.window):
            print("⚠ " + x)
    else:
        report(a.window)
