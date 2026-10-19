# 「관음동 천장 붕괴 | 기술이 좋아져도 왜 무너질까, 최근 9건 중 「기술이 없어서」는 0건이었어」 클립 (발행 10/18 17:20, logNo 224443112219 — 구구절절)
# 실행: python make_html.py → python clipCE.py → out\ceiling_why.mp4
# 10/18 결: 마스터 5-8 양식 움직이는 인포그래픽(clipkit/html_anim.py) + 10/16 결(한 장면 하나·장 카드·요약 장 three)
# 인명 피해 사고 — 떨어지는 장면 연출·과장 없음, 관음동 원인은 조사 중으로만. 첫 장면은 발행본 AI 썸네일(실제 현장 아님)
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('기술은 좋아졌는데', '천장은 왜 떨어질까')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 사고조사위 원문')
AI = 'AI 생성 이미지 · 실제 관음동 현장 아님'
MOV = 'video:' + os.path.join(BASE, 'hf_hook.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.05, label=AI, call_top=True, call=[(0.4, '휴대폰은 새것, 천장은?', WHITE)],
         cap='휴대폰은 해마다 좋아지는데, 건물 천장은 왜 아직도 떨어질까?'),
    dict(D, media=A('frame'), **AN, call=[(0.4, '10월 10일 · 대구 관음동', YEL)],
         cap='관음동 상가에서, 매달아 둔 천장이 떨어져 38명이 다쳤어. 뼈대는 그대로였어.'),
    dict(D, media=A('shelf'), **AN, call=[(0.4, '줄에 매단 선반', YEL)],
         cap='줄에 매단 선반처럼, 판과 조명이 늘수록 버틸 무게도 늘어. 무엇이 결정적이었는지는 조사 중이야.'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '판정 하나', YEL)],
         cap='그럼 이런 천장은, 누가 점검할까?'),
    dict(D, media=A('check'), **AN, call=[(0.4, '일본 vs 우리', YEL)],
         cap='일본은 큰 매단 천장을 정기적으로 보는데, 우리 법엔 그 칸이 없어.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '판정 둘', YEL)],
         cap='범위를 넓혀서, 최근 큰 건설 사고 9건을 열어 봤어.'),
    dict(D, media=A('nine'), **AN, call=[(0.4, '사고조사위 원문 기준', YEL)], sfx=[(2.7, 'ding')],
         cap='기술이 없어서 무너진 건, 한 건도 없었어. 대부분 알던 단계를 건너뛰었어.'),
    dict(D, media=A('exam'), **AN, call=[(0.4, '손상 800건', YEL)],
         cap='800건을 살핀 스위스 연구도 비슷해. 다만 처음 마주친 문제가, 손해액의 43%를 차지했어.'),
    # 10/18 사용자 「연구 숫자에서 갑자기 인원수 이야기로 넘어가 붕 뜬다」 → 이음 장 카드 하나
    dict(D, media=A('ch3'), **AN, call=[(0.4, '판정 셋', YEL)],
         cap='그럼 좋아진 기술은, 건설 현장까지 닿았을까?'),
    dict(D, media=A('speed'), **AN, call=[(0.4, '한 사람이 만드는 양', YEL)],
         cap='한 사람이 만드는 양을 견주면, 20년 동안 공장은 두 배, 건설 현장은 1.2배야. 아직 손으로 하는 일이 많거든.'),
    dict(D, media=A('age'), **AN, call=[(0.4, '건물의 나이', YEL)],
         cap='그리고 30년 넘은 건물이, 46.3%까지 늘었어.'),
    # 요약 장(10/16 「이미지도 요약 형태로」)
    dict(D, media=A('three'), **AN, call=[(0.4, '한 장으로 정리', YEL)],
         cap='정리하면 셋이야. 건너뛴 단계, 막지 않은 구멍, 쌓인 나이.'),
    dict(D, media=A('look'), **AN, call=[(0.4, '한 번 올려다보기', YEL)],
         cap='자주 가는 곳 천장에, 금이나 처짐은 없었어? 한 번 올려다볼래?'),
], BASE, 'CE')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'CE', 'ceiling_why.mp4')
