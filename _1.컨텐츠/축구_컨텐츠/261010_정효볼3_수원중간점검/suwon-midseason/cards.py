# 정효볼 3편 — 이정효 수원삼성 중간 점검 카드 (2026.10.10)
# 톤: 딥 사파이어 + 스카이 (1편 웜 차콜+골드와 다르게)
import os, sys
sys.path.insert(0, r"C:\Users\user\Desktop\Blog\_1.컨텐츠\축구_컨텐츠")
from football_cards_base import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)
def out(n): return os.path.join(OUT, n)

set_palette(BG=(14,26,54), PANEL=(28,42,74), PANEL2=(44,60,98),
            MUTED=(160,176,206), ACCENT=(128,196,245))
SUWON = KOR   # 우리 팀 = 주황 (고정 의미색)

# ---------------------------------------------------------------- 01 썸네일
def thumb():
    H = 1080
    im, d = base(H)
    center(d, (W/2,86), "정효볼 3편 · 수원 첫해 중간 점검", f(BOLD,30), P["MUTED"])
    center(d, (W/2,166), "이정효 수원삼성", f(BLACK,66), P["CREAM"])
    # 큰 숫자 두 칸
    boxes = [(MARGIN, 250, 525, 560, P["PANEL2"], "리그 순위", "1위", "25경기 승점 53", P["ACCENT"]),
             (555, 250, W-MARGIN, 560, P["PANEL"], "득점 순위", "6번째", "39골", P["CREAM"])]
    for x0,y0,x1,y1,bg,lab,big,sub,col in boxes:
        d.rounded_rectangle([x0,y0,x1,y1], radius=18, fill=bg)
        center(d, ((x0+x1)/2, y0+52), lab, f(BOLD,30), P["MUTED"])
        center(d, ((x0+x1)/2, y0+165), big, f(BLACK,124), col)
        center(d, ((x0+x1)/2, y0+268), sub, f(BOLD,30), P["CREAM"])
    # 작은 칸 셋
    cells = [("25경기", "16승 5무 4패"), ("2·3위와", "승점 2점 차"), ("남은 경기", "7경기")]
    cw = (W-2*MARGIN-2*20)/3; y0 = 590
    for i,(k,v) in enumerate(cells):
        x0 = MARGIN + i*(cw+20)
        d.rounded_rectangle([x0,y0,x0+cw,y0+150], radius=16, fill=P["PANEL"])
        center(d, (x0+cw/2,y0+46), k, f(BOLD,26), P["MUTED"])
        center(d, (x0+cw/2,y0+102), v, f(BLACK,38), P["CREAM"])
    bar(d, 776, "1위인데 득점은 6번째, 어떻게 이기고 있을까?", size=33)
    center(d, (W/2,920), "내일 10월 11일 안산전 · 한 달 만의 경기", f(BOLD,30), P["ACCENT"])
    src(d, 1030, "기록: 다음 스포츠 (2026.10.10 조회) · 직접 만든 이미지")
    im.save(out("01_thumb.png"))

# ---------------------------------------------------------------- 02 숫자
def numbers():
    rows = [("실점", "20", "리그 최소", GREEN),
            ("무실점 경기", "13", "리그 최다", GREEN),
            ("득점", "39", "6번째", AMBER),
            ("슈팅", "309", "4번째", AMBER)]
    top, rh, gap = 200, 112, 14
    H = top + len(rows)*(rh+gap) + 150 + 30 + 82 + 80
    im, d = base(H, "실점이 가장 적은 1위", "2026 K리그2 · 수원삼성 25경기 · 17팀 중 순위")
    y = top
    for i,(k,v,rk,col) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL2"] if i==0 else P["PANEL"])
        d.rectangle([MARGIN,y+16,MARGIN+8,y+rh-16], fill=col)
        left(d, (110,y+rh/2), k, f(BOLD,30), P["CREAM"])
        right(d, (640,y+rh/2), v, f(BLACK,58), P["CREAM"])
        chip(d, (W-MARGIN-30,y+rh/2), rk, col)
        y += rh+gap
    # 한 골 차 줄
    d.rounded_rectangle([MARGIN,y,W-MARGIN,y+150], radius=16, fill=P["PANEL"])
    center(d, (W/2,y+50), "16승 가운데", f(BOLD,28), P["MUTED"])
    center(d, (W/2,y+104), "한 골 차 승리 11번 · 그중 1-0이 7번", f(BLACK,40), P["ACCENT"])
    y += 150 + 30
    bar(d, y, "1위를 만든 건 공격이 아니라 실점 20", size=32)
    src(d, y+82+40, "기록: 다음 스포츠 순위·경기 기록 (2026.10.10 조회) · 직접 만든 이미지")
    im.save(out("02_numbers.png"))

