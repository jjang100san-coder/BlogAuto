# 2019-01 ~ 2026-09 매매 상세: 만세구(남양 포함) · 수원 4개 구 · 동탄구 — 캐시에 쌓기만
import re_common as C, sys
months=C.months_back("202609",93)
codes=["41591","41111","41113","41115","41117","41597"]
for code in codes:
    for i,ym in enumerate(months):
        try: C.rtms("trade",code,ym,refresh_days=30)
        except Exception as e: print("ERR",code,ym,str(e)[:80],flush=True)
    print("done",code,flush=True)
print("ALL DONE",flush=True)
