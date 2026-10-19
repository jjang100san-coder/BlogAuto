# -*- coding: utf-8 -*-
r"""「수원 맛집」 615편 중 광고·내돈내산·표기 없음 글의 결·복붙·먹거리 비교 (2026-10-14).
입력: 본문 json (fetch_bodies.py 결과 — 본문은 분석용으로만 스크래치에 두고 블로그에는 싣지 않는다)
출력: 집계 json + 콘솔 요약. 글·블로거·가게 이름은 결과에 남기지 않는다(지목 금지)."""
import json, re, sys, io, collections, itertools, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
B = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
P = {k: v for k, v in B.items() if v.get("text") and len(v["text"]) >= 200}

FEAT = {
    "1인칭 경험": r"(내가|나는|저는|제가|우리는|우리가|남편|아내|와이프|신랑|아이랑|아이와|친구랑|친구와|엄마랑|가족이랑|먹어봤|다녀왔|방문했|먹었)",
    "가격 숫자": r"\d[\d,]*\s*원",
    "영수증": r"영수증",
    "재방문": r"재방문|또\s*(올|가|방문)|단골|두\s*번째\s*방문|다시\s*(올|가|방문)",
    "아쉬운 점": r"아쉬(운|웠|움)|별로|짜(요|다|더라|서)|싱거|불친절|비싸|아쉽|실망",
    "사장님 친절": r"사장님[^\n.]{0,15}친절|친절하(게|신)",
    "메뉴판": r"메뉴판",
    "강한 추천": r"강추|강력\s*추천|꼭\s*(가|드셔|먹어)\s*보|무조건|인생\s*맛집|찐\s*맛집",
    "웨이팅": r"웨이팅|대기|줄을?\s*서",
    "주차": r"주차",
}
INFO = r"(주소|영업\s*시간|브레이크\s*타임|휴무|전화(번호)?|주차|라스트\s*오더)"
FOOD = {
    "고기·갈비": r"갈비|삼겹|고기|소금구이|목살|한우|양갈비|곱창|대창|막창",
    "국밥·해장국·탕": r"국밥|해장국|순대국|감자탕|설렁탕|곰탕|갈비탕|국물",
    "칼국수·면": r"칼국수|국수|냉면|우동|라멘|짬뽕|쌀국수|파스타",
    "돈가스·경양식": r"돈까스|돈가스|경양식|함박",
    "치킨·통닭": r"치킨|통닭",
    "해산물·게장·회": r"게장|회\b|횟집|해산물|조개|굴|생선|고등어|초밥|스시|오마카세",
    "카페·베이커리·디저트": r"카페|베이커리|빵|베이글|도넛|디저트|케이크|커피",
    "중식": r"짜장|탕수육|중식|마라|딤섬",
    "양식·브런치": r"브런치|스테이크|피자|버거|양식|레스토랑",
    "뷔페": r"뷔페",
    "부대찌개·찌개·닭갈비": r"부대찌개|찌개|닭갈비|닭볶음",
}
def feats(t, v):
    f = {k: bool(re.search(p, t)) for k, p in FEAT.items()}
    f["정보 묶음(3종↑)"] = len(set(m.group(1)[:2] for m in re.finditer(INFO, t))) >= 3
    f["존댓말"] = len(re.findall(r"(습니다|어요|에요|해요|세요|네요)\b", t)) > len(re.findall(r"(했어|었어|더라|거든|이야|했다|이다)\b", t))
    return f
rows = []
for k, v in P.items():
    t = v["text"]; f = feats(t, v)
    food = [n for n, p in FOOD.items() if re.search(p, v["title"])] or [n for n, p in FOOD.items() if re.search(p, t[:600])][:1] or ["기타·여러 가지"]
    rows.append(dict(link=k, label=v["label"], blogger=v["blogger"], chars=len(t), imgs=v.get("imgs", 0), naver="blog.naver.com" in k, food=food[0], **f))
lab = collections.Counter(r["label"] for r in rows)
print("분석 대상(본문 200자↑):", dict(lab))
S = {"대상": dict(lab), "결": {}, "먹거리": {}, "복붙": {}}
for L in ("ad", "self", "plain"):
    g = [r for r in rows if r["label"] == L]
    if not g: continue
    d = dict(n=len(g), 글자_중앙=st.median(r["chars"] for r in g), 사진_중앙=st.median(r["imgs"] for r in g))
    for k in list(FEAT) + ["정보 묶음(3종↑)", "존댓말"]:
        d[k] = sum(r[k] for r in g)
    S["결"][L] = d
    S["먹거리"][L] = collections.Counter(r["food"] for r in g).most_common()
    print("\n##", L, d); print("   먹거리", S["먹거리"][L][:8])

