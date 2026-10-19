from PIL import Image, ImageDraw, ImageFont
import math
BLACK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
REG  ="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD ="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG=(26,26,46); PANEL=(38,38,62); PANEL2=(52,52,80)
CREAM=(244,240,232); MUTED=(168,168,192); ACCENT=(232,196,120)
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
def tag(d,x,y,text,size=18,fill=CREAM,bg=(14,16,28)):
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

# ===== 01 thumb =====
H=660; im,d=base(H,"A매치 친선경기","10월 6일 화요일 오후 8시 · 용인미르스타디움")
center(d,(290,262),"한국",f(BLACK,60),CREAM)
center(d,(W/2,262),"vs",f(BOLD,40),MUTED)
center(d,(790,262),"우즈베키스탄",f(BLACK,52),CREAM)
d.rounded_rectangle([70,350,W-70,490],radius=18,fill=PANEL)
center(d,(W/2,398),"월드컵 5백의 우즈벡이 아니다",f(BOLD,36),CREAM)
center(d,(W/2,448),"9월부터 4-3-3 · 이란 3-1 · 시리아 4-1",f(REG,26),MUTED)
bar(d,530,"중원 셋이 겨누는 곳은 한국의 가운데")
im.save("images/01_thumb.png")

# ===== 02 two uzbek =====
rows=[("형태","3백 · 수비 땐 5백","4백 · 4-3-3"),
      ("가운데","미드필더 둘","미드필더 셋"),
      ("수비","낮은 블록","높게 압박 · 센터백도 전진"),
      ("공격","최전방 롱볼","탈취 즉시 공격 · 앞서면 역습"),
      ("결과","3전 전패 · 2득점 11실점","이란 3-1 · 시리아 4-1")]
top=290; rh=96; gap=12
H=top+len(rows)*(rh+gap)+30+82+80
im,d=base(H,"두 개의 우즈베키스탄","2026 월드컵(6월) → 9월 이후 칸나바로호")
lab=(70,230); c1=(242,620); c2=(632,1010)
for (x0,x1),col,t in [(c1,MUTED,"월드컵"),(c2,UZB,"9월 이후")]:
    d.rounded_rectangle([x0,190,x1,262],radius=14,fill=PANEL2)
    d.rectangle([x0,190,x1,198],fill=col)
    center(d,((x0+x1)/2,230),t,f(BLACK,30),CREAM)
y=top
for k,a,b in rows:
    left(d,(lab[0]+6,y+rh/2),k,f(BOLD,26),ACCENT)
    for (x0,x1),s,hl in ((c1,a,False),(c2,b,True)):
        d.rounded_rectangle([x0,y,x1,y+rh],radius=14,fill=PANEL2 if hl else PANEL)
        center(d,((x0+x1)/2,y+rh/2),s,f(BOLD,26),CREAM)
    y+=rh+gap
y+=18
bar(d,y,"가운데가 둘에서 셋으로 바뀌었다")
src(d,y+82+40,"칸나바로 기자회견 · 우즈벡·이란 해설 채널 · FotMob 경기 결과 · 직접 만든 이미지")
im.save("images/02_two_uzbek.png")

# ===== 03 goals =====
rows=[("상대 진영 압박",2,"이란전 첫 골 · 시리아전 첫 골"),
      ("크로스 헤더",2,"시리아전 노르차예프 두 골"),
      ("역습",1,"이란전 막판 단독 전진"),
      ("페널티킥",1,"이란전 쇼무로도프"),
      ("중앙 침투 패스",1,"시리아전 모즈고보이")]
top=200; rh=112; gap=12
H=top+len(rows)*(rh+gap)+30+82+80
im,d=base(H,"7골은 어디서 나왔나","9월 24일 이란 3-1 · 10월 1일 시리아 4-1")
BX0=380; unit=150
y=top
for k,n,ex in rows:
    d.rounded_rectangle([70,y,W-70,y+rh],radius=14,fill=PANEL)
    left(d,(100,y+38),k,f(BOLD,28),CREAM)
    left(d,(100,y+80),ex,f(REG,22),MUTED)
    for i in range(n):
        x=560+i*(140+10)
        d.rounded_rectangle([x,y+rh/2-18,x+140,y+rh/2+18],radius=8,fill=UZB if k=="상대 진영 압박" else (60,110,140))
    right(d,(W-100,y+rh/2),f"{n}골",f(BLACK,30),CREAM)
    y+=rh+gap
y+=18
bar(d,y,"동점이면 압박, 앞서면 내주고 역습",size=30)
src(d,y+82+40,"득점 루트는 우즈벡·이란·시리아 해설 채널 분석 기준 · 직접 만든 이미지")
im.save("images/03_goals.png")

