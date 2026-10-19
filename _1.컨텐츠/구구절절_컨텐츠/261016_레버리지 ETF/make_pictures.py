# -*- coding: utf-8 -*-
"""레버리지 ETF 글 — 일반인용 그림 13장(2026-10-16). 본편 L1~L8, 한 걸음 더 L9~L13.
줄기: 주가는 제자리인데 2배 상품은 -20%(실제 종가) → 왜: 퍼센트 계단 · 매일 다시 거는 판돈 → 그래도 왜 몰렸나(오르는 산)
      → 1,000만 원은 225만 원 → 정부는 조건을 걸었다 → 아직 정해지지 않은 조건 셋 → 할 일 하나.
숫자는 레버리지ETF_공부노트_2026-10-16.md 와 base data\가격(네이버 종가 CSV·직접계산_결과.txt·ETF 목록 JSON) 확인분만.
직접 계산값은 근거 줄에 「직접 계산」 표시. 상품명은 그래프 라벨·근거 줄에만, 로고·인물 얼굴 없음."""
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
BASE = os.path.join(HERE, "base data", "가격")

WARN = []
def save(im, n):
    im.save(os.path.join(OUT, n)); print("saved", n)

# ---- 글자 넘침 검사용 래퍼 ----
_canvas, _box, _ctext = canvas, box, ctext
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
def ctext(d, cx, y, text, f, color=INK):
    w = d.textlength(text, font=f)
    if cx - w / 2 < 20 or cx + w / 2 > W - 20: WARN.append(f"가운데 글자 넘침: {text}")
    _ctext(d, cx, y, text, f, color)
def ltext(d, x, y, text, f, color=INK, right=None):
    """왼쪽 맞춤 글자. right 를 주면 그 x 를 넘는지 검사"""
    w = d.textlength(text, font=f)
    if x + w > (right or W - 20): WARN.append(f"글자 넘침: {text}")
    d.text((x, y), text, font=f, fill=color)

STK = NAVY; LEV = RED; OKC = GREEN; TBD = (150, 150, 155); MONEY = (95, 150, 105); MONEY_L = (150, 195, 155)
BAND = (238, 234, 222); GRID = (232, 230, 222)

def rd(name):
    with open(os.path.join(BASE, name), encoding="utf-8-sig") as f:
        return [(dt.datetime.strptime(r["date"], "%Y%m%d").date(), float(r["close"])) for r in csv.DictReader(f)]
SKH = rd("000660_SK하이닉스.csv")
KDX = rd("0193T0_KODEX_SK하이닉스단일종목레버리지.csv")
SKH_D = dict(SKH); KDX_D = dict(KDX)
D_BASE = dt.date(2026, 5, 26); SK_BASE = SKH_D[D_BASE]; LIST_PRICE = 23450.0  # 상장 전날 종가 · 상장가(보도[19])
def pct(a, b): return (a / b - 1) * 100

# ---- 그림 부품 ----
def dashed(d, p0, p1, col=GRAY, w=2, dash=10):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0); n = max(int(L // dash), 1)
    for i in range(0, n, 2):
        a = i / n; b = min((i + 1) / n, 1)
        d.line([x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b], fill=col, width=w)
def dashed_rect(d, xy, col=GRAY, w=2):
    x0, y0, x1, y1 = xy
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): dashed(d, p, q, col, w)
def legend_line(d, x, y, col, text, w=5):
    d.line([x, y + 14, x + 44, y + 14], fill=col, width=w); ltext(d, x + 56, y, text, F_S, INK)
def stock_chart(d, D1, X0, X1, Y0, Y1, V0=50, V1=200):
    """5/26 = 100 기준 SK하이닉스 선 + 상장가 = 100 기준 KODEX 2배 선. 좌표 함수 반환"""
    def qx(day): return X0 + (day - D_BASE).days / (D1 - D_BASE).days * (X1 - X0)
    def qy(v): return Y1 - (v - V0) / (V1 - V0) * (Y1 - Y0)
    for v in (50, 100, 150, 200):
        if V0 <= v <= V1:
            d.line([X0, qy(v), X1, qy(v)], fill=GRID, width=1); ltext(d, X0 - 56, qy(v) - 12, str(v), F_SM, GRAY)
    dashed(d, (X0, qy(100)), (X1, qy(100)), GRAY, 2)
    d.line([X0, Y1, X1, Y1], fill=(200, 198, 190), width=2)
    ctext(d, qx(D_BASE), Y1 + 10, "5/26", F_SM, GRAY)
    for m in (6, 7):
        day = dt.date(2026, m, 1)
        if day < D1 and qx(day) - X0 > 60 and X1 - qx(day) > 60:
            d.line([qx(day), Y1, qx(day), Y1 + 6], fill=GRAY, width=2); ctext(d, qx(day), Y1 + 10, f"{m}월", F_SM, GRAY)
    ctext(d, qx(D1), Y1 + 10, f"{D1.month}/{D1.day}", F_SM, GRAY)
    s = [(qx(a), qy(v / SK_BASE * 100)) for a, v in SKH if D_BASE <= a <= D1]
    k = [(qx(D_BASE), qy(100))] + [(qx(a), qy(v / LIST_PRICE * 100)) for a, v in KDX if a <= D1]
    d.line(s, fill=STK, width=4); d.line(k, fill=LEV, width=5)
    for pts, col in ((s, STK), (k, LEV)):
        x, y = pts[-1]; d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=col, outline=WHITE, width=3)
    return qx, qy
def bills(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=MONEY)
    y = y1 - 16
    while y > y0 + 4:
        d.line([x0, y, x1, y], fill=MONEY_L, width=2); y -= 16
