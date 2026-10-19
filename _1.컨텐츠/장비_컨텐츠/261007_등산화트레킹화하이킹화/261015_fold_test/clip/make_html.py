# -*- coding: utf-8 -*-
# 캠프라인 밴티지 접어 보기 클립 — 마스터 5-8 양식 움직이는 인포그래픽(clipkit/html_anim.py) + 내 사진
# 장면: claim 영상 속 판별법 · ch1/ch2/ch3 장 카드 · verdict 세 켤레 다 접힘 · diff 옆모습 세 가지 차이 · scale 체중계 숫자 · recap 매장에서 볼 것
# 숫자는 발행본(224443138666) 그대로. 체중계 사진은 유리에 몸이 비쳐 클립엔 숫자 그림으로만
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from html_anim import scene, render, ic

BASE = os.path.dirname(os.path.abspath(__file__))


def chapter(name, n, title, icon):
    body = f'''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class="nb big" id="nb">{n}</div><div class="tt big" id="tt">{title}</div><img class="icon3d" id="ic" src="icons/{icon}_t.png" style="height:340px;margin-top:50px"></div>'''
    css = '''.nb{width:150px;height:150px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:92px}
.tt{font-size:112px;margin-top:40px;text-align:center}'''
    js = '''function F(t){$('#nb').style.transform=`scale(${K(P(t,.05,.4))})`;
$('#tt').style.opacity=P(t,.3,.6);$('#tt').style.transform=`translateY(${(1-P(t,.3,.7))*40}px)`;
const v=P(t,.5,1.1);$('#ic').style.transform=`translateY(${(1-v)*300+Math.sin(t*3)*8}px)`;$('#ic').style.opacity=v}'''
    return scene(name, 4.0, body, js, css)


# ---------- claim: 영상 속 판별법
cl_body = '''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px">
<div class="pill" id="src" style="background:var(--ink);color:#fff;font-size:36px">등산용품 매장 유튜브 · 2분쯤</div>
<div class="card qq" id="q1"><span class="mk">“</span>모든 등산화는 <b style="color:#C8463C">안 접히고</b>,</div>
<div class="card qq" id="q2"><span class="mk">“</span>러닝화는 운동화처럼 <b style="color:#3D62AE">접힌다</b></div>
<img class="icon3d" id="bt" src="icons/boot_t.png" style="height:170px"></div>'''
cl_css = '.qq{font-size:60px;font-weight:900;padding:40px 60px;position:relative}.qq b{font-weight:900}.mk{color:var(--ons);font-size:90px;margin-right:12px;vertical-align:-20px}'
cl_js = '''function F(t){$('#src').style.opacity=P(t,.05,.35);
$('#q1').style.transform=`translateX(${(1-P(t,.3,.8))*-160}px)`;$('#q1').style.opacity=P(t,.3,.7);
$('#q2').style.transform=`translateX(${(1-P(t,1.1,1.6))*160}px)`;$('#q2').style.opacity=P(t,1.1,1.5);
$('#bt').style.transform=`scale(${K(P(t,1.8,2.2))}) rotate(${Math.sin(t*2)*4}deg)`}'''

# ---------- verdict: 세 켤레 다 접힘
VD = [('캠프라인 밴티지', '경등산화'), ('아식스', '러닝화'), ('퓨마', '러닝화')]
vd_body = '<div class="stage" style="display:flex;flex-direction:column;gap:18px;justify-content:center">' + \
    ''.join(f'<div class="card vr" id="v{i}"><div><div class="nm">{a}</div><div class="kd">{b}</div></div><div class="ok" id="o{i}">{ic("check", 54, "#2F8F5B", 3.2)}<span>접혔다</span></div></div>' for i, (a, b) in enumerate(VD)) + \
    '<div class="stamp big" id="st">접기만으론 못 가린다</div></div>'
