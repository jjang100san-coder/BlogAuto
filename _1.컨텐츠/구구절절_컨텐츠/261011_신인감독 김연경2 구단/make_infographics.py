# -*- coding: utf-8 -*-
"""「신인감독 김연경2 — 예능이 말하지 않은 숫자」 인포그래픽 13장. 숫자는 구단_공부노트_2026-10-11.md 확인분만."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_T, F_H, F_B, F_S, F_X, F_N,
                           INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)
F_SM = font(18); F_M = font(24, True); F_BIG = font(64, True); F_MID = font(34, True)
DIM = (205, 205, 200); NAVY = (40, 60, 110); ORANGE = (235, 120, 40); PURPLE = (120, 80, 200)

def person(d, cx, top, h, col):
    r = h * 0.17
    d.ellipse([cx - r, top, cx + r, top + 2 * r], fill=col)
    bw = h * 0.42
    d.rounded_rectangle([cx - bw / 2, top + 2 * r + h * 0.05, cx + bw / 2, top + h], radius=int(bw / 2), fill=col)
def vbar(d, x, base, w, hgt, col, label=None, value=None, f=F_S, vf=None, lcol=None):
    d.rounded_rectangle([x, base - hgt, x + w, base], radius=8, fill=col)
    if value: ctext(d, x + w / 2, base - hgt - 30, value, vf or F_M, lcol or (col if col != DIM else GRAY))
    if label: ctext(d, x + w / 2, base + 8, label, f, GRAY)
def hbar(d, x0, y, w_max, frac, col, label, value, h=34):
    d.rounded_rectangle([x0, y, x0 + w_max, y + h], radius=8, fill=LIGHT)
    d.rounded_rectangle([x0, y, x0 + max(12, w_max * frac), y + h], radius=8, fill=col)
    d.text((x0 - 12 - d.textlength(label, font=F_S), y + 5), label, font=F_S, fill=INK)
    d.text((x0 + w_max * frac + 12, y + 3), value, font=F_M, fill=col)
def ticket(d, x, y, w, h, col, big, small):
    d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=col)
    for cy in (y, y + h): d.ellipse([x + w * 0.68 - 14, cy - 14, x + w * 0.68 + 14, cy + 14], fill=BG)
    ctext(d, x + w * 0.34, y + h * 0.22, big, F_MID, WHITE); ctext(d, x + w * 0.34, y + h * 0.62, small, F_S, WHITE)
def coins(d, x, y, n, col, r=14):
    for i in range(n): d.ellipse([x + (i % 10) * (r * 2 + 4), y + (i // 10) * (r * 2 + 4), x + (i % 10) * (r * 2 + 4) + r * 2, y + (i // 10) * (r * 2 + 4) + r * 2], fill=col, outline=WHITE)

# ---------- D1 가입금 20억 ----------
im, d = canvas("프로 배구단 가입금은 20억 — 그리고 도장 셋", "KOVO 정관 6조·규약 9조(보도 확인): 신청 → 이사회 심의 → 총회 승인. 페퍼저축은행 2021 창단 원본")
ticket(d, 80, 170, 560, 200, NAVY, "20억 원", "가입 회비 2억 + 배구발전기금 18억")
d.text((80, 385), "페퍼저축은행이 2021.4 창단 때 낸 돈.", font=F_S, fill=GRAY)
d.text((80, 413), "SOOP 인수(2026.5) 때도 KOVO가 「신생팀 기준 약 20억」을 요구", font=F_S, fill=GRAY)
steps = [("① 신청", "재정 현황 + 구단 운영 계획서", BLUE), ("② 이사회 심의", "총재 + 남녀 14구단 단장 등 19명", AMBER), ("③ 총회 승인", "2026.6.2 SOOP 사례: 계약 18일 뒤", GREEN)]
for i, (t, s, col) in enumerate(steps):
    x0 = 700 + i * 0; y0 = 170 + i * 95
    box(d, (700, y0, 1000, y0 + 70), col, t, F_H, WHITE)
    d.text((1020, y0 + 20), s, font=F_S, fill=INK)
    if i < 2: arrow(d, (850, y0 + 78), (850, y0 + 92), GRAY, 4)
box(d, (90, 470, 1310, 580), SAND, "1화는 이 숫자를 말하지 않았다. 「현실적 조건」으로 나온 건 운영사무국·연고지·기업·관중·경기력 다섯(+우등버스).\n가입금은 그 다섯 뒤에 서 있는 첫 번째 돈이다.", F_S, INK)
box(d, (90, 600, 1310, 690), WHITE, "농구 데이원은 가입금 15억을 두 번 연체했고 1년 뒤 제명됐다(2023). 가입금은 들어올 때보다 「계속 낼 수 있나」가 문제다.", F_S, INK, outline=RED)
foot(d, "근거: 스포티비뉴스 2021(2억+18억), 서울신문 2026.5.18, 머니투데이 6.2(정관 6조·규약 9조), 문화일보 6.2(이사회 19명), SBS 2023(데이원)")
save(im, "D1_entry_fee.png")

# ---------- D2 매년 드는 돈 vs 버는 돈 ----------
im, d = canvas("들어온 뒤가 진짜 — 매년 70억을 쓰고, 스스로 버는 건 3.6억", "운영비는 페퍼저축은행 보도치, 중계권은 6시즌 300억을 14구단으로 나눈 계산값. 입장 수입은 KOVO 미공개")
vbar(d, 200, 520, 160, 70 * 4, RED, "여자부 운영비(페퍼)", "70억")
vbar(d, 560, 520, 120, 3.6 * 4, GREEN, "중계권 배분", "약 3.6억")
vbar(d, 730, 520, 120, 2 * 4, DIM, "입장·굿즈", "미공개")
d.text((560, 165), "구단이 직접 버는 돈", font=F_M, fill=GREEN)
d.text((160, 165), "구단이 쓰는 돈", font=F_M, fill=RED)
d.line([480, 180, 480, 540], fill=DIM, width=3)
arrow(d, (900, 300), (1180, 300), GRAY, 5)
box(d, (920, 180, 1320, 260), SAND, "이 간격을 메우는 말이\n「모기업 홍보 효과」", F_B, INK)
box(d, (920, 330, 1320, 440), WHITE, "중계권: KBS N 6시즌 300억\n= 연 50억 ÷ 14구단 = 약 3.6억\n(연맹이 받아 나눔)", F_S, INK, outline=GREEN)
box(d, (90, 580, 1310, 690), SAND, "야구는 다르다 — 2025년 10구단 매출 7,796억, 입장 수입이 약 30%, 모기업 의존은 25%까지 내려왔다.\n배구는 관중이 한 시즌 63만 명(14구단)이라 입장 수입으로 운영비를 메울 수 없다.", F_S, INK)
foot(d, "근거: 머니투데이 2026.5(페퍼 70억), MK 2021(KBS N 300억), 네이트 2026.4.20(야구), KOVO 2026.4.16(관중). 3.6억은 계산값")
save(im, "D2_yearly_gap.png")

# ---------- D3 중계권 배분 비교 (한국·일본) ----------
im, d = canvas("구단당 중계권 몫 — 배구 3.6억 · 야구 약 99억 · J1 약 22억", "구단당 한 해 몫. KBO·V리그는 리그 총액 ÷ 구단 수 계산값, J1은 균등배분금 공식 발표(성과 배분 별도). 환율 100엔=880원")
rows = [("한국 야구 KBO (10구단)", 99, "약 99억", NAVY), ("일본 축구 J1 균등배분 (20클럽)", 22, "약 22억", BLUE), ("한국 배구 V리그 (14구단)", 3.6, "약 3.6억", RED)]
x0, wmax, y = 470, 640, 190
for lab, v, val, col in rows:
    d.rounded_rectangle([x0, y, x0 + wmax, y + 44], radius=10, fill=LIGHT)
    d.rounded_rectangle([x0, y, x0 + max(14, wmax * v / 100), y + 44], radius=10, fill=col)
    d.text((x0 - 12 - d.textlength(lab, font=F_S), y + 10), lab, font=F_S, fill=INK)
    d.text((x0 + max(14, wmax * v / 100) + 12, y + 6), val, font=F_M, fill=col)
    y += 80
d.text((120, 440), "KBO: 지상파 3사 연 540억 + 뉴미디어(CJ ENM) 연 450억 = 연 990억 ÷ 10. 실제 구단 배분액은 미공개라 상한으로 본다.", font=F_SM, fill=GRAY)
d.text((120, 466), "J1: 2024년도 균등배분금 2.5억 엔. 성적·팬 지표 배분(총 약 35억 엔)은 따로 붙는다. V리그: KBS N 6시즌 300억 ÷ 6 ÷ 14.", font=F_SM, fill=GRAY)
box(d, (90, 530, 1310, 690), SAND, "V리그 구단이 중계권으로 받는 몫은 KBO 구단의 4% 안팎, J1 균등배분의 6분의 1이다.\n야구 구단은 중계권만으로 운영비의 큰 몫을 채우고, 배구 구단은 그 자리를 모기업이 채운다.", F_S, INK)
foot(d, "근거: KBO 보도자료 2024(지상파 1,620억·CJ ENM 1,350억, 각 3년), J리그 2024년도 배분금, MK 2021(V리그 300억/6시즌). 구단당은 계산값")
save(im, "D3_broadcast_scale.png")

# ---------- D4 홍보 효과 ----------
im, d = canvas("「홍보 효과」라는 셈법 — 운영비 30억에 효과 106억, 센 쪽은 연맹", "KOVO·SMS리서치 2011-12 시즌 조사(14년 전). 조사 주체가 연맹이라 부풀려졌을 수 있는 참고치. 2026년 재조사 입찰 중")
vbar(d, 160, 520, 150, 30 * 2.4, DIM, "IBK 운영비(당시)", "30억")
vbar(d, 380, 520, 150, 106 * 2.4, GREEN, "IBK 홍보효과", "106억")
d.text((180, 160), "신생 IBK기업은행 첫해", font=F_M, fill=INK)
vbar(d, 760, 520, 150, 508 * 0.5, AMBER, "삼성화재", "508억")
vbar(d, 980, 520, 150, 2244 * 0.115, BLUE, "리그 전체", "2,244억")
d.text((760, 160), "같은 조사의 다른 숫자", font=F_M, fill=INK)
d.text((760, 192), "(막대 눈금은 왼쪽과 다름)", font=F_SM, fill=GRAY)
box(d, (90, 570, 1310, 690), SAND, "TV 중계·뉴스·경기장 노출을 광고비로 환산한 숫자다. 모기업은 이 숫자로 「손실」을 「마케팅비」로 바꿔 읽는다.\n단, 센 주체가 연맹(KOVO)이다 — 리그 가치를 높게 보이고 싶은 쪽의 숫자라 부풀려졌을 수 있다. 참고치로만.\nV리그 출범 뒤 창단한 4곳이 전부 금융사인 이유는 이 셈법이다.", F_S, INK)
foot(d, "근거: 이데일리 2012(KOVO 조사), 경향 2023.4.25(창단 4곳 금융사), 머니투데이 2026.7.3(2026 용역 입찰). 환산 방법은 노출 집계.")
save(im, "D4_pr_effect.png")

# ---------- D5 페퍼 → SOOP 타임라인 ----------
im, d = canvas("모기업이 아프면 구단이 바로 아프다 — 페퍼에서 수퍼스까지", "2021 창단 → 2025 손실 → 2026 해체 위기 → 인수. 날짜는 보도·KOVO 발표")
ev = [("2021.4", "창단\n20억 납부", BLUE), ("2025", "모기업 순손실\n555억", RED), ("2026.4", "코치진·사무국\n계약 종료", RED), ("5.15", "SOOP 인수\n계약", AMBER), ("6.2", "KOVO 총회\n승인", GREEN), ("10.3", "SOOP 수퍼스\n출범", GREEN), ("11.1", "개막", GREEN)]
d.line([100, 330, 1300, 330], fill=GRAY, width=4)
for i, (dt, s, col) in enumerate(ev):
    x = 140 + i * 185
    d.ellipse([x - 14, 316, x + 14, 344], fill=col)
    ctext(d, x, 270, dt, F_M, col)
    for k, ln in enumerate(s.split("\n")): ctext(d, x, 360 + k * 26, ln, F_S, INK)
box(d, (90, 450, 1310, 560), WHITE, "3년 누적 손실 약 2,600억 · 직원 487 → 344명 · 2대 주주 사모펀드엔 「비핵심 자산」 → 운영 포기.\n김연경(1화 10분쯤): 「페퍼저축은행처럼 몇 년 안 됐는데 갑자기 팀이 해체되면 선수단 자체가 또 상처를 입고」", F_S, INK, outline=RED)
box(d, (90, 590, 1310, 690), SAND, "같은 해 폴란드 야스트솀프스키(모기업 JSW 지원 중단 → 2026.4 다음 시즌 불참), 2014 독일 운터하힝(제네랄리 이탈).\n스폰서 하나가 곧 구단 수명 — 세 대륙 공통.", F_S, INK)
foot(d, "근거: 머니투데이 2026.4.30, 서울신문 5.7·5.18·7.30, 머니투데이 6.2, 전남일보 10.3, 1화 전사(whisper+화면 대조), 유럽_구단운영모델.md.")
save(im, "D5_pepper_timeline.png")

# ---------- D6 스폰서 비중 비교 ----------
im, d = canvas("어디서나 배구는 스폰서가 매출의 90%", "구단 매출 중 스폰서·모기업 비중. 나라·종목별 공시 기준(연도 다름)")
rows = [("폴란드 야스트솀프스키(배구 2017)", 0.94, "94%", RED), ("폴란드 ZAKSA(배구 2017)", 0.91, "91%", RED), ("킹스리그(축구 예능 2025)", 0.88, "약 90%", RED),
        ("일본 B리그 B1(농구 2024-25)", 0.49, "49%", AMBER), ("일본 J1(축구 2024)", 0.41, "41%", AMBER), ("한국 프로야구 모기업 지원(2025)", 0.25, "25%", GREEN)]
y = 170
for lab, fr, val, col in rows:
    hbar(d, 520, y, 640, fr, col, lab, val); y += 60
d.text((520, 540), "한국 V리그 구단은 공시가 없어 비율을 못 센다 → 「운영비 70억 vs 중계권 3.6억」으로만", font=F_S, fill=GRAY)
box(d, (90, 590, 1310, 690), SAND, "배구는 세 대륙 모두 「누군가의 광고비」 종목이다. 입장 수입이 큰 야구·축구와 같은 잣대로 보면 틀린다.", F_B, INK)
foot(d, "근거: 유럽_구단운영모델.md(Grant Thornton 검증 자료 2차 인용), 일본_구단운영모델.md(B리그·J리그 1차 PDF), 네이트 2026.4.20(야구).")
save(im, "D6_sponsor_share.png")

# ---------- D7 네이밍 스폰서 모델 ----------
im, d = canvas("「키움처럼」 — 이름만 빌려주는 기업과 운영하는 구단을 나누는 길", "1화 9분쯤 KOVO 사무국 발언. 야구에서는 됐고, 농구에서는 1년 만에 무너졌다")
# 키움 모델
box(d, (80, 170, 420, 240), NAVY, "키움증권", F_H, WHITE); d.text((80, 250), "메인 스폰서 · 지분 0 · 운영비 지원", font=F_S, fill=GRAY)
arrow(d, (430, 205), (520, 205), NAVY, 6); d.text((425, 138), "연 100억(2019~23)", font=F_SM, fill=NAVY)
box(d, (530, 170, 870, 240), BLUE, "서울히어로즈(법인)", F_H, WHITE); d.text((530, 250), "구단 운영 · 선수 계약 · 수익", font=F_S, fill=GRAY)
d.text((80, 300), "2024~28 연장 최대 695억. 모기업 없는 유일한 야구단, 흑자 보도(연도별 수치는 보도마다 다름)", font=F_S, fill=INK)
# 데이원
box(d, (80, 370, 420, 440), (120, 60, 60), "캐롯손해보험", F_H, WHITE); d.text((80, 450), "네이밍 스폰서 → 시즌 끝 계약 종료", font=F_S, fill=GRAY)
arrow(d, (430, 405), (520, 405), RED, 6)
box(d, (530, 370, 870, 440), RED, "데이원스포츠(2022)", F_H, WHITE); d.text((530, 450), "경영난 → 임금 체불 → 2023.6 제명", font=F_S, fill=GRAY)
# 원더독스 제안
box(d, (950, 170, 1320, 240), AMBER, "구단주 기업(모집 중)", F_H, WHITE)
arrow(d, (1135, 250), (1135, 360), AMBER, 6); d.text((1150, 290), "이름·마케팅", font=F_S, fill=AMBER)
box(d, (950, 370, 1320, 440), ORANGE, "MBC 운영사무국?", F_H, WHITE); d.text((950, 450), "1화 10분쯤 「우리 방송국에서 해보면」", font=F_S, fill=GRAY)
box(d, (90, 520, 1310, 690), SAND, "왜 야구만 됐나 — 야구는 10구단 매출 7,796억·입장 30%라 스폰서 100억이 「보태는 돈」이지만,\n배구는 운영비 70억이 전부 「메워야 할 돈」이다. 이름값으로 70억을 매년 낼 기업이 있어야 이 그림이 선다.", F_S, INK)
foot(d, "근거: 경향 2018.11.6, 오마이스타 2023(695억), 시사저널 2019, 한국아이닷컴 2023(데이원), 1화 전사 9분쯤·10분쯤(화면 대조). 조직도는 모식도.")
save(im, "D7_naming_model.png")

# ---------- D8 미디어가 만든 리그·팀 ----------
im, d = canvas("미디어가 「0에서 만든」 리그와 「있는 구단을 키운」 쪽", "손익은 공식 발표·공시·보도. 원더독스는 전자에서 시작해 후자로 가려는 중")
left = [("XFL 2001 (WWE·NBC)", "각 3,500만 달러 손실, 1시즌"), ("XFL 2020", "파산 → 1,500만 달러 매각"), ("팬 컨트롤드 풋볼", "4,000만 달러 조달 → 2023 소멸"), ("킹스리그 2025", "매출 €5,200만·적자 → 2026.6 스페인 6개월 중단")]
right = [("렉섬 (라이언 레이놀즈 다큐)", "매출 28배, 스폰서 1,700만 파운드"), ("F1 (Drive to Survive)", "스폰서 82%가 다큐 뒤 체결"), ("요코하마 베이스타즈 (TBS→DeNA)", "관중 110만 → 236만, 2016 흑자"), ("SOOP 수퍼스 (2026)", "페퍼 승계 → 11.1 개막, 결과는 앞으로")]
box(d, (80, 160, 660, 210), PINK, "0에서 만들다", F_H, RED); box(d, (740, 160, 1320, 210), MINT, "있는 걸 키우다", F_H, GREEN)
for i, (t, s) in enumerate(left):
    y = 230 + i * 90; d.rounded_rectangle([80, y, 660, y + 76], radius=12, fill=WHITE, outline=RED, width=2)
    d.text((100, y + 8), t, font=F_M, fill=RED); d.text((100, y + 42), s, font=F_S, fill=INK)
for i, (t, s) in enumerate(right):
    y = 230 + i * 90; d.rounded_rectangle([740, y, 1320, y + 76], radius=12, fill=WHITE, outline=GREEN, width=2)
    d.text((760, y + 8), t, font=F_M, fill=GREEN); d.text((760, y + 42), s, font=F_S, fill=INK)
box(d, (90, 600, 1310, 690), SAND, "원더독스는 「0에서 만든 팀」인데, 목표는 「있는 리그(V리그)에 들어가기」다.\n자기 리그를 만든 쪽보다는 낫고, 구단을 산 쪽보다는 어렵다.", F_S, INK)
foot(d, "근거: 미국_구단운영모델.md(WWE 공식 발표·AAF·FCF), 유럽_구단운영모델.md(킹스리그), 일본_구단운영모델.md(DeNA), 전남일보 2026.10.3.")
save(im, "D8_media_made.png")

# ---------- D9 프로 팀의 조건 5 ----------
im, d = canvas("1화가 말한 〈프로 팀의 조건〉 다섯 — 그리고 각각의 가격표", "14분쯤 PD 발언·화면 그대로. 가격표는 이 글이 붙인 것(출처 각주)")
cards = [("① 운영사무국", "MBC 「원더독스\n창단 TF」 부서 신설\n(13분쯤)", "프런트 인건비\n미공개", GREEN),
         ("② 연고지", "지자체 필수\n(13분쯤)\n아직 미정", "유치 희망 예: 전주\n새 체육관 652억\n6,000석 2026 완공\n시 「창단보다 유치」", AMBER),
         ("③ 기업", "「기업이 제일 중요」\n(13분쯤)", "연 70억(페퍼 기준)\n+ 가입금 20억", RED),
         ("④ 관중 동원력", "직관 때 보여주자\n(13분쯤)", "V리그 평균 2,389명\n주말 3,079\n주중 2,058", BLUE),
         ("⑤ 경기력", "「그래야 기업도\n관중도」(14분쯤)", "시즌1 5승 2패\n4명 프로 입단", PURPLE)]
for i, (t, s1, s2, col) in enumerate(cards):
    x0 = 70 + i * 255
    d.rounded_rectangle([x0, 160, x0 + 240, 560], radius=16, fill=WHITE, outline=col, width=3)
    d.rounded_rectangle([x0, 160, x0 + 240, 215], radius=16, fill=col); ctext(d, x0 + 120, 174, t, F_M, WHITE)
    for k, ln in enumerate(s1.split("\n")): ctext(d, x0 + 120, 235 + k * 26, ln, F_S, INK)
    d.line([x0 + 20, 330, x0 + 220, 330], fill=DIM, width=2)
    ctext(d, x0 + 120, 342, "가격표", F_SM, GRAY)
    for k, ln in enumerate(s2.split("\n")): ctext(d, x0 + 120, 378 + k * 30, ln, F_M if k == 0 else F_S, col if k == 0 else INK)
d.rounded_rectangle([1150, 600, 1330, 670], radius=12, fill=SAND); ctext(d, 1240, 620, "+ 우등 버스", F_M, INK)
d.text((70, 620), "돈 숫자는 1화에 한 번도 안 나온다. 이 다섯 중 「기업」 칸이 나머지 넷의 지갑이다.", font=F_S, fill=INK)
foot(d, "근거: 1화 13~14분쯤 전사·화면, 전북일보 2025.10.8(전주 유치론, 연고지 확정 아님), KOVO 2026.4.16·5.28(관중), 시즌1 보도.")
save(im, "D9_five_conditions.png")

# ---------- D10 77일 ----------
im, d = canvas("남은 77일 — 12월 27일까지 구단주가 없으면 「다음 시즌은 없다」", "1화 1시간 31~32분쯤 화면·발언. 중간 날짜는 보도, 역산은 이 글의 계산")
ox, ex, y = 120, 1280, 330
def X(day): return ox + (ex - ox) * day / 77
d.line([ox, y, ex, y], fill=GRAY, width=5)
marks = [(0, "10.11\n1화 방송", BLUE), (21, "11.1\nV리그 개막\n(SOOP 수퍼스)", GREEN), (51, "12.1쯤\n기업 확정\n(역산)", AMBER), (69, "12.19\nKOVO 승인\n(역산)", AMBER), (77, "12.27\n마지막 방송", RED)]
for day, lab, col in marks:
    x = X(day); d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col)
    for k, ln in enumerate(lab.split("\n")): ctext(d, x, (y + 30 if day != 51 else y + 30) + k * 26, ln, F_S, col if k == 0 else INK)
d.rounded_rectangle([X(51), y - 60, X(69), y - 20], radius=8, fill=SAND); ctext(d, (X(51) + X(69)) / 2, y - 52, "심사 18일", F_S, INK)
d.text((120, 170), "SOOP 인수 때 「계약(5.15) → 총회 승인(6.2)」이 18일. 같은 속도면 12.19 승인에 맞춰 12월 초엔 기업이 서야 한다.", font=F_S, fill=INK)
box(d, (90, 520, 1310, 690), SAND, "시즌1 뒤 연락 온 기업은 「국내 굴지의 금융 기업·국내 대표 핀테크 기업」(6분쯤 화면).\n연초 이란 전쟁과 페퍼 해체가 그 대화를 끊었다(7분쯤). 이번엔 수퍼스가 개막한 시즌 한가운데서 찾는다.", F_S, INK)
foot(d, "근거: 1화 전사 1시간 31분쯤(화면 「예상 마지막 방송일 12월 27일」「다음 시즌은 없습니다」), 서울신문 2026.5.18, 머니투데이 6.2. 역산은 가정")
save(im, "D10_deadline.png")

# ---------- D11 일본 ----------
im, d = canvas("일본은 「독립」이 아니라 「분사」로 갔다 — 규모는 한국과 같다", "SV리그 2024년도 결산(1차 PDF) · 1부 라이선스 요건")
vbar(d, 160, 480, 160, 80 * 3, NAVY, "일본 SV 클럽 평균", "8.9억 엔 = 약 80억")
vbar(d, 420, 480, 160, 70 * 3, RED, "한국 V리그 여자부(페퍼)", "70억")
d.text((160, 170), "한 구단이 1년에 움직이는 돈", font=F_M, fill=INK)
req = ["운영 법인은 주식회사(2026-27~)", "매출 4억 엔 → 6억 엔", "아레나 5,000석(2029-30까지 3,000석)", "프로 계약 과반 · 결산 공개"]
d.text((720, 170), "SV리그 1부 라이선스", font=F_M, fill=INK)
for i, r in enumerate(req):
    d.rounded_rectangle([720, 215 + i * 62, 1320, 265 + i * 62], radius=10, fill=WHITE, outline=NAVY, width=2); d.text((740, 227 + i * 62), r, font=F_S, fill=INK)
box(d, (90, 530, 1310, 690), SAND, "도레이·JTEKT·산토리·파나소닉이 세운 「클럽」은 전부 모기업 100% 자회사.\n리그 수익은 9.4억 → 35.8억 엔으로 뛰었고 관중은 112만.\n한국은 분사도 아직이다 — 그래서 모기업 결산 한 줄이 구단 운명이 된다.", F_S, INK)
foot(d, "근거: 일본_구단운영모델.md(SV리그 2024년도 결산·라이선스 규칙, 경제산업성 2025.2). 「750→1,000명」은 2부 기준이라 뺐다.")
save(im, "D11_japan.png")

# ---------- D12 관중 ----------
im, d = canvas("관중은 늘었다 — 그래도 한 경기 2,389명", "KOVO 2025-26 시즌 발표(정규+포스트 266경기)")
vbar(d, 140, 520, 130, 25.7 * 7, DIM, "남 2024-25", "25.7만")
vbar(d, 300, 520, 130, 30.7 * 7, BLUE, "남 2025-26", "30.7만")
vbar(d, 520, 520, 130, 34.1 * 7, DIM, "여 2024-25", "34.1만")
vbar(d, 680, 520, 130, 32.8 * 7, RED, "여 2025-26", "32.8만")
d.text((140, 165), "시즌 총관중 — 남자부 +19.6% (OK저축은행 부산 이전), 여자부 -3.8%", font=F_M, fill=INK)
d.text((920, 200), "경기당 평균", font=F_M, fill=INK)
for i, (lab, v) in enumerate([("전체", "2,389명"), ("주말", "3,079명"), ("주중", "2,058명"), ("OK저축은행", "3,051명")]):
    d.rounded_rectangle([920, 240 + i * 62, 1320, 290 + i * 62], radius=10, fill=WHITE, outline=GRAY, width=2)
    d.text((940, 252 + i * 62), lab, font=F_S, fill=GRAY); d.text((1160, 250 + i * 62), v, font=F_M, fill=INK)
box(d, (90, 580, 1310, 690), SAND, "원더독스 시즌1 첫 직관은 2,000명(2025.11). V리그 평균과 비슷하다 — 「관중 동원력」 칸은 이미 숫자가 있다.\n문제는 입장 수입이 공개되지 않아 그 2,000명이 얼마인지 아무도 모른다는 것.", F_S, INK)
foot(d, "근거: KOVO(네이트 2026.4.16·5.28 워크숍), 다음 2025.11.17(원더독스 직관 2,000명). 입장 수입·객단가는 K리그와 달리 미공개.")
save(im, "D12_attendance.png")

# D13·D14(결론부)는 make_sustain.py

print("done_club")
