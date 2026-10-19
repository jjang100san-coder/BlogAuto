# -*- coding: utf-8 -*-
"""기름값 글 — 일반인용 그림 12장(2026-10-14).
축: 왜 주유소 값은 늦게 내려가나(오를 땐 로켓, 내릴 땐 깃털) + 지금 값이 조용한 이유(최고가격제 = 뚜껑).
원리는 일상 비유로 심플하게(산지→도매→소매, 계단, 뚜껑 덮은 냄비, 가격표에서 덜어 낸 몫).
숫자는 기름값_공부노트_2026-10-14.md 와 base data CSV 확인분만. 계산값은 그림에 「직접 계산」 표시."""
import os, csv, math, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
# 헬퍼 원본: 예전 `..\261013_국감 이슈\make_pictures.py` — 10/14 밤 `부동산_컨텐츠\261013_LH 집값 급락 발언\`으로 옮겨짐
_cands = [os.path.join(HERE, "..", "261013_국감 이슈", "make_pictures.py"),
          os.path.join(HERE, "..", "..", "부동산_컨텐츠", "261013_LH 집값 급락 발언", "make_pictures.py")]
_src = open(next(p for p in _cands if os.path.exists(p)), encoding="utf-8").read()
# make_diagrams 를 그냥 import 하면 병역특례 그림 16장을 다시 그려 덮어쓴다 → 헬퍼 부분(「# 01」 전)만 모듈로 올린다
import sys, types
_md_path = os.path.join(HERE, "..", "261011_병역특례 논란", "make_diagrams.py")
_md_src = open(_md_path, encoding="utf-8").read()
_md = types.ModuleType("make_diagrams"); _md.__file__ = _md_path
exec(_md_src[:_md_src.index("\n# 01 ")], _md.__dict__)
sys.modules["make_diagrams"] = _md
exec(_src[:_src.index("# ---------- 01")])
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)
BASE = os.path.join(HERE, "base data")

WARN = []
def save(im, n):
    im.save(os.path.join(OUT, n)); print("saved", n)

# ---- 글자 넘침 검사용 래퍼 ----
_canvas, _box = canvas, box
def canvas(title, sub=None):
    im, d = _canvas(title, sub)
    for t, f in ((title, F_T), (sub or "", F_S)):
        if 60 + d.textlength(t, font=f) > W - 50: WARN.append(f"제목/부제 넘침: {t}")
    return im, d
def box(d, xy, fill, text, f=F_S, color=INK, **kw):
    for ln in text.split("\n"):
        if d.textlength(ln, font=f) > (xy[2] - xy[0]) - 40: WARN.append(f"상자 넘침: {ln}")
    if len(text.split("\n")) > 2: WARN.append(f"상자 세 줄: {text[:20]}")
    _box(d, xy, fill, text, f, color, **kw)
def footc(d, text):
    if 60 + d.textlength(text, font=F_S) > W - 30: WARN.append(f"근거 넘침: {text}")
    foot(d, text)

GAS = (225, 115, 25); DSL = NAVY; UP = RED; DOWN = BLUE
OIL = (60, 55, 50); GOLD = (230, 180, 40); GOLD_D = (180, 135, 20); CAPC = (110, 110, 120)
BAND = (238, 234, 222)

def rd(name):
    with open(os.path.join(BASE, name), encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def num(x):
    try: return float(x)
    except: return None
DAILY = rd("통합_일간_시계열_2025-2026.csv")

# ---- 그림 부품 ----
def dashed(d, p0, p1, col=GRAY, w=2, dash=10):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0); n = int(L // dash)
    for i in range(0, n, 2):
        a = i / n; b = min((i + 1) / n, 1)
        d.line([x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b], fill=col, width=w)
def dashed_rect(d, xy, col=GRAY, w=2):
    x0, y0, x1, y1 = xy
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): dashed(d, p, q, col, w)
def pump(d, x, yb, s=1.0, col=(200, 60, 50), screen=None, f=None):
    """주유기: 왼쪽 위 x, 바닥 yb"""
    w, h = 220 * s, 330 * s
    d.rounded_rectangle([x, yb - h, x + w, yb], radius=int(18 * s), fill=col)
    d.rectangle([x - 12 * s, yb - 14 * s, x + w + 12 * s, yb], fill=(90, 90, 90))
    d.rounded_rectangle([x + 18 * s, yb - h + 22 * s, x + w - 18 * s, yb - h + 110 * s], radius=8, fill=(25, 35, 30))
    if screen: ctext(d, x + w / 2, yb - h + 40 * s, screen, f or F_MID, (120, 255, 150))
    d.rectangle([x + 40 * s, yb - h + 140 * s, x + w - 40 * s, yb - h + 190 * s], fill=WHITE)
    # 호스와 노즐
    d.line([x + w, yb - h + 160 * s, x + w + 40 * s, yb - h + 200 * s, x + w + 40 * s, yb - 80 * s], fill=INK, width=int(7 * s))
    d.rounded_rectangle([x + w + 22 * s, yb - h + 130 * s, x + w + 60 * s, yb - h + 170 * s], radius=6, fill=INK)
def tree(d, cx, yb, s=1.0):
    d.rectangle([cx - 10 * s, yb - 70 * s, cx + 10 * s, yb], fill=(130, 90, 60))
    d.ellipse([cx - 60 * s, yb - 170 * s, cx + 60 * s, yb - 55 * s], fill=(90, 160, 90))
    for ax, ay in ((-30, -130), (15, -145), (25, -95), (-15, -90), (40, -125)):
        d.ellipse([cx + ax * s - 9 * s, yb + ay * s - 9 * s, cx + ax * s + 9 * s, yb + ay * s + 9 * s], fill=RED)
def crates(d, cx, yb, s=1.0):
    for i, (dx, dy) in enumerate(((-70, 0), (0, 0), (70, 0), (-35, -55), (35, -55))):
        x0 = cx + dx * s - 32 * s; y0 = yb + dy * s - 52 * s
        d.rectangle([x0, y0, x0 + 64 * s, y0 + 52 * s], fill=(205, 165, 110), outline=(150, 110, 70), width=3)
        for k in range(3): d.ellipse([x0 + (8 + k * 18) * s, y0 - 8 * s, x0 + (22 + k * 18) * s, y0 + 6 * s], fill=RED)
