# -*- coding: utf-8 -*-
"""같은 날 두 번 조회한 결과 비교(새벽 vs 오전) → CSV + 이미지

사용: python compare_runs.py "<출력 폴더>"
앞: data/oz_daily.json, data/ke_live.json   뒤: data/re_oz.json, data/re_ke.json
비교 구간은 10/3~12/16 (10/2 는 조회 당일 출발이라 뒤 조회에서 빠진다).
"""
import sys, os, json, csv, re, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
D = lambda f: json.load(open(os.path.join(HERE, 'data', f), encoding='utf-8'))['res']
oz0, ke0, oz1, ke1 = D('oz_daily.json'), D('ke_live.json'), D('re_oz.json'), D('re_ke.json')
LO, HI = dt.date(2026, 10, 3), dt.date(2026, 12, 16)
DAYS = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1)]
N = len(DAYS)
CITY = {'LHR': '런던', 'CDG': '파리', 'FRA': '프랑크푸르트', 'FCO': '로마', 'BCN': '바르셀로나', 'MAD': '마드리드'}
ROUTES = [('OZ', 'LHR'), ('KE', 'LHR'), ('OZ', 'CDG'), ('KE', 'CDG'), ('OZ', 'FRA'), ('KE', 'FRA'), ('OZ', 'FCO'), ('KE', 'FCO'), ('OZ', 'BCN'), ('KE', 'MAD')]
AIR = {'OZ': '아시아나', 'KE': '대한항공'}


def ke_days(db, key, cab):
    out = set()
    for ymd, v in db[key]['days'].items():
        for f in v.get('flights', []) or []:
            c = f['cab'].get(cab)
            if f.get('segs', 1) == 1 and c and c[0] > 0:
                out.add(dt.datetime.strptime(ymd, '%Y%m%d').date())
    return out


def have(run, air, o, d, cab):
    """cab: 'e' 일반석 / 'b' 비즈니스 → 좌석 있던 날짜 집합"""
    key = o + '-' + d
    if air == 'KE':
        return ke_days(ke0 if run == 0 else ke1, key, 'EY' if cab == 'e' else 'PR')
    if run == 0:
        rec = oz0[key]
        src = rec['marks'] if cab == 'e' else (rec.get('B') or {}).get('days', {})
        extra = rec['marks'] if cab == 'b' else {}
    else:
        rec = oz1[key]
        src = rec['A']['days'] if cab == 'e' else rec.get('B', {}).get('days', {})
        extra = rec['A']['days'] if cab == 'b' else {}
    k = 'E' if cab == 'e' else 'B'
    s = {dt.date.fromisoformat(i) for i, v in src.items() if v.get(k)}
    s |= {dt.date.fromisoformat(i) for i, v in extra.items() if v.get('B')}
    return s


def stamp(run, air, key):
    if air == 'KE':
        ts = sorted(v.get('at', '') for v in (ke0 if run == 0 else ke1)[key]['days'].values() if v.get('at'))
        return ts[0][11:16], ts[-1][11:16]
    if run == 0:
        ts = sorted(m['asOf'] for m in oz0[key]['marks'].values() if m.get('asOf'))
    else:
        ts = sorted(q['asOf'] for p in ('A', 'B') if p in oz1[key] for q in oz1[key][p]['queries'])
    hm = [re.search(r'(\d{2}:\d{2})', t).group(1) for t in ts]
    return hm[0], hm[-1]


def short(dates):
    dates = sorted(dates)
    if not dates:
        return ''
    runs, s, p = [], dates[0], dates[0]
    for x in dates[1:]:
        if x == p + dt.timedelta(days=1):
            p = x
            continue
        runs.append((s, p))
        s = p = x
    runs.append((s, p))
    return ', '.join('%d/%d' % (a.month, a.day) if a == b else ('%d/%d~%d' % (a.month, a.day, b.day) if a.month == b.month else '%d/%d~%d/%d' % (a.month, a.day, b.month, b.day)) for a, b in runs)


rows = [['항공사', '도시', '방향', '등급', '앞 조회 시각', '뒤 조회 시각', '앞: 좌석 있는 날(75일 중)', '뒤: 좌석 있는 날', '새로 열린 날 수', '사라진 날 수', '새로 열린 날짜', '사라진 날짜']]
RES = {}
for air, c in ROUTES:
    for o, d, direc in (('ICN', c, '가는 편'), (c, 'ICN', '오는 편')):
        key = o + '-' + d
        if key not in (oz0 if air == 'OZ' else ke0) or key not in (oz1 if air == 'OZ' else ke1):
            continue
        if air == 'KE' and not ke1[key].get('done'):
            continue   # 뒤 조회가 중간에 끊긴 방향은 비교하지 않는다
        if air == 'OZ' and 'A' not in oz1[key]:
            continue
        t0, t1 = stamp(0, air, key), stamp(1, air, key)
        for cab, cname in (('e', '일반석'), ('b', '비즈니스')):
            if cab == 'b' and air == 'OZ' and 'B' not in oz1[key]:
                continue
            a = {x for x in have(0, air, o, d, cab) if LO <= x <= HI}
            b = {x for x in have(1, air, o, d, cab) if LO <= x <= HI}
            RES[(air, o, d, cab)] = (a, b)
            rows.append([AIR[air], CITY[c], direc, cname, '%s~%s' % t0, '%s~%s' % t1, len(a), len(b), len(b - a), len(a - b), short(b - a), short(a - b)])
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, '유럽_같은날_두번조회_비교.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    csv.writer(f).writerows(rows)
for r in rows[1:]:
    if r[3] == '일반석' or r[8] or r[9] or r[6] or r[7]:
        print(' | '.join(str(x) for x in r))

