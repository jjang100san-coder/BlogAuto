# 제주항공 보조배터리 화재 클립 (발행 10/13 11:50, logNo 224439636622 — 구구절절)
# 실행: python clipPB.py stills / python clipPB.py → out\powerbank_fire.mp4
# 그림은 발행본 도해(img\) 그대로, fit='contain'(그림 위 큰 글 · 아래 말자막). 첫 장면은 발행본 AI 썸네일(실제 제품 아님)에 움직임 —
#   빛은 원본 그대로 실내 낮(10/13 사용자: 노을·어두운 톤 쏠림 금지, 장면마다 다양하게)
# 할 일 하나는 훈계형 대신 「나는 이제 ~해」(메모리 todo-no-lecturing-tone)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), 'img', n)
shorts.HEAD = ('보조배터리 화재, 왜 날까', '충전 열은 고작 4도')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 그린 도해 · 발행글 기준')
BANK = 'video:' + os.path.join(BASE, 'hf_bank.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=BANK, z0=1.0, z1=1.05, label='AI 생성 이미지 · 실제 제품 아님',
         call=[(0.4, '충전하면 뜨거워서 불?', WHITE), (3.6, '겉은 고작 +4도', YEL)], sfx=[(3.6, 'ding')],
         cap='충전하면 배터리가 뜨거워져서, 불이 나는 줄 알았어. 계산해 보니까, 겉은 고작 4도쯤 올라.'),
    dict(D, media=P('P12_bin_vs_hand.png'), **DG, call=[(0.6, '선반 속 vs 손 안', YEL)],
         cap='작년 1월 김해공항에선, 선반 속 배터리 불로 비행기가 다 탔고, 이번 청주공항은 손에 든 배터리라 바로 껐어.'),
    dict(D, media=P('S2_sandwich.png'), **DG, call=[(0.6, '막 한 장이 불을 막는다', YEL)],
         cap='배터리 속은 샌드위치야. 연료와 산소와 열이 한 봉지에 다 들어 있는데, 그 사이를 얇은 분리막 한 장이 갈라놓고 있어.'),
    dict(D, media=P('S3_charge_move.png'), **DG, call=[(0.6, '충전 = 리튬 이사', YEL)],
         cap='충전은 리튬을 마이너스 쪽 방으로 이사시키는 일이야. 자리가 꽉 찼는데 계속 넣으면, 남는 녀석들이 줄지어 그 벽을 눌러.'),
    dict(D, media=P('S5_charge_is_warm.png'), **DG, call=[(0.6, '불씨는 합선', YEL)],
         cap='결국 뚫리면 플러스와 마이너스가 바로 이어져. 이게 합선이고, 그 자리가 순식간에 뜨거워져. 평소 충전 열이 아니라, 여기가 불씨야.'),
    dict(D, media=P('S6_four_temps.png'), **DG, call=[(0.6, '90도부터 스스로', YEL)],
         cap='90도를 넘으면 배터리가 스스로 달아올라. 밖에서 불을 대지 않아도, 열이 열을 부르는 첫 계단이야.'),
    dict(D, media=P('S8_inside_outside.png'), **DG, call=[(0.6, '안에서 생기고 아무도 안 본다', YEL)],
         cap='충전 중 사고가 많은 건, 위험이 생기는 순간에 아무도 안 보고 있기 때문이야. 소방청 집계로는 절반이 과충전 상태였어.'),
    dict(D, media=P('S11_rules.png'), **DG, call=[(0.6, '선반 말고 손에 · 1인 2개', YEL)],
         cap='그래서 비행기 규칙이 바뀌었어. 선반 말고 손에, 그리고 한 사람 두 개까지.'),
    dict(D, media=P('S12_watch_charging.png'), **DG, call=[(0.6, '지켜볼 수 있을 때만', YEL)],
         cap='나는 이제 잘 때는 안 꽂아 둬. 깨어 있을 때, 딱딱한 책상 위에서만 충전해.'),
    dict(D, media=BANK, z0=1.05, z1=1.0, label='AI 생성 이미지 · 실제 제품 아님',
         cap='너는 보조배터리, 주로 어디서 충전해?'),
], BASE, 'PB')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'PB', 'powerbank_fire.mp4')
