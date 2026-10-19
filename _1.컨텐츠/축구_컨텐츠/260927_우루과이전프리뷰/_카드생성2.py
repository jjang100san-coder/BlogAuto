# -*- coding: utf-8 -*-
"""카드 07(예상 배치 다이어그램)·08(약점↔해법 매칭) 추가 생성."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "uruguay-preview", "images")
FB = "C:/Windows/Fonts/malgunbd.ttf"
FR = "C:/Windows/Fonts/malgun.ttf"

W = 1200
PAD = 70
BG = (26, 24, 24)
ACCENT = (232, 115, 90)
ROW = (43, 40, 40)
PILL = (58, 53, 53)
WHITE = (255, 255, 255)
SUB = (138, 128, 128)
GREEN = (99, 201, 138)
YELLOW = (239, 194, 92)
BLUE = (109, 168, 224)
PITCH = (34, 46, 38)
LINE = (72, 92, 78)


def F(p, s):
    return ImageFont.truetype(p, s)


def tw(d, t, f):
    return d.textbbox((0, 0), t, font=f)[2]


# ---------- 07 예상 배치 ----------
f_title = F(FB, 46)
f_sub = F(FR, 24)
f_name = F(FB, 24)
f_note = F(FB, 22)
f_foot = F(FB, 29)

PH = 880
h = 40 + 56 + 46 + PH + 36 + 82 + 40
img = Image.new("RGB", (W, h), BG)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 8], fill=ACCENT)

y = 40
t = "이렇게 나오면 약점을 찌른다"
d.text(((W - tw(d, t, f_title)) // 2, y), t, font=f_title, fill=WHITE)
y += 60
st = "내 예상이 아니라, 앞의 근거로 짜 본 배치"
d.text(((W - tw(d, st, f_sub)) // 2, y), st, font=f_sub, fill=SUB)
y += 46

px0, px1 = PAD + 60, W - PAD - 60
py0, py1 = y, y + PH
d.rounded_rectangle([px0, py0, px1, py1], radius=16, fill=PITCH)
d.rectangle([px0 + 20, py0 + 20, px1 - 20, py1 - 20], outline=LINE, width=2)
cy = (py0 + py1) // 2
d.line([px0 + 20, cy, px1 - 20, cy], fill=LINE, width=2)
d.ellipse([(px0 + px1) // 2 - 70, cy - 70, (px0 + px1) // 2 + 70, cy + 70],
          outline=LINE, width=2)
bw = 300
d.rectangle([(px0 + px1) // 2 - bw // 2, py1 - 130, (px0 + px1) // 2 + bw // 2, py1 - 20],
            outline=LINE, width=2)
d.rectangle([(px0 + px1) // 2 - bw // 2, py0 + 20, (px0 + px1) // 2 + bw // 2, py0 + 130],
            outline=LINE, width=2)


def player(cx, cy_, name, col=WHITE, ring=BLUE):
    d.ellipse([cx - 27, cy_ - 27, cx + 27, cy_ + 27], fill=ROW, outline=ring, width=3)
    d.text((cx - tw(d, name, f_name) // 2, cy_ + 36), name, font=f_name, fill=col)


L, R = px0 + 130, px1 - 130
MIDX = (px0 + px1) // 2
q1 = px0 + (px1 - px0) // 3
q2 = px0 + (px1 - px0) * 2 // 3

player(MIDX, py1 - 80, "김승규")
for cx, nm in [(L, "조현택"), (q1, "김민재"), (q2, "이한범"), (R, "설영우")]:
    player(cx, py1 - 250, nm)
for cx, nm, rg in [(L, "황희찬", GREEN), (q1, "후보 2인", SUB),
                   (q2, "황인범?", YELLOW), (R, "이강인", YELLOW)]:
    player(cx, py1 - 450, nm, ring=rg)
player(MIDX - 110, py0 + 190, "손흥민", ring=GREEN)
player(MIDX + 110, py0 + 190, "오현규?", ring=YELLOW)

# 화살표 — 이강인 안으로, 설영우 올라감
d.line([R - 30, py1 - 450, MIDX + 150, py1 - 520], fill=YELLOW, width=4)
d.polygon([(MIDX + 150, py1 - 520), (MIDX + 175, py1 - 512), (MIDX + 168, py1 - 536)],
          fill=YELLOW)
d.text((MIDX + 40, py1 - 575), "안으로 접는다", font=f_note, fill=YELLOW)
# 설영우 오버래핑 — 선수 이름을 가리지 않게 바깥쪽으로 뺀다
ax = R + 52
d.line([ax, py1 - 292, ax, py1 - 408], fill=BLUE, width=4)
d.polygon([(ax, py1 - 420), (ax - 9, py1 - 398), (ax + 9, py1 - 398)], fill=BLUE)
_wt = "폭은 풀백이 잡는다"
d.text((px1 - 44 - tw(d, _wt, f_note), py0 + 44), _wt, font=f_note, fill=BLUE)
d.text((px0 + 44, py0 + 44), "투톱이 볼란치 둘을 나눠 잡는다", font=f_note, fill=GREEN)
# 골키퍼 박스와 겹치지 않게 중원 줄 바로 아래에 둔다
_mt = "앞쪽 네 자리가 열려 있다"
d.text(((px0 + px1) // 2 - tw(d, _mt, f_note) // 2, py1 - 528), _mt, font=f_note, fill=SUB)

y = py1 + 36
d.rounded_rectangle([PAD, y, W - PAD, y + 82], radius=14, fill=ROW)
ft = "뒤는 그대로 가도, 앞은 바뀔 자리가 많다"
d.text(((W - tw(d, ft, f_foot)) // 2, y + 24), ft, font=f_foot, fill=ACCENT)
os.makedirs(OUT, exist_ok=True)
img.save(os.path.join(OUT, "07_lineup.png"))
print("07_lineup.png %dx%d" % img.size)

# ---------- 08 약점 ↔ 해법 ----------
f_h = F(FB, 27)
f_b = F(FB, 26)
rows = [("중원 핵심이 내려가면\n그 자리가 빈다",
         "투톱이 볼란치 둘을\n나눠 잡고 그 자리를 먹는다", GREEN),
        ("센터백은 발밑이 약하다",
         "쫓지 말고 센터백에게\n공을 갖게 한 뒤 압박한다", GREEN),
        ("수비가 한쪽으로\n몰아가지 못한다",
         "왼발잡이가 오른쪽에서\n안으로 접어 들어간다", YELLOW)]

rh, gap = 138, 16
h2 = 40 + 56 + 46 + len(rows) * rh + (len(rows) - 1) * gap + 36 + 82 + 40
img2 = Image.new("RGB", (W, h2), BG)
d2 = ImageDraw.Draw(img2)
d2.rectangle([0, 0, W, 8], fill=ACCENT)

y = 40
t2 = "약점 하나에 해법 하나"
d2.text(((W - tw(d2, t2, f_title)) // 2, y), t2, font=f_title, fill=WHITE)
y += 60
st2 = "왼쪽은 일본전에서 나온 지적, 오른쪽은 우리가 할 수 있는 것"
d2.text(((W - tw(d2, st2, f_sub)) // 2, y), st2, font=f_sub, fill=SUB)
y += 46

for left, right, col in rows:
    d2.rounded_rectangle([PAD, y, W - PAD, y + rh], radius=14, fill=ROW)
    d2.rounded_rectangle([PAD, y + 10, PAD + 7, y + rh - 10], radius=4, fill=col)
    d2.multiline_text((PAD + 36, y + 30), left, font=f_h, fill=SUB, spacing=12)
    cx = W // 2 + 20
    d2.line([cx - 30, y + rh // 2, cx + 18, y + rh // 2], fill=col, width=4)
    d2.polygon([(cx + 28, y + rh // 2), (cx + 12, y + rh // 2 - 9),
                (cx + 12, y + rh // 2 + 9)], fill=col)
    d2.multiline_text((cx + 60, y + 30), right, font=f_b, fill=WHITE, spacing=12)
    y += rh + gap

y += 20
d2.rounded_rectangle([PAD, y, W - PAD, y + 82], radius=14, fill=ROW)
ft2 = "셋 다 이미 이 팀이 하던 것들이다"
d2.text(((W - tw(d2, ft2, f_foot)) // 2, y + 24), ft2, font=f_foot, fill=ACCENT)
img2.save(os.path.join(OUT, "08_match_up.png"))
print("08_match_up.png %dx%d" % img2.size)
