# -*- coding: utf-8 -*-
"""대한항공 실시간 보너스 좌석 — 지정한 날짜만 (로그인된 전용 크롬, 하루 1회 호출)
사용: python ke_dates.py <출력json> <O-D:YYYYMMDD,YYYYMMDD,...> [<O-D:...> ...]
"""
import sys, os, json, time, random, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
import guardutil as G
sys.argv_backup = sys.argv[:]
sys.argv = ['ke_live.py', 'X-X', '--out', 'data/_unused.json']
from ke_live import CALL, STATE  # 호출 JS 재사용

OUT = sys.argv_backup[1]
JOBS = []
for a in sys.argv_backup[2:]:
    key, ds = a.split(':')
    JOBS.append((key, ds.split(',')))


def log(*a):
    print(dt.datetime.now().strftime('%H:%M:%S'), *a, flush=True)


res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp(G.CDP)
    ctx = b.contexts[0]
    cand = [x for x in ctx.pages if 'koreanair.com' in x.url and '/booking/search' in x.url]
    pg = cand[-1] if cand else ctx.new_page()
    if not cand:
        pg.goto('https://www.koreanair.com/booking/search', wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(6000)
    st = pg.evaluate(STATE)
    log('상태', json.dumps(st, ensure_ascii=False))
    if not st['user']:
        log('STOP 로그인 안 됨')
        sys.exit(2)
    G.ensure_guard()
    bad = 0
    for key, dates in JOBS:
        o, d = key.split('-')
        rec = res.setdefault(key, {})
        for ymd in dates:
            if ymd in rec and not rec[ymd].get('stop') and 'err' not in rec[ymd]:
                continue
            G.beat('ke')
            r = pg.evaluate(CALL, [o, d, ymd])
            r['at'] = G.ts()
            if r.get('stop') in ('HTTP_403', 'HTTP_429', 'NON_JSON', 'LOGIN_LOST'):
                log('STOP', key, ymd, r)
                json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
                sys.exit(3)
            rec[ymd] = r
            n = len(r.get('flights', []))
            ey = sum(1 for f in r.get('flights', []) if (f['cab'].get('EY') or [0])[0] > 0)
            log(key, ymd, '편', n, '일반석', ey, r.get('code', ''))
            json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
            time.sleep(random.uniform(2.0, 2.8))
log('ALL DONE')
