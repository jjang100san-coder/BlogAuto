# 판교 클립 v2 — 그림만 봐도 이해되는 움직이는 장면들 (10/16 사용자 「집중 안 해도 이미지로 이해되게」 → 「장면을 늘려서, 한 장면엔 하나만」)
#   count  : 후기 카드가 차르륵 넘어가며 숫자 0 → 292
#   zoom   : 카드 한 장을 크게 — 글 끝 해시태그 다섯 칸이 1→5 차례로 켜짐
#   tags   : 카드 5장, 해시태그 줄이 다섯 장 모두 똑같이 노랗게 켜지고 0 → 81
#   other  : 토요일 낙지집 카드 5장 — 해시태그 색이 제각각, 숫자 0
#   people : 얼굴 없는 사람 49명이 같은 노란 줄을 들고 나타남, 0 → 49명
#   ad     : 같은 49명 중 1명에게만 「광고」 딱지
#   month  : 올해 달마다 막대 — 8월만 39로 솟음
# 프레임을 _frames_<이름>\ 에 바로 쓴다(shorts 가 영상 프레임으로 읽음). 1350x1338 = 장면 칸 1080x1070 의 1.25배, 위 230px 는 큰 글 자리
# 숫자는 예약 초안 그대로: 292편 · 같은 해시태그 81편 · 낙지집 0편 · 50편을 블로거 49명 · 체험단 고지 1편 · 8월 39편(달별 값은 card5_months.png)
import os, random
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1350, 1338, 30
FB = 'C:/Windows/Fonts/malgunbd.ttf'
BG = (246, 240, 230); CARD = (255, 255, 255); GREY = (214, 208, 200); DARK = (70, 60, 52)
YEL = (255, 196, 0); RED = (226, 82, 64); TOPPAD = 230
MIX = [(120, 180, 230), (240, 140, 120), (150, 200, 140), (190, 150, 220), (240, 190, 110), (110, 190, 190)]
f = lambda s: ImageFont.truetype(FB, s)
ease = lambda u: 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)


def frames(name, sec, draw):
    d0 = os.path.join(BASE, '_frames_' + name)
    os.makedirs(d0, exist_ok=True)
    for x in os.listdir(d0):
        os.remove(os.path.join(d0, x))
    for i in range(int(sec * FPS)):
        im = Image.new('RGB', (W, H), BG)
        draw(ImageDraw.Draw(im), i / FPS, im)
        im.save(os.path.join(d0, 'f%04d.jpg' % (i + 1)), quality=90)


def pill(d, x, y, w, h, col):
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=col)
    on = col != GREY
    d.text((x + h * 0.4, y + h / 2), '#', font=f(int(h * 0.62)), fill=(255, 255, 255) if on else (150, 144, 136), anchor='lm')
    d.rounded_rectangle((x + h * 1.15, y + h * 0.38, x + w - h * 0.4, y + h * 0.62), radius=4, fill=(255, 255, 255) if on else (180, 174, 166))


def card(d, x, y, cw, ch, tagcols):
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=22, fill=CARD, outline=(232, 226, 218), width=3)
    d.rounded_rectangle((x + 18, y + 16, x + 128, y + ch - 16), radius=12, fill=(226, 200, 176))
    d.rounded_rectangle((x + 150, y + 20, x + 620, y + 38), radius=8, fill=GREY)
    d.rounded_rectangle((x + 150, y + 46, x + 500, y + 60), radius=8, fill=(232, 226, 218))
    for j, col in enumerate(tagcols):
        pill(d, x + 150 + j * 142, y + ch - 48, 130, 36, col)


def big(d, s, y=1085, sz=130, col=DARK):   # 말자막(장면 아래 18%) 위에 앉도록
    d.text((W / 2, y), s, font=f(sz), fill=col, anchor='mm')


def mix(a, b, u):
    return tuple(int(a[c] + (b[c] - a[c]) * u) for c in range(3))


CW, CH = 880, 120
X0 = (W - CW) // 2


def stack(d, t, colfun):
    for k in range(5):
        u = ease((t - 0.1 - k * 0.18) / 0.3)
        if u > 0:
            card(d, X0, TOPPAD + 20 + k * (CH + 14) - (1 - u) * 120, CW, CH, [colfun(k, j, t) for j in range(5)])


def d_count(d, t, im):   # 카드가 위로 빠르게 넘어간다
    off = (t * 900) % (CH + 14)
    for k in range(-1, 6):
        y = TOPPAD + 20 + k * (CH + 14) - off
        if TOPPAD - CH < y < 960:
            card(d, X0, y, CW, CH, [GREY] * 5)
    d.rectangle((0, 1000, W, H), fill=BG)
    big(d, '%d개' % int(round(292 * ease(t / 1.6))))


