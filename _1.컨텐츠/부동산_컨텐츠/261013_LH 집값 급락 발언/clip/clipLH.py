# 「LH사장 집값 | 서울에서 2년 기다린 사람은 15.7% 싸게 샀고, 그 뒤엔 26.1% 비싸졌어」 클립 (발행 10/18 10:00, logNo 224443149303 — 부동산)
# 실행: python make_html.py → python clipLH.py → out\lh_wait.mp4
# 10/18 결: 마스터 5-8 양식 움직이는 인포그래픽(clipkit/html_anim.py) + 10/16 결(한 장면 하나·장 카드·요약 장 five)
# 숫자는 발행본 그대로. 누구 편도 아님 — 말과 숫자 대 보기. 첫 장면은 발행본 AI 삽화(신도시 내려다보는 두 사람, 뒷모습)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('기다리면 손해 안 본다?', '지난 거래에 대 봤다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 공개 통계')
AI = 'AI 생성 이미지 · 실제 장소 아님'
MOV = 'video:' + os.path.join(BASE, 'hf_hook.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.06, label=AI, call_top=True, call=[(0.4, '지금 살까, 기다릴까', WHITE)],
         cap='지금 집을 살까, 신도시가 다 들어설 때까지 기다릴까?'),
    dict(D, media=A('quote'), **AN, call=[(0.4, 'LH 사장의 말', YEL)],
         cap='LH 사장은, 지금 안 사도 손해 보지 않는다고 했어. 이 말을 지난 거래에 대 봤어.'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '판정 하나', YEL)],
         cap='2021년 고점에서, 2년 기다린 사람은 어땠을까?'),
    dict(D, media=A('seoul'), **AN, call=[(0.4, '서울 25개 구', YEL)], sfx=[(3.5, 'ding')],
         cap='서울에선 15.7% 싸게 샀어. 하지만 그 값보다, 지금은 26.1% 비싸.'),
    dict(D, media=A('regions'), **AN, call=[(0.4, '언제·어디냐', YEL)],
         cap='경기·인천은 그 뒤 조금 올랐고, 지방은 더 내렸어. 같은 말이, 곳마다 다르게 맞았던 거야.'),
    dict(D, media=A('interest'), **AN, call=[(0.4, '이자까지 넣으면', YEL)],
         cap='게다가 기다린 사람은 금리가 더 높았어. 이자를 넣으면, 월 상환액 차이는 3.2%뿐이야.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '판정 둘', YEL)],
         cap='그럼 지금은 어떨까? 사장의 말을, 다섯 칸으로 쪼개 봤어.'),
    dict(D, media=A('supply'), **AN, call=[(0.4, '주문은 늘고 도착은 줄고', YEL)],
         cap='서울은 올해 허가와 착공이 40% 넘게 늘었는데, 입주는 19.1% 줄었어.'),
    # 요약 장(10/16 「이미지도 요약 형태로」)
    dict(D, media=A('five'), **AN, call=[(0.4, '다섯 칸, 한 장으로', YEL)],
         cap='공급이 늦게 온다는 건 통계 그대로고, 대출과 금리는 반쯤 맞아. 급락은, 지금 지표로는 안 보여.'),
    dict(D, media=A('roads'), **AN, call=[(0.4, '둘 다 2028년을 본다', YEL)],
         cap='공급돼도 안 떨어진다는 해설도, 같은 2028년을 봐. 갈리는 건 그때까지의 길이야.'),
    dict(D, media=A('cal'), **AN, call=[(0.4, '내 달력부터', YEL)],
         cap='누구 말이 맞을지는 2028년이 알려 줄 거야. 너는 언제 집이 필요해?'),
], BASE, 'LH')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'LH', 'lh_wait.mp4')
