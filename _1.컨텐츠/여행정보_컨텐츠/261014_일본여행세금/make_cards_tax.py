# -*- coding: utf-8 -*-
"""일본 출국세 글 카드·그래프 5장 (오키나와·시라카와고 편과 같은 색·서체).
① card_conclusion.png   결론 카드(2번째 이미지)
② chart_tax_stack.png   항공권 세 장 세금 코드별 막대
③ card_refund_steps.png 면세 리펀드 방식 5단계
④ chart_kyoto.png       교토 숙박세 개정 전후
⑤ card_jan_trip.png     1월 동선 세금
숫자 출처: 글방향_일본여행세금.md 「내 숫자 확정」 표, base data\\*\\조사요약_*.md
"""
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
fm.fontManager.addfont("C:/Windows/Fonts/malgun.ttf"); fm.fontManager.addfont("C:/Windows/Fonts/malgunbd.ttf")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
BG, INK, MUT, RED, NAVY, SNOW, LINE, PALE = "#faf9f5", "#1a1a1a", "#7a7a7a", "#b9333f", "#1e3264", "#8fb3d9", "#e2e2e2", "#eef2f8"
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf" if b else "C:/Windows/Fonts/malgun.ttf", s)
FOOT = "직접 만든 그림 · 걷고읽고떠나고"

def card(W, H):
    im = Image.new("RGB", (W, H), BG); return im, ImageDraw.Draw(im)

# ① 결론 카드 — 10/15 사용자 지적 반영: 배수·엔/원 환산 없이, 원화 증감만
im, d = card(1400, 1400); X0, X1 = 70, 1330
d.text((X0, 58), "일본 출국세 1,000엔 → 3,000엔,", font=F(56, True), fill=INK)
d.text((X0, 134), "내 항공권 세금은 +11,800원", font=F(58, True), fill=RED)
d.text((X0, 222), "대한항공 마일리지 표 · 인천→고베 / 간사이→인천 · 2026년 1월과 2027년 1월", font=F(22), fill=MUT)
y = 290
d.rounded_rectangle((X0, y, X1, y + 700), radius=18, fill="#ffffff", outline=LINE, width=2)
for x, t in ((X0 + 34, "세금 줄"), (560, "2026년 1월 → 2027년 1월"), (1080, "증감")): d.text((x, y + 28), t, font=F(26, True), fill=NAVY)
groups = [("늘어남", RED, [("출국세 TK", "9,500 → 25,300원", "+15,800원")]),
          ("줄어듦", NAVY, [("공항 시설 사용료 SW", "31,500 → 27,900원", "-3,600원"), ("보안 요금 OI", "3,100 → 2,700원", "-400원")]),
          ("그대로", MUT, [("한국 출발 세금 BP", "24,000 → 24,000원", "0원")])]
yy = y + 86
for g, col, items in groups:
    d.text((X0 + 34, yy), g, font=F(24, True), fill=col); yy += 40
    for name, ab, diff in items:
        d.text((X0 + 34, yy), name, font=F(30), fill=INK)
        d.text((560, yy), ab, font=F(30), fill=INK)
        d.text((1080, yy), diff, font=F(32, True), fill=col if col != MUT else INK)
        yy += 58
    yy += 16
d.line((X0 + 30, yy, X1 - 30, yy), fill=LINE, width=2); yy += 22
d.text((X0 + 34, yy), "세금 합계", font=F(32, True), fill=INK)
d.text((560, yy), "68,100 → 79,900원", font=F(32, True), fill=INK)
d.text((1080, yy), "+11,800원", font=F(34, True), fill=RED)
y += 700 + 40
d.rounded_rectangle((X0, y, X1, y + 200), radius=18, fill=PALE, outline=NAVY, width=4)
d.text((X0 + 34, y + 34), "늘어난 줄 1개 +15,800원", font=F(34, True), fill=RED)
d.text((X0 + 34, y + 100), "줄어든 줄 2개 -4,000원  →  합계 +11,800원", font=F(34, True), fill=NAVY)
d.text((X0 + 8, 1330), FOOT + " · 대한항공 e-티켓(2025-12 발권)·운임 상세 화면(2026-10-14 조회)", font=F(20), fill=MUT)
im.save(os.path.join(HERE, "card_conclusion.png"))

