# -*- coding: utf-8 -*-
"""아시아나 공개 마일리지 달력 -> raw CSV + 노선 요약 CSV + 지역별 인포그래픽 PNG"""
import json, sys, csv, os, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.stdout.reconfigure(encoding='utf-8')
SRC = sys.argv[1:] or ['main.json', 'scan2.json']
OUT = r"C:/Users/user/Desktop/Blog/아시아나_합병전_마일리지"
os.makedirs(OUT, exist_ok=True)
LO, HI = '20261002', '20261216'
KR_ORDER = ['ICN', 'GMP', 'PUS', 'CJU', 'CJJ', 'TAE', 'KWJ', 'RSU']
KR = set(KR_ORDER)
NAME = {
    'ICN': '인천', 'GMP': '김포', 'PUS': '부산', 'CJU': '제주', 'CJJ': '청주', 'TAE': '대구', 'KWJ': '광주', 'RSU': '여수',
    'SFO': '샌프란시스코', 'JFK': '뉴욕', 'LAX': 'LA', 'SEA': '시애틀', 'HNL': '호놀룰루',
    'LHR': '런던', 'FCO': '로마', 'BCN': '바르셀로나', 'IST': '이스탄불', 'CDG': '파리', 'FRA': '프랑크푸르트', 'MXP': '밀라노', 'PRG': '프라하',
    'SYD': '시드니', 'MEL': '멜버른',
    'SIN': '싱가포르', 'BKK': '방콕', 'SGN': '호찌민', 'HAN': '하노이', 'DAD': '다낭', 'CXR': '나트랑', 'PQC': '푸꾸옥', 'HKT': '푸껫',
    'CNX': '치앙마이', 'MNL': '마닐라', 'CEB': '세부', 'CRK': '클락', 'CGK': '자카르타', 'BKI': '코타키나발루', 'PNH': '프놈펜', 'KTI': '프놈펜(떼쪼)',
    'ALA': '알마티', 'TAS': '타슈켄트',
    'NRT': '도쿄 나리타', 'HND': '도쿄 하네다', 'KIX': '오사카', 'NGO': '나고야', 'FUK': '후쿠오카', 'CTS': '삿포로', 'OKA': '오키나와',
    'SDJ': '센다이', 'KMI': '미야자키', 'KMJ': '구마모토', 'AKJ': '아사히카와', 'UKB': '고베',
    'PEK': '베이징', 'PVG': '상하이 푸동', 'SHA': '상하이 훙차오', 'CAN': '광저우', 'SZX': '선전', 'DLC': '다롄', 'NKG': '난징', 'XIY': '시안',
    'YNJ': '옌지', 'YNZ': '옌청', 'CSX': '창사', 'CGQ': '창춘', 'TFU': '청두', 'TAO': '칭다오', 'TSN': '톈진', 'HRB': '하얼빈', 'HGH': '항저우',
    'CKG': '충칭', 'SHE': '선양',
    'HKG': '홍콩', 'TPE': '타이베이', 'UBN': '울란바타르',
}
REGION = {}
for _r, _aps in {
    '미주': 'SFO JFK LAX SEA HNL', '유럽': 'LHR FCO BCN IST CDG FRA MXP PRG', '대양주': 'SYD MEL',
    '동남아': 'SIN BKK SGN HAN DAD CXR PQC HKT CNX MNL CEB CRK CGK BKI PNH KTI', '중앙아시아': 'ALA TAS',
    '일본': 'NRT HND KIX NGO FUK CTS OKA SDJ KMI KMJ AKJ UKB',
    '중국': 'PEK PVG SHA CAN SZX DLC NKG XIY YNJ YNZ CSX CGQ TFU TAO TSN HRB HGH CKG SHE',
    '홍콩·대만·몽골': 'HKG TPE UBN',
}.items():
    for _a in _aps.split():
        REGION[_a] = _r
AP_ORDER = {a: i for i, a in enumerate(NAME)}


def region_of(o, d):
    if o in KR and d in KR:
        return '국내선'
    return REGION.get(d if o in KR else o, '기타')


def nm(a):
    return NAME.get(a, a)


