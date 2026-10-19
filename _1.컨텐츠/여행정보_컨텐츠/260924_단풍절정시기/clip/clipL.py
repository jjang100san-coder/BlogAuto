# 2026 단풍 절정 시기 클립 (발행 9/27, logNo 224421720643) — 정보형
# 실행: python clipL.py stills / python clipL.py → out\foliage_clip.mp4
# 숫자는 발행 본문 그대로: 산림청 2026 예측표 · 서울 관측소 은행나무 절정 2019~2025(11/13·9·14·14·17·21·17) · 사진 날짜
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(os.path.dirname(BASE), 'foliage_bundle')
D = dict(type='data', render=render, bg=LIGHT)
GOLD = (214, 150, 20)
MAPLE = (196, 64, 40)

s0 = dict(D, dur=3.4, items=[
    ('image', 0.1, os.path.join(PH, '20251115_144735.jpg'), 140, 600, 940, 1330),
    ('label', 0.9, '2025.11.15 화담숲 · 예약 전쟁 끝에 들어갔는데', 540, 1380, 34, INK),
    ('label', 1.3, '이미 끝물', 540, 1460, 64, MAPLE)],
    texts=[(0.05, 'top', '단풍 보러 갔는데\n{이미 끝물}이었어')], sfx=[(1.3, 'ding')])

PRED = [('설악산', '10월 20일'), ('속리산', '10월 28일'), ('은행나무', '10월 30일'), ('단풍나무·참나무', '10월 31일'),
        ('내장산', '11월 4일'), ('한라산', '11월 6일')]
s1_items = [('label', 0.1, '산림청 2026 단풍 예측지도 · 절정 예상일', 540, 620, 34, MUTED)]
for i, (n, d) in enumerate(PRED):
    y = 710 + i * 100; t = 0.3 + i * 0.15
    s1_items += [('box', t, 90, y - 38, 990, y + 38, (250, 236, 222) if i != 3 else PINK),
                 ('label', t, n, 130, y, 40, INK, 'l'), ('label', t, d, 950, y, 42, MAPLE if i == 3 else INK, 'r')]
s1 = dict(D, dur=3.6, items=s1_items, texts=[(0.05, 'top', '올해 예측은\n{단풍나무 10월 31일}')], sfx=[(0.3 + 3 * 0.15, 'ding')])

GINKGO = [('2019', 13), ('2020', 9), ('2021', 14), ('2022', 14), ('2023', 17), ('2024', 21), ('2025', 17)]
s2 = dict(D, dur=4.0, items=[('label', 0.1, '서울 관측소 은행나무 단풍 절정일 · 기상청', 540, 610, 34, MUTED)] +
    [('hbar', 0.3 + i * 0.15, y, d, 24, 700 + i * 95, GOLD if d != 21 else MAPLE, f'11월 {d}일') for i, (y, d) in enumerate(GINKGO)] +
    [('vline', 1.5, 9, 24, 650, 1340, '11월 9일', MAPLE),
     ('label', 2.0, '2008년엔 10월 25일 · 2024년 11월 21일은 26년 중 가장 늦음', 540, 1430, 32, INK)],
    texts=[(0.05, 'top', '서울 은행나무는\n{7년 연속 11월 9일 이후}')], sfx=[(1.5, 'ding')])

s3 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(PH, 'gwanak_20231001_vs_20231028.jpg'), 40, 620, 1040, 1180),
    ('label', 1.0, '관악산 연주대 앞 · 2023년 10월 1일 → 10월 28일', 540, 1240, 34, INK),
    ('label', 1.4, '같은 해 서울 관측소 단풍나무 절정은 11월 16일', 540, 1320, 36, MAPLE)],
    texts=[(0.05, 'top', '그런데 산은\n{4주 만에 초록 → 갈색}')], sfx=[(1.4, 'ding')])

s4 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(PH, '20221030_151123_crop.jpg'), 60, 620, 1020, 1100),
    ('label', 1.0, '2022.10.30 정선 가는 길 · 이미 노란 은행나무', 540, 1160, 34, INK),
    ('label', 1.3, '그해 서울 은행나무 절정은 11월 14일', 540, 1230, 36, MUTED),
    ('label', 1.8, '산·교외 단풍은 도심 기록보다 보름~3주 빨랐다', 540, 1340, 40, MAPLE)],
    texts=[(0.05, 'top', '내 사진첩을 맞대 보니\n{보름~3주 앞서}')], sfx=[(1.8, 'ding')])

s5 = dict(D, dur=4.0, items=[
    ('box', 0.2, 90, 640, 990, 720, (250, 236, 222)), ('label', 0.2, '설악산', 130, 680, 40, INK, 'l'), ('label', 0.2, '10월 20일 무렵', 950, 680, 40, INK, 'r'),
    ('box', 0.4, 90, 740, 990, 820, PINK), ('label', 0.4, '수도권 산·수목원', 130, 780, 40, INK, 'l'), ('label', 0.4, '10월 말~11월 초', 950, 780, 40, MAPLE, 'r'),
    ('box', 0.6, 90, 840, 990, 920, (250, 236, 222)), ('label', 0.6, '서울 도심 은행나무', 130, 880, 40, INK, 'l'), ('label', 0.6, '11월 중순', 950, 880, 40, GOLD, 'r'),
    ('box', 1.4, 90, 1040, 990, 1300, SKY),
    ('label', 1.5, '너는 올해 단풍 어디로 가?', 540, 1130, 52, NAVY),
    ('label', 1.9, '댓글로 알려줘', 540, 1225, 40, INK)],
    texts=[(0.05, 'top', '그래서 올해는\n{이렇게 잡았어}')], sfx=[(0.4, 'ding')])

SCENES = [s0, s1, s2, s3, s4, s5]

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
        build(SCENES, BASE, 'L', 'foliage_clip.mp4')
