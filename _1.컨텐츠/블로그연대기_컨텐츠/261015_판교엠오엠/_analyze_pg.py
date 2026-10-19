# -*- coding: utf-8 -*-
r"""판교 샤브샤브·스키야키 후기(두 검색어 합쳐 겹침 뺌) + 내가 갈 집 후기 판정·신호·같은 해시태그 묶음 집계 (2026-10-15).
판정은 레이더 6-1(reviewdata.classify_post)과 같은 규칙. 본문은 스크래치에만, 결과엔 글·블로거·가게 이름을 남기지 않는다.
사용: python _analyze_pg.py <지역 bodies.json> <가게 bodies.json> <광진 bodies.json> <출력.json>"""
import json, re, sys, io, collections, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
PG, SHOP, GJ, OUT = sys.argv[1:5]
AREA = re.compile(r"판교|백현동|삼평동|알파리움|테크노밸리|운중동")
FOOD = re.compile(r"샤브|스키야키|스끼야끼|스키야끼|전골|나베")
GJ_AREA = re.compile(r"광진|건대|건국대|자양|구의|중곡|화양|군자|광나루|아차산|능동|어린이대공원|뚝섬|세종대")
GJ_FISH = re.compile(r"회|횟집|수산|어시장|숙성회|방어|광어|해산물|사시미|물회|조개|대게|킹크랩|오마카세")
SIG = {
    "아쉬운 점": r"아쉬(운|웠|움)|아쉽|별로|짜(요|다|더라|서|긴)|싱거|불친절|비싸|실망|애매|느끼",
    "강한 추천": r"강추|강력\s*추천|꼭\s*(가|드셔|먹어)\s*보|무조건|인생\s*(맛집|샤브|스키야키)|찐\s*맛집",
    "주차": r"주차", "예약": r"예약",
    "대기 숫자": r"(웨이팅|대기)[^\n.]{0,15}\d+\s*(분|팀|시간)|\d+\s*(분|팀)\s*(정도\s*)?(기다|대기)",
    "총액": r"(총|합계|계산|결제|나왔|지불)[^\n.]{0,15}\d[\d,]*\s*원",
    "옷에 냄새": r"옷에\s*(냄새|배)|냄새가?\s*(배|안\s*배|덜\s*배)",
}
def ok(v): return v.get("text") and len(v["text"]) >= 200
def groups(rel):
    return {"체험단·협찬": [v for v in rel.values() if v["label"] == "ad" and "수수료" not in (v.get("why") or "")],
            "내돈내산": [v for v in rel.values() if v["label"] == "self"], "표기 없음": [v for v in rel.values() if v["label"] == "plain"]}
def signals(rel):
    out = {}
    for g, xs in groups(rel).items():
        row = {"글": len(xs)}
        for n, p in SIG.items(): row[n] = sum(bool(re.search(p, v["text"])) for v in xs)
        nv = [v for v in xs if v.get("naver") and v.get("img") is not None]
        if nv: row.update({"네이버 글": len(nv), "사진 중앙값": st.median(v["img"] for v in nv), "지도": sum(bool(v["map"]) for v in nv), "영상": sum(bool(v["video"]) for v in nv)})
        out[g] = row
    return out
def tagblocks(rel):
    grp = collections.defaultdict(list)
    for k, v in rel.items():
        tags = re.findall(r"#([^\s#]{2,20})", v["text"])
        if len(tags) >= 5: grp[tuple(tags[:5])].append(k)
    hit = {t: ks for t, ks in grp.items() if len(set(rel[k]["blogger"] for k in ks)) >= 3}
    posts = set(k for ks in hit.values() for k in ks)
    blocks = [dict(글=len(ks), 블로거=len(set(rel[k]["blogger"] for k in ks)), 처음=min(rel[k]["date"] for k in ks), 끝=max(rel[k]["date"] for k in ks),
                   판정=dict(collections.Counter(rel[k]["label"] for k in ks))) for t, ks in sorted(hit.items(), key=lambda x: -len(x[1]))]
    return dict(묶음=len(hit), 든_글=len(posts), 판정=dict(collections.Counter(rel[k]["label"] for k in posts)), 묶음별=blocks)
def summary(rel):
    return dict(글=len(rel), 판정=dict(collections.Counter(v["label"] for v in rel.values())), 신호=signals(rel), 같은_해시태그=tagblocks(rel),
                연도=dict(sorted(collections.Counter(v["date"][:4] for v in rel.values()).items())),
                월_2026=dict(sorted(collections.Counter(v["date"][:7] for v in rel.values() if v["date"] >= "2026").items())))
S = {}
B = json.load(open(PG, encoding="utf-8")); P = {k: v for k, v in B.items() if ok(v)}
rel = {k: v for k, v in P.items() if AREA.search(v["title"] + v["text"][:800]) and FOOD.search(v["title"] + v["text"][:800])}
S["판교"] = dict(모은_글=len(B), 본문200자=len(P), **summary(rel))
B = json.load(open(SHOP, encoding="utf-8")); P = {k: v for k, v in B.items() if ok(v)}
rel = {k: v for k, v in P.items() if re.search(r"엠오엠|MOM", v["title"] + v["text"][:3000], re.I) and re.search(r"판교|알파리움", v["title"] + v["text"])}
S["갈_집"] = dict(모은_글=len(B), **summary(rel))
B = json.load(open(GJ, encoding="utf-8"))
rel = {k: v for k, v in B.items() if ok(v) and GJ_AREA.search(v["title"] + v["text"][:800]) and GJ_FISH.search(v["title"] + v["text"][:800])}
S["광진"] = dict(글=len(rel), 같은_해시태그=tagblocks(rel), 옷에_냄새=sum(bool(re.search(SIG["옷에 냄새"], v["text"])) for v in rel.values()))
json.dump(S, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(S, ensure_ascii=False, indent=1, default=str)[:6000])
