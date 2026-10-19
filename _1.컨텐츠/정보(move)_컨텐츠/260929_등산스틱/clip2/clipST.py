# 등산스틱 추천 클립 — 새 틀 시험 3/5 (발행 10/10 15:10, logNo 224434615531)
# 실행: python clipST.py stills / python clipST.py → out\pole_v2.mp4
# 사진: 10/7 집에서 직접 잰 본트래커(손은 본인). 남의 유튜브 화면은 쓰지 않는다. AI 2장은 「AI 생성 이미지」 표시
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(BASE)
PH = os.path.join(UP, 'base data', '261007-2')
AI = os.path.join(UP, '클로드')
shorts.HEAD = ('유튜브 8편 보고', '고른 답은 집에 있었다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)

SCENES = prep([
    dict(D, media=os.path.join(PH, '20261007_224154.jpg'), z0=1.0, z1=1.15, ease='punch', focus=(0.5, 0.45), label='직접 찍음',
         call=[(0.4, '유튜브 8편', YEL)], sfx=[(0.4, 'ding')],
         cap='등산스틱 고르려고 유튜브 8편을 끝까지 봤어.'),
    dict(D, media=os.path.join(PH, '20261007_223949.jpg'), z0=1.0, z1=1.1, label='본트래커 · 직접 찍음',
         call=[(0.6, '3만 원대', YEL)], sfx=[(0.6, 'ding')],
         cap='고른 답은 3만 원대 두랄루민 접이식, 본트래커. 그런데 계룡산 가려고 사 둔 한 쌍이, 이미 집에 있었어.'),
    dict(D, media=os.path.join(AI, 'ai_thumb_base.png'), z0=1.0, z1=1.1, label='AI 생성 이미지',
         call=[(0.6, '8편 중 1편', WHITE)],
         cap='8편 중에, 광고 없이 제품을 직접 산 영상은 한 편뿐이었어. 무게를 달고, 밟아 보며 비교했지.'),
    dict(D, media=os.path.join(AI, 'ai_pole_length.png'), z0=1.0, z1=1.08, label='AI 생성 이미지 · 특정 인물 아님',
         call=[(0.6, '팔꿈치 직각', YEL), (2.6, '내리막 +5~10cm', WHITE)],
         cap='브랜드보다 먼저 볼 건 길이야. 평지는 팔꿈치 직각, 내리막은 조금 더 뽑아.'),
    dict(D, media=os.path.join(PH, '20261007_224238.jpg'), z0=1.0, z1=1.12, label='직접 잰 값',
         call=[(0.4, '판매 페이지 130cm', WHITE), (1.8, '직접 재니 약 134cm', YEL)], sfx=[(1.8, 'ding')],
         cap='끝까지 늘려 재 보니, 판매 페이지보다 긴 약 134cm였어.'),
    dict(D, media=os.path.join(PH, 'stick_stop_mark.jpg'), z0=1.0, z1=1.12, label='직접 찍음',
         call=[(0.6, '52 눈금 위 STOP', YEL)],   # 52 는 소리로 말하지 않는다(「오십이라고」→50, 2회) — 화면 글로만
         cap='손잡이 아래 마디엔 숫자가 새겨져 있어. 맨 위 눈금 바로 다음이 STOP 표시야. 이게 밖으로 보이면, 너무 뽑은 거야.'),
    dict(D, media=os.path.join(PH, '20261007_224334.jpg'), z0=1.0, z1=1.15, ease='punch', label='잠금 핀 · 직접 찍음',
         call=[(0.5, '딸깍', YEL)], sfx=[(0.5, 'kick')],
         cap='접이식은 잠금 핀이 딸깍 걸렸는지부터 봐. 그냥 펴서 쓰면 마디가 빠져.'),
    dict(D, media=os.path.join(PH, '20261007_224314.jpg'), z0=1.0, z1=1.08, label='직접 찍음',
         call=[(0.4, '3만 원대 = 30만 원대?', YEL)],
         cap='싼 스틱이든 비싼 스틱이든 할 일은 다 한대. 너는 살 때 뭘 제일 먼저 봐?'),
], BASE, 'ST')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'ST', 'pole_v2.mp4')
