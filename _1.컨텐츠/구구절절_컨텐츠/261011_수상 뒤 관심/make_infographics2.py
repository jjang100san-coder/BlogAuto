# -*- coding: utf-8 -*-
"""글자형 도해 7장을 인포그래픽으로 교체(R1~R4, C1, C4, C5 → *_v2). 숫자는 공부노트 확인분만."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_X, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
from PIL import ImageDraw
OUT = os.path.join(HERE, "img")
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)
F_M = font(24, True); F_BIG = font(64, True); F_MID = font(34, True)
MAN = (41, 98, 255); WOMAN = (225, 80, 120); DIM = (205, 205, 200)

def person(d, cx, top, h, col):
    r = h * 0.17
    d.ellipse([cx - r, top, cx + r, top + 2 * r], fill=col)
    bw = h * 0.42
    d.rounded_rectangle([cx - bw / 2, top + 2 * r + h * 0.05, cx + bw / 2, top + h], radius=int(bw / 2), fill=col)

def star(d, cx, cy, r, col, frac=1.0):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=DIM)
    if frac >= 1: d.polygon(pts, fill=col); return
    if frac > 0:
        # 부분 채움: 왼쪽 frac 만큼만 별색
        mask_x = cx - r + 2 * r * frac
        clipped = [(min(x, mask_x), y) for x, y in pts]
        d.polygon(clipped, fill=col)

def vbar(d, x, base, w, hgt, col, label=None, value=None, f=F_S):
    d.rounded_rectangle([x, base - hgt, x + w, base], radius=8, fill=col)
    if value: ctext(d, x + w / 2, base - hgt - 30, value, F_M, col)
    if label: ctext(d, x + w / 2, base + 8, label, f, GRAY)

# ---------- R1 정보 폭포 ----------
im, d = canvas("연구 ① 정보 폭포 — 앞사람 둘이 같으면 내 느낌은 버려진다", "Bikhchandani·Hirshleifer·Welch 1992, Journal of Political Economy 100(5). 줄서기 모식도")
names = ["A", "B", "C", "D", "E"]; sig = [GREEN, RED, RED, RED, RED]
sig_t = ["좋다", "별로", "별로", "별로", "별로"]
reason = ["내 느낌대로", "A가 샀다 vs 내 느낌\n→ 동전 던지기", "둘이 샀다\n→ 내 느낌 버림", "따라 산다", "따라 산다"]
d.rounded_rectangle([560, 150, 1330, 600], radius=20, fill=PINK)
d.text((585, 160), "폭포 구간 — 아무도 자기 느낌을 안 본다", font=F_M, fill=RED)
for i, n in enumerate(names):
    cx = 180 + i * 240
    # 속마음(개인 신호)
    d.ellipse([cx - 34, 215, cx + 34, 283], fill=WHITE, outline=sig[i], width=4)
    ctext(d, cx, 234, sig_t[i], F_M, sig[i])
    d.text((cx - 45, 190), "내 느낌", font=F_S, fill=GRAY)
    person(d, cx, 300, 150, INK)
    ctext(d, cx, 360, n, F_H, WHITE)
    box(d, (cx - 80, 470, cx + 80, 520), MAN, "산다", F_M, WHITE)
    ctext(d, cx, 532, reason[i].split("\n")[0], F_S, INK)
    if "\n" in reason[i]: ctext(d, cx, 556, reason[i].split("\n")[1], F_S, INK)
    if i < 4: arrow(d, (cx + 95, 495), (cx + 145, 495), GRAY, 4)
# 상 = 수천 명
for k in range(12):
    person(d, 110 + k * 26, 640, 46, DIM if k < 11 else INK)
d.text((440, 640), "「상」은 앞사람 수천 명이 한꺼번에 '샀다'고 보여주는 신호 — 폭포가 바로 시작된다", font=F_M, fill=INK)
d.text((440, 674), "우연한 두세 명으로 시작되고, 정보가 모이지 않아 쉽게 뒤집힌다(취약)", font=F_S, fill=GRAY)
foot(d, "원문 요지: 남의 선택을 본 뒤 자기 신호와 무관하게 같은 행동 = 정보 폭포. 소수의 초기 선택으로 시작, 정보가 안 모여 취약. 신호는 설명용.")
save(im, "R1_cascade_v2.png")

# ---------- R2 사회적 증거 ----------
im, d = canvas("연구 ② 사회적 증거 — 모를 때는 남들이 고른 것이 정답이 된다", "Cialdini 『Influence』 social proof · 보조: Lagiosa·Méon 2021 공쿠르상 회귀불연속")
# 왼쪽: 확신 있을 때
box(d, (80, 160, 620, 210), LIGHT, "확신이 있을 때 — 내 취향을 본다", F_M, INK)
person(d, 200, 240, 170, INK)
d.ellipse([300, 255, 420, 375], fill=WHITE, outline=INK, width=4); ctext(d, 360, 296, "내 취향", F_M, INK)
arrow(d, (250, 315), (296, 315), INK, 5)
for k in range(5): person(d, 480 + k * 30, 300, 60, DIM)
d.text((470, 375), "남이 뭘 읽든 무관", font=F_S, fill=GRAY)
# 오른쪽: 확신 없을 때
box(d, (700, 160, 1320, 210), PINK, "확신이 없을 때 — 남들이 고른 것을 본다", F_M, RED)
person(d, 790, 240, 170, INK)
arrow(d, (840, 315), (890, 315), RED, 5)
for r in range(2):
    for k in range(6):
        person(d, 925 + k * 42 + r * 10, 240 + r * 80, 70, RED)
d.rounded_rectangle([1190, 250, 1300, 390], radius=8, fill=WHITE, outline=RED, width=4)
d.rounded_rectangle([1190, 250, 1300, 290], radius=8, fill=RED); ctext(d, 1245, 258, "1위", F_M, WHITE)
ctext(d, 1245, 320, "시집", F_B, INK); ctext(d, 1245, 350, "낯선 작가", F_S, GRAY)
d.text((900, 420), "「비슷한 남들」이 많이 고를수록 더 옳아 보인다", font=F_S, fill=RED)
# 아래: 공쿠르 효과 막대
d.text((80, 450), "공쿠르상 수상 직후 판매", font=F_M, fill=INK)
vbar(d, 120, 690, 90, 35, DIM, "수상 전", "1배")
vbar(d, 250, 690, 90, 155, AMBER, "수상 후", "4.5배")
d.text((370, 540), "+350%", font=F_BIG, fill=AMBER)
d.text((370, 620), "원래 덜 팔리던 책일수록 효과가 컸다", font=F_S, fill=GRAY)
box(d, (720, 480, 1320, 690), SAND, "시집·낯선 작가·안 들어본 아이돌\n= 확신이 없는 영역\n\n그래서 이 영역에서\n수상·역주행 효과가 가장 크다", F_B, INK)
foot(d, "근거: Cialdini(불확실할 때 비슷한 타인을 보고 올바른 행동을 찾는다). Lagiosa·Méon 2021(ULB 워킹페이퍼, 게재 여부 미확인) 판매 +350%.")
save(im, "R2_social_proof_v2.png")

# ---------- R3 MusicLab ----------
im, d = canvas("연구 ③ 누적 이익 — 같은 48곡, 8개 세계, 1등이 다 달랐다", "Salganik·Dodds·Watts 2006, Science 311 — 참가자 14,341명, 무명 밴드 48곡. 막대는 모식도")
# 독립 세계
d.rounded_rectangle([80, 160, 400, 470], radius=16, fill=WHITE, outline=GRAY, width=3)
d.text((100, 170), "독립 세계", font=F_M, fill=INK); d.text((100, 200), "남의 다운로드 수 안 보임", font=F_S, fill=GRAY)
for i, b in enumerate([60, 54, 50, 46, 43, 40, 37, 34]):
    d.rounded_rectangle([105 + i * 35, 450 - b * 3, 130 + i * 35, 450], radius=4, fill=GRAY)
d.text((250, 170), "→ 순위 완만", font=F_S, fill=GRAY)
# 8 사회 세계
wins = [0, 1, 2, 3, 4, 5, 6, 7]; cols = [AMBER, GREEN, BLUE, RED, (150, 80, 200), (20, 160, 170), (230, 110, 40), (120, 120, 120)]
for w in range(8):
    x0 = 440 + (w % 4) * 220; y0 = 160 + (w // 4) * 160
    d.rounded_rectangle([x0, y0, x0 + 200, y0 + 140], radius=12, fill=WHITE, outline=GRAY, width=2)
    d.text((x0 + 10, y0 + 6), f"세계 {w + 1}", font=F_S, fill=GRAY)
    heights = [18] * 8; heights[wins[w]] = 95
    for i, hgt in enumerate(heights):
        c = cols[i] if i == wins[w] else DIM
        d.rounded_rectangle([x0 + 14 + i * 23, y0 + 130 - hgt, x0 + 30 + i * 23, y0 + 130], radius=3, fill=c)
    d.text((x0 + 118, y0 + 6), f"1등: {wins[w] + 1}번", font=F_S, fill=cols[w])
d.text((440, 490), "남의 다운로드 수가 보이는 8개 세계 — 먼저 받은 곡이 더 받는다. 1등은 세계마다 다르다.", font=F_S, fill=INK)
box(d, (90, 540, 1310, 690), SAND, "가장 좋은 곡은 꼴찌를 안 하고, 가장 나쁜 곡은 1등을 못 한다.\n그 사이는 뭐든 가능하다 — 이것이 역주행의 수학이다.", F_B, INK)
foot(d, "원문: 사회적 영향이 강할수록 불평등(지니계수)과 예측불가능성이 함께 커졌다. 8개 세계의 1등 곡 번호는 설명용 배치.")
save(im, "R3_musiclab_v2.png")

# ---------- R4 상의 역설 ----------
im, d = canvas("연구 ④ 상의 역설 — 수상작은 더 팔리고, 평점은 더 떨어진다", "Kovács·Sharkey 2014, ASQ 59(1) — 2007~11 수상작·최종후보 64권(32쌍), Goodreads 리뷰 38,817개")
# 좌: 독자 수
box(d, (80, 160, 640, 210), LIGHT, "독자 수", F_M, INK)
vbar(d, 150, 520, 150, 90, DIM, "최종후보(낙선)", "그대로")
vbar(d, 380, 520, 150, 250, MAN, "수상작", "급증")
d.text((560, 230), "↑", font=F_BIG, fill=MAN)
# 우: 평점
box(d, (720, 160, 1320, 210), PINK, "평점 (5점 만점)", F_M, RED)
d.text((740, 235), "최종후보", font=F_S, fill=GRAY)
for k in range(5): star(d, 790 + k * 60, 290, 26, GREEN)
d.text((1110, 272), "거의 그대로", font=F_M, fill=GREEN)
d.text((740, 345), "수상작", font=F_S, fill=GRAY)
for k in range(5): star(d, 790 + k * 60, 400, 26, RED, 1.0 if k < 4 else 0.75)
d.text((1110, 382), "약 -0.25점", font=F_M, fill=RED)
d.text((740, 450), "수상 발표 뒤 2년 동안 수상작만 가파르게 내려갔다", font=F_S, fill=INK)
# 책 쌍 픽토그램
for k in range(8):
    x = 740 + k * 70
    d.rounded_rectangle([x, 500, x + 24, 540], radius=4, fill=RED); d.rounded_rectangle([x + 30, 500, x + 54, 540], radius=4, fill=DIM)
d.text((740, 548), "32쌍 = 같은 해 같은 상의 수상작 vs 최종후보", font=F_S, fill=GRAY)
box(d, (90, 590, 1310, 700), SAND, "이유 둘 — ① 취향이 제각각인 독자가 한꺼번에 몰린다  ② 인기 자체가 반감을 부른다\n예: 『예감은 틀리지 않는다』(2011 부커) — 판매 급증과 동시에 평점 장기 하락", F_S, INK)
foot(d, "막대·별은 모식도. 「0.25점」은 2차 요약(Goodreads 블로그) 수치라 원문 표 재확인 필요. 원문: 수상작 평점이 최종후보작보다 가파르게 하락.")
save(im, "R4_paradox_v2.png")

# ---------- C1 사례의 그 뒤 — 작은 그래프 넷 ----------
im, d = canvas("사례의 그 뒤 — 폭발 다음 해에 어디에 있었나", "확인된 숫자만. 순위는 낮을수록 위, 부수는 높을수록 위")
def panel(x0, y0, title, col):
    d.rounded_rectangle([x0, y0, x0 + 590, y0 + 240], radius=16, fill=WHITE, outline=col, width=3)
    d.text((x0 + 16, y0 + 10), title, font=F_M, fill=col)
# 윤하 순위
panel(80, 160, "윤하 「사건의 지평선」 멜론 연간 순위", GREEN)
pts = [(2022, 49), (2023, 5), (2024, 44)]
def rk(y): return 232 + (y - 1) * 1.85   # 1위=232, 72위≈363
xs = [200, 370, 520]
d.line([(x, rk(v)) for x, (_, v) in zip(xs, pts)], fill=GREEN, width=6)
for x, (yr, v) in zip(xs, pts):
    d.ellipse([x - 9, rk(v) - 9, x + 9, rk(v) + 9], fill=GREEN)
    ctext(d, x, rk(v) - 36, f"{v}위", F_M, GREEN); ctext(d, x, 374, str(yr), F_S, GRAY)
d.text((575, 200), "827일\n연속\n차트인", font=F_S, fill=GRAY)
# 롤린 순위
panel(730, 160, "브레이브걸스 「롤린」 멜론 연간 순위", AMBER)
pts = [(2021, 2), (2022, 72)]; xs = [880, 1100]
d.line([(x, rk(v)) for x, (_, v) in zip(xs, pts)], fill=AMBER, width=6)
for x, (yr, v) in zip(xs, pts):
    d.ellipse([x - 9, rk(v) - 9, x + 9, rk(v) + 9], fill=AMBER)
    if v < 60: ctext(d, x, rk(v) - 36, f"{v}위", F_M, AMBER)
    else: d.text((x + 20, rk(v) - 16), f"{v}위", font=F_M, fill=AMBER)
    ctext(d, x, 374, str(yr), F_S, GRAY)
d.text((1180, 200), "일간 547일\n연속 진입\n(2022.8)", font=F_S, fill=GRAY)
# 한강 해외
panel(80, 430, "한강 해외 번역서 판매(번역원 집계, 만 부)", BLUE)
for i, (yr, v) in enumerate([(2023, 52), (2024, 120), (2025, 119.8)]):
    vbar(d, 150 + i * 150, 628, 90, v * 1.0, BLUE if i else DIM, str(yr), f"{v:g}")
d.text((560, 560), "노벨 뒤\n유지(정체)", font=F_S, fill=GRAY)
# 채식주의자
panel(730, 430, "『채식주의자』 국내 누적(만 부)", RED)
for i, (lab, v) in enumerate([("부커 전", 6), ("직후 주문", 25), ("2016 말", 60), ("노벨 전", 110)]):
    vbar(d, 790 + i * 125, 628, 80, v * 1.1, RED if i == 3 else (240, 150, 150), lab, str(v))
foot(d, "근거: 스포츠경향 2025.1.10, 와우TV 2022.1.26, 한경 2022.8.30, 멜론 2022 연간 차트, 번역원 2026.7, 한국일보 2016.5, 매일신문 2024.10.16.")
save(im, "C1_afterwards_v2.png")

# ---------- C4 조건 넷 — 아이콘 카드 ----------
im, d = canvas("관심이 남는 조건 넷 — 열 사례에서 거꾸로 뽑은 것", "하나라도 비면 2년 안에 꺼졌다. 학술 모델이 아니라 이 글의 가설")
def icon_stage(cx, cy):
    d.rectangle([cx - 60, cy + 10, cx + 60, cy + 40], fill=INK)
    d.polygon([(cx, cy - 60), (cx - 55, cy + 10), (cx + 55, cy + 10)], fill=(255, 215, 90))
    person(d, cx, cy - 40, 55, INK)
def icon_fans(cx, cy):
    for k in range(3): person(d, cx - 40 + k * 40, cy - 30, 60, WOMAN)
    d.polygon([(cx, cy + 60), (cx - 30, cy + 30), (cx - 15, cy + 12), (cx, cy + 25), (cx + 15, cy + 12), (cx + 30, cy + 30)], fill=RED)
def icon_signal(cx, cy):
    star(d, cx, cy, 55, AMBER)
    ctext(d, cx - 7, cy - 16, "!", F_H, WHITE)
def icon_clock(cx, cy):
    d.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=WHITE, outline=RED, width=6)
    d.line([cx, cy, cx, cy - 38], fill=RED, width=6); d.line([cx, cy, cx + 26, cy + 14], fill=RED, width=6)
cards = [("① 무대", "사람이 계속 모일 자리", "윤하 투어 20회 vs 브걸 콘서트 0회", GREEN, icon_stage),
         ("② 팬덤 전환", "밈이 「다시 사는 사람」으로", "리센느 초동 3.6만 → 10.7만", WOMAN, icon_fans),
         ("③ 다음 신호", "첫 신호를 갱신하는 후속", "한강 NBCC상 → 하루 만에 5배", AMBER, icon_signal),
         ("④ 시계", "계약·건강·자본이 늦게 와야", "여자친구·EXID·모모랜드·브걸 = 7년", RED, icon_clock)]
for i, (t, s1, s2, col, ic) in enumerate(cards):
    x0 = 80 + i * 310
    d.rounded_rectangle([x0, 160, x0 + 290, 640], radius=18, fill=WHITE, outline=col, width=3)
    ic(x0 + 145, 270)
    ctext(d, x0 + 145, 360, t, F_H, col)
    ctext(d, x0 + 145, 410, s1, F_S, INK)
    d.line([x0 + 30, 460, x0 + 260, 460], fill=DIM, width=2)
    # 두 줄로 나눠 쓰기
    words = s2.split(" "); mid = len(words) // 2
    ctext(d, x0 + 145, 480, " ".join(words[:mid]), F_S, GRAY); ctext(d, x0 + 145, 508, " ".join(words[mid:]), F_S, GRAY)
    ctext(d, x0 + 145, 570, "꺼진 쪽: 비었다" if i in (0, 3) else "꺼진 쪽: 약했다", F_M, col)
d.text((80, 665), "책도 같다 — 노벨 뒤 전체 도서 판매는 반년 만에 전보다 낮아졌지만(①·③ 없음), 『소년이 온다』(2년 연속 1위)는 남았다.", font=F_S, fill=INK)
foot(d, "근거: 공부노트 5장. 헤럴드경제 2025(상반기 도서 판매 후퇴), 연합 2026.3.27(NBCC상 뒤 5배).")
save(im, "C4_four_conditions_v2.png")

# ---------- C5 리센느 체크표 — 아이콘 + 게이지 ----------
im, d = canvas("리센느에게 감히 — 네 칸 중 지금 어디가 비어 있나", "공개된 숫자로만. 상표는 KIPRIS 2026.10.11 직접 조회. ○△X는 글쓴이 판단")
rows = [("① 무대", icon_stage, "축제 퀸·음방 6관왕 / 단독 콘서트 공지 없음", AMBER, "△", 0.5),
        ("② 팬덤 전환", icon_fans, "초동 3배, 밈 전 8만 / 구매자 남 69%, 반복 구매 미확인", AMBER, "△", 0.5),
        ("③ 다음 신호", icon_signal, "「데자뷰」 재역주행 / 11.3 「Pulse」가 첫 자체 시험", AMBER, "△", 0.5),
        ("④ 시계", icon_clock, "2031년 7년 만료 · 2025 영업손실 56억 · 상표 10건 전부 소속사", RED, "X", 0.15)]
y = 165
for t, ic, s, col, mark, g in rows:
    ic(150, y + 40)
    d.text((240, y + 8), t, font=F_H, fill=INK)
    d.text((240, y + 50), s, font=F_S, fill=GRAY)
    d.rounded_rectangle([900, y + 20, 1200, y + 60], radius=20, fill=LIGHT)
    d.rounded_rectangle([900, y + 20, 900 + 300 * g, y + 60], radius=20, fill=col)
    ctext(d, 1270, y + 12, mark, F_X, col)
    y += 120
box(d, (90, 640, 1310, 710), SAND, "조언 셋 — 밈 재탕 금지(「운전만해」) · 2027년 안 단독 무대를 셀 수 있는 숫자로 · 팀명 상표와 재계약 시계를 팬보다 먼저", F_S, INK)
foot(d, "근거: 엑스포츠 10.5, 스타뉴스 9.14, 일간스포츠 10.5·9.18, 머니투데이 9.14, 문화일보 10.4, KIPRIS 10.11. 게이지 길이는 판단의 시각화일 뿐 측정값이 아니다.")
save(im, "C5_rescene_checklist_v2.png")
print("done_info2")
