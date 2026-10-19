# -*- coding: utf-8 -*-
"""전국 지도 1단계 — 한국부동산원(R-ONE) 월간 통계를 지역별로 쌓는다 (2026-10-12).

  python nation_scan.py            매매가격지수 · 미분양 · 매입자거주지별 매매거래 (2019.1 ~ 최신)
  python nation_scan.py --only idx 하나만

결과: tools/_nation/<표>_<YYYYMM>.json (한 달 한 파일, 받은 달은 다시 안 받음 — 최근 3개월만 다시)
키: 레이더 설정 rone_key (출력하지 않는다).
"""
import datetime as dt
import json
import os
import sys
import time

sys.path.insert(0, r"C:\Users\user\Desktop\자동화\블로그용\Keyword_Reader")
from radar.collect import rone  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_nation")
TABLES = {
    "idx": "A_2024_00045",        # (월) 매매가격지수_아파트 — 236개 지역
    "unsold": "T237973129847263",  # 미분양주택현황
    "buyer": "A_2024_00609",       # (월) 매입자거주지별 아파트매매거래현황
}


def months(start="201901"):
    y, m = int(start[:4]), int(start[4:])
    t = dt.date.today()
    out = []
    while (y, m) <= (t.year, t.month):
        out.append(f"{y}{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def fetch(key, sid, ym):
    rows, p = [], 1
    while True:
        r = rone.call("SttsApiTblData.do", key, STATBL_ID=sid, DTACYCLE_CD="MM", WRTTIME_IDTFR_ID=ym,
                      pIndex=p, pSize=1000, timeout=60)
        rows += r["rows"]
        if len(rows) >= int(r["total"] or 0) or not r["rows"]:
            return rows
        p += 1
        time.sleep(0.3)


def main():
    os.makedirs(OUT, exist_ok=True)
    key = rone.load_key()
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    recent = set(months()[-4:])
    for name, sid in TABLES.items():
        if only and name != only:
            continue
        got = 0
        for ym in months("201901" if name != "buyer" else "202201"):
            p = os.path.join(OUT, f"{name}_{ym}.json")
            if os.path.exists(p) and ym not in recent:
                continue
            try:
                rows = fetch(key, sid, ym)
            except Exception as e:
                print("ERR", name, ym, str(e)[:80], flush=True)
                time.sleep(2)
                continue
            if rows:
                json.dump(rows, open(p, "w", encoding="utf-8"), ensure_ascii=False)
                got += 1
            time.sleep(0.3)
        print("done", name, got, flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
