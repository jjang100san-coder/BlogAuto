# 정효볼 2편 — 원리 여섯 카드·전술 도해 (2026.10.12)
# 톤: 그래파이트 블루 + 라벤더, 청백적 띠(수원 트레이드마크) — 1편 웜차콜·3편 사파이어·리뷰 로열블루와 다르게
# 전술 도해는 모두 「개념도」 — 근거가 분석 채널 설명이라 축구 지침 6-2 ⑤ 제작자 컨펌 대상
import os, sys, shutil
sys.path.insert(0, r"C:\Users\user\Desktop\Blog\_1.컨텐츠\축구_컨텐츠")
from football_cards_base import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images"); os.makedirs(OUT, exist_ok=True)
def out(n): return os.path.join(OUT, n)

set_palette(BG=(18,24,32), PANEL=(30,40,54), PANEL2=(44,58,78),
            MUTED=(162,176,196), ACCENT=(190,170,255))
T_BLUE, T_WHITE, T_RED = (28,72,170), (245,245,245), (206,32,52)
SUW = KOR      # 수원 = 우리 팀 주황 (고정 의미색)
OPPC = OPP     # 상대 = 청록

def tricolor(d, y=0, h=8):
    d.rectangle([0,y,W,y+h], fill=T_BLUE); d.rectangle([0,y+h,W,y+2*h], fill=T_WHITE); d.rectangle([0,y+2*h,W,y+3*h], fill=T_RED)

def board(title, sub, lt, rt, lcol=AMBER, rcol=GREEN, H=1370):
    im, d = base(H, title, sub); tricolor(d)
    two_pitches(d, lt, rt, lcol, rcol)
    return im, d

def finish(im, d, H, notes, foot, source, legend_items):
    legend(d, 985, legend_items)
    numbered_notes(d, 1050, notes)
    bar(d, H-150, foot, size=31)
    src(d, H-38, source)

def P_(o, fx, fy, col, lab=None, r=12, below=True, size=16):
    player(d_ref[0], *pt(o,fx,fy), col, label=lab, r=r, below=below, size=size)
d_ref = [None]

# ------------------------------------------------ 01 썸네일 (리뷰 폴더에서 만든 것 복사)
def thumb():
    src_ = r"C:\Users\user\Desktop\Blog\_1.컨텐츠\축구_컨텐츠\261011_수원안산리뷰\suwon-ansan\images\jhb2_01_thumb.png"
    shutil.copy2(src_, out("01_thumb.png"))

# ------------------------------------------------ 02 원리 여섯 한눈에
def overview():
    rows = [("1", "끌어낸다", "상대가 나오게 만들고, 나온 자리 뒤를 쓴다"),
            ("2", "숫자를 먼저", "압박이 와도 잃지 않을 숫자를 뒤에 둔다"),
            ("3", "역할로 채운다", "한 명이 움직이면 빈자리는 다른 사람이"),
            ("4", "쏠리게 하고 반대로", "한쪽에 모아 놓고 먼 쪽에서 끝낸다"),
            ("5", "약속을 반복한다", "패턴보다 원리, 일주일 강도까지 정해 둔다"),
            ("6", "뺏기면 바로", "공이 안에 있을 땐 숨 쉴 생각 하지 마라")]
    top, rh, gap = 200, 110, 14
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "정효볼 원리 여섯", "이정효 인터뷰·분석 영상·수원 2026 경기에서 추린 것"); tricolor(d)
    y = top
    for i,(n,k,v) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL2"] if i%2==0 else P["PANEL"])
        d.ellipse([MARGIN+24,y+rh/2-26,MARGIN+76,y+rh/2+26], fill=P["ACCENT"])
        center(d, (MARGIN+50,y+rh/2), n, f(BLACK,28), P["BG"])
        left(d, (MARGIN+100,y+38), k, f(BLACK,32), P["CREAM"])
        left(d, (MARGIN+100,y+80), v, f(REG,24), P["MUTED"])
        y += rh+gap
    y += 16; bar(d, y, "「원리를 알면 막혀도 선수가 푼다」", size=31)
    src(d, y+82+40, "문구: 이정효 뽈리K 인터뷰(2026.2) 요지 · 직접 만든 이미지")
    im.save(out("02_overview.png"))

