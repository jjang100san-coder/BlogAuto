# -*- coding: utf-8 -*-
"""병역특례 글 도해 추가 9장(17~25). 글자를 줄이고 그림으로 옮기는 2차분. 숫자는 공부노트에서 확인한 것만."""
import os, math
from make_diagrams import *  # canvas, box, arrow, foot, ctext, save, 색·폰트 (실행 시 1~16도 다시 그려짐)

# 17 사건 타임라인 5일
im, d = canvas("17) 닷새 만에 '선수 발언'이 '제도 수술'이 됐다", "10월 3일 결승 → 10월 7일 국정감사")
y = 300; d.line([(90, y), (1310, y)], fill=GRAY, width=5)
ev = [(150, "10.3", "결승 1-0\n'군대 안 갑니다'\n전역모 사진", PINK, RED), (380, "10.4", "선수 3명 사과문\n축구협회 사과", LIGHT, INK),
      (610, "10.5", "체육회장 공항 사과\n국회 청원 등록\n여야 '손봐야'", LIGHT, INK), (840, "10.6", "국방부 '감면·폐지\n기본계획 반영'", SAND, AMBER),
      (1070, "10.7", "국감 '궁극 폐지'\n'당연히 축소'\n법안 발의", MINT, GREEN)]
for x, dt, txt, fill, col in ev:
    d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col)
    ctext(d, x, y - 62, dt, F_H, col)
    box(d, (x - 110, y + 40, x + 110, y + 200), fill, txt, F_S, INK)
box(d, (90, 560, 1310, 640), WHITE, "발언이 나온 날부터 정부가 '폐지'를 입에 올리기까지 나흘.", F_B, INK, outline=GRAY)
foot(d, "근거: KBS·SBS 10.4, 뉴시스 10.4, 머니투데이 10.5, 경향 10.6, 국감 10.7, 스포티비 10.7.")
save(im, "17_five_days.png")

# 18 이번 대회 편입 대상 종목별
im, d = canvas("18) 이번 대회로 자격을 얻은 선수는 57명, 그중 확인된 45명", "축구 20 · 야구 16 · 농구 8 · 골프 1 — 나머지 12명은 종목별 표를 못 봤다")
def row(d, y, n, col, label):
    for i in range(n):
        cx = 330 + i * 46; d.ellipse([cx, y, cx + 36, y + 36], fill=col)
    d.text((100, y), label, font=F_B, fill=INK)
row(d, 190, 20, AMBER, "축구 20"); row(d, 250, 16, AMBER, "야구 16"); row(d, 310, 8, AMBER, "농구 8"); row(d, 370, 1, AMBER, "골프 1")
for i in range(12):
    cx = 330 + i * 46; d.ellipse([cx, 430, cx + 36, cy := 466], fill=(205, 205, 205))
d.text((100, 430), "미확인 12", font=F_B, fill=GRAY)
box(d, (90, 520, 640, 640), SAND, "국감 발언: 43명 중 36명이 축구·야구\n(36 = 20 + 16)", F_B, INK)
box(d, (760, 520, 1310, 640), LIGHT, "국방부 전언: 57명\n집계 기준이 달라 두 숫자가 공존", F_B, INK)
foot(d, "근거: SBS 10.4(축구 20), OSEN 9.27(야구 16), 일간스포츠 9.20(농구 8), 연합 10.3(골프 김주형), MBC 10.6(57), 국감 10.7(43·36).")
save(im, "18_57_by_sport.png")

# 19 세 장면
im, d = canvas("19) 논란이 된 장면은 셋", "모두 결승 당일 10월 3일, 사과는 이튿날")
cols = [("주장 · 27세", "금메달 들어 보이며\n「군대 안 갑니다」\n「못 따면 9일 뒤 입대」", PINK),
        ("미드필더 · 토트넘 소속", "「메달·트로피 중요하지 않았다\n군 면제라는 보상\n하나만 보고」", PINK),
        ("막내 · 19세 · 결승 16분", "라커룸에서\n전역모 쓴 사진 SNS\n→ 삭제", PINK)]
x = 80
for t, s, fill in cols:
    box(d, (x, 190, x + 400, 250), LIGHT, t, F_H, INK)
    d.rounded_rectangle([x, 270, x + 400, 470], radius=28, fill=fill)
    d.polygon([(x + 60, 470), (x + 90, 470), (x + 70, 500)], fill=fill)
    box(d, (x, 270, x + 400, 470), fill, s, F_B, INK)
    x += 420
