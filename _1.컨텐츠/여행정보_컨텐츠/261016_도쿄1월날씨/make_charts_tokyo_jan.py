# -*- coding: utf-8 -*-
"""도쿄 1월 그래프 3장 + 결론 카드 — 오키나와·다카야마 편과 같은 색·서체(맑은 고딕).
① chart_jan_11years.png  1월 11년 겹침(2025 굵게, 출장 주간 음영)
② chart_rain_frost.png   해마다 비 온 날(1mm↑) vs 영하 아침(최저 0도 미만)
③ chart_trip_hourly.png  2025-01-06~12 시간별 기온·비 + 사진 찍은 시각
④ card_conclusion.png    썸네일 바로 아래 결론 카드
자료: base data\\tokyo_jan_daily.json · tokyo_trip_hourly_2025-01.json · tokyo_jan_stats.json (derive_tokyo_jan.py, 사사오입)
"""
import json, os, sys, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); BD = os.path.join(HERE, 'base data')
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
BG, INK, MUT, HOT, COLD, MY = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#e07a5f"
D = json.load(open(os.path.join(BD, 'tokyo_jan_daily.json'), encoding='utf-8'))
H = json.load(open(os.path.join(BD, 'tokyo_trip_hourly_2025-01.json'), encoding='utf-8'))
S = json.load(open(os.path.join(BD, 'tokyo_jan_stats.json'), encoding='utf-8'))
P, SM = S['per_year'], S['summary']
SRC = "일본 기상청 도쿄 관측소(지요다구 기타노마루 공원)"

# ① 11년 겹침
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); ax.set_facecolor(BG)
ax.axvspan(5.6, 12.4, color=MY, alpha=.10)
ax.text(9, 19.3, "내가 있던 1월 6~12일", ha="center", fontsize=12, color=MY, fontweight="bold")
for y, rs in D.items():
    if y == '2025':
        continue
    x = [r['day'] for r in rs]
    ax.plot(x, [r['hi'] for r in rs], color="#c8c8c8", lw=1.1)
    ax.plot(x, [r['lo'] for r in rs], color="#c8c8c8", lw=1.1, ls="--")
rs = D['2025']; x = [r['day'] for r in rs]
ax.plot(x, [r['hi'] for r in rs], color=MY, lw=3, label="2025 최고 (출장 간 해)")
ax.plot(x, [r['lo'] for r in rs], color=MY, lw=3, ls="--", label="2025 최저")
ax.plot([], [], color="#c8c8c8", lw=1.5, label="2016~2026 다른 해 (회색)")
ax.axhline(0, color=COLD, lw=1.2, alpha=.7); ax.text(31.4, 0, "0도", color=COLD, va="center", fontsize=12)
ax.axhline(9.8, color=HOT, lw=1, alpha=.5, ls=":"); ax.text(31.4, 9.8, "평년 최고\n9.8도", color=HOT, va="center", fontsize=10)
ax.annotate("2018년 1월 25일\n-4.0도", xy=(25, -4.0), xytext=(19.5, -5.6), fontsize=11, color=COLD, arrowprops=dict(arrowstyle="->", color=COLD))
for xx in (10.5, 20.5): ax.axvline(xx, color="#dddddd", lw=1)
for xx, t in ((5.5, "상순"), (15.5, "중순"), (26, "하순")): ax.text(xx, 21.2, t, ha="center", fontsize=14, color=MUT, fontweight="bold")
ax.set_xlim(1, 31); ax.set_ylim(-6.5, 22.5); ax.set_xticks([1, 5, 10, 15, 20, 25, 31])
ax.set_xticklabels([f"1/{i}" for i in [1, 5, 10, 15, 20, 25, 31]], fontsize=12)
ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
ax.set_ylabel("기온 (℃)", color=MUT, fontsize=12)
ax.set_title("도쿄 1월 11년치(2016~2026) — 실선 최고기온, 점선 최저기온", fontsize=18, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=3, frameon=False, fontsize=11)
fig.text(0.01, 0.01, SRC + " 일별값 · 평년은 1991~2020년 · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(HERE, "chart_jan_11years.png"), facecolor=BG); plt.close(fig)

# ② 비 온 날 vs 영하 아침
ys = SM['years']
fig, ax = plt.subplots(figsize=(12, 6.6), dpi=110, facecolor=BG); ax.set_facecolor(BG)
xs = range(len(ys)); w = 0.38
r = [P[y]['rain_days'] for y in ys]; f = [P[y]['frost_days'] for y in ys]
ax.bar([i - w / 2 for i in xs], r, w, color="#7fa7c9", label="비 온 날 (하루 1mm 이상)")
ax.bar([i + w / 2 for i in xs], f, w, color=COLD, label="영하 아침 (최저 0도 미만)")
for i in xs:
    ax.text(i - w / 2, r[i] + 0.2, str(r[i]), ha="center", fontsize=11, color="#4f7aa0")
    ax.text(i + w / 2, f[i] + 0.2, str(f[i]), ha="center", fontsize=11, color=COLD, fontweight="bold")
ax.set_xticks(list(xs)); ax.set_xticklabels(ys, fontsize=12)
ax.set_ylim(0, 15); ax.set_yticks([])
ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
ax.set_title(f"1월 한 달, 비 온 날과 영하 아침 — 11년 합계 {SM['total_rain_days']}일 vs {SM['total_frost_days']}일",
             fontsize=18, color=INK, loc="left", pad=14, fontweight="bold")
ax.legend(loc="upper right", ncol=2, frameon=False, fontsize=12)
fig.text(0.01, 0.01, SRC + " 일별값 2016~2026년 1월 · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_rain_frost.png"), facecolor=BG); plt.close(fig)

