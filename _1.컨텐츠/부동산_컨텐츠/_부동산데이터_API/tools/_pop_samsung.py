# 셔세권 인구·세대 6개월 간격 — 영통·기흥·병점구·동탄구·평택 (+수원 4개 구 비교는 _pop_semi.json)
import re_common as C, json, collections
K = C.datago_key_q()
pts = ["202210","202304","202310","202404","202410","202504","202510","202604","202609"]
def pop(stdg, ym, lv):
    u = (f"https://apis.data.go.kr/1741000/stdgPpltnHhStus/selectStdgPpltnHhStus?serviceKey={K}&stdgCd={stdg}"
         f"&srchFrYm={ym}&srchToYm={ym}&lv={lv}&regSeCd=1&type=JSON&numOfRows=1000&pageNo=1")
    d = C.get_json(u, timeout=120)["Response"]; it = (d.get("items") or {}).get("item") or []
    return it if isinstance(it, list) else [it]
plain = {"영통구": "4111700000", "기흥구": "4146300000", "평택시": "4122000000"}
hw = {"병점구": "4159500000", "동탄구": "4159700000"}
# 화성 새 구는 2026.2 출범 — 그 전 달은 옛 화성시(4159000000) 동 단위 행을 같은 이름끼리 더한다
names = {g: {x["stdgNm"] for x in pop(c, "202609", 3)} for g, c in hw.items()}
print({g: sorted(v) for g, v in names.items()}, flush=True)
res = collections.defaultdict(dict)
for ym in pts:
    for g, c in plain.items():
        x = pop(c, ym, 6)[0]; res[g][ym] = [int(x["totNmprCnt"]), int(x["hhCnt"])]
    old = None
    for g, c in hw.items():
        rows = pop(c, ym, 3)
        if not rows or not any(r.get("stdgNm") in names[g] for r in rows):
            old = old or pop("4159000000", ym, 3); rows = [r for r in old if r.get("stdgNm") in names[g]]
        res[g][ym] = [sum(int(r["totNmprCnt"]) for r in rows), sum(int(r["hhCnt"]) for r in rows)]
    print(ym, {k: v.get(ym) for k, v in res.items()}, flush=True)
json.dump(res, open("_pop_samsung.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ALL DONE", flush=True)
