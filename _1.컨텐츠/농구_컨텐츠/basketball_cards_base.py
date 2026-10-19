# -*- coding: utf-8 -*-
"""농구 카드 공용 모듈 (2026-10-17 시안) — 「코트 카드」 양식.

축구 B 양식(팀 색 대각 면 · 각진 모서리 · 노란 띠)과 문법을 일부러 가른다.
- 색: 팀 색을 쓰지 않는다(KBL은 빨강 팀이 많아 겹친다). 시리즈 고정색 = 먹(COAL) + 볼 오렌지(ORNG) + 코트 라인 흰색(LINE), 금메달 배지에만 금색.
- 꼴: 직선·대각 대신 코트의 호·원(3점 라인·자유투 원·센터 서클), 공(솔기 있는 원), 둥근 카드 모서리. 결론은 왼쪽 정렬 오렌지 알약.
- 숫자: 유니폼 등번호처럼 겹 테두리(먹 → 흰 → 오렌지). 유니폼 모양·로고·엠블럼은 그리지 않는다(숫자 글꼴만).
- 정체성: 트레이딩 카드 — 「황금세대 12인 · No.04 / 12」 번호, 앞면(코트 도면 + 등번호) / 뒷면(신상·말·시즌 기록).
- 전술판: 농구 도해 관례 — 공격 = 번호 원, 수비 = X, 사람 움직임 = 실선, 패스 = 점선, 드리블 = 지그재그, 스크린 = 끝 가로 막대.
  (축구 전술판은 점선 = 사람, 실선 = 공 — 반대라 섞어 쓰지 않는다.)
- 기록은 공식 원값만, 계산값 없음(마스터 0-4). 사진·영상 프레임·로고 금지(6-7).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
COAL, COAL2, COAL3 = (30, 27, 26), (46, 42, 40), (66, 60, 56)
WOOD = (36, 33, 31)
ORNG, ORNG_D, ORNG_S = (234, 108, 38), (190, 80, 24), (226, 99, 32)
LINE, MUTE = (246, 241, 232), (160, 150, 142)
GOLD, GOLD_D = (218, 180, 80), (160, 124, 40)
W = 1080


def F(size, w="Black"):
    f = ImageFont.truetype(FONT, int(size)); f.set_variation_by_name(w); return f


def grain(im, amt=12):
    n = Image.effect_noise(im.size, 40).convert("L").point(lambda v: amt if v > 150 else 0)
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im.convert("RGB"), n)


def wrap(d, s, font, maxw):
    out, line = [], ""
    for ch in s:
        if d.textlength(line + ch, font=font) > maxw and line:
            cut = line.rfind(" ")
            if cut > 0: out.append(line[:cut]); line = line[cut + 1:] + ch
            else: out.append(line); line = ch
        else: line += ch
    if line: out.append(line)
    return out


# ── 작은 부품 ─────────────────────────────────────────────
def jersey(d, xy, s, size, anchor="la", shadow=True):
    """겹 테두리 숫자 — 바깥 먹, 가운데 흰, 안 오렌지. shadow = 아래로 살짝 떨어진 먹 그림자."""
    f = F(size); o1, o2 = max(6, int(size * 0.035)), max(3, int(size * 0.018))
    if shadow:
        d.text((xy[0] + size * .02, xy[1] + size * .03), s, font=f, fill=(12, 10, 10), stroke_width=o1 + o2, stroke_fill=(12, 10, 10), anchor=anchor)
    d.text(xy, s, font=f, fill=COAL, stroke_width=o1 + o2, stroke_fill=COAL, anchor=anchor)
    d.text(xy, s, font=f, fill=ORNG, stroke_width=o2, stroke_fill=LINE, anchor=anchor)


def medal(d, cx, cy, r, top="아시안게임", big="금메달"):
    d.polygon([(cx - r * .55, cy - r * 1.9), (cx - r * .05, cy - r * 1.9), (cx + r * .2, cy - r * .7), (cx - r * .3, cy - r * .7)], fill=ORNG_D)
    d.polygon([(cx + r * .05, cy - r * 1.9), (cx + r * .55, cy - r * 1.9), (cx + r * .3, cy - r * .7), (cx - r * .2, cy - r * .7)], fill=ORNG)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    d.ellipse([cx - r * .78, cy - r * .78, cx + r * .78, cy + r * .78], outline=GOLD_D, width=4)
    d.text((cx, cy - r * .18), top, font=F(r * .26, "Bold"), fill=COAL, anchor="mm")
    d.text((cx, cy + r * .2), big, font=F(r * .42), fill=COAL, anchor="mm")


def ball(d, cx, cy, r, col=ORNG, seam=COAL, w=None):
    """솔기 있는 공 — 타임라인 점·글머리표."""
    w = w or max(2, int(r * .12))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.line([cx - r, cy, cx + r, cy], fill=seam, width=w); d.line([cx, cy - r, cx, cy + r], fill=seam, width=w)
    d.arc([cx - r * 1.9, cy - r * 1.1, cx - r * .35, cy + r * 1.1], -50, 50, fill=seam, width=w)
    d.arc([cx + r * .35, cy - r * 1.1, cx + r * 1.9, cy + r * 1.1], 130, 230, fill=seam, width=w)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=seam, width=w)


def pill(d, x, y, text, size, fill=ORNG, fg=COAL):
    f = F(size); tw = d.textlength(text, font=f); h = size * 1.8
    d.rounded_rectangle([x, y, x + tw + size * 1.4, y + h], radius=h / 2, fill=fill)
    d.text((x + size * .7, y + h / 2), text, font=f, fill=fg, anchor="lm")
    return y + h


def chip(d, x, y, text, size=24, fill=COAL, fg=ORNG, outline=None, anchor="l"):
    f = F(size, "Bold"); tw = d.textlength(text, font=f); h = size * 1.7
    x0 = x if anchor == "l" else x - tw - size * 1.2
    d.rounded_rectangle([x0, y, x0 + tw + size * 1.2, y + h], radius=h / 2, fill=fill, outline=outline, width=2 if outline else 0)
    d.text((x0 + size * .6, y + h / 2), text, font=f, fill=fg, anchor="lm")


def wood(d, x0, y0, x1, y1, col=WOOD, step=36):
    for y in range(int(y0), int(y1), step): d.line([x0, y, x1, y], fill=col, width=2)


def court(d, x0, y0, w, paint=True, lw=4, col=LINE, depth=None):
    """위에서 본 하프코트(골대가 위). w = 코트 폭(15m) 픽셀, FIBA 규격 근사. depth(m)를 주면 옆줄·하프라인까지 그린다."""
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
    if depth:
        d.line([x0, y0, x0, y0 + depth * u], fill=col, width=lw); d.line([x0 + w, y0, x0 + w, y0 + depth * u], fill=col, width=lw)
        if depth >= 14:
            d.line([x0, y0 + 14 * u, x0 + w, y0 + 14 * u], fill=col, width=lw)
            d.arc([hx - 1.8 * u, y0 + 12.2 * u, hx + 1.8 * u, y0 + 15.8 * u], 180, 360, fill=col, width=lw)
    return dict(hx=hx, hy=hy, ky=ky, kx0=kx0, kx1=kx1, u=u, x0=x0, y0=y0)


def rounded_paste(im, art, xy, r):
    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, art.width - 1, art.height - 1], radius=r, fill=255)
    im.paste(art, xy, mask)


def foil(im, box, alpha=34):
    """트레이딩 카드 광택 — 대각 흰 띠 두 줄(아주 옅게)."""
    x0, y0, x1, y1 = box; ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    h = y1 - y0
    for off, wd, a in ((0.18, 120, alpha), (0.42, 40, alpha * .7)):
        sx = x0 + (x1 - x0) * off
        od.polygon([(sx, y0), (sx + wd, y0), (sx + wd - h * .55, y1), (sx - h * .55, y1)], fill=(255, 255, 255, int(a)))
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rounded_rectangle(box, radius=26, fill=255)
    ov.putalpha(Image.composite(ov.getchannel("A"), Image.new("L", im.size, 0), mask))
    return Image.alpha_composite(im.convert("RGBA"), ov)


def card_frame(H=1350):
    im = Image.new("RGB", (W, H), ORNG); d = ImageDraw.Draw(im)
    for i in range(-H, W, 46): d.line([i, 0, i + H, H], fill=ORNG_S, width=14)   # 테두리 빗결
    m = 34; d.rounded_rectangle([m, m, W - m, H - m], radius=46, fill=COAL)
    d.rounded_rectangle([m + 16, m + 16, W - m - 16, H - m - 16], radius=34, outline=COAL3, width=2)
    return im, d, m


def info_base(H, kicker, title, sub=None):
    """정보 카드 바탕 — 먹 마루 + 왼쪽 정렬 머리 + 아래 베이스라인(자유투 반원 홈)."""
    im = Image.new("RGB", (W, H), COAL); d = ImageDraw.Draw(im); wood(d, 0, 0, W, H)
    d.text((64, 64), kicker, font=F(30, "Bold"), fill=ORNG)
    d.text((60, 110), title, font=F(70), fill=LINE)
    y = 210
    if sub: d.text((64, y), sub, font=F(32, "Bold"), fill=MUTE); y += 56
    y += 18; d.line([64, y, W - 64, y], fill=ORNG, width=5)
    d.arc([W - 64 - 150, y - 75, W - 64, y + 75], 0, 180, fill=ORNG, width=5)     # 베이스라인 위 반원 홈
    return im, d, y + 40


def footer(d, H, conclusion, source, size=40):
    y = H - 84 - size * 1.8 - 22
    if conclusion: pill(d, 60, y, conclusion, size)
    d.text((64, H - 64), source, font=F(21, "Regular"), fill=MUTE)


def save(im, path):
    grain(im, 12).save(path, optimize=True); print("saved", os.path.basename(path), im.size)


# ── 1 · 네임카드 앞면 ───────────────────────────────────────
def namecard_front(path, set_name, no, number, name, role, chips, stats_label, stats, tag, source, team_line=None):
    """stats = [(값, 이름표), …] 3개. chips = 코트 위 작은 꼬리표(예: 포지션·팀)."""
    H = 1350; im, d, m = card_frame(H)
    d.text((84, 80), set_name, font=F(30, "Bold"), fill=ORNG)
    d.text((W - 84, 80), no, font=F(30), fill=LINE, anchor="ra")
    ax0, ay0, ax1, ay1 = 70, 140, W - 70, 720
    art = Image.new("RGB", (ax1 - ax0, ay1 - ay0), COAL2); ad = ImageDraw.Draw(art)
    wood(ad, 0, 0, art.width, art.height, (52, 47, 44), 34)
    g = court(ad, -60, 30, art.width + 120, lw=5)
    jersey(ad, (g["hx"], g["ky"] * 0.64), number, 320 if len(number) == 1 else 250, anchor="mm")
    rounded_paste(im, art, (ax0, ay0), 26)
    im = foil(im, (ax0, ay0, ax1, ay1)).convert("RGB"); d = ImageDraw.Draw(im)
    cx = ax0 + 24
    for c in chips:
        chip(d, cx, ay0 + 24, c, 24, fill=COAL, fg=LINE); cx += d.textlength(c, font=F(24, "Bold")) + 50
    medal(d, W - 170, ay1 - 64, 72)
    d.text((80, 736), name, font=F(140), fill=LINE)
    d.text((84, 906), role, font=F(30, "Bold"), fill=MUTE)
    d.rectangle([m + 16, 962, W - m - 16, 968], fill=ORNG)
    d.text((84, 990), stats_label, font=F(26, "Medium"), fill=MUTE)
    cw = (W - 168) / len(stats)
    for i, (v, k) in enumerate(stats):
        x = 84 + cw * i
        d.text((x, 1030), v, font=F(84), fill=ORNG if i == 0 else LINE)
        d.text((x + 4, 1132), k, font=F(26, "Medium"), fill=MUTE)
    pill(d, 84, 1186, tag, 34)
    d.text((84, H - 80), source, font=F(20, "Regular"), fill=MUTE)
    save(im, path)


# ── 2 · 네임카드 뒷면 ───────────────────────────────────────
def namecard_back(path, no, name, bio, quote, quote_src, rows_head, rows, source):
    """bio = [(이름표, 값)], rows = [(시즌, 경기, 득점, 어시스트, 꼬리표)] — 마지막 줄을 오렌지로."""
    H = 1350; im, d, m = card_frame(H)
    d.rounded_rectangle([70, 70, W - 70, 190], radius=28, fill=ORNG)
    d.text((104, 130), name, font=F(64), fill=COAL, anchor="lm")
    d.text((W - 104, 130), no, font=F(32), fill=COAL, anchor="rm")
    y = 230
    for k, v in bio:
        d.text((84, y + 8), k, font=F(26, "Medium"), fill=MUTE)
        d.text((290, y), v, font=F(36, "Bold"), fill=LINE)
        y += 68
    ball(d, W - 200, 340, 96, col=COAL2, seam=COAL3, w=6)                           # 바탕 공 무늬
    y += 30
    lines = wrap(d, quote, F(50), W - 260); qh = len(lines) * 68 + 44
    d.rounded_rectangle([84, y, 96, y + qh], radius=6, fill=ORNG)                    # 말 머리 막대
    for i, ln in enumerate(lines): d.text((126, y - 4 + i * 68), ln, font=F(50), fill=LINE)
    d.text((128, y + len(lines) * 68 + 6), quote_src, font=F(24, "Medium"), fill=MUTE)
    y += qh + 50
    d.rectangle([m + 16, y, W - m - 16, y + 6], fill=ORNG); y += 30
    fxs = (0, .34, .52, .72); x0, x1 = 84, W - 84
    for k, fx in zip(rows_head, fxs): d.text((x0 + (x1 - x0) * fx, y), k, font=F(26, "Medium"), fill=MUTE)
    y += 52
    for i, (s, g, p, a, note) in enumerate(rows):
        last = i == len(rows) - 1; fc = ORNG if last else LINE
        for v, fx in zip((s, g, p, a), fxs):
            d.text((x0 + (x1 - x0) * fx, y), v, font=F(44 if fx else 36, "Black" if fx else "Bold"), fill=fc)
        if note:
            t = F(22, "Bold"); tw = d.textlength(note, font=t)
            d.rounded_rectangle([x1 - tw - 30, y + 6, x1, y + 46], radius=20, fill=ORNG if last else COAL3)
            d.text((x1 - tw / 2 - 15, y + 26), note, font=t, fill=COAL if last else LINE, anchor="mm")
        y += 72
        if not last: d.line([x0, y - 12, x1, y - 12], fill=COAL3, width=2)
    d.text((84, H - 80), source, font=F(20, "Regular"), fill=MUTE)
    save(im, path)


# ── 3 · 센터 서클 맞대결 ────────────────────────────────────
def jumpball_vs(path, kicker, title, left_, right_, rows, conclusion, source):
    """left_/right_ = (큰 숫자, 이름, 설명). 왼쪽은 오렌지 면, 오른쪽은 먹 면, 가운데 센터 서클에 VS."""
    S = 1080; im = Image.new("RGB", (S, S), COAL); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S / 2, S], fill=ORNG); wood(d, S / 2, 0, S, S)
    for y in range(0, S, 36): d.line([0, y, S / 2, y], fill=ORNG_S, width=2)
    cy = 470; R = 150
    d.line([S / 2, 0, S / 2, S], fill=LINE, width=6)
    d.ellipse([S / 2 - R, cy - R, S / 2 + R, cy + R], outline=LINE, width=6)
    d.ellipse([S / 2 - 64, cy - 64, S / 2 + 64, cy + 64], fill=COAL, outline=LINE, width=6)
    d.text((S / 2, cy), "VS", font=F(50), fill=LINE, anchor="mm")
    d.rectangle([0, 0, S, 200], fill=COAL)
    d.text((64, 56), kicker, font=F(30, "Bold"), fill=ORNG)
    d.text((60, 100), title, font=F(62), fill=LINE)
    for side, (num, nm, ds) in ((0, left_), (1, right_)):
        x = 70 if side == 0 else S - 70; an = "ls" if side == 0 else "rs"
        fg = COAL if side == 0 else LINE
        d.text((x, 600), num, font=F(250), fill=fg, anchor=an)
        d.text((x, 666), nm, font=F(48), fill=fg, anchor=an)
        d.text((x, 712), ds, font=F(26, "Bold"), fill=(80, 36, 12) if side == 0 else MUTE, anchor=an)
    d.rectangle([0, 760, S, S], fill=COAL)
    y = 782
    for k, v in rows:
        d.text((64, y + 8), k, font=F(28, "Medium"), fill=MUTE); d.text((S - 64, y), v, font=F(40), fill=LINE, anchor="ra")
        y += 58
    footer(d, S, conclusion, source, 34)
    save(im, path)


# ── 4 · 경기 기록(박스스코어 막대) ──────────────────────────
def game_log(path, kicker, title, sub, games, avg_line, conclusion, source, scale=20, stat2="어시스트"):
    """games = [(날짜·결과, 상대, 득점, 둘째 기록, 더블더블?)]. 둘째 기록 이름은 stat2. 막대 길이는 scale 을 끝으로 한 원값 비례."""
    H = 330 + len(games) * 168 + 300; im, d, y = info_base(H, kicker, title, sub)
    bx0, bx1 = 430, W - 150
    d.text((bx0, y - 4), "득점", font=F(24, "Bold"), fill=ORNG); d.text((bx0 + 90, y - 4), stat2, font=F(24, "Bold"), fill=LINE)
    y += 44
    for when, opp, pts, ast, dd in games:
        d.text((64, y + 8), when, font=F(26, "Bold"), fill=MUTE)
        d.text((64, y + 48), opp, font=F(40 if len(opp) < 8 else 34), fill=LINE)
        for j, (v, col, hh) in enumerate(((pts, ORNG, 40), (ast, LINE, 24))):
            yy = y + 14 + j * 58; L = (bx1 - bx0) * min(v, scale) / scale
            d.rounded_rectangle([bx0, yy, bx1, yy + hh], radius=hh / 2, fill=COAL2)
            d.rounded_rectangle([bx0, yy, bx0 + max(L, hh), yy + hh], radius=hh / 2, fill=col)
            d.text((bx1 + 20, yy + hh / 2), str(v), font=F(44 if j == 0 else 32), fill=col, anchor="lm")
        if dd: chip(d, 64, y + 108, "더블더블", 20, fill=ORNG, fg=COAL)
        y += 168
        d.line([64, y - 18, W - 64, y - 18], fill=COAL3, width=2)
    d.text((64, y + 6), avg_line, font=F(34, "Bold"), fill=LINE)
    footer(d, H, conclusion, source)
    save(im, path)


# ── 5 · 공 타임라인 ─────────────────────────────────────────
def ball_timeline(path, kicker, title, sub, items, conclusion, source):
    """items = [(종류 key|step|gap, 날짜, 무엇, 곁말)]. key = 큰 공, step = 작은 공, gap = 빈 원(쉼)."""
    H = 330 + len(items) * 150 + 200; im, d, y = info_base(H, kicker, title, sub)
    lx = 110; y += 30; ys = []
    for kind, when, what, side in items:
        ys.append((y + 44, kind))
        d.text((180, y), when, font=F(28, "Bold"), fill=ORNG if kind == "key" else MUTE)
        d.text((180, y + 42), what, font=F(46), fill=LINE if kind != "gap" else MUTE)
        if side: d.text((W - 64, y + 6), side, font=F(28, "Bold"), fill=ORNG if kind == "key" else MUTE, anchor="ra")
        y += 150
    d.line([lx, ys[0][0], lx, ys[-1][0]], fill=COAL3, width=8)
    for cy, kind in ys:
        if kind == "key": ball(d, lx, cy, 34)
        elif kind == "gap": d.ellipse([lx - 22, cy - 22, lx + 22, cy + 22], fill=COAL, outline=MUTE, width=5)
        else: ball(d, lx, cy, 22, col=LINE, seam=COAL)
    footer(d, H, conclusion, source)
    save(im, path)


# ── 5-2 · 바뀐 것(원래 → 뒤) ────────────────────────────────
def change_rows(path, kicker, title, sub, head, rows, conclusion, source):
    """head = (왼쪽 이름표, 오른쪽 이름표), rows = [(항목, 원래, 바뀐 뒤)]. 가운데 작은 공이 오른쪽으로 굴러간 자리."""
    H = 370 + len(rows) * 200 + 260; im, d, y = info_base(H, kicker, title, sub)
    y += 50                                                                                       # 베이스라인 반원 홈 아래로
    d.text((64, y), head[0], font=F(26, "Bold"), fill=MUTE); d.text((W - 64, y), head[1], font=F(26, "Bold"), fill=ORNG, anchor="ra")
    y += 60
    for k, a, b in rows:
        d.text((64, y), k, font=F(40), fill=LINE)
        fa, fb = F(34, "Bold"), F(56)
        cy = y + 104
        d.text((64, cy), a, font=fa, fill=MUTE, anchor="lm")
        aw = d.textlength(a, font=fa); d.line([64, cy + 2, 64 + aw, cy + 2], fill=MUTE, width=3)      # 지나간 값은 가운데 줄
        bw = d.textlength(b, font=fb); d.text((W - 64, cy), b, font=fb, fill=ORNG, anchor="rm")
        x0, x1 = 64 + aw + 30, W - 64 - bw - 30                                                    # 그 사이를 공이 굴러간 자국
        for xx in range(int(x0), int(x1) - 40, 26): d.ellipse([xx - 3, cy - 3, xx + 3, cy + 3], fill=COAL3)
        ball(d, x1 - 16, cy, 16)
        y += 200
        d.line([64, y - 34, W - 64, y - 34], fill=COAL3, width=2)
    footer(d, H, conclusion, source)
    save(im, path)


# ── 6 · 큰 숫자(돈·기록 하나) ───────────────────────────────
def big_number(path, kicker, title, number, unit, parts, rows, conclusion, source):
    """parts = [(이름표, 표시값, 비례값)] — 캡슐 막대를 원값 비례로 나눈다(표시값은 기사 원문 그대로)."""
    S = 1200; im, d, y = info_base(S, kicker, title)
    jersey(d, (60, y + 300), number, 300, anchor="ls")
    nb = d.textbbox((60, y + 300), number, font=F(300), anchor="ls")
    d.text((nb[2] + 26, y + 290), unit, font=F(80), fill=LINE, anchor="ls")
    y += 350; tot = sum(p[2] for p in parts); x = 64; bw = W - 128; h = 54
    d.rounded_rectangle([64, y, 64 + bw, y + h], radius=h / 2, fill=COAL2)
    for i, (k, v, n) in enumerate(parts):
        L = bw * n / tot; col = ORNG if i == 0 else LINE
        d.rounded_rectangle([x, y, x + L, y + h], radius=h / 2, fill=col)
        d.text((x + (8 if i == 0 else L - 8), y + h + 22), k, font=F(26, "Medium"), fill=MUTE, anchor="la" if i == 0 else "ra")
        d.text((x + (8 if i == 0 else L - 8), y + h + 56), v, font=F(40), fill=col, anchor="la" if i == 0 else "ra")
        x += L
    y += h + 130
    for k, v in rows:
        d.text((64, y + 8), k, font=F(28, "Medium"), fill=MUTE); d.text((W - 64, y), v, font=F(40), fill=LINE, anchor="ra")
        y += 64
    footer(d, S, conclusion, source)
    save(im, path)


# ── 7 · 전술판 ──────────────────────────────────────────────
def bez(p0, p1, p2, n=40):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]


def _resample(pts, step):
    out = [pts[0]]; acc = 0
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        while acc + seg >= step:
            t = (step - acc) / seg; a = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t); out.append(a); seg = math.dist(a, b); acc = 0
        acc += seg
    if out[-1] != pts[-1]: out.append(pts[-1])
    return out


class CourtBoard:
    """농구 전술판 — 하프코트 패널을 위아래로 둘, 코트 좌표는 미터(x 0~15 왼→오, y 0 = 베이스라인, 아래로 증가)."""
    PW, DEPTH = 952, 9.6

    def __init__(self, kicker, title, sub, panels=2):
        self.u = self.PW / 15.0; self.ph = int(self.DEPTH * self.u)
        self.H = 320 + panels * (self.ph + 90) + 420
        self.im, self.d, self.y = info_base(self.H, kicker, title, sub)
        self.panels = []

    def panel(self, label):
        x0, y0 = 64, self.y + 30
        art = Image.new("RGBA", (self.PW, self.ph), COAL2 + (255,)); ad = ImageDraw.Draw(art)
        wood(ad, 0, 0, self.PW, self.ph, (52, 47, 44), 34)
        court(ad, 0, 10, self.PW, lw=4, col=LINE, depth=self.DEPTH)
        self.panels.append(dict(x0=x0, y0=y0, art=art, d=ImageDraw.Draw(art), label=label))
        self.y = y0 + self.ph + 80
        return len(self.panels) - 1

    def P(self, i, x, y): return (x * self.u, 10 + y * self.u)

    def _head(self, d, a, b, col, size=20):
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        d.polygon([b, (b[0] - size * math.cos(ang - .45), b[1] - size * math.sin(ang - .45)), (b[0] - size * math.cos(ang + .45), b[1] - size * math.sin(ang + .45))], fill=col)

    def _path(self, i, pts, ctrl):
        P = [self.P(i, *p) for p in pts]
        if ctrl is not None: return bez(P[0], self.P(i, *ctrl), P[-1])
        return P

    def cut(self, i, pts, ctrl=None, col=LINE):        # 사람 움직임 = 실선
        d = self.panels[i]["d"]; P = self._path(i, pts, ctrl); P = _shorten(P, 30)
        d.line(P, fill=COAL, width=14, joint="curve"); self._head(d, P[-2], P[-1], COAL, 30)
        d.line(P, fill=col, width=6, joint="curve"); self._head(d, P[-2], P[-1], col)

    def screen(self, i, pts, ctrl=None, col=LINE):     # 스크린 = 실선 + 끝 가로 막대
        d = self.panels[i]["d"]; P = self._path(i, pts, ctrl); P = _shorten(P, 34)
        a, b = P[-2], P[-1]; ang = math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2
        bar = [(b[0] - 24 * math.cos(ang), b[1] - 24 * math.sin(ang)), (b[0] + 24 * math.cos(ang), b[1] + 24 * math.sin(ang))]
        d.line(P, fill=COAL, width=14, joint="curve"); d.line(bar, fill=COAL, width=16)
        d.line(P, fill=col, width=6, joint="curve"); d.line(bar, fill=col, width=8)

    def pass_(self, i, pts, ctrl=None, col=LINE):       # 패스 = 점선
        d = self.panels[i]["d"]; P = _resample(_shorten(self._path(i, pts, ctrl), 30), 4)
        for k in range(0, len(P) - 6, 6): d.line([P[k], P[k + 3]], fill=COAL, width=14)
        self._head(d, P[-3], P[-1], COAL, 34)
        for k in range(0, len(P) - 6, 6): d.line([P[k], P[k + 3]], fill=col, width=6)
        self._head(d, P[-3], P[-1], col, 24)

    def dribble(self, i, pts, ctrl=None, col=LINE):     # 드리블 = 지그재그
        d = self.panels[i]["d"]; P = _resample(_shorten(self._path(i, pts, ctrl), 32), 12); Z = []
        for k in range(1, len(P) - 2):
            a, b = P[k - 1], P[k + 1]; ang = math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2; s = 9 if k % 2 else -9
            Z.append((P[k][0] + s * math.cos(ang), P[k][1] + s * math.sin(ang)))
        Z = [P[0]] + Z + [P[-2], P[-1]]
        d.line(Z, fill=COAL, width=13, joint="curve"); self._head(d, P[-2], P[-1], COAL, 32)
        d.line(Z, fill=col, width=5, joint="curve"); self._head(d, P[-2], P[-1], col, 22)

    def zone(self, i, x0, y0, x1, y1):
        art = self.panels[i]["art"]; ov = Image.new("RGBA", art.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a, b = self.P(i, x0, y0), self.P(i, x1, y1)
        od.rounded_rectangle([a, b], radius=26, fill=COAL + (120,), outline=LINE + (230,), width=4)
        for xx in range(int(a[0]) + 14, int(b[0]) - 6, 22):
            for yy in range(int(a[1]) + 14, int(b[1]) - 6, 22): od.ellipse([xx - 3, yy - 3, xx + 3, yy + 3], fill=LINE + (120,))
        self.panels[i]["art"] = Image.alpha_composite(art, ov); self.panels[i]["d"] = ImageDraw.Draw(self.panels[i]["art"])

    def o(self, i, x, y, n, ball_=False):              # 공격 = 번호 원
        d = self.panels[i]["d"]; cx, cy = self.P(i, x, y); r = 27
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORNG, outline=LINE, width=4)
        d.text((cx, cy + 1), str(n), font=F(32), fill=COAL, anchor="mm")
        if ball_: ball(d, cx + 26, cy - 26, 11, col=ORNG, seam=COAL, w=2)

    def x(self, i, x, y):                              # 수비 = X
        d = self.panels[i]["d"]; cx, cy = self.P(i, x, y); s = 16
        d.line([cx - s, cy - s, cx + s, cy + s], fill=MUTE, width=7); d.line([cx - s, cy + s, cx + s, cy - s], fill=MUTE, width=7)

    def note(self, i, x, y, text, anchor="la"):
        d = self.panels[i]["d"]; cx, cy = self.P(i, x, y)
        f = F(24, "Bold"); tw = d.textlength(text, font=f)
        x0 = cx if anchor == "la" else cx - tw - 24
        d.rounded_rectangle([x0, cy, x0 + tw + 24, cy + 40], radius=20, fill=COAL)
        d.text((x0 + 12, cy + 20), text, font=f, fill=LINE, anchor="lm")

    def finish(self, path, notes, conclusion, source):
        im = self.im
        for k, p in enumerate(self.panels):
            rounded_paste(im, p["art"].convert("RGB"), (p["x0"], p["y0"]), 26)
            d = ImageDraw.Draw(im)
            chip(d, p["x0"] + 20, p["y0"] + p["art"].height - 60, p["label"], 26, fill=ORNG, fg=COAL)
        d = ImageDraw.Draw(im); y = self.y - 20
        lg = [("실선", "사람 움직임"), ("점선", "패스"), ("지그재그", "드리블"), ("막대", "스크린")]
        x = 64
        for kind, lab in lg:
            if kind == "실선": d.line([x, y + 18, x + 54, y + 18], fill=LINE, width=6)
            elif kind == "점선":
                for k in range(0, 54, 14): d.line([x + k, y + 18, x + k + 7, y + 18], fill=LINE, width=6)
            elif kind == "지그재그": d.line([(x + k * 9, y + 18 + (8 if k % 2 else -8)) for k in range(7)], fill=LINE, width=5)
            else: d.line([x, y + 18, x + 46, y + 18], fill=LINE, width=6); d.line([x + 50, y + 2, x + 50, y + 34], fill=LINE, width=8)
            d.text((x + 66, y + 18), lab, font=F(24, "Bold"), fill=MUTE, anchor="lm"); x += 66 + d.textlength(lab, font=F(24, "Bold")) + 44
        y += 66
        for k, t in enumerate(notes):
            ball(d, 82, y + 22, 18)
            d.text((82, y + 22), "", font=F(10))
            d.text((116, y + 4), f"{k + 1}. {t}", font=F(30, "Bold"), fill=LINE); y += 56
        footer(d, self.H, conclusion, source, 36)
        save(im, path)


def _shorten(P, px):
    """양 끝을 선수 원에 닿지 않게 px 만큼 줄인다."""
    return _cut_end(_cut_end(list(P)[::-1], px)[::-1], px)


def _cut_end(P, px):
    rem = px; Q = list(P)
    while len(Q) >= 2 and rem > 0:
        a, b = Q[-2], Q[-1]; seg = math.dist(a, b)
        if seg <= rem: Q.pop(); rem -= seg
        else:
            t = (seg - rem) / seg; Q[-1] = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t); rem = 0
    return Q
