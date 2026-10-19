# -*- coding: utf-8 -*-
"""시라카와고(白川 아메다스) 1월 11년치 그래프 2장 + 결론 카드 1장.
① chart_0114_depth.png  해마다 1월 14일 쌓인 눈·그날 내린 눈
② chart_jan_depth.png   1월 한 달 적설 11년 겹침(1/14 세로선)
③ card_conclusion.png   결론 카드(오키나와 편과 같은 꼴)
자료: base data\\chubu_daily.json (기상청 白川 1306 일별, 2026-10-12 수집)
"""
import json, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
BG, INK, MUT, RED, NAVY, SNOW = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#8fb3d9"
D = json.load(open(os.path.join(HERE, 'base data', 'chubu_daily.json'), encoding='utf-8'))['시라카와']
YEARS = list(range(2016, 2027))
jan = {y: D['%d-01' % y] for y in YEARS}
v = lambda x: x if x is not None else 0.0

# ① 1/14
dep = [v(jan[y][13]['snow_depth']) for y in YEARS]; new = [v(jan[y][13]['snow']) for y in YEARS]
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); ax.set_facecolor(BG)
bars = ax.bar(range(len(YEARS)), dep, 0.62, color=SNOW, label="그날 쌓여 있던 눈 (최심적설)")
ax.bar(range(len(YEARS)), new, 0.30, color=NAVY, label="그날 새로 내린 눈 (강설)")
for i, (a, b) in enumerate(zip(dep, new)):
    ax.text(i, a + 4, f"{a:.0f}", ha="center", fontsize=13, color=INK, fontweight="bold")
    if b >= 1: ax.text(i + 0.33, b + 2, f"+{b:.0f}", ha="left", fontsize=10, color=NAVY)
ax.axhline(100, color=RED, lw=1, alpha=.5); ax.text(10.45, 101, "100cm", color=RED, fontsize=11)
ax.set_xticks(range(len(YEARS))); ax.set_xticklabels([str(y) for y in YEARS], fontsize=12)
ax.set_ylim(0, 205); ax.set_ylabel("cm", color=MUT); ax.tick_params(colors=MUT)
[s.set_visible(False) for s in ax.spines.values()]
ax.set_title("시라카와고 1월 14일, 쌓여 있던 눈은 해마다 3cm에서 182cm", fontsize=18, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(frameon=False, loc="upper left", fontsize=11)
fig.text(0.01, 0.01, "일본 기상청 白川 관측소(시라카와무라 하토가야) 일별값 2016~2026 · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_0114_depth.png"), facecolor=BG); plt.close(fig)

# ② 1월 한 달 적설
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); ax.set_facecolor(BG)
for y in YEARS:
    rs = jan[y]; x = [r['day'] for r in rs]; yy = [r['snow_depth'] for r in rs]
    hl = y in (2020, 2021)
    ax.plot(x, yy, color=(RED if y == 2021 else NAVY) if hl else "#c8c8c8", lw=2.6 if hl else 1.2, label=(f"{y}" if hl else None))
ax.plot([], [], color="#c8c8c8", lw=1.5, label="나머지 9년")
ax.axvline(14, color=MUT, lw=1, ls="--"); ax.text(14.3, 250, "1/14 (내가 가는 날)", color=MUT, fontsize=12)
for xx in (10.5, 20.5): ax.axvline(xx, color="#e2e2e2", lw=1)
ax.set_xlim(1, 31); ax.set_ylim(0, 260); ax.set_xticks([1, 5, 10, 14, 20, 25, 31])
ax.set_xticklabels([f"1/{i}" for i in [1, 5, 10, 14, 20, 25, 31]], fontsize=12)
ax.set_ylabel("쌓인 눈 (cm)", color=MUT); ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
ax.set_title("시라카와고 1월 한 달 쌓인 눈 11년 — 가장 많았던 2021년, 가장 적었던 2020년", fontsize=17, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(frameon=False, loc="upper right", fontsize=11)
fig.text(0.01, 0.01, "일본 기상청 白川 관측소 일별 최심적설 2016~2026 · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_jan_depth.png"), facecolor=BG); plt.close(fig)

# ③ 결론 카드
W, H = 1400, 1400
LINE, PINK = "#e2e2e2", "#eef4fb"
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", s)
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); X0, X1 = 70, W - 70
d.text((X0, 58), "1월 중순 시라카와고,", font=F(58, True), fill=INK)
d.text((X0, 134), "눈은 해마다 3cm부터 182cm", font=F(58, True), fill=NAVY)
d.text((X0, 222), "일본 기상청 白川 관측소 2016~2026년 11년치 · 1월 14일 기준", font=F(22), fill=MUT)
rows = [("쌓여 있던 눈", "100cm 넘은 해 5번 · 40cm 아래인 해 4번", "50cm 넘게 쌓여 있던 해는 11년 중 7번", True),
        ("그날 내린 눈", "10cm 넘게 내린 해 4번 (2016·2017·2022·2026)", "걷는 동안 눈이 올 수 있어", False),
        ("1월 중순 기온", "낮 최고 평균 1.0~5.6도 · 아침 최저 -5.5~-1.0도", "중순 아침 최저 평균은 11년 모두 영하", False)]
y = 300
for t, a, b, hl in rows:
    h = 200
    d.rounded_rectangle((X0, y, X1, y + h), radius=18, fill=PINK if hl else "#ffffff", outline=NAVY if hl else LINE, width=4 if hl else 2)
    d.text((X0 + 34, y + 30), t, font=F(36, True), fill=NAVY if hl else INK)
    d.text((X0 + 34, y + 90), a, font=F(30, True), fill=INK)
    d.text((X0 + 34, y + 140), b, font=F(28), fill=MUT)
    y += h + 26
y += 10
d.text((X0, y), "내가 가는 날", font=F(30, True), fill=NAVY); y += 56
d.rounded_rectangle((X0, y, X1, y + 170), radius=18, fill="#ffffff", outline=LINE, width=2)
d.text((X0 + 34, y + 28), "2027년 1월 14일(목) 낮 12:57 도착 ~ 16:15 버스로 나옴", font=F(30, True), fill=INK)
d.text((X0 + 34, y + 88), "추위 많이 타는 사람과 둘이 · 라이트업 날(1/11·17·24·31)은 아님", font=F(28), fill=MUT)
y += 170 + 36
d.text((X0 + 8, y), "직접 만든 그림 · 일본 기상청 白川 관측소 일별값으로 계산", font=F(22), fill=MUT)
d.text((X0 + 8, H - 62), "걷고읽고떠나고", font=F(22), fill="#b0b0b0")
im.save(os.path.join(HERE, "card_conclusion.png")); print("ok", y)
