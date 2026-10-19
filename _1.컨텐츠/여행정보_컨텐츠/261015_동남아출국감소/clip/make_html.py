# -*- coding: utf-8 -*-
# 캄보디아 사태 뒤 동남아 클립 — 마스터 5-8 양식 움직이는 인포그래픽(clipkit/html_anim.py)
# 장면: three 검색·마음·발길 · ch1/ch2/ch3 장 카드 · search 걱정 검색 100 vs 3 안팎 · fold 다섯 명 중 넷 vs 한 명
#       steps 캄보디아 넉 달 · route 출국 전체 -8.2% vs +5.2% · recap 세 층 정리(요약 장) · alert 지역별 여행경보
# 숫자는 발행본(224443981185) 그대로. 어느 나라 편도 아님 — 숫자끼리 대 보기
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from html_anim import scene, render

BASE = os.path.dirname(os.path.abspath(__file__))
RED, BLUE = '#C8463C', '#3D62AE'


def chapter(name, n, title, icon):
    body = f'''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class="nb big" id="nb">{n}</div><div class="tt big" id="tt">{title}</div><img class="icon3d" id="ic" src="icons/{icon}_t.png" style="height:340px;margin-top:50px"></div>'''
    css = '''.nb{width:150px;height:150px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:92px}
.tt{font-size:116px;margin-top:40px;text-align:center}'''
    js = '''function F(t){$('#nb').style.transform=`scale(${K(P(t,.05,.4))})`;
$('#tt').style.opacity=P(t,.3,.6);$('#tt').style.transform=`translateY(${(1-P(t,.3,.7))*40}px)`;
const v=P(t,.5,1.1);$('#ic').style.transform=`translateY(${(1-v)*300+Math.sin(t*3)*8}px)`;$('#ic').style.opacity=v}'''
    return scene(name, 4.0, body, js, css)


L3 = [('mag', '검색', '걱정할 때 찾는 말'), ('heart', '마음', '「가 보고 싶다」'), ('foot', '발길', '실제로 간 사람')]
th_body = '<div class="stage" style="display:flex;gap:30px;justify-content:center;align-items:center">' + \
    ''.join(f'<div class="card tc" id="c{i}"><img class="icon3d" src="icons/{a}_t.png" style="height:220px"><div class="k">{b}</div><div class="d">{c}</div></div>' for i, (a, b, c) in enumerate(L3)) + '</div>'
th_css = '.tc{width:370px;padding:44px 24px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:16px}.k{font-size:64px;font-weight:900}.d{font-size:34px;font-weight:700;color:var(--ink2)}'
th_js = '''function F(t){for(let i=0;i<3;i++){const v=K(P(t,.2+i*.5,.6+i*.5));$('#c'+i).style.transform=`scale(${v})`;$('#c'+i).style.opacity=Math.min(1,v*1.3)}}'''

SR = [('캄보디아 납치·감금', 100), ('태국 치안', 2.9), ('베트남 치안', 2.0), ('동남아 위험', 2.0), ('필리핀 치안', 0.9)]
se_body = '<div class="stage"><div class="card ab" style="inset:0;padding:50px 50px">' + \
    '<div class="hh">2025년 10월 걱정 검색 <span class="mut">가장 많이 찾은 달 = 100</span></div>' + \
    ''.join(f'<div class="rw"><div class="nm">{n}</div><div class="bar" id="b{i}" style="background:{RED if i == 0 else "#D9A441"}"></div><div class="vl" id="v{i}"></div></div>' for i, (n, v) in enumerate(SR)) + \
    '<div class="pill" id="nt" style="background:var(--pre-l);color:var(--pre);font-size:38px;margin-top:20px">이웃 나라 검색은 11월에 제자리</div></div></div>'
se_css = '''.hh{font-size:44px;font-weight:900;margin-bottom:30px}.hh .mut{font-size:30px}.rw{display:flex;align-items:center;gap:20px;height:104px}
.nm{width:330px;font-size:38px;font-weight:800}.bar{height:58px;border-radius:12px;width:0}.vl{font-size:44px;font-weight:900}'''
se_js = 'const V=' + str([v for _, v in SR]) + ''';
function F(t){V.forEach((v,i)=>{const u=P(t,.2+i*.3,1.0+i*.3);$('#b'+i).style.width=Math.max(v>0?8:0,700*v/100*u)+'px';$('#v'+i).textContent=u>0?(v*u).toFixed(v>=10?0:1):''});
$('#nt').style.opacity=P(t,2.8,3.2)}'''

