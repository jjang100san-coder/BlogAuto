# -*- coding: utf-8 -*-
"""지방 광역시 글 숫자 카드 5장 — 직접 만든 그림(5-6). 숫자: ../지방광역시_데이터.md · ../유튜브_지방광역시_종합.md."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
for f in ("C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"):
    fm.fontManager.addfont(f)
plt.rcParams["font.family"] = fm.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name()
plt.rcParams["axes.unicode_minus"] = False
SURF, INK, INK2, GRID, BAND = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e2dd", "#f3f2ee"
UP, DOWN = "#e34948", "#2a78d6"            # 한국식 오름 빨강·내림 파랑 (검증 통과)
A, B = "#2a78d6", "#eb6834"                 # 범주 1·2 슬롯
SRC = "자료: 국토교통부 아파트 매매 실거래가(2019.1~2026.9 계약, 해제 제외) · 직접 집계 · 2026-10-12 조회"


def frame(title, sub, src=SRC, h=10):
    fig = plt.figure(figsize=(12, h), dpi=100, facecolor=SURF)
    fig.text(0.05, 0.94, title, fontsize=30, fontweight="bold", color=INK, va="top")
    fig.text(0.05, 0.875, sub, fontsize=17, color=INK2, va="top", linespacing=1.5)
    fig.text(0.05, 0.02, src, fontsize=13, color=INK2, va="bottom", linespacing=1.4)
    return fig


def style(ax):
    ax.set_facecolor(SURF)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=16, length=0)
    ax.grid(axis="x", color=GRID, lw=1)
    ax.set_axisbelow(True)


def hbar(ax, names, vals, xlim, fmt="{:+.1f}%", color=None, labels=True):
    y = list(range(len(names)))[::-1]
    cols = [color or (UP if v >= 0 else DOWN) for v in vals]
    ax.barh(y, vals, color=cols, height=0.62, edgecolor=SURF, linewidth=2)
    ax.axvline(0, color=INK2, lw=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels(names if labels else [], fontsize=19, color=INK)
    span = xlim[1] - xlim[0]
    for yi, v in zip(y, vals):
        ax.text(v + (span * 0.015 if v >= 0 else -span * 0.015), yi, fmt.format(v), va="center",
                ha="left" if v >= 0 else "right", fontsize=17, color=INK, fontweight="bold")
    ax.set_xlim(*xlim)
    style(ax)
    ax.set_xticklabels([])


def table(fig, heads, rows, xs, top=0.8, step=0.12, color_cols=(), axtop=0.82):
    ax = fig.add_axes([0.05, 0.1, 0.9, axtop - 0.1])
    ax.axis("off")
    for x, h in zip(xs, heads):
        ax.text(x, 0.96, h, fontsize=19, color=INK2, fontweight="bold", va="center")
    for i, r in enumerate(rows):
        yy = top - i * step
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((-0.01, yy - step / 2), 1.0, step, color=BAND, lw=0))
        for j, (x, v) in enumerate(zip(xs, r)):
            c = INK
            if j in color_cols and v not in ("", "-"):
                c = DOWN if v.startswith("-") else UP
            ax.text(x, yy, v, fontsize=21, color=c, va="center", fontweight="bold" if j == 0 else "normal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


# ① 이전 최고가 대비 · 신고가 비율
names = ["울산", "대전", "부산", "광주", "대구", "세종"]
peak = [-12.1, -22.4, -22.5, -25.4, -27.8, -30.1]
newhi = [5.9, 3.8, 2.0, 1.0, 2.9, 0.7]
fig = frame("지금 거래, 그 단지 최고가보다 얼마나 낮나",
            "2026년 7~9월 매매를 같은 단지·같은 면적의 2019년 이후 이전 최고가와 비교\n(이전 거래 3건 이상, 중위값)")
ax1 = fig.add_axes([0.13, 0.1, 0.42, 0.6])
hbar(ax1, names, peak, (-40, 4))
ax1.set_title("이전 최고가 대비", fontsize=18, color=INK, loc="left", pad=12)
ax2 = fig.add_axes([0.63, 0.1, 0.32, 0.6])
hbar(ax2, names, newhi, (0, 9), fmt="{:.1f}%", color=UP, labels=False)
ax2.set_title("신고가 거래 비율", fontsize=18, color=INK, loc="left", pad=12)
fig.savefig(os.path.join(HERE, "261013_2.png"), facecolor=SURF)
plt.close(fig)

# ② 같은 단지 네 기준
rows = [("울산", "+24.2", "-1.9", "+4.3", "+3.2"), ("세종", "+36.0", "-24.0", "+0.8", "+1.9"),
        ("대전", "+28.0", "-8.5", "-1.2", "+0.2"), ("부산", "+6.9", "-12.2", "-4.1", "+0.9"),
        ("대구", "-8.7", "-27.3", "-6.6", "+0.4"), ("광주", "+4.3", "-6.5", "-7.7", "-1.9")]
fig = frame("2021년 고점 뒤로는 어디서 재도 울산이 맨 위", "같은 단지 ㎡당 가격 변화(%) · 기준 해 → 2026년(1~9월) · 단지별 중위 변화율의 중위")
table(fig, ["광역시", "2019→", "2021→", "2023→", "2025→"], rows, [0.0, 0.3, 0.48, 0.66, 0.84], color_cols=(1, 2, 3, 4))
fig.savefig(os.path.join(HERE, "261013_3.png"), facecolor=SURF)
plt.close(fig)

# ③ 울산 구별 2023→2026
fig = frame("울산 안에서도 동구는 반대로 갔다",
            "울산 구·군별 같은 단지 ㎡당 가격 변화 · 2023년 → 2026년(1~9월)\n동구는 지금 거래가 이전 최고가보다 22.1% 낮다(울산 전체 12.1%)")
ax = fig.add_axes([0.16, 0.12, 0.76, 0.62])
hbar(ax, ["남구", "중구", "북구", "울주군", "동구"], [8.9, 6.6, 4.6, 2.3, -5.9], (-10, 13))
fig.savefig(os.path.join(HERE, "261013_5.png"), facecolor=SURF)
plt.close(fig)

# ④ 미분양 2023.1 → 지금
fig = frame("미분양, 대구는 3분의 1로 부산은 3배로",
            "미분양 주택(호) · 2023년 1월 → 2026년 8월(광주·세종은 6월)",
            src="자료: 한국부동산원 R-ONE 미분양주택현황 · 공식 집계는 사업자가 공개한 물량 기준이라 실제보다 적게 잡힐 수 있다 · 2026-10-12 조회")
names = ["대구", "부산", "울산", "대전", "광주", "세종"]
v23 = [13565, 2646, 4253, 3025, 262, 6]
vnow = [4162, 7594, 1190, 2521, 1245, 43]
ax = fig.add_axes([0.13, 0.12, 0.8, 0.64])
y = list(range(len(names)))[::-1]
ax.barh([i + 0.18 for i in y], v23, height=0.34, color=A, edgecolor=SURF, linewidth=2, label="2023년 1월")
ax.barh([i - 0.18 for i in y], vnow, height=0.34, color=B, edgecolor=SURF, linewidth=2, label="지금")
for i, a, b in zip(y, v23, vnow):
    ax.text(a + 150, i + 0.18, f"{a:,}", va="center", fontsize=15, color=INK)
    ax.text(b + 150, i - 0.18, f"{b:,}", va="center", fontsize=15, color=INK, fontweight="bold")
ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=19, color=INK)
ax.set_xlim(0, 16000)
style(ax)
ax.set_xticklabels([])
ax.legend(loc="lower right", fontsize=16, frameon=False)
fig.savefig(os.path.join(HERE, "261013_6.png"), facecolor=SURF)
plt.close(fig)

# ⑤ 잣대 대조
rows = [("울산", "+1.0", "+4.3"), ("세종", "-4.8", "+0.8"), ("대전", "-6.1", "-1.2"),
        ("부산", "-9.6", "-4.1"), ("광주", "-8.1", "-7.7"), ("대구", "-14.7", "-6.6")]
fig = frame("두 잣대, 맨 위는 같고 크기는 다르다",
            "2023년 이후 변화(%)\n한국부동산원 매매가격지수(2023.1 → 2026.8) vs 같은 단지 실거래(2023 → 2026년 1~9월)",
            src="자료: 한국부동산원 R-ONE · 국토교통부 실거래가(직접 집계) · 부동산원 = 표본 단지 시세 조사, 실거래 = 신고된 거래 · 2026-10-12 조회")
table(fig, ["광역시", "부동산원 지수", "같은 단지 실거래"], rows, [0.0, 0.36, 0.7], color_cols=(1, 2), axtop=0.74)
fig.savefig(os.path.join(HERE, "261013_8.png"), facecolor=SURF)
plt.close(fig)
print("cards done")
