# 모레노호 4연전 클립 1편 — 「가운데를 어떻게 닫았나」 (끝은 2편 예고로 여운)
# 실행: python ep1.py stills  → _build\ep1_stills\ 장면별 처음·가운데·끝 정지 화면
#       python ep1.py         → out\moreno_ep1.mp4
# 위치 출처(모두 블로그 개념도): 우루과이 korea-uruguay-review\images\04_pitch.png
#   베네수엘라 korea-venezuela-result\images\05_center.png · 우즈벡 korea-uzbekistan-result\images\04_press.png
# 작업 메모 지킴: 베네수엘라 선수는 이름 없이 점 · 실명 실수 지목 없음 · 「모레노가 4-4-2를 버렸다」 안 씀
import os, sys
from tactics import *
from tactics import pos_at

BASE = os.path.dirname(os.path.abspath(__file__))


def carry(sc, labels=None):
    """앞 장면이 끝난 자리에서 다음 장면을 시작한다."""
    out = {}
    for pid, (team, x, y, label) in sc['players'].items():
        nx, ny = pos_at(sc, pid, 1e9)
        out[pid] = (team, nx, ny, (labels or {}).get(pid, label))
    return out


# 0 후킹 카드
s0 = dict(type='card', dur=3.0, items=[
    (0.45, 'row', '9월', '에콰도르', '3-0', GREEN, '출발은 좋았다', 560),
    (0.65, 'row', '9월', '우루과이', '1-4', RED, '가운데가 2대3', 730),
    (0.85, 'row', '10월', '베네수엘라', '0-0', AMBER, '가운데가 비었다', 900),
    (1.05, 'row', '10월', '우즈베키스탄', '2-0', GREEN, '가운데를 닫았다', 1070)],
    texts=[(0, 'small', '모레노호 4연전 결산 ①'), (0.05, 'top', '가운데에서\n{뭐가 바뀌었나?}')],
    sfx=[(0.1, 'ding')])

# 1 우루과이 1-4: 투톱 둘 다 센터백으로 → 내려온 벤탄쿠르 비어 있음 → 아라스카에타로
s1 = dict(type='pitch', view=(0.0, 0.45), dur=4.4, players={
    'gk': ('gk', .50, .025, None),
    'cb1': ('opp', .30, .085, None), 'cb2': ('opp', .70, .085, None),
    'ben': ('opp', .50, .24, '벤탄쿠르'), 'tor': ('opp', .25, .20, None), 'ara': ('opp', .66, .31, '아라스카에타'),
    'son': ('kor', .33, .19, '손흥민'), 'oh': ('kor', .67, .19, '오현규'),
    'kim': ('kor', .58, .25, '김봉수'), 'lee': ('kor', .43, .31, '이재성')},
    moves=[('son', 0.4, 1.4, (.31, .125)), ('oh', 0.4, 1.4, (.69, .125)),
           ('ben', 0.6, 1.6, (.50, .135)), ('lee', 2.4, 3.2, (.31, .235))],
    ball=[('at', 0, 'gk'), ('pass', 1.7, 2.1, 'gk', 'ben'), ('pass', 2.6, 3.2, 'ben', 'ara')],
    arrows=[(0.3, 9, 'son', (.31, .13), KOR, False), (0.3, 9, 'oh', (.69, .13), KOR, False),
            (0.5, 9, 'ben', (.50, .15), OPP, True), (2.3, 9, 'lee', (.32, .23), KOR, True)],
    zones=[(3.2, 99, (.48, .37), .14, .05, RED, '빈 자리')],
    texts=[(0, 'top', '우루과이전 {1-4}\n투톱 둘 다 달려들었다', 3.2), (3.2, 'top', '내려온 미드필더를\n{잡을 사람이 없었다}')],
    sfx=[(3.25, 'ding')])

# 2 베네수엘라 0-0: 투톱이 안 누름 → 셋이 끌고 올라옴 → 한 명이 사이로 → 누가 나가지? → 뒷공간
s2 = dict(type='pitch', view=(0.0, 0.90), dur=4.8, players={
    'gk': ('gk', .50, .035, None),
    'b1': ('opp', .31, .13, None), 'b2': ('opp', .69, .13, None), 'b3': ('opp', .52, .17, None),
    'o1': ('opp', .08, .55, None), 'o2': ('opp', .92, .55, None), 'o3': ('opp', .25, .63, None),
    'o4': ('opp', .75, .63, None), 'o5': ('opp', .42, .67, None), 'o6': ('opp', .58, .67, None),
    'son': ('kor', .38, .315, '손흥민'), 'oh': ('kor', .64, .315, '오현규'),
    'hw': ('kor', .65, .51, '황인범'), 'pk': ('kor', .42, .55, '박진섭'),
    'w1': ('kor', .10, .75, None), 'w2': ('kor', .90, .75, None),
    'd1': ('kor', .21, .83, None), 'd2': ('kor', .39, .83, None), 'd3': ('kor', .61, .83, None), 'd4': ('kor', .80, .83, None)},
    moves=[('b1', 0.0, 1.2, (.31, .20)), ('b2', 0.0, 1.2, (.69, .20)), ('b3', 0.0, 1.0, (.52, .254)),
           ('b3', 1.1, 2.0, (.54, .40)), ('hw', 2.3, 2.9, (.61, .46))],
    ball=[('at', 0, 'b1'), ('pass', 2.0, 2.5, 'b1', 'b3'), ('pass', 3.5, 4.2, 'b3', (.71, .87))],
    arrows=[(1.0, 9, 'b3', (.54, .39), OPP, True), (3.4, 9, (.54, .40), (.71, .87), OPP, False)],
    zones=[(2.4, 99, 'b3', .12, .045, AMBER, None)],
    tags=[(0.6, 2.3, (.51, .25), '압박 안 함'), (2.7, 99, (.80, .43), '누가 나가지?')],
    texts=[(0, 'top', '베네수엘라전 {0-0}\n압박을 줄였더니', 2.5), (2.5, 'top', '투톱과 미드필더 사이가\n{텅 비었다}')],
    sfx=[(2.55, 'ding')])

