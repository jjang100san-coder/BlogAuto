# 현풍 소굽는집 클립 (발행 10/11 15:10, logNo 224437008134)
# 실행: python clipBF.py stills / python clipBF.py → out\hyeonpung_beef.mp4
# 사진은 직접 찍은 것(261004\). 접시 든 손 사진(192457)은 동행 손일 수 있어 뺐다. 건물 사진은 차 번호판 아래를 잘라냄(bld_crop.jpg)
# 10/11 사용자: 라면은 안 먹었으니 「마무리는 라면」 금지 → 코너가 있다는 것만 · 끝 질문은 상차림비(이 집 제도) 말고 메뉴 가격으로
# 가벼운 웃음 포인트(10/11 사용자 「사이사이 유머」): 헬스장 건물 같아서 헤맸어 · 상차림비도 차곡차곡 · 소주 2,500원은 반가웠어
# 숫자는 발행본 그대로. 400g = 치마살 200g + 부채살 200g · 계산서는 영수증 순서(태블릿 76,000원 → 술 5,000원 → 81,000원, 10/11 사용자)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), '261004', n)
shorts.HEAD = ('현풍 3층 고깃집', '한우 400g에 81,000원')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
GRILL = 'video:' + os.path.join(BASE, 'hf_grill.mp4')
L3 = '2026.10.03 직접 찍음'
NUM_OK = ('400', '2026.10.03', '2026.10.04')

SCENES = prep([
    dict(D, media=GRILL, z0=1.0, z1=1.05, label=L3 + ' · 움직임 AI',
         call=[(0.3, '현풍 3층 고깃집', WHITE), (2.6, '한우 400g · 81,000원', YEL)], sfx=[(2.6, 'ding')],
         cap='대구 현풍 3층 고깃집. 한우 400g에 술 두 병, 계산은 81,000원이었어.'),
    dict(D, media=os.path.join(BASE, 'bld_crop.jpg'), z0=1.0, z1=1.1, focus=(0.5, 0.4), label='2026.10.04 직접 찍음',
         call=[(3.2, '1층 아니고 3층', YEL)],
         cap='이 고깃집, 1층이 아니라 상가 3층이야. 밖에서 보면 헬스장 건물 같아서, 처음엔 좀 헤맸어.'),
    dict(D, media=P('20261003_191312.jpg'), z0=1.0, z1=1.12, label=L3,
         call=[(2.0, '200g 33,000원', YEL)],
         cap='주문은 태블릿으로 해. 200g에 치마살 33,000원, 부채살도 같은 값이야.'),
    dict(D, media=P('20261003_191013.jpg'), z0=1.0, z1=1.1, label=L3,
         call=[(0.5, '상차림비 8,000원', YEL), (3.6, '5,000 → 7,000 → 8,000', WHITE)],
         cap='상차림비는 8,000원이야. 예전 후기엔 5,000원, 7,000원이었는데, 차곡차곡 올랐더라.'),
    dict(D, media=P('20261003_192450.jpg'), z0=1.0, z1=1.12, label=L3,
         call=[(0.5, '치마살 · 부채살', WHITE)],
         cap='고기는 맛있었어. 다만 구워 준다는 안내와 달리, 그날은 우리가 직접 구웠어.'),
    dict(D, media=P('20261003_200122.jpg'), z0=1.0, z1=1.1, label=L3,
         call=[(2.2, '셀프 술 2,500원', YEL)], sfx=[(2.2, 'ding')],
         cap='술은 냉장고에서 알아서 꺼내 와. 소주도 맥주도 2,500원. 이건 좀 반가웠어.'),
    dict(D, media=P('20261003_200055_crop.jpg'), z0=1.0, z1=1.1, label=L3,
         call=[(0.5, '셀프라면 코너 · 1,000원', YEL)],
         cap='가게 한쪽엔 셀프라면 코너도 있어. 한 개 1,000원. 이번엔 고기만으로 배가 불렀어.'),
    dict(D, media=P('20261003_201421.jpg'), z0=1.0, z1=1.12, label=L3,
         call=[(1.6, '주차 등록 · 2시간 무료', YEL)],
         cap='차로 간다면 주차 등록 꼭 해. 내가 본 안내는 2시간 무료였어.'),
    dict(D, media=os.path.join(BASE, 'card_bill.png'), z0=1.0, z1=1.0, whole=True, label='직접 만든 표 · 발행글 주문 내역',
         cap='정리하면, 태블릿 주문이 상차림비까지 76,000원. 여기에 술 두 병을 더해서 81,000원.'),
    dict(D, media=GRILL, z0=1.05, z1=1.0, label=L3 + ' · 움직임 AI',
         call=[(4.6, '한우 200g 33,000원, 어때?', YEL)],
         cap='연휴 기간이라 홀이 조용했고, 가격도 비싸다는 느낌은 없었어. 너는 한우 200g에 33,000원, 어때?'),
], BASE, 'BF')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'BF', 'hyeonpung_beef.mp4')
