# -*- coding: utf-8 -*-
"""4편 썸네일 다시 그리기 — 원본(_01_thumb_monthly_uv_원본.png)과 같은 판형·색.
원본은 '보류' 라벨과 '22명' 이 겹쳐서, 라벨과 숫자 사이를 띄우고 막대 최소 높이를 줬다.
숫자는 블로그 통계 순방문자 월간 화면(04_monthly_uv.png) 그대로: 7월 22 / 8월 52 / 9월 5,641."""
from PIL import Image, ImageDraw, ImageFont

FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BG, INK, SUB, LINE = (252, 252, 251), (11, 11, 11), (85, 85, 85), (221, 221, 221)
BLUE, RED = (42, 120, 214), (227, 73, 72)
W = H = 1080

def f(size, weight="Black"):
    ft = ImageFont.truetype(FONT, size); ft.set_variation_by_name(weight); return ft

im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
d.text((55, 35), "달별 순방문자", font=f(72), fill=INK)

base, top = 968, 330                     # 막대 바닥선, 9월 막대 꼭대기
data = [("7월", 22, "보류", RED), ("8월", 52, "보류", RED), ("9월", 5641, "승인", BLUE)]
xs = [98, 435, 773]; bw = 210
d.line([55, base + 2, W - 55, base + 2], fill=LINE, width=3)
for (m, v, tag, col), x in zip(data, xs):
    h = max(10, (base - top) * v / 5641)  # 22·52명은 비율대로면 거의 0 → 10px 띠로
    d.rectangle([x, base - h, x + bw, base], fill=col)
    cx = x + bw / 2
    d.text((cx, base - h - 18), f"{v:,}명", font=f(76), fill=INK, anchor="ms")
    d.text((cx, base - h - 112), tag, font=f(62), fill=col, anchor="ms")
    d.text((cx, 1050), m, font=f(64, "Bold"), fill=SUB, anchor="ms")
im.save("01_thumb_monthly_uv.png", optimize=True)
print("saved")
