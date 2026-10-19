# 아시안게임 금메달 클립 — 「결승 선발 6명이 3년 전 김은중호」 (발행 10/5, logNo 224431400261)
# 실행: python gold.py stills  /  python gold.py → out\gold_clip.mp4
# 근거: 발행 본문 + base data2\01_결승종합분석_한국1-0일본.md (선발 24행 · 플랜 27행 · 요코야마/강상윤 54~56행 · 결승골 69~73행)
# 지킴: 본문에 이름이 없는 선발(이기혁)은 점으로만 · 경기 수치는 「한 분석 채널 집계」 · 「지친 일본」 단정 안 함 · 위치는 개념도
import os, sys
from tactics import *
from tactics import pos_at

BASE = os.path.dirname(os.path.abspath(__file__))
GOLD = AMBER

# 결승 선발 4-2-3-1 (한국이 위로 공격)
XI = {'lyj': ('kor', .50, .42, '이영준'), 'ujs': ('kor', .18, .50, '엄지성'), 'bjh': ('kor', .50, .52, '배준호'),
      'ymh': ('kor', .82, .50, '양민혁'), 'm1': ('kor', .37, .65, None), 'lsw': ('kor', .63, .65, '이승원'),
      'bhs': ('kor', .12, .78, '배현서'), 'kjs': ('kor', .37, .82, '김지수'), 'smh': ('kor', .63, .82, '신민하'),
      'csh': ('kor', .88, .78, '최석현'), 'kjh': ('kor', .50, .95, '김준홍')}
SIX = ['kjh', 'kjs', 'csh', 'lsw', 'bjh', 'lyj']   # 2023 U-20 김은중호 최종 명단과 겹치는 6명

s0 = dict(type='pitch', view=(0.30, 1.0), dur=4.2, players=dict(XI),
    zones=[(0.6 + i * 0.35, 99, pid, .07, .028, GOLD, None) for i, pid in enumerate(SIX)],
    tags=[(2.9, 99, (.50, .345), '2023 U-20 김은중호 6명')],
    texts=[(0, 'small', '아시안게임 금메달 · 한국 1-0 일본'), (0.05, 'top', '결승 선발 11명 중 {6명}이\n3년 전 그 팀이었다')],
    sfx=[(0.1, 'ding')] + [(0.6 + i * 0.35, 'kick') for i in range(6)] + [(2.9, 'ding')])

s1 = dict(type='card', dur=3.4, items=[
    (0.15, 'big', '한국 1 - 0 일본', 560, 84, CREAM),
    (0.45, 'row', '', '슈팅', '5 : 10', RED, '한국 : 일본', 720),
    (0.65, 'row', '', '유효슈팅', '2 : 2', AMBER, '골문으로 간 공은 같았다', 890),
    (0.85, 'row', '', '코너킥', '0 : 5', RED, '', 1060),
    (1.05, 'row', '', '후반 점유율', '36 : 64', RED, '', 1230),
    (1.4, 'big', '공식 기록 아님 · 한 분석 채널 집계', 1420, 30, MUTED)],
    texts=[(0.05, 'top', '이긴 쪽이\n{밀린 경기}')], sfx=[(0.1, 'ding')])

# 2 플랜: 일본 투톱이 센터백에 달려들면 → 이영준에게 길게 → 배준호·엄지성이 떨군 공
JP = {'jgk': ('gk', .50, .03, None), 'jd1': ('opp', .22, .20, None), 'jd2': ('opp', .41, .18, None),
      'jd3': ('opp', .59, .18, None), 'jd4': ('opp', .78, .20, None), 'jm1': ('opp', .38, .40, None),
      'jm2': ('opp', .62, .40, None), 'jw1': ('opp', .15, .44, None), 'jw2': ('opp', .85, .44, None),
      'js1': ('opp', .42, .62, None), 'js2': ('opp', .58, .62, None)}
s2 = dict(type='pitch', view=(0.10, 1.0), dur=4.4, players={**JP, **XI},
    moves=[('js1', 0.2, 1.0, (.39, .76)), ('js2', 0.2, 1.0, (.60, .76)),
           ('lyj', 0.6, 1.5, (.50, .30)), ('bjh', 1.6, 2.3, (.47, .38)), ('ujs', 1.6, 2.4, (.33, .36))],
    ball=[('at', 0, 'kjs'), ('pass', 1.1, 1.9, 'kjs', 'lyj'), ('pass', 2.2, 2.6, 'lyj', 'bjh')],
    arrows=[(0.2, 9, (.42, .62), (.39, .75), OPP, False), (0.2, 9, (.58, .62), (.60, .75), OPP, False),
            (1.6, 9, (.18, .50), (.32, .37), KOR, True)],
    zones=[(1.0, 99, (.50, .68), .16, .04, GREEN, None)],
    tags=[(1.0, 99, (.50, .685), '그 뒤엔 숫자가 남는다'), (2.6, 99, (.73, .33), '떨군 공')],
    texts=[(0.05, 'top', '이민성 감독의 플랜\n{이영준 선수에게 길게}')], sfx=[(1.1, 'ding')])