# ③ 출장 주간 시간별 (JMA 「N時」 기온 = N시 정각 값, 비 = 앞 1시간 합)
T, R, X, ticks = [], [], [], []
base = dt.datetime(2025, 1, 6, 0)
for day in sorted(H):
    for k in range(1, 25):
        h = H[day]['hours'][str(k)]
        t = dt.datetime.fromisoformat(day) + dt.timedelta(hours=k)
        X.append((t - base).total_seconds() / 3600); T.append(h['temp']); R.append(h['rain'] or 0)
shots = [("2025-01-07 22:58", "7일 밤\n편의점 골목", 0, 3.2), ("2025-01-10 14:31", "10일 오후\n코트", -10, 4.0),
         ("2025-01-10 18:57", "10일 저녁\n고가 아래 길", 13, 4.6), ("2025-01-11 13:25", "11일 낮\n에비스", 0, 3.2),
         ("2025-01-12 06:26", "12일 새벽\n승강장", 0, 3.2)]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 7.6), dpi=110, facecolor=BG, sharex=True, gridspec_kw={"height_ratios": [3, 1.2]})
for a in (a1, a2): a.set_facecolor(BG); [s.set_visible(False) for s in a.spines.values()]; a.tick_params(colors=MUT)
a1.plot(X, T, color=MY, lw=2.4)
a1.axhline(0, color=COLD, lw=1, alpha=.6); a1.text(169.5, 0, "0도", color=COLD, va="center", fontsize=11)
for s, lab, dx, dy in shots:
    t = dt.datetime.strptime(s, "%Y-%m-%d %H:%M"); xx = (t - base).total_seconds() / 3600
    # 그 시각의 기온은 앞뒤 정각 값 사이 — 점은 앞 정각 값에 찍는다
    i = max(j for j, v in enumerate(X) if v <= xx); a1.plot(xx, T[i], "o", color=COLD, ms=8)
    a1.annotate(lab, xy=(xx, T[i]), xytext=(xx + dx, T[i] + dy), ha="center", fontsize=10, color=COLD, arrowprops=dict(arrowstyle="-", color=COLD, lw=.8))
a1.annotate("10일 아침 7시\n1.2도", xy=(4 * 24 + 7, 1.2), xytext=(4 * 24 + 7 - 14, -2.6), fontsize=10, color=COLD, arrowprops=dict(arrowstyle="->", color=COLD))
a1.set_ylim(-4, 18); a1.set_ylabel("기온 (℃)", color=MUT, fontsize=11)
a1.set_title("2025년 1월 6~12일 도쿄, 한 시간마다 기온과 비 — 점은 내가 사진 찍은 시각", fontsize=16, color=INK, loc="left", fontweight="bold")
a2.bar([v - 1 for v in X], R, width=0.9, color="#7fa7c9", align="edge")  # 「N時」 비 = (N-1)시~N시
a2.text(30, 6.5, "6일 오후 3시~밤 11시 사이에 25.0mm", fontsize=10, color="#4f7aa0")
a2.set_ylim(0, 9); a2.set_ylabel("비 (mm)", color=MUT, fontsize=11)
a2.set_xticks([d * 24 + 12 for d in range(7)]); a2.set_xticklabels([f"1/{6 + d}" for d in range(7)], fontsize=12)
for d in range(1, 7):
    for a in (a1, a2): a.axvline(d * 24, color="#e2e2e2", lw=1)
