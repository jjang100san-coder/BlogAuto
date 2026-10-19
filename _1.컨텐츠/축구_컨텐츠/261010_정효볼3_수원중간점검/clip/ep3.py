# 정효볼 3편 클립 — 이정효 수원삼성 중간 점검 (발행 10/10 03:40, logNo 224436763887)
# 실행: python ep3.py stills (정지 화면 + 검수) / python ep3.py → out\junghyo3_suwon_clip.mp4
# 숫자·이름은 발행본 그대로. 전술판 위치는 글의 개념도 images\05_press.png 에서 옮김(클립 지침 4-4-1 선수 표 아래)
# 호칭: 「○○○ 감독」「○○○ 선수」(이름표는 이름만). 축구는 커버·첫 장면 카드 유지(분야 예외)
import os, sys
KIT = r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit'
sys.path.insert(0, KIT)
import tactics as T
from tactics import build, still, audit
from dataviz import render

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(BASE), 'suwon-midseason', 'images')

# ── 3편 카드 색(cards.py set_palette · 개념도에서 뽑은 색) ──
NAVY = (14, 26, 54); PANEL = (28, 42, 74); PANEL2 = (44, 60, 98)
MUT = (160, 176, 206); SKY = (128, 196, 245); CREAM = (244, 240, 232)
ORANGE = (208, 119, 63); BLUE = (46, 156, 192)
GOOD = (120, 200, 140); MID = (236, 190, 100); BAD = (232, 108, 100)
T.BG = NAVY; T.ACCENT = SKY; T.MUTED = MUT
T.TEMPO = 1.13   # 12장면이라 1분 30초 안에 넣으려고 조금 빠르게(기본 1.08)
T.PITCH = (30, 52, 58); T.LINE = (92, 120, 128)
T.TEAM.update({'kor': ORANGE, 'opp': BLUE})
D = dict(type='data', render=render, bg=NAVY)


