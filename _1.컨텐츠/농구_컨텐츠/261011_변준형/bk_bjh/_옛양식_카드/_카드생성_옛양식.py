# -*- coding: utf-8 -*-
"""금메달 시리즈 4편(변준형) 자체 제작 카드 01~04.
영상 프레임은 한 장도 쓰지 않는다(마스터지침 6-7). 숫자는 종합분석_변준형.md · base data\프로필_KBL확인_변준형.md · 2차수집_변준형.md 그대로.
판형은 2·3·6편과 같다: 폭 1200 · 크림 배경 · 상단 띠 · 흰 둥근 칸 · 하단 결론 박스.
색만 6편 올리브 → 슬레이트로 바꾼다(지침 5-4 시리즈 색 분리). 주황 강조는 시리즈 공통.
썸네일은 AI 장면(bk_bjh_ai_01)이라 카드는 전부 본문용이다(지침 5-4)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
W = 1200
BG, CARD, EDGE = "#F6F4EE", "#FFFFFF", "#DDDFE2"
INK, SUB, MUTE = "#1C2228", "#6F7A84", "#A3ABB3"
SLATE, PALE, PALE_EDGE = "#3C5266", "#E3E9EE", "#C9D3DC"
ORANGE = "#E2622B"
M = 64

def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def text(d, xy, s, size, weight="Bold", fill=INK, anchor="la"):
    d.text(xy, s, font=font(size, weight), fill=fill, anchor=anchor)

def canvas(h):
    im = Image.new("RGB", (W, h), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=SLATE)
    return im, d

def box(d, x0, y0, x1, y1, fill=CARD, edge=EDGE, r=18):
    d.rounded_rectangle([x0, y0, x1, y1], r, fill=fill, outline=edge, width=2)

def footer(d, y, s, h=112):
    box(d, M, y, W - M, y + h, fill=PALE, edge=PALE_EDGE)
    text(d, (W / 2, y + h / 2), s, 40, "Bold", SLATE, "mm")

def note(d, y, s):
    text(d, (W / 2, y), s, 24, "Medium", MUTE, "mm")

def save(im, name):
    p = os.path.join(OUT, name); im.save(p, optimize=True); print("saved", name, im.size)


# 01 · 네임카드 — KBL 공식 프로필
def card_01():
    rows = [
        ("소속", "안양 정관장 · 등번호 5"),
        ("포지션", "가드"),
        ("생년월일", "1996년 3월 11일"),
        ("키", "185cm"),
        ("출신 학교", "동국대"),
        ("드래프트", "2018년 1라운드 2순위"),
        ("신인상", "2018-19 시즌"),
        ("병역", "2023년 5월 상무 입대 → 2024년 11월 전역"),
    ]
    rh, gap, y0 = 96, 14, 352
    h = y0 + len(rows) * (rh + gap) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 98), "금메달 시리즈 4", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 196), "변준형", 120, "Black", INK, "mm")
    text(d, (W / 2, 284), "2026 아시안게임 금메달", 40, "Bold", SLATE, "mm")
    y = y0
    for k, v in rows:
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + rh / 2), k, 36, "Bold", ORANGE if k == "소속" else SLATE, "lm")
        text(d, (M + 250, y + rh / 2), v, 36 if len(v) > 18 else 38, "Bold", INK, "lm")
        y += rh + gap
    y += 26
    footer(d, y, "군대를 먼저 다녀온 금메달리스트")
    note(d, y + 112 + 44, "프로필: KBL 공식 홈페이지 (2026년 10월 16일) · 입대·전역: 점프볼")
    save(im, "bk_bjh_01_namecard.png")


# 02 · 동국대에서 금메달까지 — 세로 타임라인. 계산한 숫자 없음
def card_02():
    items = [   # (종류, 날짜, 무엇, 덧붙임)
        ("in",  "2018년", "동국대 → 드래프트 2순위", "안양 KGC"),
        ("in",  "2019년 3월", "신인상", "109표 중 106표"),
        ("key", "2021년 · 2023년", "우승 두 번", "2022-23 통합우승"),
        ("out", "2023년 5월 15일", "상무 입대", "2024년 11월 14일 전역"),
        ("in",  "2026년 5월", "안양 잔류", "보수 8억 원 · 3년"),
        ("key", "2026년 9월 20일", "아시안게임 금메달", "결승 일본전 67-57"),
    ]
    hh, y0, gap = 160, 300, 20
    h = y0 + len(items) * hh + gap * (len(items) - 1) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "동국대에서 금메달까지", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "변준형 · 프로에 와서 한 팀, 안양", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 240), "금메달보다 군대가 먼저였다", 34, "Bold", MUTE, "mm")
    lx, bx = M + 26, M + 76
    ys, y = [], y0
    for kind, when, what, sub in items:
        box(d, bx, y, W - M, y + hh)
        col = {"in": SLATE, "out": SUB, "key": ORANGE}[kind]
        text(d, (bx + 40, y + 48), when, 32, "Bold", col, "lm")
        text(d, (bx + 40, y + hh - 50), what, 42, "Black", INK, "lm")
        text(d, (W - M - 40, y + 48), sub, 30, "Bold", col, "rm")
        ys.append((y + hh / 2, kind))
        y += hh + gap
    d.line([lx, ys[0][0], lx, ys[-1][0]], fill=SLATE, width=6)
    for cy, kind in ys:
        r = 18
        col = {"in": SLATE, "out": SUB, "key": ORANGE}[kind]
        if kind == "out":
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=BG, outline=col, width=5)
        else:
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=col)
    y += 18
    footer(d, y, "병역 혜택 8명 명단에는 없다")
    note(d, y + 112 + 44, "드래프트·우승: KBL 공식 홈페이지 · 신인상: 연합뉴스 · 입대·전역: 점프볼 · 계약: 구단 발표 기사")
    save(im, "bk_bjh_02_timeline.png")


# 03 · 보수 8억 — 기사 수치 그대로, 비율·인상률 안 씀
def card_03():
    rows = [   # (항목, 값)
        ("연봉", "5억 6천만 원"),
        ("인센티브", "2억 4천만 원"),
        ("계약 기간", "3년"),
    ]
    rh, gap, y0 = 132, 18, 470
    h = y0 + len(rows) * (rh + gap) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "변준형 보수 8억 원", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "2026년 5월 · 안양 정관장 재계약 첫해", 38, "Bold", SUB, "mm")
    box(d, M, 250, W - M, 420, fill=CARD, edge=EDGE)
    text(d, (M + 40, 335), "보수 총액", 40, "Bold", SLATE, "lm")
    text(d, (W - M - 40, 335), "8억 원", 88, "Black", ORANGE, "rm")
    y = y0
    for k, v in rows:
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + rh / 2), k, 38, "Bold", SLATE, "lm")
        text(d, (W - M - 40, y + rh / 2), v, 46, "Black", INK, "rm")
        y += rh + gap
    y += 22
    footer(d, y, "「증명하라고 주신 지표 같다」")
    note(d, y + 112 + 44, "계약: 구단 발표 기사(2026년 5월 21일) · 말: 바스켓코리아(5월 22일)")
    save(im, "bk_bjh_03_pay.png")


# 04 · 금메달 뒤 개막 다섯 경기 — KBL 경기별 기록
def card_04():
    games = [   # (날짜, 상대, 결과, 득점, 어시스트, 리바운드)
        ("10월 3일", "울산 현대모비스", "승 88-85", 14, 10, 1),
        ("10월 5일", "대구 한국가스공사", "승 86-80", 15, 2, 4),
        ("10월 9일", "서울 삼성", "패 58-66", 9, 5, 2),
        ("10월 11일", "창원 LG", "승 88-65", 12, 8, 2),
        ("10월 13일", "고양 소노", "승 85-81", 11, 11, 2),
    ]
    hi = {(0, 3), (0, 4), (1, 3), (4, 3), (4, 4)}   # 더블더블 두 경기 + 최다 득점
    rh, gap, y0 = 150, 16, 330
    h = y0 + len(games) * (rh + gap) + 140 + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "금메달 뒤 개막 다섯 경기", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "안양 정관장 · 2026-27 프로농구", 38, "Bold", SUB, "mm")
    lw = 430
    sw = (W - 2 * M - lw) / 3
    sx = [M + lw + sw * (k + 0.5) for k in range(3)]
    for k, lab in enumerate(["득점", "어시스트", "리바운드"]):
        text(d, (sx[k], 284), lab, 32, "Bold", SLATE, "mm")
    y = y0
    for gi, (when, opp, res, pts, ast, reb) in enumerate(games):
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + 48), when + " · " + res, 30, "Bold", SUB, "lm")
        text(d, (M + 40, y + 102), opp, 42 if len(opp) < 8 else 36, "Black", INK, "lm")
        for k, v in enumerate((pts, ast, reb)):
            col = ORANGE if (gi, k + 3) in hi else INK
            text(d, (sx[k], y + rh / 2), str(v), 68, "Black", col, "mm")
        y += rh + gap
    box(d, M, y, W - M, y + 124, fill=CARD, edge=EDGE)
    text(d, (M + 40, y + 44), "다섯 경기 평균", 30, "Bold", SUB, "lm")
    text(d, (M + 40, y + 90), "12.2점 · 7.2어시스트 · 2.2리바운드 · 출전 30분", 34, "Bold", INK, "lm")
    y += 124 + 56
    footer(d, y, "더블더블 두 번, 팀은 4승 1패")
    note(d, y + 112 + 44, "기록: KBL 공식 홈페이지 선수 경기별 기록 (2026년 10월 16일)")
    save(im, "bk_bjh_04_opening.png")


if __name__ == "__main__":
    for f in (card_01, card_02, card_03, card_04): f()