def shop(d, cx, yb, s=1.0, item=RED):
    w = 200 * s
    d.rectangle([cx - w / 2, yb - 130 * s, cx + w / 2, yb], fill=WALL)
    for k in range(6):
        d.polygon([(cx - w / 2 + k * w / 6, yb - 170 * s), (cx - w / 2 + (k + 1) * w / 6, yb - 170 * s), (cx - w / 2 + (k + 1) * w / 6, yb - 135 * s), (cx - w / 2 + k * w / 6, yb - 135 * s)], fill=RED if k % 2 == 0 else WHITE)
    d.rectangle([cx - 70 * s, yb - 40 * s, cx + 70 * s, yb - 10 * s], fill=(205, 165, 110))
    for k in range(6): d.ellipse([cx - 62 * s + k * 22 * s, yb - 58 * s, cx - 44 * s + k * 22 * s, yb - 40 * s], fill=item)
def drum(d, cx, yb, s=1.0, col=OIL):
    d.rounded_rectangle([cx - 45 * s, yb - 120 * s, cx + 45 * s, yb], radius=int(10 * s), fill=col)
    for yy in (yb - 85 * s, yb - 40 * s): d.line([cx - 45 * s, yy, cx + 45 * s, yy], fill=(140, 130, 120), width=4)
def ship(d, cx, yb, s=1.0):
    d.polygon([(cx - 130 * s, yb - 40 * s), (cx + 130 * s, yb - 40 * s), (cx + 100 * s, yb), (cx - 100 * s, yb)], fill=OIL)
    d.rectangle([cx + 50 * s, yb - 85 * s, cx + 100 * s, yb - 40 * s], fill=(235, 235, 235))
    for k in range(3): d.rounded_rectangle([cx - 110 * s + k * 52 * s, yb - 62 * s, cx - 66 * s + k * 52 * s, yb - 40 * s], radius=6, fill=(200, 70, 60))
    for k in range(5): d.arc([cx - 160 * s + k * 70 * s, yb - 6 * s, cx - 100 * s + k * 70 * s, yb + 14 * s], 0, 180, fill=BLUE, width=3)
def refinery(d, cx, yb, s=1.0):
    d.rectangle([cx - 110 * s, yb - 90 * s, cx + 20 * s, yb], fill=(150, 155, 165))
    d.rectangle([cx - 80 * s, yb - 170 * s, cx - 60 * s, yb - 90 * s], fill=(120, 125, 135))
    d.rectangle([cx - 30 * s, yb - 140 * s, cx - 12 * s, yb - 90 * s], fill=(120, 125, 135))
    for k in range(3): d.ellipse([cx - 92 * s + k * 22 * s, yb - 205 * s + k * 6 * s, cx - 52 * s + k * 22 * s, yb - 175 * s + k * 6 * s], fill=(215, 215, 215))
    for k in range(2): d.rounded_rectangle([cx + 30 * s + k * 55 * s, yb - 80 * s, cx + 78 * s + k * 55 * s, yb], radius=int(12 * s), fill=(200, 205, 210), outline=GRAY, width=2)
def jerry(d, x, yb, s=1.0, col=(200, 60, 50)):
    d.rounded_rectangle([x, yb - 110 * s, x + 80 * s, yb], radius=int(10 * s), fill=col)
    d.rounded_rectangle([x + 12 * s, yb - 130 * s, x + 50 * s, yb - 104 * s], radius=6, outline=col, width=int(7 * s))
    d.line([x + 14 * s, yb - 90 * s, x + 66 * s, yb - 20 * s], fill=(240, 120, 110), width=4)
    d.line([x + 66 * s, yb - 90 * s, x + 14 * s, yb - 20 * s], fill=(240, 120, 110), width=4)
def coin_stack(d, cx, yb, n, s=1.0):
    for k in range(n):
        y = yb - k * 13 * s
        d.ellipse([cx - 45 * s, y - 14 * s, cx + 45 * s, y + 4 * s], fill=GOLD, outline=GOLD_D, width=2)
def rocket(d, cx, cy, s=1.0, col=UP):
    d.polygon([(cx, cy - 70 * s), (cx + 22 * s, cy - 30 * s), (cx + 22 * s, cy + 40 * s), (cx - 22 * s, cy + 40 * s), (cx - 22 * s, cy - 30 * s)], fill=col)
    d.polygon([(cx - 22 * s, cy + 10 * s), (cx - 42 * s, cy + 45 * s), (cx - 22 * s, cy + 40 * s)], fill=(160, 40, 40))
    d.polygon([(cx + 22 * s, cy + 10 * s), (cx + 42 * s, cy + 45 * s), (cx + 22 * s, cy + 40 * s)], fill=(160, 40, 40))
    d.ellipse([cx - 9 * s, cy - 25 * s, cx + 9 * s, cy - 7 * s], fill=WHITE)
    d.polygon([(cx - 14 * s, cy + 42 * s), (cx + 14 * s, cy + 42 * s), (cx, cy + 80 * s)], fill=AMBER)
def feather(d, cx, cy, L=120, ang=-35, col=DOWN):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
    pts = []
    for i in range(0, 41):
        t = i / 40; w = math.sin(math.pi * t) * L * 0.18
        pts.append((cx + (t - 0.5) * L * ux + w * vx, cy + (t - 0.5) * L * uy + w * vy))
    for i in range(40, -1, -1):
        t = i / 40; w = math.sin(math.pi * t) * L * 0.18
        pts.append((cx + (t - 0.5) * L * ux - w * vx, cy + (t - 0.5) * L * uy - w * vy))
    d.polygon(pts, fill=(200, 215, 245), outline=col)
    d.line([cx - 0.62 * L * ux, cy - 0.62 * L * uy, cx + 0.5 * L * ux, cy + 0.5 * L * uy], fill=col, width=3)
def phone(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=INK)
    d.rounded_rectangle([x + 14, y + 40, x + w - 14, y + h - 40], radius=8, fill=WHITE)
