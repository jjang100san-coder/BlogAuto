# -*- coding: utf-8 -*-
"""v2(10/15 재검토 반영) — 바뀐 카드만 다시 정의하고 순서를 새로 매긴다.
숫자: base data\\로직근거\\v2\\out\\v2_all.json(실거래 보강) · v2_docs\\iros_summary_연별.tsv(등기정보광장) ·
LH집값_공식근거보강_2026-10-15.md(기관 전망·입주 예정·금리 기대 — 표에서 옮긴 값은 아래 상수에 출처와 함께 둔다)."""
import os, json, csv
import make_cards as M
from make_cards import (canvas, box, foot, ctext, chip, F_T, F_H, F_B, F_S, F_SM, F_M, F_L, F_BIG, F_MID,
                        INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, NAVY, DIM, fmt, save, reuse, REUSE)
V2 = os.path.join(M.ROOT, "base data", "로직근거", "v2", "out", "v2_all.json")
IROS = os.path.join(M.ROOT, "base data", "로직근거", "v2_docs", "iros_summary_연별.tsv")
D = json.load(open(V2, encoding="utf-8"))


def hbar(d, base_x, y, val, scale, col, f=F_L):
    L = abs(val) * scale
    if val < 0: d.rectangle([base_x - L, y + 10, base_x, y + 62], fill=col)
    else: d.rectangle([base_x, y + 10, base_x + L, y + 62], fill=col)
    t = fmt(val) + "%"
    tx = base_x + L + 10 if val >= 0 else base_x + 10
    d.text((tx, y + 18), t, font=f, fill=col)


# ---------- 기다린 사람 — 서울·경기인천·지방 ----------
def card_wait(name):
    rows = [("서울 25개 구", D["A1"]["seoul_total"]), ("경기·인천 14곳", D["A2"]["ggic_total"]), ("지방 광역시·세종", D["A2"]["metro_total"])]
    im, d = canvas("2년 기다린 사람은 어디서나 싸게 샀다, 그 뒤는 지역마다 갈렸다",
                   "같은 단지·같은 면적 실거래 가격 변화(짝의 가운데 값)")
    panels = [("2021년 고점에 산 값 → 2년 기다려 산 값", "PEAK->W2", 90),
              ("2년 기다려 산 값 → 지금 값", "W2->NOW", 735)]
    for title, key, x0 in panels:
        box(d, (x0, 150, x0 + 575, 200), LIGHT if key == "PEAK->W2" else PINK, title, F_M, BLUE if key == "PEAK->W2" else RED)
        base_x = x0 + (480 if key == "PEAK->W2" else 330)
        d.line([base_x, 225, base_x, 560], fill=GRAY, width=2)
        for i, (g, v) in enumerate(rows):
            y = 245 + i * 105
            val = v[key]["median_pct"]
            d.text((x0 + 5, y + 20), g, font=F_M, fill=INK)
            hbar(d, base_x, y, val, 7.5, RED if val > 0 else BLUE)
    box(d, (90, 590, 1310, 690), SAND,
        "서울은 25개 구 모두, 경기·인천 14곳 모두, 지방 6곳 모두 2년 기다린 쪽이 쌌다.\n"
        "그 뒤로 서울은 25개 구 모두 올랐고, 지방은 6곳 중 5곳이 더 내렸다", F_S, INK)
    foot(d, "국토교통부 아파트 매매 실거래(해제 제외) 직접 계산 · 고점 2021.8~2022.1 · 2년 뒤 2023.8~2024.1 · 지금 2026.4~9 · 시·구 단위")
    save(im, name)


