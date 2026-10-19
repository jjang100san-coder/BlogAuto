# -*- coding: utf-8 -*-
"""언더독 효과 — 장면판 도해. 숫자는 공부노트 1절 사실표(F#)만. 사용: python figs.py [이름 ...]"""
import sys
from scene_base import frame, bg, tag, stamp, render, UD, TOP, RED

F = {}

# ---- 05 돈과 확률이 엇갈리면 (개념: AI 장면 — 낡은 벤치 vs 새 장비 벤치) ----
F["U05_money_vs_odds"] = frame(5, "언더독의 정의", "돈과 확률이 <em>엇갈리면</em>",
    bg("U05_benches")
    + tag(70, 470, "A팀", "이길 확률 70% · 선수단 돈 3,500만 달러", UD, -2, small=True, w=350)
    + tag(1010, 250, "B팀", "이길 확률 30% · 선수단 돈 1억 달러", TOP, 2, small=True, w=350)
    + '<div class="tag" style="left:520px;top:600px;transform:rotate(-1deg)"><b style="color:#D07A22">3분의 2</b><span>A팀을 응원 — 질 것 같은 B가 아니라 돈 적은 A</span></div>',
    "Vandello·Goldschmied·Richards(2007) 연구 4 초록 + 같은 설계를 소개한 기사(Slate 2010) · 벤치는 AI 생성 장면(실제 경기장 아님)")

# ---- 06 세 나라 모두 돈 적은 쪽 (숫자: 관중석 깃대 — 깃발 높이 = 응원 점수 0~9) ----
G6 = (("이스라엘", 110, 5.46, 4.63), ("중국", 107, 6.35, 4.96), ("일본", 118, 6.10, 5.28))
BASE_Y, PX = 662, 52  # 점수 1 = 52px
s = ['<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">',
     '<defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6ECF3"/><stop offset="1" stop-color="#F3EEE4"/></linearGradient></defs>',
     '<rect width="1400" height="800" fill="url(#wall)"/>',
     f'<rect x="0" y="{BASE_Y}" width="1400" height="{800 - BASE_Y}" fill="#C98B4E"/><rect x="0" y="{BASE_Y}" width="1400" height="6" fill="#A86E37"/>']
# 눈금 기둥(0·3·6·9)
for v in (0, 3, 6, 9):
    y = BASE_Y - v * PX
    s.append(f'<line x1="60" x2="1360" y1="{y}" y2="{y}" stroke="#B9C3D2" stroke-width="1.2" stroke-dasharray="4 6"/>'
             f'<text x="52" y="{y + 5}" text-anchor="end" font-size="14" font-weight="800" fill="#7C8799">{v}</text>')
for i, (nm, n, a, b) in enumerate(G6):
    cx = 300 + i * 400
    # 관중석(뒤쪽 계단식 좌석)
    for r in range(7):
        y = BASE_Y - 30 - r * 34; w = 300 - r * 14
        s.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="22" rx="6" fill="{"#CBD3DF" if r % 2 else "#D7DEE8"}"/>')
    for k, (v, col, who) in enumerate(((a, UD, "A"), (b, TOP, "B"))):
        px = cx - 73 + k * 146; top = BASE_Y - v * PX
        s.append(f'<line x1="{px}" y1="{BASE_Y}" x2="{px}" y2="{top - 4:.0f}" stroke="#4A4232" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="{px}" cy="{top - 8:.0f}" r="7" fill="#4A4232"/>'
                 f'<path d="M{px + 3} {top:.0f} q30 -10 58 4 t58 2 v58 q-28 -10 -58 0 t-58 -4 z" fill="{col}"/>'
                 f'<text x="{px + 61}" y="{top + 38:.0f}" text-anchor="middle" font-size="27" font-weight="900" fill="#FFFCF5">{v:.2f}</text>')
    s.append(f'<text x="{cx}" y="{BASE_Y + 44}" text-anchor="middle" font-size="24" font-weight="900" fill="#FFFCF5">{nm}</text>'
             f'<text x="{cx}" y="{BASE_Y + 72}" text-anchor="middle" font-size="15" font-weight="800" fill="#F6E6D2">대학생 {n}명</text>')