def d_zoom(d, t, im):
    s = 1.55; cw, ch = int(CW * 0.86), int(CH * s)
    x, y = (W - cw) // 2, TOPPAD + 160
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=26, fill=CARD, outline=(232, 226, 218), width=3)
    d.rounded_rectangle((x + 28, y + 28, x + 200, y + ch - 28), radius=16, fill=(226, 200, 176))
    d.rounded_rectangle((x + 230, y + 40, x + cw - 40, y + 70), radius=10, fill=GREY)
    d.rounded_rectangle((x + 230, y + 90, x + cw - 160, y + 114), radius=10, fill=(232, 226, 218))
    py = y + ch + 50; pw, gap = 196, 18; px0 = (W - (5 * pw + 4 * gap)) / 2
    for j in range(5):
        on = ease((t - 0.6 - j * 0.35) / 0.25)
        pill(d, px0 + j * (pw + gap), py, pw, 62, mix(GREY, YEL, on))
        if on > 0.5:
            d.text((px0 + j * (pw + gap) + pw / 2, py + 100), str(j + 1), font=f(54), fill=DARK, anchor='mm')
    d.line((x + cw / 2, y + ch, W / 2, py - 6), fill=(200, 192, 182), width=4)


def d_tags(d, t, im):
    lit = ease((t - 1.1) / 0.4)
    stack(d, t, lambda k, j, t: mix(GREY, YEL, lit))
    if lit > 0:
        d.rounded_rectangle((X0 + 138, TOPPAD + 20 + CH - 58, X0 + 150 + 5 * 142 - 2, TOPPAD + 20 + 4 * (CH + 14) + CH - 6),
                            radius=20, outline=YEL, width=int(10 * lit))
    if t > 1.4:
        big(d, '%d개' % int(round(81 * ease((t - 1.5) / 1.2))))


random.seed(7)
OTHER = [[random.choice(MIX) for _ in range(5)] for _ in range(5)]


def d_other(d, t, im):
    stack(d, t, lambda k, j, t: OTHER[k][j])
    if t > 1.2:
        big(d, '0개')


COLS, ROWS, S, GX, GY = 7, 7, 50, 150, 100
OX = (W - (COLS - 1) * GX) / 2; OY = TOPPAD + 75
AD = (3, 4)


def person(d, cx, cy, s, body, tag):
    d.ellipse((cx - s * 0.32, cy - s * 0.95, cx + s * 0.32, cy - s * 0.31), fill=body)
    d.rounded_rectangle((cx - s * 0.5, cy - s * 0.24, cx + s * 0.5, cy + s * 0.55), radius=int(s * 0.3), fill=body)
    d.rounded_rectangle((cx - s * 0.62, cy + s * 0.62, cx + s * 0.62, cy + s * 0.86), radius=int(s * 0.12), fill=tag)


def crowd(d, t, appear=True):
    for r in range(ROWS):
        for c in range(COLS):
            u = ease((t - 0.1 - (r * COLS + c) * 0.025) / 0.25) if appear else 1
            if u > 0:
                person(d, OX + c * GX, OY + r * GY + (1 - u) * 30, S * (0.6 + 0.4 * u), (150, 140, 130), YEL)


def d_people(d, t, im):
    crowd(d, t)
    big(d, '%d명' % int(round(49 * ease((t - 0.1) / 1.4))), sz=120)


def d_ad(d, t, im):
    crowd(d, t, appear=False)
    v = ease((t - 0.3) / 0.35)
    if v > 0:
        cx, cy = OX + AD[1] * GX, OY + AD[0] * GY
        d.ellipse((cx - S * 0.75 * v, cy - S * 1.05 * v, cx + S * 0.75 * v, cy + S * 0.95 * v), outline=RED, width=8)
        if v > 0.6:
            d.rounded_rectangle((cx - 62, cy - S * 1.75, cx + 62, cy - S * 1.15), radius=14, fill=RED)
            d.text((cx, cy - S * 1.45), '광고', font=f(38), fill=(255, 255, 255), anchor='mm')
    if t > 0.6:
        big(d, '1개', sz=120, col=RED)


MONTHS = [8, 1, 5, 3, 0, 1, 2, 39, 13, 1]


def d_month(d, t, im):
    bw, gap = 92, 26; x0 = (W - (10 * bw + 9 * gap)) / 2; base = 960; top = TOPPAD + 110
    for i, v in enumerate(MONTHS):
        u = ease((t - 0.1 - i * 0.05) / 0.4)
        if i == 7:
            u = ease((t - 0.8) / 0.6)
        h = (base - top) * v / 39 * u
        x = x0 + i * (bw + gap)
        d.rounded_rectangle((x, base - max(h, 6), x + bw, base), radius=10, fill=(170, 160, 150) if i != 7 else (176, 92, 48))
        d.text((x + bw / 2, base + 40), '%d월' % (i + 1), font=f(34), fill=DARK, anchor='mm')
        if i == 7 and u > 0.9:
            d.text((x + bw / 2, base - h - 40), '39', font=f(64), fill=(176, 92, 48), anchor='mm')


if __name__ == '__main__':
    for name, sec, fn in [('count', 4.5, d_count), ('zoom', 4.5, d_zoom), ('tags', 6.0, d_tags), ('other', 5.0, d_other),
                          ('people', 5.0, d_people), ('ad', 4.0, d_ad), ('month', 5.0, d_month)]:
        frames(name, sec, fn); print(name)
    print('ok')
