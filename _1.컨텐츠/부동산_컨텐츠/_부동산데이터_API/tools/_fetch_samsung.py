# 셔세권 비교용 실거래 캐시 쌓기 — 기흥·병점구·평택 매매 2019.1~2026.9, 6개 지역 전월세 2025.7~2026.9
import re_common as C
trade_codes = ["41463", "41595", "41220", "41117", "41597"]
rent_codes = ["41117", "41463", "41595", "41597", "41220"]
for code in trade_codes:
    for ym in C.months_back("202609", 93):
        try: C.rtms("trade", code, ym, refresh_days=30)
        except Exception as e: print("ERR trade", code, ym, str(e)[:80], flush=True)
    print("done trade", code, flush=True)
for code in rent_codes:
    for ym in C.months_back("202609", 15):
        try: C.rtms("rent", code, ym, refresh_days=30)
        except Exception as e: print("ERR rent", code, ym, str(e)[:80], flush=True)
    print("done rent", code, flush=True)
print("ALL DONE", flush=True)