s.append('</svg>')
leg = ('<div style="position:absolute;right:40px;top:44px;z-index:6;background:rgba(255,252,245,.92);border-radius:8px;padding:12px 16px;font-size:16px;font-weight:800;color:#3A4152;line-height:1.75;box-shadow:0 6px 14px rgba(30,25,15,.12)">'
       f'<span style="display:inline-block;width:16px;height:16px;border-radius:3px;background:{UD};vertical-align:-2px;margin-right:8px"></span>A · 이길 확률 70% · 선수단 돈 3,500만 달러<br>'
       f'<span style="display:inline-block;width:16px;height:16px;border-radius:3px;background:{TOP};vertical-align:-2px;margin-right:8px"></span>B · 이길 확률 30% · 선수단 돈 1억 달러</div>')
F["U06_three_countries"] = frame(6, "세 나라에서 다시", "세 나라 모두 <em>돈 적은 쪽</em>을 더 응원했다", "".join(s) + leg
    + stamp(560, 196, "질 것 같은 쪽보다 돈 없는 쪽"),
    "Goldschmied·Galily·Keith(2018) Frontiers in Psychology 9:2246, 엇갈림 조건 평균(0~9 「이기길 바라는 정도」) · 깃발 높이 = 응원 점수")

# ================= AI 장면 + 꼬리표 =================
F["U01_team_name"] = frame(1, "원더독스", "팀 이름부터 <em>언더독</em>이었다",
    bg("U01_arena")
    + tag(790, 420, "언더독 → 원더", "「각자의 이유로 언더독이 된 이들이 다시 원더로」 — MBC 보도자료(2025.8.21), 23개 매체 같은 문장", UD, 1.5, w=520)
    + tag(90, 600, "「언더독」", "2화 첫 화면에 크게 띄운 한 단어(지난 이야기)", "#C8463C", -2, small=True, w=330),
    "MBC 보도자료(2025.8.21)·2화 화면 자막(두 판독) · 경기장은 AI 생성 장면(실제 경기장 아님)")

J2 = ((165, "방출"), (355, "방출"), (535, "은퇴 절차"), (710, "은퇴 뒤 복귀"), (890, "한 팀 17년 뒤 실업"), (1070, "드래프트 탈락<br>실업 7년"), (1250, "대학 리그"))
b2 = "".join(f'<div class="tag" style="left:{cx - 85}px;top:{600 + (i % 2) * 18}px;width:170px;padding:9px 10px 9px 22px;transform:rotate({(-2, 1.5, -1, 2, -1.5, 1, -2)[i]}deg)">'
             f'<span style="margin:0;font-size:15.5px;color:#1E2330;text-align:center">{w}</span></div>' for i, (cx, w) in enumerate(J2))
F["U02_seven_jerseys"] = frame(2, "시즌1 선수", "시즌1 일곱 명은 <em>어디서</em> 왔나", bg("U02_jerseys") + b2
    + stamp(860, 180, "기회가 적었던 일곱 명", UD),
    "보도(뉴스서울 2025.9.10, 기자 서술)·MBC 보도자료 「프로 무대에서 방출된 선수, 실업팀 선수, 은퇴 후 다시 코트를 밟으려는 선수」 · 유니폼은 AI 생성 장면")

F["U07_two_ingredients"] = frame(7, "언더독 이야기", "언더독 이야기의 <em>두 재료</em>", bg("U07_tape_shoes")
    + tag(90, 680, "바깥 불리함", "자원 부족·초라한 출발 — 내 탓이 아닌 사정", UD, -2, small=True, w=380)
    + tag(470, 190, "열정·끈기", "그래도 다시 해 보는 모습", UD, 2, small=True, w=300)
    + stamp(560, 600, "둘 다 있어야 먹힌다", "#22335A"),
    "Paharia·Keinan·Avery·Schor(2011) Journal of Consumer Research 37(5) 초록 · 손·운동화는 AI 생성 장면")

F["U08_unfair"] = frame(8, "언더독 이야기", "불리함보다 <em>「부당함」</em>", bg("U08_track")
    + tag(800, 300, "부당하게 불리", "더 매력적으로 보였다", UD, 2, small=True, w=270)
    + tag(1010, 560, "공정하게 유리", "이쪽도 매력 ↑", TOP, -1.5, small=True, w=250)
    + tag(70, 470, "공정하게 불리", "매력이 오르지 않음", "#8A8272", -2, small=True, w=250)
    + stamp(330, 690, "가로막힌 게 「내 탓이 아닐 때」", UD),
    "Michniewicz & Vandello(2013) Journal of Social and Personal Relationships 30(7) 초록, 78명·2×2 · 트랙은 AI 생성 장면(모식)")

