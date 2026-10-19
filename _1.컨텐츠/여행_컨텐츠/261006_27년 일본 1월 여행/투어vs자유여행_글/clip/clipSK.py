# 시라카와고 버스투어 vs 자유여행 클립 (발행 10/9, logNo 224434506054) — 정보형 · 아직 안 간 여행(가기 전 정리)
# 실행: python clipSK.py stills / python clipSK.py → out\shirakawago_clip.mp4
# 숫자는 발행본 그대로(1월 14일 기준). 판매처 이름은 쓰지 않는다(지침: 반쯤 가림 → 클립은 아예 뺌). 삽화는 AI 생성 — 표시
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.dirname(BASE)
D = dict(type='data', render=render, bg=LIGHT)
TEAL = (30, 100, 110)

s0 = dict(D, dur=3.8, items=[
    ('image', 0.1, os.path.join(IMG, 'img1.png'), 90, 560, 990, 960),
    ('label', 0.2, 'AI 생성 이미지 · 실제 시라카와고 아님', 980, 975, 22, MUTED, 'r'),
    ('box', 0.6, 90, 1010, 520, 1220, SKY), ('label', 0.65, '버스투어 (1/14)', 305, 1060, 32, NAVY),
    ('label', 0.75, '59,000~98,000원', 305, 1150, 40, NAVY),
    ('box', 0.9, 560, 1010, 990, 1220, PINK), ('label', 0.95, '자유여행 패스', 775, 1060, 32, RED),
    ('label', 1.05, '12,370엔 · 약 11만 5천원', 775, 1150, 34, RED)],
    texts=[(0.05, 'top', '나고야 당일치기\n{투어가 더 싸}')], sfx=[(0.1, 'ding'), (0.95, 'ding')])

s1 = dict(D, dur=3.8, items=[
    ('label', 0.1, '같은 투어 코스 · 날짜와 옵션에 따라', 540, 640, 34, MUTED),
    ('label', 0.3, '10월 첫 화면', 90, 770, 30, INK, 'l'), ('label', 0.6, '1월 14일 일반가', 90, 900, 30, INK, 'l'), ('label', 0.9, '1월 14일 다른 상품', 90, 1030, 28, INK, 'l'),
    ('hbar', 0.3, '', 59, 110, 770, (150, 165, 195), '59,000원'),
    ('hbar', 0.6, '', 79, 110, 900, NAVY, '79,000원'),
    ('hbar', 0.9, '', 98, 110, 1030, RED, '98,000원'),
    ('label', 1.5, '첫 화면 값 말고 내 날짜를 골랐을 때 값', 540, 1170, 38, RED)],
    texts=[(0.05, 'top', '판매처보다\n{날짜가 값을 바꿔}')], sfx=[(1.5, 'ding')])

CHK = ['가이드 팁 포함?', '통행료(현지 1인 2,000엔)?', '점심 포함?', '최소 인원(1~30명)?', '무료 취소 마감?', '폭설 판단 시각?']
s2_items = [('label', 0.1, '버스투어 고를 때 가격보다 먼저', 540, 640, 36, MUTED)]
for i, c in enumerate(CHK):
    y = 740 + i * 88; t = 0.3 + i * 0.15
    s2_items += [('box', t, 120, y - 36, 960, y + 36, (236, 244, 245)), ('label', t, f'{i + 1}. ' + c, 160, y, 36, TEAL, 'l')]
s2 = dict(D, dur=4.0, items=s2_items, texts=[(0.05, 'top', '싼 투어가\n{진짜 싼지}')], sfx=[(0.35, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('label', 0.1, '시라카와고에 머무는 시간', 540, 640, 36, MUTED),
    ('hbar', 0.3, '버스투어', 150, 340, 780, NAVY, '120~150분'),
    ('hbar', 0.6, '자유여행', 273, 340, 910, RED, '약 4시간 반'),
    ('label', 0.9, '12:57 도착 ~ 막차 17:30', 640, 975, 30, RED),
    ('label', 1.3, '자유여행이 두 배 가까이 길어', 540, 1050, 42, INK),
    ('label', 1.6, '대신 노히버스 무예약 편은 1~2시간에 한 대', 540, 1130, 32, MUTED)],
    texts=[(0.05, 'top', '돈 말고\n{시간}을 보면')], sfx=[(0.65, 'ding')])

s4 = dict(D, dur=4.0, items=[
    ('image', 0.1, os.path.join(IMG, 'img3.png'), 240, 560, 840, 860),
    ('label', 0.2, 'AI 생성 이미지', 830, 875, 20, MUTED, 'r'),
    ('label', 0.6, '투어 07:40 집합 · 폭설이면 운영사가 판단', 540, 930, 34, NAVY),
    ('label', 0.9, '자유여행 · 폭설 판단도 내가', 540, 1000, 34, RED),
    ('box', 1.4, 90, 1070, 990, 1260, PINK),
    ('label', 1.5, '너라면 투어? 직접?', 540, 1140, 50, RED),
    ('label', 1.9, '아직 안 간 여행 · 2027년 1월 예정', 540, 1215, 28, MUTED)],
    texts=[(0.05, 'top', '두 방법이\n{파는 게 달라}')], sfx=[(0.6, 'ding')])

SCENES = [s0, s1, s2, s3, s4]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        from PIL import Image
        d = os.path.join(BASE, '_build', 'stills'); os.makedirs(d, exist_ok=True)
        tiles = []
        for i, sc in enumerate(SCENES):
            f = os.path.join(d, f's{i}.jpg'); still(sc, sc['dur'] - 0.05, f); tiles.append(Image.open(f).resize((270, 480)))
        sh = Image.new('RGB', (270 * len(tiles), 480))
        for j, im in enumerate(tiles):
            sh.paste(im, (j * 270, 0))
        sh.save(os.path.join(d, 'sheet.jpg'), quality=90); print('stills', d)
    else:
        build(SCENES, BASE, 'SK', 'shirakawago_clip.mp4')
