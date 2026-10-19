from PIL import Image, ImageDraw, ImageFont
BLACK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
REG  ="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD ="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG=(28,24,20); PANEL=(44,38,32); PANEL2=(60,52,44)
CREAM=(246,240,228); MUTED=(178,168,152); GOLD=(238,196,72)
GJ=(172,134,32); SW=(90,140,216); CORAL=(208,112,92)
W=1080
def f(p,s): return ImageFont.truetype(p,s,index=1)
def center(d,xy,t,fo,fi):
    x,y=xy; b=d.textbbox((0,0),t,font=fo)
    d.text((x-(b[2]-b[0])/2-b[0], y-(b[3]-b[1])/2-b[1]),t,font=fo,fill=fi)
def left(d,xy,t,fo,fi):
    x,y=xy; b=d.textbbox((0,0),t,font=fo)
    d.text((x, y-(b[3]-b[1])/2-b[1]),t,font=fo,fill=fi)
def base(H,band=GOLD):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,8],fill=band); return im,d
def head(d,t,s):
    center(d,(W/2,74),t,f(BLACK,50),CREAM); center(d,(W/2,130),s,f(REG,26),MUTED)
def bar(d,y,text,size=30,col=GOLD):
    d.rounded_rectangle([70,y,W-70,y+82],radius=14,fill=PANEL2)
    center(d,(W/2,y+41),text,f(BLACK,size),col)
def src(d,y,t): center(d,(W/2,y),t,f(REG,20),MUTED)

# 01 thumb (1:1)
H=1080; im,d=base(H)
center(d,(W/2,110),"이정효 감독 광주FC 4년",f(BLACK,66),CREAM)
center(d,(W/2,185),"2022 – 2025, 그리고 정효팬이 된 밤",f(REG,30),MUTED)
d.rounded_rectangle([70,250,W-70,560],radius=22,fill=PANEL)
center(d,(W/2,300),"2025 ACL 엘리트 16강 · 비셀 고베전",f(BOLD,28),MUTED)
center(d,(300,425),"0-2",f(BLACK,130),CORAL)
center(d,(W/2,425),"→",f(BLACK,90),MUTED)
center(d,(780,425),"3-2",f(BLACK,130),GOLD)
center(d,(300,520),"1차전 원정",f(BOLD,26),MUTED)
center(d,(780,520),"2차전 뒤 합계",f(BOLD,26),MUTED)
boxes=[("2022","K리그2 우승","승점 86"),("2023","K리그1 3위","구단 최고"),("2025","ACL 엘리트 8강","시민구단 최초")]
x0=70; bw=(W-140-2*20)/3
for i,(y,a,b) in enumerate(boxes):
    xa=x0+i*(bw+20); xb=xa+bw
    d.rounded_rectangle([xa,600,xb,850],radius=18,fill=PANEL)
    d.rectangle([xa,600,xb,610],fill=GJ)
    center(d,((xa+xb)/2,665),y,f(BLACK,40),GOLD)
    center(d,((xa+xb)/2,740),a,f(BLACK,32 if len(a)<8 else 28),CREAM)
    center(d,((xa+xb)/2,800),b,f(BOLD,25),MUTED)
bar(d,890,"팀이 아니라 사람을 따라가는 정효팬 연재",size=32)
src(d,1030,"기록: 스포츠경향 · 뉴시스 (2026년 10월 확인) · 직접 만든 이미지")
im.save("images/01_thumb.png")

# 02 namecard
rows=[("현재","수원삼성 감독 · 2025년 12월 24일 부임"),
      ("지도자 시작","2011년 아주대 코치"),
      ("코치","전남 · 광주 · 성남 · 제주"),
      ("광주FC 감독","2022 – 2025 시즌"),
      ("2022","K리그2 우승 · 승점 86 (2부 역대 최다)"),
      ("2023","K리그1 3위 · 구단 첫 ACL 진출"),
      ("2025","ACL 엘리트 8강 · 코리아컵 준우승"),
      ("저서","정답은 있다 (2026년 2월)")]
