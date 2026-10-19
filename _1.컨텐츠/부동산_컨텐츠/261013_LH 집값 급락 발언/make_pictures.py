# -*- coding: utf-8 -*-
"""LH 사장 「집값 급락 가능성」 글 — 일반인용 그림 도해 15장(10/13).
숫자는 LH집값_공부노트·집값하락기_공부노트·LH집값_영상판독·LH집값_유튜브반론 확인분만.
따옴표 인용은 영상 두 판독 일치분(영상판독 #3·#5·#7·#12·#13)과 5곳 이상 일치한 9/30 기사 문장만.
대통령 8/30 X 글 비교는 넣지 않았다(정치 공방, 사용자 미결정)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "구구절절_컨텐츠", "261011_병역특례 논란"))  # 10/14 부동산으로 이관 — 도해 모듈은 구구절절 폴더에 그대로
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)
F_SM = font(18); F_M = font(24, True); F_MID = font(34, True); F_BIG = font(56, True); F_L = font(28, True); F_HUGE = font(72, True)
DIM = (205, 205, 200); SKIN = (230, 190, 160); NAVY = (40, 60, 110); ROOF = (170, 90, 70); WALL = (235, 225, 205)
REPLACED = {"02_apology_scope.png", "04_two_loan_slots.png", "06_lh_start_gauge.png", "07_rate_stairs.png", "08_my_interest.png", "10_four_cells.png", "13_scale_now.png", "14_same_numbers.png"}  # 10/13 그림판(make_simple.py)으로 교체
def save(im, n):
    if n in REPLACED: print("skip (make_simple.py 판 사용)", n); return
    im.save(os.path.join(OUT, n)); print("saved", n)

def person(d, cx, top, h, col):
    r = h * 0.17
    d.ellipse([cx - r, top, cx + r, top + 2 * r], fill=col)
    bw = h * 0.42; d.rounded_rectangle([cx - bw / 2, top + 2 * r + h * 0.05, cx + bw / 2, top + h], radius=int(bw / 2), fill=col)
def house(d, x, y, s=1.0, wall=WALL, roof=ROOF):
    d.polygon([(x, y - 70 * s), (x + 60 * s, y - 120 * s), (x + 120 * s, y - 70 * s)], fill=roof)
    d.rectangle([x + 12 * s, y - 70 * s, x + 108 * s, y], fill=wall); d.rectangle([x + 48 * s, y - 40 * s, x + 72 * s, y], fill=(150, 110, 80))
def apt(d, x, y, w, h, col=(200, 205, 215)):
    d.rectangle([x, y - h, x + w, y], fill=col, outline=GRAY, width=2)
    for yy in range(int(y - h + 12), int(y - 14), 22):
        for xx in range(int(x + 10), int(x + w - 14), 22): d.rectangle([xx, yy, xx + 10, yy + 10], fill=WHITE)
def bubble(d, xy, text, f=F_B, fill=WHITE, outline=INK, tail=None, color=INK):
    box(d, xy, fill, text, f, color, radius=24, outline=outline)
    if tail:
        (tx, ty), (bx0, bx1, by) = tail
        d.polygon([(bx0, by), (bx1, by), (tx, ty)], fill=fill)
        d.line([(bx0, by), (tx, ty), (bx1, by)], fill=outline, width=3)
def chip(d, x, y, text, col=NAVY, f=F_M):
    w = d.textlength(text, font=f) + 36
    d.rounded_rectangle([x, y, x + w, y + f.size + 18], radius=(f.size + 18) // 2, fill=col); d.text((x + 18, y + 7), text, font=f, fill=WHITE)
    return w
def check(d, cx, cy, r=16, col=GREEN):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); d.line([cx - r * 0.45, cy, cx - r * 0.1, cy + r * 0.4, cx + r * 0.5, cy - r * 0.35], fill=WHITE, width=4)
def xmark(d, cx, cy, r=16, col=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); k = r * 0.45
    d.line([cx - k, cy - k, cx + k, cy + k], fill=WHITE, width=4); d.line([cx + k, cy - k, cx - k, cy + k], fill=WHITE, width=4)
def down_arrow(d, cx, top, h, col=BLUE, w=46):
    d.rectangle([cx - w / 4, top, cx + w / 4, top + h - w * 0.8], fill=col)
    d.polygon([(cx - w / 2, top + h - w * 0.8), (cx + w / 2, top + h - w * 0.8), (cx, top + h)], fill=col)
def up_arrow(d, cx, bottom, h, col=RED, w=46):
    d.rectangle([cx - w / 4, bottom - h + w * 0.8, cx + w / 4, bottom], fill=col)
    d.polygon([(cx - w / 2, bottom - h + w * 0.8), (cx + w / 2, bottom - h + w * 0.8), (cx, bottom - h)], fill=col)
def truck(d, x, y, s=1.0, col=NAVY):
    d.rectangle([x, y - 60 * s, x + 95 * s, y - 10 * s], fill=col)
    d.polygon([(x + 95 * s, y - 45 * s), (x + 125 * s, y - 45 * s), (x + 140 * s, y - 25 * s), (x + 140 * s, y - 10 * s), (x + 95 * s, y - 10 * s)], fill=col)
    for wx in (x + 25 * s, x + 110 * s): d.ellipse([wx - 13 * s, y - 23 * s, wx + 13 * s, y + 3 * s], fill=INK)
def parcel(d, x, y, s=1.0):
    d.rectangle([x, y - 60 * s, x + 80 * s, y], fill=(200, 160, 110), outline=(150, 110, 70), width=3)
    d.line([x + 40 * s, y - 60 * s, x + 40 * s, y], fill=(150, 110, 70), width=4)
def clipboard(d, x, y, s=1.0):
    d.rounded_rectangle([x, y - 90 * s, x + 70 * s, y], radius=6, fill=WHITE, outline=INK, width=3)
    d.rectangle([x + 20 * s, y - 98 * s, x + 50 * s, y - 84 * s], fill=GRAY)
    for k in range(3): d.line([x + 14 * s, y - 64 * s + k * 18 * s, x + 56 * s, y - 64 * s + k * 18 * s], fill=GRAY, width=3)

# ---------- 01 한 문장 지도 ----------
im, d = canvas("「급락 가능성」은 열이틀 전 말의 「이유」였다", "9/30 기자 간담회 → 10/12 국정감사. 같은 사람, 같은 로직")
chip(d, 90, 170, "9/30 기자 간담회")
person(d, 190, 360, 170, GRAY)
bubble(d, (290, 230, 640, 360), "지금은 대출 규제가\n필요하지 않은가", F_M, tail=((250, 400), (300, 340, 358)))
d.text((310, 375), "생애 처음 집 사는 사람 70%·15억 이하 6억 한도를", font=F_SM, fill=GRAY)
d.text((310, 400), "더 조여야 한다는 취지 → 논란", font=F_SM, fill=GRAY)
arrow(d, (660, 440), (760, 440), INK, 6)
bubble(d, (650, 190, 780, 260), "왜요?", F_M, fill=SAND, outline=AMBER)
d.text((640, 465), "10/12 의원 질의", font=F_SM, fill=GRAY)
chip(d, 800, 170, "10/12 국정감사", RED)
person(d, 900, 360, 170, GRAY)
bubble(d, (990, 230, 1330, 360), "급락할 가능성이\n좀 많습니다", F_L, fill=PINK, outline=RED, color=RED, tail=((950, 400), (1000, 1040, 358)))
d.text((1010, 375), "앞으로 집값이 급락할 가능성이 있기 때문에", font=F_SM, fill=GRAY)
d.text((1010, 400), "그 점 고려해서 드린 말씀", font=F_SM, fill=GRAY)
box(d, (90, 575, 1310, 690), SAND, "국감의 「급락」은 새 주장이 아니다. 9/30 「대출을 더 묶자」의 근거를 꺼낸 것이다.\n9/30에도 「전례 없이 많은 물량이 나오고 금리도 상승」한다는 같은 이유를 댔다", F_S, INK)
foot(d, "근거: 공부노트 §0-1·§1(9/30 발언 5개 매체 일치), 영상판독 #5(국회방송 자동자막 = whisper 일치). 인물은 실루엣")
save(im, "01_two_dates.png")

# ---------- 02 사과한 것 · 거두지 않은 것 ----------
im, d = canvas("사과는 두 번 — 그런데 「무엇에」 사과했나", "국감장 사과 문장을 그대로 놓고 보면")
d.rounded_rectangle([90, 165, 680, 540], radius=18, fill=MINT)
check(d, 140, 205, 22); d.text((175, 186), "사과한 것", font=F_L, fill=GREEN)
d.text((130, 250), "① 관할하지 않는 업무(금융)를 언급한 것", font=F_B, fill=INK)
d.text((150, 292), "「그쪽 부서 있는 사람들한테는", font=F_S, fill=GRAY); d.text((150, 322), "좀 죄송하게 생각합니다」", font=F_S, fill=GRAY)
d.text((130, 382), "② 정책 결정 위치가 아닌데 발언한 것", font=F_B, fill=INK)
d.text((150, 424), "「정책을 결정하는 위치에 있지 않은데", font=F_S, fill=GRAY); d.text((150, 454), "발언한 점에 대해서 죄송하게 생각합니다」", font=F_S, fill=GRAY)
d.rounded_rectangle([720, 165, 1310, 540], radius=18, fill=PINK)
xmark(d, 770, 205, 22); d.text((805, 186), "거두지 않은 것", font=F_L, fill=RED)
d.text((760, 250), "대출을 더 묶어야 한다는 생각", font=F_B, fill=INK)
d.text((780, 292), "의원 질의에 「아직도 가지고 있다」는 취지", font=F_S, fill=GRAY)
d.text((760, 352), "집값이 급락할 가능성", font=F_B, fill=INK)
d.text((780, 394), "「정부 기조 아니라 제 생각」", font=F_S, fill=GRAY)
d.text((780, 424), "→ 개인 전망으로 남겨 둠", font=F_S, fill=GRAY)
box(d, (90, 585, 1310, 690), SAND, "사과는 「누가 말했나(자리)」에 대한 것이었고, 「무엇을 말했나(내용)」는 그대로다.\n그래서 이 글은 내용 — 왜 급락을 말했나 — 을 따라간다", F_S, INK)
foot(d, "근거: 영상판독 #12·#13(국회방송 자막 = whisper 일치), 공부노트 §1. 「아직도 가지고 있다」는 기사 4곳 대조")
save(im, "02_apology_scope.png")

# ---------- 03 세 계단 로직 ----------
im, d = canvas("사장의 로직 — 기둥 둘 위에 결론 하나", "국감 답변을 순서대로 이으면")
d.rounded_rectangle([90, 170, 470, 330], radius=16, fill=LIGHT)
apt(d, 115, 300, 60, 100); apt(d, 185, 300, 60, 80); apt(d, 255, 300, 60, 110)
d.text((330, 190), "기둥 ①", font=F_M, fill=NAVY); d.text((330, 225), "공급", font=F_L, fill=INK)
d.text((115, 305), "「2028년도부터 공급이 되고… 체감」", font=F_SM, fill=NAVY)
d.rounded_rectangle([90, 370, 470, 530], radius=16, fill=LIGHT)
for k, hh in enumerate([40, 65, 90]): d.rectangle([125 + k * 55, 500 - hh, 165 + k * 55, 500], fill=AMBER)
d.text((330, 390), "기둥 ②", font=F_M, fill=NAVY); d.text((330, 425), "금리", font=F_L, fill=INK)
d.text((115, 505), "「계속 금리가 높아지고」", font=F_SM, fill=NAVY)
arrow(d, (490, 350), (580, 350), INK, 6)
house(d, 610, 400, 1.2); down_arrow(d, 790, 260, 150, BLUE, 60)
ctext(d, 710, 420, "많이 낮아질", F_M, BLUE); ctext(d, 710, 452, "가능성", F_M, BLUE)
arrow(d, (860, 350), (940, 350), INK, 6)
bubble(d, (960, 200, 1320, 340), "안정이 되면 지금 바로\n집을 사지 않아도\n손해를 보지 않습니다", F_S, fill=PINK, outline=RED)
d.text((965, 350), "결론", font=F_M, fill=RED)
d.rounded_rectangle([960, 400, 1320, 520], radius=16, fill=SAND)
d.text((980, 415), "그러니(9/30)", font=F_M, fill=AMBER); d.text((980, 452), "대출을 묶어 급등도 급락도", font=F_S, fill=INK); d.text((980, 482), "없이 완만하게", font=F_S, fill=INK)
box(d, (90, 585, 1310, 690), SAND, "결론은 두 기둥이 둘 다 서야 선다.\n이 글은 기둥 하나씩 — 공급은 언제 오나, 금리는 얼마나 올랐나 — 를 확인한다", F_S, INK)
foot(d, "근거: 영상판독 #3·#6·#7(국회방송 자막 = whisper 일치), 공부노트 §0-2·§1(9/30 「완만하게」 5개 매체). 기둥 ② 인용은 #6 앞부분")
save(im, "03_logic_pillars.png")

# ---------- 04 대출 두 칸 ----------
im, d = canvas("사장이 더 조이자고 한 대출 두 칸", "둘 다 2025년에 이미 한 번씩 조인 칸이다")
# 상자
d.text((120, 170), "① 15억 이하 집", font=F_L, fill=INK)
d.rounded_rectangle([120, 230, 600, 520], radius=14, fill=WHITE, outline=INK, width=4)
house(d, 150, 500, 1.6)
d.rectangle([380, 300, 570, 500], fill=(210, 225, 245), outline=NAVY, width=3)
ctext(d, 475, 360, "대출", F_M, NAVY); ctext(d, 475, 398, "6억까지", F_MID, NAVY)
d.text((120, 535), "2025년 6월부터 수도권·규제지역 최대 6억", font=F_S, fill=GRAY)
# 사다리
d.text((780, 170), "② 생애 처음 사는 사람", font=F_L, fill=INK)
lx = 800
d.line([lx, 230, lx, 520], fill=(150, 110, 80), width=10); d.line([lx + 120, 230, lx + 120, 520], fill=(150, 110, 80), width=10)
for k in range(8):
    y = 500 - k * 36
    if k == 7: d.line([lx, y, lx + 120, y], fill=RED, width=6); d.line([lx - 10, y - 12, lx + 130, y + 12], fill=RED, width=3)
    else: d.line([lx, y, lx + 120, y], fill=(150, 110, 80), width=8)
d.text((lx + 150, 230), "80% 칸", font=F_M, fill=RED); d.text((lx + 150, 262), "2025년에 잘렸다", font=F_S, fill=RED)
d.text((lx + 150, 300), "지금 70%까지", font=F_MID, fill=NAVY)
d.text((lx + 150, 350), "집값의 70%를 대출로", font=F_S, fill=INK)
d.text((780, 535), "수도권·규제지역 생애최초 LTV 70%", font=F_S, fill=GRAY)
box(d, (90, 590, 1310, 690), SAND, "사장의 걱정 — 이 두 칸을 꽉 채워 「경쟁적으로」 사면 값이 오른다.\n질의한 의원들의 걱정 — 현금 없는 첫 집 수요는 이 두 칸 말고 길이 없다", F_S, INK)
foot(d, "근거: 공부노트 §4(6·27 대책 6억·생애최초 80→70%, 10·15 대책 15억 이하 6억), §1(9/30 「경쟁적으로 집을 사는 분들이 많다」 6곳 일치)")
save(im, "04_two_loan_slots.png")

# ---------- 05 공급은 택배 ----------
im, d = canvas("공급은 택배다 — 주문은 늘었는데 도착은 줄었다", "서울 주택, 2026년 1~8월, 1년 전과 비교")
xs = [130, 450, 770, 1090]
clipboard(d, xs[0] + 45, 330, 1.2); parcel(d, xs[1] + 40, 330, 1.3); truck(d, xs[2] + 20, 330, 1.3); house(d, xs[3] + 30, 330, 1.3)
for i in range(3): arrow(d, (xs[i] + (215 if i == 2 else 200), 290), (xs[i + 1] - 20, 290), DIM, 6)
labs = [("주문", "인허가"), ("출고", "착공"), ("배송 중", "몇 년 걸린다"), ("도착", "입주(준공)")]
vals = [("+40.4%", RED), ("+41.1%", RED), ("", INK), ("-19.1%", BLUE)]
for x, (a, b), (v, c) in zip(xs, labs, vals):
    ctext(d, x + 100, 350, a, F_L, INK); ctext(d, x + 100, 390, b, F_S, GRAY)
    if v: ctext(d, x + 100, 430, v, F_BIG, c)
ctext(d, xs[2] + 100, 440, "...", F_BIG, GRAY)
d.text((xs[3] + 20, 500), "전국은 -27.2%", font=F_S, fill=BLUE)
box(d, (90, 570, 1310, 690), SAND, "사는 사람이 느끼는 공급은 「도착」이다. 2026~2027년은 도착이 줄어드는 구간.\n도착이 다시 평년만큼 늘어나는 해 = 2028년 (정부 전망 · 사장 답변 같은 해)", F_S, INK)
foot(d, "근거: 공부노트 §2-2(국토부 8월 주택통계, 매경 9/30), §2-4. 영상판독 #7 「2028년도부터 공급이 되고」. 택배는 비유")
save(im, "05_supply_parcel.png")

# ---------- 06 LH 착공 게이지 ----------
im, d = canvas("LH 올해 착공 — 아홉 달에 4분의 1", "건설형 공공주택 착공 목표 51,783가구 중 (10/2 기준)")
x0, x1, y0 = 120, 1280, 210
d.rounded_rectangle([x0, y0, x1, y0 + 90], radius=20, fill=WHITE, outline=INK, width=4)
fx = x0 + (x1 - x0) * 0.257
d.rounded_rectangle([x0 + 6, y0 + 6, fx, y0 + 84], radius=16, fill=NAVY)
d.text((x0 + 20, y0 + 22), "13,293", font=F_MID, fill=WHITE)
d.text((fx + 20, y0 + 22), "25.7% 채움", font=F_MID, fill=NAVY)
d.text((x1 - 200, y0 + 100), "목표 51,783", font=F_M, fill=GRAY)
d.text((120, 380), "1~9월 한 달 평균", font=F_M, fill=INK)
d.rounded_rectangle([420, 378, 420 + 60, 418], radius=8, fill=NAVY); d.text((495, 380), "약 1,480가구", font=F_M, fill=NAVY)
d.text((120, 450), "남은 석 달, 한 달에", font=F_M, fill=INK)
d.rounded_rectangle([420, 448, 420 + 520, 488], radius=8, fill=AMBER); d.text((955, 450), "약 12,830가구", font=F_M, fill=AMBER)
d.text((420, 500), "지금까지 속도의 8.7배", font=F_S, fill=AMBER)
box(d, (90, 585, 1310, 690), SAND, "사장은 물량이 연말에 몰려 송구하지만 올해 목표는 달성할 수 있다는 취지로 답했다.\n착공은 「서류상 착공 신고」로 센다는 점도 국감에서 논쟁이 됐다", F_S, INK)
foot(d, "근거: 공부노트 §2-3(정희용 의원 국감 제시 25.7%, 에너지경제 월평균·배수 계산, 「신속착공」 논쟁)")
save(im, "06_lh_start_gauge.png")

# ---------- 07 금리 계단 ----------
im, d = canvas("금리 계단 — 그때는 열 칸, 지금은 두 칸", "한국은행 기준금리. 같은 높이 눈금으로 그렸다")
gy0, gy1 = 560, 180   # 0% → 4%
def ry(r): return gy0 - (gy0 - gy1) * r / 4.0
for r in [0, 1, 2, 3, 4]:
    d.line([110, ry(r), 1300, ry(r)], fill=(225, 225, 220), width=2); d.text((60, ry(r) - 14), f"{r}%", font=F_S, fill=GRAY)
steps1 = [0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.25, 2.50, 3.00, 3.25, 3.50]
sx, sw = 140, 46
for i, r in enumerate(steps1):
    d.rectangle([sx + i * sw, ry(r), sx + (i + 1) * sw - 4, gy0], fill=(200, 90, 80) if i else (210, 200, 195))
ctext(d, sx + 5.5 * sw, 600, "2021.8 → 2023.1", F_M, INK)
d.text((sx + 4 * sw, ry(3.5) - 70), "+3.00%p", font=F_BIG, fill=RED)
steps2 = [2.50, 2.75, 3.00]
sx2 = 900
for i, r in enumerate(steps2):
    d.rectangle([sx2 + i * 70, ry(r), sx2 + (i + 1) * 70 - 6, gy0], fill=AMBER if i else (210, 200, 195))
d.rectangle([sx2 + 3 * 70, ry(3.0) - 8, sx2 + 4 * 70 - 6, gy0], outline=GRAY, width=3)
ctext(d, sx2 + 3.5 * 70, ry(3.0) - 52, "10/22 ?", F_M, GRAY)
ctext(d, sx2 + 140, 600, "2026.7 → 2026.8", F_M, INK)
d.text((sx2 - 10, ry(3.0) - 120), "+0.50%p", font=F_BIG, fill=AMBER)
box(d, (90, 645, 1310, 715), SAND, "사장이 예로 든 「2021년 정점 → 고금리 → 하락」 때 오른 폭의 6분의 1에서 나온 전망이다", F_S, INK)
foot(d, "근거: 공부노트 §3-1·§3-3, 집값하락기 노트 §0-2(ECOS 722Y001). 영상판독 #4. 10/22 금통위는 예정")
save(im, "07_rate_stairs.png")

# ---------- 08 이자 계산기 ----------
im, d = canvas("「금리가 오른다」를 내 통장으로 바꾸면", "3억 원을 30년 동안 매달 같은 금액으로 갚는다고 치면(직접 계산)")
d.rounded_rectangle([110, 170, 330, 520], radius=22, fill=(60, 65, 80))
d.rounded_rectangle([135, 195, 305, 260], radius=8, fill=(200, 225, 200))
for r_ in range(4):
    for c_ in range(3): d.rounded_rectangle([140 + c_ * 56, 285 + r_ * 56, 186 + c_ * 56, 331 + r_ * 56], radius=8, fill=(120, 125, 140))
for i, (lab, rate, pay, col) in enumerate([("3월 평균", "4.34%", "149만 1,669원", NAVY), ("8월 평균", "4.66%", "154만 8,709원", RED)]):
    x = 420 + i * 450
    d.text((x, 185), lab, font=F_M, fill=GRAY); d.text((x, 225), rate, font=F_BIG, fill=col)
    d.text((x, 310), "한 달 갚는 돈", font=F_S, fill=INK); d.text((x, 345), pay, font=F_MID, fill=col)
arrow(d, (760, 260), (840, 260), INK, 6)
d.rounded_rectangle([420, 420, 1300, 520], radius=16, fill=PINK)
d.text((450, 432), "한 달 +5만 7,040원", font=F_MID, fill=RED)
d.text((450, 480), "30년 이자 합계 2억 3,700만 원 → 2억 5,754만 원", font=F_S, fill=INK)
box(d, (90, 580, 1310, 690), SAND, "대출에 기대는 비중이 큰 동네일수록 같은 금리도 무겁다.\n올해 집 산 돈 중 대출 비중 — 노원구 38.2%, 강남구 9.3%", F_S, INK)
foot(d, "근거: 공부노트 §3-2(한은 주담대 평균금리 신규), §4(자금조달계획서·김종양 의원실). 원리금균등, 실제 금리는 사람마다 다르다")
save(im, "08_my_interest.png")

# ---------- 09 40년 큰 하락 ----------
im, d = canvas("40년 동안 10% 넘게 빠진 건 두 번", "전국 아파트값이 고점에서 저점까지 빠진 폭(KB 지수)")
base_y = 240; scale = 11
d.line([100, base_y, 1320, base_y], fill=INK, width=3)
d.line([100, base_y + 10 * scale, 1320, base_y + 10 * scale], fill=RED, width=2)
d.text((1215, base_y + 10 * scale + 6), "-10% 선", font=F_S, fill=RED)
dips = [("1991~1998", -21.2, 170), ("2004", -1.9, 380), ("2008~09", -2.7, 540), ("2012~13", -1.3, 700), ("2018~19", -1.1, 860), ("2022~25", -11.4, 1080)]
for lab, v, x in dips:
    big = v <= -10
    d.rectangle([x, base_y, x + 110, base_y - v * scale], fill=RED if big else DIM)
    ctext(d, x + 55, base_y - 50, lab, F_M, INK)
    ctext(d, x + 55, base_y - v * scale + 8, f"{v}%", F_MID if big else F_M, RED if big else GRAY)
box(d, (90, 585, 1310, 690), SAND, "두 번 다 금리가 갑자기 크게 오른 때였다 — 1990년대 회사채 금리 19%대와 외환위기,\n2021~2023년 기준금리 1년 반 만에 7배(0.5% → 3.5%). 나머지는 전부 -3% 안쪽에서 멈췄다", F_S, INK)
foot(d, "근거: 집값하락기 노트 §0-1·§0-2(KB 전국 아파트 매매지수 ECOS 901Y062, 고점 월→저점 월, 명목, 계산)")
save(im, "09_two_big_drops.png")

# ---------- 10 네 칸 ----------
im, d = canvas("과거의 네 칸 — 지금은 어느 칸인가", "가로: 그때 입주(공급)가 많았나 / 세로: 금리가 급하게 크게 올랐나")
gx0, gx1, gx2 = 300, 800, 1300; gy0_, gy1_, gy2_ = 180, 370, 560
d.text((gx0 + 150, 145), "입주 많았다", font=F_M, fill=INK); d.text((gx1 + 130, 145), "입주 많지 않았다", font=F_M, fill=INK)
d.text((70, gy0_ + 60), "금리", font=F_M, fill=INK); d.text((70, gy0_ + 95), "급하게 크게", font=F_S, fill=INK)
d.text((70, gy1_ + 60), "금리", font=F_M, fill=INK); d.text((70, gy1_ + 95), "조금·낮았다", font=F_S, fill=INK)
cells = [
    ((gx0, gy0_, gx1, gy1_), PINK, "1991~93", "200만 호 입주 + 회사채 19%대", "서울 -19.8%", RED),
    ((gx1, gy0_, gx2, gy1_), PINK, "2022~23", "입주는 평년보다 적었다 + 금리 +3%p", "서울 -10.4%", RED),
    ((gx0, gy1_, gx2 - 500, gy2_), SAND, "2016~19", "지방 입주 최대 · 금리 1%대", "경북 -19.9% / 서울(2018) +13.6%", AMBER),
]
for (xy, fill, yr, desc, res, col) in cells:
    x0_, y0_, x1_, y1_ = xy
    d.rectangle([x0_ + 4, y0_ + 4, x1_ - 4, y1_ - 4], fill=fill)
    d.text((x0_ + 24, y0_ + 18), yr, font=F_M, fill=INK); d.text((x0_ + 24, y0_ + 60), desc, font=F_S, fill=INK)
    d.text((x0_ + 24, y0_ + 110), res, font=F_L, fill=col)
d.rectangle([gx1 + 4, gy1_ + 4, gx2 - 4, gy2_ - 4], fill=WHITE, outline=NAVY, width=5)
d.text((gx1 + 24, gy1_ + 18), "2026 지금", font=F_M, fill=NAVY); d.text((gx1 + 24, gy1_ + 60), "입주 감소 + 금리 +0.5%p", font=F_S, fill=INK)
d.text((gx1 + 24, gy1_ + 100), "?", font=F_BIG, fill=NAVY)
box(d, (90, 600, 1310, 700), SAND, "전국 10% 넘는 하락 두 번은 모두 윗줄(금리가 급하게 오른 때)에서 나왔다.\n입주 많은 칸은 지역을 갈랐다. 지금은 아랫줄 오른쪽 칸이다", F_S, INK)
foot(d, "근거: 집값하락기 노트 §0-4·§0-5·§1-1(KB 서울 아파트, 부동산원 경북), 2022년 준공 41.6만 호 < 2011~2025 평균 44.5만 호. 예측 아님")
save(im, "10_four_cells.png")

# ---------- 11 금리 올라도 오른 때 ----------
im, d = canvas("금리 방향과 집값 방향은 따로 갈 때가 많았다", "기준금리가 움직인 동안 아파트값은")
cards = [("2005.10~2008.9", "금리 8번 인상", "3.25 → 5.25%", "up", "서울 +37.5%", "KB"),
         ("2017.11~2019.6", "금리 두 번 인상", "1.25 → 1.75%", "up", "서울 +13.7%", "KB"),
         ("2008.9~2013.8", "금리 내린 시기", "5.25 → 2.50%", "down", "수도권 -11.9%", "부동산원")]
for i, (per, what, rng, rd, res, idx) in enumerate(cards):
    x = 100 + i * 410
    d.rounded_rectangle([x, 165, x + 380, 540], radius=18, fill=WHITE, outline=DIM, width=3)
    ctext(d, x + 190, 185, per, F_M, INK)
    d.text((x + 30, 240), "금리", font=F_S, fill=GRAY); d.text((x + 210, 240), "집값", font=F_S, fill=GRAY)
    if rd == "up": up_arrow(d, x + 80, 420, 140, AMBER)
    else: down_arrow(d, x + 80, 280, 140, AMBER)
    if res.endswith("%") and "-" in res: down_arrow(d, x + 260, 280, 140, BLUE)
    else: up_arrow(d, x + 260, 420, 140, RED)
    ctext(d, x + 80, 440, what, F_S, INK); ctext(d, x + 80, 470, rng, F_SM, GRAY)
    ctext(d, x + 260, 440, res, F_M, BLUE if "-" in res else RED); ctext(d, x + 260, 475, idx, F_SM, GRAY)
box(d, (90, 585, 1310, 690), SAND, "방향보다 「얼마나, 얼마나 빨리」가 갈랐다. 그리고 금리가 집값에 닿는 데는\n1년 남짓 걸린다는 연구가 있다(국토연구원, 지수에 따라 약 12개월·15개월)", F_S, INK)
foot(d, "근거: 집값하락기 노트 §0-3·§0-6(KB 서울 계산, 부동산원 수도권, 국토연 WP22-09). 2008~13 사이 한때 3.25%까지 재인상")
save(im, "11_rate_vs_price.png")

# ---------- 12 2021년 경고의 시차 ----------
im, d = canvas("2021년 「고점」 경고 — 방향은 맞고 시점은 어긋났다", "2021년 정부의 집값 경고와 그 뒤")
ty = 330
d.line([110, ty, 1300, ty], fill=INK, width=4)
pts = [(170, "2021.7.28", "정부 「고점」 경고", "추격 매수 신중하라는 취지", AMBER),
       (470, "1주 뒤", "수도권 주간 +0.37%", "9년 2개월 만의 최고 상승", RED),
       (790, "2021.8", "금리 인상 시작", "이후 1년 반 +3%p", AMBER),
       (1110, "2022년", "서울 실거래 -22.09%", "2006년 통계 시작 뒤 최대", BLUE)]
for x, when, what, sub, col in pts:
    d.ellipse([x - 16, ty - 16, x + 16, ty + 16], fill=col)
    ctext(d, x, ty - 70, when, F_M, INK); ctext(d, x, ty + 34, what, F_M, col); ctext(d, x, ty + 72, sub, F_SM, GRAY)
d.rounded_rectangle([170, 470, 1110, 520], radius=12, fill=SAND)
ctext(d, 640, 478, "경고 뒤에도 한동안 더 올랐고, 큰 하락은 이듬해에 왔다", F_M, AMBER)
box(d, (90, 580, 1310, 690), SAND, "「지금 안 사도 손해 안 본다」의 「지금」이 언제까지인지가 이 말의 빈칸이다.\n사장이 국감에서 직접 든 예도 이 2021년이다", F_S, INK)
foot(d, "근거: 공부노트 §6-1(뉴스1 2021-07-28, YTN 2021-08-05 부동산원 주간, 2022년 서울 아파트 실거래가지수 -22.09%), 영상판독 #4")
save(im, "12_warning_lag.png")

# ---------- 13 지금 저울 ----------
im, d = canvas("지금 시장 — 저울 양쪽에 다 올라가 있다", "10월 초 기준 숫자. 「누가 셌나」를 같이 적었다")
cx = 700
d.polygon([(cx - 40, 560), (cx + 40, 560), (cx, 470)], fill=GRAY)
d.line([345, 220, 1055, 220], fill=INK, width=8); d.line([cx, 220, cx, 470], fill=INK, width=8)
for sx_, (bx0, bx1) in [(345, (90, 600)), (1055, (800, 1310))]:
    d.line([sx_, 220, bx0 + 30, 292], fill=GRAY, width=3); d.line([sx_, 220, bx1 - 30, 292], fill=GRAY, width=3)
d.rounded_rectangle([90, 290, 600, 540], radius=16, fill=LIGHT)
d.text((110, 300), "내려갈 수 있다는 신호", font=F_M, fill=BLUE)
for k, t in enumerate(["9월 서울 아파트 거래 2,477건(아실, 잠정)", "매물 연초보다 +24.7%(아실)", "매수우위지수 71.7 — 파는 쪽이 많다(KB)", "강남3구·용산 주간 하락(부동산원)"]):
    d.text((110, 345 + k * 46), "· " + t, font=F_S, fill=INK)
d.rounded_rectangle([800, 290, 1310, 540], radius=16, fill=PINK)
d.text((820, 300), "아직 오른다는 신호", font=F_M, fill=RED)
for k, t in enumerate(["서울 87주 연속 상승(부동산원)", "올해 서울 전셋값 +8.35%(부동산원)", "생애최초 매수 53.8%, 사상 최고(8월)", "서울 입주 -19.1%(국토부, 1~8월)"]):
    d.text((820, 345 + k * 46), "· " + t, font=F_S, fill=INK)
box(d, (90, 590, 1310, 690), SAND, "「급락 가능성」은 왼쪽 접시의 지금 숫자가 아니라,\n2028년 공급과 금리를 내다본 전망이다", F_S, INK)
foot(d, "근거: 공부노트 §5(부동산원 10/5 기준, KB 9월, 아실 10/6·10/8, 대법원 등기정보광장). 9월 거래는 신고기한 30일이라 10월 말 확정")
save(im, "13_scale_now.png")

# ---------- 14 같은 숫자 두 해석 ----------
im, d = canvas("같은 숫자, 정반대 결론 — 그런데 둘 다 「2028년」을 말한다", "LH 사장 vs 「공급돼도 안 떨어진다」는 유튜브 해설들")
d.rounded_rectangle([490, 165, 910, 300], radius=16, fill=WHITE, outline=INK, width=3)
ctext(d, 700, 180, "착공 +41%", F_M, INK); ctext(d, 700, 216, "입주 -19%", F_M, INK); ctext(d, 700, 252, "금리 +0.5%p", F_M, INK)
person(d, 170, 330, 150, NAVY); ctext(d, 170, 490, "LH 사장", F_M, NAVY)
bubble(d, (250, 330, 640, 520), "곧 쏟아진다, 금리도 오른다\n→ 많이 낮아질 수 있다\n→ 지금 안 사도 손해 안 본다", F_S, fill=LIGHT, outline=NAVY)
person(d, 1230, 330, 150, RED); ctext(d, 1230, 490, "반대편 해설", F_M, RED)
bubble(d, (760, 330, 1150, 520), "입주는 2028년부터, 금리는\n2022년과 폭이 다르다\n→ 그때까진 전세·매매가 오른다", F_S, fill=PINK, outline=RED)
arrow(d, (580, 300), (450, 330), DIM, 4); arrow(d, (820, 300), (950, 330), DIM, 4)
box(d, (90, 570, 1310, 690), SAND, "두 쪽 다 공급이 체감되는 해를 2028년으로 본다.\n갈리는 건 지금부터 2028년까지의 시간을 어떻게 보느냐다", F_B, INK)
foot(d, "근거: 영상판독 #3·#7, 유튜브반론 노트 §2-A·D(자막 판독 요약, 해설 영상 여러 편의 공통 논리 — 특정 채널 아님), 공부노트 §2-2")
save(im, "14_same_numbers.png")

# ---------- 15 내 달력 ----------
im, d = canvas("누구 말이 맞을지는 2028년이 알려 준다", "그 전에 정할 수 있는 건 내 달력이다")
years = [("2026", 160), ("2027", 520), ("2028", 880), ("2029", 1240)]
ty = 330
d.line([120, ty, 1300, ty], fill=INK, width=5)
for y_, x in years:
    d.line([x, ty - 14, x, ty + 14], fill=INK, width=5); ctext(d, x, ty + 26, y_, F_L, INK)
d.rectangle([444, ty - 40, 880, ty - 8], fill=SAND); ctext(d, 662, ty - 80, "지금 ~ 2028년", F_MID, AMBER)
d.polygon([(444, ty - 8), (432, ty - 50), (456, ty - 50)], fill=NAVY); ctext(d, 444, ty - 160, "지금(2026.10)", F_M, NAVY); d.line([444, ty - 125, 444, ty - 50], fill=NAVY, width=4)
d.ellipse([862, ty - 160, 898, ty - 124], fill=GREEN); d.line([880, ty - 124, 880, ty - 8], fill=GREEN, width=4)
d.text((910, ty - 175), "공급이 체감되는 해", font=F_M, fill=GREEN); d.text((910, ty - 140), "(사장·정부 전망)", font=F_S, fill=GRAY)
d.rounded_rectangle([420, 430, 980, 530], radius=14, fill=WHITE, outline=RED, width=4)
ctext(d, 700, 445, "내가 집이 필요한 때는?", F_L, RED); ctext(d, 700, 488, "이사 · 결혼 · 계약 만기 · 아이 학교", F_S, GRAY)
d.line([700, 430, 700, ty + 70], fill=RED, width=3)
box(d, (90, 585, 1310, 690), SAND, "「지금 안 사도 손해 안 본다」는 말과 「그때까진 오른다」는 말 사이의 거리는 지금부터 2028년까지다.\n그 사이 내 일정이 어디쯤 놓이는지가 어느 말을 더 무겁게 들을지를 정한다", F_S, INK)
foot(d, "근거: 영상판독 #7(2028년도부터), 공부노트 §2-2(정부 전망 2028년). 투자 권유 아님 — 판단은 각자의 상황에 따라")
save(im, "15_my_calendar.png")
