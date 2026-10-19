# 수원삼성 vs 화성FC 프리뷰 카드 (2026.10.12)
# 톤: 미드나이트 + 골드 (리뷰 로열 블루, 2편 그래파이트·라벤더, 3편 사파이어와 다르게 — 인수인계서 4-3)
# 의미색: 수원 = 우리 팀 주황(KOR), 화성 = 상대 청록(OPP), 안산 = 회청(ANS2)
import os, sys
sys.path.insert(0, r"C:\Users\user\Desktop\Blog\_1.컨텐츠\축구_컨텐츠")
from football_cards_base import *
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images"); os.makedirs(OUT, exist_ok=True)
AI = os.path.join(HERE, "ai")
def out(n): return os.path.join(OUT, n)

set_palette(BG=(16,20,30), PANEL=(30,36,52), PANEL2=(44,52,72),
            MUTED=(170,178,196), ACCENT=(236,196,96))
T_BLUE, T_WHITE, T_RED = (28,72,170), (245,245,245), (206,32,52)
SUW, HWA, ANS2 = KOR, OPP, (128,140,170)

def tricolor(d, y=0, h=8, w=W):
    d.rectangle([0,y,w,y+h], fill=T_BLUE); d.rectangle([0,y+h,w,y+2*h], fill=T_WHITE); d.rectangle([0,y+2*h,w,y+3*h], fill=T_RED)

def outline_text(d, xy, t, fo, fill, stroke=(8,10,18), sw=3, anchor="mm"):
    d.text(xy, t, font=fo, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)

# ------------------------------------------------ 01 썸네일 (센터서클 공 + 두 빛 = 두 방식의 맞대결)
def thumb():
    bgp = os.path.join(AI, "bg_center.png")
    im = Image.open(bgp).convert("RGB").resize((1080,1080)) if os.path.exists(bgp) else Image.new("RGB", (1080,1080), P["BG"])
    ov = Image.new("RGBA", im.size, (0,0,0,0)); od = ImageDraw.Draw(ov)
    for y in range(1080):
        t = y/1080; a = int(232*(1-t/0.62)) if t < 0.62 else 0
        od.line([0,y,W,y], fill=(8,10,18,max(0,a)))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im); tricolor(d, 0, 9)
    outline_text(d, (W/2,92), "10월 18일 · K리그2 29라운드 · 수원삼성 vs 화성FC", f(BOLD,32), P["MUTED"])
    outline_text(d, (W/2,175), "같은 안산을 뚫은 시간", f(BLACK,52), (255,255,255))
    outline_text(d, (300,330), "2분", f(BLACK,170), SUW, sw=5)
    outline_text(d, (W/2,335), "vs", f(BLACK,60), P["MUTED"])
    outline_text(d, (790,330), "66분", f(BLACK,170), HWA, sw=5)
    outline_text(d, (300,460), "수원삼성", f(BLACK,44), (255,255,255))
    outline_text(d, (790,460), "화성FC", f(BLACK,44), (255,255,255))
    d.rounded_rectangle([MARGIN,905,W-MARGIN,991], radius=14, fill=T_RED)
    center(d, (W/2,948), "10월 18일엔 누가 먼저 뚫을까?", f(BLACK,38), (255,255,255))
    outline_text(d, (W/2,1040), "득점 시각: K리그 공식 기록 · 배경은 AI 생성 이미지(실제 경기 장면 아님)", f(REG,20), (204,210,226), sw=2)
    im.save(out("01_thumb.png"))

