# 수원삼성 4-1 안산 후기 클립 (발행 10/11 21:33, logNo 224438297308)
# 실행: python clipSA.py stills / python clipSA.py → out\suwon_ansan_clip.mp4
# 형식: 정효볼 3편 클립(카드·위쪽 제목) + 10/11 규칙(말 자막 cap · 장면 끝 1초 쉼 = shorts.prep)
# 개념도는 발행글 images\04·05 를 칸별로 잘라(g_left·g_right·c_left·c_right) 하나씩 보여 준다 — 전술판을 새로 그리지 않음(배치 오류 방지)
# 숫자·이름은 발행본 그대로. 호칭 「○○○ 선수 / 감독」. 축구는 커버·첫 장면 카드 유지(분야 예외)
# 말 자막 자리(y 1360~1500)는 비워 둔다 — 그림·카드는 y 1340 위에서 끝낸다
import os, sys
KIT = r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit'
sys.path.insert(0, KIT)
import tactics as T
import shorts
from tactics import build, still, audit
from dataviz import render

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(BASE), 'suwon-ansan', 'images')
im = lambda n: os.path.join(IMG, n)
here = lambda n: os.path.join(BASE, n)

NAVY = (14, 26, 54); PANEL = (28, 42, 74); PANEL2 = (44, 60, 98)
MUT = (160, 176, 206); SKY = (128, 196, 245); CREAM = (244, 240, 232)
GOOD = (120, 200, 140); MID = (236, 190, 100); BAD = (232, 108, 100)
T.BG = NAVY; T.ACCENT = SKY; T.MUTED = MUT
D = dict(type='data', render=render, bg=NAVY, dur=3.0)
BOX = (60, 520, 1020, 1340)   # 그림 상자 — 말 자막(1360~) 위에서 끝


def pic(path, t=0.05, box=BOX):
    return ('image', t, path) + box


