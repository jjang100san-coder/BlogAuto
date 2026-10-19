# -*- coding: utf-8 -*-
"""김포↔제주 주말 마일리지 좌석(공개 달력, 10/4~12/27 토·일) → CSV + 이미지
사용: python build_jeju.py "<출력 폴더>"
입력: data/jeju_ke_weekend.json (대한항공, 전날 밤 기준), data/jeju_oz_weekend.json (아시아나, 10/3 07:00 기준)
"""
import sys, os, json, csv, datetime as dt, collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
LIVE = '--live' in sys.argv  # 로그인 실시간 결과(jeju_live_convert.py 산출물)로 만든다
KE = json.load(open(os.path.join(HERE, 'data', 'jeju_ke_weekend_live.json' if LIVE else 'jeju_ke_weekend.json'), encoding='utf-8'))
OZ = json.load(open(os.path.join(HERE, 'data', 'jeju_oz_weekend_live.json' if LIVE else 'jeju_oz_weekend.json'), encoding='utf-8'))
SRC_TXT = '두 항공사 마일리지 예매 화면에 로그인해 직접 조회 (2026.10.4 밤)' if LIVE else '두 항공사 공개 마일리지 좌석 달력 (대한항공 10.3 밤, 아시아나 10.3 07:00 기준) · 하루 한 번 갱신'
THUMB_SRC = '예매 화면 직접 조회 (2026.10.4 밤)' if LIVE else '공개 좌석 달력 기준 (2026.10.3)'
LIVE0 = '--live' in sys.argv
LO, HI = (dt.date(2026, 10, 5) if LIVE0 else dt.date(2026, 10, 4)), dt.date(2026, 12, 28)  # 실시간은 조회 당일(10/4)을 뺀다
WD = '월화수목금토일'
AIR = {'KE': '대한항공', 'OZ': '아시아나'}
COL = {'OZ': '#eb6834', 'KE': '#2a78d6'}
SURF, INK, INK2, MUTED, GRID, NONE = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#e6e4dd'
W = 1080


def slot(hhmm):
    h = int(hhmm[:2])
    return '아침' if h < 10 else ('낮' if h < 17 else '저녁')


def parse(air, data):
    """→ {(o,d): {date: [ {t, flt, eco, biz, slot} ]}}"""
    out = {}
    for key, days in data.items():
        o, d = key.split('-')
        out[(o, d)] = {}
        for ds, s in days:
            if ds == 'ERR':
                continue
            day = dt.date(int(ds[:4]), int(ds[4:6]), int(ds[6:]))
            fl = []
            for part in s.split(';'):
                if not part:
                    continue
                t, flt, eco, biz = part.split('|')
                t = t if ':' in t else t[:2] + ':' + t[2:]
                def val(x):
                    return None if x == '-' else int(x)
                e, b = val(eco), val(biz)
                fl.append({'t': t, 'flt': flt, 'eco': e, 'biz': b, 'slot': slot(t), 'share': air == 'KE' and flt.startswith('KE5')})
            out[(o, d)][day] = fl
    return out


D = {'KE': parse('KE', KE), 'OZ': parse('OZ', OZ)}
SAT = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1) if (LO + dt.timedelta(days=i)).weekday() == 5]
SUN = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1) if (LO + dt.timedelta(days=i)).weekday() == 6]
FRI = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1) if (LO + dt.timedelta(days=i)).weekday() == 4]
MON = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1) if (LO + dt.timedelta(days=i)).weekday() == 0]


def have(air, o, d, day, sl=None, cab='eco'):
    """좌석 있는 편 목록. 대한항공은 유/무(1), 아시아나는 좌석 수"""
    fl = D[air].get((o, d), {}).get(day)
    if fl is None:
        return None
    return [f for f in fl if (sl is None or f['slot'] == sl) and (f[cab] or 0) > 0]