def door(d, cx, top, bot, col=(150, 110, 80), dashed_line=False):
    w = 70
    if dashed_line:
        dashed_rect(d, (cx - w, top, cx + w, bot), AMBER, 4)
    else:
        d.rectangle([cx - w - 10, top - 10, cx + w + 10, bot], fill=(205, 200, 190))
        d.rectangle([cx - w, top, cx + w, bot], fill=col)
        d.rectangle([cx - w + 14, top + 16, cx + w - 14, top + 90], outline=(120, 85, 60), width=3)
        d.rectangle([cx - w + 14, top + 110, cx + w - 14, bot - 20], outline=(120, 85, 60), width=3)
        d.ellipse([cx + w - 30, (top + bot) / 2, cx + w - 16, (top + bot) / 2 + 14], fill=GOLD if False else AMBER)
def lock(d, cx, cy, s=1.0, col=INK):
    d.arc([cx - 18 * s, cy - 40 * s, cx + 18 * s, cy - 4 * s], 180, 360, fill=col, width=int(6 * s))
    d.line([cx - 18 * s, cy - 22 * s, cx - 18 * s, cy - 6 * s], fill=col, width=int(6 * s)); d.line([cx + 18 * s, cy - 22 * s, cx + 18 * s, cy - 6 * s], fill=col, width=int(6 * s))
    d.rounded_rectangle([cx - 28 * s, cy - 8 * s, cx + 28 * s, cy + 34 * s], radius=6, fill=col)
def phone(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=INK)
    d.rounded_rectangle([x + 14, y + 40, x + w - 14, y + h - 40], radius=8, fill=WHITE)
def magnifier(d, cx, cy, r=46, col=INK):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=8)
    a = math.radians(45); d.line([cx + r * math.cos(a), cy + r * math.sin(a), cx + r * 2.0 * math.cos(a), cy + r * 2.0 * math.sin(a)], fill=col, width=14)
def clock(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=8)
    for k in range(12):
        a = math.radians(k * 30 - 90); d.line([cx + r * 0.82 * math.cos(a), cy + r * 0.82 * math.sin(a), cx + r * 0.94 * math.cos(a), cy + r * 0.94 * math.sin(a)], fill=INK, width=4)
    for ang, L, wd in ((math.radians(25 * 6 - 90), 0.75, 6), (math.radians(3.4 * 30 - 90), 0.5, 9)):
        d.line([cx, cy, cx + r * L * math.cos(ang), cy + r * L * math.sin(ang)], fill=RED if wd == 6 else INK, width=wd)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=INK)
GOLD = (230, 180, 40)


# ============ L0 10월 15일 하루 (10/16 결 바꿈: 폭락이 입구) ============
def day_chg(name):
    rows = list(csv.DictReader(open(os.path.join(BASE, name), encoding="utf-8-sig")))
    a, b = float(rows[-2]["close"]), float(rows[-1]["close"]); return rows[-1]["date"], (b / a - 1) * 100
BARS = (("코스피", "KOSPI.csv", (150, 150, 155)), ("삼성전자", "005930_삼성전자.csv", STK), ("삼성전자 2배", "0193W0_KODEX_삼성전자단일종목레버리지.csv", LEV),
        ("SK하이닉스", "000660_SK하이닉스.csv", STK), ("SK하이닉스 2배", "0193T0_KODEX_SK하이닉스단일종목레버리지.csv", LEV))
im, d = canvas("10월 15일 하루, 2배 상품은 20% 넘게 빠졌다", "코스피가 7% 넘게 떨어진 「검은 목요일」 — 전날 종가 대비 하루 등락, 직접 계산")
TOPY = 200; SCL = 14.0
d.line([90, TOPY, 1310, TOPY], fill=INK, width=2)
for k, (lab, f, col) in enumerate(BARS):
    day, ch = day_chg(f)
    assert day == "20261015", (f, day)
    cx = 180 + k * 250
    h = abs(ch) * SCL
    d.rounded_rectangle([cx - 70, TOPY, cx + 70, TOPY + h], radius=8, fill=col)
    ctext(d, cx, TOPY + h + 12, f"{ch:.1f}%", F_MID, col if col != (150, 150, 155) else INK)
    ctext(d, cx, TOPY - 46, lab, F_M, INK)
box(d, (90, 600, 1310, 700), SAND, "코스피가 7.6% 떨어진 날, 삼성전자·SK하이닉스는 11~13%가 아니라 각각 11.5%·13.1%, 그 2배 상품은 19.6%·21.7% 빠졌다".replace("11~13%가 아니라 각각 ", "") + "\n2배 상품은 「오늘 하루」 움직임을 두 배 가까이 따라간다 — 내리는 날엔 그만큼 크게",
    F_S, INK)
footc(d, "근거: 네이버 금융 종가(base data 가격 CSV) 10월 14일 → 15일, 직접 계산. 상품은 KODEX 삼성전자·SK하이닉스 단일종목레버리지")
save(im, "L0_black_thursday.png")

# ============ L1 주가는 제자리, 2배 상품은 -20% (썸네일 후보) ============
D1 = dt.date(2026, 7, 15)
im, d = canvas("7월에 실제로 그랬다 — 주가는 돌아왔는데 2배는 -19.8%", "SK하이닉스 주가와, 그 주가를 하루 2배로 따라가는 상품 — 5월 26일부터 7월 15일까지")
qx, qy = stock_chart(d, D1, 140, 1000, 180, 530)
legend_line(d, 160, 186, STK, "SK하이닉스 주가", 4); legend_line(d, 160, 222, LEV, "2배 상품")
sk_end = pct(SKH_D[D1], SK_BASE); kd_end = pct(KDX_D[D1], LIST_PRICE)
d.rounded_rectangle([1050, 180, 1330, 530], radius=16, fill=PINK)
ctext(d, 1190, 198, "7월 15일", F_M, INK)
ctext(d, 1190, 250, "주가", F_S, GRAY); ctext(d, 1190, 278, f"+{sk_end:.1f}%", F_BIG, STK)
ctext(d, 1190, 385, "2배 상품", F_S, GRAY); ctext(d, 1190, 413, f"{kd_end:.1f}%", F_BIG, LEV)
box(d, (90, 600, 1310, 700), SAND, "한 달 반 동안 크게 오르내린 주가는 7월 15일 출발점 근처(+1.5%)로 돌아왔다\n그런데 2배 상품은 20% 가까이 빠진 채였다. 점선(출발점)보다 아래가 손해다", F_S, INK)
footc(d, "근거: 네이버 금융 일별 종가(base data 가격 CSV), 상장가 23,450원은 보도[19]. 등락률은 직접 계산")
save(im, "L1_flat_vs_minus20.png")

