# -*- coding: utf-8 -*-
"""대표팀 주장 글 — 일반인용 그림 12장(2026-10-15).
결: 옳고 그름을 판정하지 않는다. 네 질문을 따라간다 — ① 다름을 품을 수 있나 ② 옳다고 믿는 사람을 설득할 수 있나
③ 대표팀엔 왜 조건이 붙나 ④ 선수 문제인가 시스템 문제인가.
원리는 일상 비유로 심플하게(가족 여행 단톡방·의자 거리·닫힌 문과 귀·월요일 옷장·늦은 택배·완장과 빈칸 서식·네 칸·띠와 도장·치즈).
숫자는 주장_보강노트_2026-10-14.md(우선)·주장_공부노트_2026-10-12.md 확인분만. 특정인 얼굴·실루엣 없음, 실명 없음."""
import os, math
HERE = os.path.dirname(os.path.abspath(__file__))
# 헬퍼 원본: 예전 `..\261013_국감 이슈\make_pictures.py` — 10/14 밤 `부동산_컨텐츠\261013_LH 집값 급락 발언\`으로 옮겨짐
_cands = [os.path.join(HERE, "..", "261013_국감 이슈", "make_pictures.py"),
          os.path.join(HERE, "..", "..", "부동산_컨텐츠", "261013_LH 집값 급락 발언", "make_pictures.py")]
_src = open(next(p for p in _cands if os.path.exists(p)), encoding="utf-8").read()
# make_diagrams 를 그냥 import 하면 병역특례 그림 16장을 다시 그려 덮어쓴다 → 헬퍼 부분(「# 01」 전)만 모듈로 올린다
import sys, types
_md_path = os.path.join(HERE, "..", "261011_병역특례 논란", "make_diagrams.py")
_md_src = open(_md_path, encoding="utf-8").read()
_md = types.ModuleType("make_diagrams"); _md.__file__ = _md_path
exec(_md_src[:_md_src.index("\n# 01 ")], _md.__dict__)
sys.modules["make_diagrams"] = _md
exec(_src[:_src.index("# ---------- 01")])
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)

WARN = []
def save(im, n):
    im.save(os.path.join(OUT, n)); print("saved", n)

# ---- 글자 넘침 검사용 래퍼 ----
_canvas, _box, _ctext = canvas, box, ctext
def canvas(title, sub=None):
    im, d = _canvas(title, sub)
    for t, f in ((title, F_T), (sub or "", F_S)):
        if 60 + d.textlength(t, font=f) > W - 50: WARN.append(f"제목/부제 넘침: {t}")
    return im, d
def box(d, xy, fill, text, f=F_S, color=INK, **kw):
    for ln in text.split("\n"):
        if d.textlength(ln, font=f) > (xy[2] - xy[0]) - 40: WARN.append(f"상자 넘침: {ln}")
    if len(text.split("\n")) > 2: WARN.append(f"상자 세 줄: {text[:20]}")
    _box(d, xy, fill, text, f, color, **kw)
def footc(d, text):
    if 60 + d.textlength(text, font=F_S) > W - 30: WARN.append(f"근거 넘침: {text}")
    foot(d, text)
def ctext(d, cx, y, text, f, color=INK, lo=15, hi=None):
    w = d.textlength(text, font=f); hi = W - 15 if hi is None else hi
    if cx - w / 2 < lo or cx + w / 2 > hi: WARN.append(f"가로 넘침: {text}")
    _ctext(d, cx, y, text, f, color)
def ltext(d, x, y, text, f, color=INK, xmax=None):
    xmax = W - 15 if xmax is None else xmax
    if x + d.textlength(text, font=f) > xmax: WARN.append(f"가로 넘침: {text}")
    d.text((x, y), text, font=f, fill=color)

# ---- 색 ----
WORK = (45, 105, 200); PEOPLE = (205, 65, 60); MAROON = (150, 35, 60); CHEESE = (246, 205, 90); CHEESE_D = (200, 150, 40)
PAPER = (255, 253, 246); HL = (255, 232, 150); DOOR = (150, 105, 70); SHIRT = (190, 190, 185)
DONE_BOX = (90, 600, 1310, 700)

# ---- 그림 부품 ----
def dashed(d, p0, p1, col=GRAY, w=2, dash=10):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0); n = max(int(L // dash), 1)
    for i in range(0, n, 2):
        a = i / n; b = min((i + 1) / n, 1)
        d.line([x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b], fill=col, width=w)
def dashed_rect(d, xy, col=GRAY, w=2):
    x0, y0, x1, y1 = xy
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): dashed(d, p, q, col, w)
def ic_table(d, cx, cy, col=NAVY):
    d.rounded_rectangle([cx - 30, cy - 6, cx + 30, cy + 2], radius=3, fill=col)
    d.line([cx - 22, cy + 2, cx - 22, cy + 22], fill=col, width=4); d.line([cx + 22, cy + 2, cx + 22, cy + 22], fill=col, width=4)
    for sx in (-44, 44):
        d.ellipse([cx + sx - 8, cy - 26, cx + sx + 8, cy - 10], fill=col)
        d.rounded_rectangle([cx + sx - 9, cy - 8, cx + sx + 9, cy + 16], radius=5, fill=col)
def ic_mic(d, cx, cy, col=NAVY):
    d.rounded_rectangle([cx - 11, cy - 28, cx + 11, cy + 4], radius=11, fill=col)
    d.arc([cx - 19, cy - 14, cx + 19, cy + 14], 0, 180, fill=col, width=4)
    d.line([cx, cy + 14, cx, cy + 26], fill=col, width=4); d.line([cx - 12, cy + 26, cx + 12, cy + 26], fill=col, width=4)
def ic_doc(d, cx, cy, col=NAVY):
    d.polygon([(cx - 20, cy - 28), (cx + 10, cy - 28), (cx + 22, cy - 16), (cx + 22, cy + 28), (cx - 20, cy + 28)], fill=WHITE, outline=col)
    d.line([cx - 20, cy - 28, cx + 10, cy - 28, cx + 22, cy - 16, cx + 22, cy + 28, cx - 20, cy + 28, cx - 20, cy - 28], fill=col, width=3)
    for k in range(3): d.line([cx - 12, cy - 8 + k * 11, cx + 14, cy - 8 + k * 11], fill=col, width=3)
def ic_hearsay(d, cx, cy, col=GRAY):
    d.ellipse([cx - 28, cy - 22, cx + 28, cy + 16], outline=col, width=3, fill=WHITE)
    d.polygon([(cx - 14, cy + 10), (cx - 22, cy + 28), (cx - 2, cy + 14)], fill=col)
    _ctext(d, cx, cy - 20, "?", F_M, col)
def heart(d, cx, cy, s, col):
    pts = []
    for i in range(60):
        t = 2 * math.pi * i / 60
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * s, cy - y * s))
    d.polygon(pts, fill=col)
