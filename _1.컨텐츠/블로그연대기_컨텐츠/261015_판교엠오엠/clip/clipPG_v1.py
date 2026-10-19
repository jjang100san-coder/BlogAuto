# 판교 스키야키 클립 (예약 발행 10/16 06:50 — 블로그연대기, 광진구 횟집 글의 확장판)
# 실행: python clipPG.py stills / python clipPG.py → out\pangyo_suki.mp4
# 발행 전에 만든다(10/16 사용자 「실제 실행일이 토·일이라 미리」) → 사실은 예약 초안 pangyo_suki_draft.md 본문만(pub_draft.txt 에 옮겨 둠)
# 첫·끝 장면은 초안 AI 썸네일(맑은 낮 창가, 특정 인물·가게 아님)에 hailuo 움직임. 가게·블로거·체험단 사이트 이름 없음, 광고라고 단정하지 않음
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
shorts.HEAD = ('주말 갈 집 후기, 전부 열어 봤다', '해시태그까지 똑같은 글')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 글 기준')
MOV = 'video:' + os.path.join(BASE, 'hf_suki.mp4')
AI = 'AI 생성 이미지 · 특정 인물·가게 아님'
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.05, label=AI,
         call=[(0.4, '해시태그 5개까지 똑같은 글', WHITE), (3.6, '낙지집 0편 · 갈 집 81편', YEL)], sfx=[(3.6, 'ding')],
         cap='이번 주말 갈 곳의 후기를, 전부 열어 봤어. 해시태그 다섯 개가, 순서까지 똑같은 글이 나왔어.'),
    dict(D, media=P('card1_split.png'), **DG, call=[(0.6, '판교 1,622편 · 표기 없음 1,023', YEL)],
         cap='판교 스키야키와 샤브샤브 후기 1,622편. 여기서도 제일 많은 건, 아무 표기 없는 쪽이었어.'),
    dict(D, media=P('card2_compare.png'), **DG, call=[(0.6, '체험단 글 중 대기 숫자 5편', YEL)],
         cap='광진구에선, 기다린 시간을 숫자로 쓴 체험단 후기가 0편. 판교에선 428편 중 5편이었어.'),
    dict(D, media=P('card3_tags.png'), **DG, call=[(0.6, '토요일 0편 · 일요일 81편', YEL)], sfx=[(0.6, 'ding')],
         cap='해시태그가 똑같은 글은, 토요일 낙지집에선 0편, 일요일 갈 집에선 81편이었어.'),
    dict(D, media=P('card4_blocks.png'), **DG, call=[(0.6, '50편 · 블로거 49명', YEL)],
         cap='이 글들은 둘로 나뉘었어. 큰 쪽 50편은 블로거 49명이 썼고, 체험단이라고 밝힌 건 1편뿐이야.'),
    dict(D, media=P('card5_months.png'), **DG, call=[(0.6, '8월 한 달에 39편', YEL)],
         cap='올해는 8월 한 달에만, 39편이 올라왔어. 그중 35편은, 아무 표기가 없었고.'),
    dict(D, media=P('card6_pubs.png'), **DG, call=[(0.6, '체험단 0편인 두 곳', YEL)],
         cap='토요일 2차 후보 여섯 군데도 열어 봤어. 체험단이 0편인 두 곳에서, 대기 시간을 숫자로 쓴 후기가 25편, 28편 나왔어.'),
    dict(D, media=P('img1.png'), z0=1.1, z1=1.0, label=AI, call=[(0.6, '왜 똑같은지는 모른다', YEL)],
         cap='왜 똑같은지는, 이 결과로 알 수 없어. 그래서 주말에 직접 가서, 내 숫자로 적어 올게.'),
    dict(D, media=MOV, z0=1.05, z1=1.0, label=AI,
         cap='옷에 냄새가 배는지 쓴 글은, 한 편도 없었어. 너는 후기 볼 때, 해시태그도 봐?'),
], BASE, 'PG')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'PG', 'pangyo_suki.mp4')
