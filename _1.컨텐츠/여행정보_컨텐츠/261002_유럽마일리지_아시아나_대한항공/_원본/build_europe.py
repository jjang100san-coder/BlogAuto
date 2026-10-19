# -*- coding: utf-8 -*-
"""유럽 마일리지 좌석(아시아나·대한항공 실시간 조회) → CSV 3종 + 블로그용 이미지

사용: python build_europe.py "<출력 폴더>"
입력: data/oz_daily.json (아시아나, 날짜별 클릭), data/ke_live.json (대한항공, 하루 1회 조회)
"""
import sys, os, json, csv, re, collections, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
LO, HI = dt.date(2026, 10, 2), dt.date(2026, 12, 16)
DAYS = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1)]
N = len(DAYS)
WD = '월화수목금토일'
CITIES = [('LHR', '런던'), ('CDG', '파리'), ('FRA', '프랑크푸르트'), ('FCO', '로마'), ('MXP', '밀라노'),
          ('BCN', '바르셀로나'), ('PRG', '프라하'), ('IST', '이스탄불'), ('AMS', '암스테르담'), ('MAD', '마드리드')]
CNAME = dict(CITIES)
AIR = {'OZ': '아시아나', 'KE': '대한항공'}
oz = json.load(open(os.path.join(HERE, 'data', 'oz_daily.json'), encoding='utf-8'))['res']
ke = json.load(open(os.path.join(HERE, 'data', 'ke_live.json'), encoding='utf-8'))['res']


KE_LISTED = {}  # 대한항공 공개 달력(전날 밤 갱신): 편이 뜬 날
_p = os.path.join(HERE, 'data', 'ke_pub_europe.json')
if os.path.exists(_p):
    for _k, _mm in json.load(open(_p, encoding='utf-8')).items():
        KE_LISTED[_k] = {f['departureDate'] for _v in _mm.values() for f in _v.get('flightList', []) if f.get('flightDetailList')}


def has(air, o, d):
    return (o + '-' + d) in (oz if air == 'OZ' else ke)


def oz_seat(txt):
    """예매 화면 칸 문구 → (있음?, 마일, 비고)"""
    if txt is None:
        return None, '', ''
    m = re.search(r'([\d,]+)\s*마일', txt)
    if m:
        return True, m.group(1).replace(',', ''), ('할인' if '할인' in txt else '')
    return False, '', txt


def day_info(air, o, d, day):
    """→ dict(e, b: 'Y' 있음 / 'N' 없음 / 'X' 편 없음 / '?' 미수집, flights:[...], asof)"""
    key = o + '-' + d
    if air == 'KE':
        v = ke[key]['days'].get(day.strftime('%Y%m%d'))
        if v is None or v.get('retry') or 'err' in v:
            return {'e': '?', 'b': '?', 'flights': [], 'asof': ''}
        fl = [f for f in v.get('flights', []) if f.get('segs', 1) == 1]
        if not fl:
            # 편 내역 없이 온 응답(빈 목록·ERT.7190): 공개 달력에 그날 편이 있으면 '좌석 없음', 없으면 '편 없음'
            st = 'N' if day.strftime('%Y%m%d') in KE_LISTED.get(key, set()) else 'X'
            return {'e': st, 'b': st, 'flights': [], 'asof': v.get('at', '')}
        out = []
        for f in fl:
            ey, pr, fr = f['cab'].get('EY'), f['cab'].get('PR'), f['cab'].get('FR')
            out.append({'flt': f['flt'], 'dep': f['dep'][8:10] + ':' + f['dep'][10:12], 'dur': f['dur'].replace(':', '시간 ') + '분',
                        'e': None if ey is None else ey[0] > 0, 'eseat': '' if ey is None else ey[0], 'emile': '' if ey is None else ey[2],
                        'b': None if pr is None else pr[0] > 0, 'bseat': '' if pr is None else pr[0], 'bmile': '' if pr is None else pr[2],
                        'f': None if fr is None else fr[0] > 0, 'note': '공동운항편' if re.match(r'KE[5-9]\d{3}$', f['flt']) else ''})
        return {'e': 'Y' if any(x['e'] for x in out) else 'N', 'b': 'Y' if any(x['b'] for x in out) else 'N', 'flights': out, 'asof': v.get('at', '')}
    rec = oz[key]
    iso = day.isoformat()
    m = rec['marks'].get(iso)
    if m is None:
        return {'e': '?', 'b': '?', 'flights': [], 'asof': ''}
    bdays = (rec.get('B') or {}).get('days', {})
    b = 'Y' if (bdays.get(iso, {}).get('B') or m['B']) else 'N'
    e = 'Y' if m['E'] else 'N'
    out = []
    drec = rec['days'].get(iso) or {}
    for r in (drec.get('rows') or []):
        es, em, en = oz_seat(r['eco'])
        bs, bm, bn = oz_seat(r['biz'])
        out.append({'flt': r['flt'], 'dep': r['dep'], 'dur': ' '.join((r.get('dur') or '').split()), 'e': es, 'eseat': '', 'emile': em,
                    'b': bs, 'bseat': '', 'bmile': bm, 'f': None, 'note': en if en == '할인' else ''})
    asof = (drec.get('asOf') or m.get('asOf', '')).replace(' 기준', '').replace('.', '-')
    return {'e': e, 'b': b, 'flights': out, 'asof': asof}