# ---------------------------------------------------------------- 03 채점표
def scorecard():
    rows = [("점유 축구로 바뀐다", "25경기 중 21경기 점유 우위", "맞음", GREEN),
            ("이건희·강성진·정호연이 맞는다", "오른쪽 이건희·강성진, 중원 정호연이 핵심", "맞음", GREEN),
            ("초반엔 안 굴러갈 수 있다", "개막 5연승", "빗나감", RED),
            ("실점이 적은 축구가 된다", "리그 최소 실점 20", "맞음", GREEN),
            ("(이정효) 상대가 내려서서 비기려 할 것", "김포전 0-1 · 안산전 1-2, 진 경기가 그 그림", "맞음", GREEN)]
    top, rh, gap = 200, 120, 14
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "부임 직후 예측, 다섯 중 넷", "2025년 12월~2026년 2월 예측 → 25경기 뒤")
    y = top
    for i,(p,now,j,col) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL2"] if i==4 else P["PANEL"])
        d.rectangle([MARGIN,y+16,MARGIN+8,y+rh-16], fill=col)
        left(d, (106,y+40), p, f(BOLD,28), P["CREAM"])
        left(d, (106,y+84), now, f(REG,24), P["MUTED"])
        chip(d, (W-MARGIN-26,y+rh/2), j, col)
        y += rh+gap
    y += 16
    bar(d, y, "수원이 진 경기는 감독이 걱정한 바로 그 방식", size=31)
    src(d, y+82+40, "예측: 축구 채널 부임 분석 · 이정효 전지훈련 인터뷰 / 기록: 다음 스포츠 · 직접 만든 이미지")
    im.save(out("03_scorecard.png"))

