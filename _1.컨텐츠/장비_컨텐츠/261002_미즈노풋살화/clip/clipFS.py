# 미즈노 풋살화 사이즈 클립 (발행 10/11 12:00, logNo 224429846841)
# 실행: python clipFS.py stills / python clipFS.py → out\futsal_size.mp4
# 사진은 직접 찍은 것(base data), 발볼 그림만 AI. 판매처 이름은 뺀다(클립 지침). 숫자는 발행본 그대로
# 녹음 전 검사(10/11): repeat_check · pron_book check 통과 — 대본 narration\FS\script.txt
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(os.path.dirname(BASE), 'base data')
ph = lambda n: os.path.join(P, n)
shorts.HEAD = ('미즈노 풋살화 사이즈', '270이 안 들어가 275로')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
FIELD = 'video:' + os.path.join(BASE, 'hf_field_slow.mp4')
NUM_OK = ('2026.10.01', '2026.10.02', '+5mm')   # 촬영 날짜(파일 이름) · 5mm 올린 것

SCENES = prep([
    dict(D, media=FIELD, z0=1.0, z1=1.04, label='2026.10.02 직접 찍음 · 움직임 AI',
         call=[(0.3, '발볼 넓은 270', WHITE), (2.2, '발이 안 들어감', YEL)], sfx=[(2.2, 'ding')],
         cap='발볼 넓은 풋살화를 270으로 샀는데, 발이 안 들어갔어.'),
    dict(D, media=os.path.join(BASE, 'ai_width_fit.jpg'), z0=1.0, z1=1.0, whole=True, label='AI 생성 그림',
         call=[(0.4, '발볼 옆이 조임', YEL)],
         cap='발볼 옆이 조여서, 반쯤 걸린 채 멈췄어.'),
    dict(D, media=os.path.join(BASE, 'fit_20261001_221218.jpg'), z0=1.0, z1=1.0, whole=True, label='2026.10.01 직접 찍음',
         call=[(0.5, '270 · 270 · 275', YEL)],
         cap='미즈노만 세 켤레째야. 앞의 둘은 270, 지금 신는 건 275.'),
    dict(D, media=ph('1-1/20261001_221218.jpg'), cx=0.0, z0=1.3, z1=1.45, focus=(0.15, 0.5), label='2026.10.01 직접 찍음',
         call=[(3.0, '2년 · 앞코 물렁', WHITE)],
         cap='첫 켤레는 매장에서 신어 보고, 270으로 골랐어. 2년쯤 신으니, 앞코가 물렁해졌어.'),
    dict(D, media=ph('1-1/20261001_221329.jpg'), z0=1.0, z1=1.1, label='2026.10.01 직접 찍음',
         call=[(0.4, '깔창도 찢어짐', WHITE)],
         cap='깔창까지 찢어져서, 새로 사기로 했어.'),
    dict(D, media=ph('1-2/20261001_223109.jpg'), cx=0.8, z0=1.05, z1=1.15, focus=(0.6, 0.5), label='2026.10.01 직접 찍음',
         call=[(0.5, '98,800원 · 270', WHITE), (3.2, '신어 보기 전에 태그부터', YEL)],
         cap='같은 미즈노니까, 270이면 되겠지. 발볼 넓은 모델이라, 신어 보기도 전에 태그부터 뗐어.'),
    dict(D, media=ph('1-2/20261001_222718.jpg'), z0=1.0, z1=1.12, ease='punch', label='2026.10.01 직접 찍음',
         call=[(0.4, '270인데 여기서 멈춤', YEL)], sfx=[(0.4, 'ding')],
         cap='미즈노에 270, 사이즈는 똑같은데 왜 다른지는 나도 몰라. 내가 아는 건, 이 신발엔 발이 안 들어간다는 것뿐이야.'),
    dict(D, media=ph('1-1/20261001_221304.jpg'), z0=1.0, z1=1.1, label='2026.10.01 직접 찍음',
         call=[(0.5, '78,700원 · 275', WHITE), (3.4, '신어 보고 태그', YEL)],
         cap='한 달 뒤엔 다른 모델을, 5mm 올린 275로 샀어. 태그는 신어 보고 나서 뗐어.'),
    dict(D, media=ph('1-2/20261001_223029.jpg'), z0=1.0, z1=1.1, label='2026.10.01 직접 찍음',
         call=[(0.5, '끝까지 들어감', YEL)], sfx=[(0.5, 'ding')],
         cap='이번엔 발이 끝까지 들어갔어. 지금 뛸 때 신는 게, 이 275야.'),
    dict(D, media=ph('1-3/20261002_195605.jpg'), z0=1.0, z1=1.1, label='2026.10.02 직접 찍음',
         call=[(0.5, '정사이즈 91%', WHITE), (3.6, '내 발은 +5mm', YEL)],
         cap='상세 페이지 후기는, 정사이즈가 91%였어. 그런데 내 발엔, 5mm 큰 쪽이 맞았어.'),
    dict(D, media=ph('1-2/20261001_223109.jpg'), z0=1.0, z1=1.06, label='2026.10.01 직접 찍음',
         call=[(0.5, '왼쪽 275 · 오른쪽 270', WHITE)],
         cap='나란히 두면 거의 똑같아 보여. 그런데 왼쪽은 편하고, 오른쪽은 발이 안 들어가.'),
    dict(D, media=ph('1-3/20261002_195759.jpg'), z0=1.0, z1=1.1, label='2026.10.02 직접 찍음',
         call=[(0.5, '태그는 신어 본 다음에', YEL)],
         cap='예전에 신던 사이즈보다, 직접 실패한 기록이 기준이 됐어. 태그는 신어 본 다음에 떼.'),
    dict(D, media=FIELD, z0=1.04, z1=1.0, label='2026.10.02 직접 찍음 · 움직임 AI',
         cap='풋살 오래 한 사람들, 같은 브랜드도 모델마다 사이즈를 다르게 신어? 댓글로 알려줘.'),
], BASE, 'FS')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'FS', 'futsal_size.mp4')
