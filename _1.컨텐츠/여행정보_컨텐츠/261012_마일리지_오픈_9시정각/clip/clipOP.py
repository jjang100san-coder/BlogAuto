# 마일리지 항공권 오픈일 클립 (발행 10/12 11:05, logNo 224438797521)
# 실행: python clipOP.py stills / python clipOP.py → out\mileage_open_0901.mp4
# 인포그래픽은 발행본 그대로(직접 만든 그림). 첫 장면은 발행본 AI 이미지(실제 공항 사진 아님)에 움직임
# 「0석」은 소리로 「매진」, 화면 숫자는 발행본 그대로 · 연휴라 → 「연휴 기간이라」(발음 장부)
# 가벼운 웃음 포인트: 정각에 딱 눌렀어 → 결과는 접근 거부 · 사십 분 가만히 있으면 알아서 로그아웃
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
shorts.HEAD = ('마일리지 좌석 오픈 9시', '정각엔 거부, 9시 1분엔 열림')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
INFO = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 발행글 기준')
SHUT = 'video:' + os.path.join(BASE, 'hf_shutter.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=SHUT, z0=1.0, z1=1.05, label='AI 생성 이미지 · 실제 공항 사진 아님',
         call=[(0.4, '09:00 정각 클릭', WHITE), (3.4, '결과는 접근 거부', YEL)], sfx=[(3.4, 'ding')],
         cap='마일리지 좌석이 아침 9시에 열린다길래, 정각에 딱 눌렀어. 결과는, 접근 거부.'),
    dict(D, media=P('info_0900_3steps_20261012.png'), **INFO,
         cap='그 전엔 달력에서 날짜가 안 골라져. 정각 첫 검색은 이틀 연속 거부였고, 1분 뒤 같은 창에서 다시 하니 열려 있었어.'),
    dict(D, media=P('open_timeline_20261012.png'), **INFO,
         cap='단, 미리 연타하는 건 금물이야. 1분 동안 12번 조회했다가, 두 시간 가까이 막혔거든.'),
    dict(D, media=P('info_holiday_eu0_20261012.png'), **INFO,
         cap='그럼 휴일 날짜는 얼마나 버틸까? 2027년 개천절 연휴 출발일, 열린 지 두 시간 만에, 유럽행 비즈니스 9편이 전부 매진이었어.'),
    dict(D, media=P('info_holiday_vs_weekday_20261012.png'), **INFO,
         cap='연휴 기간이라서 그런 것도 아니었어. 평일도 열린 지 10분 만에, 14편 중 1편만 남았어.'),
    dict(D, media=P('open_grid_europe_20261012.png'), **INFO,
         cap='반대로 일반석은 급하지 않았어. 대부분 9석 넘게 남아 있었거든. 서두를 건 비즈니스 하나야.'),
    dict(D, media=P('info_checklist_20261012.png'), **INFO,
         cap='그래서 순서는 이래. 정각 조금 전에 로그인하고, 날짜를 고른 다음, 9시 1분에 검색해.'),
    dict(D, media=P('info_checklist_20261012.png'), z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 그림 · 발행글 기준',
         call=[(0.5, '40분 가만히 있으면 로그아웃', YEL)],
         cap='로그인은 너무 일찍 하지 마. 40분 동안 가만히 있으면, 알아서 로그아웃되거든.'),
    dict(D, media=SHUT, z0=1.05, z1=1.0, label='AI 생성 이미지 · 실제 공항 사진 아님',
         cap='너는 마일리지 좌석, 오픈 시간 맞춰서 잡아 본 적 있어?'),
], BASE, 'OP')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'OP', 'mileage_open_0901.mp4')
