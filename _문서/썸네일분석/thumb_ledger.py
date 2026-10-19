# -*- coding: utf-8 -*-
"""썸네일 장부 — 마스터 5-4 「세 질문」 빅분석 도구 (2026-10-15).

장부 ledger.json 한 줄 = 글 하나: 제목·꼴·종류(P 내 사진/A AI/C 카드/G 그래프/S 포스터·캡처)·①②③(2=○ 1=△ 0=✕)
·채점 시점(blind = 발행 전에 매겼나)·글 번호·발행일·기간별 조회수.

  python thumb_ledger.py init                      # 기준선 150편(사후 채점) + 예약 28편(발행 전 채점)으로 장부를 만든다
  python thumb_ledger.py scan                      # 10/15 이후 초안의 경유표 「썸네일」 칸(①○②○③○)을 읽어 장부에 더한다
  python thumb_ledger.py views <엑셀 경로...>       # 블로그 통계 조회수 순위 엑셀(주간·월간)을 붙인다
  python thumb_ledger.py report                    # 세 질문 점수별·종류별 조회수 비교 (기준선 / 10/15 이후 따로)
"""
import io, os, re, sys, json, glob, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); L = os.path.join(HERE, 'ledger.json')
nrm = lambda s: re.sub(r'[\s|·,:~\-—()\[\]!?「」"\'.]', '', s or '')
BLOG = r'C:\Users\user\Desktop\Blog'

def load(): return json.load(io.open(L, encoding='utf-8')) if os.path.exists(L) else {}
def save(d): json.dump(d, io.open(L, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def cmd_init():
    sys.path.insert(0, HERE)
    from baseline_scores import S as BS
    from reserved_scores import S as RS
    d = {}
    V = json.load(io.open(os.path.join(HERE, 'views_baseline_2026-10-15.json'), encoding='utf-8'))
    for p in V.values():
        t, a, b, c = BS[p['rank']]
        d[nrm(p['title'])[:30]] = dict(title=p['title'], id=p['id'], date=p['date'], type=t, q=[a, b, c], src='기준선', blind=False,
                                       scored='2026-10-15', views={k: v for k, v in p['v'].items()})
    R = json.load(io.open(os.path.join(HERE, 'reserved_thumbs.json'), encoding='utf-8'))
    for r in R:
        if r['n'] not in RS: continue
        t, a, b, c, memo = RS[r['n']]
        d[nrm(r['title'])[:30]] = dict(title=r['title'], id='', date=r['dt'][:10].replace('-', ''), type=t, q=[a, b, c], src='예약(새 로직 전)',
                                       blind=True, scored='2026-10-15', memo=memo, views={})
    save(d); print('장부', len(d), '편')

def cmd_scan():
    d = load(); n = 0
    since = dt.datetime(2026, 10, 15).timestamp()
    files = glob.glob(os.path.join(BLOG, '_1.컨텐츠', '**', '*_draft.md'), recursive=True) + \
            glob.glob(os.path.join(BLOG, '_1.컨텐츠', '**', '초안_*.md'), recursive=True)   # 구구절절 등은 초안_<주제>.md (10/15)
    for f in files:
        if os.path.getmtime(f) < since: continue
        s = io.open(f, encoding='utf-8').read()
        m = re.search(r'\[\[TITLE:\s*(.+?)\]\]', s); row = re.search(r'^\|\s*썸네일[^|]*\|(.+)\|\s*$', s, re.M)
        if not (m and row): continue
        v = row.group(1)
        q = [{'○': 2, '△': 1, '✕': 0, 'x': 0, 'X': 0}.get((re.search(k + r'\s*([○△✕xX])', v) or [None, ''])[1]) for k in ('①', '②', '③')]
        if None in q: continue
        typ = 'P' if '사진' in v else 'A' if 'AI' in v else 'C' if '카드' in v else '?'
        k = nrm(m.group(1))[:30]
        e = d.get(k, {}); e.update(title=m.group(1).strip(), type=e.get('type') or typ, q=q, src=e.get('src') or '초안(10/15 이후)', blind=True,
                                   scored=dt.date.fromtimestamp(os.path.getmtime(f)).isoformat(), draft=f); e.setdefault('views', {}); e.setdefault('id', ''); e.setdefault('date', '')
        d[k] = e; n += 1
    save(d); print('초안에서 읽음', n, '편 · 장부', len(d), '편')

def cmd_views(paths):
    import openpyxl
    d = load(); byk = {k: e for k, e in d.items()}
    for f in paths:
        ws = openpyxl.load_workbook(f, data_only=True).worksheets[0]
        rows = list(ws.iter_rows(values_only=True))
        unit = rows[2][1]; period = rows[3][1]; lab = '%s %s' % (unit, period.split()[0])
        hit = 0
        for r in rows[7:]:
            if not r or not r[1] or not str(r[0]).isdigit(): continue
            k = nrm(r[1])[:30]; e = byk.get(k) or next((x for kk, x in byk.items() if kk[:18] == k[:18]), None)
            if not e: continue
            e['views'][lab] = int(r[2]); hit += 1
            if not e.get('date') or len(e['date']) < 8: e['date'] = str(r[3])[:11].replace('. ', '').replace('.', '')
        print(os.path.basename(f), lab, '장부와 맞은 글', hit)
    save(d)

def cmd_report():
    import statistics as st
    d = load()
    def grp(rows, lab):
        if not rows: return
        vals = [sum(e['views'].values()) for e in rows]
        print('  %-24s %3d편  조회 합 중앙값 %6.0f  평균 %7.1f' % (lab, len(rows), st.median(vals), st.mean(vals)))
    for src, nm in (('기준선', '㉮ 기준선 — 10/15 이전 발행 (사후 채점)'), ('예약(새 로직 전)', '㉯ 새 로직 전 — 10/15 이전 예약 (발행 전 채점)'), ('초안(10/15 이후)', '㉰ 새 로직 — 10/15 이후 초안 (세 질문 강제)')):
        rows = [e for e in d.values() if e['src'] == src and e['views']]
        print('== %s — 조회수 있는 글 %d편' % (nm, len(rows)))
        grp([e for e in rows if e['q'] == [2, 2, 2]], '세 질문 모두 ○')
        grp([e for e in rows if 0 not in e['q'] and e['q'] != [2, 2, 2]], '✕ 없음 · △ 있음')
        grp([e for e in rows if 0 in e['q']], '✕ 하나 이상')
        for i, qn in enumerate('①②③'):
            for v, l in ((2, '○'), (1, '△'), (0, '✕')): grp([e for e in rows if e['q'][i] == v], '%s %s' % (qn, l))
        for t, tn in (('P', '내 사진'), ('A', 'AI'), ('C', '카드'), ('G', '그래프'), ('S', '포스터·캡처')): grp([e for e in rows if e['type'] == t], '종류 ' + tn)

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    {'init': lambda: cmd_init(), 'scan': lambda: cmd_scan(), 'views': lambda: cmd_views(a[1:]), 'report': lambda: cmd_report()}[a[0]]()
