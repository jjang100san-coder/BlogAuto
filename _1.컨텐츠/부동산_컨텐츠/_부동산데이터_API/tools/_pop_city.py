# 지방 대도시 12곳 인구·세대 (2022.10 → 2026.09, 6개월 간격)
import json
from _pop_samsung_lib import pop, pts
C = {"창원": "4812000000", "청주": "4311000000", "천안": "4413000000", "전주": "5211000000", "김해": "4825000000", "포항": "4711000000",
     "제주": "5011000000", "구미": "4719000000", "아산": "4420000000", "원주": "5113000000", "양산": "4833000000", "진주": "4817000000"}
SIDO_OLD = {"5211000000": "4511000000", "5113000000": "4213000000"}   # 전북·강원 특별자치도 전환 전 코드
res = {k: {} for k in C}
for ym in pts:
    for k, code in C.items():
        rows = []
        for cd in (code, SIDO_OLD.get(code)):
            if not cd: continue
            try:
                rows = pop(cd, ym, "6")
            except Exception:
                rows = []
            if rows and rows[0].get("totNmprCnt"): break
        if rows and rows[0].get("totNmprCnt"):
            res[k][ym] = [int(rows[0]["totNmprCnt"]), int(rows[0]["hhCnt"])]
    print(ym, {k: v.get(ym, [None])[0] for k, v in res.items()}, flush=True)
json.dump(res, open("_pop_city.json", "w", encoding="utf-8"), ensure_ascii=False)
for k, v in res.items():
    if "202210" in v and "202609" in v:
        a, b, c = v["202210"][0], v["202609"][0], v.get("202510", [None])[0]
        print(k, f"{100*(b/a-1):+.1f}%", "1y", f"{100*(b/c-1):+.1f}%" if c else "-")
