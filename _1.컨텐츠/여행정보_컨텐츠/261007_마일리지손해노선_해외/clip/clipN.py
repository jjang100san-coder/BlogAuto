# 나트랑 괌 마일리지 항공권 클립 (발행 10/8 10:00, logNo 224434220442) — 정보형 · 마일리지 시리즈 3편
# 실행: python clipN.py stills / python clipN.py → out\mile_sea_clip.mp4
# 숫자는 발행 본문 표 그대로(2026.10.7 조회 · 11월 출발 4날짜 · 4박 왕복)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)

s0 = dict(D, dur=3.4, items=[
    ('label', 0.1, '2026년 11월 인천 ↔ 괌 왕복', 540, 640, 36, MUTED),
    ('box', 0.3, 90, 700, 520, 1020, SKY), ('label', 0.35, '현금 운임', 305, 770, 38, NAVY),
    ('count', 0.4, 0, 70000, '{:,.0f}원', 305, 900, 70, NAVY),
    ('box', 0.8, 560, 700, 990, 1020, PINK), ('label', 0.85, '마일', 775, 770, 38, RED),
    ('count', 0.9, 0, 40000, '{:,.0f}마일', 775, 900, 64, RED),
    ('label', 1.6, '1마일 = 1.8원', 540, 1170, 100, RED)],
    texts=[(0.05, 'top', '운임 7만 원 왕복에\n{4만 마일} 쓸 거야?')], sfx=[(0.1, 'ding'), (1.6, 'ding')])

s1 = dict(D, dur=3.4, items=[
    ('label', 0.1, '현금 표 · 인천 ↔ 괌 11월 네 날짜 모두', 540, 700, 34, MUTED),
    ('stack', 0.2, 760, [('운임', 70000, NAVY), ('세금·유류할증료', 383200, RED)], 470000, 160),
    ('label', 1.3, '마일로 끊어도 383,200원은 그대로', 540, 1060, 48, RED),
    ('label', 1.7, '나트랑 11/13 출발도 운임 70,000원 · 1.8원', 540, 1160, 36, INK)],
    texts=[(0.05, 'top', '세금·유류할증료가\n{운임의 5배 넘게}')], sfx=[(1.3, 'ding')])

SEA = [('괌', 1.8, 1.8), ('나트랑', 1.8, 8.1), ('마닐라', 3.2, 3.2), ('다낭', 3.2, 6.9), ('호찌민', 3.8, 3.8), ('푸껫', 4.5, 6.5),
       ('세부', 5.5, 5.5), ('치앙마이', 5.8, 5.8), ('방콕', 6.0, 6.0), ('푸꾸옥', 6.2, 6.2), ('싱가포르', 7.2, 7.2),
       ('하노이', 7.5, 7.5), ('자카르타', 8.0, 8.0), ('발리', 11.2, 13.1), ('카트만두', 19.4, 19.4)]
Y0, DY = 560, 66
s2 = dict(D, dur=4.6, items=[
    ('range', 0.2 + i * 0.1, n, lo, hi, 20, Y0 + i * DY, RED if hi < 10 else NAVY, PINK if hi < 10 else None, 28)
    for i, (n, lo, hi) in enumerate(SEA)] + [('vline', 2.0, 10, 20, Y0 - 30, Y0 + 14 * DY + 30, '10원', RED)],
    texts=[(0.05, 'top', '38개 노선 중 {24개}\n네 날짜 모두 10원 미만', 99)], sfx=[(2.05, 'ding')])

s3 = dict(D, dur=3.4, items=[
    ('label', 0.1, '같은 40,000마일', 540, 640, 46, INK),
    ('box', 0.3, 90, 720, 520, 1060, SKY), ('label', 0.35, '발리 11/10', 305, 790, 38, NAVY),
    ('count', 0.4, 0, 450000, '{:,.0f}원', 305, 915, 64, NAVY),
    ('box', 0.8, 560, 720, 990, 1060, PINK), ('label', 0.85, '나트랑 11/13', 775, 790, 38, RED),
    ('count', 0.9, 0, 70000, '{:,.0f}원', 775, 915, 64, RED),
    ('label', 1.6, '마일이 대신 내 준 운임이 이만큼 달랐다', 540, 1180, 44, INK)],
    texts=[(0.05, 'top', '같은 동남아,\n{6배 넘게 차이}')], sfx=[(1.6, 'ding')])

s4 = dict(D, dur=3.8, items=[
    ('label', 0.2, '일본 · 동남아 · 중국까지 보고 나니', 540, 740, 40, MUTED),
    ('label', 0.6, '마일 좌석보다 현금 운임부터', 540, 850, 58, NAVY),
    ('box', 1.4, 90, 1010, 990, 1270, PINK),
    ('label', 1.5, '너는 동남아 갈 때 마일 써?', 540, 1100, 50, RED),
    ('label', 1.9, '댓글로 알려줘', 540, 1195, 40, INK)],
    texts=[(0.05, 'top', '쓰더라도\n{가치 있게}')], sfx=[(0.6, 'ding')])

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
        build(SCENES, BASE, 'N', 'mile_sea_clip.mp4')
