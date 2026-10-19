# -*- coding: utf-8 -*-
# LH사장 집값 클립 — 마스터 5-8 양식 움직이는 인포그래픽(HTML+Playwright, clipkit/html_anim.py)
# 장면: quote 국감 발언 · ch1 장 카드 · seoul 서울 고점→2년→지금 선 · regions 세 지역 · interest 집값 차이 vs 월 상환 차이
#       ch2 · supply 주문·출고·도착 · five 다섯 칸 판정(요약) · roads 두 길 같은 2028 · cal 내 달력
# 숫자는 발행본(224443149303) 그대로. 단지 이름 없음
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from html_anim import scene, render, ic

BASE = os.path.dirname(os.path.abspath(__file__))
UP, DN = '#C8463C', '#3D62AE'


def chapter(name, n, title, icon):
    body = f'''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class="nb big" id="nb">{n}</div><div class="tt big" id="tt">{title}</div><img class="icon3d" id="ic" src="icons/{icon}_t.png" style="height:340px;margin-top:50px"></div>'''
    css = '''.nb{width:150px;height:150px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:92px}
.tt{font-size:112px;margin-top:40px;text-align:center}'''
    js = '''function F(t){$('#nb').style.transform=`scale(${K(P(t,.05,.4))})`;
$('#tt').style.opacity=P(t,.3,.6);$('#tt').style.transform=`translateY(${(1-P(t,.3,.7))*40}px)`;
const v=P(t,.5,1.1);$('#ic').style.transform=`translateY(${(1-v)*300+Math.sin(t*3)*8}px)`;$('#ic').style.opacity=v}'''
    return scene(name, 4.0, body, js, css)


# ---------- quote: 국감 발언
q_body = '''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px">
<div class="pill" id="dt" style="background:var(--ink);color:#fff;font-size:38px">10월 12일 · 국정감사</div>
<div class="card qq" id="qq"><div class="mk">“</div><div id="tx"></div></div>
<img class="icon3d" id="mic" src="icons/mic_t.png" style="height:300px"></div>'''
q_css = '''.qq{width:1100px;padding:56px 70px 60px;position:relative}.mk{position:absolute;left:30px;top:-30px;font-size:180px;font-weight:900;color:var(--ons);line-height:1}
#tx{font-size:58px;font-weight:800;line-height:1.45;min-height:250px}'''
q_js = '''const S='안정이 되면 지금 바로 집을 사지 않아도 손해를 보지 않습니다.';
function F(t){$('#dt').style.opacity=P(t,.05,.35);$('#qq').style.transform=`scale(${K(P(t,.2,.6))})`;
const n=Math.round(S.length*P(t,.6,3.0));$('#tx').textContent=S.slice(0,n);$('#mic').style.transform=`translateY(${(1-P(t,.3,.9))*200}px)`}'''

# ---------- seoul: 고점 → 2년 → 지금 (100 → 84.3 → 106.3)
PTS = [(140, 260, '2021 고점'), (560, 260 + 15.7 * 22, '2년 기다림'), (1000, 260 + 15.7 * 22 - (106.3 - 84.3) * 22, '지금')]
s_body = '<div class="stage"><div class="card ab" style="inset:0">' + \
    '<svg class="ab" style="inset:0" width="1210" height="825"><path id="ln" d="M%d %d L%d %d L%d %d" fill="none" stroke="#1E2330" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>' % (PTS[0][0], PTS[0][1], PTS[1][0], PTS[1][1], PTS[2][0], PTS[2][1]) + \
    ''.join(f'<div class="dt ab" id="d{i}" style="left:{x - 22}px;top:{y - 22}px"></div><div class="lb ab" id="l{i}" style="left:{x - 120}px;top:{y + (40 if i == 1 else -90)}px">{l}</div>' for i, (x, y, l) in enumerate(PTS)) + \
    f'<div class="ab vv big" id="v1" style="left:150px;top:{PTS[1][1] - 20}px;color:{DN}">−15.7%</div>' + \
    f'<div class="ab vv big" id="v2" style="left:820px;top:{PTS[2][1] + 300}px;color:{UP}">+26.1%</div>' + \
    '<div class="ab mut" style="left:40px;bottom:26px;font-size:28px;font-weight:700">서울 25개 구 · 같은 단지·같은 면적 짝</div></div></div>'
