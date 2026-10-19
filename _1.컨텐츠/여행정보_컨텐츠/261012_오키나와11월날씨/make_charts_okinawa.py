# -*- coding: utf-8 -*-
"""오키나와(나하) 11월 10년치 그래프 3장 — 도쿄 편 make_charts.py 와 같은 꼴.
① chart_nov_10years.png  10년 겹침(2016 굵게)  ② chart_decade.png  순별 10년 폭 + 2016 점
③ chart_trip_hourly.png  2016-11-26~28 시간별 관측 vs 1일 전 예보
자료: base data\\나하_일별_2016-2025.csv · base data\\예보대조\\trip2016_forecast_vs_obs.json
"""
import csv, json, sys, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); BD = os.path.join(HERE, 'base data')
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
BG, INK, MUT, HOT, COLD, MY = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#e07a5f"
rows = list(csv.DictReader(open(os.path.join(BD, '나하_일별_2016-2025.csv'), encoding='utf-8-sig')))
f = lambda x: float(x) if x not in ('', None) else None
nov = {y: [r for r in rows if r['날짜'].startswith('%d-11' % y)] for y in range(2016, 2026)}

# ① 10년 겹침
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); ax.set_facecolor(BG)
for y, rs in nov.items():
    x = [int(r['날짜'][8:]) for r in rs]
    if y == 2016:
        continue
    ax.plot(x, [f(r['최고(℃)']) for r in rs], color="#c8c8c8", lw=1.1)
    ax.plot(x, [f(r['최저(℃)']) for r in rs], color="#c8c8c8", lw=1.1, ls="--")
rs = nov[2016]; x = [int(r['날짜'][8:]) for r in rs]
ax.plot(x, [f(r['최고(℃)']) for r in rs], color=MY, lw=3, label="2016 최고 (내가 간 해)")
ax.plot(x, [f(r['최저(℃)']) for r in rs], color=MY, lw=3, ls="--", label="2016 최저")
ax.plot([], [], color="#c8c8c8", lw=1.5, label="2017~2025 (회색)")
ax.axhline(25, color=HOT, lw=1, alpha=.6); ax.text(30.4, 25, "25도", color=HOT, va="center", fontsize=12)
ax.axhline(20, color=COLD, lw=1, alpha=.6); ax.text(30.4, 20, "20도", color=COLD, va="center", fontsize=12)
for xx in (10.5, 20.5): ax.axvline(xx, color="#dddddd", lw=1)
for xx, t in ((5.5, "상순"), (15.5, "중순"), (25.5, "하순")): ax.text(xx, 32, t, ha="center", fontsize=14, color=MUT, fontweight="bold")
ax.annotate("11/26 슈리성\n최고 25.8도", xy=(26, 25.8), xytext=(21.2, 29.3), fontsize=12, color=MY, arrowprops=dict(arrowstyle="->", color=MY))
ax.annotate("11/27 비 34.5mm", xy=(27, 19.6), xytext=(22.2, 15.2), fontsize=12, color=MY, arrowprops=dict(arrowstyle="->", color=MY))
ax.set_xlim(1, 30); ax.set_ylim(14, 33); ax.set_xticks([1, 5, 10, 15, 20, 25, 30])
ax.set_xticklabels([f"11/{i}" for i in [1, 5, 10, 15, 20, 25, 30]], fontsize=12)
ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
ax.set_ylabel("기온 (℃)", color=MUT, fontsize=12)
ax.set_title("오키나와(나하) 11월 10년치 — 실선 최고기온, 점선 최저기온", fontsize=18, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(loc="lower left", ncol=3, frameon=False, fontsize=11)
fig.text(0.01, 0.01, "일본 기상청 나하 관측소 일별값 2016~2025 · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_nov_10years.png"), facecolor=BG); plt.close(fig)

# ② 순별 10년 폭(가장 낮은 해~가장 높은 해) + 2016 점
segs = [("상순", 1, 10), ("중순", 11, 20), ("하순", 21, 30)]
def mean(y, a, b, k):
    L = [f(r[k]) for r in nov[y] if a <= int(r['날짜'][8:]) <= b]; return sum(L) / len(L)
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); ax.set_facecolor(BG)
for i, (nm, a, b) in enumerate(segs):
    for k, col, off, lab in (("최고(℃)", HOT, -0.13, "최고 평균"), ("최저(℃)", COLD, 0.13, "최저 평균")):
        v = [mean(y, a, b, k) for y in nov]; lo, hi = min(v), max(v)
        ax.bar(i + off, hi - lo, 0.22, bottom=lo, color=col, alpha=.28, label=(lab + " 10년 폭") if i == 0 else None)
        ax.text(i + off, hi + 0.15, f"{hi:.1f}", ha="center", fontsize=10, color=col)
        ax.text(i + off, lo - 0.55, f"{lo:.1f}", ha="center", fontsize=10, color=col)
        m16 = mean(2016, a, b, k)
        ax.plot(i + off, m16, "o", color=MY, ms=9, label="2016" if (i == 0 and k == "최고(℃)") else None)
