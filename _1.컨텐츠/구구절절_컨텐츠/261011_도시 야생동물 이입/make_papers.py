# -*- coding: utf-8 -*-
"""「도시 야생동물 이입」 — 논문 보강 그림 6장(2026-10-14).
숫자는 이입_논문노트_국내_2026-10-14.md · 이입_논문노트_해외_2026-10-14.md · 이입_공부노트_2026-10-11.md 확인분만.
그림이 앞, 그림 안 글자는 제목·라벨·큰 숫자·아래 상자 두 줄(구구절절 지침 3장)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "make_infographics.py"), encoding="utf-8").read()
exec(_src[:_src.index("# ---------- D1")])
F_SM = font(18); F_L = font(28, True); F_HUGE = font(72, True)
NAVY = (40, 60, 110); SEAL = (150, 140, 125); COYOTE = (170, 140, 100); HERON = (245, 245, 245)

def calf(d, cx, cy, s=1.0, col=(200, 160, 120)):
    d.ellipse([cx - 34 * s, cy - 18 * s, cx + 30 * s, cy + 20 * s], fill=col)
    d.ellipse([cx + 18 * s, cy - 34 * s, cx + 46 * s, cy - 6 * s], fill=col)
    d.ellipse([cx + 14 * s, cy - 40 * s, cx + 24 * s, cy - 30 * s], fill=col); d.ellipse([cx + 40 * s, cy - 40 * s, cx + 50 * s, cy - 30 * s], fill=col)
    for lx in (-24, -8, 8, 22): d.rectangle([cx + lx * s, cy + 14 * s, cx + (lx + 6) * s, cy + 36 * s], fill=col)
    d.ellipse([cx + 32 * s, cy - 24 * s, cx + 37 * s, cy - 19 * s], fill=INK)
def mini_tag(d, x, y, text, col=BLUE):
    w = d.textlength(text, font=F_SM) + 30
    d.rounded_rectangle([x, y, x + w, y + 28], radius=8, fill=WHITE, outline=col, width=3)
    d.ellipse([x + 7, y + 10, x + 15, y + 18], fill=col); d.text((x + 20, y + 3), text, font=F_SM, fill=col)
def seal(d, cx, cy, s=1.0):
    d.ellipse([cx - 70 * s, cy - 26 * s, cx + 40 * s, cy + 26 * s], fill=SEAL)
    d.ellipse([cx + 20 * s, cy - 42 * s, cx + 72 * s, cy + 6 * s], fill=SEAL)
    d.ellipse([cx + 50 * s, cy - 28 * s, cx + 58 * s, cy - 20 * s], fill=INK)
    for k in range(3): d.line([cx + 62 * s, cy - 14 * s + k * 5 * s, cx + 86 * s, cy - 18 * s + k * 7 * s], fill=INK, width=2)
    d.polygon([(cx - 66 * s, cy), (cx - 96 * s, cy - 20 * s), (cx - 96 * s, cy + 20 * s)], fill=SEAL)
def coyote(d, cx, cy, s=1.0):
    d.ellipse([cx - 40 * s, cy - 16 * s, cx + 30 * s, cy + 16 * s], fill=COYOTE)
    d.polygon([(cx + 20 * s, cy - 12 * s), (cx + 56 * s, cy - 20 * s), (cx + 40 * s, cy + 4 * s)], fill=COYOTE)
    d.polygon([(cx + 30 * s, cy - 16 * s), (cx + 36 * s, cy - 40 * s), (cx + 44 * s, cy - 18 * s)], fill=COYOTE)
    for lx in (-30, -16, 10, 22): d.rectangle([cx + lx * s, cy + 10 * s, cx + (lx + 5) * s, cy + 36 * s], fill=COYOTE)
    d.polygon([(cx - 38 * s, cy - 6 * s), (cx - 70 * s, cy + 10 * s), (cx - 40 * s, cy + 8 * s)], fill=COYOTE)
def heron(d, cx, cy, s=1.0):
    d.ellipse([cx - 26 * s, cy - 14 * s, cx + 20 * s, cy + 14 * s], fill=HERON, outline=GRAY, width=2)
    d.line([cx + 12 * s, cy - 8 * s, cx + 22 * s, cy - 44 * s], fill=GRAY, width=int(5 * s))
    d.ellipse([cx + 14 * s, cy - 54 * s, cx + 32 * s, cy - 40 * s], fill=HERON, outline=GRAY, width=2)
    d.polygon([(cx + 30 * s, cy - 49 * s), (cx + 54 * s, cy - 46 * s), (cx + 30 * s, cy - 44 * s)], fill=AMBER)
    for lx in (-6, 6): d.line([cx + lx * s, cy + 12 * s, cx + lx * s, cy + 46 * s], fill=GRAY, width=3)
def wolf(d, cx, cy, s=1.0): coyote(d, cx, cy, s)
def puma(d, cx, cy, s=1.0, col=(200, 160, 100)):
    d.ellipse([cx - 44 * s, cy - 16 * s, cx + 30 * s, cy + 16 * s], fill=col)
    d.ellipse([cx + 18 * s, cy - 30 * s, cx + 50 * s, cy + 0 * s], fill=col)
    d.polygon([(cx + 22 * s, cy - 24 * s), (cx + 26 * s, cy - 38 * s), (cx + 32 * s, cy - 26 * s)], fill=col)
    for lx in (-34, -20, 8, 20): d.rectangle([cx + lx * s, cy + 10 * s, cx + (lx + 6) * s, cy + 36 * s], fill=col)
    d.line([cx - 42 * s, cy, cx - 70 * s, cy - 24 * s], fill=col, width=int(7 * s))
def pin(d, cx, cy, col=RED, r=12):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); d.polygon([(cx - r * 0.8, cy + r * 0.5), (cx + r * 0.8, cy + r * 0.5), (cx, cy + r * 2)], fill=col)
    d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.4, cy + r * 0.4], fill=WHITE)
def clock(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=5, fill=WHITE)
    d.line([cx, cy, cx, cy - r * 0.6], fill=INK, width=5); d.line([cx, cy, cx + r * 0.45, cy + r * 0.2], fill=INK, width=5)

# ---------- P1 이름은 「한 마리」일 때만 켜지는 스위치 ----------
im, d = canvas("이름은 「한 마리」일 때만 켜지는 스위치", "송아지를 돕는 기부에 나선 사람 비율 — 네 가지로 보여 줬을 때 (Cohen Ben-Arye·Halali 2024, 초록 기준)")
base = 560; sc = 3.0
groups = [("이름 없는 무리", 65.0, False, False), ("이름 붙인 무리", 65.8, False, True), ("이름 없는 한 마리", 65.1, True, False), ("이름 붙인 한 마리", 75.9, True, True)]
for i, (lab, v, one, named) in enumerate(groups):
    x = 120 + i * 300
    if one: calf(d, x + 95, 205, 1.1)
    else:
        for k in range(4): calf(d, x + 40 + (k % 2) * 70, 185 + (k // 2) * 46, 0.65)
    if named: mini_tag(d, x + 40, 248, "럭키" if one else "럭키네 가족", BLUE)
    col = BLUE if (one and named) else DIM
    d.rounded_rectangle([x + 40, base - v * sc, x + 160, base], radius=8, fill=col)
    ctext(d, x + 100, base - v * sc - 40, f"{v}%", F_MID if (one and named) else F_M, BLUE if (one and named) else GRAY)
    ctext(d, x + 100, base + 8, lab, F_S, INK)
d.line([100, base, 1300, base], fill=INK, width=3)
box(d, (90, 610, 1310, 705), SAND, "이름이 힘을 쓴 건 「한 마리」에 붙었을 때뿐이다. 무리에 붙인 이름, 이름 없는 한 마리는 거의 같았다.\n다른 실험(2017, 1,306명)에선 한 마리 이름도 기부액 차이가 없었다 — 스위치가 늘 켜지지는 않는다", F_S, INK)
foot(d, "근거: 해외 논문노트 N1(J. Environ. Psychol. 93, 2024, 실험 3) · N3(Thomas-Walters·Raihani 2017, Conserv. Lett. 10). 이름은 그림용")
save(im, "P1_name_switch.png")

# ---------- P2 다마짱 특별 주민표 ----------
im, d = canvas("바다물범이 주민등록을 했다 — 2002년 도쿄 다마강의 「다마짱」", "부캉이보다 24년 앞선, 가장 닮은 선례")
seal(d, 250, 330, 1.6)
d.line([60, 400, 480, 400], fill=(120, 170, 220), width=6)
ctext(d, 250, 430, "다마강에 나타난 턱수염바다물범", F_S, INK)
# 주민표
x0, y0 = 560, 170
d.rounded_rectangle([x0, y0, x0 + 520, y0 + 300], radius=10, fill=WHITE, outline=INK, width=4)
d.rectangle([x0, y0, x0 + 520, y0 + 54], fill=NAVY); ctext(d, x0 + 260, y0 + 10, "특별 주민표", F_H, WHITE)
for k, (a, b) in enumerate([("이름", "니시 다마오"), ("발급", "요코하마시 니시구"), ("때", "2003년 2월")]):
    d.text((x0 + 30, y0 + 80 + k * 64), a, font=F_M, fill=GRAY); d.text((x0 + 170, y0 + 76 + k * 64), b, font=F_L, fill=INK)
d.ellipse([x0 + 400, y0 + 190, x0 + 490, y0 + 280], outline=RED, width=5); ctext(d, x0 + 445, y0 + 220, "인", F_H, RED)
# 흐름
steps = [("2002.8.7", "첫 목격"), ("이름", "「다마짱」"), ("2003.2", "주민표"), ("그 뒤", "행방불명")]
for i, (a, b) in enumerate(steps):
    x = 140 + i * 300
    d.ellipse([x - 12, 512, x + 12, 536], fill=NAVY if i < 3 else GRAY)
    ctext(d, x, 482, a, F_S, GRAY); ctext(d, x, 544, b, F_M, INK)
    if i < 3: arrow(d, (x + 30, 524), (x + 270, 524), DIM, 4)
box(d, (90, 600, 1310, 705), SAND, "지명에 애칭을 붙인 이름(다마강 + 짱), 그리고 지자체의 공식 서류 — 부캉이의 명예홍보대사와 같은 자리다.\n같은 달 외국인 주민들은 「물범은 주민표를 받는데 우리는 못 받는다」며 항의했다", F_S, INK)
foot(d, "근거: 해외 논문노트 1-1(Sakiyama 외 2024 · Yamasaki 2018 각주 · Chapman 2008 초록). 등록명 원문은 가타카나. 바다물범·서류는 모식")
save(im, "P2_tamachan_card.png")

# ---------- P3 같은 상어, 다른 제목 ----------
im, d = canvas("「공격한 상어」와 「못 나가는 상어」", "상어는 귀여움 길이 막혀 있다 — 대신 다른 길이 하나 있다")
d.text((90, 170), "보통의 상어 기사", font=F_L, fill=RED)
for k in range(48):
    r_, c_ = divmod(k, 12); x = 90 + c_ * 38; y = 220 + r_ * 50
    d.rectangle([x, y, x + 30, y + 40], fill=RED if k < 38 else DIM)
d.text((90, 430), "48건 중 38건(79%) 제목에 「공격」", font=F_M, fill=RED)
d.text((90, 466), "플로리다 AP 기사 · 실제 물림은 모두 치명상 아님", font=F_SM, fill=GRAY)
arrow(d, (580, 330), (660, 330), INK, 6)
shark(d, 900, 300, 1.4)
d.rectangle([700, 360, 1110, 380], fill=(120, 170, 220))
for k in range(5): d.line([720 + k * 90, 200, 720 + k * 90, 380], fill=GRAY, width=4)
d.text((700, 400), "부캉이는 처음부터", font=F_M, fill=INK); d.text((700, 438), "인공수로를 못 빠져나가는 상어였다", font=F_L, fill=BLUE)
d.rounded_rectangle([1130, 190, 1320, 380], radius=14, fill=MINT)
ctext(d, 1225, 210, "곤경에 빠진", F_S, INK); ctext(d, 1225, 236, "거대 동물엔", F_S, INK); ctext(d, 1225, 270, "68.6%", F_MID, GREEN); ctext(d, 1225, 318, "연민", F_M, GREEN)
d.text((1130, 392), "좌초 고래 현장 118명", font=F_SM, fill=GRAY)
box(d, (90, 600, 1310, 705), SAND, "백상아리는 카리스마 14위인데 「귀엽다」로는 한 번도 꼽히지 않았다. 상어에게 남은 길은 「곤경」이다.\n부캉이가 사랑받은 길이 거기였다는 건 연구를 이 사건에 적용한 해석이다", F_S, INK)
foot(d, "근거: 해외 논문노트(Neff·Hueter 2013, Bearzi 외 2010 초록, Albert 외 2018), 공부노트 1-1(구조 시도·인공수로). 창살은 모식")
save(im, "P3_shark_two_headlines.png")

# ---------- P4 주민과 침입자의 갈림길 ----------
im, d = canvas("같은 도시, 두 갈래 — 「주민」이 되거나 「침입자」가 되거나", "도시에 나타난 야생동물이 어느 쪽으로 가는지 — 해외·국내 연구 네 편")
d.rectangle([90, 330, 250, 420], fill=(190, 200, 220)); d.rectangle([110, 290, 170, 420], fill=(170, 180, 205)); ctext(d, 170, 430, "도시에 나타남", F_M, INK)
d.line([260, 375, 420, 375], fill=INK, width=8)
d.line([420, 375, 560, 230], fill=GREEN, width=8); d.line([420, 375, 560, 520], fill=RED, width=8)
ctext(d, 340, 300, "이름·사연 있으면", F_S, GREEN); ctext(d, 340, 430, "없으면", F_S, RED)
d.rounded_rectangle([580, 160, 1310, 330], radius=14, fill=MINT)
d.text((600, 170), "주민", font=F_L, fill=GREEN)
otter(d, 690, 260, 0.75); d.text((760, 215), "싱가포르 수달", font=F_M, fill=INK); d.text((760, 250), "무리마다 이름 · 2016 국가 아이콘 1위", font=F_S, fill=INK); d.text((760, 280), "최소 79마리 → 170마리", font=F_M, fill=GREEN)
otter(d, 1240, 225, 0.5); d.text((1170, 270), "한강 수달", font=F_SM, fill=INK); d.text((1170, 294), "귀환 환영", font=F_SM, fill=INK)
d.rounded_rectangle([580, 400, 1310, 570], radius=14, fill=PINK)
d.text((600, 410), "침입자", font=F_L, fill=RED)
coyote(d, 690, 500, 0.9); d.text((760, 455), "캐나다 코요테", font=F_M, fill=INK); d.text((760, 490), "기사에 「공격」 185번", font=F_M, fill=RED); d.text((760, 525), "실제 물림 32건", font=F_S, fill=INK)
heron(d, 1080, 520, 0.85); d.text((1150, 455), "청주 백로", font=F_S, fill=INK); d.text((1150, 485), "민원 끝 나무 베기", font=F_SM, fill=INK); d.text((1150, 510), "새끼 4마리 죽음", font=F_SM, fill=RED)
box(d, (90, 600, 1310, 705), SAND, "같은 「어긋난 자리」인데 결말이 갈렸다. 이름과 사연이 동물 쪽에 붙으면 주민, 사람 쪽에만 붙으면 침입자.\n어느 길로 갈지는 동물이 아니라 우리 쪽 이야기가 정한다(연구들을 맞대 본 해석)", F_S, INK)
foot(d, "근거: 해외 1-3(Khoo·Sivasothi 2018b, Shivram 2023)·1-11(Alexander·Quinn 2012), 국내 C1(최명애 2024)·C2(최명애 외 2023, 2021.7 청주)")
save(im, "P4_resident_or_intruder.png")

# ---------- P5 뽀롱이와 늑구 ----------
im, d = canvas("같은 동물원, 8년 차이 — 사살에서 생포로", "대전 오월드를 빠져나간 퓨마(2018)와 늑대(2026)")
d.rounded_rectangle([90, 160, 680, 570], radius=16, fill=(240, 236, 232))
d.text((115, 175), "2018년 9월 · 퓨마 「뽀롱이」", font=F_L, fill=INK)
puma(d, 250, 330, 1.6); clock(d, 520, 300, 56); ctext(d, 520, 370, "4시간 30분", F_MID, INK)
ctext(d, 385, 470, "탈출 4시간 30분 만에 사살", F_L, RED)
d.rounded_rectangle([720, 160, 1310, 570], radius=16, fill=MINT)
d.text((745, 175), "2026년 4월 · 늑대 「늑구」", font=F_L, fill=INK)
wolf(d, 860, 330, 1.6)
d.rounded_rectangle([1000, 230, 1290, 400], radius=10, fill=WHITE, outline=GRAY, width=2)
for (px, py) in [(1040, 300), (1090, 270), (1130, 330), (1180, 290), (1230, 350), (1150, 370), (1070, 360)]: pin(d, px, py, RED, 10)
ctext(d, 1145, 410, "시민이 모은 「늑구맵」", F_S, INK)
ctext(d, 1015, 470, "4월 8일 탈출 → 4월 17일 생포", F_L, GREEN)
box(d, (90, 600, 1310, 705), SAND, "논문은 대응이 「위험 제거」에서 「생포·시민 참여」로 바뀌었다고 본다. 온라인에선 「늑구」라는 이름이 퍼졌다.\n같은 열흘 동안 AI로 만든 가짜 목격 사진도 돌았다 — 함께 보는 힘의 그늘", F_S, INK)
foot(d, "근거: 국내 논문노트 B1(현승효 외 2026, 『Crisisonomy』 22(8), 본문 196·199쪽). 동물·지도는 모식")
save(im, "P5_puma_and_wolf.png")

# ---------- P6 푸바오 팬들의 「우리」 ----------
im, d = canvas("푸바오 팬 카페에서 「푸바오」 다음으로 무게가 큰 말 — 「우리」", "회원 154,869명 카페의 3년치 글(2021.7~2024.6)을 분석한 논문")
panda(d, 220, 330, 1.8)
words = [("우리", 76, BLUE, 560, 210), ("같이", 46, BLUE, 900, 230), ("이름", 36, GRAY, 600, 340), ("잘지내", 36, GRAY, 800, 340), ("푸야", 30, GRAY, 1000, 330), ("복보", 30, GRAY, 640, 420), ("임오", 28, GRAY, 820, 430)]
for w_, sz, col, x, y in words: d.text((x, y), w_, font=font(sz, True), fill=col)
donut(d, 1180, 470, 90, 0.706, GREEN, DIM, "70.6%", "긍정")
d.text((1080, 580), "감정 단어 7,245개 중", font=F_SM, fill=GRAY)
box(d, (90, 610, 1060, 705), SAND, "귀여움에서 시작한 마음이 「우리」「같이」라는 소속감으로 굳는다.\n팬끼리만 아는 애칭(푸야·복보)이 그 울타리다", F_S, INK)
foot(d, "근거: 국내 논문노트 A1(황정혜 2025, 『철학·사상·문화』 47, TF-IDF 상위어). 글자 크기는 순위를 나타낸 모식")
save(im, "P6_fubao_we.png")
