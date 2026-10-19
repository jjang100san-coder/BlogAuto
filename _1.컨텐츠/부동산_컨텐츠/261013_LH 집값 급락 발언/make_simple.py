# -*- coding: utf-8 -*-
"""LH 글 — 그림 중심 판(10/13 사용자 「구구절절은 글보다 이미지가 중심, 일반인이 이해할 만큼 쉽고 세세하게」).
- 원리 그림 3장 신설: R1 금리가 내 집값까지 오는 길 · R2 입주가 집값까지 오는 길 · R3 생애 첫 집 대출 한도 계산
- 글자에 기대던 4장 다시: 02 사과 범위 · 10 네 칸 · 13 저울 · 14 두 해석 → 아이콘·크기·화살표
나머지(01·03·05·06·07·08·09·11·12·15)는 make_pictures.py 그대로. 헬퍼는 make_pictures.py 앞부분을 그대로 불러 쓴다.
계산: 월 150만 원·30년 원리금균등 → 4.34% 3억 168만 / 4.66% 2억 9,056만(직접 계산). 6억 ÷ 0.7 = 8억 5,714만."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "make_pictures.py"), encoding="utf-8").read()
exec(_src[:_src.index("# ---------- 01")])
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)   # 앞부분의 REPLACED 건너뛰기를 끈다 — 이 판이 그 그림을 만든다

def bank(d, x, y, s=1.0, col=NAVY, label=""):
    d.polygon([(x, y - 90 * s), (x + 70 * s, y - 125 * s), (x + 140 * s, y - 90 * s)], fill=col)
    for k in range(4): d.rectangle([x + 14 * s + k * 32 * s, y - 85 * s, x + 30 * s + k * 32 * s, y - 15 * s], fill=col)
    d.rectangle([x, y - 15 * s, x + 140 * s, y], fill=col)
    if label: ctext(d, x + 70 * s, y + 10, label, F_M, col)
def chair(d, x, y, s=1.0, col=(90, 90, 100)):
    d.rounded_rectangle([x + 20 * s, y - 170 * s, x + 120 * s, y - 70 * s], radius=14, fill=col)
    d.rounded_rectangle([x, y - 75 * s, x + 140 * s, y - 45 * s], radius=10, fill=col)
    d.rectangle([x + 62 * s, y - 45 * s, x + 78 * s, y - 15 * s], fill=col)
    d.line([x + 20 * s, y, x + 120 * s, y], fill=col, width=int(10 * s))
def stamp(d, cx, cy, r, text, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=6)
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], outline=col, width=2)
    ctext(d, cx, cy - 20, text, F_L, col)
def coin(d, cx, cy, r=20): d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 200, 80), outline=(190, 140, 30), width=3)
def envelope(d, x, y, w=150, h=100):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=3); d.line([x, y, x + w / 2, y + h * 0.55, x + w, y], fill=INK, width=3)
def sign(d, x, y, text="전세", col=GREEN):
    d.line([x + 30, y, x + 30, y + 70], fill=(150, 110, 80), width=6)
    d.rounded_rectangle([x, y - 34, x + 60, y + 4], radius=6, fill=col); ctext(d, x + 30, y - 31, text, F_SM, WHITE)
def stairs(d, x, y, n, step_w, step_h, col):
    for k in range(n): d.rectangle([x + k * step_w, y - (k + 1) * step_h, x + (k + 1) * step_w - 2, y], fill=col)
def calendar(d, x, y, w=70, h=64, col=RED):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=WHITE, outline=INK, width=3); d.rectangle([x, y, x + w, y + 18], fill=col)
    for r_ in range(2):
        for c_ in range(3): d.rectangle([x + 10 + c_ * 20, y + 26 + r_ * 16, x + 22 + c_ * 20, y + 36 + r_ * 16], fill=GRAY)
def key(d, x, y, col=AMBER):
    d.ellipse([x, y, x + 34, y + 34], outline=col, width=7); d.line([x + 32, y + 17, x + 74, y + 17], fill=col, width=7)
    d.line([x + 60, y + 17, x + 60, y + 32], fill=col, width=6); d.line([x + 70, y + 17, x + 70, y + 28], fill=col, width=6)
def tile(d, x, y, w, h, fill, icon, big, lab, col):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fill)
    icon(x + 14, y + 4)
    d.text((x + 120, y + 18), big, font=F_MID, fill=col); d.text((x + 300, y + 26), lab, font=F_B, fill=INK)

# ---------- R1 금리가 오는 길 ----------
im, d = canvas("금리가 내 집값까지 오는 길", "한국은행이 올린 금리는 은행을 거쳐 「내가 빌릴 수 있는 돈」을 줄인다")
bank(d, 90, 330, 1.0, NAVY, "한국은행"); ctext(d, 160, 380, "기준금리 3.00%", F_S, INK)
arrow(d, (260, 270), (330, 270), INK, 6)
bank(d, 350, 330, 1.0, (90, 120, 90), "은행"); ctext(d, 420, 380, "주담대 최상단 6.23% → 7.29%", F_S, INK)
arrow(d, (520, 270), (590, 270), INK, 6)
envelope(d, 610, 200); ctext(d, 685, 320, "한 달에 갚을 수 있는 돈", F_S, INK); ctext(d, 685, 350, "150만 원 그대로라면", F_M, INK)
arrow(d, (790, 270), (860, 270), INK, 6)
# 빌릴 수 있는 돈 막대
for i, (lab, v, col) in enumerate([("작년 말 6.23%일 때", 2.4413, NAVY), ("9월 7.29%일 때", 2.1901, RED)]):
    y0 = 190 + i * 95
    d.text((860, y0), lab, font=F_S, fill=GRAY)
    d.rounded_rectangle([860, y0 + 30, 860 + v * 105, y0 + 72], radius=8, fill=col)
    d.text((860 + v * 105 + 14, y0 + 34), ["2억 4,413만 원", "2억 1,901만 원"][i], font=F_M, fill=col)
d.text((860, 395), "빌릴 수 있는 돈 2,512만 원 줄어듦", font=F_M, fill=RED)
clock = lambda cx, cy, r: (d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=5, fill=WHITE), d.line([cx, cy, cx, cy - r * 0.6], fill=INK, width=5), d.line([cx, cy, cx + r * 0.45, cy + r * 0.2], fill=INK, width=5))
clock(150, 500, 36); d.text((200, 470), "살 수 있는 사람이 줄면 집값이 반응한다 — 그때까지 1년 남짓", font=F_M, fill=INK)
d.text((200, 508), "(국토연구원 연구: 지수에 따라 약 12개월·15개월)", font=F_S, fill=GRAY)
box(d, (90, 585, 1310, 690), SAND, "금리는 「이자가 얼마나 무거운가」보다 먼저 「얼마를 빌릴 수 있나」를 바꾼다.\n월 150만 원을 갚을 수 있는 사람이 빌릴 수 있는 돈이 2,512만 원 줄었다(최상단 금리 기준)", F_S, INK)
foot(d, "근거: 공부노트 §3-1, 뉴시스 9/16(5대 은행 주담대 고정 5년 혼합형 상단), 하락기 노트 §0-6. 30년 원리금균등 직접 계산")
save(im, "R1_rate_path.png")

# ---------- R2 입주가 오는 길 ----------
im, d = canvas("입주가 집값까지 오는 길 — 전세를 거쳐 간다", "새 아파트에 열쇠가 나오면 무슨 일이 생기나 (모식도)")
apt(d, 90, 350, 70, 150, (190, 200, 220)); apt(d, 170, 350, 70, 120, (190, 200, 220)); truck(d, 250, 350, 0.9)
ctext(d, 190, 370, "① 새 아파트 입주", F_M, INK)
arrow(d, (390, 280), (450, 280), INK, 6)
for k in range(3): house(d, 470 + k * 90, 350, 0.65)
for k in range(3): sign(d, 470 + k * 90 + 10, 230, "전세")
ctext(d, 600, 370, "② 이사 나온 집이", F_M, INK); ctext(d, 600, 402, "세입자를 찾는다", F_S, INK)
arrow(d, (760, 280), (820, 280), INK, 6)
key(d, 850, 230); down_arrow(d, 990, 200, 140, BLUE, 56)
ctext(d, 930, 370, "③ 전셋값이", F_M, BLUE); ctext(d, 930, 402, "내려간다", F_S, BLUE)
arrow(d, (1060, 280), (1110, 280), INK, 6)
person(d, 1200, 230, 110, GRAY); ctext(d, 1200, 370, "④ 서둘러 살", F_M, INK); ctext(d, 1200, 402, "사람이 준다", F_S, INK)
d.rounded_rectangle([1120, 170, 1290, 210], radius=10, fill=WHITE, outline=GRAY, width=2); ctext(d, 1205, 177, "전세로도 되네", F_SM, GRAY)
d.rounded_rectangle([90, 445, 1310, 545], radius=14, fill=LIGHT)
d.text((120, 458), "실제 예 — 2003~04년", font=F_M, fill=NAVY)
d.text((120, 500), "2002년 인허가가 크게 늘고 2003~04년 입주가 쏟아지자, 전셋값이 2003년 4월 고점부터 2005년 1월까지 내렸다", font=F_S, fill=INK)
box(d, (90, 585, 1310, 690), SAND, "그래서 값을 움직이는 건 「주문(착공)」이 아니라 「도착(입주)」이다.\n주문이 늘어도 도착 전까지는 이 길이 시작되지 않는다", F_S, INK)
foot(d, "근거: 집값하락기 노트 §2-C(주택금융연구원 강영신 2023, 2003~04 입주 증가와 전세 하락). ④는 모식")
save(im, "R2_supply_path.png")

# ---------- R3 생애 첫 집 대출 한도 ----------
im, d = canvas("생애 첫 집, 얼마까지 빌리나 — 70%와 6억 뚜껑 중 낮은 쪽", "수도권·규제지역, 15억 이하 집 기준 단순 계산")
base, sc = 540, 26   # 1억 = 26px
cap_y = base - 6 * sc
for i, (price, x) in enumerate([(8, 170), (10, 560), (15, 950)]):
    house(d, x + 10, 245, 0.7 + i * 0.1)
    d.text((x + 130 + i * 12, 205), f"집값 {price}억", font=F_M, fill=INK)
    want = price * 0.7; got = min(want, 6)
    d.rectangle([x + 20, base - want * sc, x + 120, base], outline=GRAY, width=3)
    d.rectangle([x + 20, base - got * sc, x + 120, base], fill=GREEN if want <= 6 else AMBER)
    lab = f"{got:.1f}억".replace(".0억", "억")
    ctext(d, x + 70, base - got * sc + 8, lab, F_M, WHITE)
    if want > 6: d.text((x + 135, base - want * sc - 4), f"70%면 {want:g}억", font=F_S, fill=GRAY)
d.line([120, cap_y, 1320, cap_y], fill=RED, width=5); d.text((1180, cap_y - 36), "6억 뚜껑", font=F_M, fill=RED)
d.line([120, base, 1320, base], fill=INK, width=3)
box(d, (90, 590, 1310, 690), SAND, "집값이 8억 5,714만 원을 넘으면 70%보다 6억 뚜껑에 먼저 닿는다(계산).\n사장이 더 낮추자고 한 게 바로 이 70%와 6억이다", F_S, INK)
foot(d, "근거: 공부노트 §4(6·27 원문 「주택구입 목적 주담대 최대한도 6억」, 생애최초 LTV 70%), §1. 소득·DSR 등 다른 조건은 뺀 단순 계산")
save(im, "R3_first_home_loan.png")

# ---------- 02 사과 범위 (그림판) ----------
im, d = canvas("사과한 건 「자리」, 남겨 둔 건 「내용」", "국감장 사과 두 번을 그림으로 놓으면")
chair(d, 200, 470, 1.4); stamp(d, 520, 330, 100, "죄송", GREEN)
ctext(d, 300, 500, "정책을 정하는 자리가 아닌데 말한 것", F_S, INK)
ctext(d, 300, 530, "관할 밖(금융) 일을 말한 것", F_S, INK)
bubble(d, (800, 200, 1140, 330), "급락 가능성", F_MID, fill=PINK, outline=RED, color=RED, tail=((860, 380), (860, 900, 328)))
d.rounded_rectangle([830, 380, 1140, 460], radius=14, fill=LIGHT, outline=NAVY, width=3); ctext(d, 985, 400, "대출 더 묶자", F_L, NAVY)
stamp(d, 1220, 330, 80, "그대로", RED)
ctext(d, 985, 500, "「정부 기조 아니라 제 생각」", F_S, INK)
box(d, (90, 590, 1310, 690), SAND, "사과는 누가 말했나(자리)에 대한 것이었다. 무엇을 말했나(내용)는 그대로다.\n그래서 이 글은 내용 — 왜 급락을 말했나 — 을 따라간다", F_S, INK)
foot(d, "근거: 영상판독 #12·#13(국회방송 자막 = whisper 일치), 공부노트 §1")
save(im, "02_apology_scope.png")

# ---------- 10 네 칸 (그림판) ----------
im, d = canvas("과거의 네 칸 — 지금은 어느 칸인가", "가로: 입주가 많았나 / 세로: 금리가 급하게 올랐나")
gx0, gx1, gx2 = 300, 800, 1300; gy0_, gy1_, gy2_ = 180, 375, 570
d.text((gx0 + 170, 145), "입주 많음", font=F_M, fill=INK); d.text((gx1 + 150, 145), "입주 적음", font=F_M, fill=INK)
stairs(d, 110, gy0_ + 150, 5, 30, 24, RED); ctext(d, 185, gy0_ + 160, "금리 급등", F_M, RED)
stairs(d, 110, gy1_ + 150, 5, 30, 6, AMBER); ctext(d, 185, gy1_ + 160, "금리 완만", F_M, AMBER)
def cell(x0_, y0_, x1_, y1_, fill, yr, n_apt, res, col, res2=None):
    d.rectangle([x0_ + 4, y0_ + 4, x1_ - 4, y1_ - 4], fill=fill)
    d.text((x0_ + 22, y0_ + 14), yr, font=F_M, fill=INK)
    for k in range(n_apt): apt(d, x0_ + 24 + k * 44, y1_ - 20, 38, 70 + (k % 2) * 20, (185, 195, 215))
    d.text((x0_ + 250, y0_ + 60), res, font=F_MID, fill=col)
    if res2: d.text((x0_ + 250, y0_ + 110), res2, font=F_MID, fill=RED)
cell(gx0, gy0_, gx1, gy1_, PINK, "1991~93", 5, "서울 -19.8%", RED)
cell(gx1, gy0_, gx2, gy1_, PINK, "2022~23", 1, "서울 -10.4%", RED)
cell(gx0, gy1_, gx1, gy2_, SAND, "2016~19", 5, "경북 -19.9%", BLUE, "서울 +13.6%")
d.rectangle([gx1 + 4, gy1_ + 4, gx2 - 4, gy2_ - 4], fill=WHITE, outline=NAVY, width=5)
d.text((gx1 + 22, gy1_ + 14), "2026 지금", font=F_M, fill=NAVY)
apt(d, gx1 + 24, gy2_ - 20, 38, 70, (185, 195, 215)); d.text((gx1 + 250, gy1_ + 50), "?", font=F_HUGE, fill=NAVY)
box(d, (90, 610, 1310, 700), SAND, "전국 10% 넘는 하락 두 번은 모두 윗줄(금리 급등)에서 나왔다. 지금은 아랫줄 오른쪽", F_S, INK)
foot(d, "근거: 집값하락기 노트 §0-4·§0-5·§1-1(KB 서울, 부동산원 경북·2016~19 지방). 2022년 준공 41.6만 호 < 평균 44.5만 호. 예측 아님")
save(im, "10_four_cells.png")

# ---------- 13 저울 (그림판) ----------
im, d = canvas("지금 시장 — 저울 양쪽에 다 올라가 있다", "10월 초 숫자. 왼쪽은 내려갈 수 있다는 신호, 오른쪽은 아직 오른다는 신호")
cx = 700
d.polygon([(cx - 40, 580), (cx + 40, 580), (cx, 500)], fill=GRAY)
d.line([345, 170, 1055, 170], fill=INK, width=8); d.line([cx, 170, cx, 500], fill=INK, width=8)
for sx_, (bx0, bx1) in [(345, (70, 620)), (1055, (780, 1330))]:
    d.line([sx_, 170, bx0 + 30, 210], fill=GRAY, width=3); d.line([sx_, 170, bx1 - 30, 210], fill=GRAY, width=3)
L = [(lambda x, y: (house(d, x, y + 72, 0.55), down_arrow(d, x + 80, y + 2, 70, BLUE, 28)), "2,477건", "9월 서울 거래(잠정)"),
     (lambda x, y: [house(d, x + k * 16, y + 74 - k * 8, 0.45) for k in range(3)], "+24.7%", "쌓인 매물(연초 대비)"),
     (lambda x, y: (person(d, x + 15, y + 6, 66, BLUE), person(d, x + 45, y + 6, 66, BLUE), person(d, x + 75, y + 24, 48, GRAY)), "71.7", "파는 사람이 더 많다"),
     (lambda x, y: (d.ellipse([x + 20, y + 4, x + 64, y + 48], fill=BLUE), d.polygon([(x + 22, y + 34), (x + 62, y + 34), (x + 42, y + 72)], fill=BLUE)), "하락", "강남3구·용산 주간")]
Rr = [(lambda x, y: calendar(d, x + 10, y + 6), "87주", "서울 연속 상승"),
      (lambda x, y: key(d, x + 6, y + 22), "+8.35%", "올해 서울 전셋값"),
      (lambda x, y: (person(d, x + 30, y + 4, 70, RED), d.polygon([(x + 62, y), (x + 70, y + 16), (x + 86, y + 16), (x + 73, y + 26), (x + 78, y + 42), (x + 62, y + 32), (x + 46, y + 42), (x + 51, y + 26), (x + 38, y + 16), (x + 54, y + 16)], fill=AMBER)), "53.8%", "생애 첫 집 매수"),
      (lambda x, y: (truck(d, x, y + 70, 0.6), down_arrow(d, x + 40, y + 4, 36, RED, 24)), "-19.1%", "서울 입주(1~8월)")]
for i, (ic, big, lab) in enumerate(L):
    tile(d, 70, 215 + i * 92, 560, 82, LIGHT, ic, big, lab, BLUE)
for i, (ic, big, lab) in enumerate(Rr):
    tile(d, 770, 215 + i * 92, 560, 82, PINK, ic, big, lab, RED)
box(d, (90, 610, 1310, 700), SAND, "「급락 가능성」은 왼쪽 접시의 지금 숫자가 아니라, 2028년 공급과 금리를 내다본 전망이다", F_S, INK)
foot(d, "근거: 공부노트 §5(부동산원 10/5, KB 매수우위지수 9월, 아실 10/6, 등기정보광장 8월), §2-2(국토부 1~8월). 9월 거래는 10월 말 확정")
save(im, "13_scale_now.png")

# ---------- 14 두 길, 같은 도착 (그림판) ----------
im, d = canvas("두 길, 같은 도착 — 둘 다 「2028년」을 본다", "LH 사장과 「공급돼도 안 떨어진다」 해설들이 그리는 길 (모식도, 실제 전망치 아님)")
x0, x1, ym = 200, 1050, 380
house(d, 80, ym + 40, 0.9); ctext(d, 140, ym + 55, "지금", F_M, INK)
d.line([x0, ym, x1, ym - 140], fill=RED, width=8); d.line([x0, ym, x1, ym + 140], fill=NAVY, width=8)
up_arrow(d, 640, ym - 95, 60, RED, 34); down_arrow(d, 640, ym + 40, 60, NAVY, 34)
d.text((240, ym - 140), "반대편 해설: 그때까진 오른다", font=F_M, fill=RED)
d.text((240, ym + 100), "LH 사장: 많이 낮아질 수 있다", font=F_M, fill=NAVY)
d.line([x1 + 20, 170, x1 + 20, 560], fill=GREEN, width=6); d.polygon([(x1 + 20, 170), (x1 + 120, 195), (x1 + 20, 220)], fill=GREEN)
ctext(d, x1 + 80, 235, "2028년", F_L, GREEN); truck(d, x1 + 50, 330, 0.9, GREEN); ctext(d, x1 + 150, 345, "입주가 늘어나는 해", F_S, GREEN)
box(d, (90, 600, 1310, 700), SAND, "도착 지점은 같다. 갈리는 건 지금부터 2028년까지의 길이다", F_B, INK)
foot(d, "근거: 영상판독 #3·#7, 유튜브반론 노트 §2·§4-1(Y2·Y3 「지금 착공해도 4년 뒤 입주」), 공부노트 §2-2. 선 기울기는 모식")
save(im, "14_same_numbers.png")

# ======== 10/13 세 번째 손질: 「4분의 1」「계단 열 칸」이 직관적이지 않다 · 금리는 최상단으로 · 마무리는 단순하게 ========
# ---------- 06 100채 중 26채 ----------
im, d = canvas("올해 짓기로 한 100채 중 26채만 땅을 팠다", "LH가 직접 짓는 공공주택 올해 착공 목표(51,783가구)를 100채로 줄여 그리면 — 10/2 기준 25.7%")
for k in range(100):
    r_, c_ = divmod(k, 10); x = 90 + c_ * 46; y = 175 + r_ * 38
    if k < 26: house(d, x, y + 34, 0.32, wall=(70, 90, 150), roof=NAVY)
    else:
        d.polygon([(x, y + 34 - 22), (x + 19, y + 34 - 38), (x + 38, y + 34 - 22)], outline=DIM, fill=None)
        d.rectangle([x + 4, y + 34 - 22, x + 34, y + 34], outline=DIM, width=2)
ctext(d, 320, 565, "파란 집 26채 = 착공 · 회색 74채 = 아직", F_S, INK)
cx0, cy0 = 640, 185
d.text((cx0, cy0 - 10), "올해 달력", font=F_M, fill=INK)
for m in range(12):
    r_, c_ = divmod(m, 4); x = cx0 + c_ * 80; y = cy0 + 30 + r_ * 70
    d.rounded_rectangle([x, y, x + 70, y + 60], radius=8, fill=GRAY if m < 9 else WHITE, outline=INK, width=2)
    ctext(d, x + 35, y + 16, f"{m + 1}월", F_S, WHITE if m < 9 else INK)
d.text((cx0 + 340, cy0 + 40), "지난 9달", font=F_L, fill=GRAY)
d.text((cx0 + 340, cy0 + 180), "남은 석 달", font=F_L, fill=RED)
d.rounded_rectangle([640, 440, 1310, 540], radius=14, fill=PINK)
d.text((665, 452), "남은 74채를 석 달 안에", font=F_MID, fill=RED)
d.text((665, 500), "지금까지는 한 달에 3채꼴 → 남은 석 달은 한 달에 25채꼴", font=F_S, fill=INK)
box(d, (90, 595, 1310, 690), SAND, "사장은 물량이 연말에 몰려 송구하지만 올해 목표는 달성할 수 있다는 취지로 답했다.\n착공을 실제 공사가 아니라 「착공 신고」 서류로 센다는 논쟁도 있었다", F_S, INK)
foot(d, "근거: 공부노트 §2-3(국감 제시 25.7%, 1~9월 월평균 약 1,480·남은 달 약 12,830가구 → 100채 기준으로 환산, 반올림)")
save(im, "06_lh_100homes.png")

# ---------- 07 금리 급등 7배 vs 1.2배 ----------
im, d = canvas("2021년엔 금리가 1년 반 만에 7배, 지금은 1.2배", "한국은행 기준금리 — 사장이 예로 든 2021년 하락기와 지금, 같은 눈금")
gy0, gy1 = 560, 200
def ry(r): return gy0 - (gy0 - gy1) * r / 4.0
for r in [0, 1, 2, 3, 4]:
    d.line([110, ry(r), 1300, ry(r)], fill=(228, 228, 222), width=2); d.text((60, ry(r) - 14), f"{r}%", font=F_S, fill=GRAY)
# 왼쪽: 17달 동안 0.5 → 3.5 (가파른 비탈)
L0, L1 = 150, 650
d.polygon([(L0, ry(0.5)), (L1, ry(3.5)), (L1, gy0), (L0, gy0)], fill=(245, 205, 200))
d.line([L0, ry(0.5), L1, ry(3.5)], fill=RED, width=10)
d.ellipse([L0 - 12, ry(0.5) - 12, L0 + 12, ry(0.5) + 12], fill=RED); d.ellipse([L1 - 12, ry(3.5) - 12, L1 + 12, ry(3.5) + 12], fill=RED)
d.text((L0 - 20, ry(0.5) - 50), "0.5%", font=F_M, fill=RED); d.text((L1 - 60, ry(3.5) - 52), "3.5%", font=F_M, fill=RED)
d.text((330, 250), "7배", font=F_HUGE, fill=RED); d.text((330, 335), "급등", font=F_MID, fill=RED)
ctext(d, (L0 + L1) / 2, 575, "2021.8 → 2023.1  (1년 반)", F_M, INK)
# 오른쪽: 2달 동안 2.5 → 3.0 (같은 시간 눈금이면 짧다)
R0 = 900; R1x = R0 + int((L1 - L0) * 2 / 17) + 30
d.polygon([(R0, ry(2.5)), (R1x, ry(3.0)), (R1x, gy0), (R0, gy0)], fill=(250, 228, 190))
d.line([R0, ry(2.5), R1x, ry(3.0)], fill=AMBER, width=10)
d.text((R0 - 70, ry(2.5) - 14), "2.5%", font=F_M, fill=AMBER); d.text((R1x + 14, ry(3.0) - 30), "3.0%", font=F_M, fill=AMBER)
d.text((R1x + 110, 300), "1.2배", font=F_HUGE, fill=AMBER)
ctext(d, R0 + 60, 575, "2026.7 → 8", F_M, INK)
box(d, (90, 620, 1310, 710), SAND, "2022년 집값이 크게 빠진 건 이 급등 뒤였다. 지금 오른 폭은 아직 그때만큼 가파르지 않다 — 다음 결정은 10/22", F_S, INK)
foot(d, "근거: 공부노트 §3-1·§3-3, 집값하락기 노트 §0-2(ECOS 722Y001). 가로는 시간 비례(17달 : 2달)")
save(im, "07_rate_jump.png")

# ---------- 08 최상단 금리로 내 통장 ----------
im, d = canvas("금리 최상단으로 보면 — 한 달에 21만 원 더", "5대 은행 주담대 고정금리(5년 혼합형) 상단 · 3억 원을 30년 동안 매달 같은 금액으로 갚으면(직접 계산)")
d.rounded_rectangle([110, 170, 330, 520], radius=22, fill=(60, 65, 80))
d.rounded_rectangle([135, 195, 305, 260], radius=8, fill=(200, 225, 200))
for r_ in range(4):
    for c_ in range(3): d.rounded_rectangle([140 + c_ * 56, 285 + r_ * 56, 186 + c_ * 56, 331 + r_ * 56], radius=8, fill=(120, 125, 140))
for i, (lab, rate, pay, col) in enumerate([("작년 말 상단", "6.23%", "184만 3,251원", NAVY), ("9월 15일 상단", "7.29%", "205만 4,674원", RED)]):
    x = 420 + i * 450
    d.text((x, 185), lab, font=F_M, fill=GRAY); d.text((x, 225), rate, font=F_BIG, fill=col)
    d.text((x, 310), "한 달 갚는 돈", font=F_S, fill=INK); d.text((x, 345), pay, font=F_MID, fill=col)
arrow(d, (760, 260), (840, 260), INK, 6)
d.rounded_rectangle([420, 420, 1300, 520], radius=16, fill=PINK)
d.text((450, 432), "한 달 +21만 1,423원", font=F_MID, fill=RED)
d.text((450, 480), "30년 이자 합계 3억 6,357만 원 → 4억 3,968만 원", font=F_S, fill=INK)
box(d, (90, 580, 1310, 690), SAND, "상단은 조건이 가장 불리한 사람이 받는 금리다(은행은 대부분 중간~하단에 든다고 말한다).\n같은 기간 하단도 3.93% → 4.89%로 올랐다", F_S, INK)
foot(d, "근거: 뉴시스 9/16(5대 은행 주담대 고정금리 작년 말 3.93~6.23% → 9/15 4.89~7.29%). 원리금균등 직접 계산")
save(im, "08_my_interest.png")

# ---------- R4 지금 두 기둥은 서 있나 ----------
im, d = canvas("지금, 두 기둥은 서 있나", "그림 3의 로직을 지금 숫자로 다시 세우면")
# 지붕(점선) — 「급락」
def dash(p0, p1, col, w=6, seg=22):
    import math
    (x0_, y0_), (x1_, y1_) = p0, p1; L_ = math.hypot(x1_ - x0_, y1_ - y0_); n_ = int(L_ // seg)
    for k in range(0, n_, 2):
        a_, b_ = k / n_, min(1, (k + 1) / n_)
        d.line([x0_ + (x1_ - x0_) * a_, y0_ + (y1_ - y0_) * a_, x0_ + (x1_ - x0_) * b_, y0_ + (y1_ - y0_) * b_], fill=col, width=w)
dash((330, 230), (1070, 230), RED); dash((330, 230), (700, 150), RED); dash((700, 150), (1070, 230), RED)
ctext(d, 700, 180, "급락?", F_L, RED)
# 왼쪽 기둥: 공급 — 공사 중(점선 기둥 + 2028)
lx = 330
dash((lx, 260), (lx, 470), NAVY); dash((lx + 180, 260), (lx + 180, 470), NAVY)
d.rectangle([lx, 470, lx + 180, 520], fill=NAVY)
calendar(d, lx + 55, 310, 70, 64, GREEN); ctext(d, lx + 90, 385, "2028년부터", F_M, GREEN)
ctext(d, lx + 90, 535, "공급 — 아직 공사 중", F_M, NAVY)
# 오른쪽 기둥: 금리 — 반만 선 기둥
rx = 920
d.rectangle([rx, 400, rx + 120, 520], fill=AMBER); d.rectangle([rx, 260, rx + 120, 400], outline=AMBER, width=3)
ctext(d, rx + 60, 430, "1.2배", F_MID, WHITE); ctext(d, rx + 60, 300, "그때는 7배", F_S, GRAY)
ctext(d, rx + 60, 535, "금리 — 오르는 중, 그때보다 낮다", F_M, AMBER)
d.line([200, 520, 1200, 520], fill=INK, width=4)
box(d, (90, 590, 1310, 700), SAND, "두 기둥이 다 서야 「급락」 지붕이 얹힌다. 공급 기둥은 2028년부터, 금리 기둥은 아직 그때만큼 높지 않다.\n그래서 「지금 안 사도 손해 안 본다」는 지금보다 2028년 이후를 내다본 말에 가깝다", F_S, INK)
foot(d, "근거: 그림 5·7·8·11의 숫자(공부노트 §2-2·§3-3, 집값하락기 노트 §0-1·§0-2). 예측 아님 — 10/22 금통위 뒤 금리 기둥 다시 보기")
save(im, "R4_two_pillars_now.png")