# ------------------------------------------------ 02 같은 안산, 두 번의 승리
def two_wins():
    rows = [("결과", "4-1 승 (10/11 홈)", "2-0 승 (9/12 원정)"),
            ("점유", "60%", "44%"),
            ("슈팅(유효)", "17(10)", "7(4)"),
            ("첫 골", "2분 루이스", "66분 플라나 PK"),
            ("마지막 골", "61분 (자책골)", "96분 일류첸코"),
            ("실점", "68분 (교체 직후)", "0")]
    top, rh, gap = 270, 92, 12
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "같은 안산, 두 번의 승리", "안산그리너스를 상대로 수원과 화성이 이긴 방식"); tricolor(d, 0, 8)
    cx = (MARGIN+300, 540, 830)
    center(d, (cx[1]+10,218), "수원삼성", f(BLACK,34), SUW); center(d, (cx[2]+20,218), "화성FC", f(BLACK,34), HWA)
    y = top
    for i,(k,a,b) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=14, fill=P["PANEL2"] if k in ("첫 골","점유") else P["PANEL"])
        left(d, (100,y+rh/2), k, f(BOLD,27), P["MUTED"])
        center(d, (cx[1]+10,y+rh/2), a, f(BLACK,30), P["CREAM"])
        center(d, (cx[2]+20,y+rh/2), b, f(BLACK,30), P["CREAM"])
        y += rh+gap
    y += 18; bar(d, y, "공을 쥐고 일찍 vs 공을 내주고 늦게", size=31)
    src(d, y+82+40, "기록: 다음 스포츠 · 득점 시각: K리그 공식 기록 · 직접 만든 이미지")
    im.save(out("02_two_wins.png"))

# ------------------------------------------------ 03 전술판 — 1차전 동점골(끌어내기) vs 안산전 첫 골 (사용자 수정 10/12)
def curve_arrow(d, p0, c, p1, col, w=4, head=13, n=40):
    pts = [((1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0], (1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1]) for t in [i/n for i in range(n+1)]]
    d.line(pts[:-2], fill=col, width=w, joint="curve")
    arrow(d, pts[-4], pts[-1], col, w=w, head=head)

