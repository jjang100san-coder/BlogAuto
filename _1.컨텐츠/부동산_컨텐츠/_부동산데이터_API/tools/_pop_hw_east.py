# 화성 병점구+동탄구 합계 인구 — 2026.2 구 출범 전은 옛 화성시 동 단위 합(능동은 두 구에 걸쳐 한 번만, 여울동은 옛 오산동에서 나뉨)
import re_common as C, json
from _pop_samsung_lib import pop, pts
NAMES = {'기산동','능동','반월동','반정동','병점동','송산동','안녕동','진안동','황계동',
         '금곡동','목동','반송동','방교동','산척동','석우동','송동','신동','영천동','장지동','중동','청계동','오산동','여울동'}
res = {}
for ym in pts:
    a = pop("4159500000", ym, 6); b = pop("4159700000", ym, 6)
    if a and b and a[0].get("totNmprCnt"):
        v = [int(a[0]["totNmprCnt"]) + int(b[0]["totNmprCnt"]), int(a[0]["hhCnt"]) + int(b[0]["hhCnt"])]
    else:
        rows = [r for r in pop("4159000000", ym, 3) if r.get("stdgNm") in NAMES]
        v = [sum(int(r["totNmprCnt"]) for r in rows), sum(int(r["hhCnt"]) for r in rows)]
    res[ym] = v; print(ym, v, flush=True)
d = json.load(open("_pop_samsung.json", encoding="utf-8"))
d["병점구+동탄구"] = res
for g in ("병점구", "동탄구"):      # 구별 값은 2026.04 이후만 믿는다
    d[g] = {k: v for k, v in d[g].items() if k >= "202604"}
json.dump(d, open("_pop_samsung.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ALL DONE")
