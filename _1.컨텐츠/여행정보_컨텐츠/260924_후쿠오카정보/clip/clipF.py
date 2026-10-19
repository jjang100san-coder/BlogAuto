# 후쿠오카 9·10·11월 날씨 클립 (발행 9/29, logNo 224421770374) — 정보형
# 실행: python clipF.py stills / python clipF.py → out\fukuoka_weather_clip.mp4
# 10월 꺾은선은 fukuoka_weather_bundle\data\후쿠오카_일별관측_JMA.csv(일본 기상청 원자료) 값 그대로. 나머지 숫자는 발행 본문 표
import os, sys, csv
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
D = dict(type='data', render=render, bg=LIGHT)
ORANGE = (226, 140, 30)

rows = list(csv.DictReader(open(os.path.join(ROOT, 'fukuoka_weather_bundle', 'data', '후쿠오카_일별관측_JMA.csv'), encoding='utf-8-sig')))
OCT = {y: [float(r['최고기온']) for r in rows if r['일자'].startswith(y + '-10-')] for y in ('2023', '2024', '2025')}

s0 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(ROOT, 'sep_dazaifu_20240901.jpg'), 60, 600, 530, 1230),
    ('image', 0.4, os.path.join(ROOT, 'nov_ohori_20231125.jpg'), 550, 600, 1020, 1230),
    ('label', 0.8, '2024.9.1 다자이후', 295, 1280, 34, RED), ('label', 0.9, '최고 32.4도', 295, 1340, 46, RED),
    ('label', 1.1, '2023.11.25 오호리공원', 785, 1280, 34, NAVY), ('label', 1.2, '최고 14.1도', 785, 1340, 46, NAVY)],
    texts=[(0.05, 'top', '같은 후쿠오카 가을\n{반팔 vs 두꺼운 겉옷}')], sfx=[(0.1, 'ding')])

s1 = dict(D, dur=3.4, items=[
    ('label', 0.1, '11월 26일 최저기온', 540, 680, 46, MUTED),
    ('box', 0.3, 70, 740, 370, 1040, SKY), ('label', 0.35, '2023 (내가 간 해)', 220, 800, 30, NAVY),
    ('count', 0.4, 0, 6.1, '{:.1f}도', 220, 920, 76, NAVY),
    ('box', 0.6, 390, 740, 690, 1040, PINK), ('label', 0.65, '2024', 540, 800, 30, RED),
    ('count', 0.7, 0, 12.5, '{:.1f}도', 540, 920, 76, RED),
    ('box', 0.9, 710, 740, 1010, 1040, (240, 240, 236)), ('label', 0.95, '2025', 860, 800, 30, INK),
    ('count', 1.0, 0, 9.5, '{:.1f}도', 860, 920, 76, INK),
    ('label', 1.6, '같은 날짜인데 6.4도 차이', 540, 1160, 52, INK)],
    texts=[(0.05, 'top', '「작년엔 이랬어」가\n{안 맞더라}')], sfx=[(1.6, 'ding')])

s2 = dict(D, dur=4.4, items=[
    ('label', 0.1, '10월 일별 최고기온 · 일본 기상청', 540, 610, 34, MUTED),
    ('line', 0.3, [('2023', OCT['2023'], ORANGE), ('2024', OCT['2024'], RED), ('2025', OCT['2025'], NAVY)],
     (110, 680, 900, 1230), (15, 33), 2.4, 28, '반팔 기준 28도'),
    ('label', 0.2, '10/1', 110, 1265, 28, MUTED, 'l'), ('label', 0.2, '10/31', 900, 1265, 28, MUTED, 'r'),
    ('label', 2.9, '반팔 마지막 날  2023 10/1 · 2024 10/21 · 2025 10/18', 540, 1360, 36, INK)],
    texts=[(0.05, 'top', '10월은\n{언제 꺾일지} 해마다 달라')], sfx=[(2.9, 'ding')])

GRID = [('9월', (2.1, 4.7, 3.3)), ('10월', (0.6, 2.0, 2.5)), ('11월', (1.3, 1.0, 1.0))]
s3_items = [('label', 0.1, '월평균 최고기온 · 평년 대비', 540, 620, 34, MUTED)]
for j, y in enumerate(('2023', '2024', '2025')):
    s3_items.append(('label', 0.2, y, 400 + j * 220, 700, 34, INK))
for i, (m, vals) in enumerate(GRID):
    s3_items.append(('label', 0.2, m, 170, 800 + i * 160, 40, INK))
    for j, v in enumerate(vals):
        t = 0.4 + (i * 3 + j) * 0.12
        x, y = 400 + j * 220, 800 + i * 160
        s3_items += [('box', t, x - 95, y - 60, x + 95, y + 60, PINK), ('label', t, f'+{v}도', x, y, 44, RED)]
s3_items.append(('label', 1.8, '아홉 칸 전부 플러스 — 한 번도 안 뒤집혔다', 540, 1340, 40, RED))
s3 = dict(D, dur=3.8, items=s3_items, texts=[(0.05, 'top', '딱 하나 일관된 건\n{평년보다 더웠다}')], sfx=[(1.8, 'ding')])

s4 = dict(D, dur=3.8, items=[
    ('label', 0.2, '9월은 여름옷 · 11월은 가을·겨울옷', 540, 740, 44, INK),
    ('label', 0.6, '10월은 둘 다 겹쳐 입게', 540, 850, 62, NAVY),
    ('box', 1.4, 90, 1010, 990, 1270, PINK),
    ('label', 1.5, '너는 후쿠오카 몇 월에 가?', 540, 1100, 52, RED),
    ('label', 1.9, '댓글로 알려줘', 540, 1195, 40, INK)],
    texts=[(0.05, 'top', '그래서\n{이렇게 싸기로 했어}')], sfx=[(0.6, 'ding')])

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
        build(SCENES, BASE, 'F', 'fukuoka_weather_clip.mp4')
