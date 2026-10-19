# 모레노호 4연전 클립 2편 — 「아시안컵 숙제는 내려앉는 팀」 (1편 끝 여운을 이어받음)
# 실행: python ep2.py stills  /  python ep2.py  → out\moreno_ep2.mp4
# 근거: draft_moreno_four_games.md (🔑·🧱·🧩·🛣️·🔄·📋 절), 도해 images\04_low_block.png 의 좌표
# 단정 금지: 4-3-3 은 「정답이 아니라 시험해 볼 그릇」, 모레노 원래 축구는 「해설 채널들 말로는」
import os, sys
from tactics import *
from tactics import pos_at
from ep1 import carry

BASE = os.path.dirname(os.path.abspath(__file__))

# 0 이기는 방식의 사슬: ① 상대가 나온다 → ② 뺏는다 → ③ 찌른다
s0 = dict(type='pitch', view=(0.0, 0.78), dur=4.6, players={
    'gk': ('gk', .50, .03, None),
    'cbl': ('opp', .35, .26, None), 'cbr': ('opp', .65, .26, None), 'fbl': ('opp', .10, .32, None), 'fbr': ('opp', .90, .32, None),
    'dm': ('opp', .50, .38, None), 'ml': ('opp', .30, .49, None), 'mr': ('opp', .70, .49, None),
    'lw': ('opp', .24, .67, None), 'rw': ('opp', .76, .67, None), 'st': ('opp', .50, .71, None),
    'son': ('kor', .42, .46, '손흥민'), 'oh': ('kor', .60, .43, '오세훈'),
    'c1': ('kor', .38, .58, None), 'c2': ('kor', .62, .58, None), 'w1': ('kor', .12, .60, None), 'w2': ('kor', .88, .60, None),
    'd1': ('kor', .12, .80, None), 'd2': ('kor', .37, .82, None), 'd3': ('kor', .63, .82, None), 'd4': ('kor', .88, .80, None),
    'kgk': ('kor', .50, .95, None)},
    moves=[('cbl', 0.2, 1.2, (.36, .34)), ('dm', 0.6, 1.4, (.48, .42)),
           ('son', 1.3, 1.8, (.46, .43)), ('oh', 1.9, 2.9, (.66, .14))],
    ball=[('at', 0, 'cbl'), ('pass', 1.3, 1.7, 'cbl', 'son'), ('pass', 2.3, 3.0, 'son', 'oh')],
    arrows=[(1.8, 9, (.60, .43), (.66, .15), KOR, True)],
    tags=[(0.5, 99, (.20, .27), '① 나온다'), (1.75, 99, (.28, .44), '② 뺏는다'), (2.6, 99, (.84, .20), '③ 찌른다')],
    texts=[(0, 'small', '모레노호 4연전 결산 ② · 1편에서 이어서'), (0.05, 'top', '우즈벡전에서 찾은 방식\n{나오면 뺏고 찌른다}')],
    sfx=[(0.1, 'ding')])

# 1 첫 고리가 빠지면: 처음부터 내려앉은 블록(04_low_block 좌표) — 한국은 4-4-2 로 공을 쥔다
LB_OPP = {'fbl': (.10, .11), 'cbl': (.30, .11), 'dm': (.50, .11), 'cbr': (.70, .11), 'fbr': (.90, .11),
          'lw': (.20, .29), 'ml': (.40, .29), 'mr': (.60, .29), 'rw': (.80, .29), 'st': (.50, .44)}
KOR_442 = {'son': (.40, .19), 'oh': (.60, .19), 'w1': (.12, .36), 'w2': (.88, .36), 'c1': (.38, .53), 'c2': (.62, .53),
           'd1': (.10, .56), 'd4': (.90, .56), 'd2': (.35, .72), 'd3': (.65, .72), 'kgk': (.50, .95)}
s1 = dict(type='pitch', view=(0.0, 0.78), dur=3.6, players=carry(s0, {'son': None, 'oh': None}),
    moves=[(k, 0.2, 1.5, v) for k, v in LB_OPP.items()] + [(k, 0.4, 1.7, v) for k, v in KOR_442.items()],
    ball=[('at', 0, 'oh'), ('pass', 0.3, 1.2, 'oh', 'd2')],
    tags=[(1.9, 99, (.50, .40), '뺏을 공도, 찌를 공간도 없다')],
    texts=[(0, 'top', '그런데 상대가\n{처음부터 내려앉으면?}')],
    sfx=[(1.95, 'ding')])

# 2 아시안컵 E조
s2 = dict(type='card', dur=3.4, items=[
    (0.35, 'row', '1/10', '레바논·예멘 승자', '', ACCENT, '조별리그 1차전', 600),
    (0.55, 'row', '1/15', '베트남', '', ACCENT, '조별리그 2차전', 770),
    (0.75, 'row', '1/20', '아랍에미리트', '', ACCENT, '조별리그 3차전', 940),
    (1.10, 'big', '세 팀 모두 피파 랭킹이 한참 아래', 1160, 44, MUTED)],
    texts=[(0, 'small', '2027 아시안컵 · 1월 7일~2월 5일 · 사우디아라비아'), (0.05, 'top', '한국은 E조\n{내려앉을} 가능성이 크다')],
    sfx=[(0.1, 'ding')])


def shift(ids, dx, t0, t1, base):
    return [(k, t0, t1, (base[k][0] + dx, base[k][1])) for k in ids]


