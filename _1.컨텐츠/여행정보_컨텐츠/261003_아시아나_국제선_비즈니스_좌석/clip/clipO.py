# 아시아나 마일리지 비즈니스 합병 전 74일 클립 (발행 10/4, logNo 224430913269) — 정보형
# 실행: python clipO.py stills / python clipO.py → out\oz_biz_clip.mp4
# 숫자는 발행 본문 표 그대로(10/3 밤~10/4 새벽 조회, 성인 1명 편도, 비즈니스만, 10/4~12/16 74일 중 며칠)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)
GO, BACK = NAVY, (95, 160, 220)          # 가는 편 · 오는 편
LEG = [('label', 0.1, '■ 가는 편', 380, 640, 32, GO), ('label', 0.1, '■ 오는 편', 700, 640, 32, BACK)]


def rows(t0, data, y0=740, dy=95):
    return [('pair', t0 + i * 0.15, n, a, b, 74, y0 + i * dy, GO, BACK) for i, (n, a, b) in enumerate(data)]


s0 = dict(D, dur=3.4, items=[
    ('label', 0.1, '아시아나 마일리지 비즈니스 · 74일 중', 540, 660, 38, MUTED),
    ('box', 0.3, 90, 720, 520, 1060, PINK), ('label', 0.35, '런던 → 인천', 305, 790, 40, RED),
    ('count', 0.4, 0, 13, '{:.0f}일', 305, 920, 110, RED),
    ('box', 0.8, 560, 720, 990, 1060, SKY), ('label', 0.85, '인천 → 오사카', 775, 790, 40, NAVY),
    ('count', 0.9, 0, 70, '{:.0f}일', 775, 920, 110, NAVY),
    ('label', 1.6, '장거리만 안 풀린다', 540, 1180, 56, INK)],
    texts=[(0.05, 'top', '합병 전 74일,\n{비즈니스} 어디 갈 수 있어?')], sfx=[(0.1, 'ding'), (1.6, 'ding')])

s1 = dict(D, dur=3.2, items=[
    ('label', 0.2, '아시아나 규정 그대로 쓰는 건', 540, 720, 46, MUTED),
    ('label', 0.5, '12월 16일 출발까지', 540, 850, 90, RED),
    ('label', 1.2, '합병 뒤에도 마일리지는 10년 남지만', 540, 1010, 40, INK),
    ('label', 1.5, '쓰는 조건이 달라진다', 540, 1080, 40, INK)],
    texts=[(0.05, 'top', '마감은\n{12월 16일}')], sfx=[(0.6, 'ding')])

s2 = dict(D, dur=4.0, items=LEG + rows(0.3, [('런던', 0, 13), ('파리', 1, 1), ('프랑크푸르트', 1, 0), ('로마', 3, 0),
                                              ('밀라노', 4, 0), ('바르셀로나', 2, 0), ('프라하', 0, 2), ('이스탄불', 1, 0)], dy=88) +
    [('label', 1.9, '왕복이 되는 곳은 파리 하루씩뿐', 540, 1490, 40, RED)],
    texts=[(0.05, 'top', '유럽은\n{한 자리 수}')], sfx=[(1.9, 'ding')])

s3 = dict(D, dur=3.4, items=LEG + rows(0.3, [('뉴욕', 4, 0), ('LA', 6, 0), ('샌프란시스코', 1, 0), ('시애틀', 4, 0)], y0=780, dy=120) +
    [('label', 1.4, '돌아오는 비즈니스는 네 곳 모두 0일', 540, 1300, 42, RED)],
    texts=[(0.05, 'top', '미주는\n{오는 편 0일}')], sfx=[(1.4, 'ding')])

s4 = dict(D, dur=4.0, items=LEG + rows(0.3, [('오사카', 70, 66), ('도쿄 하네다', 65, 49), ('다롄', 70, 74), ('베이징', 69, 70),
                                              ('마닐라', 62, 61), ('방콕', 2, 2), ('싱가포르', 0, 0)], dy=95) +
    [('label', 1.9, '일본·중국은 거의 매일, 방콕·싱가포르는 드물게', 540, 1450, 38, NAVY)],
    texts=[(0.05, 'top', '일본·중국은\n{거의 매일}')], sfx=[(1.9, 'ding')])

s5 = dict(D, dur=3.8, items=[
    ('label', 0.2, '좌석은 하루에도 바뀐다', 540, 720, 44, MUTED),
    ('label', 0.5, '오전 9시 지나서 한 번 더', 540, 830, 64, NAVY),
    ('label', 0.9, '좌석등급은 「비즈니스」만 골라서 조회', 540, 930, 40, INK),
    ('box', 1.5, 90, 1060, 990, 1320, PINK),
    ('label', 1.6, '아시아나 마일리지, 어디에 쓸 거야?', 540, 1150, 48, RED),
    ('label', 2.0, '댓글로 알려줘', 540, 1245, 40, INK)],
    texts=[(0.05, 'top', '0일이라고\n{포기는 이르다}')], sfx=[(0.6, 'ding')])

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
        build(SCENES, BASE, 'O', 'oz_biz_clip.mp4')
