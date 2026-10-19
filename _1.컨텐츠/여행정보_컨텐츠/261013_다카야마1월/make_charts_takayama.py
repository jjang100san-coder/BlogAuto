# -*- coding: utf-8 -*-
"""다카야마 1월 그래프 3장 + 결론 카드 (시라카와고 편과 같은 꼴).
① chart_0115_dawn.png      해마다 1월 15일 새벽 6시 기온·쌓인 눈 (高山 시간별)
② chart_depth_compare.png  1월 가장 많이 쌓인 눈: 다카야마 vs 시라카와고
③ chart_mid_low.png        1월 중순 아침 최저 평균: 다카야마 vs 게로(하기와라)
④ card_conclusion.png
자료: ..\\261012_시라카와고1월\\base data\\chubu_daily.json, takayama_hourly_0114_0115.json (기상청, 2026-10-12·13 수집)
반올림은 사사오입(half-up) — 본문 표와 같은 값.
"""
import json, os, sys
from decimal import Decimal, ROUND_HALF_UP
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
BD = os.path.join(HERE, '..', '261012_시라카와고1월', 'base data')
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
BG, INK, MUT, RED, NAVY, SNOW, GREEN = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#8fb3d9", "#5b8c6e"
D = json.load(open(os.path.join(BD, 'chubu_daily.json'), encoding='utf-8'))
HR = json.load(open(os.path.join(BD, 'takayama_hourly_0114_0115.json'), encoding='utf-8'))
YEARS = list(range(2016, 2027)); X = list(range(len(YEARS)))
r1 = lambda x: float(Decimal(str(x)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
v = lambda x: x if x is not None else 0.0
T = {y: D['다카야마']['%d-01' % y] for y in YEARS}; S = {y: D['시라카와']['%d-01' % y] for y in YEARS}; G = {y: D['게로시하기와라']['%d-01' % y] for y in YEARS}
def frame(ax):
    ax.set_facecolor(BG); ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
FOOT = "일본 기상청 高山 관측소 값 · 직접 만든 그래프 · 걷고읽고떠나고"

# ① 1/15 06시
t6 = [HR['%d-01-15' % y]['hours']['6']['temp'] for y in YEARS]
d6 = [v(HR['%d-01-15' % y]['hours']['6']['snow_depth']) for y in YEARS]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8), dpi=110, facecolor=BG, sharex=True); frame(a1); frame(a2)
a1.bar(X, t6, 0.55, color=[NAVY if t < 0 else SNOW for t in t6])
for i, t in enumerate(t6): a1.text(i, t + (0.35 if t >= 0 else -0.75), f"{t:.1f}", ha="center", fontsize=12, color=INK, fontweight="bold")
a1.axhline(0, color=INK, lw=1); a1.set_ylim(-7.5, 3.5)
a1.set_title("1월 15일 새벽 6시 다카야마 기온 (℃)", fontsize=16, color=INK, loc="left", fontweight="bold")
a2.bar(X, d6, 0.55, color=SNOW)
for i, d in enumerate(d6): a2.text(i, d + 1.2, ("없음" if d == 0 else f"{d:.0f}cm"), ha="center", fontsize=12, color=INK if d else MUT, fontweight="bold" if d else None)
a2.set_ylim(0, 58); a2.set_title("같은 시각 쌓여 있던 눈", fontsize=16, color=INK, loc="left", fontweight="bold")
a2.set_xticks(X); a2.set_xticklabels([str(y) for y in YEARS], fontsize=12)
fig.text(0.01, 0.01, "일본 기상청 高山 관측소 시간별값(1월 15일 6시) · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_0115_dawn.png"), facecolor=BG); plt.close(fig)

# ② 1월 최심적설 비교
mt = [max(v(r['snow_depth']) for r in T[y]) for y in YEARS]; ms = [max(v(r['snow_depth']) for r in S[y]) for y in YEARS]
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); frame(ax)
w = 0.38
ax.bar([i - w / 2 for i in X], ms, w, color=SNOW, label="시라카와고(白川)")
ax.bar([i + w / 2 for i in X], mt, w, color=NAVY, label="다카야마(高山)")
for i, (a, b) in enumerate(zip(ms, mt)):
    ax.text(i - w / 2, a + 3, f"{a:.0f}", ha="center", fontsize=10, color=MUT)
    ax.text(i + w / 2, b + 3, f"{b:.0f}", ha="center", fontsize=11, color=NAVY, fontweight="bold")
