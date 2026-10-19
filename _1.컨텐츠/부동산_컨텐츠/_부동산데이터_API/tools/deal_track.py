# -*- coding: utf-8 -*-
"""내 거래 추적기 — 내 매매가 국토부 실거래 자료에 '뜬 날'과 '등기일이 찍힌 날'을 매일 확인해 남긴다.

  python deal_track.py           한 번 확인 (작업 스케줄러가 매일 부른다)
  python deal_track.py --kakao   바뀐 게 있을 때만 카톡

내 거래 정보는 이 폴더의 my_deal.json 에만 둔다 (블로그 폴더 밖으로 나가는 파일에 단지명·면적·층·가격을 쓰지 않는다 — 마스터 0-10).
블로그용 기록(../내거래추적/기록.md)에는 날짜 흐름과 구 단위 집계만 남는다.
"""
from __future__ import annotations
import datetime as dt
import json
import statistics as st
import sys

import re_common as C

CONF = C.HERE / "my_deal.json"
STATE = C.HERE / "_track_state.json"
OUT = C.BASE / "내거래추적"
TEMPLATE = {
    "_설명": "내 거래를 찾는 조건. 이 파일은 블로그에 올리지 않는다. 모르는 칸은 비워 둔다(빈 칸은 조건에서 빠진다).",
    "lawd": "41463 (용인 기흥구 41463 · 참고 수원 영통 41117)",
    "umd": "법정동 이름 (예: 매탄동) — 비워도 됨",
    "apt_contains": "단지 이름 일부 (실거래 자료의 aptNm 에 들어 있는 글자)",
    "area_min": 0, "area_max": 0,
    "deal_date": "YYYY-MM-DD (계약일)",
    "floor": "", "price_manwon": "",
    "balance_date": "YYYY-MM-DD (잔금일, 기록용)",
}


def load_conf():
    if not CONF.exists():
        CONF.write_text(json.dumps(TEMPLATE, ensure_ascii=False, indent=1), encoding="utf-8")
        return None
    c = json.loads(CONF.read_text(encoding="utf-8"))
    if not str(c.get("lawd", "")).isdigit() or "YYYY" in str(c.get("deal_date", "YYYY")) or not c.get("apt_contains"):
        return None
    return c


def match(rows, c):
    d = dt.date.fromisoformat(c["deal_date"])
    out = []
    for r in rows:
        if c["apt_contains"] not in r.get("aptNm", ""):
            continue
        if c.get("umd") and c["umd"] not in r.get("umdNm", ""):
            continue
        a = C.num(r.get("excluUseAr")) or 0
        if c.get("area_max") and not (float(c.get("area_min") or 0) <= a <= float(c["area_max"])):
            continue
        if C.deal_date(r) != d:
            continue
        if str(c.get("floor") or "").strip() and str(r.get("floor")) != str(c["floor"]).strip():
            continue
        if str(c.get("price_manwon") or "").strip() and C.num(r.get("dealAmount")) != C.num(c["price_manwon"]):
            continue
        out.append(r)
    return out


def main():
    today = C.today()
    OUT.mkdir(parents=True, exist_ok=True)
    c = load_conf()
    if not c:
        print(f"[{today}] 설정 필요 — {CONF} 를 채워 주세요."); return
    ym = c["deal_date"][:7].replace("-", "")
    rows = C.rtms("trade", c["lawd"], ym, refresh_days=0)     # 매일 새로 받는다
    hit = match(rows, c)
    st_ = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    events = []
    if hit:
        r = hit[0]
        if not st_.get("first_seen"):
            st_["first_seen"] = str(today); events.append("실거래 자료에 내 거래가 보임")
        rg = C.rgst_date(r)
        if rg and not st_.get("rgst_date"):
            st_["rgst_date"] = str(rg); st_["rgst_seen"] = str(today); events.append(f"등기일 {rg} 찍힘")
        if r.get("cdealType") and not st_.get("cancel_seen"):
            st_["cancel_seen"] = str(today); events.append("⚠ 해제 표시가 붙음")
    st_["last_check"] = str(today); st_["matches"] = len(hit)
    # 같은 구·같은 계약월 거래의 계약→등기 (구 단위 집계 — 블로그에 써도 되는 숫자)
    v = [r for r in rows if not r.get("cdealType")]
    lags = [(C.rgst_date(r) - C.deal_date(r)).days for r in v if C.rgst_date(r)]
    st_.setdefault("gu_daily", {})[str(today)] = dict(n=len(v), registered=len(lags), lag_median=st.median(lags) if lags else None)
    STATE.write_text(json.dumps(st_, ensure_ascii=False, indent=1), encoding="utf-8")

    gu = C.NAMES.get(c["lawd"], c["lawd"])
    L = ["# 내 거래 추적 기록 (블로그용 — 날짜와 구 단위 집계만)", "",
         f"- 계약 → 잔금(예정 {c.get('balance_date') or '—'}) → 등기 → 실거래 자료 반영을 매일 확인한다.",
         "- 단지·면적·층·가격은 이 파일에 쓰지 않는다(마스터 0-10).", "",
         "| 일 | 내용 |", "|---|---|",
         f"| {c['deal_date']} | 계약 |"]
    if st_.get("first_seen"):
        L.append(f"| {st_['first_seen']} | 실거래 자료에서 내 거래를 처음 확인 (추적 시작 전에 이미 올라와 있었을 수 있음) |")
    if st_.get("rgst_date"):
        L.append(f"| {st_['rgst_date']} | 등기일 (자료에 찍힌 날: {st_['rgst_seen']}) |")
    L += ["", f"## {gu} · {ym[:4]}.{ym[4:]} 계약분의 등기 진행 (매일)", "", "| 확인일 | 계약 건수 | 등기 끝남 | 등기까지 중위 |", "|---|---|---|---|"]
    for day, g in sorted(st_["gu_daily"].items()):
        L.append(f"| {day} | {g['n']} | {g['registered']} | {('%.0f일' % g['lag_median']) if g['lag_median'] is not None else '—'} |")
    (OUT / "기록.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    msg = f"[내 거래 추적 {today}] " + (" · ".join(events) if events else f"변화 없음 (일치 {len(hit)}건)")
    print(msg)
    if events and "--kakao" in sys.argv:
        print(C.kakao(msg))


if __name__ == "__main__":
    main()
