# 제주 마일리지 항공권 주말 클립 (발행 10/5, logNo 224431468613) — 정보형
# 실행: python clipJ.py stills / python clipJ.py → out\jeju_weekend_clip.mp4
# 숫자는 발행 본문 표 그대로(10/4 밤 예매 화면 조회 · 10/10~12/26 12주말 · 아침=10시 전, 저녁=17시 이후)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)
KE, OZ = NAVY, (200, 70, 60)
EMPTY = (232, 232, 228)
SAT = ['10/10', '10/17', '10/24', '10/31', '11/7', '11/14', '11/21', '11/28', '12/5', '12/12', '12/19', '12/26']


def grid(t0, rows, y0, title):
    """주말 12칸 × 항공사 2줄. rows=[(이름, 색, {칸번호: '10편'})]"""
    items = [('label', t0, title, 540, y0 - 70, 34, MUTED)]
    for c, s in enumerate(SAT):
        items.append(('label', t0, s, 140 + c * 72 + 30, y0 - 20, 20, MUTED))
    for r, (name, col, on) in enumerate(rows):
        y = y0 + 20 + r * 110
        items.append(('label', t0, name, 70, y + 40, 28, col, 'l'))
        for c in range(12):
            x = 140 + c * 72
            filled = c in on
            items.append(('box', t0 + 0.25 + c * 0.06, x, y, x + 62, y + 80, col if filled else EMPTY))
            if filled:
                items.append(('label', t0 + 0.3 + c * 0.06, on[c], x + 31, y + 40, 20, (255, 255, 255)))
    return items


s0 = dict(D, dur=3.6, items=[
    ('label', 0.1, '일요일 저녁 제주→김포 · 마일리지 좌석', 540, 680, 38, MUTED),
    ('box', 0.3, 90, 740, 520, 1060, SKY), ('label', 0.35, '대한항공', 305, 800, 40, KE), ('label', 0.45, '12번 중 0번', 305, 930, 60, KE),
    ('box', 0.8, 560, 740, 990, 1060, PINK), ('label', 0.85, '아시아나', 775, 800, 40, OZ), ('label', 0.95, '12번 중 0번', 775, 930, 60, OZ),
    ('label', 1.6, '토 아침 가서 일 저녁 오는 한라산 1박 2일, 안 됐다', 540, 1180, 38, INK)],
    texts=[(0.05, 'top', '한라산 주말,\n{마일리지로 될까?}')], sfx=[(0.1, 'ding'), (1.0, 'ding')])

s1 = dict(D, dur=3.8, items=grid(0.1, [('대한', KE, {0: '10편', 8: '1편'}), ('아시', OZ, {0: '5편'})], 760,
                                 '토요일 아침(10시 전) 김포→제주 · 좌석 있던 토요일') +
    [('label', 1.6, '대한항공 12번 중 2번 · 아시아나 12번 중 1번', 540, 1120, 40, INK)],
    texts=[(0.05, 'top', '토요일 아침에 가는 편도\n{거의 없다}')], sfx=[(1.6, 'ding')])

s2 = dict(D, dur=3.4, items=grid(0.1, [('대한', KE, {}), ('아시', OZ, {})], 760, '일요일 저녁(17시 이후) 제주→김포') +
    [('label', 1.4, '두 항공사 모두 12번 중 0번', 540, 1120, 48, RED),
     ('label', 1.8, '좌석 있던 일요일은 전부 아침 편', 540, 1200, 36, INK)],
    texts=[(0.05, 'top', '일요일 저녁은\n{한 번도 없었다}')], sfx=[(1.4, 'ding')])

COMBO = [('토아침→일저녁', 0, 0), ('금저녁→일아침', 4, 1), ('금저녁→월아침', 4, 2), ('토저녁→월저녁', 5, 3), ('토→월 아무때', 7, 9)]
s3 = dict(D, dur=4.0, items=[('label', 0.1, '■ 대한항공', 380, 640, 32, KE), ('label', 0.1, '■ 아시아나', 700, 640, 32, OZ),
                             ('label', 0.1, '12주말 중 가는 편·오는 편이 같이 열린 횟수', 540, 590, 30, MUTED)] +
    [('pair', 0.3 + i * 0.18, n, a, b, 12, 740 + i * 110, KE, OZ, '번') for i, (n, a, b) in enumerate(COMBO)] +
    [('label', 1.8, '금요일 밤 내려가서 일요일 아침에 올라오기', 540, 1330, 40, NAVY)],
    texts=[(0.05, 'top', '대신 이 조합은\n{열려 있었다}')], sfx=[(0.5, 'ding')])

s4 = dict(D, dur=3.8, items=[
    ('label', 0.2, '10월 4일 밤 기준 · 좌석은 하루에도 바뀐다', 540, 720, 38, MUTED),
    ('label', 0.6, '오전 9시 지나서 한 번 더', 540, 830, 60, NAVY),
    ('box', 1.4, 90, 990, 990, 1250, PINK),
    ('label', 1.5, '너는 제주 갈 때 마일리지 써?', 540, 1080, 50, RED),
    ('label', 1.9, '댓글로 알려줘', 540, 1175, 40, INK)],
    texts=[(0.05, 'top', '0번이라고\n{포기는 이르다}')], sfx=[(0.6, 'ding')])

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
        build(SCENES, BASE, 'J', 'jeju_weekend_clip.mp4')
