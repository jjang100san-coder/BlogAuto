# -*- coding: utf-8 -*-
"""아시아나 전 국제선 비즈니스 유/무(비즈니스 전용 달력) → CSV + 요약 이미지
사용: python build_biz_all.py data/oz_biz_all.json "<출력 폴더>"
"""
import sys, os, json, csv, re, datetime as dt, collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\아시아나_합병전_마일리지\_원본')
import ozdata as PUB
from ozdata import short
NAME = dict(PUB.NAME)
NAME.update({'BKI': '코타키나발루', 'CEB': '세부', 'CNX': '치앙마이', 'PNH': '프놈펜(구공항)', 'PQC': '푸꾸옥', 'NKG': '난징', 'CGQ': '창춘', 'YNJ': '옌지', 'HRB': '하얼빈', 'CSX': '창사', 'TFU': '청두', 'XIY': '시안', 'YNZ': '옌청', 'KMJ': '구마모토', 'AKJ': '아사히카와', 'SHE': '선양', 'TAO': '칭다오', 'CKG': '충칭', 'HNL': '호놀룰루', 'MEL': '멜버른', 'WEH': '웨이하이', 'YNT': '옌타이', 'KWL': '구이린'})

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
db = json.load(open(SRC, encoding='utf-8'))['res']
LO, HI = dt.date(2026, 10, 4), dt.date(2026, 12, 16)  # 밤 조회라 10/3 은 이미 조회 범위 밖이었다
DAYS = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1)]
N = len(DAYS)
REG = [('미주', {'LAX', 'JFK', 'SFO', 'SEA', 'HNL'}), ('유럽', {'LHR', 'CDG', 'FRA', 'FCO', 'MXP', 'BCN', 'PRG', 'IST'}), ('대양주·중앙아', {'SYD', 'MEL', 'ALA', 'TAS'}),
       ('동남아', {'BKK', 'SIN', 'MNL', 'SGN', 'HAN', 'DAD', 'HKT', 'KTI', 'PNH', 'CRK', 'CGK', 'CXR', 'CEB', 'CNX', 'BKI', 'PQC'}),
       ('일본', {'NRT', 'HND', 'KIX', 'FUK', 'NGO', 'CTS', 'OKA', 'SDJ', 'KMI', 'UKB', 'KMJ', 'AKJ'}),
       ('중국·대만·홍콩·몽골', {'PEK', 'PVG', 'SHA', 'CAN', 'SZX', 'DLC', 'HGH', 'TSN', 'HKG', 'TPE', 'UBN', 'CGQ', 'CKG', 'CSX', 'HRB', 'NKG', 'TAO', 'SHE', 'TFU', 'XIY', 'YNJ', 'YNZ'})]
KR = {'ICN', 'GMP', 'PUS', 'CJU', 'CJJ', 'TAE', 'KWJ', 'RSU', 'USN'}
def fmt(dates):
    """[date] → '10월 4~31일, 11월 1~30일, 12월 1~16일' (달을 넘는 구간은 달마다 끊는다)"""
    dates = sorted(dates)
    if not dates:
        return ''
    bym = collections.OrderedDict()
    runs, s0, p = [], dates[0], dates[0]
    for d in dates[1:]:
        if d == p + dt.timedelta(days=1):
            p = d
            continue
        runs.append((s0, p)); s0 = p = d
    runs.append((s0, p))
    for a, b in runs:
        cur = a
        while cur <= b:
            last = min(b, dt.date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1) - dt.timedelta(days=1))
            bym.setdefault(cur.month, []).append(str(cur.day) if cur == last else '%d~%d' % (cur.day, last.day))
            cur = last + dt.timedelta(days=1)
    return ', '.join('%d월 %s일' % (m, '·'.join(v)) for m, v in bym.items())

def noflight(o, d):
    k = o + '-' + d
    return k in PUB.res and not PUB.listed(o, d, 'Y') and not PUB.listed(o, d, 'C')

def region(o, d):
    x = d if o in KR else o
    for nm, s in REG:
        if x in s:
            return nm
    return '기타'
