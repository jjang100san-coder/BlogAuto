# -*- coding: utf-8 -*-
"""탑승권 양식 공용 모듈 — 나혼산 즉흥 여행 글(2026-10-18 사용자 「이제야 안 AI스럽다, 이걸로」).
마스터 5-8 다섯 칸:
 ① 형식  탑승권 — 왼쪽 본권(그림), 오른쪽 떼는 쪽(큰 숫자 하나·둘)
 ② 배경  베이지 종이(#EDE5D6, 잔점 결) 위 크림색 탑승권(#FFFCF5)
 ③ 모양  남색 머리띠(#22335A) · 옆 단(떼는 쪽 자리) · 절취선·반달 홈은 첫 그림과 할 일 그림만(10/18), 바코드 없음(사용자 「불편」)
 ④ 강조  주황 고무도장(결론 한 줄, -7°) · 아주 큰 숫자 · 형광 대신 머리띠 위 살구색 강조어
 ⑤ 정체성 「구구절절 · BOARDING · 꼭지 · NN / 13」
색: 미리 #3D62AE · 현장 #D07A22 (dataviz validate_palette.js 라이트 전 항목 통과) · 위험 #C8463C
흔한 AI 카드 꼴(어두운 배경 + 둥근 상자 + 둥근 결론 바)은 쓰지 않는다."""
import math, pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "img_v2"; OUT.mkdir(exist_ok=True)
FONT = pathlib.Path("C:/Windows/Fonts/NotoSansKR-VF.ttf").as_uri()
TOTAL = 13

CSS = """
@font-face{font-family:'NK';src:url('%s');font-weight:100 900}
*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#1E2330;--ink2:#4A5163;--muted:#7A7466;--line:#E3D9C6;--pre:#3D62AE;--pre-l:#E7EDF8;--ons:#D07A22;--ons-l:#FBEBDA;
 --red:#C8463C;--red-l:#F8E2DF;--navy:#22335A;--paper:#FFFCF5;--bg:#EDE5D6;--ok:#2F8F5B}
html,body{width:1400px;height:800px}
body{font-family:'NK',sans-serif;color:var(--ink);position:relative;overflow:hidden;-webkit-font-smoothing:antialiased;
 background:var(--bg);background-image:radial-gradient(rgba(90,70,40,.06) 1px,transparent 1.2px);background-size:6px 6px}
.ticket{position:absolute;left:36px;top:34px;width:1328px;height:732px;background:var(--paper);border-radius:20px;
 box-shadow:0 2px 0 rgba(60,45,20,.06),0 22px 50px rgba(60,45,20,.16);overflow:hidden}
.band{position:absolute;left:0;top:0;right:0;height:158px;background:var(--navy);color:#fff;padding:26px 40px}
.band .k{display:flex;gap:14px;align-items:center;font-size:15px;font-weight:800;letter-spacing:.18em;color:#AFC0E6}
.band .k b{background:var(--ons);color:#fff;letter-spacing:.06em;border-radius:6px;padding:3px 9px;font-size:14px}
.band h1{color:#fff;font-size:50px;font-weight:900;letter-spacing:-.02em;margin-top:10px;white-space:nowrap}
.band h1 em{font-style:normal;color:#FFC27A}
.perf{position:absolute;left:1000px;top:158px;bottom:0;border-left:3px dashed #D9CFBC}
.perf.solid{border-left:2px solid #E8DFCC}
.stub.side{background:#F7F1E5}
.notch{position:absolute;width:44px;height:44px;border-radius:50%%;background:var(--bg);left:979px}
.main{position:absolute;left:0;top:158px;width:1000px;bottom:0;padding:24px 36px 44px}
.stub{position:absolute;left:1003px;right:0;top:158px;bottom:0;padding:26px 30px}
.stub .lab{font-size:13px;font-weight:800;letter-spacing:.16em;color:#9A917F}
.stub .row{margin-top:16px}
.stub .n{font-size:84px;font-weight:900;line-height:.95;letter-spacing:-.04em}
.stub .n small{font-size:36px;margin-left:2px}
.stub .t{font-size:16px;font-weight:700;color:var(--ink2);margin-top:6px;line-height:1.35}
.bar{position:absolute;left:30px;right:30px;bottom:56px;height:54px;background:repeating-linear-gradient(90deg,#22335A 0 3px,transparent 3px 6px,#22335A 6px 7px,transparent 7px 11px,#22335A 11px 15px,transparent 15px 17px)}
.src2{position:absolute;left:30px;bottom:22px;font-size:13px;font-weight:800;letter-spacing:.14em;color:#9A917F}
.src{position:absolute;left:36px;bottom:16px;right:340px;font-size:13.5px;color:#9A917F;white-space:nowrap;overflow:hidden}
.stamp{position:absolute;transform:rotate(-7deg);border:4px solid var(--ons);color:var(--ons);border-radius:12px;padding:10px 20px;
 font-size:25px;font-weight:900;background:rgba(255,252,245,.88);box-shadow:inset 0 0 0 2px rgba(208,122,34,.25);white-space:nowrap}
.stamp.red{border-color:var(--red);color:var(--red);box-shadow:inset 0 0 0 2px rgba(200,70,60,.22)}
.stamp.navy{border-color:var(--navy);color:var(--navy);box-shadow:inset 0 0 0 2px rgba(34,51,90,.2)}
img.i3{display:block;object-fit:contain}
svg.i{width:26px;height:26px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.chk{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%%;flex:none}
""" % FONT