s_css = '''.dt{width:44px;height:44px;border-radius:50%;background:#fff;border:10px solid var(--ink)}.lb{width:240px;text-align:center;font-size:36px;font-weight:800;color:var(--ink2)}
.vv{font-size:86px}'''
s_js = '''const L=document.getElementById('ln'),N=L.getTotalLength();L.style.strokeDasharray=N;
function F(t){const a=P(t,.3,1.6),b=P(t,2.2,3.5);const half=N*0.5;L.style.strokeDashoffset=N-(half*a+half*b);
[0,1,2].forEach(i=>{const v=K(P(t,[.1,1.5,3.4][i],[.4,1.8,3.7][i]));$('#d'+i).style.transform=`scale(${v})`;$('#l'+i).style.opacity=v});
$('#v1').style.opacity=P(t,1.6,1.9);$('#v2').style.opacity=P(t,3.5,3.8)}'''

# ---------- regions: 세 지역
RG = [('서울 25개 구', -15.7, 26.1), ('경기·인천 14곳', -18.3, 5.7), ('지방 광역시·세종', -13.1, -3.1)]
def pct(v): return ('+%.1f%%' % v) if v > 0 else ('−%.1f%%' % -v)
r_body = '<div class="stage" style="display:flex;flex-direction:column;gap:26px;justify-content:center">' + \
    '<div class="hd"><span></span><span>2년 기다리면</span><span>그 뒤 지금</span></div>' + \
    ''.join(f'<div class="card rw" id="r{i}"><div class="nm">{n}</div><div class="c" id="a{i}" style="color:{UP if a > 0 else DN}">{"▲" if a > 0 else "▼"} {pct(a)}</div><div class="c" id="b{i}" style="color:{UP if b > 0 else DN}">{"▲" if b > 0 else "▼"} {pct(b)}</div></div>' for i, (n, a, b) in enumerate(RG)) + '</div>'
r_css = '''.hd{display:grid;grid-template-columns:400px 1fr 1fr;text-align:center;font-size:36px;font-weight:800;color:var(--muted)}
.rw{display:grid;grid-template-columns:400px 1fr 1fr;align-items:center;padding:40px 40px;text-align:center}.rw .nm{font-size:46px;font-weight:900;text-align:left}.c{font-size:60px;font-weight:900}'''
r_js = '''function F(t){for(let i=0;i<3;i++){const v=P(t,.2+i*.35,.6+i*.35);$('#r'+i).style.opacity=v;$('#r'+i).style.transform=`translateX(${(1-v)*-100}px)`;
$('#a'+i).style.opacity=P(t,.5+i*.35,.8+i*.35);$('#b'+i).style.opacity=P(t,2.0+i*.4,2.3+i*.4)}}'''

# ---------- interest: 집값 차이 15.7% vs 월 상환액 차이 3.2%
i_body = '''<div class="stage"><div class="card ab" style="inset:0;padding:50px">
<img class="icon3d ab" id="coin" src="icons/coin_t.png" style="height:230px;right:60px;top:40px">
<div class="ab rate" id="rt" style="left:60px;top:60px"><span class="mut">대출 금리</span> 3.39% → <b style="color:#C8463C">4.52%</b></div>
<div class="row ab" style="top:250px"><div class="nm">집값 차이</div><div class="bar" id="x1" style="background:#3D62AE"></div><div class="vl" id="y1">15.7%</div></div>
<div class="row ab" style="top:460px"><div class="nm">월 상환액 차이</div><div class="bar" id="x2" style="background:#D07A22"></div><div class="vl" id="y2">3.2%</div></div>
<div class="ab mut" style="left:60px;bottom:26px;font-size:28px;font-weight:700">서울 · 집값 절반을 30년 고정금리로 빌렸다고 치면</div></div></div>'''
i_css = '''.rate{font-size:46px;font-weight:900}.row{left:60px;right:60px;height:150px}.nm{font-size:44px;font-weight:900;margin-bottom:16px}
.bar{height:80px;border-radius:18px;display:inline-block;vertical-align:middle}.vl{display:inline-block;vertical-align:middle;margin-left:20px;font-size:72px;font-weight:900}'''
i_js = '''function F(t){$('#rt').style.opacity=P(t,.1,.4);$('#coin').style.transform=`scale(${K(P(t,.1,.5))})`;
const a=P(t,.5,1.4);$('#x1').style.width=(15.7*45*a)+'px';$('#y1').style.opacity=P(t,1.2,1.5);
const b=P(t,2.0,2.6);$('#x2').style.width=Math.max(4,3.2*45*b)+'px';$('#y2').style.opacity=P(t,2.4,2.7)}'''