# ------------------------------------------------ 03 원리① 끌어낸다 — R19 부산 역전골
def p1_lure():
    H = 1370
    im, d = board("나온 자리 뒤가 길이 된다", "원리 ① 끌어낸다 · R19 부산전 역전골(7월) · 위쪽이 부산 골문 · 개념도",
                  "① 횡패스 → 윙포워드가 나온다", "② 그 등 뒤에서 받아 1대1", lcol=AMBER, rcol=GREEN)
    d_ref[0] = d
    for o, second in ((PA, False), (PB, True)):
        for x in (0.10,0.30,0.50,0.70,0.84): P_(o, x, 0.18, OPPC)              # 부산 5백
        for x in (0.38,0.62): P_(o, x, 0.36, OPPC)                               # 부산 2미들
        P_(o, 0.18, 0.54, OPPC); P_(o, 0.50, 0.56, OPPC)                          # 부산 앞 3명 중 둘
        wf = (0.70,0.75) if second else (0.82,0.54)                               # 부산 오른쪽 윙포워드(화면 오른쪽)
        P_(o, *wf, OPPC, r=14)
        P_(o, 0.38, 0.82, SUW); P_(o, 0.62, 0.82, SUW, r=14)                      # 센터백 둘
        P_(o, 0.10, 0.62, SUW); P_(o, 0.48, 0.66, SUW)                            # 왼쪽 풀백, 정호연
        P_(o, 0.84, 0.50 if second else 0.62, SUW, None, r=14)
        P_(o, 0.90, 0.30, SUW, None, r=14)
        P_(o, 0.50, 0.26, SUW, "일류첸코" if second else None, r=14, below=False)
        P_(o, 0.14, 0.32, SUW); P_(o, 0.34, 0.30, SUW)
    # ① 왼쪽: 센터백 횡패스(실선) + 윙포워드가 압박하러 나옴(점선)
    arrow(d, pt(PA,0.41,0.82), pt(PA,0.59,0.82), SUW)
    arrow(d, pt(PA,0.81,0.565), pt(PA,0.70,0.75), OPPC, dashed=True, head=11)
    tag(d, *pt(PA,0.84,0.86), "압박하러 나온다", size=16, fill=RED)
    # ② 오른쪽: 원터치로 등 뒤의 박현빈 → 이건희 → 크로스 → 일류첸코
    arrow(d, pt(PB,0.64,0.79), pt(PB,0.82,0.53), SUW)
    arrow(d, pt(PB,0.85,0.47), pt(PB,0.89,0.33), SUW)
    arrow(d, pt(PB,0.90,0.27), pt(PB,0.90,0.155), SUW, dashed=True, head=11)
    arrow(d, pt(PB,0.88,0.15), pt(PB,0.535,0.255), SUW)
    tag(d, *pt(PB,0.68,0.31), "이건희", size=16); d.line([*pt(PB,0.75,0.31), *pt(PB,0.865,0.30)], fill=P["CREAM"], width=2)
    zone(im, [PB[0]+PW*0.72, PB[1]+PH*0.44, PB[0]+PW*0.98, PB[1]+PH*0.62], GREEN, 50)
    d = ImageDraw.Draw(im)
    tag(d, *pt(PB,0.84,0.66), "윙포워드가 비운 자리", size=16, fill=GREEN)
    tag(d, *pt(PB,0.60,0.47), "박현빈", size=16); d.line([*pt(PB,0.67,0.475), *pt(PB,0.805,0.495)], fill=P["CREAM"], width=2)
    finish(im, d, H,
           ["센터백끼리 공을 옆으로 돌리자 부산 윙포워드가 압박하러 나왔다",
            "원터치 패스 한 번에 그 등 뒤의 박현빈 → 앞을 본 이건희가 1대1",
            "돌파 뒤 크로스, 일류첸코 역전골 — 끌려 나온 자리 뒤가 길이었다"],
           "끌려 나온 자리 뒤가 길이 된다",
           "장면: 축구 해석하기 R19 분석 · 기록: 다음 스포츠 · 개념도 · 직접 만든 이미지",
           [(SUW,"수원삼성"), (OPPC,"부산")])
    im.save(out("03_p1_lure.png"))

