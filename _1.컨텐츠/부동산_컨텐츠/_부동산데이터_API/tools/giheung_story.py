# -*- coding: utf-8 -*-
"""「영통 근처로 간다 → 실은 용인시 → 용인은 수원보다 덜 올랐다 → 영통권이면 말이 다르다」 — 4단 비교.
L1 시: 수원시(4구) vs 용인시(3구)   L2 구: 7개 구   L3 기흥 동별·묶음(A/B/C)   L4 영통 동별(구도심 vs 광교)
지표(국토부 매매·전월세 실거래, 2019.1~2026.9 계약, 해제 제외, region_compare 같은 잣대):
  같은 단지 ㎡당 변화(연도 짝: 2021→26·2022→26·2023→26·2024→26·2025→26), 84㎡급 중위(2026.1~9),
  같은 단지 전세가율(2026.7~9), 1~9월 거래 2025→2026, 이전 최고가 대비(2026.7~9)·신고가 비율.
결과: _giheung_story.json. 단지 이름·식별자는 저장하지 않는다(집계만)."""
import json, os, statistics as st
from collections import defaultdict
import re_common as C
import region_compare as R

HERE = os.path.dirname(os.path.abspath(__file__))
SUWON = {"장안구": "41111", "권선구": "41113", "팔달구": "41115", "영통구": "41117"}
YONGIN = {"처인구": "41461", "기흥구": "41463", "수지구": "41465"}
G_A = ["영덕동", "서천동", "하갈동", "신갈동"]
G_B = ["보정동", "상갈동", "보라동", "마북동", "공세동"]
G_C = ["구갈동", "언남동", "고매동", "지곡동", "상하동", "청덕동", "중동", "동백동"]
PAIRS = [(2021, 2026), (2022, 2026), (2023, 2026), (2024, 2026), (2025, 2026)]
MONTHS = C.months_back("202609", 93)


def load(kind, lawds, umd=None, yms=None):
    out = []
    for l in lawds:
        out += R.rows(kind, l, yms or MONTHS, umd)
    return out


def ym(r): return f"{R.year(r)}{int(r.get('dealMonth') or 0):02d}"


def metrics(lawds, umd=None):
    allr = load("trade", lawds, umd)
    tr = [r for r in allr if not r.get("cdealType")]
    res = {}
    cy = defaultdict(lambda: defaultdict(list))
    for r in tr:
        v = R.ppm(r)
        if v: cy[R.key(r)][R.year(r)].append(v)
    for a, b in PAIRS:
        ch = [st.median(d[b]) / st.median(d[a]) - 1 for d in cy.values() if len(d.get(a, [])) >= 2 and len(d.get(b, [])) >= 2]
        res[f"{a}->{b}"] = [round(st.median(ch) * 100, 1) if ch else None, len(ch)]
    v84 = [C.num(r["dealAmount"]) for r in tr if ym(r) >= "202601" and 83 <= (C.num(r.get("excluUseAr")) or 0) <= 86]
    res["p84_2026"] = [round(st.median(v84)) if v84 else None, len(v84)]
    q3 = ["202607", "202608", "202609"]
    trq, je = defaultdict(list), defaultdict(list)
    for r in tr:
        if ym(r) in q3: trq[(R.key(r), round(C.num(r.get("excluUseAr")) or 0))].append(C.num(r["dealAmount"]))
    for r in load("rent", lawds, umd, q3):
        if (C.num(r.get("monthlyRent")) or 0) == 0 and C.num(r.get("deposit")):
            je[(R.key(r), round(C.num(r.get("excluUseAr")) or 0))].append(C.num(r["deposit"]))
    rat = [st.median(je[k]) / st.median(trq[k]) for k in trq if k in je]
    res["jeonse"] = [round(st.median(rat) * 100, 1) if rat else None, len(rat)]
    res["count_1to9"] = {y: sum(1 for r in tr if R.year(r) == y and int(r.get("dealMonth") or 0) <= 9) for y in (2025, 2026)}
    hist = defaultdict(list)
    for r in sorted(tr, key=lambda r: (ym(r), int(r.get("dealDay") or 0))):
        hist[(R.key(r), round(C.num(r.get("excluUseAr")) or 0))].append((ym(r), C.num(r["dealAmount"])))
    rs, hi = [], 0
    for deals in hist.values():
        for i, (m, p) in enumerate(deals):
            if m < "202607" or not p: continue
            prev = [x for _, x in deals[:i] if x]
            if len(prev) < 3: continue
            rs.append(p / max(prev) - 1); hi += p > max(prev)
    res["peak"] = dict(n=len(rs), from_peak=round(st.median(rs) * 100, 1) if rs else None,
                       newhigh=round(100 * hi / len(rs), 1) if rs else None)
    return res


def dong_list(lawd):
    c = defaultdict(int)
    for r in load("trade", [lawd]):
        if not r.get("cdealType"): c[r.get("umdNm")] += 1
    return [d for d, n in sorted(c.items(), key=lambda x: -x[1]) if n >= 100]


out = {"L1": {}, "L2": {}, "L3_group": {}, "L3_dong": {}, "L4_dong": {}}
out["L1"]["수원시(4구)"] = metrics(list(SUWON.values()))
out["L1"]["용인시(3구)"] = metrics(list(YONGIN.values()))
for nm, c in {**SUWON, **YONGIN}.items():
    out["L2"][nm] = metrics([c])
for nm, g in (("A 영통 맞닿음", G_A), ("B 1.5~3km", G_B), ("C 3km+", G_C)):
    out["L3_group"][nm] = metrics(["41463"], g)
for d in dong_list("41463"):
    out["L3_dong"][d] = metrics(["41463"], [d])
for d in dong_list("41117"):
    out["L4_dong"][d] = metrics(["41117"], [d])
json.dump(out, open(os.path.join(HERE, "_giheung_story.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for lv in out:
    for nm, m in out[lv].items():
        print(lv, nm, "| 23→26", m["2023->2026"], "22→26", m["2022->2026"], "24→26", m["2024->2026"], "21→26", m["2021->2026"],
              "| 84", m["p84_2026"], "| 전세", m["jeonse"], "| 거래", m["count_1to9"], "| 최고가", m["peak"])
