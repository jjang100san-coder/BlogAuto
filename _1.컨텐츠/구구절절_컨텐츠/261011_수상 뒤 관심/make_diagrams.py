# -*- coding: utf-8 -*-
"""「왜 상 받은 뒤에야 주목하는가」 연구 4개 설명 도해 + 사례 지속 곡선. 숫자는 관심_공부노트에서 확인한 것만."""
import os, math, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "261011_병역특례 논란"))
from make_diagrams import canvas, box, arrow, foot, ctext, F_T, F_H, F_B, F_S, F_X, F_N, INK, GRAY, BLUE, RED, GREEN, AMBER, LIGHT, PINK, MINT, SAND, WHITE, W, H
from PIL import Image, ImageDraw
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"); os.makedirs(OUT, exist_ok=True)
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)

# R1 정보 폭포 — 계단
im, d = canvas("연구 ① 정보 폭포: 앞사람을 보면 내 판단을 버린다", "Bikhchandani·Hirshleifer·Welch 1992, Journal of Political Economy 100(5)")
people = [("A", "내 느낌: 별로\n→ 그래도 산다?", "자기 신호만 보고 결정", MINT, GREEN),
          ("B", "A가 샀네\n내 느낌: 별로", "A 한 명이면 아직 내 느낌이 이김", MINT, GREEN),
          ("C", "A·B가 샀네\n내 느낌: 별로", "둘이 샀으면 내 느낌을 버리고 산다", PINK, RED),
          ("D~Z", "앞에 전부 샀네", "아무도 자기 느낌을\n안 본다 = 폭포", PINK, RED)]
x = 80
for i, (who, s, note, fill, col) in enumerate(people):
    y0 = 420 - i * 60
    d.ellipse([x + 100, y0 - 70, x + 180, y0 + 10], fill=col)
    ctext(d, x + 140, y0 - 50, who, F_H, WHITE)
    box(d, (x, y0 + 20, x + 290, y0 + 120), fill, s, F_S, INK)
    d.text((x, y0 + 130), note, font=F_S, fill=GRAY)
    if i < 3: arrow(d, (x + 300, y0 + 70), (x + 330, y0 + 10))
    x += 320
box(d, (90, 600, 1310, 700), SAND, "폭포는 앞의 두세 명이 우연히 같은 선택을 하면 시작된다. 정보가 모이지 않아 쉽게 뒤집힌다(취약).\n「상」은 앞사람 수천 명이 한꺼번에 '샀다'고 보여주는 신호다.", F_S, INK)
foot(d, "원문 요지: 남의 선택을 본 뒤 자기 신호와 무관하게 같은 행동 = 정보 폭포. 소수의 초기 선택으로 시작, 정보가 안 모여 취약.")
save(im, "R1_cascade.png")

# R2 사회적 증거
im, d = canvas("연구 ② 사회적 증거: 모를 때는 남들이 하는 것을 정답으로 삼는다", "Cialdini 『설득의 심리학(Influence)』 — 여섯 원칙 중 하나")
box(d, (90, 190, 640, 260), LIGHT, "확신이 있을 때", F_H, INK)
box(d, (90, 275, 640, 440), WHITE, "내 취향으로 고른다\n남이 뭘 읽든 상관없다", F_B, INK, outline=GRAY)
box(d, (760, 190, 1310, 260), PINK, "확신이 없을 때", F_H, RED)
box(d, (760, 275, 1310, 440), WHITE, "'비슷한 남들'이 고른 것을 정답으로 본다\n많이 고를수록 더 옳아 보인다", F_B, INK, outline=RED)
box(d, (90, 480, 1310, 580), SAND, "시집·낯선 작가·안 들어본 아이돌 = 확신이 없는 영역. 그래서 이 영역에서 수상·역주행 효과가 가장 크다.\n(공쿠르상 연구: 원래 덜 팔리던 책일수록 수상 효과가 컸다)", F_S, INK)
box(d, (90, 610, 1310, 690), MINT, "원문 표현: 「불확실할 때 우리는 비슷한 타인을 보고 올바른 행동을 찾는다. 그 수가 많을수록 더 옳다고 여긴다」", F_S, GREEN)
foot(d, "근거: Cialdini, Influence(social proof). 보조: Lagiosa·Méon 2021 공쿠르상 회귀불연속 — 판매 +350%, 사전 판매 적을수록 효과 큼.")
save(im, "R2_social_proof.png")

# R3 MusicLab 8개 세계
im, d = canvas("연구 ③ 누적 이익: 같은 48곡, 8개 세계, 1등이 다 달랐다", "Salganik·Dodds·Watts 2006, Science — 참가자 14,341명, 무명 밴드 48곡")
# independent world
box(d, (80, 180, 420, 240), LIGHT, "독립 세계", F_H, INK)
d.text((90, 250), "남의 다운로드 수가\n안 보임 → 순위 완만", font=F_S, fill=GRAY)
bars = [60, 52, 48, 44, 41, 38, 35, 33]
for i, b in enumerate(bars):
    d.rectangle([100 + i * 38, 440 - b * 2, 128 + i * 38, 440], fill=GRAY)
