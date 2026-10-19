# -*- coding: utf-8 -*-
# 시라카와고 1월 날씨 클립 — 마스터 5-8 양식 움직이는 인포그래픽(HTML+Playwright, clipkit/html_anim.py)
# 장면: gauge 같은 1월 14일 2020 3cm vs 2021 182cm(눈이 차오름) · years 11년 막대 · ch1 · fresh 그날 새 눈 10cm+ 4번
#       temp 온도계 · lightup 2027년 1월 달력(라이트업 4일, 내가 가는 14일) · pack 짐 세 칸(요약 장)
# 숫자는 발행본(224439622339) 그대로 — 일본 기상청 시라카와 관측소(하토가야) 일별값. 합장촌 마을 안과 같다고 쓰지 않음
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from html_anim import scene, render, ic

BASE = os.path.dirname(os.path.abspath(__file__))
SNOW = '#EAF2FB'


def chapter(name, n, title, icon):
    body = f'''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class="nb big" id="nb">{n}</div><div class="tt big" id="tt">{title}</div><img class="icon3d" id="ic" src="icons/{icon}_t.png" style="height:340px;margin-top:50px"></div>'''
    css = '''.nb{width:150px;height:150px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:92px}
.tt{font-size:112px;margin-top:40px;text-align:center}'''
    js = '''function F(t){$('#nb').style.transform=`scale(${K(P(t,.05,.4))})`;
$('#tt').style.opacity=P(t,.3,.6);$('#tt').style.transform=`translateY(${(1-P(t,.3,.7))*40}px)`;
const v=P(t,.5,1.1);$('#ic').style.transform=`translateY(${(1-v)*300+Math.sin(t*3)*8}px) rotate(${Math.sin(t*2)*6}deg)`;$('#ic').style.opacity=v}'''
    return scene(name, 4.0, body, js, css)


# 눈송이(배경에 떨어지는 점) — 장면 몇 곳에 깔기
FLAKES = ''.join(f'<div class="fk ab" id="k{i}"></div>' for i in range(26))
FLAKE_CSS = '.fk{width:14px;height:14px;border-radius:50%;background:#fff;box-shadow:0 0 6px rgba(120,150,200,.5)}'
FLAKE_JS = '''function flakes(t,W,H){for(let i=0;i<26;i++){const e=$('#k'+i);const x=(i*97%W)+Math.sin(t*1.3+i)*20,y=((t*90+i*61)%H);e.style.left=x+'px';e.style.top=y+'px'}}'''

# ---------- gauge: 같은 1월 14일, 2020년 3cm vs 2021년 182cm
G = [('2020년', 3), ('2021년', 182)]
g_body = '<div class="stage" style="display:flex;gap:50px;justify-content:center;align-items:stretch">' + \
    ''.join(f'''<div class="card gc" id="g{i}"><div class="yr">{y}</div><div class="win" id="w{i}"><img class="icon3d hs" src="icons/gassho_t.png">
<div class="snow ab" id="s{i}"></div><div class="rl ab"></div></div><div class="cm big" id="c{i}">0cm</div></div>''' for i, (y, v) in enumerate(G)) + '</div>' + \
    '<div class="ab" style="left:0;right:0;top:250px;height:825px;pointer-events:none;overflow:hidden">' + FLAKES + '</div>'
g_css = FLAKE_CSS + '''.gc{width:540px;padding:30px;display:flex;flex-direction:column}.yr{font-size:56px;font-weight:900;text-align:center;margin-bottom:16px}
.win{position:relative;flex:1;border-radius:22px;background:linear-gradient(#9FB8DB,#D3E0F0);overflow:hidden}
.hs{position:absolute;left:50%;bottom:10px;height:300px;transform:translateX(-50%)}
.snow{left:0;right:0;bottom:0;background:linear-gradient(#FFFFFF,#F1F5FB);border-radius:26px 26px 0 0;box-shadow:0 -8px 22px rgba(40,70,120,.28)}
.rl{right:16px;top:20px;bottom:0;width:16px;background:repeating-linear-gradient(#5B6276 0 3px,transparent 3px 30px);opacity:.5}
.cm{text-align:center;font-size:100px;color:var(--pre);margin-top:18px}'''
g_js = FLAKE_JS + '''const V=[3,182],MX=220;
function F(t){flakes(t,1350,825);for(let i=0;i<2;i++){const v=K(P(t,.05+i*.25,.4+i*.25));$('#g'+i).style.transform=`scale(${v})`;
const u=P(t,.6,3.2),H=$('#w'+i).clientHeight;const h=H*V[i]/MX*u;$('#s'+i).style.height=Math.max(2,h)+'px';$('#c'+i).textContent=Math.round(V[i]*u)+'cm'}}'''

