# -*- coding: utf-8 -*-
# 관음동 천장 붕괴 클립 — 마스터 5-8 양식 움직이는 인포그래픽(HTML+Playwright, clipkit/html_anim.py)
# 장면: frame 뼈대는 그대로·매단 천장만 · shelf 줄에 매단 선반 · ch1 · check 일본 점검표 vs 우리 빈칸 · ch2 · nine 최근 9건
#       exam 800건 세 칸 · speed 공장 2.0배 vs 현장 1.2배 · age 30년 넘은 건물 · three 정리(요약 장) · look 천장 올려다보기
# 숫자·사고 이름은 발행본(224443112219)·글 그림 그대로. 관음동 원인은 조사 중 — 단정하지 않음. 사고 장면 연출 없음(인명 피해 사고)
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


# ---------- frame: 뼈대는 그대로, 매단 천장만
fr_body = '''<div class="stage"><div class="card ab" style="inset:0">
<svg class="ab" style="inset:0" width="1210" height="825">
 <g fill="#9AA1AE"><rect x="190" y="90" width="640" height="34" rx="6"/><rect x="190" y="330" width="640" height="34" rx="6"/><rect x="190" y="570" width="640" height="34" rx="6"/>
 <rect x="200" y="90" width="34" height="514" rx="6"/><rect x="493" y="90" width="34" height="514" rx="6"/><rect x="786" y="90" width="34" height="514" rx="6"/></g>
 <g id="hang"><g stroke="#5B6276" stroke-width="4"><line x1="300" y1="364" x2="300" y2="410"/><line x1="420" y1="364" x2="420" y2="410"/><line x1="600" y1="364" x2="600" y2="410"/><line x1="720" y1="364" x2="720" y2="410"/></g>
 <rect id="ceil" x="234" y="408" width="552" height="26" rx="5" fill="#E9C9A0" stroke="#C9A06E" stroke-width="3"/></g>
 <rect id="ghost" x="234" y="408" width="552" height="26" rx="5" fill="none" stroke="#C8463C" stroke-width="4" stroke-dasharray="12 10" opacity="0"/>
</svg>
<div class="ab tag" id="t1" style="left:870px;top:200px"><b style="color:#2F8F5B">✓</b> 뼈대는 그대로</div>
<div class="ab tag" id="t2" style="left:870px;top:440px"><b style="color:#C8463C">↓</b> 매단 천장만</div>
<div class="ab lb2" style="left:60px;top:200px">3층</div><div class="ab lb2" style="left:60px;top:440px">2층</div>
<div class="ab pill" id="ppl" style="left:250px;bottom:40px;background:var(--red-l);color:var(--red);font-size:36px">66명 대피 · 38명 부상</div></div></div>'''
fr_css = '.tag{font-size:42px;font-weight:900;background:#fff;border-radius:18px;padding:14px 22px;box-shadow:0 8px 20px rgba(0,0,0,.08);white-space:nowrap}.lb2{font-size:40px;font-weight:900;color:var(--muted)}'
fr_js = '''function F(t){$('#t1').style.opacity=P(t,.3,.7);const d=P(t,1.4,2.4);
$('#ceil').setAttribute('transform',`translate(0 ${d*120}) rotate(${d*7} 510 420)`);$('#ceil').style.opacity=1-d*.35;$('#ghost').style.opacity=d;
$('#t2').style.opacity=P(t,2.0,2.4);$('#ppl').style.opacity=P(t,2.8,3.2)}'''

