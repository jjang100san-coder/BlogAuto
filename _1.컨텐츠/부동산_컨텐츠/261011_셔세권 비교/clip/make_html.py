# -*- coding: utf-8 -*-
# 셔세권 클립 — 마스터 5-8 양식 움직이는 인포그래픽(HTML+Playwright, clipkit/html_anim.py)
# 장면: map 6곳 지도 · pair 같은 단지끼리 · ch1/ch2/ch3 장 카드 · race 6곳 막대 · duel 수지 vs 평택 · years 기준 해 4번
#       claims 유튜브 숫자 둘 · peak 이전 최고가 대비 · cliff 동탄 6월→7월 · people 인구 vs 값 · recap 요약
# 숫자는 발행본(224438963071) 그대로. 단지 이름 없음, 구·시 단위만. 색: 오름 빨강 · 내림 파랑(블로그 카드와 같게)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from html_anim import scene, render, ic

BASE = os.path.dirname(os.path.abspath(__file__))
UP, DN = '#C8463C', '#3D62AE'


def chapter(name, n, title, icon, sub=''):
    body = f'''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class="nb big" id="nb">{n}</div><div class="tt big" id="tt">{title}</div>
<div class="sb" id="sb">{sub}</div><img class="icon3d" id="ic" src="icons/{icon}_t.png" style="height:330px;margin-top:40px"></div>'''
    css = '''.nb{width:150px;height:150px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:92px}
.tt{font-size:112px;margin-top:40px;text-align:center}.sb{font-size:46px;color:var(--ink2);font-weight:700;margin-top:22px}'''
    js = '''function F(t){$('#nb').style.transform=`scale(${K(P(t,.05,.4))})`;
$('#tt').style.opacity=P(t,.3,.6);$('#tt').style.transform=`translateY(${(1-P(t,.3,.7))*40}px)`;$('#sb').style.opacity=P(t,.6,.9);
const v=P(t,.5,1.1);$('#ic').style.transform=`translateY(${(1-v)*300+Math.sin(t*3)*8}px)`;$('#ic').style.opacity=v}'''
    return scene(name, 4.0, body, js, css)


# ---------- map: 여섯 곳 핀 + 버스가 지나감
PINS = [('용인 수지구', 300, 190), ('수원 영통구', 700, 170), ('용인 기흥구', 420, 400), ('화성 병점구', 860, 370), ('화성 동탄구', 780, 580), ('평택시', 520, 740)]
m_body = '<div class="stage"><div class="card ab" style="inset:0;overflow:hidden;background:#F4EFE6">' + \
    '<svg class="ab" style="inset:0" width="1210" height="825"><path id="road" d="M300 200 C 500 170, 640 160, 700 180 S 470 400, 420 410 S 820 360, 860 380 S 800 580, 780 590 S 600 720, 520 750" fill="none" stroke="#D9CFBF" stroke-width="16" stroke-linecap="round" stroke-dasharray="2 28"/></svg>' + \
    ''.join(f'<div class="pin ab" id="p{i}" style="left:{x}px;top:{y}px"><div class="dot">{ic("pin", 46, "#fff", 2.4)}</div><div class="lb">{n}</div></div>' for i, (n, x, y) in enumerate(PINS)) + \
    '<img class="icon3d ab" id="bus" src="icons/bus_t.png" style="height:150px;left:0;top:0"></div>' + \
    '<div class="ab big" id="cnt" style="right:40px;bottom:30px;font-size:120px;color:var(--ink)">6곳</div></div>'
m_css = '''.pin{transform:translate(-50%,-100%)}.pin .dot{width:78px;height:78px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--pre);display:grid;place-items:center;margin:0 auto;box-shadow:0 10px 18px rgba(61,98,174,.3)}
.pin .dot svg{transform:rotate(45deg)}.pin .lb{margin-top:14px;background:#fff;border-radius:16px;padding:8px 18px;font-size:34px;font-weight:800;white-space:nowrap;box-shadow:0 6px 14px rgba(0,0,0,.08)}'''
m_js = '''const R=document.getElementById('road'),L=R.getTotalLength();
function F(t){const u=P(t,.3,4.2),q=R.getPointAtLength(L*u);const b=$('#bus');b.style.transform=`translate(${q.x-110}px,${q.y-40}px)`;
for(let i=0;i<6;i++){const v=K(P(t,.4+i*.55,.75+i*.55));const p=$('#p'+i);p.style.opacity=Math.min(1,v*1.5);p.style.transform=`translate(-50%,-100%) scale(${v})`}
$('#cnt').style.opacity=P(t,3.8,4.3);b.style.opacity=1-P(t,3.9,4.4)}'''

