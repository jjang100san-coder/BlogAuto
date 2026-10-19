# -*- coding: utf-8 -*-
"""예약 글의 대표 이미지(없으면 첫 이미지)를 받아 온다 — 썸네일 세 질문 점검용 (2026-10-15).
자동화 크롬(CDP 9334)에서 「예약 발행 N건」 팝업으로 글을 하나씩 에디터에 싣고, 이미지 주소만 읽는다.
아무것도 고치거나 저장하지 않는다. 결과: Blog/_문서\썸네일분석\reserved\<번호>.img + reserved_thumbs.json
  python reserved_thumbs.py            # 발행판 reserved.json 의 예약 글 전부
  python reserved_thumbs.py --limit 3  # 앞의 3편만 시험"""
import sys, os, io, json, time, re, urllib.request as ur
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from update_reserved import load_reserved, WRITE
CDP = "http://127.0.0.1:9334"
RES = r"C:\Users\user\Desktop\자동화\블로그용\발행판\reserved.json"
OUT = r"C:\Users\user\Desktop\Blog\_문서\썸네일분석\reserved"
os.makedirs(OUT, exist_ok=True)

JS = r"""() => {
  const comps = [...document.querySelectorAll('.se-content .se-component.se-image')];
  return comps.map((c, i) => {
    const im = c.querySelector('img');
    const rep = /represent/i.test(c.className) || !!c.querySelector('[class*="represent"]');
    const cap = (c.querySelector('.se-caption') || {}).innerText || '';
    return {i, src: im ? (im.getAttribute('src') || '') : '', rep, cap: cap.trim().slice(0, 80)};
  });
}"""

def main():
    lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    items = sorted(json.load(io.open(RES, encoding="utf-8"))["items"], key=lambda x: x["dt"])[:lim]
    out = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        pages = [pg for pg in b.contexts[0].pages if "PostWriteForm" in pg.url]
        page = pages[0] if pages else b.contexts[0].new_page()
        page.on("dialog", lambda d: d.accept())   # 페이지 떠날 때 확인 창
        for n, it in enumerate(items, 1):
            key = it["title"][:24]
            rec = {"n": n, "dt": it["dt"], "title": it["title"]}
            try:
                page.goto(WRITE, wait_until="domcontentloaded"); time.sleep(5)   # 글마다 새로 연다 — 앞 글이 실린 채론 팝업 클릭이 안 먹는다
                cancel = page.locator(".se-popup-button-cancel")
                if cancel.count() and cancel.first.is_visible(): cancel.first.click(); time.sleep(1)   # 「작성 중인 글」 이어쓰기 → 취소
                load_reserved(page, key)
                imgs = page.main_frame.evaluate(JS)
                rec["imgs"] = len(imgs)
                pick = next((x for x in imgs if x["rep"]), imgs[0] if imgs else None)
                rec["rep_marked"] = bool(pick and pick["rep"])
                if pick and pick["src"]:
                    src = pick["src"]   # blogfiles ...?type=w1 그대로 (w773 은 404)
                    fn = os.path.join(OUT, "%02d.img" % n)
                    data = ur.urlopen(ur.Request(src, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://blog.naver.com/"}), timeout=20).read()
                    open(fn, "wb").write(data); rec["thumb"] = fn; rec["cap"] = pick["cap"]; rec["src"] = src
                print("%02d %s 이미지 %s장 대표표시 %s · %s" % (n, it["dt"][5:16], rec.get("imgs"), rec.get("rep_marked"), it["title"][:40]))
            except Exception as e:
                rec["err"] = str(e)[:120]; print("%02d !! %s — %s" % (n, it["title"][:30], rec["err"]))
                try: page.keyboard.press("Escape"); time.sleep(1)
                except Exception: pass
            out.append(rec)
            time.sleep(1.5)
    json.dump(out, io.open(os.path.join(OUT, "..", "reserved_thumbs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("완료 %d편 · 실패 %d" % (len(out), sum(1 for r in out if r.get("err"))))

if __name__ == "__main__":
    main()