def pin(d, cx, cy, col=RED, r=12):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); d.polygon([(cx - r * 0.7, cy + r * 0.5), (cx + r * 0.7, cy + r * 0.5), (cx, cy + r * 2)], fill=col)
    d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.4, cy + r * 0.4], fill=WHITE)
def gov(d, cx, yb, s=1.0):
    d.polygon([(cx - 110 * s, yb - 150 * s), (cx, yb - 200 * s), (cx + 110 * s, yb - 150 * s)], fill=(120, 130, 150))
    d.rectangle([cx - 100 * s, yb - 150 * s, cx + 100 * s, yb - 135 * s], fill=(120, 130, 150))
    for k in range(5): d.rectangle([cx - 85 * s + k * 40 * s, yb - 135 * s, cx - 65 * s + k * 40 * s, yb - 20 * s], fill=(200, 205, 215))
    d.rectangle([cx - 115 * s, yb - 20 * s, cx + 115 * s, yb], fill=(120, 130, 150))

# ============ O0 세 장면 지도 (10/15 사용자 「글이 많고 로직이 복잡」 → 흐름을 한 장으로) ============
def pot(d, cx, top, lid=False, fire=True):
    if fire:
        for k in range(5):
            fx = cx - 100 + k * 50; d.polygon([(fx - 16, top + 195), (fx + 16, top + 195), (fx, top + 158 - (k % 2) * 14)], fill=AMBER if k % 2 else RED)
    d.rounded_rectangle([cx - 130, top + 40, cx + 130, top + 165], radius=22, fill=(90, 95, 105))
    d.rectangle([cx - 155, top + 52, cx - 130, top + 68], fill=(90, 95, 105)); d.rectangle([cx + 130, top + 52, cx + 155, top + 68], fill=(90, 95, 105))
    if lid:
        d.ellipse([cx - 145, top + 14, cx + 145, top + 48], fill=CAPC); d.rounded_rectangle([cx - 24, top - 2, cx + 24, top + 20], radius=8, fill=CAPC)
    else:
        for sx in (cx - 60, cx, cx + 60):
            d.arc([sx - 12, top - 10, sx + 12, top + 14], 90, 270, fill=GRAY, width=3); d.arc([sx - 12, top - 32, sx + 12, top - 8], 270, 90, fill=GRAY, width=3)
# 10/15 v2: 「세 장면」 추상 지도가 이해 안 된다(사용자) → 실제 값과 정부 상한선을 한 그래프에
im, d = canvas("전쟁 뒤 휘발유 값은 정부 상한선을 따라 움직였다", "전국 평균 주유소 휘발유와 석유 최고가격(정유사 공급 상한), 2026년 2월 ~ 10월 13일")
D0, D1 = dt.date(2026, 2, 1), dt.date(2026, 10, 14); X0, X1, Y0, Y1 = 120, 1290, 190, 520; V0, V1 = 1600, 2080
def qx(day): return X0 + (day - D0).days / (D1 - D0).days * (X1 - X0)
def qy(v): return Y1 - (v - V0) / (V1 - V0) * (Y1 - Y0)
d.line([X0, Y1, X1, Y1], fill=(200, 198, 190), width=2)
for v in (1700, 1800, 1900, 2000):
    d.line([X0, qy(v), X1, qy(v)], fill=(235, 233, 226), width=1); d.text((X0 - 70, qy(v) - 12), f"{v:,}", font=F_SM, fill=GRAY)
for m in range(2, 11):
    xm = qx(dt.date(2026, m, 1)); d.text((xm - 12, Y1 + 8), f"{m}월", font=F_SM, fill=GRAY)
wx = qx(dt.date(2026, 2, 28)); dashed(d, (wx, Y0 - 10), (wx, Y1), RED, 2); d.text((wx - 26, Y0 - 40), "전쟁", font=F_S, fill=RED)
CAP = ((dt.date(2026, 3, 13), 1724), (dt.date(2026, 3, 27), 1934), (dt.date(2026, 6, 27), 1784), (D1, 1784))
pts = []
for k in range(len(CAP) - 1):
    (a, v), (b, _) = CAP[k], CAP[k + 1]; pts += [(qx(a), qy(v)), (qx(b), qy(v))]
for k in range(len(pts) - 1): d.line([pts[k], pts[k + 1]], fill=CAPC, width=7)
d.text((qx(dt.date(2026, 7, 20)), qy(1784) + 14), "정부 상한", font=F_M, fill=CAPC)
ser = [(dt.date.fromisoformat(r["날짜"]), num(r["국내_휘발유"])) for r in DAILY if r["날짜"] >= "2026-02-01" and num(r["국내_휘발유"])]
d.line([(qx(a), qy(v)) for a, v in ser], fill=GAS, width=5)
d.text((qx(dt.date(2026, 4, 12)), qy(2010) - 44), "주유소 휘발유", font=F_M, fill=GAS)
for k, (day, lab, dy) in enumerate(((dt.date(2026, 3, 13), "상한 시작", 1), (dt.date(2026, 3, 27), "상한 올림", -1), (dt.date(2026, 6, 27), "150원 내림", -1))):
    x = qx(day); y = qy(dict(CAP[:3])[day]) if day in dict(CAP[:3]) else qy(1784)
    d.ellipse([x - 17, y - 17, x + 17, y + 17], fill=INK); _ctext = ctext; ctext(d, x, y - 14, str(k + 1), F_SM, WHITE)
    d.text((x + 22, y + (8 if dy > 0 else -40)), lab, font=F_S, fill=INK)
d.rounded_rectangle([qx(dt.date(2026, 3, 2)), qy(1985), qx(dt.date(2026, 3, 2)) + 92, qy(1985) + 40], radius=8, fill=PINK)
ctext(d, qx(dt.date(2026, 3, 2)) + 46, qy(1985) + 6, "+206원", F_S, RED)
box(d, (90, 600, 1310, 700), SAND, "전쟁 직후 2주는 시장 그대로 리터당 206원이 뛰었다. 3월 13일 상한이 생긴 뒤로는\n주유소 값이 상한선을 따라 오르고(②), 내리고(③), 동결 뒤엔 멈췄다", F_S, INK)
footc(d, "근거: 오피넷 주유소 평균판매가 일간, 정리_석유최고가격_차수표.csv(1·2·7차, 8~10차 동결). 상한은 정유사 공급가 기준")
save(im, "O0_cap_line.png")

