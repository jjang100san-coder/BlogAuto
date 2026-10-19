# -*- coding: utf-8 -*-
"""수원삼성 3-2 화성FC 후기 카드 — B 양식 첫 글 (축구 지침 6-0, 2026-10-18).
01 썸네일(AI 배경 + 팀 색 면) · 02 르본 네임카드 · 03 전술판(21분 왼쪽 / 59분 세트피스, 컨펌 대기)
04 파울 카드 · 05 교체 뒤 실점(안산전 vs 화성전) · 06 프리뷰 채점."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from football_cards_base import *
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "images"); os.makedirs(IMG, exist_ok=True)
out = lambda n: os.path.join(IMG, n)
SW, SWR, HW = TEAM["수원삼성"], TEAM["수원삼성_적"], TEAM["화성FC"]


# ------------------------------------------------ 01 썸네일 — AI 배경 위에 팀 색 면(반투명)
def thumb():
    S = 1080; bg = Image.open(os.path.join(HERE, "ai", "bg_rain.png")).convert("RGB").resize((S, S))
    im = bg.convert("RGBA")
    ov = Image.new("RGBA", (S, S), (0,0,0,0)); od = ImageDraw.Draw(ov)
    od.polygon([(0,0),(S*0.56,0),(S*0.44,S),(0,S)], fill=SW + (178,)); od.polygon([(S*0.56,0),(S,0),(S,S),(S*0.44,S)], fill=HW + (178,))
    od.rectangle([0,0,S,190], fill=(0,0,0,150)); od.rectangle([0,S-230,S,S], fill=(0,0,0,175))
    im = Image.alpha_composite(im, ov).convert("RGB"); d = ImageDraw.Draw(im)
    d.text((60,52), "K리그2 29R · 10월 18일 · 폭우 속 수원월드컵", font=FB(30,900), fill=(255,255,255))
    d.text((60,104), "수원삼성 3-2 화성FC", font=FB(44,900), fill=YEL)
    def big(x, num, unit, label, right):
        fn, fu = FB(230,900), FB(70,900); wn = d.textlength(num, font=fn); wu = d.textlength(unit, font=fu)
        x0 = x - (wn + wu + 8) if right else x
        d.text((x0,250), num, font=fn, fill=(255,255,255)); d.text((x0+wn+8,390), unit, font=fu, fill=(255,255,255))
        lw = d.textlength(label, font=FB(34,900)); d.text((x-lw if right else x0, 540), label, font=FB(34,900), fill=(255,255,255))
    big(70, "3", "골", "전반 수원삼성", False); big(S-70, "2", "골", "후반 화성FC", True)
    y = 650
    for k, a, b in (("전반", "3", "0"), ("후반", "0", "2")):
        d.text((70,y), a, font=FB(40,900), fill=(255,255,255))
        kw = d.textlength(k, font=FB(26,700)); d.text(((S-kw)/2, y+10), k, font=FB(26,700), fill=(255,255,255))
        bw = d.textlength(b, font=FB(40,900)); d.text((S-70-bw, y), b, font=FB(40,900), fill=(255,255,255))
        d.line([70,y+62,S-70,y+62], fill=(255,255,255), width=1); y += 80
    d.text((60,S-190), "3-0은 왜 3-2가 됐을까?", font=FB(50,900), fill=YEL)
    d.text((60,S-58), "기록: K리그 공식 · 배경은 AI 생성 이미지(실제 경기 장면 아님) · 직접 만든 이미지", font=FB(20,400), fill=(220,220,220))
    im.save(out("01_thumb.png"))


# ------------------------------------------------ 02 르본 네임카드
def lebon():
    namecard_b(out("02_lebon.png"), SW, SWR, "K리그2 29R · 오늘의 왼쪽", "21", "분", "르본", "수원삼성 #8 · 왼쪽 미드필더",
               [("왼쪽을 허문 왼발 크로스", "2-0"), ("교체 아웃", "63분")],
               "벌어진 간격, 그 사이를 노렸다",
               "기록: K리그 공식 · 장면: 중계 해설·기사 묘사 · 직접 만든 이미지")


# ------------------------------------------------ 03 전술판 — 21분 르본의 왼쪽 / 59분 화성 코너킥
def board():
    tb = TacticsBoard("왼쪽을 연 르본, 가까운 쪽을 판 화성", "21분 자책골과 59분 만회골 · 위쪽이 공격하는 쪽의 상대 골문")
    A, B = tb.A, tb.B
    # A — 수원 공격(위쪽 = 화성 골문). 사용자 확인(10/19): 이상민·르본은 더 높이, 르본을 막던 화성 수비가 넘어지며(반칙 주장) 공간이 났다
    tb.pitch(A, "21분 2-0", "르본의 왼쪽")
    tb.hatch(A, .10, .09, .28, .27)
    for x, y in ((.40,.12), (.53,.10), (.66,.12), (.50,.40), (.68,.40), (.90,.22)): tb.player(A, x, y, HW)
    tb.player(A, .22, .25, HW)                                   # 르본을 막다 넘어진 화성 수비
    tb.player(A, .47, .22, SW); tb.player(A, .58, .19, SW)      # 강현묵·루이스
    tb.run(A, (.20,.50), (.25,.41), SW)                          # 이상민 높이 전진
    tb.ball(A, [(.25,.37), (.10,.31)])                           # 이상민 → 르본
    tb.run(A, (.09,.28), (.23,.13), SW)                          # 르본 넘어진 자리로 치고 들어감
    tb.ball(A, [(.25,.11), (.38,.04), (.52,.09)])               # 왼발 크로스 → 화성 수비 머리
    tb.player(A, .26, .38, SW); tb.player(A, .08, .30, SW)
    tb.name(A, .08, .36, "르본", SW); tb.name(A, .26, .44, "이상민", SW)
    tb.name(A, .31, .245, "넘어짐", HW, size=14)
    tb.name(A, .66, .05, "화성 수비 머리 → 자책골", HW, size=15)
    tb.callout(A, .41, .30, "수비가 넘어진 자리")
    # B — 화성 공격(위쪽 = 수원 골문). 사용자 확인(10/19): 코너킥은 먼 쪽 페트로프에게 길게 → 페트로프가 머리로 가까운 쪽 빈 공간에 찔러 줌 → 보이노비치 헤더
    tb.pitch(B, "59분 3-1", "화성의 코너킥")
    tb.hatch(B, .27, .0, .45, .12)
    for x, y in ((.58,.17), (.16,.25), (.52,.30), (.68,.23), (.82,.15)): tb.player(B, x, y, SW)   # 사용자 확인: 수원 수비는 먼 쪽 공을 따라 앞으로 나와 있었다
    tb.player(B, .53, .045, SW)                                  # 수원 골키퍼
    tb.player(B, .56, .215, HW); tb.player(B, .74, .25, HW)
    tb.ball(B, [(.03,.03), (.35,.21), (.65,.105)])              # 플라나 왼쪽 코너킥 → 먼 쪽 길게
    tb.ball(B, [(.65,.10), (.37,.05)])                           # 페트로프 머리로 가까운 쪽 빈 곳에
    tb.run(B, (.41,.21), (.35,.085), HW)                          # 보이노비치 가까운 쪽 빈 공간 안쪽으로
    tb.ball(B, [(.35,.04), (.44,.006)], w=3, head=11)            # 보이노비치 헤더
    tb.player(B, .67, .10, HW); tb.player(B, .34, .055, HW); tb.player(B, .03, .025, HW)
    tb.name(B, .82, .06, "페트로프", HW); tb.name(B, .33, .245, "보이노비치", HW)
    tb.name(B, .08, .12, "플라나", HW)
    tb.callout(B, .70, .36, "약속된 가까운 쪽")
    tb.finish(out("03_board.png"), legend=[(SW, "수원삼성"), (HW, "화성FC")],
              notes=["21분: 높이 올라온 이상민이 르본에게, 르본이 왼쪽을 치고 들어가 왼발 크로스",
                     "르본을 막던 화성 수비가 넘어졌고(화성은 반칙 주장) 그 자리가 비었다",
                     "59분: 먼 쪽 페트로프가 머리로 가까운 쪽 빈 곳에 → 보이노비치 헤더"],
              foot="왼쪽은 르본이 열고, 가까운 쪽은 화성이 팠어",
              source="장면: K리그 30분 하이라이트 중계·기사 묘사 · 선수 위치는 개념도 · 직접 만든 이미지")


# ------------------------------------------------ 04 파울 카드
def fouls():
    vs_card(out("04_fouls.png"), "몸싸움 · 기록으로 본 거친 경기", "파울 13개, 선수 경고 3장",
            (SW, "8", "개", "수원삼성 파울"), (HW, "13", "개", "화성FC 파울"),
            [("선수 경고", "1", "3"), ("코너킥", "2", "8")],
            "끊고 내려가는 반칙이 많았어",
            "파울·코너킥: 다음 스포츠 기록 · 경고: K리그 공식 · 직접 만든 이미지")


# ------------------------------------------------ 05 교체 뒤 실점 — 안산전 vs 화성전
def again():
    vs_card(out("05_again.png"), "두 경기 연속 · 3명 동시 교체 뒤", "교체 뒤 실점, 또 그 시간",
            (SW, "68", "분", "안산전 실점"), (SWR, "73", "분", "화성전 실점"),
            [("전반 스코어", "2-0", "3-0"), ("3명 동시 교체", "후반 20분쯤", "63분"), ("최종", "4-1", "3-2")],
            "또 그 시간이었어",
            "득점·화성전 교체: K리그 공식 · 안산전 교체: 다음 스포츠 · 직접 만든 이미지")


# ------------------------------------------------ 06 프리뷰 채점 (B 양식, 판정색은 채점 카드에서 그대로)
VERD = {"맞음": (46,160,90), "반반": (232,160,40), "빗나감": (214,64,64), "보류": (120,126,138), "기록": (120,126,138)}
def check():
    rows = [("수원이 전반에 먼저 넣나", "19분 선제골, 전반 3-0", "맞음"),
            ("앞 선수가 뒤로 뛰나", "골은 수비 앞 중거리와 왼쪽에서", "보류"),
            ("65~75분을 버티나", "63분 3명 교체, 73분 실점", "빗나감"),
            ("장민준 없는 화성의 높이", "결장은 맞았고, 높이는 세트피스 골로", "반반"),
            ("일류첸코의 친정 첫 경기", "74분 교체 투입, 슈팅 0개", "기록")]
    H = 300 + len(rows)*132 + 220; im = Image.new("RGB", (W, H), NIGHT); d = ImageDraw.Draw(im)
    d.polygon([(0,0),(420,0),(400,12),(0,12)], fill=SW); d.polygon([(420,0),(450,0),(430,12),(400,12)], fill=SWR)
    d.text((60,52), "프리뷰 채점 · 10월 15일에 적은 다섯 가지", font=FB(22,700), fill=YEL)
    d.text((60,86), "다섯 개 중 맞음 하나", font=FB(56,900), fill=INKB)
    d.text((60,166), "판정: 맞음 · 반반 · 빗나감 · 보류 · 기록", font=FB(24,400), fill=MUTB)
    y = 250
    for q, ev, v in rows:
        d.line([60, y-18, W-60, y-18], fill=(60,64,74), width=1)
        d.text((60, y), q, font=FB(36,900), fill=INKB); d.text((60, y+52), ev, font=FB(24,500), fill=MUTB)
        fo = FB(30,900); tw = d.textlength(v, font=fo); x1 = W-60; x0 = x1 - tw - 44
        d.rectangle([x0, y+6, x1, y+62], fill=VERD[v]); d.text((x0+22, y+12), v, font=fo, fill=(255,255,255))
        y += 132
    d.rectangle([0, H-170, W, H-82], fill=YEL); d.text((60, H-157), "먼저 넣었지만, 그 시간을 또 못 버텼어", font=FB(40,900), fill=NIGHT)
    d.text((60, H-56), "프리뷰(10/15) 관전 포인트 · 기록: K리그 공식 · 직접 만든 이미지", font=FB(18,400), fill=MUTB)
    im.save(out("06_check.png"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["thumb", "lebon", "board", "fouls", "again", "check"]
    for n in which: globals()[n]()
    print("ok", which)
