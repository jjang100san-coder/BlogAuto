# -*- coding: utf-8 -*-
"""기흥·영통 경계 4개 구 비교표(10/15 이사지 정정 — 예전 기흥·영통 경계 4개 구) — 국토부 실거래(매매 상세·전월세) + 행안부 인구.

  python compare_suwon.py                  지난달까지 12개월 → 수원4개구/비교표_YYYY-MM.md · .csv · 카드 2장
  python compare_suwon.py --end 202609     끝 달 지정
  python compare_suwon.py --kakao          끝나고 카톡 요약

마스터 0-10(부동산 공공데이터 집계, 분야 예외): 구 단위 집계만 낸다. 단지명·동·호·지번은 결과에 넣지 않는다.
지표 정의는 결과 md 의 「센 방법」에 그대로 적힌다.
"""
from __future__ import annotations
import csv
import json
import statistics as st
import sys
import urllib.request

import re_common as C

OUT = C.BASE / "기흥영통4개구"
FONT = "C:/Windows/Fonts/malgun.ttf"
FONTB = "C:/Windows/Fonts/malgunbd.ttf"


def md(x):
    return st.median(x) if x else None


def r1(x, n=1):
    return None if x is None else round(x, n)


def in84(r):
    a = C.num(r.get("excluUseAr"))
    return a is not None and 80 <= a <= 86


def gu_metrics(T: list, R: list) -> dict:
    """한 구의 최근 3개월 집계. T=매매 상세, R=전월세."""
    valid = [r for r in T if not r.get("cdealType")]
    jeon = [r for r in R if (C.num(r.get("monthlyRent")) or 0) == 0]
    # 같은 단지(aptSeq)·같은 면적(반올림 ㎡)끼리 매매 중위와 전세 중위를 짝지어 비율의 중위
    key = lambda r: (r.get("aptSeq"), round(C.num(r["excluUseAr"]) or 0))
    sale, dep = {}, {}
    for r in valid:
        sale.setdefault(key(r), []).append(C.num(r["dealAmount"]))
    for r in jeon:
        dep.setdefault(key(r), []).append(C.num(r["deposit"]))
    ratios = [100 * st.median(dep[k]) / st.median(sale[k]) for k in sale if k in dep]
    renew = [r for r in jeon if r.get("contractType") == "갱신"]
    inc = [100 * (C.num(r["deposit"]) / C.num(r["preDeposit"]) - 1) for r in renew
           if C.num(r.get("preDeposit")) and (C.num(r.get("preMonthlyRent")) or 0) == 0]
    return dict(
        trades=len(T), trades_valid=len(valid),
        cancel_pct=r1(100 * (len(T) - len(valid)) / len(T)) if T else None,
        direct_pct=r1(100 * sum("직거래" in (r.get("dealingGbn") or "") for r in valid) / len(valid)) if valid else None,
        corp_buy_pct=r1(100 * sum("법인" in (r.get("buyerGbn") or "") for r in valid) / len(valid)) if valid else None,
        sale84=r1(md([C.num(r["dealAmount"]) / 1e4 for r in valid if in84(r)]), 2),
        sale84_n=sum(in84(r) for r in valid),
        rents=len(R), jeonse_pct=r1(100 * len(jeon) / len(R)) if R else None,
        jeon84=r1(md([C.num(r["deposit"]) / 1e4 for r in jeon if in84(r)]), 2),
        jeon84_new=r1(md([C.num(r["deposit"]) / 1e4 for r in jeon if in84(r) and r.get("contractType") == "신규"]), 2),
        jeon84_renew=r1(md([C.num(r["deposit"]) / 1e4 for r in jeon if in84(r) and r.get("contractType") == "갱신"]), 2),
        renew_pct=r1(100 * sum(r.get("contractType") == "갱신" for r in R) / len(R)) if R else None,
        rr_right_pct=r1(100 * sum(r.get("useRRRight") == "사용" for r in R) / len(R)) if R else None,
        renew_inc_median=r1(md(inc)), renew_inc_n=len(inc),
        jeonse_ratio=r1(md(ratios)), jeonse_ratio_pairs=len(ratios),
    )


