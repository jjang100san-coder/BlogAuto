# -*- coding: utf-8 -*-
"""카드 09 — 자리별 후보를 '역할'로 묶은 지도.

근거(새벽의 축구 전문가 라이브, 2026-09-27):
  - 이동경: 모레노가 첫 미팅에서 "너는 세컨드 스트라이커" 라고 직접 지정.
    울산에서 하던 자리 그대로. 그리고 그 자리는 "이강인 자리" 와 겹친다.
  - 박태준: "지난 경기에 이재성이 했던 역할을 맡을 것" → 받치는 쪽이 아니라
    올라가는 쪽이다. (이전 버전에서 받치는 쪽에 잘못 넣었다)
  - 김민수: 레인저스·지로나에서 가운데를 많이 봤고, 에콰도르전 후반에
    이동경과 나란히 섰다 → 오른쪽보다 중앙 라인.
  - "수비 라인보다는 공격 라인에 교체나 위치 변화가 있을 것 같다."
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
GREEN = (99, 201, 138)
YELLOW = (239, 194, 92)
BLUE = (109, 168, 224)


def F(p, s):
    return ImageFont.truetype(p, s)


def tw(d, t, f):
    return d.textbbox((0, 0), t, font=f)[2]


f_title, f_sub = F(FB, 46), F(FR, 24)
f_pos, f_names, f_desc, f_foot = F(FB, 25), F(FB, 30), F(FR, 22), F(FB, 29)

rows = [
    ("최전방", "오현규 · 오세훈", "조규성이 빠져서 열린 자리", ACCENT),
    ("세컨드 스트라이커", "이강인 · 이동경 · 김민수", "감독이 셋 다 이 역할로 본다", YELLOW),
    ("올라가는 중앙", "황인범 · 이재성 · 박태준", "지난 경기엔 이재성이 여기였다", BLUE),
    ("받치는 중앙", "김봉수 · 백승호", "세컨드볼을 먹어야 하는 쪽", GREEN),
]

rh, gap = 124, 16
h = 40 + 56 + 46 + len(rows) * rh + (len(rows) - 1) * gap + 36 + 82 + 40
img = Image.new("RGB", (W, h), BG)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 8], fill=ACCENT)

y = 40
t = "바뀐다면 앞쪽이다"
d.text(((W - tw(d, t, f_title)) // 2, y), t, font=f_title, fill=WHITE)
y += 60
st = "자리마다 후보가 다르다. 뒤보다 앞이 열려 있다"
d.text(((W - tw(d, st, f_sub)) // 2, y), st, font=f_sub, fill=SUB)
y += 46

for pos, names, desc, col in rows:
    d.rounded_rectangle([PAD, y, W - PAD, y + rh], radius=14, fill=ROW)
    d.rounded_rectangle([PAD, y + 10, PAD + 7, y + rh - 10], radius=4, fill=col)
    pw = tw(d, pos, f_pos) + 44
    d.rounded_rectangle([PAD + 32, y + 22, PAD + 32 + pw, y + 62], radius=10, fill=PILL)
    d.text((PAD + 54, y + 29), pos, font=f_pos, fill=col)
    d.text((PAD + 32 + pw + 26, y + 26), names, font=f_names, fill=WHITE)
    d.text((PAD + 36, y + 76), desc, font=f_desc, fill=SUB)
    y += rh + gap

y += 20
d.rounded_rectangle([PAD, y, W - PAD, y + 82], radius=14, fill=ROW)
ft = "평가전이다. 같은 열한 명이 나올 이유가 없다"
d.text(((W - tw(d, ft, f_foot)) // 2, y + 24), ft, font=f_foot, fill=ACCENT)

os.makedirs(OUT, exist_ok=True)
img.save(os.path.join(OUT, "09_midfield_pool.png"))
print("09_midfield_pool.png %dx%d" % img.size)
