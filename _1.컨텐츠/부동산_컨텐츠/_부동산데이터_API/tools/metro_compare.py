# -*- coding: utf-8 -*-
"""지방 광역시 실거래 비교 — region_compare.py 의 잣대를 광역시(여러 구 묶음)와 구 단위에 그대로 쓴다.

  python metro_compare.py     → _metro_compare.json + 화면 요약
추가 지표
  peak   2026.7~9 거래가 같은 단지·같은 면적의 2019년 이후 이전 최고가보다 얼마나 낮은지(중위), 20% 넘게 낮은 비율, 신고가 비율
  monthly 2026년 월별 매매 건수(해제 제외)
"""
import json
import statistics as st
from collections import defaultdict

import re_common as C
import region_compare as R
from metro_codes import METRO

_orig_rows = R.rows


def rows_multi(kind, lawd, yms, umd=None):
    if isinstance(lawd, (list, tuple)):
        out = []
        for l in lawd:
            out += _orig_rows(kind, l, yms, umd)
        return out
    return _orig_rows(kind, lawd, yms, umd)


R.rows = rows_multi


def peak_metrics(lawds):
    tr = [r for r in rows_multi("trade", lawds, C.months_back("202609", 93)) if not r.get("cdealType")]
    key = lambda r: (R.key(r), round(C.num(r.get("excluUseAr")) or 0))
    ym = lambda r: f"{R.year(r)}{int(r.get('dealMonth') or 0):02d}"
    hist = defaultdict(list)
    for r in sorted(tr, key=lambda r: (ym(r), int(r.get("dealDay") or 0))):
        hist[key(r)].append((ym(r), C.num(r["dealAmount"])))
    ratios, newhi, n = [], 0, 0
    for k, deals in hist.items():
        for i, (m, p) in enumerate(deals):
            if m < "202607" or not p:
                continue
            prev = [x for mm, x in deals[:i] if x]
            if len(prev) < 3:
                continue
            mx = max(prev)
            n += 1
            ratios.append(p / mx - 1)
            if p > mx:
                newhi += 1
    monthly = defaultdict(int)
    for r in tr:
        if R.year(r) == 2026:
            monthly[int(r.get("dealMonth") or 0)] += 1
    return dict(n=n, from_peak=round(st.median(ratios) * 100, 1) if ratios else None,
                below20=round(100 * sum(1 for x in ratios if x < -0.2) / n, 1) if n else None,
                newhigh=round(100 * newhi / n, 1) if n else None, monthly=dict(sorted(monthly.items())))


def main():
    res = {}
    for metro, gus in METRO.items():
        codes = list(gus)
        m = R.analyze(codes)
        m["peak"] = peak_metrics(codes)
        m["gu"] = {}
        for c, nm in gus.items():
            g = R.analyze(c)
            m["gu"][nm] = dict(pair=g["pair"], p84_2026=g["p84_2026"], count_1to9=g["count_1to9"])
        res[metro] = m
        print(metro, json.dumps({k: m[k] for k in ("pair", "p84_2026", "jeonse", "cancel", "count_1to9", "new18")}, ensure_ascii=False),
              "peak", json.dumps(m["peak"], ensure_ascii=False), flush=True)
    json.dump(res, open(C.HERE / "_metro_compare.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved")


if __name__ == "__main__":
    main()
