# 서울 지하철역 가까운 산 찾기 클립 (발행 9/27, logNo 224423653725) — 정보형
# 실행: python clipM.py stills / python clipM.py → out\metro_mountain_clip.mp4
# 목록 10곳은 블로그 캡처(Content_03.png)에 보이는 행 그대로(15곳 중 화면에 보인 10곳) · 용마산 3-1 숫자는 본문 표 · 고도 그래프는 Content_06 캡처를 잘라 씀
# 주의(본문): 높이는 GPS 기록 최고점이라 공식 높이와 다름(용마산 공식 348m, 그래프 394m) · 역 거리는 직선
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)
GREEN = (46, 125, 80)
MINT = (226, 242, 232)

s0 = dict(D, dur=3.4, items=[
    ('box', 0.2, 90, 640, 330, 740, MINT), ('label', 0.25, '서울', 210, 690, 40, GREEN),
    ('box', 0.45, 350, 640, 730, 740, MINT), ('label', 0.5, '높이 200~400m', 540, 690, 40, GREEN),
    ('box', 0.7, 750, 640, 990, 740, MINT), ('label', 0.75, '역 1km 안', 870, 690, 40, GREEN),
    ('label', 1.1, '조건 세 개만 넣었더니', 540, 860, 44, MUTED),
    ('count', 1.3, 0, 15, '{:.0f}곳', 540, 1010, 140, GREEN)],
    texts=[(0.05, 'top', '내일 바로 산에 가고 싶을 때\n{어디 가지?}')], sfx=[(0.1, 'ding'), (1.3, 'ding')])

LIST = [('돌산', '관악산역 0.1km'), ('우면산', '양재시민의숲역 0.0km'), ('인왕산', '독립문역 0.3km'), ('돌산국기대', '관악산역 0.1km'),
        ('용마봉(중곡동)', '양원역 0.0km'), ('용마봉', '용마산역 0.0km'), ('용마산(중곡동)', '용마산역 0.3km'),
        ('망우산', '양원역 0.0km'), ('안산', '독립문역 0.1km'), ('대모산', '일원역 0.1km')]
s1_items = [('label', 0.1, '15곳 중 화면에 보인 10곳 · 거리는 직선', 540, 600, 32, MUTED)]
for i, (n, st) in enumerate(LIST):
    y = 680 + i * 78
    t = 0.25 + i * 0.12
    s1_items += [('box', t, 70, y - 32, 1010, y + 32, MINT if i % 2 == 0 else (240, 246, 242)),
                 ('label', t, n, 110, y, 36, INK, 'l'), ('label', t, st, 980, y, 34, GREEN, 'r')]
s1 = dict(D, dur=4.0, items=s1_items, texts=[(0.05, 'top', '역에서 내리면\n{바로 산}')], sfx=[(1.6, 'ding')])

s2 = dict(D, dur=3.8, items=[
    ('label', 0.1, '용마산 · 들머리별 코스 5개', 540, 640, 38, MUTED),
    ('box', 0.3, 90, 700, 990, 820, PINK),
    ('label', 0.35, '가장 짧은 코스 2개는 정상까지 안 감 (182m에서 끝)', 540, 760, 34, RED),
    ('label', 1.2, '그래서 역에서 가까운 코스 3-1', 540, 900, 44, INK),
    ('box', 1.5, 70, 960, 370, 1200, MINT), ('label', 1.55, '거리', 220, 1010, 32, MUTED), ('count', 1.6, 0, 1.9, '{:.1f}km', 220, 1120, 64, GREEN),
    ('box', 1.7, 390, 960, 690, 1200, MINT), ('label', 1.75, '오르막', 540, 1010, 32, MUTED), ('count', 1.8, 0, 289, '{:.0f}m', 540, 1120, 64, GREEN),
    ('box', 1.9, 710, 960, 1010, 1200, MINT), ('label', 1.95, '예상', 860, 1010, 32, MUTED), ('count', 2.0, 0, 57, '{:.0f}분', 860, 1120, 64, GREEN),
    ('label', 2.3, '용마산역에서 들머리까지 걸어서 약 5분 · 휴식 제외', 540, 1270, 32, INK)],
    texts=[(0.05, 'top', '짧다고 고르면\n{정상을 못 본다}')], sfx=[(0.4, 'ding')])

s3 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(BASE, 'profile_crop.png'), 40, 640, 1040, 1080),
    ('label', 1.0, '처음 700m는 거의 평지', 540, 1150, 42, INK),
    ('label', 1.4, '0.8~1.2km 구간 평균 경사 28%', 540, 1240, 48, RED),
    ('label', 1.8, '그래프 최고점 394m는 GPS 기록 · 공식 정상 348m', 540, 1330, 30, MUTED)],
    texts=[(0.05, 'top', '어디서 숨이 찰지\n{미리 안다}')], sfx=[(1.4, 'ding')])

s4 = dict(D, dur=3.8, items=[
    ('label', 0.2, '통제 구간·쉬는 시간은 안 들어 있다', 540, 740, 40, MUTED),
    ('label', 0.6, '마지막 확인은 내 발로', 540, 850, 62, GREEN),
    ('box', 1.4, 90, 1010, 990, 1270, PINK),
    ('label', 1.5, '너는 산 고를 때 뭘 제일 먼저 봐?', 540, 1100, 48, RED),
    ('label', 1.9, '댓글로 알려줘', 540, 1195, 40, INK)],
    texts=[(0.05, 'top', '프로그램은\n{후보까지}')], sfx=[(0.6, 'ding')])

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
        build(SCENES, BASE, 'M', 'metro_mountain_clip.mp4')