rows = [['지역', '방향', '출발공항', '도착공항', '기간_일수', '비즈니스_있는_날', '날짜', '조회_시각', '상태']]
items = []
asofs = []
for key, rec in db.items():
    o, d = key.split('-')
    B = rec.get('B')
    if not B:
        rows.append([region(o, d), NAME.get(o, o) + '→' + NAME.get(d, d), o, d, N, '', '', '', '미수집(' + (rec.get('error') or '중단') + ')'])
        continue
    days = [x for x in DAYS if B['days'].get(x.isoformat(), {}).get('B')]
    covered = sum(1 for x in DAYS if x.isoformat() in B['days'])
    ts = sorted(q['asOf'] for q in B['queries'])
    asofs += ts
    items.append((region(o, d), o, d, days, covered))
    rows.append([region(o, d), NAME.get(o, o) + '→' + NAME.get(d, d), o, d, N, len(days), short(days), (ts[0] if ts else '').replace(' 기준', ''), ('완료' if rec.get('done') else '부분(%d일 확인)' % covered) + (' · 공개 달력에 편 없음' if not days and noflight(o, d) else '')])
with open(os.path.join(OUT, '아시아나_국제선_비즈니스_유무_20261003.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    csv.writer(f).writerows(rows)
have = [i for i in items if i[3]]
print('방향', len(items), '| 비즈니스 1일 이상', len(have), '| 0일', len(items) - len(have), '| 미수집', len(db) - len(items))
for r, o, d, days, cov in sorted(have, key=lambda i: (-len(i[3]), i[0])):
    print(' %s %s→%s %d일 %s' % (r, NAME.get(o, o), NAME.get(d, d), len(days), fmt(days)))
def _k(t):
    m = re.search(r'(\d{4})\.\s*(\d{2})\.\s*(\d{2})\.?\s*(\d{2}:\d{2})', t)
    return (m.group(1), m.group(2), m.group(3), m.group(4)) if m else None
ks = sorted(k for k in (_k(t) for t in asofs) if k)
SPAN = '%d.%d %s ~ %d.%d %s' % (int(ks[0][1]), int(ks[0][2]), ks[0][3], int(ks[-1][1]), int(ks[-1][2]), ks[-1][3]) if ks else ''
# ── 이미지: 지역별로 비즈니스가 있던 방향과 날짜 ──
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF, INK, INK2, MUTED, GRID, NONE, BIZ = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#e6e4dd', '#2a78d6'
W = 1080
def wrap(s, n=46):
    out, cur = [], ''
    for part in s.split(', '):
        if len(cur) + len(part) + 2 > n and cur:
            out.append(cur + ','); cur = part
        else:
            cur = (cur + ', ' + part) if cur else part
    return out + [cur] if cur else out
blocks = []
for rname, _ in REG[:4]:  # 날짜 목록은 좌석이 드문 장거리 4개 지역만 (일본·중국은 띠 달력으로)
    its = sorted([i for i in have if i[0] == rname], key=lambda i: -len(i[3]))
    zero = [i for i in items if i[0] == rname and not i[3]]
    if its or zero:
        z1 = sorted('%s→%s' % (NAME.get(o, o), NAME.get(d, d)) for r, o, d, days, cov in zero if not noflight(o, d))
        z2 = sorted('%s→%s' % (NAME.get(o, o), NAME.get(d, d)) for r, o, d, days, cov in zero if noflight(o, d))
        zlines = (wrap('0일: ' + ', '.join(z1), 56) if z1 else []) + (wrap('이 기간 편이 없던 노선: ' + ', '.join(z2), 56) if z2 else [])
        blocks.append((rname, its, zlines))
H = 200 + sum(50 + sum(34 + (len(wrap(short(i[3]))) - 1) * 26 for i in its) + (len(zl) * 24 + 10 if zl else 0) + 24 for _, its, zl in blocks) + 100
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=SURF)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
ax.text(40, 62, '아시아나 비즈니스 좌석 · 장거리 날짜 전부', fontsize=34, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '합병 전 %d일 (2026.10.4~12.16 출발) 가운데 비즈니스 좌석이 있던 날' % N, fontsize=22, color=INK2, va='center')
ax.text(40, 160, '미주·유럽·대양주·중앙아시아·동남아 — 비즈니스 좌석이 있던 날짜 전부', fontsize=20, color=INK2, va='center')
y = 200
for rname, its, zl in blocks:
    ax.text(40, y + 20, rname, fontsize=26, fontweight='bold', color=INK, va='center'); y += 50
    for r, o, d, days, cov in its:
        ax.add_patch(Rectangle((40, y + 4), 16, 16, facecolor=BIZ, edgecolor='none'))
        ax.text(66, y + 12, '%s→%s' % (NAME.get(o, o), NAME.get(d, d)), fontsize=19, color=INK2, va='center')
        ax.text(330, y + 12, '%d일' % len(days), fontsize=21, color=INK, va='center', fontweight='bold')
        for k, ln in enumerate(wrap(short(days))):
            ax.text(410, y + 12 + k * 26, ln, fontsize=18, color=INK2, va='center')
        y += 34 + (len(wrap(short(days))) - 1) * 26
    if zl:
        for k, ln in enumerate(zl):
            ax.text(66, y + 12 + k * 24, ln, fontsize=16, color=MUTED, va='center')
        y += len(zl) * 24 + 10
    y += 24
    ax.plot([40, W - 40], [y - 12, y - 12], color=GRID, lw=1)
ax.text(40, H - 58, '자료: 아시아나 마일리지 예매 화면 · 좌석등급 「비즈니스」만 조회 (2026년 %s)' % SPAN, fontsize=16, color=MUTED, va='center')
ax.text(40, H - 30, '성인 1명 편도 · 직항편 · 국내선은 등급 구분이 안 돼 제외 · 좌석은 수시로 바뀜', fontsize=16, color=MUTED, va='center')
fig.savefig(os.path.join(OUT, 'oz_biz_dates_longhaul_20261003.png'), dpi=100, facecolor=SURF); plt.close(fig)
print('oz_biz_dates_longhaul_20261003.png', W, 'x', int(H), '| 조회', SPAN)

# ───────── 추가 이미지: ① 머리 숫자 카드 ② 지역별 띠 달력(비즈니스가 있던 방향만) ─────────
def canvas(h):
    fig = plt.figure(figsize=(W / 100, h / 100), dpi=100, facecolor=SURF)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(h, 0); ax.axis('off')
    return fig, ax

def footer(ax, h):
    ax.text(40, h - 58, '자료: 아시아나 마일리지 예매 화면 · 좌석등급 「비즈니스」만 조회 (2026년 %s)' % SPAN, fontsize=16, color=MUTED, va='center')
    ax.text(40, h - 30, '성인 1명 편도 · 직항편 · 좌석은 수시로 바뀌어 조회 시점의 기록임', fontsize=16, color=MUTED, va='center')

# ① 머리 숫자
H = 1080
fig, ax = canvas(H)
ax.text(60, 92, '아시아나 비즈니스 마일리지', fontsize=50, fontweight='bold', color=INK, va='center')
ax.text(60, 168, '합병 전 %d일 · 국제선 전체를 열어봤어' % N, fontsize=32, color=INK2, va='center')
ax.text(60, 300, '조회한 방향', fontsize=30, color=INK2, va='center')
ax.text(W - 60, 300, '%d개' % len(items), fontsize=72, fontweight='bold', color=INK, va='center', ha='right')
ax.text(60, 430, '비즈니스가 하루라도 있던 방향', fontsize=30, color=INK2, va='center')
ax.text(W - 60, 430, '%d개' % len(have), fontsize=72, fontweight='bold', color=BIZ, va='center', ha='right')
ax.text(60, 560, '하루도 없던 방향', fontsize=30, color=INK2, va='center')
ax.text(W - 60, 560, '%d개' % (len(items) - len(have)), fontsize=72, fontweight='bold', color=INK, va='center', ha='right')
ax.plot([60, W - 60], [640, 640], color=GRID, lw=1)
top = sorted(have, key=lambda i: -len(i[3]))[:6]
ax.text(60, 690, '좌석이 있던 날이 많은 방향', fontsize=26, fontweight='bold', color=INK, va='center')
yy = 745
for r, o, d, days, cov in top:
    ax.text(60, yy, '%s→%s' % (NAME.get(o, o), NAME.get(d, d)), fontsize=26, color=INK2, va='center')
    ax.add_patch(Rectangle((520, yy - 14), 400 * len(days) / N, 28, facecolor=BIZ, edgecolor='none'))
    ax.text(W - 60, yy, '%d일' % len(days), fontsize=28, fontweight='bold', color=INK, va='center', ha='right')
    yy += 48
ax.text(60, 1036, '2026년 10월 3일 밤 조회 · 직접 만든 그림', fontsize=22, color=MUTED, va='center')
fig.savefig(os.path.join(OUT, 'oz_biz_thumb_20261003.png'), dpi=100, facecolor=SURF); plt.close(fig)
print('oz_biz_thumb_20261003.png')

# ② 지역별 띠 달력
X0, CW = 300, 8.6
SW = CW * N
for rname, _ in REG:
    its = sorted([i for i in have if i[0] == rname], key=lambda i: (i[1] not in KR, -len(i[3])))
    zero = [i for i in items if i[0] == rname and not i[3]]
    if not its:
        continue
    z1 = sorted('%s→%s' % (NAME.get(o, o), NAME.get(d, d)) for r, o, d, days, cov in zero if not noflight(o, d))
    z2 = sorted('%s→%s' % (NAME.get(o, o), NAME.get(d, d)) for r, o, d, days, cov in zero if noflight(o, d))
    zl = (wrap('비즈니스가 하루도 없던 방향: ' + ', '.join(z1), 54) if z1 else []) + (wrap('이 기간 편이 없던 노선: ' + ', '.join(z2), 54) if z2 else [])
    H = 232 + 24 + len(its) * 40 + 30 + len(zl) * 24 + 110
    fig, ax = canvas(H)
    ax.text(40, 62, '아시아나 비즈니스 마일리지 좌석 · %s' % rname.replace('중국·대만·홍콩·몽골', '중국·대만·홍콩').replace('대양주·중앙아', '대양주·중앙아시아'), fontsize=34, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, '합병 전 %d일 (2026.10.4~12.16 출발) 가운데 비즈니스 좌석이 있던 날' % N, fontsize=22, color=INK2, va='center')
    ax.add_patch(Rectangle((40, 157), 22, 22, facecolor=BIZ, edgecolor='none')); ax.text(70, 168, '비즈니스 있음', fontsize=18, color=INK2, va='center')
    ax.add_patch(Rectangle((250, 157), 22, 22, facecolor=NONE, edgecolor='none')); ax.text(280, 168, '없음(편이 없는 날 포함)', fontsize=18, color=INK2, va='center')
    ax.text(X0 + SW + 14, 212, '%d일 중' % N, fontsize=16, color=MUTED, va='center')
    for j, day in enumerate(DAYS):
        if day.day == 1 or j == 0:
            ax.text(X0 + j * CW, 236, '%d월' % day.month, fontsize=15, color=MUTED, va='center')
    y = 250
    for r, o, d, days, cov in its:
        ax.text(40, y + 14, '%s→%s' % (NAME.get(o, o), NAME.get(d, d)), fontsize=20, color=INK, va='center')
        hs = set(days)
        for j, day in enumerate(DAYS):
            ax.add_patch(Rectangle((X0 + j * CW, y + 2), CW - 1.4, 26, facecolor=BIZ if day in hs else NONE, edgecolor='none'))
            if day.day == 1:
                ax.plot([X0 + j * CW - 0.8, X0 + j * CW - 0.8], [y, y + 30], color='#c3c2b7', lw=1)
        ax.text(X0 + SW + 14, y + 14, '%d일' % len(days), fontsize=22, color=INK, va='center', fontweight='bold')
        y += 40
    y += 30
    for k, ln in enumerate(zl):
        ax.text(40, y + k * 24, ln, fontsize=16, color=MUTED, va='center')
    footer(ax, H)
    fn = 'oz_biz_strip_%s_20261003.png' % {'미주': 'americas', '유럽': 'europe', '대양주·중앙아': 'oceania', '동남아': 'sea', '일본': 'japan', '중국·대만·홍콩·몽골': 'china'}[rname]
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF); plt.close(fig)
    print(fn, W, 'x', int(H))