# ------------------------------------------------ 04 원리② 숫자를 먼저 — R1 서울E 빌드업
def p2_numbers():
    H = 1370
    im, d = board("뒤에 숫자를 먼저 놓는다", "원리 ② 숫자를 먼저 · 왼쪽 R1 서울E전 · 오른쪽 R3 전남전 · 위쪽이 상대 골문 · 개념도",
                  "① 골키퍼까지 일곱 명", "② 정호연이 내려오면 스리백", lcol=AMBER, rcol=GREEN)
    d_ref[0] = d
    # ① 왼쪽: 4-2 + 골키퍼 = 7 vs 서울E 압박 3 + 2
    for x,y in ((0.50,0.95),(0.34,0.85),(0.66,0.85),(0.10,0.74),(0.90,0.74),(0.40,0.64),(0.60,0.64)):
        P_(PA, x, y, SUW, r=13)
    for x,y in ((0.30,0.74),(0.50,0.76),(0.70,0.74),(0.40,0.54),(0.60,0.54)):
        P_(PA, x, y, OPPC, r=12)
    for x,y in ((0.20,0.40),(0.50,0.36),(0.80,0.40),(0.35,0.24),(0.65,0.24)): P_(PA, x, y, SUW, r=10)
    zone(im, [PA[0]+PW*0.04, PA[1]+PH*0.58, PA[0]+PW*0.96, PA[1]+PH*0.99], GREEN, 35)
    d = ImageDraw.Draw(im); d_ref[0] = d
    for x,y in ((0.50,0.95),(0.34,0.85),(0.66,0.85),(0.10,0.74),(0.90,0.74),(0.40,0.64),(0.60,0.64)):
        P_(PA, x, y, SUW, r=13)
    for x,y in ((0.30,0.74),(0.50,0.76),(0.70,0.74),(0.40,0.54),(0.60,0.54)):
        P_(PA, x, y, OPPC, r=12)
    tag(d, *pt(PA,0.50,0.46), "7 대 5", size=22, fill=GREEN)
    # ② 오른쪽: 정호연 하강 → 센터백 사이, 양 풀백은 위로, 홍정호 전진
    P_(PB, 0.50, 0.95, SUW, r=12)
    P_(PB, 0.26, 0.80, SUW, r=13); P_(PB, 0.74, 0.80, SUW, "홍정호", r=13)
    P_(PB, 0.50, 0.84, SUW, "정호연", r=14)
    arrow(d, pt(PB,0.50,0.64), pt(PB,0.50,0.80), SUW, dashed=True, head=11)
    P_(PB, 0.10, 0.56, SUW, r=13); P_(PB, 0.90, 0.56, SUW, r=13)
    arrow(d, pt(PB,0.10,0.72), pt(PB,0.10,0.59), SUW, dashed=True, head=10)
    arrow(d, pt(PB,0.90,0.72), pt(PB,0.90,0.59), SUW, dashed=True, head=10)
    arrow(d, pt(PB,0.74,0.77), pt(PB,0.74,0.66), SUW, dashed=True, head=10)
    # 서울E 압박 셋이 앞으로 끌려 나온다 → 그 뒤 중앙이 빈다 (사용자 지적 10/12)
    zone(im, [PB[0]+PW*0.24, PB[1]+PH*0.47, PB[0]+PW*0.42, PB[1]+PH*0.58], RED, 60)
    zone(im, [PB[0]+PW*0.52, PB[1]+PH*0.53, PB[0]+PW*0.68, PB[1]+PH*0.63], RED, 60)
    d = ImageDraw.Draw(im); d_ref[0] = d
    P_(PB, 0.36, 0.66, SUW, r=12)
    for (fx,fy),(tx,ty) in (((0.33,0.55),(0.29,0.655)),((0.60,0.60),(0.60,0.68)),((0.80,0.56),(0.81,0.64))):
        arrow(d, pt(PB,fx,fy), pt(PB,tx,ty), OPPC, w=3, dashed=True, head=9)
    for x,y in ((0.28,0.69),(0.60,0.71),(0.81,0.67)): P_(PB, x, y, OPPC, r=12)
    tag(d, *pt(PB,0.80,0.47), "끌려 나온 자리가 빈다", size=15, fill=RED)
    # 앞에 있던 선수가 중앙으로 내려와 그 공간을 점유
    arrow(d, pt(PB,0.50,0.36), pt(PB,0.49,0.47), SUW, dashed=True, head=11)
    P_(PB, 0.48, 0.505, SUW, r=13)
    tag(d, *pt(PB,0.26,0.41), "내려와 중앙을 차지", size=15, fill=GREEN)
    d.line([*pt(PB,0.36,0.43), *pt(PB,0.455,0.49)], fill=P["CREAM"], width=2)
    for x,y in ((0.20,0.34),(0.80,0.36),(0.35,0.20),(0.65,0.20)): P_(PB, x, y, SUW, r=10)
    tag(d, *pt(PB,0.50,0.09), "풀백은 높이, 센터백은 넓게", size=16)
    finish(im, d, H,
           ["4-2 대형에 골키퍼 김준홍까지 일곱 명이 빌드업 — 상대 압박보다 많다",
            "정호연이 센터백 사이로 내려오면 스리백, 올라가면 다시 포백",
            "상대가 압박하러 끌려 나오면 중앙이 비고, 앞 선수가 내려와 그 공간을 차지한다"],
           "압박이 와도 잃지 않을 숫자부터",
           "장면: 빅버드 게임이론 R1 · 스포츠조선 3/18(R3 전남) · 본인 육성 아님(분석 기준) · 개념도 · 직접 만든 이미지",
           [(SUW,"수원삼성"), (OPPC,"서울E · 전남")])
    im.save(out("04_p2_numbers.png"))

