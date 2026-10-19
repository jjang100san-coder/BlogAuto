# 「셔세권 아파트 상승 | 같은 셔틀 동네인데 수지는 32% 오르고 평택은 16% 내렸어」 클립 (발행 10/18 07:40, logNo 224438963071 — 부동산)
# 실행: python make_html.py → python clipSH2.py → out\shuttle_area.mp4
# 10/18 결: 마스터 5-8 양식 움직이는 인포그래픽(HTML 카드·입체 아이콘, clipkit/html_anim.py) + 10/16 결(한 장면 하나·장 카드 ①②③·요약 장)
# 숫자는 발행본 그대로, 단지 이름 없음. 첫·끝은 발행본 AI 삽화(정류장·퇴근길) — 실제 장소 아님
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = lambda n: os.path.join(os.path.dirname(BASE), '261012_shuttle', n)
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('셔틀 서는 동네면 다 오를까', '실거래로 6곳을 재 봤다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 국토교통부 실거래')
AI = 'AI 생성 이미지 · 실제 장소 아님'
MOV = 'video:' + os.path.join(BASE, 'hf_hook.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.06, label=AI, call_top=True, call=[(0.4, '셔틀 서면 다 오를까?', WHITE)],
         cap='새벽마다 회사 셔틀버스가 서는 동네. 거기면 집값이 다 오를까?'),
    dict(D, media=A('map'), **AN, call=[(0.4, '셔틀 동네 6곳', YEL)],
         cap='삼성 캠퍼스 쪽 셔틀 동네 여섯 곳을, 실거래 자료로 직접 확인해 봤어.'),
    dict(D, media=A('pair'), **AN, call=[(0.4, '같은 아파트끼리만', YEL)],
         cap='같은 아파트가 두 해 모두 팔린 경우만, 짝지어 비교했어.'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '판정 하나', YEL)],
         cap='결과부터 말하면, 이름은 같아도 값은 갈렸어.'),
    dict(D, media=A('race'), **AN, call=[(0.4, '2023년 → 올해 9월', YEL)], sfx=[(1.2, 'ding')],
         cap='2023년부터 올해까지, 용인 수지구는 31.5% 올랐고, 평택시는 15.9% 내렸어.'),
    dict(D, media=A('duel'), **AN, call=[(0.4, '위아래 차이', YEL)],
         cap='위아래 차이가 47%포인트야.'),
    dict(D, media=A('years'), **AN, call=[(0.4, '기준 해를 4번 바꿔도', YEL)],
         cap='기준 해를 네 번 바꿔도, 1등은 수지, 꼴찌는 평택이었어.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '판정 둘', YEL)],
         cap='하지만 유튜브엔, 정반대 숫자가 같이 나와.'),
    dict(D, media=A('claims'), **AN, call=[(0.4, '폭락 vs 상승', YEL)],
         cap='최고가 대비 40% 폭락, 그리고 1주에 2% 상승. 알고 보니 재는 방법이 달랐어.'),
    dict(D, media=A('peak'), **AN, call=[(0.4, '이전 최고가 대비', YEL)], sfx=[(2.0, 'ding')],
         cap='같은 방법으로 다시 따져 보니, 30% 넘게 빠진 곳은 평택 하나뿐이었어.'),
    dict(D, media=A('ch3'), **AN, call=[(0.4, '판정 셋', YEL)],
         cap='또 하나, 규제 다음 달에 거래가 확 줄었어.'),
    dict(D, media=A('cliff'), **AN, call=[(0.4, '동탄 6월 → 7월', YEL)],
         cap='동탄은 6월 1,913건에서, 7월 153건. 10분의 1이 됐어.'),
    dict(D, media=A('people'), **AN, call=[(0.4, '인구 vs 값', YEL)],
         cap='사람이 늘어난 곳과, 값이 오른 데는 달랐어. 수지는 인구가 줄었는데, 가장 많이 올랐어.'),
    dict(D, media=A('recap'), **AN, call=[(0.4, '한 장으로 정리', YEL)],
         cap='셔틀이 원인인지는, 이 자료로는 몰라. 다 같이 오른 건 아니라는 것까지만 말할 수 있어.'),
    dict(D, media=IMG('261012_12.png'), z0=1.0, z1=1.08, focus=(0.5, 0.55), label=AI, call_top=True,
         call=[(0.4, '이름보다 숫자', YEL)],
         cap='셔세권이라는 한 단어 안에, 서로 다른 곳 여섯 개가 있었어. 너희 동네 시세는 따로 봤어?'),
], BASE, 'SH2')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'SH2', 'shuttle_area.mp4')
