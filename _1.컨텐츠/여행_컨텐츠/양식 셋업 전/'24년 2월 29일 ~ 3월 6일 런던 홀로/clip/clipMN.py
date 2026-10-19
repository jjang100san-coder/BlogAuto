# 런던 맨체스터 당일치기 클립 (발행 10/15 12:10, logNo 224396378557 — 영국)
# 실행: python clipMN.py stills / python clipMN.py → out\manchester_daytrip.mp4
# 2024-03-04 직접 찍은 사진만(AI 없음, 크레딧 0). 맑은 낮 사진 그대로
# 사람 얼굴이 보이는 컷(유스턴역 광장·피카딜리역 입구·맨체스터역 대합실·책 든 손)은 뺐다. 예약 앱 이름은 말하지 않는다
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
shorts.HEAD = ('런던 → 맨체스터 당일치기', '기차 왕복 5시간, 할 게 없었다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
PH = dict(label='직접 찍은 사진 · 2024년 3월', call_top=True)
NUM_OK = ()

SCENES = prep([
    dict(D, media=P('20240304_122450.jpg'), z0=1.0, z1=1.12, **PH,
         call=[(0.4, '런던 → 맨체스터 당일치기', WHITE), (3.4, '가길 잘했는데, 할 게 없었다', YEL)], sfx=[(3.4, 'ding')],
         cap='런던에서 맨체스터까지, 기차로 당일치기를 했어. 결론부터 말하면, 가길 잘했는데 할 게 없었어.'),
    dict(D, media=P('20240304_090745.jpg'), z0=1.0, z1=1.1, **PH, call=[(0.6, '유스턴 → 피카딜리 약 2시간 20분', YEL)],
         cap='유스턴역에서 피카딜리역까지 약 2시간 20분. 표는 앱으로 미리 사서, QR로 개찰했어.'),
    dict(D, media=P('20240304_124319.jpg'), z0=1.1, z1=1.0, **PH, call=[(0.6, '지하철 말고 트램', YEL)],
         cap='맨체스터엔 지하철이 없어. 시내는 트램이고, 두 구장 다 트램으로 갈 수 있어.'),
    dict(D, media=P('20240304_122450.jpg'), z0=1.15, z1=1.3, **PH, call=[(0.6, '베스트 · 로 · 찰턴', YEL)],
         cap='올드트래포드 앞엔, 베스트, 로, 찰턴 세 사람의 동상이 서 있어.'),
    dict(D, media=P('20240304_132447.jpg'), z0=1.0, z1=1.1, **PH, call=[(0.6, '구장마다 이십 분', YEL)],
         cap='에티하드도 경기가 없는 날이라, 밖에서만 둘러봤어. 구장마다, 이십 분이면 충분했어.'),
    dict(D, media=P('20240304_140023.jpg'), z0=1.0, z1=1.1, **PH, call=[(0.6, '국립축구박물관', YEL)],
         cap='시내로 돌아와서, 국립축구박물관에 갔어. 실내라 날씨 상관없이 볼 수 있어.'),
    dict(D, media=P('20240304_140356.jpg'), z0=1.0, z1=1.12, **PH, call=[(0.6, '트로피 진열장', YEL)],
         cap='트로피가 줄지어 있는 구간이, 제일 볼만했어.'),
    dict(D, media=P('20240304_143611.jpg'), z0=1.1, z1=1.0, **PH, call=[(0.6, '이동 5시간 · 체류 5시간', YEL)],
         cap='오가는 데만 다섯 시간, 머문 것도 그만큼이었어. 하지만 그 안에, 알맹이가 없었어.'),
    dict(D, media=P('20240304_172226.jpg'), z0=1.0, z1=1.1, **PH, call=[(0.6, '구장 투어 하나는 예약', YEL)],
         cap='다시 간다면, 구장 투어 하나는 꼭 예약할 거야. 너는 맨체스터에서, 하루를 어떻게 썼어?'),
], BASE, 'MN')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'MN', 'manchester_daytrip.mp4')
