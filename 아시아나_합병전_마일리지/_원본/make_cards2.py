# -*- coding: utf-8 -*-
"""블로그 카드 v2 — 모든 숫자는 '합병 전 76일 중 N일', 일반석(주황)·비즈니스(파랑) 나란히"""
import sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ozdata import DAYS, N, SOURCE_AT, nm, avail, listed, short, missing

sys.stdout.reconfigure(encoding='utf-8')
OUT = sys.argv[1]
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF, INK, INK2, MUTED, GRID, AXIS = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'
NONE = '#e6e4dd'
ECO, BIZ = '#eb6834', '#2a78d6'
W = 1080
SRC = str(SOURCE_AT).replace('. ', '.')


def canvas(h):
    fig = plt.figure(figsize=(W / 100, h / 100), dpi=100, facecolor=SURF)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis('off')
    return fig, ax


def footer(ax, h):
    ax.text(40, h - 58, '자료: 아시아나항공 마일리지 좌석 조회 달력 (기준 ' + SRC + ')', fontsize=17, color=MUTED, va='center')
    ax.text(40, h - 30, '하루 한 번 갱신되는 표시라 실시간 잔여와 다를 수 있어 · 좌석승급용 제외', fontsize=17, color=MUTED, va='center')


def legend(ax, y):
    x = 40
    for c, lab, wd, edge in ((ECO, '일반석 있음', 165, None), (BIZ, '비즈니스 있음', 190, None), (NONE, '좌석 없음', 140, None), (SURF, '편이 안 뜬 날', 0, AXIS)):
        ax.add_patch(Rectangle((x, y - 11), 22, 22, facecolor=c, edgecolor=edge if edge else 'none', lw=1))
        ax.text(x + 30, y, lab, fontsize=19, color=INK2, va='center')
        x += 30 + wd


def strip_card(fn, title, pairs):
    X0, CW = 248, 8.6
    SW = CW * N
    rows_spec = []
    H = 232
    for a, b in pairs:
        H += 46 + 24  # 노선 제목 + 월 라벨
        for o, d, cab, lab in ((a, b, 'Y', '가는 편 일반석'), (a, b, 'C', '가는 편 비즈니스'), (b, a, 'Y', '오는 편 일반석'), (b, a, 'C', '오는 편 비즈니스')):
            av = avail(o, d, cab)
            ls = set(listed(o, d, cab))
            note = ''
            if cab == 'C' and 0 < len(av) <= 12:
                note = short(av)
            elif cab == 'Y' and len(av) >= 40 and len(missing(o, d, cab)) <= 6:
                note = '없는 날 ' + short(missing(o, d, cab))
            elif cab == 'Y' and 0 < len(av) <= 8:
                note = short(av)
            rows_spec.append((a, b, o, d, cab, lab, av, ls, note))
            H += 34 + (24 if note else 0)
        H += 30
    H += 86
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=38, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '합병 전 76일 (2026.10.2~12.16 출발) 가운데 좌석이 있던 날', fontsize=22, color=INK2, va='center')
    legend(ax, 168)
    ax.text(X0 + SW + 14, 212, '76일 중', fontsize=16, color=MUTED, va='center')
    y = 232
    i = 0
    for a, b in pairs:
        ax.text(40, y + 22, nm(a) + ' ↔ ' + nm(b), fontsize=28, fontweight='bold', color=INK, va='center')
        for j, d_ in enumerate(DAYS):
            if d_.day == 1 or j == 0:
                ax.text(X0 + j * CW, y + 56, str(d_.month) + '월', fontsize=15, color=MUTED, va='center')
        ry = y + 70
        for _ in range(4):
            _a, _b, o, d, cab, lab, av, ls, note = rows_spec[i]
            i += 1
            have = set(av)
            col = ECO if cab == 'Y' else BIZ
            ax.text(40, ry + 14, lab, fontsize=19, color=INK, va='center')
            for j, d_ in enumerate(DAYS):
                if d_ in have:
                    ax.add_patch(Rectangle((X0 + j * CW, ry + 2), CW - 1.2, 25, facecolor=col, edgecolor='none'))
                elif d_ in ls:
                    ax.add_patch(Rectangle((X0 + j * CW, ry + 2), CW - 1.2, 25, facecolor=NONE, edgecolor='none'))
                else:
                    ax.add_patch(Rectangle((X0 + j * CW, ry + 2), CW - 1.2, 25, facecolor=SURF, edgecolor=GRID, lw=0.5))
            for j, d_ in enumerate(DAYS):
                if d_.day == 1:
                    ax.plot([X0 + j * CW - 0.8, X0 + j * CW - 0.8], [ry, ry + 29], color=AXIS, lw=1)
            ax.text(X0 + SW + 14, ry + 14, str(len(av)) + '일', fontsize=22, color=INK, va='center', fontweight='bold')
            ry += 34
            if note:
                ax.text(X0, ry + 8, note, fontsize=16, color=INK2, va='center')
                ry += 24
        y = ry + 30
        ax.plot([40, W - 40], [y - 16, y - 16], color=GRID, lw=1)
    footer(ax, H)
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', H)