vd_css = '''.vr{display:flex;justify-content:space-between;align-items:center;padding:24px 50px}.nm{font-size:56px;font-weight:900}.kd{font-size:34px;font-weight:700;color:var(--muted);margin-top:6px}
.ok{display:flex;align-items:center;gap:14px;font-size:54px;font-weight:900;color:var(--ok);background:var(--ok-l);border-radius:20px;padding:14px 26px}
.stamp{align-self:center;font-size:70px;color:var(--red);border:9px solid var(--red);border-radius:24px;padding:14px 34px;background:rgba(255,255,255,.92);white-space:nowrap;margin-top:6px}'''
vd_js = '''function F(t){for(let i=0;i<3;i++){const v=P(t,.1+i*.3,.4+i*.3);$('#v'+i).style.opacity=v;$('#o'+i).style.transform=`scale(${K(P(t,.8+i*.4,1.1+i*.4))})`}
const s=P(t,2.4,2.7);$('#st').style.opacity=s;$('#st').style.transform=`scale(${1.5-.5*s}) rotate(-4deg)`}'''

# ---------- diff: 옆모습 세 가지 차이 (선 그림)
SV = {  # 왼쪽 밴티지, 오른쪽 러닝화
    'toe': ('<path d="M10 70 H150" stroke="#1E2330" stroke-width="10" stroke-linecap="round"/>',
            '<path d="M10 70 H100 Q140 70 150 35" stroke="#1E2330" stroke-width="10" fill="none" stroke-linecap="round"/>'),
    'sole': ('<path d="M10 40 H150 V70 H10 Z" fill="#5B6276"/><path d="M14 70 l10 14 l10 -14 l10 14 l10 -14 l10 14 l10 -14 l10 14 l10 -14 l10 14 l10 -14 l10 14 l10 -14 l10 14" stroke="#5B6276" stroke-width="7" fill="none"/>',
             '<path d="M10 25 H150 Q150 80 120 82 H40 Q10 80 10 25 Z" fill="#E7E1D6" stroke="#B9B2A4" stroke-width="5"/>'),
    'cap': ('<path d="M20 80 Q20 20 90 20 Q150 20 150 80 Z" fill="#E9DCC6" stroke="#9AA1AE" stroke-width="4"/><path d="M90 80 Q90 28 120 26 Q150 30 150 80 Z" fill="#3A3F4C"/>',
            '<path d="M20 80 Q20 20 90 20 Q150 20 150 80 Z" fill="#fff" stroke="#9AA1AE" stroke-width="4"/><g fill="#C9CED8"><circle cx="60" cy="50" r="4"/><circle cx="80" cy="40" r="4"/><circle cx="100" cy="52" r="4"/><circle cx="120" cy="44" r="4"/><circle cx="72" cy="64" r="4"/><circle cx="110" cy="68" r="4"/></g>'),
}
DF = [('앞코', 'toe', '바닥에 납작', '처음부터 들림'), ('밑창', 'sole', '깊은 돌기 고무창', '두꺼운 쿠션'), ('발가락', 'cap', '고무 덧댐(토캡)', '천(메시)만')]
df_body = '<div class="stage" style="display:flex;flex-direction:column;gap:24px;justify-content:center">' + \
    '<div class="hd"><span></span><span>밴티지</span><span>러닝화</span></div>' + \
    ''.join(f'''<div class="card dr" id="d{i}"><div class="k">{k}</div>
<div class="c"><svg viewBox="0 0 160 90" class="sv">{SV[s][0]}</svg><div class="l">{a}</div></div>
<div class="c"><svg viewBox="0 0 160 90" class="sv">{SV[s][1]}</svg><div class="l">{b}</div></div></div>''' for i, (k, s, a, b) in enumerate(DF)) + '</div>'
df_css = '''.hd{display:grid;grid-template-columns:200px 1fr 1fr;text-align:center;font-size:40px;font-weight:900;color:var(--ink2)}
.dr{display:grid;grid-template-columns:200px 1fr 1fr;align-items:center;padding:26px 30px}.k{font-size:50px;font-weight:900;color:var(--ons)}
.c{display:flex;flex-direction:column;align-items:center;gap:8px}.sv{width:220px;height:124px}.l{font-size:34px;font-weight:800;color:var(--ink2)}'''
df_js = '''function F(t){for(let i=0;i<3;i++){const v=P(t,.2+i*.7,.6+i*.7);$('#d'+i).style.opacity=v;$('#d'+i).style.transform=`translateY(${(1-v)*60}px)`}}'''

