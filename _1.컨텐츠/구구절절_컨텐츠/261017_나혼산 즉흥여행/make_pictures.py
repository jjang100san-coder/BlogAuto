# -*- coding: utf-8 -*-
"""나혼산 즉흥 여행 글 — 일반인용 그림(2026-10-17). 본편 N1~N7, 한 걸음 더 H1~H4.
줄기: 내 여행 글 68편을 세어 보니 큰 예약은 96% 미리, 그날 정한 건 40%만 미리 → 「즉흥」이라 쓴 글 다섯 편도 넷은 큰 예약이 먼저
      → 후쿠오카(동행 일정표, 나는 숙소·비행기만) → 「즉흥」의 뜻 세 가지 → 7/22 공문부터 10/16 보도까지 → 방송은 「알릴 수 있다」·유튜브는 「알려야 한다」
      → 할 일 하나(다음 여행 메모에 「그날 정하기」 한 줄).
숫자: base data\내여행글_예약비율_옛신문_2026-10-17.md(직접 센 값), 나혼산_논란타임라인_2026-10-17.md, 협찬고지_규칙원문_2026-10-17.md.
판정 없음. 의원 이름·인물 얼굴 없음. 마스터 3-1: 쉬는 말(문·칸·계단·뚜껑)과 「조건」 쓰지 않음."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
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

WARN = []
def save(im, n):
    im.save(os.path.join(OUT, n)); print("saved", n)
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
def ctext(d, cx, y, text, f, color=INK):
    w = d.textlength(text, font=f)
    if cx - w / 2 < 20 or cx + w / 2 > W - 20: WARN.append(f"가운데 글자 넘침: {text}")
    _ctext(d, cx, y, text, f, color)
def ltext(d, x, y, text, f, color=INK, right=None):
    w = d.textlength(text, font=f)
    if x + w > (right or W - 20): WARN.append(f"글자 넘침: {text}")
    d.text((x, y), text, font=f, fill=color)

PRE = NAVY; ONS = AMBER; UNK = (200, 200, 196); SOFT = (238, 234, 222)

def dashed(d, p0, p1, col=GRAY, w=2, dash=10):
    import math
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L // (dash * 2)))
    for k in range(n):
        a = k * 2 * dash / L; b = min(1, (k * 2 + 1) * dash / L)
        d.line([x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b], fill=col, width=w)

def split_bar(d, x, y, w, h, a, b, ca=PRE, cb=ONS, labels=True):
    """a(미리) : b(현장) 가로 막대"""
    t = a + b; wa = w * a / t
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=cb)
    if a:
        d.rounded_rectangle([x, y, x + wa, y + h], radius=12, fill=ca)
        if b: d.rectangle([x + wa - 12, y, x + wa, y + h], fill=ca)
    if labels:
        if wa > 90: ctext(d, x + wa / 2, y + h / 2 - 16, f"미리 {a}", F_M, WHITE)
        if w - wa > 90: ctext(d, x + wa + (w - wa) / 2, y + h / 2 - 16, f"현장 {b}", F_M, WHITE)

def note_sheet(d, x, y, w, h, lines, title, tcol=INK, lcol=(205, 205, 200), filled=None):
    """메모지: lines 개 줄, filled 는 글자 있는 줄 목록 [(i, text, col)]"""
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=WHITE, outline=(190, 190, 185), width=3)
    ctext(d, x + w / 2, y + 14, title, F_M, tcol)
    fl = {i: (t, c) for i, t, c in (filled or [])}
    for i in range(lines):
        yy = y + 64 + i * 46
        if i in fl:
            t, c = fl[i]
            d.rounded_rectangle([x + 18, yy - 4, x + w - 18, yy + 34], radius=8, fill=c)
            ltext(d, x + 30, yy, t, F_S, WHITE, right=x + w - 20)
        else:
            d.rounded_rectangle([x + 24, yy + 10, x + w - 24 - (i % 3) * 30, yy + 22], radius=6, fill=lcol)

# ============ N1 큰 예약 96% vs 그날 정한 것 40% (첫 그림 = 실제 숫자) ============
im, d = canvas("내 여행 글 68편을 세어 보니, 큰 예약은 96%가 미리였다",
               "블로그 여행 후기 68편(여행 18번)에서 「언제 정했나」가 적힌 159가지를 직접 셌다")
rows = (("항공·숙소·렌터카·투어", 48, 2, "96%"), ("동선·식당·현지 교통", 29, 44, "40%"))
for k, (lab, a, b, pc) in enumerate(rows):
    y = 210 + k * 170
    ltext(d, 90, y - 46, lab, F_H, INK)
    split_bar(d, 90, y, 980, 80, a, b)
    ctext(d, 1200, y - 4, pc, F_BIG, PRE)
    ctext(d, 1200, y + 62, "미리 정한 비율", F_S, GRAY)
d.rounded_rectangle([90, 545, 120, 565], radius=5, fill=PRE); ltext(d, 130, 541, "미리(그날 전에 정함)", F_S, INK)
d.rounded_rectangle([420, 545, 450, 565], radius=5, fill=ONS); ltext(d, 460, 541, "현장(그 자리에서 정함)", F_S, INK)
ltext(d, 760, 541, "글만으로 언제 정했는지 알 수 없는 36가지는 뺐다", F_S, GRAY)
box(d, (90, 600, 1310, 700), SAND, "합치면 미리 77 : 현장 46, 미리가 63%다. 그런데 무엇을 정했느냐에 따라 확 갈렸다@@비행기·숙소는 하나도 빠짐없이 미리 잡았고, 그날 어디로 갈지·뭘 먹을지는 절반 넘게 현장에서 정했다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 블로그 「걷고읽고떠나고」 여행 후기 본문을 직접 읽고 센 값(2026.10.17). 같은 항목은 한 번만 셌다")
save(im, "N1_big_bookings_first.png")

# ============ N2 「즉흥」이라 쓴 글 다섯 편 ============
im, d = canvas("「즉흥」이라고 쓴 내 글 다섯 편, 넷은 큰 예약이 먼저 있었다",
               "왼쪽은 글에 쓴 말, 오른쪽은 같은 여행에서 미리 해 둔 것 — 본문에서 그대로 찾았다")
R = (("2024.3 맨체스터", "「아무 계획 없이」", "기차는 앱으로 미리 예약", True),
     ("2025.11 화담숲", "「번개로 가자고 해서」", "대기번호 76,043번, 두 달 전 예약", True),
     ("2023.6 교토", "「즉흥적으로 들어간 집」", "왕복 항공권 2인, 미리 결제", True),
     ("2023.11 후쿠오카", "「일정표도 안 짰어」", "숙소 두 곳, 미리 예약", True),
     ("2019.5 미국 주말", "「계획이랄 게 없었어」", "큰 예약 없음 — 사는 곳에서 차로 나섬", False))
for k, (when, said, pre, ok) in enumerate(R):
    y = 175 + k * 80
    d.rounded_rectangle([90, y, 1310, y + 64], radius=14, fill=WHITE if ok else SOFT, outline=(215, 212, 205), width=2)
    ltext(d, 112, y + 16, when, F_S, GRAY, right=330)
    ltext(d, 330, y + 14, said, F_M, ONS, right=700)
    arrow(d, (712, y + 32), (782, y + 32), GRAY, 4)
    ltext(d, 800, y + 14, pre, F_M, PRE if ok else GRAY, right=1230)
    if ok: check(d, 1270, y + 32, 18, PRE)
box(d, (90, 600, 1310, 700), SAND, "즉흥이라고 쓴 글 다섯 편 가운데 넷은, 같은 여행의 비행기·숙소·입장권을 미리 잡아 두었다@@큰 예약이 하나도 없던 건 사는 곳에서 차를 몰고 나선 주말 한 번뿐이다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 각 글 본문 문장(2026.10.17 직접 확인). 화담숲 대기번호·두 달 전 예약은 화담숲 예약 글 본문")
save(im, "N2_five_impromptu_posts.png")

# ============ N3 후쿠오카 — 동행은 일정표, 나는 숙소·비행기만 ============
im, d = canvas("셋이 간 후쿠오카, 내 메모엔 두 줄뿐이었다",
               "2023년 11월 2박3일 — 동행 둘은 일정표대로 다녔고, 나는 비행기와 숙소만 잡고 갔다")
fullA = [(i, "", PRE) for i in range(6)]
note_sheet(d, 110, 170, 330, 360, 6, "동행의 일정표", filled=fullA)
note_sheet(d, 500, 170, 330, 360, 6, "동행의 일정표", filled=fullA)
note_sheet(d, 890, 170, 400, 360, 6, "내 메모", tcol=ONS, filled=[(0, "비행기 왕복", ONS), (1, "숙소 두 곳", ONS)])
d.rectangle([905, 326, 1275, 520], fill=WHITE)
ctext(d, 1090, 400, "나머지는 비워 둠", F_M, GRAY)
box(d, (90, 600, 1310, 700), SAND, "「솔직히 완전 무계획으로 갈 배짱은 없던 거지.」 — 그래서 글에는 「일정표도 안 짰어」라고 썼다@@일정표는 동행의 것이었고, 내 메모엔 비행기와 숙소 두 줄만 있었다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 블로그 후쿠오카 11월 글 두 편 + 본인 확인(2026.10.17). 일정표 그림은 모식")
save(im, "N3_fukuoka_two_lines.png")

# ============ N4 「즉흥」의 뜻 세 가지 ============
im, d = canvas("「즉흥」이라는 말, 세 곳에서 다르게 쓰였다",
               "사전 뜻풀이와, MBC가 9월 4일 입장문에서 쓴 두 문장 — 원문 그대로")
Q = (("표준국어대사전 「즉흥」", ("「그 자리에서 바로", "일어나는 감흥.", "또는 그런 기분.」"), NAVY),
     ("MBC가 말한 「즉흥 여행」", ("「목적지와 항공권을", "미리 정하지 않은 채 당일", "여행지를 결정해 떠나는 방식」"), ONS),
     ("MBC가 덧붙인 문장", ("「모든 과정이 아무런 사전", "준비 없이 진행된 것으로 받아", "들여질 수 있다는 점」"), RED))
for k, (who, lines, col) in enumerate(Q):
    x = 90 + k * 415
    d.rounded_rectangle([x, 175, x + 390, 545], radius=18, fill=WHITE, outline=col, width=4)
    d.rounded_rectangle([x, 175, x + 390, 235], radius=18, fill=col); d.rectangle([x, 215, x + 390, 235], fill=col)
    ctext(d, x + 195, 188, who, F_M, WHITE)
    for j, ln in enumerate(lines):
        ctext(d, x + 195, 285 + j * 40, ln, F_S, INK)
ctext(d, 90 + 2 * 415 + 195, 445, "→ 「…충분히 고려하지 못했습니다」", F_S, GRAY)
box(d, (90, 600, 1310, 700), SAND, "사전의 즉흥은 「그 자리의 감흥」이고, 제작진의 즉흥은 「목적지를 당일 정하는 것」이었다@@방송은 한 번에 많은 사람이 듣는다 — 심의 규정도 기준을 「시청자가 혼동했나」에 둔다(제14조)".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 표준국어대사전 「즉흥」, MBC 9.4 입장문(한겨레·더팩트 대조), 방송심의에 관한 규정 제14조(객관성)")
save(im, "N4_three_meanings.png")

# ============ N5 7월 22일 공문부터 10월 16일 보도까지 (세로 목록) ============
im, d = canvas("방송 석 주 전 공문부터 10월 보도까지, 날짜순으로",
               "확인된 날짜와 원문만 — 누가 옳은지가 아니라 무엇이 언제 나왔는지")
EV = (("7.22", "공항에 촬영 허가 공문", "8월 6일 카운터 발권 장면·오전 11시10분 편이 적혀 있었다", GRAY),
      ("8.6", "출국", "공문에 적힌 그 편으로", GRAY),
      ("8.14·21", "방송 두 편", "공항에서 목적지를 고르는 장면으로 시작", NAVY),
      ("8.25", "MBC 1차 입장", "「촬영 지원이나 협찬 등을 받은 사실은 없습니다」", ONS),
      ("8.31", "MBC 2차 입장", "금전 협찬은 없고, 행정 절차·촬영 협조는 받았다", ONS),
      ("9.4", "MBC 3차 입장", "앞의 「지원 없음」은 금전 지원만 뜻했다, 스태프 항공권은 미리", ONS),
      ("10.16", "공문 보도", "MBC 「촬영 허가를 받으려고 정리한 예시 상황」", RED))
for k, (dd, what, detail, col) in enumerate(EV):
    y = 160 + k * 60
    d.ellipse([100, y + 14, 124, y + 38], fill=col)
    if k < len(EV) - 1: d.line([112, y + 38, 112, y + 74], fill=(205, 205, 200), width=3)
    ltext(d, 140, y + 12, dd, F_M, col, right=270)
    ltext(d, 280, y + 12, what, F_M, INK, right=520)
    ltext(d, 530, y + 14, detail, F_S, INK, right=1310)
box(d, (90, 600, 1310, 700), SAND, "방송에서 「공항에서 고른」 목적지는, 방송 석 주 전 공문에 날짜·편명과 함께 적혀 있었다@@MBC는 그 공문을 「촬영 허가를 받으려고 정리한 예시」라고 설명했다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 한겨레·텐아시아·스포티비뉴스 10.16(인천국제공항공사가 국회에 낸 자료), MBC 입장문 8.25·8.31·9.4")
save(im, "N5_dates_in_order.png")

# ============ N6 방송은 「알릴 수 있다」, 유튜브는 「알려야 한다」 ============
im, d = canvas("방송은 「알릴 수 있다」, 유튜브는 「알려야 한다」",
               "도움을 받았을 때 알리는 규칙 — 방송법과 공정거래위원회 지침 원문")
cols = ((90, "방송 (방송법)", NAVY, ("받은 것에 드는 것", "돈·물품·용역·인력·장소"), ("알리는 규칙", "「할 수 있다」 — 정해진 방식만"), ("알리는 자리", "프로그램 끝 자막 1회")),
        (720, "유튜브 (공정위 지침)", ONS, ("받은 것에 드는 것", "현금·제품·상품권·포인트·할인"), ("알리는 규칙", "「공개하여야 한다」 — 매 건마다"), ("알리는 자리", "제목이나 영상 안, 시작과 끝")))
for x, head, col, *items in cols:
    d.rounded_rectangle([x, 170, x + 590, 540], radius=18, fill=WHITE, outline=col, width=4)
    d.rounded_rectangle([x, 170, x + 590, 228], radius=18, fill=col); d.rectangle([x, 208, x + 590, 228], fill=col)
    ctext(d, x + 295, 180, head, F_M, WHITE)
    for k, (lab, val) in enumerate(items):
        y = 250 + k * 96
        ltext(d, x + 30, y, lab, F_S, GRAY, right=x + 570)
        ltext(d, x + 30, y + 32, val, F_M, INK, right=x + 570)
box(d, (90, 600, 1310, 700), SAND, "방송법은 돈뿐 아니라 인력·장소를 받는 것도 협찬으로 본다. MBC는 「금전 협찬 없이 촬영 협조만」이라고 했다@@촬영 협조가 여기에 해당하는지는 방송 심의 기관이 아직 결론을 내지 않았다(10월 17일 기준)".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 방송법 제2조제22호·제74조, 협찬고지 규칙 제8조, 공정위 추천·보증 심사지침(2026.6.1 시행) — 국가법령정보센터 등 원문")
save(im, "N6_tell_rules.png")

# ============ N7 할 일 하나 — 메모에 「그날 정하기」 한 줄 ============
im, d = canvas("할 일 하나 — 다음 여행 메모에 「그날 정하기」 한 줄 남겨 두기",
               "내 여행 글 네 편에 비슷한 문장이 있었다 — 본문 그대로")
note_sheet(d, 110, 170, 420, 380, 6, "다음 여행 메모", filled=[(0, "비행기", PRE), (1, "숙소", PRE), (2, "렌터카", PRE)])
d.rectangle([126, 170 + 64 + 3 * 46 - 6, 514, 170 + 64 + 3 * 46 + 36], fill=WHITE)
d.rounded_rectangle([128, 170 + 64 + 3 * 46 - 4, 512, 170 + 64 + 3 * 46 + 34], radius=8, outline=ONS, width=3)
ltext(d, 140, 170 + 64 + 3 * 46, "그날 정하기", F_S, ONS, right=500)
Q4 = (("구마모토", "「계획에 없던 30분이 제일 선명해」"), ("규슈 일주", "「전부 계획에 없던 거야」"), ("후쿠오카 11월", "「일정표에 아무것도 안 적혀 있던 시간」"), ("미서부", "「제일 좋았던 곳들은 일정표에 없더라고」"))
for k, (where, what) in enumerate(Q4):
    y = 190 + k * 86
    d.rounded_rectangle([600, y, 1300, y + 70], radius=14, fill=WHITE, outline=(215, 212, 205), width=2)
    ltext(d, 625, y + 20, where, F_M, ONS, right=800)
    ltext(d, 800, y + 22, what, F_S, INK, right=1285)
box(d, (90, 600, 1310, 700), SAND, "네 문장 모두 비행기와 숙소를 미리 잡아 둔 여행에서 나왔다@@그래서 다음 여행 메모엔 다 채우지 않고, 「그날 정하기」 한 줄을 남겨 두기로 했다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 블로그 구마모토성·규슈 렌터카·후쿠오카 11월 코스·미서부 2년 뒤 글 본문(2026.10.17 확인). 메모는 모식")
save(im, "N7_one_blank_line.png")

# ============ H1 종류별 ============
im, d = canvas("종류별로 보면 — 항공·숙소는 전부 미리, 식당은 셋 중 하나만",
               "미리 : 현장 개수, 「알 수 없음」은 뺐다 — 직접 셈")
T = (("항공", 6, 0), ("숙소", 17, 0), ("렌터카", 10, 1), ("투어·입장권", 15, 1), ("동선", 17, 18), ("현지 교통", 3, 6), ("식당", 6, 13))
for k, (lab, a, b) in enumerate(T):
    y = 170 + k * 58
    ltext(d, 90, y + 6, lab, F_M, INK, right=300)
    w = (a + b) * 19
    split_bar(d, 310, y, w, 42, a, b, labels=False)
    ltext(d, 310 + w + 16, y + 6, f"{a} : {b}", F_S, GRAY)
    ctext(d, 1240, y + 2, f"{round(a / (a + b) * 100)}%", F_MID, PRE)
box(d, (90, 600, 1310, 700), SAND, "비행기·숙소는 미리 안 잡은 적이 한 번도 없었다. 식당은 거꾸로, 셋 중 둘을 현장에서 골랐다@@현장이 더 많았던 여행 넷 가운데 둘은, 미리 짠 첫날 계획이 틀어진 뒤였다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 여행 후기 68편 결정 항목 159가지 중 시점이 적힌 123가지(2026.10.17 직접 셈). 기타 10가지는 표에서 뺐다")
save(im, "H1_by_kind.png")

# ============ H2 옛 신문 속 「즉흥여행」 ============
im, d = canvas("1920~1999년 신문에 「즉흥여행」은 세 번 나왔다",
               "네이버 뉴스 라이브러리(조선·동아·경향·매일경제·한겨레) — 그 말이 들어간 기사 수, 10년 단위")
DEC = ("1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s")
MU = (79, 38, 2, 26, 254, 63, 61, 109); BP = (0, 0, 0, 0, 0, 0, 4, 2162); JH = (0, 0, 0, 0, 0, 0, 1, 2)
BASEY = 510; SCm = 260 / 260
for k, dec in enumerate(DEC):
    cx = 160 + k * 150
    h = MU[k] * SCm
    d.rounded_rectangle([cx - 44, BASEY - h, cx - 4, BASEY], radius=6, fill=(150, 150, 155))
    hb = min(BP[k] * SCm, 300)
    if BP[k]: d.rounded_rectangle([cx + 4, BASEY - hb, cx + 44, BASEY], radius=6, fill=NAVY)
    if BP[k] > 300: ctext(d, cx + 24, BASEY - hb - 34, "2,162", F_S, NAVY)
    ctext(d, cx, BASEY + 10, dec, F_S, INK)
    ctext(d, cx, BASEY + 44, str(JH[k]), F_M, RED if JH[k] else (200, 200, 196))
d.line([90, BASEY, 1310, BASEY], fill=INK, width=2)
d.rounded_rectangle([110, 175, 134, 195], radius=4, fill=(150, 150, 155)); ltext(d, 142, 172, "무전여행 632", F_S, INK)
d.rounded_rectangle([110, 207, 134, 227], radius=4, fill=NAVY); ltext(d, 142, 204, "배낭여행 2,166", F_S, INK)
ltext(d, 110, 236, "즉흥여행 3 — 축 아래 빨간 숫자", F_S, RED, right=600)
box(d, (90, 600, 1310, 700), SAND, "「즉흥여행」이 처음 나온 건 1989년 1월, 설 연휴에 즉흥으로 나섰다가 길에 갇혀 후회하는 글이었다@@1960년대 무전여행 기사 중 1963년 몫은 대부분 영화 「후라이보이 무전여행」 광고다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 네이버 뉴스 라이브러리 검색 결과 기사 수(따옴표 구절 검색, 2026.10.17). 「유행 건수」가 아니라 그 말이 나온 횟수")
save(im, "H2_old_papers.png")

# ============ H3 카자흐스탄 운전 서류 ============
im, d = canvas("카자흐스탄에서 운전하려면 — 국제운전면허증만으로는 안 된다",
               "주카자흐스탄 한국대사관 안내(8월 20일·25일)와 외교부 해외안전여행")
steps = (("한국 국제운전면허증", "제네바 협약 방식", False), ("카자흐스탄", "비엔나 협약 가입국", None), ("필요한 것", "한국 면허 원본 +@@러시아어 공증 번역본", True))
for k, (a, b, ok) in enumerate(steps):
    x = 90 + k * 420
    col = NAVY if ok is None else (GREEN if ok else RED)
    d.rounded_rectangle([x, 200, x + 380, 470], radius=18, fill=WHITE, outline=col, width=4)
    ctext(d, x + 190, 240, a, F_M, col)
    for j, ln in enumerate(b.split("@@")):
        ctext(d, x + 190, 300 + j * 34, ln, F_S, INK)
    if ok is True: check(d, x + 190, 400, 30, GREEN)
    if ok is False: xmark(d, x + 190, 400, 30, RED)
    if k < 2: arrow(d, (x + 384, 335), (x + 416, 335), GRAY, 4)
box(d, (90, 600, 1310, 700), SAND, "한국이 따르는 협약과 카자흐스탄이 따르는 협약이 달라서, 한국 국제운전면허증은 인정되지 않는다@@번역 공증은 현지 공증사무소나 한국 공관에서 받는다(공관은 약 반나절)".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 주카자흐스탄 대한민국 대사관 공지(8.20·8.25), 외교부 해외안전여행 운전면허 상호인정, 유엔 조약 현황")
save(im, "H3_driving_papers.png")

# ============ H4 시청률 ============
im, d = canvas("그동안의 시청률 — 숫자만 적는다",
               "닐슨코리아 전국 가구 시청률, 매주 금요일 방송")
RT = (("8.14", 5.8), ("8.21", 6.5), ("8.28", 5.1), ("9.4", 5.2), ("9.11", 4.8), ("9.18", 4.2), ("9.25", 3.5), ("10.2", 6.0), ("10.9", 5.0))
XA, XB, YT, YB = 140, 1260, 200, 500
def rx(i): return XA + i * (XB - XA) / (len(RT) - 1)
def ry(v): return YB - (v - 3.0) / (7.0 - 3.0) * (YB - YT)
for v in (3, 4, 5, 6, 7):
    d.line([XA - 20, ry(v), XB + 20, ry(v)], fill=(232, 230, 222), width=2); ltext(d, 70, ry(v) - 12, f"{v}%", F_S, GRAY)
pts = [(rx(i), ry(v)) for i, (_, v) in enumerate(RT)]
d.line(pts, fill=NAVY, width=5)
for i, (dd, v) in enumerate(RT):
    x, y = pts[i]
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=NAVY)
    ctext(d, x, y - 42, f"{v}", F_S, INK)
    ctext(d, x, YB + 14, dd, F_S, GRAY)
ltext(d, rx(6) + 22, ry(3.5) - 6, "추석 기간", F_S, AMBER)
box(d, (90, 600, 1310, 700), SAND, "알마티 2편(8.21) 6.5% 뒤 9월 25일 3.5%까지 내려갔다가, 10월 2일 6.0%로 올랐다@@추석 연휴·편성 같은 다른 이유도 겹쳐 있어, 이 숫자만으로 논란의 영향을 말할 수는 없다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 닐슨코리아(각 회차 보도), 10.16 방송분은 10.17 기준 확인 못 함")
save(im, "H4_ratings.png")

# ============ N5b 미리 한 것과 안 한 것 — 입장문이 둘 다 말했다 ============
im, d = canvas("미리 한 것과 안 한 것, 입장문이 둘 다 말했다",
               "MBC 입장문(8.25·8.31·9.4)과 공항 촬영 허가 공문(7.22)에서 확인된 것만")
L = (("공항 촬영 허가 공문", "7월 22일, 카자흐스탄 한 곳만"), ("스태프 항공권", "「미리 발권」(9.4)"), ("현지 촬영 협조", "「요청해 두었다」(9.4)"))
d.rounded_rectangle([90, 170, 690, 540], radius=18, fill=WHITE, outline=NAVY, width=4)
d.rounded_rectangle([90, 170, 690, 228], radius=18, fill=NAVY); d.rectangle([90, 208, 690, 228], fill=NAVY)
ctext(d, 390, 180, "미리 한 것", F_M, WHITE)
for k, (a, b) in enumerate(L):
    y = 250 + k * 78
    check(d, 130, y + 22, 16, NAVY)
    ltext(d, 160, y + 4, a, F_M, INK, right=680); ltext(d, 160, y + 38, b, F_S, GRAY, right=680)
ctext(d, 390, 490, "→ 「즉흥」이라는 소개와 어긋남", F_M, NAVY)
d.rounded_rectangle([710, 170, 1310, 540], radius=18, fill=WHITE, outline=RED, width=4)
d.rounded_rectangle([710, 170, 1310, 228], radius=18, fill=RED); d.rectangle([710, 208, 1310, 228], fill=RED)
ctext(d, 1010, 180, "미리 안 한 것", F_M, WHITE)
xmark(d, 750, 272, 16, RED)
ltext(d, 780, 254, "현지 운전 서류(면허 공증)", F_M, INK, right=1300)
ltext(d, 780, 288, "「뒤늦게 확인했다」(8.25)", F_S, GRAY, right=1300)
ltext(d, 750, 350, "한국 국제운전면허증은 현지에서", F_S, INK, right=1300)
ltext(d, 750, 384, "인정되지 않는다(대사관 안내)", F_S, INK, right=1300)
ctext(d, 1010, 490, "→ 여러 명이 움직이는 촬영에서 위험", F_M, RED)
box(d, (90, 600, 1310, 700), SAND, "준비했다면 즉흥이 아니고, 준비하지 않았다면 위험했다 — 비판이 양쪽에서 나온 이유다@@어느 쪽을 더 무겁게 볼지는 읽는 사람의 몫이다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: MBC 입장문 8.25·9.4, 인천국제공항공사가 국회에 낸 자료(10.16 보도), 주카자흐스탄 대사관 공지(8.20·8.25)")
save(im, "N5b_prepared_or_not.png")

# ============ N5c 검색이 다시 뜬 날 = 새 사실이 나온 날 ============
import json, datetime as _dt
_raw = json.load(open(os.path.join(HERE, "base data", "_raw_데이터랩_카자흐스탄_2026-10-17.json"), encoding="utf-8"))
_dd = {r["period"]: r["ratio"] for r in _raw["results"][0]["data"]}
D0, D1 = _dt.date(2026, 8, 10), _dt.date(2026, 10, 16)
days = [D0 + _dt.timedelta(i) for i in range((D1 - D0).days + 1)]
vals = [_dd.get(x.isoformat(), 0) for x in days]
im, d = canvas("검색이 다시 뜬 날은, 새 사실이 나온 날이었다",
               "네이버 데이터랩 날짜별 검색 추이(8.10~10.16, 가장 높은 날 = 100) — 「전현무 카자흐스탄」 등 검색어 8개 묶음")
XA, XB, YT, YB = 110, 1290, 200, 500
def gx(x): return XA + (x - D0).days / (D1 - D0).days * (XB - XA)
def gy(v): return YB - v / 100 * (YB - YT)
for v in (0, 50, 100):
    d.line([XA, gy(v), XB, gy(v)], fill=(232, 230, 222), width=2); ltext(d, 60, gy(v) - 12, str(v), F_S, GRAY)
pts = [(gx(x), gy(v)) for x, v in zip(days, vals)]
d.line(pts, fill=NAVY, width=4)
EVs = ((_dt.date(2026, 8, 14), "1편 방송", 0), (_dt.date(2026, 8, 21), "2편·알마티 보도", 1), (_dt.date(2026, 8, 25), "1차 입장", 2),
       (_dt.date(2026, 8, 31), "2차 입장", 0), (_dt.date(2026, 9, 4), "3차 입장·사과", 1), (_dt.date(2026, 10, 16), "공문 보도", 0))
for day, lab, lv in EVs:
    x = gx(day); v = _dd.get(day.isoformat(), 0)
    d.line([x, gy(v), x, YB + 8 + lv * 30], fill=(215, 160, 60), width=2)
    d.ellipse([x - 7, gy(v) - 7, x + 7, gy(v) + 7], fill=ONS)
    w = d.textlength(lab, font=F_S)
    lx = min(max(x - w / 2 - (60 if lab.startswith("2편") else 0), 30), W - 30 - w)
    ltext(d, lx, YB + 12 + lv * 30, lab, F_S, ONS)
ltext(d, gx(_dt.date(2026, 8, 26)) + 10, gy(100) - 4, "8.26 최고", F_S, NAVY)
box(d, (90, 610, 1310, 700), SAND, "검색은 방송 날보다 입장문이 나온 날 더 크게 뛰었다(8.25~26 최고, 8.31·9.4 다시)@@새 사실이 앞의 해명을 고칠 때마다 다시 화제가 됐다 — 10월 16일 공문 보도 때도 다시 올랐다".replace("@@", "\n"), F_S, INK)
footc(d, "근거: 네이버 데이터랩 검색어트렌드(NAVER API HUB, 2026.10.17 조회). 검색량이 아니라 상대 추이")
save(im, "N5c_search_peaks.png")

print("넘침 경고 없음" if not WARN else "\n".join(WARN))
