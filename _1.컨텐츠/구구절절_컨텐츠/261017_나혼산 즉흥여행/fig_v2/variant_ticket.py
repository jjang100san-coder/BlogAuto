# -*- coding: utf-8 -*-
"""마스터 5-8 시안 — 주제(여행)의 물건에서 꼴을 가져온 「탑승권」 양식(10/18).
① 형식: 탑승권(본권 + 떼는 쪽) ② 배경: 베이지 종이 ③ 모양: 남색 머리띠·절취선·반달 홈·바코드
④ 강조: 주황 고무도장 + 아주 큰 숫자 ⑤ 정체성: 「BOARDING · 01 / 13」"""
import pathlib
src = open("render.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:')
ns = {"__file__": str(pathlib.Path("render.py").resolve())}
exec(src, ns)
FIG, cubes, ic, CSS = ns["FIG"], ns["cubes"], ns["ic"], ns["CSS"]

T_CSS = CSS + """
body{background:#EDE5D6;background-image:radial-gradient(rgba(90,70,40,.06) 1px,transparent 1.2px);background-size:6px 6px}
.ticket{position:absolute;left:36px;top:34px;width:1328px;height:732px;background:#FFFCF5;border-radius:20px;
  box-shadow:0 2px 0 rgba(60,45,20,.06),0 22px 50px rgba(60,45,20,.16);overflow:hidden}
.band{position:absolute;left:0;top:0;right:0;height:158px;background:#22335A;color:#fff;padding:26px 40px}
.band .k{display:flex;gap:14px;align-items:center;font-size:15px;font-weight:800;letter-spacing:.18em;color:#AFC0E6}
.band .k b{background:#D07A22;color:#fff;letter-spacing:.06em;border-radius:6px;padding:3px 9px;font-size:14px}
.band h1{color:#fff;font-size:50px;margin-top:10px}
.band h1 em{color:#FFC27A;background:none}
.perf{position:absolute;left:1000px;top:158px;bottom:0;border-left:3px dashed #D9CFBC}
.notch{position:absolute;width:44px;height:44px;border-radius:50%;background:#EDE5D6;left:979px}
.main{position:absolute;left:0;top:158px;width:1000px;bottom:0;padding:26px 36px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
.cat .hd{display:flex;align-items:center;gap:10px}
.cat .hd img{width:86px;height:86px;object-fit:contain}
.cat .nm{font-size:23px;font-weight:900}
.cat .cnt{font-size:15px;font-weight:700;color:#6B7080;margin-top:2px}
.cat .blk{margin-top:6px}
.stub{position:absolute;left:1003px;right:0;top:158px;bottom:0;padding:26px 30px}
.stub .lab{font-size:13px;font-weight:800;letter-spacing:.16em;color:#9A917F}
.stub .row{margin-top:18px}
.stub .row .n{font-size:84px;font-weight:900;line-height:.95;letter-spacing:-.04em}
.stub .row .n small{font-size:36px}
.stub .row .t{font-size:16px;font-weight:700;color:#4A5163;margin-top:4px}
.bar{position:absolute;left:30px;right:30px;bottom:56px;height:54px;background:repeating-linear-gradient(90deg,#22335A 0 3px,transparent 3px 6px,#22335A 6px 7px,transparent 7px 11px,#22335A 11px 15px,transparent 15px 17px)}
.src{position:absolute;left:36px;bottom:20px;font-size:13.5px;color:#9A917F}
.stub .src2{position:absolute;left:30px;bottom:22px;font-size:13px;font-weight:800;letter-spacing:.14em;color:#9A917F}
.stamp{position:absolute;left:520px;top:575px;transform:rotate(-7deg);border:4px solid #D07A22;color:#D07A22;border-radius:12px;padding:10px 20px;
  font-size:25px;font-weight:900;background:rgba(255,252,245,.85);box-shadow:inset 0 0 0 2px rgba(208,122,34,.25)}
.lg{position:absolute;right:360px;top:180px;display:flex;gap:14px;font-size:15px;font-weight:700;color:#4A5163}
.lg i{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-2px}
"""
def cat(icon, name, cnt, a, b):
    return f'<div class="cat"><div class="hd"><img src="icons/{icon}_t.png"><div><div class="nm">{name}</div><div class="cnt">{cnt}</div></div></div><div class="blk">{cubes(a, b, cols=10, s=25)}</div></div>'
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{T_CSS}</style></head><body>
<div class="ticket">
 <div class="band"><div class="k"><b>구구절절</b>BOARDING · 내 여행 글 68편 · 01 / 13</div><h1>큰 예약은 <em>96%</em>가 미리였다</h1></div>
 <div class="main">{cat("suitcase", "항공·숙소·렌터카·투어", "미리 48 · 현장 2", 48, 2)}{cat("map", "동선·식당·현지 교통", "미리 29 · 현장 44", 29, 44)}</div>
 <div class="perf"></div><div class="notch" style="top:136px"></div><div class="notch" style="bottom:-22px"></div>
 <div class="stub"><div class="lab">미리 정한 비율</div>
   <div class="row"><div class="n" style="color:#3D62AE">96<small>%</small></div><div class="t">항공·숙소·렌터카·투어</div></div>
   <div class="row"><div class="n" style="color:#D07A22">40<small>%</small></div><div class="t">동선·식당·현지 교통</div></div>
   <div class="bar"></div><div class="src2">걷고읽고떠나고</div></div>
 <div class="stamp">비행기·숙소는 미리, 즉흥은 그날</div>
 <div class="src">근거 · 내 블로그 여행 후기 68편 직접 셈(2026.10.17) · 블록 하나 = 결정 하나 · 알 수 없음 36 제외</div>
</div><div class="take" style="display:none"></div></body></html>"""
FIG["ticket_N1"] = html
ns["render"](["ticket_N1"])