# ---------- years: 11년 막대(1월 14일 쌓인 눈)
YV = [(2016, 39), (2017, 103), (2018, 156), (2019, 28), (2020, 3), (2021, 182), (2022, 177), (2023, 37), (2024, 54), (2025, 161), (2026, 63)]
y_body = '<div class="stage"><div class="card ab" style="inset:0">' + '<div class="hl ab" id="hl"><span>100cm</span></div>' + \
    ''.join(f'<div class="cl ab" style="left:{60 + i * 100}px"><div class="vv" id="v{i}"></div><div class="bb" id="b{i}"></div><div class="yy">{"%02d" % (y % 100)}</div></div>' for i, (y, v) in enumerate(YV)) + \
    '<div class="ab big" id="cn" style="right:50px;top:40px;font-size:60px;color:var(--pre)">100cm 넘은 해 5번</div>' + \
    '<div class="ab mut" style="left:40px;bottom:22px;font-size:28px;font-weight:700">1월 14일 쌓인 눈 · 일본 기상청 시라카와 관측소 · 2016~2026</div></div></div>'
y_css = '''.cl{bottom:110px;width:80px;height:640px;display:flex;flex-direction:column;justify-content:flex-end;align-items:center}
.bb{width:64px;border-radius:14px 14px 0 0;background:linear-gradient(#FFFFFF,#BFD2EC);border:3px solid #9DB5DA;border-bottom:none}.vv{font-size:30px;font-weight:900;color:var(--ink2);margin-bottom:6px}
.yy{position:absolute;bottom:-44px;font-size:30px;font-weight:800;color:var(--muted)}.hl{left:40px;right:40px;bottom:%dpx;border-top:5px dashed var(--ons)}
.hl span{position:absolute;left:0;top:-48px;color:var(--ons);font-size:34px;font-weight:900}''' % (110 + 100 * 2.6)
y_js = 'const V=' + str([v for _, v in YV]) + ''';
function F(t){V.forEach((v,i)=>{const u=P(t,.2+i*.18,.9+i*.18);const b=$('#b'+i);b.style.height=(v*2.6*u)+'px';$('#v'+i).textContent=u>.05?Math.round(v*u):'';
if(v>=100&&u>.97){b.style.background='linear-gradient(#FFFFFF,#7FA0D6)';b.style.borderColor='#3D62AE'}});
$('#hl').style.opacity=P(t,.1,.5);$('#cn').style.opacity=P(t,2.8,3.2)}'''

# ---------- fresh: 그날 새 눈 10cm 넘게 온 해
FR = [(2016, 33), (2017, 22), (2018, 3), (2019, 1), (2020, 1), (2021, 0), (2022, 14), (2023, 0), (2024, 0), (2025, 4), (2026, 14)]
f_body = '<div class="stage"><div class="card ab" style="inset:0;padding:40px">' + \
    '<div class="grid">' + ''.join(f'<div class="tl" id="t{i}"><div class="y">{y}</div><img class="icon3d fl" src="icons/snowflake_t.png"><div class="v">{(str(v) + "cm") if v else "-"}</div></div>' for i, (y, v) in enumerate(FR)) + '</div>' + \
    '<div class="ab big" id="cn" style="right:60px;bottom:60px;font-size:84px;color:var(--pre)">11년 중 4번</div></div></div>'
f_css = '''.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:20px}.tl{background:#F6F2EA;border-radius:22px;height:220px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}
.tl .y{font-size:32px;font-weight:900;color:var(--ink2)}.tl .fl{height:80px;opacity:.18;filter:grayscale(1)}.tl .v{font-size:36px;font-weight:900;color:var(--muted)}
.tl.on{background:var(--pre-l);box-shadow:inset 0 0 0 5px var(--pre)}.tl.on .fl{opacity:1;filter:none}.tl.on .v{color:var(--pre)}'''
f_js = 'const V=' + str([v for _, v in FR]) + ''';
function F(t){V.forEach((v,i)=>{const e=$('#t'+i);const a=P(t,.1+i*.06,.4+i*.06);e.style.opacity=a;
const on=v>=10&&t>1.4+i*.12;e.classList.toggle('on',on);e.querySelector('.fl').style.transform=on?`scale(${1+.15*Math.sin(t*4+i)})`:'scale(1)'});
$('#cn').style.opacity=P(t,3.0,3.4)}'''

# ---------- temp: 온도계
t_body = '''<div class="stage" style="display:flex;align-items:center;justify-content:center;gap:70px">
<img class="icon3d" id="th" src="icons/thermo_t.png" style="height:520px">
<div style="display:flex;flex-direction:column;gap:34px">
<div class="card tc" id="a"><div class="lb">낮 최고 평균</div><div class="big vv" id="va" style="color:#D07A22">1.0~5.6도</div></div>
<div class="card tc" id="b"><div class="lb">아침 최저 평균</div><div class="big vv" id="vb" style="color:#3D62AE">−5.5~−1.0도</div></div>
<div class="pill" id="c" style="background:var(--ink);color:#fff;font-size:40px;align-self:flex-start">낮에도 5도 아래</div></div></div>'''
t_css = '.tc{padding:34px 44px;width:640px}.lb{font-size:38px;font-weight:800;color:var(--ink2)}.vv{font-size:84px;margin-top:10px}'
t_js = '''function F(t){$('#th').style.transform=`translateY(${(1-P(t,.1,.6))*200}px) rotate(${Math.sin(t*2)*3}deg)`;
$('#a').style.opacity=P(t,.5,.9);$('#a').style.transform=`translateX(${(1-P(t,.5,1.0))*120}px)`;
$('#b').style.opacity=P(t,1.3,1.7);$('#b').style.transform=`translateX(${(1-P(t,1.3,1.8))*120}px)`;$('#c').style.transform=`scale(${K(P(t,2.4,2.8))})`}'''

