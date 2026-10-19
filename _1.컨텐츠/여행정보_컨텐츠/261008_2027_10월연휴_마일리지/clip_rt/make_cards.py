# 복귀편 클립 끝 종합 카드 4장(음성 없이 3초씩) — 10/11 사용자: 「글만 듣고는 그래서 뭐가 남았다는 거야? → 남은 좌석 종합을 이미지로」
# 숫자는 발행본(224436602778) 그대로 + 더하기·빼기만(18 = 20-2, 156 = 158-2, 70 = 96-26, 78 = 3+70+5)
# 장면 칸 크기(1080 × 1070, shorts TOP~BOT)에 맞춰 card_*.png 를 만든다
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from PIL import Image, ImageDraw
import tactics as T

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1070
BG = (16, 22, 38); LINE = (60, 70, 95); WHITE = (255, 255, 255); GRAY = (165, 172, 190)
GREEN = (80, 220, 140); ORANGE = (255, 170, 60); YEL = (255, 214, 0); RED = (255, 95, 95)
FOOT = '10월 3·4일 복귀 · 2026.10.9 밤 조회 · 성인 1명 편도 직항'

CARDS = [
    ('card_eu', '🇪🇺', '유럽 복귀편 20편', [
        ('일반석', '18편 남음', GREEN, '0석은 파리 14:40 편뿐 (3일·4일)'),
        ('프레스티지', '3편만 1석씩', ORANGE, '4일 로마 · 빈 · 부다페스트'),
    ]),
    ('card_asia', '🌏', '아시아 복귀편 96편', [
        ('일반석', '96편 모두 남음', GREEN, '9석 아래는 7편 (후쿠오카·발리·삿포로·오키나와)'),
        ('프레스티지', '70편 남음', GREEN, '0석 26편 (3일 10편 · 4일 16편)'),
    ]),
    ('card_am', '✈️', '미주·대양주 복귀편 42편', [
        ('일반석', '42편 모두 9석 이상', GREEN, '0석도, 9석 아래도 없음'),
        ('프레스티지', '5편만 남음', RED, '브리즈번 · 시애틀 · 밴쿠버 · 보스턴 · 오클랜드'),
    ]),
    ('card_total', '', '복귀편 158편, 그래서 남은 건', [
        ('일반석', '156편 남음', GREEN, '0석은 파리 2편뿐'),
        ('프레스티지', '78편 남음', YEL, '아시아 70 · 미주·대양주 5 · 유럽 3'),
    ]),
]


def center(d, y, s, sz, col):
    f = T.font(sz)
    while d.textlength(s, font=f) > W - 80 and sz > 28:
        sz -= 2; f = T.font(sz)
    d.text(((W - d.textlength(s, font=f)) / 2, y), s, font=f, fill=col)


for name, _emoji, title, rows in CARDS:
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    center(d, 70, title, 64, WHITE)
    d.line([(80, 175), (W - 80, 175)], fill=LINE, width=3)
    y = 230
    for label, big, col, sub in rows:
        center(d, y, label, 44, GRAY)
        center(d, y + 70, big, 96, col)
        center(d, y + 195, sub, 36, WHITE)
        y += 330
    center(d, H - 90, FOOT, 30, GRAY)
    im.save(os.path.join(BASE, name + '.png'))
    print(name)
