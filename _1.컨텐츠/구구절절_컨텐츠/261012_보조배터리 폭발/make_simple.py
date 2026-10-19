# -*- coding: utf-8 -*-
"""보조배터리 글 — 일반인용 쉬운 판 v3(10/13 사용자 피드백 반영).
- 「증기에 불」→「24도에서도 불이 붙는 액체」, 「가시」→「원래 집(+쪽)으로 가려고 막을 밀고 나가는 리튬 줄 → 합선」
- 37Wh 크게, 90도의 이유를 크게, 충전량 실험은 「확률이 아니라 탈 때의 세기」, 네 가지 → 안 둘·밖 둘
- 문지기는 방패 든 사람, 마무리는 「충전은 내가 지켜볼 수 있을 때만」
숫자는 배터리_공부노트·배터리_원리노트 확인분만."""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)
F_SM = font(18); F_M = font(24, True); F_MID = font(34, True); F_BIG = font(56, True); F_L = font(28, True); F_HUGE = font(72, True)
DIM = (205, 205, 200); CATH = (70, 90, 150); ANOD = (60, 60, 60); SEP = (245, 245, 238); ELEC = (120, 190, 230)
FLAME1 = (255, 170, 40); FLAME2 = (235, 80, 40); LI = AMBER; SKIN = (230, 190, 160)
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)

def flame(d, cx, base, h):
    w = h * 0.55
    d.polygon([(cx - w / 2, base), (cx - w * 0.35, base - h * 0.55), (cx - w * 0.1, base - h * 0.35), (cx, base - h), (cx + w * 0.15, base - h * 0.45), (cx + w * 0.4, base - h * 0.6), (cx + w / 2, base)], fill=FLAME2)
    d.polygon([(cx - w * 0.25, base), (cx - w * 0.15, base - h * 0.35), (cx, base - h * 0.55), (cx + w * 0.15, base - h * 0.3), (cx + w * 0.25, base)], fill=FLAME1)
def battery(d, x, y, w, h, frac, col=GREEN, body=WHITE, outline=INK, lw=4):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=body, outline=outline, width=lw)
    d.rounded_rectangle([x + w, y + h * 0.3, x + w + 12, y + h * 0.7], radius=4, fill=outline)
    if frac > 0: d.rounded_rectangle([x + 8, y + 8, x + 8 + (w - 16) * frac, y + h - 8], radius=6, fill=col)
def plug(d, cx, cy, s=1.0, col=INK):
    d.rounded_rectangle([cx - 30 * s, cy - 22 * s, cx + 30 * s, cy + 22 * s], radius=8 * s, fill=col)
    d.rectangle([cx + 30 * s, cy - 12 * s, cx + 50 * s, cy - 6 * s], fill=col); d.rectangle([cx + 30 * s, cy + 6 * s, cx + 50 * s, cy + 12 * s], fill=col)
    d.line([cx - 30 * s, cy, cx - 70 * s, cy], fill=col, width=int(6 * s))
def clock(d, cx, cy, r, col=INK):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5, fill=WHITE)
    d.line([cx, cy, cx, cy - r * 0.6], fill=col, width=5); d.line([cx, cy, cx + r * 0.45, cy + r * 0.2], fill=col, width=5)
def thermo(d, cx, top, bottom, frac, col=RED, r=16):
    d.rounded_rectangle([cx - r, top, cx + r, bottom], radius=r, fill=WHITE, outline=INK, width=4)
    d.ellipse([cx - r * 1.7, bottom - r * 1.2, cx + r * 1.7, bottom + r * 2.2], fill=col, outline=INK, width=4)
    y0 = bottom - (bottom - top - r) * frac
    d.rounded_rectangle([cx - r * 0.55, y0, cx + r * 0.55, bottom], radius=r * 0.5, fill=col)
def beaker(d, x, y, w, h, frac, bubbles=False):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=5, fill=WHITE)
    d.rectangle([x + 5, y + h - (h - 10) * frac, x + w - 5, y + h - 5], fill=ELEC)
    if bubbles:
        for bx, by, br in [(0.3, 0.55, 9), (0.55, 0.75, 7), (0.7, 0.5, 11), (0.4, 0.85, 6)]:
            d.ellipse([x + w * bx - br, y + h * by - br, x + w * bx + br, y + h * by + br], outline=WHITE, width=3)
