# -*- coding: utf-8 -*-
"""학군 구분 글 카드 v3 — 「칠판 학구도」 양식(마스터 5-8, 10/18 시안 승인) 10장 → 261018_2~11.png.
숫자는 v1·v2(make_cards_v1.py · make_cards.py)와 같은 원문 값:
- [지표] 학군_공식지표_데이터.md (학교알리미 공개용 데이터 합산·NEIS 학원·KOSIS, 2026-10-17 조회, OpenAPI 136곳 교차 일치)
- [정책] 학군_정책연구_논란.md · [행정] 학군_기흥영통_행정사실.md · [영상] 유튜브_학군_종합.md(64편 최종)
학교명·동 이름·채널명 금지(0-10, 사용자 결정 10/17 「영통권 기흥」). 마이너스는 hyphen-minus."""
import os, math
from PIL import Image, ImageDraw
from hakgudo_cards_base import *
HERE = os.path.dirname(os.path.abspath(__file__))
GU = ["영통", "기흥", "수지", "분당"]
GHOST = (110, 132, 122)


def out(im, n): im.save(os.path.join(HERE, n)); print("saved", n)


# ---- 분필 선 아이콘 몇 개
def paper(d, cx, cy, s, col=CHALK, w=4):
    d.rectangle([cx - s * .35, cy - s * .45, cx + s * .35, cy + s * .45], outline=col, width=w)
    for k in range(3): d.line([(cx - s * .22, cy - s * .2 + k * s * .18), (cx + s * .22, cy - s * .2 + k * s * .18)], fill=col, width=max(2, w - 1))


def monitor(d, cx, cy, s, col=CHALK, w=4):
    d.rectangle([cx - s * .5, cy - s * .38, cx + s * .5, cy + s * .22], outline=col, width=w)
    d.line([(cx, cy + s * .22), (cx, cy + s * .4)], fill=col, width=w); d.line([(cx - s * .25, cy + s * .4), (cx + s * .25, cy + s * .4)], fill=col, width=w)


def dice(d, cx, cy, s, col=CHALK, w=4):
    d.rounded_rectangle([cx - s * .4, cy - s * .4, cx + s * .4, cy + s * .4], radius=s * .1, outline=col, width=w)
    for dx, dy in ((-.2, -.2), (0, 0), (.2, .2)): d.ellipse([cx + dx * s - 6, cy + dy * s - 6, cx + dx * s + 6, cy + dy * s + 6], fill=col)


def calendar(d, cx, cy, s, col=CHALK, w=4):
    d.rectangle([cx - s * .45, cy - s * .38, cx + s * .45, cy + s * .42], outline=col, width=w)
    d.line([(cx - s * .45, cy - s * .18), (cx + s * .45, cy - s * .18)], fill=col, width=w)
    for i in range(3):
        for j in range(2): d.rectangle([cx - s * .3 + i * s * .22, cy - s * .04 + j * s * .2, cx - s * .2 + i * s * .22, cy + s * .06 + j * s * .2], fill=col)


def towers(d, cx, cy, s, col=CHALK, w=4):
    for dx, h in ((-.3, .7), (0, 1.0), (.3, .55)):
        d.rectangle([cx + dx * s - s * .12, cy + s * .45 - h * s * .9, cx + dx * s + s * .12, cy + s * .45], outline=col, width=w)


def people(d, cx, cy, s, col=CHALK, w=4):
    for dx, r in ((-.25, .12), (.25, .12), (0, .09)):
        hx, hy = cx + dx * s, cy - s * .15 + (s * .1 if r < .1 else 0)
        d.ellipse([hx - r * s, hy - r * s, hx + r * s, hy + r * s], outline=col, width=w)
        d.arc([hx - r * s * 1.8, hy + r * s * 1.2, hx + r * s * 1.8, hy + r * s * 5], 180, 360, fill=col, width=w)