I = {
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>', "x": '<path d="M6 6l12 12M18 6L6 18"/>',
 "arrow": '<path d="M4 12h15M13 6l6 6-6 6"/>',
}
def ic(name, size=26, color="currentColor", sw=2):
    return f'<svg class="i" viewBox="0 0 24 24" style="width:{size}px;height:{size}px;color:{color};stroke-width:{sw}">{I[name]}</svg>'
def badge(ok=True, size=30):
    bg = "var(--pre)" if ok else "var(--red)"
    return f'<span class="chk" style="width:{size}px;height:{size}px;background:{bg}">{ic("check" if ok else "x", int(size*.6), "#fff", 3)}</span>'
def icon(name, w=86):
    return f'<img class="i3" src="icons/{name}_t.png" style="width:{w}px;height:{w}px">'

def shade(hexc, f):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 1: r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    else: r, g, b = (int(c * f) for c in (r, g, b))
    return "#%02x%02x%02x" % (r, g, b)
def cubes(n_a, n_b, cols=10, s=25, ca="#3D62AE", cb="#D07A22", gap=0.14):
    """블록 하나 = 결정 하나(아이소메트릭)."""
    n = n_a + n_b; rows = math.ceil(n / cols)
    a = s * math.cos(math.pi / 6); b = s * math.sin(math.pi / 6)
    W = (cols + rows) * a + 4; H = (cols + rows) * b + s + 4
    X0 = rows * a + 2; Y0 = s + 2
    def iso(x, y, z): return (X0 + (x - y) * a, Y0 + (x + y) * b - z * s)
    cells = [(k % cols, k // cols, ca if k < n_a else cb) for k in range(n)]
    cells.sort(key=lambda q: q[0] + q[1])
    out = []
    for x, y, col in cells:
        x0, y0, x1, y1 = x + gap / 2, y + gap / 2, x + 1 - gap / 2, y + 1 - gap / 2
        def poly(pts, fill): return '<polygon points="%s" fill="%s"/>' % (" ".join("%.1f,%.1f" % iso(*q) for q in pts), fill)
        out.append(poly([(x0, y0, 1), (x1, y0, 1), (x1, y1, 1), (x0, y1, 1)], shade(col, 1.28)))
        out.append(poly([(x0, y1, 1), (x1, y1, 1), (x1, y1, 0), (x0, y1, 0)], col))
        out.append(poly([(x1, y0, 1), (x1, y1, 1), (x1, y1, 0), (x1, y0, 0)], shade(col, 0.74)))
    return '<svg width="%d" height="%d" viewBox="0 0 %.0f %.0f">%s</svg>' % (W, H, W, H, "".join(out))

def ticket(no, kicker, title, main, stub, stamp, stamp_pos, src, css="", stamp_cls="", kind="sheet"):
    """kind: 'ticket' = 절취선·반달 홈(첫 그림·마지막 할 일만, 10/18 사용자 「전부 항공권이면 불편」), 'sheet' = 같은 종이·머리띠에 옆 단만"""
    """stub = [(숫자html, 색, 설명), ...] 또는 html 문자열"""
    if isinstance(stub, (list, tuple)):
        lab, rows = stub[0], stub[1:]
        st = f'<div class="lab">{lab}</div>' + "".join(f'<div class="row"><div class="n" style="color:{c}">{n}</div><div class="t">{t}</div></div>' for n, c, t in rows)
    else:
        st = stub
    sx, sy = stamp_pos
    perf = ('<div class="perf"></div><div class="notch" style="top:136px"></div><div class="notch" style="bottom:-22px"></div>' if kind == "ticket" else '<div class="perf solid"></div>')
    side = "" if kind == "ticket" else " side"
    stamp_html = f'<div class="stamp {stamp_cls}" style="left:{sx}px;top:{sy}px">{stamp}</div>' if stamp else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{css}</style></head><body>
<div class="ticket">
 <div class="band"><div class="k"><b>구구절절</b>{"BOARDING" if kind == "ticket" else "TRAVEL NOTE"} · {kicker} · {no:02d} / {TOTAL}</div><h1>{title}</h1></div>
 <div class="main">{main}</div>
 {perf}
 <div class="stub{side}">{st}<div class="src2">걷고읽고떠나고</div></div>
 {stamp_html}
 <div class="src">근거 · {src}</div>
</div></body></html>"""

CHECK_JS = """() => { const W=1400,H=800,bad=[];
 document.querySelectorAll('.ticket *').forEach(e=>{const r=e.getBoundingClientRect();
   if(r.width&&(r.right>W-30||r.bottom>H-30)) bad.push((e.className&&e.className.baseVal===undefined?e.className:e.tagName)+':'+(e.textContent||'').trim().slice(0,14));
   if(e.scrollWidth>e.clientWidth+2 && getComputedStyle(e).overflow==='hidden' && !e.classList.contains('ticket')) bad.push('잘림:'+(e.textContent||'').trim().slice(0,14));});
 const main=document.querySelector('.main').getBoundingClientRect(); const over=[];
 document.querySelectorAll('.main > *').forEach(e=>{const r=e.getBoundingClientRect(); if(r.bottom>main.bottom-28) over.push('본권 넘침:'+(e.textContent||'').trim().slice(0,14))});
 const h1=document.querySelector('.band h1'); if(h1.scrollWidth>1250) over.push('제목 넘침');
 return bad.concat(over).slice(0,8) }"""

def render(figs, names=None):
    names = names or list(figs)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 800}, device_scale_factor=2)
        for n in names:
            tmp = HERE / f"_{n}.html"; tmp.write_text(figs[n], encoding="utf-8")
            pg.goto(tmp.as_uri()); pg.wait_for_timeout(250)
            issues = pg.evaluate(CHECK_JS)
            pg.screenshot(path=str(OUT / f"{n}.png"))
            print("saved", n, issues if issues else "OK")
        b.close()
