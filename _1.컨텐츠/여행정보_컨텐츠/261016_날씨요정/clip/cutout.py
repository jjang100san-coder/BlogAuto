# ai_characters.png(하늘색 단색 바탕)에서 해 요정·먹구름 악마를 오려 낸다 → fairy.png · devil.png
import os
from PIL import Image, ImageDraw, ImageFilter
BASE = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(os.path.dirname(BASE), 'images', 'ai_characters.png')).convert('RGB')
W, H = src.size
fill = src.copy()
for p in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1), (W // 2, 2), (W // 2, H - 2)]:
    ImageDraw.floodfill(fill, p, (255, 0, 255), thresh=24)
m = Image.new('L', (W, H), 0)
px, fp = m.load(), fill.load()
for y in range(H):
    for x in range(W):
        if fp[x, y] != (255, 0, 255):
            px[x, y] = 255
m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
rgba = src.convert('RGBA'); rgba.putalpha(m)
for name, box in [('fairy', (70, 60, 530, 640)), ('devil', (540, 110, 930, 640))]:
    c = rgba.crop(box); c = c.crop(c.getbbox()); c.save(os.path.join(BASE, name + '.png')); print(name, c.size)