# ---------- pair: 같은 단지가 두 해 모두 팔린 경우만
p_body = '''<div class="stage" style="display:flex;align-items:center;justify-content:center;gap:40px">
<div class="card side" id="L"><div class="yr">2023</div><img class="icon3d" src="icons/apt_t.png" style="height:330px"><div class="tag">㎡당 가격</div></div>
<div class="mid" id="M"><div class="arr">→</div><div class="pill" style="background:var(--ink);color:#fff;font-size:34px">같은 단지</div></div>
<div class="card side" id="R"><div class="yr">2026</div><img class="icon3d" src="icons/apt_t.png" style="height:330px"><div class="tag" id="tg">㎡당 가격</div></div></div>'''
p_css = '''.side{width:440px;padding:40px 30px 36px;display:flex;flex-direction:column;align-items:center}.yr{font-size:64px;font-weight:900;color:var(--ink2)}
.tag{margin-top:22px;background:var(--pre-l);color:var(--pre);font-size:36px;font-weight:800;border-radius:16px;padding:10px 22px}
.mid{display:flex;flex-direction:column;align-items:center;gap:22px}.arr{font-size:120px;font-weight:900;color:var(--ons);line-height:1}'''
p_js = '''function F(t){const a=K(P(t,.1,.5)),b=K(P(t,.8,1.2));$('#L').style.transform=`scale(${a})`;$('#R').style.transform=`scale(${b})`;
$('#M').style.opacity=P(t,1.3,1.7);$('#M').style.transform=`translateX(${(1-P(t,1.3,1.8))*-60}px)`}'''

# ---------- race: 6곳 막대(0 기준 좌우)
RACE = [('용인 수지구', 31.5), ('화성 동탄구', 20.6), ('수원 영통구', 19.4), ('화성 병점구', 9.8), ('용인 기흥구', 8.6), ('평택시', -15.9)]
r_body = '<div class="stage"><div class="card ab" style="inset:0;padding:50px 40px">' + '<div class="axis ab"></div>' + \
    ''.join(f'<div class="row" style="top:{60 + i * 120}px"><div class="nm">{n}</div><div class="bar" id="b{i}" style="background:{UP if v > 0 else DN}"></div><div class="vl" id="v{i}" style="color:{UP if v > 0 else DN}">0</div></div>' for i, (n, v) in enumerate(RACE)) + \
    '<div class="ab mut" style="right:40px;bottom:26px;font-size:28px;font-weight:700">같은 단지 ㎡당 가격 · 2023 → 2026</div></div></div>'
r_css = '''.row{position:absolute;left:40px;right:40px;height:90px}.nm{position:absolute;left:0;width:250px;top:22px;font-size:38px;font-weight:800}
.axis{left:600px;top:40px;bottom:70px;width:4px;background:#D8D1C4;border-radius:2px}
.bar{position:absolute;left:562px;top:14px;height:62px;border-radius:14px}.vl{position:absolute;top:16px;font-size:46px;font-weight:900}'''
r_js = 'const V=' + str([v for _, v in RACE]) + ''';const S=12.0;
function F(t){V.forEach((v,i)=>{const u=P(t,.3+i*.35,1.3+i*.35),w=Math.abs(v)*S*u;const b=$('#b'+i),l=$('#v'+i);
b.style.width=w+'px';if(v<0){b.style.left=(562-w)+'px';l.style.left=(580)+'px'}else{b.style.left='562px';l.style.left=(562+w+18)+'px'}
l.textContent=u>0?sgn(v*u)+'%':'';l.style.opacity=u>0?1:0})}'''

