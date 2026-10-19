# -*- coding: utf-8 -*-
r"""광진구 횟집 후기 775편 측정 카드 4장 (2026-10-15).
- 숫자는 전부 _analyze_gj.py 집계(base data\gj_analysis_20261015.json) 그대로, 계산한 숫자 없음(마스터 0-4).
- 가게·블로거 이름 없음. 색은 앞 편들과 겹치지 않게 짙은 바다색·산호색(마스터 5-4). 카드는 2번째 이미지부터."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BG, INK, SUB = (251, 251, 249), (17, 17, 17), (95, 95, 95)
SEA, CORAL, GRAY = (22, 86, 128), (226, 104, 84), (178, 182, 186)
SEA_L, CORAL_L = (224, 236, 245), (251, 230, 225)
W = 1080

def f(size, w="Black"):
    ft = ImageFont.truetype(FONT, size); ft.set_variation_by_name(w); return ft
def canvas():
    im = Image.new("RGB", (W, W), BG); return im, ImageDraw.Draw(im)
def save(im, n): im.save(os.path.join(HERE, n), optimize=True); print("saved", n)
def foot(d, t): d.text((70, 1012), t, font=f(29, "Medium"), fill=SUB)

def card_split():
    im, d = canvas()
    d.text((70, 60), "광진구 횟집 후기 775편", font=f(66), fill=INK)
    d.text((70, 150), "본문을 열어 표기를 확인했다", font=f(42, "Bold"), fill=SUB)
    rows = [("표기 없음", 534, GRAY), ("체험단·협찬 고지", 137, CORAL), ("내돈내산 표기", 99, SEA), ("그 밖(수수료 고지 3·업체 글 2)", 5, (210, 210, 205))]
    y = 270; vmax = 534
    for lab, v, col in rows:
        d.text((70, y), lab, font=f(40, "Bold"), fill=INK)
        w = (W - 140) * v / vmax
        d.rounded_rectangle([70, y + 60, 70 + max(w, 30), y + 140], 16, fill=col)
        d.text((70 + max(w, 30) + 20 if w < 700 else 70 + w - 20, y + 100), f"{v}", font=f(48), fill=INK if w < 700 else (255, 255, 255), anchor="lm" if w < 700 else "rm")
        y += 175
    foot(d, "레이더 후기 찾기와 같은 판정 규칙 · 2026.10.15 · 본문 200자 이상")
    save(im, "card1_split.png")

def card_signals():
    im, d = canvas()
    d.text((70, 60), "체험단 글에 늘 붙어 있던 것", font=f(60), fill=INK)
    d.text((70, 145), "네이버 블로그 글 기준", font=f(40, "Bold"), fill=SUB)
    hdr = ["", "체험단·협찬", "내돈내산", "표기 없음"]
    rows = [("영상", "96 / 137", "28 / 96", "204 / 513"), ("지도", "136 / 137", "88 / 96", "455 / 513"), ("사진 중앙값", "28장", "17장", "24장")]
    xs = [70, 400, 640, 860]
    y = 250
    for x, h in zip(xs, hdr):
        if h: d.text((x, y), h, font=f(34, "Bold"), fill=CORAL if h == "체험단·협찬" else (SEA if h == "내돈내산" else SUB))
    y += 70
    for r in rows:
        d.rounded_rectangle([60, y - 12, W - 60, y + 92], 18, fill=(242, 242, 238))
        d.text((xs[0] + 10, y + 18), r[0], font=f(42), fill=INK)
        for x, v, col in zip(xs[1:], r[1:], (CORAL, SEA, SUB)):
            d.text((x, y + 22), v, font=f(40, "Black" if col == CORAL else "Bold"), fill=col)
        y += 130
    d.text((70, 800), "영상·지도에 사진도 더 많이 —", font=f(40, "Bold"), fill=INK)
    d.text((70, 860), "체험단 글은 이 세트를 거의 다 갖췄다", font=f(40, "Bold"), fill=INK)
    foot(d, "분모는 각 묶음의 네이버 블로그 글 수 · 2026.10.15")
    save(im, "card2_signals.png")

def card_wait():
    im, d = canvas()
    d.text((70, 60), "기다린 시간을 숫자로 쓴 글", font=f(60), fill=INK)
    d.text((70, 145), "「대기 ○분」「○팀 기다림」", font=f(40, "Bold"), fill=SUB)
    rows = [("체험단·협찬", 0, 137, CORAL), ("내돈내산", 5, 99, SEA), ("표기 없음", 24, 534, GRAY)]
    y = 300
    for lab, v, n, col in rows:
        d.rounded_rectangle([70, y, W - 70, y + 170], 26, fill=CORAL_L if col == CORAL else (SEA_L if col == SEA else (238, 238, 234)))
        d.text((110, y + 40), lab, font=f(44, "Bold"), fill=INK)
        d.text((110, y + 100), f"{n}편 중", font=f(32, "Bold"), fill=SUB)
        d.text((W - 110, y + 85), f"{v}편", font=f(84), fill=col, anchor="rm")
        y += 205
    foot(d, "본문 문장에서 「대기·웨이팅 + 숫자 + 분·팀」을 찾음 · 2026.10.15")
    save(im, "card3_wait.png")

def card_disclosure():
    im, d = canvas()
    d.text((70, 60), "대가 표시는 어디에 있었나", font=f(60), fill=INK)
    d.text((70, 145), "체험단·협찬 137편", font=f(40, "Bold"), fill=SUB)
    rows = [("제목", 0), ("본문 첫 부분", 16), ("본문 중간", 7), ("본문 끝", 8), ("글자엔 없고 배너 그림만", 106)]
    y = 250; vmax = 106
    for lab, v in rows:
        d.text((70, y + 10), lab, font=f(38, "Bold"), fill=INK)
        w = 430 * v / vmax
        d.rounded_rectangle([480, y, 480 + max(w, 8), y + 70], 14, fill=CORAL if v else GRAY)
        d.text((480 + max(w, 8) + 18, y + 35), f"{v}", font=f(44), fill=INK, anchor="lm")
        y += 115
    d.text((70, 845), "공정위 지침(2024 개정): 제목이나 첫 부분에", font=f(34, "Bold"), fill=INK)
    foot(d, "본문 글자에서 협찬·제공받음·원고료 문구 위치를 찾음 · 2026.10.15")
    save(im, "card4_disclosure.png")

if __name__ == "__main__":
    card_split(); card_signals(); card_wait(); card_disclosure()
