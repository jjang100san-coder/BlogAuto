# -*- coding: utf-8 -*-
"""셔세권 글 숫자 카드 5장 — 직접 만든 정보 그림(마스터 5-4·5-6: AI로 만들지 않는다). 숫자 출처: ../셔세권_데이터.md · ../유튜브_셔세권_종합.md 3-0."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
from matplotlib import font_manager as _fm
for _f in ("C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"):
    _fm.fontManager.addfont(_f)
plt.rcParams["font.family"] = _fm.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name()
plt.rcParams["axes.unicode_minus"] = False
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e2dd"
UP, DOWN = "#e34948", "#2a78d6"          # 한국식: 오름 빨강 · 내림 파랑 (diverging 쌍, 검증 통과)
CAT = ["#2a78d6", "#eb6834", "#1baf7a"]   # 범주 1~3 슬롯 (검증 통과, aqua 는 직접 라벨로 보완)
SRC = "자료: 국토교통부 아파트 매매 실거래가(2019.1~2026.9 계약, 해제 제외) · 직접 집계 · 2026-10-11 조회"


def frame(title, sub, src=SRC, h=10):
    fig = plt.figure(figsize=(12, h), dpi=100, facecolor=SURF)
    fig.text(0.05, 0.94, title, fontsize=30, fontweight="bold", color=INK, va="top")
    fig.text(0.05, 0.875, sub, fontsize=18, color=INK2, va="top")
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


def hbar(ax, names, vals, fmt="{:+.1f}%", xlim=None, notes=None):
    y = list(range(len(names)))[::-1]
    cols = [UP if v >= 0 else DOWN for v in vals]
    ax.barh(y, vals, color=cols, height=0.62, edgecolor=SURF, linewidth=2)
    ax.axvline(0, color=INK2, lw=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=19, color=INK)
    span = (xlim[1] - xlim[0]) if xlim else max(abs(v) for v in vals) * 2
    for yi, v, k in zip(y, vals, range(len(vals))):
        lab = fmt.format(v) + ((" " + notes[k]) if notes and notes[k] else "")
        ax.text(v + (span * 0.015 if v >= 0 else -span * 0.015), yi, lab, va="center",
                ha="left" if v >= 0 else "right", fontsize=17, color=INK, fontweight="bold")
    if xlim:
        ax.set_xlim(*xlim)
    style(ax)
    ax.set_xticklabels([])


# ① 6곳 같은 단지 2023→2026
fig = frame("셔틀 동네 6곳, 같은 아파트가 이렇게 갈렸다",
            "같은 단지 ㎡당 가격 변화 · 2023년 → 2026년(1~9월) · 단지별 중위 변화율의 중위")
ax = fig.add_axes([0.2, 0.12, 0.72, 0.68])
hbar(ax, ["용인 수지구", "화성 동탄구", "수원 영통구", "화성 병점구", "용인 기흥구", "평택시"],
     [31.5, 20.6, 19.4, 9.8, 8.6, -15.9], xlim=(-26, 42))
fig.savefig(os.path.join(HERE, "261012_3.png"), facecolor=SURF)
plt.close(fig)

# ② 네 기준 표 — 체리피킹 반론
rows = [("용인 수지구", "+83.0", "+9.9", "+31.5", "+16.7"), ("화성 동탄구", "+70.6", "-0.7", "+20.6", "+8.0"),
        ("수원 영통구", "+70.8", "+2.1", "+19.4", "+8.3"), ("화성 병점구", "+70.8", "+2.5", "+9.8", "+3.8"),
        ("용인 기흥구", "+61.2", "-4.6", "+8.6", "+5.1"), ("평택시", "+18.9", "-5.8", "-15.9", "-4.0")]
fig = frame("기준 해를 바꿔도 수지가 맨 위, 평택이 맨 아래", "같은 단지 ㎡당 가격 변화(%) · 기준 해 → 2026년(1~9월)", h=10)
ax = fig.add_axes([0.05, 0.1, 0.9, 0.72])
ax.axis("off")
heads = ["지역", "2019→", "2021→", "2023→", "2025→"]
xs = [0.0, 0.36, 0.52, 0.68, 0.84]
for x, h in zip(xs, heads):
    ax.text(x, 0.95, h, fontsize=20, color=INK2, fontweight="bold", va="center")
for i, r in enumerate(rows):
    yy = 0.82 - i * 0.14
    if i % 2 == 0:
        ax.add_patch(plt.Rectangle((-0.01, yy - 0.06), 1.0, 0.12, color="#f3f2ee", lw=0))
    for j, (x, v) in enumerate(zip(xs, r)):
        c = INK if j == 0 else (DOWN if v.startswith("-") else UP)
        ax.text(x, yy, v, fontsize=22, color=c, va="center", fontweight="bold" if j in (0, 3) else "normal")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
fig.savefig(os.path.join(HERE, "261012_4.png"), facecolor=SURF)
plt.close(fig)

# ③ 이전 최고가 대비 · 신고가 비율 (두 측정 → 두 패널, 축 하나씩)
names = ["용인 수지구", "화성 동탄구", "수원 영통구", "용인 기흥구", "화성 병점구", "평택시"]
peak = [-2.3, -3.5, -8.7, -10.0, -18.4, -31.9]
newhi = [31.9, 30.0, 16.9, 10.7, 8.2, 2.0]
fig = frame("'최고가 대비 폭락'은 동네마다 뜻이 다르다",
            "2026년 7~9월 거래 · 같은 단지·같은 면적의 2019년 이후 이전 최고가와 비교(이전 거래 3건 이상)")
ax1 = fig.add_axes([0.2, 0.12, 0.34, 0.66])
hbar(ax1, names, peak, xlim=(-44, 4))
ax1.set_title("이전 최고가보다 얼마나 낮나(중위)", fontsize=18, color=INK, loc="left", pad=12)
ax2 = fig.add_axes([0.62, 0.12, 0.33, 0.66])
y = list(range(len(names)))[::-1]
ax2.barh(y, newhi, color=UP, height=0.62, edgecolor=SURF, linewidth=2)
for yi, v in zip(y, newhi):
    ax2.text(v + 0.8, yi, "{:.1f}%".format(v), va="center", fontsize=17, color=INK, fontweight="bold")
ax2.set_yticks(y)
ax2.set_yticklabels([])
ax2.set_xlim(0, 42)
style(ax2)
ax2.set_xticklabels([])
ax2.set_title("신고가 거래 비율", fontsize=18, color=INK, loc="left", pad=12)
fig.savefig(os.path.join(HERE, "261012_6.png"), facecolor=SURF)
plt.close(fig)

# ④ 2026 월별 거래 — 7/1 규제
months = list(range(1, 10))
series = [("화성 동탄구", [961, 775, 964, 954, 1257, 1913, 153, 139, 227]),
          ("용인 기흥구", [974, 664, 740, 735, 738, 1130, 247, 254, 258]),
          ("화성 병점구", [239, 209, 280, 248, 280, 407, 487, 261, 294])]
fig = frame("규제 다음 달, 동탄 거래는 10분의 1이 됐다",
            "2026년 월별 아파트 매매 건수(계약월 기준)\n동탄구·기흥구: 7월 1일 조정대상·투기과열지구, 7월 5일 토지거래허가구역",
            src="자료: 국토교통부 실거래가(해제 제외) · 직접 집계 · 2026-10-11 조회 · 8·9월은 신고 기한 때문에 아직 채워지는 중")
ax = fig.add_axes([0.09, 0.13, 0.72, 0.62])
ax.axvspan(6.5, 9.5, color="#f3f2ee", lw=0)
ax.text(6.6, 1950, "7월 규제 이후", fontsize=16, color=INK2, va="top")
for (nm, v), c in zip(series, CAT):
    ax.plot(months, v, color=c, lw=2.5, marker="o", ms=8, markeredgecolor=SURF, markeredgewidth=2)
    ax.text(9.15, {"화성 동탄구": 150, "용인 기흥구": 300, "화성 병점구": 450}[nm], nm, color=c, fontsize=16, va="center", fontweight="bold")
    ax.plot([9.05], [v[-1]], marker="s", color=c, ms=10)
ax.annotate("1,913건", (6, 1913), xytext=(4.6, 1850), fontsize=16, color=INK, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=INK2))
ax.annotate("153건", (7, 153), xytext=(7.4, 520), fontsize=16, color=INK, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=INK2))
ax.set_xticks(months)
ax.set_xticklabels([f"{m}월" for m in months])
ax.set_xlim(0.6, 9.5)
ax.set_ylim(0, 2050)
style(ax)
ax.grid(axis="x", visible=False)
ax.grid(axis="y", color=GRID, lw=1)
fig.savefig(os.path.join(HERE, "261012_7.png"), facecolor=SURF)
plt.close(fig)

# ⑤ 인구 4년 · 같은 단지 가격 2023→2026 (두 측정 → 두 패널)
names = ["용인 수지구", "수원 영통구", "용인 기흥구", "화성 동탄구", "화성 병점구", "평택시"]
pop = [-2.2, 0.2, -1.0, 10.3, 10.3, 8.4]
price = [31.5, 19.4, 8.6, 20.6, 9.8, -15.9]
fig = frame("사람이 는 곳과 값이 오른 곳이 달랐다",
            "인구: 주민등록 2022.10 → 2026.09 · 가격: 같은 단지 ㎡당 2023 → 2026(1~9월)",
            src="자료: 행정안전부 주민등록 인구·국토교통부 실거래가 · 2026-10-11 조회\n* 동탄·병점 인구는 2026년 2월 구 신설 전후를 맞추려 두 구 합계")
ax1 = fig.add_axes([0.2, 0.12, 0.33, 0.66])
hbar(ax1, names, pop, xlim=(-6, 16), notes=["", "", "", "*", "*", ""])
ax1.set_title("인구", fontsize=19, color=INK, loc="left", pad=12)
ax2 = fig.add_axes([0.6, 0.12, 0.35, 0.66])
hbar(ax2, names, price, xlim=(-26, 42))
ax2.set_yticklabels([])
ax2.set_title("같은 단지 가격", fontsize=19, color=INK, loc="left", pad=12)
fig.savefig(os.path.join(HERE, "261012_9.png"), facecolor=SURF)
plt.close(fig)
print("cards done")
