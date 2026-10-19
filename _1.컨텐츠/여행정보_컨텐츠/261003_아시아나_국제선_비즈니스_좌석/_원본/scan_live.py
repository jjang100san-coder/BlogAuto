# -*- coding: utf-8 -*-
"""아시아나 마일리지 예매 화면(로그인·실시간) 달력 수집기

조회 전용 크롬(--remote-debugging-port=9333, 사용자가 직접 로그인)에 붙어서
편도 조회 → 결과 화면 달력(조회기간 약 31일)의 좌석 표시를 읽는다.
예매·결제 단계로는 넘어가지 않는다. 403/Access Denied/로그인 풀림이면 즉시 멈춘다.

사용: python scan_live.py ICN-LAX,LAX-ICN [--out data/live.json] [--pace 8,12]
      python scan_live.py @routes.json
"""
import sys, os, json, time, re, random, datetime as dt, traceback

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
import guardutil as G

HERE = os.path.dirname(os.path.abspath(__file__))
FORM = 'https://flyasiana.com/I/KR/KO/RedemptionRegistTravel.do'
LO, HI = dt.date(2026, 10, 2), dt.date(2026, 12, 16)
KR = {'ICN', 'GMP', 'PUS', 'CJU', 'CJJ', 'TAE', 'KWJ', 'RSU', 'USN'}
CALJS = open(os.path.join(HERE, 'calparse.js'), encoding='utf-8').read()
ROWJS = r"""() => [...document.querySelectorAll('#avail_Area1 tr, #depAvail_Area tr')].filter(tr => tr.querySelector('td.economy_area, td.business_area')).map(tr => {
  const t = e => e ? e.innerText.replace(/\s+/g, ' ').trim().slice(0, 60) : null;
  const flt = (tr.innerText.match(/OZ\s?\d{3,4}/) || [''])[0].replace(/\s/g, '');
  const tm = (tr.innerText.match(/\d{2}:\d{2}/) || [''])[0];
  const dur = (tr.innerText.match(/\d+시간\s*\d*분?/) || [''])[0];
  return { flt, dep: tm, dur, eco: t(tr.querySelector('td.economy_area')), biz: t(tr.querySelector('td.business_area')) };
})"""

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = {}
for i, a in enumerate(sys.argv):
    if a.startswith('--') and i + 1 < len(sys.argv):
        opt[a[2:]] = sys.argv[i + 1]
args = [a for a in args if a not in opt.values()]
OUT = os.path.join(HERE, opt.get('out', 'data/live.json'))
PACE = tuple(float(x) for x in opt.get('pace', '8,12').split(','))
CABINS = tuple(opt.get('cabins', 'AB'))  # A=전체(일반석 표시), B=비즈니스만
if args[0].startswith('@'):
    ROUTES = json.load(open(os.path.join(HERE, args[0][1:]), encoding='utf-8'))
else:
    ROUTES = args[0].split(',')


def log(*a):
    print(dt.datetime.now().strftime('%H:%M:%S'), *a, flush=True)


class Stop(Exception):
    pass


def load():
    if os.path.exists(OUT):
        return json.load(open(OUT, encoding='utf-8'))
    return {'res': {}, 'log': []}