# ------------------------------------------------ 05 원리③ 역할 — R22 수원FC 연쇄
def p3_roles():
    H = 1370
    im, d = board("한 명이 움직이면, 빈자리는 다른 사람이", "원리 ③ 역할 · R22 수원FC전(8월) · 위쪽이 수원FC 골문 · 개념도",
                  "① 고승범이 내려가면 상대가 따라 나온다", "② 그 자리에 헤이스 → 정호연이 빈다", lcol=AMBER, rcol=GREEN)
    d_ref[0] = d
    for o, second in ((PA, False), (PB, True)):
        for x in (0.10,0.30,0.50,0.70,0.90): P_(o, x, 0.16, OPPC)                 # 수원FC 5백
        P_(o, 0.12, 0.36 if not second else 0.36, OPPC)                            # 측면
        P_(o, 0.84, 0.36, OPPC)
        gbc = (0.26,0.52) if second else (0.34,0.36)                               # 구본철: 따라 나옴
        P_(o, *gbc, OPPC, "구본철", r=14, below=second)
        ljw = (0.42,0.45) if second else (0.56,0.36)                               # 이재원: 헤이스를 따라감
        P_(o, *ljw, OPPC, None, r=14)
        P_(o, 0.52, 0.56, OPPC)                                                    # 원톱
        ggb = (0.22,0.64) if second else (0.36,0.56)
        P_(o, *ggb, SUW, "고승범", r=14, below=second)
        hs = (0.32,0.38) if second else (0.40,0.24)
        P_(o, *hs, SUW, None, r=14)
        P_(o, 0.62, 0.58, SUW, "정호연", r=15)
        P_(o, 0.10, 0.52, SUW); P_(o, 0.66, 0.26, SUW)
        P_(o, 0.36, 0.80, SUW)
        P_(o, 0.64, 0.80, SUW, "고종현" if second else None, r=14)                 # 오른쪽 센터백
        if not second: P_(o, 0.88, 0.70, SUW)                                       # 이건희(27, 오른쪽 풀백) — 아직 아래
    # ① 왼쪽
    arrow(d, pt(PA,0.35,0.59), pt(PA,0.24,0.62), SUW, dashed=True, head=11)
    arrow(d, pt(PA,0.34,0.39), pt(PA,0.32,0.47), OPPC, dashed=True, head=11)
    tag(d, *pt(PA,0.70,0.44), "이 자리가 빈다", size=16, fill=RED)
    d.line([*pt(PA,0.58,0.44), *pt(PA,0.40,0.42)], fill=P["CREAM"], width=2)
    # ② 오른쪽
    arrow(d, pt(PB,0.40,0.27), pt(PB,0.34,0.35), SUW, dashed=True, head=11)
    arrow(d, pt(PB,0.55,0.38), pt(PB,0.45,0.43), OPPC, dashed=True, head=11)
    tag(d, *pt(PB,0.52,0.31), "헤이스", size=16); d.line([*pt(PB,0.455,0.32), *pt(PB,0.355,0.37)], fill=P["CREAM"], width=2)
    tag(d, *pt(PB,0.60,0.46), "이재원", size=16); d.line([*pt(PB,0.535,0.455), *pt(PB,0.455,0.45)], fill=P["CREAM"], width=2)
    zone(im, [PB[0]+PW*0.52, PB[1]+PH*0.50, PB[0]+PW*0.74, PB[1]+PH*0.66], GREEN, 55)
    d = ImageDraw.Draw(im)
    P_(PB, 0.62, 0.58, SUW, "정호연", r=15)
    tag(d, *pt(PB,0.63,0.70), "정호연이 중앙을 차지", size=15, fill=GREEN)
    # 이건희(27)가 빈 오른쪽으로 올라가고, 고종현이 전진 패스 (사용자 지적 10/12)
    arrow(d, pt(PB,0.88,0.72), pt(PB,0.88,0.53), SUW, dashed=True, head=11)
    P_(PB, 0.88, 0.50, SUW, r=14)
    tag(d, *pt(PB,0.885,0.437), "이건희", size=16)
    arrow(d, pt(PB,0.665,0.78), pt(PB,0.855,0.525), SUW)

    finish(im, d, H,
           ["고승범이 왼쪽으로 내려가자 구본철이 따라 나왔다",
            "구본철이 비운 자리에 헤이스가 내려오고, 이재원이 헤이스를 따라갔다",
            "정호연이 비어 중앙을 차지하고, 이건희가 빈 오른쪽으로 → 고종현 전진 패스"],
           "한 명이 움직이면, 빈자리는 다른 사람이",
           "장면: 빅버드 게임이론 R22 분석 · 개념도 · 직접 만든 이미지",
           [(SUW,"수원삼성"), (OPPC,"수원FC")])
    im.save(out("05_p3_roles.png"))

