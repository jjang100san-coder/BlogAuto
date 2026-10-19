# -*- coding: utf-8 -*-
"""금리 스냅샷 — 같은 날 은행별 주담대·전세대출 금리(금감원 finlife) + 한국은행 평균(ECOS)을 저장한다.

  python rates_snapshot.py            오늘 스냅샷 → 금리스냅샷/금리_YYYY-MM-DD.md · data/rates_YYYY-MM-DD.json · rates_history.csv
  python rates_snapshot.py --kakao    끝나고 카톡 요약 한 통

finlife 는 각 은행이 공시한 '전월 취급' 기준 금리 범위다. 내가 실제로 받을 금리는 아니다(글에 그렇게 적는다).
"""
from __future__ import annotations
import csv
import json
import statistics as st
import sys
import urllib.parse

import re_common as C

OUT = C.BASE / "금리스냅샷"
FIN = "https://finlife.fss.or.kr/finlifeapi/"
NAMES = {"mrtg_type": {"A": "아파트", "E": "아파트외"}, "rpay_type": {"D": "분할상환", "S": "만기일시"},
         "lend_rate_type": {"F": "고정", "C": "변동"}}


def finlife(service: str) -> tuple[list, list]:
    k = C.key("finlife")
    base, opts, page = [], [], 1
    while True:
        u = FIN + service + ".json?" + urllib.parse.urlencode(dict(auth=k, topFinGrpNo="020000", pageNo=page))
        r = C.get_json(u)["result"]
        if r.get("err_cd") != "000":
            raise RuntimeError(f"finlife {service}: {r.get('err_cd')} {r.get('err_msg')}")
        base += r.get("baseList", [])
        opts += r.get("optionList", [])
        if page >= int(r.get("max_page_no") or 1):
            break
        page += 1
    return base, opts


def ecos(stat: str, cycle: str, start: str, end: str, item: str) -> list[dict]:
    k = urllib.parse.quote(C.key("ecos"))
    u = f"https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/400/{stat}/{cycle}/{start}/{end}/{item}"
    d = C.get_json(u)
    if "StatisticSearch" not in d:
        raise RuntimeError(f"ECOS {stat}/{item}: {d.get('RESULT')}")
    return [dict(time=x["TIME"], value=float(x["DATA_VALUE"])) for x in d["StatisticSearch"]["row"]]


def summarize(base: list, opts: list, mortgage: bool) -> list[dict]:
    """은행 × 금리유형(× 담보유형) 별 최저·최고 금리. 분할상환만 본다(주담대 실수요)."""
    names = {b["fin_prdt_cd"] + b["kor_co_nm"]: b for b in base}
    rows = {}
    for o in opts:
        if o.get("rpay_type") != "D":
            continue
        if mortgage and o.get("mrtg_type") != "A":
            continue
        b = names.get(o["fin_prdt_cd"] + o.get("kor_co_nm", ""), {}) or next((x for x in base if x["fin_prdt_cd"] == o["fin_prdt_cd"]), {})
        bank = (b.get("kor_co_nm") or o.get("kor_co_nm", "")).replace("주식회사", "").strip()
        typ = NAMES["lend_rate_type"].get(o.get("lend_rate_type"), o.get("lend_rate_type"))
        lo, hi, av = C.num(o.get("lend_rate_min")), C.num(o.get("lend_rate_max")), C.num(o.get("lend_rate_avg"))
        r = rows.setdefault((bank, typ), dict(bank=bank, type=typ, min=None, max=None, avg=[], products=set(), month=b.get("dcls_month", "")))
        if lo is not None:
            r["min"] = lo if r["min"] is None else min(r["min"], lo)
        if hi is not None:
            r["max"] = hi if r["max"] is None else max(r["max"], hi)
        if av is not None:
            r["avg"].append(av)
        r["products"].add(b.get("fin_prdt_nm", o["fin_prdt_cd"]))
    out = []
    for r in rows.values():
        out.append(dict(bank=r["bank"], type=r["type"], min=r["min"], max=r["max"],
                        avg=round(st.mean(r["avg"]), 2) if r["avg"] else None, products=len(r["products"]), month=r["month"]))
    return sorted(out, key=lambda x: (x["type"], x["min"] if x["min"] is not None else 99))


