# -*- coding: utf-8 -*-
"""병역특례 글 도해 16장. 숫자는 병역특례_공부노트_2026-10-11.md 에서 원본 확인한 것만 쓴다.
출력: img/NN_<이름>.png (1400x800)"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)
W, H = 1400, 800
BG = (250, 250, 247); INK = (30, 30, 30); GRAY = (120, 120, 120)
BLUE = (41, 98, 255); RED = (220, 60, 60); GREEN = (30, 150, 90); AMBER = (235, 150, 20)
LIGHT = (232, 236, 245); PINK = (252, 232, 232); MINT = (226, 245, 236); SAND = (252, 240, 215)
WHITE = (255, 255, 255)

def font(size, bold=False):
    name = "malgunbd.ttf" if bold else "malgun.ttf"
    return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", name), size)

F_T = font(42, True); F_H = font(30, True); F_B = font(26); F_S = font(21); F_X = font(56, True); F_N = font(40, True)

def canvas(title, sub=None):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.text((60, 44), title, font=F_T, fill=INK)
    if sub: d.text((60, 102), sub, font=F_S, fill=GRAY)
    return im, d

def box(d, xy, fill, text, f=F_B, color=INK, radius=18, outline=None, align="center"):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3 if outline else 0)
    lines = text.split("\n"); lh = f.size + 8; total = lh * len(lines)
    y = y0 + (y1 - y0 - total) / 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        x = x0 + (x1 - x0 - w) / 2 if align == "center" else x0 + 24
        d.text((x, y), ln, font=f, fill=color); y += lh

def arrow(d, p0, p1, color=INK, width=5):
    d.line([p0, p1], fill=color, width=width)
    x0, y0 = p0; x1, y1 = p1; ang = math.atan2(y1 - y0, x1 - x0); L = 18
    a = (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5))
    b = (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))
    d.polygon([p1, a, b], fill=color)

def foot(d, text): d.text((60, H - 48), text, font=F_S, fill=GRAY)

def ctext(d, cx, y, text, f, color=INK):
    d.text((cx - d.textlength(text, font=f) / 2, y), text, font=f, fill=color)

def save(im, name): im.save(os.path.join(OUT, name)); print("saved", name)

# 01 두 길
im, d = canvas("① '면제'가 아니라 '다른 길'이다", "현역병의 길 vs 예술·체육요원의 길 — 둘 다 병역법 안에 있다")
box(d, (90, 170, 660, 230), LIGHT, "현역병", F_H, INK)
box(d, (740, 170, 1310, 230), MINT, "예술·체육요원 (보충역)", F_H, GREEN)
box(d, (90, 260, 660, 430), WHITE, "입대\n→ 18개월 복무 (육군 기준)\n→ 그동안 직업·소득 중단", F_B, INK, outline=GRAY)
box(d, (740, 260, 1310, 430), WHITE, "기초군사훈련 4주\n→ 34개월 동안 소속팀에서 그대로 활동\n→ 그 안에 공익복무 544시간", F_B, INK, outline=GREEN)
box(d, (90, 470, 1310, 580), SAND, "둘 다 '복무'다. 다만 한쪽은 선수 생활과 연봉이 그대로 이어진다.\n그래서 모두가 '면제'라고 부른다 — 544시간을 34개월로 나누면 주당 3시간 40분.", F_B, INK)
foot(d, "근거: 병역법 33조의7·33조의8, 병무청 제도소개(훈련 4주·34개월·544시간). 주당 환산은 변호사랑 영상(10.7).")
save(im, "01_two_roads.png")

# 02 세 도장
im, d = canvas("② 금메달은 '자격'이고, 도장 세 개를 더 받아야 편입된다", "병역법 시행령 68조의11 ②·③ — 금메달이 곧 면제가 아닌 이유")
steps = [("금메달", "아시안게임 1위\n올림픽 3위 이상", SAND, AMBER), ("도장 1", "본인이\n추천원서 제출", LIGHT, BLUE),
         ("도장 2", "문체부 장관이\n14일 안에 추천", LIGHT, BLUE), ("도장 3", "병무청장이\n편입 결정", MINT, GREEN)]
x = 80
for t, s, fill, col in steps:
    box(d, (x, 220, x + 280, 290), fill, t, F_H, col)
    box(d, (x, 300, x + 280, 440), WHITE, s, F_B, INK, outline=col)
    if x < 1000: arrow(d, (x + 290, 370), (x + 330, 370))
    x += 340
box(d, (90, 500, 1310, 610), PINK, "10월 8일 기준, 논란이 된 세 선수의 원서는 아직 접수되지 않았다(더팩트).\n도장이 다 찍히기 전에 규칙이 바뀌면? → 그림 ⑮", F_B, INK)
foot(d, "근거: 시행령 68조의11 ②(추천원서→문체부) ③(14일 내 병무청장 통보), 법 33조의7 ①(편입할 수 있다). 더팩트 2026.10.8.")
save(im, "02_three_stamps.png")

# 03 2020.6.30 전후
im, d = canvas("③ 2020년 6월 30일, '뛴 사람만'이 '명단 전원'으로 바뀌었다", "단체경기 출전요건 삭제 — 0구 금메달·16분 출전이 모두 대상이 된 이유")
def bench(d, x0, y0, n_play, n_bench, play_col, bench_col):
    for i in range(n_play):
        cx = x0 + (i % 6) * 60; cy = y0 + (i // 6) * 60
        d.ellipse([cx, cy, cx + 44, cy + 44], fill=play_col)
    for i in range(n_bench):
        cx = x0 + ((i + n_play) % 6) * 60; cy = y0 + ((i + n_play) // 6) * 60
        d.ellipse([cx, cy, cx + 44, cy + 44], fill=bench_col)
box(d, (90, 170, 640, 230), LIGHT, "2020.6.30 이전", F_H, INK)
box(d, (760, 170, 1310, 230), MINT, "2020.6.30 이후", F_H, GREEN)
bench(d, 150, 260, 11, 12, GREEN, (200, 200, 200))
bench(d, 820, 260, 23, 0, GREEN, GREEN)
d.text((150, 520), "경기에 나간 사람만 편입 (회색은 제외)", font=F_S, fill=GRAY)
d.text((820, 520), "명단에 있으면 전원 편입", font=F_S, fill=GREEN)
box(d, (90, 580, 1310, 680), SAND, "바꾼 이유는 '1분 교체 출전' 같은 꼼수와 주전·벤치 차별을 없애려는 것이었다.\n결과는 2022년 0구 금메달(곽빈), 2026년 결승 16분 출전(박승수)도 똑같이 대상.", F_B, INK)
foot(d, "근거: 병무청 제도소개(2020.6.30 단체경기 조항 삭제), 2019.11.21 정부 브리핑, 머니투데이 10.7(곽빈), 결승 출전 기록.")
save(im, "03_bench_all.png")

# 04 81% 파이
im, d = canvas("④ 최근 4년 체육요원 편입 80명 중 65명이 아시안게임 금이다", "2022년 ~ 2026년 8월, 문체부 자료 (조은희 의원실)")
cx, cy, r = 420, 450, 230
d.pieslice([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=LIGHT)
d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * 65 / 80, fill=AMBER)
ctext(d, cx + 70, cy - 10, "65", F_X, WHITE); ctext(d, cx + 70, cy + 60, "아시안게임 금", F_S, WHITE)
ctext(d, cx - 95, cy - 150, "15", F_H, INK); ctext(d, cx - 95, cy - 112, "올림픽", F_S, INK)
box(d, (760, 240, 1310, 330), SAND, "81.3%", F_X, AMBER)
box(d, (760, 350, 1310, 560), WHITE, "같은 기간 복무규정 위반 42건\n그중 무허가 광고·후원 22건(21명)\n그 21명 중 17명이 아시안게임 금 출신", F_B, INK, outline=GRAY)
box(d, (90, 690, 1310, 740), MINT, "제도의 입구는 '올림픽 또는 아시안게임'이지만 실제 통로는 거의 아시안게임이다.", F_S, GREEN)
foot(d, "근거: 파이낸셜뉴스·이투데이 2026.10.1, 한국일보 10.5 (문체부 → 조은희 의원실 제출 자료).")
save(im, "04_pie_81.png")

# 05 1972 뮌헨
im, d = canvas("⑤ 1972년 뮌헨, 이 메달판이 제도의 출발점이다", "북한 첫 올림픽 출전 — 종합순위 22위 vs 33위")
def medals(d, x, y, g, s, b):
    cols = [((212, 175, 55), g), ((170, 170, 170), s), ((176, 120, 70), b)]
    for col, n in cols:
        for i in range(n):
            d.ellipse([x, y, x + 56, y + 56], fill=col); x += 70
        x += 30
box(d, (90, 180, 640, 240), PINK, "대한민국 — 33위", F_H, RED)
medals(d, 120, 280, 0, 1, 0); d.text((120, 360), "은 1 (유도)   금 0   동 0", font=F_B, fill=INK)
box(d, (760, 180, 1310, 240), LIGHT, "북한 — 22위", F_H, INK)
medals(d, 790, 280, 1, 1, 3); d.text((790, 360), "금 1 (사격)   은 1   동 3", font=F_B, fill=INK)
box(d, (90, 440, 1310, 560), SAND, "대한민국 이름으로 딴 올림픽 금은 아직 없던 때. 북한이 먼저 금을 땄다.\n이듬해 1973년, 비상국무회의가 '특기자 병역특례' 법을 만든다.", F_B, INK)
box(d, (90, 590, 1310, 680), WHITE, "같은 흐름: 1966 북한 월드컵 8강 → 1967 중앙정보부 양지축구단 / 1972 박종규 경호실장 '다시는 없게' → 태릉사격장", F_S, GRAY, outline=GRAY)
foot(d, "근거: olympics.com 메달 순위(한국 은1·북한 금1 은1 동3), 연합 [재점검]① 10.10, 한국일보 10.5, 나무위키 1972 뮌헨(박종규).")
save(im, "05_munich_1972.png")

# 06 연혁 자
im, d = canvas("⑥ 53년 자(尺): 넓혔다가, 좁혔다가, 예외를 냈다가, 거뒀다", "체육 분야 기준의 변천")
y = 330; d.line([(90, y), (1310, y)], fill=GRAY, width=5)
ev = [(100, "1973", "제정\n국가이익 특기자", LIGHT, INK), (280, "1981", "5개 대회 3위\n+ 한체대 10%", SAND, AMBER),
      (440, "1984", "우승자만", LIGHT, INK), (600, "1990", "올림픽 3위\nAG 1위 (현행)", MINT, GREEN),
      (780, "2002·06", "월드컵 16강\nWBC 4강 추가", PINK, RED), (940, "2007말", "둘 다 삭제", LIGHT, INK),
      (1100, "2020", "명단 전원\n편입", SAND, AMBER), (1260, "2026", "폐지 논의", PINK, RED)]
for i, (x, yr, txt, fill, col) in enumerate(ev):
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col)
    ctext(d, x, y - 60, yr, F_H, col)
    yy = y + 40 if i % 2 == 0 else y + 170
    box(d, (x - 85, yy, x + 85, yy + 110), fill, txt, F_S, INK)
box(d, (90, 640, 1310, 720), SAND, "넓힌 때는 서울올림픽 앞(1981)과 인기 종목 성과 뒤(2002·2006). 좁힌 때는 대회를 치른 뒤(1984·1990·2007).", F_S, INK)
foot(d, "근거: 시사오늘 옛날신문(조선 1973·경향 1981.8.13·1984.8.30·동아 1989.11.14·연합 2002.6.18·매경 2006.3.18), 한국일보 2021, 병무청 연혁.")
save(im, "06_ruler_53y.png")

# 07 분기 24시간 + 경고 5일
im, d = canvas("⑦ 복무 중 지켜야 할 것은 '분기 24시간', 어기면 '경고 + 5일'", "병역법 33조의10 — 경고가 벌칙의 전부라는 지적이 나온 자리")
for q in range(4):
    x = 100 + q * 300
    box(d, (x, 190, x + 260, 250), LIGHT, f"{q + 1}분기", F_H, INK)
    box(d, (x, 260, x + 260, 360), WHITE, "공익복무\n24시간 이상", F_B, INK, outline=GRAY)
d.text((100, 385), "× 34개월 = 544시간 (아동·청소년·취약계층 대상 특기 활용 활동)", font=F_S, fill=GRAY)
box(d, (100, 440, 640, 600), PINK, "못 채우면 → 경고\n경고 1회마다 복무 5일 연장\n미달 시간은 2배로 연장", F_B, RED)
box(d, (760, 440, 1300, 600), PINK, "허가 없이 광고·후원 겸직 → 경고\n(현역병이면 징계 사안)\n연장 뒤 1년 안에도 못 채우면 → 편입 취소", F_B, RED)
box(d, (100, 630, 1300, 700), SAND, "4년간 편입 173명 중 경고 110명, 취소 7명 (SBS 10.6, 병무청 자료)", F_B, INK)
foot(d, "근거: 병역법 33조의10 ②4·5호, ③, ④7호 원문. SBS 단독 2026.10.6(분기 24시간·173·110·7). 문화일보 10.7(취소 7명, 2022년 5·2023년 2).")
save(im, "07_quarter_24h.png")

# 08 야구 24명
im, d = canvas("⑧ 야구 대표팀 24명을 색으로 나누면", "미필 16 · 2023 항저우로 이미 편입 7 · 상무 복무 1")
def dots(d, x0, y0, n, col, per=8, gap=70, r=26):
    for i in range(n):
        cx = x0 + (i % per) * gap; cy = y0 + (i // per) * gap
        d.ellipse([cx, cy, cx + r * 2, cy + r * 2], fill=col)
dots(d, 120, 190, 16, AMBER); dots(d, 120, 190 + 2 * 70, 7, GREEN, per=8)
d.ellipse([120 + 7 * 70, 190 + 2 * 70, 120 + 7 * 70 + 52, 190 + 2 * 70 + 52], fill=GRAY)
box(d, (760, 190, 1310, 260), SAND, "16명 — 이번 금메달로 편입 대상", F_B, AMBER)
box(d, (760, 280, 1310, 350), MINT, "7명 — 항저우 금으로 이미 편입 (노시환 등)", F_B, GREEN)
box(d, (760, 370, 1310, 440), LIGHT, "1명 — 상무에서 복무 (조병현)", F_B, GRAY)
box(d, (90, 490, 1310, 620), WHITE, "슈퍼라운드 일본(전원 사회인 야구) 0-5 패 → 결승 3-1 승 → 5연패.\n'프로가 사회인 이기고 특례'라는 비판은 이 색칠에서 나온다.", F_B, INK, outline=GRAY)
box(d, (90, 650, 1310, 710), PINK, "비교: 2018 자카르타 야구는 24명 중 9명이 혜택 → 선동열 감독 국감 출석", F_S, RED)
foot(d, "근거: 에스콰이어 24명 명단(6.11), OSEN 9.27(16명), 대전일보 10.7(노시환 와일드카드·항저우 편입), 연합 9.25·9.27 경기 결과.")
save(im, "08_baseball_24.png")

# 09 축구 23명
im, d = canvas("⑨ 축구 대표팀 23명 중 20명", "군필 3명(이영준·이승원·김준홍)만 제외 — 결승 1-0 일본, 4연패")
dots(d, 120, 190, 20, AMBER, per=8); dots(d, 120 + 4 * 70, 190 + 2 * 70, 3, GRAY, per=8)
box(d, (760, 190, 1310, 260), SAND, "20명 — 편입 대상 (와일드카드 3명 포함)", F_B, AMBER)
box(d, (760, 280, 1310, 350), LIGHT, "3명 — 김천 상무에서 이미 마침", F_B, GRAY)
box(d, (760, 370, 1310, 470), WHITE, "상대 일본은 U-21, 와일드카드 0\n(2028 LA 올림픽 세대)", F_S, INK, outline=GRAY)
box(d, (90, 510, 1310, 640), PINK, "논란이 된 셋: 이기혁(주장·와일드카드) '군대 안 갑니다'\n양민혁 '군 면제 하나만 보고' · 박승수(19, 결승 16분) 전역모 사진", F_B, INK)
box(d, (90, 660, 1310, 720), MINT, "같은 혜택을 받은 2018 손흥민은 '태극기만 보면 가슴이 뭉클'이라고 말했다.", F_S, GREEN)
foot(d, "근거: 데일리안 7.9 명단(23명), SBS 10.4(군필 3명 제외 20명), 데일리안 7.31(일본 U-21·와일드카드 0), KBS 10.5.")
save(im, "09_football_23.png")

# 10 세 갈래
im, d = canvas("⑩ 국회·정부가 내놓은 길은 셋", "폐지(아시안게임 삭제) · 유지+기여금 · 정부의 단계 축소")
cols = [("주호영 (국민의힘) 10.7", "병역법 개정안\n아시안게임 1위 삭제\n올림픽 3위는 유지\n특별 공적자는 국회 추천 + 국무회의", PINK, RED),
        ("차규근 (조국혁신당) 10.2", "기여금 3법\n제도는 유지\n월 500만 원 초과 소득에 5~30%\n전액 군인복지기금", MINT, GREEN),
        ("정부 (국방부·문체부·병무청)", "'점진 축소 → 궁극 폐지'\n연구용역 11월 중순\n연내 개선안\n인정대회 축소·마일리지·문턱 상향", SAND, AMBER)]
x = 80
for t, s, fill, col in cols:
    box(d, (x, 180, x + 400, 250), fill, t, F_H, col)
    box(d, (x, 265, x + 400, 520), WHITE, s, F_S, INK, outline=col)
    x += 420
box(d, (90, 560, 1310, 660), LIGHT, "민주당 10.8: '정부안이 나오면 여야가 논의한다, 당 TF는 없다'\n신중론: 이재정 문체위원장·염태영 / 반대: 홍준표", F_S, INK)
foot(d, "근거: 스포티비·매일신문(주호영), 시사위크·서울의소리(차규근 의안 21746·21748), 국감 10.7, MBC 단독 10.6, 파이낸셜뉴스 10.8.")
save(im, "10_three_bills.png")

# 11 포인트제
im, d = canvas("⑪ 포인트제: 한 번의 금이 아니라 '쌓은 점수'로", "조계원·나경원·황명선 제안, 병무청 연구용역 검토 중 — 2018에도 나왔다가 무산")
jar = (420, 230, 980, 640)
d.rounded_rectangle(jar, radius=40, fill=WHITE, outline=INK, width=5)
coins = [("세계선수권 1위", AMBER, 560), ("아시안게임 금", (212, 175, 55), 480), ("올림픽 동", (176, 120, 70), 400), ("아시아선수권", (200, 200, 200), 320)]
for t, col, y in coins:
    d.rounded_rectangle([470, y, 930, y + 60], radius=30, fill=col)
    ctext(d, 700, y + 14, t, F_B, WHITE)
ctext(d, 700, 250, "기준 점수에 닿으면 편입", F_S, GRAY)
box(d, (90, 240, 380, 420), SAND, "장점\n단일 금메달 쏠림 완화\n대회 위상 반영", F_S, INK)
box(d, (1020, 240, 1310, 460), PINK, "왜 무산됐나(2018)\n종목별 가중치 합의 실패\n병무청 '특례 늘어난다' 반대\n하위 대회 반복 출전 편법", F_S, INK)
box(d, (90, 680, 1310, 740), LIGHT, "MBC 단독 10.6: '대회 규모·참가국 수를 고려하는 누적 점수제'를 정부도 검토", F_S, INK)
foot(d, "근거: 국감 10.7(조계원), 데일리안 10.7(나경원·황명선), SBS 10.4(2018 무산 이유), MBC 10.6.")
save(im, "11_point_jar.png")

# 12 해외 세 유형
im, d = canvas("⑫ 징병제 나라들은 세 가지로 갈린다", "메달로 복무 부담을 크게 줄이는 나라는 한국·대만·이란 정도")
cols = [("깎아준다", "한국 · 대만 · 이란\n\n대만: 보충병역 + 5년 관리\n이란: AG 금·은·동 전부 면제", PINK, RED),
        ("미룬다", "싱가포르 · 튀르키예 · 스위스\n\n스쿨링(리우 금) 2021 입대 2년\n튀르키예 35세, 스위스 34세까지", SAND, AMBER),
        ("같이 한다", "이스라엘 · 핀란드 · 오스트리아\n\n군 체육 시스템 안에서 훈련\n이스라엘: 기초훈련 뒤 하루 6시간 근무", MINT, GREEN)]
x = 80
for t, s, fill, col in cols:
    box(d, (x, 180, x + 400, 250), fill, t, F_H, col)
    box(d, (x, 265, x + 400, 520), WHITE, s, F_S, INK, outline=col)
    x += 420
box(d, (90, 560, 1310, 660), LIGHT, "대다수 나라는 면제 대신 포상금·연금으로 보답한다.\n한국의 대안 논의(입영 연기·상무 확대)는 가운데·오른쪽 유형으로 옮기자는 것.", F_S, INK)
foot(d, "근거: 엑스포츠뉴스 10.5, 데일리안 10.7, 연합 10.8 영상, 연합 [재점검]③ 10.10.")
save(im, "12_three_types.png")

# 13 여론 막대
im, d = canvas("⑬ 여론: 10명 중 6명이 '줄이거나 없애라'", "한길리서치, KNA25 의뢰, 10.5~6, 전국 18세 이상 1,500명 ARS, ±2.5%p")
bars = [("아시안게임은 빼고 올림픽만", 33.0, AMBER), ("올림픽·아시안게임 모두 폐지", 28.3, RED), ("현행 유지", 30.5, GREEN), ("기타·모름", 8.1, GRAY)]
y = 200
for t, v, col in bars:
    d.text((90, y + 8), t, font=F_B, fill=INK)
    d.rounded_rectangle([520, y, 520 + int(v * 20), y + 50], radius=12, fill=col)
    d.text((530 + int(v * 20), y + 8), f"{v}%", font=F_H, fill=col)
    y += 90
box(d, (90, 580, 1310, 690), SAND, "축소+폐지 = 61.3%. 성별·연령·정치성향 모두 60% 안팎으로 차이가 거의 없다.\n'전면 폐지'보다 '아시안게임만 빼자'가 가장 많다.", F_B, INK)
foot(d, "근거: 위키트리 2026.10.7 (응답률 4.6%). 조사 시점은 결승 직후 논란 한복판.")
save(im, "13_poll_bars.png")

# 14 청원 게이지
im, d = canvas("⑭ 국회 국민동의청원은 아직 1%", "'아시안게임 금메달리스트 예술·체육요원 병역특례 제도의 폐지에 관한 청원' — 10.11 직접 조회")
d.rounded_rectangle([90, 260, 1310, 340], radius=30, fill=LIGHT, outline=GRAY, width=3)
d.rounded_rectangle([90, 260, 90 + max(14, int(1220 * 536 / 50000)), 340], radius=30, fill=RED)
d.text((120, 360), "536명 (10.11)", font=F_H, fill=RED)
d.text((1080, 360), "50,000명 = 국방위 회부", font=F_S, fill=GRAY)
box(d, (90, 440, 640, 600), WHITE, "동의 기간\n2026.10.8 ~ 11.7 (30일)", F_B, INK, outline=GRAY)
box(d, (760, 440, 1310, 600), PINK, "기사에 나온 10.5 청원\n('예능, 체육인의 병역면제 폐지')은\n공개 목록에 없다 — 심사 중 또는 불수리", F_S, INK)
box(d, (90, 630, 1310, 700), SAND, "뉴스의 온도와 청원의 숫자는 다르다. 5만 명이 돼도 폐지가 아니라 '상임위 심사'다.", F_S, INK)
foot(d, "근거: petitions.assembly.go.kr 동의진행 청원 검색 '병역' (2026.10.11 저녁). 같은 분야 '여성징병제' 청원 1,508명.")
save(im, "14_petition_gauge.png")

# 15 이기혁의 9일
im, d = canvas("⑮ 이기혁의 9일 — 결승 10월 3일, 입영 예정 10월 12일", "'금메달 못 따면 9일 뒤 입대' / 규칙이 바뀌어도 이번 수혜자는 보호될 가능성이 높다")
days = list(range(1, 15))
for i, dd in enumerate(days):
    x = 90 + i * 87; y = 200
    fill = WHITE; col = INK
    if dd == 3: fill = AMBER; col = WHITE
    if dd == 12: fill = RED; col = WHITE
    if dd == 8: fill = LIGHT
    d.rounded_rectangle([x, y, x + 76, y + 76], radius=12, fill=fill, outline=GRAY)
    ctext(d, x + 38, y + 20, f"10/{dd}", F_S, col)
d.text((90 + 2 * 87, 290), "결승 1-0 일본\n'군대 안 갑니다'", font=F_S, fill=AMBER)
d.text((90 + 7 * 87 - 30, 290), "추천원서\n미접수(더팩트)", font=F_S, fill=GRAY)
d.text((90 + 11 * 87 - 40, 290), "입영 예정일\n(처리 미확인)", font=F_S, fill=RED)
box(d, (90, 400, 640, 600), MINT, "변호사·병무청 공통 의견\n'도장 전이라도 불이익 소급은\n신뢰보호원칙상 어렵다'\n→ 경과규정으로 보호가 통례", F_S, GREEN)
box(d, (760, 400, 1310, 600), SAND, "선례: 2002 월드컵은 혜택을 '늘리는' 쪽으로\n4강 직후 시행령을 고쳐 바로 적용\n'줄이는' 쪽 즉시 적용은 전례 없음", F_S, INK)
box(d, (90, 630, 1310, 700), LIGHT, "그래서 바뀐 규칙은 다음 대회부터. 이번 57명(또는 43명)은 현행대로 갈 가능성이 높다.", F_S, INK)
foot(d, "근거: KBS 10.4 인터뷰, 더팩트 10.8, 채널A 10.7(병무청·조현삼), JTV 법썰전 10.9, 뉴시스 10.8(박세정).")
save(im, "15_nine_days.png")

# 16 병역자원 선
im, d = canvas("16) 1973년과 2026년은 조건이 정반대다", "그때는 병력이 남았고, 지금은 모자란다")
d.line([(150, 600), (1250, 600)], fill=GRAY, width=3); d.line([(150, 600), (150, 180)], fill=GRAY, width=3)
pts = [(250, 240, "1970년대\n입영가능 30만+\n(입영 17~18만)"), (650, 330, "2015\n20세 남성 37.2만"), (1050, 500, "2025\n20세 남성 22.5만")]
for i in range(len(pts) - 1):
    d.line([pts[i][:2], pts[i + 1][:2]], fill=RED, width=6)
for x, y, t in pts:
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=RED)
    d.text((x + 20 if x < 400 else x - 90, y - 100 if x < 1000 else y + 20), t, font=F_S, fill=INK)
box(d, (760, 180, 1310, 280), PINK, "상비병력 63.9만(2012) → 50만(2022)\n→ 2030년대 30만 명대 전망", F_S, RED)
box(d, (90, 650, 1310, 720), SAND, "1973: 병력 과잉 + 국위선양 → 특례 신설.   2026: 병력 절벽 + 공정 → 국방부가 먼저 '폐지'.", F_B, INK)
foot(d, "근거: 연합 [재점검]① 10.10 (KIDA 추계·국방백서), 연합 10.8 영상(45만→30만대 전망).")
save(im, "16_manpower_line.png")
print("done")
