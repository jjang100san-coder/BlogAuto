# 「관심은 왜 한발 늦게 오나」 클립 — 그림만 봐도 이해되는 움직이는 장면 (10/16 판교 클립에서 정한 결: 장면 많이, 한 장면엔 하나만)
#   sales   : 판매 막대 1 → 184배로 치솟음
#   queue   : 줄 선 다섯 사람 — A·B 는 자기 색, C 부터 앞사람 색을 따라 같은 색으로
#   crowd   : 트로피 하나 뒤로 같은 색 사람 수백 명이 깔림 = 「상은 앞사람 수천 명」
#   worlds  : 같은 곡 막대 8세트, 세트마다 다른 막대가 1등으로 솟음
#   stars   : 독자 수 화살표는 위로, 별점은 깎임
#   curling : 컬링 등록 선수 790 → 631 꺾은선
#   ends    : 두 줄 시간 막대 — 한 팀은 2년에서 빨갛게 끝, 다른 쪽은 초록 화살표로 계속
#   bread   : 사람 10명, 7명이 「남」 표시
# 숫자는 발행본 그대로(184배·48곡·8개 세계·790→668→651→631·2년·열 중 일곱)
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1350, 1338, 30
FB = 'C:/Windows/Fonts/malgunbd.ttf'
BG = (246, 240, 230); DARK = (70, 60, 52); GREY = (190, 182, 172); YEL = (255, 190, 0)
RED = (226, 82, 64); GREEN = (70, 170, 110); BLUE = (80, 140, 210); TOPPAD = 230
f = lambda s: ImageFont.truetype(FB, s)
ease = lambda u: 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)
NUMY = 1085
CANVAS = [None]   # 큰 숫자 자리 — 말자막 위


def frames(name, sec, draw):
    d0 = os.path.join(BASE, '_frames_' + name)
    os.makedirs(d0, exist_ok=True)
    for x in os.listdir(d0):
        os.remove(os.path.join(d0, x))
    for i in range(int(sec * FPS)):
        im = Image.new('RGB', (W, H), BG)
        CANVAS[0] = im
        draw(ImageDraw.Draw(im), i / FPS)
        im.save(os.path.join(d0, 'f%04d.jpg' % (i + 1)), quality=90)


def big(d, s, y=NUMY, sz=130, col=DARK):
    d.text((W / 2, y), s, font=f(sz), fill=col, anchor='mm')


def person(d, cx, cy, s, body, tag=None):
    d.ellipse((cx - s * 0.32, cy - s * 0.95, cx + s * 0.32, cy - s * 0.31), fill=body)
    d.rounded_rectangle((cx - s * 0.5, cy - s * 0.24, cx + s * 0.5, cy + s * 0.55), radius=int(s * 0.3), fill=body)
    if tag:
        d.text((cx, cy + s * 0.16), tag, font=f(int(s * 0.42)), fill=(255, 255, 255), anchor='mm')


def book(d, x, y, w, h, col):
    d.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=col)
    d.rectangle((x + 10, y + h * 0.6, x + w - 10, y + h * 0.68), fill=(255, 255, 255))


def d_sales(d, t):
    base, x1, x2, bw = 960, 330, 760, 260
    book(d, x1 + 70, base - 190, 120, 170, GREY)                       # 어제: 낮은 막대 위 책
    d.rounded_rectangle((x1, base - 14, x1 + bw, base), radius=6, fill=GREY)
    d.text((x1 + bw / 2, base + 50), '발표 전', font=f(44), fill=DARK, anchor='mm')
    u = ease((t - 0.4) / 1.3)
    hgt = 14 + (base - TOPPAD - 60) * u
    d.rounded_rectangle((x2, base - hgt, x2 + bw, base), radius=10, fill=YEL)
    d.text((x2 + bw / 2, base + 50), '12시간 뒤', font=f(44), fill=DARK, anchor='mm')
    if t > 0.5:
        big(d, '×%d' % max(1, int(round(184 * u))), sz=140)


ORDER = [YEL, YEL, YEL, YEL, YEL]   # A·B 가 같은 걸 고르면 C 부터 따라간다(발행본 줄서기 예)


def d_queue(d, t):
    xs = [W / 2 - 440 + i * 220 for i in range(5)]
    for i, x in enumerate(xs):
        u = ease((t - 0.2 - i * 0.15) / 0.3)
        if u <= 0:
            continue
        col = ORDER[i] if i < 2 or t > 1.4 + (i - 2) * 0.35 else GREY
        person(d, x, 640, 130 * (0.7 + 0.3 * u), col, 'ABCDE'[i])
        if i >= 2 and t > 1.4 + (i - 2) * 0.35:
            d.text((x, 470), '따라감', font=f(36), fill=DARK, anchor='mm')
    if t > 2.6:
        big(d, '셋째부터 따라간다', sz=84)


