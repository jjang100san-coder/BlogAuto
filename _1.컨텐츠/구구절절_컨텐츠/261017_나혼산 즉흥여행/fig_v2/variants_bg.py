# -*- coding: utf-8 -*-
"""「텅 빈 느낌」 진단용 변형(10/18) — 같은 N1 을 배경·카드 색 구성만 바꿔 셋 뽑는다."""
import pathlib
src = open("render.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:')
ns = {"__file__": str(pathlib.Path("render.py").resolve())}
exec(src, ns)
FIG, page, cubes, ic = ns["FIG"], ns["page"], ns["cubes"], ns["ic"]

def pan(icon, name, cnt, a, b, pc, col, cls, s=31):
    return (f'<div class="pan card {cls}"><div class="hd"><img class="icon3d" src="icons/{icon}_t.png"><div><div class="nm">{name}</div><div class="cnt">{cnt}</div></div></div>'
            f'<div class="blk">{cubes(a, b, cols=10, s=s)}</div>'
            f'<div class="big"><b style="color:{col}">{pc}<small>%</small></b><span>미리 정한 비율</span></div></div>')
body = ('<div class="lg"><span><i style="background:var(--pre)"></i>미리</span><span><i style="background:var(--ons)"></i>현장</span><span style="color:var(--ink2)">블록 하나 = 결정 하나</span></div>'
        + '<div class="two">' + pan("suitcase", "항공·숙소·렌터카·투어", "미리 48 · 현장 2", 48, 2, 96, "var(--pre)", "tA")
        + pan("map", "동선·식당·현지 교통", "미리 29 · 현장 44", 29, 44, 40, "var(--ons)", "tB") + '</div>')
take = "비행기·숙소는 <b>미리</b>, 즉흥은 <b>동선과 식당</b>에서"
src_ = "내 블로그 여행 후기 68편 직접 셈(2026.10.17) · 언제 정했는지 알 수 없는 36가지 제외"
BASE = ns["N1v3_CSS"] + """
:root{--muted:#6B7080}
.pan .hd img{width:104px;height:104px}
"""
# A 색면 카드 + 배경 번짐
A = BASE + """
body{background:radial-gradient(900px 520px at 92% -10%,rgba(61,98,174,.16),transparent 60%),radial-gradient(800px 480px at -5% 105%,rgba(208,122,34,.16),transparent 60%),#F6F1E8}
.tA{background:linear-gradient(165deg,#E9EEF9 0%,#FFFFFF 58%)}
.tB{background:linear-gradient(165deg,#FBEBDA 0%,#FFFFFF 58%)}
.card{border:0;box-shadow:0 2px 0 rgba(30,35,48,.04),0 18px 40px rgba(30,35,48,.10)}
"""
# B 진한 머리띠 + 색면 카드
B = A + """
body:before{content:"";position:absolute;left:0;right:0;top:0;height:215px;background:linear-gradient(120deg,#22304F,#3D62AE)}
.kicker{color:#C9D3EA}.kicker .dot{background:#FFB866}
h1{color:#fff}h1 em{color:#FFD08A;background:none}
.lg{color:#E6EBF5}.lg span[style]{color:#C9D3EA!important}
.page{z-index:1}
"""
# C 점 무늬 + 색면 카드 + 오른쪽 위 아이콘
C = A + """
body{background-image:radial-gradient(rgba(30,35,48,.09) 1.2px,transparent 1.3px),radial-gradient(900px 520px at 92% -10%,rgba(61,98,174,.14),transparent 60%),radial-gradient(800px 480px at -5% 105%,rgba(208,122,34,.14),transparent 60%);background-size:22px 22px,auto,auto;background-color:#F6F1E8}
"""
for name, css in (("bgA_tint", A), ("bgB_band", B), ("bgC_dots", C)):
    FIG[name] = page("구구절절 · 내 여행 글 68편", "큰 예약은 <em>96%</em>가 미리였다", "", body, take, src_, css)
ns["render"](["bgA_tint", "bgB_band", "bgC_dots"])