# ============ L2 퍼센트 계단 ============
im, d = canvas("20% 내렸다 20% 오르면, 제자리가 아니다", "퍼센트는 출발점이 바뀌면 크기가 바뀐다 — 금융위원회가 든 예시 그대로")
BASEY = 540; SC = 2.6
for p, (name, col, vals, moves, gap) in enumerate((("주식", STK, (100, 80, 96), ("-20%", "+20%"), "-4%"),
                                                   ("2배 상품", LEV, (100, 60, 84), ("-40%", "+40%"), "-16%"))):
    left = 120 + p * 640; xs = [left + 60 + k * 170 for k in range(3)]
    ltext(d, left, 140, name, F_H, col)
    dashed(d, (left, BASEY - 100 * SC), (left + 520, BASEY - 100 * SC), GRAY, 2)
    for k, (x, v) in enumerate(zip(xs, vals)):
        top = BASEY - v * SC
        if k == 2:
            d.rectangle([x - 55, BASEY - 100 * SC, x + 55, top], fill=PINK)
        d.rectangle([x - 55, top, x + 55, BASEY], fill=col if k else (170, 175, 190) if p == 0 else (235, 160, 160))
        ctext(d, x, top + 12, str(v), F_MID, WHITE)
        ctext(d, x, BASEY + 8, ("출발", "하루 뒤", "이틀 뒤")[k], F_SM, GRAY)
    for k in range(2):
        a, b = xs[k], xs[k + 1]; ya = BASEY - vals[k] * SC - 22; yb = BASEY - vals[k + 1] * SC - 22
        c = RED if k == 0 else GREEN
        arrow(d, (a + 20, ya), (b - 20, yb), c, 4)
        ctext(d, (a + b) / 2, 205, moves[k], F_M, c)
    ltext(d, xs[2] + 66, BASEY - 100 * SC + 6, gap, F_MID, RED)
box(d, (90, 600, 1310, 700), SAND, "80에서 20% 오르면 16만 오른다. 깎인 출발점에서 같은 퍼센트를 올라도 원래 자리에 못 닿는다.\n2배 상품은 내릴 때 40%를 잃어 출발점이 더 낮아지니, 덜 돌아온다", F_S, INK)
footc(d, "근거: 금융위원회 7.16 보완방안·7.28·8.12 보도자료의 예시(100→80→96, 100→60→84)[2][7][8]")
save(im, "L2_percent_stairs.png")

# ============ L3 매일 아침 다시 거는 판돈 ============
im, d = canvas("매일 아침, 판돈을 「내 돈의 2배」로 다시 건다", "1,000만 원으로 시작해 주가가 하루 -10%, 다음 날 +10% 움직였다면 (계산용 가정)")
BASEY = 500; SC = 300 / 2000
days = (("1일째 아침", 1000), ("2일째 아침", 800), ("3일째 아침", 960))
cxs = [210, 540, 870]
for (lab, mine), cx in zip(days, cxs):
    for dx, v, col, nm in ((-52, mine, STK, "내 돈"), (52, mine * 2, AMBER, "판돈")):
        top = BASEY - v * SC
        d.rectangle([cx + dx - 44, top, cx + dx + 44, BASEY], fill=col)
        ctext(d, cx + dx, top - 32, f"{v:,}만", F_M, col)
        ctext(d, cx + dx, BASEY - 30, nm, F_SM, WHITE)
    ctext(d, cx, BASEY + 12, lab, F_M, INK)
d.line([110, BASEY, 980, BASEY], fill=INK, width=2)
for k, (mv, money, col) in enumerate((("주가 -10%", "-200만", RED), ("주가 +10%", "+160만", GREEN))):
    a = cxs[k] + 100; b = cxs[k + 1] - 100
    arrow(d, (a, 330), (b, 330), col, 5)
    ctext(d, (a + b) / 2, 268, mv, F_S, col); ctext(d, (a + b) / 2, 346, money, F_S, col)
d.rounded_rectangle([1040, 190, 1330, 530], radius=16, fill=PINK)
ctext(d, 1185, 206, "이틀 뒤", F_M, INK)
ctext(d, 1185, 252, "주가", F_S, GRAY); ctext(d, 1185, 280, "-1%", F_BIG, STK)
ctext(d, 1185, 380, "내 돈", F_S, GRAY); ctext(d, 1185, 408, "-4%", F_BIG, LEV)
box(d, (90, 600, 1310, 700), SAND, "어제 잃으면 오늘 거는 판돈도 줄어 있다. 그래서 다음 날 같은 10%가 올라도 잃은 만큼 못 찾는다.\n주가는 1% 빠졌을 뿐인데 내 돈은 4% 빠졌다. 오르내림이 잦을수록 이 차이가 쌓인다", F_S, INK)
footc(d, "근거: 공부노트 §3-1(하루 2배를 매일 다시 맞춘다, 금융위 5.15 유의사항[3]). 1,000만 원·10%는 가정, 직접 계산")
save(im, "L3_daily_reset_bet.png")