# ───────── 이미지 ─────────
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF, INK, INK2, MUTED, GRID, AXIS, NONE = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7', '#e6e4dd'
COL = {'OZ': '#eb6834', 'KE': '#2a78d6'}
W = 1080
all0 = sorted(t for r in rows[1:] for t in r[4].split('~'))
all1 = sorted(t for r in rows[1:] for t in r[5].split('~'))
T0, T1 = '%s~%s' % (all0[0], all0[-1]), '%s~%s' % (all1[0], all1[-1])


def card(fn, cab, title):
    X0, CW = 248, 8.7
    SW = CW * N
    cities = []
    for air, c in ROUTES:
        nm = CITY[c]
        if nm not in cities:
            cities.append(nm)
    blocks = [(nm, [(air, c) for air, c in ROUTES if CITY[c] == nm]) for nm in cities]
    blocks = [(nm, b) for nm, b in blocks if any((air, o, d, cab) in RES for air, c in b for o, d in (('ICN', c), (c, 'ICN')))]
    H = 268 + sum(46 + 24 + sum(1 for air, c in b for o, d in (('ICN', c), (c, 'ICN')) if (air, o, d, cab) in RES) * 36 + 30 for _, b in blocks) + 114
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=SURF)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis('off')
    ax.text(40, 62, title, fontsize=36, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '10월 2일 새벽(%s)과 오전(%s), 같은 화면을 두 번 조회' % (T0, T1), fontsize=21, color=INK2, va='center')
    x = 40
    for fc, ec, lab, wd in ((COL['OZ'], 'none', '아시아나', 96), (COL['KE'], 'none', '대한항공', 96), (INK, 'none', '오전에 새로 열린 날', 218), (SURF, INK, '오전에 사라진 날', 192), (NONE, 'none', '좌석 없음', 0)):
        ax.add_patch(Rectangle((x, 157), 22, 22, facecolor=fc, edgecolor=ec, lw=1.6 if ec != 'none' else 0))
        ax.text(x + 30, 168, lab, fontsize=17, color=INK2, va='center')
        x += 30 + wd + 14
    ax.text(X0 + SW + 12, 228, '오전 기준', fontsize=15, color=MUTED, va='center')
    ax.text(X0 + SW + 12, 248, '(새로 / 사라짐)', fontsize=15, color=MUTED, va='center')
    y = 268
    for nm, b in blocks:
        ax.text(40, y + 22, '인천 ↔ ' + nm, fontsize=28, fontweight='bold', color=INK, va='center')
        for j, day in enumerate(DAYS):
            if day.day == 1 or j == 0:
                ax.text(X0 + j * CW, y + 56, '%d월' % day.month, fontsize=15, color=MUTED, va='center')
        ry = y + 70
        for direc_i, direc in enumerate(('가는 편', '오는 편')):
            for air, c in b:
                o, d = ('ICN', c) if direc_i == 0 else (c, 'ICN')
                if (air, o, d, cab) not in RES:
                    continue
                a0, a1 = RES[(air, o, d, cab)]
                ax.text(40, ry + 14, direc + ' ' + AIR[air], fontsize=19, color=INK, va='center')
                for j, day in enumerate(DAYS):
                    if day in a1 and day in a0:
                        fc, ec, lw = COL[air], 'none', 0
                    elif day in a1:
                        fc, ec, lw = INK, 'none', 0
                    elif day in a0:
                        fc, ec, lw = SURF, INK, 1.3
                    else:
                        fc, ec, lw = NONE, 'none', 0
                    ax.add_patch(Rectangle((X0 + j * CW, ry + 2), CW - 1.3, 25, facecolor=fc, edgecolor=ec, lw=lw))
                    if day.day == 1:
                        ax.plot([X0 + j * CW - 0.8, X0 + j * CW - 0.8], [ry, ry + 29], color=AXIS, lw=1)
                ax.text(X0 + SW + 12, ry + 14, '%d일' % len(a1), fontsize=21, color=INK, va='center', fontweight='bold')
                ax.text(X0 + SW + 80, ry + 14, '+%d / -%d' % (len(a1 - a0), len(a0 - a1)), fontsize=17, color=INK2, va='center')
                ry += 36
        y = ry + 30
        ax.plot([40, W - 40], [y - 16, y - 16], color=GRID, lw=1)
    ax.text(40, H - 86, '75일(2026.10.3~12.16 출발) 기준 · 10월 2일 출발편은 오전 조회에서 빠져 비교에서 뺐음', fontsize=17, color=MUTED, va='center')
    ax.text(40, H - 58, '자료: 아시아나항공·대한항공 마일리지 예매 화면 직접 조회 (2026.10.2)', fontsize=17, color=MUTED, va='center')
    ax.text(40, H - 30, '성인 1명 편도 · 직항편 · 좌석은 수시로 바뀌어 조회 시점의 기록임', fontsize=17, color=MUTED, va='center')
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', H)


card('eu_change_economy.png', 'e', '7시간 사이 달라진 일반석 좌석')
card('eu_change_business.png', 'b', '7시간 사이 달라진 비즈니스 좌석')