box(d, (90, 540, 1310, 640), MINT, "10월 4일 세 명 모두 사과문: 「국방의 의무를 하고 계신 모든 분께 죄송」\n법을 어긴 말은 없다. 혜택을 권리처럼 말한 태도가 문제였다.", F_S, GREEN)
foot(d, "근거: KBS 10.4, 연합뉴스TV 10.4, 뉴시스 10.4(박승수 사과), 마이데일리 10.4(이기혁 사과). 얼굴·실명 없음.")
save(im, "19_three_scenes.png")

# 20 1973 법의 다섯 서랍
im, d = canvas("20) 1973년 법은 '국가이익 특기자' 다섯 서랍이었다", "체육 전용이 아니었다 — 병역의무의 특례규제에 관한 법률, 국회 해산 중 비상국무회의 의결")
drawers = [("과학원 학생", LIGHT), ("군수·연구기관\n기술자", LIGHT), ("기간산업\n자격자", LIGHT), ("학술·예술\n특기자", LIGHT), ("체능 특기자", SAND)]
x = 90
for t, fill in drawers:
    d.rounded_rectangle([x, 200, x + 230, 400], radius=14, fill=fill, outline=GRAY, width=3)
    d.rounded_rectangle([x + 85, 215, x + 145, 230], radius=6, fill=GRAY)
    box(d, (x, 240, x + 230, 400), fill, t, F_B, INK)
    x += 245
box(d, (90, 440, 1310, 520), WHITE, "선발위원회(위원장 국무총리)가 「국가이익을 위해 특기의 계발·발휘가 필요한 자」를 뽑아 보충역으로", F_S, INK, outline=GRAY)
box(d, (90, 550, 640, 660), MINT, "그때 입영 가능 자원 연 30만+\n현역 입영은 17~18만", F_B, GREEN)
box(d, (760, 550, 1310, 660), SAND, "체육은 기준이 없어 보류\n1976 양정모가 사실상 첫 수혜", F_B, AMBER)
foot(d, "근거: 시사오늘 옛날신문(조선일보 1973 「특기자엔 병역특혜」), 한국일보 10.5, 연합 [재점검]① 10.10. 법률번호·조문 원문은 미확인.")
save(im, "20_five_drawers.png")

# 21 남북 순위 세 대회
im, d = canvas("21) 보상 패키지가 생긴 뒤, 순위는 이렇게 뒤집혔다", "1972 뮌헨 → 1974 테헤란 → 1976 몬트리올")
cols = [("1972 뮌헨", "한국 33위\n은 1", "북한 22위\n금1 은1 동3", PINK, LIGHT), ("1974 테헤란 AG", "한국 4위\n금18 은20 동31", "북한 5위\n금15 은14 동17", MINT, LIGHT), ("1976 몬트리올", "한국 19위\n금1 은1 동4", "북한 21위\n금1 은1", MINT, LIGHT)]
x = 80
for t, k, n, kf, nf in cols:
    box(d, (x, 190, x + 400, 250), LIGHT, t, F_H, INK)
    box(d, (x, 270, x + 400, 390), kf, k, F_B, INK)
    box(d, (x, 410, x + 400, 530), nf, n, F_B, GRAY)
    x += 420
box(d, (90, 580, 1310, 660), SAND, "1974년 막판 복싱 금 5개로 역전(북한 역도 약물 박탈도 겹침). 1976년 양정모 금으로 올림픽에서도 앞섰다.", F_S, INK)
foot(d, "근거: olympics.com(1972·1976), 위키백과 1974 아시안게임, North Korea at the 1976 Summer Olympics. 1978 방콕 북한 성적은 미확인.")
save(im, "21_rank_flip.png")

# 22 국회 지도 (이름 없이)
im, d = canvas("22) 국회 안의 세 목소리", "이름 대신 입장으로 — 10월 5일~8일 발언 기준")
cols = [("줄이거나 없애자", "여야 대부분\n「시대가 변했다」「BTS도 갔다」\n「목표 연도 정해 단계 축소」\n「아예 폐지, 경제적 보상으로」", PINK, RED),
        ("차분히 가자", "여당 일부\n「선수 발언 때문에\n제도 근간 흔드는 논의 반대」\n「격려도 전에 확대는 부적절」", SAND, AMBER),
        ("손대지 마라", "원로 정치인\n「철부지 한마디에 존폐 논의」\n「아마추어 동기부여 제도」", LIGHT, INK)]
x = 80
for t, s, fill, col in cols:
    box(d, (x, 190, x + 400, 250), fill, t, F_H, col)
    box(d, (x, 265, x + 400, 500), WHITE, s, F_S, INK, outline=col)
    x += 420