a2.set_xlim(0, 168)
fig.text(0.01, 0.01, SRC + " 시간별값 · 관측소 값이라 내가 있던 자리와 똑같지는 않다 · 직접 만든 그래프", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_trip_hourly.png"), facecolor=BG); plt.close(fig)

# ④ 결론 카드
W, Hh = 1400, 1480
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", s)
im = Image.new("RGB", (W, Hh), BG); d = ImageDraw.Draw(im); X0, X1 = 70, W - 70
PINK, NAVY, LINE = "#fcecec", "#1e3264", "#e2e2e2"
d.text((X0, 58), "1월 도쿄,", font=F(58, True), fill=INK)
d.text((X0, 134), "우산보다 목도리", font=F(58, True), fill=HOT)
d.text((X0, 222), "일본 기상청 도쿄 관측소 2016~2026년 1월 11년치 일별값 · 평년은 1991~2020년", font=F(22), fill=MUT)
d.text((X0 + 10, 290), "무엇", font=F(24, True), fill=NAVY); d.text((330, 290), "11년치에서 본 것", font=F(24, True), fill=NAVY); d.text((1010, 290), "챙길 것", font=F(24, True), fill=NAVY)
rows = [
    ("비", "하루 1mm↑", [f"11년 합계 {SM['total_rain_days']}일", "한 달에 하루뿐인 해가 셋"], ["작은 접는 우산", "하나"], False),
    ("아침", "최저 0도 미만", [f"11년 합계 {SM['total_frost_days']}일", "11년 중 8년은 비 온 날보다 많아"], ["목도리", "+ 코트"], True),
    ("눈", "1cm 이상 쌓임", ["11년 중 4번", "가장 많이 23cm (2018년)"], ["미끄럼 덜한", "신발"], False),
]
y = 336
for name, sub, mid, pack, hl in rows:
    h = 190
    d.rounded_rectangle((X0, y, X1, y + h), radius=18, fill=PINK if hl else "#ffffff", outline=HOT if hl else LINE, width=4 if hl else 2)
    d.text((X0 + 34, y + 44), name, font=F(54, True), fill=HOT if hl else INK)
    d.text((X0 + 38, y + 118), sub, font=F(24), fill=MUT)
    for i, t in enumerate(mid):
        d.text((330, y + 46 + i * 54), t, font=F(32, True if (hl or i == 0) else False), fill=INK if (hl or i == 0) else MUT)
    for i, t in enumerate(pack):
        d.text((1010, y + 46 + i * 54), t, font=F(34, True), fill=HOT if hl else NAVY)
    y += h + 26
y += 14
d.text((X0, y), "내가 있던 2025년 1월 6~12일", font=F(30, True), fill=NAVY); y += 58
d.rounded_rectangle((X0, y, X1, y + 230), radius=18, fill="#ffffff", outline=LINE, width=2)
d.text((X0 + 34, y + 30), "비 온 날", font=F(30, True), fill=INK)
d.text((X0 + 34, y + 80), "첫날 저녁 하루뿐", font=F(40, True), fill=NAVY)
d.text((X0 + 34, y + 140), "6일 오후~밤 25.0mm, 남은 엿새는 0mm", font=F(24), fill=MUT)
d.line((700, y + 30, 700, y + 200), fill=LINE, width=2)
d.text((730, y + 30), "가장 추운 아침", font=F(30, True), fill=INK)
d.text((730, y + 80), "10일 최저 0.1도", font=F(40, True), fill=HOT)
d.text((730, y + 140), "코트에 목도리까지 두르고 다녔어", font=F(24), fill=MUT)
y += 230 + 40
d.text((X0 + 8, y), "직접 만든 그림 · 일본 기상청 도쿄 관측소 일별·시간별값으로 계산", font=F(22), fill=MUT)
d.text((X0 + 8, Hh - 62), "걷고읽고떠나고", font=F(22), fill="#b0b0b0")
im.save(os.path.join(HERE, "card_conclusion.png")); print('done', y)
