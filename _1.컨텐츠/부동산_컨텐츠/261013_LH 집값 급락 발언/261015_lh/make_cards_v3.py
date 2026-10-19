# -*- coding: utf-8 -*-
"""v3(10/15 거시 비교 반영) — 「지금의 경제 판」 카드·「국면별 판」 카드 추가, 2017 비교 카드 문구 보강.
숫자: LH집값_거시비교_2026-10-15.md(base data\\로직근거\\v3_macro\\out\\v3_table.json·v3_extra.json)에서 옮긴 값.
카드에 옮긴 숫자는 아래 상수에 두고, 문서 1절 표의 값과 같은지 make 때 눈으로 다시 대조한다(문서 행 번호 주석)."""
import os
import make_cards as M
import make_cards_v2 as V2
from make_cards import (canvas, box, foot, ctext, F_S, F_SM, F_M, F_L, F_BIG,
                        INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, NAVY, DIM, fmt, save, reuse, REUSE)


# ---------- 지금의 경제 판: 호황 쪽 vs 긴축 쪽 ----------
def card_now_mix(name):
    im, d = canvas("지금 한국 경제는 두 쪽으로 갈라져 있다",
                   "2026년 최신 값 — 한쪽은 호황, 한쪽은 긴축")
    left = [("수출(9월, 통관)", "1,209억 달러", "1년 전보다 +83.5% · 월 기준 사상 최대"),
            ("성장률(2분기)", "3.7%", "1년 전 같은 분기 대비"),
            ("원/달러", "1,527 → 1,359원", "6월 → 9월, 원화가 강해지는 중")]
    right = [("두바이유", "62.7 → 126.7달러", "1월 → 3월(2월 말 중동 전쟁), 9월 111.8"),
             ("금리", "한국 +0.50%p · 미국 +0.25%p", "두 나라가 같이 올리는 중"),
             ("실질임금(2분기)", "-0.8%", "4~7월 넉 달 연속 감소 · 이자비용 +12.1%")]
    for x0, title, bg, col, rows in [(90, "호황 쪽", MINT, GREEN, left), (720, "긴축 쪽", PINK, RED, right)]:
        d.rounded_rectangle([x0, 150, x0 + 590, 600], radius=22, fill=bg)
        ctext(d, x0 + 295, 168, title, F_L, col)
        for i, (h, big, sub) in enumerate(rows):
            y = 225 + i * 125
            d.text((x0 + 30, y), h, font=F_M, fill=GRAY)
            d.text((x0 + 30, y + 34), big, font=F_L, fill=INK)
            d.text((x0 + 30, y + 76), sub, font=F_S, fill=GRAY)
    box(d, (90, 625, 1310, 705), SAND,
        "과거 국면은 수출·원화·금리가 한 방향이었다. 지금은 갈라져 있어 과거 결과를 그대로 대기 어렵다", F_S, INK)
    foot(d, "산업통상부 수출입동향(2026.9) · 한국은행 ECOS(성장률·환율·유가·금리) · 고용노동부 · 국가데이터처 가계동향")
    save(im, name)


# ---------- 국면별 경제 판 한 줄 ----------
def card_phases(name):
    im, d = canvas("그때와 지금, 경제 판이 이만큼 달랐다",
                   "집값이 움직인 과거 네 국면 — 그때 바깥 사정과 지금과 가장 다른 점")
    rows = [("1989~93", "1기 신도시", "경제가 해마다 8% 컸고\n가계 실질소득도 해마다 8.3% 늘던 때", "소득 증가: 그때 연 8.3%\n지금 2025년 1.9%, 실질임금 감소"),
            ("2008~13", "보금자리", "금융위기로 2009년 수출 -15.9%\n금리는 5.25% → 2.00%로 인하", "수출·금리 방향이 정반대\n지금 수출 사상 최대, 금리 인상"),
            ("2017~18", "0.5%p 인상", "반도체 호황, 물가 1%대\n2018년 입주 61.4만 호(최대)", "입주: 2025년 30.0만 호(최소)\n물가 2.9%, 두바이유 111.8달러"),
            ("2021~23", "금리 급등", "한국 +3.00%p, 미국 +5.25%p\n원화 1,427원까지 약세", "금리 충격 폭과 원화 방향\n지금 미국 +0.25%p, 원화 강세")]
    d.text((110, 150), "국면", font=F_M, fill=GRAY); d.text((390, 150), "그때 바깥 사정", font=F_M, fill=GRAY); d.text((860, 150), "지금과 가장 다른 점", font=F_M, fill=GRAY)
    for i, (yr, nm, then, diff) in enumerate(rows):
        y = 190 + i * 118
        d.rounded_rectangle([90, y, 1310, y + 104], radius=14, fill=WHITE, outline=(225, 225, 220), width=2)
        d.text((110, y + 20), yr, font=F_L, fill=NAVY); d.text((110, y + 60), nm, font=F_S, fill=GRAY)
        for j, ln in enumerate(then.split("\n")): d.text((390, y + 22 + j * 32), ln, font=F_S, fill=INK)
        for j, ln in enumerate(diff.split("\n")): d.text((860, y + 22 + j * 32), ln, font=F_S, fill=RED if j == 0 else INK)
    box(d, (90, 670, 1310, 720), SAND, "넷 중 지금과 조건이 다 맞는 국면은 없다 — 그래서 과거 결과는 「참고」이지 「예고」가 아니다", F_S, INK)
    foot(d, "한국은행 ECOS(국민계정·국제수지·물가·금리·환율) · KOSIS 국토부 준공 · 고용노동부 · 1인당 실질 가계소득은 국민계정으로 직접 계산")
    save(im, name)


