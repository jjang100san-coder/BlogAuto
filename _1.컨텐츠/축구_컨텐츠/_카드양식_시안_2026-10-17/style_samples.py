# -*- coding: utf-8 -*-
"""축구 카드 양식 시안 3종 (2026-10-17) — 「Claude로 만든 카드」처럼 보이는 공통 꼴을 피하려고.
지금 꼴의 특징(피하려는 것): 어두운 배경 + 둥근 패널 반복 + 가운데 큰 제목·회색 부제 + 둥근 결론 바 + 가운데 출처 줄.
같은 내용(수원·화성의 안산전 비교)을 세 양식으로 그린다.
  A 신문 지면형   — 크림 종이, 명조 제목, 가는 괘선, 둥근 모서리 없음, 왼쪽 정렬
  B 매치데이형    — 두 팀 색을 화면 반씩 크게 깔고 큰 숫자, 각진 블록, 대각 띠
  C 전술 노트형   — 모눈종이, 손으로 그은 듯 흔들리는 선·형광펜, 동그라미 메모(사용자가 화면에 그려 보내는 표시와 같은 결)
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SANS = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
SERIF = r"C:\Windows\Fonts\NotoSerifKR-VF.ttf"
def F(path, size, w=400):
    fo = ImageFont.truetype(path, size)
    try: fo.set_variation_by_axes([w])
    except Exception: pass
    return fo
W = 1080
ROWS = [("결과", "4-1 승", "2-0 승"), ("점유", "60%", "44%"), ("슈팅(유효)", "17(10)", "7(4)"),
        ("첫 골", "2분", "66분 PK"), ("마지막 골", "61분", "96분"), ("실점", "68분", "0")]
SUW, HWA = (28,72,170), (236,120,40)      # 수원 청 / 화성 주황(구단 색 계열, 엠블럼·로고는 안 씀)

def tw(d, t, fo): b = d.textbbox((0,0), t, font=fo); return b[2]-b[0], b[3]-b[1]

# ---------------------------------------------------------------- A 신문 지면형
def style_a():
    H = 1180; INK = (24,22,20); PAPER = (244,239,228); RULE = (60,56,50); MUT = (110,104,96)
    im = Image.new("RGB", (W,H), PAPER); d = ImageDraw.Draw(im)
    L, R = 80, W-80
    d.text((L,70), "K리그2 29라운드 프리뷰 · 10월 18일", font=F(SANS,24,700), fill=MUT)
    d.line([L,112,R,112], fill=RULE, width=3); d.line([L,118,R,118], fill=RULE, width=1)
    d.text((L,140), "같은 안산,", font=F(SERIF,76,900), fill=INK)
    d.text((L,232), "두 번의 승리", font=F(SERIF,76,900), fill=INK)
    d.text((L,338), "수원은 공을 쥐고 일찍, 화성은 공을 내주고 늦게 이겼다.", font=F(SERIF,30,500), fill=MUT)
    y = 420; c1, c2 = 470, 780
    d.text((c1,y), "수원삼성", font=F(SANS,28,900), fill=SUW); d.text((c2,y), "화성FC", font=F(SANS,28,900), fill=HWA)
    y += 52; d.line([L,y,R,y], fill=RULE, width=2)
    for i,(k,a,b) in enumerate(ROWS):
        yy = y + 22 + i*92
        d.text((L,yy+10), k, font=F(SANS,26,500), fill=MUT)
        d.text((c1,yy), a, font=F(SERIF,46,800), fill=INK); d.text((c2,yy), b, font=F(SERIF,46,800), fill=INK)
        d.line([L,yy+78,R,yy+78], fill=(196,188,174), width=1)
    yb = y + 22 + len(ROWS)*92 + 10
    d.rectangle([L,yb,L+8,yb+60], fill=INK)
    d.text((L+28,yb+8), "10월 18일의 질문은 누가 먼저 뚫느냐다.", font=F(SERIF,34,800), fill=INK)
    d.text((L,H-62), "기록: 다음 스포츠 · 득점 시각: K리그 공식 기록 · 직접 만든 이미지", font=F(SANS,20,400), fill=MUT)
    im.save(os.path.join(HERE, "A_신문지면형.png"))

# ---------------------------------------------------------------- B 매치데이형
def style_b():
    H = 1180; im = Image.new("RGB", (W,H), (14,16,22)); d = ImageDraw.Draw(im)
    d.polygon([(0,0),(W*0.56,0),(W*0.44,H),(0,H)], fill=SUW)
    d.polygon([(W*0.56,0),(W,0),(W,H),(W*0.44,H)], fill=HWA)
    ov = Image.new("RGBA", (W,H), (0,0,0,0)); od = ImageDraw.Draw(ov)
    od.rectangle([0,0,W,190], fill=(0,0,0,150)); od.rectangle([0,H-230,W,H], fill=(0,0,0,170))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im)
    d.text((60,52), "VS 안산그리너스", font=F(SANS,30,900), fill=(255,255,255))
    d.text((60,104), "같은 상대, 다른 승리", font=F(SANS,44,900), fill=(255,230,120))
    def big(x, num, unit, label, anchor_right=False):
        fn, fu = F(SANS,230,900), F(SANS,70,900)
        wn, _ = tw(d, num, fn); wu, _ = tw(d, unit, fu)
        x0 = x - (wn+wu+8) if anchor_right else x
        d.text((x0,250), num, font=fn, fill=(255,255,255)); d.text((x0+wn+8,390), unit, font=fu, fill=(255,255,255))
        lw, _ = tw(d, label, F(SANS,34,900)); d.text((x0 if not anchor_right else x-lw, 540), label, font=F(SANS,34,900), fill=(255,255,255))
    big(70, "2", "분", "수원삼성 첫 골"); big(W-70, "66", "분", "화성FC 첫 골", anchor_right=True)
    rows = [("점유", "60%", "44%"), ("슈팅(유효)", "17(10)", "7(4)"), ("마지막 골", "61분", "96분"), ("실점", "68분", "0")]
    y = 640
    for k,a,b in rows:
        d.text((70,y), a, font=F(SANS,40,900), fill=(255,255,255))
        kw, _ = tw(d, k, F(SANS,26,700)); d.text(((W-kw)/2,y+10), k, font=F(SANS,26,700), fill=(255,255,255))
        bw, _ = tw(d, b, F(SANS,40,900)); d.text((W-70-bw,y), b, font=F(SANS,40,900), fill=(255,255,255))
        d.line([70,y+62,W-70,y+62], fill=(255,255,255), width=1); y += 80
    d.text((60,H-190), "10월 18일, 누가 먼저 뚫을까", font=F(SANS,50,900), fill=(255,230,120))
    d.text((60,H-58), "기록: 다음 스포츠 · 득점 시각: K리그 공식 기록 · 직접 만든 이미지", font=F(SANS,20,400), fill=(220,220,220))
    im.save(os.path.join(HERE, "B_매치데이형.png"))

# ---------------------------------------------------------------- C 전술 노트형
def wobbly(d, p0, p1, col, w=4, amp=1.6, seed=0):
    rnd = random.Random(seed); n = max(8, int(math.hypot(p1[0]-p0[0], p1[1]-p0[1])/18))
    pts = [(p0[0]+(p1[0]-p0[0])*i/n + rnd.uniform(-amp,amp), p0[1]+(p1[1]-p0[1])*i/n + rnd.uniform(-amp,amp)) for i in range(n+1)]
    d.line(pts, fill=col, width=w, joint="curve")
def wobbly_ellipse(d, box, col, w=4, seed=0):
    rnd = random.Random(seed); x0,y0,x1,y1 = box; cx,cy,rx,ry = (x0+x1)/2,(y0+y1)/2,(x1-x0)/2,(y1-y0)/2
    pts = []
    for i in range(0, 380, 8):
        a = math.radians(i - 20); r = 1 + rnd.uniform(-0.04, 0.04)
        pts.append((cx+rx*r*math.cos(a), cy+ry*r*math.sin(a)))
    d.line(pts, fill=col, width=w, joint="curve")
def style_c():
    H = 1180; PAPER = (250,250,246); GRID = (214,226,236); INK = (34,38,48); RED = (214,52,52); BLUE = (40,96,210)
    im = Image.new("RGB", (W,H), PAPER); d = ImageDraw.Draw(im)
    for x in range(0, W, 36): d.line([x,0,x,H], fill=GRID, width=1)
    for y in range(0, H, 36): d.line([0,y,W,y], fill=GRID, width=1)
    ov = Image.new("RGBA", (W,H), (0,0,0,0)); od = ImageDraw.Draw(ov)
    od.rectangle([70,92,700,160], fill=(255,226,80,150))          # 형광펜
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im)
    d.text((80,90), "같은 안산, 두 번의 승리", font=F(SANS,58,900), fill=INK)
    d.text((82,180), "9/12 화성 2-0 (원정)  ·  10/11 수원 4-1 (홈)", font=F(SANS,28,500), fill=(90,96,110))
    c1, c2, L = 470, 780, 80
    d.text((c1,262), "수원", font=F(SANS,36,900), fill=BLUE); d.text((c2,262), "화성", font=F(SANS,36,900), fill=(220,110,30))
    wobbly(d, (L,318), (W-80,318), INK, w=3, seed=1)
    for i,(k,a,b) in enumerate(ROWS):
        y = 340 + i*96
        d.text((L,y+14), k, font=F(SANS,28,700), fill=(90,96,110))
        d.text((c1,y), a, font=F(SANS,48,900), fill=INK); d.text((c2,y), b, font=F(SANS,48,900), fill=INK)
        wobbly(d, (L,y+84), (W-80,y+84), (170,180,196), w=2, amp=1.2, seed=10+i)
    y3 = 340 + 3*96                                               # 「첫 골」 줄에 동그라미 두 개
    wobbly_ellipse(d, (c1-24, y3-14, c1+120, y3+76), RED, w=5, seed=3)
    wobbly_ellipse(d, (c2-24, y3-14, c2+250, y3+76), RED, w=5, seed=4)
    wobbly(d, (c1+124, y3+30), (c2-30, y3+30), RED, w=4, amp=2.2, seed=5)
    d.text((c1+150, y3-34), "같은 상대인데", font=F(SANS,26,900), fill=RED)
    yb = 340 + len(ROWS)*96 + 30
    d.text((L, yb), "→ 10월 18일엔 누가 먼저 뚫을까?", font=F(SANS,44,900), fill=RED)
    d.text((L,H-60), "기록: 다음 스포츠 · 득점 시각: K리그 공식 기록 · 직접 만든 이미지", font=F(SANS,20,400), fill=(110,116,130))
    im.save(os.path.join(HERE, "C_전술노트형.png"))

if __name__ == "__main__":
    style_a(); style_b(); style_c(); print("ok")