# ② 세금 코드별 막대
labels = ["2026년 1월 간사이\n(2025-12 발권)", "2027년 1월 같은 노선\n(2026-10-14 조회)", "2027년 1월 나고야 내 표\n(2026-09-04 발권)"]
data = {"BP 한국 출발 세금": [24000, 24000, 24000], "OI 보안 요금": [3100, 2700, 5000],
        "SW 공항 시설 사용료": [31500, 27900, 25700], "TK 일본 출국세": [9500, 25300, 25700]}
colors = ["#c9cfd8", "#9aa8c4", SNOW, RED]
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=110, facecolor=BG); ax.set_facecolor(BG)
bottom = [0, 0, 0]
for (k, vals), c in zip(data.items(), colors):
    ax.bar(range(3), vals, 0.55, bottom=bottom, color=c, label=k)
    for i, v in enumerate(vals):
        ax.text(i, bottom[i] + v / 2, f"{v:,}", ha="center", va="center", fontsize=12, color="white" if c in (RED,) else INK, fontweight="bold" if c == RED else None)
    bottom = [b + v for b, v in zip(bottom, vals)]
for i, t in enumerate(bottom): ax.text(i, t + 1200, f"합계 {t:,}원", ha="center", fontsize=14, color=INK, fontweight="bold")
ax.set_xticks(range(3)); ax.set_xticklabels(labels, fontsize=12); ax.set_ylim(0, 92000); ax.set_ylabel("원", color=MUT)
ax.tick_params(colors=MUT); [s.set_visible(False) for s in ax.spines.values()]
ax.set_title("대한항공 마일리지 표 세 장, 세금 줄을 쌓아 보니", fontsize=18, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(frameon=False, loc="upper left", fontsize=11, ncol=2)
fig.text(0.01, 0.01, "대한항공 e-티켓·운임 상세 화면의 세금 코드별 금액 · 유류할증료는 세금이 아니라 뺐음 · 직접 만든 그래프", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_tax_stack.png"), facecolor=BG); plt.close(fig)

# ③ 면세 리펀드 5단계
im, d = card(1400, 1560)
d.text((X0, 58), "11월 1일부터 일본 면세,", font=F(56, True), fill=INK)
d.text((X0, 132), "공항에서 확인받고 돌려받는 방식", font=F(56, True), fill=NAVY)
d.text((X0, 220), "2026년 11월 1일 산 물건부터 · 일본 관광청·국세청 안내", font=F(22), fill=MUT)
steps = [("1", "매장", "여권을 보여 주고 세금 포함 값으로 사요", "같은 날·같은 매장 세전 5,000엔 이상"),
         ("2", "기한", "산 다음 날부터 90일째까지 출국해요", "90일이 지나면 환급 없음"),
         ("3", "공항", "짐을 맡기기 전에 키오스크에 여권을 읽혀요", "맡긴 짐은 되찾을 수 없어요"),
         ("4", "판정", "그린이면 끝, 레드면 세관에서 물건을 보여 줘요", "확인은 영수증 단위"),
         ("5", "환급", "확인 뒤 매장이나 환급 사업자가 소비세를 돌려줘요", "방법·시기는 매장마다 달라요")]
y = 290
for n, t, a, b in steps:
    d.rounded_rectangle((X0, y, X1, y + 190), radius=18, fill="#ffffff", outline=LINE, width=2)
    d.ellipse((X0 + 30, y + 50, X0 + 120, y + 140), fill=NAVY); d.text((X0 + 75, y + 95), n, font=F(44, True), fill="white", anchor="mm")
    d.text((X0 + 150, y + 30), t, font=F(30, True), fill=NAVY)
    d.text((X0 + 150, y + 78), a, font=F(32, True), fill=INK)
    d.text((X0 + 150, y + 132), b, font=F(26), fill=MUT)
    y += 190 + 22
d.rounded_rectangle((X0, y + 6, X1, y + 150), radius=18, fill=PALE, outline=NAVY, width=3)
d.text((X0 + 34, y + 30), "소모품을 하나라도 먹거나 쓰면 그 영수증 전체가 환급 안 돼요", font=F(30, True), fill=RED)
d.text((X0 + 34, y + 88), "일반물품·소모품 구분, 소모품 50만 엔 상한, 특수포장은 없어져요", font=F(26), fill=INK)
d.text((X0 + 8, 1500), FOOT + " · 관광청·국세청 공식 안내(2026-10-14 확인)", font=F(20), fill=MUT)
im.save(os.path.join(HERE, "card_refund_steps.png"))

# ④ 교토 숙박세
br = ["6천 엔\n미만", "6천~2만 엔\n미만", "2만~5만 엔\n미만", "5만~10만 엔\n미만", "10만 엔\n이상"]
old = [200, 200, 500, 1000, 1000]; new = [200, 400, 1000, 4000, 10000]
fig, ax = plt.subplots(figsize=(12, 7), dpi=110, facecolor=BG); ax.set_facecolor(BG)
w = 0.36
ax.bar([i - w / 2 for i in range(5)], old, w, color="#c9cfd8", label="2026년 2월까지")
ax.bar([i + w / 2 for i in range(5)], new, w, color=RED, label="2026년 3월 1일 숙박부터")
for i, (a, b) in enumerate(zip(old, new)):
    ax.text(i - w / 2, a + 150, f"{a:,}엔", ha="center", fontsize=11, color=MUT)
    ax.text(i + w / 2, b + 150, f"{b:,}엔", ha="center", fontsize=12, color=RED, fontweight="bold")
ax.set_xticks(range(5)); ax.set_xticklabels(br, fontsize=12); ax.set_ylim(0, 11000)
ax.set_xlabel("1인 1박 숙박요금 (식사·소비세 빼고)", color=MUT, fontsize=12); ax.tick_params(colors=MUT)
[s.set_visible(False) for s in ax.spines.values()]
ax.set_title("교토 숙박세, 1인 1박 얼마가 붙나", fontsize=18, color=INK, loc="left", pad=16, fontweight="bold")
ax.legend(frameon=False, loc="upper left", fontsize=12)
fig.text(0.01, 0.01, "교토시 숙박세 조례·공식 안내(2026-10-14 확인) · 직접 만든 그래프 · 걷고읽고떠나고", fontsize=10, color=MUT)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "chart_kyoto.png"), facecolor=BG); plt.close(fig)

