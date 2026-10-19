# -*- coding: utf-8 -*-
"""대한항공 보너스 좌석 실시간 조회(로그인된 전용 크롬, 하루 1회 호출)

사용: python ke_live.py ICN-LHR,LHR-ICN,... [--out data/ke_live.json] [--pace 2.4,3.4]
회원번호·이름은 페이지 안에서만 쓰고 밖으로 꺼내지 않는다. 403/429/비JSON/로그인 풀림이면 멈춘다.
"""
import sys, os, json, time, random, datetime as dt

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
opt = {}
for i, a in enumerate(sys.argv):
    if a.startswith('--') and i + 1 < len(sys.argv):
        opt[a[2:]] = sys.argv[i + 1]
ROUTES = sys.argv[1].split(',')
OUT = os.path.join(HERE, opt.get('out', 'data/ke_live.json'))
PACE = tuple(float(x) for x in opt.get('pace', '2.4,3.4').split(','))
LO, HI = dt.date(2026, 10, 2), dt.date(2026, 12, 16)
DAYS = [LO + dt.timedelta(days=i) for i in range((HI - LO).days + 1)]

CALL = r"""async ([o, d, ymd]) => {
  const ksid = sessionStorage.getItem('ksessionId');
  let u = null;
  try { u = JSON.parse(sessionStorage.getItem('loggedInUserInfo')).userInfo; } catch (e) {}
  if (!ksid || !u || !u.skypassNumber) return { stop: 'LOGIN_LOST' };
  const body = { commercialFareFamilies: ['KEBONUSNEW'], currency: '', sta: false,
    segmentList: [{ departureDate: ymd, departureAirport: o, arrivalAirport: d }],
    travelers: [{ travellerType: 'ADT', fqtvNumber: u.skypassNumber, lastName: u.englishLastName, firstName: u.englishFirstName, discountCode: '' }],
    corporateCode: 'string' };
  let r, t;
  try {
    r = await fetch('/api/ap/booking/avail/awardAvailability', { method: 'POST', credentials: 'include',
      headers: { ksessionId: ksid, timestamp: String(Date.now()), channel: 'pc', 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(body) });
    t = await r.text();
  } catch (e) { return { err: String(e).slice(0, 100) }; }
  if (r.status === 403 || r.status === 429) return { stop: 'HTTP_' + r.status };
  let j; try { j = JSON.parse(t); } catch (e) { return { stop: 'NON_JSON', http: r.status, head: t.slice(0, 80) }; }
  const b = (j.upsellBoundAvailList || [])[0];
  if (!b) return { http: r.status, code: j.code || 'NO_BOUND', msg: ((j.subMessages || [])[0] || j.message || '').slice(0, 90) };
  const K = { KEBONUSEY: 'EY', KEBONUSPR: 'PR', KEBONUSFR: 'FR', KEBONUSFC: 'FR' };
  return { http: r.status, flights: (b.availFlightList || []).map(f => {
    const fi = (f.flightInfoList || [])[0] || {};
    const cab = {};
    (f.commercialFareFamilyList || []).forEach(c => { cab[K[c.fareFamily] || c.fareFamily] = [c.soldout ? 0 : Number(c.seatCount || 0), !!c.soldout, c.totalMileage || null]; });
    return { flt: (fi.marketingAirline || fi.carrierCode || 'KE') + (fi.flightNumber || ''), op: fi.operatingAirline || '', segs: (f.flightInfoList || []).length,
             dep: f.departureDate, arr: f.arrivalDate, dur: f.totalFlyingTime || '', cab };
  }) };
}"""


def log(*a):
    print(dt.datetime.now().strftime('%H:%M:%S'), *a, flush=True)


STATE = r"""() => {
  const vis = e => !!e && e.getClientRects().length > 0;
  return { path: location.pathname, expire: vis(document.querySelector('#ksessionExpireModal')),
    dialogs: [...document.querySelectorAll('[role=dialog], [role=alertdialog]')].filter(vis).map(d => (d.id + ': ' + d.innerText.replace(/\s+/g, ' ').trim()).slice(0, 160)),
    ksid: !!sessionStorage.getItem('ksessionId'), user: !!sessionStorage.getItem('loggedInUserInfo') };
}"""
KEEP = r"""async () => {
  const ksid = sessionStorage.getItem('ksessionId');
  if (!ksid) return 'NO_KSID';
  try {
    const r = await fetch('/api/et/ibeSupport/keepAliveRedis', { credentials: 'include',
      headers: { ksessionId: ksid, timestamp: String(Date.now()), channel: 'pc', Accept: 'application/json' } });
    const t = await r.text();
    return 'HTTP ' + r.status + ' ' + t.replace(/\s+/g, ' ').slice(0, 80);
  } catch (e) { return 'ERR ' + String(e).slice(0, 80); }
}"""


def save(db):
    json.dump(db, open(OUT + '.tmp', 'w', encoding='utf-8'), ensure_ascii=False)
    os.replace(OUT + '.tmp', OUT)


