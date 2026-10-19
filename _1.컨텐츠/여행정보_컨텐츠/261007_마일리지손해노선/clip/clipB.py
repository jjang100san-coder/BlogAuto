# 마일리지 항공권 손해 노선(일본 18개) 클립 (발행 10/7 17:00, logNo 224434102983) — 가치 클립의 「다음 편」
# 실행: python clipB.py stills  /  python clipB.py → out\mile_loss_clip.mp4
# 숫자는 발행 본문 표 그대로(2026.10.7 조회 · 11월 출발 날짜 4개 · 30,000마일). 노선 이름은 화면 폭 때문에 줄임
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)

s0 = dict(D, dur=3.4, items=[
    ('label', 0.1, '2026.11.10 인천 ↔ 가고시마 왕복', 540, 640, 36, MUTED),
    ('box', 0.3, 90, 700, 520, 1020, SKY), ('label', 0.35, '현금 운임', 305, 770, 38, NAVY),
    ('count', 0.4, 0, 90000, '{:,.0f}원', 305, 900, 70, NAVY),
    ('box', 0.8, 560, 700, 990, 1020, PINK), ('label', 0.85, '마일', 775, 770, 38, RED),
    ('count', 0.9, 0, 30000, '{:,.0f}마일', 775, 900, 64, RED),
    ('label', 1.6, '1마일 = 3원', 540, 1170, 100, RED)],
    texts=[(0.05, 'top', '운임 9만 원짜리 왕복에\n{3만 마일} 쓸 거야?')], sfx=[(0.1, 'ding'), (1.6, 'ding')])

s1 = dict(D, dur=3.0, items=[
    ('label', 0.2, '대한항공 11월 일본 노선', 540, 700, 44, MUTED),
    ('count', 0.3, 0, 18, '{:.0f}개', 540, 840, 120, NAVY),
    ('label', 0.9, '× 날짜 4개', 540, 990, 56, INK),
    ('count', 1.2, 0, 72, '{:.0f}번 조회', 540, 1140, 96, RED)],
    texts=[(0.05, 'top', '그래서 {전부} 조회했어')], sfx=[(1.2, 'ding')])

ROUTES = [('김포↔간사이', 4.0, 5.0), ('아오모리', 4.7, 5.3), ('구마모토', 3.0, 5.5), ('인천↔간사이', 3.7, 5.7),
          ('가고시마', 3.0, 5.7), ('고베', 4.0, 6.6), ('나고야', 4.3, 6.7), ('니가타', 3.7, 7.2), ('후쿠오카', 6.7, 7.3),
          ('오카야마', 3.7, 7.3), ('나리타', 4.3, 7.7), ('오이타', 4.3, 7.8), ('나가사키', 6.3, 8.5), ('고마쓰', 3.7, 10.8),
          ('오키나와', 9.7, 11.7), ('인천↔하네다', 5.7, 13.7), ('삿포로', 5.3, 15.0), ('김포↔하네다', 15.7, 18.3)]
Y0, DY = 560, 60
s2 = dict(D, dur=4.8, items=[
    ('range', 0.2 + i * 0.1, n, lo, hi, 20, Y0 + i * DY, RED if hi < 10 else NAVY, PINK if hi < 10 else None, 26)
    for i, (n, lo, hi) in enumerate(ROUTES)] + [
    ('vline', 2.2, 10, 20, Y0 - 30, Y0 + 17 * DY + 30, '10원', RED)],
    texts=[(0.05, 'top', '11월 일본 18개 노선\n1마일은 몇 원?', 2.6), (2.6, 'top', '18개 중 {13개}는\n네 날짜 모두 10원 미만')],
    sfx=[(2.65, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('label', 0.1, '2026.11.27 인천 ↔ 간사이 왕복', 540, 700, 36, MUTED),
    ('stack', 0.2, 760, [('운임', 111000, NAVY), ('세금·유류할증료', 212200, RED)], 330000, 160),
    ('label', 1.3, '다섯 노선은 11월 네 날짜 모두', 540, 1060, 40, MUTED),
    ('label', 1.6, '운임 < 세금·유류할증료', 540, 1160, 60, RED),
    ('label', 2.1, '김포·인천↔간사이 · 나고야 · 고베 · 아오모리', 540, 1270, 34, INK)],
    texts=[(0.05, 'top', '마일로 끊어도\n{세금이 운임보다 크다}')], sfx=[(1.6, 'ding')])

s4 = dict(D, dur=3.6, items=[
    ('label', 0.1, '같은 도쿄 · 11월 27일 출발', 540, 700, 36, MUTED),
    ('hbar', 0.3, '김포↔하네다', 17.0, 20, 860, NAVY, '17.0원'),
    ('hbar', 0.7, '인천↔나리타', 4.3, 20, 1010, RED, '4.3원'),
    ('vline', 1.1, 10, 20, 800, 1060, '10원', RED),
    ('label', 1.7, '운임 510,000원 vs 130,000원', 540, 1230, 44, INK)],
    texts=[(0.05, 'top', '같은 도쿄도\n{4배 차이}')], sfx=[(1.7, 'ding')])

s5 = dict(D, dur=3.8, items=[
    ('label', 0.2, '일본에 쓰더라도', 540, 740, 46, MUTED),
    ('label', 0.5, '현금 운임 · 세금부터 나란히', 540, 850, 60, NAVY),
    ('box', 1.4, 90, 1010, 990, 1270, PINK),
    ('label', 1.5, '너는 1마일 몇 원 넘으면 써?', 540, 1100, 52, RED),
    ('label', 1.9, '댓글로 알려줘', 540, 1195, 40, INK)],
    texts=[(0.05, 'top', '마일 좌석보다\n{이것부터}')], sfx=[(1.5, 'ding')])

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
        build(SCENES, BASE, 'B', 'mile_loss_clip.mp4')
