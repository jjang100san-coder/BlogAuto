# 「캠프라인 경등산화 밴티지 러닝화 차이 | 손으로 접으니 똑같이 접혔어」 클립 (발행 10/19 06:50, logNo 224443138666 — 장비)
# 실행: python make_html.py → python clipFD.py → out\fold_test.mp4
# 10/19 결: 내 사진(접기 3장·나란히 1장) + 마스터 5-8 움직이는 인포그래픽(clipkit/html_anim.py) + 장 카드·요약 장(recap)
# 체중계 사진은 유리에 몸이 비쳐 쓰지 않고 숫자 그림(scale)으로. 업체 이름은 신발 상표만(글과 같게)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
PH = lambda n: os.path.join(os.path.dirname(BASE), n)
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('등산화는 안 접힌다?', '내 신발 세 켤레로 접어 봤다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 아이콘은 AI 생성')
ME = '직접 찍은 사진'
NUM_OK = ()

SCENES = prep([
    dict(D, media=PH('04_side_by_side_3.jpg'), z0=1.0, z1=1.1, focus=(0.5, 0.42), label=ME, call_top=True,
         call=[(0.4, '등산화는 안 접힌다?', WHITE)],
         cap='흔히 등산화는, 손으로 안 접힌다고 하잖아. 정말일까?'),
    dict(D, media=A('claim'), **AN, call=[(0.4, '유튜브 속 판별법', YEL)],
         cap='유튜브에서 본 판별법이야. 등산화는 안 접히고, 러닝화는 접힌다는 거지.'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '판정 하나', YEL)],
         cap='그래서 집에 있는 신발 세 켤레로, 직접 해 봤어.'),
    dict(D, media=PH('01_runner_black_bend.jpg'), z0=1.0, z1=1.1, focus=(0.4, 0.5), label=ME, call_top=True,
         call=[(0.4, '아식스 러닝화', YEL)],
         cap='먼저 아식스 러닝화. 앞쪽이 쉽게 꺾였어.'),
    dict(D, media=PH('02_runner_white_bend.jpg'), z0=1.0, z1=1.1, focus=(0.5, 0.5), label=ME, call_top=True,
         call=[(0.4, '퓨마 러닝화', YEL)],
         cap='퓨마도 마찬가지였고.'),
    dict(D, media=PH('03_vantage_bend.jpg'), z0=1.0, z1=1.12, focus=(0.5, 0.45), label=ME, call_top=True,
         call=[(0.4, '경등산화 밴티지', YEL)], sfx=[(2.0, 'ding')],
         cap='그럼 경등산화 밴티지는? 비슷한 힘을 주니, 이것도 꺾였어.'),
    dict(D, media=A('verdict'), **AN, call=[(0.4, '세 켤레 결과', YEL)],
         cap='세 켤레 다 접혔어. 접어 보기만으로는, 등산화를 가려내기 어려웠어.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '판정 둘', YEL)],
         cap='차이는 오히려, 바닥에 내려놓았을 때 보였어.'),
    dict(D, media=PH('04_side_by_side_3.jpg'), z0=1.2, z1=1.45, focus=(0.62, 0.55), focus1=(0.62, 0.72), label=ME, call_top=True,
         call=[(0.4, '러닝화는 앞코가 들려 있다', YEL)],
         cap='러닝화 두 켤레는, 손대기 전부터 앞코가 들려 있어.'),
    dict(D, media=A('diff'), **AN, call=[(0.4, '옆에서 보면', YEL)],
         cap='밴티지는 앞코가 납작하고, 밑창 돌기가 깊고, 발가락을 고무가 감싸.'),
    dict(D, media=A('ch3'), **AN, call=[(0.4, '판정 셋', YEL)],
         cap='무게도 달아 보려고 했어.'),
    dict(D, media=A('scale'), **AN, call=[(0.4, '신발 들고 체중계', YEL)],
         cap='신발을 들고 체중계에 올랐더니, 러닝화 둘이 똑같이 나왔어. 체중계로는 못 재는 거였지.'),
    # 요약 장(10/16 「이미지도 요약 형태로」)
    dict(D, media=A('recap'), **AN, call=[(0.4, '매장에서 볼 것', YEL)],
         cap='그래서 다음엔, 접기 전에 옆모습부터 볼 거야. 너는 신발 살 때 뭐부터 봐?'),
], BASE, 'FD')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'FD', 'fold_test.mp4')