# ---------- duel: 수지 vs 평택
d_body = '''<div class="stage" style="display:flex;align-items:center;justify-content:center;gap:60px">
<div class="card dc" id="A"><div class="nm">용인 수지구</div><div class="big vv" id="va" style="color:#C8463C">+0%</div><div class="ar" style="color:#C8463C">▲</div></div>
<div class="gap" id="G"><div class="big" style="font-size:80px">47%p</div><div class="mut" style="font-size:34px;font-weight:800;margin-top:8px">차이</div></div>
<div class="card dc" id="B"><div class="nm">평택시</div><div class="big vv" id="vb" style="color:#3D62AE">0%</div><div class="ar" style="color:#3D62AE">▼</div></div></div>'''
d_css = '''.dc{width:430px;height:560px;display:flex;flex-direction:column;align-items:center;justify-content:center}.nm{font-size:48px;font-weight:900}
.vv{font-size:120px;margin-top:26px}.ar{font-size:110px;margin-top:10px;line-height:1}.gap{text-align:center}'''
d_js = '''function F(t){const a=K(P(t,.1,.45)),b=K(P(t,.5,.85));$('#A').style.transform=`scale(${a})`;$('#B').style.transform=`scale(${b})`;
const u=P(t,.5,1.8);$('#va').textContent='+'+Math.round(31.5*u)+'%';$('#vb').textContent=(u>0?'−':'')+Math.round(15.9*u)+'%';
$('#G').style.opacity=P(t,2.0,2.4);$('#G').style.transform=`scale(${K(P(t,2.0,2.5))})`}'''

# ---------- years: 기준 해를 바꿔도
YRS = [('2019년부터', 83.0, 18.9), ('2021년부터', 9.9, -5.8), ('2023년부터', 31.5, -15.9), ('2025년부터', 16.7, -4.0)]
y_body = '<div class="stage" style="display:flex;flex-direction:column;gap:26px;justify-content:center">' + \
    '<div class="hdr"><span></span><span>맨 위</span><span>맨 아래</span></div>' + \
    ''.join(f'<div class="card yr" id="y{i}"><div class="by">{b}</div><div class="cell"><span class="crown">👑</span>수지 <b style="color:{UP}">{"+%.1f" % a}%</b></div><div class="cell">평택 <b style="color:{UP if c > 0 else DN}">{("+%.1f" % c) if c > 0 else ("−%.1f" % -c)}%</b></div></div>' for i, (b, a, c) in enumerate(YRS)) + '</div>'
y_css = '''.hdr{display:grid;grid-template-columns:300px 1fr 1fr;font-size:32px;font-weight:800;color:var(--muted);padding:0 40px}
.yr{display:grid;grid-template-columns:300px 1fr 1fr;align-items:center;padding:30px 40px}.by{font-size:40px;font-weight:900;color:var(--ink2)}
.cell{font-size:44px;font-weight:800}.cell b{font-weight:900}.crown{font-size:36px;margin-right:6px}'''
y_js = '''function F(t){for(let i=0;i<4;i++){const v=P(t,.2+i*.45,.6+i*.45);const e=$('#y'+i);e.style.opacity=v;e.style.transform=`translateX(${(1-v)*-120}px)`}}'''

# ---------- claims: 유튜브 숫자 둘 → 잣대가 달랐다
c_body = '''<div class="stage"><img class="icon3d ab" id="ph" src="icons/phone_t.png" style="height:380px;left:415px;top:40px">
<div class="card bub ab" id="b1" style="left:0;top:40px"><div class="q">「최고가 대비<br><b style="color:#3D62AE">−40%</b> 폭락」</div></div>
<div class="card bub ab" id="b2" style="right:0;top:40px"><div class="q">「1주에<br><b style="color:#C8463C">+2%</b> 상승」</div></div>
<div class="ab rl" id="r1" style="left:0;top:470px"><div class="k">잰 것</div>그 단지 역대 최고가<br>한 건 vs 최근 한 건</div>
<div class="ab rl" id="r2" style="right:0;top:470px"><div class="k">잰 것</div>표본 단지의<br>주간 지수</div>
<div class="ab stamp big" id="st">재는 법이 달랐다</div></div>'''
c_css = '''.bub{width:400px;padding:34px 30px;text-align:center}.q{font-size:46px;font-weight:800;line-height:1.35}.q b{font-weight:900;font-size:62px}
.rl{width:400px;text-align:center;font-size:36px;font-weight:700;color:var(--ink2);line-height:1.4}.k{display:inline-block;background:var(--sand);color:var(--ons);border-radius:12px;padding:4px 16px;font-size:30px;font-weight:900;margin-bottom:10px}
.stamp{left:50%;top:640px;font-size:84px;color:var(--red);border:8px solid var(--red);border-radius:22px;padding:14px 34px;background:rgba(255,255,255,.85);white-space:nowrap}'''
c_js = '''function F(t){$('#ph').style.transform=`scale(${K(P(t,.05,.4))})`;
$('#b1').style.transform=`scale(${K(P(t,.4,.8))}) rotate(-4deg)`;$('#b2').style.transform=`scale(${K(P(t,1.0,1.4))}) rotate(4deg)`;
$('#r1').style.opacity=P(t,2.0,2.4);$('#r2').style.opacity=P(t,2.4,2.8);
const s=P(t,3.2,3.5);$('#st').style.opacity=s;$('#st').style.transform=`translateX(-50%) scale(${1.6-.6*s}) rotate(-6deg)`}'''

