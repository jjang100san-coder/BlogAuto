# -*- coding: utf-8 -*-
"""06_korea_shape.png — 10/1 추가 단락용. 한국 예상 형태(공격 4-4-2 / 수비 4-2-3-1)와 이강인·윙어의 움직임.
마커 밑에 자리별 후보 선수를 적는다(사용자 요청). 후보는 에콰도르·우루과이전 실제 선발 + 사용자 예상.
톤은 기존 03_shape.png 에서 뽑은 색 그대로(짙은 와인 + 골드)."""
import math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images", "06_korea_shape.png")
FONT = "C:/Windows/Fonts/NotoSansKR-VF.ttf"
BG, PITCH, LINE = (34, 14, 22), (42, 20, 29), (96, 62, 74)
GOLD, GK, BANNER = (238, 196, 110), (215, 205, 205), (60, 32, 43)
WHITE, GREY, ARROW = (246, 240, 238), (196, 180, 184), (255, 226, 160)
W, H = 1080, 1000

GK_N = ["조현우", "구성윤"]
BACK = [["조현택", "김태현"], ["김민재", "김태현"], ["이한범", "김민재"], ["최준"]]   # 10/1 사용자 지정
TOP = ["손흥민", "오현규"]
CM = "박진섭 · 황인범 · 이재성 중 2"


def font(size, weight=700):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def ctext(d, cx, y, s, f, fill):
    b = f.getbbox(s)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y - b[1]), s, font=f, fill=fill)


def names(d, x, y, lines, bold=False, left=False):
    """마커 밑(또는 옆)에 후보 이름을 줄마다 적는다."""
    f = font(20 if bold else 19, 700 if bold else 500)
    col = WHITE if bold else GREY
    for i, s in enumerate(lines):
        if left:
            b = f.getbbox(s)
            d.text((x - b[0], y + i * 23 - b[1]), s, font=f, fill=col)
        else:
            ctext(d, x, y + i * 23, s, f, col)


def pitch(d, x0):
    x1, y0, y1 = x0 + 440, 190, 710
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=PITCH, outline=LINE, width=2)
    cx = x0 + 220
    d.arc([cx - 75, y0 - 75, cx + 75, y0 + 75], 0, 180, fill=LINE, width=2)
    d.rectangle([x0 + 83, 612, x1 - 83, y1], outline=LINE, width=2)
    d.rectangle([x0 + 155, 668, x1 - 155, y1], outline=LINE, width=2)
    d.rectangle([cx - 40, y1 - 2, cx + 40, y1 + 6], fill=LINE)


def dot(d, x, y, color=GOLD, ring=False, r=13):
    if ring:
        d.ellipse([x - r - 7, y - r - 7, x + r + 7, y + r + 7], outline=WHITE, width=3)
    d.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=(20, 8, 12), width=1)


def ghost(d, x, y, r=13):
    d.ellipse([x - r, y - r, x + r, y + r], outline=GOLD, width=2)


def arrow(d, a, b, color=ARROW, width=4, dash=14, head=15, gap_end=20, gap_start=18):
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    sx, sy = x0 + ux * gap_start, y0 + uy * gap_start
    ex, ey = x1 - ux * gap_end, y1 - uy * gap_end
    seg = math.hypot(ex - sx, ey - sy)
    t = 0.0
    while t < seg - head:
        t2 = min(t + dash, seg - head)
        d.line([(sx + ux * t, sy + uy * t), (sx + ux * t2, sy + uy * t2)], fill=color, width=width)
        t += dash * 1.7
    px, py = -uy, ux
    base = (ex - ux * head, ey - uy * head)
    d.polygon([(ex, ey), (base[0] + px * head * 0.6, base[1] + py * head * 0.6),
               (base[0] - px * head * 0.6, base[1] - py * head * 0.6)], fill=color)


def back_and_gk(d, x0):
    dot(d, x0 + 220, 678, GK)
    names(d, x0 + 244, 667, GK_N, left=True)
    for x, nm in zip((60, 167, 273, 380), BACK):
        dot(d, x0 + x, 590)
        names(d, x0 + x, 612, nm)


