# -*- coding: utf-8 -*-
"""블로그용 카드 이미지 (모바일에서 읽히는 큰 글자, 가로 1080px)"""
import json, sys, os, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.stdout.reconfigure(encoding='utf-8')
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
LO, HI = '20261002', '20261216'
res, source_at = {}, None
for f in ('main.json', 'scan2.json'):
    j = json.load(open(f, encoding='utf-8'))
    source_at = j.get('sourceAt') or source_at
    res.update(j['res'])

NAME = {'ICN': '인천', 'GMP': '김포', 'PUS': '부산', 'LAX': 'LA', 'JFK': '뉴욕', 'SFO': '샌프란시스코', 'SEA': '시애틀',
        'LHR': '런던', 'CDG': '파리', 'FRA': '프랑크푸르트', 'FCO': '로마', 'MXP': '밀라노', 'BCN': '바르셀로나', 'PRG': '프라하', 'IST': '이스탄불',
        'SYD': '시드니', 'ALA': '알마티', 'TAS': '타슈켄트',
        'MNL': '마닐라', 'KTI': '프놈펜', 'SGN': '호찌민', 'HKT': '푸껫', 'HAN': '하노이', 'DAD': '다낭', 'CRK': '클락', 'BKK': '방콕', 'SIN': '싱가포르', 'CGK': '자카르타',
        'NRT': '도쿄 나리타', 'HND': '도쿄 하네다', 'KIX': '오사카', 'FUK': '후쿠오카', 'NGO': '나고야', 'CTS': '삿포로', 'OKA': '오키나와'}
days_all = []
_d = dt.date(2026, 10, 2)
while _d <= dt.date(2026, 12, 16):
    days_all.append(_d)
    _d += dt.timedelta(days=1)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF, INK, INK2, MUTED, GRID, AXIS = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'
C0, C1, C2, C3 = '#e6e4dd', '#86b6ef', '#2a78d6', '#104281'
BIZ, ECO = '#2a78d6', '#eb6834'
W = 1080


def color(v):
    return C0 if v == 0 else C1 if v <= 3 else C2 if v <= 8 else C3


def daily(k, cab):
    out = {}
    if k not in res:
        return out
    for day, row in res[k]['days'].items():
        if LO <= day <= HI and row[cab]:
            out[day] = sum(q for _, _, q in row[cab])
    return out


def canvas(h):
    fig = plt.figure(figsize=(W / 100, h / 100), dpi=100, facecolor=SURF)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis('off')
    return fig, ax


def footer(ax, h):
    ax.text(40, h - 58, '자료: 아시아나항공 마일리지 좌석 조회 달력 (기준 ' + str(source_at).replace('. ', '.') + ')', fontsize=17, color=MUTED, va='center')
    ax.text(40, h - 30, '하루 한 번 갱신되는 표시라 실시간 잔여와 다를 수 있어 · 좌석승급용 제외', fontsize=17, color=MUTED, va='center')


