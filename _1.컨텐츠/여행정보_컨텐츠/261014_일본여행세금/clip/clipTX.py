# 일본 출국세 클립 (발행 10/15 11:59, logNo 224442406997 — 정보, 일본 여행 세금)
# 실행: python clipTX.py stills / python clipTX.py → out\japan_tax.mp4
# 첫 장면은 발행본 AI 썸네일(실내 낮 공항, 실제 공항 아님)에 hailuo 움직임 — 맑은 낮 톤 그대로(10/13 톤 다양성)
# 그림·캡처는 발행본 것을 fit='contain'(그림 위 큰 글 · 아래 말자막)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
shorts.HEAD = ('일본 출국세 3,000엔', '내 항공권은 얼마 늘었나')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 발행글 기준')
SHOT = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='예약 화면 캡처')
MOV = 'video:' + os.path.join(BASE, 'hf_kiosk.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.05, label='AI 생성 이미지 · 실제 공항 아님',
         call=[(0.4, '출국세 1,000엔 → 3,000엔', WHITE), (3.6, '내 표는 얼마 늘었을까?', YEL)], sfx=[(3.6, 'ding')],
         cap='일본 출국세가, 1,000엔에서 3,000엔으로 올랐어. 그럼 내 항공권 세금은, 원화로 얼마나 늘었을까?'),
    dict(D, media=P('ig_departure.png'), **DG, call=[(0.6, '7월 1일 출국분부터', YEL)],
         cap='기준은 표를 산 날이 아니라, 일본을 떠나는 날이야. 마일리지 항공권에도 붙어.'),
    dict(D, media=P('ke_fare_2027_kix.jpg'), **SHOT, call=[(0.6, '같은 노선 · 같은 1월', YEL)],
         cap='노선도, 달도 같은 마일리지 표 두 장을, 나란히 놓고 봤어.'),
    dict(D, media=P('chart_tax_stack.png'), **DG, call=[(0.6, '출국세 줄 +15,800원', YEL)],
         cap='출국세 줄은 9,500원에서 25,300원으로 뛰었어. 대신 공항 시설 사용료와 보안 요금은, 오히려 줄었고.'),
    dict(D, media=P('card_conclusion.png'), **DG, call=[(0.6, '합계는 +11,800원', YEL)], sfx=[(0.6, 'ding')],
         cap='그래서 세금 합계는, 68,100원에서 79,900원. 늘어난 건 11,800원이었어.'),
    dict(D, media=P('ig_refund.png'), **DG, call=[(0.6, '11월 1일부터 면세 방식 바뀜', YEL)],
         cap='정작 1월 여행에서 챙길 건 따로 있었어. 11월부터 면세는, 공항에서 확인받고 돌려받아.'),
    dict(D, media=P('ig_map.png'), **DG, call=[(0.6, '숙박세는 도시마다', YEL)],
         cap='그리고 숙박세. 도시마다 달라서, 교토는 다섯 구간이 됐어.'),
    dict(D, media=P('gero_rate.jpg'), **SHOT, call=[(0.6, '숙박세는 현장 결제', YEL)],
         cap='게로 온천 료칸 확인서엔, 숙박세가 빠져 있었어. 둘이서 400엔을, 숙소에 들어갈 때 따로 내.'),
    dict(D, media=P('takayama_rate.jpg'), **SHOT, call=[(0.6, '1인 9,975엔 → 100엔 구간', YEL)],
         cap='다카야마 호텔 방값은 19,950엔. 둘이 나누면 1인 9,975엔이라, 숙박세는 100엔 구간이야.'),
    # 10/15 사용자 「100엔이라 했는데 화면엔 300엔 — 혼돈」 → 글처럼 계산 500엔 vs 화면 300엔을 따로 한 장면
    dict(D, media=P('takayama_rate.jpg'), **SHOT, call=[(0.6, '계산 500엔 · 화면 300엔', YEL)],
         cap='두 사람 숙박세 200엔에, 온천 입탕세까지 하면 500엔. 하지만 화면엔 300엔이라, 1월에 영수증으로 확인할게.'),
    dict(D, media=P('card_jan_trip.png'), **DG, call=[(0.6, '출국세 · 면세 · 숙박세', YEL)],
         cap='출국세는 이미 냈고, 면세는 공항 순서, 숙박세는 숙소에서. 너는 1월에, 일본 어디 가?'),
], BASE, 'TX')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'TX', 'japan_tax.mp4')
