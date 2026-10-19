# -*- coding: utf-8 -*-
"""금메달 시리즈 3편(문정현) 자체 제작 카드 01~04.
영상 프레임은 한 장도 쓰지 않는다(마스터지침 6-7). 숫자는 종합분석_문정현.md · base data\프로필_KBL확인_문정현.md · 개막_기록_문정현.md 그대로.
판형은 2편(_카드생성.py, bk_ljh_*)과 같다: 폭 1200 · 크림 배경 · 상단 띠 · 흰 둥근 칸 · 하단 결론 박스.
색만 2편 남색/연하늘 → 버건디/연살구로 바꾼다(지침 5-4 시리즈 색 분리). 주황 강조는 시리즈 공통.
썸네일은 AI 장면(bk_mjh_ai_01)이라 카드는 전부 본문용이다(지침 5-4, 10/9)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")

OUT = os.path.dirname(os.path.abspath(__file__))   # 초안 md 와 같은 폴더 (fill_editor 가 여기서 찾는다)
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
W = 1200
BG, CARD, EDGE = "#FBF5EA", "#FFFFFF", "#EADFCC"
INK, SUB, MUTE = "#1E2420", "#8A8070", "#B4AA99"
BURG, APRI, APRI_EDGE = "#7A2E3A", "#F6E7E1", "#EBCFC5"
ORANGE = "#E2622B"
M = 64

def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def text(d, xy, s, size, weight="Bold", fill=INK, anchor="la"):
    d.text(xy, s, font=font(size, weight), fill=fill, anchor=anchor)

def canvas(h):
    im = Image.new("RGB", (W, h), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=BURG)
    return im, d

def box(d, x0, y0, x1, y1, fill=CARD, edge=EDGE, r=18):
    d.rounded_rectangle([x0, y0, x1, y1], r, fill=fill, outline=edge, width=2)

def footer(d, y, s, h=112):
    box(d, M, y, W - M, y + h, fill=APRI, edge=APRI_EDGE)
    text(d, (W / 2, y + h / 2), s, 40, "Bold", BURG, "mm")

def note(d, y, s):
    text(d, (W / 2, y), s, 24, "Medium", MUTE, "mm")

def save(im, name):
    p = os.path.join(OUT, name); im.save(p, optimize=True); print("saved", name, im.size)


# 01 · 네임카드 — KBL 공식 프로필
def card_01():
    rows = [
        ("소속", "수원 KT · 등번호 12"),
        ("포지션", "포워드"),
        ("생년월일", "2001년 7월 30일"),
        ("키", "194cm"),
        ("출신 학교", "고려대"),
        ("드래프트", "2023년 1라운드 1순위"),
        ("지난 시즌", "평균 7.9점 · 5.5리바운드"),
        ("12번", "초등학교 때부터, 엄마가 정한 번호"),
    ]
    rh, gap, y0 = 96, 14, 352
    h = y0 + len(rows) * (rh + gap) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 98), "금메달 시리즈 3", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 196), "문정현", 120, "Black", INK, "mm")
    text(d, (W / 2, 284), "2026 아시안게임 금메달", 40, "Bold", BURG, "mm")
    y = y0
    for k, v in rows:
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + rh / 2), k, 36, "Bold", ORANGE if k == "소속" else BURG, "lm")
        text(d, (M + 250, y + rh / 2), v, 38, "Bold", INK, "lm")
        y += rh + gap
    y += 26
    footer(d, y, "명단 밖에서 불려 온 12번")
    note(d, y + 112 + 44, "프로필·기록: KBL 공식 홈페이지 (2026년 10월 3일) · 12번: 본인 인터뷰")
    save(im, "bk_mjh_01_namecard.png")


# 02 · 두 번의 대체 발탁 — 세로 타임라인. 9/2 제외 사유(부상)는 본인 말뿐이라 카드에 넣지 않는다
def card_02():
    items = [   # (종류, 날짜, 무엇, 덧붙임)
        ("in",  "5월 27일", "대표팀 대체 선발", "빠진 선수 대신 첫 발탁"),
        ("out", "9월 2일", "아시안게임 최종 12명 발표", "명단에 없음"),
        ("key", "9월 9일 오전", "대체 합류", "최종 엔트리 교체"),
        ("key", "9월 10일", "조별 1차전 사우디아라비아전", "합류 다음 날 출전"),
        ("in",  "9월 20일", "결승 일본전 선발", "67-57 금메달"),
    ]
    hh, y0, gap = 168, 300, 22
    h = y0 + len(items) * hh + gap * (len(items) - 1) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "두 번의 대체 발탁", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "2026년 남자농구 대표팀 · 문정현", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 240), "명단 밖에서 결승 선발까지", 34, "Bold", MUTE, "mm")
    lx, bx = M + 26, M + 76
    ys, y = [], y0
    for kind, when, what, sub in items:
        box(d, bx, y, W - M, y + hh)
        col = {"in": BURG, "out": SUB, "key": ORANGE}[kind]
        text(d, (bx + 40, y + 50), when, 34, "Bold", col, "lm")
        text(d, (bx + 40, y + hh - 52), what, 44, "Black", SUB if kind == "out" else INK, "lm")
        text(d, (W - M - 40, y + 50), sub, 32, "Bold", col, "rm")
        ys.append((y + hh / 2, kind))
        y += hh + gap
    d.line([lx, ys[0][0], lx, ys[-1][0]], fill=BURG, width=6)
    for cy, kind in ys:
        r = 18
        col = {"in": BURG, "out": MUTE, "key": ORANGE}[kind]
        if kind == "out":
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=BG, outline=col, width=5)
        else:
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=col)
    y += 18
    footer(d, y, "합류 다음 날부터 뛰었다")
    note(d, y + 112 + 44, "명단: 마이데일리(5월 27일·9월 2일) · 합류: 연합뉴스TV(9월 9일) · 선발: 결승 리뷰 자료 화면")
    save(im, "bk_mjh_02_two_callups.png")


# 03 · 형제 — 둘 다 1순위, 둘 다 금메달
def card_03():
    rows = [
        ("소속", "수원 KT · 12", "안양 정관장 · 24"),
        ("포지션", "포워드", "가드"),
        ("키", "194cm", "180cm"),
        ("생년", "2001년", "2004년"),
        ("드래프트", "2023 1라운드 1순위", "2025 1라운드 1순위"),
    ]
    rh, gap, y0 = 104, 14, 470
    h = y0 + len(rows) * (rh + gap) + 136 + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "형 문정현, 동생 문유현", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "KBL 등록 기준", 36, "Bold", SUB, "mm")
    lw = 210                                   # 왼쪽 항목 칸
    cw = (W - 2 * M - lw - 2 * 16) / 2         # 형·동생 칸
    cx = [M + lw + 16 + cw / 2, M + lw + 16 + cw + 16 + cw / 2]
    for i, (who, name) in enumerate([("형", "문정현"), ("동생", "문유현")]):
        x0 = cx[i] - cw / 2
        box(d, x0, 250, x0 + cw, 440, fill=APRI if i == 0 else CARD, edge=APRI_EDGE if i == 0 else EDGE)
        text(d, (cx[i], 300), who, 36, "Bold", BURG if i == 0 else SUB, "mm")
        text(d, (cx[i], 382), name, 66, "Black", INK, "mm")
    y = y0
    for k, a, b in rows:
        box(d, M, y, W - M, y + rh)
        text(d, (M + 36, y + rh / 2), k, 34, "Bold", BURG, "lm")
        hi = ORANGE if k == "드래프트" else INK
        for i, v in enumerate((a, b)):
            text(d, (cx[i], y + rh / 2), v, 36 if k == "드래프트" else 40, "Bold", hi, "mm")
        y += rh + gap
    box(d, M, y, W - M, y + 118, fill=CARD, edge=ORANGE)
    text(d, (M + 36, y + 59), "아시안게임", 34, "Bold", BURG, "lm")
    for i in range(2):
        text(d, (cx[i], y + 59), "금메달", 46, "Black", ORANGE, "mm")
    y += 118 + 40
    footer(d, y, "둘 다 1순위, 둘 다 금메달")
    note(d, y + 112 + 44, "프로필: KBL 공식 홈페이지 (2026년 10월 3일)")
    save(im, "bk_mjh_03_brothers.png")


# 04 · 금메달 뒤 개막 세 경기 — KBL 경기별 기록. %는 쓰지 않고 3점은 분수로
def card_04():
    games = [   # (날짜, 상대, 결과, 득점, 리바운드, 3점)
        ("10월 4일", "서울 삼성", "패 76-81", 5, 10, "1/4"),
        ("10월 6일", "창원 LG", "승 97-72", 14, 10, "2/3"),
        ("10월 9일", "고양 소노", "승 88-79", 12, 5, "4/6"),
    ]
    hi = {(0, 4), (1, 3), (1, 4), (2, 5)}      # 강조할 칸 (경기, 열)
    rh, gap, y0 = 176, 18, 330
    h = y0 + len(games) * (rh + gap) + 150 + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "금메달 뒤 개막 세 경기", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "수원 KT · 2026-27 프로농구", 38, "Bold", SUB, "mm")
    lw = 400
    sw = (W - 2 * M - lw) / 3
    sx = [M + lw + sw * (k + 0.5) for k in range(3)]
    for k, lab in enumerate(["득점", "리바운드", "3점"]):
        text(d, (sx[k], 284), lab, 34, "Bold", BURG, "mm")
    y = y0
    for gi, (when, opp, res, pts, reb, three) in enumerate(games):
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + 58), when, 32, "Bold", SUB, "lm")
        text(d, (M + 40, y + 116), opp, 46, "Black", INK, "lm")
        text(d, (M + 40 + d.textlength(opp, font=font(46, "Black")) + 18, y + 120), res, 28, "Bold", SUB, "lm")
        for k, v in enumerate((pts, reb, three)):
            col = ORANGE if (gi, k + 3) in hi else INK
            text(d, (sx[k], y + rh / 2), str(v), 76, "Black", col, "mm")
        y += rh + gap
    box(d, M, y, W - M, y + 132, fill=CARD, edge=EDGE)
    text(d, (M + 40, y + 46), "지난 시즌 평균", 32, "Bold", SUB, "lm")
    text(d, (M + 40, y + 96), "7.9점 · 5.5리바운드 · 3점 성공률 24.6%", 38, "Bold", INK, "lm")
    y += 132 + 58
    footer(d, y, "리바운드도 잡고, 3점도 넣었다")
    note(d, y + 112 + 44, "기록: KBL 공식 홈페이지 선수 경기별 기록 (2026년 10월 10일) · 3점은 성공/시도")
    save(im, "bk_mjh_04_opening.png")


if __name__ == "__main__":
    for f in (card_01, card_02, card_03, card_04): f()
