# -*- coding: utf-8 -*-
"""2026-10-12 아침 관찰 — 「9시 정각 거부 → 9시 1분 오픈 → 10분 안 전체 노선」 글의 카드 이미지·CSV·요약
사용: python build_open0901.py "<글 폴더>"
입력: 261008 폴더 base data 의 ke_live_2027holiday_1007_full_1012.json, projects data 의 holiday_open_watch_ui_20271007.json / 20271006.json / 20271005 API 기록
"""
import sys, os, json, csv, collections
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\user\Desktop\Blog\_1.컨텐츠\여행정보_컨텐츠\261008_2027_10월연휴_마일리지\base data\ke_live_2027holiday_1007_full_1012.json"
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e6e4dd'
KE = '#2a78d6'; NONE = '#e6e4dd'; WARN = '#d9534f'; MID = '#f0ad4e'; GREEN = '#3a9d5d'
W = 1080
NAME = {'FUK': '후쿠오카', 'KIX': '오사카', 'NRT': '도쿄 나리타', 'HND': '도쿄 하네다', 'CXR': '나트랑', 'CTS': '삿포로', 'PQC': '푸꾸옥', 'DAD': '다낭', 'PVG': '상하이', 'OKA': '오키나와', 'TPE': '타이베이', 'NGO': '나고야', 'HKG': '홍콩', 'BKK': '방콕', 'DPS': '발리', 'GUM': '괌', 'HAN': '하노이', 'CEB': '세부', 'SGN': '호치민', 'SIN': '싱가포르', 'TAO': '칭다오', 'HKT': '푸켓',
        'LHR': '런던', 'CDG': '파리', 'FRA': '프랑크푸르트', 'FCO': '로마', 'MXP': '밀라노', 'BCN': '바르셀로나', 'PRG': '프라하', 'IST': '이스탄불', 'AMS': '암스테르담', 'MAD': '마드리드', 'VIE': '빈', 'ZRH': '취리히', 'BUD': '부다페스트', 'LIS': '리스본',
        'LAX': 'LA', 'JFK': '뉴욕', 'SFO': '샌프란시스코', 'HNL': '호놀룰루', 'SEA': '시애틀', 'LAS': '라스베이거스', 'YVR': '밴쿠버', 'YYZ': '토론토', 'ORD': '시카고', 'ATL': '애틀랜타', 'DFW': '댈러스', 'BOS': '보스턴', 'IAD': '워싱턴', 'SYD': '시드니', 'BNE': '브리즈번', 'AKL': '오클랜드'}
AS = ['FUK', 'KIX', 'NRT', 'HND', 'CTS', 'NGO', 'OKA', 'CXR', 'DAD', 'PQC', 'HAN', 'SGN', 'BKK', 'HKT', 'DPS', 'CEB', 'SIN', 'PVG', 'TAO', 'TPE', 'HKG', 'GUM']
EU = ['LHR', 'CDG', 'FRA', 'AMS', 'FCO', 'MXP', 'BCN', 'MAD', 'LIS', 'PRG', 'VIE', 'ZRH', 'BUD', 'IST']
AM = ['LAX', 'SFO', 'SEA', 'LAS', 'JFK', 'BOS', 'IAD', 'ORD', 'ATL', 'DFW', 'HNL', 'YVR', 'YYZ', 'SYD', 'BNE', 'AKL']
REG = {}
for c in AS: REG[c] = '아시아'
for c in EU: REG[c] = '유럽'
for c in AM: REG[c] = '미주·대양주'
RN = ['아시아', '유럽', '미주·대양주']
YMD = '20271007'

L = json.load(open(SRC, encoding='utf-8'))
F = []
CELL = {}
for key, days in L.items():
    r = days[YMD]; o, d = key.split('-'); code = d if o == 'ICN' else o
    fl = [f for f in r.get('flights', []) if f.get('segs', 1) == 1]
    state = 'fl' if fl else ('nofare' if r.get('code') == 'ERT.7190' else 'nofl')
    rows = []
    for f in fl:
        ey = f['cab'].get('EY') or [None, None, None]; pr = f['cab'].get('PR') or [None, None, None]
        rec = {'key': key, 'dir': 'out' if o == 'ICN' else 'ret', 'code': code, 'city': NAME[code], 'region': REG[code], 'flt': f['flt'], 'dep': f['dep'][8:10] + ':' + f['dep'][10:12], 'ey': ey[0], 'ey_m': ey[2], 'pr': pr[0], 'pr_m': pr[2], 'at': r.get('at', '')}
        F.append(rec); rows.append(rec)
    CELL[key] = {'state': state, 'fl': rows, 'at': r.get('at', '')}

