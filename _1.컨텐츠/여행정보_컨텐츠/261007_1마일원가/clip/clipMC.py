# 대한항공 마일리지 카드 클립 (발행 10/9, logNo 224434534444) — 정보형 · 마일리지 시리즈
# 실행: python clipMC.py stills / python clipMC.py → out\mile_card_clip.mp4
# 숫자는 발행본 그대로(결제 1,000원당 1마일 · 연회비 5만 원 예시, 계산값). 특정 카드 이름은 쓰지 않는다
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)

s0 = dict(D, dur=3.6, items=[
    ('label', 0.1, '1,000원당 1마일 · 연회비 5만 원 카드로', 540, 640, 34, MUTED),
    ('label', 0.3, '한 달 50만 원 쓰면', 540, 730, 46, INK),
    ('count', 0.6, 0, 5, '{:.0f}년', 540, 900, 150, NAVY),
    ('label', 1.4, '일본 왕복 30,000마일까지 · 연회비 25만 원', 540, 1080, 38, RED)],
    texts=[(0.05, 'top', '일본 왕복 한 장에\n{5년}')], sfx=[(0.1, 'ding'), (1.4, 'ding')])

s1 = dict(D, dur=3.6, items=[
    ('label', 0.2, '1년 600만 원 → 6,000마일', 540, 700, 48, INK),
    ('box', 0.7, 90, 790, 990, 1010, SKY),
    ('label', 0.8, '1마일 본전 = 연회비 ÷ 1년에 쌓이는 마일', 540, 850, 34, MUTED),
    ('label', 1.1, '5만 원 ÷ 6,000 = 약 8.3원', 540, 945, 56, NAVY),
    ('label', 1.6, '1마일을 8.3원보다 비싸게 써야 본전', 540, 1090, 40, RED)],
    texts=[(0.05, 'top', '1마일 본전은\n{8.3원}')], sfx=[(1.1, 'ding')])

s2 = dict(D, dur=3.8, items=[
    ('label', 0.1, '한 달 결제액별 · 30,000마일까지 걸리는 시간', 540, 640, 32, MUTED),
    ('hbar', 0.3, '30만 원', 8.33, 9.5, 760, RED, '8년 4개월'),
    ('hbar', 0.5, '50만 원', 5, 9.5, 880, NAVY, '5년'),
    ('hbar', 0.7, '100만 원', 2.5, 9.5, 1000, (110, 130, 170), '2년 6개월'),
    ('hbar', 0.9, '200만 원', 1.25, 9.5, 1120, (150, 165, 195), '1년 3개월')],
    texts=[(0.05, 'top', '얼마나 쓰느냐에\n{따라 달라}')], sfx=[(0.55, 'ding')])

USE = [('괌 왕복(26.11)', 1.8, 1.8), ('간사이 왕복(26.11)', 3.7, 3.7), ('이마트 1만 원 할인권', 7.1, 7.1), ('삿포로 왕복(27.1)', 18.7, 18.7), ('삿포로 왕복(24.1, 영수증)', 23.3, 23.3)]
s3_items = [('label', 0.1, '내가 잰 1마일 값', 540, 620, 36, MUTED)]
for i, (n, lo, hi) in enumerate(USE):   # 이름이 길어 막대 칸(360px~)을 침범 → 이름은 줄 위에 따로(10/9 사용자 지적)
    y = 740 + i * 120; t = 0.2 + i * 0.15
    s3_items += [('label', t, n, 90, y - 40, 32, INK, 'l'),
                 ('range', t, '', lo, hi, 25, y + 8, NAVY if hi > 8.3 else RED, None, 34)]
s3_items.append(('vline', 1.2, 8.3, 25, 690, 748 + 4 * 120 + 30, '본전 8.3원', RED))
s3 = dict(D, dur=4.2, items=s3_items, texts=[(0.05, 'top', '본전 넘은 건\n{삿포로 두 줄}')], sfx=[(1.25, 'ding')])

s4 = dict(D, dur=4.0, items=[
    ('label', 0.2, '네이버페이 포인트 22P = 1마일', 540, 680, 42, INK),
    ('label', 0.5, '30,000마일 = 660,000포인트', 540, 770, 46, NAVY),
    ('label', 0.8, '1마일 22원 넘게 써야 본전', 540, 850, 34, MUTED),
    ('box', 1.4, 90, 950, 990, 1150, PINK),
    ('label', 1.5, '연회비 내고 모을 거야?', 540, 1020, 48, RED),
    ('label', 1.9, '연회비만 본 계산값 · 카드 다른 혜택 제외', 540, 1095, 28, MUTED)],
    texts=[(0.05, 'top', '쓰기 전에\n{모은 값}부터')], sfx=[(0.5, 'ding')])

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
        build(SCENES, BASE, 'MC', 'mile_card_clip.mp4')