# ── CSV: 편별 ──
rows = [['항공사', '방향', '출발일', '요일', '시간대', '출발', '편명', '일반석', '비즈니스/프레스티지', '비고']]
daily = [['항공사', '방향', '출발일', '요일', '편 수', '일반석 있는 편', '아침(10시 전) 있는 편', '낮 있는 편', '저녁(17시 후) 있는 편', '아침 첫 좌석 편']]
for air in ('KE', 'OZ'):
    for (o, d), days in D[air].items():
        for day in sorted(days):
            if day.weekday() not in (4, 5, 6, 0) or not (LO <= day <= HI):
                continue
            fl = days[day]
            for f in fl:
                e = '-' if f['eco'] is None else (('있음' if f['eco'] else '없음') if (air == 'KE' or LIVE) else ('%d석' % f['eco'] if f['eco'] else '0석'))
                b = '-' if f['biz'] is None else (('있음' if f['biz'] else '없음') if (air == 'KE' or LIVE) else ('%d석' % f['biz'] if f['biz'] else '0석'))
                rows.append([AIR[air], o + '→' + d, day.isoformat(), WD[day.weekday()], f['slot'], f['t'], f['flt'], e, b, '진에어 공동운항' if f['share'] else ''])
            hv = have(air, o, d, day)
            am = have(air, o, d, day, '아침')
            daily.append([AIR[air], o + '→' + d, day.isoformat(), WD[day.weekday()], len(fl), len(hv), len(am), len(have(air, o, d, day, '낮')), len(have(air, o, d, day, '저녁')),
                          (am[0]['t'] + ' ' + am[0]['flt']) if am else ''])
for fn, r in (('제주_주말_마일리지_편별_20261004.csv', rows), ('제주_주말_마일리지_일별_20261004.csv', daily)):
    with open(os.path.join(OUT, fn), 'w', newline='', encoding='utf-8-sig') as f:
        csv.writer(f).writerows(r)
    print(fn, len(r) - 1, '행')

# ── 요약 숫자 ──
def summary(air, o, d, days, sl):
    ok, miss, none = [], [], []
    for day in days:
        h = have(air, o, d, day, sl)
        if h is None:
            miss.append(day)
        elif h:
            ok.append(day)
        else:
            none.append(day)
    return ok, none, miss


S = {}
for air in ('KE', 'OZ'):
    for name, o, d, days, sl in (('토 아침 김포→제주', 'GMP', 'CJU', SAT, '아침'), ('토 전체 김포→제주', 'GMP', 'CJU', SAT, None), ('일 저녁 제주→김포', 'CJU', 'GMP', SUN, '저녁'),
                                 ('일 전체 제주→김포', 'CJU', 'GMP', SUN, None), ('토 전체 제주→김포', 'CJU', 'GMP', SAT, None), ('일 아침 김포→제주', 'GMP', 'CJU', SUN, '아침'),
                                 ('금 저녁 김포→제주', 'GMP', 'CJU', FRI, '저녁'), ('토 저녁 제주→김포', 'CJU', 'GMP', SAT, '저녁'), ('일 아침 제주→김포', 'CJU', 'GMP', SUN, '아침'), ('일 낮 제주→김포', 'CJU', 'GMP', SUN, '낮'), ('토 낮 김포→제주', 'GMP', 'CJU', SAT, '낮'), ('토 저녁 김포→제주', 'GMP', 'CJU', SAT, '저녁'),
                                 ('월 아침 제주→김포', 'CJU', 'GMP', MON, '아침'), ('월 낮 제주→김포', 'CJU', 'GMP', MON, '낮'), ('월 저녁 제주→김포', 'CJU', 'GMP', MON, '저녁'), ('월 전체 제주→김포', 'CJU', 'GMP', MON, None)):
        S[(air, name)] = summary(air, o, d, days, sl)
        ok, none, miss = S[(air, name)]
        print('%s %s: 있음 %d / 없음 %d / 달력에 안 뜸 %d  있는 날 %s' % (AIR[air], name, len(ok), len(none), len(miss), ', '.join('%d/%d' % (x.month, x.day) for x in ok)))