def megaphone(d, cx, cy, col):
    d.polygon([(cx - 40, cy - 12), (cx + 30, cy - 38), (cx + 30, cy + 38), (cx - 40, cy + 12)], fill=col)
    d.rounded_rectangle([cx - 56, cy - 14, cx - 36, cy + 14], radius=4, fill=col)
    for k in range(3): d.arc([cx + 24 + k * 14, cy - 30 - k * 6, cx + 54 + k * 14, cy + 30 + k * 6], -40, 40, fill=col, width=4)
def tactic_board(d, cx, cy, col=GREEN):
    d.rounded_rectangle([cx - 54, cy - 38, cx + 54, cy + 38], radius=8, fill=col)
    d.line([cx, cy - 38, cx, cy + 38], fill=WHITE, width=2); d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=WHITE, width=2)
    for (x, y) in ((-34, -16), (-30, 18)): d.ellipse([cx + x - 7, cy + y - 7, cx + x + 7, cy + y + 7], outline=WHITE, width=3)
    for (x, y) in ((28, -12), (34, 20)):
        d.line([cx + x - 6, cy + y - 6, cx + x + 6, cy + y + 6], fill=WHITE, width=3); d.line([cx + x + 6, cy + y - 6, cx + x - 6, cy + y + 6], fill=WHITE, width=3)
    d.line([cx - 24, cy - 16, cx + 18, cy - 12], fill=AMBER, width=3)
def door_ic(d, cx, cy, col):
    d.rectangle([cx - 30, cy - 44, cx + 30, cy + 40], fill=col)
    d.polygon([(cx - 30, cy - 44), (cx + 8, cy - 34), (cx + 8, cy + 50), (cx - 30, cy + 40)], fill=(230, 220, 200))
    d.ellipse([cx + 0, cy, cx + 6, cy + 6], fill=INK)
    arrow(d, (cx + 18, cy), (cx + 56, cy), col, 4)
def clock(d, cx, cy, r, col=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=col, width=3)
    d.line([cx, cy, cx, cy - r * 0.65], fill=col, width=3); d.line([cx, cy, cx + r * 0.5, cy], fill=col, width=3)
def phone(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=INK)
    d.rounded_rectangle([x + 14, y + 40, x + w - 14, y + h - 40], radius=8, fill=WHITE)
def basket(d, x0, y0, x1, y1, col, label):
    d.polygon([(x0, y0), (x1, y0), (x1 - 30, y1), (x0 + 30, y1)], fill=col)
    for k in range(1, 4):
        yy = y0 + (y1 - y0) * k / 4; d.line([x0 + 30 * k / 4, yy, x1 - 30 * k / 4, yy], fill=WHITE, width=2)
    d.rounded_rectangle([x0 - 10, y0 - 12, x1 + 10, y0 + 8], radius=8, fill=col)
    ctext(d, (x0 + x1) / 2, (y0 + y1) / 2 - 10, label, F_BIG, WHITE)

# ============ C1 확인됨 / 전언 ============
im, d = canvas("무엇이 확인됐고, 무엇이 전해졌나", "10월 6일 경기 뒤부터 10월 13일까지 — 기사 텍스트 기준")
d.rounded_rectangle([90, 160, 680, 575], radius=20, fill=MINT, outline=GREEN, width=3)
check(d, 140, 208, 20); ltext(d, 174, 186, "확인됨", F_H, GREEN); ltext(d, 300, 194, "공식 발언 · 공식 문서", F_S, GRAY)
for k, (ic, t) in enumerate((("table", "위원장 면담 (10월 6일)"), ("mic", "「은퇴 이야기는 없었다」"), ("doc", "협회 입장문 (10월 13일)"))):
    y = 252 + k * 104
    d.rounded_rectangle([120, y, 650, y + 82], radius=14, fill=WHITE)
    {"table": ic_table, "mic": ic_mic, "doc": ic_doc}[ic](d, 180, y + 44)
    ltext(d, 240, y + 25, t, F_L, INK, 640)
d.rounded_rectangle([720, 160, 1310, 575], radius=20, fill=(243, 243, 240))
dashed_rect(d, (730, 168, 1300, 567), GRAY, 3)
ic_hearsay(d, 775, 206); ltext(d, 816, 186, "전언", F_H, GRAY); ltext(d, 900, 194, "익명 관계자 · 이름 없는 취재원", F_S, GRAY)
for k, t in enumerate(("「은퇴 의사를 밝혔다」", "「리더십 변화 요구」")):
    y = 252 + k * 104
    d.rounded_rectangle([750, y, 1280, y + 82], radius=14, fill=WHITE)
    dashed_rect(d, (750, y, 1280, y + 82), (170, 170, 165), 2)
    ic_hearsay(d, 810, y + 44, (150, 150, 145))
    ltext(d, 870, y + 25, t, F_L, (95, 95, 95), 1270)
ctext(d, 1015, 488, "사실로 그리지 않는다", F_M, GRAY)
box(d, DONE_BOX, SAND, "당사자들의 공개 발언에는 「리더십」이라는 말이 없다. 그 말은 익명 관계자 전언으로만 나왔다\n이 글은 왼쪽 칸에서만 출발한다", F_S, INK)
footc(d, "근거: 공부노트 1-1·보강노트 1장(경향·중앙·MBC·SBS·뉴시스·한국경제 등 기사 텍스트). 영상 인용 없음")
save(im, "C1_confirmed_vs_reported.png")

# ============ C2 입장문 한 문장 → 질문 넷 ============
im, d = canvas("협회 입장문의 한 문장, 그 안에 든 질문 넷", "대한축구협회 10월 13일 입장문(이해당사자 문서) 중에서")
d.rounded_rectangle([90, 160, 560, 575], radius=12, fill=PAPER, outline=(200, 195, 185), width=3)
ctext(d, 325, 182, "팬 여러분께 드리는 글", F_M, INK)
for y in (240, 268):
    d.rounded_rectangle([130, y, 520 if y == 240 else 470, y + 10], radius=5, fill=(220, 218, 210))
d.rounded_rectangle([118, 300, 532, 400], radius=10, fill=HL)
ctext(d, 325, 314, "「서로의 차이를 인정하고", F_L, INK); ctext(d, 325, 354, "자유롭게 의견을 나누며」", F_L, INK)
for y, x1 in ((428, 520), (456, 500), (484, 430)):
    d.rounded_rectangle([130, y, x1, y + 10], radius=5, fill=(220, 218, 210))