def main():
    day = C.today()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "data").mkdir(exist_ok=True)
    mb, mo = finlife("mortgageLoanProductsSearch")
    rb, ro = finlife("rentHouseLoanProductsSearch")
    mort, rent = summarize(mb, mo, True), summarize(rb, ro, False)
    y = day.year
    base_d = ecos("722Y001", "D", f"{y}0101", day.strftime("%Y%m%d"), "0101000")
    series = {}
    for item, label in [("BECBLA0302", "주택담보대출"), ("BECBLA030201", "고정형 주담대"), ("BECBLA030202", "변동형 주담대"), ("BECBLA03041", "전세자금대출")]:
        series[label] = ecos("121Y006", "M", f"{y-1}{day.month:02d}", day.strftime("%Y%m"), item)
    snap = dict(date=str(day), finlife_mortgage=mort, finlife_rent=rent,
                ecos_base_rate=base_d[-1] if base_d else None, ecos_bank_new_loans=series)
    (OUT / "data" / f"rates_{day}.json").write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")

    hist = OUT / "rates_history.csv"
    new = not hist.exists()
    with hist.open("a", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["조회일", "구분", "은행", "금리유형", "최저", "최고", "평균", "공시월"])
        for kind, rows in (("주담대(아파트·분할)", mort), ("전세대출(분할)", rent)):
            for r in rows:
                w.writerow([day, kind, r["bank"], r["type"], r["min"], r["max"], r["avg"], r["month"]])

    month = next((r["month"] for r in mort if r["month"]), "")
    L = [f"# 금리 스냅샷 — {day}", "",
         "- 출처: 금융감독원 「금융상품 한눈에」 오픈API(은행권, 분할상환 기준) · 한국은행 ECOS(기준금리 722Y001 · 예금은행 대출금리 신규취급액 121Y006)",
         f"- finlife 금리는 은행이 공시한 **{month[:4]}년 {month[4:]}월** 범위다. 내가 실제로 받을 금리가 아니다(심사·우대에 따라 다르다).",
         "- 마스터 0-10: 은행 이름은 써도 된다(내 집 힌트가 아님). 내 대출 조건을 쓸 때는 단지·주소를 넣지 않는다.", ""]
    if snap["ecos_base_rate"]:
        b = snap["ecos_base_rate"]
        L += [f"**한국은행 기준금리 {b['value']}%** ({b['time']} 기준)", ""]
    L += ["## 예금은행 신규취급 평균금리 (한국은행)", "", "| 월 | 주담대 | 고정형 | 변동형 | 전세대출 |", "|---|---|---|---|---|"]
    months = [x["time"] for x in series["주택담보대출"]]
    for m in months[-13:]:
        v = [next((x["value"] for x in series[k] if x["time"] == m), "") for k in ("주택담보대출", "고정형 주담대", "변동형 주담대", "전세자금대출")]
        L.append(f"| {m[:4]}.{m[4:]} | " + " | ".join(f"{x}%" if x != "" else "—" for x in v) + " |")
    for title, rows in (("은행별 주택담보대출 (아파트 · 분할상환)", mort), ("은행별 전세자금대출 (분할상환)", rent)):
        L += ["", f"## {title}", "", "| 은행 | 유형 | 공시 최저 | 공시 최고 | 전월 취급 평균 | 상품 수 |", "|---|---|---|---|---|---|"]
        for r in rows:
            f = lambda x: f"{x:.2f}%" if isinstance(x, (int, float)) else "—"
            L.append(f"| {r['bank']} | {r['type']} | {f(r['min'])} | {f(r['max'])} | {f(r['avg'])} | {r['products']} |")
    md = OUT / f"금리_{day}.md"
    md.write_text("\n".join(L) + "\n", encoding="utf-8")
    fixed = [r for r in mort if r["type"] == "고정" and r["min"] is not None]
    low = min(fixed, key=lambda r: r["min"]) if fixed else None
    text = (f"[금리 스냅샷 {day}]\n기준금리 {snap['ecos_base_rate']['value']}%\n"
            f"주담대 평균(신규) {series['주택담보대출'][-1]['value']}% ({series['주택담보대출'][-1]['time']})\n"
            + (f"고정형 최저 {low['bank']} {low['min']:.2f}%\n" if low else "") + f"은행 {len({r['bank'] for r in mort})}곳 · 공시월 {month}")
    print(text)
    print(md)
    if "--kakao" in sys.argv:
        print(C.kakao(text))


if __name__ == "__main__":
    main()
