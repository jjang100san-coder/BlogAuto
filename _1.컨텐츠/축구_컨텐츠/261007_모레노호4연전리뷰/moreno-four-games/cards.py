from PIL import Image, ImageDraw, ImageFont
import math
BLACK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
REG  ="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD ="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG=(36,22,26); PANEL=(52,36,40); PANEL2=(68,50,54)
CREAM=(244,240,232); MUTED=(190,170,172); ACCENT=(150,220,200)
KOR=(208,119,63); UZB=(46,156,192); RED=(232,108,100); GREEN=(120,200,140)
PITCH=(32,52,48); LINE=(96,124,118)
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
def tag(d,x,y,text,size=18,fill=CREAM,bg=(20,12,14)):
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

OPP=(92,134,200); AMBER=(236,190,100)
def chip(d,xy,text,col):
    x,y=xy; fo=f(BLACK,22); b=d.textbbox((0,0),text,font=fo); w=b[2]-b[0]+30
    d.rounded_rectangle([x-w,y-20,x,y+20],radius=20,fill=col); center(d,(x-w/2,y),text,fo,BG)

# 01 thumb
H=680; im,d=base(H,"모레노호 4연전 결산","9~10월 A매치 · 에콰도르 · 우루과이 · 베네수엘라 · 우즈베키스탄")
center(d,(W/2,262),"2승 1무 1패",f(BLACK,92),CREAM)
center(d,(W/2,340),"6득점 4실점 · 우루과이전 빼면 세 경기 무실점",f(REG,27),MUTED)
d.rounded_rectangle([70,390,W-70,500],radius=18,fill=PANEL)
center(d,(W/2,445),"찾은 방식은 상대가 공을 들고 나와야 통한다",f(BOLD,32),CREAM)
bar(d,540,"아시안컵 숙제는 내려앉는 팀이다",size=32)
im.save("images/01_thumb.png")

# 02 four games
rows=[("9월","에콰도르","3-0",GREEN,"출발은 좋았다"),
      ("9월","우루과이","1-4",RED,"투톱이 둘 다 달려들어 가운데 2대3"),
      ("10월","베네수엘라","0-0",AMBER,"압박을 줄였더니 가운데가 비었다"),
      ("10월","우즈베키스탄","2-0",GREEN,"투톱 한 명이 내려와 가운데를 닫았다")]
top=190; step=130
H=top+step*len(rows)+200+30+82+40
im,d=base(H,"네 경기에서 드러난 것","결과와 한 줄 요약")
for i,(m,opp,sc,col,line) in enumerate(rows):
    y0=top+i*step
    d.rounded_rectangle([70,y0,W-70,y0+step-14],radius=16,fill=PANEL)
    left(d,(100,y0+38),m,f(REG,24),MUTED); left(d,(180,y0+38),opp,f(BLACK,32),CREAM)
    chip(d,(W-100,y0+38),sc,col)
    left(d,(180,y0+82),line,f(REG,24),MUTED)
y0=top+len(rows)*step+6
d.rounded_rectangle([70,y0,W-70,y0+190],radius=16,fill=PANEL2)
left(d,(100,y0+36),"고친 것",f(BLACK,26),GREEN)
left(d,(100,y0+76),"투톱 한 명이 내려오는 압박 · 버티는 9번",f(BOLD,25),CREAM)
left(d,(100,y0+122),"남은 것",f(BLACK,26),RED)
left(d,(100,y0+160),"3선에서 앞으로 보내는 사람 · 이강인의 자리 · 강팀 상대 검증",f(BOLD,25),CREAM)
bar(d,H-122,"정반대로 틀린 두 경기 뒤에 답을 찾았다",size=30)
im.save("images/02_four_games.png")

# 03 three routes
routes=[("세트피스","정확한 키커 · 공중에서 이기는 선수","손흥민 직접 프리킥 59호골"),
        ("측면 크로스","버티는 9번 · 바이라인까지 가는 측면","오세훈 헤더골 · 송민규 도움"),
        ("중앙 콤비네이션","앞으로 보내는 6번 · 라인 사이에서 받는 선수","황인범 투입 뒤 후반 · 가운데의 이강인")]
top=190; step=200
H=top+step*len(routes)+30+82+40
im,d=base(H,"내려앉은 팀을 여는 세 갈래","길마다 필요한 선수가 다르다")
for i,(name,need,clue) in enumerate(routes):
    y0=top+i*step
    d.rounded_rectangle([70,y0,W-70,y0+step-18],radius=16,fill=PANEL)
    d.rectangle([70,y0+18,80,y0+step-36],fill=ACCENT)
    left(d,(110,y0+42),name,f(BLACK,34),CREAM)
    left(d,(110,y0+94),"필요한 것",f(REG,21),MUTED); left(d,(240,y0+94),need,f(BOLD,25),CREAM)
    left(d,(110,y0+138),"4연전 단서",f(REG,21),MUTED); left(d,(240,y0+138),clue,f(BOLD,25),ACCENT)
bar(d,H-122,"정답 하나가 아니라, 길마다 맞는 사람 찾기",size=29)
im.save("images/03_three_routes.png")

