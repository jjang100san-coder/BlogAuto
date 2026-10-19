# 퇴근 후 등산 어디 가지 2 클립 (발행 10/13 14:50, logNo 224438005796)
# 실행: python clipMB.py stills / python clipMB.py → out\mubong_finder.mp4
# 아직 안 가 본 산이라 사진 대신: 발행본 표 3개를 카드로(make_cards.py, 숫자 그대로) + 직접 그린 등고선 지도 2장 + AI 장면 1장
# AI 장면은 흐린 평일 오후(10/13 사용자: 노을·어두운 톤 쏠림 금지, 장면마다 다양하게) · 얼굴 없음 · 「실제 산 사진 아님」
# 「그런데」는 「그런들」로 들려(발음 장부) 「하지만」
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), '클로드', n)
here = lambda n: os.path.join(BASE, n)
shorts.HEAD = ('퇴근 후 등산 어디 가지 2', '남은 건 프로그램에 없는 산')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
CARD = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 표 · 발행글 기준')
MAP = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 만든 지도')
TRAIL = 'video:' + here('hf_trail.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=TRAIL, z0=1.0, z1=1.05, label='AI 생성 이미지 · 실제 산 사진 아님',
         call=[(0.4, '퇴근하고 바로 갈 산', WHITE), (4.0, '프로그램에 없는 산', YEL)], sfx=[(4.0, 'ding')],
         cap='퇴근하고 바로 갈 수 있는 곳을, 가까운 순으로 세워 봤어. 하지만 끝까지 남은 건, 내 프로그램에 없는 산이었어.'),
    dict(D, media=here('card_near.png'), **CARD, call=[(0.6, '45km 안 149곳', YEL)],
         cap='출발 지점에서 45km 안에, 조건에 맞는 후보가 149곳. 하지만 목록을 쭉 내려 봐도, 이름을 들어 본 데가 거의 없더라.'),
    dict(D, media=here('card_search.png'), **CARD, call=[(0.6, '검색은 많고 글은 적은 산', YEL)],
         cap='그래서 산마다 검색량과 블로그 글 수를 나란히 놨어. 궁금해하는 사람은 많은데 후기는 적은 곳이, 쓸 만한 산이거든.'),
    dict(D, media=here('card_search.png'), **CARD, call=[(0.6, '무봉산: 검색 3배 · 글 3분의 1', YEL)],
         cap='무봉산은 지난번 간 수암봉보다 검색이 세 배인데, 글은 3분의 1이야. 두 번째 후보는 화성 봉담에 있어.'),
    dict(D, media=P('contour_건달산.png'), **MAP, call=[(0.6, '건달산 · 능선 한 줄기', YEL)],
         cap='건달산은 남쪽 들머리에서 정상까지, 능선이 한 줄기라 길이 단순해.'),
    dict(D, media=P('contour_무봉산_등산로.png'), **MAP, call=[(0.6, '자료마다 있다 없다', YEL)],
         cap='무봉산은 자료마다 있다가 없다가 했어. 정상석이 선 봉우리를, 산줄기 이름으로 잡아 둔 곳이 있었거든.'),
    dict(D, media=here('card_height.png'), **CARD, call=[(0.6, '정상석 360.2m', YEL)],
         cap='그래서 높이도 셋으로 갈려. 정상석에는 360m라고 새겨져 있어.'),
    dict(D, media=P('thumbnail_무봉산찾기.png'), **CARD, call=[(0.6, '내 기록이 첫 자료', YEL)],
         cap='결국 무봉산으로 정했어. 프로그램에 예상값이 없으니, 내가 걸어서 남길 기록이 첫 자료가 돼.'),
    dict(D, media=TRAIL, z0=1.05, z1=1.0, label='AI 생성 이미지 · 실제 산 사진 아님',
         cap='너희 동네에도, 지도 앱에 잘 안 나오는 산이 있어? 있으면 댓글로 알려 줘.'),
], BASE, 'MB')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'MB', 'mubong_finder.mp4')
