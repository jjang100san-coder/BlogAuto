# 민음사빵 단종 · 텍스트힙 클립 (발행 10/8 12:20, logNo 224435092927) — 정보형 · 오늘 지나면 안 팔리는 시의성 주제
# 실행: python clipB.py stills / python clipB.py → out\minumsa_bread_clip.mp4
# 숫자는 발행 본문 표 그대로. 사진: 첫·끝 장면은 본인 사진(책갈피+『평원』), 가운데 빵 그림은 AI 생성(화면에 표시)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
PHOTO = os.path.join(ROOT, 'base data', '본인사진_책갈피_평원_원본.jpg')
AI_BREAD = os.path.join(ROOT, 'images', 'texthip_01_thumb.png')
D = dict(type='data', render=render, bg=LIGHT)
GREEN = (46, 125, 80)

s0 = dict(D, dur=3.6, items=[
    ('image', 0.1, PHOTO, 240, 560, 840, 1080),
    ('label', 0.9, '160만 개 팔렸는데', 540, 1150, 52, NAVY),
    ('label', 1.4, '20대 독서량은 14년 새 절반', 540, 1240, 52, RED)],
    texts=[(0.05, 'top', '민음사빵\n{단종됐다}')], sfx=[(0.1, 'ding'), (1.4, 'ding')])

s1 = dict(D, dur=3.8, items=[
    ('label', 0.1, 'GS25 민음사빵 누적 판매 · 8월 21일 출시', 540, 640, 34, MUTED),
    ('hbar', 0.3, '8월 31일', 35, 200, 760, (150, 160, 185), '35만 개'),
    ('hbar', 0.6, '9월 14일', 100, 200, 890, NAVY, '100만 개'),
    ('hbar', 0.9, '9월 말', 160, 200, 1020, NAVY, '160만 개'),
    ('label', 1.6, '10월 7일 발주가 마지막', 540, 1160, 50, RED)],
    texts=[(0.05, 'top', '빵 4종이\n{빵 매출 1~4위}')], sfx=[(0.95, 'ding'), (1.6, 'ding')])

s2 = dict(D, dur=4.0, items=[
    ('image', 0.1, AI_BREAD, 90, 560, 990, 900),
    ('label', 0.2, 'AI 생성 이미지', 960, 920, 24, MUTED, 'r'),
    ('label', 0.8, '산 이유를 주변 2030 여덟 명에게 물었더니', 540, 990, 34, INK),
    ('label', 1.2, '여덟 명 모두 「책갈피」', 540, 1070, 56, RED),
    ('label', 1.8, '『오만과 편견』 책갈피 중고 최고 29,000원 > 책 정가 13,000원', 540, 1160, 28, MUTED)],
    texts=[(0.05, 'top', '빵보다\n{책갈피}')], sfx=[(1.2, 'ding')])

s3 = dict(D, dur=3.6, items=[
    ('label', 0.1, '9월 초 GS25 구매 고객 비중', 540, 640, 36, MUTED),
    ('hbar', 0.3, '20대 여성', 26, 35, 760, RED, '26%'),
    ('hbar', 0.5, '30대 여성', 25, 35, 880, RED, '25%'),
    ('hbar', 0.7, '40대 여성', 13, 35, 1000, (200, 150, 155), '13%'),
    ('hbar', 0.9, '20대 남성', 10, 35, 1120, (150, 160, 185), '10%')],
    texts=[(0.05, 'top', '산 사람 절반이\n{2030 여성 51%}')], sfx=[(0.55, 'ding')])

s4 = dict(D, dur=3.8, items=[
    ('label', 0.1, '20대 1인당 1년 독서량 (국가데이터처)', 540, 640, 34, MUTED),
    ('hbar', 0.3, '2011년', 18.8, 25, 770, NAVY, '18.8권'),
    ('hbar', 0.7, '2025년', 9.4, 25, 900, RED, '9.4권'),
    ('label', 1.4, '1권이라도 읽은 비율은 75.3% · 20대만 올랐다', 540, 1040, 34, INK),
    ('label', 1.7, '읽는 사람은 지켜졌는데 권수는 반', 540, 1120, 42, RED)],
    texts=[(0.05, 'top', '텍스트힙인데\n{독서량은 절반}')], sfx=[(0.75, 'ding')])

s5 = dict(D, dur=3.8, items=[
    ('label', 0.1, '2025년 출판사 매출 증감', 540, 640, 36, MUTED),
    ('dbar', 0.3, '문학동네', -20.4, 30, 770, GREEN, RED, '-20.4%'),
    ('dbar', 0.55, '창비', -18.6, 30, 890, GREEN, RED, '-18.6%'),
    ('dbar', 0.8, '민음사', 23.8, 30, 1010, GREEN, RED, '+23.8%'),
    ('label', 1.5, '빵 전부터 팬이 있었다 · 민음사TV 57만', 540, 1140, 36, INK)],
    texts=[(0.05, 'top', '한강 특수 지나고\n{민음사만 올랐다}')], sfx=[(0.85, 'ding')])

s6 = dict(D, dur=4.2, items=[
    ('image', 0.1, PHOTO, 300, 560, 780, 1000),
    ('label', 0.6, '나는 올해 26권 · 다 읽고 중고로', 540, 1050, 36, INK),
    ('label', 1.0, '내 책갈피는 지금 『평원』에', 540, 1120, 40, GREEN),
    ('box', 1.6, 90, 1180, 990, 1360, PINK),
    ('label', 1.7, '네 책갈피는 어느 책에 꽂혀 있어?', 540, 1245, 44, RED),
    ('label', 2.1, '댓글로 알려줘', 540, 1315, 36, INK)],
    texts=[(0.05, 'top', '빵은 끝났고\n{책갈피는 남았다}')], sfx=[(1.0, 'ding')])

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
        build(SCENES, BASE, 'B', 'minumsa_bread_clip.mp4')
