# 수원 4-1 안산 리뷰 + 정효볼 2편 썸네일 카드 (2026.10.11)
# 톤: 블루윙즈 로열 블루 + 청백적 띠 (3편 사파이어+스카이와 다르게, 짝 글 규칙)
# 썸네일 = 카드(축구 분야 예외) + AI 배경(마스터 5-5: 글자·로고·얼굴 없음, 캡션 표기)
import os, sys
sys.path.insert(0, r"C:\Users\user\Desktop\Blog\_1.컨텐츠\축구_컨텐츠")
from football_cards_base import *
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images"); os.makedirs(OUT, exist_ok=True)
AI = os.path.join(HERE, "ai")
def out(n): return os.path.join(OUT, n)

set_palette(BG=(10,30,74), PANEL=(22,46,98), PANEL2=(36,64,124),
            MUTED=(168,186,222), ACCENT=(255,255,255))
T_BLUE, T_WHITE, T_RED = (28,72,170), (245,245,245), (206,32,52)   # 청백적 띠 (트레이드마크 색)

def tricolor(d, y=0, h=10, w=W):
    d.rectangle([0,y,w,y+h], fill=T_BLUE); d.rectangle([0,y+h,w,y+2*h], fill=T_WHITE); d.rectangle([0,y+2*h,w,y+3*h], fill=T_RED)

def shade(im, top_alpha=230, until=0.55, bottom_alpha=0, from_=1.0):
    """위쪽을 어둡게(글자 자리) — 아래로 갈수록 투명"""
    ov = Image.new("RGBA", im.size, (0,0,0,0)); od = ImageDraw.Draw(ov); H = im.size[1]
    for y in range(H):
        t = y/H
        a = int(top_alpha*(1-t/until)) if t < until else 0
        if t > from_: a = max(a, int(bottom_alpha*(t-from_)/(1-from_)))
        od.line([0,y,W,y], fill=(6,14,36,max(0,a)))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

def red_bar(d, y, text, size=34):
    d.rounded_rectangle([MARGIN,y,W-MARGIN,y+86], radius=14, fill=T_RED)
    center(d, (W/2,y+43), text, f(BLACK,size), (255,255,255))

def outline_text(d, xy, t, fo, fill, stroke=(6,14,36), sw=3, anchor="mm"):
    d.text(xy, t, font=fo, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)

# ------------------------------------------------ 01 리뷰 썸네일 (공 세 개 = 해트트릭)
def review_thumb():
    im = Image.open(os.path.join(AI, "bg_balls.png")).convert("RGB").resize((1080,1080))
    im = shade(im, top_alpha=235, until=0.62)
    d = ImageDraw.Draw(im); tricolor(d, 0, 9)
    outline_text(d, (W/2,95), "K리그2 28라운드 · 수원삼성 vs 안산", f(BOLD,32), P["MUTED"])
    outline_text(d, (W/2,250), "4-1", f(BLACK,230), (255,255,255), sw=4)
    outline_text(d, (W/2,430), "루이스 해트트릭", f(BLACK,78), (255,255,255), sw=4)
    outline_text(d, (W/2,520), "10경기 무패 · 2위와 5점 차", f(BOLD,36), (220,232,255))
    red_bar(d, 905, "그런데 이정효는 왜 아쉽다고 했을까?", size=36)
    outline_text(d, (W/2,1040), "기록: 다음 스포츠 · 배경은 AI 생성 이미지(실제 경기 장면 아님)", f(REG,20), (200,210,232), sw=2)
    im.save(out("01_thumb.png"))

