# 신치토세공항 하코다테 렌터카 클립 (발행 10/11 17:00, logNo 224392320918)
# 실행: python clipHK.py stills / python clipHK.py → out\hakodate_rentacar.mp4
# 사진은 직접 찍은 것(2025.06 하코다테). 야키니쿠 사진은 다른 사람 손이 보여 잘라냄(yaki_crop.jpg). 카드 3장은 발행본 표·숫자 그대로
# 가벼운 웃음 포인트: 「결론부터 말할게. 그러지 마.」 · 「계획표는, 계획표였던 거지.」
# 녹음 전 검사(10/11): repeat_check · pron_book 통과
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
here = lambda n: os.path.join(BASE, n)
shorts.HEAD = ('도착 당일 280km 운전', '톨비만 8,000엔')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
L = '2025.06 직접 찍음'
CARD = dict(z0=1.0, z1=1.0, whole=True, label='직접 만든 표 · 발행글 기준')
DUSK = 'video:' + here('hf_dusk.mp4')
NUM_OK = ('2025.06',)

SCENES = prep([
    dict(D, media=DUSK, z0=1.0, z1=1.05, label=L + ' · 움직임 AI',
         call=[(0.4, '도착 당일 280km', WHITE), (3.2, '그러지 마', YEL)], sfx=[(3.2, 'ding')],
         cap='비행기에서 내린 날, 바로 280km를 운전해 본 적 있어? 결론부터 말할게. 그러지 마.'),
    dict(D, media=here('card_plan.png'), **CARD,
         cap='일정표는 이랬어. 3시 20분 착륙, 4시 출발, 8시 하코다테 체크인. 표로 보면 그럴듯하지.'),
    dict(D, media=here('rent1_mask.jpg'), z0=1.0, z1=1.1, label=L,
         call=[(3.0, '착륙 → 출발, 1시간은 잡기', YEL)],
         cap='그런데 렌터카는 공항 밖 영업소에 있어. 짐 찾고, 셔틀버스로 이동하고, 서류까지 쓰면, 한 시간은 잡아야 해.'),
    dict(D, media=here('card_license.png'), **CARD,
         cap='그리고 꼭 챙길 것. 국제운전면허증만으론 차를 못 받아. 한국 면허증과 여권까지, 세 개를 같이 냈어.'),
    dict(D, media=P('사이로전망대.jpg'), z0=1.0, z1=1.12, label=L + ' · 사이로 전망대',
         call=[(0.5, '차에서 내린 건 30분', WHITE)],
         cap='그날 차에서 내린 건 딱 한 번. 도야호가 내려다보이는, 사이로 전망대에서, 30분.'),
    dict(D, media=P('20250627_201016.jpg'), z0=1.0, z1=1.1, label=L + ' · 20시 10분',
         call=[(0.5, '체크인 20시', WHITE), (2.6, '20시 10분, 아직 휴게소', YEL)], sfx=[(2.6, 'ding')],
         cap='체크인은 8시로 적어 뒀어. 그런데 8시 10분에, 나는 아직 휴게소였어. 계획표는, 계획표였던 거지.'),
    dict(D, media=here('yaki_crop.jpg'), z0=1.0, z1=1.1, label=L,
         call=[(3.4, '저녁 17,750엔', YEL)],
         cap='9시쯤 짐을 풀었더니, 주변 가게는 거의 다 닫혀 있었어. 열려 있던 고깃집에서 낸 돈이 17,750엔.'),
    dict(D, media=here('card_toll.png'), **CARD,
         cap='렌터카는 예약가보다 8,000엔이 더 나왔어. 그게 고속도로 톨비야. 그날 거리를 그 시간에 가려면, 다른 길이 없거든.'),
    dict(D, media=P('1일차 집가는길.jpg'), z0=1.0, z1=1.1, label=L,
         call=[(0.5, '다시 짠다면', WHITE), (2.6, '첫날은 도야까지', YEL)],
         cap='다시 짠다면, 첫날은 공항 근처나 도야까지만 갈 거야. 같은 거리라도, 다음 날 여유롭게 가면 완전히 다른 여행이거든.'),
    dict(D, media=DUSK, z0=1.05, z1=1.0, label=L + ' · 움직임 AI',
         cap='너는 여행 첫날, 빡빡하게 짜는 편이야? 아니면 여유 있게 두는 편이야?'),
], BASE, 'HK')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'HK', 'hakodate_rentacar.mp4')
