# -*- coding: utf-8 -*-
"""블로그연대기 3편 자체 제작 카드. 영상 프레임은 한 장도 쓰지 않는다 (스킬 5단계, 지침 6-7).
1·2편과 같은 판형(1080 정사각, 미색 배경, Noto Sans KR)이고 주색은 파랑 대신 판정 색을 쓴다."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.dirname(os.path.abspath(__file__))   # 초안 md 와 같은 폴더 (fill_editor 가 여기서 찾는다)
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
BG, INK, SUB, LINE = "#FBFBF9", "#111111", "#555555", "#DDDDDD"
GREEN, AMBER, RED, SKULL, GRAY = "#2E9E5B", "#E0A21B", "#E24A4A", "#7A1F1F", "#9AA0A6"
W = 1080

def font(size, weight="Black"):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def text(d, xy, s, size, weight="Black", fill=INK, anchor="la"):
    d.text(xy, s, font=font(size, weight), fill=fill, anchor=anchor)

def xmark(d, cx, cy, r, fill, w):
    d.line([cx - r, cy - r, cx + r, cy + r], fill=fill, width=w)
    d.line([cx - r, cy + r, cx + r, cy - r], fill=fill, width=w)

def omark(d, cx, cy, r, fill, w):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=w)

def canvas(h=W):
    im = Image.new("RGB", (W, h), BG); return im, ImageDraw.Draw(im)

# 판정 순서 (영상 번호 01~23, 종합 문서 3절 표 그대로)
V = {1:"R",2:"S",3:"G",4:"G",5:"R",6:"S",7:"S",8:"R",9:"G",10:"Y",11:"G",12:"S",
     13:"G",14:"Y",15:"Y",16:"G",17:"Y",18:"G",19:"S",20:"S",21:"R",22:"Y",23:"O"}
COL = {"G":GREEN,"Y":AMBER,"R":RED,"S":SKULL,"O":GRAY}
cnt = {k: sum(1 for v in V.values() if v == k) for k in COL}
assert cnt == {"G":7,"Y":5,"R":4,"S":6,"O":1}, cnt

# ① 썸네일 — 23칸. 축소해도 색 덩어리와 큰 글자만 남게
def save(im, name):
    p = os.path.join(OUT, name); im.save(p, optimize=True); print("saved", p, im.size)

def card_thumb():
    im2, d2 = canvas()
    text(d2, (70, 60), "유튜브 23편", 112)
    text(d2, (70, 190), "끝까지 봤어", 112)
    order = ["G"]*7 + ["Y"]*5 + ["R"]*4 + ["S"]*6 + ["O"]
    cell, gap, x0, y0 = 128, 14, 70, 360
    for i, k in enumerate(order):
        r, c = divmod(i, 7)
        x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
        d2.rounded_rectangle([x, y, x + cell, y + cell], 16, fill=COL[k])
        if k == "S": xmark(d2, x + cell/2, y + cell/2, 34, "#FFFFFF", 14)
    y = y0 + 4 * (cell + gap) + 28
    items = [("G","믿을 7"),("Y","반반 5"),("R","거를 10"),("O","공식 1")]
    x = 70
    for k, s in items:
        c = RED if k == "R" else COL[k]
        d2.rounded_rectangle([x, y + 8, x + 44, y + 52], 10, fill=c)
        text(d2, (x + 58, y), s, 52)
        x += 58 + d2.textlength(s, font=font(52)) + 44
    save(im2, "yt23_01_thumb.png")

# ② 판정 분포 막대
def card_verdict():
    im, d = canvas()
    text(d, (70, 70), "23편을 가르니까", 76)
    rows = [("믿을 만했어", 7, GREEN, ""), ("반반", 5, AMBER, ""), ("거를 영상", 10, RED, "그중 6편은 최악 후킹"), ("네이버 공식", 1, GRAY, "")]
    y, maxw, x0 = 250, 540, 360
    for label, n, col, note in rows:
        text(d, (70, y + 14), label, 50, "Bold")
        bw = maxw * n / 10
        d.rounded_rectangle([x0, y, x0 + bw, y + 110], 14, fill=col)
        if label == "거를 영상":   # 거를 10 중 최악 6을 진하게
            d.rounded_rectangle([x0 + maxw * 4 / 10, y, x0 + bw, y + 110], 14, fill=SKULL)
            d.rectangle([x0 + maxw * 4 / 10, y, x0 + maxw * 4 / 10 + 20, y + 110], fill=SKULL)
        text(d, (x0 + bw + 20, y + 55), str(n), 70, anchor="lm")
        if note: text(d, (x0, y + 128), note, 38, "Bold", fill=SKULL)
        y += 200 if note else 170
    d.line([70, 960, W - 70, 960], fill=LINE, width=2)
    text(d, (70, 985), "같은 채널 영상 세 편이 믿을·반반·거를로 갈리기도 했어", 36, "Medium", fill=SUB)
    save(im, "yt23_02_verdict.png")

# ③ 제목의 약속 vs 본문 — ✕ 6편 (영상에서 확인한 것만)
HOOK6 = [
    ("네이버가 무너지고 있다", "출연자: \"아예 무너지지는 않을 것\""),
    ("AI로 2분 만에 월 2400만원", "AI 글 그대로 복사, 해외 사진 캡처"),
    ("처음부터 직접 한 달 키워 봤다", "예전 체험단 블로그 계정을 다시 씀"),
    ("왕초보가 1000만원 버는 기회", "10개 분야에 1명씩, 총 10명 지원금"),
    ("월 1억 인생역전 싹 다 공개", "1억은 대행 업체의 매출"),
    ("워드프레스 하면 안 되는 이유", "결론: \"워드프레스로 여전히 가능\""),
]
def card_hook6():
    im, d = canvas(1350)
    text(d, (70, 60), "제목이 약속한 것", 64)
    text(d, (70, 145), "영상 안에서 나온 것", 64, fill=SKULL)
    y = 280
    for a, b in HOOK6:
        text(d, (70, y), a, 44, "Black")
        text(d, (70, y + 62), "→ " + b, 38, "Medium", fill=SKULL)
        y += 150
        d.line([70, y - 22, W - 70, y - 22], fill=LINE, width=2)
    text(d, (70, 1260), "제목은 영상 제목을 줄여 옮긴 것", 32, "Medium", fill=SUB)
    save(im, "yt23_03_hook6.png")

# ④ 거를 신호 / 가져올 것
def card_signals():
    im, d = canvas(1350)
    text(d, (70, 60), "거를 영상은 이게 보였어", 60, fill=RED)
    bad = ["최고의 하루 수익을 제목에", "제목과 결론이 반대", "소수 상금을 누구나의 기회로",
           "AI 글 복사, 겪은 척", "남의 사진 캡처·세탁", "반대 의견에 인신공격", "끝은 강의·대행 영업"]
    y = 160
    for s in bad:
        xmark(d, 92, y + 30, 16, RED, 7); text(d, (135, y), s, 44, "Bold"); y += 76
    y += 40
    text(d, (70, y), "믿을 영상은 이걸 먼저 보여 줬어", 60, fill=GREEN); y += 100
    good = ["실패담과 작은 실적", "네이버 공지 원문", "규칙 위반 경고", "경험을 쓰라는 말"]
    for s in good:
        omark(d, 92, y + 30, 18, GREEN, 7); text(d, (135, y), s, 44, "Bold"); y += 76
    save(im, "yt23_04_signals.png")

# ⑤ 네이버가 밝힌 숫자 (뉴스핌 2026-08-07, 아이뉴스24 2026-06-04 보도)
def card_naver():
    im, d = canvas()
    text(d, (70, 70), "네이버가 직접 밝힌 것", 68)
    rows = [("애드포스트 지급 규모", "약 14% 증가", "2025년 2월 → 2026년 6월"),
            ("애드포스트+브랜드커넥트+메이트", "약 2배", "같은 기간 합산"),
            ("네이버 메이트", "매달 약 3,000명", "AI 브리핑 인용 수 기준")]
    y = 230
    for a, b, c in rows:
        text(d, (70, y), a, 40, "Bold", fill=SUB)
        text(d, (70, y + 58), b, 84)
        text(d, (70, y + 170), c, 34, "Medium", fill=SUB)
        y += 250
    text(d, (70, 1000), "출처: 네이버 발표 보도 (뉴스핌 8.7, 아이뉴스24 6.4)", 30, "Medium", fill=SUB)
    save(im, "yt23_05_naver.png")

# ①-b 썸네일 대안 — 숫자 대비형. 피드에서 "7 : 10" 이 먼저 읽히게
def card_thumb_b():
    im, d = canvas()
    text(d, (70, 70), "애드포스트 유튜브 23편", 64, "Bold", fill=SUB)
    text(d, (70, 170), "끝까지 봤어", 64, "Bold", fill=SUB)
    d.rounded_rectangle([70, 330, 520, 830], 28, fill=GREEN)
    d.rounded_rectangle([560, 330, 1010, 830], 28, fill=RED)
    text(d, (295, 560), "7", 300, fill="#FFFFFF", anchor="mm")
    text(d, (785, 560), "10", 300, fill="#FFFFFF", anchor="mm")
    text(d, (295, 760), "믿을 영상", 56, fill="#FFFFFF", anchor="mm")
    text(d, (785, 760), "거를 영상", 56, fill="#FFFFFF", anchor="mm")
    text(d, (70, 900), "반반 5편, 네이버 공식 1편", 44, "Bold", fill=SUB)
    save(im, "yt23_01b_thumb_alt.png")

# ⑥ 애드포스트 — 영상에서 한 말 vs 내 보류 메일 (화면 자막 대조 끝난 문장만)
def card_adpost():
    im, d = canvas(1350)
    text(d, (70, 60), "애드포스트,", 64)
    text(d, (70, 145), "영상이 한 말과 내 메일", 64)
    rows = [
        ("\"네이버 애드포스트 승인 너무 쉽습니다\"", "8월 31일 보류, 9월 21일 또 보류", RED),
        ("\"승인이 안 된 사람 한 번도 못 봤다\"", "여기 한 명 있어", RED),
        ("\"지난달 기준에 블로그 방문자 숫자로 판단\"", "내 메일에도 \"지난 달 기준\"", GREEN),
        ("\"네이버가 공식 발표한 방문자 수는 없어요\"", "내 메일에도 숫자는 없었어", GREEN),
    ]
    y = 290
    for q, me, col in rows:
        d.rectangle([70, y, 82, y + 190], fill=col)
        text(d, (110, y), "영상", 30, "Bold", fill=SUB)
        text(d, (110, y + 40), q, 40, "Bold")
        text(d, (110, y + 110), "나", 30, "Bold", fill=SUB)
        text(d, (160, y + 102), me, 44, fill=col)
        y += 245
    text(d, (70, 1265), "빨강은 내 경험과 어긋난 말, 초록은 들어맞은 말", 32, "Medium", fill=SUB)
    save(im, "yt23_06_adpost.png")

# ⑦ 사진 "세탁" — 바꿔도 남의 것
def card_wash():
    im, d = canvas()
    text(d, (70, 70), "남의 사진은", 76)
    text(d, (70, 170), "바꿔도 남의 사진이야", 76, fill=RED)
    steps = ["남의 사진", "캡처", "그림판으로 조금 변형", "AI로 다시 그리기"]
    y = 330
    for i, s in enumerate(steps):
        d.rounded_rectangle([70, y, 700, y + 96], 18, outline=RED if i else INK, width=5)
        text(d, (100, y + 48), s, 46, "Bold", anchor="lm")
        if i < len(steps) - 1:
            d.polygon([(385, y + 108), (415, y + 108), (400, y + 134)], fill=SUB)
        y += 140
    text(d, (740, 560), "=", 120, fill=RED, anchor="lm")
    text(d, (740, 690), "출처만", 50, fill=RED)
    text(d, (740, 755), "지워짐", 50, fill=RED)
    text(d, (70, 940), "23편 중 4편이 이 방법을 권했어", 40, "Bold", fill=SUB)
    save(im, "yt23_07_wash.png")

# ⑧ 네이버가 말한 방향 — 공식 유튜브 《B안인드》 EP.4 (23번) 발언 그대로의 요지
def card_direction():
    im, d = canvas()
    text(d, (70, 70), "네이버 공식 유튜브가 말한 것", 58)
    # 지금까지
    d.rounded_rectangle([70, 200, 1010, 470], 24, fill="#EEEEEA")
    text(d, (110, 230), "지금까지", 40, "Bold", fill=SUB)
    text(d, (110, 300), "블로그로 오는 길은", 50, "Bold")
    text(d, (110, 370), "검색과 지도 비중이 높았다", 50)
    d.polygon([(510, 495), (570, 495), (540, 545)], fill=INK)
    # 앞으로
    d.rounded_rectangle([70, 570, 1010, 860], 24, fill=GREEN)
    text(d, (110, 600), "앞으로", 40, "Bold", fill="#FFFFFF")
    text(d, (110, 670), "블로그 자체를 키운다", 50, fill="#FFFFFF")
    text(d, (110, 745), "읽는 쪽 = 좋아할 글 추천", 50, fill="#FFFFFF")
    text(d, (70, 920), "네이버 공식 유튜브 《B안인드》 EP.4 리브랜딩 편", 32, "Medium", fill=SUB)
    text(d, (70, 970), "블로그 리브랜딩 담당 디자이너 발언 요지", 32, "Medium", fill=SUB)
    save(im, "yt23_08_direction.png")

# ⑨ 10월 1일까지 — 할 것 / 안 할 것
def card_plan():
    im, d = canvas()
    text(d, (70, 70), "10월 1일 재신청까지", 70)
    colx = [(70, "할 것", GREEN, ["주제는 계속 넓히기", "직접 찍은 사진·내 통계", "겪었거나 확인한 것만", "소제목에 정확한 이름"]),
            (560, "안 할 것", RED, ["남의 사진 캡처·세탁", "AI 글 그대로 붙이기", "확인 안 된 소문 옮기기", "제목과 다른 본문"])]
    for x, head, col, items in colx:
        d.rounded_rectangle([x, 210, x + 450, 300], 18, fill=col)
        text(d, (x + 225, 255), head, 50, fill="#FFFFFF", anchor="mm")
        y = 350
        for s in items:
            text(d, (x + 10, y), s, 42, "Bold"); y += 90
    d.line([70, 760, W - 70, 760], fill=LINE, width=2)
    text(d, (70, 800), "아직 모르는 것", 44, fill=SUB)
    text(d, (70, 870), "10월 1일 애드포스트 결과", 44, "Bold")
    text(d, (70, 935), "AI 브리핑 인용이 작은 블로그에도 붙는지", 44, "Bold")
    save(im, "yt23_09_plan.png")

if __name__ == "__main__":
    card_thumb(); card_verdict(); card_hook6(); card_signals(); card_naver()
    card_thumb_b(); card_adpost(); card_wash(); card_direction(); card_plan()
