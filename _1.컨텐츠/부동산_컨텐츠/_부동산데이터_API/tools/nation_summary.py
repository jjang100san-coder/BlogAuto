# -*- coding: utf-8 -*-
"""전국 지도 1단계 요약 — 부동산원 매매지수·미분양을 광역시(+비교권역) 단위로 줄 세운다.
광주는 2026.7 통합 뒤 '전남광주>광주', 그 전은 '광주' 로 나온다 — 둘을 한 줄로 잇는다."""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
N = os.path.join(HERE, "_nation")
ALIAS = {"광주": ["광주", "전남광주>광주"], "전남": ["전남", "전남광주>전남"]}
AREAS = ["전국", "수도권", "지방권", "5대광역시", "서울", "경기", "인천", "부산", "대구", "광주", "대전", "울산", "세종"]


def load(kind):
    out = {}
    for p in sorted(glob.glob(os.path.join(N, f"{kind}_*.json"))):
        ym = re.search(r"_(\d{6})\.json$", p).group(1)
        out[ym] = json.load(open(p, encoding="utf-8"))
    return out


def series(data, name, item=None):
    names = ALIAS.get(name, [name])
    s = {}
    for ym, rows in data.items():
        for r in rows:
            if r.get("CLS_FULLNM") in names and (item is None or r.get("ITM_NM") == item):
                v = r.get("DTA_VAL")
                if v is not None:
                    s[ym] = float(v)
                    break
    return s


def pct(a, b):
    return round((b / a - 1) * 100, 1) if a and b else None


def main():
    idx = load("idx")
    uns = load("unsold")
    last = max(idx)
    res = {}
    for a in AREAS:
        s = series(idx, a)
        if not s:
            continue
        peak_ym = max(s, key=s.get)
        u = series(uns, a + ">계") or series(uns, a)
        res[a] = dict(
            last_ym=last, idx_last=round(s.get(last, 0), 2),
            chg_2019=pct(s.get("201901"), s.get(last)), chg_2023=pct(s.get("202301"), s.get(last)),
            chg_2025=pct(s.get("202501"), s.get(last)), chg_1y=pct(s.get(f"{int(last[:4]) - 1}{last[4:]}"), s.get(last)),
            peak_ym=peak_ym, from_peak=pct(s[peak_ym], s.get(last)),
            unsold_last=u.get(max(u)) if u else None, unsold_2023=u.get("202301") if u else None,
            unsold_peak=(max(u, key=u.get), max(u.values())) if u else None,
        )
    json.dump(res, open(os.path.join(HERE, "_nation_summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"기준 {last} (부동산원 월간 아파트 매매가격지수)")
    print("지역 | 2019.1→ | 2023.1→ | 2025.1→ | 1년 | 고점(월)→지금 | 미분양 2023.1→지금 (정점)")
    for a, r in res.items():
        print(a, "|", r["chg_2019"], "|", r["chg_2023"], "|", r["chg_2025"], "|", r["chg_1y"], "|", r["peak_ym"], r["from_peak"],
              "|", r["unsold_2023"], "→", r["unsold_last"], r["unsold_peak"])


if __name__ == "__main__":
    main()