def register_lag(T_first_month: list) -> dict:
    v = [r for r in T_first_month if not r.get("cdealType")]
    days = [(C.rgst_date(r) - C.deal_date(r)).days for r in v if C.rgst_date(r)]
    return dict(month_n=len(v), registered_pct=r1(100 * len(days) / len(v)) if v else None, lag_median=md(days))


def population(lawd: str, months: list[str]) -> list[dict]:
    """월별 인구·세대 (단일 시군구). API 는 3개월 이내 구간만 받는다."""
    out = []
    for i in range(0, len(months), 3):
        fr, to = months[i], months[min(i + 2, len(months) - 1)]
        u = (f"https://apis.data.go.kr/1741000/stdgPpltnHhStus/selectStdgPpltnHhStus?serviceKey={C.datago_key_q()}"
             f"&stdgCd={lawd}00000&srchFrYm={fr}&srchToYm={to}&lv=6&regSeCd=1&type=JSON&numOfRows=20&pageNo=1")
        try:
            d = C.get_json(u)["Response"]
            items = (d.get("items") or {}).get("item") or []
            items = items if isinstance(items, list) else [items]
            for x in items:
                out.append(dict(ym=x.get("statsYm"), pop=int(x.get("totNmprCnt") or 0), hh=int(x.get("hhCnt") or 0)))
        except Exception:
            pass
    return sorted({x["ym"]: x for x in out if x["ym"]}.values(), key=lambda x: x["ym"])