# ------------------------------------------------ 06 원리④ 쏠림 → 반대 — R5 용인 페신 결승골
def p4_switch():
    H = 1370
    im, d = board("한쪽에 모으고, 먼 쪽에서 끝낸다", "원리 ④ 쏠림 → 반대 · R5 용인전 결승골(3월) · 위쪽이 용인 골문 · 개념도",
                  "① 풀백이 안으로 → 측면이 열린다", "② 역발 크로스 → 먼 쪽", lcol=AMBER, rcol=GREEN)
    d_ref[0] = d
    for o, second in ((PA, False), (PB, True)):
        backs = (0.06,0.17,0.28,0.39,0.52) if second else (0.10,0.26,0.42,0.58,0.76)   # 오른쪽 = 공 쪽으로 더 쏠림(사용자 지적 10/12)
        for x in backs: P_(o, x, 0.16, OPPC)
        mids = (0.27,0.40,0.54,0.70) if second else (0.26,0.46,0.64,0.84)
        P_(o, mids[0], 0.36, OPPC, r=13); P_(o, mids[1], 0.38, OPPC); P_(o, mids[2], 0.38, OPPC); P_(o, mids[3], 0.36, OPPC)
        P_(o, 0.30, 0.46, SUW, r=13)                                                # 왼쪽 풀백 — 안으로
        P_(o, 0.08, 0.30, SUW, "브루노 실바" if second else None, r=14, below=True)
        P_(o, 0.46, 0.33, SUW); P_(o, 0.60, 0.56, SUW); P_(o, 0.40, 0.60, SUW)
        P_(o, 0.90, 0.22, SUW, "페신" if second else None, r=15, below=True)
        P_(o, 0.36, 0.80, SUW); P_(o, 0.64, 0.80, SUW); P_(o, 0.90, 0.56, SUW)
    # ① 왼쪽: 풀백이 안으로 → 상대 윙포워드도 안으로
    arrow(d, pt(PA,0.18,0.52), pt(PA,0.28,0.48), SUW, dashed=True, head=10)
    arrow(d, pt(PA,0.18,0.38), pt(PA,0.24,0.37), OPPC, dashed=True, head=10)
    zone(im, [PA[0]+PW*0.01, PA[1]+PH*0.22, PA[0]+PW*0.17, PA[1]+PH*0.44], GREEN, 55)
    d = ImageDraw.Draw(im); d_ref[0] = d
    P_(PA, 0.08, 0.30, SUW, r=14)
    tag(d, *pt(PA,0.22,0.08), "측면이 열린다", size=16, fill=GREEN)
    tag(d, *pt(PA,0.88,0.08), "먼 쪽도 비어 있다", size=16, fill=GREEN)
    # ② 오른쪽: 수비가 공 쪽으로 쏠린 방향(점선) + 역발 크로스 → 먼 쪽 페신
    for x0,x1 in ((0.76,0.56),(0.58,0.43),(0.42,0.32)):
        arrow(d, pt(PB,x0,0.105), pt(PB,x1,0.105), OPPC, w=3, dashed=True, head=9)
    zone(im, [PB[0]+PW*0.60, PB[1]+PH*0.03, PB[0]+PW*0.79, PB[1]+PH*0.28], RED, 45)
    d = ImageDraw.Draw(im); d_ref[0] = d
    arrow(d, pt(PB,0.11,0.29), pt(PB,0.87,0.21), SUW)
    zone(im, [PB[0]+PW*0.80, PB[1]+PH*0.10, PB[0]+PW*0.99, PB[1]+PH*0.32], GREEN, 55)
    d = ImageDraw.Draw(im); d_ref[0] = d
    P_(PB, 0.90, 0.22, SUW, r=15)
    tag(d, *pt(PB,0.50,0.92), "수비 다섯이 공 쪽으로 쏠렸다", size=16, fill=RED)
    tag(d, *pt(PB,0.70,0.31), "빈 공간", size=15, fill=RED)
    finish(im, d, H,
           ["왼쪽 풀백이 안으로 들어가자 상대 윙포워드도 안으로 따라왔다",
            "열린 측면에서 브루노 실바가 역발 오른발로 먼 쪽 포스트에 크로스",
            "수비가 공 쪽으로 쏠린 사이 먼 쪽 페신이 결승골 (전반 3분)"],
           "한쪽에 모으고, 먼 쪽에서 끝낸다",
           "장면: 박종윤(축구) R1~R5 분석 · 풋볼리스트 3/28 · 기록: 다음 스포츠 · 개념도 · 직접 만든 이미지",
           [(SUW,"수원삼성"), (OPPC,"용인")])
    im.save(out("06_p4_switch.png"))

