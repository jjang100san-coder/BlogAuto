# -*- coding: utf-8 -*-
# 수원삼성 화성 3-2 후기 클립 — 축구 카드 B 양식 색(짙은 바탕·수원 파랑·빨강·노란 강조)으로 짠 HTML 장면(clipkit/html_anim.py)
# 장면: ch1/ch2 장 카드 · quote 이정효 감독 회견 · table 순위(남은 5경기, 2위와 5점)
# 숫자·말은 발행본(224445997601) 그대로. 호칭은 ○○○ 선수 · ○○○ 감독
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from html_anim import scene, render

BASE = os.path.dirname(os.path.abspath(__file__))
DARK = '''body.dots{background:#11131A;background-image:radial-gradient(#1E2230 1.6px,transparent 1.6px);background-size:26px 26px;color:#fff}
.card{background:#1B1F2A;border:1px solid #2A3040;box-shadow:0 16px 40px rgba(0,0,0,.35)}'''


def chapter(name, n, title, sub, col):
    body = f'''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class="nb big" id="nb" style="background:{col}">{n}</div><div class="tt big" id="tt">{title}</div><div class="sb" id="sb">{sub}</div>
<div class="bar" id="br" style="background:{col}"></div></div>'''
    css = DARK + '''.nb{width:150px;height:150px;border-radius:50%;color:#fff;display:grid;place-items:center;font-size:92px}
.tt{font-size:116px;margin-top:40px;text-align:center}.sb{font-size:46px;font-weight:800;color:#F5D047;margin-top:24px}.bar{height:14px;border-radius:7px;margin-top:50px;width:0}'''
    js = '''function F(t){$('#nb').style.transform=`scale(${K(P(t,.05,.4))})`;
$('#tt').style.opacity=P(t,.3,.6);$('#tt').style.transform=`translateY(${(1-P(t,.3,.7))*40}px)`;$('#sb').style.opacity=P(t,.7,1.0);
$('#br').style.width=(700*P(t,.6,1.4))+'px'}'''
    return scene(name, 4.0, body, js, css)


q_body = '''<div class="stage" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px">
<div class="pill" id="who" style="background:#2E62D9;color:#fff;font-size:38px">이정효 감독 · 경기 뒤 회견</div>
<div class="card qq" id="q1"><span class="mk">“</span>체력 문제는 아니다</div>
<div class="card qq" id="q2"><span class="mk">“</span>편한 선택, 실수하지 않기 위한<br>선택 때문에 경기력 떨어진다고<br>생각한다</div></div>'''
q_css = DARK + '.qq{font-size:54px;font-weight:900;padding:40px 54px;line-height:1.4;width:1120px}.mk{color:#F5D047;font-size:90px;margin-right:12px;vertical-align:-24px}'
q_js = '''function F(t){$('#who').style.opacity=P(t,.05,.35);$('#q1').style.opacity=P(t,.3,.7);$('#q1').style.transform=`translateX(${(1-P(t,.3,.8))*-150}px)`;
$('#q2').style.opacity=P(t,1.4,1.8);$('#q2').style.transform=`translateX(${(1-P(t,1.4,1.9))*150}px)`}'''

TB = [('1', '수원삼성', 59), ('2', '수원FC', 54), ('3', '서울 이랜드', 54), ('4', '대구', 49)]
t_body = '<div class="stage" style="display:flex;flex-direction:column;gap:20px;justify-content:center">' + \
    '<div class="hd">K리그2 · 경기 뒤 순위 <span>(1·2위 바로 승격)</span></div>' + \
    ''.join(f'<div class="card rw" id="r{i}" style="{"border:4px solid #2E62D9" if i == 0 else ""}"><b>{a}</b><span>{b}</span><em id="p{i}">0</em></div>' for i, (a, b, c) in enumerate(TB)) + \
    '<div class="pill" id="gap" style="background:#F5D047;color:#11131A;font-size:44px;align-self:center">남은 5경기 · 2위와 5점</div></div>'
t_css = DARK + '''.hd{font-size:44px;font-weight:900}.hd span{font-size:32px;color:#9AA3B5}.rw{display:grid;grid-template-columns:90px 1fr 160px;align-items:center;padding:28px 40px;font-size:50px;font-weight:900}
.rw b{color:#F5D047}.rw em{font-style:normal;text-align:right}.rw em::after{content:'점';font-size:32px;margin-left:4px;color:#9AA3B5}'''
t_js = 'const V=' + str([c for _, _, c in TB]) + ''';
function F(t){V.forEach((v,i)=>{const u=P(t,.2+i*.25,.9+i*.25);$('#r'+i).style.opacity=Math.min(1,u*2);$('#p'+i).textContent=Math.round(v*u)});
$('#gap').style.transform=`scale(${K(P(t,2.2,2.6))})`}'''

SCENES = [
    chapter('ch1', '1', '왼쪽의 주인', '21분, 르본 선수', '#2E62D9'),
    chapter('ch2', '2', '또 그 시간', '63분 교체 뒤', '#D2333F'),
    scene('quote', 5.0, q_body, q_js, q_css),
    scene('table', 5.0, t_body, t_js, t_css),
]

if __name__ == '__main__':
    render(SCENES, BASE, sys.argv[1:] or None)
