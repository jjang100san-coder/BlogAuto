# 「날씨요정 판정 | 여행 31번 재 봤더니 진짜 요정은 1번, 악마는 3번이었어」 클립 (발행 10/16 18:32, logNo 224443984690 — Moments > 생활실험)
# 실행: python cutout.py → python make_anims.py → python clipWF.py → out\weather_fairy.mp4
# 10/16 결: 블로그와 결을 달리 — 그림만 봐도 이해되게, 한 장면엔 하나만, 현상→근거 사이에 장 카드(①②③), 끝에 요약 그림 한 장
#   고정 캐릭터 둘(해 요정·먹구름 악마)이 줄곧 나온다. 첫 장면은 발행 썸네일(출국장 어깨 위 둘)을 hailuo 로 움직인 것
# 숫자는 발행본 그대로. 증거 사진 둘(레이크 루이스·경주 통일전)은 내 사진 — 사람은 뒷모습·작게뿐
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = lambda n: os.path.join(os.path.dirname(BASE), 'images', n)
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('나는 날씨요정일까', '여행 31번, 비 온 날을 다 셌다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 캐릭터는 AI 생성')
AI = 'AI 생성 이미지'
MOV = 'video:' + os.path.join(BASE, 'hf_thumb.mp4')
NUM_OK = ('2025.6.9', '2025.11.8')   # 발행본 「2025년 6월 9일」「2025년 11월 8일」 사진 날짜

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.06, label=AI, call_top=True, call=[(0.4, '요정이야, 악마야?', WHITE)],
         cap='친구들이 나보고 날씨요정이래. 진짜인지, 여행 31번을 전부 확인해 봤어.'),
    dict(D, media=A('count'), **AN, call=[(0.4, '사진 폴더 속 여행 31번', YEL)],
         cap='2023년부터 사진 폴더에 남은 여행, 하나도 빼지 않고.'),
    dict(D, media=IMG('ai_scale.png'), z0=1.0, z1=1.1, focus=(0.6, 0.5), label=AI, call_top=True,
         call=[(0.4, '평소 10년 vs 내가 간 날', YEL)],
         cap='그 날짜의 평소 10년 기록과, 내가 간 날을 저울에 올렸어.'),
    dict(D, media=A('score'), **AN, call=[(0.4, '평소 - 실제 = 요정 점수', YEL)],
         cap='평소대로면 비 왔을 날에서, 실제로 젖은 날을 빼. 그게 요정 점수야.'),
    dict(D, media=A('grades'), **AN, call=[(0.4, '등급은 다섯 개', YEL)],
         cap='여기에 확률까지 더해서, 요정부터 악마까지 다섯 등급.'),
    # 현상 → 근거 사이 장 카드(10/16 AT 지적)
    dict(D, media=A('ch1'), **AN, call=[(0.4, '판정 하나', YEL)],
         cap='그럼 진짜 요정은, 몇 번이었을까?'),
    dict(D, media=A('canada'), **AN, call=[(0.4, '캐나다 로키, 엿새', YEL)], sfx=[(2.2, 'ding')],
         cap='딱 한 번, 캐나다 로키 산맥. 평소대로면 사흘 가까이 비였는데, 실제론 하루도 안 왔어.'),
    dict(D, media=IMG('20250609_1012.jpg'), z0=1.0, z1=1.12, focus=(0.5, 0.45), label='2025.6.9 레이크 루이스 · 직접 찍은 사진',
         call_top=True, call=[(0.4, '이만큼 피할 확률 1.6%', YEL)],
         cap='그날 하늘이 바로 이거야. 이만큼 비를 피할 확률은, 1.6퍼센트.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '판정 둘', YEL)],
         cap='그럼 악마는? 세 번이었어.'),
    dict(D, media=A('three'), **AN, call=[(0.4, '경주 · 규슈 · 제주', YEL)],
         cap='경주, 규슈 렌터카 여행, 그리고 제주.'),
    dict(D, media=A('gyeongju'), **AN, call=[(0.4, '경주, 이틀', YEL)], sfx=[(2.0, 'ding')],
         cap='제일 억울한 건 경주. 비가 거의 안 오는 날짜인데, 이틀 내내 젖었어.'),
    dict(D, media=IMG('20251108_1657.jpg'), z0=1.0, z1=1.1, focus=(0.6, 0.62), label='2025.11.8 경주 통일전 · 직접 찍은 사진',
         call_top=True, call=[(0.4, '이만큼 맞을 확률 0.6%', YEL)],
         cap='구름 낀 하늘 아래 우산들. 이만큼 비 맞을 확률은, 0.6퍼센트.'),
    dict(D, media=A('ch3'), **AN, call=[(0.4, '판정 셋', YEL)],
         cap='하지만 묶어 보니, 반전이 있었어.'),
    dict(D, media=A('split'), **AN, call=[(0.4, '해외 17번 vs 국내 14번', YEL)],
         cap='해외만 떼면 요정, 국내에선 견습 악마였어.'),
    # 요약 장(10/16 「이미지도 요약 형태로 장 추가」) — 다섯 등급에 31번이 쌓이고 최종 도장
    dict(D, media=A('recap'), **AN, call=[(0.4, '한 장으로 정리', YEL)],
         cap='전부 모으면, 최종 판정은 견습 요정. 열에 한둘은 그냥 나오는 운이라서.'),
    dict(D, media=IMG('ai_nagoya.png'), z0=1.0, z1=1.0, whole=True, label=AI, call_top=True,
         call=[(0.4, '다음 판정: 1월 나고야', YEL)],
         cap='다음은 1월 나고야. 그 여행에서 나는 진정한 요정이 될 수 있을까? 너는 어느 쪽이야?'),
], BASE, 'WF')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'WF', 'weather_fairy.mp4')
