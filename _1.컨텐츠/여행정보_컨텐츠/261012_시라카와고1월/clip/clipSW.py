# 「시라카와고 날씨 | 1월 중순엔 눈이 얼마나 쌓여 있어?」 클립 (발행 10/18 11:30, logNo 224439622339 — 여행정보)
# 실행: python make_html.py → python clipSW.py → out\shirakawago_snow.mp4
# 10/18 결: 마스터 5-8 양식 움직이는 인포그래픽(clipkit/html_anim.py) + 10/16 결(한 장면 하나·장 카드·요약 장 pack)
# 숫자는 발행본 그대로(일본 기상청 시라카와 관측소). 첫·끝은 발행본 AI 삽화 — 실제 시라카와고 사진 아님
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = lambda n: os.path.join(os.path.dirname(BASE), n)
A = lambda n: 'video:' + os.path.join(BASE, n + '.mp4')
shorts.HEAD = ('1월 중순 시라카와고', '눈은 얼마나 쌓여 있을까')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
AN = dict(z0=1.0, z1=1.0, whole=True, call_top=True, label='직접 만든 그림 · 일본 기상청')
AI = 'AI 생성 이미지 · 실제 시라카와고 사진 아님'
MOV = 'video:' + os.path.join(BASE, 'hf_hook.mp4')
NUM_OK = ()

SCENES = prep([
    dict(D, media=MOV, z0=1.0, z1=1.06, label=AI, call_top=True, call=[(0.4, '1월 14일, 눈은 몇 cm?', WHITE)],
         cap='1월 중순 시라카와고, 눈이 얼마나 쌓여 있을까?'),
    dict(D, media=A('gauge'), **AN, call=[(0.4, '같은 1월 14일', YEL)], sfx=[(3.0, 'ding')],
         cap='같은 1월 14일인데, 2020년엔 3cm, 이듬해엔 182cm였어.'),
    dict(D, media=A('years'), **AN, call=[(0.4, '11년치 1월 14일', YEL)],
         cap='2016년부터 2026년까지 겹쳐 보니, 100cm 넘은 해가 다섯 번이었어.'),
    dict(D, media=A('ch1'), **AN, call=[(0.4, '판정 하나', YEL)],
         cap='쌓인 양만큼 궁금한 건, 걷는 그날 새로 내리느냐야.'),
    dict(D, media=A('fresh'), **AN, call=[(0.4, '그날 10cm 넘게', YEL)],
         cap='1월 14일 하루에 10cm 넘게 내린 해는, 11년 중 4번.'),
    dict(D, media=A('ch2'), **AN, call=[(0.4, '판정 둘', YEL)],
         cap='같이 가는 사람이 추위를 많이 타서, 기온도 봤어.'),
    dict(D, media=A('temp'), **AN, call=[(0.4, '1월 중순 기온', YEL)],
         cap='1월 중순엔 낮 최고 평균도, 5도를 넘기 어려웠어.'),
    dict(D, media=A('lightup'), **AN, call=[(0.4, '라이트업은 4일뿐', YEL)],
         cap='내가 가는 1월 14일은, 라이트업 날이 아니야. 입장 제한도 없는 날이지.'),
    # 요약 장(10/16 「이미지도 요약 형태로」)
    dict(D, media=A('pack'), **AN, call=[(0.4, '그래서 이렇게 싼다', YEL)],
         cap='그래서 신발은 많이 쌓인 해에, 옷은 낮에도 5도 아래에 맞추기로 했어.'),
    dict(D, media=IMG('img_boots.jpg'), z0=1.0, z1=1.08, focus=(0.5, 0.55), label=AI, call_top=True,
         call=[(0.4, '다녀와서 적어 둘게', YEL)],
         cap='돌아오면, 그날 실제로 몇 cm였는지 적어 둘게. 너라면 뭘 챙길래?'),
], BASE, 'SW')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'SW', 'shirakawago_snow.mp4')
