# 세제개편 클립 카드 2장 — 10/11 사용자: 「AI 삽화 기반으로 시청자가 정확히 인지할 수 있도록」 → 숫자는 카드로 한눈에
# 숫자·표현은 발행본(224436974592) 표 그대로
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from PIL import Image, ImageDraw
import tactics as T
BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1070
BG = (16, 22, 38); LINE = (60, 70, 95); WHITE = (255, 255, 255); GRAY = (165, 172, 190)
GREEN = (80, 220, 140); ORANGE = (255, 170, 60); YEL = (255, 214, 0)
FOOT = '2026.10.10 기준 · 종부세·양도세는 국회 통과 전'
CARDS = [
    ('card_back', '9월 1일 수정안에서 되돌린 3개', [
        ('집에 살지 않는 1주택 기본공제', '12억 유지', GREEN, '정부안은 9억으로 낮추려 했음'),
        ('종부세 세부담 상한', '150% 유지', GREEN, '정부안은 200%'),
        ('집에 살지 않는 부부 공동명의 1인 공제', '6억', ORANGE, '정부안은 4억'),
    ]),
    ('card_sum', '한눈에 정리', [
        ('이미 시행 (10월 1일)', '일시적 2주택 3년 → 2년', GREEN, '등록임대 기한 · 상생임대 종료도 함께 시행'),
        ('국회 심사 중', '종부세 · 양도세', YEL, '다음 관문 11월 조세소위'),
        ('되돌린 것', '안 사는 1주택 종부세 3개', ORANGE, '나머지는 정부안 그대로'),
    ]),
]
def center(d, y, s, sz, col):
    f = T.font(sz)
    while d.textlength(s, font=f) > W - 80 and sz > 26:
        sz -= 2; f = T.font(sz)
    d.text(((W - d.textlength(s, font=f)) / 2, y), s, font=f, fill=col)
for name, title, rows in CARDS:
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    center(d, 60, title, 60, WHITE)
    d.line([(80, 160), (W - 80, 160)], fill=LINE, width=3)
    y = 200
    for label, big, col, sub in rows:
        center(d, y, label, 38, GRAY)
        center(d, y + 56, big, 76, col)
        center(d, y + 160, sub, 32, WHITE)
        y += 262
    im.save(os.path.join(BASE, name + '.png')); print(name)