def stamp(im, cx, cy, s, col, ang=-8):
    f = F(30, "Black"); tw = int(ImageDraw.Draw(im).textlength(s, font=f))
    t = Image.new("RGBA", (tw + 44, 64), (0, 0, 0, 0)); td = ImageDraw.Draw(t)
    td.rounded_rectangle([2, 2, tw + 42, 62], radius=10, outline=col, width=5); td.text(((tw + 44) / 2, 32), s, font=f, fill=col, anchor="mm")
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)


# 01 — 주소 하나, 배정은 세 갈래
def c_names(n):
    im, d = board()
    y = header(im, 1, "학구도란", "「학군」은 평판이고,\n학교는 주소가 정한다", "학구도 안내 서비스에 주소를 넣으면 나오는 세 가지")
    hx, hy = 165, y + 290
    chalk(im, lambda dd: house(dd, hx, hy, 150, CHALK, 7), 0.12)
    text(im, (hx, hy + 100), "우리 집 주소", 30, CHALK, anchor="ma")
    rows = [("초등학교", "통학구역 · 시행령 16조", 1, None, "정해진 한 곳"),
            ("중학교", "학교군·중학구 · 시행령 68조", 3, dice, "몇 곳 중 추첨"),
            ("고등학교", "고교 학교군 · 시행령 84조", 3, paper, "지망 쓰고 추첨")]
    for i, (a, law, ns, tool, how) in enumerate(rows):
        yy = y + 40 + i * 190
        chalk(im, lambda dd, yy=yy: arrow(dd, (hx + 95, hy - 20 + (yy + 60 - hy) * 0.25), (350, yy + 60), SKY, 6), 0.1)
        text(im, (370, yy), a, 40, CHALK)
        text(im, (370, yy + 54), law, 22, MUTE, "Medium", rough=0.03)
        for k in range(ns):
            chalk(im, lambda dd, k=k, yy=yy: school(dd, 410 + k * 105, yy + 150, 80, SKY, 5), 0.12)
        if tool: chalk(im, lambda dd, yy=yy, tool=tool: tool(dd, 410 + ns * 105 + 10, yy + 150, 70, BUTTER, 5), 0.12)
        text(im, (W - 70, yy + 135), how, 32, BUTTER if tool else CHALK, anchor="ra")
    by = y + 620
    chalk(im, lambda dd: (dd.rounded_rectangle([70, by, W - 70, by + 110], radius=40, outline=PINK, width=5),
                          dd.polygon([(150, by + 108), (138, by + 134), (190, by + 108)], fill=PINK)), 0.2)
    text(im, (110, by + 22), "「거기 학군 좋대」 = 평판", 32, PINK)
    text(im, (110, by + 68), "학교 배정을 정한 시행령에 「학군」이라는 단위는 없다", 22, CHALK2, "Medium", rough=0.03)
    conclusion(im, by + 150, "학교는 거리가 아니라 주소가 속한 구역이 정한다")
    source(im, "학구도안내서비스(한국교육시설안전원) 학구도 소개 · 초·중등교육법 시행령 16조·68조·84조")
    out(im, n)


# 02 — 잴 수 있는 것 / 없는 것
def c_measure(n):
    im, d = board()
    y = header(im, 2, "학군의 기준", "사람들이 말하는 기준,\n숫자로 잴 수 있는 건 절반", "학군 영상 64편이 쓴 기준 · 막대 = 그 기준을 쓴 영상 수")
    yes = [("학원 개수", 46), ("배정 구역", 30), ("집값", 28), ("통학 거리", 25), ("전입·전출", 20), ("특목·자사고 진학", 19)]
    no = [("이름값·평판", 47), ("면학 분위기", 30), ("아이 성향", 21), ("명문대 합격", 19), ("학교 성적", 14)]
    text(im, (70, y + 10), "공식 숫자로 잴 수 있다", 32, LIME)
    text(im, (560, y + 10), "공식 숫자가 없다", 32, PINK)
    dashed(d, (530, y + 10), (530, y + 700), GHOST, 3, 12, 10)
    for col, items, x0, c in ((LIME, yes, 70, LIME), (PINK, no, 560, PINK)):
        for i, (t, v) in enumerate(items):
            yy = y + 80 + i * 100
            text(im, (x0, yy), t, 28, CHALK)
            L = v * 8.5
            chalk(im, lambda dd, yy=yy, L=L, x0=x0, c=c: dd.rectangle([x0, yy + 48, x0 + L, yy + 74], fill=c), 0.3)
            text(im, (x0 + L + 12, yy + 44), f"{v}편", 24, c, "Bold", rough=0.04)
    yy = y + 600
    chalk(im, lambda dd: dd.polygon([(585, yy + 40), (565, yy + 74), (605, yy + 74)], outline=BUTTER, width=4), 0.1)
    text(im, (620, yy + 34), "학교폭력 8편 — 학교별로만 공시", 24, BUTTER, "Bold", rough=0.04)
    conclusion(im, y + 760, "영상 속 주장 828개 가운데 88%는 공식 자료로 확인할 수 없었다")
    source(im, "영상 64편 분석(2026.10.17) · 잴 수 있는지는 학교알리미·NEIS·교육청 고시로 확인 · 학원은 개수만 잰다(질은 못 잰다)")
    out(im, n)


