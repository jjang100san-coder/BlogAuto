# -*- coding: utf-8 -*-
r"""블로그연대기 「애드포스트 세금·정산·지급일」 카드 4장.
- 내용은 전부 애드포스트·네이버페이 고객센터 문서(2026-10-11 수집, base data\) 그대로. 계산한 숫자 없음 (마스터 0-4).
- 색: 1·2·4편 파랑/빨강, 3편 판정색, 5편 청록/주황과 겹치지 않게 보라·겨자 (마스터 5-4).
- 첫 이미지(썸네일)는 AI 장면이라 카드는 2번째부터 (마스터 5-4)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BG, INK, SUB, LINE = (251, 251, 249), (17, 17, 17), (95, 95, 95), (222, 222, 222)
PURPLE, MUSTARD, GRAY = (102, 72, 170), (204, 146, 20), (178, 182, 186)
PURPLE_L, MUSTARD_L = (236, 231, 248), (250, 240, 214)
W = 1080

def f(size, w="Black"):
    ft = ImageFont.truetype(FONT, size); ft.set_variation_by_name(w); return ft

def canvas(h=W):
    im = Image.new("RGB", (W, h), BG); return im, ImageDraw.Draw(im)

def save(im, name):
    im.save(os.path.join(HERE, name), optimize=True); print("saved", name, im.size)

def foot(d, text):
    d.text((70, 1010), text, font=f(30, "Medium"), fill=SUB)

# ① 받는 두 길
def card_two_ways():
    im, d = canvas()
    d.text((70, 60), "애드포스트 수익 받는 두 길", font=f(64), fill=INK)
    cols = [("은행 계좌", PURPLE, PURPLE_L, ["매달 25일", "5만 원부터", "쌓인 금액 전부"]),
            ("네이버페이 머니", MUSTARD, MUSTARD_L, ["신청한 다음 달 12일", "100원부터", "한 번에 최대 5만 원"])]
    labels = ["언제", "얼마부터", "한 번에"]
    x0s = [70, 560]
    for (name, col, light, vals), x0 in zip(cols, x0s):
        d.rounded_rectangle([x0, 190, x0 + 450, 300], 22, fill=col)
        d.text((x0 + 225, 245), name, font=f(48), fill=(255, 255, 255), anchor="mm")
        for i, (lab, v) in enumerate(zip(labels, vals)):
            y = 330 + i * 180
            d.rounded_rectangle([x0, y, x0 + 450, y + 155], 20, fill=light)
            d.text((x0 + 30, y + 22), lab, font=f(32, "Bold"), fill=SUB)
            d.text((x0 + 30, y + 72), v, font=f(46), fill=INK)
    d.rounded_rectangle([70, 885, W - 70, 975], 20, outline=INK, width=4)
    d.text((W // 2, 930), "세금은 두 길을 합쳐서 계산", font=f(44), fill=INK, anchor="mm")
    foot(d, "애드포스트 고객센터 문서 기준 · 개인회원 · 2026.10.11 확인")
    save(im, "card1_two_ways.png")

# ② 12만 5천 원 넘는 달
def card_threshold():
    im, d = canvas()
    d.text((70, 60), "1년 합계 12만 5천 원", font=f(66), fill=INK)
    d.text((70, 150), "넘는 달에 생기는 일", font=f(50, "Bold"), fill=SUB)
    L, R, B = 110, W - 90, 760
    # 쌓여 가는 받은 돈 (계단) — 모양만, 숫자 없음
    steps = [0.12, 0.24, 0.36, 0.48, 0.62, 0.78, 0.9, 1.0]
    n = len(steps); bw = (R - L) / n
    TH = 0.55  # 기준선 높이(그림 비율)
    cross = next(i for i, s in enumerate(steps) if s > TH)
    top = 300
    for i, s in enumerate(steps):
        x = L + i * bw
        h = (B - top) * s
        col = GRAY if i < cross else (MUSTARD if i == cross else PURPLE)
        d.rectangle([x + 10, B - h, x + bw - 10, B], fill=col)
    ty = B - (B - top) * TH
    for x in range(L, R, 28):
        d.line([x, ty, x + 16, ty], fill=INK, width=4)
    d.text((L, ty - 52), "연간 합계 12만 5천 원", font=f(34, "Bold"), fill=INK)
    d.line([L, B, R, B], fill=INK, width=3)
    d.text((L, B + 18), "1월", font=f(34, "Bold"), fill=SUB)
    d.text((R, B + 18), "12월", font=f(34, "Bold"), fill=SUB, anchor="ra")
    cx = L + cross * bw + bw / 2
    d.text((cx, B + 18), "넘는 달", font=f(36), fill=MUSTARD, anchor="ma")
    rows = [(GRAY, "넘기 전", "세금 없이 받음"),
            (MUSTARD, "넘는 달", "1월부터 받은 돈의 세금 8.8%를 한꺼번에"),
            (PURPLE, "그 뒤", "그달 받는 돈의 세금만")]
    y = 850
    for col, a, b in rows:
        d.rounded_rectangle([70, y + 8, 106, y + 44], 8, fill=col)
        d.text((124, y), a, font=f(36), fill=INK)
        d.text((300, y + 4), b, font=f(34, "Medium"), fill=INK)
        y += 52
    save(im, "card2_threshold.png")

# ③ 한 달 일정 (개인회원)
def card_calendar():
    im, d = canvas()
    d.text((70, 60), "개인회원 한 달 일정", font=f(66), fill=INK)
    d.text((70, 150), "지난달 말일까지 쌓인 돈 기준", font=f(40, "Bold"), fill=SUB)
    cell, gap, x0, y0 = 128, 10, 70, 230
    marks = {}
    for dd in range(1, 6): marks[dd] = MUSTARD
    marks[12] = PURPLE
    marks[25] = PURPLE
    for dd in range(26, 32): marks[dd] = GRAY
    for dd in range(1, 32):
        r, c = divmod(dd - 1, 7)
        x, y = x0 + c * (cell + gap), y0 + r * (cell * 0.72 + gap)
        col = marks.get(dd)
        fill = col if col else (240, 240, 237)
        d.rounded_rectangle([x, y, x + cell, y + cell * 0.72], 14, fill=fill)
        d.text((x + cell / 2, y + cell * 0.36), str(dd), font=f(40), fill=(255, 255, 255) if col else SUB, anchor="mm")
    y = 740
    legend = [(MUSTARD, "1일~5일 18시", "처음 받는 사람 주민등록번호 입력"),
              (PURPLE, "12일", "페이머니 전환 (지난달 신청분)"),
              (PURPLE, "25일", "계좌 지급 · 휴일이면 바뀜"),
              (GRAY, "26일~말일", "계좌번호 바꿀 수 있음")]
    for col, a, b in legend:
        d.rounded_rectangle([70, y + 8, 106, y + 44], 8, fill=col)
        d.text((124, y), a, font=f(34), fill=INK)
        d.text((360, y + 3), b, font=f(33, "Medium"), fill=INK)
        y += 58
    foot(d, "1일 0시~13시는 정산 중이라 지급 정보 못 바꿈 · 고객센터 문서 기준")
    save(im, "card3_calendar.png")

# ④ 5월 두 길
def card_may():
    im, d = canvas()
    d.text((70, 60), "5월 종합소득세 때", font=f(66), fill=INK)
    d.text((70, 150), "애드포스트 기타소득은", font=f(48, "Bold"), fill=SUB)
    d.rounded_rectangle([140, 250, W - 140, 380], 24, fill=INK)
    d.text((W // 2, 293), "기타소득금액", font=f(48), fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 345), "받은 돈에서 필요경비를 뺀 금액", font=f(32, "Medium"), fill=(220, 220, 220), anchor="mm")
    # 갈래
    d.line([W // 2, 380, W // 2, 430], fill=INK, width=5)
    d.line([290, 430, W - 290, 430], fill=INK, width=5)
    for x in (290, W - 290):
        d.line([x, 430, x, 480], fill=INK, width=5)
    boxes = [(70, PURPLE, PURPLE_L, "1년 300만 원 이하", ["고를 수 있음", "떼인 세금으로 끝", "또는 합쳐서 신고"]),
             (560, MUSTARD, MUSTARD_L, "1년 300만 원 초과", ["다른 소득과", "합쳐서 신고", ""])]
    for x0, col, light, head, lines in boxes:
        d.rounded_rectangle([x0, 480, x0 + 450, 580], 20, fill=col)
        d.text((x0 + 225, 530), head, font=f(40), fill=(255, 255, 255), anchor="mm")
        d.rounded_rectangle([x0, 600, x0 + 450, 880], 20, fill=light)
        for i, t in enumerate(lines):
            d.text((x0 + 225, 655 + i * 75), t, font=f(42 if i == 0 else 38, "Black" if i == 0 else "Bold"), fill=INK, anchor="mm")
    d.text((70, 920), "원천징수영수증: 애드포스트 사이트 · 홈택스 지급명세서 등 제출내역", font=f(30, "Bold"), fill=INK)
    foot(d, "세법 일반 내용 · 유리한 쪽은 다른 소득에 따라 달라짐")
    save(im, "card4_may.png")

if __name__ == "__main__":
    card_two_ways(); card_threshold(); card_calendar(); card_may()
