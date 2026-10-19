# -*- coding: utf-8 -*-
"""두 정리 md 파일을 읽어 template.html 에 데이터로 넣고 wedding.html 을 만든다.

md 를 고친 뒤 이 스크립트를 다시 돌리고 같은 경로로 재발행하면 주소가 유지된다.
항목 id 는 '문서+절 번호+문장' 해시라서, 문장을 고치면 그 항목의 체크는 초기화된다.
"""
import hashlib
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.dirname(HERE)
DOCS = [
    ('a', os.path.join(BLOG, '결혼준비_체크리스트_블로그종합_2026-10-02.md')),
    ('m', os.path.join(BLOG, '모바일청첩장_주의사항_팁_블로그종합_2026-10-02.md')),
]
# 절 번호 -> 탭. 나머지는 참고 탭.
TABS = {
    'a': {k: 'plan' for k in ['★', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']},
    'm': {k: 'mobile' for k in ['1', '2', '3', '4', '5', '6', '7', '8', '9']},
}


def sec_key(title):
    m = re.match(r'(★|\d+)', title)
    return m.group(1) if m else title[:6]


def parse(doc, path):
    lines = io.open(path, encoding='utf-8').read().split('\n')
    sections = []
    cur = None
    table = None
    seen = set()

    def flush_table():
        nonlocal table
        if table and cur is not None:
            head, rows = table[0], [r for r in table[1:] if not all(re.match(r'^:?-+:?$', c) for c in r)]
            cur['blocks'].append({'t': 'table', 'head': head, 'rows': rows})
        table = None

    for raw in lines:
        ln = raw.rstrip()
        if ln.startswith('|'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            table = (table or []) + [cells]
            continue
        flush_table()
        if not ln.strip() or ln.strip() == '---' or ln.startswith('# '):
            continue
        if ln.startswith('## '):
            title = ln[3:].strip()
            key = sec_key(title)
            cur = {'doc': doc, 'key': key, 'title': title, 'tab': TABS[doc].get(key, 'ref'), 'blocks': []}
            sections.append(cur)
            continue
        if cur is None:
            continue
        s = ln.strip()
        if ln.startswith('### '):
            cur['blocks'].append({'t': 'h3', 'x': ln[4:].strip()})
        elif re.match(r'^- \[ \] ', s):
            text = s[6:].strip()
            base = '{}|{}|{}'.format(doc, cur['key'], text)
            iid = doc + hashlib.md5(base.encode('utf-8')).hexdigest()[:9]
            while iid in seen:
                iid += 'x'
            seen.add(iid)
            cur['blocks'].append({'t': 'c', 'id': iid, 'x': text, 'lv': 1 if ln.startswith('  ') else 0})
        elif s.startswith('- '):
            cur['blocks'].append({'t': 'li', 'x': s[2:].strip(), 'lv': 1 if ln.startswith('  ') else 0})
        elif s.startswith('> '):
            cur['blocks'].append({'t': 'q', 'x': s[2:].strip()})
        elif re.match(r'^\*\*[^*]+\*\*$', s):
            cur['blocks'].append({'t': 'h4', 'x': s.strip('*')})
        else:
            cur['blocks'].append({'t': 'p', 'x': s})
    flush_table()
    return sections


def main():
    sections = []
    for doc, path in DOCS:
        sections += parse(doc, path)
    n = sum(1 for s in sections for b in s['blocks'] if b['t'] == 'c')
    data = json.dumps({'sections': sections}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    tpl = io.open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    assert '/*__DATA__*/null' in tpl
    out = tpl.replace('/*__DATA__*/null', data)
    io.open(os.path.join(HERE, 'wedding.html'), 'w', encoding='utf-8', newline='\n').write(out)
    print('sections', len(sections), 'checks', n, 'bytes', len(out.encode('utf-8')))
    for s in sections:
        print(' ', s['doc'], s['key'].ljust(2), s['tab'].ljust(6), sum(1 for b in s['blocks'] if b['t'] == 'c'), s['title'][:40])


if __name__ == '__main__':
    main()