# ---------- 첫 집 구입 vs 대출 비율 (등기정보광장) ----------
def card_firsthome(name):
    rows = {r["연"]: r for r in csv.DictReader(open(IROS, encoding="utf-8"), delimiter="\t")}
    yrs = ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]
    im, d = canvas("첫 집 사는 사람은 많아졌다, 대출을 더 끼고 사는 건 아니다",
                   "서울 집합건물 매매 등기 — 왼쪽: 생애 첫 구입 비중 / 오른쪽: 대출 낀 매매의 근저당 금액 ÷ 거래가")
    for p, (key, x0, col, lab) in enumerate([("비중_서울(÷부동산)", 90, RED, "생애 첫 구입 비중"),
                                             ("채권최고액비율_서울(월평균)", 735, NAVY, "근저당 금액 ÷ 거래가")]):
        ctext(d, x0 + 290, 150, lab, F_M, col)
        base, top = 560, 210
        for i, y in enumerate(yrs):
            v = float(rows[y][key]); x = x0 + 15 + i * 70
            h = (v - 20) / 40 * (base - top)
            c = col if y in ("2021", "2026") else DIM
            d.rectangle([x, base - h, x + 46, base], fill=c)
            ctext(d, x + 23, base - h - 26, f"{v:.1f}", F_SM, c if c != DIM else GRAY)
            ctext(d, x + 23, base + 8, ("2026\n1~9월" if y == "2026" else y).split("\n")[0], F_SM, INK)
            if y == "2026": ctext(d, x + 23, base + 30, "1~9월", F_SM, GRAY)
        d.line([x0, base, x0 + 580, base], fill=GRAY, width=2)
    box(d, (90, 615, 1310, 700), SAND,
        "첫 집 구입은 2014년 이후 가장 많다(8월 한 달 53.7%). 그런데 대출 낀 매매의 근저당 비율은 2021년보다 낮다.\n"
        "「경쟁적으로 산다」는 보이고, 「대출을 더 많이 끼고 산다」는 아직 숫자로 안 보인다", F_S, INK)
    foot(d, "대법원 등기정보광장 소유권이전(매매) 직접 계산 · 비중 = 생애 첫 구입 매수인 ÷ 매매 부동산 수 · 막대는 20%부터")
    save(im, name)


# ---------- 대출 규제 전후 — 계절 보정 ----------
def card_loan(name):
    ev = {e["event"][:10]: e for e in D["C1"]["events"]}
    def g(k, basis):
        e = [v for kk, v in ev.items() if kk.startswith(k)][0]
        return e[basis]["season_adj_pct"], e["idx_서울"]["after_pct"]
    rows = [("2017.8", "8·2", *g("2017-08", "신고_rone"), ""), ("2018.9", "9·13", *g("2018-09", "신고_rone"), ""),
            ("2019.12", "12·16", *g("2019-12", "계약"), "※"), ("2021.7", "DSR 1단계", *g("2021-07", "신고_rone"), ""),
            ("2022.1", "DSR 2단계", *g("2022-01", "신고_rone"), ""), ("2025.6", "6·27", *g("2025-06", "신고_rone"), ""),
            ("2025.10", "10·15", *g("2025-10", "신고_rone"), "")]
    im, d = canvas("계절을 빼도 거래는 대개 줄었다, 값이 크게 내린 건 한 번",
                   "서울 아파트 — 대출 규제 앞 3개월 → 뒤 3개월 거래(평년 계절 변화를 뺀 값) · 발표 뒤 12개월 값")
    d.text((300, 150), "거래 변화(계절 보정)", font=F_M, fill=NAVY)
    d.text((900, 150), "발표 뒤 12개월 서울 매매지수", font=F_M, fill=NAVY)
    cx1, cx2 = 560, 1080
    for cx in (cx1, cx2): d.line([cx, 190, cx, 190 + 7 * 62], fill=GRAY, width=2)
    for i, (ym, nm, t, p, mark) in enumerate(rows):
        y = 195 + i * 62
        d.text((90, y + 10), ym, font=F_S, fill=GRAY); d.text((190, y + 6), nm, font=F_M, fill=INK)
        L = abs(t) * 3.6; col = BLUE if t < 0 else RED
        if t < 0: d.rectangle([cx1 - L, y + 8, cx1, y + 44], fill=col)
        else: d.rectangle([cx1, y + 8, cx1 + L, y + 44], fill=col)
        d.text((cx1 + 10 if t < 0 else cx1 + L + 8, y + 10), fmt(t) + "%" + (" " + mark if mark else ""), font=F_S, fill=col)
        L2 = abs(p) * 14; col2 = RED if p > 0 else BLUE
        if p < 0: d.rectangle([cx2 - L2, y + 8, cx2, y + 44], fill=col2)
        else: d.rectangle([cx2, y + 8, cx2 + L2, y + 44], fill=col2)
        lab = fmt(p) + "%" + (" (10개월)" if nm == "10·15" else "")
        d.text((cx2 + L2 + 8 if p > 0 else cx2 + 12, y + 10), lab, font=F_M if nm in ("DSR 2단계",) else F_S, fill=col2)
    box(d, (90, 645, 1310, 725), SAND,
        "연구들도 같은 쪽이다: 거래·대출은 줄였고 값을 누르는 힘은 작았다(한은 2023, AMRO 2026).\n다만 「규제가 없었으면 더 올랐을 것」은 이 비교로 가를 수 없다", F_S, INK)
    foot(d, "부동산원 R-ONE 거래(신고)·국토부 실거래(계약, ※12·16)·매매가격지수 직접 계산 · 계절 보정 = 다른 해 같은 달 변화의 가운데 값을 뺌")
    save(im, name)