# ============ O1 전쟁 전 → 정점 → 지금 ============
im, d = canvas("봉우리는 넘었는데, 전쟁 전 값으로는 안 돌아왔다", "주유소 전국 평균 값, 2026년 1월 1일 ~ 10월 14일 (원/리터)")
D0 = dt.date(2026, 1, 1); D1 = dt.date(2026, 10, 14)
X0, X1, Y0, Y1, V0, V1 = 150, 990, 190, 530, 1500, 2060
def px(day): return X0 + (day - D0).days / (D1 - D0).days * (X1 - X0)
def py(v): return Y1 - (v - V0) / (V1 - V0) * (Y1 - Y0)
d.rectangle([px(dt.date(2026, 3, 13)), Y0, X1, Y1], fill=BAND)
d.text((px(dt.date(2026, 3, 13)) + 8, Y0 + 4), "최고가격제", font=F_SM, fill=GRAY)
for v in (1600, 1700, 1800, 1900, 2000):
    d.line([X0, py(v), X1, py(v)], fill=(225, 225, 220), width=1)
    d.text((X0 - 62, py(v) - 12), f"{v:,}", font=F_SM, fill=GRAY)
for m in range(1, 11):
    xm = px(dt.date(2026, m, 1)); d.text((xm - 10, Y1 + 8), f"{m}월", font=F_SM, fill=GRAY)
xw = px(dt.date(2026, 2, 28)); dashed(d, (xw, Y0), (xw, Y1), RED, 3)
d.text((xw - 52, Y0 - 30), "2/28 전쟁", font=F_SM, fill=RED)
series = {"g": [], "s": []}
for r in DAILY:
    day = dt.date.fromisoformat(r["날짜"])
    if day < D0: continue
    g, s_ = num(r["국내_휘발유"]), num(r["국내_경유"])
    if g: series["g"].append((px(day), py(g)))
    if s_: series["s"].append((px(day), py(s_)))
series["g"].append((px(D1), py(1856.43))); series["s"].append((px(D1), py(1842.58)))  # 10/14 오피넷 API
d.line(series["s"], fill=DSL, width=3); d.line(series["g"], fill=GAS, width=4)
for (day, v, lab, dx, dy) in ((dt.date(2026, 2, 27), 1692.58, "1,693", -75, 6), (dt.date(2026, 5, 10), 2011.90, "2,012", -30, -42), (D1, 1856.43, "1,856", -30, -44)):
    x, y = px(day), py(v); d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=GAS, outline=WHITE, width=2)
    d.text((x + dx, y + dy), lab, font=F_M, fill=GAS)
LX = px(dt.date(2026, 8, 1))
d.line([LX, Y1 - 90, LX + 40, Y1 - 90], fill=GAS, width=5); d.text((LX + 48, Y1 - 103), "휘발유", font=F_S, fill=INK)
d.line([LX, Y1 - 55, LX + 40, Y1 - 55], fill=DSL, width=4); d.text((LX + 48, Y1 - 68), "경유", font=F_S, fill=INK)
d.rounded_rectangle([1040, 200, 1320, 520], radius=16, fill=PINK)
ctext(d, 1180, 225, "휘발유, 지금도", F_M, INK); ctext(d, 1180, 262, "전쟁 전보다", F_S, GRAY)
ctext(d, 1180, 300, "+164원", F_BIG, RED)
ctext(d, 1180, 400, "경유는", F_S, GRAY); ctext(d, 1180, 432, "+245원", F_MID, DSL)
box(d, (90, 600, 1310, 700), SAND, "5월 정점에서 휘발유는 155원 내렸지만 전쟁 전보다 아직 164원 비싸다. 9월부터는 거의 움직이지도 않는다.\n왜 이렇게 천천히 내려오고, 왜 지금은 이렇게 조용할까", F_S, INK)
footc(d, "근거: 공부노트 §2-2, 오피넷 주유소 평균판매가격 일간[2](~10/13)·오픈API 10/14[1]. 차이는 직접 계산")
save(im, "O1_peak_and_now.png")

# ============ O2 50리터 가득 ============
im, d = canvas("50리터 가득 넣으면, 전쟁 전보다 8,193원 더", "주유소 전국 평균 휘발유 값으로 50리터를 넣을 때 (직접 계산)")
pump(d, 170, 520, 1.0, (120, 140, 160), "84,629원", F_N)
ctext(d, 280, 535, "전쟁 직전 (2월 27일)", F_M, INK); ctext(d, 280, 568, "리터당 1,692.58원", F_S, GRAY)
pump(d, 640, 520, 1.0, (200, 70, 55), "92,822원", F_N)
ctext(d, 750, 535, "지금 (10월 14일)", F_M, INK); ctext(d, 750, 568, "리터당 1,856.43원", F_S, GRAY)
arrow(d, (450, 300), (600, 300), RED, 6)
d.rounded_rectangle([1000, 210, 1320, 400], radius=16, fill=PINK)
ctext(d, 1160, 228, "휘발유 50리터", F_M, INK); ctext(d, 1160, 275, "+8,193원", F_BIG, RED)
d.rounded_rectangle([1000, 420, 1320, 560], radius=16, fill=LIGHT)
ctext(d, 1160, 438, "경유 50리터", F_M, INK); ctext(d, 1160, 478, "+12,267원", F_MID, DSL)
box(d, (90, 600, 1310, 700), SAND, "리터당 164원 차이가 한 번 가득 넣을 때 8천 원이 넘는 돈이 된다.\n경유는 리터당 245원이 올라 같은 50리터에 1만 2천 원이 넘게 더 든다", F_S, INK)
footc(d, "근거: 공부노트 §0·§2-2(오피넷 일간[2]·API[1]). 50리터 금액은 평균값 × 50, 원 단위 반올림 — 직접 계산")
save(im, "O2_fifty_liters.png")