# ---------- lightup: 2027년 1월 달력
# 2027-01-01 은 금요일 → 일요일 시작 달력에서 첫 칸 5개 비움
LU, ME = {11, 17, 24, 31}, 14
cells = ''.join('<div class="dd e"></div>' for _ in range(5)) + ''.join(f'<div class="dd" id="d{d}"><span>{d}</span></div>' for d in range(1, 32))
l_body = f'''<div class="stage"><div class="card ab" style="inset:0;padding:34px 50px">
<div class="hd"><span class="mo">2027년 1월</span><span class="lg"><i class="sw lu"></i>라이트업 <i class="sw me"></i>내가 가는 날</span></div>
<div class="wk">{''.join(f'<span>{w}</span>' for w in '일월화수목금토')}</div><div class="cal">{cells}</div></div></div>'''
l_css = '''.hd{display:flex;justify-content:space-between;align-items:center}.mo{font-size:56px;font-weight:900}.lg{font-size:30px;font-weight:800;color:var(--ink2);display:flex;align-items:center;gap:10px}
.sw{display:inline-block;width:30px;height:30px;border-radius:8px}.sw.lu{background:#F4C24E}.sw.me{background:var(--pre);margin-left:18px}
.wk{display:grid;grid-template-columns:repeat(7,1fr);margin-top:20px;font-size:30px;font-weight:800;color:var(--muted);text-align:center}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;margin-top:10px}.dd{height:96px;border-radius:16px;background:#F6F2EA;display:grid;place-items:center;font-size:40px;font-weight:800;color:var(--ink2)}
.dd.e{background:transparent}.dd.lu{background:#F4C24E;color:#3A2A00;box-shadow:0 0 0 0 rgba(244,194,78,.5)}.dd.me{background:var(--pre);color:#fff}'''
l_js = 'const LU=' + str(sorted(LU)) + ''';
function F(t){LU.forEach((d,i)=>{const e=$('#d'+d);const on=t>.5+i*.35;e.classList.toggle('lu',on);e.style.transform=on?`scale(${1+.08*K(P(t,.5+i*.35,.8+i*.35))-.08*P(t,.8+i*.35,1.0+i*.35)})`:''});
const m=$('#d14');const on=t>2.4;m.classList.toggle('me',on);m.style.transform=on?`scale(${K(P(t,2.4,2.8))*1.12})`:''}'''

# ---------- pack: 짐 세 칸(요약 장)
PK = [('발', '쌓인 눈 3~182cm', '방수 신발'), ('몸', '낮에도 5도 아래', '패딩·장갑·핫팩'), ('시간', '12:57 → 16:15', '몸 녹일 곳')]
p_body = '<div class="stage" style="display:flex;gap:28px;align-items:stretch;justify-content:center">' + \
    ''.join(f'<div class="card pc" id="p{i}"><div class="k">{a}</div><div class="w">{b}</div><div class="ar">↓</div><div class="c">{c}</div></div>' for i, (a, b, c) in enumerate(PK)) + '</div>' + \
    '<img class="icon3d ab" id="bt" src="icons/boots_t.png" style="height:220px;left:565px;top:250px">'
p_css = '''.pc{width:380px;padding:40px 26px;display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:240px}.k{font-size:70px;font-weight:900;color:var(--ons)}
.w{font-size:38px;font-weight:800;color:var(--ink2);margin-top:18px;line-height:1.35;min-height:110px}.ar{font-size:60px;color:var(--muted);font-weight:900}
.c{font-size:40px;font-weight:900;margin-top:10px;background:var(--pre-l);color:var(--pre);border-radius:18px;padding:16px 18px;line-height:1.3}'''
p_js = '''function F(t){for(let i=0;i<3;i++){const v=K(P(t,.2+i*.5,.6+i*.5));$('#p'+i).style.transform=`scale(${v})`;$('#p'+i).style.opacity=Math.min(1,v*1.3)}
$('#bt').style.transform=`scale(${K(P(t,1.8,2.3))}) rotate(${Math.sin(t*2)*4}deg)`}'''

SCENES = [
    scene('gauge', 6.5, g_body, g_js, g_css),
    scene('years', 7.0, y_body, y_js, y_css),
    chapter('ch1', '1', '그날 새 눈', 'snowflake'),
    scene('fresh', 6.0, f_body, f_js, f_css),
    chapter('ch2', '2', '얼마나 추울까', 'thermo'),
    scene('temp', 6.0, t_body, t_js, t_css),
    scene('lightup', 6.0, l_body, l_js, l_css),
    scene('pack', 7.0, p_body, p_js, p_css),
]

if __name__ == '__main__':
    render(SCENES, BASE, sys.argv[1:] or None)
