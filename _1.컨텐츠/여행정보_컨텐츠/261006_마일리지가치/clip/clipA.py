# 대한항공 마일리지 가치 클립 (발행 10/7 07:20, logNo 224433381419) — 끝은 「일본 18개 노선은? 다음 편」
# 실행: python clipA.py stills  /  python clipA.py → out\mile_value_clip.mp4
# 숫자는 전부 발행 본문 그대로(영수증 네 쌍 · 2026.10.6 조회 2027 날짜 20개). 삿포로 2027 범위 7.0~18.7 은 본문 문장(3/12 210,000원, 1/31 18.7원)에서
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)

s0 = dict(D, dur=3.2, items=[
    ('label', 0.1, '같은 대한항공 1마일', 540, 640, 46, MUTED),
    ('box', 0.3, 90, 720, 520, 1060, SKY), ('label', 0.35, '2024 삿포로', 305, 790, 40, NAVY),
    ('count', 0.4, 0, 23.3, '{:.1f}원', 305, 915, 100, NAVY), ('label', 0.5, '내 영수증', 305, 1010, 30, MUTED),
    ('box', 0.8, 560, 720, 990, 1060, PINK), ('label', 0.85, '2027 설 간사이', 775, 790, 40, RED),
    ('count', 0.9, 0, 4.4, '{:.1f}원', 775, 915, 100, RED), ('label', 1.0, '조회', 775, 1010, 30, MUTED),
    ('label', 1.6, '다섯 배 넘게 차이', 540, 1180, 56, INK)],
    texts=[(0.05, 'top', '1마일에 {10원도 안 되는}\n값으로 해외 갈 거야?')], sfx=[(0.1, 'ding'), (1.6, 'ding')])

s1 = dict(D, dur=3.6, items=[
    ('label', 0.1, '현금 표 · 2027.3.9 인천 ↔ 간사이 왕복', 540, 700, 34, MUTED),
    ('stack', 0.2, 750, [('운임', 165000, NAVY), ('세금·유류할증료', 212300, RED)], 390000, 150),
    ('label', 0.8, '마일 표', 540, 990, 34, MUTED),
    ('stack', 0.9, 1040, [('마일이 대신 냄', 165000, (150, 160, 185)), ('세금·유류할증료', 212300, RED)], 390000, 150),
    ('label', 1.7, '마일은 운임만 대신 내 준다', 540, 1300, 48, INK),
    ('label', 2.2, '1마일 = 운임 ÷ 쓴 마일', 540, 1430, 52, NAVY)],
    texts=[(0.05, 'top', '마일리지 항공권도\n{세금·유류할증료는 현금}')], sfx=[(1.7, 'ding')])

s2 = dict(D, dur=3.6, items=[
    ('label', 0.1, '내 영수증 네 쌍 · 같은 날 같은 편', 540, 600, 32, MUTED),
    ('hbar', 0.3, '삿포로 2024', 23.3, 25, 760, NAVY, '23.3원'),
    ('hbar', 0.5, '라스베이거스', 20.0, 25, 900, NAVY, '20.0원'),
    ('hbar', 0.7, '타이베이', 10.3, 25, 1040, NAVY, '10.3원'),
    ('hbar', 0.9, '간사이 2026', 9.6, 25, 1180, RED, '9.6원'),
    ('vline', 1.3, 10, 25, 690, 1230, '10원', RED)],
    texts=[(0.05, 'top', '내 영수증으로 재 보니\n1마일 {9.6 ~ 23.3원}')], sfx=[(1.3, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('label', 0.1, '2027년 날짜 20개 · 2026.10.6 조회', 540, 600, 32, MUTED),
    ('range', 0.3, '라스베이거스', 14.5, 20.7, 25, 760, NAVY),
    ('range', 0.5, '삿포로', 7.0, 18.7, 25, 900, NAVY),
    ('range', 0.7, '타이베이', 10.0, 12.2, 25, 1040, NAVY),
    ('range', 0.9, '간사이', 4.4, 7.3, 25, 1180, RED, PINK),
    ('vline', 1.3, 10, 25, 690, 1230, '10원', RED),
    ('label', 1.9, '10원 아래 7번 — 전부 간사이·삿포로', 540, 1390, 42, RED)],
    texts=[(0.05, 'top', '2027년 20번 조회\n{10원 아래가 7번}')], sfx=[(1.9, 'ding')])

s4 = dict(D, dur=3.8, items=[
    ('label', 0.1, '2027.3.9 인천 ↔ 간사이 왕복', 540, 700, 36, MUTED),
    ('hbar', 0.3, '마일이 내 줌', 165000, 250000, 880, NAVY, '165,000원'),
    ('hbar', 0.8, '카드로 냄', 212300, 250000, 1040, RED, '212,300원'),
    ('label', 1.5, '마일이 내 주는 돈 < 내가 내는 돈', 540, 1240, 46, RED)],
    texts=[(0.05, 'top', '30,000마일 쓰고도\n{카드로 더 낸다}')], sfx=[(1.5, 'ding')])

s5 = dict(D, dur=3.4, items=[
    ('label', 0.1, '같은 30,000마일', 540, 640, 46, INK),
    ('box', 0.3, 90, 720, 520, 1060, SKY), ('label', 0.35, '삿포로 2027.1.31', 305, 790, 36, NAVY),
    ('count', 0.4, 0, 560000, '{:,.0f}원', 305, 915, 64, NAVY),
    ('box', 0.8, 560, 720, 990, 1060, PINK), ('label', 0.85, '간사이 2027.3.9', 775, 790, 36, RED),
    ('count', 0.9, 0, 165000, '{:,.0f}원', 775, 915, 64, RED),
    ('label', 1.6, '대신 내 준 운임이 3배 넘게 차이', 540, 1180, 46, INK)],
    texts=[(0.05, 'top', '같은 3만 마일,\n{표 값은 3배 넘게}')], sfx=[(1.6, 'ding')])

s6 = dict(D, dur=3.6, items=[
    ('label', 0.2, '마일 공제표보다', 540, 760, 50, MUTED),
    ('label', 0.5, '그 날짜 현금 운임부터', 540, 870, 66, NAVY),
    ('box', 1.4, 90, 1040, 990, 1300, PINK),
    ('label', 1.5, '그럼 일본 노선 18개는?', 540, 1130, 54, RED),
    ('label', 1.9, '다음 편에서 계속 →', 540, 1225, 40, INK)],
    texts=[(0.05, 'top', '마일 쓰기 전에\n{이것부터}')], sfx=[(1.5, 'ding')])

SCENES = [s0, s1, s2, s3, s4, s5, s6]

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
        build(SCENES, BASE, 'A', 'mile_value_clip.mp4')
