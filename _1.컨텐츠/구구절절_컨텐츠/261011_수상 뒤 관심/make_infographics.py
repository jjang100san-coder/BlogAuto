# -*- coding: utf-8 -*-
"""인포그래픽형 도해 4장(F1~F3, C3 교체). 숫자는 관심_공부노트 5-1·5-7 에서 확인한 것만."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_X, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
OUT = os.path.join(HERE, "img")
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)
F_M = font(24, True); F_BIG = font(72, True)
MAN = (41, 98, 255); WOMAN = (225, 80, 120); MAN_L = (205, 218, 255); WOMAN_L = (252, 215, 228)

def person(d, cx, top, h, col):
    """사람 픽토그램: 머리 원 + 몸통 둥근 사각."""
    r = h * 0.17
    d.ellipse([cx - r, top, cx + r, top + 2 * r], fill=col)
    bw = h * 0.42
    d.rounded_rectangle([cx - bw / 2, top + 2 * r + h * 0.05, cx + bw / 2, top + h], radius=int(bw / 2), fill=col)

def hbar(d, x0, y, w_max, frac, col, label, value, f=F_S, h=34):
    d.rounded_rectangle([x0, y, x0 + w_max, y + h], radius=8, fill=LIGHT)
    d.rounded_rectangle([x0, y, x0 + max(12, w_max * frac), y + h], radius=8, fill=col)
    d.text((x0 - 10 - d.textlength(label, font=f), y + 5), label, font=f, fill=INK)
    d.text((x0 + w_max * frac + 12, y + 3), value, font=F_M, fill=col)

# ---------- F1 리센느 팬덤은 누구인가 ----------
im, d = canvas("리센느 팬덤은 누구인가 — 열 명 중 일곱이 남자", "CU 「리센느 빵」 구매자 60만 개 기준. 10월 1일까지")
for i in range(10):
    person(d, 120 + i * 62, 170, 120, MAN if i < 7 else WOMAN)
d.text((100, 305), "남 69.1%", font=F_H, fill=MAN); d.text((560, 305), "여 30.9%", font=F_H, fill=WOMAN)
# 연령·성별 막대
rows = [("30대 남", 22.7, MAN), ("40대 남", 18.6, MAN), ("20대 남", 15.8, MAN),
        ("40대 여", 10.5, WOMAN), ("30대 여", 7.2, WOMAN), ("20대 여", 6.8, WOMAN)]
x0, y = 900, 170
d.text((x0 - 90, 128), "구매자 연령·성별 비율", font=F_M, fill=GRAY)
for lab, v, col in rows:
    hbar(d, x0, y, 360, v / 25, col, lab, f"{v}%"); y += 50
box(d, (90, 480, 1310, 560), SAND, "30·40대 남성만 41.3%. 첫 팬콘(2025.8) 예매자도 남성 약 70%(나무위키 기재, 공식 미확인).", F_B, INK)
box(d, (90, 580, 1310, 660), WHITE, "유입 경로: K카 유튜브 「나의 연수 아저씨」(이선민·유영우·원이) → 2026.7 졸업식으로 시즌 종료", F_B, INK, outline=GRAY)
foot(d, "근거: 문화일보 2026.10.4(CU 집계), 일간스포츠 2026.7.4·9.12. 사람 그림 1개 = 10%.")
save(im, "F1_fandom_pictogram.png")

# ---------- F2 브레이브걸스 역설 ----------
im, d = canvas("브레이브걸스의 역설 — 여성이 끌었는데도 2년 만에 끝났다", "2021.3.14~29 멜론 「롤린」 일 스트리밍 이용자(만 명) → 2023.2.16 계약 만료")
# 범위 막대(가로 축 0~40만)
ax0, ax1, ay = 260, 900, 250
for t in range(0, 41, 10):
    x = ax0 + (ax1 - ax0) * t / 40
    d.line([x, ay - 20, x, ay + 150], fill=(215, 215, 210), width=2)
    ctext(d, x, ay + 160, f"{t}만", F_S, GRAY)
def rng(d, y, lo, hi, col, lab):
    xl = ax0 + (ax1 - ax0) * lo / 40; xh = ax0 + (ax1 - ax0) * hi / 40
    d.rounded_rectangle([ax0, y, xh, y + 48], radius=10, fill=col)
    d.rounded_rectangle([xl, y, xh, y + 48], radius=10, fill=INK if False else col, outline=WHITE, width=2)
    d.text((ax0 - 150, y + 10), lab, font=F_H, fill=col)
    d.text((xh + 14, y + 8), f"{lo}~{hi}만", font=F_H, fill=col)
rng(d, ay, 27, 36, WOMAN, "여성")
rng(d, ay + 70, 24, 28, MAN, "남성")
d.text((ax0, ay - 60), "출발은 군통령(남성)이었지만 역주행 본체는 여성 청취자였다", font=F_M, fill=GRAY)
# 오른쪽 시계 + 결말
cx, cy, r = 1170, 265, 80
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=RED, width=6)
d.line([cx, cy, cx, cy - 55], fill=RED, width=7); d.line([cx, cy, cx + 38, cy + 18], fill=RED, width=7)
ctext(d, cx, cy + r + 12, "2023.2.16", F_H, RED); ctext(d, cx, cy + r + 48, "전원 계약 만료", F_M, RED)
arrow(d, (1010, ay + 60), (cx - r - 16, cy + 10), RED, 6)
box(d, (90, 470, 1310, 560), PINK, "활동 기간 중 콘서트·팬미팅 0회 · 2023.1 팬 현수막 시위 「컴백·콘서트·콘텐츠 아무것도 없다」\n팀명 상표는 소속사 → 「브브걸」로 개명", F_S, INK)
box(d, (90, 580, 1310, 670), SAND, "성별은 「누가 듣느냐」를 정하지, 무대·다음 신호·시계를 대신해 주지 않는다.\n여자친구(여성 팬 60%)도 7년 만료로 흩어졌다.", F_B, INK)
foot(d, "근거: 여성신문 2021.4(멜론 이용자 추이 27~36만 vs 24~28만), 아주경제 2023.2.16, 엑스포츠 2023.1, 서울신문 2016.3.16.")
save(im, "F2_bravegirls_paradox.png")

# ---------- F3 빵 vs 포카 ----------
im, d = canvas("한 번 사는 팬덤과 다시 사는 팬덤 — 구매 단위가 다르다", "아저씨 팬덤의 소비 vs 여성 팬덤의 소비 (확인된 숫자만)")
# 왼쪽: 빵 1개
box(d, (90, 150, 660, 200), MAN_L, "아저씨 팬덤 — 한 번", F_H, MAN)
bx, by = 375, 260
d.rounded_rectangle([bx - 110, by - 35, bx + 110, by + 55], radius=28, fill=(205, 140, 70), outline=(150, 95, 40), width=4)
d.ellipse([bx - 115, by - 70, bx + 115, by + 10], fill=(232, 185, 110), outline=(150, 95, 40), width=4)
for i in range(3):
    d.line([bx - 60 + i * 55, by - 55, bx - 30 + i * 55, by - 20], fill=(150, 95, 40), width=4)
ctext(d, bx, by + 70, "편의점 빵 · 음원 1회 · 편의점 모델", F_B, INK)
ctext(d, bx, by + 110, "저단가 · 1인 1회 · 지나가면 끝", F_M, MAN)
# 오른쪽: 포카 5장 겹치기
box(d, (740, 150, 1310, 200), WOMAN_L, "여성 팬덤 — 다시", F_H, WOMAN)
for i in range(5):
    x = 905 + i * 34; yy = 215 + i * 6
    d.rounded_rectangle([x, yy, x + 110, yy + 150], radius=10, fill=WHITE, outline=WOMAN, width=3)
    d.rounded_rectangle([x + 12, yy + 12, x + 98, yy + 100], radius=6, fill=WOMAN_L)
ctext(d, 1025, by + 70 + 60, "앨범 복수 구매 · 포카 교환 · 재가입", F_B, INK)
ctext(d, 1025, by + 110 + 60, "반복 · 같은 사람이 여러 번", F_M, WOMAN)
# 도넛: 포카마켓 여성 92.7%
cx, cy, r = 1130, 560, 90
d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * 0.927, fill=WOMAN)
d.pieslice([cx - r, cy - r, cx + r, cy + r], -90 + 360 * 0.927, 270, fill=MAN)
d.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=BG)
ctext(d, cx, cy - 22, "92.7%", F_H, WOMAN); ctext(d, cx, cy + 14, "여성", F_S, GRAY)
d.text((860, 660), "포토카드 거래 앱 설치자 성비", font=F_S, fill=GRAY)
box(d, (90, 470, 800, 690), SAND, "리센느 초동 10.7만이 어느 손에서 나왔는지는\n아직 모른다.\n\n그래서 체크표 ② 「팬덤 전환」은 ○가 아니라 △.", F_B, INK)
foot(d, "근거: 문화일보 2026.10.4(CU), Dighty 데이터마켓(포카마켓 설치자, 안드로이드 기준), i-boss 분석. 그림은 모식도.")
save(im, "F3_bread_vs_photocard.png")

# ---------- C3 교체: 몇 년 갔나 타임라인 ----------
im, d = canvas("폭발 뒤 몇 년 갔나 — 같은 역주행, 다른 길이", "막대 = 폭발(역주행·수상)부터 계약 만료·해체까지. 화살표 = 진행 중")
teams = [("브레이브걸스", 2021.2, 2023.1, False, "2년 · 콘서트 0회"),
         ("유니스", 2026.3, 2026.7, False, "6개월 · 계약 기간 고정"),
         ("EXID", 2015.0, 2019.4, False, "4년 · 7년 만료"),
         ("모모랜드", 2018.0, 2023.1, False, "5년 · 7년 만료"),
         ("여자친구", 2015.6, 2021.4, False, "6년 · 7년 만료"),
         ("오마이걸", 2020.4, 2023.6, True, "3년+ · 이듬해 첫 1위"),
         ("윤하", 2022.8, 2026.8, True, "4년+ · 투어 20회·2만 석"),
         ("리센느", 2026.2, 2026.8, True, "7개월 · 진행 중")]
ax0, ax1 = 330, 1180; ymax = 6.5
for t in range(0, 7):
    x = ax0 + (ax1 - ax0) * t / ymax
    d.line([x, 150, x, 690], fill=(220, 220, 215), width=2)
    ctext(d, x, 695, f"{t}년", F_S, GRAY)
y = 165
for name, s, e, alive, memo in teams:
    L = e - s; xe = ax0 + (ax1 - ax0) * L / ymax
    col = GREEN if alive else RED; fill = MINT if alive else PINK
    d.text((ax0 - 20 - d.textlength(name, font=F_H), y + 8), name, font=F_H, fill=col)
    d.rounded_rectangle([ax0, y, max(xe, ax0 + 30), y + 46], radius=10, fill=col)
    if alive: arrow(d, (xe, y + 23), (xe + 50, y + 23), col, 6)
    d.text(((xe + 60) if alive else (xe + 14), y + 10), memo, font=F_M, fill=col)
    y += 66
d.text((60, 720), "■ 끝남(계약 만료·해체)", font=F_S, fill=RED); d.text((330, 720), "■ 진행 중", font=F_S, fill=GREEN)
foot(d, "근거: 공부노트 5-1(아주경제·뉴시스·OSEN·텐아시아·일간스포츠·뉴스서울·fn). 시작점은 역주행 시작 달, 길이는 반올림.")
save(im, "C3_timeline_bars.png")
print("done_info")