# ------------------------------------------------ 07 원리⑤ 약속 — 경기 주간 훈련 강도
def p5_week():
    rows = [("경기 5일 전", 60, "강도 60%"), ("경기 4일 전", 70, "강도 70%"), ("경기 3일 전", 90, "강도 90% — 가장 세게"),
            ("경기 2일 전", 50, "50% — 회복"), ("경기 하루 전", 0, "세트피스 · 전술 설명")]
    top, rh, gap = 210, 100, 16
    H = top + len(rows)*(rh+gap) + 130 + 30 + 82 + 80
    im, d = base(H, "약속은 일주일 단위로 짠다", "원리 ⑤ 약속과 반복 · 이정효가 말한 수원의 경기 주간 · 화~토 훈련 전 미팅"); tricolor(d)
    y = top; x0, x1 = 330, W-MARGIN-20
    for k,v,lab in rows:
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL"])
        left(d, (MARGIN+28,y+rh/2), k, f(BOLD,28), P["CREAM"])
        if v:
            d.rounded_rectangle([x0,y+28,x0+(x1-x0)*v/100,y+rh-28], radius=10, fill=P["ACCENT"] if v<90 else (232,108,100))
            left(d, (x0+(x1-x0)*v/100+14 if v<75 else x0+16,y+rh/2), lab, f(BLACK,26), P["CREAM"] if v<75 else P["BG"])
        else:
            left(d, (x0,y+rh/2), lab, f(BLACK,26), P["ACCENT"])
        y += rh+gap
    d.rounded_rectangle([MARGIN,y,W-MARGIN,y+120], radius=16, fill=P["PANEL2"])
    center(d, (W/2,y+40), "지난해 말엔 강도를 더 올렸다", f(BOLD,26), P["MUTED"])
    center(d, (W/2,y+84), "50m를 8초에 열 번보다, 7초에 다섯 번", f(BLACK,32), P["CREAM"])
    y += 120 + 30
    bar(d, y, "「원리를 알면 막혀도 선수가 푼다」", size=31)
    src(d, y+82+40, "이정효 뽈리K 인터뷰 ①(2026.2) 16:55~18:16 · 자막·whisper 두 판독 일치 · 직접 만든 이미지")
    im.save(out("07_p5_week.png"))

