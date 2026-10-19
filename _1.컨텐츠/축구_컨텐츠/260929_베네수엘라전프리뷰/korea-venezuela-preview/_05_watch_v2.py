# -*- coding: utf-8 -*-
"""05_watch_v2.png — 채점 항목 세 가지 → 네 가지 (10/1 업데이트). 원본 05_watch.png 의 배치·색을 따라 다시 그린다."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images", "05_watch_v2.png")
FONT = "C:/Windows/Fonts/NotoSansKR-VF.ttf"
BG, CARD, BANNER = (34, 14, 22), (48, 24, 33), (60, 32, 43)
GOLD, WHITE, SUB, GREY = (238, 196, 110), (246, 240, 238), (162, 137, 143), (190, 172, 177)

ITEMS = [
    ("① 베네수엘라가 4백으로 나오는가", "명단은 킥오프 한 시간 전에 나온다", False),
    ("② 두 중앙 미드필더가 맨마크를 끌고 다니는가", "볼에 다가가면 공간이 지워진다", False),
    ("③ 투톱의 압박이 상대 볼란치까지 닿는가", "우루과이전엔 센터백 둘만 쫓았다", False),
    ("④ 수비할 때 4-2-3-1로 내려서는가", "이강인이 상대 중앙 미드필더 앞에 서는지 · 10월 1일 추가", True),
]


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def ctext(d, cx, y, s, f, fill):
    b = f.getbbox(s)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y - b[1]), s, font=f, fill=fill)


CARD_H, GAP, TOP = 122, 18, 185
H = TOP + len(ITEMS) * (CARD_H + GAP) - GAP + 66 + 82 + 40
W = 1080
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 8], fill=GOLD)
ctext(d, W / 2, 50, "경기 뒤 채점할 네 가지", font(46, 800), WHITE)
ctext(d, W / 2, 118, "한국 베네수엘라 선발 전망", font(24, 500), SUB)

y = TOP
for head, sub, new in ITEMS:
    d.rounded_rectangle([70, y, 1010, y + CARD_H], radius=14, fill=CARD,
                        outline=GOLD if new else None, width=2 if new else 0)
    hf = font(31, 800)
    b = hf.getbbox(head)
    d.text((106 - b[0], y + 26 - b[1]), head, font=hf, fill=WHITE)
    if new:
        tag = "추가"
        tf = font(20, 800)
        tb = tf.getbbox(tag)
        tx = 106 + (b[2] - b[0]) + 16
        d.rounded_rectangle([tx, y + 26, tx + (tb[2] - tb[0]) + 22, y + 58], radius=8, fill=GOLD)
        d.text((tx + 11 - tb[0], y + 42 - (tb[3] - tb[1]) / 2 - tb[1]), tag, font=tf, fill=BG)
    sf = font(24, 500)
    sb = sf.getbbox(sub)
    d.text((106 - sb[0], y + 78 - sb[1]), sub, font=sf, fill=GREY)
    y += CARD_H + GAP

y += 66 - GAP
d.rounded_rectangle([70, y, 1010, y + 82], radius=14, fill=BANNER)
ctext(d, W / 2, y + 23, "우루과이전에서 틀린 자리를 다시 본다", font(31, 800), GOLD)
im = im.crop((0, 0, W, y + 82 + 40))
im.save(OUT)
print(OUT, im.size)