top=330; rh=86; gap=12
H=top+len(rows)*(rh+gap)+30+82+80
im,d=base(H)
center(d,(W/2,70),"정효볼을 만든 사람",f(BOLD,28),MUTED)
center(d,(W/2,160),"이정효",f(BLACK,104),CREAM)
center(d,(W/2,250),"수원삼성 감독 · 전 광주FC 감독",f(BOLD,28),CREAM)
d.rounded_rectangle([W/2-60,280,W/2+60,286],radius=3,fill=GOLD)
y=top
for i,(k,v) in enumerate(rows):
    d.rounded_rectangle([70,y,W-70,y+rh],radius=14,fill=PANEL2 if i==0 else PANEL)
    d.rectangle([70,y+14,78,y+rh-14],fill=SW if i==0 else GJ)
    left(d,(104,y+rh/2),k,f(BOLD,26),GOLD if i==0 else MUTED)
    left(d,(300,y+rh/2),v,f(BOLD,29),CREAM)
    y+=rh+gap
y+=18
bar(d,y,"환경 탓 말고 축구에 더 미쳐야 한다",size=31)
src(d,y+82+40,"이력: 다음스포츠(2025.3) · 스포츠경향(2025.12) / 문구는 감독 인터뷰 요지 · 직접 만든 이미지")
im.save("images/02_namecard.png")

# 03 timeline
ev=[("2022",GJ,"K리그2 우승","15명으로 시작한 전지훈련 → 승점 86, 1부 승격"),
    ("2023",GJ,"K리그1 3위","승격 첫해 구단 최고 성적, 첫 ACL 진출"),
    ("2024",GJ,"요코하마 7-3","ACL 엘리트 첫 경기 승리 · 긴 연패에도 잔류"),
    ("2025",GJ,"ACL 엘리트 8강","고베전 합계 3-2 역전 · 코리아컵 준우승"),
    ("2025.12",SW,"수원삼성 부임","광주와 작별, 2부 세 번째 시즌의 수원으로")]
top=200; rh=118; gap=16
H=top+len(ev)*(rh+gap)+20+82+90
im,d=base(H)
head(d,"이정효 감독 광주FC 4년","가진 게 없는 팀이 올라간 기록")
lx=190
d.line([lx,top+20,lx,top+len(ev)*(rh+gap)-gap-20],fill=PANEL2,width=6)
y=top
for yr,col,a,b in ev:
    d.rounded_rectangle([240,y,W-70,y+rh],radius=16,fill=PANEL)
    d.ellipse([lx-16,y+rh/2-16,lx+16,y+rh/2+16],fill=col,outline=CREAM,width=3)
    center(d,(105,y+rh/2),yr,f(BLACK,30 if len(yr)<5 else 24),GOLD if col==GJ else SW)
    left(d,(272,y+40),a,f(BLACK,32),CREAM)
    left(d,(272,y+84),b,f(BOLD,23),MUTED)
    y+=rh+gap
y+=4
bar(d,y,"말을 성적으로 받친 4년",size=32)
src(d,y+82+40,"기록: 스포츠경향 · 뉴시스 · 다음스포츠 / 15명 전지훈련은 감독 본인 발언 · 직접 만든 이미지")
im.save("images/03_timeline.png")

# 04 kobe
H=920; im,d=base(H,band=CORAL)
head(d,"광주 vs 비셀 고베, 0-2를 뒤집다","2025 ACL 엘리트 16강 · 2차전 3월 12일 광주월드컵경기장")
# leg1
d.rounded_rectangle([70,190,W-70,300],radius=16,fill=PANEL)
left(d,(104,245),"1차전 원정",f(BOLD,28),MUTED)
center(d,(W/2+40,245),"광주 0 – 2 고베",f(BLACK,40),CREAM)
left(d,(W-260,245),"합계 0-2",f(BOLD,28),CORAL)
steps=[("전반 18분","박정인","1-0","1-2",False),("후반 37분","아사니 PK","2-0","2-2",False),("연장 후반 13분","아사니","3-0","3-2",True)]
y=330
for t,who,sc,agg,last in steps:
    d.rounded_rectangle([70,y,W-70,y+120],radius=16,fill=PANEL2 if last else PANEL)
    d.rectangle([70,y+16,78,y+104],fill=GOLD if last else GJ)
    left(d,(104,y+42),t,f(BOLD,26),MUTED)
    left(d,(104,y+84),who,f(BLACK,34),CREAM)
    center(d,(640,y+60),"2차전 "+sc,f(BLACK,34),CREAM)
    center(d,(890,y+60),"합계 "+agg,f(BLACK,34),GOLD if last else CREAM)
    y+=136
y+=10
bar(d,y,"두 골 지고 와서도 끝까지 앞으로 갔다",size=31)
src(d,y+82+40,"기록: 뉴시스 · OSEN (2025.3.12) · 직접 만든 이미지")
im.save("images/04_kobe.png")

print("ok")