# ---------- peak: 이전 최고가 대비(아래로) · −30% 선
PK = [('수지', -2.3), ('동탄', -3.5), ('영통', -8.7), ('기흥', -10.0), ('병점', -18.4), ('평택', -31.9)]
k_body = '<div class="stage"><div class="card ab" style="inset:0">' + '<div class="zero ab"></div><div class="lim ab" id="lim"><span>−30%</span></div>' + \
    ''.join(f'<div class="col ab" style="left:{70 + i * 180}px"><div class="nm">{n}</div><div class="bar" id="k{i}"></div><div class="vl" id="kv{i}"></div></div>' for i, (n, v) in enumerate(PK)) + \
    '<div class="ab mut" style="left:40px;bottom:26px;font-size:28px;font-weight:700">올해 7~9월 거래 · 그 단지 이전 최고가 대비</div></div></div>'
k_css = '''.zero{left:40px;right:40px;top:130px;height:4px;background:#D8D1C4}.lim{left:40px;right:40px;top:%dpx;border-top:5px dashed var(--red)}
.lim span{position:absolute;left:0;top:-56px;color:var(--red);font-size:38px;font-weight:900}
.col{top:40px;width:150px;text-align:center}.nm{font-size:40px;font-weight:900;height:90px}.bar{margin:0 auto;width:96px;background:#9DB0D6;border-radius:0 0 16px 16px}
.vl{font-size:40px;font-weight:900;color:var(--pre);margin-top:12px}''' % (132 + 30 * 17)
k_js = 'const V=' + str([v for _, v in PK]) + ''';
function F(t){V.forEach((v,i)=>{const u=P(t,.3+i*.25,1.2+i*.25);const b=$('#k'+i);b.style.height=(Math.abs(v)*17*u)+'px';
if(i==5){b.style.background=u>.95?'#3D62AE':'#9DB0D6'}$('#kv'+i).textContent=u>0?'−'+(Math.abs(v)*u).toFixed(1)+'%':''});
$('#lim').style.opacity=P(t,.1,.5)}'''

# ---------- cliff: 동탄 6월 → 7월
f_body = '''<div class="stage"><div class="card ab" style="inset:0;padding:40px">
<div class="ab" style="left:60px;top:40px;font-size:46px;font-weight:900">화성 동탄구 아파트 매매</div>
<div class="cb ab" style="left:220px"><div class="v" id="jv6"></div><div class="bar" id="j6"></div><div class="m">6월</div></div>
<div class="cb ab" style="left:600px"><div class="v" id="jv7"></div><div class="bar" id="j7" style="background:#3D62AE"></div><div class="m">7월</div></div>
<img class="icon3d ab" id="doc" src="icons/doc_t.png" style="height:230px;left:800px;top:110px">
<div class="ab pill" id="rg" style="left:760px;top:360px;background:var(--red-l);color:var(--red);font-size:34px">7월 1일 규제</div>
<div class="ab big" id="ten" style="right:60px;top:470px;font-size:96px;color:var(--pre)">10분의 1</div></div></div>'''
f_css = '''.cb{bottom:110px;height:600px;width:260px;text-align:center;display:flex;flex-direction:column;justify-content:flex-end}.bar{margin:0 auto;width:200px;background:#C8463C;border-radius:18px 18px 0 0}
.v{font-size:52px;font-weight:900;margin-top:12px}.m{font-size:40px;font-weight:800;color:var(--muted);margin-top:4px}
.cb .m{position:absolute;left:0;right:0;bottom:-60px}'''
f_js = '''function F(t){const a=P(t,.2,1.1);$('#j6').style.height=(1913*.27*a)+'px';$('#jv6').textContent=a>0?num(Math.round(1913*a))+'건':'';

const s=P(t,1.4,1.7);$('#doc').style.opacity=s;$('#doc').style.transform=`scale(${1.5-.5*s}) rotate(-8deg)`;$('#rg').style.opacity=P(t,1.6,1.9);
const b=P(t,2.0,2.6);$('#j7').style.height=(153*.27*b)+'px';$('#jv7').textContent=b>0?num(Math.round(153*b))+'건':'';
$('#ten').style.opacity=P(t,2.8,3.2)}'''