def d_crowd(d, t):
    d.polygon([(W / 2 - 90, 330), (W / 2 + 90, 330), (W / 2 + 60, 470), (W / 2 - 60, 470)], fill=YEL)   # 트로피 잔
    d.rectangle((W / 2 - 18, 470, W / 2 + 18, 530), fill=YEL); d.rounded_rectangle((W / 2 - 80, 530, W / 2 + 80, 560), radius=8, fill=YEL)
    n = 0
    for r in range(6):
        for c in range(16):
            k = r * 16 + c
            if ease((t - 0.3 - k * 0.012) / 0.2) > 0:
                person(d, 140 + c * 72, 640 + r * 64, 46, YEL)
                n += 1
    if t > 1.6:
        big(d, '앞사람 수천 명', sz=96)


import random
random.seed(3)
WORLDS = []
for w in range(8):
    vals = [random.uniform(0.15, 0.6) for _ in range(8)]
    win = [3, 0, 6, 1, 7, 4, 2, 5][w]
    vals[win] = 1.0
    WORLDS.append((vals, win))


def d_worlds(d, t):
    for w, (vals, win) in enumerate(WORLDS):
        ox, oy = 110 + (w % 4) * 300, 330 + (w // 4) * 330
        d.rounded_rectangle((ox, oy, ox + 260, oy + 280), radius=18, fill=(255, 255, 255))
        for i, v in enumerate(vals):
            u = ease((t - 0.2 - w * 0.08) / 1.0)
            h = 200 * v * u
            d.rectangle((ox + 18 + i * 29, oy + 250 - h, ox + 18 + i * 29 + 22, oy + 250), fill=RED if (i == win and u > 0.9) else GREY)
        d.text((ox + 130, oy + 266), '세계 %d' % (w + 1), font=f(22), fill=DARK, anchor='mm')
    if t > 1.8:
        big(d, '1등이 다 달랐다', sz=96)


def star(d, cx, cy, r, col):
    import math
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)


