# -*- coding: utf-8 -*-
"""LH 사장 집값 글(부동산, 10/15) — 새 카드 8장 + 기존 그림 9장 출처 줄 교체 복사.
숫자는 base data\\로직근거\\out\\*.json · 집값하락기\\ECOS 원표에서 직접 읽는다(손으로 옮기지 않음).
기존 그림의 맨 아래 「근거: 공부노트 §…」 줄은 독자가 못 알아보는 내부 표시라 공개 출처 줄로 덮어 쓴다."""
import os, sys, json, shutil
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "..", "구구절절_컨텐츠", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
OUT_J = os.path.join(ROOT, "base data", "로직근거", "out")
RAW = os.path.join(ROOT, "base data", "로직근거", "raw")
ECOS = os.path.join(ROOT, "base data", "집값하락기")
F_SM = font(18); F_M = font(24, True); F_L = font(30, True); F_BIG = font(54, True); F_MID = font(38, True)
NAVY = (40, 60, 110); DIM = (200, 200, 195)


def J(n): return json.load(open(os.path.join(OUT_J, n + ".json"), encoding="utf-8"))


def ecos_txt(n):
    s = {}
    for ln in open(os.path.join(ECOS, n), encoding="utf-8"):
        p = ln.split()
        if len(p) >= 2 and p[0].isdigit(): s[p[0]] = float(p[1])
    return s


def pct(a, b): return (b / a - 1) * 100


def fmt(x, nd=1): return (f"{x:+.{nd}f}").replace("-", "-")


def save(im, n): im.save(os.path.join(HERE, n)); print("saved", n)


