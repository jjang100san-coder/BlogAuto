# -*- coding: utf-8 -*-
r"""내돈내산 표기 글 vs 광고 고지 글 — 어디서 갈리나 (2026-10-14).
「직접 경험」을 증명하는 게 아니라, 스스로 내돈내산이라고 밝힌 글과 광고라고 밝힌 글의 차이를 잰다.
입력: bodies.json(본문), naver_media.json(네이버 글 사진·지도·영상 정확 집계). 출력: 집계 json."""
import json, re, sys, io, statistics as st, collections
sys.stdout.reconfigure(encoding="utf-8")
B = json.load(open(sys.argv[1], encoding="utf-8")); M = json.load(open(sys.argv[2], encoding="utf-8")); OUT = sys.argv[3]
SIG = {
    "동행자 언급": r"(남편|신랑|아내|와이프|친구|동생|엄마|아빠|부모님|아이랑|아이와|딸|아들|가족|동료|여자\s*친구|남자\s*친구|여친|남친)",
    "방문 시점 구체(요일·시간대)": r"(\d{1,2}\s*시\s*(쯤|반|에|경)|점심\s*시간|저녁\s*시간|토요일|일요일|평일|주말\s*(점심|저녁|오후))",
    "대기 시간·팀 숫자": r"(웨이팅|대기)[^\n.]{0,15}\d+\s*(분|팀|시간)|\d+\s*(분|팀)\s*(정도\s*)?(기다|대기)",
    "주문 수량": r"\d+\s*인분|\d+\s*명이서|\d+\s*개\s*시켰|추가\s*주문|시켰(어|는데|다|습니다)",
    "낸 돈 합계": r"(총|합계|계산|결제|나왔|지불)[^\n.]{0,15}\d[\d,]*\s*원",
    "아쉬운 점": r"아쉬(운|웠|움)|아쉽|별로|짜(요|다|더라|서|긴)|싱거|불친절|비싸|실망|애매",
    "변수·헛걸음": r"품절|재료\s*소진|솔드\s*아웃|헛걸음|못\s*먹었|자리가\s*없|문\s*닫|브레이크\s*타임에\s*걸",
    "전에 와 본 비교": r"다른\s*지점|예전에|지난번|전에\s*(왔|갔|먹)|다른\s*집|여기보다|처음\s*왔을",
    "강한 추천": r"강추|강력\s*추천|꼭\s*(가|드셔|먹어)\s*보|무조건|인생\s*맛집|찐\s*맛집",
    "소개 말투(소개해 드릴게요·방문해 보았습니다)": r"소개해\s*드릴|소개해드릴|방문해\s*보았|방문해봤|다녀와\s*보았|포스팅\s*해\s*보|추천\s*드립니다|추천드립니다",
    "주차 안내": r"주차",
    "정보 묶음(주소·영업시간 등 3종↑)": None,
}
INFO = r"(주소|영업\s*시간|브레이크\s*타임|휴무|전화(번호)?|주차|라스트\s*오더)"
def has(k, t):
    if k.startswith("정보 묶음"): return len(set(m.group(1)[:2] for m in re.finditer(INFO, t))) >= 3
    return bool(re.search(SIG[k], t))
G = collections.defaultdict(list)
for k, v in B.items():
    if not v.get("text") or len(v["text"]) < 200: continue
    r = {s: has(s, v["text"]) for s in SIG}
    r["naver"] = "blog.naver.com" in k
    m = M.get(k, {})
    r["img"] = m.get("img"); r["map"] = (m.get("map") or 0) > 0 if m else None; r["video"] = (m.get("video") or 0) > 0 if m else None
    r["chars"] = len(v["text"])
    G[v["label"]].append(r)
S = {}
print("%-34s %8s %8s %8s" % ("신호 (그 신호가 있는 글 / 전체)", "내돈내산", "광고", "표기없음"))
for s in SIG:
    row = {L: (sum(r[s] for r in G[L]), len(G[L])) for L in ("self", "ad", "plain")}
    S[s] = row
    print("%-34s %8s %8s %8s" % (s, "%d/%d" % row["self"], "%d/%d" % row["ad"], "%d/%d" % row["plain"]))
med = {}
for L in ("self", "ad", "plain"):
    nv = [r for r in G[L] if r["naver"] and r["img"] is not None]
    imgs = sorted(r["img"] for r in nv)
    med[L] = dict(n=len(nv), 사진_중앙=st.median(imgs), 사진_하위4분=imgs[len(imgs)//4], 사진_상위4분=imgs[3*len(imgs)//4],
                  사진30장이상=sum(x >= 30 for x in imgs), 지도=sum(bool(r["map"]) for r in nv), 영상=sum(bool(r["video"]) for r in nv),
                  글자_중앙=st.median(r["chars"] for r in G[L]))
    print(L, med[L])
S["네이버_미디어"] = med
# 내돈내산 쪽 신호 묶음 점수: 경험 신호 7개 중 몇 개
EXP = ["동행자 언급", "방문 시점 구체(요일·시간대)", "대기 시간·팀 숫자", "주문 수량", "낸 돈 합계", "아쉬운 점", "변수·헛걸음", "전에 와 본 비교"]
dist = {}
for L in ("self", "ad", "plain"):
    c = collections.Counter(sum(r[s] for s in EXP) for r in G[L]); dist[L] = dict(sorted(c.items()))
    print("경험 신호 8개 중 몇 개:", L, dist[L])
S["경험신호_개수분포"] = dist
json.dump(S, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