def check(d, cx, cy, r=16, col=GREEN):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); d.line([cx - r * 0.45, cy, cx - r * 0.1, cy + r * 0.4, cx + r * 0.5, cy - r * 0.35], fill=WHITE, width=4)
def xmark(d, cx, cy, r=16, col=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); k = r * 0.45
    d.line([cx - k, cy - k, cx + k, cy + k], fill=WHITE, width=4); d.line([cx + k, cy - k, cx - k, cy + k], fill=WHITE, width=4)
def person(d, cx, top, h, col):
    r = h * 0.17
    d.ellipse([cx - r, top, cx + r, top + 2 * r], fill=col)
    bw = h * 0.42; d.rounded_rectangle([cx - bw / 2, top + 2 * r + h * 0.05, cx + bw / 2, top + h], radius=int(bw / 2), fill=col)
def hand(d, x, y, s=1.0, col=SKIN):
    d.rounded_rectangle([x, y, x + 90 * s, y + 70 * s], radius=22 * s, fill=col)
    for i in range(4): d.rounded_rectangle([x + 8 * s + i * 21 * s, y - 40 * s, x + 24 * s + i * 21 * s, y + 10 * s], radius=8 * s, fill=col)
    d.rounded_rectangle([x - 22 * s, y + 10 * s, x + 10 * s, y + 30 * s], radius=9 * s, fill=col)
def eye(d, cx, cy, r=26, col=INK, slash=False):
    d.ellipse([cx - r * 1.6, cy - r * 0.9, cx + r * 1.6, cy + r * 0.9], outline=col, width=4)
    d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=col)
    if slash: d.line([cx - r * 1.6, cy + r, cx + r * 1.6, cy - r], fill=RED, width=6)
def dots(d, x0, y0, x1, y1, n, col=ELEC, seed=3):
    random.seed(seed)
    for _ in range(n):
        px, py = random.randint(int(x0) + 6, int(x1) - 6), random.randint(int(y0) + 6, int(y1) - 6)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
def li(d, cx, cy, r=14, col=LI): d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(200, 120, 20), width=2)
def bed(d, x, y, s=1.0):
    d.rectangle([x, y - 70 * s, x + 20 * s, y], fill=(150, 110, 80))                     # 머리판
    d.rounded_rectangle([x, y - 30 * s, x + 200 * s, y], radius=8, fill=(200, 200, 225))    # 매트리스
    d.rounded_rectangle([x + 24 * s, y - 50 * s, x + 80 * s, y - 28 * s], radius=10, fill=WHITE, outline=GRAY)
    d.rounded_rectangle([x + 70 * s, y - 42 * s, x + 200 * s, y - 20 * s], radius=10, fill=(170, 180, 215))  # 이불
def bag(d, x, y, s=1.0):
    d.polygon([(x, y), (x + 140 * s, y), (x + 125 * s, y - 100 * s), (x + 15 * s, y - 100 * s)], fill=(190, 160, 120))
    d.arc([x + 35 * s, y - 145 * s, x + 105 * s, y - 75 * s], 180, 360, fill=(150, 120, 90), width=int(8 * s))
def house(d, x, y, s=1.0):
    d.polygon([(x, y - 70 * s), (x + 60 * s, y - 120 * s), (x + 120 * s, y - 70 * s)], fill=(170, 90, 70))
    d.rectangle([x + 12 * s, y - 70 * s, x + 108 * s, y], fill=(235, 225, 205)); d.rectangle([x + 48 * s, y - 40 * s, x + 72 * s, y], fill=(150, 110, 80))
def desk(d, x, y, s=1.0):
    d.rectangle([x, y - 12 * s, x + 200 * s, y], fill=(150, 110, 80)); d.rectangle([x + 10 * s, y, x + 22 * s, y + 60 * s], fill=(150, 110, 80)); d.rectangle([x + 178 * s, y, x + 190 * s, y + 60 * s], fill=(150, 110, 80))
def pbank(d, x, y, w=90, h=50, col=(60, 65, 80)): d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=col)

