# -*- coding: utf-8 -*-
"""도쿄 10월 5년치 그래프 2장 (기상청 北の丸公園 일별값)."""
import json, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
sys.stdout.reconfigure(encoding='utf-8')
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
d = json.load(open("jma_tokyo_oct_5y.json", encoding="utf-8"))
YC = {"2021": "#9aa8c4", "2022": "#7fb7a8", "2023": "#e07a5f", "2024": "#c9a227", "2025": "#5b6c9a"}
BG, INK, MUT = "#faf9f5", "#1a1a1a", "#7a7a7a"

# ① 5년 겹침
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); ax.set_facecolor(BG)
for y, rows in d.items():
    x = [r["day"] for r in rows]
    lw = 3.0 if y == "2023" else 1.8
    ax.plot(x, [r["hi"] for r in rows], color=YC[y], lw=lw, label=f"{y} 최고")
    ax.plot(x, [r["lo"] for r in rows], color=YC[y], lw=lw, ls="--", alpha=0.85)
ax.axhline(25, color="#b9333f", lw=1, alpha=.6); ax.text(31.4, 25, "25도", color="#b9333f", va="center", fontsize=12)
ax.axhline(15, color="#1e3264", lw=1, alpha=.6); ax.text(31.4, 15, "15도", color="#1e3264", va="center", fontsize=12)
for xx in (10.5, 20.5): ax.axvline(xx, color="#cccccc", lw=1)
for xx, t in ((5.5, "초순"), (15.5, "중순"), (26, "하순")): ax.text(xx, 34, t, ha="center", fontsize=14, color=MUT, fontweight="bold")
ax.annotate("2023-10-15\n16.9도 · 비 43.5mm", xy=(15, 16.9), xytext=(16.5, 8.5), fontsize=12, color="#e07a5f",
            arrowprops=dict(arrowstyle="->", color="#e07a5f"))
ax.set_xlim(1, 31); ax.set_ylim(5, 35); ax.set_xticks([1, 5, 10, 15, 20, 25, 31])
ax.set_xticklabels([f"10/{i}" for i in [1, 5, 10, 15, 20, 25, 31]], fontsize=12)
ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
ax.set_ylabel("기온 (℃)", color=MUT, fontsize=12)
ax.set_title("도쿄 10월 5년치 — 실선 최고기온, 점선 최저기온", fontsize=18, color=INK, loc="left", pad=16, fontweight="bold")
leg = ax.legend(loc="lower left", ncol=5, frameon=False, fontsize=11)
fig.text(0.01, 0.01, "일본 기상청 도쿄 관측소(기타노마루 공원) 일별값 · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig("chart_oct_5years.png", facecolor=BG); plt.close(fig)

# ② 순별 막대
segs = [("초순", 0, 10), ("중순", 10, 20), ("하순", 20, 31)]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8), dpi=110, facecolor=BG, gridspec_kw={"height_ratios": [3, 1.4]})
for a in (a1, a2): a.set_facecolor(BG); [s.set_visible(False) for s in a.spines.values()]; a.tick_params(colors=MUT)
w = 0.15; ys = list(d)
for i, y in enumerate(ys):
    hi = [sum(r["hi"] for r in d[y][s:e]) / (e - s) for _, s, e in segs]
    rn = [sum(1 for r in d[y][s:e] if (r["rain"] or 0) >= 1) for _, s, e in segs]
    xs = [k + (i - 2) * w for k in range(3)]
    b = a1.bar(xs, hi, w * 0.92, color=YC[y], label=y)
    for x0, v in zip(xs, hi): a1.text(x0, v + 0.3, f"{v:.1f}", ha="center", fontsize=9, color=INK)
    a2.bar(xs, rn, w * 0.92, color=YC[y])
    for x0, v in zip(xs, rn): a2.text(x0, v + 0.15, str(v), ha="center", fontsize=9, color=INK)
a1.axhline(25, color="#b9333f", lw=1, alpha=.6); a1.text(2.45, 25.2, "25도", color="#b9333f", fontsize=11)
a1.set_ylim(15, 29); a1.set_xticks(range(3)); a1.set_xticklabels([s[0] for s in segs], fontsize=14)
a1.set_title("순별 최고기온 평균 (℃) — 초순은 5년 모두 23도 위, 중순은 해마다 갈림", fontsize=16, color=INK, loc="left", fontweight="bold")
a1.legend(ncol=5, frameon=False, loc="upper right", fontsize=11)
a2.set_ylim(0, 7); a2.set_xticks(range(3)); a2.set_xticklabels([s[0] for s in segs], fontsize=13)
a2.set_title("비 1mm 이상 온 날 (일)", fontsize=13, color=MUT, loc="left")
fig.text(0.01, 0.01, "일본 기상청 도쿄 관측소 일별값 · 초순 1~10일 · 중순 11~20일 · 하순 21~31일 · 직접 만든 그래프", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig("chart_decade.png", facecolor=BG); plt.close(fig)
print("ok")
