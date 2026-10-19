# 지방 광역시 40개 구·군 — 매매 2019.1~2026.9, 전월세 2025.7~2026.9 캐시 쌓기
import time, re_common as C
from city_codes import CITY as METRO
codes = [c for g in METRO.values() for c in g]
err = 0
for kind, n in (("trade", 93), ("rent", 15)):
    for code in codes:
        for ym in C.months_back("202609", n):
            try:
                C.rtms(kind, code, ym, refresh_days=30)
            except Exception as e:
                err += 1
                print("ERR", kind, code, ym, str(e)[:90], flush=True)
                if "LIMIT" in str(e).upper() or "22" == str(e)[-2:]:
                    time.sleep(60)
        print("done", kind, code, flush=True)
print("ALL DONE err", err, flush=True)
