# -*- coding: utf-8 -*-
"""아시아나 마일리지 예매 화면: 날짜를 하나씩 눌러 편명·시각·편별 좌석까지 받는다

사용: python oz_daily.py ICN-LHR,LHR-ICN,... [--out data/oz_daily.json] [--pace 4,6]
좌석 표시가 있는 날만 누를 수 있다(좌석없음 날은 화면이 눌리지 않는다).
방향마다 끝에 비즈니스 전용 달력도 한 번 읽는다. 예매·결제 단계로는 가지 않는다.
"""
import sys, os, json, time, datetime as dt

_argv = sys.argv[:]
_opt = {}
for _i, _a in enumerate(_argv):
    if _a.startswith('--') and _i + 1 < len(_argv):
        _opt[_a[2:]] = _argv[_i + 1]
sys.argv = ['scan_live.py', 'X-X', '--out', 'data/_unused.json', '--pace', _opt.get('pace', '4,6')]
import scan_live as S  # 폼 조회·달력 읽기·차단 감지를 그대로 쓴다
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTES = _argv[1].split(',')
OUT = os.path.join(HERE, _opt.get('out', 'data/oz_daily.json'))
LO, HI = S.LO, S.HI
log = S.log


def save(db):
    json.dump(db, open(OUT + '.tmp', 'w', encoding='utf-8'), ensure_ascii=False)
    os.replace(OUT + '.tmp', OUT)


def selected(cal):
    for iso, v in cal['days'].items():
        if 'fc-today' in v['cls']:
            return iso
    return None


def marks(rec, cal):
    a, b = [S.pdate(x) for x in cal['period'].split('~')]
    for iso, v in cal['days'].items():
        day = dt.date.fromisoformat(iso)
        if a <= day <= b:
            ev = ' '.join(v['ev'])
            rec['marks'][iso] = {'E': 'economy' in ev, 'B': 'business' in ev, 'noSeat': 'no_seat' in v['cls'], 'asOf': cal['asOf']}
    return a, b


def todo(rec, cal):
    out = []
    for iso, v in cal['days'].items():
        if v['link'] and ('bg_week_days' in v['cls'] or 'bg_peak' in v['cls']):
            day = dt.date.fromisoformat(iso)
            if LO <= day <= HI and iso not in rec['days']:
                out.append(day)
    return sorted(out)


def click_day(pg, day, dialogs):
    iso = day.isoformat()
    cell = pg.locator('.flight_calendar_wrap td.fc-day-top[name=searchCalDateAvail][data-date="%s"] a' % iso)
    del dialogs[:]
    try:
        cell.first.click(timeout=15000)
    except Exception as ex:
        return None, None, 'CLICK_FAIL ' + str(ex).splitlines()[0][:80]
    ok = S.until(pg, lambda: selected(pg.evaluate(S.CALJS) or {'days': {}}) == iso, 60000, 300)
    if not ok:
        return None, None, 'CLICK_NO_CHANGE ' + ' / '.join(dialogs)[:120]
    cal, rows, _ = S.read_result(pg, dialogs)
    return cal, rows, ''


def scan_daily(pg, key, dialogs, rec):
    o, d = key.split('-')
    center = LO + dt.timedelta(days=15)
    cal, rows, notice = S.form_search(pg, o, d, center, dialogs, 'A')
    for _ in range(140):
        if cal:
            a, end = marks(rec, cal)
            sel = selected(cal)
            if sel and LO.isoformat() <= sel <= HI.isoformat():
                rec['days'][sel] = {'rows': rows, 'asOf': cal['asOf']}
            nxt = todo(rec, cal)
        else:
            rec['notes'].append({'center': center.isoformat(), 'notice': notice})
            end, nxt = center + dt.timedelta(days=15), []
        S.pause(pg)
        if nxt:
            target = nxt[0]
            c2, r2, why = click_day(pg, target, dialogs)
            if not c2:  # 클릭이 안 먹으면 그 날짜로 폼 조회를 새로 한다
                rec['notes'].append({'center': target.isoformat(), 'notice': why})
                S.guard(pg)
                S.pause(pg)
                c2, r2, n2 = S.form_search(pg, o, d, target, dialogs, 'A')
                if not c2 or selected(c2) != target.isoformat():
                    rec['days'][target.isoformat()] = {'rows': None, 'asOf': '', 'fail': True}
                    rec['notes'].append({'center': target.isoformat(), 'notice': 'FORM_RETRY_FAIL ' + (n2 or '')[:80]})
                    if not c2:
                        continue
            cal, rows, center = c2, r2, target
            continue
        if end >= HI:
            break
        center = min(end + dt.timedelta(days=16), HI)
        cal, rows, notice = S.form_search(pg, o, d, center, dialogs, 'A')


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
        fails = 0
        for n, key in enumerate(ROUTES, 1):
            rec = db['res'].get(key)
            if rec and rec.get('done'):
                continue
            rec = rec or {'days': {}, 'marks': {}, 'notes': [], 'B': None}
            db['res'][key] = rec
            t = time.time()
            try:
                if not rec.get('dailyDone'):
                    scan_daily(pg, key, dialogs, rec)
                    rec['dailyDone'] = True
                    save(db)
                    S.pause(pg)
                if rec.get('B') is None:
                    rec['B'] = S.scan_pass(pg, key, dialogs, 'B')
                rec['done'] = True
                rec.pop('error', None)
                fails = 0
                got = [v for v in rec['days'].values() if v.get('rows')]
                e = sum(1 for v in rec['marks'].values() if v['E'])
                bz = sum(1 for v in rec['B']['days'].values() if v['B'])
                log('[%d/%d] %s 누른 날=%d 일반석 표시=%d 좌석없음=%d 비즈(전용조회)=%d notes=%d %.0fs' % (
                    n, len(ROUTES), key, len(got), e, sum(1 for v in rec['marks'].values() if v['noSeat']), bz, len(rec['notes']), time.time() - t))
            except S.Stop as s:
                log('STOP', key, s)
                db['log'].append({'at': dt.datetime.now().isoformat(), 'key': key, 'stop': str(s)})
                save(db)
                return
            except Exception as ex:
                fails += 1
                msg = str(ex).split('\n')[0][:200]
                log('[%d/%d] %s ERROR %s (받은 날 %d)' % (n, len(ROUTES), key, msg, len(rec['days'])))
                rec['error'] = msg
                db['log'].append({'at': dt.datetime.now().isoformat(), 'key': key, 'error': msg})
                try:
                    S.guard(pg)
                except S.Stop as s:
                    log('STOP', key, s)
                    db['log'].append({'at': dt.datetime.now().isoformat(), 'key': key, 'stop': str(s)})
                    save(db)
                    return
                if fails >= 4:
                    log('STOP 연속 실패 4회')
                    save(db)
                    return
            save(db)
            S.pause(pg)
        log('ALL DONE')


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        import traceback
        log('FATAL', traceback.format_exc()[-1200:])
