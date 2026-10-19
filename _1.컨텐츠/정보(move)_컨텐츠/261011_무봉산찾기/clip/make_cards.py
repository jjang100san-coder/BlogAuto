# 발행본 표 3개 → 카드 (숫자·말 그대로)
import sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
from PIL import Image, ImageDraw
import tactics as T

BG, INK, SUB, LINE, HI = (247, 248, 244), (28, 32, 30), (105, 110, 105), (222, 225, 218), (30, 120, 70)


def card(path, title, sub, head, rows, X, hl=None, foot=None, size=(1080, 1080)):
    W, H = size
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((56, 52), title, font=T.font(46), fill=INK)
    d.text((56, 118), sub, font=T.font(29), fill=SUB)
    y = 200
    for i, h in enumerate(head):
        d.text((X[i], y), h, font=T.font(30), fill=SUB)
    y += 56
    step = min(110, (H - y - 110) // len(rows))
    for r in rows:
        d.line([(56, y - 14), (W - 56, y - 14)], fill=LINE, width=2)
        on = hl and r[0].startswith(hl)
        if on:
            d.rectangle([48, y - 12, W - 48, y + step - 26], fill=(226, 240, 230))
        for i, c in enumerate(r):
            d.text((X[i], y), c, font=T.font(40 if i == 0 else 38), fill=HI if on else INK)
        y += step
    if foot:
        d.text((56, H - 74), foot, font=T.font(27), fill=SUB)
    im.save(path)


card('card_near.png', '출발 지점에서 가까운 순', '45km 안 · 높이 200~450m · 짧은 코스 2.5km 이하 → 149곳',
     ('산', '거리', '높이 · 짧은 코스'),
     [('독산 (오산)', '약 3km', '230m · 1.5km'), ('서봉산 (화성)', '약 7km', '250m · 2.2km'), ('건달산 (화성)', '약 10km', '335m · 1.3km'),
      ('함봉산 (용인)', '약 11km', '325m · 1.7km'), ('백련봉 (평택)', '약 14km', '233m · 2.3km'), ('태행산 (화성)', '약 15km', '318m · 1.3km')],
     (56, 470, 700), foot='위에서부터 6곳 · 발행글 표 그대로')
card('card_search.png', '「○○ 등산코스」 검색 vs 블로그 글', '한 달 검색 수와 이미 올라온 글 수',
     ('산', '월 검색', '글 수'),
     [('무봉산 (동탄)', '2,170', '2,297'), ('칠보산 (수원)', '2,270', '9,571'), ('석성산 (용인)', '860', '7,735'),
      ('바라산 (의왕)', '440', '4,591'), ('건달산 (봉담)', '370', '799'), ('서봉산 (정남)', '200', '870')],
     (56, 560, 820), hl='무봉산', foot='비교: 수암봉 검색 770 · 글 6,242')
card('card_height.png', '무봉산 높이는 자료마다 셋', '기준점이 달라서 갈린다',
     ('자료', '높이'),
     [('산림청 산정보', '201.5m'), ('화성시 관광 안내', '약 360m'), ('지형 자료 최고점', '약 351m'), ('정상석', '해발 360.2m')],
     (56, 700), hl='정상석', foot='프로그램 등산로 자료: 없음')
print('ok')