# ---------- S2 샌드위치 ----------
im, d = canvas("배터리 속은 샌드위치 — 얇은 막 하나가 불을 막고 있다", "보조배터리 안 셀 한 장을 옆에서 자른 모습. 모식도, 두께 비율은 실제와 다르다")
x, w = 400, 470
d.rectangle([x, 180, x + w, 320], fill=CATH); dots(d, x, 180, x + w, 320, 110)
d.rectangle([x, 320, x + w, 352], fill=SEP, outline=GRAY, width=2)
d.rectangle([x, 352, x + w, 492], fill=ANOD); dots(d, x, 352, x + w, 492, 110, seed=5)
for lab, y in [("+ 쪽 (양극)", 250), ("얇은 막", 336), ("- 쪽 (음극)", 422)]:
    d.text((x - 20 - d.textlength(lab, font=F_M), y - 14), lab, font=F_M, fill=INK)
flame(d, x + w + 50, 270, 60); d.text((x + w + 90, 222), "뜨거워지면", font=F_S, fill=INK); d.text((x + w + 90, 250), "산소를 내놓는다", font=F_S, fill=INK)
d.text((x + w + 30, 322), "머리카락의 3분의 1 두께", font=F_S, fill=GRAY)
d.ellipse([x + w + 40, 405, x + w + 64, 429], fill=ELEC); d.text((x + w + 80, 392), "사이를 채운 액체", font=F_S, fill=INK); d.text((x + w + 80, 420), "24도에서도 불이 붙는다", font=F_M, fill=RED)
box(d, (90, 560, 1310, 690), SAND, "불에 필요한 연료(액체)·산소·열이 한 봉지 안에 다 들어 있다.\n+ 쪽과 - 쪽을 갈라놓고 있는 건 얇은 막 하나뿐이다", F_B, INK)
foot(d, "근거: 원리노트 §1-1(분리막 25μm, 전해액 인화점 24°C = 불씨가 닿으면 24°C에서도 불이 붙음, 양극 산소 방출). 모식도")
save(im, "S2_sandwich.png")

# ---------- S3 충전 = 이사 ----------
im, d = canvas("충전은 리튬을 - 쪽 방으로 이사시키는 일", "쓸 때는 원래 집(+ 쪽)으로 돌아가면서 전기를 낸다")
def rooms(x0, y0):
    d.rectangle([x0, y0, x0 + 200, y0 + 240], fill=(220, 228, 245), outline=CATH, width=4)
    d.rectangle([x0 + 200, y0, x0 + 214, y0 + 240], fill=SEP, outline=GRAY, width=2)
    d.rectangle([x0 + 214, y0, x0 + 414, y0 + 240], fill=(225, 225, 225), outline=ANOD, width=4)
    ctext(d, x0 + 100, y0 + 250, "+ 쪽 (원래 집)", F_S, CATH); ctext(d, x0 + 314, y0 + 250, "- 쪽 방", F_S, ANOD)
L = 110; T = 220
ctext(d, L + 207, 165, "평소 충전 — 빈자리에 차곡차곡", F_M, GREEN)
rooms(L, T)
for r_ in range(4):
    for c_ in range(4):
        if r_ * 4 + c_ < 12: li(d, L + 240 + c_ * 42, T + 40 + r_ * 50)
for k in range(3):
    cy = T + 60 + k * 60; li(d, L + 74, cy, col=(240, 205, 150)); arrow(d, (L + 100, cy), (L + 225, cy), INK, 4)
R = 760
ctext(d, R + 207, 165, "방이 꽉 찼는데 계속 밀어 넣으면", F_M, RED)
rooms(R, T)
for r_ in range(5):
    for c_ in range(4): li(d, R + 240 + c_ * 42, T + 26 + r_ * 47)
