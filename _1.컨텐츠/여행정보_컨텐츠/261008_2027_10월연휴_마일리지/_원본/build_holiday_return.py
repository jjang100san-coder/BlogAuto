# -*- coding: utf-8 -*-
"""2027년 10월 연휴 — 복귀편(10/3·10/4) 실시간 + 출발편 하루 뒤 재조회 → CSV·요약·카드 이미지
사용: python build_holiday_return.py "<글 폴더>"
입력(base data/): ke_live_2027holiday*.json(10/8 출발), ke_live_2027holiday_return_1009.json, ke_live_2027holiday_out_recheck_1009.json
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
KE = '#2a78d6'; NONE = '#e6e4dd'; WARN = '#d9534f'; MID = '#f0ad4e'; GREEN = '#3a9d5d'
W = 1080
NAME = {'FUK': '후쿠오카', 'KIX': '오사카', 'NRT': '도쿄 나리타', 'HND': '도쿄 하네다', 'CXR': '나트랑', 'CTS': '삿포로', 'PQC': '푸꾸옥', 'DAD': '다낭', 'PVG': '상하이', 'OKA': '오키나와', 'TPE': '타이베이', 'NGO': '나고야', 'HKG': '홍콩', 'BKK': '방콕', 'DPS': '발리', 'GUM': '괌', 'HAN': '하노이', 'CEB': '세부', 'SGN': '호치민', 'SIN': '싱가포르', 'TAO': '칭다오', 'HKT': '푸켓',
        'LHR': '런던', 'CDG': '파리', 'FRA': '프랑크푸르트', 'FCO': '로마', 'MXP': '밀라노', 'BCN': '바르셀로나', 'PRG': '프라하', 'IST': '이스탄불', 'AMS': '암스테르담', 'MAD': '마드리드', 'VIE': '빈', 'ZRH': '취리히', 'BUD': '부다페스트', 'LIS': '리스본',
        'LAX': 'LA', 'JFK': '뉴욕', 'SFO': '샌프란시스코', 'HNL': '호놀룰루', 'SEA': '시애틀', 'LAS': '라스베이거스', 'YVR': '밴쿠버', 'YYZ': '토론토', 'ORD': '시카고', 'ATL': '애틀랜타', 'DFW': '댈러스', 'BOS': '보스턴', 'IAD': '워싱턴', 'SYD': '시드니', 'BNE': '브리즈번', 'AKL': '오클랜드'}
AS = ['FUK', 'KIX', 'NRT', 'HND', 'CTS', 'NGO', 'OKA', 'CXR', 'DAD', 'PQC', 'HAN', 'SGN', 'BKK', 'HKT', 'DPS', 'CEB', 'SIN', 'PVG', 'TAO', 'TPE', 'HKG', 'GUM']
EU = ['LHR', 'CDG', 'FRA', 'AMS', 'FCO', 'MXP', 'BCN', 'MAD', 'LIS', 'PRG', 'VIE', 'ZRH', 'BUD', 'IST']
AM = ['LAX', 'SFO', 'SEA', 'LAS', 'JFK', 'BOS', 'IAD', 'ORD', 'ATL', 'DFW', 'HNL', 'YVR', 'YYZ', 'SYD', 'BNE', 'AKL']
REGION = {}
for c in AS: REGION[c] = '아시아'
for c in EU: REGION[c] = '유럽'
for c in AM: REGION[c] = '미주·대양주'
RNAME = ['아시아', '유럽', '미주·대양주']
RCNT = {'아시아': 22, '유럽': 14, '미주·대양주': 16}


def load(fn):
    return json.load(open(os.path.join(BD, fn), encoding='utf-8'))


def flights(r):
    out = []
    for f in r.get('flights', []):
        if f.get('segs', 1) != 1:
            continue
        ey = f['cab'].get('EY') or [None, None, None]; pr = f['cab'].get('PR') or [None, None, None]; fr = f['cab'].get('FR') or [None, None, None]
        out.append({'flt': f['flt'], 'dep': f['dep'][8:10] + ':' + f['dep'][10:12], 'ey': ey[0], 'ey_m': ey[2], 'pr': pr[0], 'pr_m': pr[2], 'fr': fr[0]})
    return out


def state(r):
    if flights(r):
        return 'fl'
    return 'nofare' if r.get('code') == 'ERT.7190' else ('unopened' if r.get('code') == 'ERT.10032' else 'nofl')


# ───────── 읽기 ─────────
OUT8 = {}
for fn in ('ke_live_2027holiday.json', 'ke_live_2027holiday_europe.json', 'ke_live_2027holiday_americas.json'):
    OUT8.update(load(fn))
RET = load('ke_live_2027holiday_return_1009.json')
RECHK = load('ke_live_2027holiday_out_recheck_1009.json')
RDAYS = [('20271003', '10/3 일'), ('20271004', '10/4 월')]
ODAYS = ['20271001', '20271002', '20271003']

# 복귀 편 단위
RF = []
RCELL = {}
RASOF = {}
for key, days in RET.items():
    code = key.split('-')[0]; reg = REGION[code]
    for ymd, lab in RDAYS:
        r = days.get(ymd, {})
        RASOF.setdefault(reg, r.get('at', ''))
        fl = flights(r)
        RCELL[(code, ymd)] = {'state': state(r), 'fl': fl}
        for f in fl:
            RF.append(dict(f, region=reg, code=code, city=NAME[code], ymd=ymd, at=r.get('at', '')))

# 출발 변화 (10/8 → 10/9)
CH = []   # 바뀐 편
OUT9 = []
for key, days in RECHK.items():
    code = key.split('-')[1]; reg = REGION[code]
    for ymd in ODAYS:
        r8 = OUT8.get(key, {}).get(ymd, {}); r9 = days.get(ymd, {})
        f8 = {f['flt']: f for f in flights(r8)}; f9 = {f['flt']: f for f in flights(r9)}
        for flt, f in f9.items():
            OUT9.append(dict(f, region=reg, code=code, city=NAME[code], ymd=ymd))
            o = f8.get(flt)
            if o is None:
                continue
            if o['ey'] != f['ey'] or (o['pr'] or 0) != (f['pr'] or 0):
                CH.append({'region': reg, 'city': NAME[code], 'code': code, 'ymd': ymd, 'flt': flt, 'dep': f['dep'], 'ey8': o['ey'], 'ey9': f['ey'], 'pr8': o['pr'], 'pr9': f['pr']})

# CSV
with open(os.path.join(OUT, '2027년10월연휴_대한항공_마일리지_복귀편별_20261009.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['권역', '도시', '공항', '복귀일', '편명', '현지 출발시각', '일반석 잔여(표시 상한 9)', '일반석 마일', '프레스티지 잔여', '프레스티지 마일', '일등석 잔여', '조회 시각'])
    for r in RF:
        w.writerow([r['region'], r['city'], r['code'], r['ymd'], r['flt'], r['dep'], r['ey'], r['ey_m'], '' if r['pr'] is None else r['pr'], r['pr_m'] or '', '' if r['fr'] is None else r['fr'], r['at']])
with open(os.path.join(OUT, '2027년10월연휴_대한항공_출발편_하루뒤변화_20261009.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['권역', '도시', '출발일', '편명', '출발시각', '일반석 10/8', '일반석 10/9', '프레스티지 10/8', '프레스티지 10/9'])
    for c in CH:
        w.writerow([c['region'], c['city'], c['ymd'], c['flt'], c['dep'], c['ey8'], c['ey9'], c['pr8'], c['pr9']])

# 요약
S = {}
for reg in RNAME:
    S[reg] = {}
    for ymd, lab in RDAYS:
        fl = [r for r in RF if r['region'] == reg and r['ymd'] == ymd]
        S[reg][ymd] = {'n': len(fl), 'ey0': sum(1 for r in fl if r['ey'] == 0), 'ey9': sum(1 for r in fl if r['ey'] == 9),
                       'low': [(r['city'], r['flt'], r['dep'], r['ey']) for r in fl if r['ey'] is not None and 0 < r['ey'] < 9],
                       'zero': [(r['city'], r['flt'], r['dep']) for r in fl if r['ey'] == 0],
                       'pr0': sum(1 for r in fl if (r['pr'] or 0) == 0), 'prok': [(r['city'], r['flt'], r['dep'], r['pr']) for r in fl if (r['pr'] or 0) > 0]}
CHS = {'n': len(CH), 'ey_down': [c for c in CH if c['ey9'] is not None and c['ey8'] is not None and c['ey9'] < c['ey8']],
       'ey_up': [c for c in CH if c['ey9'] is not None and c['ey8'] is not None and c['ey9'] > c['ey8']],
       'to_zero': [c for c in CH if c['ey9'] == 0 and c['ey8'] != 0], 'from_zero': [c for c in CH if c['ey8'] == 0 and c['ey9'] != 0],
       'pr_down': [c for c in CH if (c['pr9'] or 0) < (c['pr8'] or 0)], 'pr_up': [c for c in CH if (c['pr9'] or 0) > (c['pr8'] or 0)],
       'n_out9': len(OUT9)}
json.dump({'ret': S, 'change': CHS, 'asof': RASOF}, open(os.path.join(OUT, '_summary_return.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for reg in RNAME:
    for ymd, lab in RDAYS:
        s = S[reg][ymd]; print(reg, lab, {k: (v if not isinstance(v, list) else len(v)) for k, v in s.items()})
print('변화', {k: (v if not isinstance(v, list) else len(v)) for k, v in CHS.items()})


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


# ───────── ① 복귀 격자 (도시 × 10/3·10/4) ─────────
def rgrid(fn, title, sub, codes, when):
    rowh = 46
    H = 300 + len(codes) * rowh + 110
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=32, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, sub, fontsize=19, color=INK2, va='center')
    lx = 40
    for lab, col in (('9석 이상', KE), ('1~8석', MID), ('0석', WARN), ('편 없음·운임 없음', NONE)):
        ax.add_patch(Rectangle((lx, 150), 18, 18, facecolor=col, edgecolor='none'))
        ax.text(lx + 26, 159, lab, fontsize=16, color=INK2, va='center')
        lx += 26 + len(lab) * 15 + 36
    x0 = 250; cw = (W - 40 - x0) / 2
    for j, (ymd, lab) in enumerate(RDAYS):
        ax.text(x0 + cw * j + cw / 2, 215, lab + ' 현지 출발', fontsize=20, color=INK2, ha='center', va='center')
    ax.plot([40, W - 40], [238, 238], color=GRID, lw=1.2)
    y = 262
    for code in codes:
        ax.text(40, y + rowh / 2, NAME[code], fontsize=19, color=INK, va='center')
        for j, (ymd, lab) in enumerate(RDAYS):
            c = RCELL.get((code, ymd), {'state': 'nofl', 'fl': []})
            x = x0 + cw * j + 6
            if c['state'] != 'fl':
                ax.add_patch(Rectangle((x, y + 6), cw - 12, rowh - 12, facecolor='#f2f1ec', edgecolor='none'))
                ax.text(x + (cw - 12) / 2, y + rowh / 2, {'nofare': '운임 없음', 'unopened': '미오픈'}.get(c['state'], '편 없음'), fontsize=14, color=MUTED, ha='center', va='center')
                continue
            n = len(c['fl']); bw = (cw - 12 - 4 * (n - 1)) / n
            for k, r in enumerate(c['fl']):
                col = ey_color(r['ey'])
                ax.add_patch(Rectangle((x + k * (bw + 4), y + 6), bw, rowh - 12, facecolor=col, edgecolor='none'))
                txt = '%s %s' % (r['dep'], '0석' if r['ey'] == 0 else ('%d석' % r['ey'] if r['ey'] < 9 else '9+'))
                ax.text(x + k * (bw + 4) + bw / 2, y + rowh / 2, txt if n <= 4 else (r['dep'] if r['ey'] >= 9 else '%d' % r['ey']), fontsize=13 if n <= 4 else 11,
                        color='white' if col in (KE, WARN) else INK, ha='center', va='center')
        y += rowh
    ax.plot([40, W - 40], [y + 4, y + 4], color=GRID, lw=1.2)
    ax.text(40, y + 30, '칸 하나가 편 하나 · 안의 숫자는 일반석 잔여(9 이상은 9+) · 시각은 현지 출발', fontsize=15, color=MUTED, va='center')
    footer(ax, H, when)
    save(fig, fn)


def when(reg):
    a = RASOF.get(reg, '')
    return a[:16].replace('-', '.') if a else '2026.10.9 밤'


rgrid('return_grid_europe_20261009.png', '유럽 14도시 → 인천, 연휴 복귀 일반석 마일리지', '2027년 10월 3일(일)·4일(월) 현지 출발 · 10/4 편이 열린 날 밤 조회 · 편마다 일반석', EU, when('유럽'))
rgrid('return_grid_asia_20261009.png', '아시아 22도시 → 인천, 연휴 복귀 일반석 마일리지', '2027년 10월 3일(일)·4일(월) 현지 출발 · 10/4 편이 열린 날 밤 조회 · 편마다 일반석', AS, when('아시아'))
rgrid('return_grid_americas_20261009.png', '미주·대양주 16도시 → 인천, 연휴 복귀 일반석', '2027년 10월 3일(일)·4일(월) 현지 출발 · 10/4 편이 열린 날 밤 조회 · 편마다 일반석', AM, when('미주·대양주'))

# ───────── ② 출발편 하루 뒤 변화 카드 ─────────
rows = sorted(CH, key=lambda c: (RNAME.index(c['region']), c['ymd'], c['city']))
H = 260 + max(1, len(rows)) * 40 + 160
fig, ax = canvas(H)
ax.text(40, 62, '출발편, 하루 사이에 바뀐 편', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '인천 출발 10/1~10/3 · 10월 8일 오전 → 10월 9일 밤 · 잔여가 달라진 편만', fontsize=19, color=INK2, va='center')
ax.text(40, 165, '편 %d개 중 바뀐 편 %d개 · 일반석 줄어든 편 %d · 0석이 된 편 %d · 프레스티지 줄어든 편 %d · 늘어난 편 %d' % (
    CHS['n_out9'], CHS['n'], len(CHS['ey_down']), len(CHS['to_zero']), len(CHS['pr_down']), len(CHS['pr_up'])), fontsize=16, color=INK2, va='center')
cols = [(40, '도시'), (300, '출발'), (470, '편'), (640, '일반석 어제→오늘'), (880, '프레스티지')]
for x, t in cols:
    ax.text(x, 215, t, fontsize=17, color=MUTED, va='center')
ax.plot([40, W - 40], [236, 236], color=GRID, lw=1.2)
y = 262
if not rows:
    ax.text(40, y, '바뀐 편 없음', fontsize=18, color=MUTED, va='center'); y += 40
for c in rows:
    ax.text(40, y, c['city'], fontsize=18, color=INK, va='center')
    ax.text(300, y, '10/%d %s' % (int(c['ymd'][6:8]), c['dep']), fontsize=17, color=INK2, va='center')
    ax.text(470, y, c['flt'], fontsize=17, color=INK2, va='center')
    e8 = '-' if c['ey8'] is None else ('9+' if c['ey8'] >= 9 else str(c['ey8'])); e9 = '-' if c['ey9'] is None else ('9+' if c['ey9'] >= 9 else str(c['ey9']))
    col = INK2 if c['ey8'] == c['ey9'] else (WARN if (c['ey9'] or 0) < (c['ey8'] or 0) else GREEN)
    ax.text(640, y, '%s → %s' % (e8, e9), fontsize=18, fontweight='bold', color=col, va='center')
    p8 = c['pr8'] or 0; p9 = c['pr9'] or 0
    pcol = INK2 if p8 == p9 else (WARN if p9 < p8 else GREEN)
    ax.text(880, y, '%d → %d' % (p8, p9), fontsize=18, fontweight='bold', color=pcol, va='center')
    y += 40
ax.plot([40, W - 40], [y - 14, y - 14], color=GRID, lw=1.2)
ax.text(40, y + 12, '빨강 = 줄어듦, 초록 = 늘어남 · 9+는 화면 표시 상한', fontsize=15, color=MUTED, va='center')
footer(ax, H, '2026.10.8 오전 · 2026.10.9 밤')
save(fig, 'out_change_20261009.png')

# ───────── ③ 복귀편 프레스티지 카드 ─────────
H = 1000
fig, ax = canvas(H)
ax.text(40, 62, '복귀편 프레스티지(비즈니스)는 어디에 남았나', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '현지 → 인천, 2027년 10월 3일(일)·4일(월) · 편 단위 · 10/4 편이 열린 날 밤 조회', fontsize=19, color=INK2, va='center')
y = 190
for reg in RNAME:
    n = sum(S[reg][d]['n'] for d, _ in RDAYS); ok = sum(len(S[reg][d]['prok']) for d, _ in RDAYS)
    ax.text(40, y, reg, fontsize=28, fontweight='bold', color=INK, va='center')
    ax.text(1040, y, '%d편 중 %d편에 남음' % (n, ok), fontsize=28, fontweight='bold', color=KE, va='center', ha='right')
    y += 40
    ax.add_patch(Rectangle((40, y), W - 80, 22, facecolor=NONE, edgecolor='none'))
    if ok:
        ax.add_patch(Rectangle((40, y), (W - 80) * ok / n, 22, facecolor=KE, edgecolor='none'))
    y += 44
    tot = collections.OrderedDict()
    for r in RF:
        if r['region'] != reg: continue
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
ax.text(40, y + 4, '도시 뒤 숫자는 「프레스티지 남은 편 / 전체 편」 (10/3·10/4 합)', fontsize=15, color=MUTED, va='center')
footer(ax, H, '2026.10.9 밤')
save(fig, 'return_prestige_20261009.png')