DET = {}
for air in ('KE', 'OZ'):
    DET[air] = {'sat_am': {d.isoformat(): [(f['t'], f['flt'], f['eco']) for f in have(air, 'GMP', 'CJU', d, '아침')] for d in SAT if have(air, 'GMP', 'CJU', d, '아침')},
                'sun_last': {d.isoformat(): (have(air, 'CJU', 'GMP', d)[-1]['t'], have(air, 'CJU', 'GMP', d)[-1]['flt']) for d in SUN if have(air, 'CJU', 'GMP', d)},
                'fri_pm': {d.isoformat(): [(f['t'], f['flt'], f['eco']) for f in have(air, 'GMP', 'CJU', d, '저녁')] for d in FRI if have(air, 'GMP', 'CJU', d, '저녁')},
                'sat_pm_back': {d.isoformat(): [(f['t'], f['flt'], f['eco']) for f in have(air, 'CJU', 'GMP', d, '저녁')] for d in SAT if have(air, 'CJU', 'GMP', d, '저녁')}}
    for k, v in DET[air].items():
        print(AIR[air], k, v)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


def canvas(h):
    fig = plt.figure(figsize=(W / 100, h / 100), dpi=100, facecolor=SURF)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(h, 0); ax.axis('off')
    return fig, ax


def footer(ax, h):
    ax.text(40, h - 58, '자료: ' + SRC_TXT, fontsize=16, color=MUTED, va='center')
    ax.text(40, h - 30, '성인 1명 편도 · 좌석은 수시로 바뀌어 조회 시점의 기록임' if LIVE else '아침 = 10시 전 출발, 저녁 = 17시 이후 출발 · 실시간 예매 화면과 다를 수 있음', fontsize=16, color=MUTED, va='center')


def grid(fn, title, sub, o, d, days, highlight):
    """주말 날짜 × (대한항공 아침/낮/저녁, 아시아나 아침/낮/저녁) — 칸 안 숫자는 좌석 있는 편 수"""
    cols = [('KE', '아침'), ('KE', '낮'), ('KE', '저녁'), ('OZ', '아침'), ('OZ', '낮'), ('OZ', '저녁')]
    X0, CW, RH = 250, 128, 44
    H = 300 + RH * len(days) + 110
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=36, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, sub, fontsize=21, color=INK2, va='center')
    ax.text(X0 + CW * 1.5, 182, '대한항공', fontsize=22, fontweight='bold', color=COL['KE'], ha='center', va='center')
    ax.text(X0 + CW * 4.5, 182, '아시아나', fontsize=22, fontweight='bold', color=COL['OZ'], ha='center', va='center')
    for j, (air, sl) in enumerate(cols):
        ax.text(X0 + CW * j + CW / 2, 226, sl, fontsize=19, color=INK2, ha='center', va='center')
    ax.text(W - 40, 148, '칸 안 숫자는 좌석 있는 편 수', fontsize=15, color=MUTED, va='center', ha='right')
    ax.plot([40, W - 40], [250, 250], color='#c3c2b7', lw=1)
    y = 262
    for day in days:
        ax.text(40, y + RH / 2, '%d월 %d일 (%s)' % (day.month, day.day, WD[day.weekday()]), fontsize=20, color=INK, va='center')
        for j, (air, sl) in enumerate(cols):
            h = have(air, o, d, day, sl)
            x = X0 + CW * j
            if h is None:
                ax.add_patch(Rectangle((x + 3, y + 4), CW - 6, RH - 8, facecolor=SURF, edgecolor=GRID, lw=1))
                ax.text(x + CW / 2, y + RH / 2, '달력 없음', fontsize=13, color=MUTED, ha='center', va='center')
            elif h:
                strong = sl == highlight
                ax.add_patch(Rectangle((x + 3, y + 4), CW - 6, RH - 8, facecolor=COL[air] if strong else '#d9e6f7' if air == 'KE' else '#fbe0d4', edgecolor='none'))
                ax.text(x + CW / 2, y + RH / 2, '%d편' % len(h), fontsize=19, fontweight='bold' if strong else 'normal', color=SURF if strong else INK, ha='center', va='center')
            else:
                ax.add_patch(Rectangle((x + 3, y + 4), CW - 6, RH - 8, facecolor=NONE, edgecolor='none'))
                ax.text(x + CW / 2, y + RH / 2, '0', fontsize=17, color=MUTED, ha='center', va='center')
        y += RH
    ax.plot([40, W - 40], [y + 6, y + 6], color='#c3c2b7', lw=1)
    footer(ax, H)
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF); plt.close(fig)
    print(fn, W, 'x', H)


