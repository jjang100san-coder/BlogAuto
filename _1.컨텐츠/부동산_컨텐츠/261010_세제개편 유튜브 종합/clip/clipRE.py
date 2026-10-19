# 8.3 부동산 세제개편 클립 (발행 10/11 07:30, logNo 224436974592)
# 실행: python clipRE.py stills / python clipRE.py → out\tax_reform.mp4
# 10/11 사용자: 「AI 삽화 기반으로 시청자가 정확히 인지할 수 있도록」 — 장면은 AI 삽화(글자 없음), 숫자는 장면 위 큰 글·카드(make_cards.py)
# 숫자는 발행본 그대로. 「400만 원 넘게」= 1,203.8만 − 774.7만(429.1만) · 세액공제·상한 적용 전 추산(발행본 표현)
# 녹음 전 검사(10/11): repeat_check · pron_book check 통과 — 대본 narration\RE\script.txt
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
a = lambda n: os.path.join(BASE, n)
shorts.HEAD = ('8.3 부동산 세제개편', '되돌린 건 3개뿐')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AIL = 'AI 생성 이미지 · 10/10 기준'
NUM_OK = ('400', '10/10')   # 400 = 1,203.8만 − 774.7만(429.1만)을 줄여 말함

SCENES = prep([
    dict(D, media='video:' + a('hf_hook.mp4'), z0=1.0, z1=1.05, label=AIL,
         call=[(0.3, '한 달 만에 뒤집혔다?', WHITE), (3.0, '바뀐 건 3개뿐', YEL)], sfx=[(3.0, 'ding')],
         cap='부동산 세제개편안이, 한 달 만에 뒤집혔다고? 나란히 놓고 보니, 바뀐 건 3개뿐이었어.'),
    dict(D, media=a('ai_empty.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.5, '집에 살지 않는 1주택', WHITE), (2.6, '종부세 3개', YEL)],
         cap='되돌린 건, 집에 살지 않는 1주택자의 종부세 항목 3개야.'),
    dict(D, media=a('card_back.png'), z0=1.0, z1=1.0, whole=True, label='직접 만든 표 · 10/10 기준',
         cap='기본공제 12억, 세부담 상한 150%, 그리고 부부가 함께 가진 집의 공제. 이 셋이야.'),
    dict(D, media=a('ai_living.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(3.0, '실거주 1주택 공제 12억 → 14억', YEL)], sfx=[(3.0, 'ding')],
         cap='나머지는 그대로 국회에 갔어. 실제로 사는 1주택 공제는, 12억에서 14억으로 올라가.'),
    dict(D, media=a('ai_coins.png'), z0=1.0, z1=1.12, label='AI 생성 이미지 · 세액공제·상한 적용 전 추산',
         call=[(0.5, '공제 12억이 돌아와도', WHITE), (5.0, '공시가 30억 · 2027년', WHITE), (6.4, '774.7만 → 1,203.8만 원', YEL)],
         sfx=[(6.4, 'ding')],
         cap='그래서 집에 살지 않는 1주택은, 공제가 돌아와도 종부세가 오를 수 있어. 공시가격 30억이면, 400만 원 넘게 늘어나는 추산이야.'),
    dict(D, media=a('ai_twohouse.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.5, '10월 1일부터 시행', WHITE), (4.2, '일시적 2주택 3년 → 2년', YEL)], sfx=[(4.2, 'ding')],
         cap='10월 1일부터 이미 시행된 것도 있어. 두 집이 모두 조정지역이면, 예전 주택을 파는 기한이, 3년에서 2년으로 줄었어.'),
    dict(D, media=a('ai_confused.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.5, '장기보유특별공제 10억', WHITE), (4.0, '= 공제받는 금액의 한도', YEL), (6.5, '비과세 기준 12억은 그대로', WHITE)],
         cap='가장 많이 헷갈린 건, 장기보유특별공제 10억이야. 양도세를 안 내는 기준이 아니라, 공제받는 금액의 상한이야.'),
    dict(D, media=a('ai_meeting.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.5, '종부세 · 양도세 = 국회 통과 전', WHITE), (3.4, '11월 조세소위', YEL)], sfx=[(3.4, 'ding')],
         cap='종부세와 양도세는, 아직 국회를 지나야 확정돼. 다음 단계는 11월 조세소위야.'),
    # 한눈에 정리 — 음성 없이(복귀편 종합 카드와 같은 방식, 10/11)
    dict(D, media=a('card_sum.png'), z0=1.0, z1=1.0, whole=True, narr=None, dur=4.0, label='직접 만든 표 · 10/10 기준 · 국회 통과 전'),
    # 끝맺음 — 10/11 사용자: 「나는 매수자. 매수자는 큰 영향 없음 → 매도자는 이럴 수 있다로」
    dict(D, media=a('ai_balcony.png'), z0=1.0, z1=1.08, label=AIL, narr=8,
         call=[(0.5, '살 사람 · 실거주 한 채', WHITE), (4.6, '공제 12억 → 14억', YEL)],
         cap='나는 집을 살 사람이야. 직접 들어가 지낼 한 채라면, 당장 크게 달라지는 건 없어. 공제는 오히려 14억으로 올라.'),
    dict(D, media=a('ai_handover.png'), z0=1.0, z1=1.08, label=AIL, narr=9,
         call=[(0.5, '파는 사람', WHITE), (2.4, '장기보유특별공제: 거주 기간 중심', YEL), (6.0, '다주택자 양도세 중과: 2027·2028년만 낮춤', WHITE)],
         cap='영향이 큰 건 파는 사람 쪽이야. 장기보유특별공제는 거주한 기간이 기준이 되고, 다주택자가 더 내는 양도세는, 2027년과 2028년에만 낮아져.'),
    dict(D, media='video:' + a('hf_hook.mp4'), z0=1.05, z1=1.0, label=AIL, narr=10,
         cap='너는 집을 사려는 쪽이야? 아니면 팔려는 쪽이야? 댓글로 알려줘.'),
], BASE, 'RE')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'RE', 'tax_reform.mp4')