# ============ L2s 10% 내리고 10% 오르면 (10/16 「더 쉽게」 — 계단·판돈 두 장을 이 한 장으로) ============
im, d = canvas("10% 내렸다 10% 오르면, 2배 상품은 4% 손해", "주가가 하루 -10%, 다음 날 +10% 움직였다고 치면 (계산하기 쉽게 잡은 예)")
for row, (name, col, vals, moves, res, rcol) in enumerate((("주식", STK, (100, 90, 99), ("-10%", "+10%"), "-1%", STK),
                                                        ("2배 상품", LEV, (100, 80, 96), ("-20%", "+20%"), "-4%", LEV))):
    y0 = 165 + row * 210; BASEY2 = y0 + 175; SC2 = 1.45
    ltext(d, 90, y0 + 70, name, F_H, col)
    xs = [380, 640, 900]
    dashed(d, (320, BASEY2 - 100 * SC2), (960, BASEY2 - 100 * SC2), GRAY, 2)
    for k, (x, v) in enumerate(zip(xs, vals)):
        top = BASEY2 - v * SC2
        d.rounded_rectangle([x - 60, top, x + 60, BASEY2], radius=8, fill=col if k else (185, 188, 198))
        ctext(d, x, top + 12, str(v), F_MID, WHITE)
    for k in range(2):
        mc = RED if k == 0 else GREEN
        ctext(d, (xs[k] + xs[k + 1]) / 2, y0 - 6, moves[k], F_M, mc)
    d.rounded_rectangle([1040, y0 + 20, 1320, y0 + 170], radius=16, fill=PINK if row else LIGHT)
    ctext(d, 1180, y0 + 30, "이틀 뒤", F_S, GRAY); ctext(d, 1180, y0 + 62, res, F_BIG, rcol)
box(d, (90, 600, 1310, 700), SAND, "2배 상품은 매일 그날 움직임의 2배를 따라간다. 떨어진 날 두 배로 떨어지니, 같은 비율로 올라도 덜 돌아온다\n오르락내리락이 잦을수록 이 손해가 쌓인다 — 그림 5(7월 실제)가 그 결과다", F_S, INK)
footc(d, "근거: 공부노트 §3-1(하루 수익률의 2배를 매일 다시 맞춘다, 금융위 5.15 유의사항[3]). 10%는 계산용 예, 직접 계산")
save(im, "L2s_down10_up10.png")

# ============ L4 오르는 산 + 첫날 10.4조 ============
D1 = dt.date(2026, 6, 22)
im, d = canvas("오를 때는 2배보다 더 올랐다 — 그래서 몰렸다", "SK하이닉스 주가와 2배 상품, 5월 26일부터 주가가 가장 높았던 6월 22일까지")
qx, qy = stock_chart(d, D1, 140, 900, 180, 530)
legend_line(d, 160, 186, STK, "SK하이닉스 주가", 4); legend_line(d, 160, 222, LEV, "2배 상품")
d.rounded_rectangle([970, 180, 1330, 530], radius=16, fill=LIGHT)
ctext(d, 1150, 198, "6월 22일", F_M, INK)
ctext(d, 1150, 250, "주가", F_S, GRAY); ctext(d, 1150, 278, f"+{pct(SKH_D[D1], SK_BASE):.0f}%", F_BIG, STK)
ctext(d, 1150, 385, "2배 상품", F_S, GRAY); ctext(d, 1150, 413, f"+{pct(KDX_D[D1], LIST_PRICE):.0f}%", F_BIG, LEV)
box(d, (90, 600, 1310, 700), SAND, "주가가 꾸준히 오를 때는 반대로, 2배 상품은 주가가 오른 폭의 두 배보다 더 올랐다\n반도체 주가가 한창 오르던 때 나와서, 첫날에만 10조 4천억 원어치가 사고팔렸다", F_S, INK)
footc(d, "근거: 네이버 금융 일별 종가(등락률은 직접 계산), 첫날 거래대금은 금융위 7.16 보완방안[2]")
save(im, "L4_rising_hill_crowd.png")

# ============ L5 1,000만 원은 지금 얼마 ============
im, d = canvas("처음 나왔을 때 넣은 1,000만 원은, 검은 목요일 저녁 225만 원", "SK하이닉스 2배 상품을 처음 나온 값(23,450원)에 샀다고 치면 — 직접 계산")
pts = ((dt.date(2026, 5, 27), "처음 샀을 때", LIST_PRICE), (dt.date(2026, 6, 22), "6월 22일 최고", KDX_D[dt.date(2026, 6, 22)]),
       (dt.date(2026, 7, 30), "7월 30일", KDX_D[dt.date(2026, 7, 30)]), (dt.date(2026, 10, 15), "10월 15일", KDX_D[dt.date(2026, 10, 15)]))
BASEY = 500; SC = 300 / 1900
for k, (day, lab, price) in enumerate(pts):
    cx = 230 + k * 300; man = price / LIST_PRICE * 1000
    top = BASEY - man * SC
    bills(d, cx - 80, top, cx + 80, BASEY)
    if k == 3:
        ctext(d, cx, top - 78, f"{man:,.0f}만 원", F_BIG, LEV)
    else:
        ctext(d, cx, top - 46, f"{man:,.0f}만", F_MID, INK)
    ctext(d, cx, BASEY + 10, lab, F_M, INK)
    ctext(d, cx, BASEY + 44, f"{price:,.0f}원", F_S, GRAY)
d.line([100, BASEY, 1300, BASEY], fill=INK, width=2)
for k in range(3):
    arrow(d, (230 + k * 300 + 95, 250), (230 + (k + 1) * 300 - 95, 250), GRAY, 4)