# 자리 없는 리튬이 줄지어 막을 밀고 원래 집으로
chain_y = T + 120
for k in range(6): li(d, R + 226 - k * 24, chain_y, 12)
arrow(d, (R + 80, chain_y - 40), (R + 20, chain_y - 40), RED, 5); d.text((R + 10, chain_y - 92), "원래 집으로!", font=F_M, fill=RED)
flame(d, R + 207, chain_y - 18, 44)
d.text((R + 20, T + 285), "자리 없는 리튬이 줄지어 막을 밀고 + 쪽으로 간다", font=F_S, fill=RED)
d.text((R + 20, T + 313), "(급할 때 · 추울 때 · 거의 다 찼을 때)", font=F_SM, fill=GRAY)
box(d, (90, 600, 1310, 690), SAND, "막이 뚫리면 + 와 - 가 바로 이어진다 = 합선. 그 자리가 순식간에 뜨거워진다.\n이 줄은 충전할 때만 생긴다", F_S, INK)
foot(d, "근거: 원리노트 §2-1(리튬 석출: 저온·급속·거의 만충 충전 때만, ZSW), §4(석출 → 분리막 관통 → 내부 단락). 비유·모식도")
save(im, "S3_charge_move.png")

# ---------- S4 에너지 = 물 ----------
im, d = canvas("보조배터리 하나에 든 에너지 — 물 1L를 31.8도 올린다", "전부 열로 바뀐다고 치면(계산)")
d.text((90, 175), "10,000mAh", font=F_HUGE, fill=INK); d.text((90, 260), "= 37Wh", font=F_HUGE, fill=GREEN)
battery(d, 110, 370, 230, 110, 1.0, GREEN); ctext(d, 225, 400, "37Wh", F_MID, WHITE)
arrow(d, (470, 420), (530, 420), INK, 6)
beaker(d, 560, 250, 180, 240, 0.85); thermo(d, 800, 250, 470, 0.4); ctext(d, 650, 505, "물 1L", F_M, INK); ctext(d, 800, 515, "+31.8도", F_M, RED)
ctext(d, 890, 360, "또는", F_S, GRAY)
beaker(d, 950, 320, 140, 170, 0.6, bubbles=True); thermo(d, 1150, 250, 470, 0.95); ctext(d, 1020, 505, "물 0.4L", F_M, INK); ctext(d, 1150, 515, "끓기 직전까지", F_M, RED)
box(d, (90, 580, 1310, 690), SAND, "실제로 불이 나면 액체와 전극까지 타서 열이 더 나온다.\n실험에선 저장된 전기의 65%만큼이 더 나왔다", F_S, INK)
foot(d, "근거: 원리노트 §2-3(10,000mAh × 3.7V = 37Wh = 133,200J ÷ 물 비열 계산), JES 2024 가속열량계 실험(18650, 27.4kJ). 모식도")
save(im, "S4_energy_water.png")

# ---------- S5 평소 충전은 미지근 ----------
im, d = canvas("평소 충전 열로는 불이 나지 않는다 — 겉은 고작 +4도", "넣은 전기 100 중 열이 되는 건 약 4. 나머지는 배터리 안에 저장된다")
d.rounded_rectangle([140, 300, 420, 450], radius=22, fill=(60, 65, 80)); plug(d, 520, 375, 1.1, INK)
thermo(d, 280, 180, 280, 0.3, GREEN, 12); ctext(d, 340, 200, "+4도", F_MID, GREEN)
ctext(d, 280, 470, "10W로 충전 중", F_S, GRAY)
sx = 760
d.line([sx, 180, sx, 540], fill=INK, width=6)
for t, lab, col, y in [(30, "충전 중 손에 쥐면 미지근", GREEN, 510), (45, "충전해도 되는 상한", GREEN, 440), (90, "배터리가 스스로 달아오르기 시작", RED, 210)]:
    d.line([sx - 18, y, sx + 18, y], fill=col, width=6); d.text((sx - 120, y - 20), f"{t}도", font=F_L, fill=col); d.text((sx + 40, y - 14), lab, font=F_S, fill=INK)
d.rounded_rectangle([sx + 40, 260, sx + 560, 400], radius=12, fill=SAND)
d.text((sx + 60, 275), "이 사이는 평소 충전 열로 못 건넌다", font=F_M, fill=INK)
d.text((sx + 60, 318), "건너게 하는 건 「합선」", font=F_L, fill=RED)
d.text((sx + 60, 360), "막이 뚫려 + 와 - 가 바로 이어지는 것", font=F_S, fill=INK)
arrow(d, (sx + 20, 430), (sx + 20, 225), DIM, 4)
box(d, (90, 590, 1310, 690), SAND, "충전이 뜨거워서 불이 나는 게 아니다.\n충전 중에 막이 뚫려서 불이 난다", F_B, INK)
foot(d, "근거: 원리노트 §3-2(1C 충전 열량계 실측 3.7%), §3-4(10W 충전 겉 +4.4°C 계산), JEITA 45°C, 음극 보호막 분해 약 90°C")
save(im, "S5_charge_is_warm.png")