chip(d, 130, 518, "이해당사자 문서", GRAY, F_S)
QS = (("다름을 품을 수 있을까", WORK), ("옳다고 믿는 사람을 설득할 수 있을까", GREEN), ("대표팀에는 왜 조건이 붙을까", AMBER), ("선수 문제일까, 시스템 문제일까", NAVY))
for k, (q, col) in enumerate(QS):
    y = 172 + k * 100
    d.rounded_rectangle([690, y, 1310, y + 80], radius=16, fill=WHITE, outline=col, width=3)
    d.ellipse([712, y + 16, 760, y + 64], fill=col); ctext(d, 736, y + 22, str(k + 1), F_M, WHITE)
    ltext(d, 780, y + 26, q, F_M, INK, 1300)
    arrow(d, (540, 350), (680, y + 40), col, 4)
box(d, DONE_BOX, SAND, "이 글은 입장문이 맞는지 따지지 않는다\n그 문장이 남긴 질문 넷을 차례로 따라간다", F_S, INK)
footc(d, "근거: 보강노트 1장 — 10.13 입장문(한국경제·머니투데이·스포티비뉴스 인용 일치). 협회는 이해당사자")
save(im, "C2_one_sentence_four_questions.png")

# ============ C3 다름의 두 갈래 ============
im, d = canvas("질문 1 — 다름이 「일」에 머물까, 「사람」으로 번질까", "일터 팀 연구 116편을 모은 분석 · 그림은 가족 여행 단톡방 비유")
ROAD = (215, 208, 196)
up = [(90, 420), (380, 420), (520, 300), (820, 300)]
dn = [(380, 420), (520, 485), (820, 555)]
d.line(up, fill=ROAD, width=46, joint="curve"); d.line(dn, fill=ROAD, width=46, joint="curve")
for a, b in zip(up[:-1], up[1:]): dashed(d, a, b, WHITE, 3, 14)
for a, b in zip(dn[:-1], dn[1:]): dashed(d, a, b, WHITE, 3, 14)
# 표지판
d.line([560, 270, 560, 240], fill=GRAY, width=5)
d.polygon([(500, 200), (610, 200), (636, 220), (610, 240), (500, 240)], fill=WORK); ctext(d, 555, 203, "일", F_L, WHITE)
d.line([440, 462, 440, 495], fill=GRAY, width=5)
d.polygon([(380, 495), (500, 495), (526, 515), (500, 535), (380, 535)], fill=PEOPLE); ctext(d, 446, 498, "사람", F_L, WHITE)
bubble(d, (660, 180, 960, 236), "제주 말고 부산 어때?", F_S, WHITE, WORK, tail=((700, 262), (690, 720, 236)))
bubble(d, (620, 390, 960, 446), "넌 맨날 네 마음대로잖아", F_S, WHITE, PEOPLE, tail=((660, 486), (650, 690, 446)))
# 끝 표시
arrow(d, (832, 300), (880, 300), WORK, 6); ltext(d, 832, 330, "성과 거의 그대로", F_S, WORK, 1005)
down_arrow(d, 860, 500, 70, PEOPLE, 40); ltext(d, 890, 525, "내려간다", F_M, PEOPLE, 1000)
d.rounded_rectangle([1020, 200, 1320, 520], radius=16, fill=LIGHT)
ctext(d, 1170, 228, "연구", F_M, INK); ctext(d, 1170, 270, "116편", F_BIG, NAVY); ctext(d, 1170, 360, "을 모아 보니", F_S, GRAY)
ctext(d, 1170, 420, "일터 팀 8,880개", F_S, GRAY)
box(d, DONE_BOX, SAND, "생각이 다른 것 자체는 팀 성과와 거의 관계가 없었다\n다름이 사람을 향한 감정으로 번지면 성과가 내려갔다", F_S, INK)
footc(d, "근거: 보강노트 ①-2 de Wit·Greer·Jehn 2012(116편, 8,880팀). 일터 팀 표본, 상관관계. 단톡방은 비유")
save(im, "C3_two_roads.png")

# ============ C4 의자 거리 ============
im, d = canvas("질문 2 — 「옳고 그름」의 문제가 되면, 의자부터 멀어진다", "미국 대학생 모둠 실험(사회 쟁점) — 결론이 아니라 「어떻게 정할지」에 합의한 비율")
for k, (cx, lab, gap, pct, col) in enumerate(((365, "옳고 그름과는 먼 주제", 120, "80%", GREEN), (1035, "옳고 그름의 문제로 느낀 주제", 245, "56%", PEOPLE))):
    ctext(d, cx, 168, lab, F_L, INK)
    d.ellipse([cx - 80, 330, cx + 80, 380], fill=(200, 175, 140))
    d.rectangle([cx - 6, 370, cx + 6, 420], fill=(170, 140, 100))
    for side, pc in ((-1, WORK), (1, AMBER)):
        px_ = cx + side * gap
        d.rounded_rectangle([px_ - 30, 380, px_ + 30, 410], radius=6, fill=(160, 160, 155))
        person(d, px_, 260, 130, pc)
    if gap > 200:
        for side in (-1, 1):
            arrow(d, (cx + side * 100, 455), (cx + side * 200, 455), GRAY, 4)
    ctext(d, cx, 470, pct, F_BIG, col)
    ctext(d, cx, 545, "「어떻게 정할지」 합의한 모둠", F_S, GRAY)
dashed(d, (700, 170), (700, 570), (200, 200, 195), 2)
box(d, DONE_BOX, SAND, "옳고 그름의 문제로 느낀 주제에서는 「어떻게 정할지」라는 방법에도 합의가 덜 됐다\n생각이 다른 상대와 앉을 의자도 더 멀리 놓았다(같은 논문의 다른 실험)", F_S, INK)
footc(d, "근거: 보강노트 ②-1 Skitka·Bauman·Sargis 2005(연구 4: 86개 모둠 · 연구 3: 대학생 80명). 사회 쟁점 표본")
save(im, "C4_chair_distance.png")

# ============ C5 미는 말, 듣는 귀 ============
im, d = canvas("질문 2 — 미는 말보다 듣는 귀, 10분 대화가 석 달을 갔다", "미국 현장실험 · 그림은 비유(부모님께 건강검진 권하기)")
# 왼쪽: 닫힌 문에 튕기는 화살표
d.rectangle([150, 200, 290, 500], fill=DOOR); d.rectangle([140, 190, 300, 200], fill=(120, 85, 55))
d.ellipse([262, 345, 276, 359], fill=(240, 210, 120))
for y in (260, 350, 440):
    arrow(d, (520, y), (310, y), PEOPLE, 6)
    arrow(d, (318, y + 6), (380, y + 44), (230, 150, 145), 3)
