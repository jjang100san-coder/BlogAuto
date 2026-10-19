# -*- coding: utf-8 -*-
r"""토요일 2차 이자카야 후보 6곳(낙지집 500m 안) 후기 판정·같은 해시태그 묶음 (2026-10-15).
가게마다 이름이 본문에 실제로 나온 글만. 결과엔 가게를 번호로만 남기고 이름은 작업 메모에서 대조한다.
사용: python _analyze_pub.py <bodies.json> <출력.json>"""
import json, re, sys, io, collections
sys.stdout.reconfigure(encoding="utf-8")
B = json.load(open(sys.argv[1], encoding="utf-8"))
SHOPS = [("1", "이이토모 군자", r"이이토모"), ("2", "러브러브디럭스 군자", r"러브러브\s*디럭스"), ("3", "클로버하우스 군자", r"클로버\s*하우스"),
         ("4", "요리미치 군자", r"요리미치"), ("5", "숯불직화꼬치바베큐 군자", r"숯불\s*직화\s*꼬치"), ("6", "쿠시카츠 츠키 군자", r"쿠시카츠\s*츠키|츠키")]
S = {}
for no, q, pat in SHOPS:
    V = {k: v for k, v in B.items() if v.get("text") and len(v["text"]) >= 200 and q in (v.get("q") or []) and re.search(pat, v["title"] + v["text"][:3000])}
    grp = collections.defaultdict(list)
    for k, v in V.items():
        t = re.findall(r"#([^\s#]{2,20})", v["text"])
        if len(t) >= 5: grp[tuple(t[:5])].append(k)
    hit = {t: ks for t, ks in grp.items() if len(set(V[k]["blogger"] for k in ks)) >= 3}
    posts = set(k for ks in hit.values() for k in ks)
    wait = sum(bool(re.search(r"(웨이팅|대기)[^\n.]{0,15}\d+\s*(분|팀|시간)|\d+\s*(분|팀)\s*(정도\s*)?(기다|대기)", v["text"])) for v in V.values())
    S[no] = dict(글=len(V), 판정=dict(collections.Counter(v["label"] for v in V.values())), 같은_해시태그_글=len(posts), 묶음=len(hit),
                 묶음_판정=dict(collections.Counter(V[k]["label"] for k in posts)), 대기숫자=wait,
                 올해=sum(v["date"] >= "2026" for v in V.values()))
json.dump(S, io.open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in S.items(): print(k, v)
