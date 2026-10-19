# -*- coding: utf-8 -*-
"""힉스필드 글자 없는 배경(_원본\\bg_*.png) 위에 정확한 숫자·글자를 얹은 인포그래픽 4장 (10/15 사용자: 「글이 많다, 인포그래픽으로」).
ig_departure.png  출국세 한눈에 / ig_refund.png 면세 4단계 / ig_map.png 도시별 숙박세 지도 / ig_route.png 1월 동선 세금
숫자 출처: base data\\*\\조사요약_*.md, 글방향_일본여행세금.md (초안 본문과 같은 값)
"""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(HERE, '_원본')
INK, MUT, RED, NAVY, BG, LINE = "#1a1a1a", "#6a6a6a", "#b9333f", "#1e3264", "#fbf6ec", "#e2dccf"
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", s)
FOOT = "직접 만든 인포그래픽 · 배경 그림은 AI 생성 · 걷고읽고떠나고"

def box(d, xy, fill="#ffffff", outline=LINE, w=2, r=18):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

# 1) 출국세 한눈에 — 위 2/3 하늘 여백에 글자
bg = Image.open(os.path.join(O, 'bg_depart.png')).convert('RGB').resize((1400, 1400), Image.LANCZOS)
d = ImageDraw.Draw(bg); X0, X1 = 80, 1320
d.text((X0, 70), "일본 출국세", font=F(60, True), fill=INK)
d.text((X0, 150), "1,000엔 → 3,000엔", font=F(76, True), fill=RED)
d.text((X0, 250), "2026년 7월 1일 일본을 떠나는 사람부터 · 1인 1회", font=F(30), fill=NAVY)
rows = [("어떻게 내나", "항공권 값에 이미 들어 있어요"), ("마일리지 표", "마일리지 항공권에도 붙어요"),
        ("면제", "24시간 안에 갈아타는 환승객 · 만 2세 미만 등"), ("예외", "7월 1일 전에 사고 출국일까지 정해 둔 표만 1,000엔")]
y = 330
for k, v in rows:
    box(d, (X0, y, X1, y + 92), fill="#fffdf8")
    d.text((X0 + 30, y + 24), k, font=F(30, True), fill=NAVY); d.text((X0 + 270, y + 24), v, font=F(30), fill=INK)
    y += 108
d.text((X0, 1355), FOOT + " · 일본 국세청·관광청 안내", font=F(20), fill=MUT)
bg.save(os.path.join(HERE, 'ig_departure.png'))

# 2) 면세 4단계 — 배경 1024x688 → 1400 폭, 위 제목·아래 설명 띠
src = Image.open(os.path.join(O, 'bg_refund.png')).convert('RGB'); s = 1400 / src.width
src = src.resize((1400, int(src.height * s)), Image.LANCZOS)
can = Image.new('RGB', (1400, 230 + src.height + 330), src.getpixel((5, 5))); can.paste(src, (0, 230)); d = ImageDraw.Draw(can)
d.text((80, 60), "11월 1일부터 일본 면세", font=F(58, True), fill=INK)
d.text((80, 140), "세금 내고 사서 → 공항에서 확인 → 돌려받기", font=F(38, True), fill=NAVY)
panels = [(12, 242), (268, 498), (524, 754), (778, 1008)]
caps = [("① 매장", "세금 포함 값으로 사요"), ("② 공항", "짐 맡기기 전 키오스크"), ("③ 판정", "그린 끝 · 레드는 세관"), ("④ 환급", "확인 뒤 소비세가 와요")]
for (a, b), (t1, t2) in zip(panels, caps):
    xa, xb = int(a * s), int(b * s); ya, yb = 230 + int(413 * s), 230 + int(492 * s)
    box(d, (xa + 4, ya, xb - 4, yb), fill="#ffffff")
    cx = (xa + xb) // 2
    d.text((cx, ya + 32), t1, font=F(30, True), fill=NAVY, anchor="mm"); d.text((cx, ya + 76), t2, font=F(24), fill=INK, anchor="mm")
y = 230 + src.height + 20
notes = ["산 다음 날부터 90일 안에 출국 · 같은 날 같은 매장 세전 5,000엔 이상",
         "소모품을 하나라도 먹거나 쓰면 그 영수증 전체가 환급 안 돼요",
         "환급 받는 방법·걸리는 날짜·수수료는 매장마다 달라요"]
for i, t in enumerate(notes):
    d.text((80, y + i * 62), "· " + t, font=F(30, i == 1), fill=RED if i == 1 else INK)
d.text((80, can.height - 50), FOOT + " · 일본 관광청·국세청 안내(2026-10-14 확인)", font=F(20), fill=MUT)
can.save(os.path.join(HERE, 'ig_refund.png'))

