# -*- coding: utf-8 -*-
"""칠판 학구도 양식 시안 3장(통지표 · 졸업생 100명 · 경계 지도). 숫자는 make_cards.py 와 같은 원문 값."""
import os
from PIL import ImageDraw
from hakgudo_cards_base import *
HERE = os.path.dirname(os.path.abspath(__file__))
GU = ["영통", "기흥", "수지", "분당"]


def report():
    im, d = board()
    y = header(im, 5, "동네의 통지표", "과목 여섯 개,\n1등은 네 곳이었다", "영통·기흥·수지·분당을 공식 숫자로 재 보니")
    rows = [("아이들이 들어오나", "초등 순유입률(%) · 2025", ["+1.11", "-1.95", "+1.57", "+1.77"], 3, "%"),
            ("아이가 덜 줄었나", "초등 학생 수 변화(%) · 2021→2026", ["-13.9", "-30.4", "-15.6", "-17.6"], 0, "%"),
            ("특목·자사고 진학", "중학교 졸업생(%) · 2025", ["4.88", "4.54", "7.55", "6.11"], 2, "%"),
            ("학원 수", "6~17세 1천 명당(곳)", ["34.4", "28.4", "29.0", "41.3"], 3, ""),
            ("대학 진학률", "일반고 졸업생(%) · 2025", ["69.5", "72.7", "66.9", "63.1"], 1, "%"),
            ("과밀 중학교", "학급 28명 넘는 학교 학생(%)", ["72.2", "71.2", "82.0", "97.7"], None, "%")]
    x0 = 560
    for j, g in enumerate(GU):
        text(im, (x0 + j * 120 + 55, y + 6), g, 30, GU_COL[g], anchor="ma")
    y += 64
    d = ImageDraw.Draw(im)
    for i, (a, b, vals, star, unit) in enumerate(rows):
        yy = y + i * 108
        dashed(d, (70, yy - 8), (W - 70, yy - 8), (70, 104, 92), 2, 10, 8)
        text(im, (70, yy + 14), a, 32, CHALK)
        text(im, (70, yy + 60), b, 22, MUTE, "Medium", rough=0.03)
        for j, v in enumerate(vals):
            cx = x0 + j * 120 + 55
            if star == j:
                chalk(im, lambda dd, cx=cx, yy=yy: dd.ellipse([cx - 56, yy + 6, cx + 56, yy + 90], outline=GU_COL[GU[j]], width=6), 0.25)
                text(im, (cx, yy + 48), v, 38, GU_COL[GU[j]], anchor="mm")
            else:
                text(im, (cx, yy + 48), v, 28, MUTE, "Bold", anchor="mm", rough=0.05)
    text(im, (W - 70, y + 6 * 108 - 4), "과밀은 「인기」로도 「자리 부족」으로도 읽혀 동그라미 없음", 20, MUTE, "Medium", anchor="ra", rough=0.02)
    conclusion(im, y + 6 * 108 + 40, "「학군 1등」은 무엇을 재느냐에 따라 바뀐다")
    source(im, "학교알리미 공개용 데이터 합산(학교 위치 기준) · NEIS 학원 + KOSIS 6~17세 · 2026.10.17 조회 · 진학률은 일반고만")
    im.save(os.path.join(HERE, "v3_report.png"))


def grads():
    im, d = board()
    y = header(im, 6, "진학률의 함정", "학원이 가장 많은 동네,\n대학 진학률은 가장 낮았다", "일반고 졸업생 100명이 3월에 간 곳 · 2025년 2월 졸업")
    vals = [("기흥", 72.74, 25.0), ("영통", 69.53, 29.14), ("수지", 66.89, 28.34), ("분당", 63.12, 36.44)]
    d = ImageDraw.Draw(im)
    for i, (g, a, b) in enumerate(vals):
        x0 = 70 + (i % 2) * 490; y0 = y + 10 + (i // 2) * 340
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
        text(im, (x0, y0 + 322), f"대학 {a:.1f}%", 24, CHALK2, "Bold", rough=0.04)
    yy = y + 722
    chalk(im, lambda dd: (dd.ellipse([74, yy + 6, 92, yy + 24], fill=CHALK), dd.ellipse([250, yy + 6, 268, yy + 24], outline=BUTTER, width=4)), 0.1)
    text(im, (102, yy), "대학 진학", 22, CHALK2, "Bold", rough=0.03); text(im, (278, yy), "기타(재수생이 여기에 들어간다)", 22, BUTTER, "Bold", rough=0.03)
    conclusion(im, yy + 56, "진학률을 「학군 순위」로 읽으면 거꾸로 된다", BUTTER)
    source(im, "학교알리미 졸업생 진로 현황(일반고만, 학교 위치 기준) 합산 · 점 1개 = 1명(반올림) · 재수생만 센 숫자는 공시에 없다")
    im.save(os.path.join(HERE, "v3_grads.png"))


def border():
    im, d = board()
    y = header(im, 7, "주소가 학교를 정한다", "생활은 영통이어도\n주소가 기흥이면 학교는 용인", "영통에 맞닿은 기흥 동네 · 교육청 고시·배정 방안 원문")
    d = ImageDraw.Draw(im)
    top, bot = y + 10, y + 690
    # 두 구역 면
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
    im.save(os.path.join(HERE, "v3_border.png"))


if __name__ == "__main__":
    report(); grads(); border(); print("ok")
