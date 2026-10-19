# 날씨요정 클립 — 그림만 봐도 이해되는 움직이는 장면들 (10/16 결: 장면을 늘리고 한 장면엔 하나만, 장 카드, 요약 장)
#   count    : 여권 17·기차표 14 가 하나씩 튀어나오며 0 → 31번
#   score    : 「평소대로면」 병에 빗물 → 「실제」 병 → 빼기 = 요정 점수
#   grades   : 다섯 등급 띠가 차례로 (요정·견습 요정·보통·견습 악마·악마)
#   ch1/2/3  : 장 카드 ①진짜 요정은? ②악마는? ③반전 — 캐릭터가 들어온다
#   canada   : 엿새 칸, 평소 막대 2.98일 → 칸마다 해 → 0일
#   three    : 악마 도장 셋 쾅 (경주·규슈 렌터카·제주)
#   gyeongju : 이틀 칸, 평소 0.16일 → 둘 다 비 → 2일
#   split    : 여권(해외 17번 +6.0 요정) vs 기차표(국내 14번 −1.1 견습 악마)
#   recap    : 다섯 등급에 31번이 쌓이고(1·13·10·4·3) 「견습 요정」 도장
# 캐릭터는 cutout.py 로 오린 fairy.png·devil.png, 도장은 images 폴더 ai_stamps.png (모두 AI 생성). 숫자는 발행본 그대로
import os, math, sys
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(BASE), 'images')
W, H, FPS = 1350, 1338, 30
FB = 'C:/Windows/Fonts/malgunbd.ttf'
BG = (244, 241, 234); DARK = (58, 54, 66)
SUN = (236, 168, 0); SKY = (74, 150, 214); LAV = (160, 140, 206); PUR = (104, 66, 160); RAIN = (96, 130, 190)
TOPPAD = 230
f = lambda s: ImageFont.truetype(FB, max(8, int(s)))
ease = lambda u: 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)


def pop(u):   # 살짝 튀며 등장
    if u <= 0: return 0
    if u >= 1: return 1
    return ease(u / 0.6) * 1.12 if u < 0.6 else 1.12 - 0.12 * ease((u - 0.6) / 0.4)


FAIRY = Image.open(os.path.join(BASE, 'fairy.png')).convert('RGBA')
DEVIL = Image.open(os.path.join(BASE, 'devil.png')).convert('RGBA')
_st = Image.open(os.path.join(IMG, 'ai_stamps.png')).convert('RGB')


def _stamp(box):
    c = _st.crop(box)
    a = c.convert('L').point(lambda v: max(0, min(255, int((245 - v) * 2.4))))
    c = c.convert('RGBA'); c.putalpha(a); return c


S_FAIRY = _stamp((80, 125, 475, 535)); S_DEVIL = _stamp((543, 125, 945, 535))


def frames(name, sec, draw):
    d0 = os.path.join(BASE, '_frames_' + name)
    os.makedirs(d0, exist_ok=True)
    for x in os.listdir(d0):
        os.remove(os.path.join(d0, x))
    for i in range(int(sec * FPS)):
        im = Image.new('RGB', (W, H), BG)
        draw(ImageDraw.Draw(im), i / FPS, im)
        im.save(os.path.join(d0, 'f%04d.jpg' % (i + 1)), quality=90)


def paste(im, src, cx, cy, h, alpha=1.0, rot=0):
    if h <= 2 or alpha <= 0: return
    s = src.resize((max(1, int(src.width * h / src.height)), int(h)), Image.LANCZOS)
    if rot: s = s.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1:
        s.putalpha(s.getchannel('A').point(lambda v: int(v * alpha)))
    im.paste(s, (int(cx - s.width / 2), int(cy - s.height / 2)), s)


def big(d, s, y=1085, sz=120, col=DARK):
    d.text((W / 2, y), s, font=f(sz), fill=col, anchor='mm')


def sun(d, cx, cy, r, u=1.0):
    if u <= 0: return
    r = r * u
    for k in range(10):
        a = k * math.pi / 5
        d.line((cx + math.cos(a) * r * 1.25, cy + math.sin(a) * r * 1.25, cx + math.cos(a) * r * 1.7, cy + math.sin(a) * r * 1.7),
               fill=SUN, width=max(2, int(r * 0.18)))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SUN)


def cloud(d, cx, cy, r, col=(150, 150, 168), rain=False, t=0):
    if rain:
        for j in range(5):
            x = cx - r + j * r * 0.5
            y = cy + r * 0.8 + ((t * 300 + j * 37) % (r * 0.9))
            d.line((x, y, x - 8, y + r * 0.32), fill=RAIN, width=max(3, int(r * 0.09)))
    for dx, dy, k in [(-0.8, 0.15, 0.62), (0.8, 0.15, 0.62), (-0.25, -0.2, 0.8), (0.4, -0.3, 0.7)]:
        d.ellipse((cx + dx * r - k * r, cy + dy * r - k * r, cx + dx * r + k * r, cy + dy * r + k * r), fill=col)
    d.rounded_rectangle((cx - 1.4 * r, cy, cx + 1.4 * r, cy + 0.75 * r), radius=int(0.35 * r), fill=col)


