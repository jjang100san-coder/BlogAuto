from PIL import Image, ImageDraw, ImageFont
import math
BLACK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
REG  ="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD ="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG=(24,30,40); PANEL=(36,44,58); PANEL2=(50,60,78)
CREAM=(244,240,232); MUTED=(166,176,192); ACCENT=(240,140,130)
KOR=(208,119,63); UZB=(46,156,192); RED=(232,108,100); GREEN=(120,200,140)
PITCH=(30,52,58); LINE=(92,120,128)
W=1080
def f(p,s): return ImageFont.truetype(p,s,index=1)
def center(d,xy,t,fo,fi):
    x,y=xy; b=d.textbbox((0,0),t,font=fo)
    d.text((x-(b[2]-b[0])/2-b[0], y-(b[3]-b[1])/2-b[1]),t,font=fo,fill=fi)
def left(d,xy,t,fo,fi):
    x,y=xy; b=d.textbbox((0,0),t,font=fo)
    d.text((x, y-(b[3]-b[1])/2-b[1]),t,font=fo,fill=fi)
def right(d,xy,t,fo,fi):
    x,y=xy; b=d.textbbox((0,0),t,font=fo)
    d.text((x-(b[2]-b[0]), y-(b[3]-b[1])/2-b[1]),t,font=fo,fill=fi)
def base(H,title,sub):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,8],fill=ACCENT)
    center(d,(W/2,74),title,f(BLACK,48),CREAM)
    center(d,(W/2,130),sub,f(REG,26),MUTED)
    return im,d
def bar(d,y,text,size=30,col=ACCENT):
    d.rounded_rectangle([70,y,W-70,y+82],radius=14,fill=PANEL2)
    center(d,(W/2,y+41),text,f(BLACK,size),col)
def src(d,y,t): center(d,(W/2,y),t,f(REG,20),MUTED)
def pitch(d,x0,y0,x1,y1,lw=2):
    w=x1-x0; h=y1-y0
    d.rectangle([x0,y0,x1,y1],fill=PITCH,outline=LINE,width=lw)
    d.line([x0,y0+h/2,x1,y0+h/2],fill=LINE,width=lw)
    r=w*0.13; d.ellipse([x0+w/2-r,y0+h/2-r,x0+w/2+r,y0+h/2+r],outline=LINE,width=lw)
    bw=w*0.6; bh=h*0.13
    d.rectangle([x0+(w-bw)/2,y0,x0+(w+bw)/2,y0+bh],outline=LINE,width=lw)
    d.rectangle([x0+(w-bw)/2,y1-bh,x0+(w+bw)/2,y1],outline=LINE,width=lw)
def tag(d,x,y,text,size=18,fill=CREAM,bg=(12,16,24)):
    fo=f(BOLD,size); b=d.textbbox((0,0),text,font=fo); tw=b[2]-b[0]; th=b[3]-b[1]
    d.rounded_rectangle([x-tw/2-8,y-th/2-6,x+tw/2+8,y+th/2+8],radius=8,fill=bg)
    center(d,(x,y),text,fo,fill)
def player(d,x,y,col,label=None,r=16,below=True,size=17):
    d.ellipse([x-r,y-r,x+r,y+r],fill=col,outline=CREAM,width=3)
    if label: tag(d,x,y+(r+17 if below else -(r+17)),label,size)
def arrow(d,p1,p2,col,w=4,dashed=False,head=14):
    x1,y1=p1; x2,y2=p2; ang=math.atan2(y2-y1,x2-x1); L=math.hypot(x2-x1,y2-y1)
    if dashed:
        t=0
        while t<L-head:
            a=t; b=min(t+14,L-head*0.8)
            d.line([x1+math.cos(ang)*a,y1+math.sin(ang)*a,x1+math.cos(ang)*b,y1+math.sin(ang)*b],fill=col,width=w); t+=24
    else:
        d.line([x1,y1,x2-math.cos(ang)*head*0.8,y2-math.sin(ang)*head*0.8],fill=col,width=w)
    d.polygon([(x2,y2),(x2-math.cos(ang-0.42)*head,y2-math.sin(ang-0.42)*head),(x2-math.cos(ang+0.42)*head,y2-math.sin(ang+0.42)*head)],fill=col)