box(d, (90, 600, 1310, 700), SAND, "같은 기간 SK하이닉스 주가는 39.7% 빠졌는데, 2배 상품에 넣은 1,000만 원은 225만 원이 됐다\n1,000만 원으로 돌아가려면 지금 값에서 4.4배가 돼야 한다(직접 계산)", F_S, INK)
footc(d, "근거: 네이버 금융 종가, 상장가 23,450원[19]. 금액은 종가 ÷ 상장가 × 1,000만 원 — 직접 계산(보수·세금 빼고)")
save(im, "L5_ten_million_now.png")

# ============ L5r 주가가 5월 값으로 돌아와도 (10/16 보완: 지금 들고 있는 사람의 답) ============
D15 = dt.date(2026, 10, 15)
back = SK_BASE / SKH_D[D15]                       # 주가가 5/26 값으로 돌아가려면 몇 배
man_now = KDX_D[D15] / LIST_PRICE * 1000
man_max = man_now * back * back                   # 하루 (1+2r) <= (1+r)^2 → 2배 상품은 back^2 를 넘지 못한다(보수 빼고)
im, d = canvas("주가가 5월 값으로 돌아와도, 1,000만 원은 많아야 %d만 원" % round(man_max),
               "10월 15일 225만 원이 된 SK하이닉스 2배 상품 — 주가가 5월 26일 값(%s원)까지 돌아온다고 치면, 직접 계산" % format(int(SK_BASE), ","))
BASEY = 500; SC = 300 / 1000
cols = ((260, "10월 15일", man_now, LEV, "지금"), (700, "주가가 5월 값으로", man_max, NAVY, "가장 좋은 경우"))
for cx, lab, man, col, tag in cols:
    top = BASEY - man * SC
    bills(d, cx - 90, top, cx + 90, BASEY)
    ctext(d, cx, top - 70, "%d만 원" % round(man), F_BIG, col)
    ctext(d, cx, BASEY + 10, lab, F_M, INK); ctext(d, cx, BASEY + 44, tag, F_S, GRAY)
top1000 = BASEY - 1000 * SC
dashed_rect(d, (1050, top1000, 1230, BASEY), GRAY, 3)
ctext(d, 1140, top1000 - 46, "1,000만 원", F_MID, GRAY)
ctext(d, 1140, BASEY + 10, "처음 넣은 돈", F_M, INK)
ctext(d, 1140, (top1000 + BASEY) / 2 - 20, "%d만 원 모자람" % round(1000 - man_max), F_S, RED)
d.line([100, BASEY, 1300, BASEY], fill=INK, width=2)
arrow(d, (370, 360), (590, 360), GRAY, 5)
ctext(d, 480, 300, "주가 %.2f배" % back, F_M, INK)
box(d, (90, 600, 1310, 700), SAND, "하루하루 2배씩 따라가면, 2배 상품이 오르는 배수는 주가 배수를 두 번 곱한 값(%.2f배)을 넘지 못한다\n흔들림 없이 쭉 오르는 가장 좋은 경우가 이 막대다. 오르내리며 돌아오면 그보다 적다(보수·세금 빼고)" % (back * back), F_S, INK)
footc(d, "근거: 네이버 금융 종가(주가 5/26·10/15, 2배 상품 10/15), 처음 나온 값 23,450원[19] — 직접 계산(보수·세금 빼고)")
save(im, "L5r_back_to_may.png")

# ============ L6 정부는 조건을 걸었다 (10/16 마스터 3-1: 문 비유 → 조건) ============
im, d = canvas("정부는 상품을 없애지 않고, 새로 사는 사람에게 조건을 걸었다", "2배 상품을 새로 사려는 사람이 갖춰야 하는 조건과, 그 시작일")
GY = 470
d.line([70, GY, 1330, GY], fill=(190, 185, 175), width=4)
# 가게 셔터: 새 상품·광고 멈춤
sx = 190
d.rectangle([sx - 95, 250, sx + 95, GY], fill=(215, 215, 220))
for yy in range(262, GY, 18): d.line([sx - 95, yy, sx + 95, yy], fill=(170, 170, 180), width=3)
d.rectangle([sx - 110, 228, sx + 110, 252], fill=(120, 130, 150))
xmark(d, sx + 70, 300, 22)
ctext(d, sx, 172, "새 상품·광고 중단", F_M, INK); ctext(d, sx, GY + 14, "7월 16일부터", F_S, GRAY)
person(d, 335, 320, 150, NAVY)
for cx, lab, when in ((500, "현금 3,000만 원", "7월 31일부터"), (750, "교육 3시간", "8월 7일부터"), (1000, "모의거래 5시간", "8월 19일부터")):
    d.rounded_rectangle([cx - 95, 262, cx + 95, GY - 12], radius=18, fill=MINT)
    check(d, cx, 340, 40, OKC)
    ctext(d, cx, 172, lab, F_M, INK); ctext(d, cx, GY + 14, when, F_S, GRAY)
dashed_rect(d, (1225 - 80, 262, 1225 + 80, GY - 12), AMBER, 3)
ctext(d, 1225, 172, "20주 단위", F_M, AMBER); ctext(d, 1225, GY + 14, "11월 예정", F_S, AMBER)
ctext(d, 1225, 330, "?", F_HUGE, AMBER)
box(d, (90, 600, 1310, 700), SAND, "상품을 없애는 대신, 새로 사려는 사람이 먼저 갖춰야 할 조건 셋을 걸었다\n돈(현금 3,000만 원), 공부(교육 3시간), 연습(모의거래 5시간) — 이미 산 사람이 파는 건 자유", F_S, INK)
footc(d, "근거: 금융위 7.16 보완방안[2] · 7.24 예탁금 조기시행[6] · 8.12 보도자료[8], 20주 단위 11월은 보도[18]")
save(im, "L6_narrower_doors.png")

