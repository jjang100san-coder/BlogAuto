# 「수원삼성 화성 3-2 후기 | 르본이 왼쪽을 연 3-0, 63분 교체 뒤엔 또 흔들렸어」 클립 (발행 10/19 06:00, logNo 224445997601 — 축구)
# 실행: python make_html.py → python clipSR.py → out\suwon_hwaseong_review.mp4
# 커버·첫 장면은 발행본 카드(01_thumb, 축구는 카드 커버 유지). 장면 사이 장 카드(make_html.py), 전술은 움직이는 전술판
# 전술판 점 위치는 개념도 03_board.png 에서 픽셀로 옮김: 왼쪽 칸 x 62~500 · 오른쪽 칸 x 582~1020, y 272~990 → 0~1 (위 = 상대 골문)
# 색은 개념도와 같게 수원삼성 파랑 · 화성FC 주황. 호칭: 이정효·차두리 감독, ○○○ 선수
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build
import tactics as T

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), 'suwon-hwaseong-review', 'images', n)
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('수원삼성 3-2 화성FC', '3-0은 왜 3-2가 됐을까')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 기록 K리그 공식')
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 발행글 기준')
T.PY0, T.PY1 = 500, 1340
SW = (46, 98, 217); HS = (232, 120, 48)
T.BG = (0, 0, 0); T.PITCH = (28, 64, 46); T.LINE = (92, 130, 104)
T.TEAM.update({'sw': SW, 'hs': HS})


def L(px, py):
    return (round((px - 62) / 438, 3), round((py - 272) / 718, 3))


def R(px, py):
    return (round((px - 582) / 438, 3), round((py - 272) / 718, 3))


# ① 21분 2-0 — 이상민 선수가 올라와 르본 선수에게, 막던 수비가 넘어지고, 르본 선수가 안으로 → 왼발 크로스 → 화성 수비 머리 → 골
P1 = {'lsm': ('sw',) + L(148, 630) + ('이상민',), 'lb': ('sw',) + L(95, 487) + ('르본',), 's3': ('sw',) + L(265, 428) + (None,), 's4': ('sw',) + L(315, 406) + (None,),
      'fall': ('hs',) + L(157, 450) + (None,), 'h2': ('hs',) + L(236, 356) + (None,), 'og': ('hs',) + L(293, 342) + (None,), 'h4': ('hs',) + L(350, 356) + (None,),
      'h5': ('hs',) + L(456, 428) + (None,), 'h6': ('hs',) + L(280, 558) + (None,), 'h7': ('hs',) + L(359, 558) + (None,)}
GOAL = L(280, 300)
left21 = dict(type='pitch', dur=7.0, view=(0.0, 0.62), players=P1,
              moves=[('lsm', 0.3, 1.3, L(175, 543)), ('fall', 1.9, 2.5, L(200, 480)), ('lb', 2.4, 3.8, [L(120, 440), L(160, 365)])],
              ball=[('at', 0, 'lsm'), ('pass', 1.4, 2.1, 'lsm', 'lb'), ('pass', 4.0, 4.8, 'lb', 'og'), ('pass', 5.0, 5.5, 'og', GOAL)],
              zones=[(2.4, 9, L(143, 400), 0.10, 0.07, (240, 210, 90), None)],
              tags=[],
              texts=[(0.05, 'top', '21분 2-0\n{르본 선수가 연 왼쪽}')], sfx=[(1.4, 'kick'), (4.0, 'kick'), (5.5, 'ding')])

# ② 59분 3-1 — 화성 왼쪽 코너킥이 먼 쪽 페트로프 선수에게 → 머리로 가까운 쪽 → 보이노비치 선수 헤더
P2 = {'cr': ('hs',) + R(600, 318) + (None,), 'pt': ('hs',) + R(874, 342) + (None,), 'bv': ('hs',) + R(760, 420) + ('보이노비치',),
      'h4': ('hs',) + R(826, 424) + (None,), 'h5': ('hs',) + R(905, 450) + (None,),
      's1': ('sw',) + R(813, 302) + (None,), 's2': ('sw',) + R(940, 378) + (None,), 's3': ('sw',) + R(835, 392) + (None,),
      's4': ('sw',) + R(879, 435) + (None,), 's5': ('sw',) + R(650, 450) + (None,), 's6': ('sw',) + R(808, 486) + (None,)}