ax.set_xticks(X); ax.set_xticklabels([str(y) for y in YEARS], fontsize=12); ax.set_ylim(0, 265); ax.set_ylabel("cm", color=MUT)
ax.set_title("1월에 가장 많이 쌓였던 눈 — 같은 해, 버스로 한 시간 거리", fontsize=17, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(frameon=False, loc="upper right", fontsize=12)
fig.text(0.01, 0.01, "일본 기상청 白川·高山 관측소 일별 최심적설 2016~2026 · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_depth_compare.png"), facecolor=BG); plt.close(fig)

# ③ 중순 아침 최저 평균
lt = [r1(sum(r['lo'] for r in T[y][10:20]) / 10) for y in YEARS]; lg = [r1(sum(r['lo'] for r in G[y][10:20]) / 10) for y in YEARS]
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); frame(ax)
ax.plot(X, lt, color=NAVY, lw=2.8, marker="o", label="다카야마(高山)")
ax.plot(X, lg, color=GREEN, lw=2.8, marker="o", label="게로시(萩原)")
for i, (a, b) in enumerate(zip(lt, lg)):
    ax.text(i, a - 0.55, f"{a:.1f}", ha="center", fontsize=10, color=NAVY)
    ax.text(i, b + 0.3, f"{b:.1f}", ha="center", fontsize=10, color=GREEN)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(X); ax.set_xticklabels([str(y) for y in YEARS], fontsize=12); ax.set_ylim(-6.5, 1.5); ax.set_ylabel("℃", color=MUT)
ax.set_title("1월 중순(11~20일) 아침 최저 평균 — 다카야마와 게로", fontsize=17, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(frameon=False, loc="upper left", fontsize=12)
fig.text(0.01, 0.01, "일본 기상청 高山·萩原(게로시 하기와라) 관측소 일별값 · 게로 온천가 관측소는 없음 · 직접 만든 그래프", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_mid_low.png"), facecolor=BG); plt.close(fig)

# ④ 카드
W, H = 1400, 1400; LINE, PALE = "#e2e2e2", "#eef2f8"
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", s)
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); X0, X1 = 70, W - 70
d.text((X0, 58), "1월 15일 새벽 6시 다카야마,", font=F(56, True), fill=INK)
d.text((X0, 132), "11년 중 5년은 맨길이었어", font=F(56, True), fill=NAVY)
d.text((X0, 220), "일본 기상청 高山 관측소 2016~2026년 11년치 · 시간별값", font=F(22), fill=MUT)
rows = [("새벽 6시 쌓인 눈", "없음 5번 · 4~50cm 6번", "50cm는 2017년, 전날 저녁 6시부터 새벽 6시까지 27cm가 내렸어", True),
        ("새벽 6시 기온", f"{min(t6):.1f}도 ~ {max(t6):.1f}도", f"영하인 해 {sum(1 for t in t6 if t < 0)}번, 영상인 해 {sum(1 for t in t6 if t > 0)}번", False),
        ("1월 가장 많이 쌓인 눈", f"다카야마 {min(mt):.0f}~{max(mt):.0f}cm · 시라카와고 {min(ms):.0f}~{max(ms):.0f}cm", "같은 해 시라카와고가 늘 더 많았어", False)]
y = 296
for t, a, b, hl in rows:
    h = 200
    d.rounded_rectangle((X0, y, X1, y + h), radius=18, fill=PALE if hl else "#ffffff", outline=NAVY if hl else LINE, width=4 if hl else 2)
    d.text((X0 + 34, y + 30), t, font=F(34, True), fill=NAVY if hl else INK)
    d.text((X0 + 34, y + 88), a, font=F(32, True), fill=INK)
    d.text((X0 + 34, y + 140), b, font=F(27), fill=MUT)
    y += h + 26
y += 10
d.text((X0, y), "내가 타는 열차", font=F(30, True), fill=NAVY); y += 56
d.rounded_rectangle((X0, y, X1, y + 170), radius=18, fill="#ffffff", outline=LINE, width=2)
d.text((X0 + 34, y + 28), "2027년 1월 15일(금) 06:45 다카야마 → 나고야 09:12", font=F(30, True), fill=INK)
d.text((X0 + 34, y + 88), "지브리파크 손목밴드 교환은 당일 12시까지 · 추위 많이 타는 사람과 둘이", font=F(27), fill=MUT)
y += 170 + 36
d.text((X0 + 8, y), "직접 만든 그림 · 일본 기상청 高山 관측소 일별·시간별값으로 계산", font=F(22), fill=MUT)
d.text((X0 + 8, H - 62), "걷고읽고떠나고", font=F(22), fill="#b0b0b0")
im.save(os.path.join(HERE, "card_conclusion.png"))
print("t6", t6, "d6", d6, "mt", mt, "ms", ms, "lt", lt, "lg", lg)