ax.axhline(25, color=HOT, lw=1, alpha=.5); ax.text(2.42, 25.1, "25도", color=HOT, fontsize=11)
ax.axhline(20, color=COLD, lw=1, alpha=.5); ax.text(2.42, 20.1, "20도", color=COLD, fontsize=11)
ax.set_xticks(range(3)); ax.set_xticklabels([s[0] for s in segs], fontsize=14); ax.set_ylim(17, 29.5)
ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
ax.set_title("순별 평균기온 10년 폭 — 막대 위 끝은 가장 높았던 해, 아래 끝은 가장 낮았던 해", fontsize=16, color=INK, loc="left", fontweight="bold")
ax.legend(ncol=3, frameon=False, loc="upper right", fontsize=11)
fig.text(0.01, 0.01, "일본 기상청 나하 관측소 일별값 2016~2025 · 상순 1~10일 · 중순 11~20일 · 하순 21~30일 · 직접 만든 그래프", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_decade.png"), facecolor=BG); plt.close(fig)

# ③ 내 사흘 시간별: 관측 vs 1일 전 예보
J = json.load(open(os.path.join(BD, '예보대조', 'trip2016_forecast_vs_obs.json'), encoding='utf-8'))
H = [r for r in J['hourly'] if r['time'] >= '2016-11-26T01' and r['obs']]
xs = list(range(len(H))); lab = [r['time'][5:13].replace('T', ' ') + '시' for r in H]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8), dpi=110, facecolor=BG, sharex=True, gridspec_kw={"height_ratios": [3, 1.4]})
for a in (a1, a2): a.set_facecolor(BG); [s.set_visible(False) for s in a.spines.values()]; a.tick_params(colors=MUT)
a1.plot(xs, [r['obs']['temp'] for r in H], color=MY, lw=2.6, label="실제 (기상청 나하)")
a1.plot(xs, [r['fc1']['temp'] for r in H], color=MUT, lw=1.6, ls="--", label="하루 전 예보")
i8 = next(i for i, r in enumerate(H) if r['time'] == '2016-11-27T08:00')
a1.annotate("27일 7→8시\n24.6 → 21.1도", xy=(i8, 21.1), xytext=(i8 + 6, 19.0), fontsize=12, color=MY, arrowprops=dict(arrowstyle="->", color=MY))
i16 = next(i for i, r in enumerate(H) if r['time'] == '2016-11-26T16:00')
a1.annotate("26일 16시 슈리성\n25.0도", xy=(i16, 25.0), xytext=(i16 + 3, 26.3), fontsize=12, color=MY, arrowprops=dict(arrowstyle="->", color=MY))
a1.set_ylim(18, 27.5); a1.set_ylabel("기온 (℃)", color=MUT); a1.legend(frameon=False, loc="lower left", fontsize=11)
a1.set_title("내가 있던 2016년 11월 26~28일, 한 시간마다", fontsize=17, color=INK, loc="left", fontweight="bold")
a2.bar(xs, [r['obs']['wind'] for r in H], color=COLD, alpha=.55, label="실제 풍속")
a2.plot(xs, [r['fc1']['wind'] for r in H], color=MUT, lw=1.4, ls="--", label="하루 전 예보 풍속")
a2.set_ylabel("m/s", color=MUT); a2.legend(frameon=False, loc="upper left", fontsize=10)
for d in ('2016-11-27T01:00', '2016-11-28T01:00'):
    j = next(i for i, r in enumerate(H) if r['time'] == d)
    for a in (a1, a2): a.axvline(j - 0.5, color="#dddddd", lw=1)
tk = [i for i, r in enumerate(H) if r['time'][11:13] in ('06', '12', '18')]
a2.set_xticks(tk); a2.set_xticklabels([lab[i] for i in tk], fontsize=10, rotation=0)
fig.text(0.01, 0.01, "실제: 일본 기상청 나하 관측소 시간별값 · 예보: 일본 기상청 예보 모델 하루 전 값(Open-Meteo 보관) · 직접 만든 그래프", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_trip_hourly.png"), facecolor=BG); plt.close(fig)
print("ok")
