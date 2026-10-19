# -*- coding: utf-8 -*-
"""⑥ 나라별 기준 비교  ⑦ 6개월 우선권 — 미국 TSDR 원본 + 기사로 확인한 것만."""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1400, 800
BG = (250, 250, 247); INK = (30, 30, 30); GRAY = (120, 120, 120)
BLUE = (41, 98, 255); RED = (220, 60, 60); GREEN = (30, 150, 90); AMBER = (235, 150, 20)
LIGHT = (232, 236, 245); PINK = (252, 232, 232); MINT = (226, 245, 236); SAND = (252, 240, 215)

def font(size, bold=False):
    return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", "malgunbd.ttf" if bold else "malgun.ttf"), size)
F_T, F_H, F_B, F_S, F_XS = font(42, True), font(28, True), font(24), font(20), font(17)

def canvas(title, sub=None):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.text((60, 44), title, font=F_T, fill=INK)
    if sub: d.text((60, 102), sub, font=F_S, fill=GRAY)
    return im, d

def box(d, xy, fill, text, f=F_B, color=INK, radius=16, outline=None):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3 if outline else 0)
    lines = text.split("|"); lh = f.size + 8; y = y0 + (y1 - y0 - lh * len(lines)) / 2
    for ln in lines:
        d.text((x0 + (x1 - x0 - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=color); y += lh

def arrow(d, p0, p1, color=INK, width=5):
    d.line([p0, p1], fill=color, width=width)
    ang = math.atan2(p1[1]-p0[1], p1[0]-p0[0]); L = 18
    a = (p1[0]-L*math.cos(ang-0.5), p1[1]-L*math.sin(ang-0.5)); b = (p1[0]-L*math.cos(ang+0.5), p1[1]-L*math.sin(ang+0.5))
    d.polygon([p1, a, b], fill=color)

def foot(d, t): d.text((60, H-46), t, font=F_XS, fill=GRAY)

# ---------- ⑥ 나라별 비교 ----------
im, d = canvas("⑥ 같은 기준인가 — 한국·일본·멕시코 vs 미국",
               "한국에서 세운 세 가지 논리(먼저 낸 사람 / 나라마다 따로 / 브레이크)가 해외에서도 그대로 서는지")
cols = ["", "한국", "일본", "멕시코", "미국"]
rows = [
    ("기본 원칙", "먼저 낸 사람|(선출원)", "먼저 낸 사람|(선출원)", "먼저 낸 사람|(선출원)", "먼저 쓴 사람|(선사용)"),
    ("그런데 실제로는", "출원일이 기준", "출원일이 기준", "출원일이 기준", "사용 의사로 먼저 내면|출원일을 '사용일'로 쳐줌|(ITU + §7(c))"),
    ("나라마다 따로?", "예", "예", "예", "예"),
    ("브레이크", "§34①13|부정한 목적 거절", "4조1항19호|부정 목적 거절", "악의 출원|무효 가능", "먼저 쓰던 사람이 이김|+ 진짜 사용 의사 없으면 탈락"),
    ("패노메논 현황", "48건, 5건 등록|(문체부+JYP)", "9건 출원·5건 등록|(JYP)", "출원 (보도만)", "11건 출원, 보류 중|(JYP, 한국 출원 우선권)"),
]
x0, y0 = 70, 160; cw = [200, 265, 265, 265, 265]; rh = [70, 95, 60, 95, 95]
y = y0
for ri, row in enumerate([tuple(cols)] + rows):
    x = x0
    for ci, cell in enumerate(row):
        hdr = ri == 0 or ci == 0
        fill = LIGHT if hdr else ((SAND if ci == 4 else (255, 255, 255)))
        h = 56 if ri == 0 else rh[ri-1]
        col = INK
        if ri == 1 and ci in (1, 2, 3): fill, col = MINT, GREEN
        if ri == 1 and ci == 4: fill, col = PINK, RED
        if ri == 3 and ci in (1, 2, 3, 4): fill, col = MINT, GREEN
        box(d, (x, y, x + cw[ci] - 8, y + h - 8), fill, cell, F_H if ri == 0 else (F_S if ri in (2, 4, 5) else F_B), col, radius=10)
        x += cw[ci]
    y += 56 if ri == 0 else rh[ri-1]
box(d, (70, y + 10, 1330, y + 95), SAND,
    "결론: 세 나라는 한국과 같은 기준. 미국만 출발점이 다르지만, 아무도 안 쓰던 새 이름이면 결과는 같다 — 먼저 낸 쪽이 이긴다.", F_S, INK)
foot(d, "근거: USPTO TSDR(99498239 Basis·Owner·Priority) · JPO 공보(경향 영문 10/3) · Lanham Act §1(b)·§7(c)·§44(d) · 일본 상표법 4①19 · 한국 상표법 34①13. 멕시코는 보도만.")
im.save(os.path.join(OUT, "06_나라별_같은기준인가.png"))

# ---------- ⑦ 6개월 우선권 ----------
im, d = canvas("⑦ 한국에 먼저 내면 6개월은 '시간이 멈춘다' — 파리조약 우선권",
               "USPTO 기록: Priority Claimed Yes / Foreign Application 4020250186056 (Oct. 02, 2025, Korea)")
y = 330
d.line([(100, y), (1300, y)], fill=GRAY, width=4)
pts = [
    (190, "2025.10.2", "한국에 FANOMENON|35류 출원", MINT, GREEN),
    (640, "2025.11.14", "미국에 출원|(43일 뒤)", SAND, AMBER),
    (1090, "2026.4.2", "6개월 우선권 마감", LIGHT, INK),
]
for x, date, txt, fill, col in pts:
    d.ellipse([x-13, y-13, x+13, y+13], fill=col)
    d.text((x - d.textlength(date, font=F_H)/2, y-66), date, font=F_H, fill=col)
    box(d, (x-150, y+36, x+150, y+150), fill, txt, F_B, INK)
# 괄호 표시
d.line([(190, 230), (1090, 230)], fill=BLUE, width=6)
d.line([(190, 215), (190, 245)], fill=BLUE, width=6); d.line([(1090, 215), (1090, 245)], fill=BLUE, width=6)
d.text((640 - d.textlength("이 안에 해외에 내면 → 미국에서도 '10월 2일에 낸 것'으로 쳐준다", font=F_B)/2, 170),
       "이 안에 해외에 내면 → 미국에서도 '10월 2일에 낸 것'으로 쳐준다", font=F_B, fill=BLUE)
box(d, (100, 530, 1300, 640), PINK,
    "그래서 미국 심사관은 '한국 등록증을 가져오면 이어서 보겠다'며 멈춰 뒀다(2026.6.16 보류).|한국 5건은 2026.8.20 등록됐으니, 다음 단계는 그 등록증을 미국에 내는 것이다.", F_S, INK)
foot(d, "TSDR Prosecution History: 11/14 접수 → 3/21 1차 지적 → 6/8 답변 → 6/9 2차 지적 → 6/12 답변 → 6/16 보류. 3/20자 지적서는 '충돌 상표 없음'(경향 영문 10/7).")
im.save(os.path.join(OUT, "07_6개월_우선권.png"))
print("saved 2")
