# -*- coding: utf-8 -*-
"""학군 구분 글 카드 v2(10/18 「이미지 직관성」 요청) — 그림이 먼저, 글자는 최소.
아이콘은 Windows Segoe UI Emoji(컬러)를 그린다. 숫자는 v1(make_cards_v1.py)과 같은 원문 값:
- [지표] 학군_공식지표_데이터.md (학교알리미 공개용 데이터 합산·NEIS 학원·KOSIS, 2026-10-17 조회, OpenAPI 136곳 교차 일치)
- [정책] 학군_정책연구_논란.md · [행정] 학군_기흥영통_행정사실.md · [영상] 유튜브_학군_종합.md(64편 최종)
학교명·동 이름·채널명은 그림에 쓰지 않는다(사용자 결정 10/17 「영통권 기흥」). 마이너스는 hyphen-minus."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "구구절절_컨텐츠", "261011_병역특례 논란"))
_cwd = os.getcwd()
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_S, F_B, INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
os.chdir(_cwd)
F_XS = font(17); F_SM = font(20); F_SMB = font(20, True); F_M = font(26, True); F_L = font(32, True); F_BIG = font(52, True)
NAVY = (40, 60, 110); DIM = (210, 210, 205); LINE = (225, 225, 218)
GU = ["영통", "기흥", "수지", "분당"]
COL = {"영통": RED, "기흥": BLUE, "수지": GREEN, "분당": AMBER}
EMO = r"C:\Windows\Fonts\seguiemj.ttf"
_ecache = {}


def emoji(im, ch, cx, cy, size):
    """컬러 이모지를 (cx, cy) 가운데에 size 높이로 붙인다."""
    key = (ch, size)
    if key not in _ecache:
        f = ImageFont.truetype(EMO, 109)
        tile = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((30, 30), ch, font=f, embedded_color=True)
        bb = tile.getbbox(); tile = tile.crop(bb)
        r = size / max(tile.size); _ecache[key] = tile.resize((max(1, int(tile.width * r)), max(1, int(tile.height * r))), Image.LANCZOS)
    t = _ecache[key]
    im.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)


def card(d, xy, fill=WHITE, r=22):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=LINE, width=2)


def save(im, n): im.save(os.path.join(HERE, n)); print("saved", n)


# 2 — 주소 하나, 배정은 세 갈래
def card_names(n):
    im, d = canvas("「학군」은 평판이고, 학교는 주소가 정한다", "주소를 넣으면 나오는 세 가지 — 학구도(초등 통학구역 · 중학교 학교군 · 고교 학교군)")
    card(d, (60, 180, 330, 560), SAND)
    emoji(im, "🏠", 195, 300, 150); ctext(d, 195, 400, "우리 집 주소", F_L, INK)
    ctext(d, 195, 455, "학구도 안내 서비스에", F_XS, GRAY); ctext(d, 195, 480, "넣으면 나온다", F_XS, GRAY)
    rows = [("초등학교", "정해진 한 곳", ["🏫"], None), ("중학교", "몇 곳 중 추첨", ["🏫", "🏫", "🏫"], "🎲"),
            ("고등학교", "지망 쓰고 추첨", ["🏫", "🏫", "🏫"], "📝")]
    for i, (a, b, schools, tool) in enumerate(rows):
        y = 175 + i * 135
        arrow(d, (335, 370), (395, y + 58), GRAY, 4)
        card(d, (400, y, 1340, y + 118))
        d.text((430, y + 40), a, font=F_L, fill=NAVY)
        for k, s in enumerate(schools):
            emoji(im, s, 680 + k * 85, y + 59, 78)
        if tool: emoji(im, tool, 680 + 3 * 85 + 10, y + 59, 70)
        d.text((1030, y + 42), b, font=F_M, fill=INK)
    card(d, (60, 600, 1340, 700), PINK)
    emoji(im, "💬", 120, 650, 60)
    d.text((170, 628), "「거기 학군 좋대」 — 평판이다. 학교 배정을 정한 시행령에는 「학군」이라는 단위가 없다", font=F_SMB, fill=RED)
    foot(d, "학구도안내서비스(한국교육시설안전원) · 초·중등교육법 시행령 16조(통학구역)·68조(학교군·중학구)·84조(고교 학교군)")
    save(im, n)


# 3 — 잴 수 있는 것 / 없는 것
def card_measure(n):
    im, d = canvas("사람들이 말하는 「좋은 학군」, 숫자로 잴 수 있는 건 절반", "유튜브 학군 영상 64편이 기준으로 쓴 것 (괄호는 그 기준을 쓴 영상 수)")
    yes = [("📚", "학원 개수", 46), ("🗺", "배정 구역", 30), ("💰", "집값", 28), ("🚶", "통학 거리", 25), ("🔄", "전입·전출", 20), ("🎓", "특목·자사고 진학", 19)]
    no = [("🏷", "이름값·평판", 47), ("🤫", "면학 분위기", 30), ("🧒", "아이 성향", 21), ("🏛", "명문대 합격", 19), ("📝", "학교 성적", 14)]
    card(d, (60, 160, 690, 690), MINT); card(d, (710, 160, 1340, 690), PINK)
    emoji(im, "📏", 110, 205, 54); d.text((150, 186), "공식 숫자로 잴 수 있다", font=F_M, fill=GREEN)
    emoji(im, "❓", 760, 205, 54); d.text((800, 186), "공식 숫자가 없다", font=F_M, fill=RED)
    for i, (e, t, v) in enumerate(yes):
        x = 90 + (i % 2) * 300; y = 260 + (i // 2) * 140
        card(d, (x, y, x + 280, y + 120))
        emoji(im, e, x + 60, y + 60, 64); d.text((x + 105, y + 30), t, font=F_SMB, fill=INK); d.text((x + 105, y + 66), f"({v}편)", font=F_XS, fill=GRAY)
    for i, (e, t, v) in enumerate(no):
        x = 740 + (i % 2) * 300; y = 260 + (i // 2) * 140
        card(d, (x, y, x + 280, y + 120))
        emoji(im, e, x + 60, y + 60, 64); d.text((x + 105, y + 30), t, font=F_SMB, fill=INK); d.text((x + 105, y + 66), f"({v}편)", font=F_XS, fill=GRAY)
    x, y = 1040, 540; card(d, (x, y, x + 280, y + 120), SAND)
    emoji(im, "⚠", x + 55, y + 60, 56); d.text((x + 100, y + 30), "학교폭력", font=F_SMB, fill=INK); d.text((x + 100, y + 66), "학교별로만 공시", font=F_XS, fill=GRAY)
    foot(d, "영상 64편 분석(2026.10.17) · 잴 수 있는지는 학교알리미·NEIS·교육청 고시로 확인 · 학원은 개수만 잰다(질은 못 잰다)")
    save(im, n)


# 4 — 학교 성적표가 사라진 길
def card_timeline(n):
    im, d = canvas("「학교별 성적 순위」는 왜 공식으로 없을까", "학교별 국가 학업성취도 공개의 흐름")
    ev = [("2010", "📋", "학교별 성적\n공시 시작"), ("2017", "✂", "평가가 3% 표집으로\n학교 공시에서 빠짐"),
          ("법", "📕", "공개할 땐\n학교 이름을 뺀다"), ("2025", "⚖", "대법원: 이름 가린\n익명 공개만 가능"), ("2026.10.29", "🔒", "기초학력 진단 결과\n외부 공개 금지")]
    d.line([140, 420, 1260, 420], fill=GRAY, width=5)
    for i, (yr, e, t) in enumerate(ev):
        x = 160 + i * 270
        card(d, (x - 120, 170, x + 120, 380), WHITE if i else LIGHT)
        emoji(im, e, x, 250, 100)
        ctext(d, x, 330, yr, F_M, NAVY)
        d.ellipse([x - 13, 407, x + 13, 433], fill=NAVY if i else GREEN)
        for k, ln in enumerate(t.split("\n")): ctext(d, x, 455 + k * 30, ln, F_SM, INK)
    card(d, (60, 580, 1340, 690), SAND)
    emoji(im, "🔍", 115, 635, 56)
    d.text((165, 596), "지금 도는 「학교별 학업성취도 순위」는 2016년 이전 자료이거나 학교 내신 분포다.", font=F_SMB, fill=INK)
    d.text((165, 640), "내신 분포(A~E)는 학교마다 기준 점수가 달라서 다른 학교와 비교할 수 없다.", font=F_SM, fill=INK)
    foot(d, "교육부 발표(2017.6.14) · 정보공개 특례법 5조② · 대법원 2023추5054(2025.5.15) · 기초학력 보장법 7조 · 경기도교육청 학업성적관리 지침")
    save(im, n)


# 5 — 동네의 통지표
def card_report(n):
    rows = [("🔄", "아이들이 들어오나", "초등 순유입률 2025", ["+1.11%", "-1.95%", "+1.57%", "+1.77%"], 3),
            ("🧒", "아이가 덜 줄었나", "초등 학생 수 2021→2026", ["-13.9%", "-30.4%", "-15.6%", "-17.6%"], 0),
            ("🎓", "특목·자사고 진학", "중학교 졸업생 2025", ["4.88%", "4.54%", "7.55%", "6.11%"], 2),
            ("📚", "학원 수", "6~17세 1천 명당", ["34.4", "28.4", "29.0", "41.3"], 3),
            ("🏫", "대학 진학률", "일반고 졸업생 2025", ["69.5%", "72.7%", "66.9%", "63.1%"], 1),
            ("👥", "과밀", "학급 28명↑ 중학교", ["72.2%", "71.2%", "82.0%", "97.7%"], None)]
    im, d = canvas("동네의 통지표 — 과목 여섯 개, 1등은 네 곳", "가장 높은 곳에 금메달 · 과밀은 「인기」로도 「자리 부족」으로도 읽혀서 메달 없음")
    d.rounded_rectangle([58, 152, 1346, 712], radius=10, fill=(236, 233, 224))
    d.rounded_rectangle([50, 144, 1338, 704], radius=10, fill=WHITE, outline=(200, 195, 180), width=2)
    for j, g in enumerate(GU):
        cx = 760 + j * 150
        ctext(d, cx, 160, g, F_L, COL[g])
    d.line([70, 205, 1320, 205], fill=(200, 195, 180), width=2)
    for i, (e, a, b, vals, star) in enumerate(rows):
        y = 214 + i * 80
        if i % 2: d.rectangle([52, y, 1336, y + 80], fill=(248, 247, 242))
        emoji(im, e, 105, y + 40, 52)
        d.text((150, y + 12), a, font=F_SMB, fill=INK); d.text((150, y + 44), b, font=F_XS, fill=GRAY)
        for j, v in enumerate(vals):
            cx = 760 + j * 150
            ctext(d, cx, y + 24, v, F_M if star == j else F_SMB, COL[GU[j]] if star == j else GRAY)
            if star == j: emoji(im, "🥇", cx + 66, y + 38, 44)
    foot(d, "학교알리미 공개용 데이터 합산(학교 위치 기준) · NEIS 학원·교습소 + KOSIS 주민등록 6~17세 · 2026.10.17 조회 · 진학률은 일반고만")
    save(im, n)


# 6 — 졸업생 100명
def card_gita(n):
    vals = [("기흥", 72.74, 25.0), ("영통", 69.53, 29.14), ("수지", 66.89, 28.34), ("분당", 63.12, 36.44)]
    im, d = canvas("학원이 가장 많은 동네, 대학 진학률은 가장 낮았다", "일반고 졸업생 100명이 3월에 간 곳 (2025년 2월 졸업, 점 하나 = 1명)")
    for i, (g, a, b) in enumerate(vals):
        x0 = 70 + i * 330; y0 = 200
        ctext(d, x0 + 140, 152, g, F_L, COL[g])
        na = round(a); nb = round(b)
        for k in range(100):
            r, c = divmod(k, 10)
            cx = x0 + 20 + c * 26; cy = y0 + 20 + r * 26
            col = NAVY if k < na else (AMBER if k < na + nb else DIM)
            d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=col)
        d.text((x0 + 10, y0 + 280), f"대학 {a:.1f}%", font=F_SMB, fill=NAVY)
        d.text((x0 + 150, y0 + 280), f"기타 {b:.1f}%", font=F_SMB, fill=AMBER)
    card(d, (60, 540, 1340, 690), SAND)
    emoji(im, "📖", 125, 615, 70)
    d.text((185, 565), "「기타」 = 대학도 취업도 아닌 경우. 재수생이 여기에 들어간다.", font=F_M, fill=INK)
    d.text((185, 615), "재수생만 따로 센 숫자는 없다. 그래서 진학률을 「학군 순위」로 읽으면 거꾸로 된다.", font=F_SM, fill=INK)
    d.ellipse([1110, 552, 1128, 570], fill=NAVY); d.text((1135, 548), "대학", font=F_XS, fill=GRAY)
    d.ellipse([1190, 552, 1208, 570], fill=AMBER); d.text((1215, 548), "기타", font=F_XS, fill=GRAY)
    d.ellipse([1270, 552, 1288, 570], fill=DIM); d.text((1293, 548), "취업 등", font=F_XS, fill=GRAY)
    foot(d, "학교알리미 졸업생 진로 현황(일반고만, 학교 위치 기준) 합산 · 점은 반올림 · 2026.10.17 조회")
    save(im, n)


# 7 — 경계 지도: 생활은 영통, 학교는 용인
def card_address(n):
    im, d = canvas("생활은 영통이어도, 주소가 기흥이면 학교는 용인", "영통에 맞닿은 기흥 동네에서 본 초·중·고 — 교육청 고시·배정 방안 원문")
    d.rectangle([60, 150, 640, 700], fill=(253, 236, 236)); d.rectangle([640, 150, 1340, 700], fill=(232, 238, 252))
    pts = [(640, 150), (660, 230), (625, 320), (655, 420), (630, 520), (650, 610), (640, 700)]
    d.line(pts, fill=GRAY, width=6)
    d.text((90, 165), "수원 영통", font=F_L, fill=RED); d.text((1150, 165), "용인 기흥", font=F_L, fill=BLUE)
    emoji(im, "🛒", 470, 300, 60); emoji(im, "🚇", 560, 300, 60)
    ctext(d, 515, 340, "장 보고 지하철 타는 곳", F_XS, GRAY)
    emoji(im, "🏠", 760, 420, 110); ctext(d, 760, 485, "우리 집 (주소: 기흥)", F_SMB, INK)
    d.line([700, 380, 590, 330], fill=(170, 170, 170), width=3)
    for k, (lab, y) in enumerate([("초등", 235), ("중학", 390), ("고교", 535)]):
        emoji(im, "🏫", 300, y, 70); ctext(d, 300, y + 40, "수원 " + lab, F_XS, GRAY)
        emoji(im, "🏫", 1120, y, 70); ctext(d, 1120, y + 40, "용인 " + lab, F_SMB, BLUE)
        arrow(d, (830, 420 + (y - 400) * 0.25), (1070, y), BLUE, 5)
        d.line([690, 430 + (y - 400) * 0.2, 360, y], fill=(200, 160, 160), width=3)
    emoji(im, "🚫", 500, 450, 70)
    card(d, (900, 630, 1330, 692), WHITE)
    d.text((920, 646), "고교 자리 부족 → 수지 구역 선택 가능", font=F_SMB, fill=NAVY)
    card(d, (80, 630, 590, 692), WHITE)
    d.text((100, 646), "공동학구 0 · 수원 일반고 지원 불가", font=F_SMB, fill=RED)
    foot(d, "중학교 학교군 고시 2025~2027학년도 · 2027 고입 기본계획(평준화지역 중졸자는 그 지역에 지원) · 2027 배정 방안(출신구역 변경)")
    save(im, n)


# 8 — 두 시의 중학교 배정
def card_lottery(n):
    im, d = canvas("같은 「추첨」이 아니다 — 수원과 용인의 중학교 배정", "2027학년도 중학교 배정업무 시행계획(수원·용인 교육지원청)")
    card(d, (60, 150, 690, 700), (253, 240, 240)); card(d, (710, 150, 1340, 700), (236, 241, 252))
    ctext(d, 375, 168, "수원", F_L, RED); ctext(d, 1025, 168, "용인", F_L, BLUE)
    a = [("📝", "학교군 안 여러 곳에 지원"), ("💻", "컴퓨터 추첨"), ("🏫", "배정")]
    b = [("📝", "희망 순으로 지원"), ("📅", "1지망이 넘치면\n초등 먼저 입학한 순"), ("🎲", "입학일이 같을 때만 추첨")]
    for col, items, x in ((RED, a, 375), (BLUE, b, 1025)):
        for k, (e, t) in enumerate(items):
            y = 260 + k * 150
            emoji(im, e, x - 200, y + 20, 80)
            for m, ln in enumerate(t.split("\n")): d.text((x - 130, y - 5 + m * 32), ln, font=F_M if k == 1 and col == BLUE else F_SMB, fill=INK)
            if k < 2: arrow(d, (x - 200, y + 70), (x - 200, y + 110), GRAY, 4)
    d.text((80, 655), "발표는 두 곳 모두 2026.12.31", font=F_XS, fill=GRAY)
    d.text((730, 655), "「먼저 입학」을 전학생에게 어떻게 세는지는 원문에 없다", font=F_XS, fill=GRAY)
    foot(d, "수원교육지원청·용인교육지원청 2027학년도 중학교 신입생 배정업무 시행계획")
    save(im, n)


# 9 — 집값 연구: 배경을 지울수록 학교 몫이 작아진다
def card_research(n):
    vals = [(["🏙", "👪", "🏫"], "아무것도 안 뺐을 때", 2.3, DIM), (["👪", "🏫"], "학군 경계 양쪽끼리만", 1.3, (170, 180, 205)),
            (["🏫"], "주민 구성까지 뺐을 때", 0.5, NAVY)]
    im, d = canvas("학군과 집값 — 배경을 지울수록 학교 몫은 작아졌다", "중학교 수학 「보통학력 이상」 1%p 차이에 붙은 ㎡당 집값 차이 (서울 강남3구+인접 5구, 2006~2016 실거래)")
    for i, (icons, lab, v, c) in enumerate(vals):
        x = 140 + i * 400
        card(d, (x, 150, x + 340, 235), WHITE)
        for k, e in enumerate(icons):
            emoji(im, e, x + 170 + (k - (len(icons) - 1) / 2) * 90, 192, 62)
        h = v * 100
        d.rectangle([x + 70, 560 - h, x + 270, 560], fill=c)
        ctext(d, x + 170, 560 - h - 62, f"{v}%", F_BIG, NAVY if i == 2 else GRAY)
        ctext(d, x + 170, 572, lab, F_SMB, INK)
        if i < 2: arrow(d, (x + 345, 192), (x + 395, 192), GRAY, 4)
    d.line([120, 560, 1280, 560], fill=GRAY, width=2)
    card(d, (60, 615, 1340, 700), SAND)
    d.text((85, 628), "효과가 없다는 연구도 있다 — 서울대 합격률 변화는 집값 상승률을 설명 못 했고, 서울 25개 구에서", font=F_SM, fill=INK)
    d.text((85, 660), "집값과 함께 움직인 건 초등 전입뿐이었다. 연구 대부분이 서울 자료다(수원·용인 단독 연구는 못 찾음).", font=F_SM, fill=INK)
    foot(d, "김성준(한국은행 연구자, 2017 ISI 학술대회 발표문) · 김경민·이양원(2007, 국토연구) · 김경민 외(2010, 국토연구)")
    save(im, n)


# 10 — 영상이 말한 것 vs 공식 문서
def card_claims(n):
    rows = [("「단지 옆 학교 = 우리 아이 학교」", "중학교는 학교군 안 추첨, 고교는 출신 중학교 구역 추첨", "과장"),
            ("「학교 성적도 공개된다」", "학교별 성적 공시는 2017년부터 없다", "틀림"),
            ("「내신 9등급 기준으로 보면」", "확정된 2028 대입은 내신 5등급", "틀림"),
            ("「학원·사교육이 줄어든다」", "경기 사설학원 2020→2025 +23.9%", "과장"),
            ("「학군이 집값을 크게 올린다」", "주민 구성까지 따지면 2.3% → 0.5%", "과장")]
    im, d = canvas("영상이 말한 것 vs 공식 문서가 말한 것", "학군 영상 64편에서 틀리거나 부풀린 주장이 몰린 다섯 곳")
    emoji(im, "📺", 290, 172, 52); d.text((330, 158), "영상", font=F_M, fill=RED); emoji(im, "📄", 990, 172, 52); d.text((1030, 158), "공식 문서", font=F_M, fill=GREEN)
    for i, (a, b, j) in enumerate(rows):
        y = 210 + i * 98
        card(d, (60, y, 610, y + 82), PINK); d.text((85, y + 26), a, font=F_SMB, fill=INK)
        st = RED if j == "틀림" else AMBER
        d.rounded_rectangle([622, y + 20, 708, y + 62], radius=20, fill=st); ctext(d, 665, y + 27, j, F_SMB, WHITE)
        arrow(d, (712, y + 41), (745, y + 41), GRAY, 4)
        card(d, (750, y, 1340, y + 82), MINT); d.text((775, y + 26), b, font=F_SMB, fill=INK)
    foot(d, "영상 64편 주장 828개 중 틀림 8·과장 27 · 근거: 교육청 고시·배정 방안, 교육부 발표, 2028 대입 개편안, KOSIS, 연구 문헌")
    save(im, n)


# 11 — 이사 전 체크리스트
def card_check(n):
    rows = [("🗺", "학구도 안내 서비스에 주소 넣기"), ("📜", "통학구역 일람표 — 번지·통·반까지"), ("🎲", "중학교 배정 — 추첨? 먼저 입학한 순?"),
            ("🏫", "고교 평준화 학군·출신 중학교 구역"), ("🔄", "학년별 학생 수, 전입·전출"), ("🎓", "중학교 졸업생 진로 — 세 해로"),
            ("📈", "고교 진학률은 「기타」와 같이"), ("📚", "학원 — 1천 명당 개수, 거리는 지도로"), ("❓", "숫자가 없는 것: 학교 성적·학교폭력 비교·분위기")]
    im, d = canvas("이사 전에 내가 볼 것 아홉 가지", "어느 동네가 학군 1등인지 대신 — 모두 공개 자료")
    emoji(im, "📦", 170, 430, 230)
    for i, (e, t) in enumerate(rows):
        x = 360 + (i % 2) * 495; y = 160 + (i // 2) * 105
        if i == 8: x = 360
        card(d, (x, y, x + 470 if i < 8 else x + 965, y + 88), WHITE if i < 8 else (244, 244, 240))
        emoji(im, e, x + 48, y + 44, 52)
        d.text((x + 90, y + 30), t, font=F_SMB, fill=INK if i < 8 else GRAY)
    foot(d, "학구도안내서비스(한국교육시설안전원) · 경기도교육청·교육지원청 고시·시행계획 · 학교알리미 · NEIS")
    save(im, n)


if __name__ == "__main__":
    for i, fn in enumerate([card_names, card_measure, card_timeline, card_report, card_gita, card_address, card_lottery,
                            card_research, card_claims, card_check], start=2):
        fn(f"261018_{i}.png")