def zone(im,box,col,alpha=60):
    ov=Image.new("RGBA",im.size,(0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle(box,radius=18,fill=col+(alpha,))
    im.paste(Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB"))

AMBER=(236,190,100)
def chip(d,xy,text,col):
    x,y=xy; fo=f(BLACK,22); b=d.textbbox((0,0),text,font=fo); w=b[2]-b[0]+30
    d.rounded_rectangle([x-w,y-20,x,y+20],radius=20,fill=col); center(d,(x-w/2,y),text,fo,BG)

# ===== 01 thumb =====
H=700; im,d=base(H,"A매치 친선경기","10월 6일 · 용인미르스타디움")
center(d,(270,262),"한국",f(BLACK,52),CREAM)
center(d,(W/2,262),"2 - 0",f(BLACK,108),CREAM)
center(d,(810,262),"우즈베키스탄",f(BLACK,44),CREAM)
d.rounded_rectangle([70,350,W-70,520],radius=18,fill=PANEL)
for i,(m,who,how) in enumerate([("전반 6분","손흥민","직접 프리킥 · A매치 59호, 단독 1위"),("후반 15분","오세훈","헤더 · 도움 송민규")]):
    y=395+i*72
    left(d,(110,y),m,f(BOLD,26),MUTED); left(d,(270,y),who,f(BLACK,32),CREAM); left(d,(420,y),how,f(REG,25),MUTED)
bar(d,560,"투톱 한 명이 내려오자 가운데가 닫혔다",size=31)
im.save("images/01_thumb.png")

# ===== 02 stats =====
rows=[("점유율",45,55,"%"),("슈팅",9,13,""),("유효슈팅",6,4,""),("코너킥",2,4,""),("파울",12,10,"")]
top=250; step=92
H=top+step*len(rows)+40+140
im,d=base(H,"경기 기록","다음 스포츠 경기 기록 (KFA 원천)")
d.ellipse([300,176,326,202],fill=KOR); left(d,(338,189),"한국",f(BOLD,24),CREAM)
d.ellipse([580,176,606,202],fill=UZB); left(d,(618,189),"우즈베키스탄",f(BOLD,24),CREAM)
d.rounded_rectangle([70,top-30,W-70,top+step*len(rows)-10],radius=18,fill=PANEL)
CX=W/2; HALF=330
for i,(k,a,b,u) in enumerate(rows):
    y=top+i*step+30
    center(d,(CX,y-26),k,f(REG,22),MUTED)
    tot=a+b; la=HALF*a/tot; lb=HALF*b/tot
    d.rounded_rectangle([CX-HALF,y-2,CX-2,y+14],radius=6,fill=PANEL2); d.rounded_rectangle([CX+2,y-2,CX+HALF,y+14],radius=6,fill=PANEL2)
    d.rounded_rectangle([CX-2-la,y-2,CX-2,y+14],radius=6,fill=KOR); d.rounded_rectangle([CX+2,y-2,CX+2+lb,y+14],radius=6,fill=UZB)
    right(d,(CX-HALF-18,y+6),f"{a}{u}",f(BLACK,30),CREAM); left(d,(CX+HALF+18,y+6),f"{b}{u}",f(BLACK,30),CREAM)
bar(d,H-122,"공은 덜 가졌고, 골문 안 슈팅은 더 많았다",size=29)
im.save("images/02_stats.png")

# ===== 03 scorecard =====
A_=[("중원 셋을 킥오프부터","반반",AMBER,"수비할 땐 셋, 공을 가졌을 땐 아니었다"),
    ("투톱 한 명을 내려 가운데를 두껍게","맞음",GREEN,"수비할 때 한 명이 내려왔다"),
    ("황인범 90분 몸","빗나감",RED,"후반 45분만 뛰었다"),
    ("선발 아쉽고 후반에 고치는 패턴","반반",AMBER,"수비는 선발부터, 공격은 또 후반에")]
B_=[("첫 20분 우즈벡 압박","반반",AMBER),("손흥민 59호골은 뒷공간에서","반반",AMBER),
    ("세트피스로 균형이 깨지나","맞음",GREEN),("후반 우즈벡 압박이 꺾이나 (10/5 추가)","보류",MUTED)]
top=185; step=112
H=top+step*len(A_)+40+len(B_)*58+60+30+82+40
im,d=base(H,"우즈베키스탄전 프리뷰 채점","베네수엘라 후기에서 정한 네 가지 + 우즈벡 쪽 관전 포인트")
for i,(q,v,col,fact) in enumerate(A_):
    y0=top+i*step
    d.rounded_rectangle([70,y0,W-70,y0+step-14],radius=16,fill=PANEL)
    left(d,(102,y0+34),f"{i+1}  "+q,f(BOLD,27),CREAM); chip(d,(W-102,y0+34),v,col)
    left(d,(132,y0+72),fact,f(REG,22),MUTED)
y0=top+len(A_)*step+20
d.rounded_rectangle([70,y0,W-70,y0+60+len(B_)*58],radius=16,fill=PANEL2)
left(d,(102,y0+36),"우즈벡 쪽에서 볼 것",f(BLACK,25),UZB)
for j,(q,v,col) in enumerate(B_):
    yy=y0+90+j*58
    left(d,(102,yy),"· "+q,f(BOLD,24),CREAM); chip(d,(W-102,yy),v,col)
bar(d,H-122,"수비는 설계로, 공격은 사람으로 고쳤다",size=30)
im.save("images/03_scorecard.png")

# ===== 04 press diagram =====
H=1320; im,d=base(H,"투톱 한 명이 내려왔다","수비할 때와 공을 가졌을 때 · 개념도")
w,h=430,700; A=(75,230); B=(575,230)
def P(o,fx,fy): return (o[0]+w*fx, o[1]+h*fy)
pitch(d,A[0],A[1],A[0]+w,A[1]+h); pitch(d,B[0],B[1],B[0]+w,B[1]+h)
center(d,(A[0]+w/2,200),"수비할 때 — 가운데 3대3",f(BLACK,26),GREEN)
center(d,(B[0]+w/2,200),"공을 가졌을 때 — 대가",f(BLACK,26),RED)
zone(im,[A[0]+w*0.2,A[1]+h*0.26,A[0]+w*0.8,A[1]+h*0.53],(120,200,140),45)
zone(im,[B[0]+w*0.68,B[1]+h*0.22,B[0]+w*0.995,B[1]+h*0.52],(232,108,100),55)
d=ImageDraw.Draw(im)
# left: Uzbek building (attacking down)
for fx,fy in [(0.35,0.14),(0.65,0.14),(0.08,0.25),(0.92,0.25),(0.5,0.31),(0.32,0.43),(0.68,0.43),(0.15,0.65),(0.5,0.69),(0.85,0.65)]:
    player(d,*P(A,fx,fy),UZB,r=14)
arrow(d,P(A,0.46,0.27),P(A,0.39,0.23),KOR,dashed=True); player(d,*P(A,0.37,0.21),KOR,"손흥민",r=16,below=True)
arrow(d,P(A,0.6,0.22),P(A,0.53,0.33),KOR,dashed=True); player(d,*P(A,0.53,0.36),KOR,r=16); tag(d,*P(A,0.76,0.33),"오세훈이 내려옴",17)
player(d,*P(A,0.34,0.49),KOR,r=16); player(d,*P(A,0.66,0.49),KOR,r=16)
for fx in (0.1,0.9): player(d,*P(A,fx,0.55),KOR,r=14)
for fx in (0.15,0.38,0.62,0.85): player(d,*P(A,fx,0.82),KOR,r=14)
player(d,*P(A,0.5,0.95),KOR,r=14)
# right: Korea in possession (attacking up)
player(d,*P(B,0.5,0.95),KOR,r=14)
for fx,fy in [(0.36,0.80),(0.6,0.80)]: player(d,*P(B,fx,fy),KOR,r=14)
player(d,*P(B,0.82,0.76),KOR,r=16); tag(d,*P(B,0.78,0.86),"오른쪽 풀백은 뒤에 남음",16)
player(d,*P(B,0.12,0.48),KOR,r=14)
player(d,*P(B,0.42,0.6),KOR,r=14); player(d,*P(B,0.6,0.58),KOR,r=14)
player(d,*P(B,0.18,0.3),KOR,r=14)
player(d,*P(B,0.42,0.17),KOR,r=14); player(d,*P(B,0.58,0.15),KOR,r=14)
player(d,*P(B,0.86,0.38),KOR,"이강인",r=16)
for fx,fy in [(0.92,0.28),(0.72,0.47)]: player(d,*P(B,fx,fy),UZB,r=14)
for fx,fy in [(0.35,0.3),(0.55,0.32),(0.4,0.12),(0.62,0.1)]: player(d,*P(B,fx,fy),UZB,r=12)
tag(d,*P(B,0.66,0.69),"이강인 혼자 둘을 상대",17,RED)
d.ellipse([300,962,326,988],fill=KOR,outline=CREAM,width=2); left(d,(338,975),"한국",f(BOLD,24),CREAM)
d.ellipse([560,962,586,988],fill=UZB,outline=CREAM,width=2); left(d,(598,975),"우즈베키스탄",f(BOLD,24),CREAM)
y=1040
for i,t in enumerate(["수비 땐 손흥민이 한쪽 센터백, 오세훈이 내려와 미드필더",
                      "공을 가지면 오른쪽 풀백이 남아 셋이 빌드업",
                      "그만큼 오른쪽 이강인이 혼자 남았다 (해설 분석)"]):
    d.ellipse([90,y-17,124,y+17],fill=ACCENT); center(d,(107,y),str(i+1),f(BLACK,20),BG)
    left(d,(140,y),t,f(BOLD,24),CREAM); y+=50
bar(d,H-122,"가운데를 닫은 대가는 오른쪽이었다",size=30)
im.save("images/04_press.png")

# ===== 05 second half =====
H=1010; im,d=base(H,"하프타임 교체 두 장","46분 · 같은 자리를 같은 역할로")
rows=[("이재성","황인범","조율","감독 언급 없음 · 몸 상태 고려 가능성"),
      ("이강인","송민규","활동량","발목 불편 · 본인 요청 (감독 확인)")]
y=185
for out,inn,role,why in rows:
    d.rounded_rectangle([70,y,W-70,y+150],radius=16,fill=PANEL)
    left(d,(105,y+48),out,f(BOLD,30),MUTED); center(d,(300,y+48),"→",f(BLACK,32),MUTED)
    left(d,(350,y+48),inn,f(BLACK,34),CREAM); chip(d,(W-105,y+48),role,ACCENT)
    left(d,(105,y+108),why,f(REG,23),MUTED)
    y+=170
center(d,(W/2,y+30),"60분 둘째 골",f(BLACK,30),CREAM)
steps=["이한범","황인범","송민규","오세훈 헤더"]
y+=80; x0=95; bw=200; gap=(W-190-4*bw)/3
for i,s in enumerate(steps):
    x=x0+i*(bw+gap)
    d.rounded_rectangle([x,y,x+bw,y+90],radius=14,fill=PANEL2 if i<3 else KOR)
    center(d,(x+bw/2,y+45),s,f(BLACK,27),CREAM if i<3 else BG)
    if i<3: center(d,(x+bw+gap/2,y+45),"›",f(BLACK,40),MUTED)
y+=120
center(d,(W/2,y+10),"황인범이 받으러 움직여 상대를 제치고 공간으로 · 송민규가 끌고 가 연결",f(REG,22),MUTED)
bar(d,H-122,"새 전술이 아니라 맞는 사람을 넣었다",size=30)
im.save("images/05_second_half.png")
print("ok")