grid('jeju_sat_out_20261004.png', '토요일 아침 김포→제주 마일리지 좌석', '10월 10일부터 12월 26일까지 토요일 12번 · 진한 칸이 10시 전 출발', 'GMP', 'CJU', SAT, '아침')
grid('jeju_sun_back_20261004.png', '일요일 저녁 제주→김포 마일리지 좌석', '%d월 %d일부터 12월 27일까지 일요일 %d번 · 진한 칸이 17시 이후 출발' % (SUN[0].month, SUN[0].day, len(SUN)), 'CJU', 'GMP', SUN, '저녁')

# ── 썸네일 ──
H = 1080
fig, ax = canvas(H)
ax.text(60, 92, '주말 제주 마일리지 좌석', fontsize=58, fontweight='bold', color=INK, va='center')
ax.text(60, 168, '토요일 아침에 가서 일요일 저녁에 오기 · 10~12월', fontsize=31, color=INK2, va='center')
y = 270
for air in ('KE', 'OZ'):
    ok1, n1, m1 = S[(air, '토 아침 김포→제주')]
    ok2, n2, m2 = S[(air, '일 저녁 제주→김포')]
    ax.text(60, y, AIR[air], fontsize=42, fontweight='bold', color=COL[air], va='center')
    ax.text(60, y + 78, '토요일 아침 김포→제주', fontsize=28, color=INK2, va='center')
    ax.text(W - 60, y + 78, '%d번 중 %d번' % (len(SAT), len(ok1)), fontsize=44, fontweight='bold', color=INK, va='center', ha='right')
    ax.text(60, y + 150, '일요일 저녁 제주→김포', fontsize=28, color=INK2, va='center')
    ax.text(W - 60, y + 150, '%d번 중 %d번' % (len(SUN) - len(m2), len(ok2)), fontsize=44, fontweight='bold', color=INK, va='center', ha='right')
    # 토요일 12칸 미니 그리드
    gx, gy, cs = 60, y + 200, 40
    for i, day in enumerate(SAT):
        h = have(air, 'GMP', 'CJU', day, '아침')
        ax.add_patch(Rectangle((gx + i * cs, gy), cs - 6, 26, facecolor=COL[air] if h else NONE, edgecolor='none'))
    ax.text(gx + 12 * cs + 10, gy + 13, '토요일 아침', fontsize=16, color=MUTED, va='center')
    gy2 = gy + 36
    for i, day in enumerate(SUN):
        h = have(air, 'CJU', 'GMP', day, '저녁')
        ax.add_patch(Rectangle((gx + i * cs, gy2), cs - 6, 26, facecolor=(COL[air] if h else NONE) if h is not None else SURF, edgecolor=GRID if h is None else 'none', lw=1))
    ax.text(gx + 13 * cs + 10, gy2 + 13, '일요일 저녁', fontsize=16, color=MUTED, va='center')
    y += 330
