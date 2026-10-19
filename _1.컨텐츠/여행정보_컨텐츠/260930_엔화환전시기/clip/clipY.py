# 엔화 환전 언제 해야 쌀까 클립 (발행 10/5, logNo 224426512614) — 정보형
# 실행: python clipY.py stills / python clipY.py → out\yen_clip.mp4
# 숫자는 발행 본문 표 그대로 · 그래프 두 장은 블로그에 쓴 이미지(yen_chart_time·month)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
D = dict(type='data', render=render, bg=LIGHT)

s0 = dict(D, dur=3.2, items=[
    ('label', 0.1, '하나은행 엔화 고시 3년 치', 540, 680, 44, MUTED),
    ('count', 0.3, 0, 66, '{:.0f}만 번', 540, 840, 130, NAVY),
    ('label', 1.2, '2023.10 ~ 2026.9 · 영업일 728일', 540, 990, 38, INK),
    ('label', 1.6, '다 뽑아 봤어', 540, 1120, 56, RED)],
    texts=[(0.05, 'top', '엔화 환전,\n{몇 시}에 해야 쌀까?')], sfx=[(0.1, 'ding'), (1.6, 'ding')])

s1 = dict(D, dur=3.8, items=[
    ('label', 0.1, '100엔당 차이 · 3년 평균', 540, 610, 34, MUTED),
    ('hbar', 0.3, '1년 중 등락', 125, 175, 740, NAVY, '94~125원'),
    ('hbar', 0.6, '은행 수수료', 16, 175, 880, NAVY, '16원'),
    ('hbar', 0.9, '하루 등락', 6, 175, 1020, NAVY, '5~6원'),
    ('hbar', 1.2, '몇 시에', 0.2, 175, 1160, RED, '0.2원'),
    ('label', 1.8, '시간은 0.2원, 수수료는 16원', 540, 1320, 48, RED)],
    texts=[(0.05, 'top', '{몇 시에}는 0.2원\n수수료는 16원')], sfx=[(1.8, 'ding')])

s2 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(ROOT, 'yen_chart_time.png'), 40, 620, 1040, 1250),
    ('label', 1.2, '09시 ~ 15시, 세 해 모두 ±0.5원 안', 540, 1330, 42, NAVY),
    ('label', 1.6, '아침이든 오후든 같았다', 540, 1420, 48, RED)],
    texts=[(0.05, 'top', '아침에 바꿔도\n{오후에 바꿔도}')], sfx=[(1.6, 'ding')])

s3 = dict(D, dur=3.6, items=[
    ('label', 0.1, '요일별 · 전 영업일 대비 세 해 평균', 540, 620, 34, MUTED),
    ('dbar', 0.3, '월', 0.72, 1.0, 740, RED, NAVY, '+0.72원'),
    ('dbar', 0.45, '화', -0.46, 1.0, 860, RED, NAVY, '-0.46원'),
    ('dbar', 0.6, '수', -0.36, 1.0, 980, RED, NAVY, '-0.36원'),
    ('dbar', 0.75, '목', -0.18, 1.0, 1100, RED, NAVY, '-0.18원'),
    ('dbar', 0.9, '금', 0.29, 1.0, 1220, RED, NAVY, '+0.29원'),
    ('label', 1.6, '1원도 안 되는 차이 — 우연과 구분 안 됨', 540, 1380, 40, INK)],
    texts=[(0.05, 'top', '월요일이 비싸다?\n{0.7원}')], sfx=[(1.6, 'ding')])

s4 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(ROOT, 'yen_chart_month.png'), 40, 620, 1040, 1250),
    ('label', 1.2, '가장 싼 달: 2024 6월 · 2025 1월 · 2026 9월', 540, 1330, 40, NAVY),
    ('label', 1.6, '몇 월에 바꾸면 싸다는 규칙 없음', 540, 1420, 46, RED)],
    texts=[(0.05, 'top', '가장 싼 달도\n{해마다 달랐다}')], sfx=[(1.6, 'ding')])

s5 = dict(D, dur=3.8, items=[
    ('label', 0.2, '언제 바꿀지보다', 540, 760, 50, MUTED),
    ('label', 0.5, '어디서 얼마나 우대받을지', 540, 870, 62, NAVY),
    ('box', 1.4, 90, 1030, 990, 1290, PINK),
    ('label', 1.5, '너는 환전 우대 몇 % 받아?', 540, 1120, 52, RED),
    ('label', 1.9, '댓글로 알려줘', 540, 1215, 40, INK)],
    texts=[(0.05, 'top', '그래서 볼 건\n{환전 우대율} 하나')], sfx=[(1.5, 'ding')])

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
        build(SCENES, BASE, 'Y', 'yen_clip.mp4')