CACHE = {}


def info(air, o, d):
    k = (air, o, d)
    if k not in CACHE:
        CACHE[k] = {day: day_info(air, o, d, day) for day in DAYS}
    return CACHE[k]


def days_of(air, o, d, cab, state='Y'):
    return [day for day in DAYS if info(air, o, d)[day][cab] == state]


def short(dates):
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
    out = []
    for a, b in runs:
        if a == b:
            out.append('%d/%d' % (a.month, a.day))
        elif a.month == b.month:
            out.append('%d/%d~%d' % (a.month, a.day, b.day))
        else:
            out.append('%d/%d~%d/%d' % (a.month, a.day, b.month, b.day))
    return ', '.join(out)


# ───────────────────────── CSV ─────────────────────────
ST = {'Y': '있음', 'N': '없음', 'X': '편 없음', '?': '미수집'}
ST_OZ = {'Y': '있음', 'N': '없음(편 없는 날 포함)', 'X': '편 없음', '?': '미수집'}


def seat_txt(air, v, seat):
    if v is None:
        return '표시 없음'
    if not v:
        return '매진'
    if air == 'KE':
        return '9석 이상' if seat == 9 else '%s석' % seat
    return '있음'


def write_csv():
    raw = [['항공사', '조회시각', '출발일', '요일', '도시', '방향', '출발공항', '도착공항', '편명', '출발시각', '소요시간',
            '일반석', '일반석_마일', '비즈니스', '비즈니스_마일', '일등석', '비고']]
    daily = [['항공사', '도시', '방향', '출발공항', '도착공항', '출발일', '요일', '편수', '일반석', '비즈니스', '일반석_최저마일']]
    summ = [['항공사', '도시', '방향', '출발공항', '도착공항', '기간_일수', '편_있는_날', '일반석_있는_날', '비즈니스_있는_날', '미수집_날',
             '일반석_없는_날짜(대한항공은 편 있는 날만, 아시아나는 편 없는 날 포함)', '비즈니스_있는_날짜', '조회_시작', '조회_끝']]
    for code, nm in CITIES:
        for o, d, direc in (('ICN', code, '가는 편'), (code, 'ICN', '오는 편')):
            for air in ('OZ', 'KE'):
                if not has(air, o, d):
                    continue
                inf = info(air, o, d)
                asofs = sorted(x['asof'] for x in inf.values() if x['asof'])
                for day in DAYS:
                    x = inf[day]
                    ds, wd = day.isoformat(), WD[day.weekday()]
                    miles = [int(f['emile']) for f in x['flights'] if f['e'] and str(f['emile']).isdigit()]
                    daily.append([AIR[air], nm, direc, o, d, ds, wd, len(x['flights']) if x['flights'] else ('' if x['e'] != 'X' else 0),
                                  (ST_OZ if air == 'OZ' else ST)[x['e']], (ST_OZ if air == 'OZ' else ST)[x['b']], min(miles) if miles else ''])
                    if x['flights']:
                        for f in x['flights']:
                            raw.append([AIR[air], x['asof'], ds, wd, nm, direc, o, d, f['flt'], f['dep'], f['dur'],
                                        seat_txt(air, f['e'], f['eseat']), f['emile'], seat_txt(air, f['b'], f['bseat']), f['bmile'],
                                        '' if f['f'] is None else ('있음' if f['f'] else '매진'), f['note']])
                    elif x['e'] == 'N':
                        raw.append([AIR[air], x['asof'], ds, wd, nm, direc, o, d, '', '', '', '좌석없음', '', ST[x['b']], '', '',
                                    '달력에 좌석없음으로 표시(편별 내역이 열리지 않아 편이 없는 날과 구분 안 됨)' if air == 'OZ' else '그날 편은 있으나 보너스 좌석 응답 없음'])
                    elif x['e'] == 'Y' and air == 'OZ':
                        raw.append([AIR[air], x['asof'], ds, wd, nm, direc, o, d, '', '', '', '있음', '', ST[x['b']], '', '', '달력 표시만 수집(편별 내역 미수집)'])
                e, b = days_of(air, o, d, 'e'), days_of(air, o, d, 'b')
                listed = [day for day in DAYS if inf[day]['e'] in ('Y', 'N')]
                summ.append([AIR[air], nm, direc, o, d, N, len(listed) if air == 'KE' else '구분 불가', len(e), len(b), len(days_of(air, o, d, 'e', '?')),
                             short(days_of(air, o, d, 'e', 'N')), short(b), asofs[0] if asofs else '', asofs[-1] if asofs else ''])
    for fn, rows in (('유럽_마일리지좌석_편별_raw.csv', raw), ('유럽_마일리지좌석_일별.csv', daily), ('유럽_마일리지좌석_노선요약.csv', summ)):
        with open(os.path.join(OUT, fn), 'w', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerows(rows)
        print(fn, len(rows) - 1, '행')
    return summ


# ───────────────────────── 이미지 ─────────────────────────
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF, INK, INK2, MUTED, GRID, AXIS, NONE = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7', '#e6e4dd'
COL = {'OZ': '#eb6834', 'KE': '#2a78d6'}
W = 1080


def span_txt():
    ts = []
    for air in ('OZ', 'KE'):
        for code, _ in CITIES:
            for o, d in (('ICN', code), (code, 'ICN')):
                if has(air, o, d):
                    ts += [x['asof'] for x in info(air, o, d).values() if x['asof']]
    hm = sorted(re.search(r'(\d{2}:\d{2})', t).group(1) for t in ts if re.search(r'\d{2}:\d{2}', t))
    return '2026.10.2 %s~%s' % (hm[0], hm[-1]) if hm else '2026.10.2'


def canvas(h):
    fig = plt.figure(figsize=(W / 100, h / 100), dpi=100, facecolor=SURF)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis('off')
    return fig, ax


def footer(ax, h):
    ax.text(40, h - 58, '자료: 아시아나항공·대한항공 마일리지 예매 화면 직접 조회 (%s)' % span_txt(), fontsize=17, color=MUTED, va='center')
    ax.text(40, h - 30, '성인 1명 편도 · 직항편 · 좌석은 수시로 바뀌어 조회 시점의 기록임', fontsize=17, color=MUTED, va='center')


def footer3(ax, h):
    ax.text(40, h - 86, '아시아나 화면은 좌석 없는 날과 편 없는 날을 구분해 주지 않아 둘 다 회색으로 표시', fontsize=17, color=MUTED, va='center')
    footer(ax, h)


def legend(ax, y, extra=True):
    x = 40
    items = [(COL['OZ'], '아시아나 있음', 150, None), (COL['KE'], '대한항공 있음', 150, None), (NONE, '좌석 없음', 110, None)]
    if extra:
        items.append((SURF, '편 없는 날(대한항공만 구분)', 0, AXIS))
    for c, lab, wd, edge in items:
        ax.add_patch(Rectangle((x, y - 11), 22, 22, facecolor=c, edgecolor=edge if edge else 'none', lw=1))
        ax.text(x + 30, y, lab, fontsize=18, color=INK2, va='center')
        x += 30 + wd + 24


def save(fig, fn, h):
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF)
    plt.close(fig)
    print(fn, W, 'x', h)