# 3 우즈벡 2-0: 손흥민이 한쪽 센터백, 오세훈이 내려와 미드필더 → 가운데 3대3
s3 = dict(type='pitch', view=(0.0, 0.72), dur=3.4, players={
    'gk': ('gk', .50, .03, None),
    'cbl': ('opp', .35, .14, None), 'cbr': ('opp', .65, .14, None), 'fbl': ('opp', .08, .25, None), 'fbr': ('opp', .92, .25, None),
    'dm': ('opp', .50, .31, None), 'ml': ('opp', .32, .43, None), 'mr': ('opp', .68, .43, None),
    'lw': ('opp', .15, .65, None), 'rw': ('opp', .85, .65, None), 'st': ('opp', .50, .69, None),
    'son': ('kor', .42, .25, '손흥민'), 'oh': ('kor', .58, .25, '오세훈'),
    'c1': ('kor', .34, .50, None), 'c2': ('kor', .66, .50, None), 'w1': ('kor', .10, .56, None), 'w2': ('kor', .90, .56, None),
    'd1': ('kor', .15, .82, None), 'd2': ('kor', .38, .82, None), 'd3': ('kor', .62, .82, None), 'd4': ('kor', .85, .82, None)},
    moves=[('son', 0.4, 1.3, (.38, .195)), ('oh', 0.4, 1.3, (.50, .37))],
    ball=[('at', 0, 'cbl')],
    arrows=[(0.3, 9, 'son', (.38, .20), KOR, False), (0.3, 9, 'oh', (.50, .36), KOR, True)],
    zones=[(1.4, 99, (.50, .42), .30, .10, GREEN, '가운데 3대3')],
    texts=[(0, 'top', '우즈벡전 {2-0}\n투톱 한 명이 내려왔다')],
    sfx=[(1.45, 'ding')])

# 4 반대쪽이면 역할 교대
s4 = dict(type='pitch', view=(0.0, 0.72), dur=2.8, players=carry(s3),
    moves=[('son', 0.6, 1.5, (.50, .37)), ('oh', 0.6, 1.5, (.62, .195))],
    ball=[('at', 0, 'cbl'), ('pass', 0.2, 0.7, 'cbl', 'cbr')],
    arrows=[(0.6, 9, (.38, .195), (.50, .36), KOR, True), (0.6, 9, (.50, .37), (.62, .20), KOR, False)],
    zones=[(0, 99, (.50, .42), .30, .10, GREEN, '가운데 3대3')],
    texts=[(0, 'top', '반대쪽이면 {역할 교대}\n가운데를 닫았다')])

# 5 여운: 상대가 내려앉으면? → 2편에서
s5 = dict(type='pitch', view=(0.0, 0.70), dur=3.8, players=carry(s4),
    moves=[('fbl', 0.2, 1.4, (.12, .13)), ('cbl', 0.2, 1.4, (.32, .10)), ('dm', 0.2, 1.4, (.50, .09)),
           ('cbr', 0.2, 1.4, (.68, .10)), ('fbr', 0.2, 1.4, (.88, .13)),
           ('ml', 0.3, 1.5, (.31, .22)), ('mr', 0.3, 1.5, (.69, .22)), ('lw', 0.3, 1.6, (.14, .23)), ('rw', 0.3, 1.6, (.86, .23)),
           ('st', 0.4, 1.7, (.50, .31)),
           ('son', 0.6, 1.8, (.40, .33)), ('oh', 0.6, 1.8, (.60, .33)), ('c1', 0.6, 1.8, (.35, .46)), ('c2', 0.6, 1.8, (.65, .46)),
           ('w1', 0.6, 1.8, (.08, .36)), ('w2', 0.6, 1.8, (.92, .36)),
           ('d1', 0.6, 1.8, (.15, .62)), ('d2', 0.6, 1.8, (.38, .64)), ('d3', 0.6, 1.8, (.62, .64)), ('d4', 0.6, 1.8, (.85, .62))],
    ball=[('at', 0, 'd2'), ('pass', 1.9, 2.4, 'd2', 'c1')],
    tags=[(2.4, 99, (.50, .165), '찌를 공간이 없다?')],
    dim=(2.7, 110),
    texts=[(0.2, 'top', '그런데 이 방식,\n{아시안컵}에서도 통할까?'), (2.8, 'bot', '다음 편에서 계속 →')],
    sfx=[(2.8, 'ding')])

SCENES = [s0, s1, s2, s3, s4, s5]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        d = os.path.join(BASE, '_build', 'ep1_stills'); os.makedirs(d, exist_ok=True)
        from PIL import Image
        tiles = []
        for i, sc in enumerate(SCENES):
            for t in (0.05, sc['dur'] * 0.5, sc['dur'] - 0.05):
                f = os.path.join(d, f's{i}_{t:.1f}.jpg'); still(sc, t, f)
                tiles.append(Image.open(f).resize((270, 480)))
        sheet = Image.new('RGB', (270 * 6, 480 * 3))
        for j, im in enumerate(tiles):
            sheet.paste(im, ((j // 3) * 270, (j % 3) * 480))
        sheet.save(os.path.join(d, 'sheet.jpg'), quality=90)
        print('stills', d)
    else:
        build(SCENES, BASE, 'ep1', 'moreno_ep1.mp4')
