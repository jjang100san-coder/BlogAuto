# -*- coding: utf-8 -*-
"""ideas_data.py → 글감판.html(아티팩트) + 글감_카테고리별_종합.md. 실행: python build_board.py"""
import io, json, os, sys, datetime as dt, hashlib
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ideas_data import APIS, CATS, GROUPS, DONE

STATUS_ORDER = ['연결됨', '신청', '가입', '원문']
STATUS_LABEL = {'연결됨': '지금 바로', '신청': '공공데이터포털 신청', '가입': '별도 사이트 가입', '원문': '원문 직접'}

def need(apis):
    """글감 하나의 준비 상태: 신청·가입이 하나라도 있으면 그 단계, 아니면 바로."""
    st = [APIS[a][2] for a in apis]
    if '가입' in st: return '가입'
    if '신청' in st: return '신청'
    return '바로'

data = {'cats': [], 'apis': {}, 'groups': [], 'done': [{'d': d, 'cat': c, 't': t, 'by': w} for d, c, t, w in DONE]}
used = {}
for ci, (cat, desc, items) in enumerate(CATS):
    rows = []
    for ii, (t, memo, apis) in enumerate(items):
        for a in apis: assert a in APIS, a
        iid = hashlib.md5((cat + '|' + t).encode('utf-8')).hexdigest()[:8]   # 10/16 자리 번호 → 제목 해시 (갈래를 옮겨도 ★ 유지)
        rows.append({'id': iid, 't': t, 'm': memo, 'a': apis, 'need': need(apis)})
        for a in apis: used.setdefault(a, []).append(iid)
    data['cats'].append({'name': cat, 'desc': desc, 'items': rows})
for k, (nm, where, st, star) in APIS.items():
    data['apis'][k] = {'name': nm, 'where': where, 'st': st, 'star': star, 'used': used.get(k, [])}
catnames = {c['name'] for c in data['cats']}
grouped = set()
for g, gdesc, names in GROUPS:
    for n in names: assert n in catnames, '묶음에 없는 갈래: ' + n
    grouped |= set(names)
    data['groups'].append({'name': g, 'desc': gdesc, 'cats': names})
missing = [c for c in catnames if c not in grouped]
assert not missing, '묶음에 안 들어간 갈래: %s' % missing
total = sum(len(c['items']) for c in data['cats'])
today = dt.date.today().isoformat()
data['meta'] = {'total': total, 'cats': len(CATS), 'groups': len(GROUPS), 'date': today}

# ── md
L = ['# 카테고리별 글감 종합 (%s)' % today, '',
     '발행판과 별개의 글감 창고. 2026-10-11~14 브레인스토밍에서 나온 글감 %d개, %d갈래. 원본 데이터 `ideas_data.py`, 생성 `build_board.py`.' % (total, len(CATS)),
     '준비 상태: 「바로」는 연결된 자료·원문·내 기록만으로 됨, 「신청」은 공공데이터포털 활용신청, 「가입」은 별도 사이트 키가 필요.', '']
bycat = {c['name']: c for c in data['cats']}
for g in data['groups']:
    L += ['## %s (%d)' % (g['name'], sum(len(bycat[n]['items']) for n in g['cats'])), '_%s_' % g['desc'], '']
    for n in g['cats']:
        c = bycat[n]
        L += ['### %s (%d)' % (c['name'], len(c['items']))] + (['_%s_' % c['desc']] if c['desc'] else []) + ['', '| 준비 | 글감 | 메모 | 자료 |', '|---|---|---|---|']
        for r in c['items']:
            L.append('| %s | %s | %s | %s |' % (r['need'], r['t'].replace('|', '\\|'), r['m'].replace('|', '\\|'), ' · '.join(APIS[a][0] for a in r['a'])))
        L.append('')
L += ['## ✅ 발행·예약으로 빠진 글감 (%d)' % len(DONE), '', '| 날짜 | 갈래 | 글감 | 겹친 글 |', '|---|---|---|---|'] + ['| %s | %s | %s | %s |' % (d, c, t.replace('|', '\\|'), w.replace('|', '\\|')) for d, c, t, w in DONE] + ['']
L += ['## 필요한 API', '']
for st in STATUS_ORDER:
    ks = [k for k, v in data['apis'].items() if v['st'] == st]
    L += ['### %s (%d)' % (STATUS_LABEL[st], len(ks)), '', '| ★ | 이름 | 어디서 | 쓰는 글감 수 |', '|---|---|---|---|']
    for k in sorted(ks, key=lambda k: (data['apis'][k]['star'] != '★', -len(data['apis'][k]['used']))):
        v = data['apis'][k]
        L.append('| %s | %s | %s | %d |' % (v['star'], v['name'], v['where'], len(v['used'])))
    L.append('')
md_path = os.path.join(os.path.dirname(HERE), '글감_카테고리별_종합_%s.md' % today)
io.open(md_path, 'w', encoding='utf-8').write('\n'.join(L))

# ── html
tpl = io.open(os.path.join(HERE, 'board_template.html'), encoding='utf-8').read()
html = tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False))
io.open(os.path.join(HERE, '글감판.html'), 'w', encoding='utf-8').write(html)
print('글감 %d · 갈래 %d · 묶음 %d · API %d' % (total, len(CATS), len(GROUPS), len(APIS)))
print('md  ', md_path)
print('html', os.path.join(HERE, '글감판.html'), len(html))
for st in STATUS_ORDER: print(' ', st, sum(1 for v in data['apis'].values() if v['st'] == st))
print('  준비 상태', {s: sum(1 for c in data['cats'] for r in c['items'] if r['need'] == s) for s in ('바로', '신청', '가입')})
