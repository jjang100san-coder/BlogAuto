# -*- coding: utf-8 -*-
"""인포그래픽 v2 — HTML/CSS 로 짜서 Playwright 로 PNG(1400×800, 2배 해상도)로 뽑는다(2026-10-18).
PIL 판(make_pictures.py)이 「그래픽을 띄운 느낌」이라는 지적 → 카드·아이콘·위계·여백을 갖춘 디자인 체계로.
색: 미리 #3D62AE · 현장 #D07A22 (dataviz validate_palette.js 라이트 모드 전 항목 통과, 10/18)
사용: python render.py [그림이름 ...]   (없으면 전부)"""
import os, sys, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "img_v2"; OUT.mkdir(exist_ok=True)
FONT = pathlib.Path("C:/Windows/Fonts/NotoSansKR-VF.ttf").as_uri()

CSS = """
@font-face{font-family:'NK';src:url('%s');font-weight:100 900}
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#FAF7F2;--card:#FFFFFF;--ink:#1E2330;--ink2:#4A5163;--muted:#8A8F9C;--line:#E7E1D6;
 --pre:#3D62AE;--pre-l:#E6ECF8;--ons:#D07A22;--ons-l:#FBEBDA;--red:#C8463C;--red-l:#F9E3E0;--ok:#2F8F5B;--sand:#F3EBDD}
html,body{width:1400px;height:800px}
body{font-family:'NK',sans-serif;background:var(--bg);color:var(--ink);position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}
.page{position:absolute;inset:0;padding:46px 64px 0 64px}
.kicker{display:flex;align-items:center;gap:10px;font-size:17px;font-weight:700;color:var(--muted);letter-spacing:.02em}
.kicker .dot{width:10px;height:10px;border-radius:50%%;background:var(--ons)}
h1{font-size:44px;font-weight:900;letter-spacing:-.02em;line-height:1.2;margin-top:12px}
h1 em{font-style:normal;color:var(--pre);background:linear-gradient(transparent 62%%,#DCE5F6 62%%)}
h1 em.o{color:var(--ons);background:linear-gradient(transparent 62%%,#F8E0C7 62%%)}
.sub{font-size:20px;color:var(--ink2);margin-top:10px;font-weight:500}
.take{position:absolute;left:64px;right:64px;bottom:64px;background:var(--ink);color:#fff;border-radius:18px;padding:20px 28px;display:flex;align-items:center;gap:18px;font-size:21px;line-height:1.5}
.take b{color:#FFD08A;font-weight:800}
.take .ic{flex:none;width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,.12);display:grid;place-items:center}
.foot{position:absolute;left:64px;right:64px;bottom:20px;display:flex;justify-content:space-between;font-size:14.5px;color:var(--muted)}
.foot .brand{font-weight:800;color:#B9B2A4}
.card{background:var(--card);border-radius:22px;box-shadow:0 1px 0 rgba(30,35,48,.04),0 10px 30px rgba(30,35,48,.07);border:1px solid #EFE9DF}
svg.i{width:26px;height:26px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
""" % FONT