def overview(fn, outbound):
    RH = 108
    H = 250 + RH * len(CITIES) + 96
    fig, ax = canvas(H)
    ax.text(40, 62, '유럽 일반석 마일리지 좌석 · ' + ('인천 출발' if outbound else '인천 도착'), fontsize=38, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '합병 전 76일 (2026.10.2~12.16 출발) 가운데 좌석이 있던 날', fontsize=22, color=INK2, va='center')
    x = 40
    for air in ('OZ', 'KE'):
        ax.add_patch(Rectangle((x, 160), 24, 24, facecolor=COL[air], edgecolor='none'))
        ax.text(x + 34, 172, AIR[air], fontsize=21, color=INK2, va='center')
        x += 170
    X0, BW = 372, 530
    for t in (0, 38, 76):
        xx = X0 + BW * t / N
        ax.plot([xx, xx], [222, 250 + RH * len(CITIES) - 22], color=GRID, lw=1)
        ax.text(xx, 208, '%d일' % t, fontsize=16, color=MUTED, ha='center', va='center')
    y = 236
    for code, nm in CITIES:
        o, d = ('ICN', code) if outbound else (code, 'ICN')
        ax.text(X0 - 18, y + 40, ('인천 → ' + nm) if outbound else (nm + ' → 인천'), fontsize=22, fontweight='bold', color=INK, va='center', ha='right')
        for j, air in enumerate(('OZ', 'KE')):
            yy = y + 6 + j * 38
            if not has(air, o, d):
                ax.text(X0, yy + 14, AIR[air] + ' 노선 없음' if not (air == 'KE' and code == 'BCN') else '대한항공 이 기간 편 없음', fontsize=18, color=MUTED, va='center')
                continue
            n = len(days_of(air, o, d, 'e'))
            ax.add_patch(Rectangle((X0, yy), BW, 30, facecolor='#efeee9', edgecolor='none'))
            if n:
                ax.add_patch(Rectangle((X0, yy), max(BW * n / N, 4), 30, facecolor=COL[air], edgecolor='none'))
            ax.text(X0 + BW + 16, yy + 15, '%d일' % n, fontsize=24, color=INK, va='center', fontweight='bold')
        y += RH
        ax.plot([40, W - 40], [y - 14, y - 14], color=GRID, lw=1)
    footer(ax, H)
    save(fig, fn, H)