ctext(d, 290, 525, "논리로 밀기", F_H, PEOPLE)
# 오른쪽: 열린 문 + 귀
d.rectangle([640, 200, 780, 500], fill=(255, 238, 190)); d.rectangle([630, 190, 790, 200], fill=(120, 85, 55))
d.polygon([(640, 200), (690, 222), (690, 482), (640, 500)], fill=DOOR)
d.ellipse([860, 270, 975, 450], fill=SKIN); d.polygon([(860, 380), (900, 450), (870, 450)], fill=SKIN)
d.arc([880, 295, 955, 420], 160, 420, fill=(185, 130, 100), width=9)
d.arc([900, 330, 940, 390], 180, 400, fill=(185, 130, 100), width=6)
for k in range(3): d.arc([790 + k * 16, 330 - k * 14, 830 + k * 16, 390 + k * 14], -50, 50, fill=(150, 200, 170), width=4)
ctext(d, 820, 525, "듣고, 경험 나누기", F_H, GREEN)
d.rounded_rectangle([1010, 190, 1320, 540], radius=16, fill=MINT)
ctext(d, 1165, 210, "문 앞에서 나눈 대화", F_S, GRAY)
ctext(d, 1165, 245, "10분", F_BIG, GREEN)
down_arrow(d, 1165, 330, 60, (150, 200, 170), 40)
ctext(d, 1165, 395, "3개월", F_BIG, GREEN)
ctext(d, 1165, 475, "뒤에도 남았다", F_M, INK)
box(d, DONE_BOX, SAND, "논거만 쓴 대화는 효과가 없었다\n판단 없이 듣고 경험을 나눈 대화는 작게, 그러나 오래 태도를 움직였다", F_S, INK)
footc(d, "근거: 보강노트 ②-6 Broockman·Kalla 2016(501명, 3개월), ②-7 Kalla·Broockman 2020(6,869명). 효과는 작음")
save(im, "C5_push_vs_listen.png")

# ============ C6 월요일 아침의 옷장 ============
im, d = canvas("질문 3 — 이기면 「우리」, 못 이기면 「걔네」", "1976년 미국 대학 미식축구 연구 — 학교 팀 경기가 끝난 다음 월요일")
for k, (x0, lab, n_col, said, pct, col) in enumerate(((90, "이긴 뒤 월요일", 4, "우리가 이겼어", "32%", MAROON), (720, "못 이긴 뒤 월요일", 2, "걔네가 졌어", "18%", GRAY))):   # 12명 중 4명·2명 ≈ 32%·18%(모식)
    d.rounded_rectangle([x0, 160, x0 + 590, 585], radius=16, fill=WHITE, outline=(215, 212, 205), width=2)
    ltext(d, x0 + 30, 174, lab, F_H, INK)
    order = [0, 7, 2, 9, 4, 11, 1, 8, 3, 10, 5, 6]
    colored = set(order[:n_col])
    for i in range(12):
        r_, c_ = divmod(i, 6)
        person(d, x0 + 80 + c_ * 86, 296 + r_ * 92, 80, MAROON if i in colored else SHIRT)
    bubble(d, (x0 + 300, 222, x0 + 560, 270), said, F_M, WHITE, col, tail=((x0 + 425, 292), (x0 + 405, x0 + 440, 270)))
    ctext(d, x0 + 295, 476, pct, F_BIG, col)
    ctext(d, x0 + 295, 548, "경기 이야기에 「우리」를 쓴 비율 (색칠한 사람)", F_SM, GRAY)
box(d, DONE_BOX, SAND, "응원은 결과에 따라 붙었다 떨어졌다. 이긴 주 월요일엔 학교 옷을 입은 학생도 늘었다\n내 체면이 흔들린 날엔 이 차이가 더 컸다", F_S, INK)
footc(d, "근거: 보강노트 ③-1 Cialdini 외 1976(실험 2: 「we」 27/85 vs 15/83), ③-2 2016 재현. 12명 중 색칠은 비율 모식")
save(im, "C6_monday_closet.png")

# ============ C7 늦게 온 택배 ============
im, d = canvas("질문 4 — 택배가 늦으면, 문 앞의 얼굴부터 떠오른다", "그림은 비유 — 가까이서 보면 사람이, 멀리서 보면 길이 보인다")
G = 470
d.line([90, G, 560, G], fill=INK, width=3)
house(d, 110, G, 1.6)
parcel(d, 320, G, 0.9); clock(d, 356, 370, 24)
person(d, 480, 330, 140, NAVY)
d.ellipse([410, 300, 550, 480], outline=RED, width=4)
ctext(d, 480, 262, "먼저 떠오르는 얼굴", F_M, RED)
ctext(d, 325, 500, "가까이서 보면", F_H, INK)
dashed(d, (610, 170), (610, 570), (200, 200, 195), 2)
d.line([650, G, 1320, G], fill=INK, width=3)
d.polygon([(680, 300), (790, 250), (900, 300)], fill=(140, 145, 155)); d.rectangle([690, 300, 890, G], fill=(175, 180, 190))
for k in range(3): d.rectangle([710 + k * 60, 380, 750 + k * 60, G], fill=(130, 135, 145))
d.line([700, 280, 880, 460], fill=RED, width=10); d.line([880, 280, 700, 460], fill=RED, width=10)
for k in range(4):
    hx = 935 + k * 95; house(d, hx, G, 0.62); parcel(d, hx + 50, G, 0.32); clock(d, hx + 62, G - 105, 13)
ctext(d, 1115, 300, "그 주에 늦은 집들", F_M, INK)
ctext(d, 790, 212, "물류센터가 멈췄다", F_M, RED)
ctext(d, 985, 500, "멀리서 보면", F_H, INK)
box(d, DONE_BOX, SAND, "상황이 만든 일도 그 사람의 성향 탓으로 읽는 습관을 심리학은 「대응 편향」이라 부른다\n사고 연구는 「개인을 탓하는 쪽이 제도를 겨누는 것보다 감정적으로 더 만족스럽다」고 적는다", F_S, INK)
footc(d, "근거: 보강노트 ④-3 Gilbert·Malone 1995(대응 편향 리뷰), ④-4 Reason 2000(BMJ). 택배는 비유")
save(im, "C7_late_parcel.png")