# ============ O3 두 번 넘겨지는 값 ============
im, d = canvas("기름값은 과일값처럼 두 번 넘겨져서 온다", "산지 → 도매 → 동네 가게. 기름도 같은 길을 걷는다")
cols = [230, 700, 1170]
tree(d, cols[0], 300, 0.85); crates(d, cols[1], 300, 0.9); shop(d, cols[2], 300, 0.85)
for x, t in zip(cols, ("산지(과수원)", "도매시장", "동네 과일가게")): ctext(d, x, 308, t, F_M, INK)
ship(d, cols[0], 530, 0.9); refinery(d, cols[1] + 20, 530, 0.8); pump(d, cols[2] - 55, 530, 0.45, (200, 70, 55))
for x, t in zip(cols, ("국제 값(싱가포르)", "정유사 공급가", "주유소 판매가")): ctext(d, x, 543, t, F_M, NAVY)
for k, (a, b) in enumerate(((cols[0] + 140, cols[1] - 140), (cols[1] + 140, cols[2] - 140))):
    for y in (230, 470): arrow(d, (a, y), (b, y), GRAY, 6)
    d.ellipse([(a + b) / 2 - 22, 328, (a + b) / 2 + 22, 372], fill=AMBER); ctext(d, (a + b) / 2, 332, str(k + 1), F_M, WHITE)
box(d, (90, 600, 1310, 700), SAND, "국제 값이 움직이면 정유사가 주유소에 넘기는 값(공급가)이 따라가고, 주유소가 그걸 판매가에 옮긴다.\n넘겨지는 곳이 둘이라, 늦어질 수 있는 자리도 둘이다", F_S, INK)
footc(d, "근거: 공부노트 §3-0(오피넷 국제 제품가[5] · 정유사 공급가[3] · 주유소 판매가[2]). 그림은 비유")
save(im, "O3_two_handoffs.png")

# ============ O4 1리터 쪼개기 ============
im, d = canvas("휘발유 1리터 1,857원, 그중 796원이 세금", "전국 평균 휘발유 1리터를 네 몫으로 나누면 (원/리터)")
parts = [("정유사", 983.05, (150, 155, 165)), ("유류세", 634.50, (90, 150, 110)), ("부가세", 161.76, (140, 190, 150)), ("주유소", 78.14, AMBER)]
BX0, BX1 = 110, 1290; tot = sum(v for _, v, _ in parts); x = BX0
segs = []
for lab, v, col in parts:
    w = (BX1 - BX0) * v / tot; d.rectangle([x, 290, x + w, 400], fill=col); segs.append((x, x + w, lab, v)); x += w
for x0, x1, lab, v in segs:
    cx = (x0 + x1) / 2
    if x1 - x0 > 140:
        ctext(d, cx, 310, lab, F_M, WHITE); ctext(d, cx, 348, f"{v:,.0f}원", F_M, WHITE)
    else:
        ctext(d, cx, 410, lab, F_S, INK); ctext(d, cx, 438, f"{v:,.0f}", F_S, INK)
tx0, tx1 = segs[1][0], segs[2][1]
d.line([tx0, 270, tx0, 255, tx1, 255, tx1, 270], fill=RED, width=4)
ctext(d, (tx0 + tx1) / 2, 190, "세금 796원", F_MID, RED)
d.text((BX0, 245), "1,857원", font=F_M, fill=INK)
dashed(d, (BX0, 470), (BX1, 470), (200, 200, 195), 2)
d.text((BX0, 490), "세금은 리터당 정해진 금액이 커서, 바깥 값이 뛰어도 주유소 값은 덜 뛴다", font=F_M, fill=NAVY)
box(d, (90, 600, 1310, 700), SAND, "전쟁 뒤 두바이유는 전쟁 전의 2.4배까지 갔지만, 주유소 휘발유는 정점에서도 1.19배였다.\n세금 덩어리가 완충재 노릇을 한 셈이다", F_S, INK)
footc(d, "근거: 공부노트 §4-1(정유사 공급가 9월 5주[3], 판매가 10월 1주[2]), §2-1·2-2. 배수는 직접 계산")
save(im, "O4_one_liter.png")

# ============ O5 오를 때 3주, 내릴 때 6주 (10/16 마스터 3-1: 계단 비유 → 주 막대) ============
im, d = canvas("오를 땐 3주, 내릴 땐 6주 — 주유소 값이 원가를 따라가기까지", "경제학에서 「로켓과 깃털」이라 부르는 모양 — 오를 땐 로켓처럼, 내릴 땐 깃털처럼")
XS = 300; WK = 150
for w in range(7):
    x = XS + w * WK
    d.line([x, 205, x, 520], fill=(225, 220, 212), width=2)
    if w: ctext(d, x, 530, f"{w}주", F_S, GRAY)
for y, lab, n, col in ((250, "오를 때", 3, UP), (410, "내릴 때", 6, DOWN)):
    ctext(d, 185, y + 8, lab, F_MID, col)
    d.rounded_rectangle([XS, y, XS + n * WK, y + 60], radius=16, fill=col)
    ctext(d, XS + n * WK / 2, y + 8, f"{n}주", F_MID, WHITE)
rocket(d, XS + 3 * WK + 70, 280, 0.75, UP)
feather(d, XS + 6 * WK + 60, 430, 100, -30, DOWN)
box(d, (90, 610, 1310, 700), SAND, "원가가 오르면 주유소 휘발유는 3주 만에 거의 다 따라 오르는데, 내릴 땐 6주가 걸렸다.\n결국 다 내려오긴 한다. 다만 늦다", F_S, INK)
footc(d, "근거: 공부노트 §3-1(주유소 단계, 2018~2026.2 주간 416주, 90% 넘게 따라간 시점) — 직접 계산")
save(im, "O5_stairs.png")

