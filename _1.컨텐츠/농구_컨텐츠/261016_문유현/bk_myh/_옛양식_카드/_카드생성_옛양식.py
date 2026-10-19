# -*- coding: utf-8 -*-
"""금메달 시리즈 8편(문유현) 자체 제작 카드 01~03.
영상 프레임은 한 장도 쓰지 않는다(마스터지침 6-7). 숫자는 종합분석_문유현.md · base data\프로필_KBL확인_문유현.md 그대로.
판형은 2·3·6편과 같다. 색만 모카(회갈색)로 바꾼다(지침 5-4 시리즈 색 분리 — 3편 버건디·6편 올리브). 주황 강조는 시리즈 공통.
3편(형)의 형제 비교 카드(bk_mjh_03)는 다시 만들지 않는다 — 이 편은 동생 기록만.
썸네일은 AI 장면(bk_myh_ai_01)이라 카드는 전부 본문용이다(지침 5-4)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
W = 1200
BG, CARD, EDGE = "#F8F3EE", "#FFFFFF", "#E6DCD2"
INK, SUB, MUTE = "#241E1A", "#86776B", "#B3A69A"
MOCHA, PALE, PALE_EDGE = "#6B4E3D", "#F1E6DD", "#E0CDBE"
ORANGE = "#E2622B"
M = 64

def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def text(d, xy, s, size, weight="Bold", fill=INK, anchor="la"):
    d.text(xy, s, font=font(size, weight), fill=fill, anchor=anchor)

def canvas(h):
    im = Image.new("RGB", (W, h), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=MOCHA)
    return im, d

def box(d, x0, y0, x1, y1, fill=CARD, edge=EDGE, r=18):
    d.rounded_rectangle([x0, y0, x1, y1], r, fill=fill, outline=edge, width=2)

def footer(d, y, s, h=112):
    box(d, M, y, W - M, y + h, fill=PALE, edge=PALE_EDGE)
    text(d, (W / 2, y + h / 2), s, 40, "Bold", MOCHA, "mm")

def note(d, y, s):
    text(d, (W / 2, y), s, 24, "Medium", MUTE, "mm")

def save(im, name):
    p = os.path.join(OUT, name); im.save(p, optimize=True); print("saved", name, im.size)


# 01 · 네임카드 — KBL 공식 프로필
def card_01():
    rows = [
        ("소속", "안양 정관장 · 등번호 24"),
        ("포지션", "가드"),
        ("생년월일", "2004년 6월 8일"),
        ("키", "180cm"),
        ("출신 학교", "고려대 (3학년 때 프로 진출)"),
        ("드래프트", "2025년 1라운드 1순위"),
        ("데뷔 시즌", "24경기 평균 9.1점 · 3.0어시스트"),
        ("형", "문정현 (수원 KT, 2023년 1순위)"),
    ]
    rh, gap, y0 = 96, 14, 352
    h = y0 + len(rows) * (rh + gap) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 98), "금메달 시리즈 8", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 196), "문유현", 120, "Black", INK, "mm")
    text(d, (W / 2, 284), "2026 아시안게임 금메달", 40, "Bold", MOCHA, "mm")
    y = y0
    for k, v in rows:
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + rh / 2), k, 36, "Bold", ORANGE if k == "키" else MOCHA, "lm")
        text(d, (M + 250, y + rh / 2), v, 36 if len(v) > 18 else 38, "Bold", INK, "lm")
        y += rh + gap
    y += 26
    footer(d, y, "코트에서 작은 쪽, 1순위로 온 가드")
    note(d, y + 112 + 44, "프로필·기록: KBL 공식 홈페이지 (2026년 10월 16일)")
    save(im, "bk_myh_01_namecard.png")


# 02 · 데뷔에서 금메달까지 — 세로 타임라인. 형 기록은 넣지 않는다
def card_02():
    items = [   # (종류, 날짜, 무엇, 덧붙임)
        ("in",  "2025년 11월 14일", "드래프트 전체 1순위", "고려대 3학년"),
        ("out", "11월~12월", "부상으로 데뷔를 기다림", "햄스트링"),
        ("in",  "2026년 1월 1일", "프로 데뷔", "서울 SK 원정"),
        ("in",  "1월 4일", "홈 데뷔전 뒤 눈물", "만원 관중 앞"),
        ("key", "1월 21일", "형과 첫 맞대결 18점", "「3년 안에 공수겸장」"),
        ("in",  "2월 4일", "대표팀 명단", "신인 셋 중 한 명"),
        ("key", "9월 20일", "아시안게임 금메달", "형과 함께"),
    ]
    hh, y0, gap = 150, 300, 18
    h = y0 + len(items) * hh + gap * (len(items) - 1) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "데뷔에서 금메달까지", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "문유현 · 안양 정관장 24번", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 240), "1월 1일에 데뷔해 9월 20일에 금메달", 34, "Bold", MUTE, "mm")
    lx, bx = M + 26, M + 76
    ys, y = [], y0
    for kind, when, what, sub in items:
        box(d, bx, y, W - M, y + hh)
        col = {"in": MOCHA, "out": SUB, "key": ORANGE}[kind]
        text(d, (bx + 40, y + 46), when, 31, "Bold", col, "lm")
        text(d, (bx + 40, y + hh - 46), what, 40, "Black", SUB if kind == "out" else INK, "lm")
        text(d, (W - M - 40, y + 46), sub, 29, "Bold", col, "rm")
        ys.append((y + hh / 2, kind))
        y += hh + gap
    d.line([lx, ys[0][0], lx, ys[-1][0]], fill=MOCHA, width=6)
    for cy, kind in ys:
        r = 18
        col = {"in": MOCHA, "out": MUTE, "key": ORANGE}[kind]
        if kind == "out":
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=BG, outline=col, width=5)
        else:
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=col)
    y += 18
    footer(d, y, "3년을 말하고, 8개월 뒤 금메달")
    note(d, y + 112 + 44, "KBL 공식 홈페이지 · 드래프트·데뷔·대표 명단은 기사 · 인용은 수훈 인터뷰(크블인터뷰·KBS)")
    save(im, "bk_myh_02_timeline.png")


# 03 · 금메달 뒤 개막 다섯 경기 — KBL 경기별 기록
def card_03():
    games = [   # (날짜, 상대, 결과, 득점, 어시스트, 스틸)
        ("10월 3일", "울산 현대모비스", "승 88-85", 8, 8, 1),
        ("10월 5일", "대구 한국가스공사", "승 86-80", 9, 2, 0),
        ("10월 9일", "서울 삼성", "패 58-66", 3, 3, 0),
        ("10월 11일", "창원 LG", "승 88-65", 11, 5, 1),
        ("10월 13일", "고양 소노", "승 85-81", 9, 4, 4),
    ]
    hi = {(0, 4), (3, 3), (4, 5)}
    rh, gap, y0 = 160, 14, 330
    h = y0 + len(games) * (rh + gap) + 124 + 56 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "금메달 뒤 개막 다섯 경기", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "안양 정관장 · 2026-27 프로농구", 38, "Bold", SUB, "mm")
    lw = 430
    sw = (W - 2 * M - lw) / 3
    sx = [M + lw + sw * (k + 0.5) for k in range(3)]
    for k, lab in enumerate(["득점", "어시스트", "스틸"]):
        text(d, (sx[k], 284), lab, 32, "Bold", MOCHA, "mm")
    y = y0
    for gi, (when, opp, res, pts, ast, stl) in enumerate(games):
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + 52), when + " · " + res, 30, "Bold", SUB, "lm")
        text(d, (M + 40, y + 108), opp, 40 if len(opp) < 8 else 34, "Black", INK, "lm")
        for k, v in enumerate((pts, ast, stl)):
            col = ORANGE if (gi, k + 3) in hi else INK
            text(d, (sx[k], y + rh / 2), str(v), 70, "Black", col, "mm")
        y += rh + gap
    box(d, M, y, W - M, y + 124, fill=CARD, edge=EDGE)
    text(d, (M + 40, y + 44), "다섯 경기 평균 · 팀 4승 1패", 30, "Bold", SUB, "lm")
    text(d, (M + 40, y + 90), "8.0점 · 4.4어시스트 · 1.2스틸 · 출전 22분 26초", 34, "Bold", INK, "lm")
    y += 124 + 56
    footer(d, y, "득점보다 먼저 보이는 패스와 스틸")
    note(d, y + 112 + 44, "기록: KBL 공식 홈페이지 선수 경기별 기록 (2026년 10월 16일)")
    save(im, "bk_myh_03_opening.png")


if __name__ == "__main__":
    for f in (card_01, card_02, card_03): f()