# ------------------------------------------------ 정효볼 2편 썸네일 (손가락 신호)
def jhb2_thumb():
    im = Image.open(os.path.join(AI, "bg_hand.png")).convert("RGB").resize((1080,1080))
    ov = Image.new("RGBA", im.size, (0,0,0,0)); od = ImageDraw.Draw(ov)
    for x in range(W):                                   # 왼쪽을 어둡게(글자 자리)
        a = int(215*max(0,1-x/(W*0.62))); od.line([x,0,x,1080], fill=(6,14,36,a))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im); tricolor(d, 0, 9)
    outline_text(d, (80,120), "정효볼 2편", f(BOLD,38), P["MUTED"], anchor="lm")
    outline_text(d, (76,250), "정효볼", f(BLACK,150), (255,255,255), sw=4, anchor="lm")
    outline_text(d, (80,370), "원리 여섯", f(BLACK,76), (255,255,255), sw=4, anchor="lm")
    for i, t in enumerate(["끌어낸다", "숫자를 먼저", "역할로 채운다", "쏠리게 하고 반대로", "약속을 반복한다", "뺏기면 바로"]):
        y = 490 + i*58
        d.ellipse([80,y-17,114,y+17], fill=T_RED); center(d, (97,y), str(i+1), f(BLACK,20), (255,255,255))
        outline_text(d, (130,y), t, f(BOLD,34), (235,240,255), sw=2, anchor="lm")
    red_bar(d, 905, "손가락 신호 하나로 바뀌는 축구, 무엇을 약속했을까?", size=32)
    outline_text(d, (W/2,1040), "배경은 AI 생성 이미지(특정 인물 아님) · 직접 만든 이미지", f(REG,20), (200,210,232), sw=2)
    im.save(out("jhb2_01_thumb.png"))

# ------------------------------------------------ 02 루이스 네임카드
def luis_card():
    namecard(out("02_namecard_luis.png"), "오늘의 선수 · 수원 4-1 안산", "루이스",
             "수원삼성 공격수 · 70번 · 2026년 8월 김포에서 이적",
             [("오늘", "해트트릭 · 전반 1분 · 전반 26분 PK · 후반 11분"),
              ("수원 첫 경기", "8월 22일 천안전 · 프리킥 결승골"),
              ("수원에서", "리그 4경기 5골"),
              ("김포 시절", "2023~2026 · 122경기 55골"),
              ("이정효", "「우리 팀에 필요했던 선수」")],
             "언제든 골을 넣을 수 있는 옵션",
             "기록: 다음 스포츠 · 김포 기록: 더팩트 · 문구는 이정효 회견 요지 · 직접 만든 이미지", col=T_RED)

# ------------------------------------------------ 03 같은 주말, 10기 전역생 셋
def discharged():
    rows = [("이건희", "제주 · 10월 10일 서울 원정", "후반 시작 투입 → 동점골", GREEN),
            ("박철우", "수원FC · 10월 9일 화성전", "후반 시작 투입 → 결승골 크로스", GREEN),
            ("김주찬", "수원삼성 · 10월 11일 안산전", "후반 20분 투입 · 슈팅 1", AMBER)]
    top, rh, gap = 200, 150, 18
    H = top + len(rows)*(rh+gap) + 20 + 82 + 80
    im, d = base(H, "같은 주말, 상무 전역생 셋", "김천상무 10기 · 10월 6일 전역 · 전역 뒤 첫 경기")
    tricolor(d, 0, 8)
    y = top
    for i,(name,where,what,col) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL2"] if i==2 else P["PANEL"])
        d.rectangle([MARGIN,y+18,MARGIN+8,y+rh-18], fill=col)
        left(d, (110,y+52), name, f(BLACK,46), P["CREAM"])
        left(d, (330,y+50), where, f(BOLD,26), P["MUTED"])
        left(d, (330,y+100), what, f(BLACK,32), P["CREAM"])
        y += rh+gap
    y += 2; bar(d, y, "전역 닷새 안에 셋 다 그라운드에 섰다", size=31)
    src(d, y+82+40, "기록: 다음 스포츠 · 전역: 김천상무 10기 명단·MHN · 도움: 뉴스1 · 직접 만든 이미지")
    im.save(out("03_discharged.png"))

