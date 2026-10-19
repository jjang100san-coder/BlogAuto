# -*- coding: utf-8 -*-
"""시라카와고 1월 그래프 추가 3장 (사용자 10/12: 「통계 그래프 더」).
④ chart_mid_temp.png      해마다 1월 중순(11~20일) 최고·최저 평균 막대
⑤ chart_snow_days.png     해마다 1월 10cm↑ 내린 날 수 + 하루 가장 많이 내린 눈
⑥ chart_dec31_jan14.png   12월 31일 → 1월 14일 쌓인 눈 기울기 그래프
자료: base data\\chubu_daily.json (기상청 白川 1306 일별, 2026-10-12 수집)
"""
import json, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
BG, INK, MUT, RED, NAVY, SNOW = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#8fb3d9"
D = json.load(open(os.path.join(HERE, 'base data', 'chubu_daily.json'), encoding='utf-8'))['시라카와']
YEARS = list(range(2016, 2027)); X = range(len(YEARS))
jan = {y: D['%d-01' % y] for y in YEARS}
v = lambda x: x if x is not None else 0.0
FOOT = "일본 기상청 白川 관측소(시라카와무라 하토가야) 일별값 · 직접 만든 그래프 · 걷고읽고떠나고"
def frame(ax):
    ax.set_facecolor(BG); ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]

# ④ 중순 기온
hi = [sum(r['hi'] for r in jan[y][10:20]) / 10 for y in YEARS]
lo = [sum(r['lo'] for r in jan[y][10:20]) / 10 for y in YEARS]
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); frame(ax)
ax.bar(X, [h - l for h, l in zip(hi, lo)], 0.5, bottom=lo, color=SNOW, alpha=.85)
for i, (h, l) in enumerate(zip(hi, lo)):
    ax.text(i, h + 0.25, f"{h:.1f}", ha="center", fontsize=12, color=RED, fontweight="bold")
    ax.text(i, l - 0.75, f"{l:.1f}", ha="center", fontsize=12, color=NAVY, fontweight="bold")
ax.axhline(0, color=INK, lw=1); ax.text(10.45, 0.15, "0도", fontsize=11, color=INK)
ax.set_xticks(list(X)); ax.set_xticklabels([str(y) for y in YEARS], fontsize=12); ax.set_ylim(-7.5, 7.5)
ax.set_ylabel("℃", color=MUT)
ax.set_title("1월 중순(11~20일) 시라카와고 — 막대 위 낮 최고 평균, 아래 아침 최저 평균", fontsize=17, color=INK, loc="left", pad=16, fontweight="bold")
fig.text(0.01, 0.01, FOOT, fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_mid_temp.png"), facecolor=BG); plt.close(fig)

# ⑤ 10cm↑ 날 + 하루 최대
days = [sum(1 for r in jan[y] if v(r['snow']) >= 10) for y in YEARS]
mx = [max(v(r['snow']) for r in jan[y]) for y in YEARS]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8), dpi=110, facecolor=BG, sharex=True, gridspec_kw={"height_ratios": [1, 1]})
frame(a1); frame(a2)
a1.bar(X, days, 0.55, color=NAVY)
for i, d in enumerate(days): a1.text(i, d + 0.3, f"{d}일", ha="center", fontsize=12, color=INK, fontweight="bold")
a1.set_ylim(0, 17); a1.set_title("1월에 하루 10cm 넘게 눈이 내린 날 (일)", fontsize=16, color=INK, loc="left", fontweight="bold")
a2.bar(X, mx, 0.55, color=SNOW)
for i, m in enumerate(mx): a2.text(i, m + 1.5, f"{m:.0f}", ha="center", fontsize=12, color=INK, fontweight="bold")
a2.set_ylim(0, 82); a2.set_title("1월 하루에 가장 많이 내린 눈 (cm)", fontsize=16, color=INK, loc="left", fontweight="bold")
a2.set_xticks(list(X)); a2.set_xticklabels([str(y) for y in YEARS], fontsize=12)
fig.text(0.01, 0.01, FOOT, fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_snow_days.png"), facecolor=BG); plt.close(fig)

# ⑥ 12/31 → 1/14
dec31 = [v(D['%d-12' % (y - 1)][30]['snow_depth']) for y in YEARS]
j14 = [v(jan[y][13]['snow_depth']) for y in YEARS]
fig, ax = plt.subplots(figsize=(10, 9), dpi=110, facecolor=BG); frame(ax)
for y, a, b in zip(YEARS, dec31, j14):
    hl = y in (2020, 2026)
    c = RED if y == 2026 else (NAVY if y == 2020 else "#bfc7d3")
    ax.plot([0, 1], [a, b], color=c, lw=3 if hl else 1.4, marker="o", ms=7 if hl else 5)
    ax.text(1.04, b + {2016: 3.5, 2023: -3.5}.get(y, 0), f"{y}  {b:.0f}", va="center", fontsize=11, color=c if hl else MUT, fontweight="bold" if hl else None)
    if hl: ax.text(-0.04, a, f"{a:.0f}  {y - 1}.12.31", va="center", ha="right", fontsize=11, color=c, fontweight="bold")
ax.set_xlim(-0.45, 1.4); ax.set_ylim(-8, 200); ax.set_xticks([0, 1]); ax.set_xticklabels(["전해 12월 31일", "1월 14일"], fontsize=14)
ax.set_ylabel("쌓인 눈 (cm)", color=MUT)
ax.set_title("12월 31일과 1월 14일, 쌓인 눈 11번", fontsize=18, color=INK, loc="left", pad=16, fontweight="bold")
ax.text(-0.43, 192, "12월 말에 거의 없던 두 해: 2020년은 3cm, 2026년은 63cm", fontsize=12, color=INK)
fig.text(0.01, 0.01, FOOT, fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_dec31_jan14.png"), facecolor=BG); plt.close(fig)
print("ok", days, mx, dec31)