def strips(fn, title, codes):
    X0, CW = 248, 8.6
    SW = CW * N
    H = 232 + len(codes) * (46 + 24 + 4 * 36 + 30) + 114
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=38, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '합병 전 76일 (2026.10.2~12.16 출발) · 일반석 마일리지 좌석이 있던 날', fontsize=22, color=INK2, va='center')
    legend(ax, 168)
    ax.text(X0 + SW + 14, 212, '76일 중', fontsize=16, color=MUTED, va='center')
    y = 232
    for code in codes:
        ax.text(40, y + 22, '인천 ↔ ' + CNAME[code], fontsize=28, fontweight='bold', color=INK, va='center')
        for j, day in enumerate(DAYS):
            if day.day == 1 or j == 0:
                ax.text(X0 + j * CW, y + 56, '%d월' % day.month, fontsize=15, color=MUTED, va='center')
        ry = y + 70
        for o, d, direc in (('ICN', code, '가는 편'), (code, 'ICN', '오는 편')):
            for air in ('OZ', 'KE'):
                ax.text(40, ry + 14, direc + ' ' + AIR[air], fontsize=19, color=INK, va='center')
                if not has(air, o, d):
                    ax.text(X0, ry + 14, '노선 없음' if not (air == 'KE' and code == 'BCN') else '이 기간 편 없음', fontsize=17, color=MUTED, va='center')
                    ry += 36
                    continue
                inf = info(air, o, d)
                for j, day in enumerate(DAYS):
                    st = inf[day]['e']
                    fc, ec = (COL[air], 'none') if st == 'Y' else (NONE, 'none') if st == 'N' else (SURF, GRID)
                    ax.add_patch(Rectangle((X0 + j * CW, ry + 2), CW - 1.2, 25, facecolor=fc, edgecolor=ec, lw=0.5))
                    if day.day == 1:
                        ax.plot([X0 + j * CW - 0.8, X0 + j * CW - 0.8], [ry, ry + 29], color=AXIS, lw=1)
                ax.text(X0 + SW + 14, ry + 14, '%d일' % len(days_of(air, o, d, 'e')), fontsize=22, color=INK, va='center', fontweight='bold')
                ry += 36
        y = ry + 30
        ax.plot([40, W - 40], [y - 16, y - 16], color=GRID, lw=1)
    footer3(ax, H)
    save(fig, fn, H)