F["U10_my_town"] = frame(10, "응원은 얕다", "내 일이 걸리면 <em>사라진다</em>", bg("U10_water")
    + tag(60, 330, "먼 도시 수질 검사", "계약을 두고 신생 업체를 응원", UD, -2, small=True, w=300)
    + tag(280, 680, "「발암 수은」 가능성", "결과가 중요해지자 응원이 사라짐", RED, 1, small=True, w=330)
    + tag(1030, 250, "내 동네로 바꾸면", "언더독 응원 안 함", TOP, 2, small=True, w=300)
    + stamp(620, 560, "「폭은 1마일, 깊이는 1인치」", "#22335A"),
    "Allison 연구실 실험을 소개한 기사(Slate 2010) — Kim 외(2008) 연구 4로 추정, 원문 미확인 · 물컵·부엌은 AI 생성 장면")

F["U11_tall_poppy"] = frame(11, "거울상", "높이 선 사람이 <em>떨어질 때</em>", bg("U11_poppy")
    + tag(600, 250, "키 큰 양귀비", "높은 성취자가 떨어지면 보통 사람이 떨어질 때보다 더 반겼다", RED, -1.5, small=True, w=380)
    + tag(80, 560, "「평균까지」", "바닥까지보다 평균까지 내려올 때 더 반김", RED, 2, small=True, w=330)
    + stamp(930, 600, "언더독 응원의 거울", "#22335A"),
    "Feather(1989) Australian Journal of Psychology 41(3) 초록 — 고교생 531·대학생 361·성인 205명 · 들판은 AI 생성 장면")

F["U12_we_won"] = frame(12, "이긴 다음 날", "이긴 다음 날의 <em>「우리」</em>", bg("U12_campus")
    + tag(760, 190, "「우리가 이겼다」", "학교 팀이 이긴 뒤 학교 옷을 더 입고, 「우리」라는 말을 더 썼다", UD, 1.5, small=True, w=430)
    + stamp(860, 400, "이긴 팀에 묻어가는 마음", "#22335A"),
    "Cialdini 외(1976) Journal of Personality and Social Psychology 34(3) 초록, 현장 실험 3개 · 교정은 AI 생성 장면(얼굴 없음)")

F["U13_prove_them_wrong"] = frame(13, "선수 쪽", "「못 할 거야」가 <em>연료</em>가 될 때", bg("U13_locker")
    + tag(540, 180, "「넌 못 할 거야」", "그 말을 믿지 않으면 → 보란 듯이 증명하고 싶어져 성과 ↑", UD, -1, small=True, w=470)
    + tag(860, 450, "믿을 만한 사람이 한 말이면", "오히려 성과 ↓", RED, 2, small=True, w=410),
    "Nurmohamed(2020) Academy of Management Journal 63(4) 초록, 연구 4개 — 관중이 아니라 선수 본인의 동기 · 라커룸은 AI 생성 장면")

