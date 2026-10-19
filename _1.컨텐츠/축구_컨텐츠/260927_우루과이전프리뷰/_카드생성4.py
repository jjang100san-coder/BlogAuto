# -*- coding: utf-8 -*-
"""카드 10 — 모레노가 과거에 직접 한 말 세 개.

한국어·영어로만 찾았을 때는 '선수 기용 성향 근거 없음' 이었다.
현지 언어로 찾으니 본인 발언이 세 나라에서 나왔다 (2026-09-28).
  프랑스어(모나코) : 같은 열한 명이 매번 그대로 갈 이유가 없다 / 포지션마다 두 명
  러시아어(소치)   : 선발은 선수들의 컨디션을 보고 고른다 / 19세 선발 데뷔
  스페인어         : 시스템을 선수에게 맞추지, 선수를 시스템에 맞추지 않는다
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "uruguay-preview", "images")
FB = "C:/Windows/Fonts/malgunbd.ttf"
FR = "C:/Windows/Fonts/malgun.ttf"

W, PAD = 1200, 70
BG = (26, 24, 24)
ACCENT = (232, 115, 90)
ROW = (43, 40, 40)
PILL = (58, 53, 53)
WHITE = (255, 255, 255)
SUB = (138, 128, 128)
YELLOW = (239, 194, 92)
BLUE = (109, 168, 224)
GREEN = (99, 201, 138)


def F(p, s):
    return ImageFont.truetype(p, s)


def tw(d, t, f):
    return d.textbbox((0, 0), t, font=f)[2]


f_title, f_sub = F(FB, 46), F(FR, 24)
f_quote, f_src, f_pill, f_foot = F(FB, 29), F(FR, 22), F(FB, 23), F(FB, 29)

rows = [
    ('"같은 열한 명이 매번 그대로\n가야 한다고 생각하지 않는다"', "모나코 시절", BLUE),
    ('"선발은 선수들이 어떤 컨디션에\n있는지를 보고 고른다"', "소치 시절", GREEN),
    ('"시스템을 선수에게 맞추지,\n선수를 시스템에 맞추지 않는다"', "스페인 시절", YELLOW),
]

rh, gap = 142, 16
h = 40 + 56 + 46 + len(rows) * rh + (len(rows) - 1) * gap + 36 + 82 + 40
img = Image.new("RGB", (W, h), BG)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 8], fill=ACCENT)

y = 40
t = "감독은 이미 답을 말했다"
d.text(((W - tw(d, t, f_title)) // 2, y), t, font=f_title, fill=WHITE)
y += 60
st = "한국에 오기 전, 세 나라에서 남긴 말"
d.text(((W - tw(d, st, f_sub)) // 2, y), st, font=f_sub, fill=SUB)
y += 46

for quote, src, col in rows:
    d.rounded_rectangle([PAD, y, W - PAD, y + rh], radius=14, fill=ROW)
    d.rounded_rectangle([PAD, y + 12, PAD + 7, y + rh - 12], radius=4, fill=col)
    d.multiline_text((PAD + 36, y + 30), quote, font=f_quote, fill=WHITE, spacing=14)
    pw = tw(d, src, f_pill) + 48
    bx = W - PAD - 26 - pw
    d.rounded_rectangle([bx, y + rh - 62, bx + pw, y + rh - 22], radius=10, fill=PILL)
    d.text((bx + 24, y + rh - 55), src, font=f_pill, fill=col)
    y += rh + gap

y += 20
d.rounded_rectangle([PAD, y, W - PAD, y + 82], radius=14, fill=ROW)
ft = "그리고 지금, 며칠 사이에 네 경기다"
d.text(((W - tw(d, ft, f_foot)) // 2, y + 24), ft, font=f_foot, fill=ACCENT)

os.makedirs(OUT, exist_ok=True)
img.save(os.path.join(OUT, "10_manager_words.png"))
print("10_manager_words.png %dx%d" % img.size)