# ===== 04 midfield diagram =====
H=1330; im,d=base(H,"가운데 숫자 싸움","공이 우즈벡에 있을 때 · 개념도")
w,h=430,700; A=(75,230); B=(575,230)
def P(o,fx,fy): return (o[0]+w*fx, o[1]+h*fy)
pitch(d,A[0],A[1],A[0]+w,A[1]+h); pitch(d,B[0],B[1],B[0]+w,B[1]+h)
center(d,(A[0]+w/2,200),"4-4-2 그대로면",f(BLACK,28),RED)
center(d,(B[0]+w/2,200),"한 명이 내려오면",f(BLACK,28),GREEN)
for o,fix in ((A,False),(B,True)):
    zone(im,[o[0]+w*0.18,o[1]+h*0.36,o[0]+w*0.82,o[1]+h*0.58],(232,108,100) if not fix else (120,200,140),45)
    d=ImageDraw.Draw(im)
    # Uzbek (attacking down): CBs, mids 3, front 3
    for fx in (0.35,0.65): player(d,*P(o,fx,0.14),UZB,r=14)
    for fx in (0.08,0.92): player(d,*P(o,fx,0.24),UZB,r=14)
    for fx,fy in [(0.5,0.36),(0.3,0.48),(0.7,0.48)]: player(d,*P(o,fx,fy),UZB,r=16)
    for fx,fy in [(0.15,0.66),(0.5,0.70),(0.85,0.66)]: player(d,*P(o,fx,fy),UZB,r=14)
    # Korea
    for fx in (0.12,0.37,0.63,0.88): player(d,*P(o,fx,0.82),KOR,r=14)
    player(d,*P(o,0.5,0.95),KOR,r=14)
    for fx in (0.1,0.9): player(d,*P(o,fx,0.58),KOR,r=14)
    player(d,*P(o,0.4,0.54),KOR,r=16); player(d,*P(o,0.6,0.54),KOR,r=16)
    if not fix:
        player(d,*P(o,0.4,0.27),KOR,r=16); player(d,*P(o,0.6,0.27),KOR,r=16)
        tag(d,*P(o,0.5,0.62),"가운데 2 대 3",20,RED)
    else:
        player(d,*P(o,0.4,0.25),KOR,r=16)
        gx,gy=P(o,0.6,0.25); d.ellipse([gx-16,gy-16,gx+16,gy+16],outline=KOR,width=3)
        arrow(d,P(o,0.59,0.29),P(o,0.52,0.40),KOR,dashed=True)
        player(d,*P(o,0.5,0.42),KOR,r=16)
        tag(d,*P(o,0.5,0.62),"가운데 3 대 3",20,GREEN)
d.ellipse([300,972,326,998],fill=KOR,outline=CREAM,width=2); left(d,(338,985),"한국",f(BOLD,24),CREAM)
d.ellipse([560,972,586,998],fill=UZB,outline=CREAM,width=2); left(d,(598,985),"우즈베키스탄",f(BOLD,24),CREAM)
y=1050
for i,t in enumerate(["베네수엘라전 전반: 가운데 둘, 누가 나갈지 정해지지 않았다",
                      "베네수엘라전 후반: 한 명이 내려와 셋, 경기가 바뀌었다",
                      "우즈벡은 9월부터 처음부터 가운데 셋"]):
    d.ellipse([90,y-17,124,y+17],fill=ACCENT); center(d,(107,y),str(i+1),f(BLACK,20),BG)
    left(d,(140,y),t,f(BOLD,24),CREAM); y+=50
bar(d,H-122,"월드컵 때 우즈벡의 약점이 지금 한국의 숙제",size=29)
im.save("images/04_midfield.png")

# ===== 05 watch =====
items=[("베네수엘라전 후반의 중원 셋을 킥오프부터 쓰는가","우즈벡 4-3-3을 상대로 첫 관문"),
       ("4-4-2라면 투톱 중 한 명을 내리는가","선수 구성으로 가운데를 두껍게"),
       ("황인범이 90분을 버틸 몸인가","아니면 다른 조합이 나오는가"),
       ("선발은 아쉽고 후반에 고치는 패턴이 끝나는가","세 경기 내내 반복된 흐름")]
top=190; step=118
H=top+step*len(items)+190+30+82+60
im,d=base(H,"우즈베키스탄전 채점","베네수엘라전 후기에서 미리 정한 네 가지")
for i,(a,b) in enumerate(items):
    y0=top+i*step
    d.rounded_rectangle([70,y0,W-70,y0+step-14],radius=16,fill=PANEL)
    d.ellipse([98,y0+24,148,y0+74],fill=ACCENT); center(d,(123,y0+49),str(i+1),f(BLACK,26),BG)
    left(d,(176,y0+34),a,f(BOLD,27),CREAM)
    left(d,(176,y0+72),b,f(REG,22),MUTED)
y0=top+len(items)*step+6
d.rounded_rectangle([70,y0,W-70,y0+170],radius=16,fill=PANEL2)
left(d,(100,y0+36),"우즈벡 쪽에서 볼 것",f(BLACK,26),UZB)
for j,t in enumerate(["첫 20분, 우즈벡 압박을 어떻게 벗어나나","손흥민 59호골은 4백 뒷공간에서 나오나","세트피스로 균형이 깨지나"]):
    left(d,(100,y0+80+j*34),"· "+t,f(BOLD,23),CREAM)
bar(d,H-122,"경기 후 이 네 가지를 그대로 채점한다")
im.save("images/05_watch.png")
print("ok")
