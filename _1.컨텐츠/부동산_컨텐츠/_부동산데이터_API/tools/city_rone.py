# -*- coding: utf-8 -*-
"""지방 대도시 12곳 — 부동산원 매매지수·미분양·외지인 매입(nation_scan 캐시 재사용) → _city_rone.json"""
import json
import os

import nation_summary as NS
import buyer_summary as BS  # noqa: F401  (window/agg 재사용 — 모듈 로드 시 광역시 요약도 한 번 출력됨)

HERE = os.path.dirname(os.path.abspath(__file__))
CITIES = {"창원": "경남>창원시", "청주": "충북>청주시", "천안": "충남>천안시", "전주": "전북>전주시", "김해": "경남>김해시",
          "포항": "경북>포항시", "제주": "제주>제주시", "구미": "경북>구미시", "아산": "충남>아산시", "원주": "강원>원주시",
          "양산": "경남>양산시", "진주": "경남>진주시"}


def main():
    idx, uns = NS.load("idx"), NS.load("unsold")
    last = max(idx)
    res = {}
    for c, nm in CITIES.items():
        s = NS.series(idx, nm)
        u = NS.series(uns, nm)
        peak = max(s, key=s.get)
        bnow = BS.agg(nm, BS.window(BS.last))
        bold = BS.agg(nm, BS.window(f"{int(BS.last[:4]) - 3}{BS.last[4:]}"))
        res[c] = dict(peak_ym=peak, from_peak=NS.pct(s[peak], s.get(last)), chg_2019=NS.pct(s.get("201901"), s.get(last)),
                      chg_2023=NS.pct(s.get("202301"), s.get(last)), chg_1y=NS.pct(s.get(f"{int(last[:4]) - 1}{last[4:]}"), s.get(last)),
                      unsold_2023=u.get("202301"), unsold_now=u.get(max(u)) if u else None, unsold_now_ym=max(u) if u else None,
                      unsold_peak=(max(u, key=u.get), max(u.values())) if u else None, buyer_now=bnow, buyer_3y=bold)
        r = res[c]
        print(c, "| 고점", r["peak_ym"], r["from_peak"], "| 2023→", r["chg_2023"], "| 1y", r["chg_1y"], "| 2019→", r["chg_2019"],
              "| 미분양", r["unsold_2023"], "→", r["unsold_now"], r["unsold_now_ym"], r["unsold_peak"],
              "| 외지인", (bnow or {}).get("outsider"), "(", (bold or {}).get("outsider"), ") 서울", (bnow or {}).get("seoul"))
    json.dump(dict(last=last, res=res), open(os.path.join(HERE, "_city_rone.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