# ---------- S6 온도 네 칸 + 90도의 이유 ----------
im, d = canvas("온도로 보면 — 90도부터 배터리가 스스로 달아오른다", "배터리 실험·표준에서 나온 온도 네 개만 골랐다")
tx, top, bot = 200, 150, 470
marks = [(45, "정상 충전의 상한", GREEN), (90, "- 쪽 보호막이 무너지며 스스로 열을 낸다", AMBER), (130, "얇은 막이 녹아 + 와 - 가 닿는다(합선)", RED), (759, "가장 뜨거울 때 (실험)", RED)]
n = len(marks)
d.rounded_rectangle([tx - 22, top, tx + 22, bot], radius=22, fill=WHITE, outline=INK, width=4)
d.ellipse([tx - 42, bot - 28, tx + 42, bot + 56], fill=RED, outline=INK, width=4)
ys = [bot - 60 - (bot - top - 90) * i / (n - 1) for i in range(n)]
for i in range(n - 1, -1, -1): d.rounded_rectangle([tx - 12, ys[i], tx + 12, bot], radius=10, fill=marks[i][2])
for (t, lab, col), y in zip(marks, ys):
    d.line([tx + 22, y, tx + 60, y], fill=INK, width=4)
    d.text((tx + 75, y - 22), f"{t}도", font=F_MID, fill=col); d.text((tx + 210, y - 14), lab, font=F_B, fill=INK)
flame(d, tx + 590, ys[3] + 25, 60)
# 왜 90도 — 크게
d.rounded_rectangle([90, 545, 1310, 700], radius=16, fill=SAND)
d.text((120, 558), "왜 90도인가", font=F_L, fill=AMBER)
d.text((120, 600), "- 쪽 표면을 덮은 얇은 보호막이 이 온도쯤부터 무너지면서 열을 낸다.", font=F_B, fill=INK)
d.text((120, 638), "그 열이 온도를 더 올리고, 더 올라간 온도가 막을 더 무너뜨린다 — 밖에서 불을 대지 않아도 스스로 커지는 첫 계단.", font=F_S, fill=INK)
# 오른쪽 계단 그림(악순환)
cyc = [(1120, 280, "열"), (1230, 420, "막 분해"), (1010, 420, "더 큰 열")]
for i, (cx, cy, lab) in enumerate(cyc):
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=[AMBER, FLAME2, RED][i]); ctext(d, cx, cy - 14, lab, F_M, WHITE)
arrow(d, (1160, 318), (1200, 372), INK, 5); arrow(d, (1176, 436), (1066, 436), INK, 5); arrow(d, (1036, 372), (1078, 318), INK, 5)
foot(d, "근거: 원리노트 §4-1(JEITA 45°C, SEI 보호막 분해 약 90°C, 분리막 셧다운 130°C, 18650 최고 759.61°C), §0-4. 눈금 간격은 모식")
save(im, "S6_four_temps.png")

# ---------- S7 꽉 찬 배터리 ----------
im, d = canvas("같은 사고라도 꽉 찬 배터리가 더 쉽게, 더 세게 탄다", "같은 배터리를 오븐처럼 일부러 계속 가열한 실험. 「불이 날 확률」이 아니라 「불붙으면 어떻게 타나」")
data = [(3, None, 300), (33, 236, 566), (66, 216, 713), (100, 203, 759)]
for i, (soc, t2, tmax) in enumerate(data):
    x = 140 + i * 300
    battery(d, x, 450, 170, 90, soc / 100, GREEN if soc < 100 else AMBER); ctext(d, x + 85, 550, f"충전 {soc}%", F_M, INK)
    if t2:
        fh = tmax / 759 * 200; flame(d, x + 85, 440, fh)
        ctext(d, x + 85, 440 - fh - 64, f"최고 {tmax}도", F_M, RED); ctext(d, x + 85, 440 - fh - 32, f"{t2}도에서 시작", F_SM, RED)
    else:
        d.ellipse([x + 55, 380, x + 115, 440], outline=GRAY, width=4); d.line([x + 60, 385, x + 110, 435], fill=GRAY, width=4)
        ctext(d, x + 85, 335, "타지 않음", F_M, GRAY)