# ---------- scale: 체중계 숫자
SC = [('신발 없이', '98.87'), ('밴티지 들고', '99.93'), ('아식스 들고', '99.25'), ('퓨마 들고', '99.25')]
sc_body = '''<div class="stage" style="display:flex;align-items:center;justify-content:center;gap:50px">
<div class="card glass"><div class="lcd" id="lcd">--.--</div><div class="lb" id="lb">&nbsp;</div></div>
<div style="display:flex;flex-direction:column;gap:18px">''' + ''.join(f'<div class="card rw" id="r{i}"><span>{a}</span><b>{b}kg</b></div>' for i, (a, b) in enumerate(SC)) + '''
<div class="pill" id="nt" style="background:var(--red-l);color:var(--red);font-size:38px;align-self:flex-start">러닝화 둘이 똑같다?</div></div></div>'''
sc_css = '''.glass{width:470px;height:520px;background:linear-gradient(160deg,#F4F6F8,#DDE2E8);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px}
.lcd{font-family:'NK';font-size:120px;font-weight:300;letter-spacing:.04em;color:#2B3A4E}.lb{font-size:38px;font-weight:800;color:var(--ink2)}
.rw{display:flex;justify-content:space-between;gap:40px;padding:22px 34px;font-size:40px;font-weight:800;width:560px}.rw b{font-weight:900}'''
sc_js = 'const S=' + str([list(x) for x in SC]) + ''';
function F(t){let k=Math.min(3,Math.floor(t/0.9));$('#lcd').textContent=t<.2?'--.--':S[k][1];$('#lb').textContent=t<.2?'':S[k][0];
for(let i=0;i<4;i++){const v=P(t,.2+i*.9,.5+i*.9);$('#r'+i).style.opacity=v;$('#r'+i).style.background=(i==k&&t<3.8)?'#FBEBDA':'#fff'}
$('#nt').style.transform=`scale(${K(P(t,3.9,4.3))})`}'''

# ---------- recap: 매장에서 볼 것(요약 장)
RC = ['앞코가 들렸는지', '밑창 돌기가 깊은지', '발가락에 고무를 덧댔는지']
rc_body = '<div class="stage" style="display:flex;flex-direction:column;gap:26px;justify-content:center;align-items:center">' + \
    '<div class="hh">매장에서, 접기 전에 옆모습부터</div>' + \
    ''.join(f'<div class="card it" id="k{i}"><div class="no">{i + 1}</div><span>{s}</span></div>' for i, s in enumerate(RC)) + \
    '<img class="icon3d" id="bt" src="icons/boot_t.png" style="height:220px">' + '</div>'
rc_css = '''.hh{font-size:52px;font-weight:900}.it{display:flex;align-items:center;gap:24px;padding:30px 40px;font-size:50px;font-weight:900;width:900px}
.no{width:70px;height:70px;border-radius:50%;background:var(--ons);color:#fff;display:grid;place-items:center;font-size:40px;flex:none}'''
rc_js = '''function F(t){for(let i=0;i<3;i++){const v=K(P(t,.3+i*.5,.7+i*.5));$('#k'+i).style.transform=`scale(${v})`;$('#k'+i).style.opacity=Math.min(1,v*1.3)}
$('#bt').style.transform=`translateY(${(1-P(t,1.8,2.4))*200}px) rotate(${Math.sin(t*2)*4}deg)`;$('#bt').style.opacity=P(t,1.8,2.2)}'''

SCENES = [
    scene('claim', 5.0, cl_body, cl_js, cl_css),
    chapter('ch1', '1', '직접 접어 보기', 'boot'),
    scene('verdict', 5.5, vd_body, vd_js, vd_css),
    chapter('ch2', '2', '차이는 옆모습', 'boot'),
    scene('diff', 6.0, df_body, df_js, df_css),
    chapter('ch3', '3', '무게는?', 'scale'),
    scene('scale', 6.0, sc_body, sc_js, sc_css),
    scene('recap', 6.0, rc_body, rc_js, rc_css),
]

if __name__ == '__main__':
    render(SCENES, BASE, sys.argv[1:] or None)