# 8 social worlds
rng = [[120, 40, 30, 25, 20, 15, 12, 10], [35, 115, 28, 22, 20, 14, 12, 9], [30, 28, 110, 24, 18, 15, 11, 8], [26, 24, 22, 105, 20, 14, 12, 9],
       [100, 30, 60, 20, 18, 14, 10, 8], [28, 26, 24, 22, 108, 15, 10, 8], [30, 95, 26, 24, 20, 40, 10, 8], [25, 24, 22, 20, 18, 16, 100, 9]]
cols = [AMBER, GREEN, BLUE, RED, AMBER, GREEN, BLUE, RED]
for w in range(8):
    x0 = 470 + (w % 4) * 210; y0 = 200 + (w // 4) * 200
    d.rectangle([x0, y0, x0 + 190, y0 + 170], fill=WHITE, outline=GRAY, width=2)
    d.text((x0 + 8, y0 + 4), f"세계 {w + 1}", font=F_S, fill=GRAY)
    for i, b in enumerate(rng[w]):
        d.rectangle([x0 + 12 + i * 22, y0 + 165 - b * 1.1, x0 + 28 + i * 22, y0 + 165], fill=cols[i] if b > 90 else (200, 200, 200))
d.text((470, 600), "남의 다운로드 수가 보이는 8개 세계: 같은 곡이 세계마다 다른 자리. 1등은 더 1등이 된다.", font=F_S, fill=INK)
box(d, (90, 630, 1310, 700), SAND, "「가장 좋은 곡은 꼴찌를 안 하고, 가장 나쁜 곡은 1등을 못 하지만, 그 사이는 뭐든 가능」. 역주행의 수학.", F_S, INK)
foot(d, "막대는 모식도(실제 수치 아님). 원문: 사회적 영향이 강할수록 불평등(Gini)과 예측불가능성이 함께 커졌다. Science 311(2006).")
save(im, "R3_musiclab.png")

# R4 상의 역설
im, d = canvas("연구 ④ 상의 역설: 수상작은 더 팔리지만 평점은 더 떨어진다", "Kovács·Sharkey 2014, Administrative Science Quarterly 59(1) — 2007~11 수상작·최종후보 64권(32쌍), Goodreads 리뷰 38,817개")
# axes
ox, oy = 150, 560
d.line([(ox, 200), (ox, oy)], fill=GRAY, width=3); d.line([(ox, oy), (900, oy)], fill=GRAY, width=3)
d.text((ox - 10, oy + 10), "수상 발표", font=F_S, fill=GRAY); d.text((820, oy + 10), "2년 뒤", font=F_S, fill=GRAY)
d.line([(ox + 250, 200), (ox + 250, oy)], fill=AMBER, width=3); d.text((ox + 258, 205), "발표", font=F_S, fill=AMBER)
# finalists flat
d.line([(ox, 300), (900, 305)], fill=GREEN, width=6); d.text((910, 290), "최종후보(낙선) 평점: 거의 그대로", font=F_S, fill=GREEN)
# winners drop
d.line([(ox, 300), (ox + 250, 298), (500, 340), (700, 380), (900, 400)], fill=RED, width=6, joint="curve"); d.text((910, 390), "수상작 평점: 약 0.25점 하락(5점 만점)", font=F_S, fill=RED)
# readers up
d.line([(ox, 520), (ox + 250, 515), (420, 380), (600, 330), (900, 320)], fill=BLUE, width=4); d.text((910, 330), "수상작 독자 수: 급증", font=F_S, fill=BLUE)
box(d, (90, 600, 1310, 700), SAND, "이유 둘: ① 취향이 제각각인 독자가 한꺼번에 몰린다 ② 인기 자체가 반감을 부른다.\n예: 『예감은 틀리지 않는다』(2011 부커) — 판매 급증과 동시에 평점 장기 하락.", F_S, INK)
foot(d, "선은 모식도. 「0.25점」은 2차 요약(Goodreads 블로그) 수치, 원문 표 재확인 필요. 원문: 수상작 평점이 최종후보작보다 가파르게 하락.")
save(im, "R4_paradox.png")

# C1 사례 지속 곡선 — 윤하·롤린·한강 해외
im, d = canvas("사례의 그 뒤: 폭발 다음 해에 어디에 있었나", "확인된 숫자만 — 멜론 연간 순위 · 해외 판매 부수")
rows = [("윤하 「사건의 지평선」 멜론 연간", ["2022: 49위", "2023: 5위", "2024: 44위", "827일 연속 차트인"], MINT, GREEN),
        ("브레이브걸스 「롤린」 멜론", ["2021 연간: 2위", "일간 547일 연속\n(2022.8.29)", "2022 연간: 72위", ""], SAND, AMBER),
        ("한강 해외 번역서 판매(번역원)", ["2023: 52만", "2024: 120만", "2025: 119.8만", "유지(정체)"], LIGHT, BLUE),
        ("『채식주의자』 국내(2016 부커)", ["수상 전 누적\n약 6만", "직후 1차 주문\n25만", "2016 말\n약 60만", "노벨 전 이미\n110만(2024.10 보도)"], PINK, RED)]
y = 190
for t, cells, fill, col in rows:
    box(d, (80, y, 440, y + 90), fill, t, F_S, col)
    for i, c in enumerate(cells):
        if c: box(d, (460 + i * 215, y, 460 + i * 215 + 200, y + 90), WHITE, c, F_S, INK, outline=col)
    y += 110
box(d, (90, 640, 1310, 710), SAND, "거제 해수욕장 51일 98.4만 명(전년 55.1만, +78%). 「관광객 300%」는 멤버 발언이라 안 쓴다.\n거제 전체 관광객은 2023→2025 감소세(733만→685만).", F_S, INK)
foot(d, "근거: 스포츠경향 2025.1.10, 와우TV 2022.1.26, 나무위키(547일), 번역원 2026.7, 한국일보 2016.5, 매일신문 2024.10.16, 멜론 2022 연간 차트, 뉴스1 2026.8.24.")
save(im, "C1_afterwards.png")

# C2 등록 선수 선그래프 — 대한체육회 포털 직접 조회
im, d = canvas("메달 뒤 등록 선수는 늘었나: 컬링은 평창 뒤 오히려 줄었다", "대한체육회 스포츠지원포털 종별현황(선수) 직접 조회 10.11 — 2021까지와 2022부터는 집계 기준이 달라 선을 끊었다")
series = {"컬링": ([(2016, 709), (2017, 790), (2018, 765), (2019, 668), (2020, 651), (2021, 631)], [(2022, 626), (2023, 667), (2024, 672), (2025, 720), (2026, 573)], RED),
          "양궁": ([(2016, 1819), (2017, 1749), (2018, 1836), (2019, 1730), (2020, 1756), (2021, 2024)], [(2022, 2267), (2023, 2517), (2024, 2764), (2025, 2834), (2026, 2706)], AMBER),
          "펜싱": ([(2016, 1634), (2017, 1626), (2018, 1696), (2019, 1717), (2020, 1651), (2021, 1793)], [(2022, 3939), (2023, 4541), (2024, 4967), (2025, 5146), (2026, 4608)], GREEN)}
ox, oy, ex = 130, 600, 1210
def X(yr): return ox + (yr - 2016) * (ex - ox) / 10
def Y(v, vmax=5400): return oy - v / vmax * 370
d.line([(ox, 200), (ox, oy)], fill=GRAY, width=3); d.line([(ox, oy), (ex, oy)], fill=GRAY, width=3)
for yr in range(2016, 2027):
    ctext(d, X(yr), oy + 10, str(yr), F_S, GRAY)
d.line([(X(2021.5), 200), (X(2021.5), oy)], fill=GRAY, width=2)
d.text((X(2021.5) + 8, 205), "집계 기준 변경(새 포털)", font=F_S, fill=GRAY)
d.line([(X(2018.1), 200), (X(2018.1), oy)], fill=BLUE, width=2); d.text((X(2018.1) + 8, 230), "평창 2018.2", font=F_S, fill=BLUE)
d.line([(X(2021.6), 200), (X(2021.6), oy)], fill=BLUE, width=1)
for name, (a, b, col) in series.items():
    for seg in (a, b):
        pts = [(X(y), Y(v)) for y, v in seg]
        d.line(pts, fill=col, width=5)
        for (x, y), (yr, v) in zip(pts, seg):
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=col)
    d.text((X(2026) + 14, Y(b[4][1]) - 18), name, font=F_H, fill=col)
    if name == "컬링": ctext(d, X(2017), Y(a[1][1]) - 30, f"{a[1][1]:,}", F_S, col)
    ctext(d, X(2021), Y(a[5][1]) - 30 + (0 if name != "펜싱" else 34), f"{a[5][1]:,}", F_S, col)
    ctext(d, X(2025), Y(b[3][1]) - 30, f"{b[3][1]:,}", F_S, col)
box(d, (90, 630, 1310, 710), SAND, "컬링: 2017년 790명 → 평창 뒤 2019년 668명 → 2021년 631명. '영미' 열풍은 등록 선수로 이어지지 않았다.\n양궁은 도쿄(2021) 뒤 완만히 증가, 펜싱은 꾸준히 증가. 2026은 연중 집계라 작다.", F_S, INK)
foot(d, "근거: g1.sports.or.kr 종별현황(선수) 2016~21(이전 포털)·2022~26(현 포털), 2026.10.11 조회.")
save(im, "C2_registered_players.png")
print("done")