# ============ L7 아직 정해지지 않은 것 ============
im, d = canvas("그다음 조건 셋은 아직 정해지지 않았다", "7월 말 방향만 나왔거나 국회에 발의된 것 — 10월 15일까지 비율·시행일이 확정되지 않았다")
d.rounded_rectangle([90, 190, 390, 530], radius=16, fill=MINT)
check(d, 240, 250, 34, OKC)
ctext(d, 240, 300, "시행 중", F_H, OKC); ctext(d, 240, 350, "4", F_HUGE, OKC); ctext(d, 240, 450, "그림 7의 네 가지", F_S, GRAY)
for cx, lab, sub, chip_t in ((600, "개인별 투자한도", "20%는 예시", "검토"), (880, "과다호가부담금", "방식 협의 중", "검토"), (1160, "배율 조정 법", "8월 11일 발의", "발의")):
    dashed_rect(d, (cx - 125, 190, cx + 125, 530), TBD, 3)
    ctext(d, cx, 215, "?", F_HUGE, TBD)
    ctext(d, cx, 340, lab, F_M, INK); ctext(d, cx, 380, sub, F_S, GRAY)
    cw = d.textlength(chip_t, font=F_M) + 36
    d.rounded_rectangle([cx - cw / 2, 440, cx + cw / 2, 482], radius=21, fill=AMBER); ctext(d, cx, 447, chip_t, F_M, WHITE)
box(d, (90, 600, 1310, 700), SAND, "투자한도(가진 돈의 일정 비율 안)와 과다호가부담금은 7월 29일 방향만 나왔고, 비율·시행일은 아직 없다.\n시장이 급할 때 배율을 낮출 수 있게 하는 법은 국회에 발의된 상태다", F_S, INK)
footc(d, "근거: 금융위 7.28 간담회[7], 7.29 회의 보도[15], 법 개정안 발의 보도[16]. 금융위 보도자료는 10.15까지 확인")
save(im, "L7_doors_under_construction.png")

# ============ L8 할 일 하나 ============
im, d = canvas("할 일 하나 — 상품 이름과 설명서에서 두 단어 찾기", "내 계좌에 「레버리지」나 「2X」가 붙은 상품이 있는지, 있다면 설명서에 「일간」이 있는지")
phone(d, 150, 160, 300, 420)
d.rectangle([164, 200, 436, 240], fill=NAVY); ctext(d, 300, 206, "내 보유 상품", F_S, WHITE)
rows = ((None, 150), ("○○ 레버리지", None), (None, 120), ("○○ 2X", None))
for k, (t, wbar) in enumerate(rows):
    y = 262 + k * 66
    if t:
        d.rounded_rectangle([176, y - 6, 424, y + 40], radius=8, fill=SAND); ltext(d, 190, y, t, F_M, RED, right=420)
    else:
        d.rounded_rectangle([190, y + 6, 190 + wbar, y + 22], radius=7, fill=(205, 205, 200))
magnifier(d, 395, 320, 44, INK)
arrow(d, (500, 380), (600, 380), GRAY, 6)
d.rectangle([640, 180, 900, 560], fill=WHITE, outline=INK, width=3)
ctext(d, 770, 196, "투자설명서", F_M, INK)
for k in range(8):
    y = 250 + k * 36
    if k == 3:
        d.rounded_rectangle([668, y - 8, 750, y + 26], radius=6, fill=(255, 225, 90)); ltext(d, 676, y - 6, "일간", F_M, INK)
        d.rounded_rectangle([762, y + 2, 872, y + 16], radius=7, fill=(205, 205, 200))
    else:
        d.rounded_rectangle([668, y + 2, 872 - (k % 3) * 40, y + 16], radius=7, fill=(215, 215, 210))
d.rounded_rectangle([960, 200, 1320, 540], radius=16, fill=LIGHT)
ctext(d, 1140, 222, "찾을 두 글자", F_M, INK)
ctext(d, 1140, 290, "일간", F_HUGE, NAVY)
ctext(d, 1140, 420, "「일일」로 쓴 곳도 같은 뜻", F_S, GRAY)
box(d, (90, 600, 1310, 700), SAND, "「일간 수익률의 2배」는 하루 단위로 2배를 맞춘다는 표시다. 며칠 들고 있으면 그림 5처럼 2배와 어긋날 수 있다.\n상품 이름에 「레버리지」「2X」가 있으면, 설명서에서 그 문장 하나만 찾아 읽어 보자", F_S, INK)
footc(d, "근거: KODEX 상품 페이지 유의사항(「기간 수익률은 … 일간 수익률과 차이」, 10.16 확인), 금융위 5.15·5.26 유의사항[3][3a]. 화면은 모식")
save(im, "L8_find_daily_word.png")

# ============ L9 마감 직전 계산대 줄 ============
im, d = canvas("장 마감 무렵, 2배 상품은 주가가 간 쪽으로 더 민다", "하루 2배를 맞추려고 오른 날엔 더 사고, 내린 날엔 더 판다 — 마감 직전 계산대에 몰린 줄처럼")
clock(d, 200, 330, 105); ctext(d, 200, 450, "장 마감 무렵", F_M, INK)
d.rounded_rectangle([760, 210, 830, 500], radius=10, fill=(150, 155, 165)); ctext(d, 795, 512, "시장", F_S, GRAY)
for row, (y, col, lab, up) in enumerate(((220, RED, "오른 날 → 더 산다", True), (380, BLUE, "내린 날 → 더 판다", False))):
    for k in range(5): person(d, 400 + k * 62, y, 100, col)
    ltext(d, 380, y - 40 if row == 0 else y + 106, lab, F_M, col)
    arrow(d, (675, y + 50), (752, y + 50), col, 6)
    if up: up_arrow(d, 870, y + 110, 100, RED, 40)
    else: down_arrow(d, 870, y, 100, BLUE, 40)
