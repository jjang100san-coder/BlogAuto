# 이미 올린 클립(공개·등록 예약)의 커버만 바꿔 끼운다 — [등록]·[임시저장]은 누르지 않는다(탭을 열어 둔 채 끝)
# 사용: python set_clip_covers.py <목록.json>   목록 = [["설명 앞부분", "커버 jpg 경로"], ...]
import sys, json
from playwright.sync_api import sync_playwright

items = json.load(open(sys.argv[1], encoding='utf-8'))
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9334')
    ctx = b.contexts[0]
    for key, img in items:
        pg = ctx.new_page()
        pg.goto('https://clipcreators.naver.com/web/contents/clips', wait_until='domcontentloaded')
        pg.wait_for_timeout(4000)
        row = pg.get_by_text(key, exact=False).first
        for _ in range(12):
            if row.count():
                break
            pg.mouse.wheel(0, 3000); pg.wait_for_timeout(1000)
        if not row.count():
            print('못 찾음:', key); pg.close(); continue
        row.click(); pg.wait_for_timeout(5000)
        pg.locator("input[class*=coverUploadInput]").set_input_files(img)
        pg.wait_for_timeout(4000)
        first = pg.locator("button[class*=ClipDetailForm_coverItem]").first
        ok = 'coverSelected' in (first.get_attribute('class') or '')
        print(('커버 올림' if ok else '커버 확인 필요'), '|', key, '|', pg.url)