def board_first_leg():
    H = 1400
    im, d = base(H, "끌어내서 생긴 틈", "화성 1차전 동점골과 안산전 첫 골 · 위쪽이 상대 골문 · 개념도"); tricolor(d, 0, 8)
    two_pitches(d, "화성 1차전 동점골 (68분)", "안산전 첫 골 (2분)", GREEN, GREEN)
    # ① 왼쪽: 고종현이 센터서클 위까지 → 화성 오른쪽이 안으로 좁혀짐 → 헤이스가 골라인 근처까지 파고들어 컷백 → 강현묵 (사용자 수정 10/12)
    zone(im, (pt(PA,0.83,0)[0], pt(PA,0,0.01)[1], pt(PA,0.995,0)[0], pt(PA,0,0.40)[1]), GREEN, 60); d = ImageDraw.Draw(im)
    tag(d, *pt(PA,0.84,0.60), "오른쪽이 비었다", size=16, fill=GREEN)
    for x,y in ((0.10,0.09),(0.28,0.08),(0.45,0.075),(0.60,0.075)): player(d, *pt(PA,x,y), HWA, r=12)
    for x,y in ((0.16,0.30),(0.38,0.30),(0.56,0.31)): player(d, *pt(PA,x,y), HWA, r=12)
    player(d, *pt(PA,0.50,0.62), HWA, r=12)
    arrow(d, pt(PA,0.93,0.12), pt(PA,0.77,0.17), HWA, dashed=True, head=11); player(d, *pt(PA,0.74,0.18), HWA, r=12)
    arrow(d, pt(PA,0.90,0.34), pt(PA,0.73,0.43), HWA, dashed=True, head=11); player(d, *pt(PA,0.70,0.45), HWA, r=12)
    for x,y in ((0.38,0.80),(0.16,0.68),(0.46,0.70),(0.06,0.30),(0.30,0.24)): player(d, *pt(PA,x,y), SUW, r=13)
    arrow(d, pt(PA,0.47,0.31), pt(PA,0.50,0.20), SUW, dashed=True, head=11)
    player(d, *pt(PA,0.50,0.17), SUW, r=13); tag(d, *pt(PA,0.37,0.165), "강현묵", size=15)
    arrow(d, pt(PA,0.62,0.82), pt(PA,0.60,0.44), SUW, dashed=True, head=12)
    player(d, *pt(PA,0.60,0.42), SUW, r=13); tag(d, *pt(PA,0.42,0.47), "고종현", size=15)
    arrow(d, pt(PA,0.95,0.54), pt(PA,0.93,0.34), SUW, dashed=True, head=11)
    arrow(d, pt(PA,0.63,0.40), pt(PA,0.90,0.31), P["CREAM"], w=4, head=12)
    arrow(d, pt(PA,0.92,0.28), pt(PA,0.885,0.09), SUW, dashed=True, head=11)
    player(d, *pt(PA,0.87,0.055), SUW, r=13); tag(d, *pt(PA,0.68,0.025), "헤이스(10)", size=15)
    arrow(d, pt(PA,0.84,0.065), pt(PA,0.53,0.16), P["CREAM"], w=4, head=13)
    # ② 오른쪽: 안산 뒤 다섯, 수원 앞 넷 넓고 높게, 루이스가 틈으로
    zone(im, (pt(PB,0.40,0.10)[0], pt(PB,0,0.10)[1], pt(PB,0.62,0)[0], pt(PB,0,0.24)[1]), GREEN, 60); d = ImageDraw.Draw(im)
    for x in (0.10,0.28,0.50,0.72,0.90): player(d, *pt(PB,x,0.20), ANS2, r=12)
    for x in (0.18,0.36,0.74,0.88): player(d, *pt(PB,x,0.43), ANS2, r=12)
    for x,y in ((0.06,0.32),(0.36,0.32),(0.64,0.32),(0.94,0.32)): player(d, *pt(PB,x,y), SUW, r=13)
    for x,y in ((0.38,0.80),(0.62,0.80),(0.10,0.62),(0.90,0.62),(0.40,0.62)): player(d, *pt(PB,x,y), SUW, r=13)
    player(d, *pt(PB,0.66,0.62), SUW, r=13)
    arrow(d, pt(PB,0.66,0.60), pt(PB,0.50,0.15), P["CREAM"], w=4, head=13)
    arrow(d, pt(PB,0.38,0.30), pt(PB,0.48,0.16), GREEN, dashed=True, head=12)
    tag(d, *pt(PB,0.52,0.06), "수비 사이 틈으로 뛰어듦", size=16, fill=GREEN)
    tag(d, *pt(PB,0.24,0.27), "루이스", size=15)
    tag(d, *pt(PB,0.80,0.70), "김민우 롱패스", size=15)
    legend(d, 1000, [(SUW,"수원삼성"), (HWA,"화성"), (ANS2,"안산")])
    numbered_notes(d, 1065, ["화성 1차전: 고종현이 센터서클 위까지 몰고 가자 오른쪽 수비가 안으로 좁혀졌다",
                             "헤이스가 그 빈 오른쪽을 골라인까지 파고들어 컷백, 강현묵이 넣었다",
                             "안산전: 앞 넷이 넓게 서고 루이스가 수비 사이 틈으로 뛰었다"])
    bar(d, H-150, "누군가를 끌어내야 반대쪽이 빈다", size=30)
    src(d, H-38, "장면: 화성 1차전 중계·새벽의 축구 전문가 분석 + 사용자 확인(10/12) · 안산전 도해(사용자 확인 10/11) · 개념도 · 직접 만든 이미지")
    im.save(out("03_first_leg_board.png"))

# ------------------------------------------------ 04 65~75분 — 수원이 흔들린 시간, 화성이 찌른 시간
def timeline():
    H = 900
    im, d = base(H, "65~75분이 겹친다", "같은 안산전 — 수원 10/11 · 화성 9/12 (분 = 경기 시간)"); tricolor(d, 0, 8)
    x0, x1 = 120, 960
    def X(m): return x0 + (x1-x0)*min(m,98)/98
    for row,(y,name,col) in enumerate(((300,"수원삼성",SUW),(560,"화성FC",HWA))):
        left(d, (MARGIN,y-118), name, f(BLACK,32), col)
        zone(im, (X(65),y-40,X(75),y+40), RED, 70); d = ImageDraw.Draw(im)
        d.line([x0,y,x1,y], fill=P["MUTED"], width=4)
        for m in (0,45,90): d.line([X(m),y-14,X(m),y+14], fill=P["MUTED"], width=3); center(d, (X(m),y+36), "%d분"%m, f(REG,20), P["MUTED"])
    def ev(y, m, text, col, up=True, kind="goal", lv=0):
        if kind == "goal": d.ellipse([X(m)-13,y-13,X(m)+13,y+13], fill=col, outline=P["CREAM"], width=3)
        else: d.rounded_rectangle([X(m)-10,y-10,X(m)+10,y+10], radius=4, fill=P["BG"], outline=col, width=4)
        ty = (y-52-lv*40) if up else (y+70+lv*40)
        tag(d, X(m), ty, text, size=17, fill=col)
    ev(300, 2, "2분 골", GREEN); ev(300, 27, "27분 골", GREEN, up=False); ev(300, 57, "57분 골", GREEN); ev(300, 61, "61분 자책골", GREEN, up=False)
    ev(300, 65, "후반 20분쯤 3명 교체", AMBER, kind="sub", up=True, lv=1); ev(300, 68, "68분 실점", RED, up=False, lv=1)
    ev(560, 66, "66분 PK 골", GREEN); ev(560, 67.5, "후반 21분쯤 일류첸코 교체 투입", AMBER, kind="sub", up=False); ev(560, 96, "96분 일류첸코 골", GREEN, up=True)
    center(d, (X(70),168), "65~75분", f(BLACK,26), RED)
    bar(d, H-150, "수원이 흔들린 시간 = 화성이 찌른 시간", size=31)
    src(d, H-38, "득점: K리그 공식 기록 · 교체 시각: 다음 스포츠(후반 20·21분) · 직접 만든 이미지")
    im.save(out("04_timeline.png"))