GOAL2 = R(760, 300)
corner59 = dict(type='pitch', dur=6.5, view=(0.0, 0.62), players=P2,
                moves=[('bv', 2.0, 3.2, R(729, 310))],
                ball=[('at', 0, 'cr'), ('pass', 0.6, 2.0, 'cr', 'pt'), ('pass', 2.4, 3.3, 'pt', 'bv'), ('pass', 3.5, 4.0, 'bv', GOAL2)],
                zones=[(2.2, 9, R(738, 312), 0.09, 0.06, (240, 210, 90), None)],
                tags=[],
                texts=[(0.05, 'top', '59분 3-1\n{화성의 약속된 코너킥}')], sfx=[(0.6, 'kick'), (2.4, 'kick'), (4.0, 'ding')])

NUM_OK = ('3-1',)   # 59분 당시 스코어 — 발행본 전술 도해 03_board 에 「59분 3-1」
COACHES = ['이정효', '차두리']
PLAYERS = ['르본', '이상민', '보이노비치', '페트로프', '강현묵', '김민우']

SCENES = prep([
    dict(D, media=P('01_thumb.png'), **dict(DG, label='배경 AI 생성 이미지 · 실제 경기 아님'),
         call=[(3.0, '3-0은 왜 3-2가 됐을까', YEL)], sfx=[(3.0, 'ding')],
         cap='비가 쏟아진 날, 수원삼성이 화성FC를 이겼어. 하지만 3-0이던 경기가, 왜 3-2로 끝났을까?'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '전반 3-0', YEL)],
         cap='먼저 전반. 2-0을 만든 건, 왼쪽의 르본 선수였어.'),
    dict(left21, cap='이상민 선수가 공을 내주는 순간, 막던 수비가 넘어졌어. 르본 선수는 비어 있는 자리로 치고 들어가, 왼발로 올렸고.'),
    dict(D, media=P('02_lebon.png'), **DG, call=[(0.6, '벌어진 간격을 노렸다', YEL)],
         cap='공은 화성 수비 머리에 맞고 들어갔어. 첫 골 뒤 벌어진 간격을, 가장 빨리 알아챈 선수였지.'),
    dict(D, media=P('04_fouls.png'), **DG, call=[(0.6, '파울 13개', YEL)],
         cap='화성은 파울 13개. 공을 빼앗기면 일단 끊고 내려가는 반칙이, 계속 이어졌어.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '후반 2실점', YEL)],
         cap='그리고 경기 후반, 또 그 시간이 왔어.'),
    dict(corner59, cap='59분, 화성의 약속된 코너킥. 먼 쪽에서 머리로 떨군 공을, 보이노비치 선수가 넣었어.'),
    dict(D, media=P('05_again.png'), **DG, call=[(0.6, '두 경기 연속', YEL)],
         cap='63분에 세 명을 한꺼번에 바꾼 뒤, 73분에 또 실점. 안산전과 같은 꼴이야.'),
    dict(D, media=A('quote'), **AN, call=[(0.4, '이정효 감독의 진단', YEL)],
         cap='이정효 감독은, 체력이 아니라 편한 선택이 문제라고 했어.'),
    # 요약 장(프리뷰 채점)
    dict(D, media=P('06_check.png'), **DG, call=[(0.6, '프리뷰 채점', YEL)],
         cap='프리뷰에 적은 다섯 개 중, 맞은 건 하나. 먼저 넣었지만, 그 시간을 또 넘기지 못했어.'),
    dict(D, media=A('table'), **AN, call=[(0.4, '6연승 · 1위', YEL)],
         cap='그래도 6연승, 2위와 5점 차야. 다음 성남전에선, 63분 뒤가 달라질까?'),
], BASE, 'SR')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'SR', 'suwon_hwaseong_review.mp4')