def wrap(s, n):
    out, cur = [], ''
    for part in s.split(', '):
        if len(cur) + len(part) + 2 > n and cur:
            out.append(cur + ',')
            cur = part
        else:
            cur = (cur + ', ' + part) if cur else part
    return out + [cur] if cur else out


def business(fn):
    blocks, H = [], 196
    for code, nm in CITIES:
        lines = []
        for air in ('OZ', 'KE'):
            for o, d, direc in (('ICN', code, '가는 편'), (code, 'ICN', '오는 편')):
                if not has(air, o, d):
                    continue
                b = days_of(air, o, d, 'b')
                lines.append((air, direc, len(b), wrap(short(b), 44) if b else []))
        blocks.append((nm, lines))
        H += 50 + sum(34 + max(0, len(w) - 1) * 26 for _, _, _, w in lines) + 22
    H += 86
    fig, ax = canvas(H)
    ax.text(40, 62, '유럽 비즈니스 마일리지 좌석', fontsize=38, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '합병 전 76일 (2026.10.2~12.16 출발) 가운데 좌석이 있던 날과 그 날짜', fontsize=22, color=INK2, va='center')
    y = 168
    for nm, lines in blocks:
        ax.text(40, y + 20, '인천 ↔ ' + nm, fontsize=26, fontweight='bold', color=INK, va='center')
        y += 50
        for air, direc, n, w in lines:
            ax.add_patch(Rectangle((40, y + 4), 16, 16, facecolor=COL[air], edgecolor='none'))
            ax.text(66, y + 12, AIR[air] + ' ' + direc, fontsize=19, color=INK2, va='center')
            ax.text(300, y + 12, '%d일' % n, fontsize=21, color=INK, va='center', fontweight='bold')
            for i, ln in enumerate(w):
                ax.text(380, y + 12 + i * 26, ln, fontsize=18, color=INK2, va='center')
            y += 34 + max(0, len(w) - 1) * 26
        y += 22
        ax.plot([40, W - 40], [y - 12, y - 12], color=GRID, lw=1)
    footer(ax, H)
    save(fig, fn, H)