def strip_card(fn, title, pairs):
    X0, CW = 268, 8.6
    SW = CW * len(days_all)
    BLOCK = 46 + 22 + 4 * 34 + 30
    H = 232 + len(pairs) * BLOCK + 86
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=38, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '합병 전 76일 (2026.10.2~12.16 출발) · 날짜별 보너스 좌석', fontsize=22, color=INK2, va='center')
    lx, ly = 40, 168
    for c, lab, wd in ((C3, '9석 이상', 128), (C2, '4~8석', 106), (C1, '1~3석', 106), (C0, '좌석 없음', 136)):
        ax.add_patch(Rectangle((lx, ly - 11), 22, 22, facecolor=c, edgecolor='none'))
        ax.text(lx + 30, ly, lab, fontsize=19, color=INK2, va='center')
        lx += 30 + wd
    ax.add_patch(Rectangle((lx, ly - 11), 22, 22, facecolor=SURF, edgecolor=AXIS, lw=1))
    ax.text(lx + 30, ly, '편이 안 뜬 날', fontsize=19, color=INK2, va='center')
    ax.text(X0 + SW + 14, 212, '있는 날/뜬 날', fontsize=15, color=MUTED, va='center')
    y = 232
    for a, b in pairs:
        ax.text(40, y + 22, NAME.get(a, a) + ' ↔ ' + NAME.get(b, b), fontsize=28, fontweight='bold', color=INK, va='center')
        for i, d_ in enumerate(days_all):
            if d_.day == 1 or i == 0:
                ax.text(X0 + i * CW, y + 54, str(d_.month) + '월', fontsize=15, color=MUTED, va='center')
        ry = y + 68
        for k, cab, lab in ((a + '-' + b, 'C', '가는 편 비즈니스'), (a + '-' + b, 'Y', '가는 편 일반석'),
                            (b + '-' + a, 'C', '오는 편 비즈니스'), (b + '-' + a, 'Y', '오는 편 일반석')):
            dly = daily(k, cab)
            ax.text(40, ry + 14, lab, fontsize=19, color=INK if cab == 'C' else INK2, va='center')
            for i, d_ in enumerate(days_all):
                key = d_.strftime('%Y%m%d')
                if key in dly:
                    ax.add_patch(Rectangle((X0 + i * CW, ry + 2), CW - 1.2, 25, facecolor=color(dly[key]), edgecolor='none'))
                else:
                    ax.add_patch(Rectangle((X0 + i * CW, ry + 2), CW - 1.2, 25, facecolor=SURF, edgecolor=GRID, lw=0.5))
            for i, d_ in enumerate(days_all):
                if d_.day == 1:
                    ax.plot([X0 + i * CW - 0.8, X0 + i * CW - 0.8], [ry, ry + 29], color=AXIS, lw=1)
            av = sum(1 for v in dly.values() if v > 0)
            ax.text(X0 + SW + 14, ry + 14, (str(av) + ' / ' + str(len(dly)) + '일') if dly else '편 없음', fontsize=20, color=INK, va='center',
                    fontweight='bold' if cab == 'C' else 'normal')
            ry += 34
        y += BLOCK
        ax.plot([40, W - 40], [y - 16, y - 16], color=GRID, lw=1)
    footer(ax, H)
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', H)


# ---- 1. 썸네일 (1:1) — 인천→뉴욕 일반석 71/71, 비즈니스 1/71
def thumb(fn):
    H = 1080
    fig, ax = canvas(H)
    k = 'ICN-JFK'
    ax.text(60, 92, '합병 전 76일', fontsize=62, fontweight='bold', color=INK, va='center')
    ax.text(60, 170, '아시아나 마일리지 좌석 · 인천 → 뉴욕', fontsize=32, color=INK2, va='center')
    y = 250
    for cab, lab, col in (('Y', '일반석', C3), ('C', '비즈니스', C3)):
        dly = daily(k, cab)
        av = sum(1 for v in dly.values() if v > 0)
        ax.text(60, y + 40, lab, fontsize=44, fontweight='bold', color=INK, va='center')
        ax.text(W - 60, y + 40, str(av) + '일', fontsize=84, fontweight='bold', color=INK, va='center', ha='right')
        gx, gy, cs = 60, y + 110, 48.5
        for i, d_ in enumerate(days_all):
            key = d_.strftime('%Y%m%d')
            cx, cy = gx + (i % 20) * cs, gy + (i // 20) * cs
            if key in dly:
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=(C3 if dly[key] > 0 else C0), edgecolor='none'))
            else:
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=SURF, edgecolor=AXIS, lw=1.2))
        y += 110 + 4 * cs + 56
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', H)


