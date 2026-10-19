# -*- coding: utf-8 -*-
"""로그인 실시간 결과(jeju_ke_live.json / jeju_oz_live.json) → build_jeju.py 가 읽는 압축 형식으로 바꾸고, 공개 달력과 날짜별로 비교한다.
사용: python jeju_live_convert.py
출력: data/jeju_ke_weekend_live.json, data/jeju_oz_weekend_live.json, data/_jeju_live_vs_public.txt
"""
import sys, os, json, re, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
D = lambda f: json.load(open(os.path.join(HERE, 'data', f), encoding='utf-8'))
ke, oz = D('jeju_ke_live.json'), D('jeju_oz_live.json')
kep, ozp = D('jeju_ke_weekend.json'), D('jeju_oz_weekend.json')

# 대한항공: 하루 1회 호출 → [시각, 편명, 일반석 유무, 프레스티지 유무] (좌석 수는 비고로)
ke_out, ke_cnt = {}, {}
for key, days in ke.items():
    ke_out[key] = []
    for ymd, r in sorted(days.items()):
        fl = []
        for f in r.get('flights', []):
            if f.get('segs', 1) != 1:
                continue
            ey, pr = f['cab'].get('EY'), f['cab'].get('PR')
            t = f['dep'][8:10] + ':' + f['dep'][10:12]
            fl.append('|'.join([t, f['flt'], '-' if ey is None else ('1' if ey[0] > 0 else '0'), '-' if pr is None else ('1' if pr[0] > 0 else '0')]))
            ke_cnt[(key, ymd, f['flt'])] = None if ey is None else ey[0]
        ke_out[key].append([ymd, ';'.join(fl)])
json.dump(ke_out, open(os.path.join(HERE, 'data', 'jeju_ke_weekend_live.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# 아시아나: 편별 문구 → 일반석 1/0 (마일 표시면 있음), 비즈니스 1/0
oz_out, notes = {}, []
for key, days in oz.items():
    oz_out[key] = []
    for iso, r in sorted(days.items()):
        ymd = iso.replace('-', '')
        if r.get('state') == 'nocal':
            notes.append('%s %s 달력 없음(%s)' % (key, iso, (r.get('notice') or '')[:60]))
            continue
        fl = []
        for row in r.get('rows') or []:
            e = row.get('eco'); bz = row.get('biz')
            ev = '-' if e is None else ('1' if '마일' in e else '0')
            bv = '-' if bz is None else ('1' if '마일' in bz else '0')
            fl.append('|'.join([row['dep'].replace(':', ''), row['flt'], ev, bv]))
        if not fl and r.get('state') in ('noseat', 'none', 'nodata'):
            notes.append('%s %s 편별 내역 없음(state=%s, selected=%s)' % (key, iso, r.get('state'), r.get('selected')))
        oz_out[key].append([ymd, ';'.join(fl)])
json.dump(oz_out, open(os.path.join(HERE, 'data', 'jeju_oz_weekend_live.json'), 'w', encoding='utf-8'), ensure_ascii=False)


# 비교: 날짜별 일반석 있는 편 수 (공개 vs 실시간)
def eco_set(entry):
    out = {}
    for part in (entry or '').split(';'):
        if not part:
            continue
        t, flt, e, b = part.split('|')
        out[flt] = (t if ':' in t else t[:2] + ':' + t[2:], e)
    return out


lines = ['항공사 | 방향 | 날짜 | 공개: 좌석 편 수 | 실시간: 좌석 편 수 | 공개에만 | 실시간에만']
for name, pub, live in (('대한항공', kep, ke_out), ('아시아나', ozp, oz_out)):
    for key in live:
        pd = {d: eco_set(s) for d, s in pub.get(key, [])}
        for ymd, s in live[key]:
            lv = eco_set(s)
            p = pd.get(ymd)
            lv_on = {f for f, (t, e) in lv.items() if e == '1'}
            if p is None:
                lines.append('%s | %s | %s | 달력 없음 | %d | | %s' % (name, key, ymd, len(lv_on), ','.join(sorted(lv_on))))
                continue
            p_on = {f for f, (t, e) in p.items() if e == '1'}
            lines.append('%s | %s | %s | %d | %d | %s | %s' % (name, key, ymd, len(p_on), len(lv_on), ','.join(sorted(p_on - lv_on)), ','.join(sorted(lv_on - p_on))))
open(os.path.join(HERE, 'data', '_jeju_live_vs_public.txt'), 'w', encoding='utf-8').write('\n'.join(lines + [''] + notes) + '\n')
print('\n'.join(lines))
print('\n'.join(notes))
