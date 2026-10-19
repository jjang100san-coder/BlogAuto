# -*- coding: utf-8 -*-
"""학군 구분 글 카드(10/18). 숫자는 이 폴더 위 문서 값을 그대로 옮긴다.
- [지표] 학군_공식지표_데이터.md (학교알리미 공개용 데이터 합산·NEIS 학원·KOSIS, 2026-10-17 조회, OpenAPI 136곳 교차 일치)
- [정책] 학군_정책연구_논란.md · [행정] 학군_기흥영통_행정사실.md · [영상] 유튜브_학군_종합.md(64편 최종)
학교명·동 이름·채널명은 그림에 쓰지 않는다(사용자 결정 10/17 「영통권 기흥」). 마이너스는 hyphen-minus."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "구구절절_컨텐츠", "261011_병역특례 논란"))
_cwd = os.getcwd()
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_S, F_B, INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
os.chdir(_cwd)
F_SM = font(19); F_M = font(24, True); F_L = font(30, True); F_BIG = font(48, True); F_XS = font(17)
NAVY = (40, 60, 110); DIM = (205, 205, 200)
GU = ["영통", "기흥", "수지", "분당"]
COL = {"영통": RED, "기흥": BLUE, "수지": GREEN, "분당": AMBER}


def save(im, n): im.save(os.path.join(HERE, n)); print("saved", n)


# 2 — 같은 말, 다른 이름(학구도)
def card_names(n):
    im, d = canvas("「학군」은 평판이고, 배정은 이름이 셋이다", "학구도 = 초등 통학구역 + 중학교 학교군·중학구 + 고등학교 학교군 (초·중등교육법 시행령)")
    box(d, (70, 330, 330, 470), SAND, "우리 집\n주소", F_L, INK)
    rows = [("초등학교", "통학구역 (시행령 16조)", "정해진 학교 한 곳 · 교육장이 정함"),
            ("중학교", "학교군·중학구 (시행령 68조)", "학교군은 몇 곳 중 추첨 · 중학구는 지정"),
            ("고등학교", "고등학교 학교군 (시행령 84조)", "평준화 지역은 지망 + 추첨")]
    for i, (a, b, c) in enumerate(rows):
        y = 170 + i * 170
        arrow(d, (330, 400), (420, y + 60), GRAY, 4)
        d.rounded_rectangle([430, y, 1330, y + 120], radius=18, fill=WHITE, outline=(220, 220, 215), width=2)
        d.text((460, y + 18), a, font=F_L, fill=NAVY)
        d.text((680, y + 22), b, font=F_M, fill=INK)
        d.text((680, y + 68), c, font=F_SM, fill=GRAY)
    box(d, (70, 520, 330, 660), PINK, "「학군 좋다」\n= 평판", F_M, RED)
    foot(d, "학구도안내서비스(한국교육시설안전원) 학구도 소개 · 초·중등교육법 시행령 16·68·84조 · 「학군」은 시행령의 배정 단위 이름이 아니다")
    save(im, n)


# 3 — 잴 수 있는 것 / 없는 것 (영상 64편이 쓴 기준)
def card_measure(n):
    rows = [("이름값·평판", 47, "x"), ("학원가", 46, "o"), ("배정 구역·옆 학교", 30, "o"), ("면학 분위기·또래", 30, "x"),
            ("집값", 28, "o"), ("통학 거리", 25, "o"), ("아이 성향·형편", 21, "x"), ("전입·전출", 20, "o"),
            ("특목·자사고 진학", 19, "o"), ("명문대 합격", 19, "x"), ("학교 성적(학업성취도)", 14, "x"), ("학교폭력", 8, "t")]
    im, d = canvas("사람들이 쓰는 기준 vs 공식 숫자로 잴 수 있는 것", "유튜브 학군 영상 64편이 「학군 좋은 곳」의 기준으로 쓴 것 (영상 수)")
    for i, (lab, v, m) in enumerate(rows):
        y = 140 + i * 47
        d.text((90, y + 4), lab, font=F_SM, fill=INK)
        L = v * 13
        col = {"o": NAVY, "x": DIM, "t": (170, 175, 190)}[m]
        d.rectangle([400, y + 6, 400 + L, y + 34], fill=col)
        d.text((410 + L, y + 4), str(v), font=F_SM, fill=GRAY)
        cx = 1110
        if m == "o": d.ellipse([cx - 14, y + 6, cx + 14, y + 34], outline=GREEN, width=4)
        elif m == "x": d.line([cx - 13, y + 7, cx + 13, y + 33], fill=RED, width=4); d.line([cx - 13, y + 33, cx + 13, y + 7], fill=RED, width=4)
        else: d.polygon([(cx, y + 6), (cx - 15, y + 34), (cx + 15, y + 34)], outline=AMBER, width=3)
    lx = 1170
    d.ellipse([lx - 11, 154, lx + 11, 176], outline=GREEN, width=3); d.text((lx + 20, 150), "잴 수 있음", font=F_SM, fill=GREEN)
    d.line([lx - 10, 191, lx + 10, 211], fill=RED, width=3); d.line([lx - 10, 211, lx + 10, 191], fill=RED, width=3); d.text((lx + 20, 188), "공식 숫자 없음", font=F_SM, fill=RED)
    d.polygon([(lx, 226), (lx - 12, 248), (lx + 12, 248)], outline=AMBER, width=3); d.text((lx + 20, 224), "학교별로만 공시", font=F_SM, fill=AMBER)
    foot(d, "영상 분석 64편(2026.10.17) · 잴 수 있는지는 학교알리미·NEIS·교육청 고시 확인 결과 · 학원은 개수만, 질은 못 잰다")
    save(im, n)


# 4 — 학교 성적표가 사라진 해
def card_timeline(n):
    im, d = canvas("학교별 성적은 왜 비교할 수 없을까", "학교별 국가 학업성취도 공개의 흐름 — 법령·판결·교육부 발표")
    ev = [("2010", "학교별 성취도\n학교알리미 공시 시작", LIGHT), ("2017.6", "평가가 3% 표집으로\n학교 공시에서 빠짐", PINK),
          ("법 5조②", "교육감·교육부 공개 때\n학교 이름은 빼게 함", SAND), ("2025.5", "대법원: 이름을 가린\n익명 공개는 가능", LIGHT),
          ("2026.10.29", "기초학력 진단 결과\n외부 공개 금지", PINK)]
    d.line([110, 330, 1290, 330], fill=GRAY, width=4)
    for i, (y, t, c) in enumerate(ev):
        x = 140 + i * 280
        d.ellipse([x - 14, 316, x + 14, 344], fill=NAVY)
        ctext(d, x, 250, y, F_L, NAVY)
        box(d, (x - 125, 380, x + 125, 520), c, t, F_SM, INK)
    box(d, (90, 580, 1310, 690), SAND, "그래서 지금 돌아다니는 「학교별 학업성취도 순위」는 2016년 이전 자료이거나,\n학교 내신 분포를 그렇게 부른 것이다. 내신 분포는 학교마다 기준 점수가 달라 서로 비교할 수 없다.", F_SM, INK)
    foot(d, "교육부 발표(2017.6.14) · 정보공개 특례법 5조② · 대법원 2023추5054 · 기초학력 보장법 7조 · 경기도교육청 학업성적관리 지침")
    save(im, n)


# 5 — 동네의 통지표: 숫자 여섯 개, 1등은 네 곳
def card_report(n):
    rows = [("초등 순유입률 (2025학년도)", ["+1.11%", "-1.95%", "+1.57%", "+1.77%"], 3),
            ("초등 학생 수 변화 (2021→2026)", ["-13.9%", "-30.4%", "-15.6%", "-17.6%"], 0),
            ("특목·자사고 진학 (2025.2 중졸)", ["4.88%", "4.54%", "7.55%", "6.11%"], 2),
            ("학원·교습소 (6~17세 1천 명당)", ["34.4", "28.4", "29.0", "41.3"], 3),
            ("일반고 대학 진학률 (2025.2 졸업)", ["69.5%", "72.7%", "66.9%", "63.1%"], 1),
            ("중학교 과밀교 학생 비율 (2026)", ["72.2%", "71.2%", "82.0%", "97.7%"], None)]
    im, d = canvas("동네의 통지표 — 숫자 여섯 개로 재니 1등이 네 곳", "가장 높은 곳에 ★ (학생 수는 가장 덜 줄어든 곳) · 과밀은 두 가지로 읽혀 순위를 매기지 않음")
    for j, g in enumerate(GU):
        ctext(d, 700 + j * 165, 150, g, F_L, COL[g])
    for i, (lab, vals, star) in enumerate(rows):
        y = 205 + i * 78
        d.rounded_rectangle([70, y, 1330, y + 64], radius=12, fill=WHITE if i % 2 == 0 else (244, 244, 240))
        d.text((95, y + 18), lab, font=F_SM, fill=INK)
        for j, v in enumerate(vals):
            cx = 700 + j * 165
            ctext(d, cx, y + 16, v, F_M, COL[GU[j]] if star == j else GRAY)
            if star == j: d.text((cx + 52, y + 12), "★", font=F_M, fill=AMBER)
        if star is None: d.text((1180, y + 20), "", font=F_SM, fill=GRAY)
    foot(d, "학교알리미 공개용 데이터 합산(학교 위치 기준) · NEIS 학원·교습소 + KOSIS 주민등록 6~17세 · 2026.10.17 조회 · 일반고만 비교")
    save(im, n)


# 6 — 진학률의 함정: 「기타」
def card_gita(n):
    vals = [("기흥", 72.74, 25.0), ("영통", 69.53, 29.14), ("수지", 66.89, 28.34), ("분당", 63.12, 36.44)]
    im, d = canvas("학원이 가장 많은 동네의 대학 진학률이 가장 낮았다", "일반고 졸업생 100명이 간 곳 (2025년 2월 졸업, 공시 기준)")
    for i, (g, a, b) in enumerate(vals):
        y = 180 + i * 105
        d.text((90, y + 22), g, font=F_L, fill=COL[g])
        x0 = 230; L = 1000
        d.rectangle([x0, y + 10, x0 + L * a / 100, y + 80], fill=NAVY)
        d.rectangle([x0 + L * a / 100, y + 10, x0 + L * (a + b) / 100, y + 80], fill=SAND)
        d.text((x0 + 16, y + 28), f"대학 진학 {a:.1f}%", font=F_M, fill=WHITE)
        d.text((x0 + L * a / 100 + 12, y + 28), f"기타 {b:.1f}%", font=F_M, fill=INK)
    box(d, (90, 610, 1310, 700), SAND, "「기타」는 진학·취업에 속하지 않는 경우다. 재수생이 여기에 들어간다(재수생만 따로 센 숫자는 공시에 없다).\n그래서 진학률을 「학군 순위」로 읽으면 거꾸로 된다.", F_SM, INK)
    foot(d, "학교알리미 졸업생 진로 현황(일반고만, 학교 위치 기준) 합산 · 나머지는 취업 등 · 2026.10.17 조회")
    save(im, n)


# 7 — 주소가 학교를 정한다
def card_address(n):
    im, d = canvas("생활은 영통이어도, 주소가 기흥이면 학교는 용인", "영통에 맞닿은 기흥 동네에서 본 초·중·고 배정 — 경기도교육청·교육지원청 원문")
    d.line([700, 150, 700, 700], fill=GRAY, width=4)
    ctext(d, 400, 160, "수원 영통 (생활권)", F_L, RED); ctext(d, 1000, 160, "용인 기흥 (주소)", F_L, BLUE)
    box(d, (860, 230, 1140, 300), SAND, "집 (주소: 기흥)", F_M, INK)
    steps = [("초등학교", "용인 통학구역", 360), ("중학교", "용인 학교군 (공동학구 0)", 470), ("고등학교", "용인 평준화 학군", 580)]
    for t, s, y in steps:
        box(d, (820, y - 40, 1320, y + 40), MINT, t + " — " + s, F_SM, INK)
        box(d, (130, y - 40, 630, y + 40), (240, 240, 236), t + " — 수원 쪽", F_SM, GRAY)
        d.line([640, y, 810, y], fill=(200, 200, 200), width=3)
        d.line([710, y - 16, 742, y + 16], fill=RED, width=5); d.line([710, y + 16, 742, y - 16], fill=RED, width=5)
    box(d, (820, 640, 1320, 700), LIGHT, "정원이 모자라면 → 수지 구역으로 옮길 길", F_SM, NAVY)
    foot(d, "중학교 학교군 고시 2025·2026·2027학년도 · 2027 고입 기본계획(평준화지역 중졸자는 그 지역에 지원) · 2027 배정 방안(출신구역 변경)")
    save(im, n)


# 8 — 두 시의 중학교 배정
def card_lottery(n):
    im, d = canvas("같은 「추첨」이 아니다 — 수원과 용인의 중학교 배정", "2027학년도 중학교 배정업무 시행계획(수원·용인 교육지원청)")
    ctext(d, 360, 150, "수원", F_L, RED); ctext(d, 1040, 150, "용인", F_L, BLUE)
    a = [("학교군 안 여러 중학교에\n지원서를 낸다", 210), ("컴퓨터로 추첨", 360), ("배정", 510)]
    b = [("희망 순으로 지원", 210), ("1지망이 넘치면\n그 구역 초등학교에\n먼저 입학한 학생부터", 360), ("입학일이 같을 때만 추첨", 510)]
    for (t, y) in a:
        box(d, (170, y, 550, y + 110), LIGHT if y < 500 else MINT, t, F_SM, INK)
        if y < 500: arrow(d, (360, y + 112), (360, y + 146), GRAY, 4)
    for (t, y) in b:
        box(d, (850, y, 1230, y + 110), LIGHT if y != 360 else SAND, t, F_SM, INK)
        if y < 500: arrow(d, (1040, y + 112), (1040, y + 146), GRAY, 4)
    box(d, (170, 650, 1230, 705), WHITE, "배정 학교 발표는 두 곳 모두 2026년 12월 31일 · 「먼저 입학」이 전학생에게 어떻게 셈되는지는 원문에 없다", F_XS, GRAY)
    foot(d, "수원교육지원청·용인교육지원청 2027학년도 중학교 신입생 배정업무 시행계획")
    save(im, n)


# 9 — 집값 연구: 배경을 빼면 학교 몫이 줄어든다
def card_research(n):
    vals = [("아무것도 안 뺐을 때", 2.3, DIM), ("학군 경계 양쪽끼리만", 1.3, (170, 180, 205)), ("주민 구성까지 뺐을 때", 0.5, NAVY)]
    im, d = canvas("학군과 집값 — 따지는 범위를 넓힐수록 학교 몫은 줄었다", "중학교 수학 「보통학력 이상」 비율 1%p 차이에 붙은 ㎡당 집값 차이 (서울 강남3구+인접 5구, 2006~2016 실거래)")
    for i, (lab, v, c) in enumerate(vals):
        x = 220 + i * 360; h = v * 150
        d.rectangle([x, 560 - h, x + 220, 560], fill=c)
        ctext(d, x + 110, 560 - h - 60, f"{v}%", F_BIG, NAVY if i == 2 else GRAY)
        ctext(d, x + 110, 575, lab, F_SM, INK)
    d.line([160, 560, 1240, 560], fill=GRAY, width=2)
    box(d, (90, 630, 1310, 705), SAND, "효과가 없다는 연구도 있다: 서울대 합격률 변화는 집값 상승률을 설명하지 못했고(수도권 42개 시·구),\n서울 25개 구에서 집값과 함께 움직인 건 초등 전입뿐이었다. 연구 대부분이 서울 자료다.", F_XS, INK)
    foot(d, "김성준(한국은행 연구자, 2017 ISI 학술대회 발표문) · 김경민·이양원(2007, 국토연구) · 김경민 외(2010, 국토연구)")
    save(im, n)


# 10 — 영상이 말한 것 / 공식 문서가 말한 것
def card_claims(n):
    rows = [("「단지 옆 학교 = 우리 아이 학교」", "중학교는 학교군 안 추첨, 고교 2단계는 출신 중학교 구역 추첨"),
            ("「학교 성적도 공개된다」", "학교별 학업성취도 공시는 2017년부터 없다"),
            ("「내신 9등급·절대평가 전환」", "확정된 2028 대입은 내신 5등급 + 통합형 수능"),
            ("「학원·사교육이 줄어든다」", "경기 사설학원 2020→2025 +23.9%"),
            ("「학군이 집값을 크게 올린다」", "주민 구성까지 따지면 2.3% → 0.5%")]
    im, d = canvas("영상이 말한 것 vs 공식 문서가 말한 것", "학군 영상 64편에서 틀리거나 부풀린 주장이 몰린 다섯 곳")
    for i, (a, b) in enumerate(rows):
        y = 150 + i * 105
        box(d, (70, y, 600, y + 85), PINK, a, F_SM, INK)
        arrow(d, (610, y + 42), (680, y + 42), GRAY, 4)
        box(d, (690, y, 1330, y + 85), MINT, b, F_SM, INK)
    foot(d, "영상 64편 주장 828개 중 틀림 8·과장 27 · 근거: 교육청 고시·배정 방안, 교육부 발표, 2028 대입 개편안, KOSIS, 연구 문헌")
    save(im, n)


# 11 — 이사 전 체크리스트
def card_check(n):
    rows = ["학구도안내서비스에 주소 넣기 → 초등 통학구역·중학교 학교군·고교 학교군",
            "교육지원청 통학구역 일람표 — 번지·통·반까지",
            "그 시의 중학교 배정 시행계획 — 추첨인지, 먼저 입학한 순인지",
            "고교 평준화 학군과 출신 중학교 구역 — 정원이 모자란 구역의 규정",
            "학교알리미 학년별 학생 수와 전입·전출 (초등이 가장 정직하다)",
            "중학교 졸업생 진로 — 한 해 말고 세 해로",
            "고교 진학률은 「기타」와 같이, 일반고끼리만",
            "학원은 1천 명당 개수와 입시·보습 비중, 거리는 지도로",
            "숫자가 없는 것: 학교별 성적 비교, 학교폭력 묶음 비교, 분위기"]
    im, d = canvas("이사 전에 내가 볼 숫자 아홉 줄", "어느 동네가 학군 1등인지 대신 — 모두 공개 자료")
    for i, t in enumerate(rows):
        y = 140 + i * 62
        d.rounded_rectangle([90, y + 6, 126, y + 42], radius=6, outline=NAVY if i < 8 else GRAY, width=3)
        d.text((150, y + 8), t, font=F_SM, fill=INK if i < 8 else GRAY)
    foot(d, "학구도안내서비스(한국교육시설안전원) · 경기도교육청·교육지원청 고시·시행계획 · 학교알리미 · NEIS")
    save(im, n)


if __name__ == "__main__":
    for i, fn in enumerate([card_names, card_measure, card_timeline, card_report, card_gita, card_address, card_lottery,
                            card_research, card_claims, card_check], start=2):
        fn(f"261018_{i}.png")