# ---------- 앞을 보는 지표 ----------
def card_ahead(name):
    im, d = canvas("앞을 보는 지표는 엇갈린다 — 같은 방향은 금리 하나",
                   "「급락할 가능성이 좀 많다」를 앞날 지표에 대 보면")
    tiles = [("입주 예정", "서울 한 해 평균\n약 2.5만 호", "2026 하반기~2028 상반기\n적은 구간", "급락과 반대", BLUE, LIGHT,
              "부동산원·R114 공동(2026.8.31)"),
             ("기관 진단", "한은·KDI\n「상승 압력」", "하락을 내다본\n공식 기관 문장 없음", "급락과 반대", BLUE, LIGHT,
              "한은 금융안정 상황(2026.9)·KDI"),
             ("금리 기대", "10월 동결 뒤\n추가 인상 전망", "금통위원 금리 전망\n21개 중 16개가 인상", "급락과 같은 방향", RED, PINK,
              "금통위 의사록(8월)·보도")]
    for i, (h, big, sub, tag, col, bg, src) in enumerate(tiles):
        x = 90 + i * 410
        d.rounded_rectangle([x, 160, x + 380, 590], radius=22, fill=bg)
        ctext(d, x + 190, 185, h, F_M, GRAY)
        for j, ln in enumerate(big.split("\n")): ctext(d, x + 190, 235 + j * 46, ln, F_L, INK)
        for j, ln in enumerate(sub.split("\n")): ctext(d, x + 190, 355 + j * 30, ln, F_S, GRAY)
        w = d.textlength(tag, font=F_M) + 40
        d.rounded_rectangle([x + 190 - w / 2, 450, x + 190 + w / 2, 496], radius=23, fill=col)
        ctext(d, x + 190, 457, tag, F_M, WHITE)
        ctext(d, x + 190, 540, src, F_SM, GRAY)
    box(d, (90, 620, 1310, 700), SAND, "지금 지표로는 급락이 안 보이고, 앞을 보는 지표는 엇갈린다. 금리 칸은 10월 22일 결정 뒤 다시 본다", F_S, INK)
    foot(d, "부동산원·R114 공동주택 입주예정물량(2026.8.31) · 한국은행 금융안정 상황(2026.9)·금통위 의사록(2026.8.27) · 2026.10.15 조회")
    save(im, name)


# ---------- 1989 — 겹친 것들 표시 ----------
def card_1989(name):
    kb = M.ecos_txt("ECOS_901Y062_KB매매_P63ACA.txt")
    ks = sorted(k for k in kb if "198601" <= k <= "200112")
    b0 = kb["198904"]
    im, d = canvas("1989년 신도시 발표, 입주 전 2년은 올랐고 첫 입주 무렵부터 내렸다",
                   "KB 서울 아파트 매매가격지수(1989년 4월 = 100) — 당시 KB 지수는 표본 2,000여 호의 시세 조사")
    gx0, gx1, gy0, gy1 = 130, 1300, 560, 190
    vmin, vmax = 50, 175
    def X(k): return gx0 + ks.index(k) / (len(ks) - 1) * (gx1 - gx0)
    def Y(v): return gy0 - (v - vmin) / (vmax - vmin) * (gy0 - gy1)
    for v in (80, 100, 120, 140):
        d.line([gx0, Y(v), gx1, Y(v)], fill=(230, 230, 225), width=1); d.text((gx0 - 50, Y(v) - 12), str(v), font=F_SM, fill=GRAY)
    d.line([(X(k), Y(kb[k] / b0 * 100)) for k in ks], fill=NAVY, width=4)
    for yy in range(1986, 2002, 2): d.text((X(f"{yy}01") - 22, gy0 + 10), str(yy), font=F_SM, fill=GRAY)
    marks = [("198904", "신도시 발표", AMBER, -75), ("199104", "정점 " + fmt(M.pct(kb["198904"], kb["199104"])) + "%\n(발표 뒤 2년)", RED, -95),
             ("199109", "분당 첫 입주", GREEN, 70), ("199404", "정점 뒤 3년\n" + fmt(M.pct(kb["199104"], kb["199404"])) + "%", BLUE, 55),
             ("200108", "정점 회복\n(124개월 뒤)", GRAY, -80)]
    for k, lab, col, dy in marks:
        x, y = X(k), Y(kb[k] / b0 * 100)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=col)
        for j, ln in enumerate(lab.split("\n")): ctext(d, x, y + dy + j * 28, ln, F_M if j == 0 else F_S, col)
    box(d, (90, 610, 1310, 715), SAND,
        "같은 시기에 겹친 것: 토지공개념 3법(1989.12) · 5·8 대책(1990, 비업무용 부동산 담보대출 제한) · 회사채 금리 18.8%(1991.4)\n"
        "· 정부의 주택 건설 억제(1991.5)와 신도시 분양 순연. 무엇이 얼마나 내렸는지는 이 숫자로 가를 수 없다", F_S, INK)
    foot(d, "한국은행 ECOS KB 주택매매가격지수(서울 아파트) 직접 계산 · 200만 호 = 1988~1991 허가 기준 214만 호(건설부 1992)")
    save(im, name)


