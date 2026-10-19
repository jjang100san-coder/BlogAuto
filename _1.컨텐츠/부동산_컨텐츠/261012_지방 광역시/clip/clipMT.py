# 지방 아파트 클립 (발행 10/13 17:00, logNo 224440123467)
# 실행: python clipMT.py stills / python clipMT.py → out\metro_apartments.mp4
# 그림은 발행본 직접 만든 그림(261013_metro\), fit='contain'. 발행본 AI 그림(노을 도시·노을 항구·새벽 안개)은 쓰지 않고
#   클립용 AI 장면을 새로 — 맑은 한낮 강변 도시(첫 장면·움직임) · 흐리고 비 오는 아침 항구 도시(10/13 사용자: 노을 쏠림 금지, 장면마다 다양하게)
# 단지 이름 없이 시·구 단위만. 이유를 단정하지 않는다(발행본 「왜 오르는지는 말하지 않을게」)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), '261013_metro', n)
here = lambda n: os.path.join(BASE, n)
shorts.HEAD = ('지방 아파트, 바닥일까', '최고가보다 울산 12% · 세종 30% 아래')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 2026.10.12 조회')
CITY = 'video:' + here('hf_city.mp4')
NUM_OK = ('2026.10.12',)

SCENES = prep([
    dict(D, media=CITY, z0=1.0, z1=1.05, label='AI 생성 이미지 · 실제 도시 사진 아님',
         call=[(0.4, '지방 아파트 바닥?', WHITE), (4.2, '예전 최고가와 맞춰 봤다', YEL)], sfx=[(4.2, 'ding')],
         cap='지방 아파트, 바닥 찍었다는 말 많이 들리지? 그래서 광역시 여섯 곳의 거래를, 그 단지가 예전에 찍은, 가장 비싼 값과 하나하나 맞춰 봤어.'),
    dict(D, media=P('261013_2.png'), **DG, call=[(0.6, '울산 -12.1% · 세종 -30.1%', YEL)],
         cap='울산은 최고가보다 12% 아래에서 거래되고 있었어. 세종은 30% 아래였고.'),
    dict(D, media=P('261013_2.png'), **DG, call=[(0.6, '절반 넘게 20% 이상 아래', YEL)],
         cap='울산 말고 나머지 다섯 곳은, 절반이 넘는 거래가 최고가보다 20% 이상 낮았어.'),
    dict(D, media=P('261013_3.png'), **DG, call=[(0.6, '어디서 재도 울산 1위', YEL)],
         cap='같은 단지를 해마다 짝지어 봐도, 언제부터 재든 울산이 맨 위였어.'),
    dict(D, media=P('261013_5.png'), **DG, call=[(0.6, '남구 +8.9% · 동구 -5.9%', YEL)],
         cap='다만 거기도 다 오른 건 아니야. 같은 도시 안에서도, 남구는 올랐고 동구는 내렸어.'),
    dict(D, media=here('ai_port_overcast.png'), z0=1.0, z1=1.1, label='AI 생성 이미지 · 실제 울산 사진 아님',
         call=[(0.5, '왜 울산만?', WHITE), (4.2, '흔한 설명 3개, 숫자와 안 맞음', YEL)],
         cap='그럼 왜 울산만 오를까? 영상에서 자주 나온 설명 세 개를 숫자와 맞춰 봤는데, 하나도 확인이 안 됐어.'),
    dict(D, media=P('261013_6.png'), **DG, call=[(0.6, '부산 3배 · 대구 3분의 1', YEL)],
         cap='미분양은 부산이 세 배가 됐고, 대구는 3분의 1로 줄었어. 다만 그렇게 남은 물량 대부분이, 다 짓고도 안 팔린 집이야.'),
    dict(D, media=P('261013_8.png'), **DG, call=[(0.6, '잣대마다 다른 답', YEL)],
         cap='결국 바닥이냐고 물으면, 잣대마다 답이 달라. 지방이라고 한데 묶지 말고, 그 도시 그 구를 따로 보는 게 먼저였어.'),
    dict(D, media=CITY, z0=1.05, z1=1.0, label='AI 생성 이미지 · 실제 도시 사진 아님',
         cap='너는 어느 도시가 제일 궁금해?'),
], BASE, 'MT')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'MT', 'metro_apartments.mp4')