# ---------- count
def passport(d, x, y, w, h):
    if w < 12 or h < 12: return
    d.rounded_rectangle((x, y, x + w, y + h), radius=max(2, int(w * 0.1)), fill=(32, 52, 102))
    d.ellipse((x + w * 0.28, y + h * 0.3, x + w * 0.72, y + h * 0.3 + w * 0.44), outline=(214, 180, 90), width=max(1, int(w * 0.035)))


def ticket(d, x, y, w, h, bg=BG):
    if w < 12 or h < 12: return
    d.rounded_rectangle((x, y, x + w, y + h), radius=max(2, int(min(w, h) * 0.08)), fill=(255, 255, 255), outline=(200, 196, 188), width=3)
    d.rectangle((x + 3, y + h * 0.16, x + w - 3, y + h * 0.3), fill=(60, 160, 120))
    r = min(w, h) * 0.07
    d.ellipse((x - r, y + h / 2 - r, x + r, y + h / 2 + r), fill=bg); d.ellipse((x + w - r, y + h / 2 - r, x + w + r, y + h / 2 + r), fill=bg)


def d_count(d, t, im):
    cols, cw, ch, gx, gy = 8, 104, 136, 142, 158
    x0 = (W - (cols - 1) * gx - cw) / 2; y0 = TOPPAD + 50
    n = 0
    for i in range(31):
        u = pop((t - 0.2 - i * 0.075) / 0.25)
        if u <= 0: continue
        n = i + 1
        r, c = divmod(i, cols)
        w, h = cw * u, ch * u
        cx, cy = x0 + c * gx + cw / 2, y0 + r * gy + ch / 2
        (passport if i < 17 else ticket)(d, cx - w / 2, cy - h / 2, w, h)
    if t > 2.8:
        d.text((W / 2 - 250, 985), '여권 17', font=f(50), fill=(32, 52, 102), anchor='mm')
        d.text((W / 2 + 250, 985), '기차표 14', font=f(50), fill=(40, 130, 96), anchor='mm')
    big(d, '%d번' % n, y=1090)


# ---------- score
def jar(d, x, y, w, h, level, col):
    lh = (h - 24) * level
    if lh > 2:
        d.rounded_rectangle((x + 12, y + h - 12 - lh, x + w - 12, y + h - 12), radius=22, fill=col)
    d.rounded_rectangle((x, y, x + w, y + h), radius=30, outline=(150, 146, 140), width=8)


def d_score(d, t, im):
    y, h, w = TOPPAD + 190, 460, 250
    xl, xr = 130, 500
    jar(d, xl, y, w, h, 0.75 * ease((t - 0.2) / 1.0), (120, 160, 220))
    cloud(d, xl + w / 2, y - 70, 50, rain=t < 1.3, t=t)
    jar(d, xr, y, w, h, 0.35 * ease((t - 1.1) / 0.7), (90, 120, 190))
    d.text((xl + w / 2, y + h + 55), '평소대로면', font=f(52), fill=DARK, anchor='mm')
    d.text((xr + w / 2, y + h + 55), '실제', font=f(52), fill=DARK, anchor='mm')
    if t > 1.9: d.text(((xl + w + xr) / 2, y + h / 2), '-', font=f(150), fill=DARK, anchor='mm')
    if t > 2.3: d.text((xr + w + 75, y + h / 2), '=', font=f(130), fill=DARK, anchor='mm')
    u = pop((t - 2.5) / 0.35)
    if u > 0:
        paste(im, FAIRY, 1110, y + h / 2 - 10, 330 * u)
        d.text((1110, y + h + 55), '요정 점수', font=f(52), fill=SUN, anchor='mm')


# ---------- grades / recap
GR = [('요정', SUN, S_FAIRY), ('견습 요정', SKY, S_FAIRY), ('보통', (150, 146, 140), None),
      ('견습 악마', LAV, S_DEVIL), ('악마', PUR, S_DEVIL)]
COUNTS = [1, 13, 10, 4, 3]
RY0, RH, RG = TOPPAD + 40, 124, 22


