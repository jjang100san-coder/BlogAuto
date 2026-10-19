# 블로그 조회수 클립 — 새 틀 시험 4/5 (발행 10/10 10:13, logNo 224436919235)
# 실행: python clipBV.py stills / python clipBV.py → out\blog_views_v2.mp4
# 장면은 전부 AI(사진 재료 없음) — 「AI 생성 이미지」 표시. 숫자는 발행본 그대로(9월 통계)
# 10/11 사용자: 「영상만 보면 이게 그래서 뭔 소리야?」 → 블로그 용어를 풀어 쓴다
#   검색 유입 = 검색창에 쳐서 들어온 사람 / 홈판 = 네이버 앱 첫 화면에 뜨는 추천 글 / 16.88% = 열 명 중 두 명도 안 됨
#   「축구 글 없는 날 조회수가 뛰었다」는 발행본처럼 원인을 단정하지 않는다(「어느 글이 얼마를 데려왔는지는 가를 수 없었어」)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(BASE)
OPEN = r'C:\Users\user\Desktop\Blog\_1.컨텐츠\여행정보_컨텐츠\260927_오픈시각\clip\cover_scene.png'
shorts.HEAD = ('검색어 고르느라 진 뺐는데', '검색으로 온 사람 16.88%')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AIL = 'AI 생성 이미지'

SCENES = prep([
    dict(D, media=os.path.join(UP, 'img1.png'), z0=1.0, z1=1.12, ease='punch', label=AIL,
         call=[(0.4, '제목에 넣을 검색어 고민', WHITE)],
         cap='블로그 글 하나 쓸 때마다, 제목에 넣을 검색어 고르느라 진이 빠졌어.'),
    dict(D, media=os.path.join(BASE, 'ai_laptop.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.5, '검색창에 쳐서 온 사람', WHITE), (2.4, '16.88%', YEL)], sfx=[(2.4, 'ding')],
         cap='그런데 통계를 열어 보니, 검색창에 쳐서 들어온 사람은, 열 명 중 두 명도 안 됐어.'),
    dict(D, media=os.path.join(BASE, 'ai_feed.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.5, '네이버 앱 첫 화면 = 홈판', WHITE), (2.6, '사이트 유입 중 75.92%', YEL)], sfx=[(2.6, 'ding')],
         cap='나머지는 대부분 네이버 앱 첫 화면, 추천 글이 뜨는 홈판에서 넘어왔어.'),
    dict(D, media=os.path.join(BASE, 'ai_soccer.png'), z0=1.0, z1=1.1, label=AIL,
         call=[(0.6, '검색 상위 20개 중 16개 축구', WHITE)],
         cap='검색으로 들어온 쪽은, 축구 경기에 맞춰 쓴 글이 대부분이었어. 노린 대로는 된 거야.'),
    dict(D, media=os.path.join(UP, 'img1.png'), z0=1.1, z1=1.2, focus=(0.6, 0.5), label=AIL,
         call=[(0.5, '축구 글 없던 날', WHITE), (2.0, '조회수 104 → 287', YEL)], sfx=[(2.0, 'ding')],
         cap='그런데 축구 글이 하나도 없던 날에도, 하루 조회수가 287로 뛰었어.'),
    dict(D, media=OPEN, z0=1.0, z1=1.08, label=AIL,
         call=[(0.5, '한 달 검색량 110', WHITE), (2.4, '들어온 사람 89%가 홈판', YEL)], sfx=[(2.4, 'ding')],
         cap='오히려 홈판에서 오래 읽힌 건, 마일리지 좌석 글이었어. 한 달 검색량이 110밖에 안 됐는데.'),
    dict(D, media=os.path.join(UP, 'img2.png'), z0=1.0, z1=1.08, label=AIL,
         call=[(0.6, '검색어보다 직접 해 본 것', YEL)],
         cap='그래서 검색어 고르는 시간은 줄이고, 남는 힘은 현장에 가 보고, 실제로 측정하는 데 쓰기로 했어.'),
    dict(D, media=os.path.join(BASE, 'ai_feed.png'), z0=1.1, z1=1.0, label=AIL,
         cap='블로그 하는 너는, 검색으로 들어오는 사람이 많아? 아니면 홈판이 많아? 댓글로 알려줘.'),
], BASE, 'BV')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'BV', 'blog_views_v2.mp4')