# ---------- people: 인구 vs 값
PP = [('용인 수지구', -2.2, 31.5), ('평택시', 8.4, -15.9)]
pe_body = '<div class="stage" style="display:flex;flex-direction:column;gap:40px;justify-content:center">' + \
    '<div class="hd"><span></span><span><img src="icons/people_t.png" class="icon3d" style="height:110px"><br>인구 4년</span><span><img src="icons/apt_t.png" class="icon3d" style="height:110px"><br>같은 단지 값</span></div>' + \
    ''.join(f'<div class="card pr" id="q{i}"><div class="nm">{n}</div><div class="c" style="color:{UP if a > 0 else DN}">{"▲" if a > 0 else "▼"} {("+%.1f" % a) if a > 0 else ("−%.1f" % -a)}%</div><div class="c" style="color:{UP if b > 0 else DN}">{"▲" if b > 0 else "▼"} {("+%.1f" % b) if b > 0 else ("−%.1f" % -b)}%</div></div>' for i, (n, a, b) in enumerate(PP)) + \
    '<div class="ab big" id="ne" style="left:50%;bottom:20px;font-size:72px;color:var(--ons)">사람 ≠ 값</div></div>'
pe_css = '''.hd{display:grid;grid-template-columns:330px 1fr 1fr;text-align:center;font-size:34px;font-weight:800;color:var(--ink2)}
.pr{display:grid;grid-template-columns:330px 1fr 1fr;align-items:center;padding:38px 40px;text-align:center}.pr .nm{font-size:46px;font-weight:900;text-align:left}.c{font-size:62px;font-weight:900}'''
pe_js = '''function F(t){for(let i=0;i<2;i++){const v=P(t,.3+i*.7,.8+i*.7);$('#q'+i).style.opacity=v;$('#q'+i).style.transform=`translateY(${(1-v)*60}px)`}
const s=P(t,2.2,2.6);$('#ne').style.opacity=s;$('#ne').style.transform=`translateX(-50%) scale(${K(s)})`}'''

# ---------- recap
RC = [('수지 +31.5% · 평택 −15.9%', 1), ('동탄·기흥 거래 10분의 1', 1), ('인구 늘어난 곳 ≠ 오른 곳', 1),
      ('셔틀 때문에 올랐다', 0), ('앞으로 오른다 · 내린다', 0), ('호재가 값을 올린다', 0)]
rc_body = '<div class="stage" style="display:grid;grid-template-columns:1fr 1fr;gap:34px;align-content:center">' + \
    '<div class="hh" style="color:var(--ok)">숫자가 말한 것</div><div class="hh" style="color:var(--red)">말하지 않은 것</div>' + \
    ''.join(f'<div class="card it" id="r{i}">{ic("check" if ok else "x", 46, "#2F8F5B" if ok else "#C8463C", 3)}<span>{s}</span></div>' for i, (s, ok) in enumerate([RC[0], RC[3], RC[1], RC[4], RC[2], RC[5]])) + '</div>'
rc_css = '''.hh{font-size:44px;font-weight:900;text-align:center}.it{display:flex;align-items:center;gap:18px;padding:34px 28px;font-size:38px;font-weight:800;line-height:1.3}
.it svg{flex:none}'''
rc_js = '''const O=[0,2,4,1,3,5];function F(t){O.forEach((k,j)=>{const v=K(P(t,.2+j*.4,.6+j*.4));const e=$('#r'+k);e.style.opacity=Math.min(1,v*1.4);e.style.transform=`scale(${v})`})}'''

SCENES = [
    scene('map', 6.0, m_body, m_js, m_css),
    scene('pair', 5.0, p_body, p_js, p_css),
    chapter('ch1', '1', '같은 셔틀, 다른 값', 'bus'),
    scene('race', 7.0, r_body, r_js, r_css),
    scene('duel', 5.0, d_body, d_js, d_css),
    scene('years', 6.0, y_body, y_js, y_css),
    chapter('ch2', '2', '유튜브 숫자', 'phone'),
    scene('claims', 6.5, c_body, c_js, c_css),
    scene('peak', 6.5, k_body, k_js, k_css),
    chapter('ch3', '3', '규제 다음 달', 'doc'),
    scene('cliff', 6.0, f_body, f_js, f_css),
    scene('people', 6.5, pe_body, pe_js, pe_css),
    scene('recap', 7.5, rc_body, rc_js, rc_css),
]

if __name__ == '__main__':
    render(SCENES, BASE, sys.argv[1:] or None)