ax.text(60, 1020, THUMB_SRC + ' · 칸 하나가 주말 하루 · 직접 만든 그림', fontsize=21, color=MUTED, va='center')
fig.savefig(os.path.join(OUT, 'jeju_thumb_20261004.png'), dpi=100, facecolor=SURF); plt.close(fig)
print('jeju_thumb_20261004.png')
SLOTS = [('금 저녁', 'GMP', 'CJU', -1, '저녁'), ('토 아침', 'GMP', 'CJU', 0, '아침'), ('토 낮', 'GMP', 'CJU', 0, '낮'), ('토 저녁', 'GMP', 'CJU', 0, '저녁'),
         ('일 아침', 'CJU', 'GMP', 1, '아침'), ('일 낮', 'CJU', 'GMP', 1, '낮'), ('일 저녁', 'CJU', 'GMP', 1, '저녁'), ('월 아침', 'CJU', 'GMP', 2, '아침'), ('월 저녁', 'CJU', 'GMP', 2, '저녁')]


def slot_have(air, sat, slot):
    name, o, d, off, sl = slot
    return have(air, o, d, sat + dt.timedelta(days=off), sl)


def matrix(fn, air):
    X0, CW, RH = 212, 92, 44
    H = 310 + RH * len(SAT) + 120
    fig, ax = canvas(H)
    ax.text(40, 62, '%s 주말 제주 마일리지 좌석 한눈에' % AIR[air], fontsize=36, fontweight='bold', color=COL[air], va='center')
    ax.text(40, 116, '금·토 출발(김포→제주)과 일·월 복귀(제주→김포) · 칸 안 숫자는 좌석 있는 편 수', fontsize=20, color=INK2, va='center')
    ax.text(X0 + CW * 2, 176, '김포 → 제주', fontsize=21, fontweight='bold', color=INK, ha='center', va='center')
    ax.text(X0 + CW * 6.5, 176, '제주 → 김포', fontsize=21, fontweight='bold', color=INK, ha='center', va='center')
    ax.plot([X0 + CW * 4 - 2, X0 + CW * 4 - 2], [160, 310 + RH * len(SAT)], color='#c3c2b7', lw=1)
    for j, sl in enumerate(SLOTS):
        ax.text(X0 + CW * j + CW / 2, 222, sl[0], fontsize=18, color=INK2, ha='center', va='center')
    ax.plot([40, W - 40], [250, 250], color='#c3c2b7', lw=1)
    y = 262
    for sat in SAT:
        ax.text(40, y + RH / 2, '%d/%d 주말' % (sat.month, sat.day), fontsize=20, color=INK, va='center')
        for j, sl in enumerate(SLOTS):
            h = slot_have(air, sat, sl)
            x = X0 + CW * j
            if h is None:
                ax.add_patch(Rectangle((x + 3, y + 4), CW - 6, RH - 8, facecolor=SURF, edgecolor=GRID, lw=1))
                ax.text(x + CW / 2, y + RH / 2, '-', fontsize=15, color=MUTED, ha='center', va='center')
            elif h:
                ax.add_patch(Rectangle((x + 3, y + 4), CW - 6, RH - 8, facecolor=COL[air], edgecolor='none'))
                ax.text(x + CW / 2, y + RH / 2, '%d' % len(h), fontsize=19, fontweight='bold', color=SURF, ha='center', va='center')
            else:
                ax.add_patch(Rectangle((x + 3, y + 4), CW - 6, RH - 8, facecolor=NONE, edgecolor='none'))
                ax.text(x + CW / 2, y + RH / 2, '0', fontsize=17, color=MUTED, ha='center', va='center')
        y += RH
    ax.plot([40, W - 40], [y + 6, y + 6], color='#c3c2b7', lw=1)
    ax.text(40, y + 34, '아침 = 10시 전 출발, 낮 = 10~17시, 저녁 = 17시 이후 · 「-」는 달력에 편이 안 뜬 날', fontsize=16, color=MUTED, va='center')
    footer(ax, H)
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF); plt.close(fig)
    print(fn, W, 'x', H)