box(d, (90, 540, 1310, 640), MINT, "여당 원내 10.8: 「문제 있다는 데 모두 공감, 정부안이 나오면 여야 논의. 당 TF는 없다」\n→ 공은 11월 정부안으로.", F_S, GREEN)
foot(d, "근거: 경향 10.7(민주 손질·신중론), 연합 10.5(여야 발언), 뉴시스 10.8, 시사체크 영상 10.5, 파이낸셜뉴스 10.8.")
save(im, "22_three_voices.png")

# 23 왜 36년 동안 안 바뀌었나
im, d = canvas("23) 36년 동안 안 바뀐 이유는 셋", "2018년에도 포인트제까지 갔다가 멈췄다")
rocks = [("종목끼리 합의 실패", "대회 위상·난이도가 달라\n가중치를 못 정했다", PINK), ("병무청 반대", "「포인트제면 특례가\n오히려 늘어난다」", PINK), ("결정을 안 했다", "TF·위원회는 있었지만\n2019 「현행 유지」", PINK)]
x = 80
for i, (t, s, fill) in enumerate(rocks):
    d.ellipse([x + 60, 200, x + 340, 440], fill=fill)
    box(d, (x + 60, 200, x + 340, 440), fill, t + "\n\n" + s, F_S, INK)
    x += 420
box(d, (90, 500, 1310, 600), SAND, "평론가 한 줄: 「충분한 논의가 있었고 모범답안도 다 나왔다. 개선이 안 된 건 결정을 안 했기 때문」", F_S, INK)
box(d, (90, 620, 1310, 680), LIGHT, "이번이 다른 점: 국방부가 먼저 '폐지'를 말했고, 여론 61%가 축소·폐지", F_S, INK)
foot(d, "근거: SBS 8뉴스 10.4(2018 무산 이유), 2019.11.21 정부 브리핑, 오마이뉴스 10.9(최동호 인터뷰).")
save(im, "23_three_rocks.png")

# 24 다음 달력
im, d = canvas("24) 앞으로 두 달, 날짜 넷", "이 글을 고쳐 써야 할 때")
items = [("10월 말", "병무청 시행령 개정\n(예술 대회 축소 확정,\n아시안게임 포함 여부 미정)", SAND, AMBER), ("11월 7일", "국회 청원 동의 마감\n5만 명이면 국방위 회부", LIGHT, INK),
         ("11월 중순", "병무청 연구용역 결과\n인정대회·누적점수제", MINT, GREEN), ("연내", "정부 개선안 발표\n→ 여야 논의 시작", PINK, RED)]
x = 80
for t, s, fill, col in items:
    box(d, (x, 200, x + 290, 260), fill, t, F_H, col)
    box(d, (x, 275, x + 290, 470), WHITE, s, F_S, INK, outline=col)
    x += 310
box(d, (90, 530, 1310, 630), SAND, "바뀐 규칙은 다음 대회부터. 이번 57명은 현행 절차로 간다(신뢰보호원칙).", F_B, INK)
foot(d, "근거: 한국일보 10.7(10월 말), 국민동의청원(11.7), 연합 [재점검]④ 10.10·MBC 10.6(11월·연내), 뉴시스 10.8.")
save(im, "24_next_dates.png")

# 25 2018 vs 2026 말풍선
im, d = canvas("25) 같은 혜택, 다른 말", "2018 자카르타 금 vs 2026 나고야 금 — 비판의 축은 혜택이 아니라 태도")
d.rounded_rectangle([90, 200, 660, 420], radius=28, fill=MINT)
box(d, (90, 200, 660, 420), MINT, "2018\n「태극기만 보면 아직도 가슴이 뭉클하고\n애국가만 나와도 눈물이 날 것 같다」", F_B, GREEN)
d.rounded_rectangle([740, 200, 1310, 420], radius=28, fill=PINK)
box(d, (740, 200, 1310, 420), PINK, "2026\n「저 군대 안 갑니다」\n「군 면제라는 보상 하나만 보고」", F_B, RED)
box(d, (90, 470, 1310, 580), WHITE, "둘 다 아시안게임 금으로 같은 자격을 얻었다.\n뉴스 영상 여러 편이 이 둘을 나란히 붙여 편집했다.", F_B, INK, outline=GRAY)
box(d, (90, 610, 1310, 680), LIGHT, "축구 채널의 해석: U-23 팀은 대회마다 새로 모여 미디어 교육이 닿기 어렵고, 「금 따도 본전」인 대회라 혜택이 앞에 선다", F_S, INK)
foot(d, "근거: KBS 10.5(2018 손흥민 인터뷰 원음), 연합뉴스TV 10.6, TV조선 10.6, 뉴스헌터스 10.7. 공개 인터뷰 인용만.")
save(im, "25_same_medal_different_words.png")
print("done2")
