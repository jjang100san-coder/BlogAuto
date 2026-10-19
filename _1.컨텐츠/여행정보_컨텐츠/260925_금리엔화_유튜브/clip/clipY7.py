# 엔화 환전 시기 2026 · 유튜버 7명 클립 (발행 9/27, logNo 224422995778) — 정보형 · 엔화 환전 클립과 짝
# 실행: python clipY7.py stills / python clipY7.py → out\yen_youtube_clip.mp4
# 숫자는 발행 본문 그대로. 채널 이름은 클립에서 빼고 「같은 주 영상」으로만(남의 채널 실명 노출 최소화) · 투자 권유 아님 표시
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)

s0 = dict(D, dur=3.4, items=[
    ('label', 0.1, '9월 17~23일 · 같은 주 엔화 영상 7편 · 달러당', 540, 640, 32, MUTED),
    ('box', 0.3, 90, 700, 520, 880, SKY), ('label', 0.35, '152엔', 305, 790, 80, NAVY),
    ('box', 0.5, 560, 700, 990, 880, SKY), ('label', 0.55, '153엔', 775, 790, 80, NAVY),
    ('box', 0.7, 90, 900, 520, 1080, PINK), ('label', 0.75, '158엔', 305, 990, 80, RED),
    ('box', 0.9, 560, 900, 990, 1080, PINK), ('label', 0.95, '164엔', 775, 990, 80, RED),
    ('label', 1.5, '누가 맞는 거야?', 540, 1180, 52, INK)],
    texts=[(0.05, 'top', '같은 주 엔화 영상\n{숫자가 네 개}')], sfx=[(0.1, 'ding'), (1.5, 'ding')])

s1 = dict(D, dur=3.6, items=[
    ('label', 0.1, '일본은행 기준금리 · 9월 18일', 540, 660, 36, MUTED),
    ('label', 0.3, '1.00% → 1.25%', 540, 780, 90, NAVY),
    ('label', 0.8, '1995년 이후 가장 높음', 540, 890, 38, INK),
    ('label', 1.3, '그런데 엔화는 오히려', 540, 1010, 42, MUTED),
    ('label', 1.6, '달러당 158엔까지 약세', 540, 1100, 60, RED)],
    texts=[(0.05, 'top', '금리는 올랐는데\n{엔화는 내려갔다}')], sfx=[(1.6, 'ding')])

ROWS = [('164엔', '8월 중순 고점', '9/18 영상'), ('153엔', '녹화하던 날', '9/18 영상'),
        ('152엔', '금리 발표 전', '9/21 영상'), ('158엔', '금리 발표 뒤 한때', '9/21 영상')]
s2_items = []
for i, (n, w, s) in enumerate(ROWS):
    y = 700 + i * 120; t = 0.3 + i * 0.2
    s2_items += [('box', t, 70, y - 48, 1010, y + 48, (240, 240, 236)), ('label', t, n, 150, y, 48, NAVY, 'l'),
                 ('label', t, w, 560, y, 38, INK), ('label', t, s, 970, y, 30, MUTED, 'r')]
s2_items.append(('label', 1.4, '누가 틀린 게 아니라 녹화한 날이 달랐다', 540, 1230, 42, RED))
s2 = dict(D, dur=3.8, items=s2_items, texts=[(0.05, 'top', '환율 영상은\n{언제 찍었나}부터')], sfx=[(1.4, 'ding')])

s3 = dict(D, dur=3.6, items=[
    ('label', 0.2, '영상은 대부분 「1달러에 몇 엔」', 540, 700, 40, MUTED),
    ('label', 0.6, '여행자가 내는 건', 540, 810, 44, INK),
    ('label', 0.9, '100엔에 몇 원', 540, 920, 90, NAVY),
    ('label', 1.5, '원화도 달러 따라 같이 움직인다 (최근 10년 상관 0.9)', 540, 1050, 32, INK)],
    texts=[(0.05, 'top', '여행자가 볼 환율은\n{따로 있다}')], sfx=[(0.95, 'ding')])

s4 = dict(D, dur=3.6, items=[
    ('label', 0.1, '100엔당 원', 540, 640, 38, MUTED),
    ('hbar', 0.3, '2023.11.3', 879.93, 1150, 760, (150, 160, 185), '879원'),
    ('hbar', 0.5, '2026.9.17', 871, 1150, 890, NAVY, '871원'),
    ('hbar', 0.7, '2026.9.26', 861, 1150, 1020, RED, '861원'),
    ('label', 1.4, '싼 건 맞지만 처음 보는 가격은 아니다', 540, 1170, 42, INK)],
    texts=[(0.05, 'top', '100엔 800원대\n{처음이 아니야}')], sfx=[(1.4, 'ding')])

s5 = dict(D, dur=4.0, items=[
    ('label', 0.2, '방향은 아무도 확신 못 한다', 540, 720, 44, INK),
    ('label', 0.6, '한 번에 말고 나눠서 바꾸기', 540, 820, 56, NAVY),
    ('label', 0.9, '여행자 기록 · 환전·투자 권유 아님', 540, 900, 30, MUTED),
    ('box', 1.5, 90, 1010, 990, 1270, PINK),
    ('label', 1.6, '너는 엔화 언제 바꿔?', 540, 1100, 52, RED),
    ('label', 2.0, '댓글로 알려줘', 540, 1195, 40, INK)],
    texts=[(0.05, 'top', '그래서 나는\n{나눠서 바꾼다}')], sfx=[(0.6, 'ding')])

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
        build(SCENES, BASE, 'Y7', 'yen_youtube_clip.mp4')
