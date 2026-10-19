# -*- coding: utf-8 -*-
"""보조배터리 글 — 그림이 설명하는 도해 17장. 글자는 라벨만. 숫자는 배터리_공부노트·배터리_원리노트 확인분."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
from PIL import Image, ImageDraw
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)
F_SM = font(18); F_M = font(24, True); F_MID = font(34, True); F_BIG = font(52, True)
NAVY = (40, 60, 110); ORANGE = (235, 120, 40); DIM = (205, 205, 200); CU = (200, 120, 60); AL = (170, 175, 185)
CATH = (70, 90, 150); ANOD = (60, 60, 60); SEP = (240, 240, 235); ELEC = (120, 190, 230); FLAME1 = (255, 170, 40); FLAME2 = (235, 80, 40)
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)

# ---------- 픽토그램 ----------
def flame(d, cx, base, h, c1=FLAME2, c2=FLAME1):
    w = h * 0.55
    d.polygon([(cx - w / 2, base), (cx - w * 0.35, base - h * 0.55), (cx - w * 0.1, base - h * 0.35), (cx, base - h), (cx + w * 0.15, base - h * 0.45), (cx + w * 0.4, base - h * 0.6), (cx + w / 2, base)], fill=c1)
    d.polygon([(cx - w * 0.25, base), (cx - w * 0.15, base - h * 0.35), (cx, base - h * 0.55), (cx + w * 0.15, base - h * 0.3), (cx + w * 0.25, base)], fill=c2)
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
def beaker(d, x, y, w, h, fill_frac, water=ELEC, bubbles=False):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=5, fill=WHITE)
    d.rectangle([x + 5, y + h - (h - 10) * fill_frac, x + w - 5, y + h - 5], fill=water)
    if bubbles:
        for i, (bx, by, br) in enumerate([(0.3, 0.35, 9), (0.55, 0.6, 7), (0.7, 0.3, 11), (0.4, 0.75, 6), (0.8, 0.7, 8)]):
            d.ellipse([x + w * bx - br, y + h * by - br, x + w * bx + br, y + h * by + br], outline=WHITE, width=3)
def thermo(d, cx, top, bottom, frac, col=RED, r=16):
    d.rounded_rectangle([cx - r, top, cx + r, bottom], radius=r, fill=WHITE, outline=INK, width=4)
    d.ellipse([cx - r * 1.7, bottom - r * 1.2, cx + r * 1.7, bottom + r * 2.2], fill=col, outline=INK, width=4)
    y0 = bottom - (bottom - top - r) * frac
    d.rounded_rectangle([cx - r * 0.55, y0, cx + r * 0.55, bottom], radius=r * 0.5, fill=col)
def needle(d, x, y, h, col=INK):
    d.polygon([(x - 6, y), (x + 6, y), (x, y - h)], fill=col)
def eye_x(d, cx, cy, r=26):
    d.ellipse([cx - r * 1.6, cy - r * 0.9, cx + r * 1.6, cy + r * 0.9], outline=GRAY, width=4)
    d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=GRAY)
    d.line([cx - r * 1.6, cy + r, cx + r * 1.6, cy - r], fill=RED, width=6)
def shield(d, cx, cy, s, col=GREEN):
    d.polygon([(cx - s, cy - s * 0.9), (cx + s, cy - s * 0.9), (cx + s, cy + s * 0.2), (cx, cy + s), (cx - s, cy + s * 0.2)], fill=col)
def gauge(d, cx, cy, r, frac, col, label, val):
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=LIGHT)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 180 + 180 * frac, fill=col)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=WHITE)
    ctext(d, cx, cy - 14, val, F_M, col); ctext(d, cx, cy + r * 0.3, label, F_SM, GRAY)
def hand(d, x, y, s=1.0, col=(230, 190, 160)):
    d.rounded_rectangle([x, y, x + 90 * s, y + 70 * s], radius=22 * s, fill=col)
    for i in range(4): d.rounded_rectangle([x + 8 * s + i * 21 * s, y - 40 * s, x + 24 * s + i * 21 * s, y + 10 * s], radius=8 * s, fill=col)
    d.rounded_rectangle([x - 22 * s, y + 10 * s, x + 10 * s, y + 30 * s], radius=9 * s, fill=col)
def powerbank(d, x, y, w, h, col=(60, 65, 80)):
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=col)
    d.rounded_rectangle([x + w - 34, y + h * 0.35, x + w - 14, y + h * 0.65], radius=4, fill=(30, 30, 30))
def layer_stack(d, x, y, w, layers):
    """layers: list of (height, color, label_left, label_right)"""
    cy = y
    for hgt, col, ll, lr in layers:
        d.rectangle([x, cy, x + w, cy + hgt], fill=col, outline=(90, 90, 90), width=2)
        if ll: d.text((x - 16 - d.textlength(ll, font=F_S), cy + hgt / 2 - 13), ll, font=F_S, fill=INK)
        if lr: d.text((x + w + 16, cy + hgt / 2 - 13), lr, font=F_S, fill=GRAY)
        cy += hgt
    return cy

# ---------- P1 셀 단면 ----------
im, d = canvas("배터리 한 장의 속 — 다섯 층, 그 사이에 불붙는 액체", "두께는 공급사 규격 대표값. 분리막 25μm는 머리카락(약 70μm)의 3분의 1")
end = layer_stack(d, 420, 170, 560, [(26, AL, "알루미늄 박", "15μm · 전자 길"), (120, CATH, "양극 (리튬이 사는 집 ①)", "뜨거워지면 산소를 내놓음"),
                                      (34, SEP, "분리막", "25μm · 130°C에 녹음"), (120, ANOD, "음극 (흑연, 집 ②)", "표면 막이 90°C부터 분해"), (20, CU, "구리 박", "10μm · 1,085°C에 녹음")])
# 전해액 점
import random; random.seed(3)
for _ in range(260):
    px, py = random.randint(430, 970), random.randint(200, 460)
    if 196 <= py <= 316 or 350 <= py <= 470: d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=ELEC)
d.ellipse([440, 213, 480, 253], fill=ELEC); ctext(d, 460, 258, "전해액", F_SM, INK)
# 머리카락 비교
d.rectangle([1100, 600, 1104, 690], fill=(90, 70, 50)); d.rectangle([1130, 600, 1200, 690], fill=(90, 70, 50))
ctext(d, 1165, 560, "머리카락 약 70μm", F_SM, GRAY); d.rectangle([1250, 600, 1275, 690], fill=SEP, outline=INK, width=2); ctext(d, 1262, 695, "분리막 25μm", F_SM, INK)
box(d, (90, 560, 1000, 690), SAND, "전해액 인화점 24°C — 실온에서 증기가 붙는다.\n양극이 내놓는 산소 + 이 증기 + 열 = 바깥 공기 없이도 타는 불", F_S, INK)
foot(d, "근거: 원리노트 §1-1(Celgard 2325 25μm·PE 130°C 셧다운·Al 15μm·Cu 10μm·전해액 인화점 24°C KIT), Finegan 2015(구리 용융). 모식도")
save(im, "P1_cell_layers.png")

# ---------- P2 충전·방전 ----------
im, d = canvas("이온은 안으로, 전자는 밖으로 — 충전은 방전을 거꾸로 돌린 것", "흔들의자 반응. 충전 때 흑연이 못 받아들인 리튬은 표면에 금속으로 쌓인다(석출)")
def half_cell(d, x, y, title, charging):
    ctext(d, x + 170, y + 300, title, F_M, INK)
    d.rectangle([x, y, x + 110, y + 260], fill=CATH); d.rectangle([x + 110, y, x + 230, y + 260], fill=ELEC); d.rectangle([x + 165, y, x + 175, y + 260], fill=SEP)
    d.rectangle([x + 230, y, x + 340, y + 260], fill=ANOD)
    ctext(d, x + 55, y + 268, "양극", F_SM, INK); ctext(d, x + 285, y + 268, "음극(흑연)", F_SM, INK)
    for k in range(4):
        yy = y + 40 + k * 55
        if charging: arrow(d, (x + 120, yy), (x + 220, yy), WHITE, 5)
        else: arrow(d, (x + 220, yy), (x + 120, yy), WHITE, 5)
        d.ellipse([x + 158, yy - 12, x + 184, yy + 12], fill=AMBER); ctext(d, x + 171, yy - 9, "Li+", font(14, True), INK)
    # 외부 회로
    d.line([x + 55, y, x + 55, y - 70, x + 285, y - 70, x + 285, y], fill=INK, width=5)
    for k in range(3):
        ex = x + 90 + k * 65
        if charging: arrow(d, (ex + 30, y - 70), (ex, y - 70), BLUE, 5)
        else: arrow(d, (ex, y - 70), (ex + 30, y - 70), BLUE, 5)
    ctext(d, x + 170, y - 100, "e- 바깥 회로", F_SM, BLUE)
half_cell(d, 110, 260, "방전 — 폰으로 나감", False); half_cell(d, 760, 260, "충전 — 충전기가 밀어 넣음", True)
d.rounded_rectangle([520, 150, 610, 210], radius=10, fill=INK); ctext(d, 565, 168, "폰", F_M, WHITE)
plug(d, 1240, 180, 1.0, INK)
# 석출 바늘
for k, (nx, nh) in enumerate([(990, 40), (1005, 60), (1020, 35), (1035, 55)]): needle(d, nx, 410 + k * 20, nh, AMBER)
d.text((1110, 440), "석출", font=F_M, fill=AMBER); d.text((1110, 470), "춥거나·빠르거나·거의 찼을 때", font=F_SM, fill=AMBER)
box(d, (90, 600, 1310, 690), SAND, "석출은 충전 때만 생긴다. 쌓인 금속이 25μm 분리막을 뚫으면 내부 단락 — 「충전 중」이 위험한 첫 번째 원리", F_S, INK)
foot(d, "근거: 원리노트 §2-1(인터칼레이션·ZSW Waldmann 석출 조건). 만충 4.2V · 공칭 3.7V · 방전 종지 3.0V. 모식도")
save(im, "P2_charge_discharge.png")

# ---------- P3 37Wh ----------
im, d = canvas("10,000mAh 하나에 든 에너지 — 37Wh, 물 1L를 31.8도 올린다", "37Wh × 3,600 = 133,200J ÷ 물 비열 4,186J/(kg·K). 손실 0 가정, 전기에너지만(계산)")
battery(d, 110, 300, 260, 130, 1.0, GREEN); ctext(d, 240, 340, "37Wh", F_MID, WHITE); ctext(d, 240, 445, "10,000mAh × 3.7V", F_SM, GRAY)
arrow(d, (400, 365), (480, 365), INK, 6)
beaker(d, 520, 220, 200, 260, 0.85); thermo(d, 780, 220, 450, 0.4); ctext(d, 620, 490, "물 1L", F_M, INK); ctext(d, 780, 500, "+31.8°C", F_M, RED)
ctext(d, 660, 180, "또는", F_SM, GRAY)
beaker(d, 920, 300, 150, 180, 0.6, bubbles=True); thermo(d, 1120, 220, 450, 0.95); ctext(d, 995, 490, "물 0.4L", F_M, INK); ctext(d, 1120, 500, "20 → 100°C", F_M, RED)
box(d, (90, 570, 1310, 690), SAND, "사고 때 실제로 나오는 열은 이보다 많다 — 전해액·전극이 타는 화학열이 보태진다.\n18650 한 개(11.7Wh) 실측: 열폭주에서 27.4kJ, 저장 전기에너지의 65%가 더 나왔다", F_S, INK)
foot(d, "근거: 원리노트 §2-3(계산), JES 2024 ARC 실측(3.25Ah NCA, 100% SOC 27.4kJ). 비커·온도계는 모식도")
save(im, "P3_energy_water.png")

# ---------- P4 발열식 세 항 ----------
im, d = canvas("배터리에서 열이 나는 세 길 — 평소엔 두 개, 폭주 땐 세 번째", "Bernardi 1985 열수지. 막대는 10,000mAh 1C 기준 계산값, 세 번째는 Liu 2018 실측(W/g)")
base = 560
vb = [(250, 1.25, "줄열 I²R", "1.25W", NAVY), (520, 0.3, "엔트로피열", "0.3W", BLUE)]
for x, v, lab, val, col in vb:
    hgt = v * 200; d.rounded_rectangle([x, base - hgt, x + 150, base], radius=10, fill=col); ctext(d, x + 75, base - hgt - 34, val, F_M, col); ctext(d, x + 75, base + 10, lab, F_S, INK)
d.text((520, 610), "(흡열일 때도 있음)", font=F_SM, fill=GRAY)
# 세 번째: 그래프 밖으로 솟는 불
d.rounded_rectangle([860, base - 6, 1010, base], radius=3, fill=DIM); ctext(d, 935, base + 10, "부반응열", F_S, INK); d.text((860, 610), "평소엔 거의 0", font=F_SM, fill=GRAY)
flame(d, 1180, base, 330); ctext(d, 1180, 165, "87.8 W/g", F_M, RED); ctext(d, 1180, 198, "열폭주 때", F_SM, RED); d.text((1090, 610), "그래프 밖", font=F_SM, fill=RED)
d.line([200, base, 1300, base], fill=GRAY, width=4)
d.text((200, 160), "Q = I(U - V)  -  I·T·dU/dT  +  Q_side", font=F_M, fill=INK)
foot(d, "근거: 원리노트 §3-1(Bernardi·Pawlikowski·Newman 1985 JES 132; 줄열 1.25W·엔트로피열 0.3W 계산; Liu 2018 Joule 87.8W/g). 모식도")
save(im, "P4_three_heats.png")

# ---------- P5 몇 %가 열 ----------
im, d = canvas("들어간 에너지의 몇 %가 열이 되나 — 한 자릿수", "NMC622 코인셀 열량계 실측(충전 0.5C·1C·2C) · LFP 26650 실측(방전 5.8C). 나머지는 저장 → 폭주 때 한꺼번에")
rows = [("충전 0.5C", 2.1), ("충전 1C", 3.7), ("충전 2C", 5.8), ("방전 5.8C", 8.0)]
for i, (lab, pct) in enumerate(rows):
    x = 110 + i * 300
    battery(d, x, 230, 220, 110, 1.0, DIM)
    d.rounded_rectangle([x + 8 + (220 - 16) * (1 - pct / 100), 238, x + 8 + 204, 332], radius=6, fill=RED)
    ctext(d, x + 110, 350, lab, F_S, INK); ctext(d, x + 110, 380, f"열 {pct}%", F_M, RED); ctext(d, x + 110, 412, "저장 " + f"{100 - pct:.1f}%", F_SM, GRAY)
arrow(d, (700, 480), (700, 540), GRAY, 6)
battery(d, 480, 560, 440, 110, 1.0, RED); flame(d, 700, 560, 90); ctext(d, 700, 600, "열폭주: 저장분이 한꺼번에 열로", F_M, WHITE)
foot(d, "근거: 원리노트 §3-2(Zhao 2020 NMC622 23.59·41.60·65.62J ÷ 1,132J; Drake 2015 LFP 8%). 비율은 계산값")
save(im, "P5_heat_share.png")

# ---------- P6 C율 제곱 ----------
im, d = canvas("빨리 넣을수록 열은 제곱으로 — 0.5C 1.8, 1C 5.8, 2C 22.4mW", "NMC622 코인셀 확산 발열 항(Zhao 2020). C율 2배 → 열 약 4배")
ox, oy, ex, ty = 200, 620, 1200, 170
d.line([ox, oy, ex, oy], fill=INK, width=4); d.line([ox, oy, ox, ty], fill=INK, width=4)
def X(c): return ox + (ex - ox) * c / 2.3
def Y(mw): return oy - (oy - ty) * mw / 25
pts = [(X(c), Y(5.6 * c * c)) for c in [i / 20 for i in range(0, 47)]]
d.line(pts, fill=RED, width=5)
for c, mw in [(0.5, 1.8), (1, 5.8), (2, 22.4)]:
    d.ellipse([X(c) - 12, Y(mw) - 12, X(c) + 12, Y(mw) + 12], fill=RED, outline=WHITE, width=3)
    ctext(d, X(c), Y(mw) - 48, f"{mw}mW", F_M, RED); ctext(d, X(c), oy + 12, f"{c}C", F_S, INK)
d.text((ox - 150, ty - 10), "열(mW)", font=F_S, fill=GRAY); d.text((ex - 40, oy + 40), "충전 속도(C)", font=F_S, fill=GRAY)
d.text((330, 250), "보조배터리 본체 충전(10W)은 약 0.23C →", font=F_S, fill=GRAY); d.text((330, 280), "셀 줄열 0.07W, 기판 손실 합쳐 약 1W, 표면 +4°C(계산)", font=F_S, fill=GRAY)
foot(d, "근거: 원리노트 §3-1(Zhao 2020 확산 항 1.8→5.8→22.4mW), §3-4(10W 입력 0.23C·+4.4°C 계산). 곡선은 I² 비례 모식")
save(im, "P6_crate_square.png")

# ---------- P7 온도계 ----------
im, d = canvas("온도계 하나로 보는 전부 — 정상은 45도까지, 불은 90도부터", "전부 실측·표준·물성 확정치. 눈금 간격은 모식(비례 아님)")
tx, top, bot = 330, 150, 700
marks = [(30, "정상 충전 표면 (약 30°C, 보조배터리 +4°C)", GREEN), (45, "정상 충전 상한 (JEITA)", GREEN), (72, "100% 충전 셀, 스스로 열 내기 시작", AMBER), (90, "SEI 막 분해 — 불의 시작", AMBER),
         (130, "분리막 녹아 막힘 = 내부 단락", RED), (165, "분리막 붕괴", RED), (203, "열폭주 (100% 충전 18650)", RED), (274, "양극 산소 반응 피크 87.8W/g", RED), (759, "최고 온도 (실측)", RED), (1085, "구리 녹음 — CT로 확인", RED)]
# 세로 위치는 등간격(모식)
n = len(marks)
d.rounded_rectangle([tx - 22, top, tx + 22, bot], radius=22, fill=WHITE, outline=INK, width=4)
d.ellipse([tx - 42, bot - 30, tx + 42, bot + 54], fill=RED, outline=INK, width=4)
for i in range(n - 1, -1, -1):
    t, lab, col = marks[i]
    y = bot - 30 - (bot - top - 50) * (i + 0.5) / n
    d.rounded_rectangle([tx - 12, y, tx + 12, bot], radius=10, fill=col)
for i, (t, lab, col) in enumerate(marks):
    y = bot - 30 - (bot - top - 50) * (i + 0.5) / n
    d.line([tx + 22, y, tx + 60, y], fill=INK, width=3)
    d.text((tx + 70, y - 16), f"{t:,}°C", font=F_M, fill=col); d.text((tx + 200, y - 13), lab, font=F_S, fill=INK)
d.rounded_rectangle([tx - 200, 420, tx - 60, 470], radius=8, fill=SAND); ctext(d, tx - 130, 432, "45도 → 90도 사이", F_SM, INK)
d.text((tx - 290, 480), "이 빈 구간을 건너는 건\n열이 아니라 「단락」", font=F_S, fill=INK)
foot(d, "근거: 원리노트 §4-1(JEITA 45, 자가발열 72.67, SEI 90, 셧다운 130, 붕괴 165, T2 203.29, 산소 274.2°C·87.8W/g, 최고 759.61, Cu 1,085°C)")
save(im, "P7_thermometer.png")

# ---------- P8 같은 셀 다른 충전량 ----------
im, d = canvas("같은 셀, 충전량만 다르면 — 100%는 203도에서 폭주, 3%는 없음", "3.25Ah NCA 18650, 가속열량계(ARC) 실측. 충전은 셀을 매번 가장 불안정한 꼭대기로 데려간다")
data = [(3, None, 300), (33, 236, 566), (66, 216, 713), (100, 203, 759)]
for i, (soc, t2, tmax) in enumerate(data):
    x = 140 + i * 300
    battery(d, x, 460, 170, 90, soc / 100, GREEN if soc < 100 else AMBER); ctext(d, x + 85, 560, f"충전 {soc}%", F_M, INK)
    fh = tmax / 759 * 220
    if t2: flame(d, x + 85, 450, fh); ctext(d, x + 85, 450 - fh - 60, f"최고 {tmax}°C", F_M, RED); ctext(d, x + 85, 450 - fh - 30, f"폭주 {t2}°C에서", F_SM, RED)
    else:
        d.ellipse([x + 55, 390, x + 115, 450], outline=GRAY, width=4); d.line([x + 60, 395, x + 110, 445], fill=GRAY, width=4)
        ctext(d, x + 85, 340, "폭주 없음", F_M, GRAY); ctext(d, x + 85, 370, f"최고 {tmax}°C", F_SM, GRAY)
box(d, (90, 610, 1310, 690), SAND, "가득 찰수록 낮은 온도에서 터지고, 더 뜨겁게 탄다. 「충전 중」이 위험한 두 번째 원리", F_S, INK)
foot(d, "근거: 원리노트 §4-1·§0-3(JES 2024, SOC 3/33/66/100% → T2 없음/236.14/216.26/203.29°C, 최고 300/566/713/759.61°C)")
save(im, "P8_soc_flames.png")

# ---------- P9 네 겹침 ----------
im, d = canvas("「충전 중 51%」는 열의 통계가 아니라 네 가지가 겹친 통계다", "소방청 2019~23 612건 중 과충전 상태 312건(51%) · 일본 NITE 150건 중 충전 중 41%")
cx, cy, r = 700, 400, 190
circles = [(cx - 120, cy - 90, "꼭대기", "100% = 가장 불안정"), (cx + 120, cy - 90, "바늘", "석출은 충전 때만"), (cx - 120, cy + 90, "플러그", "충전기는 계속 민다"), (cx + 120, cy + 90, "시계", "몇 시간 무인")]
cols = [(255, 190, 120, 120), (255, 150, 150, 120), (150, 190, 255, 120), (200, 200, 200, 120)]
ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for (x, y, _, _), c in zip(circles, cols): od.ellipse([x - r, y - r, x + r, y + r], fill=c)
im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")); d = ImageDraw.Draw(im)
# 아이콘
battery(d, cx - 330, cy - 230, 110, 60, 1.0, AMBER); d.text((cx - 330, cy - 160), "100% 충전", font=F_S, fill=INK)
for k, (nx, nh) in enumerate([(cx + 280, 40), (cx + 300, 60), (cx + 320, 45)]): needle(d, nx, cy - 170, nh, RED)
d.text((cx + 240, cy - 160), "리튬 석출", font=F_S, fill=INK)
plug(d, cx - 300, cy + 230, 1.0, BLUE); d.text((cx - 360, cy + 270), "에너지 계속 공급", font=F_S, fill=INK)
clock(d, cx + 300, cy + 230, 36, GRAY); d.text((cx + 250, cy + 275), "자리를 비움", font=F_S, fill=INK)
d.ellipse([cx - 95, cy - 60, cx + 95, cy + 60], fill=WHITE, outline=INK, width=4); ctext(d, cx, cy - 40, "51% · 41%", F_MID, RED); ctext(d, cx, cy + 8, "충전 중 사고", F_SM, INK)
foot(d, "근거: 공부노트 §1-2(소방청 312/612)·§4-1(NITE 41%), 원리노트 §4-3. 소방청 「과충전 상태」의 정의 원문은 미확인")
save(im, "P9_four_overlap.png")

# ---------- P10 BMS ----------
im, d = canvas("보호회로가 보는 숫자 셋, 못 보는 것 넷", "셀 밖의 전압·전류·온도만 잰다(보호 IC DW01-G 데이터시트·JEITA). 셀 안은 단락이 완성된 뒤에야 전압이 꺼진다")
shield(d, 330, 400, 230, MINT); ctext(d, 330, 190, "보호회로가 보는 것", F_M, GREEN)
gauge(d, 330, 330, 80, 0.85, GREEN, "과충전 차단", "4.25V"); gauge(d, 220, 470, 70, 0.6, GREEN, "과전류", "150mV"); gauge(d, 440, 470, 70, 0.7, GREEN, "충전 상한", "45°C")
# 셀 안
d.rounded_rectangle([760, 230, 1260, 580], radius=20, fill=WHITE, outline=GRAY, width=5); ctext(d, 1010, 190, "보호회로가 못 보는 것 (셀 안)", F_M, GRAY)
d.ellipse([820, 300, 850, 330], fill=GRAY); d.text((860, 302), "금속 이물", font=F_S, fill=GRAY)
for k, (nx, nh) in enumerate([(1060, 40), (1080, 55), (1100, 35)]): needle(d, nx, 345, nh, GRAY)
d.text((1120, 310), "석출 리튬", font=F_S, fill=GRAY)
d.rectangle([820, 400, 1240, 406], fill=SEP); d.ellipse([1020, 396, 1034, 410], fill=WHITE, outline=GRAY, width=2); d.text((860, 420), "분리막 핀홀", font=F_S, fill=GRAY)
d.text((860, 500), "노후(저항 상승)", font=F_S, fill=GRAY); d.rectangle([1060, 505, 1240, 525], fill=DIM); d.rectangle([1060, 505, 1180, 525], fill=GRAY)
eye_x(d, 640, 400)
box(d, (90, 610, 1310, 690), SAND, "밖에서 오는 위험(과충전·외부 단락·고온 충전)은 막고, 안에서 자라는 위험(결함·노후)은 못 막는다", F_S, INK)
foot(d, "근거: 원리노트 §5(DW01-G 4.25V·2.40V·150mV, JEITA 10~45°C 정상, 경산성 2016 FT 「셀 내부단락 사전 검지 곤란」). 모식도")
save(im, "P10_bms_sees.png")

# ---------- P11 원통형 vs 파우치 ----------
im, d = canvas("원통형엔 있고 파우치엔 없는 것 — 압력을 읽는 안전장치", "18650 캡: CID 약 1MPa 차단 · 안전벤트 약 2MPa 배출 · PTC. 보조배터리 대부분은 파우치")
# 원통
d.rounded_rectangle([200, 220, 420, 620], radius=40, fill=(90, 110, 140)); d.rectangle([250, 180, 370, 225], fill=(70, 80, 100))
for k, (lab, yy, col) in enumerate([("CID 1MPa", 250, GREEN), ("벤트 2MPa", 300, GREEN), ("PTC", 350, GREEN)]):
    d.ellipse([280, yy - 10, 300, yy + 10], fill=col); d.line([300, yy, 470, yy], fill=col, width=3); d.text((480, yy - 14), lab, font=F_S, fill=col)
ctext(d, 310, 640, "원통형 18650", F_M, INK); ctext(d, 310, 672, "셀이 스스로 끊고 터뜨림", F_SM, GREEN)
# 파우치
d.rounded_rectangle([760, 300, 1140, 560], radius=12, fill=(190, 195, 205)); d.rectangle([760, 300, 1140, 316], fill=(150, 155, 165))
d.rounded_rectangle([1160, 400, 1240, 460], radius=6, fill=(40, 110, 60)); d.text((1250, 415), "외부 기판", font=F_S, fill=INK)
d.line([1140, 430, 1160, 430], fill=INK, width=3)
ctext(d, 950, 640, "파우치(리튬폴리머)", F_M, INK); ctext(d, 950, 672, "필름뿐 — 기판이 유일한 방패", F_SM, RED)
d.ellipse([900, 330, 1000, 430], outline=RED, width=5); d.line([915, 345, 985, 415], fill=RED, width=5); ctext(d, 950, 440, "CID·벤트·PTC 없음", F_SM, RED)
foot(d, "근거: 원리노트 §1-2(특허 배경·ENEA 과충전 실험 CID 약 70°C 작동·NITE 「모바일배터리는 주로 라미네이트형」). 모식도")
save(im, "P11_cyl_vs_pouch.png")

# ---------- P12 김해 vs 청주 ----------
im, d = canvas("같은 발화, 다른 결말 — 선반 속과 손 안", "2025.1.28 김해공항 에어부산(선반) · 2026.10.10 청주공항 제주항공(승객 손)")
# 왼쪽: 선반
d.rounded_rectangle([120, 230, 600, 330], radius=14, fill=(120, 125, 135)); d.rectangle([120, 330, 600, 345], fill=(90, 95, 105))
flame(d, 360, 330, 150); ctext(d, 360, 190, "머리 위 선반, 닫힌 채", F_M, INK)
for k in range(6): d.ellipse([150 + k * 75, 400, 180 + k * 75, 430], fill=GRAY); d.rounded_rectangle([145 + k * 75, 432, 185 + k * 75, 500], radius=12, fill=GRAY)
ctext(d, 360, 530, "기체 전소 · 176명 슬라이드 탈출", F_M, RED); ctext(d, 360, 565, "최종 원인 보고서는 아직(2026.8 기준)", F_SM, GRAY)
# 오른쪽: 손
hand(d, 980, 330, 1.4); flame(d, 1030, 320, 70); ctext(d, 1010, 190, "승객 손 안, 눈앞", F_M, INK)
d.rounded_rectangle([1150, 280, 1290, 360], radius=10, fill=(60, 120, 180)); ctext(d, 1220, 305, "진압 파우치", F_SM, WHITE)
ctext(d, 1010, 530, "손 경상 1명 · 168명 중 125명 재탑승", F_M, GREEN); ctext(d, 1010, 565, "5시간 지연, 기체 무사", F_SM, GRAY)
d.line([700, 180, 700, 600], fill=DIM, width=3)
box(d, (90, 610, 1310, 690), SAND, "규정이 「선반 금지 → 손에」로 바뀐 이유가 이 두 장면이다(2025.3.1 시행)", F_S, INK)
foot(d, "근거: 공부노트 §1-1(항철위·국과수 중간 결론 「선반 속 배터리 내부 절연파괴 추정」, 청주 보도 10.10). 사람·선반은 픽토그램")
save(im, "P12_bin_vs_hand.png")

# ---------- P13 표준이 묻는 것 ----------
im, d = canvas("인증은 새 제품에게만 묻는다 — 1년 뒤의 셀은 시험 밖", "UN 38.3 · IEC/KC 62133-2 · UL 2056 전부 새 셀·새 제품. IEC는 「제조 6개월 이내 셀」 조항")
battery(d, 160, 250, 260, 130, 1.0, GREEN); ctext(d, 290, 200, "새 셀 (6개월 이내)", F_M, GREEN)
for k, lab in enumerate(["과충전", "외부 단락", "충격·낙하", "열 130°C", "기압 11.6kPa"]):
    y = 405 + k * 38; d.ellipse([170, y, 196, y + 26], fill=GREEN); d.line([176, y + 13, 182, y + 20, 191, y + 7], fill=WHITE, width=3); d.text((210, y - 2), lab, font=F_S, fill=INK)
battery(d, 820, 250, 260, 130, 0.6, DIM, body=(240, 240, 235), outline=GRAY); ctext(d, 950, 200, "1년 쓴 셀 · 저가 셀 · 충격 누적", F_M, GRAY)
for k, lab in enumerate(["노후(석출: 개시 171°C vs 181°C)", "저가 셀 결함 (1,054개 중 33개)", "떨어뜨린 뒤 생긴 핀홀", "리콜 뒤에도 쓰는 제품"]):
    y = 405 + k * 38; d.ellipse([830, y, 856, y + 26], fill=RED); d.line([836, y + 6, 850, y + 20], fill=WHITE, width=3); d.line([850, y + 6, 836, y + 20], fill=WHITE, width=3); d.text((870, y - 2), lab, font=F_S, fill=INK)
d.line([700, 200, 700, 590], fill=DIM, width=3)
box(d, (90, 610, 1310, 690), SAND, "KC 인증을 받고도 리콜 중인 모델이 기내에서 발화했다(2026.9.24) — 인증은 출시 때 사진 한 장", F_S, INK)
foot(d, "근거: 공부노트 §2-3(표준 5종·IEC 6개월 조항·UN38.3 T1 11.6kPa), §1-1(에어서울 9.24), 샌디아(171 vs 181°C), Lumafield CT(장비사). 모식도")
save(im, "P13_standards_new_only.png")

# ---------- P14 노후·저가 CT ----------
im, d = canvas("저가 셀 1,054개를 CT로 찍었더니 — 결함 33개가 전부 싼 구간", "CT 장비사 연구(이해당사자 자료). 10개 브랜드 18650, 음극 오버행 음수 = 내부 단락 위험")
random.seed(7); cols_n = 36; rows_n = 22; cell = 20
x0, y0 = 120, 180
bad = set(random.sample(range(0, 10 * rows_n), 33))  # 왼쪽 10열(저가 구간)에만 결함 33개
for r_ in range(rows_n):
    for c_ in range(cols_n):
        x = x0 + c_ * cell; y = y0 + r_ * cell
        low = c_ < 10
        col = RED if (low and (r_ * 10 + c_) in bad) else (DIM if low else GREEN)
        d.ellipse([x + 3, y + 3, x + cell - 3, y + cell - 3], fill=col)
d.rectangle([x0 - 6, y0 - 6, x0 + 10 * cell + 2, y0 + rows_n * cell + 2], outline=RED, width=4)
d.text((x0, y0 + rows_n * cell + 14), "저가·위조 구간 (붉은 점 = 결함 33개)", font=F_S, fill=RED); d.text((x0, y0 + rows_n * cell + 44), "오른쪽 정품 구간: 결함 0", font=F_S, fill=GREEN)
d.text((900, 230), "1,054개 중 33개", font=F_MID, fill=RED); d.text((900, 285), "약 13개 중 1개 꼴", font=F_M, fill=INK)
d.text((900, 340), "같은 모양, 같은 라벨,", font=F_S, fill=GRAY); d.text((900, 368), "속만 다르다", font=F_S, fill=GRAY)
foot(d, "근거: Lumafield 2025.9.24(장비사 연구, 공부노트 §3). 점 배치는 비율만 맞춘 모식도")
save(im, "P14_ct_lowcost.png")

# ---------- P15 네 나라 ----------
im, d = canvas("인증 방식은 네 가지, 사고는 네 곳 다 늘었다", "한국 KC(3자 시험) · 일본 PSE(자기검사) · 대만 BSMI(3자) · EU CE(자기선언). 숫자는 각국 집계 기준이 달라 추세만")
cols4 = [("한국 (서울)", "KC · 3자 시험", 15, 55, "2023→2025", NAVY), ("일본", "PSE · 자기검사", 47, 123, "2020→2024", BLUE), ("대만 (타이베이)", "BSMI · 3자", 7, 15, "최근 2개년", AMBER), ("EU", "CE · 자기선언", None, None, "단독 집계 없음", GRAY)]
for i, (nat, cert, a, b, yrs, col) in enumerate(cols4):
    x = 130 + i * 300
    ctext(d, x + 100, 160, nat, F_M, INK); ctext(d, x + 100, 192, cert, F_SM, GRAY)
    if a:
        s_ = 2.4
        d.rounded_rectangle([x + 30, 560 - a * s_, x + 85, 560], radius=6, fill=DIM); d.rounded_rectangle([x + 115, 560 - b * s_, x + 170, 560], radius=6, fill=col)
        ctext(d, x + 57, 560 - a * s_ - 30, str(a), F_M, GRAY); ctext(d, x + 142, 560 - b * s_ - 30, str(b), F_M, col)
    else:
        d.rounded_rectangle([x + 30, 470, x + 170, 560], radius=6, fill=LIGHT); ctext(d, x + 100, 500, "?", F_MID, GRAY)
    ctext(d, x + 100, 575, yrs, F_SM, GRAY)
box(d, (90, 620, 1310, 690), SAND, "변수는 인증 방식이 아니라 보유 대수·리콜 회수율(일본 47.8%)·충전 습관", F_S, INK)
foot(d, "근거: 공부노트 §4-5(서울소방 15→37→55, NITE 47→123, 타이베이 소방 7→15, EU Safety Gate 보조배터리 단독 건수 미확인). 추세 비교용")
save(im, "P15_four_countries.png")

# ---------- P16 규정 연표 ----------
im, d = canvas("규정은 1년 반에 다섯 번 바뀌었다 — 선반에서 손으로, 5개에서 2개로", "국토교통부·ICAO·서울교통공사 발효일 기준")
ev = [("2025.3.1", "선반 금지\n몸에 소지\n5개까지", BLUE), ("2025.9.1", "온도 스티커\n격리보관백", BLUE), ("2026.2.20", "11개 항공사\n기내 사용 금지", AMBER), ("2026.4.20", "1인 2개\n충전·사용 금지", RED), ("2026.7.1", "지하철\n160Wh 초과 금지", AMBER), ("2026.10.2", "리콜 모델\n반입 금지", RED)]
d.line([110, 400, 1290, 400], fill=GRAY, width=6)
for i, (dt, s, col) in enumerate(ev):
    x = 160 + i * 215
    d.ellipse([x - 16, 384, x + 16, 416], fill=col); ctext(d, x, 330, dt, F_M, col)
    for k, ln in enumerate(s.split("\n")): ctext(d, x, 440 + k * 27, ln, F_S, INK)
# 선반→손 픽토
d.rounded_rectangle([130, 170, 300, 230], radius=10, fill=(120, 125, 135)); ctext(d, 215, 240, "선반", F_SM, GRAY)
arrow(d, (320, 200), (400, 200), INK, 5); hand(d, 440, 200, 0.8); ctext(d, 480, 250, "손", F_SM, INK)
d.text((830, 182), "5개", font=F_M, fill=GRAY)
for k in range(5): battery(d, 900 + k * 80, 175, 60, 40, 1, DIM)
d.text((830, 240), "2개", font=F_M, fill=RED); battery(d, 900, 235, 60, 40, 1, RED); battery(d, 980, 235, 60, 40, 1, RED)
box(d, (90, 600, 1310, 690), SAND, "공항 적발 1년 433,051건 — 그중 80.6%가 위탁수하물 속(공부노트). 규정이 바뀐 걸 모르는 사람이 아직 많다", F_S, INK)
foot(d, "근거: 공부노트 §1-3 규정 연표(국토부 2025.2.13 발표·3.1 시행, 9.1 보완, 2026.2.20 11개사, 4.20 개정, 서울교통공사 7.1, 국토부 공문 10.2)")
save(im, "P16_rules_timeline.png")

# ---------- P17 할 일 ----------
im, d = canvas("오늘 할 일 하나 — 가방 속 그 녀석의 뒷면을 한 번 뒤집어 보자", "제조년월 · KC 마크 · 모델명. 리콜 조회는 제품안전정보센터. 버리라는 말이 아니다, 아는 사이가 되자는 말이다")
powerbank(d, 300, 250, 420, 230, (60, 65, 80))
d.rounded_rectangle([340, 300, 680, 430], radius=8, fill=(235, 235, 230))
for k, (lab, col) in enumerate([("KC", GREEN), ("모델명 ·······", GRAY), ("제조년월 20··.··", AMBER)]):
    d.text((360, 312 + k * 38), lab, font=F_M if k == 0 else F_S, fill=col)
hand(d, 560, 520, 1.2)
d.text((840, 250), "제조년월이 3년 전이면", font=F_S, fill=INK); d.text((840, 282), "셀은 이미 표준 밖(「6개월 이내」)", font=F_S, fill=GRAY)
d.text((840, 340), "KC가 없으면", font=F_S, fill=INK); d.text((840, 372), "보호회로 기준값을 아무도 확인 안 한 것", font=F_S, fill=GRAY)
d.text((840, 430), "리콜 목록에 있으면", font=F_S, fill=INK); d.text((840, 462), "2026.10.2부터 기내 반입도 안 된다", font=F_S, fill=GRAY)
box(d, (90, 590, 1310, 690), SAND, "충전은 눈앞에서, 잘 때는 뽑아 두는 쪽이 원리에 맞다 —\n51%는 「무인 + 만충 + 계속 공급」이 겹친 숫자였으니까", F_S, INK)
foot(d, "근거: 공부노트 §1-3(10.2 리콜 모델 반입 금지), §2-3(IEC 6개월 조항), 원리노트 §4-3. 제품은 모식도(특정 브랜드 아님)")
save(im, "P17_todo_flip.png")
print("done_batt")
