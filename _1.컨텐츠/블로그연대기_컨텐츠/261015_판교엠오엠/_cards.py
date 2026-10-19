# -*- coding: utf-8 -*-
r"""판교 스키야키·샤브샤브 후기 측정 카드 6장 (2026-10-15).
- 숫자는 전부 base data\pg_analysis_20261015.json(_analyze_pg.py) + 광진 gj_analysis_20261015.json 그대로, 계산한 숫자 없음(마스터 0-4).
- 가게·블로거 이름 없음. 색은 광진 편(바다·산호)과 겹치지 않게 간장색·쑥색(마스터 5-4). 카드는 2번째 이미지부터."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BG, INK, SUB = (250, 249, 246), (17, 17, 17), (95, 95, 95)
SOY, MUGWORT, GRAY = (128, 74, 38), (78, 120, 70), (178, 180, 176)
SOY_L, MUG_L, GRAY_L = (243, 232, 222), (228, 238, 224), (238, 238, 234)
W = 1080

def f(size, w="Black"):
    ft = ImageFont.truetype(FONT, size); ft.set_variation_by_name(w); return ft
def canvas():
    im = Image.new("RGB", (W, W), BG); return im, ImageDraw.Draw(im)
def save(im, n): im.save(os.path.join(HERE, n), optimize=True); print("saved", n)
def foot(d, t): d.text((70, 1012), t, font=f(29, "Medium"), fill=SUB)

def card_split():
    im, d = canvas()
    d.text((70, 60), "판교 스키야키·샤브샤브 후기", font=f(60), fill=INK)
    d.text((70, 145), "1,622편 본문을 열어 표기를 확인했다", font=f(42, "Bold"), fill=SUB)
    rows = [("표기 없음", 1023, GRAY), ("체험단·협찬 고지", 428, SOY), ("내돈내산 표기", 164, MUGWORT), ("그 밖(수수료 고지 4·업체 글 3)", 7, (210, 210, 205))]
    y = 270; vmax = 1023
    for lab, v, col in rows:
        d.text((70, y), lab, font=f(40, "Bold"), fill=INK)
        w = (W - 140) * v / vmax
        d.rounded_rectangle([70, y + 60, 70 + max(w, 30), y + 140], 16, fill=col)
        inside = w >= 700
        d.text((70 + w - 20 if inside else 70 + max(w, 30) + 20, y + 100), f"{v:,}", font=f(48), fill=(255, 255, 255) if inside else INK, anchor="rm" if inside else "lm")
        y += 175
    foot(d, "「판교 샤브샤브」「판교 스키야키」 검색 결과 · 겹친 글 1편으로 · 2026.10.15")
    save(im, "card1_split.png")

def card_compare():
    im, d = canvas()
    d.text((70, 60), "광진구 횟집과 나란히 놓으면", font=f(58), fill=INK)
    d.text((70, 145), "같은 판정 규칙, 같은 날 측정", font=f(40, "Bold"), fill=SUB)
    hdr = ["", "광진구 횟집", "판교 스키야키·샤브"]
    rows = [("본문 연 글", "775편", "1,622편"), ("체험단·협찬", "137편", "428편"), ("내돈내산", "99편", "164편"), ("표기 없음", "534편", "1,023편"),
            ("체험단 글 중\n대기 ○분·○팀", "0편", "5편")]
    xs = [70, 470, 760]
    y = 245
    for x, h in zip(xs, hdr):
        if h: d.text((x, y), h, font=f(34, "Bold"), fill=SOY if "판교" in h else SUB)
    y += 70
    for i, r in enumerate(rows):
        hgt = 120 if "\n" in r[0] else 92
        d.rounded_rectangle([60, y - 10, W - 60, y + hgt - 10], 18, fill=SOY_L if i == 4 else (242, 242, 238))
        d.multiline_text((xs[0] + 10, y + 10), r[0], font=f(36, "Bold"), fill=INK, spacing=4)
        d.text((xs[1], y + 14), r[1], font=f(42, "Bold"), fill=SUB)
        d.text((xs[2], y + 14), r[2], font=f(42), fill=SOY)
        y += hgt + 18
    foot(d, "레이더 후기 찾기와 같은 판정 · 본문 200자 이상 · 2026.10.15")
    save(im, "card2_compare.png")

def card_tags():
    im, d = canvas()
    d.text((70, 60), "해시태그 다섯 개가 똑같은 글", font=f(58), fill=INK)
    d.text((70, 145), "앞 5개가 순서까지 같고, 쓴 블로거가 3명 이상", font=f(36, "Bold"), fill=SUB)
    rows = [("광진구 횟집 775편 중", 6, GRAY), ("토요일 낙지집 196편 중", 0, GRAY), ("판교 스키야키·샤브 1,622편 중", 25, MUGWORT), ("일요일 갈 집 292편 중", 81, SOY)]
    y = 250; vmax = 81
    for lab, v, col in rows:
        d.text((70, y), lab, font=f(38, "Bold"), fill=INK)
        w = 760 * v / vmax
        d.rounded_rectangle([70, y + 58, 70 + max(w, 14), y + 128], 14, fill=col)
        d.text((70 + max(w, 14) + 22, y + 93), f"{v}편", font=f(52), fill=col if col != GRAY else SUB, anchor="lm")
        y += 180
    foot(d, "본문 속 해시태그를 앞에서부터 다섯 개씩 비교 · 2026.10.15")
    save(im, "card3_tags.png")

def card_pubs():
    im, d = canvas()
    d.text((70, 60), "토요일 2차 후보 6곳의 후기", font=f(58), fill=INK)
    d.text((70, 145), "낙지집에서 500m 안 · 가게 이름이 본문에 나온 글", font=f(34, "Bold"), fill=SUB)
    hdr = ["", "글", "체험단", "내돈내산", "대기 숫자", "같은 태그"]
    rows = [("후보 1", 113, 36, 15, 3, 0), ("후보 2", 114, 0, 32, 25, 0), ("후보 3", 104, 4, 14, 0, 0),
            ("후보 4", 181, 33, 15, 0, 19), ("후보 5", 132, 0, 34, 28, 0), ("후보 6", 86, 35, 5, 6, 0)]
    xs = [80, 270, 410, 580, 760, 930]
    y = 240
    for x, h in zip(xs, hdr):
        if h: d.text((x, y), h, font=f(30, "Bold"), fill=SUB, anchor="ma" if x > 80 else "la")
    y += 60
    for r in rows:
        hi = r[2] == 0
        d.rounded_rectangle([60, y - 8, W - 60, y + 92], 16, fill=MUG_L if hi else (242, 242, 238))
        d.text((xs[0], y + 18), r[0], font=f(38), fill=INK)
        for x, v, i in zip(xs[1:], r[1:], range(5)):
            col = SOY if (i == 1 and v) else (MUGWORT if (i == 3 and v >= 20) else (SOY if (i == 4 and v) else INK))
            d.text((x, y + 20), str(v), font=f(40, "Black" if col != INK else "Bold"), fill=col, anchor="ma")
        y += 112
    foot(d, "대기 숫자 = 「대기 ○분·○팀」을 쓴 글 · 2026.10.15")
    save(im, "card6_pubs.png")

def card_blocks():
    im, d = canvas()
    d.text((70, 60), "내가 갈 집, 같은 해시태그 묶음 둘", font=f(54), fill=INK)
    d.text((70, 140), "가게 후기 292편 중", font=f(40, "Bold"), fill=SUB)
    blocks = [("2024년 12월 ~ 2025년 3월", "50편 · 블로거 49명", [("표기 없음", 49, GRAY), ("체험단 고지", 1, SOY)]),
              ("2024년 3월 13일 ~ 31일", "24편 · 블로거 24명", [("표기 없음", 15, GRAY), ("체험단 고지", 9, SOY)])]
    y = 240
    for when, size, parts in blocks:
        d.rounded_rectangle([60, y, W - 60, y + 330], 26, fill=(242, 242, 238))
        d.text((100, y + 32), when, font=f(40, "Bold"), fill=INK)
        d.text((100, y + 90), size, font=f(36, "Bold"), fill=SUB)
        x = 100; tot = sum(p[1] for p in parts); bw = W - 200
        for lab, v, col in parts:
            w = bw * v / tot
            d.rounded_rectangle([x, y + 160, x + w, y + 230], 10, fill=col)
            x += w
        x = 100
        for lab, v, col in parts:
            d.text((x, y + 250), f"{lab} {v}", font=f(36, "Black"), fill=col if col == SOY else SUB)
            x += 420
        y += 370
    foot(d, "체험단 고지는 본문 문구·배너로 판정 · 2026.10.15")
    save(im, "card4_blocks.png")

def card_months():
    im, d = canvas()
    d.text((70, 60), "내가 갈 집, 올해 달마다 쌓인 후기", font=f(54), fill=INK)
    d.text((70, 140), "2026년 1월 ~ 10월 15일", font=f(40, "Bold"), fill=SUB)
    m = [("1", 8), ("2", 1), ("3", 5), ("4", 3), ("5", 0), ("6", 1), ("7", 2), ("8", 39), ("9", 13), ("10", 1)]
    base = 880; top = 300; vmax = 39; bw = 70; gap = 22; x = 90
    for lab, v in m:
        h = (base - top) * v / vmax
        col = SOY if lab == "8" else GRAY
        if v: d.rounded_rectangle([x, base - h, x + bw, base], 10, fill=col)
        d.text((x + bw / 2, base - h - 14), str(v), font=f(38 if lab == "8" else 32), fill=col if lab == "8" else SUB, anchor="md")
        d.text((x + bw / 2, base + 22), f"{lab}월", font=f(32, "Bold"), fill=INK, anchor="ma")
        x += bw + gap
    foot(d, "8월 39편 중 표기 없음 35 · 체험단 고지 3 · 내돈내산 1 · 2026.10.15")
    save(im, "card5_months.png")

if __name__ == "__main__":
    card_split(); card_compare(); card_tags(); card_pubs(); card_blocks(); card_months()