# 03 — 학교별 성적표가 사라진 흐름
def c_timeline(n):
    im, d = board()
    y = header(im, 3, "학교 성적", "「학교별 성적 순위」는\n왜 공식으로 없을까", "학교별 국가 학업성취도 공개의 흐름 — 법령·판결·교육부 발표")
    ev = [("2010", "학교별 성적, 학교알리미 공시 시작", CHALK), ("2017", "평가가 3% 표집으로 → 학교 공시에서 빠짐", PINK),
          ("법 5조②", "교육감·교육부가 공개할 땐 학교 이름을 뺀다", CHALK), ("2025", "대법원 — 이름을 가린 익명 공개만 가능", CHALK),
          ("10.29", "2026년부터 기초학력 진단 결과 외부 공개 금지", PINK)]
    chalk(im, lambda dd: dd.line([(150, y + 30), (150, y + 545)], fill=CHALK2, width=6), 0.25)
    for i, (yr, t, c) in enumerate(ev):
        yy = y + 30 + i * 128
        chalk(im, lambda dd, yy=yy, c=c: dd.ellipse([136, yy - 14, 164, yy + 14], fill=c), 0.1)
        text(im, (200, yy - 30), yr, 44, SKY if c == CHALK else PINK)
        text(im, (200, yy + 26), t, 28, CHALK, "Bold", rough=0.05)
    by = y + 610
    text(im, (70, by), "지금 도는 「학교별 학업성취도 순위」는", 26, CHALK2, "Bold", rough=0.04)
    text(im, (70, by + 40), "2016년 이전 자료이거나, 학교 내신 분포다.", 26, CHALK2, "Bold", rough=0.04)
    text(im, (70, by + 80), "내신 분포(A~E)는 학교마다 기준 점수가 달라 서로 비교할 수 없다.", 22, MUTE, "Medium", rough=0.03)
    conclusion(im, by + 140, "학교끼리 성적을 비교할 공식 숫자는 없다", PINK)
    source(im, "교육부 발표(2017.6.14) · 정보공개 특례법 5조② · 대법원 2023추5054(2025.5.15) · 기초학력 보장법 7조 · 경기도교육청 지침")
    out(im, n)