def thumb(fn):
    H = 1080
    fig, ax = canvas(H)
    ax.text(60, 92, '합병 전 76일', fontsize=62, fontweight='bold', color=INK, va='center')
    ax.text(60, 170, '아시아나 마일리지 좌석 · 인천 → 뉴욕', fontsize=32, color=INK2, va='center')
    y = 250
    for cab, lab, col in (('Y', '일반석', ECO), ('C', '비즈니스', BIZ)):
        av = set(avail('ICN', 'JFK', cab))
        ls = set(listed('ICN', 'JFK', cab))
        ax.text(60, y + 40, lab, fontsize=44, fontweight='bold', color=INK, va='center')
        ax.text(W - 60, y + 40, str(len(av)) + '일', fontsize=84, fontweight='bold', color=INK, va='center', ha='right')
        gx, gy, cs = 60, y + 110, 48.5
        for i, d_ in enumerate(DAYS):
            cx, cy = gx + (i % 20) * cs, gy + (i // 20) * cs
            if d_ in av:
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=col, edgecolor='none'))
            elif d_ in ls:
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=NONE, edgecolor='none'))
            else:
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=SURF, edgecolor=AXIS, lw=1.2))
        y += 110 + 4 * cs + 56
    ax.text(60, 1020, '칸 하나가 하루 · 색칠한 칸이 좌석이 있던 날', fontsize=24, color=MUTED, va='center')
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', H)


def overview(fn, routes):
    RH = 104
    H = 250 + RH * len(routes) + 96
    fig, ax = canvas(H)
    ax.text(40, 62, '합병 전 76일 중 좌석이 있던 날', fontsize=38, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '아시아나 마일리지 · 한국에서 가는 편 · 2026.10.2~12.16 출발', fontsize=22, color=INK2, va='center')
    ax.add_patch(Rectangle((40, 160), 24, 24, facecolor=ECO, edgecolor='none'))
    ax.text(74, 172, '일반석', fontsize=21, color=INK2, va='center')
    ax.add_patch(Rectangle((180, 160), 24, 24, facecolor=BIZ, edgecolor='none'))
    ax.text(214, 172, '비즈니스', fontsize=21, color=INK2, va='center')
    X0, BW = 360, 540
    for t in (0, 38, 76):
        x = X0 + BW * t / N
        ax.plot([x, x], [222, 250 + RH * len(routes) - 22], color=GRID, lw=1)
        ax.text(x, 208, str(t) + '일', fontsize=16, color=MUTED, ha='center', va='center')
    y = 236
    for o, d in routes:
        ax.text(X0 - 18, y + 38, nm(o) + ' → ' + nm(d), fontsize=25, fontweight='bold', color=INK, va='center', ha='right')
        for j, (cab, col) in enumerate((('Y', ECO), ('C', BIZ))):
            n = len(avail(o, d, cab))
            yy = y + 6 + j * 36
            ax.add_patch(Rectangle((X0, yy), BW, 28, facecolor='#efeee9', edgecolor='none'))
            if n:
                ax.add_patch(Rectangle((X0, yy), max(BW * n / N, 4), 28, facecolor=col, edgecolor='none'))
            ax.text(X0 + BW + 16, yy + 14, str(n) + '일', fontsize=24, color=INK, va='center', fontweight='bold')
        y += RH
        ax.plot([40, W - 40], [y - 14, y - 14], color=GRID, lw=1)
    footer(ax, H)
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', H)


thumb('oz_thumb_newyork.png')
overview('oz_overview.png', [('ICN', 'JFK'), ('ICN', 'LAX'), ('ICN', 'LHR'), ('ICN', 'CDG'), ('ICN', 'SYD'), ('ICN', 'BKK'), ('ICN', 'SIN'),
                             ('ICN', 'MNL'), ('ICN', 'NRT'), ('ICN', 'KIX'), ('ICN', 'PEK'), ('GMP', 'CJU')])
strip_card('oz_americas.png', '아시아나 마일리지 좌석 · 미주', [('ICN', 'JFK'), ('ICN', 'LAX'), ('ICN', 'SFO'), ('ICN', 'SEA')])
strip_card('oz_europe.png', '아시아나 마일리지 좌석 · 유럽', [('ICN', 'LHR'), ('ICN', 'CDG'), ('ICN', 'FRA'), ('ICN', 'FCO'), ('ICN', 'MXP'), ('ICN', 'BCN'), ('ICN', 'PRG'), ('ICN', 'IST')])
strip_card('oz_sydney_almaty.png', '아시아나 마일리지 좌석 · 시드니·중앙아시아', [('ICN', 'SYD'), ('ICN', 'ALA'), ('ICN', 'TAS')])
strip_card('oz_southeast_asia.png', '아시아나 마일리지 좌석 · 동남아', [('ICN', 'BKK'), ('ICN', 'SIN'), ('ICN', 'MNL'), ('ICN', 'SGN'), ('ICN', 'HAN'), ('ICN', 'DAD'), ('ICN', 'HKT'), ('ICN', 'KTI'), ('ICN', 'CRK'), ('ICN', 'CGK')])
strip_card('oz_japan.png', '아시아나 마일리지 좌석 · 일본', [('ICN', 'NRT'), ('ICN', 'HND'), ('GMP', 'HND'), ('ICN', 'KIX'), ('GMP', 'KIX'), ('ICN', 'FUK'), ('ICN', 'NGO'), ('ICN', 'CTS'), ('ICN', 'OKA')])
