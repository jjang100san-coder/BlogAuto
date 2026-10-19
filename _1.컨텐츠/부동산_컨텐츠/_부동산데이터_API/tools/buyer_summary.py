# 매입자 거주지별 아파트 매매(부동산원) — 광역시별 외지인(관할 시도 밖)·서울 거주자 비율, 12개월 합
import glob, json, os, re
from collections import defaultdict
N = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_nation")
ALIAS = {"광주": ["광주", "전남광주>광주", "전남광주>(구)광주"]}
AREAS = ["서울", "경기", "인천", "부산", "대구", "광주", "대전", "울산", "세종"]
data = {re.search(r"_(\d{6})", p).group(1): json.load(open(p, encoding="utf-8")) for p in glob.glob(os.path.join(N, "buyer_*.json"))}
def window(end, n=12):
    y, m = int(end[:4]), int(end[4:]); out = []
    for _ in range(n):
        out.append(f"{y}{m:02d}"); m -= 1
        if m == 0: y, m = y - 1, 12
    return out
def agg(area, yms):
    names = ALIAS.get(area, [area]); c = defaultdict(float)
    for ym in yms:
        for r in data.get(ym, []):
            if r["GRP_FULLNM"] in names and r["ITM_NM"] == "동(호)" and r["DTA_VAL"] is not None:
                c[r["CLS_NM"]] += float(r["DTA_VAL"])
    t = c["합계"]
    if not t: return None
    out = (c["관할시도외_서울"] + c["관할시도외_기타"]) / t * 100
    return dict(total=int(t), outsider=round(out, 1), seoul=round(c["관할시도외_서울"] / t * 100, 1))
last = max(data)
res = {}
for a in AREAS:
    res[a] = dict(now=agg(a, window(last)), before=agg(a, window(f"{int(last[:4]) - 3}{last[4:]}")))
    print(a, res[a])
json.dump(dict(last=last, res=res), open(os.path.join(os.path.dirname(N), "_buyer_summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