# ---- 데이터 적재
res, source_at = {}, None
for f in SRC:
    if not os.path.exists(f):
        print('skip', f)
        continue
    j = json.load(open(f, encoding='utf-8'))
    source_at = j.get('sourceAt') or source_at
    for k, v in j['res'].items():
        res[k] = v
print('방향 수', len(res), '기준', source_at)

days_all = []
_d = dt.date(2026, 10, 2)
while _d <= dt.date(2026, 12, 16):
    days_all.append(_d)
    _d += dt.timedelta(days=1)
WD = '월화수목금토일'

# ---- raw CSV
raw_path = os.path.join(OUT, '아시아나_마일리지좌석_raw_20261002-1216.csv')
nrow = 0
with open(raw_path, 'w', newline='', encoding='utf-8-sig') as fp:
    w = csv.writer(fp)
    w.writerow(['달력기준시각', '출발일', '요일', '지역', '출발공항', '도착공항', '노선', '편명', '출발시각', '좌석등급', '예약클래스', '잔여석표시'])
    for k in sorted(res, key=lambda k: (region_of(*k.split('-')), k)):
        o, dd = k.split('-')
        reg = region_of(o, dd)
        route = nm(o) + '→' + nm(dd)
        for day in sorted(res[k]['days']):
            if not (LO <= day <= HI):
                continue
            date = dt.date(int(day[:4]), int(day[4:6]), int(day[6:]))
            for cab, label, cls in (('Y', '일반석', 'X'), ('C', '비즈니스', 'I')):
                for flt, tm, qty in res[k]['days'][day][cab]:
                    w.writerow([source_at, date.isoformat(), WD[date.weekday()], reg, o, dd, route,
                                'OZ' + flt.lstrip('0'), tm[:2] + ':' + tm[2:], label, cls, qty])
                    nrow += 1
print('raw rows', nrow, raw_path)


def daily(k, cab):
    out = {}
    for day, row in res[k]['days'].items():
        if LO <= day <= HI and row[cab]:
            out[day] = sum(q for _, _, q in row[cab])
    return out


# ---- 노선 요약 CSV
summ = []
for k in res:
    o, dd = k.split('-')
    row = {'지역': region_of(o, dd), '노선': nm(o) + '→' + nm(dd), '출발': o, '도착': dd}
    for cab, label in (('Y', '일반석'), ('C', '비즈니스')):
        dly = daily(k, cab)
        row[label + '_운항일'] = len(dly)
        row[label + '_좌석있는날'] = sum(1 for v in dly.values() if v > 0)
        row[label + '_잔여석합'] = sum(dly.values())
    summ.append(row)
summ.sort(key=lambda r: (r['지역'], r['노선']))
sp = os.path.join(OUT, '아시아나_마일리지좌석_노선요약.csv')
with open(sp, 'w', newline='', encoding='utf-8-sig') as fp:
    w = csv.DictWriter(fp, fieldnames=list(summ[0].keys()))
    w.writeheader()
    w.writerows(summ)
print('summary', len(summ), sp)

# ---- 인포그래픽
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF, INK, INK2, MUTED, GRID, AXIS = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'
C0, C1, C2, C3 = '#eceae4', '#86b6ef', '#2a78d6', '#104281'  # 0석 / 1~3 / 4~8 / 9석 이상


def color(v):
    return C0 if v == 0 else C1 if v <= 3 else C2 if v <= 8 else C3