# ------------------------------------------------ 08 원리⑥ 수비 — R16 성남 역압박
def p6_press():
    H = 1370
    im, d = board("뺏긴 자리에서 바로, 다시", "원리 ⑥ 수비 · R16 성남전(7월) · 위쪽이 성남 골문 · 개념도",
                  "① 상대 진영에서 뺏기면 — 좁히고 길목", "② 최전방에서 뺏기면 — 사람에 붙는다", lcol=AMBER, rcol=GREEN)
    d_ref[0] = d
    # ① 상대 진영 왼쪽에서 뺏김 (사용자 지적 10/12) — 가까운 둘 압박, 강성진 길목, 한 풀백은 올라가 있고
    #    높이 있던 수비 셋이 바깥에서 안쪽으로 간격을 좁히며 같이 내려와 중앙을 내주지 않는다
    zone(im, [PA[0]+PW*0.26, PA[1]+PH*0.56, PA[0]+PW*0.80, PA[1]+PH*0.72], GREEN, 45)
    d = ImageDraw.Draw(im); d_ref[0] = d
    for x,y in ((0.30,0.10),(0.50,0.08),(0.70,0.10),(0.60,0.30),(0.88,0.26)): P_(PA, x, y, OPPC, r=11)
    P_(PA, 0.12, 0.25, OPPC, r=15)
    tag(d, *pt(PA,0.13,0.06), "공 뺏은 선수", size=15)
    d.line([*pt(PA,0.12,0.08), *pt(PA,0.12,0.225)], fill=P["CREAM"], width=2)
    P_(PA, 0.24, 0.18, SUW, r=13); P_(PA, 0.20, 0.36, SUW, r=13)                     # 가까운 둘이 붙는다
    arrow(d, pt(PA,0.22,0.195), pt(PA,0.155,0.23), SUW, dashed=True, head=10)
    arrow(d, pt(PA,0.185,0.34), pt(PA,0.14,0.285), SUW, dashed=True, head=10)
    d.line([*pt(PA,0.15,0.27), *pt(PA,0.325,0.335)], fill=RED, width=3)               # 중앙으로 가는 길 — 강성진 앞에서 막힘
    P_(PA, 0.36, 0.35, SUW, r=14)                                                     # 강성진: 길목
    tag(d, *pt(PA,0.42,0.27), "강성진 · 길목 차단", size=15, fill=GREEN)
    d.line([*pt(PA,0.40,0.29), *pt(PA,0.37,0.325)], fill=P["CREAM"], width=2)
    P_(PA, 0.06, 0.44, SUW, r=13)                                                     # 공격에 올라간 풀백
    tag(d, *pt(PA,0.11,0.53), "올라간 풀백", size=14)
    d.line([*pt(PA,0.08,0.505), *pt(PA,0.065,0.465)], fill=P["CREAM"], width=2)
    P_(PA, 0.56, 0.38, SUW, r=12); P_(PA, 0.74, 0.20, SUW, r=12)                     # 정호연·앞쪽 한 명
    for (fx,fy),(tx,ty) in (((0.30,0.48),(0.40,0.61)),((0.62,0.47),(0.56,0.62)),((0.92,0.48),(0.72,0.61))):
        P_(PA, fx, fy, SUW, r=12)
        arrow(d, pt(PA,fx+(0.02 if tx>fx else -0.02),fy+0.02), pt(PA,tx,ty), SUW, dashed=True, head=10)
    tag(d, *pt(PA,0.53,0.78), "수비 셋이 좁히며 같이 내려와 중앙을 차지", size=15, fill=GREEN)
    P_(PA, 0.50, 0.95, SUW, r=11)
    # ② 최전방에서 뺏김 — 주위가 사람에 붙어 롱볼만 남긴다
    for x in (0.14,0.38,0.62,0.86): P_(PB, x, 0.18, OPPC, r=12)                      # 성남 뒷줄
    for x in (0.18,0.34,0.58,0.82): P_(PB, x, 0.25, SUW, r=12)                       # 수원: 가까운 상대에 붙음
    for x0,x1 in ((0.18,0.155),(0.34,0.365),(0.58,0.605),(0.82,0.845)):
        arrow(d, pt(PB,x0,0.235), pt(PB,x1,0.205), SUW, w=3, dashed=True, head=8)
    arrow(d, pt(PB,0.40,0.20), pt(PB,0.53,0.60), OPPC, w=3)                          # 남는 건 롱볼
    tag(d, *pt(PB,0.74,0.42), "롱볼밖에 없다", size=16, fill=GREEN)
    for x,y in ((0.36,0.70),(0.64,0.70),(0.50,0.64)): P_(PB, x, y, SUW, r=12)
    tag(d, *pt(PB,0.50,0.84), "뒤에서 받아 다시 시작", size=16)
    finish(im, d, H,
           ["상대 진영에서 뺏기면 가까운 둘이 붙고, 강성진은 중앙으로 가는 길목을 막는다",
            "높이 있던 수비 셋은 바깥에서 안쪽으로 좁히며 내려와 중앙을 내주지 않는다",
            "최전방에서 뺏기면 주위가 사람에 붙어 롱볼만 남긴다"],
           "뺏긴 자리에서 바로, 숨 쉴 틈 없이",
           "장면: 빅버드 게임이론 R16 카운터프레싱 분석 · 개념도 · 직접 만든 이미지",
           [(SUW,"수원삼성"), (OPPC,"성남")])
    im.save(out("08_p6_press.png"))