def d_stars(d, t):
    u = ease((t - 0.3) / 1.2)
    for i in range(int(3 + 9 * u)):       # 독자가 늘어난다
        person(d, 200 + (i % 6) * 80, 480 + (i // 6) * 90, 56, GREY)
    d.polygon([(700, 720), (760, 720), (760, 460), (800, 460), (730, 380), (660, 460), (700, 460)], fill=GREEN)   # 위로 — 독자 급증
    d.text((730, 760), '독자', font=f(40), fill=DARK, anchor='mm')
    v = ease((t - 1.4) / 0.8)
    for k in range(5):                     # 별 다섯 중 마지막 하나가 4분의 1 깎인다
        col = YEL if not (k == 4 and v > 0) else (YEL if v < 0.5 else (230, 210, 170))
        star(d, 880 + k * 90, 520, 40, col)
    d.text((1060, 600), '별점', font=f(40), fill=DARK, anchor='mm')
    if v > 0:
        d.text((1060, 680), '-0.25', font=f(56), fill=RED, anchor='mm')
    if t > 2.2:
        big(d, '늘어난 독자, 깎인 별점', sz=80)


CUR = [(2017, 790), (2018, 668), (2020, 651), (2021, 631)]


def d_curling(d, t):
    x0, x1, y0, y1 = 200, 1150, 380, 900
    lo, hi = 600, 820
    pts = [(x0 + (x1 - x0) * i / 3, y1 - (y1 - y0) * (v - lo) / (hi - lo)) for i, (_, v) in enumerate(CUR)]
    u = ease((t - 0.3) / 1.6) * 3
    d.line((x0, y1, x1, y1), fill=GREY, width=4)
    for i, (yr, v) in enumerate(CUR):
        d.text((pts[i][0], y1 + 44), str(yr), font=f(36), fill=DARK, anchor='mm')
    for i in range(3):
        seg = max(0, min(1, u - i))
        if seg > 0:
            a, b = pts[i], pts[i + 1]
            d.line((a[0], a[1], a[0] + (b[0] - a[0]) * seg, a[1] + (b[1] - a[1]) * seg), fill=RED, width=10)
    for i in range(4):
        if u >= i:
            d.ellipse((pts[i][0] - 14, pts[i][1] - 14, pts[i][0] + 14, pts[i][1] + 14), fill=RED)
            d.text((pts[i][0], pts[i][1] - 50), '%d명' % CUR[i][1], font=f(40), fill=DARK, anchor='mm')
    if t > 2.0:
        big(d, '790 → 631', sz=120)


def d_ends(d, t):
    u = ease((t - 0.3) / 1.6)
    y1, y2, x0 = 470, 800, 160
    d.text((x0, y1 - 70), '역주행 A', font=f(48), fill=DARK, anchor='lm')
    d.text((x0, y2 - 70), '역주행 B', font=f(48), fill=DARK, anchor='lm')
    w1 = 420 * min(1, u * 2)
    d.rounded_rectangle((x0, y1, x0 + w1, y1 + 70), radius=14, fill=YEL)
    if u > 0.5:
        d.rounded_rectangle((x0 + 420, y1 - 10, x0 + 470, y1 + 80), radius=10, fill=RED)
        d.text((x0 + 520, y1 + 35), '2년에 끝', font=f(48), fill=RED, anchor='lm')
    w2 = 900 * u
    d.rounded_rectangle((x0, y2, x0 + w2, y2 + 70), radius=14, fill=YEL)
    if u > 0.9:
        d.polygon([(x0 + 900, y2 - 20), (x0 + 980, y2 + 35), (x0 + 900, y2 + 90)], fill=GREEN)
    if t > 2.2:
        big(d, '노래 탓이 아니었다', sz=96)


def d_bread(d, t):
    for i in range(10):
        u = ease((t - 0.2 - i * 0.1) / 0.3)
        if u <= 0:
            continue
        x, y = 215 + (i % 5) * 230, 520 + (i // 5) * 260
        male = i < 7
        on = t > 1.6
        person(d, x, y, 150 * (0.7 + 0.3 * u), (BLUE if male else (230, 140, 160)) if on else GREY, ('남' if male else '여') if on else None)
    if t > 1.8:
        big(d, '10명 중 7명은 남자', sz=96)


def d_why(d, t):   # 교통정리 ① — 현상에서 이유로 넘어가는 자리(10/16 사용자 「현상→근거 사이에 한 장면」)
    u = ease((t - 0.1) / 0.4)
    d.text((W / 2, 470), '?', font=f(int(60 + 220 * u)), fill=YEL, anchor='mm')
    for k, s in enumerate(['① 남을 따라 산다', '② 신호가 꺼지면 관심도 꺼진다']):
        v = ease((t - 1.0 - k * 0.6) / 0.35)
        if v > 0:
            y = 760 + k * 150
            d.rounded_rectangle((W / 2 - 520, y - 55, W / 2 + 520, y + 55), radius=55, fill=(255, 255, 255), outline=YEL, width=6)
            d.text((W / 2 - 40 * (1 - v), y), s, font=f(60), fill=DARK, anchor='mm')


def chapter(n, text, col):
    def draw(d, t):
        u = ease((t - 0.1) / 0.4)
        r = 150 * u
        d.ellipse((W / 2 - r, 560 - r, W / 2 + r, 560 + r), fill=col)
        if u > 0.6:
            d.text((W / 2, 560), n, font=f(170), fill=(255, 255, 255), anchor='mm')
        v = ease((t - 0.6) / 0.4)
        if v > 0:
            d.text((W / 2, 830 + 30 * (1 - v)), text, font=f(84), fill=DARK, anchor='mm')
    return draw


def last(name):   # 각 장면의 마지막 프레임 — 요약 장에 작은 그림으로
    d0 = os.path.join(BASE, '_frames_' + name)
    return Image.open(os.path.join(d0, sorted(os.listdir(d0))[-1]))


def d_recap(d, t, im=None):   # 요약 장(10/16 사용자 「이미지도 요약 형태로 장 추가」) — ①·② 칸마다 앞 장면 그림을 작게
    rows = [('1', '남을 따라 산다', YEL, ['queue', 'crowd', 'worlds']),
            ('2', '신호가 꺼지면, 관심도 꺼진다', RED, ['stars', 'curling', 'ends', 'bread'])]
    for r, (n, text, col, names) in enumerate(rows):
        u = ease((t - 0.2 - r * 0.9) / 0.4)
        if u <= 0:
            continue
        y = 270 + r * 440
        d.ellipse((90, y, 170, y + 80), fill=col)
        d.text((130, y + 40), n, font=f(54), fill=(255, 255, 255), anchor='mm')
        d.text((200, y + 40), text, font=f(58), fill=DARK, anchor='lm')
        tw = 260 if len(names) == 4 else 300
        for k, nm in enumerate(names):
            v = ease((t - 0.4 - r * 0.9 - k * 0.15) / 0.3)
            if v <= 0:
                continue
            th = last(nm).resize((tw, int(tw * H / W)))
            x = 100 + k * (tw + 26)
            CANVAS[0].paste(th, (x, y + 110))
            d.rounded_rectangle((x, y + 110, x + tw, y + 110 + th.height), radius=10, outline=(220, 212, 200), width=3)


if __name__ == '__main__':
    for name, sec, fn in [('sales', 4.0, d_sales), ('queue', 4.5, d_queue), ('crowd', 4.0, d_crowd), ('worlds', 5.0, d_worlds),
                          ('stars', 4.5, d_stars), ('curling', 4.5, d_curling), ('ends', 5.0, d_ends), ('bread', 4.0, d_bread),
                          ('why', 4.0, d_why), ('ch1', 3.0, chapter('1', '남을 따라 산다', YEL)), ('ch2', 3.0, chapter('2', '신호가 꺼지면, 관심도 꺼진다', RED)),
                          ('recap', 4.5, d_recap)]:
        frames(name, sec, fn); print(name)