# ---------- supply: 주문·출고·도착
SP = [('주문', '인허가', 40.4), ('출고', '착공', 41.1), ('도착', '입주', -19.1)]
u_body = '<div class="stage"><div class="card ab" style="inset:0">' + \
    '<div class="trk ab"></div><img class="icon3d ab" id="box" src="icons/parcel_t.png" style="height:200px;top:150px;left:0">' + \
    ''.join(f'<div class="st ab" id="s{i}" style="left:{80 + i * 380}px"><div class="nm">{a}</div><div class="sb">{b}</div><div class="v" style="color:{UP if v > 0 else DN}">{pct(v)}</div></div>' for i, (a, b, v) in enumerate(SP)) + \
    '<div class="ab mut" style="left:40px;bottom:26px;font-size:28px;font-weight:700">서울 주택 · 2026년 1~8월 · 1년 전 같은 기간 대비</div></div></div>'
u_css = '''.trk{left:80px;right:80px;top:380px;height:12px;border-radius:6px;background:repeating-linear-gradient(90deg,#D9CFBF 0 30px,transparent 30px 50px)}
.st{top:440px;width:300px;text-align:center}.nm{font-size:60px;font-weight:900}.sb{font-size:36px;font-weight:700;color:var(--muted);margin-top:4px}.v{font-size:76px;font-weight:900;margin-top:20px}'''
u_js = '''function F(t){const x=80+P(t,.2,3.4)*760;$('#box').style.transform=`translateX(${x}px) translateY(${-Math.abs(Math.sin(t*6))*14}px)`;
for(let i=0;i<3;i++){const v=K(P(t,.3+i*1.3,.7+i*1.3));$('#s'+i).style.opacity=Math.min(1,v*1.4);$('#s'+i).style.transform=`scale(${v})`}}'''

# ---------- five: 다섯 칸 판정(요약 장)
FV = [('공급은 늦게 온다', '숫자와 맞다', 'ok'), ('대출로 경쟁적으로 산다', '반만 보인다', 'ons'), ('금리가 계속 오른다', '방향만 맞다', 'ons'),
      ('기다리면 손해 안 본다', '언제·어디냐에 달렸다', 'pre'), ('급락할 가능성이 많다', '지금 지표로는 안 보인다', 'red')]
f_body = '<div class="stage" style="display:flex;flex-direction:column;gap:20px;justify-content:center">' + \
    ''.join(f'<div class="card fv" id="f{i}"><div class="no">{i + 1}</div><div class="cl">{a}</div><div class="vd" id="g{i}" style="background:var(--{c}-l);color:var(--{c})">{b}</div></div>' for i, (a, b, c) in enumerate(FV)) + '</div>'
f_css = ''':root{--ok-l:#E2F1E8;--pre-l:#E6ECF8}.fv{display:grid;grid-template-columns:70px 1fr auto;align-items:center;gap:22px;padding:30px 36px}
.no{width:60px;height:60px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:34px;font-weight:900}
.cl{font-size:44px;font-weight:900}.vd{font-size:38px;font-weight:900;border-radius:16px;padding:12px 22px;white-space:nowrap}'''
f_js = '''function F(t){for(let i=0;i<5;i++){const v=P(t,.1+i*.25,.4+i*.25);$('#f'+i).style.opacity=v;
const s=P(t,1.6+i*.5,1.85+i*.5);$('#g'+i).style.opacity=s;$('#g'+i).style.transform=`scale(${1.5-.5*s})`}}'''

