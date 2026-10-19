# -*- coding: utf-8 -*-
"""결론 카드 card_conclusion.png — 썸네일 바로 아래 2번째 이미지(마스터 5-4: 카드는 2번째부터).
마일리지 손해노선 카드(card_routes_nov.png)와 같은 색·서체. 숫자는 base data\\나하_일별_2016-2025.csv 재계산값과 같다(초안 표 참고)."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1400, 1460
BG, INK, MUT, RED, NAVY, PINK, LINE = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#fcecec", "#e2e2e2"
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", s)
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
X0, X1 = 70, W - 70

d.text((X0, 58), "11월 하순 오키나와,", font=F(58, True), fill=INK)
d.text((X0, 134), "반팔에 얇은 겉옷 하나", font=F(58, True), fill=RED)
d.text((X0, 222), "일본 기상청 나하 관측소 2016~2025년 10년치 일별값 · 상순 1~10일 · 중순 11~20일 · 하순 21~30일", font=F(22), fill=MUT)

d.text((X0 + 10, 290), "언제", font=F(24, True), fill=NAVY)
d.text((330, 290), "10년치에서 본 것", font=F(24, True), fill=NAVY)
d.text((1010, 290), "짐", font=F(24, True), fill=NAVY)

rows = [
    ("상순", "1~10일", ["낮 최고 평균 25.3~28.0도", "30도 넘은 해 둘 (2024·2025)"], ["반팔 위주", "+ 얇은 겉옷"], False),
    ("중순", "11~20일", ["낮 최고 평균 23.1~27.5도", "해마다 갈렸어"], ["반팔과 긴팔", "섞어서"], False),
    ("하순", "21~30일", ["낮 25도 넘은 날  열흘 중 2~6일", "아침 20도 아래인 날  1~9일"], ["반팔", "+ 가디건 같은 겉옷"], True),
]
y = 336
for name, days, mid, pack, hl in rows:
    h = 190
    d.rounded_rectangle((X0, y, X1, y + h), radius=18, fill=PINK if hl else "#ffffff", outline=RED if hl else LINE, width=4 if hl else 2)
    d.text((X0 + 34, y + 44), name, font=F(54, True), fill=RED if hl else INK)
    d.text((X0 + 38, y + 118), days, font=F(24), fill=MUT)
    for i, t in enumerate(mid):
        d.text((330, y + 46 + i * 54), t, font=F(32, True if (hl or i == 0) else False), fill=INK if (hl or i == 0) else MUT)
    for i, t in enumerate(pack):
        d.text((1010, y + 46 + i * 54), t, font=F(34, True), fill=RED if hl else NAVY)
    y += h + 26

# 내가 간 날
y += 14
d.text((X0, y), "내가 간 2016년 11월", font=F(30, True), fill=NAVY); y += 58
d.rounded_rectangle((X0, y, X1, y + 230), radius=18, fill="#ffffff", outline=LINE, width=2)
d.text((X0 + 34, y + 30), "26일 오후 4시 슈리성", font=F(30, True), fill=INK)
d.text((X0 + 34, y + 80), "25.0도 · 반팔 티셔츠에 얇은 가디건", font=F(30), fill=INK)
d.text((730, y + 30), "27일 아침 7시 → 8시", font=F(30, True), fill=INK)
d.text((730, y + 80), "24.6도 → 21.1도", font=F(40, True), fill=RED)
d.text((730, y + 140), "남풍 초속 5m → 북풍 10m, 하루 비 34.5mm", font=F(26), fill=MUT)
d.line((700, y + 30, 700, y + 200), fill=LINE, width=2)
y += 230 + 40
d.text((X0 + 8, y), "직접 만든 그림 · 일본 기상청 나하 관측소 일별·시간별값으로 계산", font=F(22), fill=MUT)
d.text((X0 + 8, H - 62), "걷고읽고떠나고", font=F(22), fill="#b0b0b0")
im.save(os.path.join(HERE, "card_conclusion.png")); print(im.size, y)
