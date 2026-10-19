# -*- coding: utf-8 -*-
"""여러 구·시를 같은 잣대로 비교한다 (실거래 캐시 기준, 블로그에는 집계만 — 마스터 0-10).

  python region_compare.py                 셔세권 기본 5곳
  python region_compare.py --out <json>    결과 저장 위치

지표
  pair      같은 단지 ㎡당 중위값 변화율의 중위 (두 해 모두 2건 이상 거래된 단지만)
  yearly    연도별 ㎡당 중위값 · 거래 건수 (해제 제외)
  new18     2018년 이후 준공 ㎡당 중위값 (2025~2026 거래)
  p84       84㎡급(83~86㎡) 매매 중위값 — 2026년 1~9월 / 7~9월
  jeonse    같은 단지·같은 면적 전세가율 (2026년 7~9월, 매매 중위 대비 전세 중위)
  cancel    해제 비율 (2026년 1~9월)
"""
from __future__ import annotations
import json
import statistics as st
import sys
from collections import defaultdict

import re_common as C

REGIONS = {
    "영통구": dict(lawd="41117"),
    "기흥구": dict(lawd="41463"),
    "수지구": dict(lawd="41465"),
    "동탄구": dict(lawd="41597"),
    "병점구": dict(lawd="41595"),
    "평택 고덕": dict(lawd="41220", umd=("고덕",)),
    "평택시": dict(lawd="41220"),
}
END = "202609"
YEARS = list(range(2019, 2027))
PERIODS = [(2019, 2026), (2021, 2026), (2023, 2026), (2025, 2026)]


def rows(kind, lawd, yms, umd=None):
    out = []
    for ym in yms:
        for r in C.rtms(kind, lawd, ym, refresh_days=30):
            if umd and not any(u in (r.get("umdNm") or "") for u in umd):
                continue
            out.append(r)
    return out


def key(r):
    return r.get("aptSeq") or (r.get("umdNm", "") + "|" + r.get("aptNm", "") + "|" + r.get("jibun", ""))


def ppm(r):
    a = C.num(r.get("excluUseAr")); p = C.num(r.get("dealAmount"))
    return p / a if a and p else None


def year(r):
    return int(r.get("dealYear") or 0)


def analyze(lawd, umd=None):
    trade_all = rows("trade", lawd, C.months_back(END, 93), umd)
    trade = [r for r in trade_all if not r.get("cdealType")]
    res = {}
    # 연도별
    by_y = defaultdict(list)
    for r in trade:
        v = ppm(r)
        if v: by_y[year(r)].append(v)
    res["yearly"] = {y: [round(st.median(by_y[y])) if by_y[y] else None, len(by_y[y])] for y in YEARS}
    # 같은 단지 짝
    cy = defaultdict(lambda: defaultdict(list))
    for r in trade:
        v = ppm(r)
        if v: cy[key(r)][year(r)].append(v)
    pair = {}
    for a, b in PERIODS:
        ch = [st.median(d[b]) / st.median(d[a]) - 1 for d in cy.values() if len(d.get(a, [])) >= 2 and len(d.get(b, [])) >= 2]
        pair[f"{a}->{b}"] = [round(st.median(ch) * 100, 1) if ch else None, len(ch)]
    res["pair"] = pair
    # 신축
    nv = [ppm(r) for r in trade if year(r) >= 2025 and int(r.get("buildYear") or 0) >= 2018 and ppm(r)]
    res["new18"] = [round(st.median(nv)) if nv else None, len(nv)]
    # 84㎡급
    def p84(yms):
        s = set(yms)
        v = [C.num(r["dealAmount"]) for r in trade if f"{year(r)}{int(r.get('dealMonth') or 0):02d}" in s and 83 <= (C.num(r.get("excluUseAr")) or 0) <= 86]
        return [round(st.median(v)) if v else None, len(v)]
    res["p84_2026"] = p84([f"2026{m:02d}" for m in range(1, 10)])
    res["p84_q3"] = p84(["202607", "202608", "202609"])
    # 전세가율
    q3 = ["202607", "202608", "202609"]
    tr = defaultdict(list); je = defaultdict(list)
    for r in trade:
        if f"{year(r)}{int(r.get('dealMonth') or 0):02d}" in q3:
            tr[(key(r), round(C.num(r.get("excluUseAr")) or 0))].append(C.num(r["dealAmount"]))
    for r in rows("rent", lawd, q3, umd):
        if (C.num(r.get("monthlyRent")) or 0) == 0 and C.num(r.get("deposit")):
            je[(key(r), round(C.num(r.get("excluUseAr")) or 0))].append(C.num(r["deposit"]))
    ratios = [st.median(je[k]) / st.median(tr[k]) for k in tr if k in je]
    res["jeonse"] = [round(st.median(ratios) * 100, 1) if ratios else None, len(ratios)]
    # 해제
    y26 = [r for r in trade_all if year(r) == 2026]
    res["cancel"] = [round(100 * sum(1 for r in y26 if r.get("cdealType")) / len(y26), 1) if y26 else None, len(y26)]
    # 2025 대비 2026 같은 기간(1~9월) 거래 건수
    n25 = sum(1 for r in trade if year(r) == 2025 and int(r.get("dealMonth") or 0) <= 9)
    res["count_1to9"] = {"2025": n25, "2026": len([r for r in trade if year(r) == 2026])}
    return res


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else str(C.HERE / "_region_samsung.json")
    allres = {}
    for name, cfg in REGIONS.items():
        allres[name] = analyze(cfg["lawd"], cfg.get("umd"))
        print(name, json.dumps(allres[name], ensure_ascii=False), flush=True)
    json.dump(allres, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", out)


if __name__ == "__main__":
    main()