im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 8], fill=GOLD)
ctext(d, W / 2, 46, "한국은 두 가지 형태를 오갈 것 같아", font(46, 800), WHITE)
ctext(d, W / 2, 116, "공격할 때 4-4-2, 수비할 때 4-2-3-1 · 10월 1일 추가한 예상", font(24, 500), GREY)

# ---- 왼쪽: 공격할 때 4-4-2
L0 = 70
pitch(d, L0)
back_and_gk(d, L0)
dot(d, L0 + 167, 500); dot(d, L0 + 273, 500)
names(d, L0 + 220, 522, [CM])
dot(d, L0 + 55, 420); names(d, L0 + 55, 442, ["김민수"], bold=True)
dot(d, L0 + 385, 420); names(d, L0 + 385, 442, ["송민규"], bold=True)
arrow(d, (L0 + 55, 420), (L0 + 42, 335), width=3, head=12, gap_end=6)      # 윙은 넓고 높게
arrow(d, (L0 + 385, 420), (L0 + 398, 335), width=3, head=12, gap_end=6)
ghost(d, L0 + 235, 410)                                                    # 수비 때 이강인 자리
arrow(d, (L0 + 235, 410), (L0 + 160, 285))
dot(d, L0 + 160, 285, ring=True); names(d, L0 + 105, 274, ["이강인"], bold=True, left=False)
dot(d, L0 + 285, 285); names(d, L0 + 285, 307, TOP)
ctext(d, L0 + 220, 730, "공격할 때 · 4-4-2", font(34, 800), GOLD)
ctext(d, L0 + 220, 778, "이강인이 톱까지 올라가 투톱, 윙은 넓게", font(22, 500), GREY)

# ---- 오른쪽: 수비할 때 4-2-3-1
R0 = 570
pitch(d, R0)
back_and_gk(d, R0)
dot(d, R0 + 167, 510); dot(d, R0 + 273, 510)
names(d, R0 + 220, 532, [CM])
dot(d, R0 + 220, 270); names(d, R0 + 245, 260, TOP, left=True)
ghost(d, R0 + 150, 285)                                                    # 공격 때 이강인 자리
arrow(d, (R0 + 150, 285), (R0 + 220, 395))
dot(d, R0 + 220, 395, ring=True); names(d, R0 + 220, 417, ["이강인"], bold=True)
ghost(d, R0 + 55, 420); ghost(d, R0 + 385, 420)                            # 공격 때 윙 자리
arrow(d, (R0 + 55, 420), (R0 + 108, 440), width=3, head=12, gap_end=16)
arrow(d, (R0 + 385, 420), (R0 + 332, 440), width=3, head=12, gap_end=16)
dot(d, R0 + 108, 440); names(d, R0 + 108, 462, ["김민수"], bold=True)
dot(d, R0 + 332, 440); names(d, R0 + 332, 462, ["송민규"], bold=True)
ctext(d, R0 + 220, 730, "수비할 때 · 4-2-3-1", font(34, 800), GOLD)
ctext(d, R0 + 220, 778, "이강인은 10번, 윙은 안으로 좁힌다", font(22, 500), GREY)

# ---- 범례 + 배너
ly = 830
dot(d, 300, ly + 12, ring=True, r=9); d.text((322, ly - 2), "움직이는 선수", font=font(21, 500), fill=GREY)
ghost(d, 500, ly + 12, r=9); d.text((520, ly - 2), "다른 단계의 자리", font=font(21, 500), fill=GREY)
arrow(d, (690, ly + 12), (760, ly + 12), width=3, head=11, gap_start=0, gap_end=0)
d.text((772, ly - 2), "움직임", font=font(21, 500), fill=GREY)
ctext(d, W / 2, 872, "※ 수비 라인: 김태현이 선발이면 김민재가 오른쪽 센터백으로 옮길 수 있다", font(21, 600), GOLD)
d.rounded_rectangle([70, 904, 1010, 982], radius=14, fill=BANNER)
ctext(d, W / 2, 927, "선수는 그대로, 이강인과 양쪽 윙의 자리만 바뀐다", font(30, 800), GOLD)

im.save(OUT)
print(OUT)