# 04 — 통지표
def c_report(n):
    im, d = board()
    y = header(im, 4, "동네의 통지표", "과목 여섯 개,\n1등은 네 곳이었다", "영통·기흥·수지·분당을 공식 숫자로 재 보니")
    rows = [("아이들이 들어오나", "초등 순유입률(%) · 2025", ["+1.11", "-1.95", "+1.57", "+1.77"], 3),
            ("아이가 덜 줄었나", "초등 학생 수 변화(%) · 2021→2026", ["-13.9", "-30.4", "-15.6", "-17.6"], 0),
            ("특목·자사고 진학", "중학교 졸업생(%) · 2025", ["4.88", "4.54", "7.55", "6.11"], 2),
            ("학원 수", "6~17세 1천 명당(곳)", ["34.4", "28.4", "29.0", "41.3"], 3),
            ("대학 진학률", "일반고 졸업생(%) · 2025", ["69.5", "72.7", "66.9", "63.1"], 1),
            ("과밀 중학교", "학급 28명 넘는 학교 학생(%)", ["72.2", "71.2", "82.0", "97.7"], None)]
    x0 = 560
    for j, g in enumerate(GU):
        text(im, (x0 + j * 120 + 55, y + 6), g, 30, GU_COL[g], anchor="ma")
    y += 64
    d = ImageDraw.Draw(im)
    for i, (a, b, vals, star) in enumerate(rows):
        yy = y + i * 108
        dashed(d, (70, yy - 8), (W - 70, yy - 8), (70, 104, 92), 2, 10, 8)
        text(im, (70, yy + 14), a, 32, CHALK)
        text(im, (70, yy + 60), b, 22, MUTE, "Medium", rough=0.03)
        for j, v in enumerate(vals):
            cx = x0 + j * 120 + 55
            if star == j:
                chalk(im, lambda dd, cx=cx, yy=yy, j=j: dd.ellipse([cx - 56, yy + 6, cx + 56, yy + 90], outline=GU_COL[GU[j]], width=6), 0.25)
                text(im, (cx, yy + 48), v, 38, GU_COL[GU[j]], anchor="mm")
            else:
                text(im, (cx, yy + 48), v, 28, MUTE, "Bold", anchor="mm", rough=0.05)
    text(im, (W - 70, y + 6 * 108 - 4), "과밀은 「인기」로도 「자리 부족」으로도 읽혀 동그라미 없음", 20, MUTE, "Medium", anchor="ra", rough=0.02)
    conclusion(im, y + 6 * 108 + 40, "「학군 1등」은 무엇을 재느냐에 따라 바뀐다")
    source(im, "학교알리미 공개용 데이터 합산(학교 위치 기준) · NEIS 학원 + KOSIS 6~17세 · 2026.10.17 조회 · 진학률은 일반고만")
    out(im, n)


# 05 — 졸업생 100명
def c_grads(n):
    im, d = board()
    y = header(im, 5, "진학률의 함정", "학원이 가장 많은 동네,\n대학 진학률은 가장 낮았다", "일반고 졸업생 100명이 3월에 간 곳 · 2025년 2월 졸업")
    vals = [("기흥", 72.74, 25.0), ("영통", 69.53, 29.14), ("수지", 66.89, 28.34), ("분당", 63.12, 36.44)]
    for i, (g, a, b) in enumerate(vals):
        x0 = 70 + (i % 2) * 490; y0 = y + 10 + (i // 2) * 352
        text(im, (x0, y0), g, 40, GU_COL[g])
        text(im, (x0 + 120, y0 + 10), f"기타 {b:.1f}%", 30, BUTTER if g == "분당" else CHALK2, "Black" if g == "분당" else "Bold")
        na, nb = round(a), round(b)
        def dots(dd, x0=x0, y0=y0, na=na, nb=nb):
            for k in range(100):
                r, c = divmod(k, 10); cx = x0 + 18 + c * 40; cy = y0 + 90 + r * 24
                if k < na: dd.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=CHALK)
                elif k < na + nb: dd.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=BUTTER, width=4)
                else: dd.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=MUTE)
        chalk(im, dots, 0.15)
        text(im, (x0, y0 + 316), f"대학 {a:.1f}%", 24, CHALK2, "Bold", rough=0.04)
    yy = y + 728
    chalk(im, lambda dd: (dd.ellipse([74, yy + 6, 92, yy + 24], fill=CHALK), dd.ellipse([250, yy + 6, 268, yy + 24], outline=BUTTER, width=4)), 0.1)
    text(im, (102, yy), "대학 진학", 22, CHALK2, "Bold", rough=0.03); text(im, (278, yy), "기타(재수생이 여기에 들어간다)", 22, BUTTER, "Bold", rough=0.03)
    conclusion(im, yy + 56, "진학률을 「학군 순위」로 읽으면 거꾸로 된다", BUTTER)
    source(im, "학교알리미 졸업생 진로 현황(일반고만, 학교 위치 기준) 합산 · 점 1개 = 1명(반올림) · 재수생만 센 숫자는 공시에 없다")
    out(im, n)