def d_grades(d, t, im):
    x0, w = 110, 1130
    for k in range(5):
        name, col, st = GR[k]
        u = ease((t - 0.2 - k * 0.32) / 0.35)
        if u <= 0: continue
        y = RY0 + k * (RH + RG); xo = (1 - u) * -500
        d.rounded_rectangle((x0 + xo, y, x0 + xo + w, y + RH), radius=RH // 2, fill=col)
        d.ellipse((x0 + xo + 18, y + 10, x0 + xo + 18 + RH - 20, y + RH - 10), fill=(255, 255, 255))
        if st is not None: paste(im, st, x0 + xo + 18 + (RH - 20) / 2, y + RH / 2, RH - 26)
        d.text((x0 + xo + 165, y + RH / 2), name, font=f(62), fill=(255, 255, 255), anchor='lm')
    if t > 2.2:
        d.text((W / 2, RY0 + 5 * (RH + RG) + 30), '점수 ±0.5 · 확률 10%', font=f(56), fill=DARK, anchor='mm')


def d_recap(d, t, im):
    for k in range(5):
        name, col, st = GR[k]
        y = RY0 + k * (RH + RG)
        d.text((330, y + RH / 2), name, font=f(54), fill=col if k != 2 else (130, 126, 120), anchor='rm')
        u = ease((t - 0.2 - k * 0.18) / 0.9)
        bw = max(24, 700 * COUNTS[k] / 13 * u)
        d.rounded_rectangle((360, y + 18, 360 + bw, y + RH - 18), radius=30, fill=col)
        if u > 0.05:
            d.text((360 + bw + 22, y + RH / 2), '%d' % round(COUNTS[k] * u), font=f(60), fill=DARK, anchor='lm')
        if k == 1 and t > 2.5:
            d.rounded_rectangle((60, y - 8, W - 60, y + RH + 8), radius=40, outline=SKY, width=8)
    u = (t - 2.7) / 0.3
    if u > 0:
        paste(im, S_FAIRY, W - 175, RY0 + 3.75 * (RH + RG), 240 * (1.6 - 0.6 * ease(u)), alpha=min(1, ease(u) * 1.2), rot=-12)
    if t > 3.0:
        big(d, '최종 견습 요정', y=1075, sz=104, col=SKY)


# ---------- 장 카드
def chapter(num, text, who, bgc, rainy=False):
    def dr(d, t, im):
        d.rectangle((0, 0, W, H), fill=bgc)
        if rainy:
            for j in range(26):
                x = (j * 53) % W; y = (t * 520 + j * 97) % H
                d.line((x, y, x - 10, y + 40), fill=(190, 186, 214), width=5)
        u = pop((t - 0.1) / 0.3)
        if u > 0:
            r = 80 * u; cy = TOPPAD + 110
            d.ellipse((W / 2 - r, cy - r, W / 2 + r, cy + r), fill=DARK)
            d.text((W / 2, cy + 2), num, font=f(100 * u), fill=(255, 255, 255), anchor='mm')
        if t > 0.35:
            d.text((W / 2, TOPPAD + 300), text, font=f(118), fill=DARK, anchor='mm')
        v = ease((t - 0.5) / 0.6); bob = math.sin(t * 4) * 10
        if who in ('fairy', 'both'):
            paste(im, FAIRY, (W / 2 if who == 'fairy' else W / 2 - 250) + (1 - v) * -800, 820 + bob, 440)
        if who in ('devil', 'both'):
            paste(im, DEVIL, (W / 2 if who == 'devil' else W / 2 + 250) + (1 - v) * 800, 830 - bob, 410)
    return dr


# ---------- 날 칸
def day_tile(d, x, y, w, h, label, state, t, u=1.0):
    d.rounded_rectangle((x, y, x + w, y + h), radius=22, fill=(255, 255, 255), outline=(220, 214, 204), width=4)
    d.text((x + w / 2, y + 42), label, font=f(40), fill=DARK, anchor='mm')
    cx, cy = x + w / 2, y + h / 2 + 30
    if state == 'sun': sun(d, cx, cy, w * 0.2, u)
    elif state == 'rain' and u > 0: cloud(d, cx, cy - 20, w * 0.24 * u, col=(120, 118, 140), rain=True, t=t)


def meter(d, x, y, w, val, full, col, label, u):
    d.text((x, y - 42), label, font=f(46), fill=DARK, anchor='lm')
    d.rounded_rectangle((x, y, x + w, y + 54), radius=27, fill=(226, 222, 214))
    bw = w * val / full * ease(u)
    if u > 0: d.rounded_rectangle((x, y, x + max(bw, 54), y + 54), radius=27, fill=col)


def d_canada(d, t, im):
    tw, th, gap = 172, 250, 20; x0 = (W - 6 * tw - 5 * gap) / 2; y = TOPPAD + 330
    meter(d, x0, TOPPAD + 140, 6 * tw + 5 * gap, 2.98, 6, (130, 150, 190), '평소대로면 2.98일', (t - 0.2) / 1.0)
    for i in range(6):
        u = pop((t - 1.3 - i * 0.16) / 0.3)
        day_tile(d, x0 + i * (tw + gap), y, tw, th, '6/%d' % (5 + i), 'sun', t, u)
    if t > 2.4:
        d.text((x0, 960), '실제 0일', font=f(118), fill=SUN, anchor='lm')
        paste(im, FAIRY, W - 230, 930 + math.sin(t * 5) * 8, 250)


def d_gyeongju(d, t, im):
    tw, th, gap = 330, 330, 60; x0 = (W - 2 * tw - gap) / 2; y = TOPPAD + 300
    meter(d, x0, TOPPAD + 130, 2 * tw + gap, 0.16, 2, (130, 150, 190), '평소대로면 0.16일', (t - 0.2) / 0.6)
    for i in range(2):
        u = pop((t - 1.1 - i * 0.35) / 0.35)
        day_tile(d, x0 + i * (tw + gap), y, tw, th, '11/%d' % (8 + i), 'rain', t, u)
    if t > 2.0:
        d.text((x0, 980), '실제 2일', font=f(118), fill=PUR, anchor='lm')
        paste(im, DEVIL, W - 230, 950 + math.sin(t * 5) * 8, 240)


# ---------- 악마 셋
def d_three(d, t, im):
    rows = [('경주', '25.11', '-1.8'), ('규슈 렌터카', '25.03', '-1.8'), ('제주', '24.04', '-1.5')]
    for k, (a, b, c) in enumerate(rows):
        y = TOPPAD + 60 + k * 245; x = 160; w = 1030; h = 210
        u = ease((t - 0.1 - k * 0.15) / 0.3)
        if u <= 0: continue
        xo = (1 - u) * 300
        ticket(d, x + xo, y, w, h)
        d.text((x + xo + 70, y + 130), a, font=f(64), fill=DARK, anchor='lm')
        d.text((x + xo + 70, y + 182), b, font=f(34), fill=(130, 126, 120), anchor='lm')
        d.text((x + xo + w - 270, y + 135), c, font=f(70), fill=PUR, anchor='rm')
        v = (t - 0.8 - k * 0.55) / 0.25
        if v > 0:
            paste(im, S_DEVIL, x + w - 130, y + h / 2 + 15, 180 * (1.7 - 0.7 * ease(v)), alpha=min(1, ease(v) * 1.3), rot=10)


# ---------- 해외 vs 국내
def d_split(d, t, im):
    y = TOPPAD + 70
    u = ease((t - 0.1) / 0.4)
    px = 110 - (1 - u) * 600
    passport(d, px, y, 520, 600)
    d.text((px + 260, y + 80), '해외 17번', font=f(60), fill=(240, 220, 160), anchor='mm')
    v = ease((t - 0.3) / 0.4)
    tx = 720 + (1 - v) * 600
    ticket(d, tx, y + 70, 520, 520)
    d.text((tx + 260, y + 285), '국내 14번', font=f(60), fill=DARK, anchor='mm')
    if t > 0.8:
        a = ease((t - 0.8) / 0.9)
        d.text((370, y + 510), '%+.1f' % (6.0 * a), font=f(110), fill=(255, 255, 255), anchor='mm')
        d.text((980, y + 400), '%+.1f' % (-1.1 * a), font=f(110), fill=PUR, anchor='mm')
    p = (t - 1.9) / 0.25
    if p > 0: paste(im, S_FAIRY, 370, y + 300, 230 * (1.6 - 0.6 * ease(p)), alpha=min(1, ease(p) * 1.3), rot=-10)
    q = (t - 2.4) / 0.25
    if q > 0: paste(im, S_DEVIL, 980, y + 528, 115 * (1.6 - 0.6 * ease(q)), alpha=min(0.75, ease(q)), rot=8)
    if t > 2.0: d.text((370, 1000), '요정', font=f(84), fill=SUN, anchor='mm')
    if t > 2.5: d.text((980, 1000), '견습 악마', font=f(84), fill=LAV, anchor='mm')


TODO = [('count', 6.0, d_count), ('score', 6.0, d_score), ('grades', 6.0, d_grades),
        ('ch1', 4.0, chapter('1', '진짜 요정은?', 'fairy', (255, 243, 200))),
        ('canada', 7.0, d_canada),
        ('ch2', 4.0, chapter('2', '악마는?', 'devil', (228, 224, 240), rainy=True)),
        ('three', 5.0, d_three), ('gyeongju', 6.5, d_gyeongju),
        ('ch3', 4.0, chapter('3', '반전', 'both', (226, 238, 248))),
        ('split', 5.5, d_split), ('recap', 7.5, d_recap)]

if __name__ == '__main__':
    only = sys.argv[1:]
    for name, sec, fn in TODO:
        if only and name not in only: continue
        frames(name, sec, fn); print(name, flush=True)
    print('ok')