def card(path, title, sub, header, rows, foot):
    from PIL import Image, ImageDraw, ImageFont
    f = lambda s, b=False: ImageFont.truetype(FONTB if b else FONT, s)
    W, H = 1200, 1200
    im = Image.new("RGB", (W, H), (250, 248, 244)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=(47, 93, 138))
    d.text((70, 66), title, font=f(50, True), fill=(31, 35, 40))
    d.text((70, 140), sub, font=f(28), fill=(100, 107, 115))
    cols = len(header); x0, cw = 70, (W - 140) // cols
    y = 220
    d.rounded_rectangle([70, y, W - 70, y + 70], radius=14, fill=(47, 93, 138))
    for i, h in enumerate(header):
        d.text((x0 + i * cw + 20, y + 18), h, font=f(28, True), fill=(255, 255, 255))
    y += 86
    rh = min(118, (H - 180 - y) // max(1, len(rows)))
    for j, row in enumerate(rows):
        d.rounded_rectangle([70, y, W - 70, y + rh - 14], radius=14, fill=(231, 238, 246) if j % 2 == 0 else (241, 244, 249))
        for i, c in enumerate(row):
            d.text((x0 + i * cw + 20, y + (rh - 14) // 2 - 20), str(c), font=f(34 if i else 34, i == 0), fill=(31, 35, 40))
        y += rh
    d.line([70, H - 130, W - 70, H - 130], fill=(225, 222, 215), width=2)
    yy = H - 112
    for line in foot.split("\n"):
        d.text((70, yy), line, font=f(22), fill=(100, 107, 115)); yy += 32
    im.save(path)


def main():
    args = sys.argv[1:]
    today = C.today()
    end = args[args.index("--end") + 1] if "--end" in args else f"{today.year if today.month > 1 else today.year - 1}{(today.month - 1 or 12):02d}"
    months12 = C.months_back(end, 12)
    last3 = months12[-3:]
    OUT.mkdir(parents=True, exist_ok=True)
    res, trend = {}, {}
    for lawd, gu in C.BORDER.items():
        T3 = [r for ym in last3 for r in C.rtms("trade", lawd, ym)]
        R3 = [r for ym in last3 for r in C.rtms("rent", lawd, ym)]
        res[gu] = gu_metrics(T3, R3)
        res[gu].update({"lag_" + k: v for k, v in register_lag(C.rtms("trade", lawd, last3[0])).items()})
        trend[gu] = []
        for ym in months12:
            T = [r for r in C.rtms("trade", lawd, ym) if not r.get("cdealType")]
            R = C.rtms("rent", lawd, ym)
            trend[gu].append(dict(ym=ym, trades=len(T), sale84=r1(md([C.num(r["dealAmount"]) / 1e4 for r in T if in84(r)]), 2),
                                  rents=len(R)))
        pop = population(lawd, months12)
        res[gu]["pop"] = pop[-1] if pop else None
        res[gu]["pop_first"] = pop[0] if pop else None
        print(gu, "완료", flush=True)

    tag = f"{end[:4]}-{end[4:]}"
    period = f"{last3[0][:4]}.{last3[0][4:]}~{last3[-1][:4]}.{last3[-1][4:]}"
    (OUT / "data").mkdir(exist_ok=True)
    (OUT / "data" / f"compare_{end}.json").write_text(json.dumps(dict(end=end, last3=last3, metrics=res, trend=trend, made=str(today)), ensure_ascii=False, indent=1), encoding="utf-8")
    with (OUT / f"비교표_{tag}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        keys = list(next(iter(res.values())).keys())
        w.writerow(["구"] + keys)
        for gu, m in res.items():
            w.writerow([gu] + [json.dumps(m[k], ensure_ascii=False) if isinstance(m[k], dict) else m[k] for k in keys])

    tot_t = sum(m["trades"] for m in res.values()); tot_r = sum(m["rents"] for m in res.values())
    src = (f"국토교통부 실거래가 공개 자료(아파트 매매 상세·전월세 API), 기흥·영통 경계 4개 구 {period} 계약분 매매 {tot_t:,}건·전월세 {tot_r:,}건, "
           f"{today} 조회 기준. 인구는 행정안전부 주민등록 인구 API.")
    L = [f"# 기흥·영통 경계 4개 구 비교표 — {period}", "", f"- 출처: {src}",
         "- 마스터 0-10: 구 단위 집계만. 단지명·동·호·지번은 쓰지 않는다. 원인·전망은 쓰지 않는다.",
         "- 실거래는 신고 기한(계약 후 30일)과 등기 때문에 최근 달이 계속 채워진다 — 다시 돌리면 숫자가 조금 바뀐다.", "",
         "## 1. 매매 (최근 3개월)", "", "| 구 | 매매 건수 | 84㎡급 매매 중위 | 해제 표시 | 직거래 | 법인 매수 |", "|---|---|---|---|---|---|"]
    for gu, m in res.items():
        L.append(f"| {gu} | {m['trades']:,} | {m['sale84']}억 ({m['sale84_n']}건) | {m['cancel_pct']}% | {m['direct_pct']}% | {m['corp_buy_pct']}% |")
    L += ["", "## 2. 전세 (최근 3개월)", "", "| 구 | 전월세 건수 | 전세 비중 | 84㎡급 전세 중위 | 신규 | 갱신 | 같은 단지 전세가율 |", "|---|---|---|---|---|---|---|"]
    for gu, m in res.items():
        L.append(f"| {gu} | {m['rents']:,} | {m['jeonse_pct']}% | {m['jeon84']}억 | {m['jeon84_new']}억 | {m['jeon84_renew']}억 | {m['jeonse_ratio']}% ({m['jeonse_ratio_pairs']}쌍) |")
    L += ["", "## 3. 갱신 계약", "", "| 구 | 갱신 계약 비중 | 갱신요구권 사용 | 갱신 전세 보증금 인상률 중위 |", "|---|---|---|---|"]
    for gu, m in res.items():
        L.append(f"| {gu} | {m['renew_pct']}% | {m['rr_right_pct']}% | {m['renew_inc_median']}% ({m['renew_inc_n']}건) |")
    L += ["", f"## 4. 계약 → 등기 ({last3[0][:4]}.{last3[0][4:]} 계약분, {today} 기준)", "", "| 구 | 계약 건수 | 등기 끝난 비율 | 등기까지 중위 |", "|---|---|---|---|"]
    for gu, m in res.items():
        L.append(f"| {gu} | {m['lag_month_n']} | {m['lag_registered_pct']}% | {m['lag_lag_median']:.0f}일 |")
    L += ["", "※ 아직 등기 안 된 거래가 빠진 값이라 실제 중위는 이보다 길다.", "",
          "## 5. 인구·세대 (주민등록)", "", "| 구 | 인구 | 세대 | 12개월 전 대비 인구 |", "|---|---|---|---|"]
    for gu, m in res.items():
        p, p0 = m.get("pop"), m.get("pop_first")
        if p:
            L.append(f"| {gu} | {p['pop']:,} ({p['ym'][:4]}.{p['ym'][4:]}) | {p['hh']:,} | {p['pop'] - p0['pop']:+,} ({p0['ym'][:4]}.{p0['ym'][4:]} → ) |")
    L += ["", "## 6. 12개월 추이 — 매매 건수 · 84㎡급 매매 중위(억)", "", "| 월 | " + " | ".join(C.BORDER.values()) + " |", "|---|" + "---|" * 4]
    for i, ym in enumerate(months12):
        L.append(f"| {ym[:4]}.{ym[4:]} | " + " | ".join(f"{trend[g][i]['trades']} · {trend[g][i]['sale84']}" for g in C.BORDER.values()) + " |")
    L += ["", "## 센 방법", "",
          "- 84㎡급 = 전용 80~86㎡. 매매는 해제 표시 거래를 뺐다. 전세 = 월세 0원 계약.",
          "- 같은 단지 전세가율 = 같은 단지(국토부 단지 일련번호)·같은 전용면적(㎡ 반올림)끼리 전세 중위 ÷ 매매 중위, 그 비율들의 중위.",
          "- 갱신 인상률 = 갱신 전세 중 종전 보증금이 있고 종전 월세 0원인 계약의 (보증금 ÷ 종전 보증금 − 1).",
          "- 계약 → 등기 = 등기일이 찍힌 거래의 (등기일 − 계약일).", ""]
    mdp = OUT / f"비교표_{tag}.md"
    mdp.write_text("\n".join(L) + "\n", encoding="utf-8")

    foot = f"출처: 국토부 실거래가 공개 자료 · 기흥·영통 경계 4개 구 {period} 계약분 매매 {tot_t:,}건 · 전월세 {tot_r:,}건\n{today} 조회 · 84㎡급 = 전용 80~86㎡ · 해제 거래 제외 · 직접 만든 표"
    card(OUT / f"card1_{tag}.png", "기흥·영통 경계 4개 구, 같은 84㎡의 매매와 전세", f"{period} 계약분 중위값 · 같은 단지 전세가율",
         ["구", "매매 중위", "전세 중위", "전세가율"],
         [[g, f"{m['sale84']}억", f"{m['jeon84']}억", f"{m['jeonse_ratio']}%"] for g, m in res.items()], foot)
    card(OUT / f"card2_{tag}.png", "같은 84㎡ 전세, 새로 들어가면 더 비싸다", f"{period} 신규 vs 갱신 전세 보증금 중위",
         ["구", "신규", "갱신", "갱신 인상률"],
         [[g, f"{m['jeon84_new']}억", f"{m['jeon84_renew']}억", f"{m['renew_inc_median']}%"] for g, m in res.items()], foot)
    text = f"[기흥·영통 경계 4개 구 {period}]\n" + "\n".join(f"{g} 매매{m['trades']} 84㎡ {m['sale84']}억 / 전세 {m['jeon84']}억" for g, m in res.items())
    print(text); print(mdp)
    if "--kakao" in args:
        print(C.kakao(text))


if __name__ == "__main__":
    main()
