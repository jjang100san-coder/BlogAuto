# -*- coding: utf-8 -*-
"""전술판 B 양식 시안 (2026-10-17) — 꼴(세로 피치 두 장·선수 원·점선=사람·실선=공)은 그대로, 디자인만 다듬기.
바뀐 것: 잔디 줄무늬 피치 · 실제 팀 색(수원 청 / 화성 주황 / 안산 회백) · 원에 그림자 · 공 화살표에 은은한 빛
        · 둥근 이름표 대신 각진 이름표(팀 색 왼쪽 날) · 빈 공간은 노란 빗금 · 왼쪽 정렬 제목 · 노란 결론 띠
같은 장면: 화성 프리뷰 03 「끌어내서 생긴 틈」(사용자 확인 배치 그대로)
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
SANS = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
def F(size, w=400):
    fo = ImageFont.truetype(SANS, size); fo.set_variation_by_axes([w]); return fo
W, H = 1080, 1440
BG, INK, MUT, YEL = (14,16,22), (240,238,232), (150,156,168), (245,211,74)
SUW, SUW_RED, HWA, ANS = (42,94,224), (208,38,59), (238,122,44), (196,202,212)
PW, PH = 440, 720
PA, PB = (60,270), (580,270)
def pt(o, fx, fy): return (o[0]+PW*fx, o[1]+PH*fy)

im = Image.new("RGBA", (W,H), BG+(255,))
def layer(): return Image.new("RGBA", (W,H), (0,0,0,0))
def paste(l):
    global im; im = Image.alpha_composite(im, l)

# ---------- 머리 (B 양식: 왼쪽 정렬 · 팀 색 사선 조각) ----------
L0 = layer(); d0 = ImageDraw.Draw(L0)
d0.polygon([(0,0),(420,0),(400,12),(0,12)], fill=SUW+(255,)); d0.polygon([(420,0),(450,0),(430,12),(400,12)], fill=SUW_RED+(255,))
paste(L0); d = ImageDraw.Draw(im)
d.text((60,52), "전술 도해 · 개념도", font=F(22,700), fill=YEL)
d.text((60,86), "끌어내서 생긴 틈", font=F(56,900), fill=INK)
d.text((60,166), "화성 1차전 동점골과 안산전 첫 골 · 위쪽이 상대 골문", font=F(24,400), fill=MUT)

# ---------- 피치 ----------
def pitch(o):
    x0, y0 = o; x1, y1 = x0+PW, y0+PH
    base = layer(); b = ImageDraw.Draw(base)
    n = 12
    for i in range(n):                                   # 잔디 깎은 줄무늬
        c = (24,62,46,255) if i % 2 == 0 else (28,70,52,255)
        b.rectangle([x0, y0+PH*i/n, x1, y0+PH*(i+1)/n], fill=c)
    paste(base)
    ln = layer(); l = ImageDraw.Draw(ln); C = (255,255,255,150); w = 2
    l.rectangle([x0,y0,x1,y1], outline=C, width=w)
    l.line([x0,y0+PH/2,x1,y0+PH/2], fill=C, width=w)
    r = PW*0.13; l.ellipse([x0+PW/2-r,y0+PH/2-r,x0+PW/2+r,y0+PH/2+r], outline=C, width=w)
    l.ellipse([x0+PW/2-3,y0+PH/2-3,x0+PW/2+3,y0+PH/2+3], fill=C)
    for top in (True, False):
        bw, bh, sw, sh = PW*0.6, PH*0.13, PW*0.3, PH*0.05
        yb = y0 if top else y1
        sgn = 1 if top else -1
        l.rectangle([x0+(PW-bw)/2, min(yb, yb+sgn*bh), x0+(PW+bw)/2, max(yb, yb+sgn*bh)], outline=C, width=w)
        l.rectangle([x0+(PW-sw)/2, min(yb, yb+sgn*sh), x0+(PW+sw)/2, max(yb, yb+sgn*sh)], outline=C, width=w)
        gw = PW*0.16; l.rectangle([x0+(PW-gw)/2, yb-(8 if top else 0), x0+(PW+gw)/2, yb+(0 if top else 8)], fill=(255,255,255,200))
    paste(ln)

def head(o, num, title, sub):
    d = ImageDraw.Draw(im); x, y = o[0], o[1]-62
    d.rectangle([x, y+6, x+8, y+34], fill=YEL)            # 번호 대신 노란 날 — 아래 설명 번호와 헷갈리지 않게
    d.text((x+20, y), title, font=F(26,900), fill=INK)
    d.text((x+20+d.textlength(title, font=F(26,900))+12, y+6), sub, font=F(20,500), fill=MUT)

def hatch(o, fx0, fy0, fx1, fy1, label=None, lpos=None):
    (x0,y0), (x1,y1) = pt(o,fx0,fy0), pt(o,fx1,fy1)
    hl = layer(); h = ImageDraw.Draw(hl)
    h.rectangle([x0,y0,x1,y1], fill=YEL+(28,))
    step = 14; span = (x1-x0)+(y1-y0)
    for k in range(-int(y1-y0), int(x1-x0), step):        # 빗금(사각형 안으로 자름)
        h.line([x0+k, y1, x0+k+(y1-y0), y0], fill=YEL+(90,), width=2)
    mask = Image.new("L", (W,H), 0); ImageDraw.Draw(mask).rectangle([x0,y0,x1,y1], fill=255)
    clipped = layer(); clipped.paste(hl, (0,0), mask)
    ImageDraw.Draw(clipped).rectangle([x0,y0,x1,y1], outline=YEL+(220,), width=2)
    paste(clipped)

def player(o, fx, fy, col, r=14):
    x, y = pt(o, fx, fy)
    sh = layer(); ImageDraw.Draw(sh).ellipse([x-r+2, y-r+4, x+r+2, y+r+4], fill=(0,0,0,120))
    paste(sh.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(im); d.ellipse([x-r, y-r, x+r, y+r], fill=col, outline=(255,255,255), width=3)

def name(o, fx, fy, text, col, size=16):
    x, y = pt(o, fx, fy); d = ImageDraw.Draw(im); fo = F(size, 700)
    tw = d.textlength(text, font=fo)
    bx0, by0 = x - tw/2 - 10, y - size/2 - 7
    bl = layer(); ImageDraw.Draw(bl).rectangle([bx0, by0, bx0+tw+20, by0+size+14], fill=(8,10,14,215)); paste(bl)
    d = ImageDraw.Draw(im); d.rectangle([bx0, by0, bx0+4, by0+size+14], fill=col)
    d.text((bx0+12, by0+3), text, font=fo, fill=INK)

def callout(o, fx, fy, text, size=17):
    x, y = pt(o, fx, fy); d = ImageDraw.Draw(im); fo = F(size, 900)
    tw = d.textlength(text, font=fo)
    d.rectangle([x-tw/2-10, y-size/2-7, x+tw/2+10, y+size/2+9], fill=YEL)
    d.text((x-tw/2, y-size/2-4), text, font=fo, fill=BG)

def _head(d, x1, y1, ang, col, head):
    d.polygon([(x1,y1),(x1-math.cos(ang-0.42)*head, y1-math.sin(ang-0.42)*head),(x1-math.cos(ang+0.42)*head, y1-math.sin(ang+0.42)*head)], fill=col)

def run(o, a, b, col, w=4, head=13):          # 사람의 움직임 = 팀 색 점선
    (x0,y0), (x1,y1) = pt(o,*a), pt(o,*b); d = ImageDraw.Draw(im)
    ang = math.atan2(y1-y0, x1-x0); L = math.hypot(x1-x0, y1-y0); t = 0
    while t < L-head:
        e = min(t+13, L-head*0.8)
        d.line([x0+math.cos(ang)*t, y0+math.sin(ang)*t, x0+math.cos(ang)*e, y0+math.sin(ang)*e], fill=col, width=w); t += 22
    _head(d, x1, y1, ang, col, head)

def ball(o, pts, w=4, head=14):               # 공 = 흰 실선 + 은은한 빛, pts 가 3개면 곡선
    P = [pt(o,*p) for p in pts]
    if len(P) == 2:
        n = 30; P = [(P[0][0]+(P[1][0]-P[0][0])*i/n, P[0][1]+(P[1][1]-P[0][1])*i/n) for i in range(n+1)]
    elif len(P) == 3:
        n = 40; P = [((1-t)**2*P[0][0]+2*(1-t)*t*P[1][0]+t*t*P[2][0], (1-t)**2*P[0][1]+2*(1-t)*t*P[1][1]+t*t*P[2][1]) for t in [i/n for i in range(n+1)]]
    gl = layer(); ImageDraw.Draw(gl).line(P[:-1], fill=(255,255,255,90), width=w+8, joint="curve")
    paste(gl.filter(ImageFilter.GaussianBlur(4)))
    d = ImageDraw.Draw(im); d.line(P[:-1], fill=(255,255,255), width=w, joint="curve")
    ang = math.atan2(P[-1][1]-P[-3][1], P[-1][0]-P[-3][0]); _head(d, P[-1][0], P[-1][1], ang, (255,255,255), head)

# ---------- 장면 ① 화성 1차전 동점골 (사용자 확인 배치) ----------
pitch(PA); head(PA, "1", "화성 1차전 동점골", "68분")
hatch(PA, 0.83, 0.01, 0.995, 0.40)
for x,y in ((0.10,0.09),(0.28,0.08),(0.45,0.075),(0.60,0.075)): player(PA, x, y, HWA, 12)
for x,y in ((0.16,0.30),(0.38,0.30),(0.56,0.31)): player(PA, x, y, HWA, 12)
player(PA, 0.50, 0.62, HWA, 12)
run(PA, (0.93,0.12), (0.77,0.17), HWA, w=3, head=11); player(PA, 0.74, 0.18, HWA, 12)
run(PA, (0.90,0.34), (0.73,0.43), HWA, w=3, head=11); player(PA, 0.70, 0.45, HWA, 12)
for x,y in ((0.38,0.80),(0.16,0.68),(0.46,0.70),(0.06,0.30),(0.30,0.24)): player(PA, x, y, SUW, 13)
run(PA, (0.47,0.31), (0.50,0.20), SUW)
run(PA, (0.62,0.82), (0.60,0.44), SUW)
run(PA, (0.95,0.54), (0.93,0.34), SUW)
run(PA, (0.92,0.28), (0.885,0.09), SUW, head=11)
ball(PA, [(0.63,0.40),(0.90,0.31)])
ball(PA, [(0.84,0.065),(0.53,0.16)])
player(PA, 0.50, 0.17, SUW, 14); player(PA, 0.60, 0.42, SUW, 14); player(PA, 0.87, 0.055, SUW, 14)
name(PA, 0.37, 0.165, "강현묵", SUW); name(PA, 0.42, 0.47, "고종현", SUW); name(PA, 0.66, 0.025, "헤이스(10)", SUW)
callout(PA, 0.80, 0.60, "오른쪽이 비었다")

# ---------- 장면 ② 안산전 첫 골 ----------
pitch(PB); head(PB, "2", "안산전 첫 골", "2분")
hatch(PB, 0.40, 0.10, 0.62, 0.24)
for x in (0.10,0.28,0.50,0.72,0.90): player(PB, x, 0.20, ANS, 12)
for x in (0.18,0.36,0.74,0.88): player(PB, x, 0.43, ANS, 12)
for x,y in ((0.06,0.32),(0.64,0.32),(0.94,0.32),(0.38,0.80),(0.62,0.80),(0.10,0.62),(0.90,0.62),(0.40,0.62)): player(PB, x, y, SUW, 13)
run(PB, (0.38,0.30), (0.48,0.16), SUW)
ball(PB, [(0.66,0.60),(0.50,0.15)])
player(PB, 0.36, 0.32, SUW, 14); player(PB, 0.66, 0.62, SUW, 14)
name(PB, 0.22, 0.27, "루이스", SUW); name(PB, 0.80, 0.70, "김민우 롱패스", SUW)
callout(PB, 0.52, 0.055, "수비 사이 틈으로")

# ---------- 아래: 범례 · 설명 · 결론 띠 · 출처 ----------
d = ImageDraw.Draw(im); y = 1032
x = 60
for col, t in ((SUW,"수원삼성"),(HWA,"화성"),(ANS,"안산")):
    d.rectangle([x, y-9, x+18, y+9], fill=col); d.text((x+28, y-15), t, font=F(22,700), fill=INK); x += 28 + d.textlength(t, font=F(22,700)) + 40
d.line([x, y, x+40, y], fill=(255,255,255), width=4); d.text((x+50, y-15), "공", font=F(22,700), fill=INK); x += 110
for k in range(3): d.line([x+k*16, y, x+k*16+9, y], fill=SUW, width=4)
d.text((x+56, y-15), "사람", font=F(22,700), fill=INK); x += 140
d.rectangle([x, y-10, x+22, y+10], outline=YEL, width=2); d.text((x+32, y-15), "빈 공간", font=F(22,700), fill=INK)
notes = ["화성 1차전: 고종현이 센터서클 위까지 몰고 가자 오른쪽 수비가 안으로 좁혀졌다",
         "헤이스가 그 빈 오른쪽을 골라인까지 파고들어 컷백, 강현묵이 넣었다",
         "안산전: 앞 넷이 넓게 서고 루이스가 수비 사이 틈으로 뛰었다"]
y = 1086
for i, t in enumerate(notes):
    d.rectangle([60, y, 92, y+32], fill=YEL); d.text((70, y-1), str(i+1), font=F(22,900), fill=BG)
    d.text((106, y-1), t, font=F(24,500), fill=INK); y += 50
d.rectangle([0, H-170, W, H-82], fill=YEL)
d.text((60, H-157), "누군가를 끌어내야 반대쪽이 빈다", font=F(40,900), fill=BG)
d.text((60, H-56), "장면: 화성 1차전 중계·새벽의 축구 전문가 분석 + 사용자 확인 · 안산전 도해(사용자 확인) · 개념도 · 직접 만든 이미지", font=F(18,400), fill=MUT)
im.convert("RGB").save(os.path.join(HERE, "전술판_B양식_시안.png"))
print("ok")