# ------------------------------------------------ 09 엇갈림 — 같은 말, 다른 평가
def split_card():
    rows = [("끌어내기", "상대가 안 나오면 성립 안 한다 — 칼럼 「유인 축구가 성립하기 어려운 환경」", "2월 「대놓고 비기려고 할 것, 당연하다」 → 여름 루이스·두비츠카스"),
            ("뒷공간", "라인을 올리면 역습을 맞는다 — 4월 김포·6월 화성", "「몇몇 경기는 골 먹는다」 「역습 대비가 제일 골머리」 → 뒤에 숫자"),
            ("시간", "60분 넘어가면·동점 뒤·교체 뒤 약속이 흔들린다", "4월 「60분 이후에 급해진다」 · 8월 「폭탄 돌리기」 질타"),
            ("머리", "알아야 할 게 많아 느리다 — 4월 「막히면 풀지 못한다」", "「저 때문에 성장이 늦는 건가」(2024) · 「생각보다 좀 많이 더디고」(2026.2)"),
            ("사람", "마지막 1대1은 선수 몫 — 광주 2025 아사니 빠지자 전반 슈팅 0", "「스쿼드상 한계가 조금씩 나오지 않나」 → 페신·브루노 실바")]
    top, rh, gap = 230, 150, 16
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "정효볼 단점 다섯", "왼쪽 = 약점·비판 / 오른쪽 = 이정효가 한 말 → 대답"); tricolor(d)
    mid = W/2
    center(d, (MARGIN+(mid-MARGIN)/2, 190), "약점 · 비판", f(BLACK,26), RED)
    center(d, (mid+(W-MARGIN-mid)/2, 190), "본인 · 대답", f(BLACK,26), GREEN)
    y = top
    for k,a,b in rows:
        d.rounded_rectangle([MARGIN,y,mid-8,y+rh], radius=14, fill=P["PANEL"])
        d.rounded_rectangle([mid+8,y,W-MARGIN,y+rh], radius=14, fill=P["PANEL2"])
        left(d, (MARGIN+22,y+32), k, f(BLACK,26), P["ACCENT"])
        for i,ln in enumerate(wrap(d, a, f(REG,23), mid-8-MARGIN-44)[:3]): left(d, (MARGIN+22,y+72+i*32), ln, f(REG,23), P["CREAM"])
        for i,ln in enumerate(wrap(d, b, f(REG,23), W-MARGIN-mid-8-44)[:4]): left(d, (mid+30,y+34+i*32), ln, f(REG,23), P["CREAM"])
        y += rh+gap
    y += 14; bar(d, y, "다섯 다 본인도 인정했다", size=31)
    src(d, y+82+40, "칼럼·기사: 발리볼코리아·스포츠조선·엑스포츠뉴스·풋볼리스트·더팩트 / 발언: 뽈리K 2026.2 · 직접 만든 이미지")
    im.save(out("09_split.png"))

# ------------------------------------------------ 10 선수가 본 정효볼 — 광주 ↔ 수원
def players_card():
    rows = [("처음엔 누구나 어렵다", "이민기(광주 2023) 처음 왔을 땐 그냥 걷어냈을 거라고", "강성진 「몸만 빠르다고 되는 게 아니라 머리도 빨라야」"),
            ("빈자리를 채운다", "이민기 안으로 들어갈 때와 벌릴 때를 상황 보고 정한다", "정호연 「누가 어디를 가든 그 역할을 소화해야」"),
            ("쉴 틈이 없다", "이민기 맨마킹이 붙으면 뒤에서 받치고, 뺏기면 바로 압박", "강성진 「1초도 몰입을 안 하면 안 된다」")]
    top, rh, gap = 230, 170, 16
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "선수가 본 정효볼", "광주 2023 이민기 ↔ 수원 2026 정호연·강성진"); tricolor(d)
    mid = W/2
    center(d, (MARGIN+(mid-MARGIN)/2, 190), "광주", f(BLACK,26), P["MUTED"])
    center(d, (mid+(W-MARGIN-mid)/2, 190), "수원", f(BLACK,26), P["ACCENT"])
    y = top
    for k,a,b in rows:
        d.rounded_rectangle([MARGIN,y,mid-8,y+rh], radius=14, fill=P["PANEL"])
        d.rounded_rectangle([mid+8,y,W-MARGIN,y+rh], radius=14, fill=P["PANEL2"])
        left(d, (MARGIN+22,y+32), k, f(BLACK,25), P["ACCENT"])
        for i,ln in enumerate(wrap(d, a, f(REG,23), mid-8-MARGIN-44)[:3]): left(d, (MARGIN+22,y+74+i*32), ln, f(REG,23), P["CREAM"])
        for i,ln in enumerate(wrap(d, b, f(REG,23), W-MARGIN-mid-8-44)[:4]): left(d, (mid+30,y+50+i*32), ln, f(REG,23), P["CREAM"])
        y += rh+gap
    y += 14; bar(d, y, "3년이 지나도 선수들이 하는 말은 같다", size=31)
    src(d, y+82+40, "이민기: 문도그 선수초대석(2023) / 정호연·강성진: 뽈리K 미야자키 인터뷰(2026.2) 요지 · 직접 만든 이미지")
    im.save(out("10_players.png"))

if __name__ == "__main__":
    thumb(); overview(); p1_lure(); p2_numbers(); p3_roles(); p4_switch(); p5_week(); p6_press(); split_card(); players_card()
    print(sorted(os.listdir(OUT)))