# ---- 2. 지역 요약 (날 수 그대로)
def region_card(fn):
    REG = [('미주', ['LAX', 'JFK', 'SFO', 'SEA']), ('유럽', ['LHR', 'CDG', 'FRA', 'FCO', 'MXP', 'BCN', 'PRG', 'IST']), ('대양주', ['SYD']),
           ('동남아', ['MNL', 'KTI', 'SGN', 'HKT', 'HAN', 'DAD', 'CRK', 'BKK', 'SIN', 'CGK']),
           ('일본', ['NRT', 'HND', 'KIX', 'FUK', 'NGO', 'CTS', 'OKA', 'SDJ', 'KMI', 'UKB'])]
    rows = []
    for reg, aps in REG:
        t = {'C': [0, 0], 'Y': [0, 0]}
        for ap in aps:
            for k in ('ICN-' + ap, ap + '-ICN'):
                for cab in ('C', 'Y'):
                    dly = daily(k, cab)
                    t[cab][0] += sum(1 for v in dly.values() if v > 0)
                    t[cab][1] += len(dly)
        rows.append((reg, t))
    RH = 150
    H = 250 + RH * len(rows) + 96
    fig, ax = canvas(H)
    ax.text(40, 62, '합병 전 76일, 아시아나 마일리지 좌석', fontsize=36, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '인천 노선 · 2026.10.2~12.16 · 편이 뜬 날 중 좌석이 있던 날', fontsize=22, color=INK2, va='center')
    ax.add_patch(Rectangle((40, 160), 24, 24, facecolor=BIZ, edgecolor='none'))
    ax.text(74, 172, '비즈니스', fontsize=21, color=INK2, va='center')
    ax.add_patch(Rectangle((200, 160), 24, 24, facecolor=ECO, edgecolor='none'))
    ax.text(234, 172, '일반석', fontsize=21, color=INK2, va='center')
    X0, BW = 180, 560
    y = 230
    for reg, t in rows:
        ax.text(40, y + 52, reg, fontsize=32, fontweight='bold', color=INK, va='center')
        for j, (cab, col) in enumerate((('C', BIZ), ('Y', ECO))):
            av, op = t[cab]
            yy = y + 14 + j * 46
            ax.add_patch(Rectangle((X0, yy), BW, 34, facecolor='#efeee9', edgecolor='none'))
            ax.add_patch(Rectangle((X0, yy), max(BW * av / op, 3), 34, facecolor=col, edgecolor='none'))
            ax.text(X0 + BW + 16, yy + 17, '{:,}일 / {:,}일'.format(av, op), fontsize=24, color=INK, va='center')
        y += RH
        ax.plot([40, W - 40], [y - 18, y - 18], color=GRID, lw=1)
    ax.text(40, H - 86, '노선·방향별로 센 날을 지역 안에서 더한 값이야 (인천 노선만)', fontsize=17, color=MUTED, va='center')
    footer(ax, H)
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', H)
    return rows


thumb('oz_thumb_newyork.png')
rows = region_card('oz_region_summary.png')
for reg, t in rows:
    print('  ', reg, t)
strip_card('oz_americas.png', '아시아나 마일리지 좌석 · 미주', [('ICN', 'LAX'), ('ICN', 'JFK'), ('ICN', 'SFO'), ('ICN', 'SEA')])
strip_card('oz_europe.png', '아시아나 마일리지 좌석 · 유럽', [('ICN', 'LHR'), ('ICN', 'CDG'), ('ICN', 'FRA'), ('ICN', 'FCO'), ('ICN', 'MXP'), ('ICN', 'BCN'), ('ICN', 'PRG'), ('ICN', 'IST')])
strip_card('oz_sydney_almaty.png', '아시아나 마일리지 좌석 · 시드니·중앙아시아', [('ICN', 'SYD'), ('ICN', 'ALA'), ('ICN', 'TAS')])
strip_card('oz_southeast_asia.png', '아시아나 마일리지 좌석 · 동남아', [('ICN', 'MNL'), ('ICN', 'KTI'), ('ICN', 'SGN'), ('ICN', 'HKT'), ('ICN', 'HAN'), ('ICN', 'DAD'), ('ICN', 'CRK'), ('ICN', 'BKK'), ('ICN', 'SIN'), ('ICN', 'CGK')])
strip_card('oz_japan.png', '아시아나 마일리지 좌석 · 일본', [('ICN', 'NRT'), ('ICN', 'HND'), ('GMP', 'HND'), ('ICN', 'KIX'), ('GMP', 'KIX'), ('ICN', 'FUK'), ('ICN', 'NGO'), ('ICN', 'CTS'), ('ICN', 'OKA')])
