# 수원삼성 화성FC 프리뷰 클립 (발행 10/15 15:10, logNo 224439601706 — 축구)
# 실행: python clipSH.py stills / python clipSH.py → out\suwon_hwaseong_preview.mp4
# 커버·첫 장면은 발행본 카드(01_thumb, 축구는 카드 커버 유지)
# 전술은 움직이는 전술판(10/14 사용자 「이미지 이동 말고 말이 움직이도록」) — 점 위치는 개념도 03_first_leg_board.png 에서 픽셀로 옮김
#   왼쪽 칸 x 75~505 · 오른쪽 칸 x 575~1005, y 230~930 → 0~1 (위 = 상대 골문). 화살표 시작점이 출발 자리, 점이 끝 자리
# 호칭: 이정효·차두리 감독, ○○○ 선수
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build
import tactics as T

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), 'images', n)
shorts.HEAD = ('수원삼성 vs 화성FC', '10월 18일, 누가 먼저 뚫나')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 발행글 기준')
T.PY0, T.PY1 = 500, 1340   # 위 큰 글(~470) 아래부터, 말 자막(1364~) 위까지
ORANGE = (208, 119, 63); BLUE = (46, 156, 192); GRAY = (132, 138, 160)
T.BG = (0, 0, 0); T.PITCH = (30, 52, 58); T.LINE = (92, 120, 128)
T.TEAM.update({'kor': ORANGE, 'opp': BLUE, 'ans': GRAY})


def L(px, py):   # 왼쪽 칸 픽셀 → 0~1
    return (round((px - 75) / 430, 3), round((py - 230) / 700, 3))


def R(px, py):   # 오른쪽 칸 픽셀 → 0~1
    return (round((px - 575) / 430, 3), round((py - 230) / 700, 3))


# ① 화성 1차전 동점골(68분) — 고종현 선수 전진 → 화성 오른쪽 둘이 안으로 → 빈 오른쪽
SW = {'gjh': L(340, 800), 'hs': L(481, 605), 'khm': L(278, 445), 's1': L(204, 398), 's2': L(100, 440),
      's3': L(143, 706), 's4': L(272, 720), 's5': L(238, 790)}
HW = {'h1': L(118, 292), 'h2': L(195, 286), 'h3': L(268, 282), 'h4': L(333, 282), 'h5': L(475, 315),
      'h6': L(143, 440), 'h7': L(238, 440), 'h8': L(315, 447), 'h9': L(463, 468), 'h10': L(290, 664)}
NAME = {}   # 이름표는 빽빽한 판에서 다른 점을 가려(audit 10건) 뺐다 — 이름은 말과 자막으로
P1 = {k: ('kor',) + v + (NAME.get(k),) for k, v in SW.items()}
P1.update({k: ('opp',) + v + (None,) for k, v in HW.items()})
GJH_UP = L(333, 524); H5_IN = L(393, 356); H9_IN = L(376, 545); HS_MID = L(470, 450); HS_END = L(449, 268); KHM_END = L(290, 348)
GAP = (L(468, 380), 0.08, 0.2)

carry = dict(type='pitch', dur=6.0, view=(0.0, 0.86), players=P1,
             moves=[('gjh', 0.4, 2.4, GJH_UP), ('h5', 1.4, 3.0, H5_IN), ('h9', 1.4, 3.0, H9_IN)],
             ball=[('at', 0, 'gjh')], zones=[(3.0, 9, GAP[0], GAP[1], GAP[2], (120, 200, 140), None)],
             tags=[(3.2, 9, (0.80, 0.75), '오른쪽 측면')],
             texts=[(0.05, 'top', '화성 1차전 동점골\n{몰고 올라가자 좁혀 들어왔다}')], sfx=[(3.0, 'ding')])
P2 = dict(P1); P2['gjh'] = ('kor',) + GJH_UP + (None,); P2['h5'] = ('opp',) + H5_IN + (None,); P2['h9'] = ('opp',) + H9_IN + (None,)
finish = dict(type='pitch', dur=6.0, view=(0.0, 0.86), players=P2,
              moves=[('hs', 0.3, 1.6, [L(478, 540), HS_MID]), ('hs', 1.7, 3.0, HS_END), ('khm', 2.6, 3.9, KHM_END)],
              ball=[('at', 0, 'gjh'), ('pass', 0.8, 1.6, 'gjh', 'hs'), ('pass', 3.4, 4.2, 'hs', 'khm')],
              zones=[(0, 9, GAP[0], GAP[1], GAP[2], (120, 200, 140), None)],
              tags=[],
              texts=[(0.05, 'top', '빈 오른쪽으로\n{컷백에 가까운 크로스}')], sfx=[(0.8, 'kick'), (3.4, 'kick'), (4.3, 'ding')])