# ============ O6 실측 곡선 ============
im, d = canvas("3주 뒤, 오를 땐 94% 따라왔고 내릴 땐 68%만", "정유사 공급가가 움직인 뒤 주유소 값이 몇 %를 따라왔나 — 2018년 1월 ~ 2026년 2월, 416주")
LOG = {"g": ([30.8, 65.6, 78.9, 94.4, 103.9, 103.1, 99.9, 107.1, 112.3], [20.3, 47.6, 61.2, 68.4, 79.6, 89.2, 96.4, 100.5, 102.9]),
       "s": ([32.3, 70.1, 84.1, 94.9, 98.5, 95.8, 90.5, 95.6, 99.4], [9.3, 25.9, 41.2, 52.7, 67.1, 77.2, 86.3, 93.1, 98.7])}
for pi_, (key, name, col) in enumerate((("g", "휘발유", GAS), ("s", "경유", DSL))):
    px0, px1, py0, py1 = 140 + pi_ * 640, 600 + pi_ * 640, 210, 520
    def gx(w): return px0 + w / 8 * (px1 - px0)
    def gy(v): return py1 - v / 115 * (py1 - py0)
    d.text((px0, 165), name, font=F_H, fill=col)
    d.rectangle([gx(2.6), py0, gx(3.4), py1], fill=BAND)
    d.line([px0, py1, px1, py1], fill=INK, width=2); d.line([px0, py0, px0, py1], fill=INK, width=2)
    dashed(d, (px0, gy(100)), (px1, gy(100)), GRAY, 2); d.text((px0 - 58, gy(100) - 12), "100%", font=F_SM, fill=GRAY)
    d.text((px0 - 44, gy(50) - 12), "50%", font=F_SM, fill=GRAY)
    for w, lab in ((0, "그 주"), (3, "3주 뒤"), (6, "6주 뒤"), (8, "8주")):
        ctext(d, gx(w), py1 + 8, lab, F_SM, GRAY)
    upv, dnv = LOG[key]
    d.line([(gx(i), gy(v)) for i, v in enumerate(upv)], fill=UP, width=4)
    d.line([(gx(i), gy(v)) for i, v in enumerate(dnv)], fill=DOWN, width=4)
    for i in range(9):
        for v, c in ((upv[i], UP), (dnv[i], DOWN)): d.ellipse([gx(i) - 5, gy(v) - 5, gx(i) + 5, gy(v) + 5], fill=c)
    u3, d3 = upv[3], dnv[3]
    d.ellipse([gx(3) - 10, gy(u3) - 10, gx(3) + 10, gy(u3) + 10], fill=UP, outline=WHITE, width=3)
    d.ellipse([gx(3) - 10, gy(d3) - 10, gx(3) + 10, gy(d3) + 10], fill=DOWN, outline=WHITE, width=3)
    d.text((gx(3) - 80, gy(u3) - 50), f"{u3:.0f}%", font=F_MID, fill=UP)
    d.text((gx(3) + 18, gy(d3) + 2), f"{d3:.0f}%", font=F_MID, fill=DOWN)
d.line([1010, 172, 1050, 172], fill=UP, width=5); d.text((1058, 158), "오를 때", font=F_S, fill=INK)
d.line([1160, 172, 1200, 172], fill=DOWN, width=5); d.text((1208, 158), "내릴 때", font=F_S, fill=INK)
box(d, (90, 600, 1310, 700), SAND, "같은 원가 변화라도 내릴 때는 주유소 값이 늦게 따라온다. 경유는 더 느려 3주 뒤 절반을 조금 넘었다.\n이 차이는 주유소 단계에서 뚜렷했고, 정유사 단계에선 통계로 보이지 않았다", F_S, INK)
footc(d, "근거: 공부노트 §3-1·3-2, base data 계산_로켓깃털_전쟁주제외_로그.txt(오피넷 주간[2][3][5]) — 직접 계산(비대칭 분포시차 모형)")
save(im, "O6_rocket_feather_curve.png")

# ============ O7 내 돈으로 ============
im, d = canvas("같은 100원인데, 3주 뒤 50리터에 1,300원 차이", "정유사 공급가가 리터당 100원 오를 때와 내릴 때, 3주 뒤 주유소 휘발유 (100원은 가정, 직접 계산)")
SC = 2.8
for k, (lab, v, col, money, arr) in enumerate((("100원 오르면", 94.4, UP, "50리터면 4,720원 더", "up"), ("100원 내리면", 68.4, DOWN, "50리터면 3,420원 덜", "down"))):
    cx = 300 + k * 420; yb = 500
    ctext(d, cx, 165, lab, F_H, col)
    dashed_rect(d, (cx - 70, yb - 100 * SC, cx + 70, yb), GRAY, 2)
    d.rectangle([cx - 70, yb - v * SC, cx + 70, yb], fill=col)
    ctext(d, cx, yb - v * SC + 14, f"{v:.0f}원", F_MID, WHITE)
    if arr == "up": up_arrow(d, cx + 120, yb, 200, UP)
    else: down_arrow(d, cx + 120, yb - 200, 200, DOWN)
    ctext(d, cx, yb + 14, "3주 뒤 리터당", F_S, GRAY)
    ctext(d, cx, yb + 44, money, F_M, col)
d.text((455, 478), "점선 = 100원 전부", font=F_SM, fill=GRAY)
d.rounded_rectangle([1010, 220, 1320, 520], radius=16, fill=PINK)
ctext(d, 1165, 240, "50리터 한 번에", F_M, INK); ctext(d, 1165, 290, "1,300원", F_BIG, RED)
ctext(d, 1165, 380, "경유는", F_S, GRAY); ctext(d, 1165, 412, "2,110원", F_MID, DSL)
box(d, (90, 610, 1310, 700), SAND, "오를 땐 3주 만에 거의 다 따라 오르고, 내릴 땐 3주가 지나도 리터당 32원이 아직 덜 내려와 있다.\n6주쯤 지나면 둘이 거의 같아진다 — 깃털은 결국 바닥에 닿는다", F_S, INK)
footc(d, "근거: 공부노트 §3-1(3주 뒤 휘발유 94.4%·68.4%, 경유 94.9%·52.7%) × 100원 × 50리터 — 직접 계산")
save(im, "O7_my_fifty_liters.png")

