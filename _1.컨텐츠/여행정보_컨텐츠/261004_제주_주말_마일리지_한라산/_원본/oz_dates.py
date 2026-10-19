# -*- coding: utf-8 -*-
"""아시아나 예매 화면(로그인·실시간)에서 지정한 날짜의 편별 좌석을 읽는다 — 국내선 포함
사용: python oz_dates.py <출력json> <O-D:YYYY-MM-DD,...> [<O-D:...> ...]
좌석 표시가 있는 날은 달력에서 눌러 편별 내역을 받고, 좌석없음 날은 폼 조회를 그 날짜로 다시 해서 편별 내역(매진 포함)을 받는다.
"""
import sys, os, json, time, datetime as dt
_argv = sys.argv[:]
sys.argv = ['scan_live.py', 'X-X', '--out', 'data/_unused.json', '--pace', '4,6']
import scan_live as S
from playwright.sync_api import sync_playwright
import guardutil as G

OUT = _argv[1]
JOBS = []
for a in _argv[2:]:
    key, ds = a.split(':')
    JOBS.append((key, [dt.date.fromisoformat(x) for x in ds.split(',')]))
log = S.log


def selected(cal):
    for iso, v in cal['days'].items():
        if 'fc-today' in v['cls']:
            return iso
    return None


def window(cal):
    a, b = [S.pdate(x) for x in cal['period'].split('~')]
    return a, b


def dayinfo(cal, day):
    v = cal['days'].get(day.isoformat())
    if not v:
        return 'nodata'
    if v['link'] and ('bg_week_days' in v['cls'] or 'bg_peak' in v['cls']):
        return 'clickable'
    if 'no_seat' in v['cls']:
        return 'noseat'
    return 'none'


def click_day(pg, day, dialogs):
    iso = day.isoformat()
    cell = pg.locator('.flight_calendar_wrap td.fc-day-top[name=searchCalDateAvail][data-date="%s"] a' % iso)
    cell.first.click(timeout=15000)
    if not S.until(pg, lambda: selected(pg.evaluate(S.CALJS) or {'days': {}}) == iso, 60000, 300):
        return None, None
    cal, rows, _ = S.read_result(pg, dialogs)
    return cal, rows


res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp(G.CDP)
    ctx = b.contexts[0]
    for old in ctx.pages:
        if 'Redemption' in old.url:
            old.close()
    pg = ctx.new_page()
    dialogs = []
    pg.on('dialog', lambda dl: (dialogs.append(dl.message[:200]), dl.accept()))
    G.ensure_guard()
    for key, dates in JOBS:
        o, d = key.split('-')
        rec = res.setdefault(key, {})
        todo = [x for x in sorted(dates) if x.isoformat() not in rec]
        if not todo:
            continue
        cal = None
        try:
            for day in todo:
                G.beat('oz')
                iso = day.isoformat()
                need_form = cal is None or not (window(cal)[0] <= day <= window(cal)[1])
                if not need_form:
                    st = dayinfo(cal, day)
                    if st == 'clickable':
                        c2, rows = click_day(pg, day, dialogs)
                        if c2:
                            cal = c2
                            rec[iso] = {'how': 'click', 'state': 'seat', 'rows': rows, 'asOf': cal['asOf']}
                        else:
                            need_form = True
                    else:
                        need_form = True   # 좌석없음·표시없음인 날도 편별 내역(매진 표시)을 보려고 폼으로 다시 조회
                if need_form:
                    cal, rows, notice = S.form_search(pg, o, d, day, dialogs, 'A')
                    if not cal:
                        rec[iso] = {'how': 'form', 'state': 'nocal', 'rows': [], 'notice': notice, 'asOf': ''}
                    else:
                        st = dayinfo(cal, day)
                        rec[iso] = {'how': 'form', 'state': {'clickable': 'seat', 'noseat': 'noseat', 'nodata': 'nodata', 'none': 'none'}[st],
                                    'selected': selected(cal), 'rows': rows if selected(cal) == iso else [], 'asOf': cal['asOf']}
                n_seat = sum(1 for r in rec[iso]['rows'] if r.get('eco') and '마일' in (r.get('eco') or ''))
                log(key, iso, rec[iso]['how'], rec[iso]['state'], '편', len(rec[iso]['rows']), '일반석 있는 편', n_seat)
                json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
                S.pause(pg)
        except S.Stop as s:
            log('STOP', key, s)
            json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
            sys.exit(3)
        except Exception as ex:
            log('ERROR', key, str(ex).splitlines()[0][:160])
            json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
            try:
                S.guard(pg)
            except S.Stop as s:
                log('STOP', key, s)
                sys.exit(3)
log('ALL DONE')
