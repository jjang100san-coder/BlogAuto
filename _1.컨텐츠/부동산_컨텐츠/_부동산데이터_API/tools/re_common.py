# -*- coding: utf-8 -*-
"""부동산 데이터 도구 공용 — 키 읽기(레이더 설정, 읽기만) · HTTP · 실거래 받기(월 단위 캐시).

키는 콘텐츠 트렌드 레이더 ⚙ 설정에 저장된 것을 그대로 읽는다. 여기서 키를 쓰거나 바꾸지 않는다.
  %LOCALAPPDATA%\\ContentTrendRadar\\settings.json  — ecos_key · finlife_key · rone_key · kosis_key · vworld_key
  %LOCALAPPDATA%\\ContentTrendRadar\\datago.json    — service_key (공공데이터포털)
"""
from __future__ import annotations
import datetime as dt
import json
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent                       # _부동산데이터_API
CACHE = HERE / "_cache"
RADAR = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "ContentTrendRadar"
KST = dt.timezone(dt.timedelta(hours=9))

SUWON = {"41111": "장안구", "41113": "권선구", "41115": "팔달구", "41117": "영통구"}
# 10/15 이사지 정정: 용인 기흥구(생활권 수원 영통). 비교표·내 거래 추적은 이 4개 구로
BORDER = {"41463": "용인 기흥구", "41117": "수원 영통구", "41465": "용인 수지구", "41115": "수원 팔달구"}
NAMES = {**SUWON, **BORDER}


def today() -> dt.date:
    return dt.datetime.now(KST).date()


def _json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        return {}


def key(name: str) -> str:
    if name == "datago":
        return str(_json(RADAR / "datago.json").get("service_key", "")).strip()
    return str(_json(RADAR / "settings.json").get(name + "_key", "")).strip()


def datago_key_q() -> str:
    """URL 에 넣을 공공데이터포털 키 (Encoding 키든 Decoding 키든 한 번만 인코딩)."""
    k = key("datago")
    return urllib.parse.quote(urllib.parse.unquote(k), safe="")


def get(url: str, timeout: int = 40) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 BlogRealEstateTools"})
    last = None
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:      # 일시 오류는 잠깐 쉬고 다시
            last = e
            time.sleep(3 * (i + 1))
    raise last


def get_json(url: str, timeout: int = 40):
    return json.loads(get(url, timeout))


# ------------------------------------------------------------------ 국토부 실거래 (매매 상세 · 전월세)
RTMS = {"trade": "RTMSDataSvcAptTradeDev", "rent": "RTMSDataSvcAptRent"}


def rtms(kind: str, lawd: str, ym: str, refresh_days: int = 1) -> list[dict]:
    """한 구·한 달 실거래 전부. 최근 3개월은 신고·등기가 계속 채워지므로 refresh_days 가 지나면 다시 받는다."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{kind}_{lawd}_{ym}.json"
    if p.exists():
        age = (time.time() - p.stat().st_mtime) / 86400
        old_month = (today().year * 12 + today().month) - (int(ym[:4]) * 12 + int(ym[4:])) > 3
        if old_month or age < refresh_days:
            return json.loads(p.read_text(encoding="utf-8"))
    svc = RTMS[kind]
    rows, page = [], 1
    while True:
        u = (f"https://apis.data.go.kr/1613000/{svc}/get{svc}?serviceKey={datago_key_q()}"
             f"&LAWD_CD={lawd}&DEAL_YMD={ym}&numOfRows=1000&pageNo={page}")
        root = ET.fromstring(get(u))
        code = root.findtext(".//resultCode") or ""
        if code not in ("000", "00", "0"):
            raise RuntimeError(f"실거래 {svc} {lawd} {ym}: {code} {root.findtext('.//resultMsg')}")
        items = [{c.tag: (c.text or "").strip() for c in it} for it in root.iter("item")]
        rows += items
        total = int(root.findtext(".//totalCount") or 0)
        if len(rows) >= total or not items:
            break
        page += 1
        time.sleep(0.4)
    p.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    time.sleep(0.4)
    return rows


def num(s):
    s = str(s or "").replace(",", "").strip()
    try:
        return float(s) if s not in ("", "-") else None
    except ValueError:
        return None


def deal_date(r: dict) -> dt.date:
    return dt.date(int(r["dealYear"]), int(r["dealMonth"]), int(r["dealDay"]))


def rgst_date(r: dict):
    s = (r.get("rgstDate") or "").strip()
    if not s:
        return None
    for f in ("%y.%m.%d", "%Y.%m.%d", "%Y%m%d"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    return None


def months_back(end_ym: str, n: int) -> list[str]:
    y, m = int(end_ym[:4]), int(end_ym[4:])
    out = []
    for _ in range(n):
        out.append(f"{y}{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return list(reversed(out))


def kakao(text: str) -> str:
    """발행판 카카오 보내기 재사용. 실패해도 예외를 올리지 않고 사유를 돌려준다."""
    try:
        import sys
        sys.path.insert(0, r"C:\Users\user\Desktop\자동화\블로그용\발행판")
        import kakao_send
        r = kakao_send.send(kakao_send.access_token(kakao_send.load()), text[:200])
        return "SENT" if isinstance(r, dict) and r.get("result_code") == 0 else "KAKAO FAIL " + json.dumps(r, ensure_ascii=False)[:120]
    except BaseException as e:      # 카톡이 실패해도 기록은 남는다
        return f"KAKAO ERR {str(e)[:150]}"
