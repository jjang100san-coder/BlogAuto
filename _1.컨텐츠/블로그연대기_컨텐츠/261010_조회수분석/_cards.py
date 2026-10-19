# -*- coding: utf-8 -*-
"""블로그연대기 5편(조회수 분석) 카드 3장. 숫자는 전부 블로그 통계 화면 값 그대로(마스터 0-4, 계산값 없음).
- 검색 유입 화면의 검색어 이름은 넣지 않는다(작업 메모 🚫 — 비공개 전략이 드러난다). 개수만.
- 색: 1·2·4편 파랑/빨강, 3편 판정색과 겹치지 않게 청록·주황 (마스터 5-4).
- 첫 이미지(썸네일)는 AI 장면이라 이 카드들은 2번째부터 들어간다 (마스터 5-4, 2026.10.9)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BG, INK, SUB, LINE = (251, 251, 249), (17, 17, 17), (95, 95, 95), (222, 222, 222)
TEAL, ORANGE, GRAY = (14, 138, 122), (232, 124, 36), (178, 182, 186)
W = 1080

def f(size, w="Black"):
    ft = ImageFont.truetype(FONT, size); ft.set_variation_by_name(w); return ft

def canvas(h=W):
    im = Image.new("RGB", (W, h), BG); return im, ImageDraw.Draw(im)

def save(im, name):
    im.save(os.path.join(HERE, name), optimize=True); print("saved", name, im.size)

# ① 검색 유입 vs 사이트 유입 — 유입분석 [검색 유입]·[사이트 유입] 탭 상단 값
def card_split():
    im, d = canvas()
    d.text((70, 60), "어디로 들어왔나", font=f(74), fill=INK)
    rows = [("9월 한 달", 16.88, 83.08), ("9월 28일 ~ 10월 4일", 29.24, 70.72)]
    y = 250
    for label, s, t in rows:
        d.text((70, y), label, font=f(46, "Bold"), fill=SUB)
        x0, x1, top = 70, W - 70, y + 80
        mid = x0 + (x1 - x0) * s / 100
        d.rectangle([x0, top, mid, top + 150], fill=ORANGE)
        d.rectangle([mid, top, x1, top + 150], fill=TEAL)
        d.text((x0 + 10, top + 175), f"검색 {s}%", font=f(48), fill=ORANGE)
        d.text((x1, top + 175), f"사이트 {t}%", font=f(48), fill=TEAL, anchor="ra")
        y += 360
    d.text((70, 990), "블로그 통계 유입분석 화면 값 그대로", font=f(32, "Medium"), fill=SUB)
    save(im, "card1_search_vs_site.png")

# ② 검색 유입 상위 검색어 — 분야 개수만 (이름 없음)
def card_top20():
    im, d = canvas()
    d.text((70, 60), "검색으로 들어온 말", font=f(70), fill=INK)
    d.text((70, 155), "9월 상위 20개", font=f(46, "Bold"), fill=SUB)
    cell, gap, x0, y0 = 128, 18, 70, 250
    for i in range(20):
        r, c = divmod(i, 5)
        x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
        d.rounded_rectangle([x, y, x + cell, y + cell], 18, fill=ORANGE if i < 16 else GRAY)
    yl = y0 + 4 * (cell + gap) + 30
    d.rounded_rectangle([70, yl + 10, 114, yl + 54], 10, fill=ORANGE)
    d.text((132, yl), "축구 16", font=f(50), fill=INK)
    d.rounded_rectangle([420, yl + 10, 464, yl + 54], 10, fill=GRAY)
    d.text((482, yl), "그 밖 4", font=f(50), fill=INK)
    d.text((70, yl + 95), "9월 28일 주간은 상위 19개 중 축구 12개", font=f(38, "Bold"), fill=SUB)
    save(im, "card2_top20_football.png")

# ③ 하루 조회수 8/24~10/9 — 엑셀(블로그 통계 조회수 일간) 값 그대로
def card_daily():
    data = json.load(open(os.path.join(HERE, "base data", "daily_views_0712_1009.json"), encoding="utf-8"))
    data = [(dd, v) for dd, w, v in data if dd >= "2026-08-24"]
    im, d = canvas()
    d.text((70, 60), "하루 조회수", font=f(74), fill=INK)
    d.text((70, 160), "8월 24일 ~ 10월 9일", font=f(42, "Bold"), fill=SUB)
    L, R, T, B = 90, W - 60, 300, 930
    vmax = 1000
    d.line([L, B, R, B], fill=LINE, width=3)
    n = len(data)
    pts = [(L + (R - L) * i / (n - 1), B - (B - T) * v / vmax) for i, (dd, v) in enumerate(data)]
    d.polygon(pts + [(R, B), (L, B)], fill=(214, 238, 234))
    d.line(pts, fill=TEAL, width=7, joint="curve")
    idx = {dd: i for i, (dd, v) in enumerate(data)}
    marks = [("2026-09-16", "9/16", ORANGE, "축구 글 없는 날"), ("2026-09-28", "9/28", INK, ""), ("2026-10-06", "10/6", INK, "")]
    for dd, lab, col, note in marks:
        x, y = pts[idx[dd]]; v = data[idx[dd]][1]
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col, outline=BG, width=4)
        d.text((x, y - 30), f"{lab} {v}", font=f(40), fill=col, anchor="ms")
        if note: d.text((x, y - 80), note, font=f(32, "Bold"), fill=col, anchor="ms")
    for dd, lab in [("2026-09-01", "9월"), ("2026-10-01", "10월")]:
        x = pts[idx[dd]][0]; d.text((x, B + 50), lab, font=f(44, "Bold"), fill=SUB, anchor="ms")
    d.text((70, 1035), "블로그 통계 조회수 일간 내보내기 값", font=f(30, "Medium"), fill=SUB)
    save(im, "card3_daily_views.png")

if __name__ == "__main__":
    card_split(); card_top20(); card_daily()