def save(db):
    tmp = OUT + '.tmp'
    json.dump(db, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
    os.replace(tmp, OUT)


def until(pg, fn, ms=10000, step=200):
    end = time.time() + ms / 1000
    while time.time() < end:
        try:
            if fn():
                return True
        except Exception:
            pass
        pg.wait_for_timeout(step)
    return False


def pause(pg):
    G.beat('oz')
    pg.wait_for_timeout(int(random.uniform(*PACE) * 1000))


def guard(pg):
    """차단·로그아웃 감지 → Stop. 세션 연장 창은 연장을 누른다."""
    url = pg.url
    try:
        head = pg.evaluate("document.body ? document.body.innerText.slice(0, 400) : ''")
    except Exception:
        head = ''
    if re.search(r'Access Denied|errors\.edgesuite', head, re.I):
        raise Stop('ACCESS_DENIED')
    if 'viewLogin' in url or 'Login.do' in url:
        raise Stop('LOGIN_LOST')
    try:  # 예매 세션(9분)·로그인 세션(약 19분) 연장 창이 떠 있으면 연장을 누른다
        for sel in ('#ibeSessionPopCont', '#ssoSessionLayer button', '#ibeSessionCont'):
            btn = pg.locator(sel).filter(has_text='연장')
            if btn.count() and btn.first.is_visible():
                btn.first.click(timeout=5000)
                log('세션 연장 클릭', sel)
                pg.wait_for_timeout(1500)
                break
    except Exception:
        pass


def pick_airport(pg, field, code):
    inp = pg.locator('#txt%sAirport1' % field)
    lst = pg.locator('#div%sAirportAC1 li' % ('Dep' if field == 'Departure' else 'Arr')).filter(has_text=code)
    inp.click(timeout=8000)
    inp.fill('')
    inp.press_sequentially(code, delay=140)
    try:
        lst.first.wait_for(timeout=10000)
    except Exception:
        raise RuntimeError('ROUTE_UNAVAILABLE')
    lst.first.click()
    hid = '#%sAirport1' % ('departure' if field == 'Departure' else 'arrival')
    if not until(pg, lambda: pg.locator(hid).input_value() == code):
        raise RuntimeError('AIRPORT_NOT_COMMITTED')


def choose_date(pg, day):
    y, m, d = day.year, day.month, day.day
    ymd = day.strftime('%Y%m%d')
    if not pg.locator('.ui-datepicker-title:visible').count():
        pg.locator('#sCalendar').click()
        until(pg, lambda: pg.locator('.ui-datepicker-title:visible').count() > 0)
    for _ in range(18):
        title = pg.locator('.ui-datepicker-title:visible').first.inner_text()
        mt = re.search(r'(20\d{2})\.\s*(\d+)', title)
        delta = (y - int(mt.group(1))) * 12 + m - int(mt.group(2))
        if delta in (0, 1):
            break
        pg.get_by_role('link', name='다음달' if delta > 0 else '이전달', exact=True).click()
        until(pg, lambda: pg.locator('.ui-datepicker-title:visible').first.inner_text() != title, 5000)
    cell = pg.locator('td[data-year="%d"][data-month="%d"] a[data-date="%d"]' % (y, m - 1, d))
    try:
        cell.wait_for(timeout=8000)
    except Exception:
        raise RuntimeError('DATE_NOT_BOOKABLE')
    cell.click()
    if not until(pg, lambda: pg.locator('#departureDate1').input_value() == ymd):
        raise RuntimeError('DATE_NOT_COMMITTED')


def read_result(pg, dialogs):
    G.beat('oz')
    """결과 화면에서 달력·편 목록을 읽는다. 달력이 없으면 notice 문구를 돌려준다."""
    until(pg, lambda: pg.locator('.flight_calendar_wrap').count() > 0, 45000, 300)
    pg.wait_for_timeout(1200)
    guard(pg)
    try:  # 국내선 안내창
        pop = pg.locator('#btnDomPopup')
        if pop.count() and pop.first.is_visible():
            pop.first.click(timeout=5000)
            pg.wait_for_timeout(600)
    except Exception:
        pass
    cal = pg.evaluate(CALJS)
    rows = pg.evaluate(ROWJS)
    notice = ''
    if not cal:
        body = pg.evaluate("document.body.innerText")
        i = body.find('가는 여정')
        notice = re.sub(r'\s+', ' ', body[i:i + 300]) if i >= 0 else re.sub(r'\s+', ' ', body[:300])
    return cal, rows, notice


CABJS = "[...document.querySelectorAll('[name=selectSeg1CabinClass] li')].filter(l=>l.classList.contains('on')).map(l=>l.querySelector('a').getAttribute('cabinClass')).filter(c=>c!=='A').sort().join('')"


def set_cabin(pg, cabin):
    """국제선 좌석등급 선택: 'A' 전체(E+B), 'B' 비즈니스만. 국내선은 선택 칸이 없다."""
    box = pg.locator('[name=selectSeg1CabinClass] a[name=cabinClassAll]')
    if not (box.count() and box.first.is_visible()):
        return
    want = 'BE' if cabin == 'A' else 'B'
    for _ in range(4):
        cur = pg.evaluate(CABJS)
        if cur == want:
            return
        if cabin == 'A':
            box.first.click()
        elif 'B' not in cur:
            pg.locator('[name=selectSeg1CabinClass] a[cabinClass=B]').first.click()
        else:
            pg.locator('[name=selectSeg1CabinClass] a[cabinClass=E]').first.click()
        pg.wait_for_timeout(500)
    raise RuntimeError('CABIN_NOT_SET ' + pg.evaluate(CABJS))


def form_search(pg, o, d, day, dialogs, cabin='A'):
    pg.goto(FORM, wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_timeout(2500)
    guard(pg)
    ow = pg.get_by_role('link', name='편도', exact=True)
    (ow if ow.count() else pg.get_by_text('편도', exact=True)).first.click()
    until(pg, lambda: pg.locator('#tripType').input_value() == 'OW', 5000)
    pick_airport(pg, 'Departure', o)
    pick_airport(pg, 'Arrival', d)
    choose_date(pg, day)
    pg.wait_for_timeout(400)
    set_cabin(pg, cabin)
    del dialogs[:]
    pg.locator('#btn_coupon_layer').click(timeout=10000)
    conf = pg.locator('button[onclick*="toFlightsSelect"]:visible')
    if not until(pg, lambda: conf.first.is_visible(), 15000):
        raise RuntimeError('NO_CONFIRM_LAYER ' + ' / '.join(dialogs)[:120])
    conf.first.click(timeout=15000)
    if not until(pg, lambda: 'RedemptionRegistTravel' not in pg.url, 120000, 500):
        raise RuntimeError('SUBMIT_TIMEOUT ' + ' / '.join(dialogs)[:120])
    return read_result(pg, dialogs)


def click_date(pg, day, before, dialogs):
    iso = day.strftime('%Y-%m-%d')
    cell = pg.locator('.flight_calendar_wrap td.fc-day-top[name=searchCalDateAvail][data-date="%s"] a' % iso)
    cell.first.click(timeout=8000)
    ok = until(pg, lambda: (pg.evaluate(CALJS) or {}).get('period') not in (None, before), 40000, 300)
    if not ok:
        return None, None, 'CLICK_NO_CHANGE'
    return read_result(pg, dialogs)


def pdate(s):
    return dt.datetime.strptime(s.strip(), '%Y.%m.%d').date()


def absorb(rec, cal, rows, center, how):
    a, b = [pdate(x) for x in cal['period'].split('~')]
    rec['queries'].append({'center': center.isoformat(), 'how': how, 'period': cal['period'], 'asOf': cal['asOf']})
    for iso, v in cal['days'].items():
        day = dt.date.fromisoformat(iso)
        if not (a <= day <= b):
            continue
        ev = ' '.join(v['ev'])
        rec['days'][iso] = {'E': 'economy' in ev, 'B': 'business' in ev, 'F': 'first' in ev,
                            'noSeat': 'no_seat' in v['cls'], 'asOf': cal['asOf']}
    rec['flights'][center.isoformat()] = rows
    return a, b


def clickable(cal, after):
    out = []
    for iso, v in cal['days'].items():
        if v['link'] and re.search(r'bg_week_days|bg_peak', v['cls']):
            day = dt.date.fromisoformat(iso)
            if day > after:
                out.append(day)
    return sorted(out)


def scan_pass(pg, key, dialogs, cabin):
    o, d = key.split('-')
    rec = {'days': {}, 'queries': [], 'flights': {}, 'notes': []}
    center = LO + dt.timedelta(days=15)
    cal, rows, notice = form_search(pg, o, d, center, dialogs, cabin)
    how = 'form'
    for _ in range(8):
        if not cal:
            rec['notes'].append({'center': center.isoformat(), 'how': how, 'notice': notice, 'dialogs': list(dialogs)})
            end = center + dt.timedelta(days=15)  # 달력이 안 뜬 구간: 다음 구간으로 넘어간다
            cover_ok = False
        else:
            a, end = absorb(rec, cal, rows, center, how)
            cover_ok = True
        if end >= HI:
            break
        pause(pg)
        nxt = clickable(cal, center) if cal else []
        nxt = [x for x in nxt if x <= end]
        if cover_ok and nxt:
            target = nxt[-1]
            before = cal['period']
            c2, r2, n2 = click_date(pg, target, before, dialogs)
            if c2:
                cal, rows, notice, center, how = c2, r2, '', target, 'click'
                continue
            rec['notes'].append({'center': target.isoformat(), 'how': 'click', 'notice': n2})
            pause(pg)
        center = min(end + dt.timedelta(days=16), HI)
        cal, rows, notice = form_search(pg, o, d, center, dialogs, cabin)
        how = 'form'
    return rec


def main():
    log('세션 가드', '확인됨' if G.ensure_guard() else '기동 실패 — 가드 없이 진행(수집기 자체 연장 클릭만 동작)')
    db = load()
    try:  # 수집이 도는 동안만 절전 진입을 막는다(프로세스가 끝나면 풀린다)
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)
    except Exception:
        pass
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp('http://127.0.0.1:9333')
        ctx = b.contexts[0]
        for old in ctx.pages:
            if 'Redemption' in old.url:
                old.close()
        pg = ctx.new_page()
        dialogs = []

        def on_dialog(dl):
            dialogs.append(dl.message[:200])
            try:
                dl.accept()
            except Exception:
                pass
        pg.on('dialog', on_dialog)
        if pg.evaluate('navigator.webdriver'):
            raise SystemExit('webdriver flag on')
        fails = 0
        for n, key in enumerate(ROUTES, 1):
            cur = db['res'].get(key) or {}
            if cur.get('done'):
                continue
            cur = {k: v for k, v in cur.items() if k in ('A', 'B')}
            dom = set(key.split('-')) <= KR
            t = time.time()
            try:
                for cabin in (('A',) if dom else CABINS):
                    if cabin in cur:
                        continue
                    cur[cabin] = scan_pass(pg, key, dialogs, cabin)
                    db['res'][key] = dict(cur, done=False)
                    save(db)
                    if cabin == 'A' and not dom:
                        pause(pg)
                cur['done'] = True
                cur['domestic'] = dom
                db['res'][key] = cur
                fails = 0
                E0 = {'days': {}, 'queries': [], 'notes': []}
                A, B = cur.get('A', E0), cur.get('B', E0)
                e = sum(1 for v in A['days'].values() if v['E'])
                b1 = sum(1 for v in A['days'].values() if v['B'])
                b2 = sum(1 for v in B['days'].values() if v['B'])
                log('[%d/%d] %s 전체조회: 일수=%d E=%d B표시=%d | 비즈조회: 일수=%d B=%d | 조회 %d회 notes=%d %.0fs' % (
                    n, len(ROUTES), key, len(A['days']), e, b1, len(B['days']), b2, len(A['queries']) + len(B['queries']), len(A['notes']) + len(B['notes']), time.time() - t))
            except Stop as s:
                log('STOP', key, s)
                db['log'].append({'at': dt.datetime.now().isoformat(), 'key': key, 'stop': str(s)})
                save(db)
                return
            except Exception as ex:
                fails += 1
                msg = str(ex).split('\n')[0][:200]
                log('[%d/%d] %s ERROR %s' % (n, len(ROUTES), key, msg))
                db['log'].append({'at': dt.datetime.now().isoformat(), 'key': key, 'error': msg})
                db['res'][key] = dict(cur, done=False, error=msg)
                try:
                    guard(pg)
                except Stop as s:
                    log('STOP', key, s)
                    db['log'].append({'at': dt.datetime.now().isoformat(), 'key': key, 'stop': str(s)})
                    save(db)
                    return
                if fails >= 5:
                    log('STOP 연속 실패 5회')
                    db['log'].append({'at': dt.datetime.now().isoformat(), 'stop': 'FIVE_FAILS'})
                    save(db)
                    return
            save(db)
            pause(pg)
        log('ALL DONE')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        log('FATAL', traceback.format_exc()[-1500:])
