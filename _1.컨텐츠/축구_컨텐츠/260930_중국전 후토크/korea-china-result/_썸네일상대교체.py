# -*- coding: utf-8 -*-
"""01_thumb.png 가운데 박스 둘째 줄(결승 상대)만 다시 그린다.
사용: python _썸네일상대교체.py "결승은 10월 3일, 우즈베키스탄과" [출력경로]
원본은 처음 한 번 images/01_thumb_orig.png 로 보관한다."""
import os, shutil, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "images", "01_thumb.png")
ORIG = os.path.join(HERE, "images", "01_thumb_orig.png")
BG, FG = (46, 36, 30), (182, 168, 156)
BAND = (86, 422, 994, 462)           # 박스 안쪽 둘째 줄 영역 (x0,y0,x1,y1)
OLD = "결승은 10월 3일, 일본·우즈베키스탄 4강 승자와"
FONT = "C:/Windows/Fonts/NotoSansKR-VF.ttf"
WEIGHT = 400                          # 가변 폰트 기본값은 100(가늘다). 원본과 대조해 400 으로 맞춤

def font_of(size):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([WEIGHT])
    return f

def measure(im):
    xs, ys = [], []
    for y in range(BAND[1], BAND[3]):
        for x in range(BAND[0], BAND[2]):
            p = im.getpixel((x, y))
            if sum(abs(a - b) for a, b in zip(p, BG)) > 60:
                xs.append(x); ys.append(y)
    return min(xs), max(xs), min(ys), max(ys)

def main(text, out):
    if not os.path.exists(ORIG):
        shutil.copy2(SRC, ORIG)
    im = Image.open(ORIG).convert("RGB")
    x0, x1, y0, y1 = measure(im)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    # 원래 문구 폭에 맞는 글자 크기를 찾는다
    size = 10
    for s in range(14, 40):
        f = font_of(s)
        b = f.getbbox(OLD)
        if b[2] - b[0] > (x1 - x0): break
        size = s
    font = font_of(size)
    d = ImageDraw.Draw(im)
    d.rectangle(BAND, fill=BG)
    b = font.getbbox(text)
    w, h = b[2] - b[0], b[3] - b[1]
    d.text((cx - w / 2.0 - b[0], cy - h / 2.0 - b[1]), text, font=font, fill=FG)
    im.save(out)
    print("size", size, "orig box", (x0, x1, y0, y1), "->", out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else SRC)