box(d, (90, 595, 1310, 690), SAND, "33%·66%라서 평소에 불이 잘 나는 게 아니다. 사고가 났을 때의 차이다 —\n꽉 찰수록 더 낮은 온도에서 시작해 더 뜨겁게 탄다. 충전은 매번 배터리를 그 꼭대기로 데려간다", F_S, INK)
foot(d, "근거: 원리노트 §4-1(JES 2024 가속열량계: 충전 3/33/66/100% → 폭주 없음/236/216/203°C, 최고 300/566/713/759°C)")
save(im, "S7_full_burns.png")

# ---------- S8 안 둘 · 밖 둘 ----------
im, d = canvas("충전 중 사고가 많은 이유 — 안에서 생기고, 밖에서 못 본다", "소방청: 리튬이온 배터리 화재(킥보드 등 포함) 51% · 일본 NITE: 보조배터리 사고 41%가 충전 중")
d.rounded_rectangle([90, 170, 560, 460], radius=18, fill=WHITE, outline=RED, width=4); ctext(d, 325, 185, "배터리 안 — 충전이 만드는 위험", F_M, RED)
battery(d, 150, 260, 200, 100, 1.0, AMBER)
for k in range(5): li(d, 380 + k * 26, 310, 11)
ctext(d, 325, 390, "꽉 찬 상태에서", F_S, INK); ctext(d, 325, 420, "자리 없는 리튬이 막을 민다", F_S, INK)
ctext(d, 625, 285, "+", F_BIG, GRAY)
d.rounded_rectangle([680, 170, 1080, 460], radius=18, fill=WHITE, outline=BLUE, width=4); ctext(d, 880, 185, "배터리 밖 — 키우고 못 본다", F_M, BLUE)
plug(d, 790, 290, 1.1, BLUE); clock(d, 960, 290, 45, GRAY)
ctext(d, 875, 390, "충전기는 계속 밀어 넣고", F_S, INK); ctext(d, 875, 420, "사람은 자리를 비운다", F_S, INK)
ctext(d, 1115, 280, "=", F_BIG, GRAY)
d.ellipse([1150, 220, 1320, 390], fill=WHITE, outline=RED, width=6); ctext(d, 1235, 265, "51%", F_BIG, RED); ctext(d, 1235, 335, "충전 중", F_S, INK)
box(d, (90, 510, 1310, 650), SAND, "충전이 뜨거워서가 아니다.\n위험이 생기는 순간과 아무도 안 보는 순간이 「충전 중」에 겹친다", F_B, INK)
foot(d, "근거: 소방청 2019~2023 리튬이온 화재 612건 중 「과충전 상태」 312건(보조배터리 따로 못 셈·정의 미확인), NITE 150건 중 41%")
save(im, "S8_inside_outside.png")

# ---------- S9 방패 든 문지기 ----------
im, d = canvas("보호회로는 방패 든 문지기 — 밖에서 오는 건 막고, 안은 못 본다", "보조배터리 안 작은 기판이 전압·전류·온도를 지켜본다")
threats = [("충전기가 이상할 때", 250), ("단자에 동전·열쇠가 닿을 때", 360), ("너무 뜨거울 때 충전", 470)]
ctext(d, 300, 175, "밖에서 오는 위험 — 막는다", F_M, GREEN)
for lab, y in threats:
    d.text((90, y - 14), lab, font=F_S, fill=INK); arrow(d, (410, y), (540, y), RED, 5)