# 3 일본이 읽었다: 투톱 하나는 미드필드로 · 이영준에게 두 명 · 윙이 안으로
s3 = dict(type='pitch', view=(0.10, 1.0), dur=4.0, players={**JP, **XI},
    moves=[('js1', 0.2, 1.0, (.42, .74)), ('js2', 0.2, 1.0, (.56, .50)),
           ('jw1', 0.3, 1.1, (.30, .42)), ('jw2', 0.3, 1.1, (.70, .42)), ('jm1', 0.3, 1.1, (.45, .34)),
           ('jd2', 0.3, 1.1, (.48, .25)), ('lyj', 0.3, 1.1, (.50, .30))],
    ball=[('at', 0, 'kjs'), ('pass', 1.4, 2.2, 'kjs', 'lyj'), ('pass', 2.4, 2.8, 'lyj', 'jm1')],
    zones=[(1.2, 99, (.50, .32), .14, .05, RED, '두 명이 붙었다')],
    tags=[(2.9, 99, (.74, .52), '다른 수가 없었다')],
    texts=[(0.05, 'top', '일본은 15분 만에\n{그 플랜을 읽었다}')], sfx=[(1.25, 'ding')])

# 4 버틴 이유: 요코야마의 드리블 → 강상윤이 들어와 최석현과 2대1
s4 = dict(type='pitch', view=(0.35, 1.0), dur=4.2, players={
    'kjh': ('kor', .50, .95, '김준홍'), 'bhs': ('kor', .14, .80, None), 'kjs': ('kor', .38, .82, None),
    'smh': ('kor', .62, .82, None), 'csh': ('kor', .84, .80, '최석현'), 'm1': ('kor', .40, .66, None),
    'lsw': ('kor', .58, .66, None), 'ujs': ('kor', .18, .64, None),
    'yoko': ('opp', .80, .52, '요코야마'), 'j2': ('opp', .55, .50, None), 'j3': ('opp', .30, .52, None), 'j4': ('opp', .48, .62, None),
    'kang': ('kor', .70, .48, '강상윤')},
    moves=[('yoko', 0.3, 1.3, (.86, .70)), ('csh', 0.6, 1.3, (.86, .76)), ('kang', 1.0, 1.9, (.79, .72))],
    ball=[('at', 0, 'yoko'), ('pass', 2.1, 2.4, 'yoko', 'kang')],
    arrows=[(0.9, 9, (.70, .48), (.78, .70), KOR, True)],
    zones=[(1.9, 99, (.83, .73), .10, .05, GREEN, '2대1로 닫았다')],
    texts=[(0.05, 'top', '버틴 이유 하나\n{요코야마 길을 둘이 막았다}')], sfx=[(1.95, 'ding')])

# 5 결승골: 양민혁이 살린 공 → 크로스 → 골키퍼 맞고 → 엄지성이 한 번 접고
s5 = dict(type='pitch', view=(0.0, 0.55), dur=4.6, players={
    'jgk': ('gk', .50, .03, None), 'jd1': ('opp', .30, .10, None), 'jd2': ('opp', .44, .08, None),
    'jd3': ('opp', .58, .08, None), 'jd4': ('opp', .74, .14, None), 'jm': ('opp', .40, .22, None),
    'ymh': ('kor', .80, .30, '양민혁'), 'ujs': ('kor', .28, .26, '엄지성'), 'lyj': ('kor', .60, .18, '이영준')},
    moves=[('ymh', 0.2, 1.3, (.88, .05)), ('ujs', 1.0, 2.1, (.40, .13)), ('ujs', 2.5, 2.9, (.46, .13))],
    ball=[('at', 0, 'ymh'), ('pass', 1.5, 2.0, 'ymh', (.50, .045)), ('pass', 2.0, 2.4, (.50, .045), 'ujs'),
          ('pass', 3.0, 3.3, 'ujs', (.455, .0))],
    tags=[(0.9, 1.6, (.72, .12), '나가는 공을 살렸다'), (2.5, 3.2, (.30, .10), '한 번 접고')],
    zones=[(3.3, 99, (.46, .02), .10, .02, GOLD, None)],
    texts=[(0.05, 'top', '후반 16분\n{엄지성} 결승골', 3.3), (3.3, 'top', '포기 안 한 발 하나\n{판단 하나}')],
    sfx=[(3.32, 'ding')])

# 6 바통: 같은 6명이 다시 빛나고 → 김은중호는 2028 LA
s6 = dict(type='pitch', view=(0.30, 1.0), dur=4.0, players=dict(XI), dim=(0.0, 120),
    zones=[(0.1, 99, pid, .07, .028, GOLD, None) for pid in SIX],
    texts=[(0.05, 'top', '김은중 감독이 키운 세대\n{이민성 감독이 금메달}'), (1.6, 'bot', '김은중호, 다음 장은 2028 LA')],
    sfx=[(1.6, 'ding')])

SCENES = [s0, s1, s2, s3, s4, s5, s6]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        from PIL import Image
        d = os.path.join(BASE, '_build', 'stills'); os.makedirs(d, exist_ok=True)
        tiles = []
        for i, sc in enumerate(SCENES):
            for t in (sc['dur'] * 0.45, sc['dur'] - 0.05):
                f = os.path.join(d, f's{i}_{t:.1f}.jpg'); still(sc, t, f); tiles.append(Image.open(f).resize((216, 384)))
        sh = Image.new('RGB', (216 * len(SCENES), 384 * 2))
        for j, im in enumerate(tiles):
            sh.paste(im, ((j // 2) * 216, (j % 2) * 384))
        sh.save(os.path.join(d, 'sheet.jpg'), quality=90); print('stills', d)
    else:
        build(SCENES, BASE, 'gold', 'gold_clip.mp4')