# ------------------------------------------------ 05 빠지는 자리 — 장민준
def jang():
    namecard(out("05_jang_minjun.png"), "10월 18일 경고누적 출전정지 대상(대회요강 제39조)", "장민준",
             "화성FC 수비수 · 2002년생 · 186cm · 왼발",
             [("올해", "21경기 2골(K리그 공식) · 뒤 셋의 왼쪽"),
              ("화성 1차전", "전반 42분 선제골 · 플라나 코너킥을 왼발로"),
              ("역할", "세트피스 높이 · 곧바로 전방으로 연결"),
              ("경고", "8장 · 5장째 다음 경기(R19)도 결장"),
              ("작년 안산", "5장째·8장째 다음 경기 모두 결장"),
              ("없던 경기", "R19 승 · R25 무 · R26 승 · R27 무")],
             "빠져도 무너지진 않았다, 바뀌는 건 높이와 왼쪽",
             "기록: 다음 스포츠 · K리그 공식 기록 · 대회요강 · 출전정지 공시는 없음(10/12) · 직접 만든 이미지", col=HWA)

# ------------------------------------------------ 06 관전 포인트 = 후기 채점 기준
def checkpoints():
    rows = [("수원이 전반에 먼저 넣나", "안산전 2분 / 화성 1차전은 화성이 먼저(42분)"),
            ("앞 선수가 뒤로 뛰나", "화성 1차전엔 사이사이에만 섰다"),
            ("65~75분을 버티나", "안산전 교체 뒤 68분 실점"),
            ("장민준 없는 화성의 높이와 왼쪽", "화성 1차전 골 = 그의 코너킥 골"),
            ("일류첸코, 친정 첫 경기", "화성 1차전 수원 결승골 → 지금은 화성")]
    top, rh, gap = 200, 116, 14
    H = top + len(rows)*(rh+gap) + 30 + 82 + 80
    im, d = base(H, "10월 18일에 볼 다섯 가지", "경기 뒤 후기에서 하나씩 채점한다"); tricolor(d, 0, 8)
    y = top
    for i,(p,now) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=16, fill=P["PANEL"])
        d.rectangle([MARGIN,y+16,MARGIN+8,y+rh-16], fill=P["ACCENT"])
        center(d, (128,y+rh/2), str(i+1), f(BLACK,40), P["ACCENT"])
        left(d, (180,y+40), p, f(BLACK,30), P["CREAM"])
        left(d, (180,y+84), now, f(REG,24), P["MUTED"])
        y += rh+gap
    y += 16; bar(d, y, "답은 경기 뒤 후기에서", size=31)
    src(d, y+82+40, "기록: 다음 스포츠 · K리그 공식 기록 · 직접 만든 이미지")
    im.save(out("06_checkpoints.png"))

if __name__ == "__main__":
    thumb(); two_wins(); board_first_leg(); timeline(); jang(); checkpoints()
    print(sorted(os.listdir(OUT)))
