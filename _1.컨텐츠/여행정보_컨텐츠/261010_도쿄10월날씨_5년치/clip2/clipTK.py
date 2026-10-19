# 10월 도쿄 날씨 클립 — 새 틀(shorts.py: 고정 제목 띠 + 움직이는 장면 + 말 자막) 시험 1/5 (발행 10/10 17:00, logNo 224436698890)
# 실행: python clipTK.py stills / python clipTK.py → out\tokyo_oct_v2.mp4
# 사진: 2023-10-13~16 도쿄에서 직접 찍은 것(사람은 뒷모습·먼 거리뿐). AI 1장은 「AI 생성 이미지」 표시
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(BASE)
PH = r"C:\Users\user\Desktop\Blog\_1.컨텐츠\여행_컨텐츠\양식 셋업 전\'23년 10월 13일 ~ 16일 도쿄 혼자가서 사람들"
shorts.HEAD = ('10월 도쿄 날씨', '반팔이야? 외투야?')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)

NUM_OK = ('2023.10.15', '2023.10.14', '2023.10.13', '09:48', '16:59')   # 사진 촬영 날짜·시각(파일 이름 = 촬영 기록), 발행본 본문엔 없음
SCENES = prep([
    dict(D, media='video:' + os.path.join(BASE, 'hf_rain.mp4'), z0=1.0, z1=1.06, label='2023.10.15 · 직접 찍음',
         call=[(0.4, '16.9도', YEL)], sfx=[(0.4, 'ding')],
         cap='10월 중순 도쿄, 반팔이야? 외투야? 내가 간 나흘은 날마다 달랐어.',
         breath=[(3, 0.55)]),   # 「외투야?」 뒤 0.5초 쉼(10/11 사용자) — 틈 번호: 시월 중순 / 도쿄, / 반팔이야? / 외투야?
    dict(D, media=os.path.join(PH, '20231015_094802.jpg'), z0=1.0, z1=1.12, label='2023.10.15 09:48',
         call=[(0.6, '비 43.5mm', WHITE)],
         cap='2023년 10월 15일 아침, 창밖은 온통 빗줄기였어. 이날 최고기온은 16.9도.'),
    dict(D, media='video:' + os.path.join(BASE, 'hf_odaiba.mp4'), z0=1.0, z1=1.05, label='2023.10.15 16:59 · 오다이바',
         call=[(0.8, '다음 날 25.8도', YEL)], sfx=[(0.8, 'ding')],
         cap='그런데 저녁엔 비가 그쳤고, 다음 날은 25.8도 쾌청이었어.'),
    dict(D, media=os.path.join(PH, '20231014_150609.jpg'), z0=1.05, z1=1.15, label='2023.10.14',
         call=[(0.5, '23.4도', WHITE)],
         cap='그 앞 이틀은 23.4도였어. 나흘이 다 달랐던 거야.'),
    dict(D, media=os.path.join(UP, 'img1.png'), z0=1.0, z1=1.1, label='AI 생성 이미지 · 실제 도쿄·특정 인물 아님',
         call=[(0.8, '21.5도 ~ 25.8도', YEL)], sfx=[(0.8, 'ding')],
         cap='기상청 5년 치를 겹쳐 보니, 10월 중순 최고기온 평균이, 해마다 4도 넘게 차이 났어.'),
    dict(D, media=os.path.join(PH, '20231013_142819.jpg'), z0=1.0, z1=1.1, label='2023.10.13 · 하네다',
         call=[(0.7, '10/15 ~ 10/24', WHITE)],
         cap='반팔로 다닐 만한 마지막 날도, 해마다 달랐어. 10월 15일부터 24일 사이야.'),
    dict(D, media=os.path.join(PH, '20231015_200555.jpg'), z0=1.0, z1=1.1, label='2023.10.15 밤',
         call=[(0.6, '초순·중순·하순', YEL)], sfx=[(0.6, 'ding')],
         cap='그래서 날짜가 아니라 초순, 중순, 하순으로 짐을 싸고, 마지막은 출발 전날 예보로 정하는 게 맞았어.'),
    dict(D, media='video:' + os.path.join(BASE, 'hf_odaiba.mp4'), z0=1.08, z1=1.0, label='2023.10.15 · 오다이바',
         cap='너는 10월 도쿄에 반팔 챙겨? 아니면 외투 챙겨? 댓글로 알려줘.'),
], BASE, 'TK')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'TK', 'tokyo_oct_v2.mp4')
