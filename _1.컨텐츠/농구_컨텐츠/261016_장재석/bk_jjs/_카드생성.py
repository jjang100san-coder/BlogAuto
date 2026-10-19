# -*- coding: utf-8 -*-
r"""금메달 시리즈 11편(장재석) 카드 01~04 — 농구 지침 6-0 「코트 카드」.
숫자는 종합분석_장재석.md · base data\프로필_KBL확인·2차수집 그대로(KBL 10/19 kbl_gamelog.py 290539). 계산값 없음.
결승 출전 시간은 기사끼리 갈려(28분 56초 / 14분 15초) 카드에 넣지 않는다. 「8cm」는 KBS 9/14 내레이션 값.
썸네일은 AI 장면(bk_jjs_ai_01)이라 카드는 전부 본문용(마스터 5-4)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
sys.stdout.reconfigure(encoding="utf-8")
from basketball_cards_base import *

O = lambda n: os.path.join(HERE, n)


def jumpball_vs_fit(path, kicker, title, left_, right_, rows, conclusion, source, num_size=165):
    """basketball_cards_base.jumpball_vs 와 같은 그림 — 세 자리 키(203·211)가 센터 서클·VS를 덮지 않게 큰 숫자만 줄인 사본(11편 10/19)."""
    S = 1080; im = Image.new("RGB", (S, S), COAL); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S / 2, S], fill=ORNG); wood(d, S / 2, 0, S, S)
    for y in range(0, S, 36): d.line([0, y, S / 2, y], fill=ORNG_S, width=2)
    cy = 470; R = 150
    d.line([S / 2, 0, S / 2, S], fill=LINE, width=6)
    d.ellipse([S / 2 - R, cy - R, S / 2 + R, cy + R], outline=LINE, width=6)
    d.ellipse([S / 2 - 64, cy - 64, S / 2 + 64, cy + 64], fill=COAL, outline=LINE, width=6)
    d.text((S / 2, cy), "VS", font=F(50), fill=LINE, anchor="mm")
    d.rectangle([0, 0, S, 200], fill=COAL)
    d.text((64, 56), kicker, font=F(30, "Bold"), fill=ORNG)
    d.text((60, 100), title, font=F(62), fill=LINE)
    for side, (num, nm, ds) in ((0, left_), (1, right_)):
        x = 60 if side == 0 else S - 60; an = "ls" if side == 0 else "rs"
        fg = COAL if side == 0 else LINE
        d.text((x, 600), num, font=F(num_size), fill=fg, anchor=an)
        d.text((x, 666), nm, font=F(48), fill=fg, anchor=an)
        d.text((x, 712), ds, font=F(26, "Bold"), fill=(80, 36, 12) if side == 0 else MUTE, anchor=an)
    d.rectangle([0, 760, S, S], fill=COAL)
    y = 782
    for k, v in rows:
        d.text((64, y + 8), k, font=F(28, "Medium"), fill=MUTE); d.text((S - 64, y), v, font=F(40), fill=LINE, anchor="ra")
        y += 58
    footer(d, S, conclusion, source, 34)
    save(im, path)

namecard_front(O("bk_jjs_01_namecard.png"), "황금세대 12인", "No.11 / 12", "31", "장재석",
               "부산 KCC · 중앙대 · 2012 드래프트 1순위", ["센터", "최고참 · 최장신"],
               "아시안게임 조별 일본전 (9월 13일)", [("18", "득점"), ("8", "리바운드"), ("35살", "첫 아시안게임")],
               "네 번째 만에 온 아시안게임",
               "프로필: KBL 공식 홈페이지 · 일본전 기록: 엑스포츠뉴스(9월 26일) · 직접 만든 이미지")

ball_timeline(O("bk_jjs_02_timeline.png"), "장재석 · 장키치", "아시안게임 3전 4기", None,
              [("step", "2010년", "「따는 줄 알았어요」", "대학 2학년"),
               ("step", "2012년", "드래프트 1순위", "부산 KT"),
               ("gap", "2014년 7월 21일", "대표팀 명단에서 빠짐", "이승현·최준용도"),
               ("key", "2015-16 시즌", "챔피언결정전 우승", "고양 오리온"),
               ("gap", "2017~2019년", "공익근무", "2018년엔 안 감"),
               ("step", "2020-21 시즌", "시즌 평균 최고 9.1점", "현대모비스"),
               ("gap", "2023년", "항저우 앞 어깨 부상", ""),
               ("key", "2025-26 시즌", "KCC 통합 우승", "트레이드 첫해"),
               ("key", "2026년 9월 20일", "첫 아시안게임 금메달", "35살")],
              "「내려놓으니까 또 가게 됐어」",
              "KBL 공식 홈페이지 · 기사(마이데일리·오마이뉴스) · 크블인생 라이브 · 직접 만든 이미지")

jumpball_vs_fit(O("bk_jjs_03_kirk.png"), "9월 13일 · 아시안게임 조별 일본전 100-83", "키는 8cm 작았어",
            ("203", "장재석", "부산 KCC · 센터"), ("211", "커크", "일본 귀화 센터"),
            [("조별 일본전 · 이승현 파울 2개 뒤 투입", "18점 8리바운드"), ("결승 일본전", "블록 세 차례")],
            "픽앤롤 수비가 약하다고 봤다",
            "키: KBL 공식 홈페이지 · KBS(9월 14일) · 기록: 엑스포츠뉴스(9월 26일) · 직접 만든 이미지")

game_log(O("bk_jjs_04_season.png"), "금메달 뒤 부산 KCC", "데뷔 뒤 가장 오래 뛰는 시즌", "장재석 · 2026-27 프로농구",
         [("10월 3일 · 패 68-103", "창원 LG", 12, 3, False), ("10월 5일 · 승 97-87", "울산 현대모비스", 7, 5, False),
          ("10월 7일 · 승 103-98", "대구 한국가스공사", 8, 2, False), ("10월 10일 · 패 79-85", "원주 DB", 15, 6, False),
          ("10월 11일 · 패 81-87", "수원 KT", 11, 7, False), ("10월 18일 · 패 74-81", "안양 정관장", 7, 5, False)],
         "평균 10.0점 · 4.7리바운드", "많이 뛸 수 있을 때 열심히",
         "기록: KBL 공식 홈페이지(10월 19일) · 2·3쿼터 외국 선수 2명 규정 · 직접 만든 이미지", scale=20, stat2="리바운드")
