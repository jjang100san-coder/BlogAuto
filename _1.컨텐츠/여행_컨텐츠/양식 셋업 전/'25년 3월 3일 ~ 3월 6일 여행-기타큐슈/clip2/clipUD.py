# 우도신궁 · 벳푸 빵집 클립 (발행 10/12 07:00, logNo 224408204465 — 기타큐슈 2편)
# 실행: python clipUD.py stills / python clipUD.py → out\udo_beppu.mp4
# 사진·영상은 직접 찍은 것(2025.03). 가게 이름은 클립에서 뺀다(빵집·라멘집). 영업시간 안내는 뒤에 비친 사람들을 잘라냄(sign_crop.jpg)
# 사람이 찍힌 참배로 사진(173727·173757)은 쓰지 않음. 해안은 현장 영상(20250303_173554) 앞 5초
# 발행본의 「해가 낮게 들어와 붉은 건물이 더 진하게」는 사진이 흐린 날이라 화면과 어긋나서 대본에서 뺐다 — 「사람이 거의 없었다」만
# 가벼운 웃음 포인트: 빵 먹자마자 라멘이라 배가 좀 그랬어
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
here = lambda n: os.path.join(BASE, n)
shorts.HEAD = ('바위 동굴 속 신사', '그날 주인공은 빵집')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
L = '2025.03 직접 찍음'
CAVE = 'video:' + here('hf_cave.mp4')
NUM_OK = ('2025.03',)

SCENES = prep([
    dict(D, media=CAVE, z0=1.0, z1=1.05, label=L + ' · 움직임 AI',
         call=[(0.4, '동굴 속에 신사가 통째로', WHITE), (4.0, '본전 전체가 동굴 속', YEL)], sfx=[(4.0, 'ding')],
         cap='바위 천장 아래에 신사가 통째로 들어간 곳, 본 적 있어? 입구에 문만 세운 게 아니야. 본전 전체가 동굴 속이야.'),
    dict(D, media=here('form_crop.jpg'), z0=1.0, z1=1.12, label=L,
         call=[(2.6, '그날의 주인공', YEL)],
         cap='그런데 그날 제일 기억에 남은 건 따로 있어. 동네 빵집에서 받아 적은, 이 주문서야.'),
    dict(D, media=P('1789093148578.jpg'), z0=1.0, z1=1.1, label=L,
         call=[(3.2, '비 와서 지옥 순례는 접음', WHITE)],
         cap='원래는 벳푸 지옥 순례를 돌 생각이었어. 그런데 야외를 계속 걷는 코스라, 비가 오락가락하니까 접었지. 대신 빵집 한 곳만 들렀어.'),
    dict(D, media=here('form_crop.jpg'), z0=1.15, z1=1.3, focus=(0.45, 0.55), label=L,
         call=[(0.5, '집지 않고 적어서 낸다', YEL)],
         cap='여긴 진열장에서 직접 집지 않아. 종이에 원하는 개수를 적어서 내면, 직원이 봉투에 담아 줘.'),
    dict(D, media=P('1789093148730.jpg'), z0=1.0, z1=1.12, label=L,
         call=[(0.5, '앙팡 110엔', YEL)], sfx=[(0.5, 'ding')],
         cap='앙팡 하나가 110엔인데, 반으로 갈라 보니까 이래. 빵보다 팥이 더 많아 보일 정도야.'),
    dict(D, media=here('sign_crop.jpg'), z0=1.0, z1=1.0, whole=True, label=L,
         call=[(0.5, '일요일 · 공휴일 휴무', YEL)],
         cap='다만 일요일과 공휴일엔 문을 닫아. 주말에 벳푸를 간다면, 토요일에 들러야 헛걸음이 없어.'),
    dict(D, media=P('20250303_135444.jpg'), z0=1.0, z1=1.1, label=L,
         call=[(2.4, '빵 다음 바로 라멘', WHITE)],
         cap='점심은 오이타로 넘어가서 해결했어. 빵을 먹자마자 라멘이라, 배가 좀 그랬어.'),
    dict(D, media='video:' + here('coast.mp4'), z0=1.0, z1=1.05, label=L,
         call=[(2.6, '오후 5시 반 도착', YEL)],
         cap='그리고 해안을 따라 미야자키까지 내려와서, 오후 5시 반에 우도신궁에 닿았어.'),
    dict(D, media=P('20250303_173531.jpg'), z0=1.0, z1=1.1, label=L,
         call=[(0.5, '사람이 거의 없었어', WHITE)],
         cap='늦게 도착한 게 오히려 좋았어. 사람이 거의 없어서, 붉은 건물과 바위를 천천히 볼 수 있었거든.'),
    dict(D, media=P('20250303_174123.jpg'), z0=1.05, z1=1.0, label=L,
         cap='결국 지옥 순례는 못 갔고, 지나가다 들른 빵집이 남았어. 너는 여행에서, 계획에 없던 곳이 더 오래 생각난 적 있어?'),
], BASE, 'UD')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'UD', 'udo_beppu.mp4')
