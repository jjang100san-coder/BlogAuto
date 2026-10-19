# -*- coding: utf-8 -*-
r"""블로그연대기 「애드포스트 수익 인증 — 승인 열흘」 카드 4장.
- 숫자는 전부 화면·내보내기 값 그대로(base data\). 계산한 숫자 없음(마스터 0-4).
- 🚫 노출 수·클릭 수·클릭률은 애드포스트 기밀 정보 — 공개하면 게재 제한(고객센터 17798). 카드에 넣지 않는다.
- 색: 1·2·4편 파랑/빨강, 3편 판정색, 5편 청록/주황, 세금 초안 보라/겨자와 겹치지 않게 초록·장미색(마스터 5-4).
- 첫 이미지(썸네일)는 AI 장면, 카드는 2번째부터(마스터 5-4)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BG, INK, SUB, LINE = (251, 251, 249), (17, 17, 17), (95, 95, 95), (222, 222, 222)
GREEN, ROSE, GRAY = (46, 125, 50), (206, 74, 104), (178, 182, 186)
GREEN_L, ROSE_L = (226, 241, 227), (249, 228, 234)
W = 1080
DAYS = ["10/2", "10/3", "10/4", "10/5", "10/6", "10/7", "10/8", "10/9", "10/10", "10/11"]
VIEWS = [851, 710, 682, 850, 899, 651, 672, 502, 592, 687]
INCOME = [1216, 2842, 779, 4116, 3250, 1910, 2685, 1310, 2220, 2369]

def f(size, w="Black"):
    ft = ImageFont.truetype(FONT, size); ft.set_variation_by_name(w); return ft

def canvas(h=W):
    im = Image.new("RGB", (W, h), BG); return im, ImageDraw.Draw(im)

def save(im, name):
    im.save(os.path.join(HERE, name), optimize=True); print("saved", name, im.size)

def foot(d, t): d.text((70, 1012), t, font=f(29, "Medium"), fill=SUB)

# ① 열흘 수입 막대
def card_income():
    im, d = canvas()
    d.text((70, 60), "승인 열흘, 하루 수입", font=f(66), fill=INK)
    d.text((70, 150), "애드포스트 수입 예정액 · 10월 2일~11일", font=f(38, "Bold"), fill=SUB)
    L, R, T, B = 80, W - 50, 270, 880
    vmax = 4500; n = len(DAYS); bw = (R - L) / n
    d.line([L, B, R, B], fill=INK, width=3)
    for i, (dd, v) in enumerate(zip(DAYS, INCOME)):
        x = L + i * bw; h = (B - T) * v / vmax
        col = GREEN if v == max(INCOME) else (ROSE if v == min(INCOME) else (168, 205, 170))
        d.rectangle([x + 12, B - h, x + bw - 12, B], fill=col)
        d.text((x + bw / 2, B - h - 12), f"{v:,}", font=f(28, "Bold"), fill=INK, anchor="ms")
        d.text((x + bw / 2, B + 16), dd, font=f(28, "Bold"), fill=SUB, anchor="ma")
    d.text((70, 950), "단위 원 · 가장 많은 날 초록, 가장 적은 날 장미색", font=f(32, "Bold"), fill=INK)
    foot(d, "애드포스트 수입 보고서 화면 값 · 잔액 22,697원과 같다")
    save(im, "card1_income_10days.png")

# ② 조회수 1등 ≠ 수입 1등
def card_views_vs_income():
    im, d = canvas()
    d.text((70, 60), "조회수 1등인 날과", font=f(64), fill=INK)
    d.text((70, 145), "수입 1등인 날", font=f(64), fill=INK)
    pairs = [("10월 6일 화", 899, 3250, "조회수 1등"), ("10월 5일 월", 850, 4116, "수입 1등")]
    y = 280
    for (lab, v, inc, tag), col, light in zip(pairs, (ROSE, GREEN), (ROSE_L, GREEN_L)):
        d.rounded_rectangle([70, y, W - 70, y + 290], 26, fill=light)
        d.rounded_rectangle([100, y + 28, 330, y + 84], 14, fill=col)
        d.text((215, y + 56), tag, font=f(32), fill=(255, 255, 255), anchor="mm")
        d.text((360, y + 30), lab, font=f(42, "Bold"), fill=INK)
        d.text((110, y + 130), "조회수", font=f(34, "Bold"), fill=SUB)
        d.text((110, y + 175), f"{v:,}", font=f(76), fill=INK)
        d.text((560, y + 130), "수입 예정액", font=f(34, "Bold"), fill=SUB)
        d.text((560, y + 175), f"{inc:,}원", font=f(76), fill=col)
        y += 330
    d.text((70, 945), "조회수가 더 많은 날이 더 번 날은 아니었다", font=f(38, "Bold"), fill=INK)
    foot(d, "블로그 통계 조회수 · 애드포스트 수입 보고서 화면 값")
    save(im, "card2_views_vs_income.png")

# ③ 사람은 어디서 왔나 — 두 주 나란히
def card_inflow():
    im, d = canvas()
    d.text((70, 60), "사람은 어디서 왔나", font=f(66), fill=INK)
    rows = [("9월 28일~10월 4일", 29.24, 70.72, 79.37), ("10월 5일~11일", 16.39, 83.57, 78.73)]
    y = 210
    for lab, s, t, hp in rows:
        d.text((70, y), lab, font=f(44, "Bold"), fill=SUB)
        x0, x1, top = 70, W - 70, y + 75
        mid = x0 + (x1 - x0) * s / 100
        d.rectangle([x0, top, mid, top + 130], fill=ROSE)
        d.rectangle([mid, top, x1, top + 130], fill=GREEN)
        d.text((x0 + 8, top + 150), f"검색 {s}%", font=f(44), fill=ROSE)
        d.text((x1, top + 150), f"사이트 {t}%", font=f(44), fill=GREEN, anchor="ra")
        d.text((x1, top + 208), f"사이트 중 홈판 {hp}%", font=f(34, "Bold"), fill=INK, anchor="ra")
        y += 370
    foot(d, "블로그 통계 유입분석 주간 화면 값")
    save(im, "card3_inflow_2weeks.png")

# ④ 잔액과 최소 지급액
def card_balance():
    im, d = canvas()
    d.text((70, 60), "아직 한 번도 못 받은 이유", font=f(62), fill=INK)
    d.text((70, 150), "최소 지급액을 20만 원으로 해 뒀다", font=f(42, "Bold"), fill=SUB)
    L, R, top = 70, W - 70, 380
    d.rounded_rectangle([L, top, R, top + 120], 30, fill=(236, 236, 232))
    fill_to = L + (R - L) * 22697 / 200000
    d.rounded_rectangle([L, top, max(fill_to, L + 60), top + 120], 30, fill=GREEN)
    d.text((L, top + 150), "현재 잔액 22,697원", font=f(50), fill=GREEN)
    d.text((R, top + 150), "20만 원", font=f(50), fill=INK, anchor="ra")
    lines = ["지난달 말일 잔액이 최소 지급액을 넘으면", "다음 달 25일(휴일이면 바뀜)에 계좌로", "1년 합계 12만 5천 원을 넘으면 그해 전부 8.8%"]
    for i, t in enumerate(lines):
        d.text((70, 700 + i * 70), t, font=f(38, "Bold"), fill=INK)
    foot(d, "지급 보고서 화면 · 애드포스트 고객센터 문서 기준")
    save(im, "card4_balance.png")

if __name__ == "__main__":
    card_income(); card_views_vs_income(); card_inflow(); card_balance()
