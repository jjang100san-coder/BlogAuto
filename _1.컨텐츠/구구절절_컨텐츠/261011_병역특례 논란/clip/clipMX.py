# 아시안게임 병역특례 클립 (발행 10/12 10:30, logNo 224438185069 — 구구절절)
# 실행: python clipMX.py stills / python clipMX.py → out\military_exemption.mp4
# 그림은 발행본 도해(img\) 그대로. 첫 장면은 발행본 AI 이미지(특정 인물 아님). 선수 이름은 쓰지 않는다
# 「2019년 개정 / 2020년 6월 30일 시행」이 발행본에 둘 다 있어 대본은 「법이 바뀐 뒤로는」으로 연도를 말하지 않음
# 마지막은 발행본 끝 「오늘 할 수 있는 것 하나」(청원 검색)를 그대로 — 찬반을 묻지 않는다
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(os.path.dirname(BASE), 'img', n)
shorts.HEAD = ('금메달이면 군 면제?', '법에는 면제가 없다')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
DG = dict(z0=1.0, z1=1.0, whole=True, fit='contain', label='직접 그린 도해 · 발행글 기준')
NUM_OK = ()

SCENES = prep([
    dict(D, media=P('00_thumb_two_gates.png'), z0=1.0, z1=1.12, label='AI 생성 이미지 · 특정 인물 아님',
         call=[(0.4, '금메달 = 군 면제?', WHITE), (3.6, '법에는 면제가 없다', YEL)], sfx=[(3.6, 'ding')],
         cap='금메달 따면 군대 안 간다. 다들 그렇게 알지? 하지만 법에는, 면제라는 말이 한 번도 안 나와.'),
    dict(D, media=P('01_two_roads.png'), **DG, call=[(0.6, '면제 아니고 편입', YEL)],
         cap='조문에 적힌 건 편입이야. 현역 대신 보충역으로, 기초훈련 4주를 받고, 34개월 동안 소속팀에서 뛰면서 공익복무를 해.'),
    dict(D, media=P('02_three_stamps.png'), **DG, call=[(0.6, '도장 3개 더', YEL)],
         cap='금메달은 자격일 뿐이야. 본인 원서, 문체부 추천, 병무청장 결정까지, 도장 세 개를 더 받아야 해.'),
    dict(D, media=P('03_bench_all.png'), **DG, call=[(0.6, '뛴 사람 → 명단 전원', YEL)],
         cap='법이 바뀐 뒤로는, 경기에 뛴 사람만이 아니라, 명단에 든 전원이 대상이 됐어.'),
    dict(D, media=P('04_pie_81.png'), **DG, call=[(0.6, '80명 중 65명', YEL)],
         cap='최근 4년 편입한 80명 중, 65명이 아시안게임 금메달이었어. 그래서 논의가, 폐지보다 그 대회를 뺄까로 먼저 가는 거야.'),
    dict(D, media=P('05_munich_1972.png'), **DG, call=[(0.6, '1972년 뮌헨', YEL)],
         cap='이 제도는 1972년 뮌헨에서 시작됐어. 북한이 사격 금메달을 딸 때, 우리는 은 하나였거든.'),
    dict(D, media=P('13_poll_bars.png'), **DG, call=[(0.6, '10명 중 6명', YEL)],
         cap='여론은 10명 중 6명이, 줄이거나 없애자는 쪽이야. 가장 많은 답은 아시안게임만 빼자였고.'),
    dict(D, media=P('15_nine_days.png'), **DG, call=[(0.6, '소급은 어렵다', YEL)],
         cap='그럼 이번 대회 선수들은? 변호사들과 병무청 의견이 같았어. 이미 받은 메달에 소급하긴 어렵다는 거야. 바뀐 규칙은 다음 대회부터일 가능성이 커.'),
    dict(D, media=P('14_petition_gauge.png'), **DG, call=[(0.6, '국민동의청원 · 병역', YEL)],
         cap='궁금하면 국회 국민동의청원에서, 병역을 검색해 봐. 뉴스의 온도와 거기 찍힌 동의 수가, 얼마나 다른지 보일 거야.'),
], BASE, 'MX')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'MX', 'military_exemption.mp4')