def chip(d, x, y, text, col=NAVY, f=F_M):
    w = d.textlength(text, font=f) + 36
    d.rounded_rectangle([x, y, x + w, y + f.size + 18], radius=(f.size + 18) // 2, fill=col)
    d.text((x + 18, y + 7), text, font=f, fill=WHITE)
    return w


# ---------- 카드 A: 기다린 사람 (같은 단지) ----------
def card_wait(name):
    d0 = J("a4_same_complex")
    rows = [("노원구", d0["서울 노원구"]), ("마포구", d0["서울 마포구"]), ("송파구", d0["서울 송파구"])]
    im, d = canvas("2년 기다린 사람은 싸게 샀다, 그 뒤까지 기다린 사람은 비싸게 샀다",
                   "서울 3개 구, 같은 단지·같은 면적 실거래 가격 변화(가운데 값)")
    # 두 판: 왼쪽 2021 고점 → 2년 뒤, 오른쪽 2년 뒤 → 지금
    panels = [("2021년 고점에 산 값 → 2년 기다려 산 값", "PEAK->W2", BLUE, 90),
              ("2년 기다려 산 값 → 지금 값", "W2->NOW", RED, 735)]
    for title, key, col, x0 in panels:
        box(d, (x0, 150, x0 + 575, 200), LIGHT if col == BLUE else PINK, title, F_M, col)
        base_x = x0 + 300
        d.line([base_x, 225, base_x, 560], fill=GRAY, width=2)
        for i, (g, v) in enumerate(rows):
            y = 245 + i * 105
            val = v[key]["median_pct"]
            d.text((x0 + 10, y + 18), g, font=F_L, fill=INK)
            L = abs(val) * 5.2
            if val < 0: d.rectangle([base_x - L, y + 10, base_x, y + 62], fill=col)
            else: d.rectangle([base_x, y + 10, base_x + L, y + 62], fill=col)
            tx = base_x - L - 10 - d.textlength(fmt(val) + "%", font=F_L) if val < 0 else base_x + L + 10
            if val < 0 and tx < x0 + 110: tx = base_x + 12
            d.text((tx, y + 18), fmt(val) + "%", font=F_L, fill=col)
    box(d, (90, 590, 1310, 690), SAND,
        "세 구 모두 2021년 고점 무렵보다 2년 기다린 쪽이 같은 집을 싸게 샀다(짝의 90% 넘게).\n"
        "그런데 그 2023년 값보다 지금은 세 구 모두 비싸다. 「기다리면 손해 안 본다」는 언제까지 기다리느냐에 달렸다", F_S, INK)
    foot(d, "국토교통부 아파트 매매 실거래(해제 제외) 직접 계산 · 고점 2021.8~2022.1 · 2년 뒤 2023.8~2024.1 · 지금 2026.4~9 · 구 단위")
    save(im, name)


# ---------- 카드 B: 대출 규제 뒤 거래·값 ----------
def card_loan(name):
    ev = J("a2_a3")["loan_events"]
    keep = [("2017.8", "8·2", ev[0]), ("2018.9", "9·13", ev[1]), ("2019.12", "12·16", ev[2]),
            ("2021.7", "DSR 1단계", ev[4]), ("2022.1", "DSR 2단계", ev[5]), ("2025.6", "6·27", ev[6]), ("2025.10", "10·15", ev[7])]
    im, d = canvas("대출을 묶자 거래는 대개 줄었다, 값이 크게 내린 건 한 번",
                   "서울 아파트, 대출 규제 발표 앞 3개월과 뒤 3개월의 거래 · 발표 뒤 12개월 값")
    d.text((330, 150), "거래(월평균) 앞 3개월 → 뒤 3개월", font=F_M, fill=NAVY)
    d.text((900, 150), "발표 뒤 12개월 값(서울 매매지수)", font=F_M, fill=NAVY)
    cx1, cx2 = 560, 1080
    for cx in (cx1, cx2): d.line([cx, 190, cx, 190 + 7 * 62], fill=GRAY, width=2)
    for i, (ym, nm, e) in enumerate(keep):
        y = 195 + i * 62
        d.text((90, y + 10), ym, font=F_S, fill=GRAY); d.text((190, y + 6), nm, font=F_M, fill=INK)
        t = e["서울거래_신고기준_월평균"][2]
        L = abs(t) * 3.6
        col = BLUE if t < 0 else RED
        if t < 0: d.rectangle([cx1 - L, y + 8, cx1, y + 44], fill=col)
        else: d.rectangle([cx1, y + 8, cx1 + L, y + 44], fill=col)
        lab = fmt(t) + "%" + (" ※" if nm == "12·16" else "")
        d.text((cx1 + 10 if t < 0 else cx1 + L + 8, y + 10), lab, font=F_S, fill=col)
        p = e["서울지수_뒤12개월변동"]
        if p is None:
            d.text((cx2 + 12, y + 10), "아직(12개월 안 됨)", font=F_S, fill=GRAY)
        else:
            L2 = abs(p) * 14
            col2 = RED if p > 0 else BLUE
            if p < 0: d.rectangle([cx2 - L2, y + 8, cx2, y + 44], fill=col2)
            else: d.rectangle([cx2, y + 8, cx2 + L2, y + 44], fill=col2)
            d.text((cx2 + L2 + 8 if p > 0 else cx2 + 12, y + 10), fmt(p) + "%", font=F_M if nm in ("DSR 2단계", "6·27") else F_S, fill=col2)
    box(d, (90, 645, 1310, 725), SAND,
        "크게 내린 건 금리가 한꺼번에 뛰던 2022년 1월(-9.4%)뿐. 6·27 뒤엔 거래가 21% 줄었는데 값은 1년에 10.7% 더 올랐다", F_S, INK)
    foot(d, "한국부동산원 R-ONE 아파트 매매거래(신고 기준)·매매가격지수(월) 직접 계산 · ※12·16은 신고 시차로 늘어 보임(계약 기준 3개 구 -41.4%)")
    save(im, name)


# ---------- 카드 C: 같은 0.5%p ----------
def card_rate(name):
    eps = {e["episode"]: e for e in J("a2_a3")["rate_episodes"]}
    a, b, c = eps["2017.11~2018.11"], eps["2021.08~2023.01"], eps["2026.07~(진행)"]
    im, d = canvas("같은 0.5%p 인상, 2017년엔 서울 아파트가 14% 올랐다",
                   "한국은행 기준금리 인상기 세 번 — 오른 폭과 그 뒤 서울 아파트")
    cols = [(90, "2017.11~2018.11", "+0.50%p", "1.25 → 1.75%", "1년 뒤 서울 아파트", fmt(a["KB서울아파트_12개월"]) + "%", RED, "KB 시세 지수", MINT),
            (520, "2021.8~2023.1", "+3.00%p", "0.50 → 3.50%", "2년 뒤 서울 아파트", fmt(b["실거래서울_24개월"]) + "%", BLUE, "실거래가지수 · 거래 -58%", LIGHT),
            (950, "2026.7~ 지금", "+0.50%p", "2.50 → 3.00%", "주담대 금리(8월)", f"{c['주담대금리_최고']:.2f}%", AMBER, "2022.10 최고 4.82%", SAND)]
    for x, per, up, rng, lab, val, col, note, bg in cols:
        d.rounded_rectangle([x, 160, x + 380, 600], radius=22, fill=bg)
        ctext(d, x + 190, 185, per, F_M, GRAY)
        ctext(d, x + 190, 230, up, F_BIG, NAVY)
        ctext(d, x + 190, 305, "기준금리 " + rng, F_S, GRAY)
        d.line([x + 40, 360, x + 340, 360], fill=WHITE, width=3)
        ctext(d, x + 190, 385, lab, F_M, INK)
        ctext(d, x + 190, 430, val, F_BIG, col)
        ctext(d, x + 190, 520, note, F_S, GRAY)
    box(d, (90, 630, 1310, 710), SAND, "인상 폭은 2017년과 같다. 다만 대출 금리 수준은 이미 2022년 최고치 가까이 와 있다 — 그래서 「아직 모른다」", F_S, INK)
    foot(d, "한국은행 ECOS 기준금리·예금은행 주담대 금리(신규)·KB 주택매매가격지수·부동산원 아파트 실거래가지수, 한국부동산원 거래 직접 계산")
    save(im, name)


# ---------- 카드 D: 30대 이하 ----------
def card_young(name):
    ag = J("a2_a3")["buyer_age_2030"]
    yrs = [("2019", "서울|2019"), ("2020", "서울|2020"), ("2021", "서울|2021"), ("2022", "서울|2022"), ("2023", "서울|2023"),
           ("2024", "서울|2024"), ("2025", "서울|2025"), ("2026\n1~8월", "서울|2026_1-8")]
    im, d = canvas("서울 아파트를 산 사람 10명 중 4명은 30대 이하, 2021년보다 많다",
                   "서울 아파트 매매 중 산 사람이 30대 이하인 비율")
    x0, base, top = 130, 600, 200
    for i, (lab, k) in enumerate(yrs):
        v = ag[k]["share"]; x = x0 + i * 145
        h = (v - 20) / 30 * (base - top)
        col = RED if k in ("서울|2026_1-8",) else (AMBER if k == "서울|2021" else DIM)
        d.rectangle([x, base - h, x + 95, base], fill=col)
        ctext(d, x + 47, base - h - 42, f"{v:.1f}%", F_M if col != DIM else F_S, col if col != DIM else GRAY)
        for j, ln in enumerate(lab.split("\n")): ctext(d, x + 47, base + 12 + j * 26, ln, F_S, INK)
    d.line([110, base, 1310, base], fill=GRAY, width=2)
    d.text((1000, 175), "생애최초 LTV 70%는", font=F_S, fill=GRAY); d.text((1000, 200), "6·27 뒤에도 남아 있다", font=F_S, fill=GRAY)
    foot(d, "한국부동산원 R-ONE 매입자 연령대별 아파트 매매거래(동·호수) 직접 계산 · 30대 이하 = 20대 이하 + 30대 · 막대는 20%부터")
    save(im, name)


# ---------- 카드 E: 착공 반토막 → 30개월 ----------
def card_supply(name):
    s = J("a7_extra")
    im, d = canvas("땅을 덜 판 3년이 이제 입주로 온다",
                   "수도권 주택 착공, 한 해 평균 — 착공에서 입주까지는 약 30개월")
    a1 = J("a1_supply")
    # 숫자는 로직근거 1-3 표와 같은 값(KOSIS 직접 계산)
    v_old, v_new = 312275, 152239
    base, top = 520, 190
    for i, (lab, v, col) in enumerate([("2015~2021년\n한 해 평균", v_old, DIM), ("2023~2025년\n한 해 평균", v_new, BLUE)]):
        x = 150 + i * 230; h = v / v_old * (base - top)
        d.rectangle([x, base - h, x + 150, base], fill=col)
        ctext(d, x + 75, base - h - 44, f"{v/10000:.1f}만 호", F_M, INK if col == DIM else BLUE)
        for j, ln in enumerate(lab.split("\n")): ctext(d, x + 75, base + 12 + j * 26, ln, F_S, INK)
    ctext(d, 495, 200, "예전의", F_S, GRAY); ctext(d, 495, 226, f"{v_new / v_old * 100:.1f}%", F_BIG, BLUE)
    arrow(d, (640, 400), (900, 400), INK, 6)
    ctext(d, 770, 345, "약 30개월", F_L, INK)
    ctext(d, 770, 420, "착공 → 입주", F_S, GRAY)
    d.rounded_rectangle([930, 250, 1310, 560], radius=22, fill=LIGHT)
    ctext(d, 1120, 280, "그래서 입주는", F_M, NAVY)
    ctext(d, 1120, 330, "2026년 하반기 ~", F_L, INK)
    ctext(d, 1120, 375, "2028년 상반기", F_L, INK)
    ctext(d, 1120, 425, "적은 구간", F_L, BLUE)
    ctext(d, 1120, 490, "올해 1~8월 입주 전국 -27.2%", F_S, GRAY)
    box(d, (90, 620, 1310, 700), SAND, "「입주 체감은 2028년부터」는 착공 통계로 이미 정해진 숫자다 — 사장의 로직 중 가장 단단한 칸", F_S, INK)
    foot(d, "통계청 KOSIS 국토교통부 주택건설 착공·준공 실적(2011.1~2026.8) 직접 계산 · 30개월 = 착공·준공 증감이 가장 잘 맞는 시차(전국)")
    save(im, name)


# ---------- 카드 F: 1989 1기 신도시 ----------
def card_1989(name):
    kb = ecos_txt("ECOS_901Y062_KB매매_P63ACA.txt")
    ks = sorted(k for k in kb if "198601" <= k <= "200112")
    b0 = kb["198904"]
    im, d = canvas("1989년 신도시 발표, 입주 전 2년은 오르고 입주 뒤엔 내렸다",
                   "KB 서울 아파트 매매가격지수(1989년 4월 = 100)")
    gx0, gx1, gy0, gy1 = 130, 1300, 600, 190
    vmin, vmax = 50, 175
    def X(k): return gx0 + (ks.index(k)) / (len(ks) - 1) * (gx1 - gx0)
    def Y(v): return gy0 - (v - vmin) / (vmax - vmin) * (gy0 - gy1)
    for v in (80, 100, 120, 140):
        d.line([gx0, Y(v), gx1, Y(v)], fill=(230, 230, 225), width=1); d.text((gx0 - 50, Y(v) - 12), str(v), font=F_SM, fill=GRAY)
    pts = [(X(k), Y(kb[k] / b0 * 100)) for k in ks]
    d.line(pts, fill=NAVY, width=4)
    for yy in range(1986, 2002, 2): d.text((X(f"{yy}01") - 22, gy0 + 10), str(yy), font=F_SM, fill=GRAY)
    marks = [("198904", "신도시 발표", AMBER, -75), ("199104", "정점 " + fmt(pct(kb["198904"], kb["199104"])) + "%\n(발표 뒤 2년)", RED, -95),
             ("199109", "분당 첫 입주", GREEN, 70), ("199404", "정점 뒤 3년\n" + fmt(pct(kb["199104"], kb["199404"])) + "%", BLUE, 55),
             ("200108", "정점 회복\n(124개월 뒤)", GRAY, -110)]
    for k, lab, col, dy in marks:
        x, y = X(k), Y(kb[k] / b0 * 100)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=col)
        lines = lab.split("\n")
        for j, ln in enumerate(lines): ctext(d, x, y + dy + j * 28, ln, F_M if j == 0 else F_S, col)
    box(d, (90, 650, 1310, 715), SAND, "공급은 2년 넘게 걸려 왔고, 그 사이엔 올랐다. 다만 1991년 4월 회사채 금리는 18.8%였고, LTV 같은 대출 규제는 없었다", F_S, INK)
    foot(d, "한국은행 ECOS KB 주택매매가격지수(서울 아파트) 직접 계산 · 1기 신도시 발표 1989.4.27, 분당 첫 입주 1991.9")
    save(im, name)


