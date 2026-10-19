# -*- coding: utf-8 -*-
"""농구 네임카드 시안 3종(2026-10-17) — 축구 B 양식(팀 색 대각 면·각진 모서리·노란 띠)과 결을 달리한다.
농구 문법: 직선 대신 호·원(3점 라인·공), 팀 색 면 대신 시리즈 고정색(먹색 + 볼 오렌지 + 코트 라인 흰색), 강조는 둥근 오렌지 알약.
예시 값은 4편 변준형(KBL 10/16 확인값)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
COAL, COAL2 = (33, 30, 29), (52, 47, 44)
ORNG, ORNG_D = (234, 108, 38), (196, 82, 24)
LINE, WHITE, MUTE = (247, 242, 234), (255, 255, 255), (168, 158, 150)
GOLD = (214, 176, 72)

def F(size, w="Black"):
    f = ImageFont.truetype(FONT, int(size)); f.set_variation_by_name(w); return f

P = dict(kicker="금메달 시리즈 4 · 안양 정관장", num="5", unit="번", name="변준형", role="가드 · 동국대 · 2018 드래프트 2순위",
         rows=[("개막 다섯 경기", "12.2점 7.2어시스트"), ("보수 총액", "8억 원")], tag="군대를 먼저 다녀온 금메달",
         src="기록: KBL 공식 홈페이지 · 직접 만든 이미지")

# A · 하프코트 — 위에서 내려다본 코트 선을 크게 잘라 쓴다(3점 호 + 페인트존 오렌지 면)
def sample_a():
    S = 1080; im = Image.new("RGB", (S, S), COAL); d = ImageDraw.Draw(im)
    c = lambda v: v * S / 100
    d.rectangle([c(50), 0, S, c(52)], fill=ORNG)                                   # 페인트존
    d.arc([c(59), c(36), c(91), c(68)], 180, 360, fill=LINE, width=6)             # 자유투 반원(페인트 안쪽만)
    d.rectangle([c(50), -10, S + 10, c(52)], outline=LINE, width=6)
    r = c(88); cx, cy = c(80), c(-6)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=COAL2, width=10)          # 3점 호(배경 결)
    d.text((c(6), c(5)), P["kicker"], font=F(c(3.1), "Bold"), fill=LINE)
    fn = F(c(52)); bb = d.textbbox((0, 0), P["num"], font=fn)
    d.text((c(5) - bb[0], c(60) - bb[3]), P["num"], font=fn, fill=LINE)
    fu = F(c(8)); ub = d.textbbox((0, 0), P["unit"], font=fu)
    d.text((c(5) + bb[2] - bb[0] + c(1.5) - ub[0], c(60) - ub[3]), P["unit"], font=fu, fill=ORNG)
    fnm = F(c(12)); nw = d.textlength(P["name"], font=fnm); d.text((S - c(6) - nw, c(9)), P["name"], font=fnm, fill=COAL)
    fr = F(c(2.6), "Bold"); rw = d.textlength(P["role"], font=fr); d.text((S - c(6) - rw, c(25.5)), P["role"], font=fr, fill=COAL)
    for i, (k, v) in enumerate(P["rows"]):
        y = c(65) + i * c(9.5)
        d.text((c(6), y + c(1.6)), k, font=F(c(3), "Medium"), fill=MUTE)
        fv = F(c(5.6)); vw = d.textlength(v, font=fv); d.text((S - c(6) - vw, y), v, font=fv, fill=LINE)
        d.line([c(6), y + c(8), S - c(6), y + c(8)], fill=COAL2, width=2)
    ft = F(c(4.4)); tw = d.textlength(P["tag"], font=ft); h = c(8)
    d.rounded_rectangle([c(5), c(85), c(5) + tw + c(7), c(85) + h], radius=h / 2, fill=ORNG)
    d.text((c(8.5), c(85) + h / 2), P["tag"], font=ft, fill=COAL, anchor="lm")
    d.text((c(5), S - c(3.6)), P["src"], font=F(c(2.0), "Regular"), fill=MUTE)
    im.save(os.path.join(OUT, "A_하프코트.png"))

# B · 공 솔기 — 오렌지 면 위에 공의 검은 솔기 곡선 두 줄
def sample_b():
    S = 1080; im = Image.new("RGB", (S, S), ORNG); d = ImageDraw.Draw(im)
    c = lambda v: v * S / 100
    for x in range(0, S, 18):                                                      # 가죽 오돌토돌 결(아주 옅게)
        for y in range((x // 18) % 2 * 9, S, 18):
            d.ellipse([x, y, x + 3, y + 3], fill=(226, 100, 34))
    w = 14
    d.ellipse([c(-90), c(-20), c(10), c(120)], outline=COAL, width=w)              # 왼쪽 솔기
    d.ellipse([c(70), c(-30), c(170), c(110)], outline=COAL, width=w)              # 오른쪽 솔기
    d.line([0, c(58), S, c(58)], fill=COAL, width=w)                               # 가로 솔기
    d.text((c(6), c(5)), P["kicker"], font=F(c(3.1), "Bold"), fill=COAL)
    fn = F(c(50)); bb = d.textbbox((0, 0), P["num"], font=fn)
    d.text((c(40) - bb[0], c(55) - bb[3]), P["num"], font=fn, fill=WHITE, stroke_width=0)
    fu = F(c(8)); ub = d.textbbox((0, 0), P["unit"], font=fu)
    d.text((c(40) + bb[2] - bb[0] + c(1.5) - ub[0], c(55) - ub[3]), P["unit"], font=fu, fill=COAL)
    fnm = F(c(12)); d.text((c(9), c(12)), P["name"], font=fnm, fill=COAL)
    d.text((c(10), c(28)), "가드 · 동국대", font=F(c(3.2), "Bold"), fill=COAL)
    d.text((c(10), c(32.5)), "2018 드래프트 2순위", font=F(c(3.2), "Bold"), fill=COAL)
    box_y = c(62)
    d.rectangle([0, box_y, S, S], fill=COAL)
    for i, (k, v) in enumerate(P["rows"]):
        y = box_y + c(4) + i * c(9)
        d.text((c(6), y + c(1.6)), k, font=F(c(3), "Medium"), fill=MUTE)
        fv = F(c(5.6)); vw = d.textlength(v, font=fv); d.text((S - c(6) - vw, y), v, font=fv, fill=LINE)
    ft = F(c(4.4)); tw = d.textlength(P["tag"], font=ft); h = c(8)
    d.rounded_rectangle([c(5), c(85), c(5) + tw + c(7), c(85) + h], radius=h / 2, fill=ORNG)
    d.text((c(8.5), c(85) + h / 2), P["tag"], font=ft, fill=COAL, anchor="lm")
    d.text((c(5), S - c(3.6)), P["src"], font=F(c(2.0), "Regular"), fill=MUTE)
    im.save(os.path.join(OUT, "B_공솔기.png"))

# C · 트레이딩 카드 — 세로 4:5, 둥근 테두리, 앞면(번호·이름) + 아래 뒷면 기록 줄, 둥근 금메달 배지
def sample_c():
    W, H = 1080, 1350; im = Image.new("RGB", (W, H), ORNG); d = ImageDraw.Draw(im)
    m = 36
    d.rounded_rectangle([m, m, W - m, H - m], radius=44, fill=COAL)
    d.rounded_rectangle([m + 18, m + 18, W - m - 18, H - m - 18], radius=32, outline=COAL2, width=3)
    d.text((86, 92), P["kicker"], font=F(32, "Bold"), fill=ORNG)
    fn = F(640); bb = d.textbbox((0, 0), P["num"], font=fn)
    d.text((W / 2 - (bb[2] + bb[0]) / 2, 700 - bb[3]), P["num"], font=fn, fill=COAL, stroke_width=6, stroke_fill=ORNG)   # 외곽선 번호
    bx, by, br = W - 190, 210, 92
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=GOLD)                      # 둥근 배지
    d.ellipse([bx - br + 10, by - br + 10, bx + br - 10, by + br - 10], outline=COAL, width=3)
    d.text((bx, by - 18), "아시안게임", font=F(26, "Bold"), fill=COAL, anchor="mm")
    d.text((bx, by + 22), "금메달", font=F(40), fill=COAL, anchor="mm")
    d.text((86, 720), P["name"], font=F(132), fill=LINE)
    d.text((88, 880), P["role"], font=F(34, "Bold"), fill=MUTE)
    y0 = 960; d.rectangle([m + 18, y0, W - m - 18, y0 + 6], fill=ORNG)
    d.text((86, y0 + 40), "2026-27 개막 다섯 경기", font=F(30, "Bold"), fill=MUTE)
    cols = [("득점", "12.2"), ("어시스트", "7.2"), ("리바운드", "2.2"), ("보수", "8억")]
    cw = (W - 2 * 86) / 4
    for i, (k, v) in enumerate(cols):
        x = 86 + cw * i
        d.text((x, y0 + 100), v, font=F(76), fill=LINE if i < 3 else ORNG)
        d.text((x, y0 + 196), k, font=F(28, "Medium"), fill=MUTE)
    d.text((86, H - 92), P["src"], font=F(22, "Regular"), fill=MUTE)
    im.save(os.path.join(OUT, "C_트레이딩카드.png"))

if __name__ == "__main__":
    sample_a(); sample_b(); sample_c()
    ims = [Image.open(os.path.join(OUT, n)) for n in ("A_하프코트.png", "B_공솔기.png", "C_트레이딩카드.png")]
    ims = [i.resize((int(i.width * 1080 / i.height * 0.6), int(648))) for i in ims]
    sheet = Image.new("RGB", (sum(i.width for i in ims) + 40, 648), (255, 255, 255)); x = 0
    for i in ims: sheet.paste(i, (x, 0)); x += i.width + 20
    sheet.save(os.path.join(OUT, "_시안3종_비교.jpg"), quality=88); print("ok")
