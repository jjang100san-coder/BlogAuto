# 숫자형 클립 커버 교체(10/10) — 그래프 대신 「꽉 찬 후킹 장면 + 첫 장면 질문 자막」 (클립 지침 2-4 · 마스터 5-4)
# 실행: python make_covers_1010.py  → 각 clip 폴더에 cover_scene.png(원본 AI 장면)·cover_hook.jpg(올릴 커버)
import os, sys, urllib.request
from PIL import Image, ImageOps, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tactics import still, font
from dataviz import render, LIGHT, WHITE

R = r'C:\Users\user\Desktop\Blog\_1.컨텐츠'
U = 'https://d8j0ntlcm91z4.cloudfront.net/user_3KK4c7emNkdIixmJMHSlXcwfJ9F/hf_20261009_'
JOBS = [  # (클립 폴더, 첫 장면 자막, AI 장면 URL 꼬리 또는 None=내 사진)
    (r'여행_컨텐츠\261006_27년 일본 1월 여행\투어vs자유여행_글\clip', '나고야 당일치기\n{투어가 더 싸}', '170923_56559d37-ca60-4b04-890d-310671d1df72'),
    (r'여행정보_컨텐츠\260930_엔화환전시기\clip', '엔화 환전,\n{몇 시}에 해야 쌀까?', '170922_6ad5cf83-1c77-4c64-bcae-fddcf5bda498'),
    (r'여행정보_컨텐츠\261007_1마일원가\clip', '일본 왕복 한 장에\n{5년}', '170924_692c172b-65a7-415d-b274-2ca812d7961a'),
    (r'여행정보_컨텐츠\260927_오픈시각\clip', '대한항공 마일리지 좌석\n{몇 시}에 열릴까?', '170923_a8ea841a-b604-47fe-a745-762afa066adc'),
    (r'여행정보_컨텐츠\260925_금리엔화_유튜브\clip', '같은 주 엔화 영상\n{숫자가 네 개}', '170922_d3cfdfa4-34f8-4425-bcfa-3f8b878f0969'),
    (r'정보(move)_컨텐츠\260928_야간산찾기\clip', '퇴근 후 등산\n{어디 가지?}', '170921_1dd5db09-4a24-4457-9af4-0888350b063d'),
    (r'여행정보_컨텐츠\261007_마일리지손해노선_해외\clip', '운임 7만 원 왕복에\n{4만 마일} 쓸 거야?', '170924_f94718d2-df98-46ee-a895-1ac7a56aede6'),
    (r'정보(move)_컨텐츠\260926_등산어디가지\clip', '내일 바로 산에 가고 싶을 때\n{어디 가지?}', '170922_ac1c0653-3cd5-43c5-820b-fff437323bc4'),
    (r'여행정보_컨텐츠\261004_제주_주말_마일리지_한라산\clip', '한라산 주말,\n{마일리지로 될까?}', '170910_30d70f42-20b1-4d5c-a53c-2027fb5aeefc'),
    (r'여행정보_컨텐츠\261003_아시아나_국제선_비즈니스_좌석\clip', '합병 전 74일,\n{비즈니스} 어디 갈 수 있어?', '170922_184fa231-a379-4899-9654-17dae7c3cc59'),
    (r'독후감_컨텐츠\261009_앤카슨\clip', '2026 노벨문학상\n{앤 카슨}', '170923_b08bf8f1-b389-4310-b4a5-bf58bf541a53'),
    (r'여행정보_컨텐츠\261007_마일리지손해노선\clip', '운임 9만 원짜리 왕복에\n{3만 마일} 쓸 거야?', '170924_a4a8227b-1f6a-4048-bd6d-234a96bc7abc'),
    (r'여행정보_컨텐츠\261006_마일리지가치\clip', '1마일에 {10원도 안 되는}\n값으로 해외 갈 거야?', '170929_02866440-38b5-433d-97eb-ece4351f010f'),
    (r'여행정보_컨텐츠\261008_2027_10월연휴_마일리지\clip', '이번 주 연휴 끝나면\n{내년 연휴 차례}', '170929_637e93f4-6f8e-46f0-bf7b-1241ab1d8c7c'),
    (r'여행정보_컨텐츠\260924_후쿠오카정보\clip', '같은 후쿠오카 가을\n{반팔 vs 두꺼운 겉옷}', None),
]


def fukuoka(d):
    """내 사진 두 장(9월 다자이후 · 11월 오호리)을 위아래로."""
    up = os.path.dirname(d)
    a = ImageOps.exif_transpose(Image.open(os.path.join(up, 'sep_dazaifu_20240901.jpg'))).convert('RGB')
    b = ImageOps.exif_transpose(Image.open(os.path.join(up, 'nov_ohori_20231125.jpg'))).convert('RGB')
    im = Image.new('RGB', (1080, 1920), WHITE)
    im.paste(ImageOps.fit(a, (1080, 958), centering=(0.5, 0.0)), (0, 0))  # 아래쪽 길가 사람은 잘라냄
    im.paste(ImageOps.fit(b, (1080, 958)), (0, 962))
    return im


for d, hook, tail in JOBS:
    d = os.path.join(R, d)
    scene = os.path.join(d, 'cover_scene.png')
    if tail:
        if not os.path.exists(scene):
            urllib.request.urlretrieve(U + tail + '.png', scene)
        im = ImageOps.fit(Image.open(scene).convert('RGB'), (1080, 1920))
        labels = [('label', 0, 'AI 생성 이미지', 1040, 1880, 24, WHITE, 'r')]
    else:
        im = fukuoka(d)
        labels = [('label', 0, '2024년 9월 · 다자이후', 1040, 920, 30, WHITE, 'r'),
                  ('label', 0, '2023년 11월 · 오호리 공원', 1040, 1880, 30, WHITE, 'r')]
    # 'image' 항목은 label 보다 나중에 그려져 라벨을 덮는다 → 라벨은 사진에 미리 박는다(검은 띠, 마스터 5-3)
    dr = ImageDraw.Draw(im)
    for _, _, s, x, y, sz, col, _a in labels:
        f = font(sz); b = dr.textbbox((0, 0), s, font=f); w, h = b[2] - b[0], b[3] - b[1]
        dr.rectangle([x - w - 14, y - h // 2 - 10, x + 10, y + h // 2 + 12], fill=(0, 0, 0))
        dr.text((x - w - b[0], y - h // 2 - b[1]), s, font=f, fill=col)
    full = os.path.join(d, '_build', 'cover_full.png'); os.makedirs(os.path.dirname(full), exist_ok=True)
    im.save(full)
    sc = dict(type='data', render=render, bg=LIGHT, dur=1.0,
              items=[('image', 0, full, 0, 0, 1080, 1920)], texts=[(0, 'top', hook)])
    out = os.path.join(d, 'cover_hook.jpg')
    still(sc, 0.95, out)
    print('ok', out)
