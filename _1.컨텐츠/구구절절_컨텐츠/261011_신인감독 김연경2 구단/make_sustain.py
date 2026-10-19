# -*- coding: utf-8 -*-
"""결론부 2장: D13 운영비÷순이익 비율, D14 지속가능성 점검표 다섯 칸. 숫자는 구단_공부노트 §1-10."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
OUT = os.path.join(HERE, "img")
F_SM = font(18); F_M = font(24, True); F_MID = font(34, True)
DIM = (205, 205, 200); NAVY = (40, 60, 110); ORANGE = (235, 120, 40)
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)

# ---------- D13 비율 ----------
im, d = canvas("구단 비용 ÷ 모기업 순이익 — 기존 구단은 2% 아래, 페퍼 8.6%", "2025 당기순이익 기준(페퍼는 창단 해 2021). 비용은 여자부 운영비 70억으로 통일한 계산값")
rows = [("IBK기업은행(2025)", 0.3, "0.3%", GREEN), ("키움증권 네이밍(2025)", 0.9, "0.9%", GREEN), ("현대건설(2025)", 1.3, "1.3%", GREEN),
        ("흥국생명(2025)", 2.1, "2.1%", GREEN), ("SOOP(2025)", 7.1, "7.1%", AMBER), ("페퍼저축은행(2021 창단 해)", 8.6, "8.6%", AMBER),
        ("페퍼저축은행(2023~25)", 0, "순손실 3년 · 비율 없음", RED)]
x0, wmax, y = 470, 600, 165
for lab, v, val, col in rows:
    d.rounded_rectangle([x0, y, x0 + wmax, y + 34], radius=8, fill=LIGHT)
    if v: d.rounded_rectangle([x0, y, x0 + wmax * v / 10, y + 34], radius=8, fill=col)
    d.text((x0 - 12 - d.textlength(lab, font=F_S), y + 5), lab, font=F_S, fill=INK)
    d.text((x0 + wmax * v / 10 + 12, y + 3), val, font=F_M, fill=col)
    y += 52
d.line([x0 + wmax * 0.5, 160, x0 + wmax * 0.5, 530], fill=DIM, width=2); ctext(d, x0 + wmax * 0.5, 535, "5%", F_SM, GRAY)
box(d, (90, 575, 1310, 690), SAND, "페퍼는 창단 해 8.6%였고 2년 뒤 적자로 돌아섰다. SOOP의 7.1%는 그 창단 시점과 비슷한 숫자다 —\n다른 점은 2년 연속 흑자(2024 1,024억 → 2025 984억), 광고 매출 +61%, 노출을 스스로 만드는 중계 플랫폼이라는 것.", F_S, INK)
foot(d, "근거: 딜사이트(페퍼 2021), 뉴스스페이스(2023~25), 쿠키뉴스 2026.2.12(SOOP), 새턴경제(흥국·현대건설), 헤럴드경제 2026.2.3(키움). 계산값")
save(im, "D13_profit_ratio.png")

# ---------- D14 점검표 ----------
im, d = canvas("할 일 하나 — 2화에 「기업」 이름이 나오면 이 다섯 칸을 채운다", "페퍼(2021 창단 때)·SOOP(2026)·키움(야구)을 같은 칸에 넣어 본 것. 평가가 아니라 자리 확인")
cols = [("① 비율", "70억 ÷ 순이익"), ("② 흐름", "3년 연속 흑자?"), ("③ 주인", "누가 결정하나"), ("④ 계약", "몇 년인가"), ("⑤ 업종", "홍보 셈법이 서나")]
rowsT = [("페퍼 2021", ["8.6%", "흑자 2년째\n(2년 뒤 적자)", "2대 주주\n사모펀드", "모기업 직영\n(기한 없음)", "B2C 금융\n(저축은행)"], [AMBER, AMBER, RED, GRAY, GREEN]),
         ("SOOP 2026", ["7.1%", "흑자 2년 연속", "상장사\n창업자 경영", "모기업 직영\n(기한 없음)", "플랫폼\n자체 중계"], [AMBER, GREEN, GREEN, GRAY, GREEN]),
         ("키움 (야구)", ["0.9%", "흑자", "구단 법인 별도\n스폰서는 이름만", "5년 + 5년", "B2C 금융\n(증권)"], [GREEN, GREEN, GREEN, GREEN, GREEN]),
         ("캐롯·데이원 (농구)", ["—", "모기업\n회생절차", "회생 중\n모기업", "한 시즌\n못 채움", "B2C 보험"], [GRAY, RED, RED, RED, GREEN])]
LX, TOPY, CW, RH = 70, 165, 215, 88
d.rounded_rectangle([LX, TOPY, LX + 180, TOPY + 60], radius=10, fill=NAVY); ctext(d, LX + 90, TOPY + 18, "2화에 나올 이름", F_S, WHITE)
for i, (t, s) in enumerate(cols):
    x = LX + 190 + i * CW
    d.rounded_rectangle([x, TOPY, x + CW - 8, TOPY + 60], radius=10, fill=NAVY)
    ctext(d, x + (CW - 8) / 2, TOPY + 8, t, F_M, WHITE); ctext(d, x + (CW - 8) / 2, TOPY + 36, s, F_SM, WHITE)
for r, (name, cells, colors) in enumerate(rowsT):
    y = TOPY + 70 + r * RH
    d.rounded_rectangle([LX, y, LX + 180, y + RH - 8], radius=10, fill=WHITE, outline=DIM, width=2); ctext(d, LX + 90, y + 28, name, F_S, INK)
    for i, (c, col) in enumerate(zip(cells, colors)):
        x = LX + 190 + i * CW
        d.rounded_rectangle([x, y, x + CW - 8, y + RH - 8], radius=10, fill=WHITE, outline=col, width=3)
        lines = c.split("\n")
        for k, ln in enumerate(lines): ctext(d, x + (CW - 8) / 2, y + (28 if len(lines) == 1 else 15) + k * 24, ln, F_S, col if col != GRAY else INK)
y = TOPY + 70 + 4 * RH + 6
d.text((LX, y), "초록=기존 구단 범위 · 주황=페퍼 창단 때와 같은 자리 · 빨강=페퍼·데이원이 무너진 칸 · 회색=해당 없음", font=F_SM, fill=GRAY)
box(d, (90, 625, 1310, 700), SAND, "빨간 칸이 하나라도 있으면 「5년 뒤」를 묻는다. 페퍼는 ③이 빨강이었고 2년 만에 ②도 빨강이 됐다.\n선수단이 또 상처 입지 않으려면(김연경, 1화 10분쯤) 구단주 발표 날 이 표부터.", F_S, INK)
foot(d, "근거: §1-10 표, 데일리안 2023.3.21(캐롯 종료), 오마이스타 2023(키움 5년), 머니투데이 2026.4.30(페퍼 2대 주주). 70억은 통일 가정")
save(im, "D14_checklist.png")
print("done_sustain")
