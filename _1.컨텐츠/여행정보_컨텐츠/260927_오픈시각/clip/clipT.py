# 대한항공 마일리지 좌석 오픈 시간 클립 (발행 9/28, logNo 224423671841) — 정보형
# 실행: python clipT.py stills / python clipT.py → out\open_time_clip.mp4
# 숫자는 발행 본문 표 그대로(9/18·9/20·9/27 측정, 2027.9.22 인천-나리타, KE902 9:01 9석 → 9:12 매진)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)
GREEN = (46, 125, 80)

# 0 후킹: 시계가 넘어가면 0편 → 5편 (앞 숫자는 바탕색 상자로 덮고 새 숫자를 띄운다)
s0 = dict(D, dur=3.6, items=[
    ('label', 0.1, '2027.9.22 출발 인천-나리타 · 1분마다 조회', 540, 660, 34, MUTED),
    ('label', 0.2, '08:59:34', 540, 820, 130, INK), ('label', 0.3, '0편', 540, 1000, 96, RED),
    ('box', 1.6, 60, 730, 1020, 1090, LIGHT),
    ('label', 1.62, '09:00:42', 540, 820, 130, NAVY), ('count', 1.7, 0, 5, '{:.0f}편', 540, 1000, 96, GREEN),
    ('label', 2.2, '1분 사이에 없던 날짜가 생겼다', 540, 1160, 44, INK)],
    texts=[(0.05, 'top', '대한항공 마일리지 좌석\n{몇 시}에 열릴까?')], sfx=[(0.1, 'ding'), (1.65, 'ding')])

ROWS = [('9월 18일', '07:39', '09:00'), ('9월 20일', '05:40', '20:40'), ('9월 27일', '08:59:34', '09:00:42')]
s1_items = [('label', 0.1, '측정한 날', 220, 680, 32, MUTED), ('label', 0.1, '닫혀 있던 시각', 560, 680, 32, MUTED),
            ('label', 0.1, '열려 있던 시각', 860, 680, 32, MUTED)]
for i, (d, a, b) in enumerate(ROWS):
    y = 790 + i * 130; t = 0.3 + i * 0.3
    s1_items += [('box', t, 70, y - 50, 1010, y + 50, (240, 240, 236)), ('label', t, d, 220, y, 42, INK),
                 ('label', t, a, 560, y, 42, RED), ('label', t, b, 860, y, 42, GREEN)]
s1_items.append(('label', 1.5, '세 번 모두 9시 전엔 닫힘 · 9시 뒤엔 열림', 540, 1230, 42, NAVY))
s1 = dict(D, dur=3.4, items=s1_items, texts=[(0.05, 'top', '세 번 쟀는데\n{세 번 다 9시}')], sfx=[(1.5, 'ding')])

s2 = dict(D, dur=3.8, items=[
    ('label', 0.2, '타고 싶은 날짜', 540, 700, 44, INK),
    ('label', 0.5, '- 360일', 540, 820, 100, RED),
    ('label', 0.9, '= 오픈일, 그날 오전 9시', 540, 960, 56, NAVY),
    ('box', 1.4, 90, 1060, 990, 1240, SKY),
    ('label', 1.5, '예) 2027.12.24 출발', 540, 1115, 40, INK),
    ('label', 1.7, '→ 2026.12.29 오전 9시 오픈', 540, 1185, 44, NAVY)],
    texts=[(0.05, 'top', '361일 전이 아니라\n{360일 전 오전 9시}')], sfx=[(0.6, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('label', 0.1, '똑같이 비어 보여도', 540, 650, 36, MUTED),
    ('box', 0.3, 70, 720, 1010, 850, (240, 240, 236)), ('label', 0.3, '날짜 선택이 안 됨', 110, 760, 38, INK, 'l'), ('label', 0.3, '아직 안 연 날', 110, 815, 32, MUTED, 'l'),
    ('box', 0.6, 70, 870, 1010, 1000, PINK), ('label', 0.6, '항공편 0건, 오류 없음', 110, 910, 38, INK, 'l'), ('label', 0.6, '오늘 9시에 열릴 날 (매진 아님)', 110, 965, 32, RED, 'l'),
    ('box', 0.9, 70, 1020, 1010, 1150, (240, 240, 236)), ('label', 0.9, '항공편 있는데 좌석 0', 110, 1060, 38, INK, 'l'), ('label', 0.9, '매진 → 며칠 뒤 다시', 110, 1115, 32, MUTED, 'l'),
    ('label', 1.6, '인천-나리타도 0건이면 아직 안 연 거야', 540, 1240, 40, NAVY)],
    texts=[(0.05, 'top', '9시 전 빈 목록은\n{매진이 아니야}')], sfx=[(0.65, 'ding')])

s4 = dict(D, dur=3.6, items=[
    ('label', 0.1, 'KE902 파리→인천 · 2027.9.22 일반석', 540, 660, 36, MUTED),
    ('box', 0.3, 90, 720, 520, 1060, SKY), ('label', 0.35, '9시 1분', 305, 790, 42, NAVY), ('count', 0.4, 0, 9, '{:.0f}석', 305, 920, 110, NAVY),
    ('box', 0.9, 560, 720, 990, 1060, PINK), ('label', 0.95, '9시 12분', 775, 790, 42, RED), ('label', 1.0, '매진', 775, 920, 110, RED),
    ('label', 1.5, '열리는 순간 재고가 같이 들어온다', 540, 1180, 44, INK)],
    texts=[(0.05, 'top', '파리 귀국편은\n{11분 만에 매진}')], sfx=[(1.0, 'ding')])

s5 = dict(D, dur=3.8, items=[
    ('label', 0.2, '노리는 날짜 360일 전, 아침 9시', 540, 720, 48, NAVY),
    ('label', 0.6, '놓쳤으면 며칠 뒤 다시 — 매진 구간에 1~3석이 다시 열렸다', 540, 820, 32, INK),
    ('box', 1.4, 90, 990, 990, 1250, PINK),
    ('label', 1.5, '너는 몇 시에 마일리지 좌석 봐?', 540, 1080, 48, RED),
    ('label', 1.9, '댓글로 알려줘', 540, 1175, 40, INK)],
    texts=[(0.05, 'top', '한 번 보고\n{포기하지 마}')], sfx=[(0.3, 'ding')])

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
        build(SCENES, BASE, 'T', 'open_time_clip.mp4')
