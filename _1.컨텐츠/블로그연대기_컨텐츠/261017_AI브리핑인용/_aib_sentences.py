# -*- coding: utf-8 -*-
r"""AI 브리핑 문장 ↔ 출처 글 문장 짝짓기 (2026-10-17).
브리핑 문장마다 인용 블로그 글들에서 가장 닮은 문장을 찾고(4글자 조각 겹침 비율), 같은 검색어의 미인용 상위 글에서도 찾아 비교한다.
짝지은 원문 문장의 꼴(숫자·정의·조건·방법·경험)과 본문 속 위치를 센다. 블로그 밖 출처는 본문을 받아 같은 방식으로.
사용: python _aib_sentences.py <aib.json> <bodies.json> <출력.json>"""
import sys, json, io, re, collections, statistics as st, urllib.request as ur, html as H
sys.stdout.reconfigure(encoding="utf-8")
A = json.load(open(sys.argv[1], encoding="utf-8")); B = json.load(open(sys.argv[2], encoding="utf-8")); OUT = sys.argv[3]
def sents(t):
    out = []
    for line in re.split(r"\n+", t):
        for s in re.split(r"(?<=[.!?。])\s+|(?<=[다요죠음함])\.\s*", line):
            s = re.sub(r"\s+", " ", s).strip()
            if 12 <= len(s) <= 220: out.append(s)
    return out
def grams(s, n=4): s = re.sub(r"[\s\W_]+", "", s); return {s[i:i+n] for i in range(max(0, len(s) - n + 1))}
def best(bs, cand):
    g = grams(bs); top = (0, None, None)
    if not g: return top
    for key, ss in cand.items():
        for i, s in enumerate(ss):
            sc = len(g & grams(s)) / len(g)
            if sc > top[0]: top = (sc, key, (i, len(ss), s))
    return top
def kind(s):
    k = []
    if re.search(r"\d", s): k.append("숫자")
    if re.search(r"(경우|이면|라면|면\s|이상|미만|초과|이하|부터|까지|조건|단,|다만)", s): k.append("조건")
    if re.search(r"(방법|순서|먼저|하면 됩니다|하세요|해야|신청|접수|확인할 수|확인하면)", s): k.append("방법")
    if re.search(r"(이란|란\s|은\s.*(이다|입니다|을 말|를 말|뜻)|의미|정식 명칭|라고 부)", s): k.append("정의")
    if re.search(r"(저는|제가|저희|나는|내가|우리는|다녀|먹어 보|신어 보|써 보|해 보니|직접)", s): k.append("경험")
    return k or ["기타"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def fetch_text(u):
    try:
        h = ur.urlopen(ur.Request(u, headers={"User-Agent": UA}), timeout=20).read().decode("utf-8", "replace")
        h = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", h)
        return H.unescape(re.sub(r"<[^>]+>", "\n", h))
    except Exception: return ""
rows = []; per_q = []
for r in A:
    if not r.get("ai"): continue
    brief = [s for s in sents(r["brief"]) if not re.fullmatch(r"[\w\s·]{1,15}", s) and "AI 브리핑" not in s]
    cited = {k: sents(B.get(k, {}).get("text", "")) for k in r["src_blogs"] if B.get(k, {}).get("text")}
    for u in r["src_other"]:
        t = fetch_text(u)
        if t: cited["(밖)" + u[:60]] = sents(t)
    unc = {k: sents(B.get(k, {}).get("text", "")) for k in r["org_blogs"][:10] if k not in r["src_blogs"] and B.get(k, {}).get("text")}
    for bs in brief:
        sc, key, hit = best(bs, cited); su, ku, hu = best(bs, unc)
        row = dict(q=r["q"], brief=bs, cited_score=round(sc, 2), cited_src=key, src_sent=hit[2] if hit else None,
                   src_pos=round(hit[0] / max(1, hit[1]), 2) if hit else None, src_kind=kind(hit[2]) if hit else [], brief_kind=kind(bs),
                   unc_score=round(su, 2), unc_src=ku, unc_sent=hu[2] if hu else None, blog=bool(key and not key.startswith("(밖)")))
        rows.append(row)
M = [x for x in rows if x["cited_score"] >= 0.45]
S = {"브리핑 문장": len(rows), "인용 글에서 짝 찾음(겹침 45%↑)": len(M),
     "짝 원문이 블로그": sum(x["blog"] for x in M), "짝 원문이 블로그 밖": sum(not x["blog"] for x in M),
     "짝 원문 꼴(겹침 허용)": dict(collections.Counter(k for x in M for k in x["src_kind"])),
     "브리핑 문장 꼴": dict(collections.Counter(k for x in rows for k in x["brief_kind"])),
     "짝 원문 위치 앞/중/뒤": [sum(1 for x in M if x["src_pos"] < 1/3), sum(1 for x in M if 1/3 <= x["src_pos"] < 2/3), sum(1 for x in M if x["src_pos"] >= 2/3)],
     "같은 내용이 미인용 상위 글에도(겹침 45%↑)": sum(1 for x in M if x["unc_score"] >= 0.45),
     "인용 글 겹침 중앙값": st.median(x["cited_score"] for x in rows) if rows else 0,
     "미인용 글 겹침 중앙값": st.median(x["unc_score"] for x in rows) if rows else 0}
json.dump(dict(summary=S, rows=rows), io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(S, ensure_ascii=False, indent=1))