# ------------------------------------------------ 전술판 공통
SUW, ANS = KOR, OPP          # 수원 = 우리 팀 주황, 안산 = 상대 청록 (고정 의미색)
def board(title, sub, lt, rt, lcol=AMBER, rcol=RED, H=1370):
    im, d = base(H, title, sub); tricolor(d, 0, 8)
    two_pitches(d, lt, rt, lcol, rcol)
    return im, d
def finish(im, d, H, notes, foot, source, legend_items):
    legend(d, 985, legend_items)
    numbered_notes(d, 1050, notes)
    bar(d, H-150, foot, size=31)
    src(d, H-38, source)

def curve_arrow(d, p0, c, p1, col, w=4, head=14, n=40):
    """휘어 가는 공(2차 곡선) — 실선 + 끝 화살촉"""
    pts = [((1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0], (1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1]) for t in [i/n for i in range(n+1)]]
    d.line(pts[:-2], fill=col, width=w, joint="curve")
    arrow(d, pts[-4], pts[-1], col, w=w, head=head)

# 배치표 (위쪽 = 안산 골문, 수원은 위로 공격) — 사용자 확인(10/11, 중계 1:33~1:35)
# 앞 네 명은 높고 넓게, 양 풀백은 김민우와 같은 높이, 센터백 둘이 뒤
SUW_BACK = dict(LB=(0.10,0.60), LCB=(0.36,0.78), RCB=(0.64,0.78), RB=(0.90,0.60), 김민우=(0.66,0.60), 정호연=(0.40,0.62))
SUW_FRONT = dict(르본=(0.08,0.32), 루이스=(0.38,0.32), 페신=(0.64,0.32), 강성진=(0.92,0.32))
ANS_BACK_X, ANS_MID_X = (0.12,0.30,0.50,0.70,0.88), (0.18,0.36,0.52,0.76)
ANS_BY, ANS_MY = 0.22, 0.44

# ------------------------------------------------ 04 첫 골 — 넓게 선 네 명, 그 사이가 비었다
def goal1():
    H = 1370
    im, d = board("넓게 선 네 명, 그 사이가 비었다", "전반 1분 루이스 첫 골 · 위쪽이 안산 골문 · 개념도",
                  "① 앞 네 명이 넓게 → 간격이 벌어진다", "② 김민우 → 수비가 놓친 틈으로", lcol=AMBER, rcol=GREEN, H=H)
    zone(im, [PB[0]+PW*0.33, PB[1]+PH*0.12, PB[0]+PW*0.47, PB[1]+PH*0.28], RED, 70)      # 수비가 놓친 틈
    d = ImageDraw.Draw(im)
    for o, second in ((PA, False), (PB, True)):
        for x in ANS_BACK_X: player(d, *pt(o,x,ANS_BY), ANS, r=12)
        for x in ANS_MID_X:
            player(d, *pt(o,x,ANS_MY), ANS, r=14 if x==0.76 else 12)
        player(d, *pt(o,0.52,0.56), ANS, r=12)
        for k,(x,y) in SUW_BACK.items():
            lab = "김민우 · 견제 없음" if (k=="김민우" and second) else None
            player(d, *pt(o,x,y), SUW, label=lab, r=14 if k=="김민우" else 12)
        for k,(x,y) in SUW_FRONT.items():
            if k == "루이스" and second: y = 0.33
            player(d, *pt(o,x,y), SUW, label=("루이스" if k=="루이스" and second else None), r=14 if k=="루이스" else 12)
    # ① 넓은 간격 표시(양쪽 화살표) + 망설이는 안산 미드필더
    for x0,x1 in ((0.10,0.36),(0.40,0.62),(0.66,0.90)):
        arrow(d, pt(PA,(x0+x1)/2,0.27), pt(PA,x0,0.27), P["CREAM"], w=2, head=9)
        arrow(d, pt(PA,(x0+x1)/2,0.27), pt(PA,x1,0.27), P["CREAM"], w=2, head=9)
    tag(d, *pt(PA,0.50,0.09), "앞 네 명이 폭을 넓게 잡는다", size=17)
    arrow(d, pt(PA,0.75,0.475), pt(PA,0.69,0.565), ANS, w=3, dashed=True, head=10)   # 앞(김민우)?
    arrow(d, pt(PA,0.74,0.41), pt(PA,0.67,0.355), ANS, w=3, dashed=True, head=10)    # 뒤(페신)?
    tag(d, *pt(PA,0.84,0.50), "앞? 뒤?", size=17, fill=RED)
    tag(d, *pt(PA,0.40,0.88), "양 풀백은 김민우와 같은 높이", size=16)
    # ② 김민우 → 틈으로 곧장(실선), 루이스가 틈으로 뛰어듦(점선)
    arrow(d, pt(PB,0.655,0.555), pt(PB,0.405,0.17), SUW)
    arrow(d, pt(PB,0.39,0.30), pt(PB,0.40,0.16), SUW, dashed=True, head=12)
    tag(d, *pt(PB,0.70,0.08), "수비가 놓친 틈", size=17, fill=RED)
    finish(im, d, H,
           ["앞 네 명이 폭을 넓게 잡아 안산 수비 사이 간격이 벌어졌다",
            "안산 미드필더가 앞(김민우)과 뒤 사이에서 망설여 김민우가 비었다",
            "김민우가 그 틈으로 곧장, 루이스가 뛰어들어 가슴으로 받고 골 (1분)"],
           "넓게 선 네 명, 그 사이가 비었다",
           "장면: 중계 화면 확인 · 새벽의 축구 전문가 전술판 해설 · 기록: 다음 스포츠 · 직접 만든 이미지",
           [(SUW,"수원삼성"), (ANS,"안산")])
    im.save(out("04_goal1_board.png"))