# 06 — 경계 지도
def c_border(n):
    im, d = board()
    y = header(im, 6, "주소가 학교를 정한다", "생활은 영통이어도\n주소가 기흥이면 학교는 용인", "영통에 맞닿은 기흥 동네 · 교육청 고시·배정 방안 원문")
    d = ImageDraw.Draw(im)
    top, bot = y + 10, y + 690
    left = [(70, top), (520, top), (560, top + 150), (500, top + 300), (555, top + 470), (520, bot), (70, bot)]
    right = [(520, top), (W - 70, top), (W - 70, bot), (520, bot), (555, top + 470), (500, top + 300), (560, top + 150)]
    chalk(im, lambda dd: dd.polygon(left, fill=(64, 58, 66)), 0.3)
    chalk(im, lambda dd: dd.polygon(right, fill=(44, 72, 92)), 0.3)
    bl = [(520, top), (560, top + 150), (500, top + 300), (555, top + 470), (520, bot)]
    for a, b in zip(bl, bl[1:]): dashed(d, a, b, CHALK, 6, 18, 12)
    text(im, (95, top + 24), "수원 영통", 36, PINK); text(im, (W - 95, top + 24), "용인 기흥", 36, SKY, anchor="ra")
    text(im, (95, top + 74), "장 보고 지하철 타는 곳", 22, CHALK2, "Medium", rough=0.03)
    hx, hy = 640, top + 360
    chalk(im, lambda dd: house(dd, hx, hy, 110, CHALK, 6), 0.12)
    text(im, (hx, hy + 80), "우리 집", 28, CHALK, anchor="ma")
    for k, (lab, yy) in enumerate([("초등", top + 170), ("중학", top + 360), ("고교", top + 550)]):
        chalk(im, lambda dd, yy=yy: school(dd, 900, yy, 92, SKY, 5), 0.12)
        text(im, (900, yy + 52), "용인 " + lab, 26, SKY, anchor="ma")
        chalk(im, lambda dd, yy=yy: arrow(dd, (hx + 70, hy - 10 + (yy - hy) * 0.15), (840, yy), SKY, 6), 0.1)
        chalk(im, lambda dd, yy=yy: school(dd, 250, yy, 92, (150, 140, 150), 5), 0.2)
        text(im, (250, yy + 52), "수원 " + lab, 24, MUTE, "Bold", anchor="ma", rough=0.05)
        chalk(im, lambda dd, yy=yy: dashed(dd, (hx - 70, hy + (yy - hy) * 0.15), (310, yy), (150, 140, 150), 4, 12, 10), 0.1)
        chalk(im, lambda dd, yy=yy: xmark(dd, 410, hy + (yy - hy) * 0.55, 18, PINK, 7), 0.1)
    yy = bot + 34
    text(im, (70, yy), "공동학구 0곳 (2025~2027 고시)", 26, PINK, "Bold", rough=0.04)
    text(im, (70, yy + 40), "용인 중학교 졸업 → 수원 일반고 지원 불가", 26, PINK, "Bold", rough=0.04)
    text(im, (W - 70, yy), "고교 정원이 모자라면", 26, SKY, "Bold", anchor="ra", rough=0.04)
    text(im, (W - 70, yy + 40), "수지 구역으로 옮길 길이 있다", 26, SKY, "Bold", anchor="ra", rough=0.04)
    source(im, "경기도교육청 중학교 학교군 고시 2025~2027 · 2027 고입 기본계획 · 2027 평준화지역 배정 방안(출신구역 변경)")
    out(im, n)