# ============ O8 작년 6월 12일 전쟁 ============
im, d = canvas("작년 6월, 주유소는 오를 때 덜 남기고 내릴 때 되찾았다", "2025년 6월 이스라엘-이란 「12일 전쟁」 때 주유소 몫(판매가 - 정유사 공급가), 휘발유 원/리터")
weeks = [("공습 직전", "6월 2주", 45.77), ("휴전 발표 주", "6월 4주", 27.48), ("한 달 뒤", "7월 4주", 74.25)]
xs = [230, 700, 1170]
for x, (a, b, v) in zip(xs, weeks):
    n = round(v / 5); coin_stack(d, x, 500, n, 1.0)
    ctext(d, x, 500 - n * 13 - 62, f"{v:.0f}원", F_MID, INK)
    ctext(d, x, 518, a, F_M, INK); ctext(d, x, 552, b, F_S, GRAY)
arrow(d, (340, 300), (560, 230), UP, 6); ctext(d, 450, 190, "공급가 +54원", F_M, UP)
arrow(d, (820, 230), (1040, 300), DOWN, 6); ctext(d, 930, 190, "공급가 -43원", F_M, DOWN)
box(d, (90, 610, 1310, 700), SAND, "원가가 오를 땐 판매가를 바로 다 못 올려 남는 몫이 줄고, 원가가 내릴 땐 값을 천천히 내려 그 몫을 되찾았다.\n국제 값은 6월 말 전쟁 전보다 낮아졌는데, 주유소 휘발유는 7월 25일에도 40원 오른 그대로였다", F_S, INK)
footc(d, "근거: 공부노트 §3-3(오피넷 주간[2][3], 일간[2][5]). 주유소 몫·차이는 직접 계산. 동전 1개 = 약 5원(모식)")
save(im, "O8_june_2025.png")

# ============ O9 뚜껑 덮은 냄비 ============
im, d = canvas("지금 값이 조용한 이유 — 냄비에 뚜껑이 덮였다", "석유 최고가격제: 정유사가 주유소에 넘기는 값에 정부가 상한을 씌웠다 (2026년 3월 13일부터)")
pcx = 300
for k in range(5):
    fx = pcx - 120 + k * 60; d.polygon([(fx - 22, 545), (fx + 22, 545), (fx, 480 - (k % 2) * 25)], fill=AMBER if k % 2 else RED)
d.rounded_rectangle([pcx - 170, 330, pcx + 170, 500], radius=26, fill=(90, 95, 105))
d.rectangle([pcx - 200, 345, pcx - 170, 365], fill=(90, 95, 105)); d.rectangle([pcx + 170, 345, pcx + 200, 365], fill=(90, 95, 105))
ctext(d, pcx, 395, "국제 값", F_H, WHITE)
d.ellipse([pcx - 190, 296, pcx + 190, 340], fill=CAPC); d.rounded_rectangle([pcx - 30, 276, pcx + 30, 302], radius=10, fill=CAPC)
ctext(d, pcx, 228, "뚜껑(상한) 휘발유 1,784원", F_M, INK)
for sx in (pcx - 210, pcx + 200):
    d.arc([sx - 15, 250, sx + 15, 280], 90, 270, fill=GRAY, width=3); d.arc([sx - 15, 222, sx + 15, 252], 270, 90, fill=GRAY, width=3)
# 오른쪽: 9월 흔들림 두 줄 (같은 % 눈금)
sep = [r for r in DAILY if r["날짜"].startswith("2026-09")]
dub = [(r["날짜"], num(r["두바이_$"])) for r in sep if num(r["두바이_$"])]
gas = [(r["날짜"], num(r["국내_휘발유"])) for r in sep if num(r["국내_휘발유"])]
def strip(vals, y_mid, col, lab):
    b = vals[0][1]; n = len(vals)
    pts = [(640 + i / (n - 1) * 520, y_mid - (v / b - 1) * 100 * 4.2) for i, (_, v) in enumerate(vals)]
    d.line([640, y_mid, 1160, y_mid], fill=(220, 220, 215), width=1)
    d.line(pts, fill=col, width=4); d.text((640, y_mid - 150 if col == OIL else y_mid - 60), lab, font=F_M, fill=col)
dlo, dhi = min(v for _, v in dub), max(v for _, v in dub)
strip(dub, 400, OIL, "바깥: 두바이유")
strip(gas, 520, GAS, "주유소 휘발유")
ctext(d, 1250, 290, f"+{(dhi / dlo - 1) * 100:.0f}%", F_MID, OIL); ctext(d, 1250, 332, "한 달 출렁임", F_SM, GRAY)
ctext(d, 1250, 470, "4.24원", F_MID, GAS); ctext(d, 1250, 512, "한 달 최고-최저", F_SM, GRAY)
d.text((640, 556), "9월 1일 ~ 30일, 같은 % 눈금", font=F_SM, fill=GRAY)
box(d, (90, 600, 1310, 700), SAND, "상한은 정유사가 주유소에 넘기는 값에만 씌웠다. 6월 27일 150원 내린 뒤 8·9·10차 내리 동결이라,\n바깥 값이 크게 출렁인 9월에도 주유소 휘발유는 한 달 동안 4.24원 안에서만 움직였다", F_S, INK)
footc(d, "근거: 공부노트 §0·§1-1, 정리_석유최고가격_차수표.csv[19][23][24][25], 오피넷 일간[2][4]. 출렁임 %는 직접 계산")
save(im, "O9_lid_on_pot.png")

# ============ O10 뚜껑 아래 빈칸 ============
im, d = canvas("상한 아래 차액은 나랏돈이 메운다", "국제 휘발유 값과 정유사 휘발유 공급가(세금 빼고) 비교, 원/리터")
yb = 520; S = 0.26
def col_bar(x, v, col, lab):
    d.rectangle([x - 55, yb - v * S, x + 55, yb], fill=col); ctext(d, x, yb - v * S - 34, f"{v:,.0f}", F_M, col); ctext(d, x, yb + 10, lab, F_S, INK)