# 3 공을 쥐어도: 블록은 옆으로 따라오고, 라인 사이엔 투톱뿐 · 가운데 둘은 블록 앞
s3 = dict(type='pitch', view=(0.0, 0.78), dur=3.8, players=carry(s1),
    moves=shift(LB_OPP.keys(), .04, 0.5, 1.4, LB_OPP) + shift(LB_OPP.keys(), .07, 1.6, 2.5, LB_OPP),
    ball=[('at', 0, 'd2'), ('pass', 0.3, 0.8, 'd2', 'd3'), ('pass', 1.1, 1.6, 'd3', 'c2'), ('pass', 1.9, 2.4, 'c2', 'd4')],
    zones=[(0.6, 99, (.50, .20), .40, .045, AMBER, None)],
    tags=[(0.7, 99, (.50, .245), '라인 사이엔 투톱뿐'), (1.4, 99, (.50, .61), '가운데 둘은 블록 앞')],
    texts=[(0, 'top', '숙제는 압박이 아니라\n{공을 쥔 뒤의 설계}')],
    sfx=[(0.1, 'ding')])

# 4 4-4-2 → 4-3-3 (04_low_block 오른쪽 판): 8번 둘이 라인 사이로 · 측면 두 겹 · 6번이 열쇠
s4 = dict(type='pitch', view=(0.0, 0.78), dur=4.4, players=carry(s3, {'c2': '6번'}),
    moves=[(k, 0.3, 1.2, v) for k, v in LB_OPP.items()] +
          [('son', 0.5, 1.7, (.50, .17)), ('oh', 0.5, 1.7, (.63, .21)), ('c1', 0.5, 1.7, (.37, .21)), ('c2', 0.5, 1.7, (.50, .53)),
           ('w1', 0.5, 1.7, (.07, .16)), ('w2', 0.5, 1.7, (.93, .16)), ('d1', 0.5, 1.7, (.12, .40)), ('d4', 0.5, 1.7, (.88, .40)),
           ('d2', 0.5, 1.7, (.36, .70)), ('d3', 0.5, 1.7, (.64, .70)),
           ('d1', 2.2, 3.0, (.12, .26)), ('d4', 2.2, 3.0, (.88, .26))],
    ball=[('at', 0, 'd4'), ('pass', 1.8, 2.3, 'd4', 'c2'), ('pass', 2.8, 3.3, 'c2', 'oh')],
    arrows=[(2.1, 9, (.12, .40), (.12, .27), KOR, True), (2.1, 9, (.88, .40), (.88, .27), KOR, True)],
    zones=[(1.8, 99, (.50, .20), .22, .04, GREEN, None)],
    tags=[(1.9, 99, (.50, .245), '8번 둘이 라인 사이로'), (2.6, 99, (.24, .33), '측면 두 겹')],
    texts=[(0, 'top', '모레노의 원래 축구\n{4-3-3} 이라면'), (3.0, 'bot', '정답이 아니라 시험해 볼 그릇')],
    sfx=[(1.85, 'ding')])

# 5 블록을 여는 세 갈래 길
s5 = dict(type='card', dur=3.4, items=[
    (0.30, 'row', '①', '세트피스', '', ACCENT, '손흥민 직접 프리킥 59호골', 600),
    (0.55, 'row', '②', '측면 크로스', '', ACCENT, '오세훈 헤더 · 송민규 도움', 770),
    (0.80, 'row', '③', '중앙 콤비네이션', '', ACCENT, '앞으로 보내는 6번 + 라인 사이', 940),
    (1.20, 'big', '길마다 맞는 선수가 다르다', 1160, 48, CREAM)],
    texts=[(0.05, 'top', '블록을 여는 길은\n{세 갈래}')],
    sfx=[(0.1, 'ding')])

# 6 11월에 볼 4가지 — 저장 유도
s6 = dict(type='card', dur=3.6, items=[
    (0.30, 'row', '1', '3선에서 앞으로 보내는 사람', '', ACCENT, '황인범 선발 90분?', 560),
    (0.50, 'row', '2', '이강인의 자리', '', ACCENT, '바깥 · 안쪽 · 가운데', 730),
    (0.70, 'row', '3', '어느 길을 시험하나', '', ACCENT, '세트피스 · 크로스 · 콤비네이션', 900),
    (0.90, 'row', '4', '아시안게임 출신', '', ACCENT, '몇 명, 어느 자리로', 1070)],
    texts=[(0, 'small', '저장해 두고 11월에 꺼내 보기'), (0.05, 'top', '11월 A매치에서 볼\n{네 가지}')],
    sfx=[(0.1, 'ding')])

# 7 질문으로 끝 — 4-3-3 판 위에서
s7 = dict(type='pitch', view=(0.0, 0.78), dur=3.6, players=carry(s4),
    ball=[('at', 0, 'c2')], dim=(0.0, 120),
    zones=[(0.2, 99, 'c2', .10, .035, AMBER, None)],
    texts=[(0.05, 'top', '3선에서 공을 앞으로 보낼 사람\n{누구여야 할까?}'), (0.8, 'bot', '댓글로 알려줘')],
    sfx=[(0.1, 'ding')])

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        d = os.path.join(BASE, '_build', 'ep2_stills'); os.makedirs(d, exist_ok=True)
        from PIL import Image
        tiles = []
        for i, sc in enumerate(SCENES):
            for t in (0.3, sc['dur'] * 0.5, sc['dur'] - 0.05):
                f = os.path.join(d, f's{i}_{t:.1f}.jpg'); still(sc, t, f)
                tiles.append(Image.open(f).resize((216, 384)))
        sheet = Image.new('RGB', (216 * 8, 384 * 3))
        for j, im in enumerate(tiles):
            sheet.paste(im, ((j // 3) * 216, (j % 3) * 384))
        sheet.save(os.path.join(d, 'sheet.jpg'), quality=90)
        print('stills', d)
    else:
        build(SCENES, BASE, 'ep2', 'moreno_ep2.mp4')