# ---------- shelf: 줄에 매단 선반
sh_body = '''<div class="stage"><div class="card ab" style="inset:0">
<div class="ab slab"></div><div class="ab str" id="s1" style="left:330px"></div><div class="ab str" id="s2" style="left:850px"></div>
<div class="ab shelf" id="sf"><div class="ly" id="l0"></div><div class="ly" id="l1"></div><div class="ly" id="l2"></div>
<div class="bulbs" id="bb">''' + ''.join(f'<i id="u{i}"></i>' for i in range(10)) + '''</div></div>
<div class="ab tag" id="g1" style="left:80px;top:470px">판 3겹</div><div class="ab tag" id="g2" style="left:80px;top:580px">조명 10개 <span class="mut" style="font-size:28px">(보도)</span></div>
<div class="ab pill" id="iv" style="right:60px;bottom:40px;background:var(--ink);color:#fff;font-size:34px">무엇이 결정적이었는지는 조사 중</div></div></div>'''
sh_css = '''.slab{left:200px;right:200px;top:60px;height:50px;background:#9AA1AE;border-radius:10px}.str{top:110px;width:6px;height:240px;background:#5B6276;border-radius:3px;transform-origin:top}
.shelf{left:300px;width:590px;top:350px}.ly{height:24px;background:#E9C9A0;border:3px solid #C9A06E;border-radius:6px;margin-top:-3px;opacity:0}
.bulbs{display:flex;justify-content:space-between;padding:10px 20px}.bulbs i{width:30px;height:30px;border-radius:50%;background:#FFD45E;box-shadow:0 0 16px #FFD45E;opacity:0}
.tag{font-size:42px;font-weight:900}'''
sh_js = '''function F(t){for(let i=0;i<3;i++)$('#l'+i).style.opacity=P(t,.3+i*.35,.5+i*.35);$('#g1').style.opacity=P(t,1.2,1.5);
for(let i=0;i<10;i++)$('#u'+i).style.opacity=P(t,1.8+i*.08,1.9+i*.08);$('#g2').style.opacity=P(t,2.4,2.7);
const s=P(t,1.0,3.0);['#s1','#s2'].forEach(q=>{$(q).style.transform=`scaleY(${1+s*.08})`;$(q).style.background=s>.6?'#D07A22':'#5B6276'});
$('#sf').style.transform=`translateY(${s*19}px)`;$('#iv').style.opacity=P(t,3.2,3.6)}'''

# ---------- check: 일본 점검표 vs 우리 빈칸
ck_body = '''<div class="stage" style="display:flex;flex-direction:column;gap:44px;justify-content:center;align-items:center"><div style="display:flex;gap:40px">
<div class="card cb" id="J"><div class="hd">일본 <span class="mut">2014년부터</span></div>
<div class="rw on">✓ 큰 매단 천장 정기조사</div><div class="sm">높이 6m · 넓이 200㎡ 넘으면</div></div>
<div class="card cb" id="Kr"><div class="hd">우리 건축물관리법</div>
<div class="rw">· 마감재 살펴보기</div><div class="rw gap" id="gp">매단 천장 — 조항 없음</div></div></div>
<div class="pill" id="nt" style="background:var(--red-l);color:var(--red);font-size:40px;white-space:nowrap">관음동 건물은 정기점검 대상도 아니었어</div></div>
<img class="icon3d ab" id="cl" src="icons/clip_t.png" style="height:180px;right:80px;top:260px">'''
ck_css = '''.cb{width:540px;padding:44px 40px;min-height:420px}.hd{font-size:48px;font-weight:900;margin-bottom:26px}.hd .mut{font-size:30px}
.rw{font-size:40px;font-weight:800;padding:18px 0;border-bottom:2px solid #EFE9DF}.rw.on{color:var(--ok)}.sm{font-size:30px;color:var(--ink2);font-weight:700;margin-top:12px}
.gap{color:var(--red);border:4px dashed var(--red);border-radius:16px;padding:18px 20px;margin-top:14px}'''
ck_js = '''function F(t){$('#J').style.transform=`scale(${K(P(t,.1,.5))})`;$('#Kr').style.transform=`scale(${K(P(t,.8,1.2))})`;
$('#gp').style.opacity=P(t,1.8,2.1)>0?(0.4+0.6*Math.abs(Math.sin(t*3))):0;$('#nt').style.opacity=P(t,2.8,3.2);
$('#cl').style.transform=`scale(${K(P(t,.3,.7))}) rotate(-8deg)`}'''