# ---------- 카드 G: 보금자리 매매 vs 전세 ----------
def card_bogeum(name):
    kb = ecos_txt("ECOS_901Y062_KB매매_P63ACA.txt")
    js = {r["t"]: float(r["v"]) for r in json.load(open(os.path.join(RAW, "ecos_kb_jeonse_seoul_apt.json"), encoding="utf-8"))}
    ks = [k for k in sorted(kb) if "200809" <= k <= "201309"]
    im, d = canvas("반값 아파트를 기다린 5년, 매매는 9% 내리고 전세는 36% 올랐다",
                   "2008년 9월 보금자리주택 발표 = 100, KB 서울 아파트 매매·전세 지수")
    gx0, gx1, gy0, gy1 = 130, 1100, 600, 190
    vmin, vmax = 80, 145
    def X(i): return gx0 + i / (len(ks) - 1) * (gx1 - gx0)
    def Y(v): return gy0 - (v - vmin) / (vmax - vmin) * (gy0 - gy1)
    for v in (90, 100, 110, 120, 130, 140):
        d.line([gx0, Y(v), gx1, Y(v)], fill=(230, 230, 225), width=1); d.text((gx0 - 50, Y(v) - 12), str(v), font=F_SM, fill=GRAY)
    m = [(X(i), Y(kb[k] / kb["200809"] * 100)) for i, k in enumerate(ks)]
    j = [(X(i), Y(js[k] / js["200809"] * 100)) for i, k in enumerate(ks)]
    d.line(j, fill=GREEN, width=5); d.line(m, fill=NAVY, width=5)
    for i, k in enumerate(ks):
        if k.endswith("09"): d.text((X(i) - 30, gy0 + 10), k[:4] + ".9", font=F_SM, fill=GRAY)
    mv, jv = pct(kb["200809"], kb["201309"]), pct(js["200809"], js["201309"])
    d.text((1120, j[-1][1] - 20), "전세 " + fmt(jv) + "%", font=F_L, fill=GREEN)
    d.text((1120, m[-1][1] - 20), "매매 " + fmt(mv) + "%", font=F_L, fill=NAVY)
    box(d, (90, 650, 1310, 715), SAND, "집을 안 사고 기다린 동안의 집값(전세)은 올랐다. 기다림에도 비용이 있다", F_S, INK)
    foot(d, "한국은행 ECOS KB 주택매매·전세가격지수(서울 아파트) 직접 계산 · 보금자리주택 150만 호 발표 2008.9.19 · 같은 시기 금융위기 겹침")
    save(im, name)
    return mv, jv