def row(t, y, title, sub, pill=None, pcol=GOOD, h=128, tsz=40):
    """패널 한 줄: 왼쪽 제목·작은 설명, 오른쪽 알약."""
    it = [('box', t, 70, y, 1010, y + h, PANEL), ('box', t, 70, y, 82, y + h, pcol)]
    it.append(('label', t, title, 110, y + (38 if sub else h // 2), tsz, CREAM, 'l'))
    if sub:
        it.append(('label', t, sub, 110, y + 90, 28, MUT, 'l'))
    if pill:
        w = 34 * len(pill) + 40
        it += [('box', t, 980 - w, y + h // 2 - 30, 980, y + h // 2 + 30, pcol),
               ('label', t, pill, 980 - w / 2, y + h // 2, 32, NAVY)]
    return it


# s0 — 카드 첫 장면(축구 분야 예외: 카드 커버 유지)
s0 = dict(D, dur=3.4, items=[('image', 0.05, os.path.join(IMG, '01_thumb.png'), 90, 560, 990, 1460)],
          texts=[(0.05, 'top', '1위인데 득점은\n{6번째}')], sfx=[(0.1, 'ding')])

s1 = dict(D, dur=3.6, items=[('label', 0.1, '2026 K리그2 · 수원삼성 25경기 · 17팀 중 순위', 540, 600, 30, MUT)]
          + row(0.3, 660, '실점', None, '20 · 리그 최소', GOOD)
          + row(0.5, 810, '무실점 경기', None, '13 · 리그 최다', GOOD)
          + row(0.7, 960, '득점', None, '39 · 6번째', MID)
          + row(0.9, 1110, '슈팅', None, '309 · 4번째', MID)
          + [('label', 1.4, '1위를 만든 건 공격이 아니라 실점 20', 540, 1320, 40, SKY)],
          texts=[(0.05, 'top', '공격이 아니라\n{실점 20}')], sfx=[(0.35, 'ding')])

s2 = dict(D, dur=3.6, items=[
    ('label', 0.1, '16승 가운데', 540, 680, 44, MUT),
    ('count', 0.4, 0, 11, '{:.0f}번', 540, 840, 170, SKY),
    ('label', 0.9, '한 골 차 승리', 540, 990, 48, CREAM),
    ('box', 1.4, 190, 1090, 890, 1210, PANEL2),
    ('label', 1.5, '그중 1-0만 7번', 540, 1150, 52, ORANGE)],
    texts=[(0.05, 'top', '{꾸역꾸역}\n이기는 1위')], sfx=[(0.45, 'ding'), (1.5, 'ding')])

s3 = dict(D, dur=4.4, items=[('label', 0.1, '부임 직후 예측 → 25경기 뒤', 540, 590, 32, MUT)]
          + row(0.3, 640, '점유 축구로 바뀐다', '25경기 중 21경기 점유 우위', '맞음', GOOD)
          + row(0.5, 785, '이건희·강성진·정호연 선수', '오른쪽 이건희·강성진 선수, 중원 정호연 선수', '맞음', GOOD)
          + row(0.7, 930, '초반엔 안 굴러갈 수 있다', '개막 5연승', '빗나감', BAD)
          + row(0.9, 1075, '실점이 적은 축구가 된다', '리그 최소 실점 20', '맞음', GOOD)
          + row(1.1, 1220, '(본인) 내려서서 비기려 할 것', '4패 중 둘이 그 그림', '맞음', GOOD),
          texts=[(0.05, 'top', '부임 직후 예측\n{다섯 중 넷}')], sfx=[(0.35, 'ding'), (0.75, 'ding')])

s4 = dict(D, dur=4.0, items=[
    ('label', 0.1, '이정효 감독이 꼽은 가장 큰 고민', 540, 610, 32, MUT),
    ('label', 0.3, '「대놓고 내려서서 비기려 할 것」', 540, 690, 44, SKY)]
    + row(0.8, 790, '4월 김포전', '점유율 67% · 슈팅 3', '0-1', BAD)
    + row(1.1, 950, '7월 안산전', '슈팅 34 · 결승골은 역습', '1-2', BAD)
    + [('label', 1.6, '진 경기는 감독이 걱정한 바로 그 방식', 540, 1170, 38, CREAM)],
    texts=[(0.05, 'top', '가장 정확한 예측은\n{감독 본인}')], sfx=[(0.85, 'ding'), (1.15, 'ding')])

s5 = dict(D, dur=4.4, items=[('label', 0.1, '이정효 감독 기준 「상대 박스를 두드리는 게 주도」', 540, 590, 30, MUT)]
          + row(0.3, 640, '4월 · 박스를 못 두드렸다', '김포전 점유 67%, 슈팅 3', None, BAD, h=120, tsz=38)
          + row(0.5, 775, '5월 · 「U자로 돌리기만」 비판', '점유는 높은데 슈팅이 안 나옴', None, BAD, h=120, tsz=38)
          + row(0.7, 910, '7월 · 두드렸는데 못 넣었다', '안산전 슈팅 34, 1-2 패', None, MID, h=120, tsz=38)
          + row(0.9, 1045, '8월 · 라인 사이에 남는 선수', '구조가 바뀌기 시작', None, GOOD, h=120, tsz=38)
          + row(1.1, 1180, '9월 · 공을 덜 쥐고도 이겼다', '서울E전 점유 40%로 1-0', None, GOOD, h=120, tsz=38)
          + [('label', 1.6, '지금 숙제는 점유가 아니라 마무리', 540, 1370, 40, SKY)],
          texts=[(0.05, 'top', '숙제는 점유가 아니라\n{마무리}')], sfx=[(1.6, 'ding')])

# ── 전술판: 개념도 05_press.png 에서 옮긴 좌표(왼쪽 판 x=(px-76)/429, 오른쪽 판 x=(px-576)/429, y=(py-231)/699) ──
# 이름        팀    x      y      출처(개념도 px)
# 공격 왼쪽   수원  .357  .259   (229,412)
# 공격 오른쪽 수원  .633  .259   (350,412)
# 맨투맨 미드 수원  .599  .619→.439 (333,648)→(333,538) 주황 점선 화살표
# 미드 셋     수원  .117/.357/.879  .619  (126/229/453,664)
# 수비 넷     수원  .138/.378/.618/.858  .820  (135/238/341/444,804)
# 상대 핵심   상대  .599  .359   (333,482)
# 상대 왼쪽   상대  .217  .399   (169,510) — 실선 = 공, 빈 공간으로
# 상대 오른쪽 상대  .839  .399   (436,510) — 점선 = 사람, 빈 공간으로 (.662,.585)
# 빈 공간     구역  .611  .609   rx .19 ry .08 (257~419, 601~713)
# 고종현 전진 수원  .618  .820→.629 (841,671) · 대응 판에서 상대 오른쪽은 (.723,.528) 에서 멈춤
P0 = {'f1': ('kor', .357, .259, None), 'f2': ('kor', .633, .259, None),
      'mk': ('kor', .599, .619, None),
      'm1': ('kor', .117, .619, None), 'm2': ('kor', .357, .619, None), 'm3': ('kor', .879, .619, None),
      'd1': ('kor', .138, .820, None), 'd2': ('kor', .378, .820, None), 'd3': ('kor', .618, .820, None),
      'd4': ('kor', .858, .820, None),
      'oh': ('opp', .599, .359, None), 'ol': ('opp', .217, .399, None), 'or': ('opp', .839, .399, None)}
VIEW = (0.0, 1.0)   # 개념도처럼 경기장 전체 — 위쪽 자막(~y470)과 경기장(y560~)이 안 겹친다

s6 = dict(type='pitch', dur=5.6, view=VIEW, players=dict(P0),
          moves=[('mk', 0.4, 1.4, (.599, .439)),
                 ('or', 2.4, 3.7, [(.79, .47), (.662, .585)])],
          ball=[('at', 0, 'ol'), ('pass', 3.0, 3.8, 'ol', 'or')],
          arrows=[(0.3, 1.5, (.599, .600), (.599, .470), ORANGE, True),
                  (2.0, 9, 'or', (.662, .585), BLUE, True)],
          zones=[(1.6, 9, (.611, .609), .19, .08, BAD, '빈 공간')],
          tags=[(1.5, 9, (.45, .37), '맨투맨'), (0.6, 9, (.60, .315), '상대 핵심')],
          texts=[(0.05, 'top', '상대가 찌른 곳\n{맨투맨 뒤}')], sfx=[(1.6, 'ding'), (3.0, 'kick')])

P1 = dict(P0); P1['mk'] = ('kor', .599, .439, None); P1['d3'] = ('kor', .618, .820, '고종현')
s7 = dict(type='pitch', dur=5.0, view=VIEW, players=P1,
          moves=[('d3', 0.4, 1.6, (.618, .629)),
                 ('or', 1.2, 2.4, [(.79, .46), (.723, .528)])],
          ball=[('at', 0, 'ol')],
          arrows=[(0.3, 1.7, (.618, .790), (.618, .660), ORANGE, True),
                  (1.0, 9, 'or', (.723, .528), BLUE, True)],
          zones=[(1.6, 9, (.611, .609), .19, .08, GOOD, None)], tags=[(1.8, 9, (.36, .72), '숫자를 메움')],
          texts=[(0.05, 'top', '이정효 감독이 고친 곳\n{센터백 전진}')], sfx=[(1.6, 'ding')])

s8 = dict(D, dur=4.0, items=[('label', 0.1, '약점이 보이면 경기 중에 고쳤다', 540, 600, 32, MUT)]
          + row(0.3, 650, '마크할 상대를 바꿔 다시 맞춤', '선제골 내주고 역전', '부산 4-1', GOOD)
          + row(0.6, 800, '센터백 고종현 선수가 앞으로', '빈자리 숫자를 메움', '김포·서울E', GOOD)
          + row(0.9, 950, '막히면 5-4-1로 내려서서 잠금', '점유 40%에도', '서울E 1-0', GOOD)
          + [('label', 1.5, '「쉽게 무너지지 않을 것 같은 팀」', 540, 1170, 42, SKY),
             ('label', 1.8, '— 이정효 감독, 9월', 540, 1240, 30, MUT)],
          texts=[(0.05, 'top', '약점은 남았지만\n{대응하는 팀}')], sfx=[(1.5, 'ding')])

s9 = dict(D, dur=4.4, items=[('label', 0.1, '2026 여름 · 경기와 공격수 합류 순서', 540, 590, 30, MUT)]
          + row(0.3, 640, '7/11 · 안산전 1-2 패', '시즌 네 번째 패배', None, BAD, h=120, tsz=38)
          + row(0.5, 775, '7/19 · 무패 시작', '영입생 없이', None, GOOD, h=120, tsz=38)
          + row(0.7, 910, '7/25 · 부산전 4-1', '영입생 없이', None, GOOD, h=120, tsz=38)
          + row(1.0, 1045, '8/1 · 두비츠카스 선수 첫 출전', '리투아니아 대표 공격수', None, SKY, h=120, tsz=38)
          + row(1.2, 1180, '8/22 · 루이스 선수 첫 출전', '김포에서 이적 · 뛴 세 경기 1-0, 2-0, 1-0', None, SKY, h=120, tsz=38)
          + [('label', 1.7, '반등의 출발은 전술, 영입은 흐름을 이었다', 540, 1370, 38, SKY)],
          texts=[(0.05, 'top', '반등은 영입보다\n{먼저 시작됐다}')], sfx=[(0.55, 'ding'), (1.05, 'ding')])

SCHED = [('10/11', '안산', '홈', '내일' if False else None), ('10/18', '화성', '홈', '상위권'), ('10/25', '성남', '원정', None),
         ('10/31', '대구', '원정', '상위권'), ('11/8', '용인', '홈', None), ('11/21', '경남', '홈', None), ('11/29', '전남', '원정', None)]
s10_items = [('box', 0.1, 120, 580, 960, 690, PANEL2),
             ('label', 0.15, '1·2위 바로 승격 · 3~6위 플레이오프', 540, 620, 34, CREAM),
             ('label', 0.2, '승강 플레이오프까지 최대 네 팀이 올라간다', 540, 664, 24, MUT)]
for i, (dt, opp, home, badge) in enumerate(SCHED):
    y = 720 + i * 92; t = 0.4 + i * 0.12
    s10_items += [('box', t, 120, y, 960, y + 80, PANEL), ('label', t, dt, 160, y + 40, 32, SKY, 'l'),
                  ('label', t, opp, 340, y + 40, 36, CREAM, 'l'), ('label', t, home, 500, y + 40, 28, MUT, 'l')]
    if badge:
        s10_items += [('box', t, 770, y + 18, 930, y + 62, MID), ('label', t, badge, 850, y + 40, 26, NAVY)]
s10_items.append(('label', 1.5, '목표는 1위보다 2위 안', 540, 1400, 42, SKY))
s10 = dict(D, dur=4.4, items=s10_items, texts=[(0.05, 'top', '남은 7경기\n{2위와 승점 2점 차}')], sfx=[(1.5, 'ding')])

s11 = dict(D, dur=4.6, items=[('label', 0.1, '10월 11일 안산전 · 한 달 만의 경기', 540, 600, 32, MUT)]
           + row(0.3, 650, '루이스·두비츠카스 선수 같이 골?', '처음 한 달을 같이 훈련한 공격진', None, SKY, h=110, tsz=36)
           + row(0.5, 775, '슈팅이 골로 바뀌나', '7월 같은 상대에게 슈팅 34개, 1골', None, MID, h=110, tsz=36)
           + row(0.7, 900, '안산의 역습 한 방을 막나', '7월 결승골도 역습', None, BAD, h=110, tsz=36)
           + row(0.9, 1025, '김주찬 선수가 명단에 드나', '10월 6일 전역 · 수원 37번', None, GOOD, h=110, tsz=36)
           + [('box', 1.5, 100, 1190, 980, 1340, PANEL2),
              ('label', 1.6, '너는 수원이 몇 위로 끝날 것 같아?', 540, 1245, 40, SKY),
              ('label', 1.9, '댓글로 알려줘', 540, 1300, 30, CREAM)],
           texts=[(0.05, 'top', '안산전에서\n{이 네 가지를 봐}')], sfx=[(1.6, 'ding')])

PLAYERS = ['고종현', '루이스', '두비츠카스', '김주찬', '이건희', '강성진', '정호연', '김민준', '김준홍']   # 호칭 검사(qa_clip)
COACHES = ['이정효']
NUM_OK = ('17',)   # 「17팀 중 순위」 — 발행본 카드 02_numbers 부제(다음 스포츠 순위), 본문엔 없음
SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        from PIL import Image
        d = os.path.join(BASE, '_build', 'stills'); os.makedirs(d, exist_ok=True)
        tiles = []
        for i, sc in enumerate(SCENES):
            ts = [sc['dur'] - 0.05] if sc['type'] != 'pitch' else [0.2, sc['dur'] * 0.45, sc['dur'] - 0.05]
            for j, t in enumerate(ts):
                f = os.path.join(d, f's{i:02d}_{j}.jpg'); still(sc, t, f); tiles.append(Image.open(f).resize((270, 480)))
        cols = 8
        sh = Image.new('RGB', (270 * cols, 480 * ((len(tiles) + cols - 1) // cols)))
        for j, im in enumerate(tiles):
            sh.paste(im, ((j % cols) * 270, (j // cols) * 480))
        sh.save(os.path.join(d, 'sheet.jpg'), quality=88); print('stills', d)
        post = os.path.join(BASE, 'pub_224436763887.txt')
        audit(SCENES, open(post, encoding='utf-8').read() if os.path.exists(post) else None)
    else:
        build(SCENES, BASE, 'J3', 'junghyo3_suwon_clip.mp4')
