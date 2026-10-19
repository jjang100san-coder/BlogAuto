# 런던 대영박물관 도슨트 후기 클립 — 새 틀 시험 2/5 (발행 10/10 12:00, logNo 224396368157)
# 실행: python clipBM.py stills / python clipBM.py → out\british_museum_v2.mp4
# 사진: 2024-03-05 오전 직접 찍은 것. 관람객 얼굴이 크게 나온 컷(로제타석 앞 112148·113608)은 뺐다. 업체 이름은 쓰지 않는다
# 10/11 사용자 두 번 지적 → 이야기 순서(클립 지침 3-5 연결성):
#   궁금증(무료인데 4만원) → 나(박물관 싫어함) → 선택(그래서 설명해 줄 사람 = 도슨트 값) → 경험(그런데 설명은 기억 안 남 / 대신 목소리)
# 10/11 사용자: 「30분 전인데 왜 보안검색 때문?」 → 미팅은 입구(보안검색 뒤) → 입장 줄이 길다 → 30분 전 줄 서기 순서로
#   → 깨달음(알고 보니 방식) → 결론(그러니까 읽어 줄 사람을 산 값) → 팁 묶음(혹시 갈 거면: 30분 전 · 그레이트 코트) → 질문
#   실용 팁은 이야기 중간에 끼우지 않고 결론 뒤 「혹시 갈 거면」으로 묶는다
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.dirname(BASE)
shorts.HEAD = ('무료 박물관에', '4만원 낸 이유')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)

NUM_OK = ('2024.03.05', '10:18', '11:37', '10:48')   # 사진 촬영 날짜·시각(파일 이름 = 촬영 기록), 발행본 본문엔 없음
SCENES = prep([
    dict(D, media='video:' + os.path.join(BASE, 'hf_court.mp4'), z0=1.0, z1=1.06, label='2024.03.05 · 대영박물관',
         call=[(0.4, '입장 무료', WHITE), (1.9, '그런데 4만원', YEL)], sfx=[(0.4, 'ding'), (1.9, 'ding')],
         cap='대영박물관은 입장이 무료야. 그런데 나는 4만원을 냈어.'),
    dict(D, media=os.path.join(PH, '20240305_101858.jpg'), z0=1.0, z1=1.1, label='2024.03.05 10:18',
         cap='솔직히 나는 박물관을 안 좋아해. 십 분쯤 지나면 다리부터 아파 와.'),
    dict(D, media=os.path.join(PH, '20240305_104806.jpg'), z0=1.0, z1=1.1, label='2024.03.05 10:48',
         call=[(0.5, '설명해 줄 사람', WHITE), (2.6, '도슨트 2시간 30분', YEL)], sfx=[(2.6, 'ding')],
         cap='그래서 이번엔 설명해 줄 사람을 붙였어. 4만원은 입장료가 아니라 도슨트 설명 값이야.'),
    dict(D, media=os.path.join(PH, '20240305_113710.jpg'), z0=1.0, z1=1.1, label='2024.03.05 11:37',
         cap='그런데 로제타석도, 이집트관 석상도 봤는데, 무슨 설명이었는지는 잘 기억이 안 나.'),
    dict(D, media=os.path.join(PH, '20240305_110348.jpg'), z0=1.0, z1=1.12, focus=(0.5, 0.4), label='이집트관',
         call=[(0.5, '대신 목소리', YEL)], sfx=[(0.5, 'ding')],
         cap='대신 확실히 기억나는 건 목소리야. 어디에 강약을 주고, 어디서 감정을 실을지, 정확히 아는 말투였어.'),
    dict(D, media=os.path.join(PH, '20240305_122832.jpg'), cx=0.85, z0=1.0, z1=1.1, focus=(0.6, 0.5), label='파르테논 마블',
         cap='알고 보니 박물관이 싫었던 게 아니라, 정보가 들어오는 방식이 지루했던 거였어.'),
    dict(D, media=os.path.join(PH, '20240305_123458.jpg'), z0=1.15, z1=1.0, label='그레이트 코트',
         call=[(0.5, '이야기를 들려줄 사람', YEL)], sfx=[(0.5, 'ding')],
         cap='그러니까 4만원은 입장료가 아니라, 작품 이야기를 들려줄 사람을 산 값이야.'),
    dict(D, media=os.path.join(PH, '20240305_101833.jpg'), z0=1.05, z1=1.15, label='개관 전 앞마당',
         call=[(0.5, '혹시 갈 거면', WHITE), (1.8, '보안검색 마치고 미팅', WHITE), (5.0, '30분 전 도착', YEL)],
         cap='혹시 갈 거면, 미팅은 박물관 입구에서 하는데, 보안검색까지 마치고 가야 해. 그런데 입장 줄이 길어서, 30분 전엔 도착해야 안 늦어.'),
    dict(D, media=os.path.join(PH, '20240305_123458.jpg'), z0=1.0, z1=1.12, focus=(0.5, 0.35), label='그레이트 코트',
         call=[(0.6, '고개를 들어', WHITE)],
         cap='그레이트 코트에선 꼭 고개를 들어. 삼각형 유리 지붕이 광장 전체를 덮고 있어.'),
    dict(D, media='video:' + os.path.join(BASE, 'hf_court.mp4'), z0=1.08, z1=1.0, label='2024.03.05 · 대영박물관',
         cap='너도 안 맞는다고 생각했던 게, 사실은 방식 문제였던 적 있어? 댓글로 알려줘.'),
], BASE, 'BM')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'BM', 'british_museum_v2.mp4')
