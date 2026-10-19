# -*- coding: utf-8 -*-
r"""금메달 시리즈 관리표 만들기 — python series_check.py [--no-kbl]

입력: 금메달시리즈_설정.json (상태·발행일·링크·메모만 손으로)
출력: 금메달시리즈_관리표.md (매번 새로 씀)
자동으로 보는 것:
  · 제목(초안 TITLE) · draft_lint 결과 · 썸네일 세 질문 칸 · 카드 양식(_카드생성.py 가 basketball_cards_base 를 쓰는지)
  · 「다음 편은」 예고 · 본문 경기 표의 마지막 날짜 vs KBL 최신 경기일(kbl_gamelog API)
  · 발행된 편 링크가 초안 도입부에 다 들어 있는지
발행된 편(상태=발행)은 고치지 않는다 — 점검만 하고 「발행본」으로 표시(지침 6-0: 발행된 1~3편 카드는 다시 그리지 않음)."""
import json, os, re, subprocess, sys, urllib.request, datetime
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.dirname(os.path.dirname(HERE))
LINT = os.path.join(BLOG, "_1.컨텐츠", "_자동화", "draft_lint.py")
sys.path.insert(0, os.path.dirname(LINT))
import draft_lint as _dl


def tone(s):
    """마스터 2-7-1 말투 — 「~어/~야」 비율 · 질문 수 · 짧은 문장 비율 (10/19 강제)."""
    try:
        body = s.split(_dl.SEP_A, 1)[1].split(_dl.SEP_B, 1)[0]
        ss = _dl.tone_sentences(body)
        flat = sum(1 for x in ss if re.search(r"(어|야)\.$", x))
        q = sum(x.endswith("?") for x in ss); short = sum(len(x) <= 12 for x in ss)
        return f"{round(flat / len(ss) * 100)}%·질문{q}·짧은{round(short / len(ss) * 100)}%"
    except Exception:
        return "?"
API = "https://kbl-api.sports2i.com/api/v1/players/categories/game/49/48/"
HDR = {"Referer": "https://www.kbl.or.kr/", "Origin": "https://www.kbl.or.kr", "User-Agent": "Mozilla/5.0"}


def kbl_last(pno):
    try:
        req = urllib.request.Request(API + pno, headers=HDR)
        g = json.loads(urllib.request.urlopen(req, timeout=20).read().decode("utf-8")).get("RegularGameRecords", [])
        return max((x["gameDate"] for x in g), default="")
    except Exception as e:
        return "ERR"


def lint(path):
    r = subprocess.run([sys.executable, LINT, path], capture_output=True, text=True, encoding="utf-8", cwd=BLOG)
    out = r.stdout + r.stderr
    if "❌" in out: return "❌", out
    if "⚠" in out: return "⚠", out
    return "✅", out


def body_of(s):
    a = s.find("===== ✂️ 여기부터 복사 =====")
    b = s.find("===== ✂️ 여기까지 =====")
    return s[a:b] if a >= 0 and b > a else s


def last_game_in_body(body):
    today = datetime.date.today()
    # 예정일(복귀 예정 등 오늘 뒤 날짜)은 경기일로 치지 않는다
    days = [int(d) for d in re.findall(r"10월 (\d+)일", body) if (today.month, today.day) >= (10, int(d)) or today.month > 10]
    return f"202610{max(days):02d}" if days else ""


