# 발행본 「📝 시간이 없다면 이 순서로」 표 → card_rank.png (숫자·말 그대로)
import sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from PIL import Image, ImageDraw
import tactics as T

ROWS = [('1', '페이토', '불필요', '30분~1시간'), ('2', '모레인', '셔틀 필수', '반나절'), ('3', '레이크 루이스', '셔틀 필수', '반나절'),
        ('4', '보우', '불필요', '30분'), ('5', '에메랄드', '불필요', '1시간'), ('6', '말리뉴', '크루즈 예약', '반나절'),
        ('7', '패트리샤', '불필요', '30분'), ('8', '클리어워터', '불필요', '—')]
W, H = 1080, 1080
BG, INK, SUB, LINE, HI = (250, 248, 243), (30, 30, 30), (110, 110, 110), (225, 222, 214), (14, 120, 160)
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
d.text((60, 50), '캐나다 로키 호수 8곳, 시간이 없다면 이 순서로', font=T.font(46), fill=INK)
d.text((60, 118), '2025년 6월 · 5박6일 2,700km · 직접 다녀온 순위', font=T.font(30), fill=SUB)
X = [60, 150, 520, 790]
y = 200
for i, h in enumerate(('순위', '호수', '예약', '소요')):
    d.text((X[i], y), h, font=T.font(32), fill=SUB)
y += 56
for r in ROWS:
    d.line([(60, y - 12), (W - 60, y - 12)], fill=LINE, width=2)
    top = r[0] in ('1', '2', '3')
    col = HI if r[2] == '불필요' else (190, 70, 60)
    d.text((X[0], y), r[0], font=T.font(44), fill=HI if top else INK)
    d.text((X[1], y), r[1], font=T.font(44), fill=INK)
    d.text((X[2], y), r[2], font=T.font(38), fill=col)
    d.text((X[3], y), r[3], font=T.font(38), fill=INK)
    y += 92
d.text((60, H - 70), '파란 글씨 = 예약 없이 바로 · 붉은 글씨 = 예약 필요', font=T.font(28), fill=SUB)
im.save(sys.argv[1] if len(sys.argv) > 1 else 'card_rank.png')
print('ok')