# ---------- nine: 최근 9건
NN = [('광주 학동', 2021, '순서를 바꾸고 흙을 쌓았다'), ('광주 화정', 2022, '받침을 일찍 뺐다'), ('인천 검단', 2023, '철근을 빠뜨렸다'),
      ('성남 정자교', 2023, '고칠 때를 놓쳤다'), ('안성 교량', 2025, '받침 72개를 치웠다'), ('오산 옹벽', 2025, '물길을 안 챙겼다'),
      ('광명 터널', 2025, '무게를 2.5배 작게 셌다'), ('광주 도서관', 2025, '용접을 대충 했다'), ('서울 서소문', 2026, '조사 중')]
nn_body = '<div class="stage"><div class="grid">' + ''.join(f'<div class="card nt" id="n{i}" style="{"background:#F3F0EA" if i == 8 else ""}"><div class="nm">{a} <span>{y}</span></div><div class="cs">{c}</div></div>' for i, (a, y, c) in enumerate(NN)) + '</div>' + \
    '<div class="ab stamp big" id="st">「기술이 없어서」 0건</div></div>'
nn_css = '''.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.nt{padding:30px 28px;height:240px}.nm{font-size:42px;font-weight:900}.nm span{font-size:32px;color:var(--muted)}
.cs{font-size:34px;font-weight:700;color:var(--ink2);margin-top:14px;line-height:1.35}
.stamp{left:50%;top:300px;font-size:88px;color:var(--red);border:9px solid var(--red);border-radius:24px;padding:16px 36px;background:rgba(255,255,255,.92);white-space:nowrap}'''
nn_js = '''function F(t){for(let i=0;i<9;i++){const v=P(t,.1+i*.17,.4+i*.17);$('#n'+i).style.opacity=v;$('#n'+i).style.transform=`translateY(${(1-v)*40}px)`}
const s=P(t,2.6,2.9);$('#st').style.opacity=s;$('#st').style.transform=`translateX(-50%) scale(${1.6-.6*s}) rotate(-5deg)`}'''

# ---------- exam: 800건 세 칸
EX = [('아는 문제를 틀림', 64.5, '#9AA1AE'), ('알면서 넘김', 21.75, '#C9A06E'), ('처음 보는 문제', 13.75, '#C8463C')]
ex_body = '<div class="stage"><div class="card ab" style="inset:0;padding:60px 60px">' + \
    '<div class="hh">손상 800건의 원인 <span class="mut">스위스 1976</span></div><div class="bar" id="br">' + \
    ''.join(f'<div class="sg" id="e{i}" style="background:{c}"></div>' for i, (n, v, c) in enumerate(EX)) + '</div>' + \
    '<div class="lg">' + ''.join(f'<div class="li" id="x{i}"><i style="background:{c}"></i>{n} <b>{v:g}%</b></div>' for i, (n, v, c) in enumerate(EX)) + '</div>' + \
    '<div class="hh" style="margin-top:60px" id="h2">그런데 손해액으로는</div><div class="bar"><div class="sg" id="loss" style="background:#C8463C"></div></div>' + \
    '<div class="big" id="lv" style="font-size:72px;color:#C8463C;margin-top:18px">처음 보는 문제 43%</div></div></div>'
ex_css = '''.hh{font-size:44px;font-weight:900}.hh .mut{font-size:30px}.bar{display:flex;height:84px;border-radius:18px;background:#F2EEE7;overflow:hidden;margin-top:24px}
.sg{height:100%;width:0}.lg{margin-top:22px;display:flex;flex-direction:column;gap:12px}.li{font-size:36px;font-weight:800;color:var(--ink2);display:flex;align-items:center;gap:14px}
.li i{width:30px;height:30px;border-radius:8px}.li b{color:var(--ink);font-weight:900}'''
ex_js = 'const V=' + str([v for _, v, _ in EX]) + ''';const W=1090;
function F(t){V.forEach((v,i)=>{const u=P(t,.2+i*.5,.7+i*.5);$('#e'+i).style.width=(W*v/100*u)+'px';$('#x'+i).style.opacity=P(t,.5+i*.5,.8+i*.5)});
$('#h2').style.opacity=P(t,2.3,2.6);$('#loss').style.width=(W*.43*P(t,2.6,3.4))+'px';$('#lv').style.opacity=P(t,3.3,3.6)}'''