# ⑤ 1월 동선
im, d = card(1400, 1300)
d.text((X0, 58), "2027년 1월 13~16일, 둘이서", font=F(52, True), fill=INK)
d.text((X0, 128), "일본에서 따로 붙는 세금", font=F(52, True), fill=NAVY)
d.text((X0, 210), "게로 → 다카야마 → 나고야 · 숙소 확인서와 항공권 기준", font=F(22), fill=MUT)
rows = [("1/13 게로 료칸", "입탕세 300엔은 예약값에 포함", "숙박세 400엔은 현장에서 따로", "숙박세 200엔 × 2"),
        ("1/14 다카야마 호텔", "1인 9,975엔 → 1만 엔에 25엔 모자라", "숙박세 둘이 200엔 + 온천 입탕세 300엔", "예약 화면엔 현장 결제 300엔"),
        ("1/15 나고야 호텔", "나고야는 숙박세가 없어요", "0엔", ""),
        ("1/16 주부공항 출국", "출국세 3,000엔 × 2", "항공권 값에 이미 들어 있어요", "내 표 TK 25,700원")]
y = 280
for t, a, b, c in rows:
    d.rounded_rectangle((X0, y, X1, y + 200), radius=18, fill="#ffffff", outline=LINE, width=2)
    d.text((X0 + 34, y + 28), t, font=F(32, True), fill=NAVY)
    d.text((X0 + 34, y + 82), a, font=F(28, True), fill=INK)
    d.text((X0 + 34, y + 130), b + ("  ·  " + c if c else ""), font=F(26), fill=MUT)
    y += 200 + 22
d.text((X0 + 8, 1240), FOOT + " · 게로시·다카야마시 숙박세·입탕세 공식 안내", font=F(20), fill=MUT)
im.save(os.path.join(HERE, "card_jan_trip.png"))
print("ok")