# 사람 + 큰 방패
person(d, 670, 230, 250, GREEN)
d.line([650, 340, 610, 350], fill=GREEN, width=14)
d.polygon([(550, 250), (630, 250), (630, 420), (590, 475), (550, 420)], fill=(220, 240, 228), outline=GREEN)
d.polygon([(550, 250), (630, 250), (630, 420), (590, 475), (550, 420)], outline=GREEN)
d.line([590, 268, 590, 450], fill=GREEN, width=5); d.line([560, 330, 620, 330], fill=GREEN, width=5)
ctext(d, 650, 500, "보호회로", F_M, GREEN)
d.rounded_rectangle([780, 210, 1300, 520], radius=20, fill=WHITE, outline=GRAY, width=5)
ctext(d, 1040, 175, "배터리 안에서 생기는 위험 — 못 본다", F_M, GRAY)
for k in range(5): li(d, 840 + k * 26, 300, 11, col=DIM)
d.text((830, 330), "막을 미는 리튬 줄", font=F_S, fill=GRAY)
d.ellipse([1075, 285, 1105, 315], fill=GRAY); d.text((1035, 330), "금속 부스러기", font=F_S, fill=GRAY)
d.line([820, 420, 1260, 420], fill=GRAY, width=6); d.ellipse([1010, 412, 1026, 428], fill=WHITE, outline=GRAY, width=3); d.text((920, 440), "막에 난 바늘구멍", font=F_S, fill=GRAY)
eye(d, 1225, 460, 22, GRAY, slash=True)
box(d, (90, 590, 1310, 690), SAND, "원통형 배터리엔 압력으로 스스로 끊는 장치가 따로 있다.\n보조배터리 대부분(납작한 파우치형)엔 이 문지기 하나뿐이다", F_S, INK)
foot(d, "근거: 원리노트 §5(보호 IC 데이터시트: 과충전 4.25V 차단·과전류 차단, JEITA 충전 온도), §1-2(파우치엔 CID·벤트 없음), 경산성 2016")
save(im, "S9_gatekeeper.png")

# ---------- S10 인증은 사진 한 장 ----------
im, d = canvas("인증은 출시 때 찍은 사진 한 장", "국내외 안전 표준은 모두 「새 제품」을 시험한다")
fx0, fy0, fx1, fy1 = 130, 200, 560, 470
for (ax, ay, sx_, sy_) in [(fx0, fy0, 1, 1), (fx1, fy0, -1, 1), (fx0, fy1, 1, -1), (fx1, fy1, -1, -1)]:
    d.line([ax, ay, ax + 60 * sx_, ay], fill=INK, width=6); d.line([ax, ay, ax, ay + 60 * sy_], fill=INK, width=6)
battery(d, 220, 290, 230, 110, 1.0, GREEN); check(d, 500, 250, 26)
ctext(d, 345, 490, "출시 때 새 제품으로 시험 — 통과", F_M, GREEN)
battery(d, 820, 220, 230, 110, 0.55, DIM, body=(240, 240, 235), outline=GRAY); ctext(d, 1160, 245, "?", F_BIG, GRAY)
ctext(d, 960, 350, "3년 뒤 · 떨어뜨린 뒤 · 싼 셀", F_M, GRAY)
for k in range(13):
    x = 760 + k * 42; d.rounded_rectangle([x, 392, x + 32, 422], radius=6, fill=RED if k == 6 else DIM)
d.text((760, 435), "싼·위조 셀은 13개 중 1개 꼴로 속에 결함, 정품은 0", font=F_S, fill=INK)
d.text((760, 465), "(CT 장비 회사 연구 — 이해당사자 자료)", font=F_SM, fill=GRAY)
d.line([700, 200, 700, 540], fill=DIM, width=3)
box(d, (90, 580, 1310, 690), SAND, "KC를 받고도 리콜 중이던 모델이 비행기 안에서 불났다(2026.9.24).\n인증은 그날 찍은 사진 한 장이다", F_S, INK)
foot(d, "근거: 공부노트 §2-3(국제·국내 표준 모두 새 셀 시험, IEC 「제조 6개월 이내 셀」), §1-1(에어서울), Lumafield 2025(1,054개 중 33개)")
save(im, "S10_certified_photo.png")

