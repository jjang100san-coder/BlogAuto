# 판교 스키야키 클립 v2 (예약 발행 10/16 06:50 — 블로그연대기)
# 실행: python make_anims.py → python clipPG.py → out\pangyo_suki.mp4   (첫 판은 clipPG_v1.py · narration\PG_v1 · out\pangyo_suki_v1.mp4)
# 10/16 사용자: 「블로그랑 결을 달리 — 집중 안 해도 그림만으로 이해되게」 「장면을 늘려서, 한 장면엔 하나만」
#   → 광진구 비교·판교 1,622편·2차 후보는 빼고 「일요일 갈 집 후기, 해시태그가 똑같다」 한 줄기만. 장면마다 큰 글 한 줄 + 숫자 하나, 표 카드 대신 움직이는 그림(make_anims.py)
# 사실은 예약 초안 pangyo_suki_draft.md 숫자만. 가게·블로거 이름 없음, 광고라고 단정하지 않음
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')   # 프레임은 _frames_<n>\ 에 이미 있다
shorts.HEAD = ('일요일 갈 스키야키 집', '후기 해시태그가 똑같다?')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 글 기준')
MOV = 'video:' + os.path.join(BASE, 'hf_suki.mp4')
AI = 'AI 생성 이미지 · 특정 인물·가게 아님'
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.05, label=AI, call=[(0.4, '가기 전에 후기부터', WHITE)],
         cap='일요일에 갈 스키야키 집이 있어. 가기 전에, 후기부터 열어 봤어.'),
    dict(D, media=A('count'), **AN, call=[(0.4, '후기 292개 전부', YEL)],
         cap='후기 292개, 하나하나 전부.'),
    dict(D, media=A('zoom'), **AN, call=[(0.4, '글 끝 해시태그 다섯 개', YEL)],
         cap='그러다 글 끝에 붙은 해시태그에서, 손이 멈췄어.'),
    dict(D, media=A('tags'), **AN, call=[(0.4, '순서까지 똑같다', YEL)], sfx=[(1.1, 'ding')],
         cap='해시태그 다섯 개가, 순서까지 똑같은 후기가 81개.'),
    dict(D, media=A('other'), **AN, call=[(0.4, '토요일 낙지집은?', YEL)],
         cap='토요일에 갈 낙지집은? 똑같은 후기가 0개였어.'),
    dict(D, media=A('people'), **AN, call=[(0.4, '서로 다른 사람 49명', YEL)],
         cap='그중 50개는, 서로 다른 49명이 썼어.'),
    dict(D, media=A('ad'), **AN, call=[(0.4, '광고 표시는 1개', YEL)], sfx=[(0.6, 'ding')],
         cap='광고라고 밝힌 글은, 딱 1개.'),
    dict(D, media=A('month'), **AN, call=[(0.4, '8월 한 달에 39개', YEL)],
         cap='올해는 8월 한 달에만, 39개가 올라왔고.'),
    dict(D, media=MOV, z0=1.05, z1=1.0, label=AI, call=[(0.4, '일요일, 직접 가서 확인', YEL)],
         cap='왜 똑같은지는 나도 몰라. 그래서 일요일에 직접 가서 확인할게. 너는 후기 볼 때, 해시태그도 봐?'),
], BASE, 'PG')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'PG', 'pangyo_suki.mp4')
