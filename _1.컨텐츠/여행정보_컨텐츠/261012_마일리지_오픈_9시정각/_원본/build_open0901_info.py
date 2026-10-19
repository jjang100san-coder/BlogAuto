# -*- coding: utf-8 -*-
"""「마일리지 항공권 오픈일」 글 — 인포그래픽 카드 4장 (2026-10-12 사용자: 「글이 너무 많아, 이미지화·인포그래픽화」)
사용: python build_open0901_info.py "<글 폴더>"   (build_open0901.py 가 만든 _summary.json 을 읽는다)
"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

OUT = sys.argv[1]
J = json.load(open(os.path.join(OUT, '_summary.json'), encoding='utf-8'))
S = J['summary']; SN = {t[:10]: a for t, e, a in J['snaps']}
D3, D7 = SN['2027-10-03'], SN['2027-10-07']
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e6e4dd'
KE = '#2a78d6'; NONE = '#e6e4dd'; WARN = '#d9534f'; MID = '#f0ad4e'; GREEN = '#3a9d5d'; PALE = '#f3f2ee'
W = 1080


def canvas(h):
    fig = plt.figure(figsize=(W / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(h, 0); ax.axis('off')
    fig.patch.set_facecolor(SURF)
    return fig, ax


def footer(ax, h, when):
    ax.text(40, h - 58, '자료: 대한항공 마일리지 예매 화면에 로그인해 직접 조회 (%s)' % when, fontsize=16, color=MUTED, va='center')
    ax.text(40, h - 30, '성인 1명 편도 · 잔여 수는 화면 표시 상한 9 · 좌석은 수시로 바뀌어 조회 시점의 기록임', fontsize=16, color=MUTED, va='center')


def save(fig, fn):
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF); plt.close(fig); print(fn)


def box(ax, x, y, w, h, fc, ec='none', r=18):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=%d' % r, facecolor=fc, edgecolor=ec, lw=2))


# ── 카드 1: 08:59 → 09:00 → 09:01 세 칸 ──────────────────────────────
H = 820
fig, ax = canvas(H)
ax.text(40, 62, '9시 정각에 누르면 거부, 9시 1분에 누르면 열려', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '10월 11일·12일 아침, 1분에 한 번 「항공편 검색」을 눌렀어 · 이틀이 똑같았어', fontsize=18, color=INK2, va='center')
panels = [
    ('08:59', '날짜가 안 눌려', '달력에서 그 날짜가 회색.\n미리 골라 둘 수 없어.', NONE, INK2, ''),
    ('09:00', '접근 거부', '「접근이 거부됐다」 화면\n11일 09:00:25 · 12일 09:00:18', WARN, 'white', 'X'),
    ('09:01', '열렸어', '다시 누르니 정상 응답\n12일 09:01:16 · 로그인 그대로', KE, 'white', 'O'),
]
pw, gap, px0, py = 320, 20, 40, 160
for i, (t, head, body, col, fg, mark) in enumerate(panels):
    x = px0 + i * (pw + gap)
    box(ax, x, py, pw, 400, col if i else PALE)
    tc = fg if i else INK
    ax.text(x + pw / 2, py + 70, t, fontsize=56, fontweight='bold', color=tc, ha='center', va='center')
    ax.text(x + pw / 2, py + 165, mark, fontsize=64, fontweight='bold', color=tc if i else MUTED, ha='center', va='center')
    ax.text(x + pw / 2, py + 255, head, fontsize=28, fontweight='bold', color=tc, ha='center', va='center')
    ax.text(x + pw / 2, py + 330, body, fontsize=15, color=tc, ha='center', va='center', linespacing=1.5)
    if i < 2:
        ax.text(x + pw + gap / 2, py + 200, '›', fontsize=40, color=MUTED, ha='center', va='center')
# 아래 띠: 9시 전 연타 경고
box(ax, 40, 590, W - 80, 86, '#fdf1ec', ec='#f3c9bf')
ax.text(70, 633, '!', fontsize=34, fontweight='bold', color=WARN, va='center', ha='center')
ax.text(120, 622, '9시 전에 연타하면 안 돼', fontsize=22, fontweight='bold', color=INK, va='center')
ax.text(120, 654, '10월 10일, 9시 전에 12방향을 1분 동안 연달아 조회했더니 두 시간 가까이 막혔어', fontsize=16, color=INK2, va='center')
footer(ax, H, '2026.10.10~10.12 아침')
save(fig, 'info_0900_3steps_20261012.png')


# ── 카드 2: 연휴 출발일, 열린 지 두 시간 — 유럽 프레스티지 0/9 ─────────
eu_cities = ['런던', '파리', '프랑크푸르트', '밀라노', '이스탄불', '암스테르담', '마드리드', '빈', '리스본']
n_eu, ok_eu, _ = D3['유럽']; n_am, ok_am, _ = D3['미주·대양주']; n_as, ok_as, _ = D3['아시아']
assert n_eu == 9 and ok_eu == 0
H = 860
fig, ax = canvas(H)
ax.text(40, 62, '연휴 출발일은 열린 지 두 시간 만에 이랬어', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '2027년 10월 3일(일) 출발 · 10월 8일 아침 9시에 열렸고, 11시 전후에 52도시를 봤어', fontsize=18, color=INK2, va='center')
# 큰 숫자
box(ax, 40, 160, 480, 300, PALE)
ax.text(70, 205, '유럽 프레스티지', fontsize=22, fontweight='bold', color=INK2, va='center')
ax.text(280, 320, '0', fontsize=120, fontweight='bold', color=WARN, ha='center', va='center')
ax.text(280, 420, '%d편 중 0편' % n_eu, fontsize=24, fontweight='bold', color=INK, ha='center', va='center')
# 도시 칩 3×3
cx0, cy0, cw, ch = 560, 170, 150, 84
for i, c in enumerate(eu_cities):
    x = cx0 + (i % 3) * (cw + 12); y = cy0 + (i // 3) * (ch + 12)
    box(ax, x, y, cw, ch, NONE, r=12)
    ax.text(x + cw / 2, y + 30, c, fontsize=16 if len(c) < 6 else 14, fontweight='bold', color=INK2, ha='center', va='center')
    ax.text(x + cw / 2, y + 60, '0석', fontsize=16, color=WARN, ha='center', va='center')
# 아래 두 칸
for i, (lab, n, ok, col) in enumerate((('미주·대양주 프레스티지', n_am, ok_am, '#6b5bd6'), ('아시아 프레스티지', n_as, ok_as, KE))):
    x = 40 + i * 520
    box(ax, x, 500, 500, 150, PALE)
    ax.text(x + 30, 540, lab, fontsize=20, fontweight='bold', color=INK2, va='center')
    ax.add_patch(Rectangle((x + 30, 585), 440, 26, facecolor=NONE, edgecolor='none'))
    ax.add_patch(Rectangle((x + 30, 585), 440 * ok / n, 26, facecolor=col, edgecolor='none'))
    ax.text(x + 30, 632, '%d편 중 %d편에 남음' % (n, ok), fontsize=18, fontweight='bold', color=INK, va='center')
ax.text(40, 690, '일반석은 달랐어 — 0석은 파리 공동운항 2편뿐, 나머지는 9석 이상', fontsize=18, color=INK2, va='center')
footer(ax, H, '2026.10.8 10:42~11:08')
save(fig, 'info_holiday_eu0_20261012.png')


# ── 카드 3: 연휴 vs 평일 — 두 기둥 ─────────────────────────────────
H = 760
fig, ax = canvas(H)
ax.text(40, 62, '연휴라서가 아니야, 평일도 10분이면 거의 없어', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '유럽 프레스티지가 남은 편 수 · 각 날짜를 열린 당일에 조회', fontsize=18, color=INK2, va='center')
cols = [
    ('연휴 출발일', '2027-10-03 (일)', '열린 지 2시간', D3, PALE, INK),
    ('평일', '2027-10-07 (목)', '열린 지 10분', D7, '#eaf2fc', KE),
]
for i, (lab, d, el, A, fc, hc) in enumerate(cols):
    x = 40 + i * 520
    box(ax, x, 160, 500, 440, fc)
    ax.text(x + 250, 200, lab, fontsize=26, fontweight='bold', color=INK, ha='center', va='center')
    ax.text(x + 250, 236, d + ' · ' + el, fontsize=17, color=MUTED, ha='center', va='center')
    n, ok, _ = A['유럽']
    ax.text(x + 250, 340, '%d / %d' % (ok, n), fontsize=84, fontweight='bold', color=WARN if ok == 0 else hc, ha='center', va='center')
    ax.text(x + 250, 420, '유럽 %d편 중 %d편' % (n, ok), fontsize=22, fontweight='bold', color=INK, ha='center', va='center')
    yy = 480
    for reg, col in (('미주·대양주', '#6b5bd6'), ('아시아', KE)):
        n2, ok2, _ = A[reg]
        ax.text(x + 40, yy, reg, fontsize=16, color=INK2, va='center')
        ax.add_patch(Rectangle((x + 160, yy - 9), 200, 18, facecolor=NONE, edgecolor='none'))
        ax.add_patch(Rectangle((x + 160, yy - 9), 200 * ok2 / n2, 18, facecolor=col, edgecolor='none'))
        ax.text(x + 375, yy, '%d편 중 %d편' % (n2, ok2), fontsize=16, fontweight='bold', color=INK, va='center')
        yy += 44
ax.text(40, 640, '날짜가 달라 같은 날의 비교는 아님 · 10/3 은 출발편만, 10/7 은 왕복', fontsize=15, color=MUTED, va='center')
footer(ax, H, '2026.10.8 · 10.12')
save(fig, 'info_holiday_vs_weekday_20261012.png')


# ── 카드 4: 실행 순서 체크리스트 ──────────────────────────────────
steps = [
    ('08:50쯤', '로그인하기', '너무 일찍 하면 안 돼 — 40분 안 움직이면 자동 로그아웃'),
    ('09:00', '날짜 고르기', '9시가 지나야 달력에서 날짜가 살아나'),
    ('09:01', '항공편 검색', '정각이 아니라 1분에 눌러'),
    ('거부가 뜨면', '1분 뒤 한 번 더', '같은 창에서. 로그인 다시 할 필요 없어'),
    ('보이면', '비즈니스부터 잡기', '일반석은 열린 날 낮에 봐도 있었어'),
]
H = 900
fig, ax = canvas(H)
ax.text(40, 62, '연휴 비즈니스를 노린다면, 순서는 이 다섯 줄', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '이번 나흘 아침에 본 것만으로 만든 순서야', fontsize=18, color=INK2, va='center')
y = 165
for i, (when, what, why) in enumerate(steps):
    box(ax, 40, y, W - 80, 108, PALE if i != 2 else '#eaf2fc')
    ax.add_patch(Circle((95, y + 54), 28, facecolor=KE if i != 3 else WARN, edgecolor='none'))
    ax.text(95, y + 54, str(i + 1), fontsize=24, fontweight='bold', color='white', ha='center', va='center')
    ax.text(150, y + 38, when, fontsize=18, color=MUTED, va='center')
    ax.text(150, y + 74, what, fontsize=28, fontweight='bold', color=INK, va='center')
    ax.text(W - 70, y + 56, why, fontsize=16, color=INK2, va='center', ha='right')
    y += 124
ax.text(40, y + 14, '좌석은 그 뒤에도 움직여 — 0이던 자리가 다시 열리기도 하니 원하는 날이 0이어도 시간을 달리해 다시 봐', fontsize=15, color=MUTED, va='center')
footer(ax, H, '2026.10.8~10.12')
save(fig, 'info_checklist_20261012.png')