# ---------- 카드 H: 점검표 ----------
def card_score(name):
    im, d = canvas("사장의 로직, 숫자로 대 보니", "2026년 10월 14일까지 공개된 공공 통계 기준 — 예측 아님")
    rows = [("공급은 늦게 온다", "착공 반토막 → 약 30개월 뒤 입주", "맞다", GREEN),
            ("대출로 경쟁적으로 산다", "서울 30대 이하 매수 42.8%", "숫자로 보인다", GREEN),
            ("대출을 묶으면 완만해진다", "6·27 뒤 거래 -21%, 값 +10.7%", "근거 아직 없음", AMBER),
            ("금리가 계속 오른다", "+0.5%p(2021년엔 +3.0%p)", "아직 약하다", AMBER),
            ("기다리면 손해 안 본다", "2021년엔 맞고 2023년엔 반대", "언제냐에 달렸다", AMBER),
            ("급락할 가능성이 좀 많다", "서울 87주 연속 상승", "지금 숫자로는 아니다", BLUE)]
    d.text((110, 150), "사장의 로직", font=F_M, fill=GRAY); d.text((560, 150), "숫자", font=F_M, fill=GRAY); d.text((1020, 150), "판정", font=F_M, fill=GRAY)
    for i, (a, b, c, col) in enumerate(rows):
        y = 195 + i * 82
        d.rounded_rectangle([90, y, 1310, y + 70], radius=14, fill=WHITE, outline=(225, 225, 220), width=2)
        d.text((110, y + 18), a, font=F_M, fill=INK)
        d.text((560, y + 21), b, font=F_S, fill=INK)
        w = d.textlength(c, font=F_M) + 40
        d.rounded_rectangle([1010, y + 12, 1010 + w, y + 58], radius=23, fill=col)
        d.text((1030, y + 19), c, font=F_M, fill=WHITE)
    foot(d, "출처: 국토교통부(KOSIS)·한국부동산원 R-ONE·한국은행 ECOS·국토교통부 실거래, 이 글의 앞 그림들과 같은 숫자")
    save(im, name)


