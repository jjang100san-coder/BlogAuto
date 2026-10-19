# -*- coding: utf-8 -*-
r"""네이버 통합검색 AI 브리핑 수집 (2026-10-17). 로그인 없는 새 크롬 창, 검색어마다 6초 간격.
검색어마다: AI 브리핑 유무 · 브리핑 본문 · 출처 링크(펼쳐서 더보기 뒤) · 검색 결과의 블로그 글 순서(브리핑 밖) · 내 블로그 위치.
사용: python _aib_collect.py <qs.json> <out.json> <shots폴더>"""
import sys, tempfile, json, io, time, re, urllib.parse as up
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
QS = json.load(open(sys.argv[1], encoding="utf-8")); OUT = sys.argv[2]; SHOT = sys.argv[3]
JS = r"""() => {
 const hs=[...document.querySelectorAll('h2,h3,strong,span,div')].filter(e=>e.childElementCount<=2 && /^AI\s?브리핑$/.test(e.textContent.trim()));
 const blk = hs.length ? (hs[0].closest('section')||hs[0].parentElement.parentElement) : null;
 const inBlk = a => blk && blk.contains(a);
 const all=[...document.querySelectorAll('a[href]')];
 const src = blk ? all.filter(inBlk).map(a=>a.href) : [];
 const org=[]; for(const a of all){ if(inBlk(a)) continue; const m=a.href.match(/blog\.naver\.com\/([\w\-]+)\/(\d{9,})/); if(m){ const k=m[1]+'/'+m[2]; if(!org.includes(k)) org.push(k);} }
 return {found:!!blk, text: blk? blk.innerText.slice(0,5000):'', src, org};
}"""
res = []
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(tempfile.mkdtemp(), channel="chrome", headless=False, locale="ko-KR", viewport={"width": 1280, "height": 1800})
    pg = ctx.new_page()
    for i, (q, kind) in enumerate(QS):
        try:
            r = pg.goto("https://search.naver.com/search.naver?query=" + up.quote(q), wait_until="domcontentloaded", timeout=30000)
            pg.wait_for_timeout(4000)
            try: pg.get_by_text(re.compile(r"^AI\s?브리핑$")).first.wait_for(timeout=8000)
            except Exception: pass
            expanded = False
            try:
                loc = pg.get_by_text("펼쳐서 더보기", exact=True)
                loc.first.wait_for(timeout=8000)
                loc.first.scroll_into_view_if_needed(); loc.first.click(timeout=5000); pg.wait_for_timeout(3000); expanded = True
            except Exception: pass
            d = pg.evaluate(JS)
            blogs_src = []
            for h in d["src"]:
                m = re.search(r"blog\.naver\.com/([\w\-]+)/(\d{9,})", h)
                if m and m.group(1) + "/" + m.group(2) not in blogs_src: blogs_src.append(m.group(1) + "/" + m.group(2))
            other_src = sorted(set(h.split("?")[0] for h in d["src"] if h.startswith("http") and "blog.naver.com" not in h and "search.naver.com" not in h and "ader.naver.com" not in h))
            mine_org = [k for k in d["org"] if k.startswith("baiyan_novembre/")]
            row = dict(q=q, kind=kind, status=r.status if r else None, ai=d["found"], expanded=expanded, brief=d["text"], src_blogs=blogs_src, src_other=other_src,
                       org_blogs=d["org"][:15], cited_mine=any(k.startswith("baiyan_novembre/") for k in blogs_src),
                       mine_rank=(d["org"].index(mine_org[0]) + 1) if mine_org else None, at=time.strftime("%Y-%m-%d %H:%M"))
            pg.screenshot(path=f"{SHOT}/{i:02d}.png", full_page=False)
        except Exception as e:
            row = dict(q=q, kind=kind, err=str(e)[:100])
        res.append(row)
        print(i, q, "| AI", row.get("ai"), "| 펼침", row.get("expanded"), "| 블로그 출처", len(row.get("src_blogs", [])), "| 내 인용", row.get("cited_mine"), "| 내 글 순위", row.get("mine_rank"), flush=True)
        json.dump(res, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(6)
    ctx.close()