# ============ C8 규정이 비워 둔 자리 ============
im, d = canvas("규정이 비워 둔 자리 — 운영규정에 「주장」은 0번", "대한축구협회 「축구국가대표팀 운영규정」 2026년 1월 개정판(12쪽) 본문")
d.rounded_rectangle([330, 308, 520, 382], radius=37, fill=SKIN); d.ellipse([480, 296, 560, 394], fill=SKIN)
d.rounded_rectangle([90, 296, 400, 394], radius=30, fill=WORK)
d.rectangle([255, 286, 345, 404], fill=(240, 200, 40)); ctext(d, 300, 302, "C", F_BIG, INK)
ctext(d, 300, 425, "주장 완장", F_H, INK)
ctext(d, 300, 472, "「특별한 지위나 특권은 없다」", F_M, NAVY)
ctext(d, 300, 510, "FIFA 경기규칙 제3조", F_S, GRAY)
d.rounded_rectangle([600, 160, 1000, 580], radius=10, fill=PAPER, outline=(190, 185, 175), width=3)
ctext(d, 800, 176, "대표팀 구성 (제5조)", F_M, INK)
for k, t in enumerate(("단장", "감독", "코치", "지원인력", "선수")):
    y = 228 + k * 56
    check(d, 660, y + 16, 14); ltext(d, 690, y, t, F_L, INK, 990)
    d.line([690, y + 42, 960, y + 42], fill=(225, 222, 214), width=2)
dashed_rect(d, (640, 510, 965, 562), RED, 3); ltext(d, 690, 518, "주장", F_L, (200, 150, 150), 990)
ctext(d, 910, 516, "?", F_L, RED)
d.rounded_rectangle([1040, 200, 1320, 520], radius=16, fill=PINK)
ctext(d, 1180, 225, "「주장」이라는 말", F_M, INK); ctext(d, 1180, 265, "0번", F_HUGE, RED)
ctext(d, 1180, 380, "본문 12쪽 전체에서", F_S, GRAY)
box(d, DONE_BOX, SAND, "경기규칙은 주장에게 「특별한 지위나 특권은 없다」고 적는다\n누가, 어떤 기준으로, 언제까지 맡는지는 규정에 없다 — 지금까지는 감독이 정해 왔다", F_S, INK)
footc(d, "근거: 보강노트 ④-13(KFA 운영규정 2026.1.27 PDF 낱말 세기), 공부노트 1-3(IFAB 경기규칙 제3조 10항 KFA 대역본)")
save(im, "C8_empty_seat.png")

# ============ C9 리더 역할 넷 ============
im, d = canvas("「네 역할 모두 주장」이라고 답한 사람은 1%", "벨기에 9개 종목 선수·코치 4,451명에게 자기 팀의 역할별 리더를 물었다 — 네 역할 모두 주장을 꼽은 응답")
tiles = (("작전", "경기 안", "board"), ("기운", "경기 안", "mega"), ("분위기", "경기 밖", "heart"), ("바깥 창구", "경기 밖", "door"))
for k, (lab, where, ic) in enumerate(tiles):
    r_, c_ = divmod(k, 2); x0 = 90 + c_ * 270; y0 = 165 + r_ * 210
    d.rounded_rectangle([x0, y0, x0 + 250, y0 + 195], radius=16, fill=WHITE, outline=(215, 212, 205), width=2)
    cx, cy = x0 + 125, y0 + 70
    if ic == "board": tactic_board(d, cx, cy)
    elif ic == "mega": megaphone(d, cx - 6, cy, AMBER)
    elif ic == "heart": heart(d, cx, cy + 4, 2.6, PEOPLE)
    else: door_ic(d, cx - 14, cy, NAVY)
    ctext(d, cx, y0 + 122, lab, F_L, INK); ctext(d, cx, y0 + 160, where, F_SM, GRAY)
GX, GY, C = 690, 190, 30
for i in range(100):
    r_, c_ = divmod(i, 10)
    col = (240, 180, 40) if i == 0 else (222, 220, 214)
    d.rounded_rectangle([GX + c_ * (C + 4), GY + r_ * (C + 4), GX + c_ * (C + 4) + C, GY + r_ * (C + 4) + C], radius=5, fill=col)
ctext(d, GX + 168, 535, "응답자 100명 중", F_M, GRAY)
d.rounded_rectangle([1070, 200, 1320, 520], radius=16, fill=SAND)
ctext(d, 1195, 225, "네 칸 모두 주장", F_M, INK); ctext(d, 1195, 275, "1%", F_HUGE, (200, 140, 20))
ctext(d, 1195, 400, "한 칸도 주장이", F_S, GRAY); ctext(d, 1195, 430, "아니라고 답한 사람", F_S, GRAY); ctext(d, 1195, 470, "44%", F_L, GRAY)
box(d, DONE_BOX, SAND, "작전·기운·분위기·바깥 창구는 대개 여러 사람에게 나뉘어 있었다\n완장은 한 사람이 차도, 리더 역할은 팀 곳곳에 흩어져 있다", F_S, INK)
footc(d, "근거: Fransen 외 2014(J Sports Sci) 원문 결과 절 — 참가자 1%·43.6%(응답자 기준, 응답률 27%). 리더십논문 보강 3장")
save(im, "C9_four_roles.png")

# ============ C10 다시 정하는 단위 ============
im, d = canvas("같은 「감독 지명」, 다시 정하는 단위가 다르다", "대표팀 주장 지명 방식, 2018년 9월부터 2026년 10월까지 — 한국 · 일본 (모식)")
AX0, AX1, T0, T1 = 350, 1290, 2018.5, 2026.95
def tx(t): return AX0 + (t - T0) / (T1 - T0) * (AX1 - AX0)
for yr in range(2019, 2027):
    x = tx(yr); d.line([x, 220, x, 520], fill=(232, 230, 224), width=1); ctext(d, x, 525, str(yr), F_SM, GRAY)
# 한국
ltext(d, 90, 232, "한국", F_H, INK); ltext(d, 90, 272, "한 번 정해 이어 가기", F_S, GRAY, AX0 - 10)
d.rounded_rectangle([tx(2018.69), 240, tx(2026.79), 290], radius=25, fill=WORK)
ctext(d, (tx(2018.69) + tx(2026.79)) / 2, 248, "한 번 지명 → 감독이 바뀌어도 유지", F_M, WHITE)
for t in (2023.15, 2024.55, 2026.67):
    x = tx(t); d.polygon([(x, 300), (x - 11, 320), (x + 11, 320)], fill=NAVY)