# ---------- speed: 공장 2.0배 vs 현장 1.2배
sp_body = '''<div class="stage"><div class="card ab" style="inset:0;padding:60px">
<div class="hh">일하는 사람 한 명이 만드는 양 · 20년 뒤</div>
<div class="r"><div class="nm">공장</div><div class="b" id="a" style="background:#3D62AE"></div><div class="v" id="av">2.0배</div></div>
<div class="r"><div class="nm">건설 현장</div><div class="b" id="b" style="background:#D07A22"></div><div class="v" id="bv">1.2배</div></div>
<div class="sm">한 해 3.6% vs 1% · 직접 계산</div>
<img class="icon3d ab" id="hh" src="icons/helmet_t.png" style="height:200px;right:60px;bottom:40px"></div></div>'''
sp_css = '''.hh{font-size:42px;font-weight:900;margin-bottom:50px}.r{display:flex;align-items:center;gap:24px;margin-bottom:46px}.nm{width:230px;font-size:46px;font-weight:900}
.b{height:96px;border-radius:20px;width:0}.v{font-size:76px;font-weight:900;white-space:nowrap}.sm{font-size:32px;color:var(--muted);font-weight:700}'''
sp_js = '''function F(t){const a=P(t,.3,1.6),b=P(t,.6,1.6);$('#a').style.width=(270*2.0*a)+'px';$('#b').style.width=(270*1.2*b)+'px';
$('#av').style.opacity=P(t,1.5,1.8);$('#bv').style.opacity=P(t,1.5,1.8);$('#hh').style.transform=`scale(${K(P(t,1.8,2.2))})`}'''

# ---------- age: 30년 넘은 건축물
house = '<svg viewBox="0 0 100 100" class="hs"><path d="M10 48 L50 12 L90 48 V92 H10 Z" fill="#E7E1D6"/><path class="fl" d="M10 48 L50 12 L90 48 V92 H10 Z" fill="#B66A2C"/></svg>'
ag_body = '<div class="stage"><div class="card ab" style="inset:0;padding:50px 60px">' + \
    '<div class="hh">지은 지 30년 넘은 건축물</div><div class="hrow">' + ''.join(f'<div class="hc" id="h{i}">{house}</div>' for i in range(10)) + '</div>' + \
    '<div class="yy"><span class="big" id="pv">42.6%</span> <span class="mut" id="yr">2023년 말</span></div>' + \
    '<div class="sm">관음동 건물은 1994년에 지은 32년 된 건물</div></div></div>'
ag_css = '''.hh{font-size:46px;font-weight:900}.hrow{display:flex;gap:16px;margin-top:50px}.hc{width:100px;height:100px;position:relative}.hs{width:100px;height:100px}
.yy{margin-top:56px}.yy .big{font-size:140px;color:#B66A2C}.yy .mut{font-size:44px;font-weight:800}.sm{font-size:34px;font-weight:700;color:var(--ink2);margin-top:30px}'''
ag_js = '''const S=[[0,42.6,'2023년 말'],[1.6,44.4,'2024년 말'],[3.0,46.3,'2025년 말']];
function F(t){let v=0,y='';for(const [a,p,l] of S){if(t>=a){v=p;y=l}}const u=P(t,.2,1.0);const show=v*u;
for(let i=0;i<10;i++){const f=Math.max(0,Math.min(1,show/10-i));const p=$('#h'+i).querySelector('.fl');p.style.clipPath=`inset(${(1-f)*100}% 0 0 0)`}
$('#pv').textContent=(u<1?show:v).toFixed(1)+'%';$('#yr').textContent=y}'''