I = {  # 단순 선 아이콘(직접 그림)
 "plane": '<path d="M2 16l20-8-6 12-3-5-5 3 1-5z"/>',
 "bed": '<path d="M3 18V8m0 6h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="2"/>',
 "car": '<path d="M5 16h14M6 16l1.5-5h9L18 16"/><circle cx="8" cy="17" r="1.6"/><circle cx="16" cy="17" r="1.6"/><path d="M4 16h-.5v-2.5L6 11M20 16h.5v-2.5L18 11"/>',
 "ticket": '<path d="M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z"/><path d="M14 7v10" stroke-dasharray="2 2"/>',
 "route": '<circle cx="6" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="M8 6h6a3 3 0 0 1 0 6H10a3 3 0 0 0 0 6h6"/>',
 "fork": '<path d="M7 3v8a2 2 0 0 0 4 0V3M9 11v10M17 3c-2 2-2 6 0 8v10"/>',
 "bus": '<rect x="5" y="4" width="14" height="13" rx="2"/><path d="M5 11h14M8 20v-3M16 20v-3"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "x": '<path d="M6 6l12 12M18 6L6 18"/>',
 "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
 "hand": '<path d="M3 12l4-4 4 2 3-2 7 5-4 4-3-2-2 2-3-2z"/>',
 "id": '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="8.5" cy="12" r="2"/><path d="M13 10.5h5M13 13.5h4"/>',
 "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
 "scale": '<path d="M12 4v16M5 20h14M5 8h14M5 8l-3 6h6zM19 8l-3 6h6z"/>',
}
def ic(name, size=26, color="currentColor", sw=2):
    return f'<svg class="i" viewBox="0 0 24 24" style="width:{size}px;height:{size}px;color:{color};stroke-width:{sw}">{I[name]}</svg>'

def page(kicker, title, sub, body, take, src, extra_css=""):
    subh = f'<div class="sub">{sub}</div>' if sub else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{extra_css}</style></head><body><div class="page">
<div class="kicker"><span class="dot"></span>{kicker}</div><h1>{title}</h1>{subh}{body}</div>
<div class="take"><div class="ic">{ic('bulb', 26, '#FFD08A')}</div><div>{take}</div></div>
<div class="foot"><span>근거 · {src}</span><span class="brand">걷고읽고떠나고</span></div></body></html>"""

FIG = {}
K = "구구절절 · 즉흥 여행은 어디까지 즉흥일까"

# ---------- N1 큰 예약 96% vs 그날 정한 것 40% ----------
def bar_row(icons, label, a, b, pc, pc_col, note):
    t = a + b; wa = a / t * 100
    small = b and b / t < 0.12
    seg_b = (f'<div class="sb" style="flex:{b}">' + ("" if small else f'<span>현장 {b}</span>') + '</div>') if b else ""
    outside = f'<div class="out">현장 {b}</div>' if small else ""
    lb = f'<span>미리 {a}</span>' if wa > 12 else ""
    icn = "".join(f'<span class="chip">{ic(n, 22, "#5B6276")}</span>' for n in icons)
    return f"""<div class="row card"><div class="lab"><div class="chips">{icn}</div><div class="lt">{label}</div><div class="ln">{note}</div></div>
