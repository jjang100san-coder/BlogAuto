# 거창 감악산 축제 정보편 클립 (발행 9/30, logNo 224427624947) — 정보형 · 축제 10/11 종료 전 마지막 주말용
# 실행: python clipGI.py stills / python clipGI.py → out\gamak_info_clip.mp4
# 숫자는 정보편 발행본 그대로. 「다녀와 보니」 장면만 후기 발행본(224431411229)의 실제 기록 — 정보편에서 「가서 확인하겠다」고 한 답
# 사진은 10/4 직접 찍은 것(후기 꾸러미 폴더) — 사람 얼굴 없는 컷만
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(BASE, '..', '..', '261004_감악산 축제', 'gamak_review_pack')
D = dict(type='data', render=render, bg=LIGHT)
PURPLE = (110, 70, 160)
LAV = (238, 230, 248)

s0 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(PH, '20261004_142936.jpg'), 190, 560, 890, 1060),
    ('label', 0.8, '제6회 감악산 꽃별여행 · 거창 별바람언덕', 540, 1120, 34, MUTED),
    ('label', 1.2, '10월 11일(일)까지', 540, 1205, 64, PURPLE)],
    texts=[(0.05, 'top', '이번 주말이\n{마지막이야}')], sfx=[(0.1, 'ding'), (1.2, 'ding')])

s1 = dict(D, dur=3.6, items=[
    ('label', 0.1, '감악산 꽃별여행 방문객', 540, 640, 38, MUTED),
    ('hbar', 0.3, '2020년', 14.3, 70, 760, (180, 170, 200), '14만 3천'),
    ('hbar', 0.5, '2022년', 35.3, 70, 880, (160, 140, 195), '35만 3천'),
    ('hbar', 0.7, '2024년', 46.2, 70, 1000, (140, 110, 185), '46만 2천'),
    ('hbar', 0.9, '2025년', 56.2, 70, 1120, PURPLE, '56만 2천'),
    ('label', 1.6, '그래서 올해부터 차량 예약제', 540, 1250, 40, RED)],
    texts=[(0.05, 'top', '5년 만에\n{4배 가까이}')], sfx=[(0.95, 'ding')])

s2 = dict(D, dur=3.8, items=[
    ('label', 0.1, '차량 사전예약은 8월 19일에 끝났다', 540, 650, 38, RED),
    ('box', 0.4, 90, 720, 990, 1120, LAV),
    ('label', 0.5, '예약 없으면 셔틀이 유일한 길', 540, 790, 44, PURPLE),
    ('label', 0.8, '임시주차장 남상면 승강기단지길 94 · 주차 무료', 540, 880, 34, INK),
    ('label', 1.0, '셔틀 왕복 3,000원 (거창군민 무료)', 540, 960, 40, INK),
    ('label', 1.2, '현장 매표소 · 산길 약 11km', 540, 1040, 32, MUTED)],
    texts=[(0.05, 'top', '차로는 못 올라가\n{셔틀 타야 해}')], sfx=[(0.55, 'ding')])

ROWS = [('상행 막차', '평일 16:30 · 휴일 16:55', PURPLE), ('행사장 하산 유도', '18:00', INK), ('하행 막차(현장 배너)', '휴일 19:00', RED)]
s3_items = [('label', 0.1, '마감 시간 (공식 안내 + 다녀와서 본 배너)', 540, 640, 32, MUTED)]
for i, (a, b, c) in enumerate(ROWS):
    y = 760 + i * 130; t = 0.3 + i * 0.3
    s3_items += [('box', t, 70, y - 52, 1010, y + 52, (244, 240, 250)), ('label', t, a, 110, y, 40, INK, 'l'), ('label', t, b, 970, y, 44, c, 'r')]
s3_items.append(('label', 1.6, '기사의 16:30은 평일 기준이야', 540, 1180, 38, RED))
s3 = dict(D, dur=4.0, items=s3_items, texts=[(0.05, 'top', '휴일 올라가는 막차\n{16시 55분}')], sfx=[(0.6, 'ding')])

s4 = dict(D, dur=4.0, items=[
    ('image', 0.1, os.path.join(PH, 'map_waitline_crop.jpg'), 240, 560, 840, 960),
    ('label', 0.6, '10/4 일요일 11:45 도착 → 셔틀 줄 83분', 540, 1020, 40, INK),
    ('label', 0.9, '내려올 땐 10분도 안 기다렸어', 540, 1100, 40, INK),
    ('label', 1.4, '휴일엔 11시 전에 도착', 540, 1200, 60, RED)],
    texts=[(0.05, 'top', '다녀와 보니\n{줄이 핵심}')], sfx=[(1.4, 'ding')])

s5 = dict(D, dur=3.8, items=[
    ('image', 0.1, os.path.join(PH, 'shuttle_banner_crop.jpg'), 300, 560, 780, 980),
    ('label', 0.6, '아스타국화는 10/4 기준 절정', 540, 1040, 38, PURPLE),
    ('box', 1.2, 90, 1100, 990, 1300, LAV),
    ('label', 1.3, '이번 주말 감악산 갈 거야?', 540, 1170, 48, PURPLE),
    ('label', 1.7, '시간표는 블로그에', 540, 1250, 36, INK)],
    texts=[(0.05, 'top', '셔틀 시간만\n{알고 가}')], sfx=[(0.6, 'ding')])

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
        build(SCENES, BASE, 'GI', 'gamak_info_clip.mp4')
