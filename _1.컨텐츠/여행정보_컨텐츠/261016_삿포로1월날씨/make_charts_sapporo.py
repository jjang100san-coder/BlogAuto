# -*- coding: utf-8 -*-
"""삿포로 1월 그래프 4장 + 결론 카드 (시라카와고·다카야마 편과 같은 꼴).
1 chart_cold_days.png   해마다 1월 최저기온 영하 10도 이하 날 수 + 그해 가장 추운 날
2 chart_jan_band.png    1월 1~31일 11년 폭(최고·최저)과 2024년, 내가 있던 28~30일
3 chart_snow_depth.png  1월 쌓인 눈 11년, 2024년 강조
4 chart_trip_hourly.png 2024-01-28 06시 ~ 01-30 15시 한 시간마다 기온 + 사진 찍은 시각, 1/29 비에이·후라노
5 card_conclusion.png
자료: base data 의 sapporo_daily.json, sapporo_jan_derived.json, trip_hourly.json (일본 기상청, 2026-10-16 수집). 반올림은 사사오입.
마이너스는 「-」(맑은 고딕 굵게에 「−」 없음).
"""
import json, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); BD = os.path.join(HERE, 'base data')
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
BG, INK, MUT, RED, NAVY, SNOW, GREEN, GREY = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#8fb3d9", "#5b8c6e", "#c9c9c9"
PURPLE = "#9b6bb3"
D = json.load(open(os.path.join(BD, 'sapporo_daily.json'), encoding='utf-8'))['삿포로']
S = json.load(open(os.path.join(BD, 'sapporo_jan_derived.json'), encoding='utf-8'))
H = json.load(open(os.path.join(BD, 'trip_hourly.json'), encoding='utf-8'))
YEARS = list(range(2016, 2027)); X = list(range(len(YEARS)))
DAYS = list(range(1, 32))
DTICKS = [1, 5, 10, 15, 20, 25, 31]


def frame(ax):
    ax.set_facecolor(BG); ax.tick_params(colors=MUT)
    for s in ax.spines.values():
        s.set_visible(False)


def fmt(t):
    return "%.1f" % t


def save(fig, name, foot):
    fig.text(0.01, 0.01, foot, fontsize=10, color=MUT)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, name), facecolor=BG); plt.close(fig)


# 1 영하 10도 이하 날
cnt = [S['years'][str(y)]['lo_le_m10'] for y in YEARS]; cold = [S['years'][str(y)]['coldest'] for y in YEARS]
fig, ax = plt.subplots(figsize=(12, 7.4), dpi=110, facecolor=BG); frame(ax)
ax.bar(X, cnt, 0.55, color=[NAVY if c else GREY for c in cnt])
for i, c in enumerate(cnt):
    ax.text(i, c + 0.15, ("없음" if c == 0 else "%d일" % c), ha="center", fontsize=13, color=INK if c else MUT, fontweight="bold")
    ax.text(i, -0.7, "%s도\n(1/%d)" % (fmt(cold[i][1]), cold[i][0]), ha="center", va="top", fontsize=10.5,
            color=RED if cold[i][1] <= -13 else MUT)
ax.set_xticks(X); ax.set_xticklabels([str(y) for y in YEARS], fontsize=12); ax.tick_params(axis='x', pad=4, length=0)
ax.set_ylim(-1.9, 9.6); ax.set_yticks([0, 2, 4, 6, 8]); ax.set_yticklabels(["0", "2", "4", "6", "8일"]); ax.axhline(0, color=INK, lw=1)
ax.set_title("삿포로 1월, 최저기온이 영하 10도까지 내려간 날 (11년 341일 중 %d일)" % S['pooled']['lo_le_m10'],
             fontsize=16, color=INK, loc="left", pad=14, fontweight="bold")
ax.text(-0.5, 8.9, "막대 아래 숫자 = 그해 1월 가장 추웠던 날의 최저기온", fontsize=11, color=MUT)
save(fig, "chart_cold_days.png", "일본 기상청 札幌 관측소 일별값 2016~2026년 1월 · 직접 만든 그래프 · 걷고읽고떠나고")

