# -*- coding: utf-8 -*-
"""공공데이터포털 활용신청 뒤 실제 호출 확인 (2026-10-16).
  python datago_check.py <번호...>            # 번호 없으면 _문서\datago_apply_result_*.json 의 승인 건 전부
각 API 상세 페이지의 swagger 에서 host·basePath·첫 GET 경로를 읽어 serviceKey 만 붙여 한 번 부른다.
판정: ✅ 정상 / ✅ 키 통함(필수 인자 필요) / ⏳ 키 미등록(아직 승인 반영 전) / ⚠ 그 외. 결과는 _문서\datago_check_<날짜>.md"""
import sys, io, os, re, json, glob, datetime as dt, urllib.request as ur, urllib.parse as up
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
BLOG = r'C:\Users\user\Desktop\Blog'
KEY = json.load(io.open(os.path.expandvars(r'%LOCALAPPDATA%\ContentTrendRadar\datago.json'), encoding='utf-8'))['service_key']
UA = {'User-Agent': 'Mozilla/5.0'}

def ids_from_results():
    out = ['15127578', '15134735']
    for f in sorted(glob.glob(os.path.join(BLOG, '_문서', 'datago_apply_result_*.json'))):
        d = json.load(io.open(f, encoding='utf-8'))
        out += [k for k, v in d.items() if v.get('ok')]
    return list(dict.fromkeys(out))

def swagger(pk):
    s = ur.urlopen(ur.Request('https://www.data.go.kr/data/%s/openapi.do' % pk, headers=UA), timeout=40).read().decode('utf-8', 'replace')
    title = (re.search(r'<title>([^<|]+)', s) or [None, '?'])[1].strip()
    m = re.search(r'swaggerJson = `(.*?)`', s, re.S)
    if not m: return title, None
    try: j = json.loads(m.group(1))
    except Exception: return title, None
    return title, j

def first_get(j):
    host = j.get('host', ''); base = j.get('basePath', '') or ''
    for path, v in (j.get('paths') or {}).items():
        if isinstance(v, dict) and 'get' in v:
            ps = v['get'].get('parameters', []) or v.get('parameters', []) or []
            req = [p.get('name') for p in ps if isinstance(p, dict) and p.get('required') and p.get('name') not in ('serviceKey', 'ServiceKey')]
            return host, base, path, req
    return host, base, None, []

def call(url):
    try:
        r = ur.urlopen(ur.Request(url, headers=UA), timeout=25); return r.status, r.read(4000).decode('utf-8', 'replace')
    except Exception as e:
        body = ''
        try: body = e.read(2000).decode('utf-8', 'replace')
        except Exception: pass
        return getattr(e, 'code', str(e)[:40]), body

def judge(status, body):
    b = body.upper()
    if 'NORMAL SERVICE' in b or '"RESULTCODE":"00"' in b.replace(' ', '') or '<RESULTCODE>00<' in b.replace(' ', ''): return '✅ 정상'
    if 'NOT REGISTERED' in b or '등록되지 않은' in body or 'UNREGISTERED' in b or '"RETURNREASONCODE":"30"' in b.replace(' ', '') or '>30<' in b: return '⏳ 키 미등록(승인 반영 전)'
    if 'NO_OPENAPI_SERVICE' in b or '폐기' in body or 'RETURNREASONCODE":"12"' in b.replace(' ', ''): return '⚠ 서비스 없음(주소 다름)'
    if 'PARAMETER' in b or '파라미터' in body or '필수' in body or 'MANDATORY' in b or 'INVALID REQUEST' in b or 'RETURNREASONCODE":"10"' in b.replace(' ', '') or 'MISSING' in b or 'BAD REQUEST' in b: return '✅ 키 통함(필수 인자 필요)'
    if 'LIMITED' in b or 'EXCEEDS' in b or '"22"' in b: return '✅ 키 통함(한도)'
    if 'HTTP_ERROR' in b or 'RETURNREASONCODE":"04"' in b.replace(' ', ''): return '⚠ 기관 서버 오류(04)'
    if 'ACCESS DENIED' in b or status == 403: return '⚠ 403'
    if isinstance(status, int) and 200 <= status < 300 and body.strip(): return '✅ 응답 있음(판정 불명)'
    return '⚠ %s' % status

def main():
    ids = [a for a in sys.argv[1:] if a.isdigit()] or ids_from_results()
    rows = []
    for pk in ids:
        try:
            title, j = swagger(pk)
            if not j: rows.append((pk, title, '-', '⚠ swagger 없음')); print(pk, title[:30], '⚠ swagger 없음'); continue
            host, base, path, req = first_get(j)
            if not path: rows.append((pk, title, '-', '⚠ GET 경로 없음')); print(pk, title[:30], '⚠ GET 없음'); continue
            url = 'https://%s%s%s?' % (host, base, path) + up.urlencode({'serviceKey': KEY, 'pageNo': 1, 'numOfRows': 1, 'type': 'json', '_type': 'json'})
            st, body = call(url); verdict = judge(st, body)
            if req and '정상' not in verdict and '통함' not in verdict and '미등록' not in verdict: verdict += ' · 필수 %s' % ','.join(req[:4])
            rows.append((pk, title, host + base + path, verdict)); print(pk, title[:36], '→', verdict, '|', body[:90].replace('\n', ' '))
        except Exception as e:
            rows.append((pk, '?', '-', '⚠ 예외 ' + str(e)[:60])); print(pk, '예외', str(e)[:80])
    today = dt.date.today().isoformat()
    L = ['# 공공데이터포털 승인 API 호출 확인 — %s %s' % (today, dt.datetime.now().strftime('%H:%M')), '', '| 번호 | API | 경로 | 판정 |', '|---|---|---|---|']
    L += ['| %s | %s | `%s` | %s |' % r for r in rows]
    ok = sum(1 for r in rows if r[3].startswith('✅')); wait = sum(1 for r in rows if r[3].startswith('⏳'))
    L += ['', '- ✅ %d · ⏳ %d · ⚠ %d / %d' % (ok, wait, len(rows) - ok - wait, len(rows))]
    io.open(os.path.join(BLOG, '_문서', 'datago_check_%s.md' % today), 'w', encoding='utf-8').write('\n'.join(L))
    print('\n'.join(L[-1:]))

if __name__ == '__main__':
    main()
