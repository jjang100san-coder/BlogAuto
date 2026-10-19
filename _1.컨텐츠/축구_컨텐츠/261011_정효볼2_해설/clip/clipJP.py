# 정효볼 원리 클립 (발행 10/13 19:00, logNo 224438502830 — 정효볼 2편)
# 실행: python clipJP.py stills / python clipJP.py → out\jhb_principles.mp4
# 커버·첫 장면은 발행본 카드(01_thumb, 축구는 카드 커버 유지).
# 원리 도해 4장은 움직이는 전술판으로(10/14 사용자 「이미지 이동 말고 말이 움직이도록」): 개념도의 점을 extract → dots2.py 로 뽑아(dots.json)
#   boards.morph 가 왼쪽 칸(①) 배치에서 오른쪽 칸(②) 배치로 바뀐 점만 움직인다. 역압박(⑥)은 한 칸이라 boards.close_in 으로 좁혀 들어오게
# 호칭: 이정효 감독. 「뺏기면」은 「공을 빼앗기면」(발음 장부, 10/11 사용자)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build
import tactics as T
import boards

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), 'jhb2', 'images', n)
shorts.HEAD = ('이정효 감독 정효볼 원리', '공통점은 빈자리')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 발행글 기준')
T.PY1 = 1330   # 경기장 아래 끝을 말 자막(1364~) 위로
ORANGE = (208, 119, 63); BLUE = (46, 156, 192)
T.BG = (0, 0, 0); T.PITCH = (30, 52, 58); T.LINE = (92, 120, 128); T.TEAM.update({'kor': ORANGE, 'opp': BLUE})


def near(pl, xy, team='kor'):
    return min((k for k, v in pl.items() if v[0] == team), key=lambda k: (pl[k][1] - xy[0]) ** 2 + (pl[k][2] - xy[1]) ** 2)


def board(f, title, tags, zones=(), ball=None, kind='morph', view=(0.08, 0.88), passes=()):
    if kind == 'morph':
        pl, mv = boards.morph(f)
    else:
        pl, mv = boards.close_in(f, ball)
    sc = dict(type='pitch', dur=6.0, view=view, players=pl, moves=mv, tags=list(tags), zones=list(zones),
              texts=[(0.05, 'top', title)], sfx=[(3.2, 'ding')])
    if passes:   # [(t0, t1, 출발 선수 자리, 받는 선수 자리)] — 자리는 개념도 왼쪽 칸 좌표, 가장 가까운 수원 선수에게
        b = [('at', 0, near(pl, passes[0][2]))]
        for t0, t1, a, c in passes:
            b.append(('pass', t0, t1, near(pl, a), near(pl, c)))
        sc['ball'] = b; sc['sfx'] = sc['sfx'] + [(t0, 'kick') for t0, _, _, _ in passes]
    if kind != 'morph':
        oid = min((k for k, v in pl.items() if v[0] == 'opp'), key=lambda k: (pl[k][1] - ball[0]) ** 2 + (pl[k][2] - ball[1]) ** 2)
        sc['ball'] = [('at', 0, oid)]
    return sc

NUM_OK = ()
COACHES = ['이정효']
PLAYERS = []

SCENES = prep([
    dict(D, media=P('01_thumb.png'), z0=1.0, z1=1.0, whole=True, fit='contain', label='배경 AI 생성 이미지 · 특정 인물 아님',
         call=[(3.0, '공간을 소유하는 축구', YEL)], sfx=[(3.0, 'ding')],
         cap='이정효 감독에게 정효볼이 뭐냐고 물으면, 답은 짧아. 공간을 소유하는 축구.'),
    dict(D, media=P('02_overview.png'), **DG, call=[(0.6, '빈자리를 먼저 차지한다', YEL)],
         cap='수원 경기 다섯 장면을 전술판에 그려 보니, 공통점은 하나였어. 빈자리를 만들고, 먼저 차지하는 거야.'),
    dict(board('03_p1_lure.png', '끌어낸다\n{나온 자리 뒤가 길}', [(3.3, 9, (0.84, 0.40), '나온 자리 뒤')],
               passes=[(0.3, 1.1, (0.38, 0.821), (0.62, 0.821)), (3.4, 4.2, (0.62, 0.821), (0.841, 0.621))],
               zones=[(3.3, 9, (0.84, 0.62), 0.07, 0.05, (120, 200, 140), None)]),
         cap='첫째는 끌어내기. 7월 부산전, 상대 윙포워드가 압박하러 나오자, 그 등 뒤가 바로 길이 됐어.'),
    dict(board('05_p3_roles.png', '역할로 채운다\n{빈자리는 다른 사람이}', [(3.3, 9, (0.32, 0.30), '빈자리는 다른 사람이')]),
         cap='둘째는 역할로 채우기. 한 명이 내려가면, 그 빈자리는 다른 선수가 메워. 포지션이 왜 필요하냐는 게, 감독의 오래된 생각이래.'),
    dict(board('06_p4_switch.png', '쏠리게 하고 반대로\n{먼 쪽에서 끝낸다}', [(3.3, 9, (0.90, 0.13), '먼 쪽')],
               zones=[(3.3, 9, (0.90, 0.30), 0.07, 0.07, (232, 108, 100), None)],
               passes=[(0.3, 1.0, (0.401, 0.601), (0.079, 0.3)), (3.5, 4.5, (0.079, 0.3), (0.902, 0.22))]),
         cap='셋째는 쏠리게 하고 반대로. 농구에서 가져온 방식이야. 한쪽에 모아 놓고, 먼 쪽에서 끝내.'),
    dict(board('08_p6_press.png', '빼앗기면 바로 다시\n{가까운 선수가 좁혀 든다}', [(2.8, 9, (0.12, 0.10), '가까운 둘이 바로 붙고')],
               ball=(0.119, 0.25), kind='close', view=(0.05, 0.62)),
         cap='그리고 공을 빼앗기면 바로 다시. 볼이 경기장 안에 있을 땐, 숨 쉴 생각도 하지 말라고 할 정도야.'),
    dict(D, media=P('09_split.png'), **DG, call=[(0.6, '단점 다섯, 본인도 인정', YEL)],
         cap='물론 약점도 있어. 상대가 안 나오면 끌어낼 수 없고, 라인을 올리면 수비 뒤가 비어. 재밌는 건, 그 다섯 가지를 이정효 감독도 다 인정했다는 거야.'),
    dict(D, media=P('02_overview.png'), **DG, call=[(0.6, '다음 상대 화성', YEL)],
         cap='다음 상대는 화성이라, 수비 뒤가 비는 장면을 다시 볼 만해. 너는 여섯 원리 중에, 어떤 게 제일 인상적이야?'),
], BASE, 'JP')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'JP', 'jhb_principles.mp4')
