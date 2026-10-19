# 지방 광역시 인구·세대 6개월 간격 (+전국·서울·경기 비교). 광주는 2026.7 통합 뒤 1200000000 아래 5개 구 합.
import json
from _pop_samsung_lib import pop
pts = ["202210","202304","202310","202404","202410","202504","202510","202604","202609"]
want = {"부산광역시":"부산","대구광역시":"대구","대전광역시":"대전","울산광역시":"울산","세종특별자치시":"세종","광주광역시":"광주","서울특별시":"서울","경기도":"경기","인천광역시":"인천"}
GJ = {"1221000000","1224000000","1227000000","1230000000","1233000000"}
res = {v: {} for v in want.values()}; res["전국"] = {}
for ym in pts:
    rows = pop("1000000000", ym, "1")
    res["전국"][ym] = [sum(int(r["totNmprCnt"]) for r in rows), sum(int(r["hhCnt"]) for r in rows)]
    for r in rows:
        nm = want.get(r.get("ctpvNm"))
        if nm: res[nm][ym] = [int(r["totNmprCnt"]), int(r["hhCnt"])]
    if ym not in res["광주"]:
        g = [r for r in pop("1200000000", ym, "2") if r.get("stdgCd") in GJ]
        res["광주"][ym] = [sum(int(r["totNmprCnt"]) for r in g), sum(int(r["hhCnt"]) for r in g)]
    print(ym, {k: v.get(ym, [None])[0] for k, v in res.items()}, flush=True)
json.dump(res, open("_pop_metro.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ALL DONE")
