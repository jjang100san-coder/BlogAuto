# -*- coding: utf-8 -*-
"""v4(10/15 밤) — 반대편 영상(「생존 매수·전세 멸종」) 숫자를 실거래로 대 본 카드 1장 추가.
숫자: base data\\로직근거\\out\\v4_jeonse_share.json · v4_wolbu_check.json(국토부 실거래 서울 25개 구 직접 계산)."""
import os, json
import make_cards as M
import make_cards_v2 as V2
import make_cards_v3 as V3
from make_cards import (canvas, box, foot, ctext, F_S, F_SM, F_M, F_L, F_BIG,
                        INK, GRAY, RED, GREEN, AMBER, BLUE, LIGHT, PINK, MINT, SAND, WHITE, NAVY, DIM, save, reuse, REUSE)
OUTJ = os.path.join(M.ROOT, "base data", "로직근거", "out")
JS = json.load(open(os.path.join(OUTJ, "v4_jeonse_share.json"), encoding="utf-8"))
WB = json.load(open(os.path.join(OUTJ, "v4_wolbu_check.json"), encoding="utf-8"))


def card_jeonse(name):
    im, d = canvas("전세는 줄고, 세입자는 눌러앉고, 싼 집 거래는 늘었다",
                   "서울 25개 구 아파트 실거래 — 「생존 매수」를 말하는 쪽이 보는 숫자를 대 보니")
    panels = [
        ("전월세 중 전세 비중", [("21.8~22.1", JS["2021.8~2022.1"]["전세비중"]), ("23.8~24.1", JS["2023.8~2024.1"]["전세비중"]),
                            ("24.8~25.1", JS["2024.8~2025.1"]["전세비중"]), ("26.4~9", JS["2026.4~9"]["전세비중"])], BLUE),
        ("계약 중 갱신 비율", [("23.8~24.1", WB["③_갱신"]["2023.8~2024.1"]["갱신비율(신규+갱신 중)"]),
                         ("24.8~25.1", WB["③_갱신"]["2024.8~2025.1"]["갱신비율(신규+갱신 중)"]),
                         ("26.4~9", WB["③_갱신"]["2026.4~9"]["갱신비율(신규+갱신 중)"])], AMBER),
        ("매매 중 6억 이하 비중", [("24.12~25.9", WB["①_2024.12~2025.9"]["6억 이하"]), ("25.11~26.8", WB["①_2025.11~2026.8"]["6억 이하"]),
                             ("26.8", WB["①_2026.8"]["6억 이하"])], RED)]
    for p, (title, vals, col) in enumerate(panels):
        x0 = 90 + p * 415
        d.rounded_rectangle([x0, 150, x0 + 390, 590], radius=20, fill=WHITE, outline=(225, 225, 220), width=2)
        ctext(d, x0 + 195, 168, title, F_M, col)
        base, top = 530, 230
        bw = 70 if len(vals) == 4 else 90
        gap = (390 - 40 - bw * len(vals)) / max(1, len(vals) - 1)
        for i, (lab, v) in enumerate(vals):
            x = x0 + 20 + i * (bw + gap)
            h = v / 70 * (base - top)
            c = col if i == len(vals) - 1 else DIM
            d.rectangle([x, base - h, x + bw, base], fill=c)
            ctext(d, x + bw / 2, base - h - 30, f"{v:.1f}%", F_S, c if c != DIM else GRAY)
            ctext(d, x + bw / 2, base + 10, lab, F_SM, INK)
    box(d, (90, 615, 1310, 705), SAND,
        "전세 비중은 네 시기 중 처음 절반 아래로 내려왔고, 갱신 계약 비율은 46.7%로 올랐다. 6억 이하 거래 비중도 늘었다.\n「멸종」은 과장이지만 방향은 숫자와 맞는다",
        F_S, INK)
    foot(d, "국토교통부 아파트 전월세·매매 실거래(서울 25개 구, 계약일, 매매는 해제 제외) 직접 계산 · 전세 = 월세 0 · 2026.9 계약분은 덜 찼음")
    save(im, name)


if __name__ == "__main__":
    ORDER = [("01_two_dates.png", None), ("03_logic_pillars.png", None), ("05_supply_parcel.png", None), (None, M.card_supply),
             ("R2_supply_path.png", None), ("R3_first_home_loan.png", None), (None, V2.card_firsthome), (None, V2.card_loan),
             ("07_rate_jump.png", None), (None, V3.card_rate), ("09_two_big_drops.png", None), (None, V2.card_wait),
             (None, V2.card_ahead), (None, V3.card_now_mix), (None, V3.card_phases), (None, V2.card_1989), (None, M.card_bogeum),
             (None, card_jeonse), (None, V2.card_score), ("14_same_numbers.png", None), ("15_my_calendar.png", None)]
    for f in os.listdir(M.HERE):
        if f.startswith("261015_") and f.endswith(".png") and f != "261015_1.png": os.remove(os.path.join(M.HERE, f))
    for i, (src, fn) in enumerate(ORDER, start=2):
        n = f"261015_{i}.png"
        if src: reuse(src, n, REUSE[src])
        else: fn(n)
