# -*- coding: utf-8 -*-
"""「도시 야생동물 이입」 인포그래픽 12장. 숫자는 이입_공부노트_2026-10-11.md 에서 확인한 것만."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_X, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)
F_M = font(24, True); F_BIG = font(64, True); F_MID = font(34, True)
DIM = (205, 205, 200); BROWN = (150, 100, 60); SHARK = (110, 120, 135); PANDA = (40, 40, 40); PURPLE = (120, 80, 200)

def person(d, cx, top, h, col):
    r = h * 0.17
    d.ellipse([cx - r, top, cx + r, top + 2 * r], fill=col)
    bw = h * 0.42
    d.rounded_rectangle([cx - bw / 2, top + 2 * r + h * 0.05, cx + bw / 2, top + h], radius=int(bw / 2), fill=col)

def vbar(d, x, base, w, hgt, col, label=None, value=None, f=F_S, vf=None):
    d.rounded_rectangle([x, base - hgt, x + w, base], radius=8, fill=col)
    if value: ctext(d, x + w / 2, base - hgt - 30, value, vf or F_M, col if col != DIM else GRAY)
    if label: ctext(d, x + w / 2, base + 8, label, f, GRAY)

def donut(d, cx, cy, r, frac, col, col2, label, sub):
    d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=col)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], -90 + 360 * frac, 270, fill=col2)
    d.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6], fill=BG)
    ctext(d, cx, cy - 22, label, F_H, col); ctext(d, cx, cy + 14, sub, F_S, GRAY)

def tag(d, x, y, w, text, col):
    """이름표: 둥근 사각 + 구멍."""
    d.rounded_rectangle([x, y, x + w, y + 54], radius=12, fill=WHITE, outline=col, width=4)
    d.ellipse([x + 10, y + 19, x + 26, y + 35], fill=col)
    d.text((x + 38, y + 11), text, font=F_H, fill=col)

def otter(d, cx, cy, s=1.0):
    d.ellipse([cx - 40 * s, cy - 40 * s, cx + 40 * s, cy + 40 * s], fill=BROWN)
    d.ellipse([cx - 34 * s, cy - 50 * s, cx - 10 * s, cy - 26 * s], fill=BROWN); d.ellipse([cx + 10 * s, cy - 50 * s, cx + 34 * s, cy - 26 * s], fill=BROWN)
    d.ellipse([cx - 22 * s, cy - 6 * s, cx + 22 * s, cy + 30 * s], fill=(235, 210, 170))
    for dx in (-14, 14): d.ellipse([cx + dx * s - 6 * s, cy - 14 * s, cx + dx * s + 6 * s, cy - 2 * s], fill=INK)
    d.ellipse([cx - 6 * s, cy + 2 * s, cx + 6 * s, cy + 12 * s], fill=INK)
    for dy in (6, 14):
        d.line([cx - 10 * s, cy + dy * s, cx - 46 * s, cy + (dy - 4) * s], fill=INK, width=2); d.line([cx + 10 * s, cy + dy * s, cx + 46 * s, cy + (dy - 4) * s], fill=INK, width=2)
def shark(d, cx, cy, s=1.0):
    d.ellipse([cx - 70 * s, cy - 28 * s, cx + 50 * s, cy + 28 * s], fill=SHARK)
    d.polygon([(cx - 10 * s, cy - 24 * s), (cx + 10 * s, cy - 62 * s), (cx + 24 * s, cy - 24 * s)], fill=SHARK)
    d.polygon([(cx + 46 * s, cy), (cx + 80 * s, cy - 30 * s), (cx + 80 * s, cy + 30 * s)], fill=SHARK)
    d.ellipse([cx - 50 * s, cy - 12 * s, cx - 38 * s, cy], fill=WHITE); d.ellipse([cx - 47 * s, cy - 9 * s, cx - 41 * s, cy - 3 * s], fill=INK)
def panda(d, cx, cy, s=1.0):
    d.ellipse([cx - 40 * s, cy - 40 * s, cx + 40 * s, cy + 40 * s], fill=WHITE, outline=(200, 200, 200), width=2)
    d.ellipse([cx - 44 * s, cy - 52 * s, cx - 16 * s, cy - 24 * s], fill=PANDA); d.ellipse([cx + 16 * s, cy - 52 * s, cx + 44 * s, cy - 24 * s], fill=PANDA)
    for dx in (-16, 16): d.ellipse([cx + dx * s - 13 * s, cy - 18 * s, cx + dx * s + 13 * s, cy + 6 * s], fill=PANDA)
    for dx in (-16, 16): d.ellipse([cx + dx * s - 4 * s, cy - 10 * s, cx + dx * s + 4 * s, cy - 2 * s], fill=WHITE)
    d.ellipse([cx - 6 * s, cy + 8 * s, cx + 6 * s, cy + 18 * s], fill=PANDA)

# ---------- D1 세 마리 ----------
im, d = canvas("세 마리가 같은 가을에 왔다 — 상어, 수달, 그리고 떠난 판다", "부산 북항 흑상어 「부캉이」 · 온천천 수달 「온처니」 · 에버랜드 「푸바오」. 숫자는 집계 기관·보도 기준")
cols3 = [("온처니", "온천천 수달", otter, GREEN, "10.5", "「이 친구도 이름\n지어주세요」(스레드)", "검색 월 3,660"),
         ("부캉이", "북항 흑상어 3m", shark, SHARK, "9.18", "꺾인 수로에 갇힘\n구조 2회 실패", "누적 134.9만 명"),
         ("푸바오", "에버랜드 판다", panda, PANDA, "2024.4.3", "중국 반환\n빗속 배웅", "6,000명 · 굿즈 270만")]
for i, (n, sp, ic, col, dt, s1, big) in enumerate(cols3):
    x0 = 80 + i * 410
    d.rounded_rectangle([x0, 160, x0 + 390, 690], radius=20, fill=WHITE, outline=col, width=3)
    ic(d, x0 + 195, 270, 1.1 if ic is not shark else 1.0)
    tag(d, x0 + 95, 360, 200, n, col)
    ctext(d, x0 + 195, 430, sp, F_S, GRAY)
    ctext(d, x0 + 195, 470, dt, F_M, col)
    for k, ln in enumerate(s1.split("\n")): ctext(d, x0 + 195, 505 + k * 28, ln, F_S, INK)
    d.line([x0 + 40, 580, x0 + 350, 580], fill=DIM, width=2)
    ctext(d, x0 + 195, 600, big, F_H, col)
foot(d, "근거: 부산시설공단 집계(한경 2026.10.11), 데일리안 2026.10.8, fn 2024.4.3, 한국일보 2024.3.3. 그림은 캐릭터 모식도.")
save(im, "D1_three_cases.png")

# ---------- D2 방문객 곡선 ----------
im, d = canvas("상어 한 마리에 134만 명 — 24일 동안 쌓인 방문객", "부산시설공단 집계(누적, 만 명). 9.18 발견 → 10.11 18시")
pts = [(0, 0.0), (1, 0.8), (6, 10), (9, 48.3), (15, 81), (19, 100), (21, 120.3), (22, 127.6), (23, 134.9)]
ox, oy, ex, top = 140, 600, 1180, 200
def X(dd): return ox + dd / 23 * (ex - ox)
def Y(v): return oy - v / 140 * (oy - top)
for v in (0, 50, 100):
    d.line([ox, Y(v), ex, Y(v)], fill=(220, 220, 215), width=2); d.text((ox - 70, Y(v) - 12), f"{v}만", font=F_S, fill=GRAY)
d.line([(X(a), Y(b)) for a, b in pts], fill=BLUE, width=7, joint="curve")
for a, b in pts: d.ellipse([X(a) - 7, Y(b) - 7, X(a) + 7, Y(b) + 7], fill=BLUE)
ctext(d, X(23), Y(134.9) - 40, "134.9만", F_H, BLUE); d.text((X(9) + 16, Y(48.3) + 6), "추석 4일 48.3만", font=F_S, fill=BLUE); ctext(d, X(19), Y(100) - 36, "100만", F_M, BLUE)
for dd, lab in ((0, "9.18"), (9, "9.27"), (15, "10.3"), (23, "10.11")): ctext(d, X(dd), oy + 10, lab, F_S, GRAY)
for dd, lab, yy in ((11, "9.29 1차 구조 실패", 130), (14, "10.2 2차 실패 → 그물 철거", 118)):
    d.line([X(dd), Y(0), X(dd), Y(yy)], fill=RED, width=2); d.text((X(dd) + 6, Y(yy) - 26), lab, font=F_S, fill=RED)
box(d, (90, 640, 1310, 700), SAND, "구조에 두 번 실패하고 「지켜보기」로 바뀐 뒤에도 하루 7만 명이 왔다. 개천절 연휴 26.4만, 한글날 연휴 20.5만.", F_S, INK)
foot(d, "근거: 한경 2026.10.11·10.9, 머니투데이 10.10, fn 10.3(16일 81만), 경기일보 10.3. 중간 점은 보도일 기준, 선은 보간.")
save(im, "D2_visitor_curve.png")

# ---------- D3 귀여움 차선 ----------
im, d = canvas("「귀여움」은 수달·판다의 길이지 상어의 길이 아니다", "로렌츠 베이비 스키마(1943) → Glocker 2009 → Nittono 2012. 얼굴은 모식도")
d.text((80, 160), "베이비 스키마 — 큰 눈 · 둥근 얼굴 · 짧은 팔다리", font=F_M, fill=INK)
otter(d, 190, 300, 1.2); panda(d, 400, 300, 1.2); shark(d, 640, 300, 1.1)
ctext(d, 190, 380, "수달 ○", F_H, GREEN); ctext(d, 400, 380, "판다 ○", F_H, GREEN); ctext(d, 640, 380, "상어 X", F_H, RED)
d.text((80, 425), "Glocker 2009: 아기 얼굴의 눈·이마를 키우면", font=F_S, fill=GRAY)
d.text((80, 452), "귀여움과 돌봄 동기가 같이 올랐다(대학생 122명)", font=F_S, fill=GRAY)
d.text((80, 479), "fMRI에선 보상 회로가 켜진다(16명). 상어 얼굴엔 이 스위치가 없다", font=F_S, fill=GRAY)
# 니토노 막대
d.text((820, 160), "귀여운 사진을 본 뒤 정밀 작업 성적(Nittono 2012)", font=F_M, fill=INK)
vbar(d, 880, 440, 120, 44 * 5, GREEN, "새끼 동물", "+43.9%")
vbar(d, 1080, 440, 120, 12 * 5, DIM, "성체 동물", "+11.9%")
d.text((820, 470), "완료 시간도 +12%: 더 천천히, 더 조심스럽게", font=F_S, fill=GRAY)
box(d, (90, 540, 1310, 690), SAND, "그런데 134만 명이 간 건 상어다.\n귀여움은 가속 페달이지 엔진이 아니다 — 엔진은 다음 네 칸.", F_B, INK)
foot(d, "근거: Glocker 외 2009 Ethology 115 · PNAS 106, Nittono 외 2012 PLoS ONE 7(e46362), Sherman·Haidt 2011. 사진 자극은 강아지·고양이.")
save(im, "D3_cute_lane.png")

# ---------- D4 네 칸 ----------
im, d = canvas("상어까지 묶는 네 칸 — 이름 · 사연 · 어긋난 자리 · 같이 보기", "열 사례(국내 4 · 해외 6)를 거꾸로 돌려 뽑은 것. 이 글의 가설")
def ic_tag(cx, cy): tag(d, cx - 100, cy - 27, 200, "이름표", BLUE)
def ic_trap(cx, cy):
    d.rectangle([cx - 90, cy - 20, cx + 90, cy + 40], fill=(200, 215, 235)); d.rectangle([cx - 100, cy - 30, cx - 86, cy + 40], fill=GRAY); d.rectangle([cx + 86, cy - 30, cx + 100, cy + 40], fill=GRAY)
    shark(d, cx, cy + 5, 0.8)
def ic_city(cx, cy):
    for k, hh in enumerate((60, 90, 70, 110, 80)): d.rectangle([cx - 100 + k * 40, cy + 40 - hh, cx - 70 + k * 40, cy + 40], fill=DIM)
    d.ellipse([cx - 30, cy - 70, cx + 30, cy - 10], fill=AMBER); ctext(d, cx, cy - 58, "?", F_H, WHITE)
def ic_crowd(cx, cy):
    for r in range(2):
        for k in range(6): person(d, cx - 90 + k * 36 + r * 10, cy - 40 + r * 40, 50, RED)
cards = [("① 이름", ic_tag, "한 마리가 「개체」가 된다", "온처니는 「이름 지어주세요」로 시작"),
         ("② 사연", ic_trap, "갇힘 · 길 잃음 · 떠남", "81%가 약자를 응원(1991)"),
         ("③ 어긋난 자리", ic_city, "도심에 야생 = 신기함·경외", "「왜 안 나가지?」 설명 욕구"),
         ("④ 같이 보기", ic_crowd, "군중 · 공인 · 굿즈", "홍보대사 투표 91% 찬성")]
for i, (t, ic, s1, s2) in enumerate(cards):
    x0 = 80 + i * 310
    d.rounded_rectangle([x0, 160, x0 + 290, 640], radius=18, fill=WHITE, outline=INK, width=2)
    ic(x0 + 145, 260)
    ctext(d, x0 + 145, 350, t, F_H, INK)
    ctext(d, x0 + 145, 400, s1, F_S, INK)
    d.line([x0 + 30, 450, x0 + 260, 450], fill=DIM, width=2)
    ws = s2.split(" "); m = (len(ws) + 1) // 2
    ctext(d, x0 + 145, 470, " ".join(ws[:m]), F_S, GRAY); ctext(d, x0 + 145, 498, " ".join(ws[m:]), F_S, GRAY)
    ctext(d, x0 + 145, 570, "귀여움 없어도 돈다", F_M, GREEN)
d.text((80, 665), "귀여움은 ①~④를 더 빨리 돌리는 페달. 수달·판다는 페달까지 있고, 상어는 네 칸만으로 134만 명을 모았다.", font=F_S, fill=INK)
foot(d, "근거: 공부노트 2장. Jaric 2023(flagship individuals: 개체 특성·종·접촉·운명), Epley 2007(설명 욕구), Frazier·Snyder 1991.")
save(im, "D4_four_conditions.png")

# ---------- D5 이름의 순간 ----------
im, d = canvas("이름이 붙은 다음 날부터 숫자가 뛴다", "세 사례의 「이름 → 첫 숫자」와, 이름 있는 송아지 실험")
rows = [("부캉이", "9.18 발견 → 다음 날", "8,000명", SHARK), ("온처니", "10.5 「이름 지어주세요」 → 10.8", "YTN·데일리안 등 보도", GREEN), ("푸바오", "2020.11.4 이름 발표 → 2023", "연 215만 명(2배)", PANDA)]
y = 165
for n, s, big, col in rows:
    tag(d, 80, y, 220, n, col)
    arrow(d, (320, y + 27), (380, y + 27), col, 5)
    d.text((395, y + 2), s, font=F_S, fill=GRAY); d.text((395, y + 28), big, font=F_H, fill=col)
    y += 100
# Lucky 실험
d.text((820, 165), "이름 있는 송아지 vs 이름 없는 송아지들", font=F_M, fill=INK)
vbar(d, 880, 440, 130, 26 * 8, BLUE, "「Lucky」", "26%")
vbar(d, 1080, 440, 130, 13 * 8, DIM, "이름 없음", "13%")
d.text((820, 500), "실제 청원에 서명한 비율(3개 연구 중 1차)", font=F_S, fill=GRAY)
box(d, (90, 540, 1310, 690), SAND, "「한 명의 얼굴이 숫자보다 세다」는 식별 가능 피해자 효과는 2023년 메타분석에서 거의 0으로 나왔다.\n그래서 이 칸은 「효과가 있다」가 아니라 「이름이 붙어야 다음 칸(사연·같이 보기)이 돌아간다」로 읽는다.", F_S, INK)
foot(d, "근거: 한경 10.11(다음 날 8,000명), 데일리안 10.8, 한국일보 2024.3.3, Faunalytics(Lucky), Maier·Wong·Feldman 2023(r=0.002).")
save(im, "D5_name_moment.png")

# ---------- D6 약자 응원 ----------
im, d = canvas("우리는 약자를 응원한다 — 81%, 그리고 「그냥 두자」 71%", "Frazier·Snyder 1991(가상 7전 시리즈) · 부캉이 온라인 조사(381명, 10.1~7)")
d.text((80, 160), "강팀이 유력한 시리즈에서 누구를 응원하나", font=F_M, fill=INK)
for i in range(10): person(d, 120 + i * 60, 200, 110, GREEN if i < 8 else DIM)
d.text((100, 330), "81%가 약체", font=F_H, fill=GREEN); d.text((360, 330), "약체가 3연승하자 그중 절반이 강팀으로 옮겼다", font=F_S, fill=GRAY)
donut(d, 1000, 300, 110, 0.71, GREEN, DIM, "71%", "그냥 두자")
d.text((840, 430), "구조해야 29% · 응원 메시지 1위 「억수로 고맙데이」", font=F_S, fill=GRAY)
d.text((840, 456), "※ 특정 채널 이용자 381명, 전체 여론 아님", font=F_S, fill=RED)
box(d, (90, 520, 1310, 690), SAND, "꺾인 수로에서 못 나가는 상어, 탈출했지만 도시에서 버틴 부엉이, 길 잃은 바다코끼리, 떠나야 하는 판다.\n사연이 「약자」일 때 응원이 붙는다. 귀엽지 않아도 된다.", F_S, INK)
foot(d, "근거: Frazier·Snyder 1991 SSJ 8(대학생 100여 명), Vandello 외 2007 PSPB 33, 머니투데이 2026.10.10.")
save(im, "D6_underdog.png")

# ---------- D7 어긋난 자리 — 배경 숫자 ----------
im, d = canvas("도시에서 야생을 만날 확률이 올라갔다", "동해안 대형 상어 · 한강 수달 · 전국 야생동물 구조. 집계 기관 기준")
d.text((80, 160), "동해안 대형 상어 출현(건)", font=F_M, fill=INK)
for i, (yr, v) in enumerate([("2022", 1), ("2023", 29), ("2024", 44), ("2026\n1~8월", 73)]):
    vbar(d, 110 + i * 110, 480, 80, v * 3.6, SHARK if i < 3 else RED, None, str(v))
    ctext(d, 150 + i * 110, 488, yr.split("\n")[0], F_S, GRAY)
    if "\n" in yr: ctext(d, 150 + i * 110, 512, yr.split("\n")[1], F_S, GRAY)
d.text((80, 545), "표층 수온 1968~2025년 +1.6도(전 지구 +0.76도)", font=F_S, fill=GRAY)
d.text((600, 160), "한강 수달(마리)", font=F_M, fill=INK)
vbar(d, 640, 480, 90, 15 * 10, DIM, None, "15"); vbar(d, 770, 480, 90, 27 * 10, GREEN, None, "27")
ctext(d, 685, 488, "2022", F_S, GRAY); ctext(d, 685, 512, "서울시", F_S, GRAY); ctext(d, 815, 488, "2026", F_S, GRAY); ctext(d, 815, 512, "생물자원관", F_S, GRAY)
d.text((600, 545), "분변 106점 DNA · 다섯 가족", font=F_S, fill=GRAY)
d.text((960, 160), "야생동물 구조(마리)", font=F_M, fill=INK)
vbar(d, 1000, 480, 90, 14190 / 80, DIM, "2019", "14,190"); vbar(d, 1130, 480, 90, 20408 / 80, AMBER, "2023", "20,408")
d.text((960, 545), "전국 17개 센터, 4년 새 +43.8%", font=F_S, fill=GRAY)
box(d, (90, 600, 1310, 690), SAND, "「왜 저게 여기 있지?」 — 거대함 + 설명이 안 됨 = 경외(Keltner·Haidt 2003). 그 확률이 해마다 커진다.", F_S, INK)
foot(d, "근거: 경향 2025.4.24·한국일보 2026.9.24(수과원), 뉴시스 2026.9.2(생물자원관), 환경부 2024 발표. 2019 구조 수는 역산.")
save(im, "D7_out_of_place.png")

# ---------- D8 같이 보기 사다리 ----------
im, d = canvas("사적인 마음이 공적인 사실이 되는 사다리", "이름 → 군중 → 공인 → 기념. 다섯 사례")
steps = [("이름", "시민·누리꾼", BLUE), ("군중", "부캉이 134.9만\n다마짱 하루 1,000명+", AMBER), ("공인", "홍보대사(91%)\n특별주민표(2003)", GREEN), ("기념", "프레이야 동상\n27만 크로네", PURPLE)]
for i, (t, s, col) in enumerate(steps):
    x0 = 100 + i * 300; y0 = 470 - i * 90
    d.rounded_rectangle([x0, y0, x0 + 270, y0 + 70], radius=14, fill=col); ctext(d, x0 + 135, y0 + 18, t, F_H, WHITE)
    for k, ln in enumerate(s.split("\n")): ctext(d, x0 + 135, y0 + 85 + k * 28, ln, F_S, INK)
    if i < 3: arrow(d, (x0 + 280, y0 + 35), (x0 + 300, y0 - 55), GRAY, 4)
box(d, (90, 630, 1310, 700), SAND, "세실의 죽음(2015)은 미디어 하루 9만 9천 건 — 관심은 「관심이 있다는 신호」를 먹고 자란다(지난 글의 정보 폭포).", F_S, INK)
foot(d, "근거: 부산시설공단(한경 10.11), 일본 국토교통성 백서 2002, 시코쿠신문 2003.2.6, NPR 2023.5.1, Macdonald 외 2016 Animals 6(5).")
save(im, "D8_public_ladder.png")

# ---------- D9 사람 쪽 ----------
im, d = canvas("보는 쪽의 사정 — 혼자 사는 집이 역대 최고인 해", "국가데이터처 「2025 통계로 보는 1인가구」(2025.12.9). 원인 증명이 아니라 배경")
d.text((80, 160), "열 집 중 1인 가구", font=F_M, fill=INK)
for i in range(10):
    x = 100 + i * 62; col = BLUE if i < 3 else (BLUE if i == 3 and False else DIM)
    d.polygon([(x, 230), (x + 25, 205), (x + 50, 230)], fill=col); d.rectangle([x + 5, 230, x + 45, 275], fill=col)
d.rectangle([100 + 3 * 62 + 5, 230, 100 + 3 * 62 + 5 + 40 * 0.61, 275], fill=BLUE)
d.text((100, 295), "36.1% · 804.5만 가구", font=F_H, fill=BLUE)
donut(d, 1000, 290, 110, 0.489, RED, DIM, "48.9%", "외롭다")
d.text((820, 420), "1인 가구 중 「자주 또는 가끔 외롭다」(전체 가구 38.2%)", font=F_S, fill=GRAY)
box(d, (90, 480, 1310, 600), WHITE, "이론: 사람과 연결이 부족할수록 동물·사물에 마음을 부여한다(Epley 2007 의인화 3요인 중 「연결 동기」).\n2008년 실험은 외로움을 유도하면 반려동물 의인화가 늘었다고 했지만, 2020년대 885명 재현은 「약하거나 없음」.", F_S, INK, outline=GRAY)
box(d, (90, 620, 1310, 690), SAND, "그래서 이 글은 「외로워서 본다」라고 쓰지 않는다. 「혼자 사는 집이 가장 많은 해에, 같이 볼 거리가 생겼다」까지만.", F_S, INK)
foot(d, "근거: 경향 2025.12.9, Epley·Waytz·Cacioppo 2007 Psych Rev 114, Epley 외 2008 Psych Sci 19, Bartz 2016, PCI RR 등록보고서.")
save(im, "D9_loneliness.png")

# ---------- D10 이름의 주인 ----------
im, d = canvas("이름의 주인은 셋 다 다르다 — 특허청 직접 조회", "KIPRIS 2026.10.11. 출원 = 신청, 등록 = 권리")
rows = [("부캉이", SHARK, "9.18 발견", "9.22 · 9.25 · 9.26 개인 3명 출원(완구·열쇠고리·빵)", "부산시 10월 중 공공 브랜드 출원 예정 · 공단 「검토한 바 없다」"),
        ("푸바오", PANDA, "2020.7.20 출생", "9.18 삼성물산 출원 ← 이름 투표(9.22~10.11) 시작 4일 전", "11.4 이름 발표 → 2021.11 등록, 관련 상표 1,526건"),
        ("온처니", GREEN, "10.5 이름 요청", "출원 0건", "아무도 주인이 아니다(10.11 기준)")]
y = 165
for n, col, a, b, c in rows:
    tag(d, 80, y + 10, 200, n, col)
    d.rounded_rectangle([310, y, 1320, y + 130], radius=14, fill=WHITE, outline=col, width=3)
    d.text((330, y + 12), a, font=F_M, fill=GRAY); d.text((330, y + 48), b, font=F_B, fill=INK); d.text((330, y + 90), c, font=F_S, fill=GRAY)
    y += 150
box(d, (90, 625, 1310, 695), SAND, "개인 출원은 심사(6개월~1년)에서 「부정한 목적」 조항으로 걸릴 수 있다 — 2020년 펭수 선점 출원은 전부 거절됐다(보도).", F_S, INK)
foot(d, "근거: KIPRIS 4020260199461·4020260201875·4020260201995·4020200167216 직접 조회, fn 2026.9.29, 서울신문 10.2, 데일리안 2020.11.4. 개인 이름은 쓰지 않는다.")
save(im, "D10_name_owner.png")

# ---------- D11 그늘 ----------
im, d = canvas("이입의 그늘 — 사랑이 동물을 위험하게 만드는 네 가지", "실제 일어난 일만")
items = [("거리 안 지키기", "프레이야(2022): 군중이 거리 두기 무시\n→ 안락사", RED),
         ("먹이 주기 · 난간 넘기", "부캉이: 먹이 투척, 휴대폰 주우러\n난간 넘은 시민", AMBER),
         ("위치 퍼뜨리기", "「온천천 수달 위치」 검색 월 760건\n천연기념물 접근 금지", GREEN),
         ("마음대로 서사 붙이기", "세로(2023) 「외로워서 탈출」\n→ 의인화 소비 비판", PURPLE)]
for i, (t, s, col) in enumerate(items):
    x0 = 80 + (i % 2) * 620; y0 = 165 + (i // 2) * 215
    d.rounded_rectangle([x0, y0, x0 + 600, y0 + 190], radius=16, fill=WHITE, outline=col, width=3)
    d.ellipse([x0 + 24, y0 + 24, x0 + 84, y0 + 84], fill=col); ctext(d, x0 + 54, y0 + 36, "!", F_H, WHITE)
    d.text((x0 + 104, y0 + 30), t, font=F_H, fill=col)
    for k, ln in enumerate(s.split("\n")): d.text((x0 + 104, y0 + 90 + k * 30), ln, font=F_S, fill=INK)
box(d, (90, 610, 1310, 690), SAND, "이름은 한 마리에 관심을 모으고, 그 종 전체(수달·상어)는 가린다(Auster 2023). 관심이 보호가 되려면 거리가 필요하다.", F_S, INK)
foot(d, "근거: CBS·AFP 2022.8.14, 머니투데이 2026.10.10, title_check 2026.10.11, 경향 2023.4.3 칼럼, Auster 외 2023 People and Nature.")
save(im, "D11_shadow.png")

# ---------- D12 할 일 하나 (10.12 수정: 거리감) ----------
im, d = canvas("오늘 할 일 하나 — 좋아하는 만큼, 한 걸음 뒤에서", "보고 싶은 마음은 그대로. 다만 그 친구에게 가장 좋은 자리는 우리와 조금 떨어진 곳이다")
# 산책로와 물: 사람은 난간 뒤, 동물은 물속. 사이에 빈 거리
box(d, (640, 150, 1320, 230), WHITE, "프레이야는 사람들이 너무 가까이 가서 떠났다(2022)", F_B, INK, outline=RED)
box(d, (640, 242, 1320, 322), WHITE, "수달은 천연기념물이라 가까이 가는 것도 법이 막는다", F_B, INK, outline=GREEN)
d.rounded_rectangle([80, 445, 1320, 700], radius=0, fill=(200, 225, 240))          # 물
d.rectangle([80, 405, 1320, 445], fill=(225, 220, 205))                              # 산책로
d.line([80, 405, 1320, 405], fill=GRAY, width=6)                                      # 난간
for x in range(120, 1320, 120): d.line([x, 405, x, 340], fill=GRAY, width=5)
d.line([80, 340, 1320, 340], fill=GRAY, width=6)
person(d, 260, 205, 200, INK); person(d, 340, 225, 180, INK); person(d, 420, 205, 200, INK)
shark(d, 980, 570, 1.6); otter(d, 1180, 630, 1.1)
# 거리 표시
d.line([470, 490, 860, 490], fill=RED, width=4); d.polygon([(860, 490), (840, 480), (840, 500)], fill=RED); d.polygon([(470, 490), (490, 480), (490, 500)], fill=RED)
ctext(d, 665, 500, "이만큼", F_M, RED)
box(d, (90, 600, 600, 690), SAND, "이름도, 마음도 그대로.\n보는 자리만 한 걸음 뒤에서.", F_B, INK)
foot(d, "근거: CBS 2022(프레이야), 국가유산청(수달 천연기념물 1982), 머니투데이 10.10(부캉이 난간·먹이). 장면은 모식도.")
save(im, "D12_todo.png")
print("done_wild")
