# 2027년 10월 연휴 마일리지 복귀편 클립 — 새 틀 시험 5/5 (발행 10/10 06:50, logNo 224436602778)
# 실행: python clipRT.py stills / python clipRT.py → out\holiday_return_v2.mp4
# 10/11 사용자: 「복귀편을 열린 / 날 밤에」 호흡이 끊긴다 → 의미 덩어리마다 문장을 끊어 7장면으로(지침 6-1-2)
# 장면은 전부 AI(실제 공항 사진 아님) — 「AI 생성 이미지」 표시. 숫자는 발행본 그대로(10/9 밤 한 시점)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(BASE)
shorts.HEAD = ('2027 연휴 복귀편', '유럽 0석은 파리뿐')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AIL = 'AI 생성 이미지 · 실제 공항 아님'

SCENES = prep([
    dict(D, media='video:' + os.path.join(BASE, 'hf_gate.mp4'), z0=1.0, z1=1.06, label=AIL,
         call=[(0.5, '2027 10월 연휴', YEL)],
         cap='2027년 10월 연휴 복귀편. 예약이 열린 날 밤에, 하나씩 조회해 봤어.'),
    dict(D, media=os.path.join(BASE, 'ai_paris.png'), z0=1.0, z1=1.1, label='AI 생성 이미지',
         call=[(0.5, '유럽 20편 중 2편', WHITE), (2.4, '14시 40분 편 0석', YEL)], sfx=[(2.4, 'ding')],
         cap='유럽에서 0석은 파리뿐이었어. 3일과 4일, 같은 오후 편이야.'),
    dict(D, media=os.path.join(BASE, 'ai_paris.png'), z0=1.1, z1=1.2, focus=(0.55, 0.45), label='AI 생성 이미지',
         call=[(0.5, '20시 35분 편 9석 이상', YEL)],
         cap='4일 저녁 비행기는, 9석 이상 남아 있었어.'),
    dict(D, media=os.path.join(BASE, 'ai_asia.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.5, '아시아 96편 · 미주 42편', WHITE), (2.2, '0석 없음', YEL)], sfx=[(2.2, 'ding')],
         cap='아시아와 미주·대양주는 달랐어. 일반석 0석이 하나도 없었거든.'),
    dict(D, media=os.path.join(UP, 'ai_biz_empty_20261009.png'), z0=1.0, z1=1.1, label='AI 생성 이미지',
         call=[(0.8, '유럽 프레스티지 20편 중 3편', WHITE)],
         cap='대신 유럽 프레스티지는 거의 남아 있지 않았어.'),
    # 종합 카드 4장 — 음성 없이 3초씩(10/11 사용자: 「그래서 결론으로 뭐가 남았다는 거야?」) · make_cards.py
    dict(D, media=os.path.join(BASE, 'card_eu.png'), z0=1.0, z1=1.0, whole=True, narr=None, dur=3.0, label='직접 만든 표'),
    dict(D, media=os.path.join(BASE, 'card_asia.png'), z0=1.0, z1=1.0, whole=True, narr=None, dur=3.0, label='직접 만든 표'),
    dict(D, media=os.path.join(BASE, 'card_am.png'), z0=1.0, z1=1.0, whole=True, narr=None, dur=3.0, label='직접 만든 표'),
    dict(D, media=os.path.join(BASE, 'card_total.png'), z0=1.0, z1=1.0, whole=True, narr=None, dur=3.0, label='직접 만든 표'),
    dict(D, media=os.path.join(BASE, 'ai_desk.png'), z0=1.0, z1=1.12, label='AI 생성 이미지', narr=5,
         call=[(1.6, '하루 사이 14편', YEL)], sfx=[(1.6, 'ding')],
         cap='그리고 하루 전에 확인한 가는 편을 다시 조회해 봤어. 14편이 바뀌어 있었어.'),
    dict(D, media='video:' + os.path.join(BASE, 'hf_gate.mp4'), z0=1.08, z1=1.0, label=AIL, narr=6,
         cap='남은 좌석은 볼 때마다 달라져. 너는 가는 편부터 잡아? 아니면 오는 편부터 잡아?'),
], BASE, 'RT')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'RT', 'holiday_return_v2.mp4')