matrix('jeju_matrix_ke_20261004.png', 'KE')
matrix('jeju_matrix_oz_20261004.png', 'OZ')

PATTERNS = [('토 아침 → 일 저녁', ('토 아침',), ('일 저녁',)), ('토 아침 → 월 아침', ('토 아침',), ('월 아침',)), ('금 저녁 → 일 아침', ('금 저녁',), ('일 아침',)),
            ('금 저녁 → 일 저녁', ('금 저녁',), ('일 저녁',)), ('금 저녁 → 월 아침', ('금 저녁',), ('월 아침',)), ('토 저녁 → 월 저녁', ('토 저녁',), ('월 저녁',)),
            ('토 아무 때 → 월 아무 때', ('토 아침', '토 낮', '토 저녁'), ('월 아침', '월 낮', '월 저녁'))]
SL = {sl[0]: sl for sl in SLOTS}
SL['월 낮'] = ('월 낮', 'CJU', 'GMP', 2, '낮')
COMBO = {}
for air in ('KE', 'OZ'):
    for name, outs, backs in PATTERNS:
        oks = []
        for sat in SAT:
            o_ok = any(slot_have(air, sat, SL[x]) for x in outs)
            b_ok = any(slot_have(air, sat, SL[x]) for x in backs)
            if o_ok and b_ok:
                oks.append(sat.isoformat())
        COMBO['%s|%s' % (air, name)] = oks
        print(AIR[air], name, len(oks), '/', len(SAT), oks)