# ------------------------------------------------ 05 실점 — 교체 직후 왼쪽 + 먼 쪽 3대2
def concede():
    H = 1370
    im, d = board("교체 3분 뒤, 왼쪽에서 먼 쪽으로", "후반 20분대 초반 안산 류승완 골 · 아래쪽이 수원 골문 · 개념도",
                  "① 공 쪽: 두 명이 한 명에게", "② 먼 쪽: 골라인 앞 컷백 헤더", lcol=RED, rcol=RED, H=H)
    zone(im, [PB[0]+PW*0.66, PB[1]+PH*0.88, PB[0]+PW*0.98, PB[1]+PH*0.995], RED, 55)
    d = ImageDraw.Draw(im)
    # ① 왼쪽 피치 — 수원 왼쪽(화면 왼쪽) 측면, 골대 가까이
    player(d, *pt(PA,0.08,0.76), ANS, r=15)                                  # 안산 오른쪽에서 크로스
    player(d, *pt(PA,0.24,0.62), ANS, r=13)                                  # 2대1 상대
    player(d, *pt(PA,0.30,0.53), SUW, r=13)                                  # 왼쪽 측면 자리(교체) — 늦게 나옴
    player(d, *pt(PA,0.18,0.55), SUW, r=13)                                  # 왼쪽 풀백 자리(교체) — 위로 나감
    arrow(d, pt(PA,0.17,0.585), pt(PA,0.11,0.70), SUW, dashed=True, head=11) # 늦은 복귀
    tag(d, *pt(PA,0.40,0.45), "두 명이 한 명에게", size=17, fill=RED)
    tag(d, *pt(PA,0.22,0.90), "크로스 길이 열렸다", size=17, fill=RED)
    for x,y in ((0.40,0.84),(0.60,0.84),(0.86,0.80)): player(d, *pt(PA,x,y), SUW, r=12)
    player(d, *pt(PA,0.50,0.66), SUW, r=12)
    # ② 오른쪽 피치 — 골문 앞
    player(d, *pt(PB,0.06,0.80), ANS, r=13)                                  # 크로스 지점
    arrow(d, pt(PB,0.08,0.81), pt(PB,0.78,0.955), ANS)                       # 크로스 → 먼 쪽 골라인 앞
    player(d, *pt(PB,0.34,0.81), SUW, r=13)                                  # 왼쪽 센터백 자리 — 늦은 커버
    arrow(d, pt(PB,0.35,0.835), pt(PB,0.40,0.89), SUW, dashed=True, head=10)
    player(d, *pt(PB,0.55,0.86), SUW, r=13)                                  # 오른쪽 센터백 자리
    player(d, *pt(PB,0.70,0.84), SUW, r=13)                                  # 오른쪽 풀백 자리 — 안으로 좁힘
    player(d, *pt(PB,0.62,0.86), ANS, r=13)                                  # 둘이 함께 막은 공격수
    player(d, *pt(PB,0.81,0.965), ANS, r=15)                                 # 강동현 — 골라인 앞(코너와 골포스트 중간)
    d.line([*pt(PB,0.83,0.94), *pt(PB,0.86,0.83)], fill=P["CREAM"], width=2)
    tag(d, *pt(PB,0.86,0.80), "강동현(교체)", size=16)
    player(d, *pt(PB,0.44,0.935), ANS, label="류승완(교체)", r=15)
    arrow(d, pt(PB,0.78,0.962), pt(PB,0.475,0.937), ANS, w=3, head=11)        # 컷백처럼 머리로 뒤로 떨굼
    d.line([*pt(PB,0.70,0.815), *pt(PB,0.70,0.765)], fill=P["CREAM"], width=2)
    tag(d, *pt(PB,0.70,0.74), "좁힌 풀백", size=15)
    finish(im, d, H,
           ["교체로 바뀐 왼쪽 두 자리가 한 명에게 겹쳐 크로스를 못 막았다",
            "먼 쪽 풀백 자리는 안으로 좁혀 골라인까지 간 선수를 놓쳤다",
            "골라인 앞에서 컷백처럼 떨군 헤더를 류승완이 밀어 넣었다"],
           "교체 3분 뒤, 약속이 흔들렸다",
           "장면: 축구왕 이덕배 · K리그 하이라이트 중계 · 스포츠조선 · 직접 본 장면 확인 · 직접 만든 이미지",
           [(SUW,"수원삼성"), (ANS,"안산")])
    im.save(out("05_concede_board.png"))