# 3) 숙박세 지도 — 지도 880x1168
mp = Image.open(os.path.join(O, 'bg_map.png')).convert('RGB'); k = 1.2
mp = mp.resize((int(880 * k), int(1168 * k)), Image.LANCZOS)
can = Image.new('RGB', (1400, 1720), mp.getpixel((5, 5))); MX, MY = 120, 240; can.paste(mp, (MX, MY)); d = ImageDraw.Draw(can)
d.text((80, 60), "일본 숙박세, 도시마다 달라요", font=F(56, True), fill=INK)
d.text((80, 140), "1인 1박 · 2026년 10월 14일 확인 · 2027년 1월 여행 기준", font=F(28), fill=NAVY)
P = lambda x, y: (MX + int(x * k), MY + int(y * k))
cities = [  # 이름, 지도 좌표, 박스 기준(왼쪽 x 또는 오른쪽 끝 'R'), 박스 위 y, 줄들, 색
    ("삿포로", (640, 285), 'R', 300, ["300 · 400 · 1,000엔", "2026년 4월 신설"], INK),
    ("도쿄", (588, 695), 'R', 620, ["1만 엔 미만 없음 · 100 · 200엔", "2027년 4월부터 요금의 3%"], INK),
    ("나고야", (497, 722), 'R', 860, ["없음", "공항 있는 도코나메시만 200엔"], NAVY),
    ("교토", (436, 726), 640, 1300, ["200 · 400 · 1,000 · 4,000 · 10,000엔", "2026년 3월 1일 개정"], RED),
    ("오사카", (420, 745), 80, 1520, ["5천 엔 미만 없음 · 200 · 400 · 500엔", "2025년 9월 1일 개정"], INK),
    ("후쿠오카", (172, 815), 80, 960, ["200 · 500엔"], INK),
]
for name, (x, y), bx, by, lines, col in cities:
    px, py = P(x, y)
    w = int(max(max(F(26).getlength(t) for t in lines), F(30, True).getlength(name)) + 60)
    h = 56 + 40 * len(lines)
    if bx == 'R': bx = 1360 - w
    # 점에서 박스의 가장 가까운 변 가운데까지 곧은 선
    cands = [(bx + w / 2, by), (bx + w / 2, by + h), (bx, by + h / 2), (bx + w, by + h / 2)]
    tx, ty = min(cands, key=lambda c: (c[0] - px) ** 2 + (c[1] - py) ** 2)
    d.line((px, py, tx, ty), fill=col, width=3)
    d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=col, outline="white", width=3)
    box(d, (bx, by, bx + w, by + h), fill="#ffffff", outline=col, w=3)
    d.text((bx + 28, by + 14), name, font=F(30, True), fill=col)
    for i, t in enumerate(lines): d.text((bx + 28, by + 58 + i * 40), t, font=F(26), fill=INK if i == 0 else MUT)
d.text((80, 1680), FOOT + " · 각 지자체 공식 안내 · 구간 기준은 식사·소비세 뺀 1인 1박 요금", font=F(20), fill=MUT)
can.save(os.path.join(HERE, 'ig_map.png'))

# 4) 1월 동선 — 배경 1024x688, 그림은 위쪽(138~404), 아래 여백에 칸
src = Image.open(os.path.join(O, 'bg_route.png')).convert('RGB'); s = 1400 / src.width
src = src.resize((1400, int(src.height * s)), Image.LANCZOS)
can = Image.new('RGB', (1400, 1500), src.getpixel((5, 5))); can.paste(src.crop((0, int(120 * s), 1400, int(420 * s))), (0, 230)); d = ImageDraw.Draw(can)
d.text((80, 60), "2027년 1월 13~16일, 둘이서", font=F(54, True), fill=INK)
d.text((80, 138), "일본에서 따로 붙는 세금", font=F(54, True), fill=NAVY)
top = 230 + int(300 * s) + 30
cols = [("1/13 게로 료칸", ["입탕세 300엔", "예약값에 포함", "숙박세 400엔", "체크인 때 현장"], NAVY),
        ("1/14 다카야마", ["1인 9,975엔", "1만 엔보다 25엔 적어", "숙박세 200엔", "입탕세 300엔 따로"], NAVY),
        ("1/15 나고야", ["숙박세", "없음", "", ""], NAVY),
        ("1/16 주부공항", ["출국세", "3,000엔 × 2", "항공권에 포함", "내 표 25,700원"], RED)]
W = (1400 - 160 - 3 * 20) // 4
for i, (t, lines, col) in enumerate(cols):
    x = 80 + i * (W + 20)
    box(d, (x, top, x + W, top + 520), fill="#ffffff", outline=col, w=3)
    d.text((x + W // 2, top + 46), t, font=F(30, True), fill=col, anchor="mm")
    d.line((x + 24, top + 86, x + W - 24, top + 86), fill=LINE, width=2)
    for j, ln in enumerate(lines):
        if ln: d.text((x + W // 2, top + 140 + j * 88), ln, font=F(30 if j in (0, 2) else 25, j in (0, 2)), fill=INK if j in (0, 2) else MUT, anchor="mm")
d.text((80, top + 560), "다카야마 예약 화면엔 「호텔에서 300엔 결제」 — 계산(500엔)과 달라 1월에 영수증으로 확인", font=F(26), fill=MUT)
d.text((80, 1450), FOOT + " · 게로시·다카야마시 공식 세율 · 내 예약 확인서", font=F(20), fill=MUT)
can.save(os.path.join(HERE, 'ig_route.png'))
print("ok")
