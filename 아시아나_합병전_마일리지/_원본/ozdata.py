# -*- coding: utf-8 -*-
"""아시아나 합병 전 76일 데이터 헬퍼: 노선·방향·등급별 좌석 있는 날짜 목록"""
import json, os, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
LO, HI = dt.date(2026, 10, 2), dt.date(2026, 12, 16)
DAYS = []
_d = LO
while _d <= HI:
    DAYS.append(_d)
    _d += dt.timedelta(days=1)
N = len(DAYS)  # 76

res, SOURCE_AT = {}, None
for f in ('main.json', 'scan2.json'):
    j = json.load(open(os.path.join(HERE, f), encoding='utf-8'))
    SOURCE_AT = j.get('sourceAt') or SOURCE_AT
    res.update(j['res'])

NAME = {'ICN': '인천', 'GMP': '김포', 'PUS': '부산', 'CJU': '제주', 'CJJ': '청주', 'TAE': '대구', 'KWJ': '광주', 'RSU': '여수',
        'LAX': 'LA', 'JFK': '뉴욕', 'SFO': '샌프란시스코', 'SEA': '시애틀',
        'LHR': '런던', 'CDG': '파리', 'FRA': '프랑크푸르트', 'FCO': '로마', 'MXP': '밀라노', 'BCN': '바르셀로나', 'PRG': '프라하', 'IST': '이스탄불',
        'SYD': '시드니', 'ALA': '알마티', 'TAS': '타슈켄트',
        'MNL': '마닐라', 'KTI': '프놈펜', 'SGN': '호찌민', 'HKT': '푸껫', 'HAN': '하노이', 'DAD': '다낭', 'CRK': '클락', 'BKK': '방콕',
        'SIN': '싱가포르', 'CGK': '자카르타', 'CXR': '나트랑',
        'NRT': '도쿄 나리타', 'HND': '도쿄 하네다', 'KIX': '오사카', 'FUK': '후쿠오카', 'NGO': '나고야', 'CTS': '삿포로', 'OKA': '오키나와',
        'SDJ': '센다이', 'KMI': '미야자키', 'UKB': '고베',
        'PEK': '베이징', 'PVG': '상하이 푸동', 'SHA': '상하이 훙차오', 'CAN': '광저우', 'SZX': '선전', 'DLC': '다롄', 'HGH': '항저우', 'TSN': '톈진',
        'HKG': '홍콩', 'TPE': '타이베이', 'UBN': '울란바타르'}


def nm(a):
    return NAME.get(a, a)


def avail(o, d, cab):
    """좌석 1석 이상 있던 날짜(date) 목록"""
    k = o + '-' + d
    out = []
    if k not in res:
        return out
    for day in DAYS:
        row = res[k]['days'].get(day.strftime('%Y%m%d'))
        if row and sum(q for _, _, q in row[cab]) > 0:
            out.append(day)
    return out


def listed(o, d, cab):
    """달력에 편이 뜬 날짜 목록"""
    k = o + '-' + d
    out = []
    if k not in res:
        return out
    for day in DAYS:
        row = res[k]['days'].get(day.strftime('%Y%m%d'))
        if row and row[cab]:
            out.append(day)
    return out


def fmt(dates):
    """[date] -> '10월 2~6일·8~11일, 12월 4일'"""
    if not dates:
        return ''
    runs, s, p = [], dates[0], dates[0]
    for d in dates[1:]:
        if d == p + dt.timedelta(days=1):
            p = d
            continue
        runs.append((s, p))
        s = p = d
    runs.append((s, p))
    bym = {}
    for a, b in runs:
        if a.month == b.month:
            bym.setdefault(a.month, []).append(str(a.day) if a == b else '{}~{}'.format(a.day, b.day))
        else:  # 달을 넘는 구간은 쪼갠다
            last = (dt.date(a.year, a.month + 1, 1) - dt.timedelta(days=1)).day
            bym.setdefault(a.month, []).append(str(a.day) if a.day == last else '{}~{}'.format(a.day, last))
            bym.setdefault(b.month, []).append('1' if b.day == 1 else '1~{}'.format(b.day))
    return ', '.join('{}월 {}일'.format(m, '·'.join(v)) for m, v in sorted(bym.items()))


def short(dates):
    """이미지용 짧은 표기 '10/2~6, 10/8~11, 12/4'"""
    if not dates:
        return ''
    runs, s, p = [], dates[0], dates[0]
    for d in dates[1:]:
        if d == p + dt.timedelta(days=1):
            p = d
            continue
        runs.append((s, p))
        s = p = d
    runs.append((s, p))
    out = []
    for a, b in runs:
        if a == b:
            out.append('{}/{}'.format(a.month, a.day))
        elif a.month == b.month:
            out.append('{}/{}~{}'.format(a.month, a.day, b.day))
        else:
            out.append('{}/{}~{}/{}'.format(a.month, a.day, b.month, b.day))
    return ', '.join(out)


def missing(o, d, cab):
    have = set(avail(o, d, cab))
    return [x for x in DAYS if x not in have]


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print('N', N, SOURCE_AT)
    for a, b in [('ICN', 'JFK'), ('ICN', 'LAX'), ('ICN', 'SFO'), ('ICN', 'SEA'), ('ICN', 'LHR'), ('ICN', 'CDG'), ('ICN', 'FRA'), ('ICN', 'FCO'),
                 ('ICN', 'MXP'), ('ICN', 'BCN'), ('ICN', 'PRG'), ('ICN', 'IST'), ('ICN', 'SYD'), ('ICN', 'ALA'), ('ICN', 'TAS'),
                 ('ICN', 'BKK'), ('ICN', 'SIN'), ('ICN', 'CGK'), ('ICN', 'DAD'), ('ICN', 'CRK'), ('ICN', 'NRT'), ('ICN', 'HND'), ('GMP', 'HND'), ('ICN', 'KIX'), ('ICN', 'FUK')]:
        for o, d in ((a, b), (b, a)):
            y, c = avail(o, d, 'Y'), avail(o, d, 'C')
            my = missing(o, d, 'Y')
            print('{}→{} | 일반석 {}일 (편 뜬 날 {}) | 비즈 {}일'.format(nm(o), nm(d), len(y), len(listed(o, d, 'Y')), len(c)))
            if len(c) <= 14:
                print('     비즈 날짜:', fmt(c))
            if len(my) <= 14:
                print('     일반석 없는 날:', fmt(my))
            elif len(y) <= 50:
                print('     일반석 있는 날:', fmt(y))