d.polygon([(tx(2019.2), 334), (tx(2019.2) - 9, 350), (tx(2019.2) + 9, 350)], fill=NAVY)
ltext(d, tx(2019.2) + 16, 330, "감독이 바뀐 때", F_SM, GRAY)
# 일본
ltext(d, 90, 412, "일본", F_H, INK); ltext(d, 90, 452, "소집마다 다시 지명", F_S, GRAY, AX0 - 10)
JC = [(230, 140, 40), (90, 160, 120), (150, 90, 170), (60, 140, 200), (210, 90, 110)]
t = 2018.69; stamps = []
while t <= 2026.46:
    if t < 2018.8: c = 0
    elif 2022.0 <= t < 2022.12: c = 2
    elif t < 2023.1: c = 1
    elif t < 2026.15: c = 2
    elif t < 2026.35: c = 3
    else: c = 4
    stamps.append((t, c)); t += 0.27
stamps[-1] = (2026.45, 4)
for (t, c) in stamps:
    x = tx(t); d.ellipse([x - 13, 425, x + 13, 451], fill=JC[c], outline=WHITE, width=2)
ltext(d, tx(2019.2), 470, "도장 하나 = 소집 한 번 · 색 = 그때의 주장", F_SM, GRAY)
box(d, DONE_BOX, SAND, "두 나라 모두 주장은 감독이 정한다. 일본도 2010년부터 2018년까지는 한 주장이 이어졌다\n다른 것은 사람이 아니라 「언제 다시 정하나」라는 단위다", F_S, INK)
footc(d, "근거: 공부노트 3-1(KFA 집계·서울신문 2018.9.7 / 일본 감독 회견·JFA 2026.6.11 발표). 띠·도장 수와 간격은 모식")
save(im, "C10_two_ways_to_name.png")

# ============ C11 구멍 난 치즈 여러 장 ============
im, d = canvas("질문 4 — 구멍 하나로는 일이 커지지 않는다", "사고 연구의 「스위스 치즈」 비유 — 원인을 한 장에서만 찾지 않는다")
AY = 345
HOLES = [[(40, 250, 18), (100, 450, 22)], [(50, 470, 20), (110, 230, 16)], [(40, 230, 20), (105, 460, 16)], [(45, 455, 18), (110, 260, 22)]]
SX = (230, 450, 670, 890)
for k, x in enumerate(SX):
    d.polygon([(x, 205), (x + 140, 175), (x + 140, 495), (x, 525)], fill=CHEESE, outline=CHEESE_D)
    d.line([x, 205, x + 140, 175, x + 140, 495, x, 525, x, 205], fill=CHEESE_D, width=3)
    for (hx, hy, r) in HOLES[k]: d.ellipse([x + hx - r, hy - r, x + hx + r, hy + r], fill=(225, 175, 60))
    d.ellipse([x + 70 - 26, AY - 26 - 0, x + 70 + 26, AY + 26], fill=BG, outline=CHEESE_D, width=2)
arrow(d, (110, AY), (1130, AY), RED, 8)
for x, lab in zip(SX, ("규정", "지명 방식", "소통 창구", "선수")):
    ctext(d, x + 70, 536, lab, F_L, INK)
ctext(d, SX[0] + 70, 572, "「주장」 0번", F_SM, GRAY)
ctext(d, 1225, 318, "일이", F_M, RED); ctext(d, 1225, 352, "커진다", F_M, RED)
box(d, DONE_BOX, SAND, "구멍이 하나도 없는 장은 없다. 구멍 여러 개가 한 줄로 설 때 일이 커진다\n그래서 이 비유는 「누가 틀렸나」보다 「어느 막들이 함께 비었나」를 먼저 묻는다", F_S, INK)
footc(d, "근거: 보강노트 ④-4 Reason 2000(BMJ), ④-13. 의료·항공 사고 연구의 비유일 뿐, 대표팀 일을 사고로 본다는 뜻은 아님")
save(im, "C11_cheese_slices.png")

# ============ C12 할 일 하나 ============
im, d = canvas("할 일 하나 — 단톡방의 「다름」을 두 바구니에 나눠 보기", "우리 팀·회사·가족 단톡방에서, 최근 생각이 갈렸던 대화 하나만 골라서")
phone(d, 150, 160, 330, 425)
d.rectangle([164, 200, 466, 236], fill=NAVY); ctext(d, 315, 205, "가족 여행 계획", F_S, WHITE)
MSG = (("제주 말고 부산 어때?", "L", WORK), ("숙소는 내가 알아볼게", "R", None), ("넌 맨날 네 마음대로잖아", "L", PEOPLE), ("그럼 투표로 정하자", "R", None))
ys = []
for k, (t, side, hl) in enumerate(MSG):
    y = 256 + k * 70; w = d.textlength(t, font=F_SM) + 30
    x0 = 178 if side == "L" else 452 - w
    d.rounded_rectangle([x0, y, x0 + w, y + 42], radius=16, fill=WHITE if side == "L" else (255, 236, 150), outline=hl, width=4 if hl else 0)
    d.text((x0 + 15, y + 9), t, font=F_SM, fill=INK); ys.append(y + 21)
    if x0 + w > 458: WARN.append(f"말풍선 넘침: {t}")
basket(d, 760, 200, 1060, 350, WORK, "일")
basket(d, 760, 420, 1060, 570, PEOPLE, "사람")
arrow(d, (452, ys[0]), (740, 270), WORK, 5)
arrow(d, (452, ys[2]), (740, 490), PEOPLE, 5)
d.rounded_rectangle([1110, 230, 1320, 520], radius=16, fill=LIGHT)
ctext(d, 1215, 255, "우리 방은", F_M, INK); ctext(d, 1215, 300, "?", F_HUGE, NAVY)
ctext(d, 1215, 420, "어느 쪽이", F_S, GRAY); ctext(d, 1215, 452, "더 찼을까", F_S, GRAY)
box(d, DONE_BOX, SAND, "생각이 갈린 문장은 「일」 바구니, 사람을 향한 문장은 「사람」 바구니에 한 번 나눠 본다\n어느 쪽이 더 찼는지는 나만 알면 된다", F_S, INK)
footc(d, "그림은 모식 — 갈림길 비유는 그림 3, 근거는 보강노트 ①-2(일터 팀 연구 116편)")
save(im, "C12_two_baskets.png")

# ================= 10.15 보강 6장 (주장_리더십논문_보강_2026-10-15.md) =================
def armband(d, cx, cy, s=1.0):
    d.rounded_rectangle([cx - 150 * s, cy - 40 * s, cx + 150 * s, cy + 40 * s], radius=int(28 * s), fill=WORK)
    d.rectangle([cx - 42 * s, cy - 50 * s, cx + 42 * s, cy + 50 * s], fill=(240, 200, 40)); _ctext(d, cx, cy - 34 * s, "C", F_BIG, INK)