def row(t, y, title, sub, pill=None, pcol=GOOD, h=128, tsz=40):
    it = [('box', t, 70, y, 1010, y + h, PANEL), ('box', t, 70, y, 82, y + h, pcol)]
    it.append(('label', t, title, 110, y + (38 if sub else h // 2), tsz, CREAM, 'l'))
    if sub:
        it.append(('label', t, sub, 110, y + 90, 28, MUT, 'l'))
    if pill:
        w = 30 * len(pill) + 40
        it += [('box', t, 980 - w, y + h // 2 - 30, 980, y + h // 2 + 30, pcol),
               ('label', t, pill, 980 - w / 2, y + h // 2, 30, NAVY)]
    return it


SCHED = [('10/18', '화성', '홈', '5위'), ('10/25', '성남', '원정', None), ('10/31', '대구', '원정', None),
         ('11/8', '용인', '홈', None), ('11/21', '경남', '홈', None), ('11/29', '전남', '원정', None)]
sched = [('label', 0.1, '수원 승점 56 · 2위 수원FC·서울 이랜드 51', 540, 600, 32, CREAM)]
for i, (dt, opp, home, badge) in enumerate(SCHED):
    y = 660 + i * 92; t = 0.3 + i * 0.1
    sched += [('box', t, 120, y, 960, y + 80, PANEL), ('label', t, dt, 160, y + 40, 32, SKY, 'l'),
              ('label', t, opp, 340, y + 40, 36, CREAM, 'l'), ('label', t, home, 500, y + 40, 28, MUT, 'l')]
    if badge:
        sched += [('box', t, 800, y + 18, 930, y + 62, MID), ('label', t, badge, 865, y + 40, 26, NAVY)]


# ── 움직이는 전술판(10/11 사용자: 「도해 그림 그대로라 영상으로서 액티브한 면이 줄어든다」) ──
# 좌표는 발행글 개념도 images\04·05 의 점을 픽셀로 뽑아 옮김(경기장 테두리 기준 0~1, 전술판 세 원칙 ①)
#   왼쪽 칸 x=(px-62)/426, 오른쪽 칸 x=(px-42)/426, y=(py-82)/696  (g_left/g_right/c_left/c_right.png 기준)
T.PY1 = 1330                      # 경기장 아래 끝을 말 자막(1364~) 위로
ORANGE = (208, 119, 63); BLUE = (46, 156, 192)
T.PITCH = (30, 52, 58); T.LINE = (92, 120, 128)
T.TEAM.update({'kor': ORANGE, 'opp': BLUE})
nx = lambda px, left=True: round((px - (62 if left else 42)) / 426, 3)
ny = lambda py: round((py - 82) / 696, 3)
# 첫 골 — 수원 위로 공격(위쪽이 안산 골문)
G = {'f1': ('kor', nx(94), ny(304), None), 'lu': ('kor', nx(223), ny(304), '루이스'), 'f3': ('kor', nx(335), ny(304), None),
     'f4': ('kor', nx(455), ny(304), None), 'm1': ('kor', nx(103), ny(500), None), 'km': ('kor', nx(343), ny(500), '김민우'),
     'm3': ('kor', nx(447), ny(500), None), 'm2': ('kor', nx(232), ny(514), None), 'b1': ('kor', nx(214), ny(626), None),
     'b2': ('kor', nx(335), ny(626), None)}
for i, px in enumerate((111, 189, 275, 361, 438)):
    G['d%d' % i] = ('opp', nx(px), ny(234), None)
for i, px in enumerate((137, 214, 283)):
    G['a%d' % i] = ('opp', nx(px), ny(388), None)
G['h'] = ('opp', nx(386), ny(388), None); G['a9'] = ('opp', nx(283), ny(472), None)
GAP = (0.40, 0.15)                # 개념도 ② 「수비가 놓친 틈」(안산 d1·d2 사이 뒤 공간)
VG = (0.06, 0.84)
GA = dict(G)                      # 시작: 앞 네 명·안산 수비가 좁게 → 넓어진다(개념도 ① 화살표)
moves_a = []
for k in ('f1', 'lu', 'f3', 'f4'):
    team, x, y, lab = G[k]; GA[k] = (team, round(0.5 + (x - 0.5) * 0.72, 3), y, lab); moves_a.append((k, 0.3, 1.6, (x, y)))
for k in ('d0', 'd1', 'd2', 'd3', 'd4'):
    team, x, y, lab = G[k]; GA[k] = (team, round(0.5 + (x - 0.5) * 0.8, 3), y, lab); moves_a.append((k, 0.9, 2.2, (x, y)))
hx, hy = G['h'][1], G['h'][2]
moves_a.append(('h', 2.6, 4.8, [(hx - 0.05, hy + 0.06), (hx + 0.04, hy - 0.05), (hx, hy)]))   # 「앞? 뒤?」 망설임
sg1 = dict(type='pitch', dur=6.0, view=VG, players=GA, moves=moves_a, ball=[('at', 0, 'km')],
           arrows=[(0.3, 1.7, (0.30, 0.27), (0.12, 0.27), ORANGE, False), (0.3, 1.7, (0.70, 0.27), (0.88, 0.27), ORANGE, False)],
           tags=[(0.4, 9, (0.5, 0.12), '폭을 넓게'), (2.6, 9, (0.91, 0.53), '망설이다')],
           texts=[(0.05, 'top', '앞 네 명이 넓게\n{간격이 벌어진다}')], sfx=[(1.6, 'ding')],
           cap='공을 가졌을 때, 앞 네 명이 넓게 섰어. 그러자 안산 수비 사이가 자꾸 벌어졌지.')
G2 = dict(G); G2['lu'] = ('kor', G['lu'][1], G['lu'][2], None)   # 뛰는 동안 이름표가 수비·공을 가리지 않게 — 이름은 태그로
sg2 = dict(type='pitch', dur=7.4, view=VG, players=G2,
           moves=[('lu', 1.4, 3.4, [(0.39, 0.25), GAP])],
           ball=[('at', 0, 'km'), ('pass', 2.3, 3.4, 'km', 'lu')],
           arrows=[(0.6, 9, 'km', GAP, ORANGE, False), (1.2, 9, 'lu', GAP, ORANGE, True)],
           zones=[(0.5, 9, (0.40, 0.18), 0.07, 0.05, BAD, None)],
           tags=[(0.5, 3.3, (0.40, 0.09), '수비가 놓친 틈'), (0.5, 9, (0.66, 0.71), '아무 방해 없이'),
                 (0.2, 1.4, (0.38, 0.37), '루이스'), (3.4, 9, (0.40, 0.09), '루이스')],
           texts=[(0.05, 'top', '수비가 놓친 틈\n{1분 만에 골}')], sfx=[(2.3, 'kick'), (3.4, 'ding')],
           cap='안산 미드필더가 망설이는 사이, 김민우 선수가 그 틈으로 길게 넣었어. 루이스 선수가 뛰어들어 가슴으로 받았지.')
# 실점 — 안산 아래로 공격(아래쪽이 수원 골문)
VC = (0.40, 1.02)
CL = {'s1': ('kor', nx(189), ny(451), None), 's2': ('kor', nx(137), ny(465), None), 's3': ('kor', nx(275), ny(542), None),
      's4': ('kor', nx(429), ny(640), None), 's5': ('kor', nx(232), ny(668), None), 's6': ('kor', nx(318), ny(668), None),
      'aa': ('opp', nx(163), ny(514), None), 'cr': ('opp', nx(94), ny(612), None)}
C1 = dict(CL); C1['s1'] = ('kor', 0.40, 0.47, None); C1['s2'] = ('kor', 0.09, 0.47, None)   # 두 명이 한 명에게 붙기 전
FAR = (nx(387, False), ny(755))   # 먼 쪽 골라인 앞(개념도 ② 강동현 자리)
sc1 = dict(type='pitch', dur=7.9, view=VC, players=C1,
           moves=[('s1', 0.6, 2.2, (CL['s1'][1], CL['s1'][2])), ('s2', 0.6, 2.2, (CL['s2'][1], CL['s2'][2])),
                  ('cr', 2.6, 4.0, (0.075, 0.72))],
           ball=[('at', 0, 'aa'), ('pass', 2.4, 3.2, 'aa', 'cr'), ('pass', 5.2, 6.6, 'cr', FAR)],
           arrows=[(2.2, 9, 'cr', FAR, BLUE, True)],
           tags=[(1.6, 9, (0.30, 0.45), '한 명에게 겹쳐 붙는'), (4.2, 9, (0.14, 0.92), '크로스 길이 열렸어')],
           texts=[(0.05, 'top', '4-0에서 세 명 교체\n{3분 뒤}')], sfx=[(5.2, 'kick')],
           cap='그런데 4-0이던 후반 20분, 세 명을 한꺼번에 바꿨어. 3분 뒤, 바로 그 왼쪽에서 크로스가 올라왔어.')
CR = {'s1': ('kor', nx(186, False), ny(647), None), 's3': ('kor', nx(276, False), ny(682), None),
      'sn': ('kor', nx(341, False), ny(667), None), 'a1': ('opp', nx(306, False), ny(682), None),
      'cr': ('opp', nx(65, False), ny(640), None),
      'ry': ('opp', nx(229, False), ny(734), None), 'kd': ('opp', nx(387, False), ny(755), '강동현')}
sc2 = dict(type='pitch', dur=7.2, view=VC, players=CR,
           moves=[('s1', 0.4, 2.0, (nx(210, False), ny(700))), ('ry', 0.6, 2.2, (nx(240, False), ny(745)))],
           ball=[('at', 0, 'kd'), ('pass', 1.2, 2.4, 'kd', 'ry'), ('pass', 2.8, 3.4, 'ry', (0.5, 1.0))],
           arrows=[(1.0, 9, 'kd', 'ry', BLUE, False)],
           zones=[(0.3, 9, FAR, 0.09, 0.04, BAD, None)],
           tags=[(0.4, 9, (0.80, 0.90), '먼 쪽'), (0.2, 9, (0.24, 0.92), '류승완 선수')],
           texts=[(0.05, 'top', '감독이 아쉬워한\n{20분}')], sfx=[(1.2, 'kick'), (3.0, 'kick'), (3.4, 'ding')],
           cap='먼 쪽에서 머리로 떨군 공을, 류승완 선수가 밀어 넣었어. 이정효 감독이 아쉽다고 한 게 바로 이 20분이야.')

SCENES = shorts.prep([
    dict(D, items=[pic(im('01_thumb.png'))], texts=[(0.05, 'top', '4-1인데\n{왜 아쉬웠을까}')], sfx=[(0.1, 'ding')],
         cap='수원삼성이 안산을 4-1로 이겼어. 루이스 선수 해트트릭. 그런데 이정효 감독은 웃지 않았어.'),
    dict(D, items=[pic(im('06_scorecard.png'))], texts=[(0.05, 'top', '어제 적은 네 가지\n{채점}')],
         cap='어제 적은 네 가지부터 채점할게. 둘은 맞혔고, 나머지는 반반이야.'),
    dict(D, items=[pic(im('02_namecard_luis.png'))], texts=[(0.05, 'top', '오늘의 선수\n{루이스 선수}')], sfx=[(0.3, 'ding')],
         cap='루이스 선수는 전반 1분과 26분, 후반 11분에 골을 넣었어. 수원에선 2020년 타가트 선수 이후, 6년 만의 해트트릭이야.'),
    sg1,
    sg2,
    dict(D, items=[('label', 0.1, '수원 · 안산', 540, 600, 34, MUT)]
         + row(0.3, 660, '점유율', None, '60% · 40%', GOOD)
         + row(0.5, 810, '슈팅(유효)', None, '17(10) · 8(4)', GOOD)
         + row(0.7, 960, '파울', None, '4 · 11', MID)
         + [('label', 1.2, '뺏겨도 그 자리에서 다시 찾아왔다', 540, 1170, 40, SKY)],
         texts=[(0.05, 'top', '공을 빼앗기면\n{바로 다시 누른다}')], sfx=[(0.35, 'ding')],
         cap='공을 빼앗기면 그 자리에서 바로 다시 눌렀어. 점유율 60%, 슈팅 17개에 유효슈팅 10개.'),
    sc1,
    sc2,
    dict(D, items=[pic(im('03_discharged.png'))], texts=[(0.05, 'top', '같은 주말\n{상무 전역생 셋}')],
         cap='같은 주말, 상무에서 전역한 셋이 모두 그라운드에 섰어. 김주찬 선수는 전역 닷새 만에 20분을 뛰었지.'),
    dict(D, items=sched, texts=[(0.05, 'top', '2위와\n{5점 차}')], sfx=[(0.35, 'ding')],
         cap='이제 2위와 5점 차, 남은 건 6경기야. 다음 상대는 5위 화성이야.'),
    dict(D, items=[('image', 0.05, im('01_thumb.png'), 240, 520, 840, 1100),
                   ('box', 0.6, 100, 1150, 980, 1300, PANEL2),
                   ('label', 0.7, '너는 화성전, 고쳐 올 거라고 봐?', 540, 1205, 40, SKY),
                   ('label', 0.9, '댓글로 알려줘', 540, 1262, 30, CREAM)],
         texts=[(0.05, 'top', '교체 뒤 20분\n{화성전에서는?}')],
         cap='정효팬인 나도, 그 20분이 제일 마음에 걸렸어. 너는 화성전에서 고쳐 올 거라고 봐?'),
], BASE, 'SA')

PLAYERS = ['루이스', '김민우', '류승완', '김주찬', '타가트', '두비츠카스', '이건희', '박철우', '강동현']
COACHES = ['이정효']
NUM_OK = ('2020',)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'SA', 'suwon_ansan_clip.mp4')
