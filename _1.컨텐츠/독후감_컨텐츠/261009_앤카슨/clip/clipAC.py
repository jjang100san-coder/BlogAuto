# 노벨문학상 앤 카슨 클립 (발행 10/9, logNo 224436611592) — 정보형 · 수상 직후 시의성
# 실행: python clipAC.py stills / python clipAC.py → out\carson_clip.mp4
# 숫자는 발행본 그대로(배당·국내 9종 쪽수·서점 판매 배수). 삽화는 AI 생성 — 화면에 표시
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, '..', 'images')
D = dict(type='data', render=render, bg=LIGHT)
CRIM = (170, 30, 40)

s0 = dict(D, dur=3.8, items=[
    ('image', 0.1, os.path.join(IMG, 'carson_01_thumb.png'), 90, 560, 990, 1000),
    ('label', 0.2, 'AI 생성 이미지', 980, 1015, 22, MUTED, 'r'),
    ('label', 0.7, '캐나다 시인·고전학자 · 1950년생', 540, 1080, 38, INK),
    ('label', 1.0, '대표작 『빨강의 자서전』', 540, 1160, 50, CRIM)],
    texts=[(0.05, 'top', '2026 노벨문학상\n{앤 카슨}')], sfx=[(0.1, 'ding'), (1.0, 'ding')])

ROWS = [('9월 2일', '명단에 없음', MUTED), ('9월 29일', '33배', INK), ('10월 7일', '10배 · 공동 1위', NAVY), ('10월 8일', '수상', CRIM)]
s1_items = [('label', 0.1, '영국 배당 사이트 래드브록스의 앤 카슨', 540, 640, 34, MUTED)]
for i, (a, b, c) in enumerate(ROWS):
    y = 760 + i * 125; t = 0.3 + i * 0.3
    s1_items += [('box', t, 70, y - 50, 1010, y + 50, (244, 240, 236)), ('label', t, a, 110, y, 40, INK, 'l'), ('label', t, b, 970, y, 46, c, 'r')]
s1 = dict(D, dur=4.0, items=s1_items, texts=[(0.05, 'top', '9월 배당표엔\n{이름도 없었다}')], sfx=[(1.25, 'ding')])

BOOKS = [('짧은 이야기들', 132), ('녹스', 192), ('남편의 아름다움', 204), ('레드 닥>', 208), ('빨강의 자서전', 256),
         ('플로트', 292), ('에로스, 달콤씁쓸한', 320), ('유리, 아이러니…', 324), ('플레인워터', 396)]
s2_items = [('label', 0.1, '국내에 나온 앤 카슨 책 · 쪽수(알라딘)', 540, 610, 32, MUTED)]
for i, (n, pg) in enumerate(BOOKS):
    s2_items.append(('label', 0.2 + i * 0.12, n, 90, 690 + i * 72, 30, INK, 'l'))
    s2_items.append(('hbar', 0.2 + i * 0.12, '', pg, 520, 690 + i * 72, CRIM if n == '빨강의 자서전' else (190, 160, 160), f'{pg}쪽'))
s2 = dict(D, dur=4.2, items=s2_items, texts=[(0.05, 'top', '국내에 이미\n{아홉 종}')], sfx=[(0.75, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('label', 0.1, '발표 다음 날 아침까지 · 발표 전 대비', 540, 640, 34, MUTED),
    ('hbar', 0.3, '예스24', 184, 220, 780, CRIM, '약 184배'),
    ('hbar', 0.6, '교보문고', 138, 220, 910, (200, 90, 90), '약 138배'),
    ('label', 1.3, '『빨강의 자서전』 두 곳 모두 일간 1위', 540, 1050, 40, INK),
    ('label', 1.6, '알라딘 실시간 1~4위가 전부 카슨', 540, 1130, 36, MUTED)],
    texts=[(0.05, 'top', '하룻밤 새\n{184배}')], sfx=[(0.35, 'ding')])

s4 = dict(D, dur=4.2, items=[
    ('label', 0.2, '어디서부터 읽냐는 질문에', 540, 660, 38, MUTED),
    ('label', 0.5, '「중간부터 시작하라」', 540, 750, 60, CRIM),
    ('box', 1.0, 70, 840, 1010, 1060, (248, 238, 236)),
    ('label', 1.1, '가장 많이 읽힌 책 · 빨강의 자서전 256쪽', 540, 905, 34, INK),
    ('label', 1.3, '가장 짧은 책 · 짧은 이야기들 132쪽', 540, 990, 34, INK),
    ('box', 1.8, 90, 1110, 990, 1290, PINK),
    ('label', 1.9, '너는 어떤 책부터 펼칠 거야?', 540, 1175, 46, CRIM),
    ('label', 2.2, '댓글로 알려줘', 540, 1245, 34, INK)],
    texts=[(0.05, 'top', '처음이라면\n{두 갈래}')], sfx=[(0.55, 'ding')])

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
        build(SCENES, BASE, 'AC', 'carson_clip.mp4')
