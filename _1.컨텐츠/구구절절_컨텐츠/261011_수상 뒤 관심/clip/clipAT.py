# 「노벨문학상 앤카슨, 나는 왜 발표 다음 날에야 검색했나」 클립 (발행 10/16 07:10, logNo 224438386897 — 구구절절)
# 실행: python make_anims.py → python clipAT.py → out\attention_late.mp4
# 10/16 판교 클립에서 정한 결: 블로그와 결을 달리 — 집중 안 해도 그림만으로 이해되게, 장면을 늘리고 한 장면엔 하나만
#   첫·끝은 발행본 AI 썸네일(어제 서가 → 오늘 매대) 을 왼쪽에서 오른쪽으로 옮겨 보기, 나머지는 make_anims.py 움직이는 그림
# 숫자는 발행본 그대로. 팀 실명 없음 — 역주행 끝난 팀은 「A·B」, 리센느는 「요즘 대세 아이돌」(10/16 사용자: 발음이 이상하다)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
TH = os.path.join(os.path.dirname(BASE), 'img', '00_thumb_same_book.png')
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('관심은 왜 한발 늦게 올까', '상 받은 다음 날에야 검색했다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 발행글 기준')
AI = 'AI 생성 이미지 · 실제 서점 아님'
NUM_OK = ()

SCENES = prep([
    dict(D, media=TH, z0=1.7, z1=1.7, focus=(0.25, 0.55), focus1=(0.75, 0.55), label=AI, call_top=True,
         call=[(0.4, '어제는 맨 아래 칸, 오늘은 매대', WHITE)],
         cap='노벨상 발표 다음 날에야, 나는 처음으로 앤 카슨을 검색했어.'),
    dict(D, media=A('sales'), **AN, call=[(0.4, '발표 12시간 만에', YEL)], sfx=[(1.6, 'ding')],
         cap='발표 12시간 만에, 한 서점 판매가 184배가 됐어.'),
    # 10/16 사용자 「책·음원·컬링이 섞여 복잡 — 현상에서 근거로 넘어가는 자리에 한 장면」 → 왜? + ①·② 장 나눔
    dict(D, media=A('why'), **AN, call=[(0.4, '왜 다들 한꺼번에?', YEL)],
         cap='왜 다들, 한꺼번에 몰릴까? 이유는 두 가지야.'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '이유 하나', YEL)],
         cap='첫째, 우리는 남을 따라 사.'),
    dict(D, media=A('queue'), **AN, call=[(0.4, '앞사람 둘이 같으면', YEL)],
         cap='줄 선 사람을 떠올려 봐. 앞사람 둘이 같은 걸 고르면, 세 번째 사람부터는 그냥 따라가.'),
    dict(D, media=A('crowd'), **AN, call=[(0.4, '상 = 앞사람 수천 명', YEL)],
         cap='상은, 앞사람 수천 명이 이미 샀다는 신호야.'),
    dict(D, media=A('worlds'), **AN, call=[(0.4, '같은 48곡, 8개 세계', YEL)],
         cap='같은 노래 48곡을 8곳에 따로 풀었더니, 1등이 전부 달랐어.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '이유 둘', YEL)],
         cap='둘째, 신호가 꺼지면 관심도 꺼져.'),
    dict(D, media=A('stars'), **AN, call=[(0.4, '수상작의 별점', YEL)],
         cap='수상작은 독자가 확 늘었는데, 별점은 오히려 떨어졌어.'),
    dict(D, media=A('curling'), **AN, call=[(0.4, '메달 뒤 컬링 선수', YEL)],
         cap='메달 뒤에 종목이 클까? 컬링 등록 선수는, 790명에서 631명으로 줄었어.'),
    dict(D, media=A('ends'), **AN, call=[(0.4, '같은 역주행, 다른 끝', YEL)],
         cap='역주행해도, 2년 만에 끝난 팀이 있어. 노래 탓이 아니었어. 무대가 없었고, 계약이 끝났지.'),
    dict(D, media=A('bread'), **AN, call=[(0.4, '요즘 대세 아이돌 빵', YEL)],
         cap='요즘 대세 아이돌 빵은, 열 중 일곱을 남자가 샀어. 한 번 사면 끝나는 물건이고.'),
    # 요약 장(10/16 사용자 「이미지도 요약 형태로 장 추가」) — ①·② 칸에 앞 장면 그림을 작게 모아 한 장
    dict(D, media=A('recap'), **AN, call=[(0.4, '한 장으로 정리', YEL)],
         cap='정리하면 이거야. 우리는 남을 따라 사고, 그 신호가 꺼지면 관심도 같이 꺼져.'),
    dict(D, media=TH, z0=1.7, z1=1.55, focus=(0.75, 0.55), label=AI, call_top=True,
         call=[(0.4, '작품일까, 신호일까', YEL)],
         cap='장바구니에 든 그 책, 상 받기 전에 알던 작가야? 너는 최근에, 뒤늦게 산 거 있어?'),
], BASE, 'AT')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'AT', 'attention_late.mp4')