# ---------- 기존 그림: 출처 줄만 바꿔 복사 ----------
REUSE = {
    "01_two_dates.png": "출처: 9.30 기자간담회 보도(5개 매체 일치), 10.12 국회 국토교통위 국정감사 중계(자막·음성 대조). 인물은 실루엣",
    "03_logic_pillars.png": "출처: 10.12 국토교통위 국정감사 중계(자막·음성 대조), 9.30 기자간담회 보도",
    "05_supply_parcel.png": "출처: 국토교통부 주택통계(2026년 1~8월 누계, 전년 같은 기간 대비)",
    "R2_supply_path.png": "출처: 주택금융연구원 보고서(2023)·KB 전세지수(2003~2005). 모식도",
    "R3_first_home_loan.png": "출처: 6·27 가계부채 관리방안(주택구입 주담대 최대 6억, 생애최초 LTV 70%). 소득 기준(DSR) 등은 뺀 단순 계산",
    "07_rate_jump.png": "출처: 한국은행 기준금리(ECOS). 가로는 시간 비례",
    "09_two_big_drops.png": "출처: KB 전국 아파트 매매가격지수(한국은행 ECOS) 고점→저점 직접 계산",
    "14_same_numbers.png": "출처: 국정감사 답변 「2028년도부터 공급이 되고」, 공급 반론 해설들의 공통 시점. 모식도, 전망 아님",
    "15_my_calendar.png": "2028년: 국정감사 답변·정부 주택공급 전망. 투자 권유 아님 — 판단은 각자의 상황에 따라",
}


def reuse(src, dst, line):
    im = Image.open(os.path.join(ROOT, "img", src)).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 56, W, H], fill=BG)
    foot(d, line)
    im.save(os.path.join(HERE, dst)); print("reused", src, "->", dst)


if __name__ == "__main__":
    ORDER = [("01_two_dates.png", None), ("03_logic_pillars.png", None), ("05_supply_parcel.png", None), (None, card_supply),
             ("R2_supply_path.png", None), ("R3_first_home_loan.png", None), (None, card_young), (None, card_loan),
             ("07_rate_jump.png", None), (None, card_rate), ("09_two_big_drops.png", None), (None, card_wait),
             (None, card_1989), (None, card_bogeum), (None, card_score), ("14_same_numbers.png", None), ("15_my_calendar.png", None)]
    for i, (src, fn) in enumerate(ORDER, start=2):   # 1번은 AI 썸네일
        name = f"261015_{i}.png"
        if src: reuse(src, name, REUSE[src])
        else: fn(name)
