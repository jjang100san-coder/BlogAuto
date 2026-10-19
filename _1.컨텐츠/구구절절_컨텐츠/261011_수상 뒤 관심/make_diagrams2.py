# -*- coding: utf-8 -*-
"""「폭발 뒤 1~2년」 도해 3장(C3·C4·C5). 숫자·사실은 관심_공부노트 5장에서 확인한 것만."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "261011_병역특례 논란"))
from make_diagrams import canvas, box, foot, ctext, F_H, F_B, F_S, INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE
OUT = os.path.join(HERE, "img")
def save(im, n): im.save(os.path.join(OUT, n)); print("saved", n)

# C3 그 뒤 운명표
im, d = canvas("폭발 뒤 1~2년: 같은 역주행, 다른 끝", "음악 역주행 여덟 팀 — 계기 · 그 뒤 · 갈림의 이유 (기사 확인분)")
rows = [("브레이브걸스 2021", "후속곡 부진·콘서트 0회\n→ 2023.2 계약 만료\n팀명은 소속사 상표", PINK, RED),
        ("여자친구 2015", "6년 활동 → 2021.5\n7년 만료, 재계약 안 함\n→ 3인 비비지", PINK, RED),
        ("모모랜드 2018", "멤버 이탈·신곡 반응 하락\n소속사 재정\n→ 2023.1 계약 만료", PINK, RED),
        ("EXID 2015", "정규 1집 2위까지\n건강 이탈(2016)\n→ 2019 7년 만료 2명 이탈", PINK, RED),
        ("유니스 2026", "역주행 중인데\n'정해진 2년 6개월' 만료\n→ 2026.9.26 종료", PINK, RED),
        ("윤하 2022", "축제·투어 20회\n2024 체조경기장 2만 석\n연간 49→5→44위", MINT, GREEN),
        ("오마이걸 2020", "퀸덤으로 넓힌 팬층\n+ 수록곡 역주행\n→ 이듬해 신곡 첫 1위", MINT, GREEN),
        ("리센느 2026", "초동 3.6만→10.7만\n시리즈A 20억\n11.3 새 앨범 — 진행 중", SAND, AMBER)]
d.text((80, 150), "꺼진 쪽", font=F_H, fill=RED); d.text((720, 150), "남은 쪽", font=F_H, fill=GREEN)
y = 195
for i, (t, s, fill, col) in enumerate(rows):
    x = 80 if i < 5 else 720
    yy = y + (i if i < 5 else i - 5) * 92
    box(d, (x, yy, x + 200, yy + 84), fill, t, F_S, col)
    box(d, (x + 208, yy, x + 600, yy + 84), WHITE, s, F_S, INK, outline=col)
box(d, (90, 665, 1310, 720), SAND, "꺼진 쪽의 공통점은 '노래가 나빠서'가 아니다. 후속 무대가 없었고, 계약 시계가 먼저 울렸다.", F_S, INK)
foot(d, "근거: 아주경제 2023.2.16, 뉴시스 2021.5.18, OSEN 2023.1, 텐아시아 2019.5, 일간스포츠 2026.9.22, 뉴스서울 2024, fn 2025.1, 머니투데이 2026.9.14.")
save(im, "C3_two_years_later.png")

# C4 지속 조건 체크리스트
im, d = canvas("관심이 남는 조건 넷 — 열 사례에서 거꾸로 뽑은 것", "하나라도 비면 2년 안에 꺼졌다")
items = [("① 무대가 생겼나", "축제·투어·클럽·강릉 컬링 대회\n윤하 20회 투어 / 브걸 콘서트 0회", MINT, GREEN),
         ("② 밈이 팬덤으로 바뀌었나", "초동·팬클럽 선예매 같은 '다시 사는 사람' 숫자\n리센느 초동 3배 / 롤린은 군 밖 팬덤 미확인", MINT, GREEN),
         ("③ 다음 신호가 왔나", "후속곡·후속 수상이 첫 신호를 갱신\n오마이걸 이듬해 1위 / 한강 2026 NBCC상 → 5배", MINT, GREEN),
         ("④ 시계가 맞나", "계약 만료·멤버 건강·소속사 자본이 폭발보다 늦게 와야\n여자친구·EXID·모모랜드·브걸 전부 7년 시계에 걸림", MINT, GREEN)]
x = 80
for i, (t, s, fill, col) in enumerate(items):
    xx = x + (i % 2) * 620; yy = 180 + (i // 2) * 220
    box(d, (xx, yy, xx + 600, yy + 60), fill, t, F_H, col)
    box(d, (xx, yy + 70, xx + 600, yy + 190), WHITE, s, F_S, INK, outline=col)
box(d, (90, 630, 1310, 700), SAND, "책도 같다: 노벨 뒤 전체 도서 판매는 반년 만에 전보다 낮아졌지만(①·③ 없음), 소설 분야와 『소년이 온다』(2년 연속 1위)는 남았다.", F_S, INK)
foot(d, "근거: 공부노트 5장. 헤럴드경제 2025(상반기 도서 판매 후퇴), 뉴스스페이스 2025 연간, 연합 2026.3.27(NBCC상 뒤 5배).")
save(im, "C4_four_conditions.png")

# C5 리센느 체크표 (삼류 분석가의 조언)
im, d = canvas("리센느에게 감히 — 네 칸 중 지금 어디가 비어 있나", "공개된 숫자로만 채운 체크표. 2026.10.11 기준")
rows = [("① 무대", "축제 시즌 '신흥 축제 퀸', 음방 6관왕\n단독 콘서트·팬콘 공지는 미확인", AMBER, "△"),
        ("② 팬덤 전환", "초동 3.6만 → 10.7만(198%), 밈 전 '디어리스트' 8만 — 팬덤은 있다\n다만 구매자 남 69%·30·40대, 초동이 '다시 사는 손'인지는 미확인", AMBER, "△"),
        ("③ 다음 신호", "「데자뷰」 10월 멜론 3위(2025.7 발매곡의 재역주행)\n11.3 새 앨범 'Pulse' — 첫 자체 신호 시험대", AMBER, "△"),
        ("④ 시계", "2024.3 데뷔 → 표준계약 7년이면 2031 · 소속사 2025 영업손실 56억·자본잠식\n팀명 상표 RESCENE 10건 전부 소속사 명의(데뷔 8일 전 출원, 밈 뒤 7건 추가)", RED, "X")]
y = 170
for t, s, col, mark in rows:
    box(d, (80, y, 300, y + 95), LIGHT, t, F_H, INK)
    box(d, (310, y, 1200, y + 95), WHITE, s, F_S, INK, outline=col)
    ctext(d, 1260, y + 22, mark, F_H, col)
    y += 110
box(d, (90, 620, 1310, 710), SAND, "조언 셋 — 밈을 다시 쓰지 말 것(「운전만해」의 교훈) · 2027년 안에 단독 무대를 '셀 수 있는 숫자'로 남길 것\n· 팀명 상표와 재계약 시계를 팬보다 먼저 볼 것.", F_S, INK)
foot(d, "근거: 엑스포츠 10.5, 스타뉴스 9.14, 일간스포츠 10.5·9.18, 머니투데이 9.14, KIPRIS 10.11 직접 조회. ○△X는 글쓴이 판단.")
save(im, "C5_rescene_checklist.png")
print("done2")
