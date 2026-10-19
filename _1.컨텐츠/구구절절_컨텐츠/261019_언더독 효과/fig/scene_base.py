# -*- coding: utf-8 -*-
"""언더독 효과 글 「장면판」 공용 — 구구절절 지침 3장 🎬(나혼산 scene_figs.py 에서 가져옴).
색: 언더독(돈 적은 쪽) 주황 #D07A22 · 강자(돈 많은 쪽) 파랑 #3D62AE · 해체·위험 빨강 #C8463C."""
import pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "img_v2"; OUT.mkdir(exist_ok=True)
FONT = pathlib.Path("C:/Windows/Fonts/NotoSansKR-VF.ttf").as_uri()
TOTAL = 18
UD, TOP, RED = "#D07A22", "#3D62AE", "#C8463C"

BASE = """
@font-face{font-family:'NK';src:url('%s');font-weight:100 900}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1400px;height:800px}
body{font-family:'NK',sans-serif;color:#1E2330;position:relative;overflow:hidden;-webkit-font-smoothing:antialiased;background:#EFE7D8;word-break:keep-all}
.label{position:absolute;left:44px;top:38px;background:#FFFCF5;padding:16px 26px 18px;transform:rotate(-1.2deg);
 box-shadow:0 2px 0 rgba(60,45,20,.06),0 12px 26px rgba(60,45,20,.18);z-index:5}
.label:before{content:"";position:absolute;left:38%%;top:-12px;width:110px;height:26px;background:rgba(208,122,34,.32);transform:rotate(2deg)}
.label .k{font-size:14px;font-weight:800;letter-spacing:.14em;color:#8A7F6A}
.label h1{font-size:40px;font-weight:900;letter-spacing:-.02em;margin-top:4px;white-space:nowrap}
.label h1 em{font-style:normal;color:#D07A22}
.src{position:absolute;left:44px;bottom:16px;font-size:13px;color:#6E6656;z-index:5;background:rgba(255,252,245,.86);padding:3px 8px;border-radius:4px}
.brand{position:absolute;right:30px;bottom:16px;font-size:13px;font-weight:800;letter-spacing:.14em;color:#4A4232;z-index:5;background:rgba(255,252,245,.86);padding:3px 8px;border-radius:4px}
.tag{position:absolute;z-index:6;background:#FFFCF5;border-radius:8px;padding:10px 16px 10px 30px;box-shadow:0 8px 18px rgba(30,25,15,.22)}
.tag:before{content:"";position:absolute;left:11px;top:50%%;width:10px;height:10px;margin-top:-5px;border-radius:50%%;background:#EFE7D8;box-shadow:inset 0 0 0 2px rgba(0,0,0,.18)}
.tag b{display:block;font-size:44px;font-weight:900;line-height:1;letter-spacing:-.03em}
.tag span{display:block;font-size:15px;font-weight:800;color:#4A5163;margin-top:5px;text-wrap:balance}
.tag.t2 b{font-size:27px}
.stamp{position:absolute;transform:rotate(-7deg);border:4px solid #D07A22;color:#D07A22;border-radius:12px;padding:9px 18px;z-index:6;
 font-size:24px;font-weight:900;background:rgba(255,252,245,.9);white-space:nowrap}
""" % FONT

def frame(no, kicker, title, body, src, css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{css}</style></head><body>
{body}<div class="label"><div class="k">구구절절 · {kicker} · {no:02d} / {TOTAL}</div><h1>{title}</h1></div>
<div class="src">근거 · {src}</div><div class="brand">걷고읽고떠나고</div></body></html>"""

def bg(name):
    return f'<img src="scenes/{name}.png" style="position:absolute;left:0;top:0;width:1400px;height:800px;object-fit:cover">'

def tag(x, y, head, sub, color, rot=0, w=None, small=False):
    ws = f"width:{w}px;" if w else ""
    return f'<div class="tag{" t2" if small else ""}" style="left:{x}px;top:{y}px;{ws}transform:rotate({rot}deg)"><b style="color:{color}">{head}</b><span>{sub}</span></div>'

def stamp(x, y, text, color=UD):
    return f'<div class="stamp" style="left:{x}px;top:{y}px;border-color:{color};color:{color}">{text}</div>'

def render(figs, names=None):
    names = names or list(figs)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 800}, device_scale_factor=2)
        for n in names:
            tmp = HERE / f'_{n}.html'; tmp.write_text(figs[n], encoding='utf-8'); pg.goto(tmp.as_uri()); pg.wait_for_timeout(300)
            bad = pg.evaluate("() => [...document.querySelectorAll('.label,.tag,.stamp,.src')].filter(e=>{const r=e.getBoundingClientRect();return r.right>1395||r.bottom>798||r.left<0}).map(e=>e.className)")
            pg.screenshot(path=str(OUT / f'{n}.png')); print('saved', n, bad or 'OK')
        b.close()