def draw(region, pairs, part=None):
    rows = []
    for a, b in pairs:
        for k in (a + '-' + b, b + '-' + a):
            if k in res and any(LO <= d_ <= HI for d_ in res[k]['days']):
                rows.append(k)
    if not rows:
        return None
    n = len(rows)
    CW, RH = 11.2, 25
    LBL, W = 255, 1240
    grid_w = CW * len(days_all)
    panel_h = 50 + n * RH + 16
    H = 150 + 2 * panel_h + 64
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=SURF)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis('off')
    title = '아시아나 마일리지 좌석 · ' + region + ((' (' + part + ')') if part else '')
    ax.text(30, 46, title, fontsize=25, fontweight='bold', color=INK, va='center')
    ax.text(30, 84, '합병 전 탑승분(2026.10.2~12.16) 날짜별 보너스 좌석 잔여 표시', fontsize=13.5, color=INK2, va='center')
    lx, ly = 30, 118
    for c, lab, wdt in ((C3, '9석 이상', 86), (C2, '4~8석', 72), (C1, '1~3석', 72), (C0, '좌석 없음', 92)):
        ax.add_patch(Rectangle((lx, ly - 8), 16, 16, facecolor=c, edgecolor='none'))
        ax.text(lx + 22, ly, lab, fontsize=12, color=INK2, va='center')
        lx += 22 + wdt
    ax.add_patch(Rectangle((lx, ly - 8), 16, 16, facecolor=SURF, edgecolor=AXIS, lw=1))
    ax.text(lx + 22, ly, '운항·자료 없음', fontsize=12, color=INK2, va='center')
    y0 = 150
    for cab, label in (('C', '비즈니스'), ('Y', '일반석')):
        ax.text(30, y0 + 16, label, fontsize=17, fontweight='bold', color=INK, va='center')
        ax.text(LBL + grid_w + 14, y0 + 38, '있는 날/운항', fontsize=10, color=MUTED, va='center')
        for i, d_ in enumerate(days_all):
            if d_.day == 1 or i == 0:
                ax.text(LBL + i * CW, y0 + 38, str(d_.month) + '월', fontsize=11.5, color=INK2, va='center', fontweight='bold')
            elif d_.day in (10, 20):
                ax.text(LBL + i * CW + CW / 2, y0 + 38, str(d_.day), fontsize=9.5, color=MUTED, va='center', ha='center')
        top = y0 + 50
        for r_i, k in enumerate(rows):
            o, dd = k.split('-')
            y = top + r_i * RH
            ax.text(LBL - 12, y + RH / 2 - 1, nm(o) + ' → ' + nm(dd), fontsize=12.5, color=INK, va='center', ha='right')
            dly = daily(k, cab)
            for i, d_ in enumerate(days_all):
                key = d_.strftime('%Y%m%d')
                if key in dly:
                    ax.add_patch(Rectangle((LBL + i * CW, y + 2), CW - 1.6, RH - 5, facecolor=color(dly[key]), edgecolor='none'))
                else:
                    ax.add_patch(Rectangle((LBL + i * CW, y + 2), CW - 1.6, RH - 5, facecolor=SURF, edgecolor=GRID, lw=0.5))
            av = sum(1 for v in dly.values() if v > 0)
            ax.text(LBL + grid_w + 14, y + RH / 2 - 1, str(av) + ' / ' + str(len(dly)) + '일', fontsize=12.5, color=INK, va='center')
            if r_i % 2 == 1 and r_i < n - 1:
                ax.plot([30, W - 30], [y + RH + 0.5, y + RH + 0.5], color=GRID, lw=0.6)
        for i, d_ in enumerate(days_all):
            if d_.day == 1:
                ax.plot([LBL + i * CW - 1, LBL + i * CW - 1], [top, top + n * RH], color=AXIS, lw=1)
        y0 += panel_h
    ax.text(30, H - 42, '자료: 아시아나항공 마일리지 좌석 조회(공개 달력) · 달력 기준 ' + str(source_at) + ' · 조회 2026.10.2', fontsize=11, color=MUTED, va='center')
    ax.text(30, H - 22, '하루 1회 갱신되는 표시이며 실시간 잔여가 아닙니다. 편당 표시 상한 9~10석, 승급용 좌석 제외.', fontsize=11, color=MUTED, va='center')
    fn = os.path.join(OUT, '아시아나_마일리지좌석_' + region.replace('·', '') + (('_' + part.replace('/', 'of')) if part else '') + '.png')
    fig.savefig(fn, dpi=100, facecolor=SURF)
    plt.close(fig)
    return fn


pairs_by = {}
for k in res:
    o, dd = k.split('-')
    if o in KR and dd in KR:
        a, b = sorted([o, dd], key=KR_ORDER.index)
    else:
        a, b = (o, dd) if o in KR else (dd, o)
    reg = region_of(o, dd)
    pairs_by.setdefault(reg, [])
    if (a, b) not in pairs_by[reg]:
        pairs_by[reg].append((a, b))