col_bar(220, 713.71, OIL, "국제"); col_bar(350, 775.06, (150, 155, 165), "정유사")
col_bar(640, 1231.74, OIL, "국제"); col_bar(770, 982.58, (150, 155, 165), "정유사")
ctext(d, 285, 562, "전쟁 직전 (2월 4주)", F_M, GRAY); ctext(d, 705, 562, "지금 (9월 5주)", F_M, INK)
d.line([110, yb, 860, yb], fill=INK, width=2)
gtop, gbot = yb - 1231.74 * S, yb - 982.58 * S
dashed_rect(d, (715, gtop, 825, gbot), RED, 3)
for k in range(4): d.ellipse([735, gbot - 16 - k * 14, 805, gbot - 2 - k * 14], fill=GOLD, outline=GOLD_D, width=2)
d.text((835, gtop + 14), "차액", font=F_M, fill=RED)
ctext(d, 350, yb - 775.06 * S - 72, "+61원", F_M, GRAY)
gov(d, 1080, 470, 0.9)
ctext(d, 1080, 482, "정부 예비비", F_M, INK)
arrow(d, (960, 350), (840, 350), GOLD_D, 6)
d.rounded_rectangle([1180, 180, 1330, 300], radius=14, fill=PINK)
ctext(d, 1255, 196, "리터당", F_S, INK); ctext(d, 1255, 228, "249원", F_MID, RED)
box(d, (90, 600, 1310, 700), SAND, "평소엔 정유사 값이 국제 값보다 조금 비쌌다(운송·정제 몫). 지금은 상한 때문에 249원 싸게 넘기고,\n그 차이는 정부가 예비비로 정유사에 메워 준다. 정유사 공급가는 정유사가 보고한 값이다", F_S, INK)
footc(d, "근거: 공부노트 §4-5(오피넷 정유사 공급가[3] — 정유사 보고치, 싱가포르 휘발유[5]), 손실보전 [20][25]. 차이는 직접 계산")
save(im, "O10_gap_filled.png")

# ============ O11 가격표에서 덜어 낸 몫 ============
im, d = canvas("유류세가 65원, 환율이 78원을 덜어 냈다", "전쟁 직전과 지금 사이, 휘발유 값에서 빠진 두 몫 (원/리터)")
d.polygon([(130, 340), (210, 230), (760, 230), (760, 470), (210, 470)], fill=SAND, outline=GOLD_D)
d.ellipse([175, 330, 205, 360], fill=BG, outline=GOLD_D, width=3)
ctext(d, 490, 270, "지금 휘발유", F_M, GRAY); ctext(d, 490, 310, "1,856원", F_HUGE, INK)
dashed(d, (790, 220), (790, 490), GRAY, 3)
d.rounded_rectangle([830, 230, 1010, 340], radius=12, fill=(90, 150, 110)); ctext(d, 920, 244, "유류세", F_M, WHITE); ctext(d, 920, 282, "-65원", F_MID, WHITE)
d.rounded_rectangle([830, 360, 1010, 470], radius=12, fill=BLUE); ctext(d, 920, 374, "환율", F_M, WHITE); ctext(d, 920, 412, "-78원", F_MID, WHITE)
d.text((1030, 260), "판매가에서 바로", font=F_M, fill=INK); d.text((1030, 296), "인하율 7% → 15%", font=F_S, fill=GRAY)
d.text((1030, 390), "국제 값에서", font=F_M, fill=INK); d.text((1030, 426), "1,424.5원 → 1,335.8원", font=F_S, fill=GRAY)
box(d, (90, 600, 1310, 700), SAND, "유류세는 3월 27일 인하 폭을 넓혀 판매가에서 리터당 65원을 바로 뺐다.\n환율이 내려 국제 휘발유 값이 원화로 78원 싸졌다. 다만 지금은 상한이 값을 정해 그대로 옮겨 가진 않는다", F_S, INK)
footc(d, "근거: 공부노트 §4-1·4-3·4-4(정부 발표[32], 오피넷 세금 내역[3], ECOS 환율[6], 싱가포르 휘발유[5]). 환율 몫은 직접 계산")
save(im, "O11_cut_from_tag.png")

# ============ O12 할 일 하나 ============
im, d = canvas("할 일 하나 — 주유 전에 오피넷 「내 주변」 최저가 한 번 보기", "같은 날에도 지역마다, 주유소마다 값이 다르다")
phone(d, 160, 160, 300, 420)
d.rectangle([174, 200, 446, 240], fill=NAVY); ctext(d, 310, 206, "내 주변 · 가격순", F_S, WHITE)
for k, wbar in enumerate((90, 130, 160, 200)):
    y = 265 + k * 70
    pin(d, 200, y + 6, GREEN if k == 0 else GRAY, 11)
    d.rounded_rectangle([225, y, 225 + 120, y + 14], radius=7, fill=(215, 215, 210))
    d.rounded_rectangle([225, y + 24, 225 + wbar, y + 38], radius=7, fill=GREEN if k == 0 else (190, 190, 185))
person(d, 580, 330, 200, NAVY); arrow(d, (540, 365), (472, 365), GRAY, 4)
d.rounded_rectangle([720, 200, 1310, 520], radius=16, fill=LIGHT)
ctext(d, 1015, 222, "오늘 시도 평균만 봐도", F_M, INK)
ctext(d, 1015, 265, "서울 1,902원  대구 1,829원", F_S, GRAY)
ctext(d, 1015, 310, "73원", F_HUGE, NAVY)
ctext(d, 1015, 420, "50리터면 3,663원 차이", F_M, INK)
ctext(d, 1015, 460, "같은 날 전국 최저 주유소는 1,755원", F_S, GRAY)
box(d, (90, 600, 1310, 700), SAND, "값이 천천히 내려오는 동안에는 근처 주유소끼리도 값이 다를 수 있다.\n오피넷 앱 「내 주변」이나 오피넷 사이트 「싼 주유소 찾기」에서 가격순으로 한 번 보고 가자", F_S, INK)
footc(d, "근거: 공부노트 §2-4(오피넷 API 시도별·최저가 TOP10, 10/14[1]). 50리터 차이는 직접 계산. 앱 화면은 모식")
save(im, "O12_check_nearby.png")

print("\n".join(WARN) if WARN else "넘침 경고 없음")
