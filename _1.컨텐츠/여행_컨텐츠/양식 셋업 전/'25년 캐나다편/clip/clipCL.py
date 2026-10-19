# 캐나다 로키 호수 8곳 순위 클립 (발행 10/12 17:10, logNo 224392249671)
# 실행: python clipCL.py stills / python clipCL.py → out\rockies_lakes.mp4
# 사진은 직접 찍은 것(호수사진\260827). 사진↔호수는 발행본 사진 순서와 해시로 맞춤(10/12):
#   페이토 6월7일-2 · 모레인 6월8일 · 레이크 루이스 6월9일-2 · 보우 6월7일 · 에메랄드 6월9일 · 말리뉴 6월6일-3 · 패트리샤 6월7일-3 · 클리어워터 6월5일
# 표 카드는 발행본 「시간이 없다면 이 순서로」 그대로(make_card.py). 첫 장면은 페이토 사진에 움직임 AI
# 가벼운 웃음 포인트: 보정한 거 아니야, 진짜 저래 · 밤에 가는 길은 살짝 공포야
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), '호수사진', '260827', n)
shorts.HEAD = ('캐나다 로키 호수 8곳', '1위는 모레인이 아니었어')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
L = '2025.06 직접 찍음'
PEYTO = 'video:' + os.path.join(BASE, 'hf_peyto.mp4')
NUM_OK = ('2025.06',)

SCENES = prep([
    dict(D, media=PEYTO, z0=1.0, z1=1.05, label=L + ' · 페이토 호수 · 움직임 AI',
         call=[(0.4, '호수 8곳, 1위는?', WHITE), (3.0, '모레인이 아니었어', YEL)], sfx=[(3.0, 'ding')],
         cap='캐나다 로키 산맥에서 호수 여덟 곳을 돌았는데, 제일 좋았던 데는 모레인이 아니었어.'),
    dict(D, media=P('6월7일-2.jpg'), z0=1.0, z1=1.12, label=L + ' · 페이토 호수',
         call=[(0.4, '1위 페이토', YEL), (3.6, '보정 아님', WHITE)],
         cap='내 일 등은 페이토 호수야. 물색이 형광 파랑인데, 보정한 거 아니야. 진짜 저래.'),
    dict(D, media=P('6월7일-2.jpg'), z0=1.15, z1=1.3, focus=(0.6, 0.6), label=L + ' · 페이토 호수',
         call=[(0.6, '예약·셔틀 필요 없음', YEL)],
         cap='주차장에서 조금만 걸으면 전망대고, 예약도 셔틀도 필요 없어. 하지만 밴프만 도는 일정이면, 그냥 지나치게 돼.'),
    dict(D, media=P('6월8일.jpg'), z0=1.0, z1=1.12, label=L + ' · 모레인 호수',
         call=[(0.4, '2위 모레인', YEL), (5.0, '셔틀 예약 필수', WHITE)],
         cap='이 등은 모레인 호수. 20달러 지폐에 실렸던 풍경이라, 실제로 봐도 실망은 안 해. 다만 셔틀 예약이 필수야.'),
    dict(D, media=P('6월9일-2.jpg'), z0=1.0, z1=1.12, label=L + ' · 레이크 루이스',
         call=[(0.4, '3위 레이크 루이스', YEL)],
         cap='삼 등은 레이크 루이스. 빙하가 정면에 걸려 있고, 호숫가를 걷기엔 여기가 더 나아.'),
    dict(D, media=P('6월7일.jpg'), z0=1.0, z1=1.1, label=L + ' · 보우 호수',
         call=[(0.4, '보우 · 도로변', WHITE)],
         cap='보우 호수는 도로변에 있어. 차를 세우고 바로 내려가면, 뒤로 빙하가 그냥 보여.'),
    dict(D, media=P('6월6일-3.jpg'), z0=1.0, z1=1.1, label=L + ' · 말리뉴 호수',
         call=[(0.4, '말리뉴 · 배로만', WHITE)],
         cap='재스퍼의 말리뉴 호수는, 배를 타야만 안쪽 섬까지 들어갈 수 있어.'),
    dict(D, media=P('6월5일.jpg'), z0=1.0, z1=1.1, label=L + ' · 클리어워터 호수',
         call=[(3.6, '밤길은 살짝 공포', YEL)],
         cap='그리고 첫날 잠깐 쉬어 간 클리어워터. 해 질 무렵이라 사진은 어두운데, 밤에 가는 길은 살짝 공포야.'),
    dict(D, media=os.path.join(BASE, 'card_rank.png'), z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 표 · 발행글 기준',
         call=[(0.5, '하루면 모레인, 사흘이면 파크웨이', YEL)],
         cap='하루뿐이면 모레인 하나, 사흘 이상이면 파크웨이를 달려. 페이토와 보우가 그 길에 다 있어.'),
    dict(D, media=PEYTO, z0=1.05, z1=1.0, label=L + ' · 페이토 호수 · 움직임 AI',
         cap='유명한 두 곳에만 걸지 말고, 가는 길에 있는 호수도 넣어 봐. 너는 어디가 제일 끌려?'),
], BASE, 'CL')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'CL', 'rockies_lakes.mp4')