# ---------- three: 정리(요약 장)
TH = [('건너뛴 단계', '알던 걸 안 했다', 'helmet'), ('막지 않은 구멍', '규칙이 닿지 않는 칸', 'clip'), ('쌓인 나이', '30년 넘은 건물 46.3%', 'old')]
th_body = '<div class="stage" style="display:flex;flex-direction:column;gap:50px;justify-content:center;align-items:center"><div style="display:flex;gap:30px">' + \
    ''.join(f'<div class="card tc" id="c{i}"><img class="icon3d" src="icons/{ic_}_t.png" style="height:200px"><div class="k">{a}</div><div class="d">{b}</div></div>' for i, (a, b, ic_) in enumerate(TH)) + '</div>' + \
    '<div class="big" id="ft" style="font-size:56px;white-space:nowrap;color:var(--ink2)">「몰랐던 공학」은 적었다</div></div>'
th_css = '.tc{width:370px;padding:40px 24px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:16px}.k{font-size:50px;font-weight:900}.d{font-size:34px;font-weight:700;color:var(--ink2);line-height:1.35}'
th_js = '''function F(t){for(let i=0;i<3;i++){const v=K(P(t,.2+i*.5,.6+i*.5));$('#c'+i).style.transform=`scale(${v})`;$('#c'+i).style.opacity=Math.min(1,v*1.3)}
const s=P(t,2.2,2.6);$('#ft').style.opacity=s;$('#ft').style.transform=`translateY(${(1-s)*30}px)`}'''

# ---------- look: 천장 올려다보기
LK = ['금이 갔는지', '가운데가 처졌는지', '조각이 떨어져 있는지']
lk_body = '<div class="stage" style="display:flex;align-items:center;justify-content:center;gap:60px">' + \
    '<img class="icon3d" id="mg" src="icons/mag_t.png" style="height:400px">' + \
    '<div style="display:flex;flex-direction:column;gap:24px">' + ''.join(f'<div class="card lk" id="k{i}">{ic("check", 50, "#2F8F5B", 3)}<span>{s}</span></div>' for i, s in enumerate(LK)) + \
    '<div class="pill" id="sg" style="background:var(--ink);color:#fff;font-size:36px;align-self:flex-start">보이면 관리자·안전신문고</div></div></div>'
lk_css = '.lk{display:flex;align-items:center;gap:20px;padding:30px 36px;font-size:46px;font-weight:900;width:640px}'
lk_js = '''function F(t){$('#mg').style.transform=`rotate(${-10+Math.sin(t*1.6)*8}deg) translateY(${(1-P(t,.1,.6))*200}px)`;
for(let i=0;i<3;i++){const v=P(t,.6+i*.5,.9+i*.5);$('#k'+i).style.opacity=v;$('#k'+i).style.transform=`translateX(${(1-v)*120}px)`}
$('#sg').style.transform=`scale(${K(P(t,2.4,2.8))})`}'''

SCENES = [
    scene('frame', 6.0, fr_body, fr_js, fr_css),
    scene('shelf', 6.5, sh_body, sh_js, sh_css),
    chapter('ch1', '1', '점검표의 빈칸', 'clip'),
    scene('check', 6.0, ck_body, ck_js, ck_css),
    chapter('ch2', '2', '최근 9건', 'helmet'),
    scene('nine', 6.5, nn_body, nn_js, nn_css),
    scene('exam', 7.0, ex_body, ex_js, ex_css),
    chapter('ch3', '3', '기술은 현장까지?', 'factory'),
    scene('speed', 5.5, sp_body, sp_js, sp_css),
    scene('age', 6.0, ag_body, ag_js, ag_css),
    scene('three', 6.0, th_body, th_js, th_css),
    scene('look', 6.0, lk_body, lk_js, lk_css),
]

if __name__ == '__main__':
    render(SCENES, BASE, sys.argv[1:] or None)
