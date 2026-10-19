# 잘 나가는 클립의 길이·첫 장면 보기 — 자동화 크롬(9334)으로 m.naver.com/shorts 를 열어 video 길이를 읽고 0·1·2·5초·중간 화면을 찍는다(10/10)
# 사용: python clip_frames.py <ranked.json> <저장폴더> [개수=12]
#   ranked.json = clip_serp 결과를 조회수 순으로 정렬한 목록. 결과: <저장폴더>\frames\<순위>_<초>.jpg · frames.json(길이·조회수·제목)
import sys, os, json, time
from playwright.sync_api import sync_playwright

L = json.load(open(sys.argv[1], encoding='utf-8'))
dest = os.path.join(sys.argv[2], 'frames'); os.makedirs(dest, exist_ok=True)
n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
out = []
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9334')
    ctx = b.contexts[0]
    pg = ctx.new_page()
    pg.set_viewport_size({'width': 430, 'height': 860})
    for i, c in enumerate(L[:n]):
        url = 'https://m.naver.com/shorts/?mediaType=VOD&serviceType=CLIP&seedMediaId=' + c['media_id']
        try:
            pg.goto(url, wait_until='domcontentloaded'); pg.wait_for_timeout(6000)
            v = pg.locator('video').first
            dur = pg.evaluate("() => { const v = document.querySelector('video'); return v ? v.duration : null }")
            pg.evaluate("() => { const v = document.querySelector('video'); if (v) { v.muted = true; v.pause(); } }")
            shots = []
            for t in [0.1, 1.0, 2.0, 5.0, (dur or 20) / 2]:
                pg.evaluate("(t) => { const v = document.querySelector('video'); if (v) v.currentTime = t }", t)
                pg.wait_for_timeout(1200)
                f = os.path.join(dest, '%02d_%04.1f.jpg' % (i + 1, t))
                (v if v.count() else pg).screenshot(path=f)
                shots.append(f)
            out.append(dict(rank=i + 1, views=c['views'], title=c['title'], channel=c['channel'], q=c.get('q'), duration=dur, shots=shots))
            print(i + 1, c['views'], dur, c['title'][:40])
        except Exception as e:
            print(i + 1, 'fail', e)
    pg.close()
json.dump(out, open(os.path.join(sys.argv[2], 'frames.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