# ---------- S11 규칙 ----------
im, d = canvas("규칙은 이렇게 바뀌었다 — 선반에서 손으로, 5개에서 2개로", "국토교통부 시행일 기준")
cols = [(240, "2025.3.1", "선반에 두지 말고 몸에", BLUE), (700, "2026.4.20", "1인 2개, 기내 충전 금지", AMBER), (1160, "2026.10.2", "리콜 모델은 아예 못 탄다", RED)]
d.line([120, 420, 1280, 420], fill=GRAY, width=6)
for cx, dt, lab, col in cols:
    d.ellipse([cx - 18, 402, cx + 18, 438], fill=col); ctext(d, cx, 455, dt, F_M, col); ctext(d, cx, 495, lab, F_S, INK)
d.rounded_rectangle([120, 200, 260, 250], radius=10, fill=(120, 125, 135)); arrow(d, (270, 225), (320, 225), INK, 5); hand(d, 340, 230, 0.8)
for k in range(5): battery(d, 560 + k * 58, 200, 44, 28, 1, DIM)
for k in range(2): battery(d, 620 + k * 58, 260, 44, 28, 1, AMBER)
plug(d, 800, 340, 0.9, GRAY); xmark(d, 810, 340, 20, RED); d.text((860, 326), "충전 금지", font=F_SM, fill=GRAY)
battery(d, 1090, 230, 130, 70, 1, DIM); xmark(d, 1240, 225, 26, RED)
box(d, (90, 570, 1310, 690), SAND, "규칙은 비행기 안을 바꿨다.\n하지만 소방청이 센 배터리 화재는 절반이 「충전 중」이었다", F_B, INK)
foot(d, "근거: 공부노트 §1-3(국토부 2025.3.1·2026.4.20 시행, 국적사 공문 10.2), §1-2(소방청 612건 중 312건, 공항 적발 1년 433,051건)")
save(im, "S11_rules.png")

# ---------- S12 할 일: 지켜볼 수 있을 때만 ----------
im, d = canvas("오늘 할 일 하나 — 충전은 내가 지켜볼 수 있을 때만", "비행기 규칙이 바꾼 건 「선반 → 손」. 같은 원리를 집에서도")
# 왼쪽 ✕ 세 장면
ctext(d, 340, 165, "이럴 때는 꽂아 두지 않기", F_M, RED)
bed(d, 110, 290, 1.0); pbank(d, 130, 200, 60, 32); xmark(d, 330, 220, 20); d.text((360, 205), "잠든 사이 침대 옆", font=F_S, fill=INK)
bag(d, 120, 420, 0.8); pbank(d, 150, 360, 60, 32); xmark(d, 330, 360, 20); d.text((360, 345), "이불·가방 속", font=F_S, fill=INK)
house(d, 120, 530, 0.8); xmark(d, 330, 490, 20); d.text((360, 475), "집을 비울 때", font=F_S, fill=INK)
d.line([700, 170, 700, 560], fill=DIM, width=3)
# 오른쪽 ✓ 세 장면
ctext(d, 1010, 165, "이렇게", F_M, GREEN)
eye(d, 820, 225, 22, INK); pbank(d, 880, 205, 70, 40); check(d, 980, 225, 20); d.text((1010, 210), "깨어 있을 때 눈앞에서", font=F_S, fill=INK)
desk(d, 790, 380, 0.8); pbank(d, 820, 330, 70, 36); check(d, 980, 355, 20); d.text((1010, 340), "딱딱한 책상 위", font=F_S, fill=INK)
pbank(d, 800, 470, 70, 40, GREEN); arrow(d, (880, 490), (940, 490), INK, 4); check(d, 980, 490, 20); d.text((1010, 475), "다 차면 뽑기", font=F_S, fill=INK)
box(d, (90, 590, 1310, 690), SAND, "청주공항 배터리는 손 안이라 바로 껐다. 잠든 사이 침대 옆에서 충전하던 배터리 화재로는 두 사람이 숨졌다.\n불을 다 막을 순 없어도, 일찍 보면 작게 끝난다", F_S, INK)
foot(d, "근거: 공부노트 §1-1(청주 10.10 손 안, 관악구 2025.11 침대 옆 충전 중·2명 사망), 원리노트 §3-4(이불 속 +10°C, 폰 시험). 모식도")
save(im, "S12_watch_charging.png")
print("done_simple_v3")