# ------------------------------------------------ 06 3편 「볼 것 네 가지」 채점
def scorecard():
    rows = [("루이스·두비츠카스 같이 선발로 골?", "루이스 해트트릭 · 두비츠카스는 후반 34분 투입", "반반", AMBER),
            ("슈팅이 골로 바뀌나", "7월 같은 상대 슈팅 30개 넘게 1골 → 오늘 17개로 4골", "맞음", GREEN),
            ("안산의 역습 한 방을 막나", "역습 실점은 없음 · 교체 직후 크로스로 1실점", "반반", AMBER),
            ("김주찬이 명단에 드나", "후반 20분 투입 · 전역 닷새 만의 경기", "맞음", GREEN)]
    top, rh, gap = 200, 124, 14
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "어제 적은 네 가지, 채점", "정효볼 3편 「내일 볼 것」 → 수원 4-1 안산"); tricolor(d, 0, 8)
    y = top
    for i,(p,now,j,col) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL"])
        d.rectangle([MARGIN,y+16,MARGIN+8,y+rh-16], fill=col)
        left(d, (106,y+42), p, f(BOLD,29), P["CREAM"])
        left(d, (106,y+88), now, f(REG,24), P["MUTED"])
        chip(d, (W-MARGIN-26,y+rh/2), j, col)
        y += rh+gap
    y += 16; bar(d, y, "넷 중 둘은 맞고, 둘은 반만 맞았다", size=31)
    src(d, y+82+40, "기록: 다음 스포츠 (2026.10.11 경기 종료 조회) · 직접 만든 이미지")
    im.save(out("06_scorecard.png"))

if __name__ == "__main__":
    review_thumb(); jhb2_thumb(); luis_card(); discharged(); goal1(); concede(); scorecard()
    print(sorted(os.listdir(OUT)))