d.rounded_rectangle([930, 190, 1330, 530], radius=16, fill=PINK)
ctext(d, 1130, 210, "6월 19일 (주가 +2.9%)", F_M, INK)
ctext(d, 1130, 290, "약 0.53조 원", F_BIG, RED)
ctext(d, 1130, 380, "마감 무렵 더 산 것으로 추정", F_S, GRAY)
ctext(d, 1130, 414, "주식 0.26조 + 선물 0.27조", F_S, GRAY)
box(d, (90, 600, 1310, 700), SAND, "모두가 같은 시각에 같은 쪽으로 사고팔면 그 순간 값이 더 흔들릴 수 있다. 정부가 주문 시점을 나눠 달라 한 이유다.\n다만 이 쏠림이 주가 변동을 얼마나 키웠는지는 아직 확정된 분석이 없다", F_S, INK)
footc(d, "근거: 자본시장연구원 자본시장포커스 2026-13호[5](추정치, 합은 직접 계산), 금융위 7.28 간담회[7]")
save(im, "L9_closing_rush.png")

# ============ L10 정가표와 계산대 가격 ============
im, d = canvas("정가표와 계산대 가격이 다를 때 — 괴리율", "상품 안에 든 실제 가치(순자산가치)와, 시장에서 사고파는 값의 차이")
# 왼쪽: 평소(10월 15일)
d.polygon([(100, 300), (170, 210), (420, 210), (420, 390), (170, 390)], fill=SAND, outline=GOLD)
d.ellipse([140, 288, 166, 314], fill=BG, outline=GOLD, width=3)
ctext(d, 300, 228, "정가표(안에 든 가치)", F_S, GRAY); ctext(d, 300, 268, "5,251원", F_MID, INK)
d.rounded_rectangle([470, 230, 640, 390], radius=10, fill=(90, 95, 105)); d.rectangle([488, 250, 622, 310], fill=(25, 35, 30))
ctext(d, 555, 262, "5,285원", F_M, (120, 255, 150)); ctext(d, 555, 330, "계산대", F_S, WHITE)
ctext(d, 370, 420, "평소 — 10월 15일", F_M, INK)
ctext(d, 370, 460, "0.65%", F_BIG, NAVY)
dashed(d, (700, 190), (700, 560), (200, 200, 195), 3)
# 오른쪽: 6월 8일 사례
ctext(d, 1010, 185, "6월 8일 마감, 한 SK하이닉스 2배 상품", F_M, INK)
down_arrow(d, 860, 250, 180, BLUE, 70); ctext(d, 860, 445, "주가 7%대 하락", F_S, BLUE)
up_arrow(d, 1110, 430, 180, RED, 70); ctext(d, 1110, 445, "상품 마감가", F_S, RED)
ctext(d, 1110, 482, "+49.7%", F_BIG, RED)
box(d, (90, 600, 1310, 700), SAND, "평소엔 둘이 거의 같다. 마감 직전 값을 받쳐 줄 주문이 비면 크게 벌어진다(6월 8일).\n그래서 8월 19일부터 국내 상품의 관리 기준을 3%에서 2%로 좁혔다", F_S, INK)
footc(d, "근거: 네이버 ETF 목록 10.15(NAV·종가, 차이는 직접 계산), 6.8 ACE 상품 사례 보도[13], 금융위 8.12[8]")
save(im, "L10_price_tag_gap.png")

# ============ L11 홍콩은 다이얼 ============
im, d = canvas("홍콩은 배율 다이얼을 하루 단위로 돌릴 수 있게 했다", "같은 삼성전자·SK하이닉스 2배 상품이라도 — 한국은 2배 고정, 홍콩은 2배 안에서 낮출 수 있다")
def dial(cx, cy, r, v, col):
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=WHITE, outline=INK, width=6)
    for t in (0, 0.5, 1, 1.5, 2, 2.5):
        a = math.radians(180 + t / 2.5 * 180)
        d.line([cx + r * 0.85 * math.cos(a), cy + r * 0.85 * math.sin(a), cx + r * 0.98 * math.cos(a), cy + r * 0.98 * math.sin(a)], fill=INK, width=4)
        if t in (0, 1, 2):
            lx, ly = cx + r * 1.13 * math.cos(a), cy + r * 1.13 * math.sin(a)
            ctext(d, lx, ly - 16, f"{t:g}", F_M, GRAY)
    a2 = math.radians(180 + 2 / 2.5 * 180)
    d.line([cx + r * 0.85 * math.cos(a2), cy + r * 0.85 * math.sin(a2), cx + r * 1.0 * math.cos(a2), cy + r * 1.0 * math.sin(a2)], fill=RED, width=10)
    a = math.radians(180 + v / 2.5 * 180)
    d.line([cx, cy, cx + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a)], fill=col, width=10)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=col)
dial(370, 440, 190, 2, LEV); lock(d, 500, 512, 0.8, INK)
ctext(d, 370, 470, "한국", F_H, INK); ctext(d, 370, 515, "2배 고정", F_M, GRAY)
dial(1000, 440, 190, 1.4, NAVY)
d.arc([1000 - 250, 440 - 250, 1000 + 250, 440 + 250], 190, 318, fill=AMBER, width=8)
for ang in (190, 318):
    a = math.radians(ang); px_, py_ = 1000 + 250 * math.cos(a), 440 + 250 * math.sin(a)
    d.ellipse([px_ - 10, py_ - 10, px_ + 10, py_ + 10], fill=AMBER)