json.dump({'DET': DET, 'COMBO': COMBO, **{'%s|%s' % k: [[x.isoformat() for x in v[0]], [x.isoformat() for x in v[1]], [x.isoformat() for x in v[2]]] for k, v in S.items()}},
          open(os.path.join(OUT, '_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ───────── 추가 이미지 ① 시간대 점 그림: 일요일 제주→김포 / 토요일 김포→제주 좌석 있는 편의 출발 시각 ─────────
def timeline(fn, title, sub, o, d, days, mark_h=None, mark_label=''):
    X0, X1 = 230, W - 60
    def xt(hhmm):
        h, m = int(hhmm[:2]), int(hhmm[3:])
        return X0 + (X1 - X0) * ((h + m / 60) - 6) / 16  # 06:00 ~ 22:00
    RH = 40
    H = 250 + RH * len(days) + 130
    fig, ax = canvas(H)
    ax.text(40, 62, title, fontsize=36, fontweight='bold', color=INK, va='center')
    ax.text(40, 116, sub, fontsize=20, color=INK2, va='center')
    for air, lab, x in (('KE', '대한항공 좌석 있는 편', 40), ('OZ', '아시아나 좌석 있는 편', 330)):
        ax.add_patch(Rectangle((x, 152), 18, 18, facecolor=COL[air], edgecolor='none'))
        ax.text(x + 26, 161, lab, fontsize=17, color=INK2, va='center')
    ax.add_patch(Rectangle((630, 152), 18, 18, facecolor=NONE, edgecolor='none'))
    ax.text(656, 161, '편은 있지만 좌석 없음', fontsize=17, color=INK2, va='center')
    for h in range(6, 23, 2):
        x = xt('%02d:00' % h)
        ax.plot([x, x], [214, 250 + RH * len(days)], color=GRID, lw=1)
        ax.text(x, 200, '%d시' % h, fontsize=15, color=MUTED, ha='center', va='center')
    if mark_h:
        x = xt(mark_h)
        ax.plot([x, x], [214, 250 + RH * len(days)], color=INK, lw=1.2, linestyle='--')
        ax.text(x + 6, 232, mark_label, fontsize=15, color=INK, va='center')
    y = 250
    for day in days:
        ax.text(40, y + RH / 2, '%d월 %d일 (%s)' % (day.month, day.day, WD[day.weekday()]), fontsize=18, color=INK, va='center')
        for air, dy in (('KE', -8), ('OZ', 8)):
            fl = D[air].get((o, d), {}).get(day)
            if fl is None:
                continue
            for f in fl:
                on = (f['eco'] or 0) > 0
                ax.add_patch(plt.Circle((xt(f['t']), y + RH / 2 + dy), 6 if on else 3.5, facecolor=COL[air] if on else NONE, edgecolor='none'))
        y += RH
    ax.plot([40, W - 40], [y + 8, y + 8], color='#c3c2b7', lw=1)
    ax.text(40, y + 34, '점 하나가 편 하나 · 위 줄이 대한항공, 아래 줄이 아시아나 · 가로가 출발 시각', fontsize=16, color=MUTED, va='center')
    footer(ax, H)
    fig.savefig(os.path.join(OUT, fn), dpi=100, facecolor=SURF); plt.close(fig)
    print(fn, W, 'x', H)


timeline('jeju_sun_times_20261004.png', '일요일 제주→김포, 좌석 있는 편은 몇 시였나', '%d월 %d일부터 12월 27일까지 일요일 %d번 · 색칠한 점이 마일리지 좌석 있는 편' % (SUN[0].month, SUN[0].day, len(SUN)), 'CJU', 'GMP', SUN, '17:00', '17시')
timeline('jeju_sat_times_20261004.png', '토요일 김포→제주, 좌석 있는 편은 몇 시였나', '10월 10일부터 12월 26일까지 토요일 12번 · 색칠한 점이 마일리지 좌석 있는 편', 'GMP', 'CJU', SAT, '10:00', '10시')

# ───────── 추가 이미지 ② 조합 카드 ─────────
H = 200 + len(PATTERNS) * 2 * 58 + 170
fig, ax = canvas(H)
ax.text(40, 62, '주말 조합별로 열린 횟수', fontsize=36, fontweight='bold', color=INK, va='center')
ax.text(40, 116, '10월 10일부터 12월 26일까지 12주말 · 가는 편과 오는 편이 같은 주말에 둘 다 있던 수', fontsize=19, color=INK2, va='center')
y = 180
for name, outs, backs in PATTERNS:
    ax.text(40, y + 14, name, fontsize=24, fontweight='bold', color=INK, va='center')
    y += 44
    for air in ('KE', 'OZ'):
        oks = COMBO['%s|%s' % (air, name)]
        ax.add_patch(Rectangle((60, y + 3), 16, 16, facecolor=COL[air], edgecolor='none'))
        ax.text(86, y + 11, AIR[air], fontsize=19, color=INK2, va='center')
        ax.add_patch(Rectangle((200, y - 2), 420, 26, facecolor='#efeee9', edgecolor='none'))
        if oks:
            ax.add_patch(Rectangle((200, y - 2), 420 * len(oks) / len(SAT), 26, facecolor=COL[air], edgecolor='none'))
        ax.text(636, y + 11, '%d번' % len(oks), fontsize=22, fontweight='bold', color=INK, va='center')
        ds = ['%d/%d' % (int(x[5:7]), int(x[8:10])) for x in oks]
        txt = ', '.join(ds) if ds else '없음'
        if len(ds) > 6:
            txt = ', '.join(ds[:4]) + ' 외 %d주말' % (len(ds) - 4)
        ax.text(720, y + 11, txt, fontsize=15, color=MUTED, va='center', linespacing=1.3)
        y += 36
    y -= 8
    ax.plot([40, W - 40], [y + 4, y + 4], color=GRID, lw=1)
    y += 16
ax.text(40, y + 12, '막대는 12주말 중 몇 번인지 · 날짜는 그 주말의 토요일', fontsize=16, color=MUTED, va='center')
footer(ax, H)
fig.savefig(os.path.join(OUT, 'jeju_combos_20261004.png'), dpi=100, facecolor=SURF); plt.close(fig)
print('jeju_combos_20261004.png', W, 'x', H)