ORDER = ['미주', '유럽', '대양주', '동남아', '중앙아시아', '일본', '중국', '홍콩·대만·몽골', '국내선']
made = []
for reg in ORDER:
    ps = pairs_by.get(reg)
    if not ps:
        continue
    ps.sort(key=lambda p: (KR_ORDER.index(p[0]), AP_ORDER.get(p[1], 999)))
    if len(ps) > 11:
        half = (len(ps) + 1) // 2
        for i, chunk in enumerate((ps[:half], ps[half:]), 1):
            made.append(draw(reg, chunk, str(i) + '/2'))
    else:
        made.append(draw(reg, ps))
for m in made:
    if m:
        print(m)


# ---- 지역 한눈에 보기 (좌석 있는 날 비율)
agg = {}
for r in summ:
    g = agg.setdefault(r['지역'], {'Y_op': 0, 'Y_av': 0, 'C_op': 0, 'C_av': 0})
    g['Y_op'] += r['일반석_운항일']; g['Y_av'] += r['일반석_좌석있는날']
    g['C_op'] += r['비즈니스_운항일']; g['C_av'] += r['비즈니스_좌석있는날']
regs = [r for r in ORDER if r in agg and agg[r]['Y_op']]
W2, RH2, TOP = 1240, 78, 170
H2 = TOP + RH2 * len(regs) + 80
fig = plt.figure(figsize=(W2 / 100, H2 / 100), dpi=100, facecolor=SURF)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W2); ax.set_ylim(H2, 0); ax.axis('off')
ax.text(30, 46, '아시아나 마일리지 좌석 · 지역별 한눈에 보기', fontsize=25, fontweight='bold', color=INK, va='center')
ax.text(30, 84, '합병 전 탑승분(2026.10.2~12.16) · 운항일 중 보너스 좌석이 1석 이상 표시된 날의 비율', fontsize=13.5, color=INK2, va='center')
BIZ, ECO = '#2a78d6', '#eb6834'
ax.add_patch(Rectangle((30, 112), 16, 16, facecolor=BIZ, edgecolor='none')); ax.text(52, 120, '비즈니스', fontsize=12.5, color=INK2, va='center')
ax.add_patch(Rectangle((140, 112), 16, 16, facecolor=ECO, edgecolor='none')); ax.text(162, 120, '일반석', fontsize=12.5, color=INK2, va='center')
X0, BW = 230, 820
for t in (0, 25, 50, 75, 100):
    x = X0 + BW * t / 100
    ax.plot([x, x], [TOP - 14, TOP + RH2 * len(regs) - 8], color=GRID, lw=0.8)
    ax.text(x, TOP - 26, str(t) + '%', fontsize=10.5, color=MUTED, ha='center', va='center')
for i, reg in enumerate(regs):
    g = agg[reg]; y = TOP + i * RH2
    ax.text(X0 - 16, y + 27, reg, fontsize=15, fontweight='bold', color=INK, ha='right', va='center')
    for j, (cab, col) in enumerate((('C', BIZ), ('Y', ECO))):
        pct = g[cab + '_av'] / g[cab + '_op'] if g[cab + '_op'] else 0
        yy = y + 6 + j * 24
        ax.add_patch(Rectangle((X0, yy), max(BW * pct, 2), 20, facecolor=col, edgecolor='none'))
        ax.text(X0 + BW * pct + 10, yy + 10, '{:.0%}  ({}/{}일)'.format(pct, g[cab + '_av'], g[cab + '_op']), fontsize=12, color=INK, va='center')
ax.text(30, H2 - 42, '자료: 아시아나항공 마일리지 좌석 조회(공개 달력) · 달력 기준 ' + str(source_at) + ' · 조회 2026.10.2 · 노선·방향별 운항일 합계 기준', fontsize=11, color=MUTED, va='center')
ax.text(30, H2 - 22, '하루 1회 갱신되는 표시이며 실시간 잔여가 아닙니다. 승급용 좌석 제외.', fontsize=11, color=MUTED, va='center')
fn = os.path.join(OUT, '아시아나_마일리지좌석_0_지역별요약.png')
fig.savefig(fn, dpi=100, facecolor=SURF); plt.close(fig); print(fn)