# ---------- 점검표 ----------
def card_score(name):
    im, d = canvas("사장의 로직, 공개된 숫자에 대 보니", "2026년 10월 15일까지 공개된 공공 통계·연구 기준 — 예측 아님")
    rows = [("공급은 늦게 온다", "착공 반토막 → 약 30개월 뒤 입주", "숫자와 맞는다", GREEN),
            ("대출로 경쟁적으로 산다", "첫 집 구입 최고, 대출 비율은 낮아짐", "반만 보인다", AMBER),
            ("대출을 묶으면 완만해진다", "거래·대출은 줄고 값 효과는 작음(연구)", "효과가 작게 나온다", AMBER),
            ("금리가 계속 오른다", "+0.5%p, 시장은 추가 인상 전망", "방향은 맞고 폭은 작다", AMBER),
            ("기다리면 손해 안 본다", "서울 2021년엔 맞고 2023년엔 반대", "언제·어디냐에 달렸다", AMBER),
            ("급락할 가능성이 좀 많다", "87주 상승·입주 적음·기관 「상승 압력」", "지금 지표로는 안 보인다", BLUE)]
    d.text((110, 150), "사장의 로직", font=F_M, fill=GRAY); d.text((500, 150), "숫자", font=F_M, fill=GRAY); d.text((980, 150), "판정", font=F_M, fill=GRAY)
    for i, (a, b, c, col) in enumerate(rows):
        y = 195 + i * 82
        d.rounded_rectangle([90, y, 1310, y + 70], radius=14, fill=WHITE, outline=(225, 225, 220), width=2)
        d.text((110, y + 18), a, font=F_M, fill=INK)
        d.text((500, y + 21), b, font=F_S, fill=INK)
        w = d.textlength(c, font=F_M) + 40
        d.rounded_rectangle([970, y + 12, 970 + w, y + 58], radius=23, fill=col)
        d.text((990, y + 19), c, font=F_M, fill=WHITE)
    foot(d, "출처: 국토교통부(KOSIS·실거래)·한국부동산원·한국은행 ECOS·대법원 등기정보광장·한은·AMRO 연구, 이 글의 앞 그림들과 같은 숫자")
    save(im, name)


if __name__ == "__main__":
    ORDER = [("01_two_dates.png", None), ("03_logic_pillars.png", None), ("05_supply_parcel.png", None), (None, M.card_supply),
             ("R2_supply_path.png", None), ("R3_first_home_loan.png", None), (None, card_firsthome), (None, card_loan),
             ("07_rate_jump.png", None), (None, M.card_rate), ("09_two_big_drops.png", None), (None, card_wait),
             (None, card_ahead), (None, card_1989), (None, M.card_bogeum), (None, card_score),
             ("14_same_numbers.png", None), ("15_my_calendar.png", None)]
    for f in os.listdir(M.HERE):
        if f.startswith("261015_") and f.endswith(".png") and f != "261015_1.png": os.remove(os.path.join(M.HERE, f))
    for i, (src, fn) in enumerate(ORDER, start=2):
        n = f"261015_{i}.png"
        if src: reuse(src, n, REUSE[src])
        else: fn(n)
