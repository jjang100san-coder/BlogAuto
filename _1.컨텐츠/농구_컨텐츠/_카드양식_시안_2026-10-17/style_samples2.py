# -*- coding: utf-8 -*-
"""농구 네임카드 시안 2차(2026-10-17, 「조금 더 디벨롭」).
1차 공통 문법(먹색 + 볼 오렌지 + 코트 라인 흰색 · 호·원 · 둥근 알약)은 두고 깊이를 더한다.
- 등번호는 저지 숫자처럼 겹 테두리(먹 → 흰 → 오렌지). 유니폼 모양·로고 재현은 하지 않는다(숫자 글꼴만).
- 시리즈 번호 「No.04 / 12」(금메달 12명 중 4편) — 트레이딩 카드 문법.
- 기록 줄은 KBL 시즌별 원값만(계산값 없음). 바탕에 아주 옅은 결(노이즈)."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
COAL, COAL2, COAL3 = (30, 27, 26), (46, 42, 40), (64, 58, 54)
ORNG, ORNG_D = (234, 108, 38), (190, 80, 24)
LINE, MUTE = (246, 241, 232), (160, 150, 142)
GOLD, GOLD_D = (218, 180, 80), (160, 124, 40)


def F(size, w="Black"):
    f = ImageFont.truetype(FONT, int(size)); f.set_variation_by_name(w); return f


def grain(im, amt=12):
    n = Image.effect_noise(im.size, 40).convert("L").point(lambda v: amt if v > 150 else 0)
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, n)


def jersey(d, xy, s, size, anchor="la"):
    """겹 테두리 숫자 — 바깥 먹, 가운데 흰, 안 오렌지."""
    f = F(size); o1, o2 = max(6, int(size * 0.035)), max(3, int(size * 0.018))
    d.text(xy, s, font=f, fill=COAL, stroke_width=o1 + o2, stroke_fill=COAL, anchor=anchor)
    d.text(xy, s, font=f, fill=ORNG, stroke_width=o2, stroke_fill=LINE, anchor=anchor)


def medal(d, cx, cy, r):
    d.polygon([(cx - r * .55, cy - r * 1.9), (cx - r * .05, cy - r * 1.9), (cx + r * .2, cy - r * .7), (cx - r * .3, cy - r * .7)], fill=ORNG_D)
    d.polygon([(cx + r * .05, cy - r * 1.9), (cx + r * .55, cy - r * 1.9), (cx + r * .3, cy - r * .7), (cx - r * .2, cy - r * .7)], fill=ORNG)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    d.ellipse([cx - r * .78, cy - r * .78, cx + r * .78, cy + r * .78], outline=GOLD_D, width=4)
    d.text((cx, cy - r * .18), "아시안게임", font=F(r * .26, "Bold"), fill=COAL, anchor="mm")
    d.text((cx, cy + r * .2), "금메달", font=F(r * .42), fill=COAL, anchor="mm")


def court(d, x0, y0, w, paint=True, lw=4, col=LINE):
    """위에서 본 하프코트(골대가 위). w = 코트 폭(15m) 픽셀. 비율은 FIBA 규격 근사."""
    u = w / 15.0; hx, hy = x0 + w / 2, y0 + 1.575 * u
    kx0, kx1, ky = hx - 2.45 * u, hx + 2.45 * u, y0 + 5.8 * u
    if paint: d.rectangle([kx0, y0, kx1, ky], fill=ORNG)
    d.line([x0, y0, x0 + w, y0], fill=col, width=lw)
    d.rectangle([kx0, y0, kx1, ky], outline=col, width=lw)
    r = 1.8 * u; d.ellipse([hx - r, ky - r, hx + r, ky + r], outline=col, width=lw)
    R = 6.75 * u; cxl, cxr = x0 + 0.9 * u, x0 + w - 0.9 * u
    dy = math.sqrt(R * R - (hx - cxl) ** 2)
    d.line([cxl, y0, cxl, hy + dy], fill=col, width=lw); d.line([cxr, y0, cxr, hy + dy], fill=col, width=lw)
    a = math.degrees(math.atan2(dy, cxr - hx))
    d.arc([hx - R, hy - R, hx + R, hy + R], a, 180 - a, fill=col, width=lw)
    rr = 1.25 * u; d.arc([hx - rr, hy - rr, hx + rr, hy + rr], 0, 180, fill=col, width=lw)
    d.line([hx - 0.9 * u, y0 + 1.2 * u, hx + 0.9 * u, y0 + 1.2 * u], fill=col, width=lw + 2)
    d.ellipse([hx - .23 * u, hy - .23 * u, hx + .23 * u, hy + .23 * u], outline=col, width=lw)
    return dict(hx=hx, hy=hy, ky=ky, kx0=kx0, kx1=kx1, u=u)


ROWS = [("2022-23", "53", "14.1", "5.0", "우승"), ("2025-26", "38", "10.6", "4.0", ""), ("2026-27", "5", "12.2", "7.2", "개막")]
SRC = "기록: KBL 공식 홈페이지(2026년 10월 16일) · 직접 만든 이미지"
TAG = "군대를 먼저 다녀온 금메달"
ROLE = "안양 정관장 · 가드 · 동국대 · 2018 드래프트 2순위"


def stat_table(d, x0, x1, y, light=LINE):
    fxs = (0, .34, .52, .72)
    for k, fx in zip(("시즌", "경기", "득점", "어시스트"), fxs):
        d.text((x0 + (x1 - x0) * fx, y), k, font=F(26, "Medium"), fill=MUTE)
    y += 50
    for i, (s, g, p, a, note) in enumerate(ROWS):
        last = i == len(ROWS) - 1; fc = ORNG if last else light
        for v, fx in zip((s, g, p, a), fxs):
            d.text((x0 + (x1 - x0) * fx, y), v, font=F(40 if fx else 34, "Black" if fx else "Bold"), fill=fc)
        if note:
            t = F(22, "Bold"); tw = d.textlength(note, font=t)
            d.rounded_rectangle([x1 - tw - 30, y + 4, x1, y + 44], radius=20, fill=ORNG if last else COAL3)
            d.text((x1 - tw / 2 - 15, y + 24), note, font=t, fill=COAL if last else light, anchor="mm")
        y += 62
        if not last: d.line([x0, y - 10, x1, y - 10], fill=COAL3, width=2)
    return y


def pill(d, x, y, text, size):
    f = F(size); tw = d.textlength(text, font=f); h = size * 1.8
    d.rounded_rectangle([x, y, x + tw + size * 1.4, y + h], radius=h / 2, fill=ORNG)
    d.text((x + size * .7, y + h / 2), text, font=f, fill=COAL, anchor="lm")


def card_frame(W, H):
    im = Image.new("RGB", (W, H), ORNG); d = ImageDraw.Draw(im)
    for i in range(-H, W, 46): d.line([i, 0, i + H, H], fill=(226, 99, 32), width=14)   # 테두리 빗결
    m = 34; d.rounded_rectangle([m, m, W - m, H - m], radius=46, fill=COAL)
    d.rounded_rectangle([m + 16, m + 16, W - m - 16, H - m - 16], radius=34, outline=COAL3, width=2)
    return im, d, m


# C2 · 트레이딩 카드 다듬기
def c2():
    W, H = 1080, 1350; im, d, m = card_frame(W, H)
    d.text((84, 84), "황금세대 12인", font=F(30, "Bold"), fill=ORNG)
    d.text((W - 84, 84), "No.04 / 12", font=F(30), fill=LINE, anchor="ra")
    jersey(d, (W / 2 - 60, 600), "5", 560, anchor="ms")
    medal(d, W - 200, 420, 84)
    d.text((84, 640), "변준형", font=F(150), fill=LINE)
    d.text((88, 828), ROLE, font=F(30, "Bold"), fill=MUTE)
    d.rectangle([m + 16, 892, W - m - 16, 898], fill=ORNG)
    stat_table(d, 84, W - 84, 922)
    pill(d, 84, H - 178, TAG, 36)
    d.text((84, H - 84), SRC, font=F(21, "Regular"), fill=MUTE)
    grain(im, 14).save(os.path.join(OUT, "C2_트레이딩카드.png"))


# A2 · 하프코트 다듬기 — 화면 전체가 위에서 본 코트
def a2():
    S = 1080; im = Image.new("RGB", (S, S), COAL); d = ImageDraw.Draw(im)
    for y in range(0, S, 36): d.line([0, y, S, y], fill=(36, 33, 31), width=2)          # 마루 결
    g = court(d, S * 0.40, -S * 0.02, S * 0.78, lw=5)
    jersey(d, (g["hx"], g["ky"] + 30), "5", 300, anchor="mm")
    d.text((64, 70), "황금세대 12인 · No.04", font=F(30, "Bold"), fill=ORNG)
    d.text((60, 130), "변준형", font=F(132), fill=LINE)
    d.text((64, 300), "안양 정관장 · 가드", font=F(34, "Bold"), fill=LINE)
    d.text((64, 346), "동국대 · 2018 드래프트 2순위", font=F(30, "Bold"), fill=MUTE)
    medal(d, 150, 560, 66)
    for i, (k, v) in enumerate([("개막 다섯 경기", "12.2점 7.2어시스트"), ("보수 총액", "8억 원")]):
        y = 700 + i * 100
        d.rectangle([40, y - 18, S - 40, y + 78], fill=COAL)
        d.text((64, y + 16), k, font=F(30, "Medium"), fill=MUTE)
        d.text((S - 64, y + 4), v, font=F(58), fill=LINE, anchor="ra")
        d.line([64, y + 82, S - 64, y + 82], fill=COAL3, width=2)
    pill(d, 54, 924, TAG, 44)
    d.text((54, S - 44), SRC, font=F(21, "Regular"), fill=MUTE)
    grain(im, 12).save(os.path.join(OUT, "A2_하프코트.png"))


# E · 카드 + 코트 — 사진 대신 코트 도면이 카드 그림 자리에
def e():
    W, H = 1080, 1350; im, d, m = card_frame(W, H)
    ax0, ay0, ax1, ay1 = 70, 140, W - 70, 700
    art = Image.new("RGB", (ax1 - ax0, ay1 - ay0), COAL2); ad = ImageDraw.Draw(art)
    for y in range(0, art.height, 34): ad.line([0, y, art.width, y], fill=(52, 47, 44), width=2)
    g = court(ad, -60, 30, art.width + 120, lw=5)
    jersey(ad, (g["hx"], g["ky"] * 0.62), "5", 300, anchor="mm")
    mask = Image.new("L", art.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, art.width - 1, art.height - 1], radius=26, fill=255)
    im.paste(art, (ax0, ay0), mask); d = ImageDraw.Draw(im)
    d.text((84, 80), "황금세대 12인", font=F(30, "Bold"), fill=ORNG)
    d.text((W - 84, 80), "No.04 / 12", font=F(30), fill=LINE, anchor="ra")
    medal(d, W - 170, ay1 - 70, 72)
    d.text((80, 716), "변준형", font=F(140), fill=LINE)
    d.text((84, 890), ROLE, font=F(29, "Bold"), fill=MUTE)
    d.rectangle([m + 16, 946, W - m - 16, 952], fill=ORNG)
    stat_table(d, 84, W - 84, 976)
    d.text((84, H - 84), SRC, font=F(21, "Regular"), fill=MUTE)
    grain(im, 14).save(os.path.join(OUT, "E_카드속코트.png"))


if __name__ == "__main__":
    c2(); a2(); e()
    names = ("A2_하프코트.png", "C2_트레이딩카드.png", "E_카드속코트.png")
    ims = [Image.open(os.path.join(OUT, n)) for n in names]
    ims = [i.resize((int(i.width * 720 / i.height), 720)) for i in ims]
    sheet = Image.new("RGB", (sum(i.width for i in ims) + 40, 720), (255, 255, 255)); x = 0
    for i in ims: sheet.paste(i, (x, 0)); x += i.width + 20
    sheet.save(os.path.join(OUT, "_시안2차_비교.jpg"), quality=88); print("ok")
