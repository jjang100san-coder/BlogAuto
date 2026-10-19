# -*- coding: utf-8 -*-
"""「장면판」 시안(10/18 사용자 「발표형 ppt 같다 — 이미지 자체에 창의성」).
그림마다 장면 하나가 주인공. 숫자는 장면 위 꼬리표·깃발로, 제목은 왼쪽 위 종이 띠 하나. 옆 단·큰 머리띠 없음.
 - 개념 그림: AI 장면(글자 없음) + HTML 꼬리표
 - 숫자 그림: 데이터 모양 그대로 그린 장면(SVG)"""
import json, datetime as dt, math, sys, pathlib
from ticket_cards_base import HERE, FONT, OUT
from playwright.sync_api import sync_playwright
def render(figs, names=None):
    names = names or list(figs)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 800}, device_scale_factor=2)
        for n in names:
            tmp = HERE / f'_{n}.html'; tmp.write_text(figs[n], encoding='utf-8'); pg.goto(tmp.as_uri()); pg.wait_for_timeout(300)
            bad = pg.evaluate("() => [...document.querySelectorAll('.label,.tag,.stamp,.src')].filter(e=>{const r=e.getBoundingClientRect();return r.right>1395||r.bottom>798||r.left<0}).map(e=>e.className)")
            pg.screenshot(path=str(OUT / f'{n}.png')); print('saved', n, bad or 'OK')
        b.close()

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
.src{position:absolute;left:44px;bottom:16px;font-size:13px;color:#6E6656;z-index:5;background:rgba(255,252,245,.82);padding:3px 8px;border-radius:4px}
.brand{position:absolute;right:30px;bottom:16px;font-size:13px;font-weight:800;letter-spacing:.14em;color:#4A4232;z-index:5;background:rgba(255,252,245,.82);padding:3px 8px;border-radius:4px}
.tag{position:absolute;z-index:6;background:#FFFCF5;border-radius:8px;padding:10px 16px 10px 30px;box-shadow:0 8px 18px rgba(30,25,15,.22)}
.tag:before{content:"";position:absolute;left:11px;top:50%%;width:10px;height:10px;margin-top:-5px;border-radius:50%%;background:#EFE7D8;box-shadow:inset 0 0 0 2px rgba(0,0,0,.18)}
.tag b{display:block;font-size:46px;font-weight:900;line-height:1;letter-spacing:-.03em}
.tag span{display:block;font-size:15px;font-weight:800;color:#4A5163;margin-top:4px}
.string{position:absolute;z-index:5;border-top:2px dashed rgba(30,25,15,.45);transform-origin:0 0}
.stamp{position:absolute;transform:rotate(-7deg);border:4px solid #D07A22;color:#D07A22;border-radius:12px;padding:9px 18px;z-index:6;
 font-size:24px;font-weight:900;background:rgba(255,252,245,.9);white-space:nowrap}
""" % FONT
F = {}
def frame(no, kicker, title, body, src, css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{css}</style></head><body>
{body}<div class="label"><div class="k">구구절절 · {kicker} · {no:02d} / 13</div><h1>{title}</h1></div>
<div class="src">근거 · {src}</div><div class="brand">걷고읽고떠나고</div><div class="take" style="display:none"></div><div class="page"></div></body></html>"""

# ---- 07 검색 산맥: 데이터 모양 그대로 ----
raw = json.load(open(HERE.parent / "base data" / "_raw_데이터랩_카자흐스탄_2026-10-17.json", encoding="utf-8"))
dd = {r["period"]: r["ratio"] for r in raw["results"][0]["data"]}
D0, D1 = dt.date(2026, 8, 10), dt.date(2026, 10, 16)
days = [D0 + dt.timedelta(i) for i in range((D1 - D0).days + 1)]
X0, X1, GY, TOP = 40, 1360, 690, 190
def gx(d): return X0 + (d - D0).days / (D1 - D0).days * (X1 - X0)
def gy(v): return GY - v / 100 * (GY - TOP)
pts = [(gx(d), gy(dd.get(d.isoformat(), 0))) for d in days]
def smooth(p, k):
    out = []
    for i in range(len(p)):
        a = p[max(0, i - k):i + k + 1]; out.append((p[i][0], sum(y for _, y in a) / len(a)))
    return out
def ridge(p, fill, dy=0, scale=1.0):
    s = " ".join("%.1f,%.1f" % (x, GY - (GY - y) * scale + dy) for x, y in p)
    return f'<polygon points="0,800 0,{GY + dy:.0f} {s} 1400,{GY + dy:.0f} 1400,800" fill="{fill}"/>'
svg = ['<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">',
       '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDE7F4"/><stop offset="1" stop-color="#F6F1E6"/></linearGradient>'
       '<linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3D62AE"/><stop offset="1" stop-color="#22335A"/></linearGradient></defs>',
       '<rect width="1400" height="800" fill="url(#sky)"/>',
       '<circle cx="1240" cy="150" r="46" fill="#FFE2B3" opacity=".9"/>',
       ridge(smooth(pts, 6), "#C9D5EA", -6, 0.55), ridge(smooth(pts, 3), "#8FA6D2", 0, 0.8), ridge(pts, "url(#m1)")]
# 눈 덮인 정상(8.26)
pk = max(pts, key=lambda q: -q[1])
svg.append(f'<polygon points="{pk[0] - 16:.1f},{pk[1] + 34:.1f} {pk[0]:.1f},{pk[1]:.1f} {pk[0] + 13:.1f},{pk[1] + 30:.1f} {pk[0] + 5:.1f},{pk[1] + 24:.1f} {pk[0] - 4:.1f},{pk[1] + 30:.1f}" fill="#FFFFFF" opacity=".92"/>')
EV = ((dt.date(2026, 8, 14), "1편 방송", "#8FA6D2"), (dt.date(2026, 8, 21), "2편 · 알마티 보도", "#8FA6D2"), (dt.date(2026, 8, 25), "1차 입장", "#D07A22"),
      (dt.date(2026, 8, 31), "2차 입장", "#D07A22"), (dt.date(2026, 9, 4), "3차 입장", "#D07A22"), (dt.date(2026, 10, 16), "공문 보도", "#C8463C"))
for i, (d, lab, col) in enumerate(EV):
    x, y = gx(d), gy(dd.get(d.isoformat(), 0))
    h = 54 if lab not in ("2차 입장",) else 54
    svg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - h:.1f}" stroke="#1E2330" stroke-width="2.5"/><polygon points="{x:.1f},{y - h:.1f} {x + 30:.1f},{y - h + 8:.1f} {x:.1f},{y - h + 16:.1f}" fill="{col}"/>')
    ty = y - h - 12; anchor = "end" if (d == D1 or lab == "2차 입장") else ("start" if lab == "3차 입장" else "middle")
    tx = x + (0 if anchor == "middle" else -6 if anchor == "end" else 6)
    svg.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" font-size="17" font-weight="900" fill="#1E2330" paint-order="stroke" stroke="#F6F1E6" stroke-width="5">{d.month}.{d.day} {lab}</text>')
# 땅의 날짜
for m, d in ((8, 15), (9, 1), (9, 15), (10, 1), (10, 15)):
    x = gx(dt.date(2026, m, d)); svg.append(f'<text x="{x:.1f}" y="{GY + 34}" text-anchor="middle" font-size="14" font-weight="700" fill="#C9D5EA">{m}.{d}</text>')
svg.append('</svg>')
tag = (f'<div class="tag" style="left:{pk[0] + 70:.0f}px;top:{pk[1] - 18:.0f}px"><b style="color:#3D62AE">8.26</b><span>검색이 가장 높았던 날 · 1차 입장문 다음 날</span></div>')
stamp = '<div class="stamp" style="left:820px;top:262px">해명이 바뀔 때마다 다시 솟았다</div>'
F["S_N5c_search_peaks"] = frame(7, "왜 계속 화제였나", "검색이 다시 뜬 날 = <em>새 사실</em>이 나온 날", "".join(svg) + tag + stamp,
    "네이버 데이터랩 검색어트렌드(검색어 8개 묶음, 2026.10.17) · 산 높이 = 상대 검색량, 가장 높은 날 100")


# ---- 01 큰 예약 96%: AI 장면(정돈된 가방 vs 자유로운 지도) + 꼬리표 ----
def minibar(a, b, w=230):
    t = a + b
    return (f'<div style="display:flex;gap:2px;height:12px;width:{w}px;margin-top:8px">'
            f'<div style="flex:{a};background:#3D62AE;border-radius:3px"></div>' + (f'<div style="flex:{b};background:#D07A22;border-radius:3px"></div>' if b else "") + '</div>')
N1_BODY = ('<img src="scenes/N1_flatlay.png" style="position:absolute;left:0;top:0;width:1400px;height:800px;object-fit:cover">'
           '<div class="tag" style="left:34px;top:300px;transform:rotate(-3deg)"><b style="color:#3D62AE">96%</b><span>항공·숙소·렌터카·투어<br>미리 48 · 현장 2</span>' + minibar(48, 2, 200) + '</div>'
           '<div class="tag" style="left:930px;top:612px;transform:rotate(2deg)"><b style="color:#D07A22">40%</b><span>동선·식당·현지 교통 · 미리 29 · 현장 44</span>' + minibar(29, 44, 330) + '</div>'
           '<div class="stamp" style="left:760px;top:70px">비행기·숙소는 미리, 즉흥은 그날</div>')
F["S_N1_big_bookings"] = frame(1, "내 여행 글 68편", "큰 예약은 <em>96%</em>가 미리였다", N1_BODY,
    "내 블로그 여행 후기 68편 직접 셈(2026.10.17) · 알 수 없음 36 제외 · 사진은 AI 생성 장면(실제 내 가방 아님)")

# ---- 05 날짜순: 라이트박스 위 필름 띠(한 칸 = 한 사건, 칸 사이 = 지난 날수) ----
EV5 = (("7.22", "공항에 촬영<br>허가 공문", "#8A8272"), ("8.6", "출국", "#8A8272"), ("8.14", "1편 방송", "#3D62AE"),
       ("8.21", "2편 방송", "#3D62AE"), ("8.25", "1차 입장", "#D07A22"), ("8.31", "2차 입장", "#D07A22"),
       ("9.4", "3차 입장", "#D07A22"), ("10.16", "공문 보도", "#C8463C"))
GAP5 = (15, 8, 7, 4, 6, 4, 42)
s5 = ['<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">',
      '<defs><radialGradient id="lb" cx=".5" cy=".55" r=".75"><stop offset="0" stop-color="#FFFDF6"/><stop offset="1" stop-color="#E9DFCB"/></radialGradient></defs>',
      '<rect width="1400" height="800" fill="url(#lb)"/>']
FW, FG, SPL, SX, SY, SH = 132, 22, 120, 46, 300, 240
xs = []; x = SX
for i in range(8):
    xs.append(x); x += FW + (SPL if i == 6 else FG)
segs = ((SX - 46, xs[6] + FW + 30), (xs[7] - 30, 1400))
for a, b in segs:
    s5.append(f'<rect x="{a}" y="{SY}" width="{b - a}" height="{SH}" fill="#2A2522"/>')
    for hx in range(a + 10, b - 14, 34):
        for hy in (SY + 12, SY + SH - 26):
            s5.append(f'<rect x="{hx}" y="{hy}" width="18" height="14" rx="3" fill="#FBF4E4"/>')
# 이음 테이프(42일)
mx = xs[6] + FW + SPL / 2
s5.append(f'<rect x="{mx - 40}" y="{SY - 18}" width="80" height="{SH + 36}" fill="rgba(208,122,34,.30)" transform="rotate(4 {mx} {SY + SH / 2})"/>')
s5.append(f'<text x="{mx:.0f}" y="{SY - 34}" text-anchor="middle" font-size="18" font-weight="900" fill="#C8463C">42일 뒤</text>')
for i, (d, e, c) in enumerate(EV5):
    x = xs[i]
    s5.append(f'<rect x="{x}" y="{SY + 42}" width="{FW}" height="{SH - 84}" rx="4" fill="{c}" opacity=".92"/>'
              f'<rect x="{x}" y="{SY + 42}" width="{FW}" height="{SH - 84}" rx="4" fill="url(#lb)" opacity=".18"/>')
    s5.append(f'<text x="{x + FW / 2}" y="{SY + 100}" text-anchor="middle" font-size="30" font-weight="900" fill="#FFFCF5">{d}</text>')
for i, g in enumerate(GAP5[:-1]):
    gx_ = xs[i] + FW + FG / 2
    s5.append(f'<text x="{gx_:.0f}" y="{SY + SH + 34}" text-anchor="middle" font-size="16" font-weight="800" fill="#6E6656">{g}일</text>')
s5.append('</svg>')
ev5 = "".join(f'<div style="position:absolute;left:{xs[i]}px;top:{SY + 112}px;width:{FW}px;text-align:center;color:#FFFCF5;font-size:17px;font-weight:800;line-height:1.3;z-index:4">{e}</div>' for i, (d, e, c) in enumerate(EV5))
tag5 = ('<div class="tag" style="left:1010px;top:96px;transform:rotate(2deg)"><b style="color:#D07A22">3번</b><span>MBC 입장문 · 8.25 → 8.31 → 9.4</span></div>'
        '<div class="tag" style="left:1050px;top:620px;transform:rotate(-2deg)"><b style="color:#3D62AE">86일</b><span>7.22 공문 → 10.16 보도</span></div>')
stamp5 = '<div class="stamp" style="left:300px;top:640px">처음 발표는 일주일 뒤 고쳐졌다</div>'
F["S_N5_dates_in_order"] = frame(5, "날짜순", "방송 석 주 전 공문부터 <em>10월</em> 보도까지", "".join(s5) + ev5 + tag5 + stamp5,
    "한겨레·텐아시아·스포티비뉴스 10.16(인천국제공항공사가 국회에 낸 자료), MBC 입장문 8.25·8.31·9.4 · 칸 사이 숫자 = 지난 날수")

# ---- 10 종류별: 빨랫줄에 걸린 짐표 일곱 장(파랑 = 미리, 주황 = 현장) ----
K10 = (("항공", 6, 0), ("숙소", 17, 0), ("렌터카", 10, 1), ("투어·입장권", 15, 1), ("동선", 17, 18), ("현지 교통", 3, 6), ("식당", 6, 13))
s10 = ['<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">',
       '<defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E4EAF2"/><stop offset="1" stop-color="#F4EFE4"/></linearGradient></defs>',
       '<rect width="1400" height="800" fill="url(#wall)"/>',
       '<path d="M-10 214 Q700 262 1410 214" fill="none" stroke="#7A6A50" stroke-width="3"/>']
TW, TH, TY0 = 136, 330, 270
for i, (l, a, b) in enumerate(K10):
    cx = 120 + i * 194; ry_ = 214 + 48 * (1 - ((cx - 700) / 710) ** 2)
    pc = round(a / (a + b) * 100); hb = (TH - 84) * a / (a + b)
    top = TY0 + (i % 2) * 14; rot = (-3, 2, -2, 3, -1, 2, -3)[i]
    s10.append(f'<g transform="rotate({rot} {cx} {ry_:.0f})">'
               f'<line x1="{cx}" y1="{ry_:.0f}" x2="{cx}" y2="{top + 18}" stroke="#7A6A50" stroke-width="2"/>'
               f'<rect x="{cx - TW / 2 + 4}" y="{top + 8}" width="{TW}" height="{TH}" rx="12" fill="rgba(40,30,15,.16)"/>'
               f'<rect x="{cx - TW / 2}" y="{top}" width="{TW}" height="{TH}" rx="12" fill="#FFFCF5"/>'
               f'<circle cx="{cx}" cy="{top + 20}" r="8" fill="#E4EAF2" stroke="#B9AE98" stroke-width="2"/>'
               f'<text x="{cx}" y="{top + 58}" text-anchor="middle" font-size="19" font-weight="900" fill="#1E2330">{l}</text>'
               f'<rect x="{cx - TW / 2 + 14}" y="{top + 70}" width="{TW - 28}" height="{TH - 84 - hb:.1f}" rx="4" fill="#D07A22"/>'
               f'<rect x="{cx - TW / 2 + 14}" y="{top + TH - 14 - hb:.1f}" width="{TW - 28}" height="{hb:.1f}" rx="4" fill="#3D62AE"/>'
               f'<text x="{cx}" y="{top + TH + 52}" text-anchor="middle" font-size="40" font-weight="900" fill="{"#3D62AE" if pc >= 50 else "#D07A22"}">{pc}%</text>'
               f'<text x="{cx}" y="{top + TH + 80}" text-anchor="middle" font-size="16" font-weight="800" fill="#6E6656">미리 {a} · 현장 {b}</text></g>')
s10.append('<rect x="1010" y="70" width="18" height="18" rx="3" fill="#3D62AE"/><text x="1036" y="86" font-size="17" font-weight="800" fill="#4A5163">미리 정함</text>'
           '<rect x="1150" y="70" width="18" height="18" rx="3" fill="#D07A22"/><text x="1176" y="86" font-size="17" font-weight="800" fill="#4A5163">그날 정함</text></svg>')
F["S_H1_by_kind"] = frame(10, "한 걸음 더 · 종류별", "항공·숙소는 <em>전부</em> 미리, 식당은 셋 중 하나", "".join(s10),
    "여행 후기 결정 항목 중 시점이 적힌 123가지(직접 셈) · 기타 10가지 제외 · 미리는 일정표 1개, 현장은 들른 곳마다 셈")

# ---- 11 옛 신문: 십 년마다 쌓인 신문 더미(높이 = 기사 수) ----
DEC = ("1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s")
MU = (79, 38, 2, 26, 254, 63, 61, 109); BP = (0, 0, 0, 0, 0, 0, 4, 2162); JH = (0, 0, 0, 0, 0, 0, 1, 2)
FY, PX = 640, 1.6
s11 = ['<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">',
       '<defs><linearGradient id="room" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3ECDD"/><stop offset="1" stop-color="#E6DAC2"/></linearGradient>'
       '<pattern id="pp" width="10" height="7" patternUnits="userSpaceOnUse"><rect width="10" height="7" fill="#EFE6D2"/><line x1="0" y1="6.5" x2="10" y2="6.5" stroke="#C9BC9F" stroke-width="1"/></pattern>'
       '<pattern id="pb" width="10" height="7" patternUnits="userSpaceOnUse"><rect width="10" height="7" fill="#D6E0F2"/><line x1="0" y1="6.5" x2="10" y2="6.5" stroke="#3D62AE" stroke-width="1"/></pattern></defs>',
       '<rect width="1400" height="800" fill="url(#room)"/>',
       f'<rect x="0" y="{FY}" width="1400" height="{800 - FY}" fill="#C9AE84"/><rect x="0" y="{FY}" width="1400" height="5" fill="#A88C62"/>']
def stack(x, n, fill, w=58):
    h = n * PX
    if h < 3 and n: h = 3
    if not n: return ""
    top = FY - h
    out = f'<rect x="{x + 4}" y="{top + 4:.1f}" width="{w}" height="{h:.1f}" fill="rgba(60,40,10,.18)"/><rect x="{x}" y="{top:.1f}" width="{w}" height="{h:.1f}" fill="url(#{fill})" stroke="#B9AE98" stroke-width="1"/>'
    if h > 40: out += f'<rect x="{x + w / 2 - 3}" y="{top:.1f}" width="6" height="{h:.1f}" fill="{"#A88C62" if fill == "pp" else "#22335A"}" opacity=".55"/>'
    return out
for k, d in enumerate(DEC):
    cx = 110 + k * 160
    s11.append(stack(cx - 62, MU[k], "pp"))
    if BP[k]: s11.append(stack(cx + 4, BP[k], "pb"))
    if MU[k] > 20: s11.append(f'<text x="{cx - 33}" y="{FY - MU[k] * PX - 10:.0f}" text-anchor="middle" font-size="16" font-weight="900" fill="#6E6656">{MU[k]}</text>')
    if 0 < BP[k] < 300: s11.append(f'<text x="{cx + 33}" y="{FY - BP[k] * PX - 10:.0f}" text-anchor="middle" font-size="16" font-weight="900" fill="#22335A">{BP[k]}</text>')
    s11.append(f'<text x="{cx}" y="{FY + 38}" text-anchor="middle" font-size="18" font-weight="800" fill="#4A3A22">{d}</text>')
    for j in range(JH[k]):  # 즉흥여행 기사 = 바닥에 놓인 빨간 표시 신문 한 장
        jx = cx - 40 + j * 46
        s11.append(f'<g transform="rotate({-8 + j * 12} {jx + 20} {FY + 80})"><rect x="{jx}" y="{FY + 62}" width="44" height="32" fill="#FFFCF5" stroke="#C8463C" stroke-width="3"/>'
                   f'<line x1="{jx + 6}" y1="{FY + 72}" x2="{jx + 38}" y2="{FY + 72}" stroke="#C8463C" stroke-width="3"/><line x1="{jx + 6}" y1="{FY + 82}" x2="{jx + 30}" y2="{FY + 82}" stroke="#D9CFBC" stroke-width="3"/></g>')
bx = 110 + 7 * 160 + 4
s11.append(f'<text x="{bx + 29}" y="200" text-anchor="middle" font-size="26" font-weight="900" fill="#22335A" paint-order="stroke" stroke="#F3ECDD" stroke-width="6">2,162 ↑</text>')
s11.append('</svg>')
tag11 = ('<div class="tag" style="left:860px;top:300px;transform:rotate(-2deg)"><b style="color:#C8463C">3번</b><span>「즉흥여행」 · 첫 기사 1989.1.31<br>바닥의 빨간 신문 한 장 = 기사 한 건</span></div>'
         '<div style="position:absolute;left:44px;top:200px;z-index:5;font-size:17px;font-weight:800;color:#4A5163;background:rgba(255,252,245,.85);padding:8px 14px;border-radius:6px">'
         '<span style="display:inline-block;width:16px;height:16px;background:#EFE6D2;border:1px solid #B9AE98;vertical-align:-3px;margin-right:6px"></span>무전여행 632'
         '<span style="display:inline-block;width:16px;height:16px;background:#D6E0F2;border:1px solid #3D62AE;vertical-align:-3px;margin:0 6px 0 18px"></span>배낭여행 2,166</div>')
F["S_H2_old_papers"] = frame(11, "한 걸음 더 · 옛 신문", "1920~1999 신문에 「즉흥여행」은 <em>세 번</em>", "".join(s11) + tag11,
    "네이버 뉴스 라이브러리 5개 신문, 따옴표 구절 검색(2026.10.17) · 더미 높이 = 그 말이 나온 기사 수 · 1960년대 무전여행은 영화 광고 많음")

# ---- 13 시청률: 아파트 아홉 동(높이 = 가구 시청률) ----
RT = (("8.14", 5.8), ("8.21", 6.5), ("8.28", 5.1), ("9.4", 5.2), ("9.11", 4.8), ("9.18", 4.2), ("9.25", 3.5), ("10.2", 6.0), ("10.9", 5.0))
GY13 = 660
s13 = ['<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">',
       '<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFE0F2"/><stop offset="1" stop-color="#F5F0E6"/></linearGradient></defs>',
       '<rect width="1400" height="800" fill="url(#sk)"/>',
       '<ellipse cx="300" cy="150" rx="120" ry="22" fill="#FFFFFF" opacity=".7"/><ellipse cx="1180" cy="230" rx="90" ry="16" fill="#FFFFFF" opacity=".6"/>',
       f'<rect x="0" y="{GY13}" width="1400" height="{800 - GY13}" fill="#B9C3AE"/><rect x="0" y="{GY13}" width="1400" height="4" fill="#97A38A"/>']
import random
rnd = random.Random(13)
for i, (d, v) in enumerate(RT):
    x = 92 + i * 140; w = 104; h = v * 66; top = GY13 - h
    body = "#E9DCC6" if d != "9.25" else "#F3D9BC"
    s13.append(f'<rect x="{x + 6}" y="{top + 6:.0f}" width="{w}" height="{h:.0f}" fill="rgba(40,40,60,.14)"/><rect x="{x}" y="{top:.0f}" width="{w}" height="{h:.0f}" fill="{body}" stroke="#B8A888" stroke-width="1.5"/>'
               f'<rect x="{x - 4}" y="{top - 8:.0f}" width="{w + 8}" height="10" fill="#A8977A"/>')
    for fy in range(int(top) + 16, GY13 - 14, 26):
        for c in range(4):
            lit = rnd.random() < 0.35
            col = ("#7FA7E0" if d != "9.25" else "#E9A25B") if lit else "#CFC4B0"
            s13.append(f'<rect x="{x + 12 + c * 23}" y="{fy}" width="14" height="14" rx="2" fill="{col}"/>')
    c = "#D07A22" if d == "9.25" else "#22335A"
    s13.append(f'<text x="{x + w / 2}" y="{top - 20:.0f}" text-anchor="middle" font-size="30" font-weight="900" fill="{c}">{v}</text>'
               f'<text x="{x + w / 2}" y="{GY13 + 40}" text-anchor="middle" font-size="18" font-weight="800" fill="#3E4A36">{d}</text>')
s13.append('</svg>')
tag13 = '<div style="position:absolute;left:910px;top:718px;width:150px;text-align:center;z-index:5;font-size:17px;font-weight:900;color:#D07A22">추석 기간</div>'
stamp13 = '<div class="stamp" style="left:860px;top:110px">이 숫자만으로 원인은 말할 수 없다</div>'
F["S_H4_ratings"] = frame(13, "한 걸음 더 · 시청률", "그동안의 시청률 — <em>숫자만</em>", "".join(s13) + tag13 + stamp13,
    "닐슨코리아 전국 가구 시청률(각 회차 보도) · 건물 높이 = 시청률(%) · 10.16 방송분은 10.17 기준 확인 못 함")

# ================= AI 장면 + 꼬리표 (10/18 생성 7장, scenes/) =================
CSS_T2 = """.tag.t2 b{font-size:27px;letter-spacing:-.02em}.tag.t2 span{font-size:15px;text-wrap:balance}
.ok{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;color:#fff;font-size:16px;font-weight:900;margin-right:8px;vertical-align:3px}
.board{position:absolute;z-index:5;font-weight:900;text-align:center;letter-spacing:-.01em}"""
def bg(name): return f'<img src="scenes/{name}.png" style="position:absolute;left:0;top:0;width:1400px;height:800px;object-fit:cover">'
CHK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
XX = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
def t2(x, y, head, sub, color, rot=0, mark=None, w=None):
    m = "" if mark is None else f'<span class="ok" style="display:inline-grid;background:{"#3D62AE" if mark else "#C8463C"}">{CHK if mark else XX}</span>'
    ws = f"width:{w}px;" if w else ""
    return f'<div class="tag t2" style="left:{x}px;top:{y}px;{ws}transform:rotate({rot}deg)"><b style="color:{color}">{m}{head}</b><span>{sub}</span></div>'
def st(x, y, text, color="#D07A22"):
    return f'<div class="stamp" style="left:{x}px;top:{y}px;border-color:{color};color:{color}">{text}</div>'

# 02 엽서 다섯 장
P2 = ((150, "2024.3 맨체스터", "「아무 계획 없이」", "기차는 앱으로 미리 예약", True),
      (380, "2025.11 화담숲", "「번개로 가자고 해서」", "두 달 전 예약 · 대기 76,043번", True),
      (600, "2023.6 교토", "「즉흥적으로 들어간 집」", "왕복 항공권 2인 미리 결제", True),
      (820, "2023.11 후쿠오카", "「일정표도 안 짰어」", "숙소 두 곳 미리 예약", True),
      (1040, "2019.5 미국 주말", "「계획이랄 게 없었어」", "큰 예약 없음 · 차로 나선 주말", None))
b2 = "".join(f'<div class="tag" style="left:{x}px;top:{560 + (i % 2) * 14}px;width:212px;padding:10px 10px 10px 14px;transform:rotate({(-2, 1.5, -1, 2, -1.5)[i]}deg)">'
             f'<span style="margin:0;color:#8A7F6A;font-size:13.5px">{w}</span><b style="font-size:17px;color:#D07A22;margin-top:4px;white-space:nowrap;letter-spacing:-.04em">{q}</b>'
             f'<span style="font-size:13.5px;white-space:nowrap;letter-spacing:-.02em;color:{"#3D62AE" if ok else "#8A8272"};margin-top:6px">{"✓ " if ok else "– "}{p}</span></div>' for i, (x, w, q, p, ok) in enumerate(P2))
F["S_N2_five_impromptu_posts"] = frame(2, "「즉흥」이라 쓴 글", "즉흥이라 쓴 글 다섯 편, <em>넷</em>은 예약이 먼저",
    bg("N2_postcards") + b2 + st(960, 186, "즉흥이라 쓰고, 예약은 미리"),
    "각 글 본문 문장(2026.10.17 확인) · 화담숲 대기번호·예약 시점은 화담숲 예약 글 · 엽서는 AI 생성 장면(실제 사진 아님)", CSS_T2)

# 03 후쿠오카 수첩 셋
F["S_N3_fukuoka_two_lines"] = frame(3, "2023.11 후쿠오카", "셋이 간 후쿠오카, 내 메모엔 <em>두 줄</em>",
    bg("N3_notebooks") + t2(330, 610, "동행 둘의 일정표", "날마다 갈 곳이 빼곡", "#3D62AE", -2, w=250)
    + '<div class="tag" style="left:930px;top:470px;transform:rotate(2deg)"><b style="color:#D07A22">2줄</b><span>내 메모 · 비행기 왕복 · 숙소 두 곳<br>그날 어디 갈지는 0줄</span></div>'
    + st(60, 222, "「완전 무계획으로 갈 배짱은 없었다」"),
    "블로그 후쿠오카 11월 글 두 편 + 본인 확인(2026.10.17) · AI 생성 장면(실제 수첩 아님)", CSS_T2)

# 04 사전 · 마이크 · 벽의 쪽지 셋
CSS4 = CSS_T2 + """.nt{position:absolute;left:700px;width:668px;background:#FFFCF5;border-left:8px solid;padding:14px 20px;z-index:5;box-shadow:0 10px 22px rgba(30,25,15,.22)}
.nt .w{font-size:14.5px;font-weight:800;letter-spacing:.04em}.nt .t{font-size:20.5px;font-weight:800;line-height:1.45;margin-top:4px;text-wrap:balance}.nt .f{font-size:14px;font-weight:700;color:#6E6656;margin-top:4px}"""
Q4 = (("표준국어대사전 「즉흥」", "그 자리에서 바로 일어나는 감흥. 또는 그런 기분.", "", "#3D62AE", -1),
      ("MBC가 말한 「즉흥 여행」 · 9.4 입장문", "목적지와 항공권을 미리 정하지 않은 채 당일 여행지를 결정해 떠나는 방식", "", "#D07A22", .8),
      ("MBC가 덧붙인 문장 · 9.4 입장문", "모든 과정이 아무런 사전 준비 없이 진행된 것으로 받아들여질 수 있다는 점", "→ 「충분히 고려하지 못했습니다」", "#C8463C", -.6))
n4 = "".join(f'<div class="nt" style="top:{y}px;border-color:{c};transform:rotate({r}deg)"><div class="w" style="color:{c}">{w}</div><div class="t">「{t}」</div>' + (f'<div class="f">{f}</div>' if f else "") + '</div>'
             for (w, t, f, c, r), y in zip(Q4, (196, 332, 494)))
F["S_N4_three_meanings"] = frame(4, "「즉흥」의 뜻", "「즉흥」, 세 곳에서 <em>다르게</em> 쓰였다",
    bg("N4_dictionary") + n4 + t2(330, 236, "듣는 쪽", "한 번에 많은 사람이 듣는 방송<br>심의규정 제14조 「시청자를 혼동케 하여서는 아니 된다」", "#22335A", -2, w=330)
    + st(760, 668, "기준은 시청자", "#22335A"),
    "표준국어대사전, MBC 9.4 입장문(한겨레·더팩트 대조), 방송심의에 관한 규정 제14조 · 사전·마이크는 AI 생성 장면", CSS4)

# 06 책상 위 셋 + 빈 비닐
F["S_N5b_prepared_or_not"] = frame(6, "MBC 입장문이 말한 것", "미리 한 것 <em>셋</em>, 안 한 것 <em>하나</em>",
    bg("N5b_table") + t2(70, 300, "촬영 허가 공문", "7월 22일 · 공항에", "#3D62AE", -2, True)
    + t2(430, 234, "스태프 항공권", "미리 발권", "#3D62AE", 1.5, True)
    + t2(830, 118, "현지 촬영 협조", "미리 요청", "#3D62AE", -1, True)
    + t2(1100, 300, "운전 서류", "면허 공증 · 「뒤늦게 확인」", "#C8463C", 2, False)
    + st(560, 640, "준비했으면 즉흥이 아니고, 안 했으면 위험했다"),
    "MBC 입장문 8.25·9.4, 인천국제공항공사가 국회에 낸 자료(10.16 보도), 주카자흐스탄 대사관 공지 · 물건은 AI 생성 장면", CSS_T2)

# 08 비 오는 거실의 TV와 휴대폰
F["S_N6_tell_rules"] = frame(8, "알리는 규칙", "방송은 「알릴 수 <em>있다</em>」, 유튜브는 「<em>알려야</em> 한다」",
    bg("N6_tv_phone") + t2(160, 250, "방송 · 알릴 수 있다", "방송법 · 협찬고지 규칙<br>정해진 방식만 · 프로그램 끝 자막 1회", "#22335A", -1.5, w=420)
    + t2(700, 236, "유튜브 · 알려야 한다", "공정위 추천·보증 심사지침<br>매 건마다 · 제목이나 영상 안, 시작과 끝", "#D07A22", 2, w=400)
    + '<div class="string" style="left:900px;top:340px;width:70px;transform:rotate(80deg)"></div>'
    + st(250, 640, "촬영 협조가 협찬인지는 아직 결론 없음", "#22335A"),
    "방송법 제2조제22호·제74조, 협찬고지 규칙 제8조, 공정위 추천·보증 심사지침(2026.6.1 시행) · 거실은 AI 생성 장면", CSS_T2)

# 09 갈림길 이정표 — 파란 판 넷은 미리, 맨 나무 판 하나는 그날
CSS9 = CSS_T2 + ".board{color:#FFFCF5;font-size:27px;text-shadow:0 2px 4px rgba(20,40,80,.45)}"
boards = "".join(f'<div class="board" style="left:{x}px;top:{y}px;width:190px;transform:rotate({r}deg)">{t}</div>' for x, y, t, r in (
    (745, 112, "비행기", -1), (745, 196, "숙소", -1), (745, 280, "렌터카", -1), (745, 362, "투어·입장권", -1)))
boards += '<div class="board" style="left:982px;top:214px;width:210px;transform:rotate(-2deg);color:#8A3F0C;font-size:29px;text-shadow:0 1px 0 rgba(255,240,220,.6)">그날 정하기</div>'
F["S_N7_one_blank_line"] = frame(9, "할 일 하나", "다음 여행 메모엔 「그날 정하기」 <em>한 줄</em>",
    bg("N7_signpost") + boards
    + t2(54, 560, "4편", "내 여행 글에 남은 비슷한 문장<br>「계획에 없던 30분이 제일 선명해」", "#3D62AE", -2, w=360)
    + st(1010, 606, "다 채우지 않기로 했다"),
    "블로그 구마모토성·규슈 렌터카·후쿠오카 11월 코스·미서부 2년 뒤 글 본문(2026.10.17 확인) · 이정표는 AI 생성 장면(모식)", CSS9)

# 12 초원 길가의 렌터카
F["S_H3_driving_papers"] = frame(12, "한 걸음 더 · 운전 서류", "카자흐스탄 운전, 국제면허증만으론 <em>안 된다</em>",
    bg("H3_car") + t2(36, 300, "한국 국제운전면허증", "제네바 협약 방식 · 카자흐스탄은 비엔나 협약(1994 가입)<br>→ 카자흐스탄에선 인정 안 됨", "#C8463C", -1.5, False, w=430)
    + t2(36, 470, "필요한 서류 2가지", "한국 면허 원본 + 러시아어 공증 번역본", "#2F8F5B", 1, True, w=430)
    + t2(1110, 470, "반나절", "한국 공관에서<br>공증 받을 때", "#3D62AE", 2)
    + st(700, 180, "국제운전면허증만으로는 운전 불가", "#C8463C"),
    "주카자흐스탄 대한민국 대사관 공지(8.20·8.25), 외교부 해외안전여행 운전면허 상호인정, 유엔 조약 현황 · 차는 AI 생성 장면", CSS_T2)

if __name__ == "__main__":
    render(F, sys.argv[1:] or None)