<div class="barw"><div class="bar"><div class="sa" style="flex:{a}">{lb}</div>{seg_b}</div>{outside}</div>
<div class="pc"><div class="pn" style="color:{pc_col}">{pc}<small>%</small></div><div class="pl">미리 정한 비율</div></div></div>"""
N1_CSS = """
.rows{margin-top:30px;display:flex;flex-direction:column;gap:18px}
.row{display:grid;grid-template-columns:300px 1fr 170px;align-items:center;gap:26px;padding:24px 30px}
.chips{display:flex;gap:6px}.chip{width:38px;height:38px;border-radius:11px;background:#F2EEE7;display:grid;place-items:center}
.lt{font-size:23px;font-weight:800;margin-top:10px}.ln{font-size:15.5px;color:var(--muted);margin-top:3px}
.bar{display:flex;gap:3px;height:58px}
.bar>div{border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:19px;min-width:0}
.barw{position:relative}.out{position:absolute;right:0;top:66px;font-size:15px;font-weight:800;color:var(--ons)}
.sa{background:var(--pre)}.sb{background:var(--ons)}.sb span{white-space:nowrap}
.pc{text-align:right}.pn{font-size:64px;font-weight:900;line-height:1;letter-spacing:-.03em}.pn small{font-size:30px;margin-left:2px}
.pl{font-size:15px;color:var(--muted);margin-top:6px}
.legend{display:flex;gap:26px;align-items:center;margin-top:20px;font-size:16px;color:var(--ink2)}
.legend i{display:inline-block;width:16px;height:16px;border-radius:5px;margin-right:8px;vertical-align:-2px}
.legend .m{margin-left:auto;color:var(--muted)}
"""
FIG["N1_big_bookings_first"] = page(K,
    "내 여행 글 68편을 세어 보니, 큰 예약은 <em>96%</em>가 미리였다",
    "블로그 여행 후기 68편(여행 18번)에서 「언제 정했는지」가 적힌 159가지를 직접 셌다",
    '<div class="rows">'
    + bar_row(("plane", "bed", "car", "ticket"), "항공·숙소·렌터카·투어", 48, 2, 96, "var(--pre)", "큰 예약 50가지")
    + bar_row(("route", "fork", "bus"), "동선·식당·현지 교통", 29, 44, 40, "var(--ons)", "그날그날 정한 것 73가지")
    + '</div><div class="legend"><span><i style="background:var(--pre)"></i>미리 · 그날 전에 정함</span><span><i style="background:var(--ons)"></i>현장 · 그 자리에서 정함</span><span class="m">언제 정했는지 글로 알 수 없는 36가지는 뺐다</span></div>',
    "합치면 미리가 63%. 그런데 <b>비행기·숙소는 빠짐없이 미리</b> 잡았고, 어디 갈지·뭘 먹을지는 절반 넘게 현장에서 정했다",
    "블로그 「걷고읽고떠나고」 여행 후기 본문 직접 셈(2026.10.17), 같은 항목은 한 번만", N1_CSS)

# ---------- N5b 미리 한 것과 안 한 것 ----------
N5b_CSS = """
.duo{margin-top:22px;display:grid;grid-template-columns:1fr 64px 1fr;align-items:stretch}
.col{padding:0;overflow:hidden}
.ch{display:flex;align-items:center;gap:12px;padding:18px 26px;font-size:22px;font-weight:800;color:#fff}
.items{padding:14px 26px 6px}
.it{display:flex;gap:16px;align-items:flex-start;padding:10px 0;border-bottom:1px dashed var(--line)}
.it:last-child{border-bottom:0}
.it .b{flex:none;width:46px;height:46px;border-radius:14px;display:grid;place-items:center}
.it .t{font-size:21px;font-weight:800;line-height:1.3}.it .s{font-size:16px;color:var(--ink2);margin-top:3px}
.it .tag{margin-left:auto;flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;margin-top:6px}
.res{margin:6px 26px 22px;border-radius:14px;padding:12px 16px;font-size:18px;font-weight:800;display:flex;align-items:center;gap:10px}
.vs{display:grid;place-items:center}.vs span{width:52px;height:52px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-weight:900;font-size:15px}
.need{margin:12px 0 12px;background:#FAF7F2;border-radius:14px;padding:16px 18px}
.nh{font-size:15px;font-weight:700;color:var(--muted);margin-bottom:10px}
.nr{display:flex;align-items:center;gap:10px;margin-top:8px}
.nr span{display:flex;align-items:center;gap:8px;background:#fff;border-radius:10px;padding:9px 12px;font-size:17px;font-weight:700;border:1px solid var(--line)}
.nx{color:#9AA0AD}.nx em{font-style:normal;margin-left:6px;color:var(--red);font-size:14px;font-weight:800}
.plus{background:none!important;border:0!important;padding:0!important;font-size:20px;color:var(--muted)}
"""
def item(icon, t, s, col, bg, tag):
    tg = ic("check", 18, "#fff", 3) if tag == "ok" else ic("x", 18, "#fff", 3)
    tc = "var(--pre)" if tag == "ok" else "var(--red)"
    return f'<div class="it"><div class="b" style="background:{bg}">{ic(icon, 26, col)}</div><div><div class="t">{t}</div><div class="s">{s}</div></div><div class="tag" style="background:{tc}">{tg}</div></div>'
left = ('<div class="col card"><div class="ch" style="background:var(--pre)">' + ic("check", 24, "#fff", 3) + '미리 한 것</div><div class="items">'
        + item("doc", "공항 촬영 허가 공문", "7월 22일 · 카자흐스탄 한 곳만 신청", "var(--pre)", "var(--pre-l)", "ok")
        + item("plane", "스태프 항공권", "「미리 발권하고」 (9.4 입장문)", "var(--pre)", "var(--pre-l)", "ok")
        + item("hand", "현지 촬영 협조", "「요청해 두었습니다」 (9.4 입장문)", "var(--pre)", "var(--pre-l)", "ok")
        + '</div><div class="res" style="background:var(--pre-l);color:var(--pre)">→ 「즉흥」이라는 소개와 어긋남</div></div>')
right = ('<div class="col card"><div class="ch" style="background:var(--red)">' + ic("x", 24, "#fff", 3) + '미리 안 한 것</div><div class="items">'
         + item("id", "현지 운전 서류(면허 공증)", "「뒤늦게 확인하였습니다」 (8.25 입장문)", "var(--red)", "var(--red-l)", "no")
         + '<div class="need"><div class="nh">현지에서 필요했던 것 · 대사관 안내</div><div class="nr"><span class="nx">' + ic("id", 22, "#9AA0AD") + '<s>한국 국제운전면허증</s><em>인정 안 됨</em></span></div>'
         + '<div class="nr"><span class="nk">' + ic("id", 22, "var(--ok)") + '한국 면허 원본</span><span class="plus">+</span><span class="nk">' + ic("doc", 22, "var(--ok)") + '러시아어 공증 번역본</span></div></div>'
         + '</div><div class="res" style="background:var(--red-l);color:var(--red)">→ 여러 명이 움직이는 해외 촬영에서 위험</div></div>')
FIG["N5b_prepared_or_not"] = page(K,
    "미리 한 것과 안 한 것, <em>입장문</em>이 둘 다 말했다",
    "MBC 입장문(8.25·8.31·9.4)과 공항 촬영 허가 공문(7.22)에서 확인된 것만",
    f'<div class="duo">{left}<div class="vs"><span>VS</span></div>{right}</div>',
    "<b>준비했다면 즉흥이 아니고, 준비하지 않았다면 위험했다</b> — 비판이 양쪽에서 나온 이유. 어느 쪽을 더 무겁게 볼지는 읽는 사람의 몫",
    "MBC 입장문 8.25·9.4, 인천국제공항공사가 국회에 낸 자료(10.16 보도), 주카자흐스탄 대사관 공지(8.20·8.25)", N5b_CSS)

# ================= v3: 글은 제목 한 줄 + 결론 한 줄, 숫자는 입체 블록, 사물은 3D 아이콘 =================
import math
def shade(hexc, f):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 1: r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    else: r, g, b = (int(c * f) for c in (r, g, b))
    return "#%02x%02x%02x" % (r, g, b)
def cubes(n_a, n_b, cols=10, s=30, ca="#3D62AE", cb="#D07A22", gap=0.14):
    """블록 하나 = 결정 하나. 뒤에서부터 미리(ca)를 채우고 앞쪽에 현장(cb)."""
    n = n_a + n_b; rows = math.ceil(n / cols)
    a = s * math.cos(math.pi / 6); b = s * math.sin(math.pi / 6)
    W = (cols + rows) * a + 4; H = (cols + rows) * b + s + 4
    X0 = rows * a + 2; Y0 = s + 2
    def iso(x, y, z): return (X0 + (x - y) * a, Y0 + (x + y) * b - z * s)
    cells = []
    for k in range(n):
        r, c = divmod(k, cols)
        cells.append((c, r, ca if k < n_a else cb))
    cells.sort(key=lambda q: q[0] + q[1])
    out = []
    for x, y, col in cells:
        x0, y0, x1, y1 = x + gap / 2, y + gap / 2, x + 1 - gap / 2, y + 1 - gap / 2
        def poly(pts, fill): return '<polygon points="%s" fill="%s"/>' % (" ".join("%.1f,%.1f" % iso(*q) for q in pts), fill)
        out.append(poly([(x0, y0, 1), (x1, y0, 1), (x1, y1, 1), (x0, y1, 1)], shade(col, 1.28)))
        out.append(poly([(x0, y1, 1), (x1, y1, 1), (x1, y1, 0), (x0, y1, 0)], col))
        out.append(poly([(x1, y0, 1), (x1, y1, 1), (x1, y1, 0), (x1, y0, 0)], shade(col, 0.74)))
    return '<svg width="%d" height="%d" viewBox="0 0 %.0f %.0f">%s</svg>' % (W, H, W, H, "".join(out))

V3_CSS = """
h1{font-size:50px;margin-top:6px}
.kicker{font-size:16px}
.take{bottom:58px;padding:18px 28px;font-size:24px;font-weight:600}
.take b{font-weight:900}
.icon3d{display:block;object-fit:contain}
"""
N1v3_CSS = V3_CSS + """
.two{margin-top:26px;display:grid;grid-template-columns:1fr 1fr;gap:28px}
.pan{position:relative;height:470px;padding:22px 26px;overflow:hidden}
.pan .hd{display:flex;align-items:center;gap:14px}
.pan .hd img{width:92px;height:92px;margin:-10px -6px -10px -12px}
.pan .nm{font-size:25px;font-weight:900;line-height:1.25}
.pan .cnt{font-size:16px;color:var(--muted);font-weight:600;margin-top:2px}
.pan .blk{position:absolute;left:26px;bottom:24px}
.pan .big{position:absolute;right:28px;bottom:22px;text-align:right}
.pan .big b{display:block;font-size:92px;font-weight:900;line-height:.9;letter-spacing:-.04em}
.pan .big b small{font-size:40px}
.pan .big span{font-size:16px;color:var(--muted);font-weight:700}
.lg{position:absolute;right:64px;top:62px;display:flex;gap:18px;font-size:16px;font-weight:700;color:var(--ink2)}
.lg i{display:inline-block;width:15px;height:15px;border-radius:4px;margin-right:6px;vertical-align:-2px}
"""
def pan(icon, name, cnt, a, b, pc, col):
    return (f'<div class="pan card"><div class="hd"><img class="icon3d" src="icons/{icon}_t.png"><div><div class="nm">{name}</div><div class="cnt">{cnt}</div></div></div>'
            f'<div class="blk">{cubes(a, b, cols=10, s=27)}</div>'
            f'<div class="big"><b style="color:{col}">{pc}<small>%</small></b><span>미리 정한 비율</span></div></div>')
FIG["N1_v3"] = page("구구절절 · 내 여행 글 68편",
    "큰 예약은 <em>96%</em>가 미리였다", "",
    '<div class="lg"><span><i style="background:var(--pre)"></i>미리</span><span><i style="background:var(--ons)"></i>현장</span><span style="color:var(--muted)">블록 하나 = 결정 하나</span></div>'
    + '<div class="two">' + pan("suitcase", "항공·숙소·렌터카·투어", "미리 48 · 현장 2", 48, 2, 96, "var(--pre)")
    + pan("map", "동선·식당·현지 교통", "미리 29 · 현장 44", 29, 44, 40, "var(--ons)") + '</div>',
    "비행기·숙소는 <b>미리</b>, 즉흥은 <b>동선과 식당</b>에서",
    "내 블로그 여행 후기 68편 직접 셈(2026.10.17) · 언제 정했는지 알 수 없는 36가지 제외", N1v3_CSS)

N5bv3_CSS = V3_CSS + """
.duo{margin-top:26px;display:grid;grid-template-columns:1.55fr 1fr;gap:28px}
.box{position:relative;height:470px;padding:22px 26px}
.box .hd{display:inline-flex;align-items:center;gap:10px;font-size:22px;font-weight:900;color:#fff;border-radius:999px;padding:9px 18px}
.objs{display:flex;justify-content:space-around;margin-top:18px}
.ob{width:230px;text-align:center;position:relative}
.ob img{width:210px;height:210px;margin:0 auto}
.ob .l{font-size:21px;font-weight:800;margin-top:-6px}
.ob .d{font-size:15.5px;color:var(--muted);font-weight:600;margin-top:4px}
.badge{position:absolute;top:16px;right:18px;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;box-shadow:0 4px 10px rgba(0,0,0,.15)}
.res{position:absolute;left:26px;right:26px;bottom:22px;border-radius:14px;padding:13px 18px;font-size:20px;font-weight:900;text-align:center}
"""
def ob(icon, l, d, ok=True):
    bg = "var(--pre)" if ok else "var(--red)"
    mark = ic("check", 24, "#fff", 3) if ok else ic("x", 24, "#fff", 3)
    badge = f'<div class="badge" style="background:{bg}">{mark}</div>' if ok else ""   # 면허증 아이콘엔 빨간 X 가 이미 있음
    return f'<div class="ob"><img class="icon3d" src="icons/{icon}_t.png">{badge}<div class="l">{l}</div><div class="d">{d}</div></div>'
FIG["N5b_v3"] = page("구구절절 · MBC 입장문이 말한 것",
    "미리 한 것 <em>셋</em>, 안 한 것 <em class='o'>하나</em>", "",
    '<div class="duo"><div class="box card"><span class="hd" style="background:var(--pre)">' + ic("check", 22, "#fff", 3) + '미리 한 것</span><div class="objs">'
    + ob("permit", "촬영 허가 공문", "7월 22일") + ob("tickets", "스태프 항공권", "미리 발권") + ob("camera", "현지 촬영 협조", "미리 요청") + '</div>'
    + '<div class="res" style="background:var(--pre-l);color:var(--pre)">→ 「즉흥」과 어긋난다</div></div>'
    + '<div class="box card"><span class="hd" style="background:var(--red)">' + ic("x", 22, "#fff", 3) + '안 한 것</span><div class="objs">'
    + ob("license", "운전 서류(면허 공증)", "「뒤늦게 확인」", ok=False) + '</div>'
    + '<div class="res" style="background:var(--red-l);color:var(--red)">→ 여러 명이 움직이는 촬영에서 위험</div></div></div>',
    "준비했으면 <b>즉흥이 아니고</b>, 안 했으면 <b>위험했다</b>",
    "MBC 입장문 8.25·9.4, 인천국제공항공사가 국회에 낸 자료(10.16 보도), 주카자흐스탄 대사관 공지", N5bv3_CSS)

def render(names):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 800}, device_scale_factor=2)
        for n in names:
            html = FIG[n]
            tmp = HERE / f"_{n}.html"; tmp.write_text(html, encoding="utf-8")
            pg.goto(tmp.as_uri()); pg.wait_for_timeout(300)
            over = pg.evaluate("""() => { const W=1400,H=800; const bad=[];
              document.querySelectorAll('.page *, .take, .foot').forEach(e=>{const r=e.getBoundingClientRect(); if(r.width&&(r.right>W-8||r.bottom>H-4||e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible')) bad.push(e.className||e.tagName)});
              const t=document.querySelector('.take').getBoundingClientRect(); let lowest=0; document.querySelectorAll('.page > *').forEach(e=>{lowest=Math.max(lowest,e.getBoundingClientRect().bottom)});
              return {bad:bad.slice(0,8), gap: Math.round(t.top-lowest)} }""")
            pg.screenshot(path=str(OUT / f"{n}.png"))
            print("saved", n, over)
        b.close()

if __name__ == "__main__":
    render(sys.argv[1:] or list(FIG))
