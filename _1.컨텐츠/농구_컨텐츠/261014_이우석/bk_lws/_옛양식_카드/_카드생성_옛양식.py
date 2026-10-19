# -*- coding: utf-8 -*-
"""금메달 시리즈 6편(이우석) 자체 제작 카드 01~04.
영상 프레임은 한 장도 쓰지 않는다(마스터지침 6-7). 숫자는 종합분석_이우석.md · base data\프로필_KBL확인_이우석.md · 2차수집_이우석.md 그대로.
판형은 2·3편과 같다: 폭 1200 · 크림 배경 · 상단 띠 · 흰 둥근 칸 · 하단 결론 박스.
색만 3편 버건디 → 올리브로 바꾼다(지침 5-4 시리즈 색 분리). 주황 강조는 시리즈 공통.
썸네일은 AI 장면(bk_lws_ai_01)이라 카드는 전부 본문용이다(지침 5-4)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
W = 1200
BG, CARD, EDGE = "#F7F5EC", "#FFFFFF", "#E2E0CF"
INK, SUB, MUTE = "#1F231C", "#7D8070", "#ABAE9C"
OLIVE, PALE, PALE_EDGE = "#4E5F2C", "#EBEFDD", "#D3DABD"
ORANGE = "#E2622B"
M = 64

def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def text(d, xy, s, size, weight="Bold", fill=INK, anchor="la"):
    d.text(xy, s, font=font(size, weight), fill=fill, anchor=anchor)

def canvas(h):
    im = Image.new("RGB", (W, h), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=OLIVE)
    return im, d

def box(d, x0, y0, x1, y1, fill=CARD, edge=EDGE, r=18):
    d.rounded_rectangle([x0, y0, x1, y1], r, fill=fill, outline=edge, width=2)

def footer(d, y, s, h=112):
    box(d, M, y, W - M, y + h, fill=PALE, edge=PALE_EDGE)
    text(d, (W / 2, y + h / 2), s, 40, "Bold", OLIVE, "mm")

def note(d, y, s):
    text(d, (W / 2, y), s, 24, "Medium", MUTE, "mm")

def save(im, name):
    p = os.path.join(OUT, name); im.save(p, optimize=True); print("saved", name, im.size)


# 01 · 네임카드 — KBL 공식 프로필
def card_01():
    rows = [
        ("소속", "울산 현대모비스 · 등번호 11"),
        ("포지션", "가드"),
        ("생년월일", "1999년 7월 10일"),
        ("키", "196cm"),
        ("출신 학교", "고려대"),
        ("드래프트", "2020년 1라운드 3순위"),
        ("신인상", "2021-22 시즌, 데뷔 2년 차에"),
        ("병역", "2025년 5월 상무 입대 → 9월 말 조기 전역"),
    ]
    rh, gap, y0 = 96, 14, 352
    h = y0 + len(rows) * (rh + gap) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 98), "금메달 시리즈 6", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 196), "이우석", 120, "Black", INK, "mm")
    text(d, (W / 2, 284), "2026 아시안게임 금메달", 40, "Bold", OLIVE, "mm")
    y = y0
    for k, v in rows:
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + rh / 2), k, 36, "Bold", ORANGE if k == "소속" else OLIVE, "lm")
        text(d, (M + 250, y + rh / 2), v, 36 if len(v) > 18 else 38, "Bold", INK, "lm")
        y += rh + gap
    y += 26
    footer(d, y, "군인 신분으로 딴 금메달")
    note(d, y + 112 + 44, "프로필·기록: KBL 공식 홈페이지 (2026년 10월 16일) · 입대·전역: 점프볼·구단 발표")
    save(im, "bk_lws_01_namecard.png")


# 02 · 입대에서 전역까지 — 세로 타임라인. 퇴장은 사실만, 판정 평가 없음
def card_02():
    items = [   # (종류, 날짜, 무엇, 덧붙임)
        ("in",  "2025년 5월 19일", "상무 입대", "전날 「이룬 업적은 없잖아요」"),
        ("out", "2026년 9월 13일", "조별 일본전 3쿼터 퇴장", "100-83 승"),
        ("key", "9월 18일", "4강 이란전 19점", "77-51 · 결승행"),
        ("key", "9월 20일", "결승 일본전 금메달", "67-57"),
        ("in",  "9월 말", "조기 전역", "원래 11월 18일"),
        ("in",  "10월 3일", "개막전 선발", "울산 현대모비스 11번"),
    ]
    hh, y0, gap = 160, 300, 20
    h = y0 + len(items) * hh + gap * (len(items) - 1) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "입대에서 전역까지", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "이우석 · 상무 신분으로 나간 아시안게임", 38, "Bold", SUB, "mm")
    text(d, (W / 2, 240), "입대 전날의 말에서 개막전 선발까지", 34, "Bold", MUTE, "mm")
    lx, bx = M + 26, M + 76
    ys, y = [], y0
    for kind, when, what, sub in items:
        box(d, bx, y, W - M, y + hh)
        col = {"in": OLIVE, "out": SUB, "key": ORANGE}[kind]
        text(d, (bx + 40, y + 48), when, 32, "Bold", col, "lm")
        text(d, (bx + 40, y + hh - 50), what, 42, "Black", SUB if kind == "out" else INK, "lm")
        text(d, (W - M - 40, y + 48), sub, 30, "Bold", col, "rm")
        ys.append((y + hh / 2, kind))
        y += hh + gap
    d.line([lx, ys[0][0], lx, ys[-1][0]], fill=OLIVE, width=6)
    for cy, kind in ys:
        r = 18
        col = {"in": OLIVE, "out": MUTE, "key": ORANGE}[kind]
        if kind == "out":
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=BG, outline=col, width=5)
        else:
            d.ellipse([lx - r, cy - r, lx + r, cy + r], fill=col)
    y += 18
    footer(d, y, "11월 전역이 9월이 됐다")
    note(d, y + 112 + 44, "입대: 점프볼(2025년 5월 18일 영상) · 경기: 기사·하이라이트 점수판 · 전역: 구단 발표·점프볼")
    save(im, "bk_lws_02_timeline.png")


# 03 · 금메달 뒤 바뀐 것 — 기사 수치 그대로, 계산한 숫자 없음
def card_03():
    rows = [   # (항목, 전, 후)
        ("전역", "2026년 11월 18일 예정", "9월 말"),
        ("연봉", "2억 9천만 원", "5억 9천만 원"),
        ("FA", "2028년", "2027년"),
    ]
    rh, gap, y0 = 150, 18, 330
    h = y0 + len(rows) * (rh + gap) + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "금메달 뒤 바뀐 것", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "이우석 · 2026-27 시즌 계약", 38, "Bold", SUB, "mm")
    lw = 210
    cw = (W - 2 * M - lw - 2 * 16) / 2
    cx = [M + lw + 16 + cw / 2, M + lw + 16 + cw + 16 + cw / 2]
    for i, lab in enumerate(["원래", "금메달 뒤"]):
        text(d, (cx[i], 280), lab, 34, "Bold", SUB if i == 0 else ORANGE, "mm")
    y = y0
    for k, a, b in rows:
        box(d, M, y, W - M, y + rh)
        text(d, (M + 36, y + rh / 2), k, 40, "Bold", OLIVE, "lm")
        text(d, (cx[0], y + rh / 2), a, 36, "Bold", SUB, "mm")
        text(d, (cx[1], y + rh / 2), b, 44, "Black", ORANGE, "mm")
        y += rh + gap
    y += 22
    footer(d, y, "전역도, 연봉도, FA도 앞당겨졌다")
    note(d, y + 112 + 44, "전역: 구단 발표(9월 28일자)·점프볼(9월 30일 전역 신고) · 연봉·FA: 구단 계약 발표 기사(10월 2일)")
    save(im, "bk_lws_03_changes.png")


# 04 · 금메달 뒤 개막 네 경기 — KBL 경기별 기록. 3점은 분수로
def card_04():
    games = [   # (날짜, 상대, 결과, 득점, 리바운드, 어시스트)
        ("10월 3일", "안양 정관장", "패 85-88", 9, 9, 4),
        ("10월 5일", "부산 KCC", "패 87-97", 16, 2, 5),
        ("10월 10일", "대구 한국가스공사", "패 75-81", 21, 5, 2),
        ("10월 12일", "원주 DB", "승 99-89", 15, 9, 6),
    ]
    hi = {(2, 3), (3, 5)}
    rh, gap, y0 = 168, 16, 330
    h = y0 + len(games) * (rh + gap) + 140 + 40 + 112 + 80
    im, d = canvas(h)
    text(d, (W / 2, 104), "금메달 뒤 개막 네 경기", 70, "Black", INK, "mm")
    text(d, (W / 2, 184), "울산 현대모비스 · 2026-27 프로농구", 38, "Bold", SUB, "mm")
    lw = 430
    sw = (W - 2 * M - lw) / 3
    sx = [M + lw + sw * (k + 0.5) for k in range(3)]
    for k, lab in enumerate(["득점", "리바운드", "어시스트"]):
        text(d, (sx[k], 284), lab, 32, "Bold", OLIVE, "mm")
    y = y0
    for gi, (when, opp, res, pts, reb, ast) in enumerate(games):
        box(d, M, y, W - M, y + rh)
        text(d, (M + 40, y + 54), when + " · " + res, 30, "Bold", SUB, "lm")
        text(d, (M + 40, y + 112), opp, 42 if len(opp) < 8 else 36, "Black", INK, "lm")
        for k, v in enumerate((pts, reb, ast)):
            col = ORANGE if (gi, k + 3) in hi else INK
            text(d, (sx[k], y + rh / 2), str(v), 72, "Black", col, "mm")
        y += rh + gap
    box(d, M, y, W - M, y + 124, fill=CARD, edge=EDGE)
    text(d, (M + 40, y + 44), "네 경기 평균", 30, "Bold", SUB, "lm")
    text(d, (M + 40, y + 90), "15.3점 · 6.3리바운드 · 4.3어시스트 · 출전 35분 26초", 34, "Bold", INK, "lm")
    y += 124 + 56
    footer(d, y, "네 번째 경기에서 팀 첫 승")
    note(d, y + 112 + 44, "기록: KBL 공식 홈페이지 선수 경기별 기록 (2026년 10월 16일)")
    save(im, "bk_lws_04_opening.png")


if __name__ == "__main__":
    for f in (card_01, card_02, card_03, card_04): f()
