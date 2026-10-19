# -*- coding: utf-8 -*-
r"""동남아 인식 글 도해 17장 — images\sea_01.png ~ sea_17.png
숫자 출처: 공부노트 「동남아인식_공부노트_2026-10-16.md」 원본 번호 그대로.
- 출국: base data\출국통계\series_202608.json (관광공사, 같은 달 전년비)
- 검색: base data\출국통계\safety_search_2025-2026.json (한 호출 안 5묶음)
- 설문: base data\설문\설문_종합.md (컨슈머인사이트 월간)
- 세 사건: base data\비교사건\세사건_비교.md · 세사건_대체지.csv
「−」 대신 「-」만 쓴다(맑은 고딕에서 깨짐).
"""
import os, json
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images"); os.makedirs(OUT, exist_ok=True)
BD = os.path.join(HERE, "base data")

for f in ("malgun.ttf", "malgunbd.ttf"):
    fm.fontManager.addfont("C:/Windows/Fonts/" + f)
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})

BG, INK, MUT = "#FBF7EE", "#1E1E1E", "#7A7A7A"
RED, NAVY, ORANGE, GREEN, BLUE, GRAY, LIGHT = "#C0392B", "#1F3A5F", "#D9822B", "#5E9A55", "#3C6E9E", "#A8A8A8", "#E7E0D0"
FOOT = "직접 만든 그림 · 걷고읽고떠나고"

# ---------------- 공통: PIL (2배로 그리고 줄인다) ----------------
S = 2
def F(sz, b=False):
    return ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", sz * S)

def canvas(w, h, bg=BG):
    im = Image.new("RGB", (w * S, h * S), bg); return im, ImageDraw.Draw(im)

def T(d, xy, s, sz, col=INK, b=False, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=F(sz, b), fill=col, anchor=anchor)

def R(d, box, fill=None, outline=None, w=0, r=0):
    x0, y0, x1, y1 = [v * S for v in box]
    d.rounded_rectangle((x0, y0, x1, y1), radius=r * S, fill=fill, outline=outline, width=w * S)

