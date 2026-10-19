# 캠프라인 AS 보내기 클립 (발행 10/14 21:14, logNo 224441817499 — 장비, 델타 A/S 1편)
# 실행: python clipCA.py stills / python clipCA.py → out\campline_as.mp4
# 그림은 전부 직접 찍은 사진(261013_delta_as\) — AI 없음, 크레딧 0. 화면 캡처(댓글·문의·메모)는 fit='contain'
# 사진 빛은 원래대로(흰 바탕 낮·편의점 실내) — 노을·어두운 톤 쏠림 없음(10/13)
# 개인정보: 01 닉네임 · 12 이름·전화·주소 · 15 송장은 가림본만. 편의점·택배사 이름은 말하지 않는다
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), '261013_delta_as', n)
shorts.HEAD = ('캠프라인 AS 보내는 법', '창갈이 말고 토캡만')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
PH = dict(label='직접 찍은 사진', call_top=True)   # 큰 글은 위 띠로 — 접수기 화면 숫자를 가리지 않게
CAP = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='화면 캡처 · 개인정보 가림')
NUM_OK = ()

SCENES = prep([
    dict(D, media=P('06_toe_left_side_gap.jpg'), z0=1.0, z1=1.12, **PH,
         call=[(0.4, '10년 신은 등산화', WHITE), (3.0, '토캡만 붙여 주세요', YEL)], sfx=[(3.0, 'ding')],
         cap='10년 신은 등산화 앞코가, 이렇게 벌어졌어. 창갈이 대신, 토캡만 붙여 달라고 보냈어.'),
    dict(D, media=P('01_comment_masked.png'), **CAP, call=[(0.6, '새 등산화가 돼서 온다', YEL)],
         cap='시작은 등산화 글에 달린 댓글이야. 밑창을 갈면, 새 신발이 돼서 돌아온대.'),
    dict(D, media=P('02_inquiry_page.png'), **CAP, call=[(0.6, '문의 다음 날 전화', YEL)],
         cap='홈페이지에 문의를 남겼더니, 다음 날 전화가 왔어. 지금 상태면, 창갈이까진 안 해도 된대.'),
    dict(D, media=P('08_toe_left_front_crack.jpg'), z0=1.05, z1=1.15, **PH, call=[(0.6, '가운데 세로 금', YEL)],
         cap='토캡은 앞코를 감싼 고무야. 왼쪽은 가운데에 금이 갔고, 밑창과 닿는 경계가 벌어졌어.'),
    dict(D, media=P('07_toe_right_side.jpg'), z0=1.12, z1=1.02, **PH, call=[(0.6, '창갈이 6만 원 · 접착 무상', YEL)],
         cap='홈페이지 안내로는, 이 신발 창갈이가 6만 원. 떨어진 토캡을 붙이는 건, 일반 접착이면 무상이야.'),
    dict(D, media=P('05_wiped_drying_top.jpg'), z0=1.0, z1=1.1, **PH, call=[(0.6, '빨지 말고 겉만', YEL)],
         cap='빨지는 않았어. 물티슈로 겉만 닦고, 끈과 깔창을 빼서 말렸지.'),
    dict(D, media=P('11_in_vantage_box.jpg'), z0=1.1, z1=1.0, **PH, call=[(0.6, '새 상자에 헌 신발', YEL)],
         cap='보낼 상자가 없어서, 새로 산 신발 박스에 담았어. 금도끼가 나올지, 쇠도끼가 그대로 올라올지.'),
    dict(D, media=P('12_request_memo_masked.jpg'), **CAP, call=[(0.6, '메모가 곧 접수서', YEL)],
         cap='따로 접수가 없으니까, 손으로 쓴 메모가 접수서야. 접착만 해 주고, 방수 테스트 결과지도 부탁했어.'),
    dict(D, media=P('13_postbox_weight.jpg'), z0=1.0, z1=1.12, **PH, call=[(0.6, '1,780g', YEL)],
         cap='보내는 건 편의점 무인 접수기로 했어. 저울에 올리니, 상자까지 1,780g.'),
    dict(D, media=P('14_postbox_fee.jpg'), z0=1.0, z1=1.12, **PH, call=[(0.6, '선불 5,600원', YEL)], sfx=[(0.6, 'ding')],
         cap='부산까지 운임은, 선불 5,600원. 직원한테 물어볼 일도 없었어.'),
    dict(D, media=P('10_laced_top.jpg'), z0=1.1, z1=1.0, **PH,
         cap='수선은 열흘에서 보름쯤 걸린대. 너는 오래 신은 등산화, 토캡만 붙여 본 적 있어?'),
], BASE, 'CA')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'CA', 'campline_as.mp4')
