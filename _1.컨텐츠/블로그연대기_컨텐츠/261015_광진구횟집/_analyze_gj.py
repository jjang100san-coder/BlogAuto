# -*- coding: utf-8 -*-
r"""「광진구 횟집」 블로그 글 전부(제목에 광진구가 없는 동네 글 포함) 판정·신호·표시 위치 집계 (2026-10-15).
판정은 레이더 6-1(reviewdata.classify_post)과 같은 규칙. 본문은 스크래치에만, 결과엔 글·블로거·가게 이름을 남기지 않는다.
입력: bodies.json  출력: 집계 json"""
import json, re, sys, io, collections, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
B = json.load(open(sys.argv[1], encoding="utf-8")); OUT = sys.argv[2]
AREA = re.compile(r"광진|건대|건국대|자양|구의|중곡|화양|군자|광나루|아차산|능동|어린이대공원|뚝섬|세종대")
FISH = re.compile(r"회|횟집|수산|어시장|숙성회|방어|광어|해산물|사시미|물회|조개|대게|킹크랩|오마카세")
P = {k: v for k, v in B.items() if v.get("text") and len(v["text"]) >= 200}
# 관련: 제목이나 본문 앞부분에 광진구 동네 + 회 관련 말
rel = {k: v for k, v in P.items() if AREA.search(v["title"] + v["text"][:800]) and FISH.search(v["title"] + v["text"][:800])}
S = {"모은 글": len(B), "본문 200자↑": len(P), "광진구·회 관련": len(rel)}
lab = collections.Counter(v["label"] for v in rel.values()); S["판정"] = dict(lab)
coupang = [k for k, v in rel.items() if v["label"] == "ad" and "수수료" in (v.get("why") or "")]
S["쿠팡 등 수수료 고지"] = len(coupang)
S["광고 근거"] = collections.Counter(v["why"] for v in rel.values() if v["label"] == "ad").most_common(15)
S["구청·지자체 서포터즈 언급"] = sum(1 for v in rel.values() if re.search(r"서포터즈|SNS\s*서포터|기자단", v["text"][:1500] + v["title"]))
SIG = {
    "아쉬운 점": r"아쉬(운|웠|움)|아쉽|별로|짜(요|다|더라|서|긴)|싱거|불친절|비싸|실망|애매|비린",
    "강한 추천": r"강추|강력\s*추천|꼭\s*(가|드셔|먹어)\s*보|무조건|인생\s*(맛집|횟집)|찐\s*맛집",
    "주차 안내": r"주차",
    "대기 ○분·○팀": r"(웨이팅|대기)[^\n.]{0,15}\d+\s*(분|팀|시간)|\d+\s*(분|팀)\s*(정도\s*)?(기다|대기)",
    "낸 돈 총 ○원": r"(총|합계|계산|결제|나왔|지불)[^\n.]{0,15}\d[\d,]*\s*원",
    "시가·싯가 언급": r"시가|싯가|시세",
    "스끼다시(곁들이) 언급": r"스끼다시|곁들이|밑반찬|서비스\s*안주",
}
groups = {"체험단·협찬": lambda k, v: v["label"] == "ad" and k not in coupang, "내돈내산": lambda k, v: v["label"] == "self", "표기 없음": lambda k, v: v["label"] == "plain"}
S["신호"] = {}
for g, f in groups.items():
    xs = [(k, v) for k, v in rel.items() if f(k, v)]
    row = {"글": len(xs)}
    for n, p in SIG.items(): row[n] = sum(bool(re.search(p, v["text"])) for k, v in xs)
    nv = [v for k, v in xs if v.get("naver") and v.get("img") is not None]
    if nv:
        row["네이버 글"] = len(nv); row["사진 중앙값"] = st.median(v["img"] for v in nv)
        row["지도"] = sum(bool(v["map"]) for v in nv); row["영상"] = sum(bool(v["video"]) for v in nv)
    S["신호"][g] = row
# 대가 표시 위치 (체험단·협찬만)
PAT = re.compile(r"소정의|원고료|제공받|지원받|협찬|체험단|광고")
pos = collections.Counter()
for k, v in rel.items():
    if v["label"] != "ad" or k in coupang: continue
    if PAT.search(v["title"]): pos["제목"] += 1; continue
    m = PAT.search(v["text"])
    if not m: pos["글자엔 없음(배너 이미지만)"] += 1; continue
    r = m.start() / max(1, len(v["text"]))
    pos["본문 첫 10%" if r < 0.1 else ("본문 끝 10%" if r > 0.9 else "본문 중간")] += 1
S["표시 위치(체험단·협찬)"] = dict(pos)
# 작성 시기별
S["시기"] = {}
for a, b, n in [("2026-01", "2099", "2026년"), ("2024-01", "2026-01", "2024~2025년"), ("0000", "2024-01", "2023년 이전")]:
    xs = [v for v in rel.values() if a <= v["date"] < b]
    S["시기"][n] = dict(collections.Counter(v["label"] for v in xs), 글=len(xs))
# 복붙: 25자↑ 같은 문장을 서로 다른 블로거 2명↑
own = collections.defaultdict(set); posts = collections.defaultdict(set)
BOIL = re.compile(r"Tistory|Facebook|Calendar|동영상 서비스|플러그인|주소|영업시간|전화|특별시|광역시|[a-zA-Z_]{6,}\(|[{}();]|번길|로\s*\d+|정보성 기사")
for k, v in rel.items():
    for s in set(re.split(r"(?<=[.!?])\s+|\n", v["text"])):
        s = re.sub(r"\s+", " ", s).strip()
        if len(s) >= 25 and not BOIL.search(s): own[s].add(v["blogger"]); posts[s].add(k)
sh = [s for s, b in own.items() if len(b) >= 2]; ps = set(p for s in sh for p in posts[s])
S["복붙"] = dict(문장=len(sh), 든_글=len(ps), 판정=dict(collections.Counter(rel[p]["label"] for p in ps)))
S["_복붙_문장_분석용"] = sorted([(len(own[s]), s[:70]) for s in sh], reverse=True)[:15]
json.dump(S, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
for k, v in S.items(): print(k, v)
