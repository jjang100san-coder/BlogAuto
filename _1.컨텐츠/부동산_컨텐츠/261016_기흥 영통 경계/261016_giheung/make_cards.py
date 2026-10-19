# -*- coding: utf-8 -*-
"""기흥 ↔ 영통 글 카드(10/16). 숫자는 원자료에서 직접 읽는다.
- 부동산원 지수: _부동산데이터_API\\tools 의 nation_summary(R-ONE 월간 매매가격지수 캐시)
- 실거래: _giheung_story.json(giheung_story.py — 국토부 실거래 같은 단지 짝)
- 이슈 단계: base data\\영상\\_공식단계_확인.md 의 🟢 칸(문구는 아래에 옮기고 출처를 foot 에 적는다)
동 이름은 그림에 쓰지 않는다(사용자 결정 10/16 「영통권 기흥」)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "..", "..", "_부동산데이터_API", "tools")
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "구구절절_컨텐츠", "261011_병역특례 논란"))
from make_diagrams import (canvas, box, foot, ctext, arrow, font, F_S, INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, BG, W, H)
_cwd = os.getcwd(); os.chdir(TOOLS)
import nation_summary as NS
os.chdir(_cwd)
F_SM = font(18); F_M = font(24, True); F_L = font(30, True); F_BIG = font(54, True)
NAVY = (40, 60, 110); DIM = (200, 200, 195)
ST = json.load(open(os.path.join(TOOLS, "_giheung_story.json"), encoding="utf-8"))
IDX = NS.load("idx")
P = "경기>경부2권>"
NM = {"수원시": P + "수원시", "용인시": P + "용인시", "영통구": P + "수원시>영통구", "장안구": P + "수원시>장안구",
      "권선구": P + "수원시>권선구", "팔달구": P + "수원시>팔달구", "기흥구": P + "용인시>기흥구", "수지구": P + "용인시>수지구", "처인구": P + "용인시>처인구"}


def ch(nm, a, b):
    s = NS.series(IDX, NM[nm]); return NS.pct(s[a], s[b])


def fmt(x): return f"{x:+.1f}%".replace("-", "-")


def save(im, n): im.save(os.path.join(HERE, n)); print("saved", n)


def bar_h(d, x0, base_x, y, val, scale, col, lab, f=F_M):
    d.text((x0, y + 14), lab, font=f, fill=INK)
    L = abs(val) * scale
    if val >= 0: d.rectangle([base_x, y + 8, base_x + L, y + 52], fill=col)
    else: d.rectangle([base_x - L, y + 8, base_x, y + 52], fill=col)
    d.text((base_x + L + 10 if val >= 0 else base_x + 10, y + 14), fmt(val), font=F_L, fill=col)


# 카드 1 — 시로 보면 용인이 더 올랐다
def card_city(n):
    im, d = canvas("「용인은 덜 올랐다」? 시 전체로는 거의 같다", "부동산원 아파트 매매가격지수, 2023년 1월 → 2026년 9월")
    for i, (nm, col) in enumerate([("수원시", DIM), ("용인시", NAVY)]):
        v = ch(nm, "202301", "202609"); x = 260 + i * 460
        h = v * 22
        d.rectangle([x, 540 - h, x + 220, 540], fill=col)
        ctext(d, x + 110, 540 - h - 70, fmt(v), F_BIG, NAVY if i else GRAY)
        ctext(d, x + 110, 555, nm, F_L, INK)
    d.line([200, 540, 1200, 540], fill=GRAY, width=2)
    box(d, (90, 620, 1310, 700), SAND, "두 시는 거의 같이 올랐다. 용인은 지금(2026.9)이 최고점, 수원은 2021년 고점보다 2.1% 아래. 용인을 끈 건 수지구", F_S, INK)
    foot(d, "한국부동산원 R-ONE 월간 아파트 매매가격지수 직접 계산(수원시 4개 구·용인시 3개 구 전체)")
    save(im, n)


# 카드 2 — 구로 쪼개면
def card_gu(n):
    im, d = canvas("구로 쪼개면, 영통 바로 옆 기흥이 덜 올랐다", "부동산원 아파트 매매가격지수, 2023년 1월 → 2026년 9월")
    rows = sorted(["영통구", "수지구", "권선구", "팔달구", "장안구", "기흥구", "처인구"], key=lambda k: -ch(k, "202301", "202609"))
    for i, nm in enumerate(rows):
        v = ch(nm, "202301", "202609"); y = 150 + i * 70
        city = "수원" if nm in ("영통구", "권선구", "팔달구", "장안구") else "용인"
        col = RED if nm == "영통구" else (BLUE if nm == "기흥구" else DIM)
        bar_h(d, 120, 420, y, v, 30, col, f"{city} {nm}")
    box(d, (90, 650, 1310, 720), SAND, "수원 안에서도 영통만 따로 올랐고, 용인 안에서는 수지가 끌었다. 영통과 붙어 있는 기흥은 그 둘 사이에 끼지 못했다", F_S, INK)
    foot(d, "한국부동산원 R-ONE 월간 아파트 매매가격지수 직접 계산")
    save(im, n)


# 카드 3 — 기흥 안에서도
def card_dong(n):
    G = ST["L3_group"]
    vals = [("영통에 맞닿은 동네", G["A 영통 맞닿음"], RED), ("1.5~3km 떨어진 동네", G["B 1.5~3km"], DIM), ("3km 넘게 떨어진 동네", G["C 3km+"], DIM),
            ("(비교) 기흥구 전체", ST["L2"]["기흥구"], BLUE), ("(비교) 수원 영통구", ST["L2"]["영통구"], NAVY)]
    im, d = canvas("기흥 안에서도 영통에 맞닿은 동네는 달랐다", "같은 단지·같은 면적 실거래 ㎡당 가격 변화, 2023년 → 2026년(1~9월)")
    d.text((960, 150), "전세가율(같은 단지)", font=F_M, fill=NAVY)
    for i, (lab, m, col) in enumerate(vals):
        y = 200 + i * 80
        bar_h(d, 100, 420, y, m["2023->2026"][0], 14, col, lab, F_S)
        d.text((1010, y + 14), f"{m['jeonse'][0]:.1f}%", font=F_L, fill=GRAY)
    box(d, (90, 625, 1310, 715), SAND, "영통에 맞닿은 동네는 기흥 평균의 거의 두 배 올라 영통 쪽에 가까웠다. 비교 시작을 2022·2024년으로 바꿔도 순서는 같았다.\n전세가율은 영통에서 멀수록 높았다", F_S, INK)
    foot(d, "국토교통부 아파트 매매·전월세 실거래(해제 제외) 직접 계산 · 묶음은 영통구 경계까지 지도 거리(브이월드) · 동별 짝이 적어 묶음으로만 표시")
    save(im, n)


# 카드 4 — 언제 벌어졌나
def card_gap(n):
    per = [("2023.1 → 2025.9", "202301", "202509", "둘 다 비규제"), ("2025.9 → 2026.6", "202509", "202606", "영통만 규제"),
           ("2026.6 → 2026.9", "202606", "202609", "둘 다 규제")]
    im, d = canvas("격차는 영통이 규제로 묶이기 전에 벌어졌다", "부동산원 아파트 매매가격지수 구간별 변화 — 영통 vs 기흥")
    for i, (lab, a, b, note) in enumerate(per):
        x = 110 + i * 410
        d.rounded_rectangle([x, 160, x + 380, 600], radius=22, fill=WHITE, outline=(225, 225, 220), width=2)
        ctext(d, x + 190, 180, lab, F_M, INK); ctext(d, x + 190, 220, note, F_S, GRAY)
        for j, (nm, col) in enumerate([("영통구", RED), ("기흥구", BLUE)]):
            v = ch(nm, a, b); bx = x + 70 + j * 140; base = 470
            h = abs(v) * 12
            if v >= 0: d.rectangle([bx, base - h, bx + 100, base], fill=col)
            else: d.rectangle([bx, base, bx + 100, base + h], fill=col)
            ctext(d, bx + 50, (base - h - 40) if v >= 0 else base + h + 8, fmt(v), F_M, col)
            ctext(d, bx + 50, 572, nm[:2], F_S, INK)
        d.line([x + 40, 470, x + 340, 470], fill=GRAY, width=2)
    box(d, (90, 630, 1310, 710), SAND, "영통이 규제로 묶이기 전 2년 9개월 동안 영통은 오르고 기흥은 내렸다. 그 뒤로는 둘이 거의 같이 움직였다", F_S, INK)
    foot(d, "한국부동산원 R-ONE 월간 지수 직접 계산 · 영통 규제·토지거래허가 2025.10(10·15 대책), 기흥 규제지역 2026.7.1·토허 2026.7.5~")
    save(im, n)


# 카드 5 — 이름은 영통, 주소는 기흥
def card_border(n):
    im, d = canvas("생활은 영통, 주소와 학교는 용인", "경계가 만드는 일 — 공식 자료로 확인한 것만")
    tiles = [("이름", "영통역 이름을 단 분양 광고", "「행정상으로는 용인이지만」\n(광고 화면 문구)"),
             ("학교", "중학군은 용인 쪽", "2027학년도 고시상 수원 영통\n중학군과 공동학구 없음"),
             ("경계", "2019년 9월 경계 조정", "수원·용인이 땅 일부를 맞바꿨다\n(대통령령, 2019.9.13 시행)")]
    for i, (h, big, sub) in enumerate(tiles):
        x = 90 + i * 410
        d.rounded_rectangle([x, 160, x + 380, 600], radius=22, fill=LIGHT if i != 1 else MINT)
        ctext(d, x + 190, 190, h, F_M, GRAY)
        for j, ln in enumerate(big.split("\n")): ctext(d, x + 190, 280 + j * 44, ln, F_L, INK)
        for j, ln in enumerate(sub.split("\n")): ctext(d, x + 190, 420 + j * 32, ln, F_S, GRAY)
    box(d, (90, 625, 1310, 705), SAND, "장 보는 곳·지하철역은 영통인데, 시청·학교·집값 통계는 용인으로 잡힌다", F_S, INK)
    foot(d, "경기도교육청 2027학년도 중학교 학교군 고시 · 대통령령 제30036호 · 분양 광고 화면은 영상 두 판독으로 확인(단지명 생략)")
    save(im, n)


# 카드 6 — 호재는 어디까지 왔나
def card_issue(n):
    im, d = canvas("말 많은 호재, 공식 단계는 여기까지", "국토부·철도공단·경기도·용인시·수원시 원문으로 확인(2026년 10월 16일)")
    rows = [("GTX-A", "구성역 2024.6 개통 — 기흥역은 GTX 역이 아니다", GREEN),
            ("인덕원~동탄선", "공사 중, 공정률 20.4%(2026.6) — 공식 개통 연도 없음", AMBER),
            ("용인 플랫폼시티", "2025.3 착공식, 준공 예정 2030년", AMBER),
            ("영통 노후계획도시", "기본계획 목표 2026.12로 늦춰짐 — 선도지구 지정 없음", AMBER),
            ("새 아파트 입주", "기흥 2027년 0세대 · 영통 2027년 상반기 580세대", BLUE)]
    for i, (a, b, col) in enumerate(rows):
        y = 160 + i * 92
        d.rounded_rectangle([90, y, 1310, y + 78], radius=14, fill=WHITE, outline=(225, 225, 220), width=2)
        d.rounded_rectangle([90, y, 110, y + 78], radius=6, fill=col)
        d.text((135, y + 22), a, font=F_M, fill=INK)
        d.text((430, y + 25), b, font=F_S, fill=INK)
    foot(d, "국가철도공단(2026.6)·국토부·경기도 보도자료·수원시의회(2026.2.2)·부동산원 입주예정물량 · 「예정」은 확정 아님")
    save(im, n)


if __name__ == "__main__":
    for i, fn in enumerate([card_city, card_gu, card_dong, card_gap, card_border, card_issue], start=2):
        fn(f"261016_{i}.png")
