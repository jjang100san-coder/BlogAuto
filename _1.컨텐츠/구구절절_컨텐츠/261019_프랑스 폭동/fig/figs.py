# -*- coding: utf-8 -*-
"""프랑스 폭동 — 장면판 도해. 숫자는 공부노트 1절 사실표(F#)만. 사용: python figs.py [이름 ...]"""
import sys
from scene_base import frame, bg, tag, stamp, render, UD, TOP, RED
GOV, ORG, KR = TOP, UD, "#444444"
F = {}
SVG0 = '<svg width="1400" height="800" viewBox="0 0 1400 800" style="position:absolute;left:0;top:0;font-family:NK">'
def T(x, y, s, size=16, w=800, fill="#1E2330", anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{w}" fill="{fill}" {extra}>{s}</text>'

# ---- 05 4주 노선도 (숫자: 역 하나 = 날짜 하나, 환승역 둘, 종점 빨강) ----
STA = [  # (x, 날짜, 역 이름, 아래 숫자, 색)
    (110, "9.17", "2027 예산 발표<br>교사 파업", "540억 유로 절감", GOV),
    (270, "9월 셋째 주", "크레테유 고교", "시작", GOV),
    (420, "9.28", "학교 180곳", "체포 164", GOV),
    (560, "9.30", "학교 356곳", "체포 625", GOV),
    (700, "10.1", "고교 1,027곳", "체포 1,949", GOV),
    (860, "10.6", "노조 합류", "11/5 파업 예고", ORG),
    (1010, "10.13", "청년·노조 행진", "", GOV),
    (1150, "10.16", "노란 조끼 합류", "경로 합의", ORG),
    (1300, "10.17", "리모주 시청", "체포 2,397", RED),
]
Y = 420
s = [SVG0, '<defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6F3EC"/><stop offset="1" stop-color="#E9E3D6"/></linearGradient></defs>',
     '<rect width="1400" height="800" fill="url(#pg)"/>']
# 바탕 격자(노선도 종이 느낌)
for gx in range(0, 1400, 50): s.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="800" stroke="#E2DCCB" stroke-width="1"/>')
for gy in range(0, 800, 50): s.append(f'<line x1="0" y1="{gy}" x2="1400" y2="{gy}" stroke="#E2DCCB" stroke-width="1"/>')
# 파랑 본선(고교 시위) 9.17 → 10.17
s.append(f'<path d="M {STA[0][0]} {Y} H {STA[-1][0]}" stroke="{GOV}" stroke-width="18" stroke-linecap="round" fill="none"/>')
# 주황 노선(노조) 10.6 에서 아래에서 올라탐 / 노란 조끼 10.16 에서 위에서 올라탐 — 글자와 안 겹치게 수직으로
s.append(f'<path d="M {STA[5][0]} 740 V {Y + 18}" stroke="{ORG}" stroke-width="12" fill="none" stroke-linecap="round"/>')
s.append(f'<path d="M {STA[5][0]} {Y + 18} H {STA[-1][0]}" stroke="{ORG}" stroke-width="12" fill="none" stroke-linecap="round"/>')
s.append(f'<path d="M {STA[7][0]} 150 V {Y - 18}" stroke="{ORG}" stroke-width="12" fill="none" stroke-linecap="round"/>')
s.append(f'<path d="M {STA[7][0]} {Y - 18} H {STA[-1][0]}" stroke="{ORG}" stroke-width="12" fill="none" stroke-linecap="round"/>')
s.append(T(STA[5][0] - 16, 735, "노조(CGT 등) 합류", 15, 900, ORG, "end") + T(STA[7][0] - 16, 160, "노란 조끼 호출 · 틱톡", 15, 900, ORG, "end"))
UP = {0, 2, 4, 5, 8}
for i, (x, d, nm, num, col) in enumerate(STA):
    big = i in (5, 7, 8)
    r = 22 if big else 14
    s.append(f'<circle cx="{x}" cy="{Y}" r="{r}" fill="#FFFCF5" stroke="{col}" stroke-width="{7 if big else 6}"/>')
    if big and i != 8: s.append(f'<circle cx="{x}" cy="{Y}" r="8" fill="{col}"/>')
    if i == 8: s.append(f'<rect x="{x - 16}" y="{Y - 16}" width="32" height="32" rx="6" fill="{RED}"/>')
    up = i in UP
    lines = nm.split("<br>")
    if up:
        ty = Y - 46 - (len(lines) + (1 if num else 0)) * 20 - 8
    else:
        ty = Y + 82
    s.append(T(x, ty, d, 22, 900, col))
    for k, ln in enumerate(lines): s.append(T(x, ty + 24 + k * 20, ln, 15, 800, "#1E2330"))
    if num: s.append(T(x, ty + 24 + len(lines) * 20 + 2, num, 15, 900, col))
s.append(T(1300, Y + 50, "종점", 14, 800, RED))
s.append('</svg>')
F["FR05_four_weeks_map"] = frame(5, "4주", "고교 시위가 시청 화재까지 가는 <em>4주</em>", "".join(s)
    + tag(40, 640, "환승 두 번", "10/6 노조 · 10/16 노란 조끼가 고교 노선에 올라탔다", ORG, -1.5, small=True, w=330)
    + stamp(1000, 700, "한 달 만에 종점", RED),
    "위키 EN·FR(내무부 발표 재인용)·AFP(10/1 1,949)·내무장관 확정(10/17 2,397)·Public Sénat(9/17 예산) · 역 하나 = 날짜 하나, 노선도는 모식")

# ---- 11 우산 하나로 열 명 (개념: AI 장면 + 꼬리표) ----
F["FR11_one_umbrella"] = frame(11, "구조", "노조원은 열에 하나, 협약은 <em>거의 모두</em>에게",
    bg("FR11_umbrella")
    + tag(60, 300, "10.3%", "노조 조직률(2019) · 우산을 든 사람<br>공공 18.1% · 민간 8% 미만", ORG, -2, w=330)
    + tag(990, 200, "98%", "단체협약 적용률 · 우산 아래 들어온 사람", GOV, 2, w=340)
    + stamp(700, 660, "가입은 적고, 적용은 넓다", "#22335A"),
    "DARES 조직률(iFRAP 재인용)·OECD/ICTWSS 협약 적용률 · 거리는 AI 생성 장면(실제 파리 아님, 얼굴 없음)")

if __name__ == "__main__":
    render(F, sys.argv[1:] or None)