# 04 low block diagram
H=1330; im,d=base(H,"내려앉은 상대 앞에서","한국이 공을 쥐었을 때 · 개념도")
w,h=430,700; A=(75,230); B=(575,230)
def P(o,fx,fy): return (o[0]+w*fx, o[1]+h*fy)
pitch(d,A[0],A[1],A[0]+w,A[1]+h); pitch(d,B[0],B[1],B[0]+w,B[1]+h)
center(d,(A[0]+w/2,200),"4-4-2",f(BLACK,30),CREAM)
center(d,(B[0]+w/2,200),"4-3-3",f(BLACK,30),CREAM)
for o in (A,B):
    zone(im,[o[0]+w*0.2,o[1]+h*0.17,o[0]+w*0.8,o[1]+h*0.25],(150,220,200),40)
d=ImageDraw.Draw(im)
for o in (A,B):
    for fx in (0.1,0.3,0.5,0.7,0.9): player(d,*P(o,fx,0.11),OPP,r=13)
    for fx in (0.2,0.4,0.6,0.8): player(d,*P(o,fx,0.29),OPP,r=13)
    player(d,*P(o,0.5,0.44),OPP,r=13)
    player(d,*P(o,0.5,0.95),KOR,r=14)
# left 4-4-2
for fx,fy in [(0.35,0.72),(0.65,0.72),(0.1,0.56),(0.9,0.56),(0.38,0.53),(0.62,0.53),(0.12,0.36),(0.88,0.36),(0.4,0.19),(0.6,0.19)]:
    player(d,*P(A,fx,fy),KOR,r=15)
tag(d,*P(A,0.5,0.62),"가운데 둘은 블록 앞",17)
tag(d,*P(A,0.5,0.06),"라인 사이엔 투톱뿐",16)
# right 4-3-3
for fx,fy in [(0.36,0.70),(0.64,0.70),(0.12,0.40),(0.88,0.40),(0.07,0.16),(0.93,0.16),(0.5,0.18)]:
    player(d,*P(B,fx,fy),KOR,r=15)
player(d,*P(B,0.5,0.53),KOR,"6번",r=16)
player(d,*P(B,0.34,0.21),KOR,r=16); player(d,*P(B,0.66,0.21),KOR,r=16)
tag(d,*P(B,0.5,0.36),"8번 둘이 라인 사이로",17)
arrow(d,P(B,0.12,0.44),P(B,0.12,0.24),KOR,dashed=True)
arrow(d,P(B,0.88,0.44),P(B,0.88,0.24),KOR,dashed=True)
tag(d,*P(B,0.3,0.47),"측면 두 겹",16)
d.ellipse([300,962,326,988],fill=KOR,outline=CREAM,width=2); left(d,(338,975),"한국",f(BOLD,24),CREAM)
d.ellipse([540,962,566,988],fill=OPP,outline=CREAM,width=2); left(d,(578,975),"내려앉은 상대",f(BOLD,24),CREAM)
y=1040
for i,t in enumerate(["4-4-2: 가운데 둘이 블록 앞에 머물고 라인 사이가 빈다",
                      "4-3-3: 8번 둘이 라인 사이로, 측면은 두 겹",
                      "어느 쪽이든 앞으로 보내는 6번이 열쇠"]):
    d.ellipse([90,y-17,124,y+17],fill=ACCENT); center(d,(107,y),str(i+1),f(BLACK,20),BG)
    left(d,(140,y),t,f(BOLD,24),CREAM); y+=50
bar(d,H-122,"정답이 아니라 시험해 볼 그릇의 차이",size=30)
im.save("images/04_low_block.png")

# 05 november
items=[("내려앉은 상대 앞에서 공을 앞으로 보내는 사람","황인범 선발 90분인가, 다른 답인가"),
       ("이강인이 어디에 서는가","오른쪽 바깥 · 안쪽 · 가운데"),
       ("세 갈래 중 어느 길을 시험하나","세트피스 · 측면 크로스 · 중앙 콤비네이션"),
       ("아시안게임 출신이 몇 명, 어느 자리로","9번과 3선에 들어오는가")]
top=190; step=120
H=top+step*len(items)+30+82+80
im,d=base(H,"11월 A매치에서 볼 것","모레노 감독 임시 계약의 마지막 두 경기")
for i,(a,b) in enumerate(items):
    y0=top+i*step
    d.rounded_rectangle([70,y0,W-70,y0+step-14],radius=16,fill=PANEL)
    d.ellipse([98,y0+26,148,y0+76],fill=ACCENT); center(d,(123,y0+51),str(i+1),f(BLACK,26),BG)
    left(d,(176,y0+36),a,f(BOLD,27),CREAM); left(d,(176,y0+74),b,f(REG,22),MUTED)
bar(d,H-122-40,"조합을 정할 때가 아니라 찾을 때",size=31)
src(d,H-40,"아시안컵 2027.1.7~2.5 사우디아라비아 · 한국 E조: 레바논·예멘 승자 · 베트남 · UAE")
im.save("images/05_november.png")
print("ok")
