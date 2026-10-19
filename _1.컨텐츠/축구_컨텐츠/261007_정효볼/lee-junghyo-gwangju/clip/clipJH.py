# 이정효 감독 광주FC 4년 클립 (발행 10/9, logNo 224434539197) — 정보형 · 정효볼 연재 1편
# 실행: python clipJH.py stills / python clipJH.py → out\junghyo_gwangju_clip.mp4
# 숫자는 발행본 그대로. 글에 넣은 카드(images/)를 화면에 쓰고, 호칭은 「○○○ 감독」「○○○ 선수」로 통일(지침 6-2)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(BASE), 'images')
DARK = (24, 24, 28)
GOLD = (240, 190, 60)
D = dict(type='data', render=render, bg=DARK)
W_ = (235, 235, 235)

s0 = dict(D, dur=3.8, items=[
    ('image', 0.1, os.path.join(IMG, '01_thumb.png'), 140, 540, 940, 1340)],
    texts=[(0.05, 'top', '0-2를 3-2로\n{정효팬이 된 밤}')], sfx=[(0.1, 'ding')])

s1 = dict(D, dur=4.2, items=[
    ('image', 0.1, os.path.join(IMG, '03_timeline.png'), 140, 520, 940, 1300),
    ('label', 0.6, '가진 게 없는 시민구단이 올라간 4년', 540, 1340, 34, GOLD)],
    texts=[(0.05, 'top', '광주FC 4년\n{말을 성적으로}')], sfx=[(0.4, 'ding')])

s2 = dict(D, dur=4.4, items=[
    ('image', 0.1, os.path.join(IMG, '04_kobe.png'), 110, 540, 970, 1270),
    ('label', 0.8, '2025년 3월 12일 · 광주월드컵경기장', 540, 1310, 32, W_)],
    texts=[(0.05, 'top', '비셀 고베전\n{합계 3-2 역전}')], sfx=[(0.5, 'ding'), (1.6, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('label', 0.2, '경기만 끝나면 기사 제목이 되는 거친 말', 540, 700, 36, W_),
    ('label', 0.6, '그런데 화살은', 540, 800, 48, W_),
    ('label', 0.9, '선수를 향하지 않았다', 540, 890, 64, GOLD),
    ('label', 1.5, '선수는 못하는 게 아니라 몰랐던 거라고', 540, 1010, 34, (180, 180, 180))],
    texts=[(0.05, 'top', '말이 센 감독\n{그 말의 방향}')], sfx=[(0.9, 'ding')])

s4 = dict(D, dur=4.2, items=[
    ('image', 0.1, os.path.join(IMG, '02_namecard.png'), 230, 520, 850, 1270),
    ('box', 1.2, 90, 1300, 990, 1460, (60, 52, 30)),
    ('label', 1.3, '너는 팀을 응원해, 사람을 응원해?', 540, 1355, 40, GOLD),
    ('label', 1.7, '정효팬 연재 시작 · 다음은 수원삼성', 540, 1420, 30, W_)],
    texts=[(0.05, 'top', '팀이 아니라\n{사람을 따라간다}')], sfx=[(1.3, 'ding')])

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
        build(SCENES, BASE, 'JH', 'junghyo_gwangju_clip.mp4')