# 2 11년 폭 + 2024
B = S['pooled']['band']; r24 = D['2024-01']
fig, ax = plt.subplots(figsize=(12, 7.4), dpi=110, facecolor=BG); frame(ax)
ax.fill_between(DAYS, [B[str(d)]['hi_min'] for d in DAYS], [B[str(d)]['hi_max'] for d in DAYS], color=RED, alpha=0.12, lw=0, label="낮 최고기온 11년 폭")
ax.fill_between(DAYS, [B[str(d)]['lo_min'] for d in DAYS], [B[str(d)]['lo_max'] for d in DAYS], color=NAVY, alpha=0.12, lw=0, label="최저기온 11년 폭")
ax.plot(DAYS, [r['hi'] for r in r24], color=RED, lw=2.4, marker="o", ms=3.5, label="2024년 낮 최고")
ax.plot(DAYS, [r['lo'] for r in r24], color=NAVY, lw=2.4, marker="o", ms=3.5, label="2024년 최저")
ax.axvspan(27.6, 30.4, color="#f2d27a", alpha=0.35, lw=0)
for d in (28, 29, 30):
    ax.text(d, r24[d - 1]['hi'] + 0.55, fmt(r24[d - 1]['hi']), ha="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(d, r24[d - 1]['lo'] - 1.2, fmt(r24[d - 1]['lo']), ha="center", fontsize=11, color=NAVY, fontweight="bold")
ax.text(29, 8.9, "내가 있던 28~30일", ha="center", fontsize=12, color=INK, fontweight="bold")
ax.axhline(0, color=INK, lw=1); ax.axhline(-10, color=MUT, lw=1, ls="--"); ax.text(1, -9.6, "영하 10도", fontsize=10, color=MUT)
ax.set_xlim(0.5, 31.5); ax.set_ylim(-14.5, 10)
ax.set_xticks(DTICKS); ax.set_xticklabels(["%d일" % t for t in DTICKS], fontsize=12); ax.set_ylabel("℃", color=MUT)
ax.set_title("삿포로 1월 날마다 기온 — 11년 폭과 2024년", fontsize=17, color=INK, loc="left", pad=14, fontweight="bold")
ax.legend(frameon=False, loc="lower left", fontsize=11, ncol=2)
save(fig, "chart_jan_band.png", "일본 기상청 札幌 관측소 일별값 2016~2026년 1월 · 색 띠 = 그날짜 11년 중 가장 낮은 값과 높은 값 사이 · 직접 만든 그래프")

# 3 쌓인 눈
fig, ax = plt.subplots(figsize=(12, 7.4), dpi=110, facecolor=BG); frame(ax)
for y in YEARS:
    v = [r['snow_depth'] for r in D['%d-01' % y]]
    if y == 2024:
        ax.plot(DAYS, v, color=NAVY, lw=3, zorder=5, label="2024년 (내가 간 해)")
    elif y == 2026:
        ax.plot(DAYS, v, color=SNOW, lw=2.4, zorder=4, label="2026년 (가장 많이 쌓인 해)")
    elif y == 2020:
        ax.plot(DAYS, v, color=GREEN, lw=2.4, zorder=4, label="2020년 (가장 적게 쌓인 해)")
    else:
        ax.plot(DAYS, v, color=GREY, lw=1.3)
ax.scatter([28, 29, 30], [r24[d - 1]['snow_depth'] for d in (28, 29, 30)], color=NAVY, zorder=6, s=36)
ax.text(28.6, r24[27]['snow_depth'] + 6, "28일 %dcm" % r24[27]['snow_depth'], fontsize=12, color=NAVY, fontweight="bold", ha="center")
mn = S['pooled']['sd_min_all']
ax.annotate("11년 중 가장 적었던 날도 %dcm\n(%d년 1월 %d일)" % (mn[2], mn[0], mn[1]), (mn[1], mn[2]), (4.5, 14),
            fontsize=11, color=GREEN, arrowprops=dict(arrowstyle="-", color=GREEN))
ax.set_xlim(0.5, 31.5); ax.set_ylim(0, 122)
ax.set_xticks(DTICKS); ax.set_xticklabels(["%d일" % t for t in DTICKS], fontsize=12); ax.set_ylabel("cm", color=MUT)
ax.set_title("삿포로 1월 쌓인 눈 11년 — 0cm인 날은 하루도 없었어", fontsize=17, color=INK, loc="left", pad=14, fontweight="bold")
ax.legend(frameon=False, loc="upper left", fontsize=11)
save(fig, "chart_snow_depth.png", "일본 기상청 札幌 관측소 일별 최심적설 2016~2026년 1월 · 회색 = 나머지 해 · 직접 만든 그래프 · 걷고읽고떠나고")

# 4 시간별
seq = []
for d in (28, 29, 30):
    for h in range(1, 25):
        r = H['札幌 2024-01-%02d' % d]['hours'].get(str(h))
        if r:
            seq.append(((d - 28) * 24 + h, r['temp']))
seq = [p for p in seq if 6 <= p[0] <= 48 + 15]
fig, ax = plt.subplots(figsize=(12, 7.4), dpi=110, facecolor=BG); frame(ax)
ax.plot([p[0] for p in seq], [p[1] for p in seq], color=RED, lw=2.6, label="삿포로(札幌) 관측소")
for nm, col, lab in (("美瑛", GREEN, "비에이(美瑛) 관측소"), ("富良野", PURPLE, "후라노(富良野) 관측소")):
    hh = H['%s 2024-01-29' % nm]['hours']
    ax.plot([24 + int(h) for h in hh], [hh[h]['temp'] for h in hh], color=col, lw=2.0, ls="--", label=lab)
shots = [(15.0, "15:00"), (16.6, "16:34"), (18.8, "18:49"), (20.7, "20:41"), (24 + 7.75, "07:45"), (24 + 13.05, "13:03\n비에이"), (24 + 16.1, "16:07\n후라노")]
for x, lab in shots:
    k = shots.index((x, lab))
    ax.axvline(x, color=MUT, lw=0.8, ls=":"); ax.text(x, 4.4 if k % 2 else 5.4, lab, ha="center", va="bottom", fontsize=10, color=INK)
ax.axhline(0, color=INK, lw=1)
for lab, x in (("1월 28일(일)", 6), ("1월 29일(월)", 24), ("1월 30일(화)", 48)):
    ax.text(x + 0.4, 6.9, lab, fontsize=12, color=INK, fontweight="bold")
for x in (24, 48):
    ax.axvline(x, color=INK, lw=0.6)
ax.set_xlim(6, 63); ax.set_ylim(-12.8, 8.2)
ticks = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
ax.set_xticks(ticks); ax.set_xticklabels(["%d시" % (t % 24) for t in ticks], fontsize=11); ax.set_ylabel("℃", color=MUT)
ax.set_title("2024년 1월 28~30일 한 시간마다 기온과 내 사진 찍은 시각", fontsize=17, color=INK, loc="left", pad=14, fontweight="bold")
ax.legend(frameon=False, loc="lower right", fontsize=11)
save(fig, "chart_trip_hourly.png", "일본 기상청 삿포로·비에이·후라노 관측소 시간별값 · 점선 세로줄 = 내 사진 촬영 시각 · 직접 만든 그래프 · 걷고읽고떠나고")

# 5 카드
P = S['pooled']; ys = S['years']
W, Hh = 1400, 1400; LINE, PALE = "#e2e2e2", "#eef2f8"
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", s)
im = Image.new("RGB", (W, Hh), BG); d = ImageDraw.Draw(im); X0, X1 = 70, W - 70
d.text((X0, 58), "1월 삿포로, 영하 10도까지 떨어진 날은", font=F(54, True), fill=INK)
d.text((X0, 132), "11년 %d일 중 %d일이었어" % (P['n'], P['lo_le_m10']), font=F(54, True), fill=NAVY)
d.text((X0, 220), "일본 기상청 札幌 관측소 2016~2026년 1월 11년치 · 일별값", font=F(22), fill=MUT)
hl = [ys[str(y)]['hi_lt0'] for y in YEARS]
sdmax = max(ys[str(y)]['sd_max'][1] for y in YEARS)
rows = [("최저기온 영하 10도 이하", "%d일 중 %d일 · 하루도 없던 해 %d번" % (P['n'], P['lo_le_m10'], len(P['years_no_m10'])),
         "11년 중 가장 추운 날은 %d년 1월 %d일 %s도" % (P['coldest'][0], P['coldest'][1], fmt(P['coldest'][2])), True),
        ("낮 최고기온 0도 이상", "%d일 중 %d일" % (P['n'], P['hi_ge0']), "낮에도 영하였던 날은 적은 해 %d일, 많은 해 %d일" % (min(hl), max(hl)), False),
        ("쌓인 눈", "%d일 내내 쌓여 있었어" % P['n'],
         "가장 적었던 날 %dcm(%d년) · 가장 많았던 날 %dcm(2026년)" % (P['sd_min_all'][2], P['sd_min_all'][0], sdmax), False)]
y = 296
for t, a, b, h in rows:
    hgt = 200
    d.rounded_rectangle((X0, y, X1, y + hgt), radius=18, fill=PALE if h else "#ffffff", outline=NAVY if h else LINE, width=4 if h else 2)
    d.text((X0 + 34, y + 30), t, font=F(34, True), fill=NAVY if h else INK)
    d.text((X0 + 34, y + 88), a, font=F(32, True), fill=INK)
    d.text((X0 + 34, y + 140), b, font=F(27), fill=MUT)
    y += hgt + 26
y += 10
d.text((X0, y), "내가 간 날", font=F(30, True), fill=NAVY); y += 56
t28 = S['trip']['28']
d.rounded_rectangle((X0, y, X1, y + 170), radius=18, fill="#ffffff", outline=LINE, width=2)
d.text((X0 + 34, y + 28), "2024년 1월 28일(일) 낮 최고 %s도 · 쌓인 눈 %dcm" % (fmt(t28['hi']), t28['depth']), font=F(30, True), fill=INK)
d.text((X0 + 34, y + 88), "11년 1월 %d일 중 낮 4도 이상 오른 날은 %d일뿐이었어" % (P['n'], P['hi_ge4']), font=F(27), fill=MUT)
y += 170 + 36
d.text((X0 + 8, y), "직접 만든 그림 · 일본 기상청 札幌 관측소 일별값으로 계산", font=F(22), fill=MUT)
d.text((X0 + 8, Hh - 62), "걷고읽고떠나고", font=F(22), fill="#b0b0b0")
im.save(os.path.join(HERE, "card_conclusion.png"))
print('cnt', cnt, 'cold', cold, 'hi_lt0', hl, P['hi_ge0'], P['hi_ge4'], t28, sdmax)
