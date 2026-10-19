# 2027년 10월 연휴 마일리지 항공권 클립 (발행 10/8 11:36, logNo 224435045387) — 정보형 · 오픈 시각 클립과 짝
# 실행: python clipK.py stills / python clipK.py → out\oct2027_award_clip.mp4
# 숫자는 발행 본문 그대로(10/8 오전 10:42~11:08 조회 · 인천 출발 편도 직항 · 10/1~3 출발 52도시 236편)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)
GREEN = (46, 125, 80)
MINT = (226, 242, 232)

intro = dict(D, dur=3.8, items=[
    ('label', 0.1, '이번 주 · 10월 연휴', 540, 650, 40, MUTED),
    ('box', 0.4, 90, 720, 990, 1010, SKY),
    ('label', 0.5, '내년 이맘때도 사흘 연휴', 540, 790, 52, NAVY),
    ('label', 0.8, '2027년 10/2(토) ~ 10/4(월)', 540, 885, 50, NAVY),
    ('label', 1.0, '개천절 + 대체공휴일 · 금요일 붙이면 나흘', 540, 960, 32, INK),
    ('label', 1.7, '그 연휴 마일리지 좌석이', 540, 1100, 46, INK),
    ('label', 1.9, '벌써 열렸다', 540, 1180, 72, RED)],
    texts=[(0.05, 'top', '이번 주 연휴 끝나면\n{내년 연휴 차례}')], sfx=[(0.5, 'ding'), (1.9, 'ding')])

s0 = dict(D, dur=3.6, items=[
    ('label', 0.1, '2027년 10월 1~3일 출발 · 인천 → 유럽 28편', 540, 640, 34, MUTED),
    ('box', 0.3, 90, 700, 520, 1040, SKY), ('label', 0.35, '일반석 0석', 305, 770, 40, NAVY),
    ('count', 0.4, 0, 9, '{:.0f}편', 305, 920, 110, NAVY),
    ('box', 0.8, 560, 700, 990, 1040, PINK), ('label', 0.85, '프레스티지 0석', 775, 770, 40, RED),
    ('count', 0.9, 0, 28, '{:.0f}편', 775, 920, 110, RED),
    ('label', 1.7, '28편 전부', 540, 1150, 70, RED)],
    texts=[(0.05, 'top', '열린 지 이틀\n{유럽 비즈니스 0편}')], sfx=[(0.1, 'ding'), (1.7, 'ding')])

DAYS = [('10/1 금', '10/6 열림', SKY, NAVY), ('10/2 토', '10/7 열림', SKY, NAVY), ('10/3 일', '10/8 열림', SKY, NAVY), ('10/4 월', '10/9 내일', PINK, RED)]
s1_items = [('label', 0.1, '2027년 10월 연휴 · 개천절이 일요일 → 4일 대체공휴일', 540, 640, 32, MUTED)]
for i, (d, o, bg, fg) in enumerate(DAYS):
    x0 = 70 + i * 240; t = 0.3 + i * 0.25
    s1_items += [('box', t, x0, 700, x0 + 220, 960, bg), ('label', t, d, x0 + 110, 780, 40, fg), ('label', t + 0.1, o, x0 + 110, 880, 32, fg)]
s1_items += [('label', 1.6, '출발 360일 전 아침 9시에 열린다', 540, 1080, 44, INK),
             ('label', 1.9, '10/3 출발은 열린 지 두 시간 안에 봤다', 540, 1160, 34, MUTED)]
s1 = dict(D, dur=3.8, items=s1_items, texts=[(0.05, 'top', '출발편 셋은\n{이미 열렸다}')], sfx=[(1.6, 'ding')])

ZERO = ['파리', '로마', '밀라노', '프라하', '마드리드', '취리히']
FULL = ['런던', '암스테르담', '빈', '부다페스트']
s2_items = [('label', 0.1, '유럽 일반석 · 금·토·일', 540, 640, 36, MUTED), ('label', 0.2, '0석이 나온 도시', 540, 710, 40, RED)]
for i, c in enumerate(ZERO):
    x0 = 90 + (i % 3) * 300; y0 = 760 + (i // 3) * 110; t = 0.3 + i * 0.12
    s2_items += [('box', t, x0, y0, x0 + 280, y0 + 90, PINK), ('label', t, c, x0 + 140, y0 + 45, 42, RED)]
s2_items.append(('label', 1.3, '뜨는 편 전부 9석 이상', 540, 1030, 40, GREEN))
for i, c in enumerate(FULL):
    x0 = 90 + (i % 2) * 450; y0 = 1080 + (i // 2) * 110; t = 1.4 + i * 0.12
    s2_items += [('box', t, x0, y0, x0 + 430, y0 + 90, MINT), ('label', t, c, x0 + 215, y0 + 45, 42, GREEN)]
s2 = dict(D, dur=4.2, items=s2_items, texts=[(0.05, 'top', '유럽은\n{도시마다 갈렸다}')], sfx=[(0.35, 'ding'), (1.45, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('label', 0.1, '일반석 0석인 편 비율', 540, 640, 38, MUTED),
    ('hbar', 0.3, '유럽', 32, 60, 760, RED, '28편 중 9편'),
    ('hbar', 0.6, '아시아', 0.7, 60, 890, NAVY, '144편 중 1편'),
    ('hbar', 0.9, '미주·대양주', 0, 60, 1020, NAVY, '64편 중 0편'),
    ('label', 1.6, '아시아 0석은 오키나와 10/1 한 편뿐', 540, 1160, 38, INK)],
    texts=[(0.05, 'top', '같은 날 아침\n{권역마다 달랐다}')], sfx=[(0.35, 'ding')])

s4 = dict(D, dur=3.6, items=[
    ('label', 0.1, '프레스티지 0석인 편 비율', 540, 640, 38, MUTED),
    ('hbar', 0.3, '유럽', 100, 135, 760, RED, '28편 전부'),
    ('hbar', 0.6, '미주·대양주', 94, 135, 890, RED, '64편 중 60편'),
    ('label', 1.3, '남은 건 시애틀 3편 · 댈러스 1편, 각 1석', 540, 1040, 38, INK),
    ('label', 1.6, '왜 그런지는 모르겠다 · 확인한 사실만', 540, 1120, 32, MUTED)],
    texts=[(0.05, 'top', '비즈니스는\n{미주도 거의 없다}')], sfx=[(1.3, 'ding')])

s5 = dict(D, dur=4.0, items=[
    ('box', 0.2, 90, 680, 990, 900, PINK),
    ('label', 0.3, '10/4 복귀편은 내일 10/9', 540, 750, 46, RED),
    ('label', 0.5, '아침 9시에 열린다', 540, 840, 46, RED),
    ('label', 1.0, '0석이던 날이 다시 열린 적도 있다 · 시간 달리해 다시 보기', 540, 960, 30, MUTED),
    ('box', 1.6, 90, 1030, 990, 1270, SKY),
    ('label', 1.7, '너는 10월 연휴에 어디 가?', 540, 1115, 50, NAVY),
    ('label', 2.1, '댓글로 알려줘', 540, 1205, 40, INK)],
    texts=[(0.05, 'top', '갈 거면\n{내일 아침 9시}')], sfx=[(0.35, 'ding')])

SCENES = [intro, s0, s1, s2, s3, s4, s5]

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
        build(SCENES, BASE, 'K', 'oct2027_award_clip.mp4')