person = '<svg viewBox="0 0 60 80" class="ps"><circle cx="30" cy="18" r="14"/><path d="M8 78 Q8 40 30 40 Q52 40 52 78 Z"/></svg>'
fo_body = '<div class="stage" style="display:flex;flex-direction:column;gap:22px;justify-content:center">' + \
    ''.join(f'''<div class="card fr" id="f{i}"><div class="hd"><b>{a}</b><span class="mut">{b}</span></div><div class="pp">{"".join(f'<div class="pc" id="p{i}{j}">{person}</div>' for j in range(5))}</div>
<div class="big pv" id="pv{i}" style="color:{c}">{d}</div></div>''' for i, (a, b, c, d) in enumerate([('2019 노재팬 · 일본', '25% → 5%', BLUE, '80% 접음'), ('2025 캄보디아 사태 · 동남아', '27.1% → 20.5%', RED, '24% 접음')])) + \
    '<div class="mut" style="font-size:28px;font-weight:700;text-align:center">같은 설문 · 사건 전 달 → 가장 낮은 달</div></div>'
fo_css = '''.fr{padding:24px 44px}.hd{display:flex;justify-content:space-between;align-items:baseline}.hd b{font-size:46px;font-weight:900}.hd .mut{font-size:32px;font-weight:800}
.pp{display:flex;gap:30px;margin:14px 0 4px}.pc{width:100px;height:130px}.ps{width:100px;height:130px;fill:#3D62AE;transition:none}.pc.off .ps{fill:#E2DDD3}
.pv{font-size:62px}'''
fo_js = '''const N=[4,1];function F(t){for(let i=0;i<2;i++){$('#f'+i).style.opacity=P(t,.1+i*.4,.4+i*.4);
for(let j=0;j<5;j++){const e=$('#p'+i+j);const off=j>=5-N[i]&&t>1.2+i*1.2+(4-j)*.25;e.classList.toggle('off',off);e.style.transform=off?'scale(.92) translateY(10px)':'scale(1)'}
$('#pv'+i).style.opacity=P(t,1.8+i*1.2,2.1+i*1.2)}}'''

KH = [('11월', -56.5), ('12월', -61.9), ('1월', -70.0), ('2월', -70.5)]
st_body = '<div class="stage"><div class="card ab" style="inset:0;padding:50px">' + \
    '<div class="hh">캄보디아 한국인 입국자 <span class="mut">1년 전 같은 달 대비</span></div><div class="zero"></div>' + \
    ''.join(f'<div class="col" style="left:{110 + i * 240}px"><div class="bar" id="b{i}"></div><div class="vl" id="v{i}"></div><div class="mo">{m}</div></div>' for i, (m, v) in enumerate(KH)) + \
    '<div class="pill ab" id="nt" style="right:50px;bottom:40px;background:var(--ok-l);color:var(--ok);font-size:34px">이웃 태국·베트남·필리핀은 이만큼 안 빠졌다</div></div></div>'
st_css = '''.hh{font-size:44px;font-weight:900}.hh .mut{font-size:30px}.zero{position:absolute;left:50px;right:50px;top:200px;height:4px;background:#D8D1C4}
.col{position:absolute;top:204px;width:170px;text-align:center}.bar{margin:0 auto;width:130px;background:#C8463C;border-radius:0 0 16px 16px}
.vl{font-size:46px;font-weight:900;color:var(--red);margin-top:12px}.mo{position:absolute;top:-60px;left:0;right:0;font-size:36px;font-weight:800;color:var(--muted)}'''
st_js = 'const V=' + str([v for _, v in KH]) + ''';
function F(t){V.forEach((v,i)=>{const u=P(t,.2+i*.4,1.0+i*.4);$('#b'+i).style.height=(Math.abs(v)*6*u)+'px';$('#v'+i).textContent=u>0?'−'+(Math.abs(v)*u).toFixed(1)+'%':''});
$('#nt').style.opacity=P(t,2.6,3.0)}'''

