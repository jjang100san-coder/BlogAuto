# -*- coding: utf-8 -*-
"""움직이는 인포그래픽 장면 — 마스터 5-8 양식(HTML/CSS 카드·그림자·선 아이콘·입체 아이콘)을 Playwright 로 프레임마다 찍는다(2026-10-18).
PIL 로 그린 장면(make_anims.py)은 「그래픽을 띄운 느낌」 → 블로그 정보 그림과 같은 디자인 체계로 올린다.

쓰는 법(클립 폴더의 make_html.py):
    from html_anim import scene, render
    S = [scene('bars', 6.0, BODY_HTML, JS_F, css=EXTRA)]
    render(S, BASE)            # → BASE\\_frames_<이름>\\f0001.jpg … (shorts 의 'video:' 미디어가 읽는다)
    render(S, BASE, ['bars'])  # 하나만 다시
JS_F 는 function F(t){...} — t 초에 맞춰 DOM 의 width·transform·textContent 를 바꾼다. 도우미: E(u) 부드럽게, P(t,a,b) a~b초 진행률(0~1, 부드럽게), K(u) 살짝 튀는 등장, $(sel), $$(sel), num(x,자릿수).
화면 1350×1338 = 장면 칸 1080×1070 의 1.25배. 위 240px 는 큰 글(call_top) 자리, 아래 1080px 밑은 말자막 자리 → 그림은 SAFE_TOP~SAFE_BOT 안에.
"""
import os, pathlib
from playwright.sync_api import sync_playwright

W, H, FPS = 1350, 1338, 30
SAFE_TOP, SAFE_BOT = 250, 1075
FONT = pathlib.Path('C:/Windows/Fonts/NotoSansKR-VF.ttf').as_uri()

CSS = """
@font-face{font-family:'NK';src:url('%s');font-weight:100 900}
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#FAF7F2;--card:#FFFFFF;--ink:#1E2330;--ink2:#4A5163;--muted:#8A8F9C;--line:#E7E1D6;
 --pre:#3D62AE;--pre-l:#E6ECF8;--ons:#D07A22;--ons-l:#FBEBDA;--red:#C8463C;--red-l:#F9E3E0;--ok:#2F8F5B;--ok-l:#E2F1E8;--sand:#F3EBDD}
html,body{width:%dpx;height:%dpx}
body{font-family:'NK',sans-serif;background:var(--bg);color:var(--ink);position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}
.stage{position:absolute;left:70px;right:70px;top:%dpx;bottom:%dpx}
.card{background:var(--card);border-radius:30px;box-shadow:0 2px 0 rgba(30,35,48,.04),0 16px 40px rgba(30,35,48,.09);border:1px solid #EFE9DF}
.pill{display:inline-flex;align-items:center;gap:10px;border-radius:999px;padding:10px 22px;font-weight:800}
.big{font-weight:900;letter-spacing:-.03em;line-height:1}
.mut{color:var(--muted)}
.ab{position:absolute}
.icon3d{object-fit:contain;filter:drop-shadow(0 14px 18px rgba(30,35,48,.16))}
svg.i{stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.dots{background-image:radial-gradient(#E9E2D5 1.6px,transparent 1.6px);background-size:26px 26px}
""" % (FONT, W, H, SAFE_TOP, H - SAFE_BOT)

JS = r"""
const E=u=>u<=0?0:u>=1?1:u*u*(3-2*u);
const P=(t,a,b)=>E((t-a)/(b-a));
const K=u=>u<=0?0:u>=1?1:(u<.6?E(u/.6)*1.12:1.12-.12*E((u-.6)/.4));
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const num=(x,d=0)=>x.toLocaleString('ko-KR',{minimumFractionDigits:d,maximumFractionDigits:d});
const sgn=(x,d=1)=>(x>0?'+':x<0?'−':'')+Math.abs(x).toFixed(d);
"""

ICON = {  # 선 아이콘(직접 그림, 24 격자)
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'x': '<path d="M6 6l12 12M18 6L6 18"/>',
    'up': '<path d="M12 19V5M6 11l6-6 6 6"/>',
    'down': '<path d="M12 5v14M6 13l6 6 6-6"/>',
    'bulb': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
    'pin': '<path d="M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/>',
    'scale': '<path d="M12 4v16M5 20h14M5 8h14M5 8l-3 6h6zM19 8l-3 6h6z"/>',
    'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'q': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5v.7M12 17h.01"/>',
}


def ic(name, size=40, color='currentColor', sw=2.2):
    return f'<svg class="i" viewBox="0 0 24 24" style="width:{size}px;height:{size}px;color:{color};stroke-width:{sw}">{ICON[name]}</svg>'


def scene(name, sec, body, js, css=''):
    return dict(name=name, sec=sec, body=body, js=js, css=css)


def _html(s):
    return ('<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + s['css'] + '</style></head><body class="dots">'
            + s['body'] + '<script>' + JS + s['js'] + '</script></body></html>')


def render(scenes, base, only=None, quality=90):
    base = pathlib.Path(base)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        for s in scenes:
            if only and s['name'] not in only:
                continue
            f = base / ('_scene_%s.html' % s['name'])
            f.write_text(_html(s), encoding='utf-8')
            pg.goto(f.as_uri()); pg.wait_for_load_state('networkidle')
            pg.evaluate('document.fonts.ready')
            d0 = base / ('_frames_' + s['name']); d0.mkdir(exist_ok=True)
            for x in d0.iterdir():
                x.unlink()
            n = int(s['sec'] * FPS)
            for i in range(n):
                pg.evaluate('F(%f)' % (i / FPS))
                pg.screenshot(path=str(d0 / ('f%04d.jpg' % (i + 1))), type='jpeg', quality=quality)
            # 넘침 검사: 화면 밖·안전 구역 밖으로 나간 글자
            bad = pg.evaluate('''([T,B,W])=>[...document.querySelectorAll('.stage *')].filter(e=>e.children.length==0&&e.textContent.trim()).map(e=>{const r=e.getBoundingClientRect();return [e.textContent.trim().slice(0,20),Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]}).filter(([s,l,t,r,b])=>l<0||r>W||t<T-5||b>B+5)''', [SAFE_TOP, SAFE_BOT, W])
            print(s['name'], n, 'frames', ('⚠ 구역 밖: %s' % bad) if bad else '', flush=True)
        b.close()


def cutout_white(src, dst, thresh=242):
    """흰 바탕 입체 아이콘 → 바탕 투명 PNG (가장자리부터 번지듯 지움)"""
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.open(src).convert('RGB'); w, h = im.size
    fl = im.copy()
    for pnt in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(fl, pnt, (255, 0, 255), thresh=255 - thresh + 10)
    m = Image.new('L', (w, h), 255); mp, fp = m.load(), fl.load()
    for y in range(h):
        for x in range(w):
            if fp[x, y] == (255, 0, 255):
                mp[x, y] = 0
    m = m.filter(ImageFilter.GaussianBlur(1.0))
    out = im.convert('RGBA'); out.putalpha(m)
    bb = out.getbbox(); out = out.crop(bb) if bb else out
    out.save(dst)
    return dst
