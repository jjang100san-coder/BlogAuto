# 「캄보디아 사태 뒤 동남아가 무서워졌을까 | 노재팬 땐 80% 식었고 이번엔 24%였어」 클립 (발행 10/19 11:30, logNo 224443981185 — 여행정보)
# 실행: python make_html.py → python clipSE.py → out\sea_fear.mp4
# 10/19 결: 마스터 5-8 움직이는 인포그래픽(clipkit/html_anim.py) + 장 카드 ①②③(검색·마음·발길) + 요약 장(recap)
# 첫 장면은 발행본 첫 그림(물음표 지도, 배경 지도 AI 생성). 숫자는 발행본 그대로, 어느 나라 편도 아님
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = lambda n: os.path.join(os.path.dirname(BASE), 'images', n)
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('동남아가 무서워졌을까', '검색·마음·발길로 재 봤다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 공개 통계·설문')
NUM_OK = ()

SCENES = prep([
    dict(D, media=IMG('sea_01.png'), z0=1.0, z1=1.12, focus=(0.4, 0.55), label='직접 만든 그림 · 배경 지도 AI 생성', call_top=True,
         call=[(0.4, '붉은색이 번졌을까?', WHITE)],
         cap='캄보디아 사태 뒤, 동남아 전체가 무서워졌을까?'),
    dict(D, media=A('three'), **AN, call=[(0.4, '세 군데에서 따로', YEL)],
         cap='무서움을 세 군데에서 따로 살폈어. 검색, 마음, 그리고 발길.'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '판정 하나', YEL)],
         cap='먼저, 걱정할 때 찾는 검색.'),
    dict(D, media=A('search'), **AN, call=[(0.4, '2025년 10월', YEL)],
         cap='캄보디아가 100이면, 이웃 나라는 3도 안 됐어. 그마저 한 달 만에 내려왔고.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '판정 둘', YEL)],
         cap='다음은, 그 나라에 끌리는 마음.'),
    dict(D, media=A('fold'), **AN, call=[(0.4, '노재팬 vs 이번', YEL)], sfx=[(3.2, 'ding')],
         cap='가 보고 싶다던 사람을 다섯 명으로 치면, 노재팬 땐 네 명이 마음을 접었고, 이번엔 한 명쯤이야.'),
    dict(D, media=A('ch3'), **AN, call=[(0.4, '판정 셋', YEL)],
         cap='마지막으로, 실제로 떠난 사람.'),
    dict(D, media=A('steps'), **AN, call=[(0.4, '사태 뒤 넉 달', YEL)],
         cap='발길이 끊긴 건 캄보디아 한 나라. 넉 달 내리, 1년 전보다 절반 넘게 줄었어.'),
    dict(D, media=A('route'), **AN, call=[(0.4, '접었나, 바꿨나', YEL)],
         cap='노재팬 땐 해외여행 자체가 줄었는데, 이번엔 오히려 늘었어. 여행을 접은 게 아니라, 행선지를 바꾼 거야.'),
    # 요약 장(10/16 「이미지도 요약 형태로」)
    dict(D, media=A('recap'), **AN, call=[(0.4, '한 장으로 정리', YEL)],
         cap='정리하면, 검색은 한 달, 마음은 24%, 발길은 캄보디아만.'),
    dict(D, media=A('alert'), **AN, call=[(0.4, '경보는 지역마다', YEL)],
         cap='여행경보는 나라가 아니라 지역에 걸려. 너는 갈 곳을 고를 때, 경보 화면도 열어 봐?'),
], BASE, 'SE')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'SE', 'sea_fear.mp4')