# 07 — 두 시의 중학교 배정
def c_lottery(n):
    im, d = board()
    y = header(im, 7, "중학교 배정", "같은 「추첨」이 아니다", "2027학년도 중학교 배정업무 시행계획 — 수원·용인 교육지원청")
    dashed(d, (540, y + 10), (540, y + 720), GHOST, 3, 12, 10)
    cols = [("수원", PINK, 70, [(paper, "학교군 안 여러 곳에", "지원서를 낸다"), (monitor, "컴퓨터로", "추첨"), (school, "배정", "")]),
            ("용인", SKY, 580, [(paper, "희망 순으로", "지원한다"), (calendar, "1지망이 넘치면", "초등 먼저 입학한 순"), (dice, "입학일이 같을 때만", "추첨")])]
    for name, c, x0, steps in cols:
        text(im, (x0, y + 10), name, 48, c)
        for k, (ic, a, b) in enumerate(steps):
            yy = y + 120 + k * 210
            chalk(im, lambda dd, yy=yy, ic=ic, x0=x0, c=c: ic(dd, x0 + 60, yy + 50, 90, c, 5), 0.12)
            text(im, (x0 + 140, yy + 10), a, 28, CHALK, "Bold", rough=0.05)
            if b: text(im, (x0 + 140, yy + 52), b, 34 if (name == "용인" and k == 1) else 30, BUTTER if (name == "용인" and k == 1) else CHALK)
            if k < 2: chalk(im, lambda dd, yy=yy, x0=x0: arrow(dd, (x0 + 60, yy + 118), (x0 + 60, yy + 186), CHALK2, 5, 16), 0.1)
    by = y + 760
    text(im, (70, by), "배정 학교 발표는 두 곳 모두 2026년 12월 31일", 22, MUTE, "Medium", rough=0.03)
    text(im, (70, by + 36), "「먼저 입학」을 전학생에게 어떻게 세는지는 원문에 없다", 22, MUTE, "Medium", rough=0.03)
    conclusion(im, by + 100, "「초등 입학 전에 와야 안정권」이라는 말의 이유")
    source(im, "수원교육지원청·용인교육지원청 2027학년도 중학교 신입생 배정업무 시행계획")
    out(im, n)


# 08 — 집값 연구
def c_research(n):
    im, d = board()
    y = header(im, 8, "학군과 집값", "배경을 지울수록\n학교 몫은 작아졌다", "중학교 수학 「보통학력 이상」 1%p 차이에 붙은 ㎡당 집값 차이")
    vals = [("아무것도 안 뺐을 때", 2.3, [towers, people, school]), ("학군 경계 양쪽끼리만", 1.3, [people, school]), ("주민 구성까지 뺐을 때", 0.5, [school])]
    base = y + 600
    for i, (lab, v, icons) in enumerate(vals):
        cx = 220 + i * 320
        alln = [towers, people, school]
        for k, ic in enumerate(alln):
            on = ic in icons
            chalk(im, lambda dd, k=k, ic=ic, on=on, cx=cx: ic(dd, cx - 80 + k * 80, y + 40, 60, CHALK if on else GHOST, 4 if on else 2), 0.12 if on else 0.45)
        h = v * 140
        chalk(im, lambda dd, cx=cx, h=h, i=i: dd.rectangle([cx - 80, base - h, cx + 80, base], fill=SKY if i == 2 else CHALK2), 0.25)
        text(im, (cx, base - h - 20), f"{v}%", 72, SKY if i == 2 else CHALK, anchor="mb")
        text(im, (cx, base + 18), lab, 24, CHALK2, "Bold", anchor="ma", rough=0.04)
    chalk(im, lambda dd: dd.line([(80, base), (W - 80, base)], fill=CHALK2, width=4), 0.2)
    text(im, (80, y + 100), "도시·주민 구성·학교", 20, MUTE, "Medium", rough=0.02)
    by = base + 80
    text(im, (70, by), "효과가 없다는 연구도 있다 — 서울대 합격률 변화는 집값 상승률을 설명 못 했고,", 22, CHALK2, "Medium", rough=0.03)
    text(im, (70, by + 34), "서울 25개 구에서 집값과 함께 움직인 건 초등 전입뿐이었다. 연구 대부분이 서울 자료다.", 22, CHALK2, "Medium", rough=0.03)
    conclusion(im, by + 100, "「학군이 집값을 몇 % 올린다」는 숫자 하나는 없다")
    source(im, "김성준(한국은행 연구자, 2017 학술대회 발표문, 서울 강남3구+인접 5구 실거래) · 김경민·이양원(2007) · 김경민 외(2010)")
    out(im, n)


