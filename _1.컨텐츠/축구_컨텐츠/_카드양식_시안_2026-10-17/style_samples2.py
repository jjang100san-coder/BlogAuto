# -*- coding: utf-8 -*-
"""시안 2차 (2026-10-17) — 밝은 바탕 A·C 가 「촌스럽다」(본인) → 어두운 바탕 유지, 구조만 바꾼다.
원인: 밝은 바탕에서 원색·900 굵기가 그대로 드러남, 장식(괘선·모눈·형광펜)이 흉내처럼 보임.
D  어두운 편집형 — 둥근 상자 없음, 가는 선·왼쪽 정렬, 숫자는 크게·굵기 300~600, 강조색 하나(골드), 팀 색은 작은 표시만
B' 매치데이 다듬기 — 팀 색 채도 낮춤(남색·적갈색 쪽), 두 숫자만 크게, 나머지는 가늘게
"""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
SANS = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
def F(size, w=400):
    fo = ImageFont.truetype(SANS, size); fo.set_variation_by_axes([w]); return fo
def tw(d, t, fo): b = d.textbbox((0,0), t, font=fo); return b[2]-b[0]
W = 1080
BG, INK, MUT, LINE, GOLD = (17,19,24), (236,233,226), (128,132,142), (52,56,66), (214,180,106)
SUW, HWA = (92,128,214), (214,128,72)          # 채도 낮춘 팀 색

def style_d():
    H = 1180; im = Image.new("RGB", (W,H), BG); d = ImageDraw.Draw(im)
    L, R = 90, W-90
    d.text((L,86), "K리그2 29R 프리뷰", font=F(22,500), fill=GOLD)
    d.text((L,128), "같은 안산,", font=F(64,700), fill=INK)
    d.text((L,206), "두 번의 승리", font=F(64,700), fill=INK)
    d.text((L,300), "수원은 공을 쥐고 일찍, 화성은 공을 내주고 늦게 이겼다", font=F(26,300), fill=MUT)
    # 큰 숫자 두 개 — 이 카드의 핵심
    y = 400
    d.line([L,y,R,y], fill=LINE, width=1)
    cx = (L, 590)
    for (x, team, col, num, sub) in ((cx[0],"수원삼성",SUW,"2","분 · 첫 골"),(cx[1],"화성FC",HWA,"66","분 · 첫 골 (PK)")):
        d.rectangle([x,y+40,x+10,y+50], fill=col)
        d.text((x+22,y+30), team, font=F(26,600), fill=INK)
        d.text((x-6,y+70), num, font=F(170,300), fill=INK)
        d.text((x+tw(d,num,F(170,300))+6,y+190), sub, font=F(26,400), fill=MUT)
    y = 690
    d.line([L,y,R,y], fill=LINE, width=1)
    rows = [("점유","60%","44%"),("슈팅(유효)","17(10)","7(4)"),("마지막 골","61분","96분"),("실점","68분","0")]
    for i,(k,a,b) in enumerate(rows):
        yy = y + 24 + i*66
        d.text((L,yy+6), k, font=F(24,400), fill=MUT)
        d.text((330,yy), a, font=F(36,500), fill=INK); d.text((590+22,yy), b, font=F(36,500), fill=INK)
        d.line([L,yy+58,R,yy+58], fill=(32,35,42), width=1)
    yb = y + 24 + len(rows)*66 + 34
    d.text((L,yb), "10월 18일, 누가 먼저 뚫을까", font=F(38,700), fill=GOLD)
    d.text((L,H-60), "기록: 다음 스포츠 · 득점 시각: K리그 공식 기록 · 직접 만든 이미지", font=F(19,300), fill=(96,100,110))
    im.save(os.path.join(HERE, "D_어두운편집형.png"))

def style_b2():
    H = 1180; NAVY, RUST = (22,40,86), (120,58,30)
    im = Image.new("RGB", (W,H), BG); d = ImageDraw.Draw(im)
    d.polygon([(0,0),(W*0.55,0),(W*0.45,H),(0,H)], fill=NAVY)
    d.polygon([(W*0.55,0),(W,0),(W,H),(W*0.45,H)], fill=RUST)
    ov = Image.new("RGBA", (W,H), (0,0,0,0)); od = ImageDraw.Draw(ov)
    for yy in range(H):                                    # 위·아래로 갈수록 어둡게(평평한 색면 피함)
        t = abs(yy - H*0.42) / (H*0.58); od.line([0,yy,W,yy], fill=(8,10,14,int(170*min(1,t**1.4))))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im)
    d.text((70,70), "VS 안산그리너스", font=F(24,500), fill=(200,204,214))
    d.text((70,108), "같은 상대, 다른 승리", font=F(46,700), fill=INK)
    for x, num, lab, right in ((70,"2","수원삼성 첫 골",False),(W-70,"66","화성FC 첫 골",True)):
        fn = F(250,300); fu = F(56,400)
        wn = tw(d,num,fn); wu = tw(d,"분",fu)
        x0 = x-(wn+wu+10) if right else x
        d.text((x0,250), num, font=fn, fill=INK); d.text((x0+wn+10,420), "분", font=fu, fill=INK)
        lw = tw(d,lab,F(28,600)); d.text((x-lw if right else x, 560), lab, font=F(28,600), fill=INK)
    rows = [("점유","60%","44%"),("슈팅(유효)","17(10)","7(4)"),("마지막 골","61분","96분"),("실점","68분","0")]
    y = 660
    for k,a,b in rows:
        d.text((70,y), a, font=F(34,500), fill=INK)
        kw = tw(d,k,F(22,400)); d.text(((W-kw)/2,y+8), k, font=F(22,400), fill=(190,194,204))
        bw = tw(d,b,F(34,500)); d.text((W-70-bw,y), b, font=F(34,500), fill=INK)
        d.line([70,y+56,W-70,y+56], fill=(255,255,255,), width=1); y += 72
    d.text((70,H-170), "10월 18일, 누가 먼저 뚫을까", font=F(42,700), fill=GOLD)
    d.text((70,H-58), "기록: 다음 스포츠 · 득점 시각: K리그 공식 기록 · 직접 만든 이미지", font=F(19,300), fill=(170,174,184))
    im.save(os.path.join(HERE, "B2_매치데이_다듬기.png"))

if __name__ == "__main__":
    style_d(); style_b2(); print("ok")
