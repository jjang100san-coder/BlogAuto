# -*- coding: utf-8 -*-
"""공공데이터포털 활용신청 일괄 v2 — 버튼 대신 신청 폼 주소로 바로 간다 (10/16: 버튼이 window.open 으로 여는 주소를 소스에서 확인).
자동화 크롬(CDP 9334)에 로그인돼 있어야 한다. 캡차가 뜨면 멈춘다."""
import sys, time, json, os, io
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
from playwright.sync_api import sync_playwright
PURPOSE = '개인 블로그 콘텐츠 작성 — 공공데이터를 근거로 한 정보 글 (걷고읽고떠나고 블로그, 비상업)'
IDS = [x for x in sys.argv[1:] if x.isdigit()]
OUT = os.path.join(os.environ['TEMP'], 'datago_apply_result.json')
res = json.load(io.open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9334'); ctx = b.contexts[0]
    form = ctx.new_page(); msgs = []
    form.on('dialog', lambda d: (msgs.append(d.type + ':' + d.message[:120]), d.accept()))
    for i, pk in enumerate(IDS, 1):
        if res.get(pk, {}).get('ok'): print(pk, '이미 완료'); continue
        r = {'ok': False, 'msgs': []}; msgs.clear()
        try:
            form.goto('https://www.data.go.kr/tcs/dss/redirectDevAcountRequestForm.do?publicDataPk=%s&isBusinessApply=undefined' % pk, wait_until='load'); time.sleep(3)
            body = form.inner_text('body')
            if '로그인' in body and '로그아웃' not in body: r['msgs'].append('로그인 풀림'); res[pk] = r; print(pk, '→ 로그인 풀림'); break
            if '페이지를 찾을 수 없습니다' in body: r['msgs'].append('없는 번호'); res[pk] = r; print(pk, '→ 없는 번호'); continue
            j = body.find('데이터명'); r['title'] = body[j + 3:j + 70].strip().split('\n')[0] if j >= 0 else form.title()[:40]
            if form.locator('#useScopeAgreAt').count() == 0:
                for k in ('이미', '신청중', '신청 중', '불가', '기업회원'):
                    jj = body.find(k)
                    if jj > 0: r['msgs'].append(body[max(0, jj - 40):jj + 60].replace('\n', ' ')); break
                else: r['msgs'].append('신청 폼 아님: ' + body[:120].replace('\n', ' '))
                res[pk] = r; print('%2d/%d' % (i, len(IDS)), pk, r['title'][:36], '→ ❌', r['msgs'][-1][:100]); continue
            form.locator('label[for=radio4]').click()
            form.fill('#prcusePurps', PURPOSE)
            if form.locator('#all-chk').count() and not form.is_checked('#all-chk'): form.locator('label[for=all-chk]').click()
            if not form.is_checked('#useScopeAgreAt'): form.locator('label[for=useScopeAgreAt]').click()
            form.locator('button:has-text("활용 신청하기")').first.click(); time.sleep(4)
            cap = form.locator('#captchaCmm')
            if cap.count() and cap.first.is_visible():
                r['msgs'] += msgs + ['캡차 떴음 — 사용자 입력 필요']; res[pk] = r; print(pk, r['title'], '→ 캡차'); break
            r['msgs'] += msgs
            r['ok'] = any('완료' in m for m in msgs)
            if not r['ok']:
                after = form.inner_text('body')
                for k in ('이미', '중복', '반려', '불가', '오류', '첨부'):
                    jj = after.find(k)
                    if jj > 0: r['msgs'].append(after[max(0, jj - 40):jj + 60].replace('\n', ' ')); break
            print('%2d/%d' % (i, len(IDS)), pk, r['title'][:36], '→', '✅' if r['ok'] else '❌', ' | '.join(r['msgs'])[:110])
        except Exception as e:
            r['msgs'].append('예외: ' + str(e)[:150]); print(pk, '→ 예외', str(e)[:100])
        res[pk] = r
        json.dump(res, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        time.sleep(2)
    try: form.close()
    except Exception: pass
json.dump(res, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('완료', sum(1 for v in res.values() if v.get('ok')), '/', len(res))
