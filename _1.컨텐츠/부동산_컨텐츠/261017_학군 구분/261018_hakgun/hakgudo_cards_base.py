# -*- coding: utf-8 -*-
"""학군·학교 글 카드 공용 모듈 (2026-10-18 시안) — 「칠판 학구도」 양식.

축구 B(팀 색 대각 면·노란 띠)·농구 코트 카드(먹+볼 오렌지·호/원)와 문법을 일부러 가른다.
- 바탕: 칠판 초록(BOARD) + 분필 결(grain·얼룩). 글자는 분필 흰색(CHALK), 강조는 분필 하늘(SKY).
- 꼴: 학구도 = 「구역 지도」. 점선 경계선·구역 면·학교 핀, 분필 밑줄. 둥근 상자 남발 금지, 왼쪽 정렬.
- 네 구는 분필 네 색으로 고정: 영통 분홍 · 기흥 하늘 · 수지 연두 · 분당 버터.
- 숫자: Noto Sans KR Black, 아주 크게. 결론은 왼쪽 정렬 분필 하늘 띠 한 줄.
- 정체성: 「학구도 노트 · 0n / 10」 번호. 4:5 세로(1080×1350).
- 숫자는 원문 값만(마스터 0-4), 학교명·동 이름 금지(0-10).
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BOARD, BOARD2, BOARD3 = (30, 56, 48), (38, 68, 58), (52, 86, 74)
CHALK, CHALK2, MUTE = (243, 240, 230), (214, 222, 214), (150, 172, 160)
SKY, PINK, LIME, BUTTER = (128, 200, 250), (250, 150, 170), (190, 228, 120), (250, 218, 120)
GU_COL = {"영통": PINK, "기흥": SKY, "수지": LIME, "분당": BUTTER}
W, H = 1080, 1350
random.seed(7)


def F(size, w="Black"):
    f = ImageFont.truetype(FONT, int(size)); f.set_variation_by_name(w); return f


def board():
    """칠판: 초록 바탕 + 지운 자국 얼룩 + 분필 가루 결."""
    im = Image.new("RGB", (W, H), BOARD)
    smear = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(smear)
    for _ in range(14):
        x, y = random.randint(-200, W), random.randint(-100, H)
        sd.ellipse([x, y, x + random.randint(300, 700), y + random.randint(80, 200)], fill=random.randint(10, 26))
    smear = smear.filter(ImageFilter.GaussianBlur(60))
    im = Image.composite(Image.new("RGB", (W, H), BOARD3), im, smear)
    n = Image.effect_noise((W, H), 28).convert("L").point(lambda v: 18 if v > 170 else 0)
    im = Image.composite(Image.new("RGB", (W, H), (70, 100, 88)), im, n)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(92, 70, 46), width=22)      # 나무 틀
    d.rectangle([22, 22, W - 23, H - 23], outline=(20, 38, 32), width=3)
    return im, d


def chalk(im, draw_fn, rough=0.18):
    """분필 질감: 레이어에 그린 뒤 알파를 잘게 깎는다."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    a = layer.split()[3]
    hole = Image.effect_noise(im.size, 60).convert("L").point(lambda v: 0 if v > 255 * (1 - rough) else 255)
    layer.putalpha(ImageChops.multiply(a, hole))
    im.paste(layer, (0, 0), layer)


def text(im, xy, s, size, fill=CHALK, w="Black", anchor="la", rough=0.12):
    chalk(im, lambda d: d.text(xy, s, font=F(size, w), fill=fill, anchor=anchor), rough)


def header(im, no, kicker, title, sub=None):
    text(im, (70, 70), f"학구도 노트 · {no:02d} / 10", 26, MUTE, "Bold", rough=0.05)
    text(im, (70, 118), kicker, 30, SKY, "Bold", rough=0.05)
    y = 160
    for ln in title.split("\n"):
        text(im, (70, y), ln, 64, CHALK); y += 84
    underline(im, 72, y + 6, 520)
    if sub: text(im, (70, y + 30), sub, 26, CHALK2, "Medium", rough=0.04)
    return y + 80


def underline(im, x, y, L, col=SKY, wgt=7):
    def fn(d):
        pts = [(x + i, y + math.sin(i / 37) * 3) for i in range(0, L, 6)]
        d.line(pts, fill=col, width=wgt, joint="curve")
    chalk(im, fn, 0.22)


def dashed(d, p0, p1, col=CHALK2, w=4, dash=16, gap=12):
    x0, y0 = p0; x1, y1 = p1; L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    t = 0
    while t < L:
        e = min(t + dash, L); d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * e, y0 + uy * e)], fill=col, width=w); t = e + gap


def school(d, cx, cy, s, col=CHALK, w=4, fill=None):
    """학교 선 아이콘: 몸통 + 박공 + 깃발 + 문."""
    bw, bh = s, s * .55
    d.rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], outline=col, width=w, fill=fill)
    d.polygon([(cx - bw * .28, cy - bh / 2), (cx, cy - bh / 2 - s * .28), (cx + bw * .28, cy - bh / 2)], outline=col, fill=fill)
    d.line([(cx, cy - bh / 2 - s * .28), (cx, cy - bh / 2 - s * .52)], fill=col, width=w)
    d.polygon([(cx, cy - bh / 2 - s * .52), (cx + s * .2, cy - bh / 2 - s * .45), (cx, cy - bh / 2 - s * .38)], fill=col)
    d.rectangle([cx - s * .08, cy + bh / 2 - s * .22, cx + s * .08, cy + bh / 2], outline=col, width=max(2, w - 1))
    for k in (-1, 1):
        d.rectangle([cx + k * s * .3 - s * .07, cy - s * .08, cx + k * s * .3 + s * .07, cy + s * .04], outline=col, width=max(2, w - 2))


def house(d, cx, cy, s, col=CHALK, w=5, fill=None):
    d.rectangle([cx - s * .4, cy - s * .1, cx + s * .4, cy + s * .45], outline=col, width=w, fill=fill)
    d.polygon([(cx - s * .55, cy - s * .08), (cx, cy - s * .5), (cx + s * .55, cy - s * .08)], outline=col, fill=fill)
    d.line([(cx - s * .55, cy - s * .08), (cx, cy - s * .5), (cx + s * .55, cy - s * .08)], fill=col, width=w)
    d.rectangle([cx - s * .1, cy + s * .15, cx + s * .1, cy + s * .45], outline=col, width=max(2, w - 2))


def arrow(d, p0, p1, col=CHALK, w=6, head=22):
    d.line([p0, p1], fill=col, width=w)
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (-0.45, 0.45):
        d.line([p1, (p1[0] - head * math.cos(a + s), p1[1] - head * math.sin(a + s))], fill=col, width=w)


def xmark(d, cx, cy, r, col=PINK, w=8):
    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=col, width=w); d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=col, width=w)


def conclusion(im, y, s, col=SKY):
    """결론 띠: 왼쪽 정렬 분필 하늘 면 + 칠판색 글자."""
    f = F(32, "Black")
    d = ImageDraw.Draw(im)
    tw = d.textlength(s, font=f)
    chalk(im, lambda dd: dd.rectangle([60, y, 60 + tw + 60, y + 66], fill=col), 0.08)
    d.text((90, y + 33), s, font=f, fill=BOARD, anchor="lm")


def source(im, s):
    text(im, (70, H - 78), s, 20, MUTE, "Medium", rough=0.02)
