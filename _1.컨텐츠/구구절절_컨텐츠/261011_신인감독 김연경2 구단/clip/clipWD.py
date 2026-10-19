# 신인감독 김연경2 원더독스 구단 창단 비용 클립 (발행 10/12 13:04, logNo 224438862354 — 구구절절)
# 실행: python clipWD.py stills / python clipWD.py → out\wonderdogs_cost.mp4
# 그림은 발행본 도해(img\) 그대로, fit='contain'(그림 위 큰 글 · 아래 말자막 — 10/12 사용자 「글귀가 그림을 덮는다」)
# 첫 장면은 발행본 AI 이미지(빈 구단주 의자, 실제 경기장 아님)에 움직임. 가입금(입장료 아님) · 범위 숫자 안 씀 · NFL 비교 없음(메모리)
# 「일화·이화」는 逸話로 들릴 수 있어 「첫 방송·다음 화」. 2.1% → 8.6% 는 「그 네 배가 넘었어」(8.6 ÷ 2.1 = 4.1)
# 가벼운 웃음 포인트: 같은 말을 세 번 했어 — 그래서, 얼마인데?
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), 'img', n)
shorts.HEAD = ('원더독스 구단 창단 비용', '가입금 20억, 해마다 70억')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 그린 도해 · 발행글 기준')
CHAIR = 'video:' + os.path.join(BASE, 'hf_chair.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=CHAIR, z0=1.0, z1=1.05, label='AI 생성 이미지 · 실제 경기장 아님',
         call=[(0.4, '빈 구단주 자리', WHITE), (3.0, '그래서, 얼마인데?', YEL)], sfx=[(3.0, 'ding')],
         cap='원더독스 첫 방송을 보다가, 같은 말을 세 번 했어. 그래서, 얼마인데?'),
    dict(D, media=P('D9_five_conditions.png'), **DG, call=[(0.6, '프로 팀 조건 다섯', YEL)],
         cap='제작진이 말한 프로 팀 조건은 다섯이야. 운영사무국·연고지·기업 관중 동원력·경기력. 그중 나머지 넷을 먹여 살리는 건, 세 번째 칸이야.'),
    dict(D, media=P('D1_entry_fee.png'), **DG, call=[(0.6, '가입금 20억', YEL)],
         cap='먼저 리그에 들어갈 때 내는 가입금이 20억. 페퍼저축은행이 창단하면서 냈던 금액이야.'),
    dict(D, media=P('D2_yearly_gap.png'), **DG, call=[(0.6, '쓰는 돈 70억 · 버는 돈 3.6억', YEL)],
         cap='들어온 뒤가 진짜야. 해마다 70억을 쓰는데, 구단이 스스로 버는 중계권 몫은 3.6억 정도야.'),
    dict(D, media=P('D3_broadcast_scale.png'), **DG, call=[(0.6, '야구 약 99억 · 배구 3.6억', YEL)],
         cap='야구는 달라. 구단당 중계권 수입이 99억쯤이라, 운영비를 크게 덜어 줘. 배구는 그 빈자리를 모회사가 메우고.'),
    dict(D, media=P('D5_pepper_timeline.png'), **DG, call=[(0.6, '페퍼 → 수퍼스', YEL)],
         cap='그래서 모기업이 아프면 구단이 바로 아파. 페퍼저축은행은 3년 내리 손실을 냈고, 결국 배구단을 넘겼어.'),
    dict(D, media=P('D13_profit_ratio.png'), **DG, call=[(0.6, '기존 2.1% 이하 · 페퍼 8.6%', YEL)],
         cap='그러니 볼 건, 운영비를 모기업 순이익으로 나눈 비율이야. 기존 구단은 많아야 2.1%였는데, 페퍼는 창단 때 그 네 배가 넘었어.'),
    dict(D, media=P('D10_deadline.png'), **DG, call=[(0.6, '시한 12월 27일', YEL)],
         cap='방송 속 시한은 12월 27일. 내가 역산해 보니, 그달 초엔 구단주가 정해져야 해.'),
    dict(D, media=CHAIR, z0=1.05, z1=1.0, label='AI 생성 이미지 · 실제 경기장 아님',
         cap='다음 화에 회사 이름이 나오면, 축하보다 먼저 순이익부터 찾아봐. 너는 어디가 나올 것 같아?'),
], BASE, 'WD')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'WD', 'wonderdogs_cost.mp4')
