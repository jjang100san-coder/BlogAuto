# 애드포스트 승인 열흘 수익 클립 (발행 10/12 10:16, logNo 224438742081)
# 실행: python clipAD.py stills / python clipAD.py → out\adpost_10days.mp4
# 카드 4장·지급 보고서·수입 그래프 캡처는 발행본 그대로. 첫 장면은 발행본 AI 이미지(img1, 특정 인물 아님)에 움직임
# 노출 수·클릭 수·클릭률은 쓰지 않는다(게재 제한 사유 — 메모리 adpost-stats-confidential). 수입·조회수·유입 비율만
# 가벼운 웃음 포인트: 천 원도 안 된 날 바로 다음 날 4천 원 · 지금 속도면 한참 걸려
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
shorts.HEAD = ('애드포스트 승인 열흘', '22,697원 · 받은 돈 0원')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
CARD = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 표 · 발행글 기준')
CAP = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='애드포스트 화면 캡처')
COIN = 'video:' + os.path.join(BASE, 'hf_coins.mp4')
NUM_OK = ('2만', '2천', '4천', '12만', '5천', '20만', '5만')

SCENES = prep([
    dict(D, media=COIN, z0=1.0, z1=1.05, label='AI 생성 이미지 · 특정 인물 아님',
         call=[(0.4, '승인 열흘 수입 22,697원', WHITE), (4.2, '받은 돈 0원', YEL)], sfx=[(4.2, 'ding')],
         cap='블로그 애드포스트 승인 열흘, 얼마나 벌었을까? 2만 2천 원 남짓이야. 그런데 아직, 한 푼도 못 받았어.'),
    dict(D, media=P('card1_income_10days.png'), **CARD,
         cap='날마다 보면 들쭉날쭉해. 가장 적은 날은 천 원도 안 됐는데, 바로 다음 날은 4천 원이 넘었어.'),
    dict(D, media=P('card2_views_vs_income.png'), **CARD,
         cap='재밌는 건 따로 있어. 조회수가 제일 높던 날, 돈은 두 번째였어. 일 등은 그 전날이었고.'),
    dict(D, media=P('capture_income_graph.png'), **CAP,
         cap='왜 그런지는 나도 몰라. 광고 종류나 성과에 따라, 배분이 달라진다고만 적혀 있어서, 열흘치로 단정하진 않을게.'),
    dict(D, media=P('card3_inflow_2weeks.png'), **CARD,
         cap='그럼 다들 어디서 왔냐면, 대부분 블로그 홈 화면이야. 검색으로 들어온 건 여섯 명 중 한 명꼴이었어.'),
    dict(D, media=os.path.join(BASE, 'balance_crop.png'), **CAP,
         call=[(2.4, '5만 원부터 고를 수 있음', WHITE), (5.0, '내가 정한 건 20만 원', YEL)],
         cap='그럼 왜 아직 못 받았냐고? 최소 지급액은 5만 원부터 고를 수 있는데, 나는 20만 원으로 정해 뒀거든. 지금 속도면, 한참 걸려.'),
    dict(D, media=P('card4_balance.png'), **CARD,
         cap='그리고 입금되는 순간부터 세금이 붙어. 1년 합계가 12만 5천 원을 넘으면, 그해 받은 돈 전부가 대상이야. 첫 지급이 20만 원이니까, 처음부터 걸리는 거지.'),
    dict(D, media=COIN, z0=1.05, z1=1.0, label='AI 생성 이미지 · 특정 인물 아님',
         cap='다음엔 이번 달 전체를 같은 표로 적을게. 너는 블로그 수익, 공개하는 편이야? 아니면 조용히 두는 편이야?'),
], BASE, 'AD')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'AD', 'adpost_10days.mp4')