def save_pil(im, name):
    im = im.resize((im.width // S, im.height // S), Image.LANCZOS)
    im.save(os.path.join(OUT, name)); print("saved", name, im.size)

def title_pil(d, t1, t2=None, y=60):
    T(d, (70, y), t1, 44, INK, True)
    if t2: T(d, (70, y + 64), t2, 44, INK, True)

def foot_pil(d, h, src):
    T(d, (70, h - 52), FOOT + (" · " + src if src else ""), 19, MUT)

# ---------------- 공통: matplotlib ----------------
def fig_base(h=1080, title="", sub=None):
    fig = plt.figure(figsize=(10.8, h / 100), dpi=100, facecolor=BG)
    y = 1 - 75 / h
    fig.text(70 / 1080, y, title, fontsize=30, fontweight="bold", color=INK, va="center")
    if sub: fig.text(70 / 1080, y - 62 / h, sub, fontsize=17, color=NAVY, va="center")
    return fig

def ax_base(fig, rect):
    ax = fig.add_axes(rect, facecolor=BG)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#BBBBBB")
    ax.tick_params(colors="#555555", labelsize=15)
    return ax

def foot_mpl(fig, h, src):
    fig.text(70 / 1080, 34 / h, FOOT + " · " + src, fontsize=13, color=MUT, va="center")

def save_mpl(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=100, facecolor=BG); plt.close(fig); print("saved", name)

# ---------------- 데이터 ----------------
SER = json.load(open(os.path.join(BD, "출국통계", "series_202608.json"), encoding="utf-8"))
SS, TT = SER["series"], SER["total"]
def yoy(c, y, m):
    a = SS.get(f"{y-1}-{m:02d}", {}).get(c); b = SS.get(f"{y}-{m:02d}", {}).get(c)
    return round((b / a - 1) * 100, 1) if a and b else None
SAFE = json.load(open(os.path.join(BD, "출국통계", "safety_search_2025-2026.json"), encoding="utf-8"))["data"]

# =============== 01 썸네일·입구: 캄보디아만 붉은 지도 ===============
def f01():
    W = H = 1080
    im, d = canvas(W, H, "#E4F1F6")
    mp = Image.open(os.path.join(OUT, "_원본", "bg_map_a.png")).convert("RGB")
    k = 1.0  # 1024 → 1024 그대로, 위쪽 띠 아래에 붙인다
    mp = mp.resize((int(1024 * k * S), int(1024 * k * S)), Image.LANCZOS)
    MX, MY = 28, 150
    im.paste(mp, (MX * S, MY * S))
    d = ImageDraw.Draw(im)
    R(d, (0, 0, W, 175), fill=BG)
    T(d, (W // 2, 62), "캄보디아 사태 뒤", 46, INK, True, "mm")
    T(d, (W // 2, 128), "동남아 전체가 무서워졌을까?", 50, RED, True, "mm")
    P = lambda x, y: (MX + x * k, MY + y * k)
    # 캄보디아 이름표
    cx, cy = P(372, 400)
    R(d, (cx - 70, cy - 24, cx + 70, cy + 24), fill="#9E1F16", outline="white", w=3, r=24)
    T(d, (cx, cy), "캄보디아", 26, "white", True, "mm")
    # 이웃 나라 물음표
    q = [("태국", 262, 318), ("라오스", 335, 255), ("베트남", 448, 290), ("미얀마", 175, 205),
         ("말레이시아", 312, 625), ("필리핀", 795, 440), ("인도네시아", 545, 745)]
    for name, x, y in q:
        px, py = P(x, y)
        r = 30
        d.ellipse(((px - r) * S, (py - r - 14) * S, (px + r) * S, (py + r - 14) * S), fill="white", outline=NAVY, width=4 * S)
        T(d, (px, py - 14), "?", 40, NAVY, True, "mm")
        T(d, (px, py + 34), name, 22, NAVY, True, "mm")
    T(d, (W - 24, H - 24), "직접 만든 그림 · 배경 지도는 AI 생성", 17, MUT, anchor="rd")
    save_pil(im, "sea_01.png")

# ---------------- 아이콘 ----------------
def icon_search(d, cx, cy, col):
    r = 62
    d.ellipse(((cx - r) * S, (cy - r - 15) * S, (cx + r) * S, (cy + r - 15) * S), outline=col, width=16 * S)
    d.line(((cx + 44) * S, (cy + 30) * S, (cx + 92) * S, (cy + 78) * S), fill=col, width=26 * S)

def icon_heart(d, cx, cy, col):
    import math
    pts = []
    for i in range(200):
        t = 2 * math.pi * i / 200
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append(((cx + x * 5.6) * S, (cy - y * 5.6) * S))
    d.polygon(pts, fill=col)

def icon_feet(d, cx, cy, col):
    for dx, dy in ((-36, 26), (36, -26)):
        x, y = cx + dx, cy + dy
        d.ellipse(((x - 24) * S, (y - 34) * S, (x + 24) * S, (y + 48) * S), fill=col)
        for j, (tx, ty, tr) in enumerate(((-18, -50, 9), (-4, -58, 9), (11, -55, 8), (22, -46, 7))):
            d.ellipse(((x + tx - tr) * S, (y + ty - tr) * S, (x + tx + tr) * S, (y + ty + tr) * S), fill=col)

LAYERS = [("검색", icon_search, BLUE), ("마음", icon_heart, RED), ("발길", icon_feet, GREEN)]

# =============== 02 원리: 세 층 ===============
def f02():
    W, H = 1080, 1080
    im, d = canvas(W, H)
    title_pil(d, "「무서워졌다」는", "세 군데에서 따로 잰다")
    subs = [("네이버 검색량", "걱정할 때 찾는 말"), ("설문 「가 보고 싶다」", "마음이 식었나"), ("그 나라 입국자 수", "실제로 갔나")]
    cw = 300
    for i, ((name, icon, col), (s1, s2)) in enumerate(zip(LAYERS, subs)):
        x0 = 60 + i * (cw + 30); cx = x0 + cw // 2
        R(d, (x0, 260, x0 + cw, 820), fill="white", outline=LIGHT, w=3, r=26)
        icon(d, cx, 410, col)
        T(d, (cx, 560), name, 52, col, True, "mm")
        T(d, (cx, 650), s1, 24, INK, True, "mm")
        T(d, (cx, 700), s2, 24, MUT, False, "mm")
    for i in range(2):
        x = 60 + (i + 1) * (cw + 30) - 15
        T(d, (x, 540), "›", 60, GRAY, True, "mm")
    R(d, (60, 870, W - 60, 990), fill="#F1EADB", r=20)
    T(d, (W // 2, 905), "셋이 같이 움직이면 「번졌다」", 28, INK, True, "mm")
    T(d, (W // 2, 955), "하나만 움직이면 아직 모른다", 28, NAVY, False, "mm")
    foot_pil(d, H, "")
    save_pil(im, "sea_02.png")

# =============== 03 2025-10 치안 검색 ===============
def f03():
    H = 1000
    fig = fig_base(H, "2025년 10월, 걱정 검색은 캄보디아에 몰렸다", "네이버 검색량 · 다섯 묶음을 한 번에 조회 · 가장 많이 찾은 달 = 100")
    ax = ax_base(fig, [0.30, 0.16, 0.62, 0.66])
    names = ["캄보디아 납치·감금", "태국 치안", "베트남 치안", "동남아 위험", "필리핀 치안"]
    keys = ["캄보디아 납치", "태국 치안", "베트남 치안", "동남아 위험", "필리핀 치안"]
    vals = [round(SAFE[k]["2025-10"], 1) for k in keys]
    cols = [RED, ORANGE, GREEN, GRAY, BLUE]
    y = list(range(len(names)))[::-1]
    ax.barh(y, vals, color=cols, height=0.62)
    for yi, v in zip(y, vals):
        lab = "100" if v >= 100 else f"{v:.1f}"
        ax.text(v + 1.5, yi, lab, va="center", fontsize=22, fontweight="bold", color=INK)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=19)
    ax.set_xlim(0, 112); ax.set_xticks([0, 50, 100])
    foot_mpl(fig, H, "네이버 데이터랩 검색어 트렌드(2025-06~2026-09)")
    save_mpl(fig, "sea_03.png")

# =============== 04 이웃 치안 검색 한 달 만에 원위치 ===============
def f04():
    H = 1000
    fig = fig_base(H, "이웃 나라 치안 검색은 한 달 만에 내려왔다", "같은 조회 안의 값 · 캄보디아(10월 100)는 이 그래프 밖")
    ax = ax_base(fig, [0.10, 0.20, 0.84, 0.60])
    ms = ["2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03"]
    lab = ["6월", "7월", "8월", "9월", "10월", "11월", "12월", "1월", "2월", "3월"]
    for k, c, nm in (("태국 치안", ORANGE, "태국 치안"), ("베트남 치안", GREEN, "베트남 치안")):
        v = [SAFE[k][m] for m in ms]
        ax.plot(range(len(ms)), v, color=c, lw=4, marker="o", ms=8)
        ax.text(len(ms) - 0.85, v[-1] + (0.12 if c == GREEN else -0.12), nm, color=c, fontsize=17, fontweight="bold", va="center")
    ax.axvspan(3.5, 4.5, color=RED, alpha=0.10)
    ax.text(4, 3.25, "캄보디아 사태", ha="center", fontsize=16, color=RED, fontweight="bold")
    ax.text(4.12, SAFE["태국 치안"]["2025-10"], f'{SAFE["태국 치안"]["2025-10"]:.1f}', fontsize=17, color=ORANGE, va="bottom", fontweight="bold")
    ax.text(3.85, SAFE["베트남 치안"]["2025-10"], f'{SAFE["베트남 치안"]["2025-10"]:.1f}', fontsize=17, color=GREEN, va="center", ha="right", fontweight="bold")
    ax.set_xticks(range(len(ms))); ax.set_xticklabels(lab, fontsize=15)
    ax.set_xlim(-0.3, len(ms) + 0.9); ax.set_ylim(0, 3.5)
    ax.text(-0.2, -0.5, "2025", fontsize=13, color=MUT); ax.text(6.8, -0.5, "2026", fontsize=13, color=MUT)
    foot_mpl(fig, H, "네이버 데이터랩 검색어 트렌드")
    save_mpl(fig, "sea_04.png")

# =============== 05 「동남아 가 보고 싶다」 27.1 → 20.5 ===============
SEA25 = [30.2, 32.6, 27.1, 20.5, 23.8, 23.8]
SEA24 = [37.3, 36.4, 33.8, 34.8, 35.0, 34.3]   # 원문 전년 동월 대비 %p 로 역산
M6 = ["7월", "8월", "9월", "10월", "11월", "12월"]
CI_SRC = "컨슈머인사이트 월간 여행 동향(2025년 7~12월호)"

def f05():
    H = 1000
    fig = fig_base(H, "「동남아 가 보고 싶다」, 10월에 꺾였다", "「요즘 동남아를 가 보고 싶은 생각이 예전보다 커졌다」고 답한 비율(%)")
    ax = ax_base(fig, [0.10, 0.14, 0.84, 0.64])
    x = range(6)
    cols = [GRAY, GRAY, NAVY, RED, GRAY, GRAY]
    ax.bar(x, SEA25, color=cols, width=0.62)
    for xi, v in zip(x, SEA25):
        ax.text(xi, v + 0.6, f"{v}", ha="center", fontsize=19, fontweight="bold", color=INK)
    ax.annotate("", xy=(2.72, 21.6), xytext=(2.34, 26.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=3, mutation_scale=28))
    ax.text(3.0, 33.0, "-24%", ha="center", fontsize=40, fontweight="bold", color=RED)
    ax.set_xticks(list(x)); ax.set_xticklabels(M6, fontsize=17)
    ax.set_ylim(0, 40); ax.set_yticks([0, 10, 20, 30, 40])
    ax.text(-0.4, -4.8, "2025", fontsize=13, color=MUT)
    foot_mpl(fig, H, CI_SRC)
    save_mpl(fig, "sea_05.png")

# =============== 06 1년 전과의 틈 ===============
def f06():
    H = 1000
    fig = fig_base(H, "1년 전과의 틈은 사태 전부터 있었고, 12월까지 남았다", None)
    fig.texts[0].set_fontsize(25)
    ax = ax_base(fig, [0.10, 0.14, 0.80, 0.68])
    x = range(6)
    ax.plot(x, SEA24, color=GRAY, lw=3.5, ls="--", marker="o", ms=7)
    ax.plot(x, SEA25, color=RED, lw=4.5, marker="o", ms=9)
    ax.text(5.15, SEA24[-1], "1년 전", color=MUT, fontsize=17, va="center", fontweight="bold")
    ax.text(5.15, SEA25[-1], "2025년", color=RED, fontsize=17, va="center", fontweight="bold")
    for xi, lab in ((0, "-7.1%p"), (3, "-14.3%p"), (5, "-10.5%p")):
        ax.vlines(xi, SEA25[xi] + 0.4, SEA24[xi] - 0.4, color=NAVY, lw=2)
        ax.text(xi + 0.08, (SEA25[xi] + SEA24[xi]) / 2, lab, fontsize=17, color=NAVY, fontweight="bold", va="center")
    ax.axvspan(2.5, 3.5, color=RED, alpha=0.08)
    ax.text(3, 41.3, "캄보디아 사태", ha="center", fontsize=15, color=RED, fontweight="bold")
    ax.set_xticks(list(x)); ax.set_xticklabels(M6, fontsize=17)
    ax.set_xlim(-0.3, 5.9); ax.set_ylim(15, 43)
    foot_mpl(fig, H, "컨슈머인사이트 월간 여행 동향 · 1년 전 값은 원문의 「전년 대비」로 거꾸로 계산")
    save_mpl(fig, "sea_06.png")

# =============== 07 노재팬과 같은 지표, 시간 흐름 ===============
def f07():
    H = 1040
    fig = fig_base(H, "같은 설문, 노재팬은 바닥에서 안 올라왔다", "「가 보고 싶다」 비율(%) · 사건 직전 달부터 넉 달")
    ax = ax_base(fig, [0.10, 0.16, 0.78, 0.64])
    x = [0, 1, 2, 3]
    nj = [25, 12, 5, 5]
    ca = [27.1, 20.5, 23.8, 23.8]
    ax.plot(x, nj, color=NAVY, lw=4.5, marker="o", ms=10)
    ax.plot(x, ca, color=RED, lw=4.5, marker="o", ms=10)
    for xi, v in zip(x, nj): ax.text(xi, v - 2.6, f"{v}", ha="center", fontsize=18, color=NAVY, fontweight="bold")
    for xi, v in zip(x, ca): ax.text(xi, v + 1.2, f"{v}", ha="center", fontsize=18, color=RED, fontweight="bold")
    ax.text(3.15, 5, "일본\n(2019 노재팬)", color=NAVY, fontsize=16, fontweight="bold", va="center")
    ax.text(3.15, 23.8, "동남아\n(2025 캄보디아)", color=RED, fontsize=16, fontweight="bold", va="center")
    ax.set_xticks(x); ax.set_xticklabels(["사건 전 달", "사건 달", "+1달", "+2달"], fontsize=17)
    ax.set_xlim(-0.3, 3.9); ax.set_ylim(0, 32)
    fig.text(0.10, 0.105, "일본: 2019년 6·7·8·9월   ·   동남아: 2025년 9·10·11·12월", fontsize=14, color=MUT)
    foot_mpl(fig, H, "컨슈머인사이트 여행 조사 · 2019년 값은 기사(머니S 2019-10-12) 정수")
    save_mpl(fig, "sea_07.png")

# =============== 08 마음을 접은 몫 80% vs 24% ===============
def f08():
    W, H = 1080, 1000
    im, d = canvas(W, H)
    title_pil(d, "가 보고 싶다던 마음,", "얼마나 접혔나")
    rows = [("2019 노재팬 · 일본", "25% → 5%", 80, NAVY), ("2025 캄보디아 사태 · 동남아", "27.1% → 20.5%", 24, RED)]
    for i, (nm, fr, pct, col) in enumerate(rows):
        y = 300 + i * 270
        T(d, (70, y), nm, 30, col, True)
        T(d, (W - 70, y + 4), fr, 26, MUT, False, "ra")
        bx0, bx1 = 70, W - 70
        R(d, (bx0, y + 60, bx1, y + 150), fill="#EFE8D8", r=14)
        R(d, (bx0, y + 60, bx0 + (bx1 - bx0) * pct / 100, y + 150), fill=col, r=14)
        ex = bx0 + (bx1 - bx0) * pct / 100
        if pct > 50: T(d, (ex - 24, y + 105), f"{pct}% 접힘", 40, "white", True, "rm")
        else: T(d, (ex + 18, y + 105), f"{pct}% 접힘", 40, col, True, "lm")
    R(d, (70, 830, W - 70, 920), fill="#F1EADB", r=18)
    T(d, (W // 2, 875), "같은 잣대: 사건 전 달 → 가장 낮은 달", 27, INK, True, "mm")
    foot_pil(d, H + 10, "컨슈머인사이트 · 24%는 -24.35%를 반올림")
    save_pil(im, "sea_08.png")

# =============== 09 해외여행 계획률 ===============
def f09():
    H = 1000
    fig = fig_base(H, "해외여행 계획은 10월에 오히려 늘었다", "앞으로 6개월 안에 해외여행 계획이 있다(%)")
    ax = ax_base(fig, [0.10, 0.16, 0.84, 0.64])
    v = [45.6, 43.0, 44.6, 46.1, 44.6, 45.8]
    ax.plot(range(6), v, color=BLUE, lw=4.5, marker="o", ms=10)
    for xi, val in enumerate(v):
        ax.text(xi, val + 0.45, f"{val}", ha="center", fontsize=19, fontweight="bold", color=NAVY if xi in (2, 3) else INK)
    ax.axvspan(2.5, 3.5, color=RED, alpha=0.08)
    ax.text(3, 49.2, "캄보디아 사태", ha="center", fontsize=15, color=RED, fontweight="bold")
    ax.set_ylim(40, 50); ax.set_yticks([40, 45, 50])
    ax.set_xticks(range(6)); ax.set_xticklabels(M6, fontsize=17)
    ax.text(-0.3, 38.7, "2025", fontsize=13, color=MUT)
    foot_mpl(fig, H, CI_SRC)
    save_mpl(fig, "sea_09.png")

# =============== 10 발길: 캄보디아만 절벽 ===============
def f10():
    H = 1040
    fig = fig_base(H, "발길이 끊긴 건 캄보디아 한 나라였다", "한국인 방문객, 1년 전 같은 달보다(%)")
    ax = ax_base(fig, [0.12, 0.14, 0.74, 0.68])
    mm = [(2025, 9), (2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2)]
    lab = ["9월", "10월", "11월", "12월", "1월", "2월"]
    for c, col in (("캄보디아", RED), ("태국", ORANGE), ("베트남", GREEN), ("필리핀", BLUE)):
        v = [yoy(c, y, m) for y, m in mm]
        ax.plot(range(6), v, color=col, lw=5 if c == "캄보디아" else 3, marker="o", ms=9 if c == "캄보디아" else 6)
        dy = {"캄보디아": 0, "태국": -3, "베트남": 3, "필리핀": -1}[c]
        ax.text(5.18, v[-1] + dy, c, color=col, fontsize=18, fontweight="bold", va="center")
    v = [yoy("캄보디아", y, m) for y, m in mm]
    for xi in (2, 3, 4, 5):
        ax.text(xi, v[xi] - 7, f"{v[xi]}", ha="center", fontsize=16, color=RED, fontweight="bold")
    ax.axhline(0, color="#999999", lw=1.2)
    ax.axvspan(0.5, 1.5, color=RED, alpha=0.08)
    ax.text(1, 27, "사태", ha="center", fontsize=15, color=RED, fontweight="bold")
    ax.set_xticks(range(6)); ax.set_xticklabels(lab, fontsize=17)
    ax.set_ylim(-85, 32); ax.set_xlim(-0.3, 5.9)
    ax.text(-0.3, -97, "2025", fontsize=13, color=MUT); ax.text(3.7, -97, "2026", fontsize=13, color=MUT)
    foot_mpl(fig, H, "한국관광공사 국민 해외관광객 주요 목적지별 통계(2026년 8월 기준)")
    save_mpl(fig, "sea_10.png")

# =============== 11 태국·필리핀은 사태 전부터 ===============
def f11():
    H = 1000
    fig = fig_base(H, "태국·필리핀은 사태 전부터 줄고 있었다", "한국인 방문객, 1년 전 같은 달보다(%) · 2025년 1~9월")
    ax = ax_base(fig, [0.10, 0.14, 0.84, 0.66])
    import numpy as np
    x = np.arange(9)
    th = [yoy("태국", 2025, m) for m in range(1, 10)]
    ph = [yoy("필리핀", 2025, m) for m in range(1, 10)]
    ax.bar(x - 0.2, th, width=0.38, color=ORANGE, label="태국")
    ax.bar(x + 0.2, ph, width=0.38, color=BLUE, label="필리핀")
    ax.axhline(0, color="#999999", lw=1.2)
    ax.set_xticks(x); ax.set_xticklabels([f"{m}월" for m in range(1, 10)], fontsize=16)
    ax.set_ylim(-40, 8)
    ax.legend(loc="lower left", fontsize=17, frameon=False, ncol=2)
    ax.text(8.6, 4, "10월\n사태 →", fontsize=16, color=RED, fontweight="bold", ha="center", va="center")
    ax.set_xlim(-0.6, 9.1)
    foot_mpl(fig, H, "한국관광공사 국민 해외관광객 주요 목적지별 통계")
    save_mpl(fig, "sea_11.png")

# =============== 12 이웃이 받았나 ===============
def f12():
    H = 1080
    fig = fig_base(H, "노재팬 땐 이웃이 늘었고, 이번엔 이웃도 줄었다", "사건 뒤 6개월, 한국인 방문객이 1년 전보다(%)")
    fig.texts[0].set_fontsize(27)
    def panel(rect, ttl, names, vals, cols):
        ax = ax_base(fig, rect)
        ax.bar(range(len(vals)), vals, color=cols, width=0.62)
        for i, v in enumerate(vals):
            ax.text(i, v + (3 if v >= 0 else -3), f"{v:+.1f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=16, fontweight="bold", color=INK)
        ax.axhline(0, color="#999999", lw=1.2)
        ax.set_xticks(range(len(vals))); ax.set_xticklabels(names, fontsize=16)
        ax.set_ylim(-80, 50); ax.set_yticks([-60, -30, 0, 30])
        ax.set_title(ttl, fontsize=20, fontweight="bold", color=INK, pad=14)
    panel([0.09, 0.17, 0.38, 0.62], "2019 노재팬", ["일본", "대만", "베트남", "필리핀"], [-60.0, 35.4, 26.9, 25.9], [NAVY, GREEN, GREEN, GREEN])
    panel([0.57, 0.17, 0.38, 0.62], "2025 캄보디아 사태", ["캄보디아", "태국", "필리핀", "베트남"], [-61.4, -18.3, -11.0, -1.7], [RED, ORANGE, ORANGE, ORANGE])
    fig.text(0.09, 0.105, "노재팬: 2019년 8월~2020년 1월 · 캄보디아: 2025년 11월~2026년 4월", fontsize=14, color=MUT)
    foot_mpl(fig, H, "한국관광공사 목적지별 통계 · 일본은 JNTO와 대조")
    save_mpl(fig, "sea_12.png")

# =============== 13 2026년 봄 이후는 비용과 시점 ===============
def f13():
    H = 1040
    fig = fig_base(H, "이웃 나라가 크게 빠진 건 유류할증료가 오른 뒤", "한국인 방문객, 1년 전 같은 달보다(%) · 2026년")
    fig.texts[0].set_fontsize(27)
    ax = ax_base(fig, [0.10, 0.14, 0.78, 0.64])
    ms = range(1, 9)
    for c, col in (("태국", ORANGE), ("베트남", GREEN)):
        v = [yoy(c, 2026, m) for m in ms]
        ax.plot(range(8), v, color=col, lw=4, marker="o", ms=8)
        ax.text(7.18, v[-1], c, color=col, fontsize=18, fontweight="bold", va="center")
    ax.axhline(0, color="#999999", lw=1.2)
    ax.axvspan(3.5, 6.5, color=GRAY, alpha=0.18)
    ax.axvline(1.5, color=NAVY, lw=2, ls=":")
    ax.text(1.55, 24, "2월 말\n이란 전쟁", fontsize=15, color=NAVY, fontweight="bold", va="top")
    ax.text(5.0, 24, "유류할증료 최고 단계(5월)\n동남아 노선 감편(5~7월)", fontsize=15, color=INK, fontweight="bold", va="top", ha="center")
    ax.text(5, yoy("태국", 2026, 6) - 3, f'{yoy("태국", 2026, 6)}', fontsize=17, color=ORANGE, fontweight="bold", ha="center", va="top")
    ax.set_xticks(range(8)); ax.set_xticklabels([f"{m}월" for m in ms], fontsize=17)
    ax.set_ylim(-62, 28); ax.set_xlim(-0.3, 7.9)
    foot_mpl(fig, H, "한국관광공사 목적지별 통계 · 유가·감편은 기사(뉴스1·뉴시스·MTN)")
    save_mpl(fig, "sea_13.png")

# ---------------- 아이콘 2 ----------------
def icon_no(d, cx, cy, col, r=70):
    d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), outline=col, width=14 * S)
    o = r * 0.7
    d.line(((cx - o) * S, (cy + o) * S, (cx + o) * S, (cy - o) * S), fill=col, width=14 * S)

def icon_warn(d, cx, cy, col, r=80):
    pts = [(cx * S, (cy - r) * S), ((cx + r * 0.95) * S, (cy + r * 0.7) * S), ((cx - r * 0.95) * S, (cy + r * 0.7) * S)]
    d.polygon(pts, fill=col)
    T(d, (cx, cy + 12), "!", 70, "white", True, "mm")

# =============== 14 선택 vs 불안 (해석) ===============
def f14():
    W, H = 1080, 1080
    im, d = canvas(W, H)
    title_pil(d, "노재팬은 여행을 줄였고,", "이번엔 행선지를 바꿨다")
    R(d, (W - 190, 66, W - 70, 112), fill=NAVY, r=22)
    T(d, (W - 130, 89), "해석", 24, "white", True, "mm")
    cols = [("2019 노재팬", "안 간다", icon_no, NAVY, "-8.2%"), ("2025 캄보디아", "무섭다", icon_warn, RED, "+5.2%")]
    for i, (nm, word, ic, col, num) in enumerate(cols):
        x0 = 70 + i * 480; cx = x0 + 230
        R(d, (x0, 250, x0 + 460, 880), fill="white", outline=LIGHT, w=3, r=26)
        T(d, (cx, 300), nm, 28, col, True, "mm")
        ic(d, cx, 420, col)
        T(d, (cx, 560), word, 46, col, True, "mm")
        T(d, (cx, 680), "해외 출국 전체", 24, MUT, False, "mm")
        T(d, (cx, 760), num, 64, INK, True, "mm")
    T(d, (W // 2, 930), "사건 뒤 6개월, 1년 전보다 · 한국 쪽 출국 기록", 24, MUT, False, "mm")
    foot_pil(d, H, "한국관광공사 목적지별 통계 「전체」 열")
    save_pil(im, "sea_14.png")

# =============== 15 한한령은 방향이 반대 ===============
def f15():
    W, H = 1080, 1000
    im, d = canvas(W, H)
    title_pil(d, "한한령은 막힌 쪽이 반대였다")
    T(d, (70, 140), "2017년, 1년 전보다", 26, NAVY)
    # 두 나라 상자
    R(d, (70, 300, 330, 560), fill="#F3D9D5", r=30); T(d, (200, 430), "중국", 52, RED, True, "mm")
    R(d, (750, 300, 1010, 560), fill="#D8E3EF", r=30); T(d, (880, 430), "한국", 52, NAVY, True, "mm")
    def arrow(y, x0, x1, th, col):
        hd = max(th * 1.1, 40)
        if x1 > x0:
            d.rectangle((x0 * S, (y - th / 2) * S, (x1 - hd) * S, (y + th / 2) * S), fill=col)
            d.polygon([((x1 - hd) * S, (y - hd * 0.8) * S), (x1 * S, y * S), ((x1 - hd) * S, (y + hd * 0.8) * S)], fill=col)
        else:
            d.rectangle(((x1 + hd) * S, (y - th / 2) * S, x0 * S, (y + th / 2) * S), fill=col)
            d.polygon([((x1 + hd) * S, (y - hd * 0.8) * S), (x1 * S, y * S), ((x1 + hd) * S, (y + hd * 0.8) * S)], fill=col)
    arrow(375, 345, 735, 50, RED)
    T(d, (540, 290), "중국인 → 한국  -48.3%", 30, RED, True, "mm")
    arrow(510, 735, 345, 22, NAVY)
    T(d, (540, 575), "한국인 → 중국  -19.1%", 30, NAVY, True, "mm")
    R(d, (70, 700, W - 70, 840), fill="#F1EADB", r=20)
    T(d, (W // 2, 745), "막힌 건 중국인의 한국 단체관광", 30, INK, True, "mm")
    T(d, (W // 2, 795), "(2017년 3월 15일부터, 중국 쪽 조치)", 24, MUT, False, "mm")
    foot_pil(d, H, "KOSIS 방한 외래객 · 중국통계연감 표17-13(연간)")
    save_pil(im, "sea_15.png")

# =============== 16 경보는 지역에 걸린다 ===============
def f16():
    W, H = 1080, 1140
    im, d = canvas(W, H)
    title_pil(d, "여행경보는 나라가 아니라", "지역에 걸린다")
    T(d, (70, 200), "캄보디아, 2026년 7월 9일 조정 기준", 26, NAVY)
    steps = [("4단계 여행금지", "#222222", "white", "없음 (2026년 7월 3단계로 내림)"),
             ("3단계 출국권고", "#C62828", "white", "태국 국경 50km 안 · 시하누크빌시 · 보코산 · 바벳 · 포이펫"),
             ("2단계 여행자제", "#E0A800", INK, "시하누크빌주"),
             ("1단계 여행유의", "#1F3A8A", "white", "그 밖 전역")]
    for i, (lv, col, fc, where) in enumerate(steps):
        y = 280 + i * 175
        R(d, (70, y, 360, y + 135), fill=col, r=20)
        T(d, (215, y + 67), lv, 30, fc, True, "mm")
        R(d, (380, y, W - 70, y + 135), fill="white", outline=LIGHT, w=3, r=20)
        if len(where) > 22:
            a, b = "태국 국경 50km 안 · 시하누크빌시", "보코산 · 바벳 · 포이펫"
            T(d, (410, y + 45), a, 26, INK, True, "lm"); T(d, (410, y + 92), b, 26, INK, True, "lm")
        else:
            T(d, (410, y + 67), where, 28, INK, True, "lm")
    T(d, (W // 2, 1010), "외교부 해외안전여행(0404.go.kr) 「국가별 여행경보」", 26, NAVY, True, "mm")
    foot_pil(d, H, "외교부 보도자료 2026-07-09 「상반기 여행경보 정기 조정」")
    save_pil(im, "sea_16.png")

# =============== 17 결론 ===============
def f17():
    W, H = 1080, 1140
    im, d = canvas(W, H)
    title_pil(d, "그래서, 동남아가", "무서워졌을까")
    res = [("검색", "한 달", "이웃 나라 치안 검색은 11월에 내려옴"),
           ("마음", "-24%", "노재팬(-80%)보다 약하게, 석 달 넘게"),
           ("발길", "캄보디아만", "이웃은 사태 전부터 줄던 흐름")]
    for i, ((name, icon, col), (n, big, small)) in enumerate(zip(LAYERS, res)):
        y = 260 + i * 255
        R(d, (70, y, W - 70, y + 220), fill="white", outline=LIGHT, w=3, r=26)
        # 작은 아이콘
        sub, sd = canvas(240, 240, "white")
        icon(sd, 120, 125, col)
        sub = sub.resize((int(240 * S * 0.62), int(240 * S * 0.62)), Image.LANCZOS)
        im.paste(sub, (int(95 * S), int((y + 35) * S)))
        T(d, (290, y + 62), name, 30, col, True, "lm")
        T(d, (290, y + 132), big, 54, INK, True, "lm")
        T(d, (W - 100, y + 190), small, 22, MUT, False, "rm")
    foot_pil(d, H, "컨슈머인사이트 · 네이버 데이터랩 · 한국관광공사")
    save_pil(im, "sea_17.png")

if __name__ == "__main__":
    for f in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12, f13, f14, f15, f16, f17):
        f()