# 09 — 영상 vs 공식 문서
def c_claims(n):
    im, d = board()
    y = header(im, 9, "영상 대조", "영상이 말한 것,\n공식 문서가 말한 것", "학군 영상 64편에서 틀리거나 부풀린 주장이 몰린 다섯 곳")
    rows = [("「단지 옆 학교 = 우리 아이 학교」", "중학교는 학교군 안 추첨, 고교는 출신 중학교 구역 추첨", "과장"),
            ("「학교 성적도 공개된다」", "학교별 성적 공시는 2017년부터 없다", "틀림"),
            ("「내신 9등급 기준으로 보면」", "확정된 2028 대입은 내신 5등급", "틀림"),
            ("「학원·사교육이 줄어든다」", "경기 사설학원 2020→2025 +23.9%", "과장"),
            ("「학군이 집값을 크게 올린다」", "주민 구성까지 따지면 2.3% → 0.5%", "과장")]
    for i, (a, b, j) in enumerate(rows):
        yy = y + 20 + i * 145
        text(im, (70, yy), a, 30, PINK)
        text(im, (110, yy + 52), "→ " + b, 24, CHALK, "Bold", rough=0.05)
        stamp(im, W - 140, yy + 30, j, PINK if j == "틀림" else BUTTER, -10 if i % 2 else 8)
        if i < 4: dashed(d, (70, yy + 118), (W - 70, yy + 118), (70, 104, 92), 2, 10, 8)
    conclusion(im, y + 760, "주장 828개 가운데 틀림 8 · 과장 27")
    source(im, "영상 64편 분석 · 근거: 교육청 고시·배정 방안, 교육부 발표(2017.6.14), 2028 대입 개편안, KOSIS 사설학원, 연구 문헌")
    out(im, n)


# 10 — 이사 전 체크리스트
def c_check(n):
    im, d = board()
    y = header(im, 10, "이사 전에", "내가 볼 것 아홉 가지", "어느 동네가 학군 1등인지 대신 — 모두 공개 자료")
    rows = ["학구도 안내 서비스에 주소 넣기", "통학구역 일람표 — 번지·통·반까지", "중학교 배정 — 추첨? 먼저 입학한 순?",
            "고교 평준화 학군과 출신 중학교 구역", "학년별 학생 수, 전입·전출", "중학교 졸업생 진로 — 세 해로",
            "고교 진학률은 「기타」와 같이", "학원 — 1천 명당 개수, 거리는 지도로", "숫자가 없는 것: 학교 성적·학교폭력 비교·분위기"]
    for i, t in enumerate(rows):
        yy = y + 10 + i * 80
        c = SKY if i == 0 else (MUTE if i == 8 else CHALK)
        chalk(im, lambda dd, yy=yy, c=c: dd.rectangle([72, yy + 4, 112, yy + 44], outline=c, width=5), 0.2)
        if i == 0: chalk(im, lambda dd, yy=yy: dd.line([(78, yy + 24), (90, yy + 38), (118, yy - 2)], fill=SKY, width=7), 0.15)
        text(im, (140, yy + 2), t, 32 if i == 0 else 28, c, "Black" if i == 0 else "Bold", rough=0.06)
    conclusion(im, y + 760, "숫자가 없는 것은 없다고 알고 듣는다")
    source(im, "학구도안내서비스(한국교육시설안전원) · 경기도교육청·교육지원청 고시·시행계획 · 학교알리미 · NEIS")
    out(im, n)


if __name__ == "__main__":
    for i, fn in enumerate([c_names, c_measure, c_timeline, c_report, c_grads, c_border, c_lottery, c_research, c_claims, c_check], start=2):
        fn(f"261018_{i}.png")