ctext(d, 1000, 470, "홍콩", F_H, INK); ctext(d, 1000, 515, "상한 2배 안에서 조정", F_M, GRAY)
box(d, (90, 600, 1310, 700), SAND, "홍콩은 올해 7월 상한 2배는 그대로 두고, 배율을 하루 단위로 낮출 수 있는 구조를 허용했다.\n한국은 지금 법으로는 배율을 바꾸기 어려울 수 있어, 법을 고치는 방안을 검토하고 있다", F_S, INK)
footc(d, "근거: 공부노트 §4-2 — 홍콩 SFC 보도(The Standard·머니투데이)[21], 한국 검토는 보도[15]")
save(im, "L11_hongkong_dial.png")

# ============ L12 2.3조 vs 54조 ============
im, d = canvas("손실 2.3조와 54조 — 재는 자가 다르다", "같은 상품의 손실을 두고 23배 차이 나는 두 숫자")
RX0, RX1 = 120, 1280; FULL = 54.0
def ruler_ticks(y):
    for k in range(0, 55, 5):
        x = RX0 + k / FULL * (RX1 - RX0); d.line([x, y, x, y + (14 if k % 10 == 0 else 8)], fill=GRAY, width=2)
        if k % 10 == 0: ctext(d, x, y - 26, f"{k}조", F_SM, GRAY)
ruler_ticks(190)
d.rectangle([RX0, 220, RX0 + 2.3242 / FULL * (RX1 - RX0), 290], fill=OKC)
ltext(d, RX0 + 70, 228, "2조 3,242억 원", F_MID, OKC)
x = RX0 + 70
for t in ("확정손실(판 뒤 손실만)", "증권사 10곳 개인", "5월 27일 ~ 8월 14일"):
    w = chip(d, x, 300, t, OKC, F_S); x += w + 14
dashed_rect(d, (RX0, 390, RX1, 460), RED, 3)
for k in range(0, int(RX1 - RX0), 28): d.line([RX0 + k, 458, RX0 + k + 20, 392], fill=(245, 200, 200), width=3)
ctext(d, (RX0 + RX1) / 2, 400, "54조 원", F_MID, RED)
x = RX0
for t in ("추정", "원문 미확인", "금융위원장 「시장 논평」"):
    w = chip(d, x, 476, t, (160, 70, 70), F_S); x += w + 14
box(d, (90, 600, 1310, 700), SAND, "2.3조는 금감원이 증권사 10곳에서 받은, 개인이 이미 팔아서 확정된 손실만 더한 값이다.\n54조는 더 넓게 잡은 추정치로 알려졌지만 원문을 확인하지 못했다", F_S, INK)
footc(d, "근거: 금감원 자료 보도[10](5.27~8.14), 국감 답변 보도[11], 전자신문[29]. 54조는 추정·원문 미확인")
save(im, "L12_two_rulers.png")

# ============ L13 시간띠 ============
im, d = canvas("1월 발표, 5월 상장, 7월 대책, 10월 국감", "단일종목 2배 상품이 걸어온 길 (2026년) — 위의 선은 KODEX SK하이닉스 2배 상품 종가")
T0, T1 = dt.date(2026, 1, 1), dt.date(2026, 10, 31); TX0, TX1 = 110, 1300; TL = 470
def tx(day): return TX0 + (day - T0).days / (T1 - T0).days * (TX1 - TX0)
def ty(p): return 380 - p / 45000 * 200
d.rectangle([tx(dt.date(2026, 5, 27)), 170, TX1, 385], fill=BAND)
d.line([(tx(a), ty(v)) for a, v in KDX], fill=LEV, width=3)
ltext(d, TX1 - 140, 178, "2배 상품 종가", F_SM, LEV)
d.line([TX0, TL, TX1, TL], fill=INK, width=4)
for m in range(1, 11):
    xm = tx(dt.date(2026, m, 1)); d.line([xm, TL - 6, xm, TL + 6], fill=INK, width=2); ltext(d, xm + 4, TL - 34, f"{m}월", F_SM, GRAY)
# 정렬: c 가운데 · r 표시점 왼쪽에서 끝남 · l 표시점 오른쪽에서 시작 — 아래 줄 라벨이 위 줄 지시선과 안 겹치게
EV = ((dt.date(2026, 1, 30), "1/30 허용 발표", 0, "c"), (dt.date(2026, 5, 27), "5/27 상장", 0, "r"), (dt.date(2026, 6, 22), "6/22 최고점", 1, "c"),
      (dt.date(2026, 7, 16), "7/16 1차 대책", 0, "l"), (dt.date(2026, 10, 8), "10/8 국감 사과", 0, "r"),
      (dt.date(2026, 10, 15), "10/15 두 번째 급락", 1, "r"))
for day, lab, tier, al in EV:
    x = tx(day); y = 500 if tier == 0 else 540
    d.line([x, TL, x, y + 12], fill=GRAY, width=2); d.ellipse([x - 9, TL - 9, x + 9, TL + 9], fill=RED if "급락" in lab or "최고" in lab else NAVY)
    w = d.textlength(lab, font=F_S)
    if al == "c": ctext(d, x, y + 2, lab, F_S, INK)
    elif al == "r": ltext(d, x - 8 - w, y + 2, lab, F_S, INK)
    else: ltext(d, x + 8, y + 2, lab, F_S, INK)
box(d, (90, 600, 1310, 700), SAND, "허용 발표부터 상장까지 넉 달이 채 안 걸렸고, 상장부터 1차 대책까지는 50일이었다.\n10월 국감에서 금융위원장(8일)과 한국은행 총재(12일)가 사과했고, 같은 주에 두 번째 급락이 왔다", F_S, INK)
footc(d, "근거: 공부노트 §1(금융위 보도자료[1][2][8], 국감 보도[10][12], 급락 보도[19]), 가격 선은 네이버 종가")
save(im, "L13_timeline.png")

print("\n".join(WARN) if WARN else "넘침 경고 없음")