def hand_up(d, cx, top, h, col):
    sx, sy = cx + h * 0.16, top + h * 0.42
    d.line([sx, sy, sx + h * 0.12, top - h * 0.02], fill=col, width=max(int(h * 0.11), 4))
    r = h * 0.09; d.ellipse([sx + h * 0.12 - r, top - h * 0.02 - r * 1.6, sx + h * 0.12 + r, top - h * 0.02 + r * 0.4], fill=col)
def equal_sign(d, cx, cy, col=GRAY, w=60):
    d.rounded_rectangle([cx - w / 2, cy - 16, cx + w / 2, cy - 6], radius=4, fill=col)
    d.rounded_rectangle([cx - w / 2, cy + 6, cx + w / 2, cy + 16], radius=4, fill=col)

# ============ C13 같은 완장, 다른 기대 (C8 옆) ============
im, d = canvas("같은 완장을 두고, 먼저 떠올린 것이 달랐다", "대학 축구팀 지도자·주장·선수 69명에게 「주장의 가장 큰 역할」을 물었다")
armband(d, 700, 205, 0.7)
for x, who, said, col, first in ((260, "지도자", "내 대신 팀을 이끌어 줘", NAVY, "1순위 — 지도자 대행"), (700, "주장", "사람이 먼저", GREEN, "1순위 — 인성"), (1140, "선수", "사람이 먼저", GREEN, "1순위 — 인성")):
    dashed(d, (700, 250), (x, 300), (190, 188, 180), 2)
    bubble(d, (x - 170, 300, x + 170, 352), said, F_M, WHITE, col, tail=((x, 378), (x - 18, x + 18, 352)))
    person(d, x, 385, 120, col)
    ctext(d, x, 512, who, F_H, INK); ctext(d, x, 555, first, F_S, GRAY)
box(d, DONE_BOX, SAND, "같은 자리를 두고 감독은 「내 대리인」을, 주장과 선수는 「사람됨」을 먼저 떠올렸다\n규정이 비워 둔 자리를, 사람마다 다른 기대가 채우고 있었다", F_S, INK)
footc(d, "근거: 리더십논문 보강 1-3 이종훈·황재욱·육동원 2019(코칭능력개발지, 대학 축구 69명, 설문·면담). 빈도 미확인")
save(im, "C13_same_band.png")

# ============ C14 역할을 나눠 맡긴 팀 (C9 옆) ============
im, d = canvas("리더 역할을 나눠 맡긴 팀, 한 시즌 뒤", "벨기에 농구 8팀 96명 실험 — 4팀은 역할을 나눠 맡고 「우리」를 다지는 연습, 4팀은 평소대로")
BANDS = (WORK, AMBER, GREEN, PEOPLE)
for x0, lab, banded in ((90, "역할을 나눠 맡은 팀", (0, 1, 2, 3)), (720, "평소대로인 팀", (1,))):
    d.rounded_rectangle([x0, 160, x0 + 590, 350], radius=16, fill=WHITE, outline=(215, 212, 205), width=2)
    ltext(d, x0 + 24, 172, lab + ("  — 역할마다 다른 사람" if len(banded) > 1 else ""), F_M, INK)
    for k in range(4):
        cx = x0 + 110 + k * 125
        person(d, cx, 215, 120, BANDS[k] if k in banded else SHIRT)
for k, (lab, same) in enumerate((("팀 소속감", False), ("하려는 마음(동기)", False), ("팀 자신감 · 성적에 대한 느낌", True))):
    y = 372 + k * 72
    d.rounded_rectangle([90, y, 1310, y + 60], radius=12, fill=LIGHT if not same else (243, 243, 240))
    ltext(d, 120, y + 14, lab, F_M, INK)
    if same: equal_sign(d, 700, y + 30); ltext(d, 750, y + 14, "두 쪽이 같았다", F_M, GRAY)
    else: up_arrow(d, 700, y + 54, 48, GREEN, 30); ltext(d, 750, y + 14, "나눠 맡은 팀 쪽이 더 높게 남았다", F_M, GREEN)
box(d, DONE_BOX, SAND, "리더 역할을 여럿이 나눠 맡자 소속감과 하려는 마음은 시즌 뒤까지 지켜졌다\n팀 자신감과 성적에 대한 느낌은 평소대로인 팀과 같았다", F_S, INK)
footc(d, "근거: 보강 4-1 Mertens 외 2020(J Sci Med Sport, 5R 프로그램). 나눠 맡은 팀이 출발점부터 높았다 — 작은 실험")
save(im, "C14_shared_roles.png")

# ============ C15 오래 질 때 원한 것 (질문 4) ============
im, d = canvas("오래 질 때 선수들이 더 원한 건 「지시」가 아니었다", "노르웨이 엘리트 축구 선수 88명 — 잘 풀릴 때와 오래 질 때, 감독에게 바라는 행동")
CARDS = (("훈련·작전 설명", "board"), ("칭찬·피드백", "check"), ("의견 묻기", "table"), ("챙겨 주기", "heart"), ("지시", "bang"))
for k, (lab, ic) in enumerate(CARDS):
    x0 = 94 + k * 248; cx = x0 + 110; last = ic == "bang"
    d.rounded_rectangle([x0, 165, x0 + 220, 480], radius=16, fill=WHITE if not last else (243, 243, 240), outline=(215, 212, 205), width=2)
    if ic == "board": tactic_board(d, cx, 235)
    elif ic == "check": d.ellipse([cx - 40, 195, cx + 40, 275], fill=MINT); check(d, cx, 235, 26)
    elif ic == "table": ic_table(d, cx, 240)
    elif ic == "heart": heart(d, cx, 240, 2.4, PEOPLE)
    else: d.ellipse([cx - 40, 195, cx + 40, 275], fill=NAVY); _ctext(d, cx, 205, "!", F_BIG, WHITE)
    ctext(d, cx, 295, lab, F_M, INK)
    if last: equal_sign(d, cx, 385, GRAY, 70); ctext(d, cx, 430, "그대로", F_M, GRAY)
    else: up_arrow(d, cx, 420, 80, GREEN, 46); ctext(d, cx, 430, "더 원했다", F_M, GREEN)
ctext(d, 700, 520, "잘 풀릴 때 → 오래 질 때", F_M, GRAY)
box(d, DONE_BOX, SAND, "길을 잃은 차 안에서 바라는 말이 「내 말대로 가」보다 「지도를 같이 보자」에 가까웠던 셈이다\n지시만 빼고 나머지 네 가지 감독 행동을 모두 더 원했다", F_S, INK)
footc(d, "근거: 보강 2-1 Høigaard·Jones·Peters 2008(Int J Sports Sci Coach, 88명). 가상 시나리오 응답 · 길 잃은 차는 비유")
save(im, "C15_when_losing.png")