# ---------------------------------------------------------------- 타임라인 공통
def timeline(path, title, sub, rows, foot, source, legend_items=None):
    top, rh, gap = 210, 118, 18
    extra = 70 if legend_items else 0
    H = top + len(rows)*(rh+gap) + extra + 20 + 82 + 80
    im, d = base(H, title, sub)
    lx = 190
    d.line([lx, top+rh/2, lx, top+(len(rows)-1)*(rh+gap)+rh/2], fill=P["PANEL2"], width=6)
    y = top
    for i,(when,head,desc,col) in enumerate(rows):
        right(d, (lx-34, y+rh/2), when, f(BLACK,32), P["CREAM"])
        d.ellipse([lx-15,y+rh/2-15,lx+15,y+rh/2+15], fill=col, outline=P["CREAM"], width=3)
        x0 = lx+40
        d.rounded_rectangle([x0,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL"])
        d.rectangle([x0,y+16,x0+8,y+rh-16], fill=col)
        left(d, (x0+30,y+40), head, f(BLACK,30), P["CREAM"])
        left(d, (x0+30,y+84), desc, f(REG,24), P["MUTED"])
        y += rh+gap
    if legend_items:
        legend(d, y+22, legend_items); y += extra
    y += 2
    bar(d, y, foot, size=31)
    src(d, y+82+40, source)
    im.save(path)

def attack_timeline():
    rows = [("4월", "박스를 못 두드렸다", "김포전 점유 67%, 슈팅 3개로 0-1", RED),
            ("5월", "「점유율 놀이」 비판", "공은 뒤에서 U자로만 돈다", RED),
            ("7월", "두드렸는데 못 넣었다", "안산전 슈팅 34개, 1-2 패", AMBER),
            ("8월", "라인 사이에 사람이 남기 시작", "「슈팅이 나와야 골이 나온다」 — 이정효", GREEN),
            ("9월", "공을 덜 쥐고도 이겼다", "서울E전 점유 40%로 1-0", GREEN)]
    timeline(out("04_timeline.png"), "공격 문제의 모양이 바뀌었다",
             "이정효 기준 「상대 박스를 두드리는 게 주도」 · 2026 K리그2", rows,
             "지금 숙제는 점유가 아니라 마무리",
             "기록: 다음 스포츠 · 발언: 구단 영상·인터뷰 요지 · 직접 만든 이미지",
             [(RED,"못 미침"), (AMBER,"반쯤"), (GREEN,"좋아짐")])

def signings_timeline():
    rows = [("7/11", "안산전 1-2 패", "시즌 네 번째 패배", RED),
            ("7/19", "무패 시작", "영입생 없이", GREEN),
            ("7/25", "부산전 4-1", "영입생 없이", GREEN),
            ("7/27", "일류첸코 이적", "최전방이 비었다", RED),
            ("8/1", "두비츠카스 첫 출전", "리투아니아 대표 공격수", P["ACCENT"]),
            ("8/22", "루이스 첫 출전", "김포에서 이적 · 뛴 세 경기 1-0, 2-0, 1-0", P["ACCENT"])]
    timeline(out("06_signings.png"), "반등은 영입보다 먼저 시작됐다",
             "2026 여름 · 수원삼성 경기와 공격수 합류 순서", rows,
             "반등의 출발은 전술, 영입은 흐름을 이었다",
             "기록: 다음 스포츠 · 이적: 머니투데이 (7/28) · 직접 만든 이미지",
             [(GREEN,"반등"), (RED,"패배·이탈"), (P["ACCENT"],"공격수 합류")])

# ---------------------------------------------------------------- 05 전술판
def press():
    H = 1370
    im, d = base(H, "상대가 찌른 곳, 이정효가 고친 곳", "수원이 수비할 때 · 아래쪽이 수원 골문 · 개념도")
    two_pitches(d, "상대가 찌른 곳 — 맨투맨 뒤", "대응 — 센터백이 나와 닫는다", lcol=RED, rcol=GREEN)
    # 구역
    zone(im, [PA[0]+PW*0.42, PA[1]+PH*0.53, PA[0]+PW*0.80, PA[1]+PH*0.69], RED, 60)
    zone(im, [PB[0]+PW*0.42, PB[1]+PH*0.53, PB[0]+PW*0.80, PB[1]+PH*0.69], GREEN, 50)
    d = ImageDraw.Draw(im)
    for o, fixed in ((PA, False), (PB, True)):
        # 수원 수비 넷 (오른쪽 그림은 왼쪽 센터백이 앞으로)
        backs = [(0.14,0.82),(0.38,0.82),(0.62,0.82),(0.86,0.82)]
        for i,(x,y_) in enumerate(backs):
            if fixed and i == 2: continue
            player(d, *pt(o,x,y_), SUWON, r=13)
        # 수원 미드 넷 — 오른쪽 가운데 미드는 상대 핵심을 따라 올라가 있음
        for x,y_ in [(0.12,0.62),(0.36,0.62),(0.88,0.62)]:
            player(d, *pt(o,x,y_), SUWON, r=13)
        player(d, *pt(o,0.60,0.44), SUWON, r=14)
        arrow(d, pt(o,0.60,0.60), pt(o,0.60,0.48), SUWON, dashed=True, head=12)
        # 수원 투톱
        for x,y_ in [(0.36,0.26),(0.64,0.26)]:
            player(d, *pt(o,x,y_), SUWON, r=13)
        # 상대: 핵심 미드, 패스하는 선수, 침투하는 선수
        player(d, *pt(o,0.60,0.36), OPP, r=14)
        player(d, *pt(o,0.22,0.40), OPP, r=14)
        player(d, *pt(o,0.84,0.40), OPP, r=14)
    # 왼쪽: 등 뒤로 침투 + 패스
    arrow(d, pt(PA,0.84,0.43), pt(PA,0.66,0.59), OPP, dashed=True)
    arrow(d, pt(PA,0.25,0.43), pt(PA,0.56,0.60), OPP)
    tag(d, *pt(PA,0.61,0.66), "빈 공간", fill=RED)
    tag(d, *pt(PA,0.42,0.445), "맨투맨", size=17)
    # 오른쪽: 센터백 전진으로 닫음
    player(d, *pt(PB,0.62,0.63), SUWON, r=16)
    arrow(d, pt(PB,0.62,0.80), pt(PB,0.62,0.68), SUWON, dashed=True, head=12)
    tag(d, pt(PB,0.30,0.70)[0], pt(PB,0.30,0.70)[1], "센터백 고종현 전진", size=17, fill=GREEN)
    arrow(d, pt(PB,0.84,0.43), pt(PB,0.72,0.53), OPP, dashed=True)
    legend(d, 985, [(SUWON,"수원삼성"), (OPP,"상대")])
    numbered_notes(d, 1050, ["가운데 미드필더 한 명이 상대 핵심을 사람으로 붙잡는다",
                             "그 등 뒤로 다른 선수가 들어온다 (부산·수원FC·서울E)",
                             "대응: 센터백 전진 · 마크 상대 바꾸기 · 막히면 5-4-1"])
    bar(d, H-150, "약점은 남았지만, 대응하는 팀이 됐다", size=31)
    src(d, H-38, "전술 해설 영상 요지 · 이정효 기자회견 (9/12) · 직접 만든 이미지")
    im.save(out("05_press.png"))

# ---------------------------------------------------------------- 07 남은 경기
def remaining():
    rows = [("10/11", "안산", "홈", None),
            ("10/18", "화성", "홈", "상위권"),
            ("10/25", "성남", "원정", None),
            ("10/31", "대구", "원정", "상위권"),
            ("11/8", "용인", "홈", None),
            ("11/21", "경남", "홈", None),
            ("11/29", "전남", "원정", None)]
    top, rh, gap = 330, 84, 10
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "남은 7경기, 2위와 승점 2점 차", "수원삼성 25경기 승점 53 · 2위 수원FC·3위 서울E 승점 51")
    # 승격 규칙 띠
    d.rounded_rectangle([MARGIN,190,W-MARGIN,300], radius=16, fill=P["PANEL2"])
    center(d, (W/2,228), "1·2위 바로 승격 · 3~6위 플레이오프", f(BLACK,32), P["CREAM"])
    center(d, (W/2,272), "승강 플레이오프까지 최대 네 팀이 올라간다", f(REG,24), P["MUTED"])
    y = top
    for i,(dt,opp,ha,flag) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=14, fill=P["PANEL2"] if i==0 else P["PANEL"])
        d.rectangle([MARGIN,y+14,MARGIN+8,y+rh-14], fill=P["ACCENT"] if i==0 else (AMBER if flag else P["PANEL2"]))
        left(d, (110,y+rh/2), dt, f(BLACK,32), P["ACCENT"] if i==0 else P["CREAM"])
        left(d, (300,y+rh/2), opp, f(BLACK,34), P["CREAM"])
        left(d, (480,y+rh/2), ha, f(BOLD,28), P["MUTED"])
        if i == 0: chip(d, (W-MARGIN-26,y+rh/2), "내일", P["ACCENT"])
        elif flag: chip(d, (W-MARGIN-26,y+rh/2), flag, AMBER)
        y += rh+gap
    y += 20
    bar(d, y, "목표는 1위보다 2위 안", size=32)
    src(d, y+82+40, "일정: K리그 · 순위: 다음 스포츠 (2026.10.10 조회) · 승격 규칙: K리그 공지 · 직접 만든 이미지")
    im.save(out("07_remaining.png"))

if __name__ == "__main__":
    thumb(); numbers(); scorecard(); attack_timeline(); press(); signings_timeline(); remaining()
    print("ok", sorted(os.listdir(OUT)))