# 복붙 — 문장 단위: 25자 이상 같은 문장이 서로 다른 블로거 3명 이상의 글에
sent_owner = collections.defaultdict(set); sent_posts = collections.defaultdict(set)
for k, v in P.items():
    for s in set(re.split(r"(?<=[.!?。])\s+|\n", v["text"])):
        s2 = re.sub(r"\s+", " ", s).strip()
        if len(s2) >= 25 and not re.search(r"(주소|영업시간|전화|휴무|https?://|지도|플레이스)", s2):
            sent_owner[s2].add(v["blogger"]); sent_posts[s2].add(k)
shared = {s: b for s, b in sent_owner.items() if len(b) >= 3}
posts_with_shared = set(p for s in shared for p in sent_posts[s])
print("\n같은 문장(25자↑)을 블로거 3명 이상이 쓴 경우:", len(shared), "문장 / 그 문장이 든 글", len(posts_with_shared))
by_label = collections.Counter(P[p]["label"] for p in posts_with_shared)
print("   그 글의 판정:", dict(by_label))
S["복붙"]["공유문장_수"] = len(shared); S["복붙"]["공유문장_든_글"] = dict(by_label)
S["복붙"]["공유문장_예(길이·블로거 수만)"] = sorted([(len(s), len(b)) for s, b in shared.items()], key=lambda x: -x[1])[:15]
S["복붙"]["_문장_원문_분석용"] = sorted([(len(b), s[:80]) for s, b in shared.items()], reverse=True)[:30]

# 복붙 — 글 단위: 글자 5-그램 자카드, 서로 다른 블로거
def sh(t):
    t = re.sub(r"\s+", "", t); return set(t[i:i+5] for i in range(0, max(0, len(t) - 5), 2))
SH = {k: sh(v["text"]) for k, v in P.items()}
pairs = []
ks = list(P)
for a, b in itertools.combinations(ks, 2):
    if P[a]["blogger"] == P[b]["blogger"]: continue
    A, Bs = SH[a], SH[b]
    if not A or not Bs: continue
    j = len(A & Bs) / len(A | Bs)
    if j >= 0.2: pairs.append((round(j, 2), P[a]["label"], P[b]["label"]))
print("서로 다른 블로거 글끼리 5-그램 겹침 0.2 이상 쌍:", len(pairs), collections.Counter((min(x[1], x[2]), max(x[1], x[2])) for x in pairs).most_common())
S["복붙"]["유사쌍_0.2이상"] = len(pairs); S["복붙"]["유사쌍_판정조합"] = [list(k) + [v] for k, v in collections.Counter((min(x[1], x[2]), max(x[1], x[2])) for x in pairs).items()]
S["복붙"]["유사쌍_최고값"] = sorted(pairs, reverse=True)[:10]

# 같은 블로거 여러 편
bc = collections.Counter(P[k]["blogger"] for k in P)
S["같은블로거"] = dict(최다=bc.most_common(1)[0][1], 세편이상_블로거수=sum(1 for v in bc.values() if v >= 3), 그_글수=sum(v for v in bc.values() if v >= 3))
print("같은 블로거 3편 이상:", S["같은블로거"])

# 표기 없는 글이 어느 쪽 결에 가까운가 (특징 9개 + 정보묶음 + 존댓말, 비율 벡터 거리) — 단정 아님
keys = list(FEAT) + ["정보 묶음(3종↑)", "존댓말"]
def cen(L):
    g = [r for r in rows if r["label"] == L]; return {k: sum(r[k] for r in g) / len(g) for k in keys}
ca, cs = cen("ad"), cen("self")
near = collections.Counter()
for r in rows:
    if r["label"] != "plain": continue
    da = sum((r[k] - ca[k]) ** 2 for k in keys); ds = sum((r[k] - cs[k]) ** 2 for k in keys)
    near["광고 글 결에 더 가까움" if da < ds else "내돈내산 글 결에 더 가까움"] += 1
print("표기 없는 글의 결:", dict(near))
S["표기없음_결_가까운쪽"] = dict(near)
json.dump(S, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