ro_body = '''<div class="stage" style="display:flex;gap:40px;justify-content:center;align-items:center">
<div class="card rc" id="a"><div class="yr">2019 노재팬</div><div class="ic">🚫</div><div class="k">여행을 접었다</div><div class="mut sm">해외 출국 전체</div><div class="big v" style="color:#3D62AE" id="va">0%</div></div>
<div class="card rc" id="b"><div class="yr">2025 캄보디아</div><div class="ic">🧭</div><div class="k">행선지를 바꿨다</div><div class="mut sm">해외 출국 전체</div><div class="big v" style="color:#C8463C" id="vb">0%</div></div></div>'''
ro_css = '.rc{width:520px;padding:44px 30px;text-align:center}.yr{font-size:40px;font-weight:900;color:var(--ink2)}.ic{font-size:110px;margin:16px 0}.k{font-size:54px;font-weight:900}.sm{font-size:32px;font-weight:700;margin-top:20px}.v{font-size:110px;margin-top:10px}'
ro_js = '''function F(t){$('#a').style.transform=`scale(${K(P(t,.1,.5))})`;$('#b').style.transform=`scale(${K(P(t,.7,1.1))})`;
const u=P(t,1.2,2.4);$('#va').textContent=u>0?'−'+(8.2*u).toFixed(1)+'%':'';$('#vb').textContent=u>0?'+'+(5.2*u).toFixed(1)+'%':''}'''

RC = [('mag', '검색', '이웃 나라까지 한 달'), ('heart', '마음', '동남아 전체 −24%'), ('foot', '발길', '캄보디아만')]
rc_body = '<div class="stage" style="display:flex;flex-direction:column;gap:24px;justify-content:center">' + \
    ''.join(f'<div class="card rr" id="r{i}"><img class="icon3d" src="icons/{a}_t.png" style="height:130px"><div class="k">{b}</div><div class="v">{c}</div></div>' for i, (a, b, c) in enumerate(RC)) + '</div>'
rc_css = '.rr{display:grid;grid-template-columns:170px 200px 1fr;align-items:center;padding:24px 40px}.rr .k{font-size:56px;font-weight:900}.rr .v{font-size:54px;font-weight:900;color:var(--red)}'
rc_js = '''function F(t){for(let i=0;i<3;i++){const v=P(t,.2+i*.6,.6+i*.6);$('#r'+i).style.opacity=v;$('#r'+i).style.transform=`translateX(${(1-v)*-120}px)`}}'''

AL = [('#C8463C', '3단계', '태국 국경 50km 안 · 시하누크빌시 · 보코산 · 바벳 · 포이펫'), ('#D9A441', '2단계', '시하누크빌주'), ('#3D62AE', '1단계', '그 밖 전역')]
al_body = '<div class="stage" style="display:flex;flex-direction:column;gap:26px;justify-content:center">' + \
    '<div class="hh">캄보디아 여행경보 <span class="mut">2026년 7월 9일 조정 기준</span></div>' + \
    ''.join(f'<div class="card ar" id="a{i}"><div class="lv" style="background:{c}">{l}</div><div class="tx">{x}</div></div>' for i, (c, l, x) in enumerate(AL)) + \
    '<div class="pill" id="nt" style="background:var(--ink);color:#fff;font-size:38px;align-self:center">나라가 아니라 지역에 걸린다</div></div>'
al_css = '.hh{font-size:46px;font-weight:900}.hh .mut{font-size:30px}.ar{display:flex;align-items:center;gap:28px;padding:26px 30px}.lv{flex:none;color:#fff;font-size:44px;font-weight:900;border-radius:16px;padding:16px 24px}.tx{font-size:40px;font-weight:800;line-height:1.35}'
al_js = '''function F(t){for(let i=0;i<3;i++){const v=P(t,.2+i*.5,.6+i*.5);$('#a'+i).style.opacity=v;$('#a'+i).style.transform=`translateY(${(1-v)*50}px)`}
$('#nt').style.transform=`scale(${K(P(t,2.0,2.4))})`}'''

SCENES = [
    scene('three', 5.0, th_body, th_js, th_css),
    chapter('ch1', '1', '검색', 'mag'),
    scene('search', 6.0, se_body, se_js, se_css),
    chapter('ch2', '2', '마음', 'heart'),
    scene('fold', 6.5, fo_body, fo_js, fo_css),
    chapter('ch3', '3', '발길', 'foot'),
    scene('steps', 6.0, st_body, st_js, st_css),
    scene('route', 5.5, ro_body, ro_js, ro_css),
    scene('recap', 5.5, rc_body, rc_js, rc_css),
    scene('alert', 5.5, al_body, al_js, al_css),
]

if __name__ == '__main__':
    render(SCENES, BASE, sys.argv[1:] or None)