def flights_card(fn):
    """도시별 편명·출발 시각(가장 자주 나온 시각)"""
    rows = []
    for code, nm in CITIES:
        for o, d, direc in (('ICN', code, '가는 편'), (code, 'ICN', '오는 편')):
            cell = {}
            for air in ('OZ', 'KE'):
                if not has(air, o, d):
                    cell[air] = ['노선 없음' if not (air == 'KE' and code == 'BCN') else '이 기간 편 없음']
                    continue
                c = collections.defaultdict(collections.Counter)
                for x in info(air, o, d).values():
                    for f in x['flights']:
                        c[f['flt']][f['dep']] += 1
                cell[air] = ['%s  %s 출발' % (flt, ' / '.join(t for t, _ in cc.most_common(2))) for flt, cc in sorted(c.items())] or ['편별 내역 없음']
            rows.append((nm, direc, cell))
    H = 232 + sum(max(len(c['OZ']), len(c['KE'])) * 30 + 22 for _, _, c in rows) + len(CITIES) * 14 + 86
    fig, ax = canvas(H)
    ax.text(40, 62, '유럽 노선 편명과 출발 시각', fontsize=38, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '2026.10.2~12.16 출발편 · 마일리지 예매 화면에 뜬 직항편', fontsize=22, color=INK2, va='center')
    ax.text(330, 180, '아시아나', fontsize=22, color=INK, va='center', fontweight='bold')
    ax.text(700, 180, '대한항공', fontsize=22, color=INK, va='center', fontweight='bold')
    ax.plot([40, W - 40], [206, 206], color=AXIS, lw=1)
    y = 222
    for i, (nm, direc, cell) in enumerate(rows):
        if direc == '가는 편':
            ax.text(40, y + 15, nm, fontsize=22, fontweight='bold', color=INK, va='center')
        ax.text(238, y + 15, direc, fontsize=17, color=MUTED, va='center')
        for air, x0 in (('OZ', 330), ('KE', 700)):
            for k, ln in enumerate(cell[air]):
                ax.text(x0, y + 15 + k * 30, ln, fontsize=19, color=INK2 if '없음' not in ln else MUTED, va='center')
        y += max(len(cell['OZ']), len(cell['KE'])) * 30 + 22
        if direc == '오는 편':
            ax.plot([40, W - 40], [y - 6, y - 6], color=GRID, lw=1)
            y += 14
    footer(ax, H)
    save(fig, fn, H)


def thumb(fn, code='CDG'):
    H = 1080
    fig, ax = canvas(H)
    ax.text(60, 92, '유럽 마일리지 일반석', fontsize=58, fontweight='bold', color=INK, va='center')
    ax.text(60, 168, '합병 전 76일 · 인천 → %s' % CNAME[code], fontsize=32, color=INK2, va='center')
    y = 250
    for air in ('OZ', 'KE'):
        inf = info(air, 'ICN', code)
        n = len(days_of(air, 'ICN', code, 'e'))
        ax.text(60, y + 40, AIR[air], fontsize=44, fontweight='bold', color=INK, va='center')
        ax.text(W - 60, y + 40, '%d일' % n, fontsize=84, fontweight='bold', color=INK, va='center', ha='right')
        gx, gy, cs = 60, y + 110, 48.5
        for i, day in enumerate(DAYS):
            cx, cy = gx + (i % 20) * cs, gy + (i // 20) * cs
            st = inf[day]['e']
            fc, ec = (COL[air], 'none') if st == 'Y' else (NONE, 'none') if st == 'N' else (NONE, 'none') if air == 'OZ' else (SURF, AXIS)
            ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=fc, edgecolor=ec, lw=1.2))
        y += 110 + 4 * cs + 56
    ax.text(60, 1020, '칸 하나가 하루 · 색칠한 칸이 좌석이 있던 날', fontsize=24, color=MUTED, va='center')
    save(fig, fn, H)


if __name__ == '__main__':
    summ = write_csv()
    for r in summ[1:]:
        print(' ', r[0], r[1], r[2], '| 편 %s 일반석 %s 비즈 %s 미수집 %s' % (r[6], r[7], r[8], r[9]))
    if '--csv-only' not in sys.argv:
        thumb('eu_thumb.png')
        overview('eu_overview_out.png', True)
        overview('eu_overview_in.png', False)
        strips('eu_strip_1.png', '유럽 일반석 좌석 달력 ①', [c for c, _ in CITIES[:5]])
        strips('eu_strip_2.png', '유럽 일반석 좌석 달력 ②', [c for c, _ in CITIES[5:]])
        business('eu_business.png')
        flights_card('eu_flights.png')
