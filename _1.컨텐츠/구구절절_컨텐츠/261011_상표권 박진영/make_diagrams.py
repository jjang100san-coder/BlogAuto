# -*- coding: utf-8 -*-
"""상표권 설명용 도해 5장. 숫자·날짜는 KIPRIS·국감 영상·기사에서 확인한 것만 쓴다."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1400, 800
BG = (250, 250, 247)
INK = (30, 30, 30)
GRAY = (120, 120, 120)
BLUE = (41, 98, 255)
RED = (220, 60, 60)
GREEN = (30, 150, 90)
AMBER = (235, 150, 20)
LIGHT = (232, 236, 245)
PINK = (252, 232, 232)
MINT = (226, 245, 236)
SAND = (252, 240, 215)

def font(size, bold=False):
    name = "malgunbd.ttf" if bold else "malgun.ttf"
    return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", name), size)

F_T = font(44, True)   # 제목
F_H = font(30, True)   # 소제목
F_B = font(26)         # 본문
F_S = font(21)         # 작은 글씨
F_X = font(60, True)   # 큰 기호

def canvas(title, sub=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((60, 44), title, font=F_T, fill=INK)
    if sub:
        d.text((60, 104), sub, font=F_S, fill=GRAY)
    return im, d

def box(d, xy, fill, text, f=F_B, color=INK, radius=18, outline=None, align="center"):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3 if outline else 0)
    lines = text.split("\n")
    lh = f.size + 8
    total = lh * len(lines)
    y = y0 + (y1 - y0 - total) / 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        x = x0 + (x1 - x0 - w) / 2 if align == "center" else x0 + 24
        d.text((x, y), ln, font=f, fill=color)
        y += lh

def arrow(d, p0, p1, color=INK, width=5):
    d.line([p0, p1], fill=color, width=width)
    x0, y0 = p0; x1, y1 = p1
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    L = 18
    a = (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5))
    b = (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))
    d.polygon([p1, a, b], fill=color)

def foot(d, text):
    d.text((60, H - 48), text, font=F_S, fill=GRAY)

# ---------------- 1. 선출원주의 — 부캉이 ----------------
im, d = canvas("① 먼저 '쓴' 사람이 아니라 먼저 '낸' 사람이 가진다",
               "선출원주의 — 2026년 9~10월 부산 상어 '부캉이' 실제 사례")
# 타임라인
y = 300
d.line([(100, y), (1300, y)], fill=GRAY, width=4)
pts = [
    (160, "9/18", "북항 수로에\n상어 출현", LIGHT, INK),
    (470, "9/21~", "개인이 '부캉이'\n상표 5건 출원", PINK, RED),
    (780, "9/29", "부산시, 부캉이를\n명예홍보대사로", LIGHT, INK),
    (1090, "10/2", "부산시 뒤늦게\n출원 + 이의신청", MINT, GREEN),
]
for x, date, txt, fill, col in pts:
    d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=col)
    d.text((x - d.textlength(date, font=F_H) / 2, y - 70), date, font=F_H, fill=col)
    box(d, (x - 140, y + 40, x + 140, y + 160), fill, txt, F_B, INK)
# 핵심 문장
box(d, (100, 520, 1300, 640), SAND,
    "이름은 시민이 지었다.  그런데 종이를 먼저 낸 쪽은 개인이었다.\n"
    "→ 심사는 '누가 먼저 썼나'가 아니라 '누가 먼저 냈나'부터 본다.", F_B, INK)
foot(d, "출처: 서울신문·위키트리·경향 2026-10-02 보도. 개인 출원 5건, 지정상품 약 40개(키링·의류·봉제완구). 현재 심사 대기 중.")
im.save(os.path.join(OUT, "01_선출원주의_부캉이.png"))

# ---------------- 2. 속지주의 ----------------
im, d = canvas("② 상표는 나라마다 '따로' 산다",
               "속지주의 — 한국에서 등록해도 미국·일본에서는 효력 0")
cols = [
    ("한국", "국내 48건 (영문 37 · 한글 11)\n2025.10.1부터 출원\n5건은 2026.8.20 등록 완료\n문체부 + JYP 공동 명의", MINT, GREEN),
    ("미국", "FANOMENON 11건\n2025.11.14 출원 · 심사 보류\n출원인: JYP 단독 (KIPRIS 확인)", SAND, AMBER),
    ("일본", "FANOMENON 9건\n2026년 출원 (KIPRIS 확인)", LIGHT, INK),
    ("멕시코", "출원함 (보도)\nKIPRIS 미수록 국가", LIGHT, INK),
]
x = 90
for name, txt, fill, col in cols:
    box(d, (x, 190, x + 290, 260), fill, name, F_H, col)
    box(d, (x, 275, x + 290, 470), (255, 255, 255), txt, F_S, INK, outline=col)
    x += 315
# 벽
for xx in (395, 710, 1025):
    d.line([(xx - 12, 180), (xx - 12, 480)], fill=INK, width=6)
box(d, (100, 530, 1300, 650), PINK,
    "한국 특허청에 낸 종이는 한국 안에서만 힘이 있다.\n"
    "그래서 '국내 상표권'과 '해외 상표권'은 완전히 다른 재산이고, 국감에서 둘을 따로 따졌다.", F_B, INK)
foot(d, "출처: KIPRIS 직접 조회 — 국내 48건, 미국 11건(출원인 JYP ENTERTAINMENT CORPORATION), 일본 9건. 멕시코는 보도(Korea Times).")
im.save(os.path.join(OUT, "02_속지주의_나라별.png"))

# ---------------- 3. 개별국 vs 마드리드 ----------------
im, d = canvas("③ 해외로 나가는 길은 둘 — 각각 내기 vs 한 번에 내기",
               "개별국 직접출원(파리조약)  /  마드리드 국제출원(WIPO)")
# 왼쪽: 개별국
box(d, (90, 180, 660, 240), LIGHT, "개별국 직접출원", F_H, INK)
for i, c in enumerate(["미국", "일본", "멕시코"]):
    bx = 120 + i * 180
    box(d, (bx, 290, bx + 150, 370), (255, 255, 255), c + "\n특허청", F_S, INK, outline=GRAY)
    arrow(d, (bx + 75, 440), (bx + 75, 378))
box(d, (120, 450, 630, 520), MINT, "나라 수만큼 따로 낸다 — 서로 독립", F_S, GREEN)
# 오른쪽: 마드리드
box(d, (740, 180, 1310, 240), LIGHT, "마드리드 국제출원", F_H, INK)
box(d, (920, 560, 1130, 640), SAND, "한국 기초출원\n(뿌리)", F_S, INK, outline=AMBER)
box(d, (900, 420, 1150, 480), (255, 255, 255), "WIPO 국제사무국", F_S, INK, outline=GRAY)
arrow(d, (1025, 555), (1025, 488))
for i, c in enumerate(["미국", "일본", "멕시코"]):
    bx = 770 + i * 180
    box(d, (bx, 290, bx + 150, 370), (255, 255, 255), c, F_S, INK, outline=GRAY)
    arrow(d, (1025, 415), (bx + 75, 378))
box(d, (740, 660, 1310, 740), PINK,
    "! 5년 안에 뿌리(한국 출원)가 죽으면 가지(해외)도 같이 죽는다 = 집중공격", F_S, RED)
foot(d, "일반론. 패노메논 해외 3개국이 어느 경로였는지는 보도에 없음.")
im.save(os.path.join(OUT, "03_개별국_vs_마드리드.png"))

# ---------------- 4. 패노메논 타임라인 + 명의 ----------------
im, d = canvas("④ 패노메논 — 무슨 일이 어떤 순서로 있었나",
               "국감(2026.10.7 문체위) 질의 + KIPRIS 조회로 확인한 날짜")
y = 250
d.line([(80, y), (1320, y)], fill=GRAY, width=4)
ev = [
    (130, "2025\n9/9", "박진영\n위원장 임명", LIGHT, INK),
    (330, "10/1", "대중위\n출범 발표", LIGHT, INK),
    (530, "10/1~", "국내 출원 시작\n(JYP 단독)", PINK, RED),
    (730, "11/14", "미국 11건 출원\n(JYP 단독)", PINK, RED),
    (930, "2026\n초", "일본·멕시코\n출원", PINK, RED),
    (1110, "4/1", "국내 50%\n정부로 양도 계약", SAND, AMBER),
    (1280, "10/7", "국정감사", MINT, GREEN),
]
for x, date, txt, fill, col in ev:
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col)
    dl = date.split("\n")
    yy = y - 50 - 30 * (len(dl) - 1)
    for ln in dl:
        d.text((x - d.textlength(ln, font=F_S) / 2, yy), ln, font=F_S, fill=col); yy += 30
    box(d, (x - 80, y + 30, x + 80, y + 140), fill, txt, F_S, INK)
# 명의 현황
box(d, (100, 440, 680, 500), LIGHT, "지금 '출원인' 칸에 누가 적혀 있나", F_H, INK)
box(d, (100, 515, 680, 600), MINT, "국내 48건 → 문체부 + JYP 공동", F_B, GREEN)
box(d, (100, 615, 680, 700), PINK, "해외(미·일·멕) → JYP 단독 (보도)", F_B, RED)
box(d, (720, 440, 1300, 700), SAND,
    "박진영 본인 말(국감):\n\"미리 출원해 놓고 나중에 넘긴다든지,\n정상적이지 않은 면은 있다.\n누가 뺏길까 봐 그랬다.\"\n\n문체부 답변: 전담법인 계약서·계획 없음", F_S, INK, align="center")
foot(d, "KIPRIS: 영문 37건(10/1·10/2·10월 중순)·한글 11건(10/14·16), 16류 등은 2026.8.20 등록. 출원인 2명, 대리인 특허법인아주. 질의: 배현진 의원.")
im.save(os.path.join(OUT, "04_패노메논_타임라인.png"))

# ---------------- 5. 이름 × 류 ----------------
im, d = canvas("⑤ 상표는 '이름'이 아니라 '이름 × 칸'으로 가진다",
               "니스분류 45개 류 — 패노메논이 실제로 찍은 11칸 (영문·한글 같은 칸)")
cls = {
    "03": "화장품·샴푸", "09": "앱·전자기기", "14": "귀금속", "16": "문구·인쇄물",
    "18": "가방", "21": "컵·주방", "25": "의류·신발", "28": "완구·응원봉",
    "35": "굿즈 소매업", "38": "통신·방송", "41": "공연·교육",
}
filled = set(cls.keys())
cols_n, cell, gap = 9, 98, 10
x0, y0 = 90, 175
for i in range(45):
    n = i + 1
    r, c = divmod(i, cols_n)
    k = "%02d" % n
    x = x0 + c * (cell + gap); y = y0 + r * (cell + gap)
    if k in filled:
        d.rounded_rectangle([x, y, x + cell, y + cell], 14, fill=BLUE)
        d.text((x + 12, y + 8), k, font=F_H, fill=(255, 255, 255))
        d.text((x + 10, y + 46), cls[k], font=font(15), fill=(255, 255, 255))
    else:
        d.rounded_rectangle([x, y, x + cell, y + cell], 14, fill=(236, 236, 236))
        d.text((x + 12, y + 8), k, font=F_H, fill=(170, 170, 170))
foot(d, "파란 칸 = KIPRIS 확인 패노메논 국내 11건의 류. 1~34류 상품 / 35~45류 서비스. 회색 칸에서는 남이 같은 이름을 쓸 수 있다.")
im.save(os.path.join(OUT, "05_이름x류_11칸.png"))
print("saved 5 diagrams")
