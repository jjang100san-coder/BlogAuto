# -*- coding: utf-8 -*-
"""2027년 10월 연휴(10/1~10/3 출발) 대한항공 실시간 보너스 좌석 → 통합 CSV + 카드 이미지
사용: python build_holiday.py "<글 폴더>"
입력: <글 폴더>/base data/ke_live_2027holiday.json (아시아), _europe.json, _americas.json
"""
import sys, os, json, csv, collections
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

OUT = sys.argv[1]
BD = os.path.join(OUT, 'base data')
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e6e4dd'
KE = '#2a78d6'; NONE = '#e6e4dd'; WARN = '#d9534f'; MID = '#f0ad4e'
W = 1080
DAYS = [('20271001', '10/1 금'), ('20271002', '10/2 토'), ('20271003', '10/3 일')]
NAME = {'FUK': '후쿠오카', 'KIX': '오사카', 'NRT': '도쿄 나리타', 'HND': '도쿄 하네다', 'CXR': '나트랑', 'CTS': '삿포로', 'PQC': '푸꾸옥', 'DAD': '다낭', 'PVG': '상하이', 'OKA': '오키나와', 'TPE': '타이베이', 'NGO': '나고야', 'HKG': '홍콩', 'BKK': '방콕', 'DPS': '발리', 'GUM': '괌', 'HAN': '하노이', 'CEB': '세부', 'SGN': '호치민', 'SIN': '싱가포르', 'TAO': '칭다오', 'HKT': '푸켓',
        'LHR': '런던', 'CDG': '파리', 'FRA': '프랑크푸르트', 'FCO': '로마', 'MXP': '밀라노', 'BCN': '바르셀로나', 'PRG': '프라하', 'IST': '이스탄불', 'AMS': '암스테르담', 'MAD': '마드리드', 'VIE': '빈', 'ZRH': '취리히', 'BUD': '부다페스트', 'LIS': '리스본',
        'LAX': 'LA', 'JFK': '뉴욕', 'SFO': '샌프란시스코', 'HNL': '호놀룰루', 'SEA': '시애틀', 'LAS': '라스베이거스', 'YVR': '밴쿠버', 'YYZ': '토론토', 'ORD': '시카고', 'ATL': '애틀랜타', 'DFW': '댈러스', 'BOS': '보스턴', 'IAD': '워싱턴', 'SYD': '시드니', 'BNE': '브리즈번', 'AKL': '오클랜드'}
REGION = [('아시아', 'ke_live_2027holiday.json'), ('유럽', 'ke_live_2027holiday_europe.json'), ('미주·대양주', 'ke_live_2027holiday_americas.json')]

# ───────── 읽기 ─────────
F = []     # 편 단위
CELL = {}  # (region, code, ymd) → {'state': 'fl'|'nofl'|'nofare', 'fl': [...]}
ASOF = {}
for region, fn in REGION:
    L = json.load(open(os.path.join(BD, fn), encoding='utf-8'))
    for key, days in L.items():
        code = key.split('-')[1]
        for ymd, lab in DAYS:
            r = days.get(ymd, {})
            fl = [f for f in r.get('flights', []) if f.get('segs', 1) == 1]
            ASOF.setdefault(region, r.get('at', ''))
            if not fl:
                CELL[(region, code, ymd)] = {'state': 'nofare' if r.get('code') == 'ERT.7190' else 'nofl', 'fl': []}
                continue
            rows = []
            for f in fl:
                ey = f['cab'].get('EY') or [None, None, None]; pr = f['cab'].get('PR') or [None, None, None]; fr = f['cab'].get('FR') or [None, None, None]
                rec = {'region': region, 'code': code, 'city': NAME[code], 'ymd': ymd, 'flt': f['flt'], 'dep': f['dep'][8:10] + ':' + f['dep'][10:12],
                       'ey': ey[0], 'ey_m': ey[2], 'pr': pr[0], 'pr_m': pr[2], 'fr': fr[0], 'at': r.get('at', '')}
                F.append(rec); rows.append(rec)
            CELL[(region, code, ymd)] = {'state': 'fl', 'fl': rows}