def main():
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)
    except Exception:
        pass
    db = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {'res': {}, 'log': []}
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp('http://127.0.0.1:9333')
        ctx = b.contexts[0]
        cand = [x for x in ctx.pages if x.url.rstrip('/').endswith('koreanair.com/booking/search')]
        pg = cand[-1] if cand else ctx.new_page()
        if not cand:
            pg.goto('https://www.koreanair.com/booking/search', wait_until='domcontentloaded', timeout=60000)
            pg.wait_for_timeout(5000)
        bad, recov, last_keep = 0, 0, time.time()

        def note(kind, **kw):
            db['log'].append({'at': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'kind': kind, **kw})
            save(db)

        def recover(why):
            """세션이 죽은 것 같으면 검색 첫 화면을 새로 열어 세션값을 다시 받는다. 로그인은 건드리지 않는다."""
            nonlocal recov
            recov += 1
            st0 = pg.evaluate(STATE)
            log('복구 시도 %d회째 (%s) 직전 상태 %s' % (recov, why, json.dumps(st0, ensure_ascii=False)))
            if st0['expire']:  # 만료 창이 이 탭에 떠 있으면 확인을 눌러 닫는다
                try:
                    pg.locator('#ksessionExpireModal').get_by_role('button').first.click(timeout=8000)
                    log('만료 창 확인 클릭')
                except Exception as ex:
                    log('만료 창 클릭 실패', str(ex).splitlines()[0][:100])
            pg.goto('https://www.koreanair.com/booking/search', wait_until='domcontentloaded', timeout=60000)
            pg.wait_for_timeout(7000)
            st1 = pg.evaluate(STATE)
            ok = st1['ksid'] and st1['user']
            log('복구 %s, 새로 연 뒤 상태 %s' % ('성공' if ok else '실패(로그인 풀림)', json.dumps(st1, ensure_ascii=False)))
            note('recover', why=why, before=st0, after=st1, ok=ok)
            return ok and recov <= 5

        for n, key in enumerate(ROUTES, 1):
            o, d = key.split('-')
            rec = db['res'].setdefault(key, {'days': {}})
            t = time.time()
            for day in DAYS:
                ymd = day.strftime('%Y%m%d')
                if ymd in rec['days'] and 'err' not in rec['days'][ymd] and not rec['days'][ymd].get('retry'):
                    continue
                if time.time() - last_keep > 1200:  # 20분마다 사이트 자체 세션 연장 호출 + 화면 상태 기록
                    last_keep = time.time()
                    try:
                        ka = pg.evaluate(KEEP)
                        st = pg.evaluate(STATE)
                        log('세션 연장 호출', ka, '| 상태', json.dumps(st, ensure_ascii=False))
                        note('keepalive', result=ka, state=st)
                    except Exception as ex:
                        log('세션 연장 호출 실패', str(ex).splitlines()[0][:100])
                for attempt in (1, 2):
                    try:
                        r = pg.evaluate(CALL, [o, d, ymd])
                    except Exception as ex:
                        r = {'err': str(ex).splitlines()[0][:120]}
                    r['at'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    hard = r.get('stop') in ('HTTP_403', 'HTTP_429', 'NON_JSON')
                    soft = r.get('stop') == 'LOGIN_LOST' or 'err' in r or (r.get('code') and r['code'] != 'ERT.7190')
                    if hard:
                        log('STOP', key, ymd, r)
                        note('stop', key=key, ymd=ymd, **r)
                        return
                    if not soft:
                        bad = 0
                        break
                    bad += 1
                    log('주의', key, ymd, r.get('stop') or r.get('code') or r.get('err'), r.get('msg', ''))
                    # ERT.7190(그 날 줄 운임 없음)은 정상. 그 밖의 오류가 2번 이어지거나 로그인 값이 없으면 새로 열어 본다.
                    if attempt == 1 and (bad >= 2 or r.get('stop') == 'LOGIN_LOST'):
                        if not recover(r.get('stop') or r.get('code') or 'err'):
                            log('STOP 복구 불가', key, ymd)
                            note('stop', key=key, ymd=ymd, why='RECOVER_FAILED')
                            return
                        continue
                    break
                if r.get('stop') or 'err' in r or (r.get('code') and r['code'] != 'ERT.7190'):
                    r['retry'] = True  # 다음 실행 때 다시 받는다
                rec['days'][ymd] = r
                if bad >= 8:
                    log('STOP 연속 오류 8회')
                    note('stop', key=key, ymd=ymd, why='EIGHT_ERRORS')
                    return
                if len(rec["days"]) % 5 == 0:
                    save(db)
                time.sleep(random.uniform(*PACE))
            rec['done'] = True
            save(db)
            fl = [v for v in rec['days'].values() if v.get('flights')]
            ey = sum(1 for v in fl if any(f['cab'].get('EY', [0, True])[0] > 0 for f in v['flights']))
            pr = sum(1 for v in fl if any(f['cab'].get('PR', [0, True])[0] > 0 for f in v['flights']))
            log('[%d/%d] %s 편 있는 날=%d 일반석=%d 프레스티지=%d 코드응답=%d %.0fs' % (
                n, len(ROUTES), key, len(fl), ey, pr, sum(1 for v in rec['days'].values() if v.get('code')), time.time() - t))
        log('ALL DONE')


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        log('FATAL', str(ex)[:400])
