# 부캉이 뜻 클립 (발행 10/14 22:52, logNo 224441908299 — 구구절절, 도시 야생동물 이입)
# 실행: python clipBK.py stills / python clipBK.py → out\bukangi.mp4
# 첫·끝 장면은 발행본 AI 썸네일(캐릭터 일러스트, 실제 동물 아님)에 hailuo 움직임 — 빛은 원본 그대로 맑은 낮 하늘색(10/13 톤 다양성)
# 도해는 발행본 img\ 그대로 fit='contain'(그림 위 큰 글 · 아래 말자막)
# 할 일 하나는 훈계형 대신 거리감 문장(메모리 todo-no-lecturing-tone)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), 'img', n)
shorts.HEAD = ('부캉이 뜻, 왜 이름을 붙일까', '논문 117편으로 파 봤다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 발행글 기준')
MOV = 'video:' + os.path.join(BASE, 'hf_three.mp4')
AI = 'AI 생성 캐릭터 · 실제 동물 아님'
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.05, label=AI,
         call=[(0.4, '상어가 귀엽나?', WHITE), (3.4, '24일 동안 134만 명', YEL)], sfx=[(3.4, 'ding')],
         cap='상어가 귀엽나? 큰 눈도 둥근 뺨도 없는데, 24일 동안 134만 명이 보러 갔어.'),
    dict(D, media=P('D1_three_cases.png'), **DG, call=[(0.6, '부캉이 · 온처니 · 푸바오', YEL)],
         cap='부산 북항 수로에 들어온 흑상어가, 부캉이야. 항구 이름에서 따온 거지.'),
    dict(D, media=P('D2_visitor_curve.png'), **DG, call=[(0.6, '연휴마다 계단처럼', YEL)],
         cap='발견 다음 날 8,000명이 왔고, 추석 연휴 나흘엔 48만 3천 명이 몰렸어.'),
    dict(D, media=P('D3_cute_lane.png'), **DG, call=[(0.6, '귀여움 길은 막혔다', YEL)],
         cap='귀여운 얼굴을 보면 돌보고 싶어져. 하지만 상어는, 그 길이 막혀 있어.'),
    dict(D, media=P('D4_four_conditions.png'), **DG, call=[(0.6, '이름 · 사연 · 어긋난 자리 · 같이 보기', YEL)],
         cap='논문 117편을 찾아봤더니, 네 칸이 남았어. 이름, 사연, 어긋난 자리, 그리고 같이 보기.'),
    dict(D, media=P('P1_name_switch.png'), **DG, call=[(0.6, '이름표 단 한 마리만 75.9%', YEL)],
         cap='송아지 실험에선, 이름표를 단 한 마리일 때만, 기부가 75.9%로 올라갔어.'),
    dict(D, media=P('P3_shark_two_headlines.png'), **DG, call=[(0.6, '공격 말고 곤경', YEL)],
         cap='상어 기사는 보통, 공격으로 시작해. 부캉이는 달랐어. 수로를 못 빠져나가는 쪽이었지.'),
    dict(D, media=P('P4_resident_or_intruder.png'), **DG, call=[(0.6, '주민 아니면 침입자', YEL)],
         cap='도시에 나타난 동물은, 주민이 되거나 침입자가 돼. 이름과 사연이, 어느 쪽에 붙느냐에 달렸어.'),
    dict(D, media=P('P2_tamachan_card.png'), **DG, call=[(0.6, '물범에게 주민표', YEL)],
         cap='2003년 요코하마에선, 강에 나타난 바다물범에게, 특별 주민표까지 내줬어.'),
    dict(D, media=P('D11_shadow.png'), **DG, call=[(0.6, '너무 가까운 사랑', YEL)],
         cap='하지만 마음이 너무 가까이 가면, 그 한 마리가 다쳐. 부캉이는 밤에 비춘 랜턴에, 주둥이를 다친 것으로 보인대.'),
    dict(D, media=P('D12_todo.png'), **DG, call=[(0.6, '자리만 한 걸음 뒤로', YEL)],
         cap='이름도 마음도 그대로 두고, 자리만 한 걸음 뒤로. 너는 부캉이, 직접 가 봤어?'),
], BASE, 'BK')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'BK', 'bukangi.mp4')
