# -*- coding: utf-8 -*-
"""건축물 붕괴 글 — 일반인용 그림 10장(2026-10-14).
원리는 깊게 들어가지 않고 일상 비유로(사용자 10/14: 「배터리처럼 디테일하면 안 된다, 다른 걸 예시로 심플하게」).
숫자는 붕괴_공부노트_2026-10-14_합본.md · 붕괴_원본확인_국내/해외_2026-10-14.md 확인분만."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
# 헬퍼 위치: 10/14 LH 폴더가 부동산으로 옮겨져 두 경로를 다 본다. make_diagrams 는 그림 그리는 부분(# 01) 앞까지만 읽어
# 병역특례 그림이 다시 그려지지 않게 한다(기름값 make_pictures.py 와 같은 방식).
_cands = [os.path.join(HERE, "..", "261013_국감 이슈", "make_pictures.py"),
          os.path.join(HERE, "..", "..", "부동산_컨텐츠", "261013_LH 집값 급락 발언", "make_pictures.py")]
_src = open(next(p for p in _cands if os.path.exists(p)), encoding="utf-8").read()
import sys, types
_md_path = os.path.join(HERE, "..", "261011_병역특례 논란", "make_diagrams.py")
_md_src = open(_md_path, encoding="utf-8").read()
_md = types.ModuleType("make_diagrams"); _md.__file__ = _md_path
exec(_md_src[:_md_src.index("\n# 01 ")], _md.__dict__)
sys.modules["make_diagrams"] = _md
exec(_src[:_src.index("# ---------- 01")])
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)
CONC = (175, 175, 170); BOARD = (235, 230, 215); WIRE = (90, 90, 90); WOOD = (180, 140, 95)

def bulb(d, cx, cy, r=9, col=(255, 210, 80)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(200, 150, 40), width=2)
def cow(d, cx, cy, s=1.0):
    d.ellipse([cx - 40 * s, cy - 20 * s, cx + 30 * s, cy + 20 * s], fill=WHITE, outline=INK, width=2)
    d.ellipse([cx - 20 * s, cy - 14 * s, cx - 4 * s, cy + 2 * s], fill=INK); d.ellipse([cx + 6 * s, cy - 4 * s, cx + 20 * s, cy + 12 * s], fill=INK)
    d.ellipse([cx + 22 * s, cy - 30 * s, cx + 50 * s, cy - 4 * s], fill=WHITE, outline=INK, width=2)
    for lx in (-30, -14, 8, 20): d.line([cx + lx * s, cy + 18 * s, cx + lx * s, cy + 40 * s], fill=INK, width=int(4 * s))
def card(d, x, y, w, h, title, line, col=PINK):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=col)
    d.text((x + 16, y + 12), title, font=F_M, fill=INK); d.text((x + 16, y + 50), line, font=F_S, fill=INK)

# ---------- B1 무너진 건 천장이었다 ----------
im, d = canvas("건물은 그대로였고, 매달린 천장이 떨어졌다", "2026년 10월 10일 대구 북구 관음동, 4층 상가 건물 2층")
x0, x1 = 300, 900
for k, y in enumerate([560, 460, 360, 260, 160]):
    d.rectangle([x0, y - 12, x1, y], fill=CONC)
for x in (x0, 600 - 10, x1 - 20): d.rectangle([x, 160, x + 20, 560], fill=CONC)
for k, lab in enumerate(["1층", "2층", "3층", "4층"]): d.text((x0 - 70, 500 - k * 100), lab, font=F_S, fill=GRAY)
# 2층 천장 낙하
for k in range(6):
    xx = 330 + k * 92; d.polygon([(xx, 420 + (k % 2) * 14), (xx + 80, 410 + (k % 3) * 10), (xx + 86, 432), (xx + 6, 444)], fill=BOARD, outline=GRAY)
for xx in range(340, 880, 60): d.line([xx, 372, xx + 8, 400], fill=WIRE, width=2)
arrow(d, (950, 300), (950, 420), RED, 6)
d.text((980, 250), "뼈대(기둥·보·바닥)", font=F_M, fill=INK); d.text((980, 285), "그대로", font=F_L, fill=GREEN)
d.text((980, 400), "매달린 천장", font=F_M, fill=INK); d.text((980, 435), "떨어짐", font=F_L, fill=RED)
d.rounded_rectangle([980, 480, 1300, 560], radius=12, fill=PINK); d.text((1000, 492), "경상 38명", font=F_MID, fill=RED); d.text((1180, 500), "사망 0", font=F_M, fill=INK)
box(d, (90, 600, 1310, 700), SAND, "「붕괴」라는 말이 붙었지만 건물 뼈대가 무너진 게 아니라 천장 마감이 떨어진 사고다.\n그런데도 38명이 다쳤다. 천장은 어떻게 붙어 있었을까", F_S, INK)
foot(d, "근거: 합본 §2 · 공부노트 §1-1(소방 집계, 경북일보·파이낸셜뉴스·서울경제). 건물 단면은 모식")
save(im, "B1_ceiling_not_building.png")

# ---------- B2 천장은 줄에 매단 선반 ----------
im, d = canvas("매단 천장은 줄에 매단 선반과 같다", "위층 바닥에 줄을 걸어 판을 매단다 — 무게는 줄이 버틴다")
# 왼쪽: 선반 비유
d.rectangle([90, 170, 600, 190], fill=CONC); d.text((100, 140), "천장(위)", font=F_S, fill=GRAY)
for x in (160, 520): d.line([x, 190, x, 400], fill=WIRE, width=4)
d.rectangle([130, 400, 560, 418], fill=WOOD)
for k in range(3): d.rectangle([150, 380 - k * 14, 540, 392 - k * 14], fill=BOARD, outline=GRAY)
for k in range(10): bulb(d, 170 + k * 38, 330)
ctext(d, 345, 440, "판 3장 + 전구 10개를 올린 선반", F_M, INK)
ctext(d, 345, 476, "줄이 낡거나 위가 무거워지면 버티는 힘이 준다", F_S, GRAY)
# 오른쪽: 실제 천장
d.rectangle([760, 170, 1300, 200], fill=CONC); d.text((770, 140), "위층 바닥(콘크리트)", font=F_S, fill=GRAY)
for x in range(800, 1290, 70): d.line([x, 200, x, 330], fill=WIRE, width=3)
d.rectangle([780, 330, 1290, 344], fill=(140, 140, 150)); d.text((1140, 300), "천장틀", font=F_SM, fill=INK)
for k in range(3): d.rectangle([780, 346 + k * 14, 1290, 358 + k * 14], fill=BOARD, outline=GRAY)
d.text((800, 400), "석고보드·종이합판 3겹", font=F_S, fill=INK)
for k in range(10): bulb(d, 805 + k * 50, 452, 8)
d.text((800, 470), "판매업체가 단 LED 조명 10개(보도)", font=F_S, fill=INK)
box(d, (90, 590, 1310, 700), SAND, "대구 천장도 줄(달대·와이어)에 매달린 판 3겹이었고, 그 아래 조명이 더 달렸다.\n다만 무엇이 결정적이었는지는 아직 조사 중이다 — 원인을 단정하지 않는다", F_S, INK)
foot(d, "근거: 합본 §2(경량 철골 천장틀, 3중 마감, LED 10개 — 보도), 원인 공식 발표·국과수 결과 없음(10/14). 선반·천장 단면은 모식")
save(im, "B2_hanging_shelf.png")

# ---------- B3 일본은 본다, 우리는 빈칸 ----------
im, d = canvas("일본은 매단 천장을 정기적으로 본다, 우리 법에는 그 칸이 없다", "건물 정기점검표를 나란히 놓으면")
for i, (title, col, rows) in enumerate([("일본", NAVY, [("기둥·보", True), ("외벽", True), ("큰 매단 천장", True)]), ("한국", RED, [("기둥·보", True), ("외벽", True), ("매단 천장", False)])]):
    x = 120 + i * 560
    d.rounded_rectangle([x, 160, x + 460, 520], radius=14, fill=WHITE, outline=INK, width=4)
    d.rectangle([x + 170, 145, x + 290, 175], fill=GRAY)
    d.text((x + 30, 190), title + " 정기점검표", font=F_L, fill=col)
    for k, (lab, ok) in enumerate(rows):
        y = 260 + k * 75
        d.rectangle([x + 30, y, x + 70, y + 40], outline=INK, width=3)
        if ok: d.line([x + 36, y + 20, x + 48, y + 34, x + 66, y + 6], fill=GREEN, width=6)
        d.text((x + 90, y + 4), lab, font=F_M, fill=INK if ok else RED)
    if i == 0: d.text((x + 30, 470), "2014년부터 (높이 6m·넓이 200㎡·무게 ㎡당 2kg 넘는 것)", font=F_SM, fill=GRAY)
    else: d.text((x + 30, 470), "매단 천장 정기점검 조항 없음", font=F_SM, fill=RED)
d.rounded_rectangle([1150, 250, 1320, 420], radius=14, fill=PINK)
ctext(d, 1235, 265, "대구 건물", F_M, INK); ctext(d, 1235, 305, "892.92㎡", F_M, INK); ctext(d, 1235, 345, "정기점검", F_S, RED); ctext(d, 1235, 375, "대상 아님", F_S, RED)
box(d, (90, 590, 1310, 700), SAND, "일본은 2011년 대지진 뒤 큰 매단 천장을 정기조사 대상에 넣었다. 우리 점검지침엔 마감재 관찰 정도만 있고,\n대구 건물은 정기점검 대상 건물도 아니었다", F_S, INK)
foot(d, "근거: 합본 §0-3, 해외 확인(일본 特定天井 고시 771호, 2014.4.1), 국내 확인 §2-6(건축물관리법 제13·15조). 점검표는 모식")
save(im, "B3_checklist_gap.png")

# ---------- B4 레시피는 있었다 ----------
im, d = canvas("레시피는 있었는데 단계를 건너뛰었다 — 최근 9건", "국토부 사고조사위 원문이 꼽은 원인을 쉬운 말 한 줄로. 「기술이 없어서」는 0건")
items = [("광주 학동 2021", "순서를 바꾸고 흙을 쌓았다"), ("광주 화정 2022", "받침을 일찍 뺐다"), ("인천 검단 2023", "철근을 빠뜨렸다"),
         ("성남 정자교 2023", "고칠 때를 놓쳤다"), ("안성 교량 2025", "받침 72개를 치웠다"), ("오산 옹벽 2025", "물길을 안 챙겼다"),
         ("광명 터널 2025", "무게를 2.5배 작게 셌다"), ("광주 도서관 2025", "용접을 대충 했다"), ("서울 서소문 2026", "자르는 순서가 달랐다(조사 중)")]
d.rounded_rectangle([90, 165, 330, 560], radius=14, fill=SAND)
ctext(d, 210, 185, "레시피", F_L, INK)
for k, t in enumerate(["설계도", "계획서", "기준"]): d.text((120, 240 + k * 50), "· " + t, font=F_M, fill=INK)
ctext(d, 210, 420, "있었다", F_MID, GREEN)
for k, (a, b) in enumerate(items):
    r_, c_ = divmod(k, 3); x = 360 + c_ * 320; y = 165 + r_ * 135
    card(d, x, y, 300, 120, a, b, PINK if "조사 중" not in b else (240, 236, 232))
box(d, (90, 590, 1310, 700), SAND, "몰라서 무너진 게 아니라, 알던 걸 건너뛰어서 무너졌다. 계획과 다르게 하거나, 빼먹거나, 치우거나, 미뤘다.\n(이 「0건」은 국내 최근 9건 이야기다)", F_S, INK)
foot(d, "근거: 국내 확인 §2-5(사조위 보도자료 원문 8건, 서소문은 국토안전관리원 초기 보고·최종 미발표)")
save(im, "B4_recipe_skipped.png")

# ---------- B5 시험지로 보면 ----------
im, d = canvas("800건을 시험지로 보면 — 처음 보는 문제의 배점이 컸다", "스위스 연구(1976) — 건물·구조물 손상 800건의 원인을 세 칸으로")
rows = [("아는 문제를 틀렸다", "기준을 어기거나 빠뜨림", 64.5, RED), ("알고 넘긴 문제", "위험인 줄 알고 받아들임", 21.75, AMBER), ("처음 보는 문제", "원인을 알 수 없음", 13.75, NAVY)]
for k, (a, b, v, col) in enumerate(rows):
    y = 190 + k * 115
    d.rounded_rectangle([90, y, 160, y + 80], radius=8, fill=WHITE, outline=INK, width=3)
    for j in range(3): d.line([102, y + 20 + j * 18, 148, y + 20 + j * 18], fill=GRAY, width=3)
    d.text((180, y + 6), a, font=F_M, fill=INK); d.text((180, y + 42), b, font=F_S, fill=GRAY)
    d.rounded_rectangle([500, y + 14, 500 + v * 6, y + 66], radius=8, fill=col)
    d.text((510 + v * 6, y + 18), f"{v}%", font=F_MID, fill=col)
d.rounded_rectangle([1000, 400, 1310, 540], radius=14, fill=LIGHT)
ctext(d, 1155, 412, "그런데 손해액으로는", F_S, INK); ctext(d, 1155, 446, "43%", F_BIG, NAVY)
arrow(d, (1000, 470), (760, 470), NAVY, 5)
box(d, (90, 590, 1310, 700), SAND, "대부분은 아는 걸 안 해서였다. 처음 보는 문제는 열에 한 번꼴이었지만, 나오면 피해가 컸다.\n그래서 「기술은 상관없다」도 틀린 말이다", F_S, INK)
foot(d, "근거: 해외 확인 §1(Matousek·Schneider 1976 원표). 「알 수 없음」 정의는 미확인, 연구비 일부 보험사. 시험지는 비유")
save(im, "B5_exam_800.png")

# ---------- B6 휴대폰과 망치 ----------
im, d = canvas("공장은 해마다 빨라졌는데, 집 짓는 손은 덜 변했다", "일하는 사람 한 명이 만들어 내는 양이 늘어난 속도 — 지난 20년 한 해 평균")
for i, (lab, v, col, icon) in enumerate([("제조업", 3.6, NAVY, "공장"), ("건설업", 1.0, AMBER, "현장")]):
    x = 150 + i * 600
    d.text((x, 175), lab, font=F_L, fill=col); d.text((x, 215), f"한 해 {v}%", font=F_BIG, fill=col)
    mult = (1 + v / 100) ** 20
    d.rounded_rectangle([x, 520 - mult * 85, x + 160, 520], radius=10, fill=col)
    ctext(d, x + 80, 520 - mult * 85 - 40, f"20년 뒤 {mult:.1f}배", F_M, col)
    d.rounded_rectangle([x + 200, 410, x + 360, 520], radius=10, fill=LIGHT)
    ctext(d, x + 280, 440, "로봇·자동화" if i == 0 else "용접·받침·철근", F_S, INK); ctext(d, x + 280, 475, "기계가 잇는다" if i == 0 else "사람 손이 잇는다", F_S, INK)
box(d, (90, 590, 1310, 700), SAND, "재료와 계산은 좋아졌지만, 현장에서 용접하고 받침을 세우고 철근을 엮는 건 여전히 사람 손이다.\n앞에서 본 9건이 무너진 자리도 거기였다", F_S, INK)
foot(d, "근거: 해외 확인 §1(McKinsey 2017 「Reinventing construction」 요약 2쪽, 본문 15·22쪽). 「20년 뒤 몇 배」는 직접 계산")
save(im, "B6_factory_vs_site.png")

# ---------- B7 소 잃고 외양간 ----------
im, d = canvas("소 잃고 외양간 고치기 — 규칙은 사고 뒤에 생긴다", "사고가 난 자리마다 구멍을 막았다. 그런데 막지 않은 구멍이 남아 있다")
d.rectangle([90, 200, 1310, 520], outline=(150, 110, 80), width=8)
d.polygon([(90, 200), (700, 140), (1310, 200)], outline=(150, 110, 80))
holes = [("학동 2021", "해체계획서·상주감리", True), ("검단 2023", "무량판 특수구조 지정", True), ("정자교 2023", "점검 부실 벌칙 강화", True), ("대구 천장 2026", "매단 천장 점검 ?", False)]
for k, (a, b, fixed) in enumerate(holes):
    x = 140 + k * 290
    if fixed:
        d.rectangle([x, 300, x + 240, 420], fill=(200, 170, 130), outline=(150, 110, 80), width=3)
        for j in range(4): d.line([x, 310 + j * 28, x + 240, 310 + j * 28], fill=(150, 110, 80), width=2)
    else:
        d.rectangle([x, 300, x + 240, 420], fill=BG, outline=RED, width=4); ctext(d, x + 120, 330, "?", F_BIG, RED)
    ctext(d, x + 120, 236, a, F_M, INK); ctext(d, x + 120, 440, b, F_S, GREEN if fixed else RED)
cow(d, 1255, 548, 0.7)
box(d, (90, 590, 1310, 700), SAND, "사고가 나면 그 구멍은 막았다. 다만 다음 사고는 아직 안 막은 구멍에서 났다.\n대만은 사고 뒤 개정안이 끝내 법이 되지 못했다 — 사고 뒤라고 늘 막히는 것도 아니다", F_S, INK)
foot(d, "근거: 국내 확인 §2-6(건축물관리법 제30·31조, 건축법 시행령 2024.12.17, 시설물안전법 벌칙 2025.12.4), 해외 확인(대만 2018)")
save(im, "B7_barn_holes.png")

# ---------- B8 건물의 나이 ----------
im, d = canvas("30년 넘은 건물, 열 채 중 다섯 채 가까이", "전국 건축물 중 사용승인 뒤 30년이 지난 비율")
for k in range(10):
    x = 120 + k * 118
    house(d, x, 400, 0.85, wall=(200, 200, 200) if k < 4 else WALL, roof=(130, 130, 130) if k < 4 else ROOF)
x5 = 120 + 4 * 118; s5 = 0.85
d.polygon([(x5, 400 - 70 * s5), (x5 + 60 * s5, 400 - 120 * s5), (x5 + 72 * s5, 400 - 110 * s5), (x5 + 72 * s5, 400 - 70 * s5)], fill=(130, 130, 130))
d.rectangle([x5 + 12 * s5, 400 - 70 * s5, x5 + 72 * s5, 400], fill=(200, 200, 200))
d.text((120, 430), "회색 = 30년 넘음", font=F_S, fill=GRAY)
for k, (yr, v) in enumerate([("2023년 말", "42.6%"), ("2024년 말", "44.4%"), ("2025년 말", "46.3%")]):
    x = 300 + k * 300
    ctext(d, x, 480, yr, F_S, GRAY); ctext(d, x, 510, v, F_MID if k == 2 else F_M, RED if k == 2 else INK)
box(d, (90, 590, 1310, 700), SAND, "짓다가 무너지는 사고는 줄일 수 있어도, 쓰다가 생기는 사고는 해마다 늘어날 자리가 있다.\n대구 관음동 건물도 1994년에 지어진 32년 된 건물이었다", F_S, INK)
foot(d, "근거: 합본 §0-4(국토부 건축물 통계 2026.9.30 — 2024·2025년 말), 공부노트(2023년 말). 집 그림 4.6채는 모식")
save(im, "B8_building_age.png")

# ---------- B9 정리 ----------
im, d = canvas("정리 — 건물을 무너뜨린 건 기술보다 이 셋이었다", "최근 9건과 800건 연구, 그리고 대구 천장을 한 장으로")
three = [("건너뛴 단계", "알던 걸 안 했다", "레시피 9건", PINK), ("막지 않은 구멍", "규칙이 닿지 않았다", "매단 천장", SAND), ("쌓인 나이", "쓰는 동안 낡았다", "30년 넘은 집 46.3%", LIGHT)]
for k, (a, b, c, col) in enumerate(three):
    x = 100 + k * 410
    d.rounded_rectangle([x, 170, x + 380, 540], radius=18, fill=col)
    ctext(d, x + 190, 200, a, F_L, INK); ctext(d, x + 190, 250, b, F_S, INK)
    if k == 0:
        d.rounded_rectangle([x + 120, 300, x + 260, 460], radius=8, fill=WHITE, outline=INK, width=3)
        for j in range(4): d.line([x + 140, 330 + j * 30, x + 240, 330 + j * 30], fill=GRAY, width=3)
        d.line([x + 135, 360, x + 245, 360], fill=RED, width=5)
    elif k == 1:
        d.rectangle([x + 110, 300, x + 270, 460], outline=(150, 110, 80), width=6); d.rectangle([x + 150, 340, x + 230, 420], fill=BG, outline=RED, width=4); ctext(d, x + 190, 350, "?", F_BIG, RED)
    else:
        house(d, x + 130, 460, 1.0, wall=(200, 200, 200), roof=(130, 130, 130))
    ctext(d, x + 190, 485, c, F_S, GRAY)
box(d, (90, 590, 1310, 700), SAND, "「몰랐던 공학」이 무너뜨린 경우는 적었다. 건너뛴 단계, 막지 않은 구멍, 쌓인 나이가 대부분이었다.\n그중 낡음과 빈칸은 지나가는 우리 눈에도 보인다", F_S, INK)
foot(d, "근거: 그림 4·5·7·8. 세 칸은 이 글의 정리이고 공식 분류가 아니다")
save(im, "B9_three_causes.png")

# ---------- B10 할 일 하나 ----------
im, d = canvas("오늘 할 일 하나 — 자주 가는 곳의 천장을 한 번 올려다보기", "점검 조항이 없는 칸은 지나가는 눈이 먼저 본다")
person(d, 220, 330, 200, NAVY); arrow(d, (250, 320), (360, 230), GRAY, 4)
d.rectangle([380, 170, 1310, 200], fill=CONC)
signs = [("금이 갔다", "균열"), ("가운데가 처졌다", "변형"), ("조각이 떨어졌다", "탈락")]
for k, (a, b) in enumerate(signs):
    x = 420 + k * 300
    d.rectangle([x, 220, x + 260, 260], fill=BOARD, outline=GRAY)
    if k == 0: d.line([x + 40, 225, x + 90, 255, x + 130, 230, x + 180, 255], fill=INK, width=3)
    if k == 1: d.arc([x + 20, 200, x + 240, 300], 20, 160, fill=RED, width=5)
    if k == 2: d.polygon([(x + 100, 280), (x + 150, 290), (x + 140, 320), (x + 95, 310)], fill=BOARD, outline=GRAY)
    ctext(d, x + 130, 340, a, F_M, INK); ctext(d, x + 130, 378, b, F_S, GRAY)
d.rounded_rectangle([420, 430, 1310, 540], radius=14, fill=LIGHT)
d.text((445, 445), "보이면 건물 관리자에게 알리거나 안전신문고에 신고", font=F_M, fill=NAVY)
d.text((445, 490), "건물 나이는 건축물대장, 다리·큰 건물 등급은 시설물 정보공개(FMS)에서", font=F_S, fill=INK)
box(d, (90, 590, 1310, 700), SAND, "천장을 점검하라는 조항은 없지만, 올려다보지 말라는 법도 없다.\n대구시도 점검할 때 천장 마감의 금·처짐·떨어짐을 본다", F_S, INK)
foot(d, "근거: 국내 확인 §4(대구시 점검 항목 「천장마감재의 균열·변형·탈락」, 안전신문고, 건축물대장·FMS 공식 경로). 장면은 모식")
save(im, "B10_look_up.png")
