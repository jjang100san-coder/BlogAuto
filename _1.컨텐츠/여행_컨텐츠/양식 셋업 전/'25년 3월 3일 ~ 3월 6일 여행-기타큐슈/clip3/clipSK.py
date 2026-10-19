# 사쿠라지마 페리·유노히라 전망대 클립 (발행 10/15 07:10, logNo 224408212852 — 일본-규슈, 기타큐슈 3편)
# 실행: python clipSK.py stills / python clipSK.py → out\sakurajima_ferry.mp4
# 직접 찍은 사진만(AI 없음, 크레딧 0). 흐린 날 사진 그대로
# 사람이 든 컷은 뺐다 — 표지석은 사람이 없는 왼쪽만 잘라냄(yunohira_sign_crop), 배 안 운전 컷은 앞차 번호판 모자이크·룸미러 흐림(ferry_drive_masked)
# 글에 없는 장면(옆 차 강아지, 야생마 사진)은 넣지 않는다
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), n)
H = lambda n: os.path.join(BASE, n)
shorts.HEAD = ('사쿠라지마 페리', '차를 싣고 15분')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
PH = dict(label='직접 찍은 사진', call_top=True)
NUM_OK = ()

SCENES = prep([
    dict(D, media=P('1741363659083.jpg'), z0=1.0, z1=1.12, **PH,
         call=[(0.4, '차를 싣고 배를 탔어', WHITE), (3.4, '15분 뒤 건너편', YEL)], sfx=[(3.4, 'ding')],
         cap='차를 몰고, 그대로 배 안으로 들어갔어. 그리고 15분 뒤에, 다른 쪽 육지에 내렸지.'),
    dict(D, media=H('ferry_drive_masked.jpg'), z0=1.0, z1=1.1, label='직접 찍은 사진 · 번호판 가림', call_top=True,
         call=[(0.6, '예약도 표도 없이', YEL)],
         cap='줄을 서서 차를 몰고 들어가면 끝이야. 예약도 없고, 요금은 내릴 때 내.'),
    dict(D, media=H('yunohira_sign_crop.jpg'), z0=1.0, z1=1.1, **PH, call=[(0.6, '유노히라 전망대 373m', YEL)],
         cap='배를 타기 전엔, 유노히라 전망대에 들렀어. 표고 373m, 일반인이 올라갈 수 있는 가장 높은 곳이야.'),
    dict(D, media=H('yunohira_sign_crop.jpg'), z0=1.15, z1=1.3, **PH, call=[(0.6, '구름이 정상을 덮었다', YEL)],
         cap='화산 표면은 회색인데, 이날은 구름이 정상을 덮어서, 분화구는 못 봤어.'),
    dict(D, media=H('ferry_corridor_masked.jpg'), z0=1.0, z1=1.1, label='직접 찍은 사진 · 사람 가림', call_top=True, call=[(0.6, '배 안에 우동 가게', YEL)],
         cap='차를 세워 두고 위층에 올라가 보니, 배 안에 우동 가게가 있더라.'),
    dict(D, media=P('1741363659708.jpg'), z0=1.0, z1=1.08, **PH, call=[(0.6, '15분 안에 먹는 우동', YEL)],
         cap='15분짜리 배에서 우동이라니. 하지만 여기선, 그게 유명한 거래.'),
    dict(D, media=P('1741363659283.jpg'), z0=1.1, z1=1.0, **PH, call=[(0.6, '갑판 위 자판기와 의자', YEL)],
         cap='갑판으로 나가면 바람은 찬데, 시야가 트여서, 건너편 가고시마 시내가 다가와.'),
    dict(D, media=P('1741363659083.jpg'), z0=1.15, z1=1.0, **PH, call=[(0.6, '차까지 약 2,500엔', YEL)], sfx=[(0.6, 'ding')],
         cap='차 한 대에 세 명, 합쳐서 약 2,500엔이었어. 육로로 돌아가는 걸 생각하면, 싸다고 느꼈지.'),
    dict(D, media=P('1741363659916.jpg'), z0=1.0, z1=1.1, **PH,
         cap='분화구도 야생마도 못 본 날인데, 이 15분이 다 덮더라. 너는 여행에서, 계획에 없던 게 제일 좋았던 적 있어?'),
], BASE, 'SK')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'SK', 'sakurajima_ferry.mp4')