# ============ C16 상황이 세 배 (질문 4) ============
im, d = canvas("「누가 정할까」는 사람보다 상황이 더 가른다", "대학 농구 선수 99명·코치 22명 · 결정 상황 32가지마다 「감독 혼자」부터 「다 같이」까지 골랐다")
L, R = (200, 270), (760, 190)
d.polygon([(420, 565), (540, 565), (480, 230)], fill=(150, 150, 145))
d.line([L, R], fill=INK, width=10); d.ellipse([468, 218, 492, 242], fill=INK)
for (px, py), n, lab, col in ((L, 3, "상황 차이", NAVY), (R, 1, "사람마다 다른 성향", GRAY)):
    d.line([px - 80, py + 155, px, py], fill=GRAY, width=3); d.line([px + 80, py + 155, px, py], fill=GRAY, width=3)
    d.chord([px - 100, py + 120, px + 100, py + 190], 0, 180, fill=(200, 195, 185))
    for k in range(n):
        d.rounded_rectangle([px - 42, py + 155 - 44 * (k + 1) + 4, px + 42, py + 155 - 44 * k], radius=6, fill=col)
    ctext(d, px, py + 200, lab, F_M, col)
d.rounded_rectangle([960, 190, 1320, 520], radius=16, fill=LIGHT)
ctext(d, 1140, 215, "선택을 가른 몫", F_M, INK); ctext(d, 1140, 260, "3배", F_HUGE, NAVY)
ctext(d, 1140, 390, "상황 쪽이", F_S, GRAY); ctext(d, 1140, 422, "사람 쪽보다", F_S, GRAY)
box(d, DONE_BOX, SAND, "같은 사람도 회식 장소는 「다 같이」 정하자 하고, 내일 출발 시간은 「누가 정해 줘」 한다\n수직이냐 수평이냐는 그 사람의 성격보다 지금이 어떤 상황이냐에 더 달려 있었다", F_S, INK)
footc(d, "근거: 보강 2-2 Chelladurai·Haggerty·Baxter 1989(J Sport Exerc Psychol). 상황에 위기·시간 압박은 없었다 · 회식은 비유")
save(im, "C16_situation_x3.png")

# ============ C17 「그건 아니다」라는 손 (질문 2·4) ============
im, d = canvas("지도자가 권위적일수록, 「그건 아니다」라는 말이 줄었다", "중국 대학 팀 종목 선수 256명 설문 — 잘못된 걸 잘못됐다고 말하는 정도")
for x0, lab, ups in ((90, "덜 권위적인 지도자", (0, 2, 4)), (720, "더 권위적인 지도자", (3,))):
    d.rounded_rectangle([x0, 160, x0 + 590, 440], radius=16, fill=WHITE, outline=(215, 212, 205), width=2)
    ltext(d, x0 + 24, 172, lab, F_M, INK)
    person(d, x0 + 95, 250, 150, NAVY)
    d.rounded_rectangle([x0 + 170, 352, x0 + 560, 372], radius=6, fill=(200, 175, 140))
    for k in range(5):
        cx = x0 + 215 + k * 78
        if k in ups: hand_up(d, cx, 270, 90, (120, 120, 115))
        person(d, cx, 270, 90, SHIRT if k not in ups else (120, 120, 115))
for k, (t, col) in enumerate((("권위적인 지도", NAVY), ("「말해도 괜찮다」 ↓", PEOPLE), ("「내가 바꿀 수 있다」 ↓", PEOPLE), ("「그건 아니다」 ↓", PEOPLE))):
    x = 90 + k * 310
    d.rounded_rectangle([x, 470, x + 270, 540], radius=14, fill=WHITE, outline=col, width=3)
    ctext(d, x + 135, 488, t, F_S, col)
    if k < 3: arrow(d, (x + 274, 505), (x + 306, 505), GRAY, 4)
box(d, DONE_BOX, SAND, "지도자가 권위적일수록 「말해도 괜찮다」는 느낌이 줄었고, 그 길을 거쳐 「그건 아니다」도 줄었다\n누가 옳은지가 아니라, 다른 말이 나올 수 있는 자리인지에 관한 연구다", F_S, INK)
footc(d, "근거: 보강 1-15 부얀·김대희 2026(AJPESS, 256명). 총효과 -0.31(95% CI -0.43, -0.19) · 중국 선수·한 번 조사, 손 수는 모식")
save(im, "C17_hands_up.png")

# ============ C18 일로 뭉치기 vs 사람으로 뭉치기 (C3 옆) ============
im, d = canvas("「일로 뭉치기」가 「사람으로 뭉치기」보다 성적과 가까웠다", "스포츠 팀 응집력 연구들을 모은 분석 · 그림은 비유(이삿짐 나르는 친구들)")
ctext(d, 1010, 165, "성적과 함께 움직인 정도(상관)", F_S, GRAY)
for k, (lab, v, col, kind) in enumerate((("일로 뭉치기", .45, WORK, "box"), ("사람으로 뭉치기", .11, PEOPLE, "heart"))):
    y = 205 + k * 190
    d.rounded_rectangle([90, y, 1310, y + 165], radius=16, fill=WHITE, outline=(215, 212, 205), width=2)
    person(d, 175, y + 25, 120, col); person(d, 345, y + 25, 120, col)
    if kind == "box": d.rectangle([205, y + 70, 315, y + 120], fill=(190, 145, 95)); d.line([205, y + 95, 315, y + 95], fill=(150, 110, 70), width=3)
    else: heart(d, 260, y + 70, 1.8, PEOPLE)
    ltext(d, 430, y + 60, lab, F_H, col, 700)
    d.rounded_rectangle([720, y + 60, 720 + int(v * 1100), y + 105], radius=10, fill=col)
    ltext(d, 735 + int(v * 1100), y + 64, ("%.2f" % v)[1:], F_H, col, 1300)
box(d, DONE_BOX, SAND, "같은 목표를 향해 함께 일하는 뭉침이, 서로 친한 뭉침보다 성적과 더 가까웠다\n다만 축구 대표팀 8곳 조사에서는 일 갈등과 사람 갈등이 한데 붙어 움직였다(상관 .75)", F_S, INK)
footc(d, "근거: 보강 4-4 Filho 외 2014(2차, Lochbaum 2022 표)·Carron 외 2002(46편) · 4-4c López-Gajardo 외 2022(170명)")
save(im, "C18_work_vs_people.png")

print("\n".join(WARN) if WARN else "넘침 경고 없음")