# ---------- 2017 비교 카드 — 그때 물가·입주 붙이기 ----------
def card_rate(name):
    eps = {e["episode"]: e for e in M.J("a2_a3")["rate_episodes"]}
    a, b, c = eps["2017.11~2018.11"], eps["2021.08~2023.01"], eps["2026.07~(진행)"]
    im, d = canvas("같은 0.5%p 인상, 2017년엔 서울 아파트가 14% 올랐다",
                   "다만 그때는 물가 1%대·새 아파트 입주가 가장 많던 때 — 판이 다르다")
    cols = [(90, "2017.11~2018.11", "+0.50%p", "물가 1%대 · 입주 최대", "1년 뒤 서울 아파트", fmt(a["KB서울아파트_12개월"]) + "%", RED, "KB 시세 지수", MINT),
            (520, "2021.8~2023.1", "+3.00%p", "미국 +5.25%p · 원화 약세", "2년 뒤 서울 아파트", fmt(b["실거래서울_24개월"]) + "%", BLUE, "실거래가지수 · 거래 -58%", LIGHT),
            (950, "2026.7~ 지금", "+0.50%p", "물가 2.9% · 입주 최소", "주담대 금리(8월)", f"{c['주담대금리_최고']:.2f}%", AMBER, "물가 빼면 +1.6%(2022.10은 -0.8%)", SAND)]
    for x, per, up, ctx, lab, val, col, note, bg in cols:
        d.rounded_rectangle([x, 160, x + 380, 600], radius=22, fill=bg)
        ctext(d, x + 190, 185, per, F_M, GRAY)
        ctext(d, x + 190, 230, up, F_BIG, NAVY)
        ctext(d, x + 190, 305, ctx, F_S, GRAY)
        d.line([x + 40, 360, x + 340, 360], fill=WHITE, width=3)
        ctext(d, x + 190, 385, lab, F_M, INK)
        ctext(d, x + 190, 430, val, F_BIG, col)
        ctext(d, x + 190, 520, note, F_S, GRAY)
    box(d, (90, 630, 1310, 710), SAND, "인상 폭은 2017년과 같지만, 물가·입주·금리 부담은 그때와 다르다 — 그래서 이 칸은 「아직 모른다」", F_S, INK)
    foot(d, "한국은행 ECOS 금리·물가·KB 지수·실거래가지수 · KOSIS 준공 · 실질 금리 = 주담대 금리 - 물가(직접 계산)")
    save(im, name)


if __name__ == "__main__":
    ORDER = [("01_two_dates.png", None), ("03_logic_pillars.png", None), ("05_supply_parcel.png", None), (None, M.card_supply),
             ("R2_supply_path.png", None), ("R3_first_home_loan.png", None), (None, V2.card_firsthome), (None, V2.card_loan),
             ("07_rate_jump.png", None), (None, card_rate), ("09_two_big_drops.png", None), (None, V2.card_wait),
             (None, V2.card_ahead), (None, card_now_mix), (None, card_phases), (None, V2.card_1989), (None, M.card_bogeum),
             (None, V2.card_score), ("14_same_numbers.png", None), ("15_my_calendar.png", None)]
    for f in os.listdir(M.HERE):
        if f.startswith("261015_") and f.endswith(".png") and f != "261015_1.png": os.remove(os.path.join(M.HERE, f))
    for i, (src, fn) in enumerate(ORDER, start=2):
        n = f"261015_{i}.png"
        if src: reuse(src, n, REUSE[src])
        else: fn(n)
