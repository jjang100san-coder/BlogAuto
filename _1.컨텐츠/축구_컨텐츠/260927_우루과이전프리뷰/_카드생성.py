# -*- coding: utf-8 -*-
"""우루과이전 프리뷰 카드 6장 생성.

기존 글(에콰도르전·베트남전)의 카드 스타일을 그대로 따른다.
  - 다크 배경 + 상단 코럴 액센트 바
  - 행마다 왼쪽 컬러 바, 오른쪽 배지
  - 맨 아래 한 줄 요약
중계 화면 캡처나 선수 사진은 쓰지 않는다. 텍스트와 도형만으로 만든다(저작권).
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "uruguay-preview", "images")
FB = "C:/Windows/Fonts/malgunbd.ttf"
FR = "C:/Windows/Fonts/malgun.ttf"

W = 1200
PAD = 70
BG = (26, 24, 24)
ACCENT = (232, 115, 90)
ROW = (43, 40, 40)
PILL = (58, 53, 53)
WHITE = (255, 255, 255)
SUB = (138, 128, 128)
GREEN = (99, 201, 138)
YELLOW = (239, 194, 92)
GRAY = (160, 149, 149)
BLUE = (109, 168, 224)


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, font):
    return d.textbbox((0, 0), text, font=font)[2]


def card(name, title, subtitle, rows, footer, foot_color=ACCENT):
    """rows = [(왼쪽 바 색, 본문, 배지문구 또는 None, 배지색)]"""
    f_title = F(FB, 46)
    f_sub = F(FR, 24)
    f_body = F(FB, 30)
    f_pill = F(FB, 25)
    f_foot = F(FB, 30)

    row_h, gap = 92, 16
    head = 40 + 56 + (42 if subtitle else 10)
    body_h = len(rows) * row_h + (len(rows) - 1) * gap
    h = head + body_h + 36 + 82 + 40

    img = Image.new("RGB", (W, h), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=ACCENT)

    y = 40
    d.text(((W - tw(d, title, f_title)) // 2, y), title, font=f_title, fill=WHITE)
    y += 60
    if subtitle:
        d.text(((W - tw(d, subtitle, f_sub)) // 2, y), subtitle, font=f_sub, fill=SUB)
        y += 46
    else:
        y += 14

    for bar, text, badge, bcol in rows:
        d.rounded_rectangle([PAD, y, W - PAD, y + row_h], radius=14, fill=ROW)
        d.rounded_rectangle([PAD, y + 8, PAD + 7, y + row_h - 8], radius=4, fill=bar)
        d.text((PAD + 36, y + (row_h - 38) // 2), text, font=f_body, fill=WHITE)
        if badge:
            bw = tw(d, badge, f_pill) + 52
            bx = W - PAD - 24 - bw
            d.rounded_rectangle([bx, y + 22, bx + bw, y + row_h - 22], radius=11, fill=PILL)
            d.text((bx + 26, y + (row_h - 32) // 2), badge, font=f_pill, fill=bcol)
        y += row_h + gap

    y += 20
    d.rounded_rectangle([PAD, y, W - PAD, y + 82], radius=14, fill=ROW)
    d.text(((W - tw(d, footer, f_foot)) // 2, y + 24), footer, font=f_foot, fill=foot_color)

    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, name))
    return name, img.size


def flow(name, title, subtitle, steps, footer):
    """세로 흐름도. steps = [(문구, 색)]"""
    f_title = F(FB, 46)
    f_sub = F(FR, 24)
    f_body = F(FB, 29)
    f_foot = F(FB, 30)

    box_h, arrow = 78, 34
    head = 40 + 56 + 42
    h = head + len(steps) * box_h + (len(steps) - 1) * arrow + 36 + 82 + 40

    img = Image.new("RGB", (W, h), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=ACCENT)

    y = 40
    d.text(((W - tw(d, title, f_title)) // 2, y), title, font=f_title, fill=WHITE)
    y += 60
    d.text(((W - tw(d, subtitle, f_sub)) // 2, y), subtitle, font=f_sub, fill=SUB)
    y += 46

    bw = W - PAD * 2 - 120
    bx = (W - bw) // 2
    for i, (text, col) in enumerate(steps):
        d.rounded_rectangle([bx, y, bx + bw, y + box_h], radius=14, fill=ROW)
        d.rounded_rectangle([bx, y + 8, bx + 7, y + box_h - 8], radius=4, fill=col)
        d.text((bx + 34, y + (box_h - 37) // 2), text, font=f_body, fill=WHITE)
        y += box_h
        if i < len(steps) - 1:
            cx = W // 2
            d.line([cx, y + 6, cx, y + arrow - 12], fill=SUB, width=3)
            d.polygon([(cx - 8, y + arrow - 14), (cx + 8, y + arrow - 14),
                       (cx, y + arrow - 3)], fill=SUB)
            y += arrow

    y += 36
    d.rounded_rectangle([PAD, y, W - PAD, y + 82], radius=14, fill=ROW)
    d.text(((W - tw(d, footer, f_foot)) // 2, y + 24), footer, font=f_foot, fill=ACCENT)

    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, name))
    return name, img.size


made = []

made.append(card(
    "01_preview_card.png",
    "한국 vs 우루과이",
    "9월 28일(월) 저녁 8시 · 서울월드컵경기장",
    [(BLUE, "9~10월 A매치 4연전 두 번째 경기", None, None),
     (BLUE, "FIFA 랭킹", "한국 32위 · 우루과이 20위", WHITE),
     (YELLOW, "역대 전적", "10경기 1승 2무 7패", YELLOW),
     (GREEN, "우루과이 직전 경기", "일본에 1-3 패", GREEN)],
    "일본전에서 약점 세 개가 보였다"))

made.append(card(
    "02_uruguay_now.png",
    "우루과이는 지금 이런 상태다",
    "이름값과 최근 성적이 따로 논다",
    [(YELLOW, "작년 11월 이후", "8경기 무승", YELLOW),
     (YELLOW, "2026년 성적", "6경기 4무 2패", YELLOW),
     (YELLOW, "북중미 월드컵", "조별 3위 · 32강 탈락", YELLOW),
     (GRAY, "감독", "임시 체제", GRAY),
     (GRAY, "결장", "발베르데 · 우가르테 외", GRAY)],
    "남미 3위라는 이름값을 못 따라가고 있다"))

made.append(card(
    "03_three_weaknesses.png",
    "일본전에서 드러난 약점 셋",
    "일본 분석 채널과 우루과이 현지 매체에서 각각 나온 지적",
    [(GREEN, "중원 핵심이 내려가면 그 자리가 빈다", "일본 분석", GREEN),
     (GREEN, "두 공격수가 골대를 등지고 있었다", "우루과이 매체", YELLOW),
     (GREEN, "수비가 한쪽으로 몰아가지 못한다", "일본 분석", GREEN)],
    "셋이 따로가 아니라 한 줄로 이어진다"))

made.append(flow(
    "04_cycle.png",
    "약점 셋이 이어지는 방식",
    "일본전 90분 동안 반복된 흐름",
    [("중원 핵심이 수비 라인까지 내려온다", YELLOW),
     ("그가 있어야 할 중원 자리가 빈다", YELLOW),
     ("길게 차서 두 공격수에게 붙인다", YELLOW),
     ("등지고 받으니 앞으로 나아가지 못한다", YELLOW),
     ("안으로 볼이 안 가니 멀리서 때린다", ACCENT),
     ("빈 중원에서 상대가 그대로 주워 간다", ACCENT)],
    "이 고리를 끊지 못해 여덟 경기를 이기지 못했다"))

made.append(card(
    "05_korea_changes.png",
    "한국은 무엇이 달라지나",
    "에콰도르전과 비교해서",
    [(GREEN, "이강인 복귀", "본인이 출전 가능 언급", GREEN),
     (YELLOW, "황인범은 당일 확인", "몸 상태 더 필요", YELLOW),
     (ACCENT, "조규성 소집 해제", "대체 발탁 없음", ACCENT),
     (BLUE, "상대 발베르데 결장", "발목 인대 손상", BLUE)],
    "모레노 : 선수는 소속팀에서 뛰던 자리에서 뛴다"))

made.append(card(
    "06_watchpoints.png",
    "경기 끝나고 채점할 세 가지",
    "미리 적어두고 90분 뒤에 맞춰본다",
    [(BLUE, "앞쪽을 얼마나 바꿨나", "라인업", BLUE),
     (BLUE, "빈 중원을 우리가 주워 왔는가", "경기 내내", BLUE),
     (BLUE, "세트피스로 한 골 내줬는가", "실점 형태", BLUE)],
    "첫 번째 답은 라인업이 뜨는 순간 나온다"))

for n, sz in made:
    print("%s  %dx%d" % (n, sz[0], sz[1]))