with open(os.path.join(OUT, '2027년10월7일_오픈10분_대한항공_편별_20261012.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['권역', '도시', '방향', '편명', '출발시각', '일반석 잔여(상한 9)', '일반석 마일', '프레스티지 잔여', '프레스티지 마일', '조회 시각'])
    for r in F:
        w.writerow([r['region'], r['city'], '인천→' if r['dir'] == 'out' else '→인천', r['flt'], r['dep'], r['ey'], r['ey_m'], '' if r['pr'] is None else r['pr'], r['pr_m'] or '', r['at']])

S = {}
for reg in RN:
    fl = [r for r in F if r['region'] == reg]
    S[reg] = {'n': len(fl), 'ey0': sum(1 for r in fl if r['ey'] == 0), 'ey9': sum(1 for r in fl if r['ey'] == 9),
              'low': [(r['city'], r['flt'], r['ey']) for r in fl if r['ey'] is not None and 0 < r['ey'] < 9],
              'ey0_list': [(r['city'], r['flt'], r['dep'], r['dir']) for r in fl if r['ey'] == 0],
              'pr0': sum(1 for r in fl if (r['pr'] or 0) == 0), 'prok': [(r['city'], r['flt'], r['dep'], r['pr'], r['dir']) for r in fl if (r['pr'] or 0) > 0],
              'first': min((r['at'] for r in fl), default=''), 'last': max((r['at'] for r in fl), default=''),
              'nofl': sum(1 for k, c in CELL.items() if REG[k.replace('ICN-', '').replace('-ICN', '')] == reg and c['state'] == 'nofl'),
              'nofare': sum(1 for k, c in CELL.items() if REG[k.replace('ICN-', '').replace('-ICN', '')] == reg and c['state'] == 'nofare')}
# 분 단위 관찰 기록
W1 = json.load(open(os.path.join(HERE, 'data', 'holiday_open_watch_ui_20271007.json'), encoding='utf-8'))
TL = [(k, v.get('mark'), v.get('result', '')[:60]) for k, v in sorted(W1.items())]
json.dump({'summary': S, 'timeline': TL}, open(os.path.join(OUT, '_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for reg in RN:
    print(reg, {k: (v if not isinstance(v, list) else len(v)) for k, v in S[reg].items()})
print('timeline', TL)


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


# ① 9시 타임라인 카드 — 사흘(10/10·10/11·10/12)의 9시 전후
H = 980
fig, ax = canvas(H)
ax.text(40, 62, '아침 9시, 마일리지 좌석이 열리는 순간', fontsize=36, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '같은 방법으로 사흘을 지켜본 기록 · 조회 날짜 + 360일이 그날 열린다', fontsize=19, color=INK2, va='center')
days = [
    ('10월 10일 (토)', '열리는 날짜 2027-10-05', [('08:50', '12방향 전부 미오픈', NONE), ('08:51', '접근 거부 — 2시간 뒤 풀림', WARN), ('10:55', '정상 조회', KE)]),
    ('10월 11일 (일)', '열리는 날짜 2027-10-06', [('08:50~08:59', '달력에서 날짜가 안 눌림 = 미오픈', NONE), ('09:00:25', '첫 조회 접근 거부', WARN), ('12:15', '정상 조회 (다음 날짜는 여전히 미오픈)', KE)]),
    ('10월 12일 (월)', '열리는 날짜 2027-10-07', [('08:58', '달력에서 날짜가 안 눌림 = 미오픈', NONE), ('09:00:18', '접근 거부', WARN), ('09:01:16', '열림 — 파리 편이 바로 보임', KE), ('09:01~09:11', '52도시 왕복 104방향 전부 조회', GREEN)]),
]
y = 175
for title, sub, evs in days:
    ax.text(40, y, title, fontsize=26, fontweight='bold', color=INK, va='center')
    ax.text(300, y, sub, fontsize=18, color=MUTED, va='center')
    y += 44
    for t, lab, col in evs:
        ax.add_patch(Rectangle((60, y - 11), 14, 22, facecolor=col, edgecolor='none'))
        ax.text(90, y, t, fontsize=19, fontweight='bold', color=INK, va='center')
        ax.text(300, y, lab, fontsize=19, color=INK2, va='center')
        y += 36
    y += 22
    ax.plot([40, W - 40], [y - 12, y - 12], color=GRID, lw=1)
    y += 14
ax.text(40, y + 4, '회색 = 아직 안 열림 · 빨강 = 사이트가 접근을 거부함 · 파랑 = 정상 응답 · 초록 = 전체 조회', fontsize=15, color=MUTED, va='center')
footer(ax, H, '2026.10.10~10.12 아침')
save(fig, 'open_timeline_20261012.png')


# ② 권역 격자: 도시 × (인천→ / →인천), 칸 안 편별 일반석·프레스티지
def grid(region, fn, title, sub, codes, when):
    rowh = 46
    H = 300 + len(codes) * rowh + 110
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=32, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, sub, fontsize=19, color=INK2, va='center')
    lx = 40
    for lab, col in (('일반석 9석 이상', KE), ('1~8석', MID), ('0석', WARN), ('편 없음·운임 없음', NONE)):
        ax.add_patch(Rectangle((lx, 150), 18, 18, facecolor=col, edgecolor='none'))
        ax.text(lx + 26, 159, lab, fontsize=16, color=INK2, va='center')
        lx += 26 + len(lab) * 15 + 36
    ax.text(lx + 10, 159, '· 칸 끝 P숫자 = 프레스티지 잔여', fontsize=16, color=INK2, va='center')
    x0 = 250; cw = (W - 40 - x0) / 2
    for j, lab in enumerate(('인천 → 도시', '도시 → 인천')):
        ax.text(x0 + cw * j + cw / 2, 215, lab, fontsize=20, color=INK2, ha='center', va='center')
    ax.plot([40, W - 40], [238, 238], color=GRID, lw=1.2)
    y = 262
    for code in codes:
        ax.text(40, y + rowh / 2, NAME[code], fontsize=19, color=INK, va='center')
        for j, key in enumerate(('ICN-%s' % code, '%s-ICN' % code)):
            c = CELL.get(key, {'state': 'nofl', 'fl': []})
            x = x0 + cw * j + 6
            if c['state'] != 'fl':
                ax.add_patch(Rectangle((x, y + 6), cw - 12, rowh - 12, facecolor='#f2f1ec', edgecolor='none'))
                ax.text(x + (cw - 12) / 2, y + rowh / 2, '운임 없음' if c['state'] == 'nofare' else '편 없음', fontsize=14, color=MUTED, ha='center', va='center')
                continue
            n = len(c['fl']); bw = (cw - 12 - 4 * (n - 1)) / n
            for k, r in enumerate(c['fl']):
                col = NONE if r['ey'] is None else (WARN if r['ey'] == 0 else (MID if r['ey'] < 9 else KE))
                ax.add_patch(Rectangle((x + k * (bw + 4), y + 6), bw, rowh - 12, facecolor=col, edgecolor='none'))
                ptxt = 'P%d' % (r['pr'] or 0) if r['pr'] is not None else ''
                txt = ('%s %s %s' % (r['dep'], '0석' if r['ey'] == 0 else ('%d석' % r['ey'] if r['ey'] < 9 else '9+'), ptxt)).strip() if n <= 3 else ('%s %s' % (r['dep'], ptxt)).strip()
                ax.text(x + k * (bw + 4) + bw / 2, y + rowh / 2, txt, fontsize=13 if n <= 3 else 11, color='white' if col in (KE, WARN) else INK, ha='center', va='center')
        y += rowh
    ax.plot([40, W - 40], [y + 4, y + 4], color=GRID, lw=1.2)
    ax.text(40, y + 30, '칸 하나가 편 하나 · 시각은 출발지 현지 · 2027년 10월 7일(목) 출발', fontsize=15, color=MUTED, va='center')
    footer(ax, H, when)
    save(fig, fn)


grid('유럽', 'open_grid_europe_20261012.png', '유럽 14도시, 열린 지 10분 안의 마일리지 좌석', '2027년 10월 7일(목) · 2026년 10월 12일 09:03~09:09 조회 · 왕복 양방향', EU, '2026.10.12 09:03~09:09')
grid('아시아', 'open_grid_asia_20261012.png', '아시아 22도시, 열린 지 10분 안의 마일리지 좌석', '2027년 10월 7일(목) · 2026년 10월 12일 09:01~09:08 조회 · 왕복 양방향', AS, '2026.10.12 09:01~09:08')
grid('미주·대양주', 'open_grid_americas_20261012.png', '미주·대양주 16도시, 열린 지 10분 안의 좌석', '2027년 10월 7일(목) · 2026년 10월 12일 09:04~09:11 조회 · 왕복 양방향', AM, '2026.10.12 09:04~09:11')

# ③ 프레스티지 카드: 열린 지 10분 안에 남은 것
H = 1000
fig, ax = canvas(H)
ax.text(40, 62, '열린 지 10분, 프레스티지는 어디에 남았나', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '2027년 10월 7일(목) 왕복 양방향 · 2026년 10월 12일 09:01~09:11 조회 · 편 단위', fontsize=19, color=INK2, va='center')
y = 190
for reg in RN:
    s = S[reg]; n = s['n']; ok = len(s['prok'])
    ax.text(40, y, reg, fontsize=28, fontweight='bold', color=INK, va='center')
    ax.text(1040, y, '%d편 중 %d편에 남음' % (n, ok), fontsize=28, fontweight='bold', color=KE, va='center', ha='right')
    y += 40
    ax.add_patch(Rectangle((40, y), W - 80, 22, facecolor=NONE, edgecolor='none'))
    if ok:
        ax.add_patch(Rectangle((40, y), (W - 80) * ok / n, 22, facecolor=KE, edgecolor='none'))
    y += 44
    tot = collections.OrderedDict()
    for r in F:
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
ax.text(40, y + 4, '도시 뒤 숫자는 「프레스티지 남은 편 / 전체 편」 (인천→·→인천 합)', fontsize=15, color=MUTED, va='center')
footer(ax, H, '2026.10.12 09:01~09:11')
save(fig, 'open_prestige_20261012.png')


# ④ 연휴 날짜 vs 평일: 열린 뒤 경과 시간별 프레스티지 남은 편 (10/8·10/9·10/10·10/12 자료)
BD = r"C:\Users\user\Desktop\Blog\_1.컨텐츠\여행정보_컨텐츠\261008_2027_10월연휴_마일리지\base data"
SNAPS = [
    ('2027-10-03 (일) 연휴 출발', '열린 지 2시간쯤', ['ke_live_2027holiday.json', 'ke_live_2027holiday_europe.json', 'ke_live_2027holiday_americas.json'], '20271003'),
    ('2027-10-04 (월) 연휴 복귀', '열린 지 13시간', ['ke_live_2027holiday_return_1009.json'], '20271004'),
    ('2027-10-05 (화) 왕복 20도시', '열린 지 2시간', ['ke_live_2027holiday_1005_20cities_1010.json'], '20271005'),
    ('2027-10-07 (목) 평일 왕복', '열린 지 10분', ['ke_live_2027holiday_1007_full_1012.json'], '20271007'),
]
R3 = {}
for c in AS: R3[c] = '아시아'
for c in EU: R3[c] = '유럽'
for c in AM: R3[c] = '미주·대양주'
SNAP = []
for title, elapsed, files, ymd in SNAPS:
    agg = {r: [0, 0, 0] for r in RN}   # 전체, 프레스티지 있음, 일반석 0
    for fn in files:
        Lx = json.load(open(os.path.join(BD, fn), encoding='utf-8'))
        for key, days in Lx.items():
            r = days.get(ymd)
            if not r: continue
            reg = R3[key.replace('ICN-', '').replace('-ICN', '')]
            for f in r.get('flights', []):
                if f.get('segs', 1) != 1: continue
                agg[reg][0] += 1
                agg[reg][1] += 1 if ((f['cab'].get('PR') or [None])[0] or 0) > 0 else 0
                agg[reg][2] += 1 if (f['cab'].get('EY') or [None])[0] == 0 else 0
    SNAP.append((title, elapsed, agg))
json.dump({'summary': S, 'timeline': TL, 'snaps': SNAP}, open(os.path.join(OUT, '_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)

SNAP2 = [SNAP[0], SNAP[3]]
H = 660
fig, ax = canvas(H)
ax.text(40, 62, '열린 뒤 몇 시간째, 프레스티지가 몇 편에 남았나', fontsize=30, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '연휴 출발일과 평일, 각각 열린 당일에 조회 · 막대 = 전체 편 중 프레스티지가 남은 편', fontsize=19, color=INK2, va='center')
COLS = {'아시아': KE, '유럽': '#eb6834', '미주·대양주': '#6b5bd6'}
lx = 40
for reg in RN:
    ax.add_patch(Rectangle((lx, 150), 18, 18, facecolor=COLS[reg], edgecolor='none'))
    ax.text(lx + 26, 159, reg, fontsize=16, color=INK2, va='center'); lx += 26 + len(reg) * 16 + 40
y = 205
for title, elapsed, agg in SNAP2:
    ax.text(40, y, title, fontsize=24, fontweight='bold', color=INK, va='center')
    ax.text(1040, y, elapsed, fontsize=20, color=WARN if '10분' in elapsed else INK2, va='center', ha='right')
    y += 36
    for reg in RN:
        n, ok, ey0 = agg[reg]
        ax.text(60, y + 11, reg, fontsize=16, color=INK2, va='center')
        ax.add_patch(Rectangle((200, y), 640, 22, facecolor=NONE, edgecolor='none'))
        if n and ok:
            ax.add_patch(Rectangle((200, y), 640 * ok / n, 22, facecolor=COLS[reg], edgecolor='none'))
        ax.text(856, y + 11, '%d편 중 %d편' % (n, ok), fontsize=18, fontweight='bold', color=INK, va='center')
        y += 32
    y += 22
    ax.plot([40, W - 40], [y - 10, y - 10], color=GRID, lw=1)
    y += 12
ax.text(40, y + 6, '10/3 은 52도시 출발편만, 10/7 은 52도시 왕복 · 날짜가 달라 같은 날의 비교는 아님', fontsize=14, color=MUTED, va='center')
footer(ax, H, '2026.10.8 · 10.12')
save(fig, 'open_prestige_compare_20261012.png')