# ---------- roads: 두 길, 같은 2028
w_body = '''<div class="stage"><div class="card ab" style="inset:0">
<svg class="ab" style="inset:0" width="1210" height="825">
<path id="pu" d="M180 430 C 450 360, 700 260, 960 230" fill="none" stroke="#C8463C" stroke-width="12" stroke-linecap="round"/>
<path id="pd" d="M180 430 C 450 520, 700 620, 960 560" fill="none" stroke="#3D62AE" stroke-width="12" stroke-linecap="round"/>
<line x1="980" y1="140" x2="980" y2="700" stroke="#2F8F5B" stroke-width="8" stroke-dasharray="14 12"/></svg>
<div class="ab now" style="left:70px;top:390px">지금</div>
<div class="ab flag big" id="fl">2028</div>
<div class="ab ll" id="lu" style="left:330px;top:200px;color:#C8463C">반대편: 그 사이엔 오른다</div>
<div class="ab ll" id="ld" style="left:330px;top:620px;color:#3D62AE">LH 사장: 많이 낮아질 수 있다</div>
<div class="ab big" id="sm" style="left:50%;bottom:40px;font-size:56px;white-space:nowrap">도착은 같고, 길이 다르다</div></div></div>'''
w_css = '''.now{font-size:44px;font-weight:900;background:var(--ink);color:#fff;border-radius:16px;padding:10px 20px}
.flag{left:1000px;top:330px;font-size:80px;color:var(--ok)}.ll{font-size:42px;font-weight:900;white-space:nowrap}'''
w_js = '''const U=document.getElementById('pu'),D=document.getElementById('pd'),nu=U.getTotalLength(),nd=D.getTotalLength();U.style.strokeDasharray=nu;D.style.strokeDasharray=nd;
function F(t){U.style.strokeDashoffset=nu*(1-P(t,.3,2.0));D.style.strokeDashoffset=nd*(1-P(t,.6,2.3));
$('#lu').style.opacity=P(t,1.0,1.4);$('#ld').style.opacity=P(t,1.4,1.8);$('#fl').style.transform=`scale(${K(P(t,2.2,2.6))})`;
const s=P(t,3.0,3.4);$('#sm').style.opacity=s;$('#sm').style.transform=`translateX(-50%) translateY(${(1-s)*30}px)`}'''

# ---------- cal: 내 달력
c_body = '''<div class="stage"><div class="card ab" style="inset:0">
<img class="icon3d ab" id="ci" src="icons/cal_t.png" style="height:260px;left:50%;top:40px;margin-left:-130px">
<div class="ab tl"></div>''' + ''.join(f'<div class="ab yr" style="left:{90 + i * 330}px"><div class="tk"></div>{y}</div>' for i, y in enumerate([2026, 2027, 2028, 2029])) + '''
<div class="ab band" id="bd"></div>
<div class="ab mk" id="mk"><div class="q">내가 집이<br>필요한 때는?</div><div class="ar">▼</div></div></div></div>'''
c_css = '''.tl{left:90px;right:120px;top:560px;height:8px;background:var(--ink);border-radius:4px}.yr{top:540px;width:120px;margin-left:-60px;text-align:center;font-size:42px;font-weight:900;padding-top:70px}
.yr .tk{position:absolute;left:50%;top:6px;width:8px;height:48px;margin-left:-4px;background:var(--ink);border-radius:4px}
.band{left:160px;top:520px;height:88px;background:rgba(208,122,34,.18);border-radius:18px}
.mk{top:300px;width:330px;margin-left:-165px;text-align:center}.q{background:#fff;border:5px solid var(--red);color:var(--red);border-radius:22px;padding:16px;font-size:38px;font-weight:900;line-height:1.3}
.ar{color:var(--red);font-size:56px;line-height:1}'''
c_js = '''function F(t){$('#ci').style.transform=`scale(${K(P(t,.05,.45))})`;const w=P(t,.4,1.4);$('#bd').style.width=(820*w)+'px';
const x=180+700*(0.5+0.5*Math.sin(t*1.1-1.6))*P(t,1.0,1.6);$('#mk').style.left=x+'px';$('#mk').style.opacity=P(t,1.0,1.4)}'''

SCENES = [
    scene('quote', 5.5, q_body, q_js, q_css),
    chapter('ch1', '1', '기다린 2년', 'hourglass'),
    scene('seoul', 6.5, s_body, s_js, s_css),
    scene('regions', 6.5, r_body, r_js, r_css),
    scene('interest', 6.0, i_body, i_js, i_css),
    chapter('ch2', '2', '다섯 칸 점검', 'mic'),
    scene('supply', 6.0, u_body, u_js, u_css),
    scene('five', 7.5, f_body, f_js, f_css),
    scene('roads', 6.0, w_body, w_js, w_css),
    scene('cal', 6.5, c_body, c_js, c_css),
]

if __name__ == '__main__':
    render(SCENES, BASE, sys.argv[1:] or None)