import json, datetime as dt, pathlib
SVG0 = '<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">'
def T(x, y, s, size=16, w=800, fill="#1E2330", anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{w}" fill="{fill}" {extra}>{s}</text>'

# ---- 03 4패면 해체 + 방출제 (숫자: 체육관 벽 점수판, 동그라미 하나 = 경기 하나) ----
s = [SVG0, '<defs><linearGradient id="gw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DCE3EC"/><stop offset="1" stop-color="#EEE7DA"/></linearGradient></defs>',
     '<rect width="1400" height="800" fill="url(#gw)"/>',
     '<rect x="150" y="214" width="1100" height="410" rx="18" fill="#2B2F3A"/><rect x="164" y="228" width="1072" height="382" rx="12" fill="#353A47"/>',
     '<line x1="300" y1="150" x2="300" y2="214" stroke="#6B7080" stroke-width="5"/><line x1="1100" y1="150" x2="1100" y2="214" stroke="#6B7080" stroke-width="5"/>']
def row(y, label, sub, cells):
    out = [T(230, y + 8, label, 30, 900, "#FFFCF5"), T(230, y + 36, sub, 15, 700, "#AEB4C2")]
    for i, (kind, txt) in enumerate(cells):
        cx = 410 + i * 116
        if kind == "W": out.append(f'<circle cx="{cx}" cy="{y}" r="40" fill="{UD}"/>' + T(cx, y + 10, txt, 26, 900, "#FFFCF5"))
        elif kind == "L": out.append(f'<circle cx="{cx}" cy="{y}" r="40" fill="#5A6070"/>' + T(cx, y + 10, txt, 26, 900, "#C9CDD6"))
        elif kind == "N": out.append(f'<circle cx="{cx}" cy="{y}" r="40" fill="none" stroke="{UD}" stroke-width="4" stroke-dasharray="7 6"/>' + T(cx, y + 8, txt, 17, 800, "#F2C79B"))
        else: out.append(f'<circle cx="{cx}" cy="{y}" r="40" fill="none" stroke="#6B7080" stroke-width="3"/>')
    return "".join(out)
s.append(row(330, "시즌1", "5승 2패", [("W", "승")] * 5 + [("L", "패")] * 2))
s.append(row(500, "시즌2", "첫 경기 진행 중", [("N", "3화")] + [("E", "")] * 6))
s.append(f'<path d="M 694 438 h 456 M 694 438 v 14 M 1150 438 v 14" stroke="{RED}" stroke-width="4" fill="none"/>' + T(922, 428, "이 중 4번 지면 즉시 해체", 20, 900, "#FF9C8F"))
s.append('</svg>')
F["U03_four_losses"] = frame(3, "규칙", "4번 지면 <em>해체</em>, 이번엔 방출제까지", "".join(s)
    + tag(870, 650, "방출제 &amp; 영입제", "이번 시즌 새로 도입 — 2화 자막·내레이션", RED, -1.5, small=True)
    + '<div style="position:absolute;left:170px;top:648px;font-size:14px;font-weight:700;color:#6E6656;z-index:5">시즌1 동그라미는 승·패 개수(경기 순서 아님)</div>',
    "2화 내레이션 「4패를 기록하게 되면 원더독스는 즉시 해체」·자막 「방출제&영입제 도입」(음성·화면 두 판독), 시즌1 7전 5승 2패(MBC·보도)")

# ---- 04 리벤지 매치 세트 점수판 ----
s = [SVG0, '<rect width="1400" height="800" fill="#E9E2D3"/>',
     '<rect x="0" y="560" width="1400" height="240" fill="#D9874A"/><rect x="0" y="560" width="1400" height="6" fill="#B96A31"/>',
     '<line x1="0" y1="690" x2="1400" y2="690" stroke="#FFFCF5" stroke-width="5" opacity=".8"/>']
def sets(y, title, sub, cols):
    out = [f'<rect x="120" y="{y}" width="1160" height="150" rx="14" fill="#FFFCF5" stroke="#D8CDB8" stroke-width="2"/>',
           T(160, y + 62, title, 26, 900, "#1E2330", "start"), T(160, y + 96, sub, 15, 700, "#6E6656", "start")]
    for i, (lab, top_, bot, st) in enumerate(cols):
        x = 480 + i * 156
        fill = UD if st == "W" else ("#8E96A8" if st == "L" else "#FFFCF5")
        out.append(f'<rect x="{x}" y="{y + 20}" width="136" height="110" rx="10" fill="{fill}" stroke="{UD if st == "P" else "none"}" stroke-width="3" stroke-dasharray="{"7 5" if st == "P" else "0"}"/>')
        out.append(T(x + 68, y + 46, lab, 14, 800, "#FFFCF5" if st != "P" else "#8A7F6A"))
        out.append(T(x + 68, y + 88, top_, 30 if len(top_) < 6 else 20, 900, "#FFFCF5" if st != "P" else UD))
        if bot: out.append(T(x + 68, y + 116, bot, 14, 800, "#FFFCF5" if st != "P" else "#8A7F6A"))
    return "".join(out)
s.append(sets(200, "시즌1 · 일본 원정", "2세트를 먼저 따고 역전패", [("1세트", "승", "", "W"), ("2세트", "승", "", "W"), ("3세트", "패", "", "L"), ("4세트", "패", "", "L"), ("5세트", "패", "", "L")]))
s.append(sets(380, "시즌2 · 2화 첫 경기", "같은 상대, 슈지츠 고교", [("1세트", "18 : 25", "원더독스 : 슈지츠", "L"), ("2세트", "추격 중", "결과는 3화", "P")]))
s.append('</svg>')
F["U04_revenge_sets"] = frame(4, "리벤지 매치", "1년 만의 리벤지, 1세트는 <em>18 : 25</em>", "".join(s)
    + tag(820, 404, "32% : 30%", "공격 성공률은 원더독스가 앞섰다", UD, 2, small=True, w=330)
    + stamp(980, 640, "결과는 10월 25일 3화", UD),
    "2화 캐스터 멘트·스코어 그래픽(음성·화면 두 판독) — 시즌1 세트별 점수는 방송에 없어 승패만")

# ---- 09 언더독이 3연승하면 (숫자 모식: 점 100개가 관중석 사이로 옮겨 감) ----
s = [SVG0, '<rect width="1400" height="800" fill="#EDF1F5"/>']
def stand(x0, n_ud, moved=0):
    out = [f'<rect x="{x0}" y="250" width="270" height="330" rx="14" fill="#FBEBDA"/>', f'<rect x="{x0 + 300}" y="250" width="270" height="330" rx="14" fill="#E3EAF6"/>',
           T(x0 + 135, 610, "언더독 응원석", 17, 900, UD), T(x0 + 435, 610, "강자 응원석", 17, 900, TOP)]
    ud = [(x0 + 24 + (k % 9) * 27, 280 + (k // 9) * 27) for k in range(n_ud)]
    tp = [(x0 + 324 + (k % 9) * 27, 280 + (k // 9) * 27) for k in range(100 - n_ud)]
    for i, (x, y) in enumerate(ud): out.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{UD}"/>')
    for i, (x, y) in enumerate(tp):
        mv = i >= (100 - n_ud) - moved
        out.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{"#9DB3DE" if mv else TOP}"/>')
    return "".join(out)
s.append(stand(70, 81)); s.append(stand(760, 41, 40))
s.append(f'<path d="M 660 410 h 70" stroke="#4A5163" stroke-width="4" marker-end="url(#ar)"/><defs><marker id="ar" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#4A5163"/></marker></defs>')
s.append(T(355, 228, "처음", 20, 900, "#3A4152") + T(1045, 228, "「언더독이 3연승」 소식 뒤", 20, 900, "#3A4152") + '</svg>')
F["U09_after_three_wins"] = frame(9, "응원은 옮겨 간다", "언더독이 3연승하면, <em>절반</em>이 강자 쪽으로", "".join(s)
    + tag(250, 660, "81%", "처음엔 언더독 응원", UD, -2, small=True)
    + tag(900, 660, "그중 절반", "강자 쪽으로 옮김(연한 파랑 점)", TOP, 2, small=True),
    "Frazier & Snyder(1991) 7전 4선승 가상 시리즈를 소개한 기사(Slate 2010) — 원문 숫자 미확인 · 점 100개는 대학생 약 100명의 모식")

# ---- 14 이변을 보러 오나 (숫자 모식: TV 세 대) ----
s = [SVG0, '<rect width="1400" height="800" fill="#EAE4D8"/>', '<rect x="0" y="600" width="1400" height="200" fill="#B98E62"/><rect x="0" y="600" width="1400" height="8" fill="#9C744A"/>']
TVS = (("스페인 무료 중계 304경기", "큰 언더독·큰 강자 경기 > 박빙"), ("잉글랜드·챔피언스리그 TV", "박빙 여부 무관 — 스타·팀 수준"), ("K리그 유튜브 댓글 16,937개", "예상 밖 승리 → 긍정 댓글 ↑"))
for i, (nm, sub) in enumerate(TVS):
    x = 90 + i * 420; y = 250
    s.append(f'<rect x="{x}" y="{y}" width="380" height="250" rx="16" fill="#23262E"/><rect x="{x + 16}" y="{y + 16}" width="348" height="206" rx="8" fill="#F4F1EA"/>'
             f'<rect x="{x + 150}" y="{y + 250}" width="80" height="40" fill="#23262E"/><rect x="{x + 100}" y="{y + 288}" width="180" height="14" rx="4" fill="#23262E"/>')
    gx0, gx1, gy0 = x + 46, x + 334, y + 180
    if i == 0:
        s.append(f'<path d="M {gx0} {y + 60} Q {x + 190} {y + 230} {gx1} {y + 60}" fill="none" stroke="{UD}" stroke-width="7" stroke-linecap="round"/>'
                 + T(gx0 + 10, gy0 + 30, "큰 언더독", 13, 800, "#6E6656") + T(x + 190, gy0 + 30, "박빙", 13, 800, "#6E6656") + T(gx1 - 10, gy0 + 30, "큰 강자", 13, 800, "#6E6656"))
    elif i == 1:
        s.append(f'<path d="M {gx0} {y + 120} L {gx1} {y + 120}" stroke="{TOP}" stroke-width="7" stroke-linecap="round"/>'
                 f'<path d="M {x + 190} {y + 52} l 9 18 20 3 -15 14 4 20 -18 -10 -18 10 4 -20 -15 -14 20 -3 z" fill="#E6B23C"/>')
    else:
        for k, (bx, h) in enumerate(((x + 90, 50), (x + 190, 120))):
            s.append(f'<rect x="{bx}" y="{gy0 - h}" width="80" height="{h}" rx="6" fill="{UD if k else "#C9C2B3"}"/>')
        s.append(T(x + 130, gy0 + 30, "예상대로", 13, 800, "#6E6656") + T(x + 230, gy0 + 30, "예상 밖 승리", 13, 800, "#6E6656"))
    s.append(T(x + 190, 640, nm, 19, 900, "#FFFCF5") + T(x + 190, 668, sub, 15, 800, "#F6E6D2"))
s.append('</svg>')
F["U14_upset_demand"] = frame(14, "보는 쪽", "이변을 보러 오나 — <em>리그마다</em> 달랐다", "".join(s),
    "Humphreys & Pérez(2019), Buraimo & Simmons(2015)·Wills 외(2022), Sung 외(2023) KJSS 34(4) · 화면 속 선·막대는 방향만 보인 모식")

# ---- 15 코모, 어느 줄로 재나 (숫자: 호숫가 20층 탑 여섯 — 불 켜진 층 = 세리에A 순위) ----
AX = (("구단주 재산", 1, "2026.3 보도"), ("이적 순지출", 1, "2025-26"), ("선수단 시장가치", 3, "2026-27"), ("리그 순위", 4, "10/18 기준"), ("연봉 총액", 8, "2026-27"), ("평균 관중", 19, "세 시즌 연속"))
s = [SVG0, '<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DCE8F3"/><stop offset="1" stop-color="#F3EFE6"/></linearGradient>'
     '<linearGradient id="lk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FB0C9"/><stop offset="1" stop-color="#5E86A6"/></linearGradient></defs>',
     '<rect width="1400" height="800" fill="url(#sk)"/>', '<path d="M0 300 L180 220 L330 270 L520 190 L700 260 L900 200 L1100 250 L1400 210 L1400 640 L0 640Z" fill="#C9D6CF" opacity=".7"/>',
     '<rect x="0" y="640" width="1400" height="160" fill="url(#lk)"/>']
FH = 22
for i, (nm, rk, when) in enumerate(AX):
    x = 120 + i * 200; w = 120; top = 640 - 20 * FH
    col = TOP if rk <= 5 else UD
    for f in range(20):
        r = f + 1; y = top + f * FH
        lit = r == rk
        s.append(f'<rect x="{x}" y="{y + 2}" width="{w}" height="{FH - 4}" rx="2" fill="{col if lit else "#E9E2D5"}" stroke="#CDBFA6" stroke-width="1"/>')
        if r in (1, 5, 10, 15, 20) and i == 0: s.append(T(x - 14, y + 16, f"{r}위", 13, 800, "#7C8799", "end"))
    ly = top + (rk - 1) * FH
    s.append(T(x + w / 2, ly + 16, f"{rk}위", 15, 900, "#FFFCF5"))
    s.append(f'<rect x="{x}" y="645" width="{w}" height="{20 * FH * .35:.0f}" fill="#FFFCF5" opacity=".12"/>')
    s.append(T(x + w / 2, 690, nm, 18, 900, "#FFFCF5") + T(x + w / 2, 714, when, 13, 800, "#E3EDF5"))
s.append('</svg>')
F["U15_como_ranks"] = frame(15, "코모", "코모는 어느 줄로 재느냐에 따라 <em>1위</em>도 19위도", "".join(s)
    + tag(1060, 120, "43%", "연봉 총액 = 인테르의 43%(2026-27)", UD, 2, small=True, w=300)
    + stamp(980, 250, "상대가 누구냐에 따라 바뀐다", "#22335A"),
    "Forbes 인용 보도(2026.3)·Transfermarkt(순지출·시장가치·관중)·Calcio e Finanza(연봉, 보너스 제외)·세리에A 순위(10/18) · 탑 한 층 = 세리에A 20개 팀 중 순위")

# ---- 16 예상 11위가 4위로, 이제 우승 후보 (숫자: 암벽 루트 — 아래 20위, 위 1위) ----
def ry(r): return 232 + (r - 1) * 23
s = [SVG0, '<rect width="1400" height="800" fill="#D9D2C5"/>']
import random
rnd = random.Random(16)
for _ in range(160):
    x, y = rnd.randint(30, 1370), rnd.randint(150, 700)
    s.append(f'<circle cx="{x}" cy="{y}" r="{rnd.randint(4, 9)}" fill="#C4BBAC" opacity=".8"/>')
for r in (1, 5, 10, 15, 20):
    s.append(f'<line x1="70" x2="1360" y1="{ry(r)}" y2="{ry(r)}" stroke="#B5AC9C" stroke-width="1.2" stroke-dasharray="3 7"/>' + T(60, ry(r) + 5, f"{r}위", 13, 800, "#7A7062", "end"))
def hold(x, r, col, lab, sub, dashed=False, anchor="start", dx=26, dy=0):
    st = f'fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="6 5"' if dashed else f'fill="{col}"'
    return (f'<ellipse cx="{x}" cy="{ry(r)}" rx="18" ry="14" {st}/>' + T(x + (dx if anchor == "start" else -dx), ry(r) - 2 + dy, lab, 18, 900, col if not dashed else "#4A4232", anchor)
            + T(x + (dx if anchor == "start" else -dx), ry(r) + 18 + dy, sub, 13, 800, "#5E564A", anchor))
# 레스터
s.append(f'<path d="M 230 {ry(15)} C 260 {ry(10)} 300 {ry(5)} 330 {ry(1)}" fill="none" stroke="{UD}" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round"/>')
s.append(hold(230, 15, UD, "연봉 15위", "레스터 2015-16 시작", anchor="end") + hold(330, 1, UD, "우승", "시즌 전 배당 5000 대 1"))
# 코모
pts = ((640, 10, "10위", "2024-25 (승격 첫해)", False), (860, 11, "예상 11위", "2025-26 시즌 전 Opta", True), (960, 4, "실제 4위", "2025-26 → 첫 챔스", False),
       (1150, 2, "예상 우승 후보 2위", "2026-27 Opta 13.6%", True), (1180, 4, "지금 4위", "10/18 기준", False))
s.append(f'<path d="M 640 {ry(10)} C 760 {ry(9)} 880 {ry(6)} 960 {ry(4)} S 1120 {ry(4)} 1180 {ry(4)}" fill="none" stroke="{TOP}" stroke-width="5" stroke-linecap="round" opacity=".7"/>')
for x, r, lab, sub, d in pts:
    s.append(hold(x, r, TOP if not d else "#7A8CB5", lab, sub, d, "end" if lab == "10위" else "start", dy=36 if lab in ("실제 4위", "지금 4위") else 0))
s.append('</svg>')
F["U16_como_climb"] = frame(16, "코모", "예상 11위가 4위로, 올해는 <em>우승 후보</em>", "".join(s)
    + stamp(520, 640, "언더독 자리에서 강자 자리로", "#22335A"),
    "코모: Opta 시즌 전 예상·세리에A 최종 순위·10/18 순위 / 레스터: 2015-16 시즌 전 배당·연봉 순위(보도) · 점선 고리 = 시즌 전 예상")

# ---- 17 방송은 「언더독」, 기사 제목은 「복수」 (숫자: 기사 제목 쪽지 무더기) ----
W17 = (("복수", 14, RED), ("리벤지", 13, RED), ("설욕", 6, RED), ("언더독", 2, UD), ("방출", 0, "#8A8272"), ("잡초", 0, "#8A8272"))
s = [SVG0, '<rect width="1400" height="800" fill="#EFE9DE"/>']
for i, (wd, n, col) in enumerate(W17):
    x = 150 + i * 196; base = 600
    for k in range(n):
        rot = rnd.uniform(-5, 5); y = base - 22 - k * 24
        s.append(f'<g transform="rotate({rot:.1f} {x + 70} {y + 9})"><rect x="{x}" y="{y}" width="140" height="18" rx="2" fill="#FFFCF5" stroke="#CFC4AE"/>'
                 f'<rect x="{x + 8}" y="{y + 6}" width="{40 + (k * 13) % 70}" height="6" rx="2" fill="{col}" opacity=".85"/></g>')
    s.append(f'<line x1="{x - 10}" x2="{x + 150}" y1="{base}" y2="{base}" stroke="#8A7F6A" stroke-width="3"/>')
    s.append(T(x + 70, base + 44, f"「{wd}」", 24, 900, col) + T(x + 70, base + 72, f"제목 {n}건", 16, 800, "#4A4232"))
    if n: s.append(T(x + 70, base - 32 - n * 24, str(n), 30, 900, col))
s.append('</svg>')
F["U17_headline_words"] = frame(17, "한국 반응", "방송은 「언더독」을 띄웠고, 기사 제목은 <em>「복수」</em>", "".join(s)
    + tag(870, 250, "2건 모두", "「언더독스」 — 팀 이름을 잘못 쓴 제목", UD, 2, small=True, w=320),
    "네이버 뉴스 검색 API로 모은 「신인감독 김연경2」·「원더독스」 기사 549건(10.4~10.19) 제목 직접 셈 · 쪽지 한 장 = 제목 한 건")

# ---- 18 「언더독」 검색이 뛴 날 (숫자: 데이터랩 일별 맥박) ----
raw = json.load(open(HERE_ := pathlib.Path(__file__).resolve().parent.parent / "base data" / "_raw_데이터랩_언더독_2026-10-19.json", encoding="utf-8"))
ser = [g for g in raw["date_시즌2검색어포함"]["results"] if g["title"] == "언더독"][0]["data"]
D = {dt.date.fromisoformat(p["period"]): p["ratio"] for p in ser}
d0, d1 = dt.date(2025, 9, 1), dt.date(2026, 10, 17)
days = [d0 + dt.timedelta(i) for i in range((d1 - d0).days + 1)]
mx = max(D.get(d, 0) for d in days)
X0, X1, Y0, Y1 = 80, 1340, 600, 250
def px(d): return X0 + (d - d0).days / (d1 - d0).days * (X1 - X0)
def py(v): return Y0 - v / mx * (Y0 - Y1)
s = [SVG0, '<rect width="1400" height="800" fill="#F3F0E9"/>']
for gx in range(X0, X1, 40): s.append(f'<line x1="{gx}" x2="{gx}" y1="{Y1 - 20}" y2="{Y0}" stroke="#E6DFD2" stroke-width="1"/>')
for gy in range(int(Y1) - 20, Y0, 40): s.append(f'<line x1="{X0}" x2="{X1}" y1="{gy}" y2="{gy}" stroke="#E6DFD2" stroke-width="1"/>')
s.append('<polyline points="%s" fill="none" stroke="#C8463C" stroke-width="2.6" stroke-linejoin="round"/>' % " ".join("%.1f,%.1f" % (px(d), py(D.get(d, 0))) for d in days))
for m in ((2025, 10, 1), (2026, 1, 1), (2026, 4, 1), (2026, 7, 1), (2026, 10, 1)):
    dd = dt.date(*m); s.append(T(px(dd), Y0 + 28, f"{dd.year % 100}.{dd.month}", 14, 800, "#7A7062"))
for dd, lab in ((dt.date(2025, 9, 28), "시즌1 첫 방송"), (dt.date(2026, 10, 11), "시즌2 첫 방송")):
    s.append(f'<circle cx="{px(dd):.1f}" cy="{py(D[dd]):.1f}" r="8" fill="{UD}" stroke="#FFFCF5" stroke-width="3"/>')
s.append('</svg>')
p1, p2 = dt.date(2025, 9, 28), dt.date(2026, 10, 11)
F["U18_search_pulse"] = frame(18, "한국 반응", "「언더독」 검색은 <em>첫 방송 날</em> 뛰었다", "".join(s)
    + tag(int(px(p1)) + 26, int(py(D[p1])) - 20, "3.4배", "시즌1 첫 방송 날 · 전날 대비", UD, -2, small=True)
    + tag(int(px(p2)) - 290, int(py(D[p2])) - 150, "2.3배", "시즌2 첫 방송 날 · 높이는 시즌1의 약 28%", UD, 2, small=True, w=260)
    + tag(560, 140, "41%", "2025년 9~12월 「언더독」 기사 206건 중 「김연경」과 함께 나온 84건(빅카인즈)", "#22335A", 1, small=True, w=430),
    "네이버 데이터랩 검색어트렌드(일별 상대값, 2025.9.1~2026.10.17, 10.18 값 없음) · 빅카인즈 기사 검색 · 「언더독 효과」 검색은 33개월 내내 0")

if __name__ == "__main__":
    render(F, sys.argv[1:] or None)