with open(os.path.join(OUT, '2027년10월연휴_대한항공_마일리지_편별_20261008.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['권역', '도시', '공항', '출발일', '편명', '출발시각', '일반석 잔여(표시 상한 9)', '일반석 마일', '프레스티지 잔여', '프레스티지 마일', '일등석 잔여', '조회 시각'])
    for r in F:
        w.writerow([r['region'], r['city'], r['code'], r['ymd'], r['flt'], r['dep'], r['ey'], r['ey_m'], '' if r['pr'] is None else r['pr'], r['pr_m'] or '', '' if r['fr'] is None else r['fr'], r['at']])

# ───────── 집계 ─────────
S = {}
for region, _ in REGION:
    fl = [r for r in F if r['region'] == region]
    S[region] = {'n': len(fl), 'ey0': sum(1 for r in fl if r['ey'] == 0), 'ey9': sum(1 for r in fl if r['ey'] == 9), 'eylow': sum(1 for r in fl if r['ey'] is not None and 0 < r['ey'] < 9),
                 'pr0': sum(1 for r in fl if (r['pr'] or 0) == 0), 'prok': sum(1 for r in fl if (r['pr'] or 0) > 0),
                 'cities': len({r['code'] for r in fl}),
                 'ey0_list': [(r['city'], r['ymd'], r['flt'], r['dep']) for r in fl if r['ey'] == 0],
                 'eylow_list': [(r['city'], r['ymd'], r['flt'], r['dep'], r['ey']) for r in fl if r['ey'] is not None and 0 < r['ey'] < 9],
                 'prok_list': [(r['city'], r['ymd'], r['flt'], r['dep'], r['pr']) for r in fl if (r['pr'] or 0) > 0]}
json.dump({'summary': S, 'asof': ASOF}, open(os.path.join(OUT, '_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for k, v in S.items():
    print(k, {a: b for a, b in v.items() if not a.endswith('_list')})

# ───────── 그림 공통 ─────────
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


def ey_color(v):
    if v is None: return NONE
    if v == 0: return WARN
    if v < 9: return MID
    return KE


# ───────── ① 썸네일: 세 권역 비교 ─────────
H = 1080
fig, ax = canvas(H)
ax.text(60, 90, '2027년 10월 연휴 마일리지 좌석', fontsize=46, fontweight='bold', color=INK, va='center')
ax.text(60, 150, '대한항공 · 인천 출발 10/1~10/3 · 열린 지 이틀 안에 조회', fontsize=24, color=INK2, va='center')
y = 230
for region, _ in REGION:
    s = S[region]
    ax.text(60, y, region, fontsize=34, fontweight='bold', color=KE, va='center')
    ax.text(1020, y, '%d도시 %d편' % ({'아시아': 22, '유럽': 14, '미주·대양주': 16}[region], s['n']), fontsize=24, color=INK2, va='center', ha='right')
    y += 62
    ax.text(60, y, '일반석 0석인 편', fontsize=26, color=INK2, va='center')
    ax.text(1020, y, '%d편 중 %d편' % (s['n'], s['ey0']), fontsize=38, fontweight='bold', color=INK, va='center', ha='right')
    y += 58
    ax.text(60, y, '프레스티지 0석인 편', fontsize=26, color=INK2, va='center')
    ax.text(1020, y, '%d편 중 %d편' % (s['n'], s['pr0']), fontsize=38, fontweight='bold', color=INK, va='center', ha='right')
    y += 52
    # 막대: 일반석(위)·프레스티지(아래) 0석 비율을 칸으로
    for i, (lab, z) in enumerate((('일반석', s['ey0']), ('프레스티지', s['pr0']))):
        bx = 60; bw = 760
        ax.add_patch(Rectangle((bx, y + i * 26), bw, 16, facecolor=NONE, edgecolor='none'))
        if z:
            ax.add_patch(Rectangle((bx, y + i * 26), bw * z / s['n'], 16, facecolor=WARN if lab == '일반석' else INK2, edgecolor='none'))
        ax.text(bx + bw + 14, y + i * 26 + 8, lab + ' 0석', fontsize=15, color=MUTED, va='center')
    y += 100
ax.text(60, H - 40, '예매 화면 직접 조회 (2026.10.8 오전) · 직접 만든 그림', fontsize=18, color=MUTED, va='center')
save(fig, 'holiday_thumb_20261008.png')

# ───────── ② 권역별 격자: 도시 × 날짜, 칸 안은 편별 일반석 잔여 ─────────
def grid(region, fn, title, sub, codes):
    rowh = 46
    H = 300 + len(codes) * rowh + 110
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=32, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, sub, fontsize=19, color=INK2, va='center')
    # 범례
    lx = 40
    for lab, col in (('9석 이상', KE), ('1~8석', MID), ('0석', WARN), ('편 없음·운임 없음', NONE)):
        ax.add_patch(Rectangle((lx, 150), 18, 18, facecolor=col, edgecolor='none'))
        ax.text(lx + 26, 159, lab, fontsize=16, color=INK2, va='center')
        lx += 26 + len(lab) * 15 + 36
    x0 = 250; cw = (W - 40 - x0) / 3
    for j, (ymd, lab) in enumerate(DAYS):
        ax.text(x0 + cw * j + cw / 2, 215, lab, fontsize=20, color=INK2, ha='center', va='center')
    ax.plot([40, W - 40], [238, 238], color=GRID, lw=1.2)
    y = 262
    for code in codes:
        ax.text(40, y + rowh / 2, NAME[code], fontsize=19, color=INK, va='center')
        for j, (ymd, lab) in enumerate(DAYS):
            c = CELL.get((region, code, ymd), {'state': 'nofl', 'fl': []})
            x = x0 + cw * j + 6
            if c['state'] != 'fl':
                ax.add_patch(Rectangle((x, y + 6), cw - 12, rowh - 12, facecolor='#f2f1ec', edgecolor='none'))
                ax.text(x + (cw - 12) / 2, y + rowh / 2, '운임 없음' if c['state'] == 'nofare' else '편 없음', fontsize=14, color=MUTED, ha='center', va='center')
                continue
            n = len(c['fl']); bw = (cw - 12 - 4 * (n - 1)) / n
            for k, r in enumerate(c['fl']):
                col = ey_color(r['ey'])
                ax.add_patch(Rectangle((x + k * (bw + 4), y + 6), bw, rowh - 12, facecolor=col, edgecolor='none'))
                txt = '%s %s' % (r['dep'], '0석' if r['ey'] == 0 else ('%d석' % r['ey'] if r['ey'] < 9 else '9+'))
                ax.text(x + k * (bw + 4) + bw / 2, y + rowh / 2, txt if n <= 3 else (r['dep'] if r['ey'] >= 9 else '%d' % r['ey']), fontsize=13 if n <= 3 else 11,
                        color='white' if col in (KE, WARN) else INK, ha='center', va='center')
        y += rowh
    ax.plot([40, W - 40], [y + 4, y + 4], color=GRID, lw=1.2)
    ax.text(40, y + 30, '칸 하나가 편 하나 · 안의 숫자는 일반석 잔여(9 이상은 9+) · 시각은 인천 출발', fontsize=15, color=MUTED, va='center')
    footer(ax, H, ASOF[region][:16].replace('-', '.') if ASOF[region] else '2026.10.8')
    save(fig, fn)


AS = ['FUK', 'KIX', 'NRT', 'HND', 'CTS', 'NGO', 'OKA', 'CXR', 'DAD', 'PQC', 'HAN', 'SGN', 'BKK', 'HKT', 'DPS', 'CEB', 'SIN', 'PVG', 'TAO', 'TPE', 'HKG', 'GUM']
EU = ['LHR', 'CDG', 'FRA', 'AMS', 'FCO', 'MXP', 'BCN', 'MAD', 'LIS', 'PRG', 'VIE', 'ZRH', 'BUD', 'IST']
AM = ['LAX', 'SFO', 'SEA', 'LAS', 'JFK', 'BOS', 'IAD', 'ORD', 'ATL', 'DFW', 'HNL', 'YVR', 'YYZ', 'SYD', 'BNE', 'AKL']
grid('유럽', 'holiday_grid_europe_20261008.png', '유럽 14도시, 연휴 출발 일반석 마일리지', '인천 출발 2027년 10월 1~3일 · 조회 당일 오전 11시 · 편마다 일반석 잔여', EU)
grid('아시아', 'holiday_grid_asia_20261008.png', '아시아 22도시, 연휴 출발 일반석 마일리지', '인천 출발 2027년 10월 1~3일 · 조회 당일 오전 10시 42분~48분 · 편마다 일반석 잔여', AS)
grid('미주·대양주', 'holiday_grid_americas_20261008.png', '미주·대양주 16도시, 연휴 출발 일반석 마일리지', '인천 출발 2027년 10월 1~3일 · 조회 당일 오전 11시 5분~8분 · 편마다 일반석 잔여', AM)

# ───────── ③ 프레스티지 카드: 권역별 남은 편 수 + 남은 편 목록 ─────────
H = 1040
fig, ax = canvas(H)
ax.text(40, 62, '프레스티지(비즈니스) 좌석은 어디에 남았나', fontsize=36, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '인천 출발 2027년 10월 1~3일 · 편 단위 · 열린 지 이틀 안에 조회', fontsize=19, color=INK2, va='center')
y = 190
for region, _ in REGION:
    s = S[region]
    ax.text(40, y, region, fontsize=28, fontweight='bold', color=INK, va='center')
    ax.text(1040, y, '%d편 중 %d편에 남음' % (s['n'], s['prok']), fontsize=28, fontweight='bold', color=KE, va='center', ha='right')
    y += 40
    bw = W - 80
    ax.add_patch(Rectangle((40, y), bw, 22, facecolor=NONE, edgecolor='none'))
    if s['prok']:
        ax.add_patch(Rectangle((40, y), bw * s['prok'] / s['n'], 22, facecolor=KE, edgecolor='none'))
    y += 44
    # 도시별 남은 편/전체 편
    tot = collections.OrderedDict()
    for r in F:
        if r['region'] != region: continue
        t = tot.setdefault(r['city'], [0, 0]); t[1] += 1; t[0] += 1 if (r['pr'] or 0) > 0 else 0
    pieces = ['%s %d/%d' % (c, a, b) for c, (a, b) in tot.items()]
    lines, line = [], ''
    for pc in pieces:
        if len(line) + len(pc) > 52:
            lines.append(line); line = ''
        line += ('   ' if line else '') + pc
    lines.append(line)
    for ln in lines:
        ax.text(40, y, ln, fontsize=16, color=INK2, va='center'); y += 30
    y += 26
    ax.plot([40, W - 40], [y - 10, y - 10], color=GRID, lw=1)
    y += 10
ax.text(40, y + 4, '도시 뒤 숫자는 「프레스티지 남은 편 / 전체 편」', fontsize=15, color=MUTED, va='center')
footer(ax, H, '2026.10.8 오전')
save(fig, 'holiday_prestige_20261008.png')