# ② 안산전 첫 골(2분) — 앞 넷이 넓게 → 수비 사이 틈 → 루이스 선수가 뛰어듦, 김민우 선수 롱패스
F4 = {'f1': R(600, 454), 'lu': R(729, 454), 'f3': R(850, 454), 'f4': R(979, 454)}
BK = {'m1': R(618, 664), 'm2': R(747, 664), 'kmw': R(858, 664), 'm4': R(962, 664), 'c1': R(738, 790), 'c2': R(841, 790)}
AN = {'a1': R(618, 370), 'a2': R(695, 370), 'a3': R(790, 370), 'a4': R(884, 370), 'a5': R(962, 370),
      'b1': R(652, 531), 'b2': R(729, 531), 'b3': R(893, 531), 'b4': R(953, 531)}
squeeze = lambda xy, k: (round(0.5 + (xy[0] - 0.5) * k, 3), xy[1])
P3 = {k: ('kor',) + squeeze(v, 0.55) + (NAME.get(k),) for k, v in F4.items()}
P3.update({k: ('kor',) + v + (None,) for k, v in BK.items()})
P3.update({k: ('ans',) + squeeze(v, 0.7) + (None,) for k, v in AN.items() if k.startswith('a')})
P3.update({k: ('ans',) + v + (None,) for k, v in AN.items() if k.startswith('b')})
wide = [(k, 0.4, 1.8, v) for k, v in F4.items()] + [(k, 0.7, 2.1, v) for k, v in AN.items() if k.startswith('a')]
ansan = dict(type='pitch', dur=6.5, view=(0.05, 0.9), players=P3,
             moves=wide + [('lu', 2.4, 3.8, R(790, 340))],
             ball=[('at', 0, 'kmw'), ('pass', 2.6, 3.8, 'kmw', 'lu')],
             zones=[(2.0, 9, R(795, 350), 0.11, 0.07, (120, 200, 140), None)],
             tags=[],
             texts=[(0.05, 'top', '안산전 첫 골 2분\n{넓게 서자 사이가 벌어졌다}')], sfx=[(2.6, 'kick'), (3.9, 'ding')])

NUM_OK = ()
COACHES = ['이정효', '차두리']
PLAYERS = ['고종현', '헤이스', '강현묵', '루이스', '장민준', '일류첸코']

SCENES = prep([
    dict(D, media=P('01_thumb.png'), **dict(DG, label='배경 AI 생성 이미지 · 실제 경기 아님'),
         call=[(3.2, '누가 먼저 뚫나', YEL)], sfx=[(3.2, 'ding')],
         cap='같은 안산을, 수원삼성은 2분 만에 뚫었고, 화성FC는 66분까지 기다렸다 뚫었어.'),
    dict(D, media=P('02_two_wins.png'), **DG, call=[(0.6, '쥐는 수원 · 내주는 화성', YEL)],
         cap='점유는 수원 60%, 화성은 44%. 공을 쥐고 일찍 끝내는 쪽과, 내주고 기다렸다 덮치는 팀이야.'),
    dict(carry, cap='6월 1차전 동점골을 보자. 고종현 선수가 공을 몰고 올라가자, 화성 오른쪽 수비가 안으로 좁혀 들어왔어.'),
    dict(finish, cap='그 빈 오른쪽으로 헤이스 선수가 파고들었고, 강현묵 선수가 마무리했지.'),
    dict(ansan, cap='안산전 첫 골은, 앞 넷이 넓게 서면서 시작됐어. 수비 사이가 벌어지자, 루이스 선수가 그 틈으로 뛰었고.'),
    dict(D, media=P('04_timeline.png'), **DG, call=[(0.6, '65~75분이 겹친다', YEL)],
         cap='수원은 안산전에서, 교체 뒤 68분에 실점했어. 화성은 바로 그 시간대, 66분에 먼저 넣은 팀이고.'),
    dict(D, media=P('05_jang_minjun.png'), **DG, call=[(0.6, '장민준 선수 경고 8장째', YEL)],
         cap='화성 수비수 장민준 선수는, 이번 시즌 경고가 8장째야. 규정대로라면, 수원전엔 못 나와.'),
    dict(D, media=P('06_checkpoints.png'), **DG, call=[(0.6, '10월 18일에 볼 다섯 가지', YEL)],
         cap='먼저 뚫는 쪽은 어디고, 65분 이후는 누가 쥘까. 너는 이번 경기, 첫 골이 어느 팀일 것 같아?'),
], BASE, 'SH')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'SH', 'suwon_hwaseong_preview.mp4')