def main():
    cfg = json.load(open(os.path.join(HERE, "금메달시리즈_설정.json"), encoding="utf-8"))
    eps = cfg["편"]; use_kbl = "--no-kbl" not in sys.argv
    published = [e for e in eps if e["상태"] == "발행"]
    rows, detail = [], []
    for e in eps:
        todo = []
        title = lint_mark = thumb = card = nxt = games = tn = "—"
        path = os.path.join(HERE, e["초안"]) if e["초안"] else ""
        if path and os.path.exists(path):
            s = open(path, encoding="utf-8").read(); body = body_of(s)
            m = re.search(r"\[\[TITLE:\s*(.+?)\]\]", s); title = m.group(1).strip() if m else "?"
            if e["상태"] != "발행":
                lint_mark, out = lint(path)
                if lint_mark == "❌": todo.append("lint ❌ 고치기")
                thumb = "①○②○③○" if "①○ ②○ ③○" in s else "✕"
                tn = tone(s)
                if any("2-7-1" in l and "❌" in l for l in out.splitlines()): todo.append("말투 2-7-1 ❌")
                if thumb == "✕": todo.append("썸네일 세 질문 칸")
                cs = os.path.join(os.path.dirname(path), "_카드생성.py")
                card = "코트 카드" if os.path.exists(cs) and "basketball_cards_base" in open(cs, encoding="utf-8").read() else "옛 양식"
                if card != "코트 카드": todo.append("카드를 코트 카드로(지침 6-0)")
                nxt = "있음" if re.search(r"다음 편(은|이자)", body) else "없음"
                if nxt == "없음" and e["no"] != 12: todo.append("마무리 「다음 편」 예고")
                for p in published:
                    if p["링크"] and p["링크"] not in body: todo.append(f"{p['no']}편 링크 추가")
                if e["kbl"] and use_kbl:
                    mine, kb = last_game_in_body(body), kbl_last(e["kbl"])
                    games = "0경기(KBL)" if kb == "" else (f"{mine[4:6]}/{mine[6:]}까지" if mine else "표 없음")
                    if kb and kb != "ERR" and mine and kb > mine:
                        todo.append(f"{kb[4:6]}/{kb[6:]} 경기까지 반영(KBL 최신)")
                    elif kb == "ERR": todo.append("KBL 조회 실패 — 다시")
            else:
                lint_mark, card = "발행본", "옛 양식(발행본·다시 안 그림)"
        elif e["상태"] in ("조사", "보류"):
            todo.append("2차 수집 → 종합분석 → 제목 → 초안")
        if e["메모"]: todo.append(e["메모"])
        rows.append(f"| {e['no']} | {e['선수']} | {e['소속']} | {e['상태']}{(' ' + e['발행일']) if e['발행일'] else ''} | {title.replace('|', '／')} | {lint_mark} | {tn} | {thumb} | {card} | {nxt} | {games} | {' · '.join(todo) if todo else '없음'} |")
    order = " → ".join(f"{n}편" for n in cfg.get("발행_순서", []))
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"""# 농구 금메달 시리즈 관리표

> 자동 생성 {now} · `python _1.컨텐츠\\농구_컨텐츠\\series_check.py` 로 다시 만든다. 손으로 고치는 곳은 `금메달시리즈_설정.json`(상태·발행일·링크·메모)뿐.
> 지침: `지침\\농구카테고리_운영지침.md`. 발행 순서(정해진 것): {order}

| 편 | 선수 | 소속 | 상태 | 제목 | lint | 말투 | 썸네일 | 카드 | 다음 편 예고 | 본문 경기 | 업데이트 필요 |
|---|---|---|---|---|---|---|---|---|---|---|---|
""" + "\n".join(rows) + """

- **본문 경기** = 초안 경기 표의 마지막 날짜. KBL 최신 경기가 더 뒤면 「업데이트 필요」에 뜬다(`kbl_gamelog.py <번호> --since <날짜>` 로 받아 표·카드·평균 함께).
- **말투** = 마스터 2-7-1(10/19 강제) — 「~어/~야」 끝맺음 비율(50% 이하) · 질문 수(2번 이상) · 12자 이하 짧은 문장(8% 이상). 하나라도 어기면 lint ❌.
- **카드** — 10/18 코트 카드(지침 6-0). 발행된 1~3편은 옛 양식 그대로(다시 그리지 않음).
- 발행하면 설정 파일의 상태를 「발행」, 발행일·링크를 적고 다시 돌린다 → 뒤 편 초안의 링크 누락이 자동으로 뜬다.
"""
    open(os.path.join(HERE, "금메달시리즈_관리표.md"), "w", encoding="utf-8").write(md)
    print(md)


if __name__ == "__main__":
    main()
