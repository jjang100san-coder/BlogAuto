# 2026 하남이성산성문화제 후기 클립 (발행 9/19, logNo 224417324152) — 정보형 · 축제는 끝남 → 「내년에 간다면」 기록용
# 실행: python clipIS.py stills / python clipIS.py → out\iseong_clip.mp4
# 숫자·사실은 발행본 그대로. 가수 얼굴이 크게 나온 무대 사진은 쓰지 않는다(마스코트·타이틀 화면·무대 배경만, 사람은 작게 잘라냄)
# 내년 일정은 발행본에 없으니 단정하지 않는다
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(BASE, '..', 'photos_used')
D = dict(type='data', render=render, bg=LIGHT)
GOLD = (176, 110, 30)
SAND = (250, 240, 222)


def crop(src, box, name):
    """사진 일부만 잘라 _build 에 저장(사람 얼굴이 크게 나오지 않게)"""
    from PIL import Image, ImageOps
    os.makedirs(os.path.join(BASE, '_build'), exist_ok=True)
    out = os.path.join(BASE, '_build', name)
    if not os.path.exists(out):
        im = ImageOps.exif_transpose(Image.open(os.path.join(PH, src))).convert('RGB')
        W, H = im.size
        im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H))).save(out, quality=92)
    return out


TITLE = crop('20260919_205823.jpg', (0.0, 0.30, 1.0, 0.95), 'title.jpg')
SEA = crop('20260919_210303.jpg', (0.0, 0.25, 1.0, 0.62), 'sea.jpg')

s0 = dict(D, dur=3.6, items=[
    ('image', 0.1, os.path.join(PH, '20260919_195801.jpg'), 240, 560, 840, 1100),
    ('label', 0.8, '2026년 9월 19~20일 · 미사호수공원', 540, 1160, 36, MUTED),
    ('label', 1.2, '첫날 밤 무대를 보고 왔어', 540, 1240, 50, GOLD)],
    texts=[(0.05, 'top', '하남이성산성문화제\n{다녀온 기록}')], sfx=[(0.1, 'ding'), (1.2, 'ding')])

s1 = dict(D, dur=3.6, items=[
    ('image', 0.1, TITLE, 90, 560, 990, 1000),
    ('label', 0.7, '주제 「하남의 역사, 미래를 두드리다」', 540, 1060, 38, INK),
    ('label', 1.0, '이성산성에서 나온 고대 타악기 「요고」가 상징', 540, 1140, 34, GOLD)],
    texts=[(0.05, 'top', '축제 이름에\n{역사가 있다}')], sfx=[(0.75, 'ding')])

s2 = dict(D, dur=3.8, items=[
    ('label', 0.1, '공지부터 「주차 협소, 대중교통 이용」', 540, 650, 36, RED),
    ('box', 0.4, 90, 720, 990, 1080, SAND),
    ('label', 0.5, '5호선 미사역 1·5번 출구', 540, 790, 48, GOLD),
    ('label', 0.8, '걸어서 5~8분 · 평지', 540, 880, 42, INK),
    ('label', 1.1, '버스 30-5 · 9202 · 마을버스 1', 540, 980, 34, MUTED)],
    texts=[(0.05, 'top', '차 말고\n{미사역에서 걸어}')], sfx=[(0.55, 'ding')])

s3 = dict(D, dur=3.8, items=[
    ('image', 0.1, SEA, 90, 560, 990, 900),
    ('label', 0.6, '첫날 밤 무대 신유 → 윤종신 → 비비', 540, 960, 40, INK),
    ('label', 0.9, '90분을 꽉 채웠어 · 무료', 540, 1040, 44, GOLD),
    ('label', 1.3, '잔디광장 앞쪽은 금방 찬다', 540, 1130, 34, MUTED)],
    texts=[(0.05, 'top', '동네 축제인데\n{무대는 꽉 찼다}')], sfx=[(0.95, 'ding')])

s4 = dict(D, dur=3.8, items=[
    ('label', 0.2, '요고 만들기 · 유물발굴장 같은 체험 부스는', 540, 700, 36, INK),
    ('label', 0.5, '밤엔 대부분 닫혀 있었어', 540, 790, 48, RED),
    ('label', 1.0, '체험이 목적이면 낮에', 540, 900, 52, GOLD),
    ('label', 1.4, '「하남여행버스」는 사전예약제', 540, 1000, 34, MUTED)],
    texts=[(0.05, 'top', '아이랑 간다면\n{낮에 가}')], sfx=[(1.0, 'ding')])

s5 = dict(D, dur=3.8, items=[
    ('image', 0.1, os.path.join(PH, '20260919_195801.jpg'), 340, 560, 740, 920),
    ('box', 1.0, 90, 980, 990, 1200, SAND),
    ('label', 1.1, '너는 동네 축제, 낮에 가 밤에 가?', 540, 1050, 44, GOLD),
    ('label', 1.5, '댓글로 알려줘', 540, 1135, 38, INK)],
    texts=[(0.05, 'top', '공연은 밤\n{체험은 낮}')], sfx=[(1.1, 'ding')])

SCENES = [s0, s1, s2, s3, s4, s5]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        from PIL import Image
        d = os.path.join(BASE, '_build', 'stills'); os.makedirs(d, exist_ok=True)
        tiles = []
        for i, sc in enumerate(SCENES):
            f = os.path.join(d, f's{i}.jpg'); still(sc, sc['dur'] - 0.05, f); tiles.append(Image.open(f).resize((270, 480)))
        sh = Image.new('RGB', (270 * len(tiles), 480))
        for j, im in enumerate(tiles):
            sh.paste(im, (j * 270, 0))
        sh.save(os.path.join(d, 'sheet.jpg'), quality=90); print('stills', d)
    else:
        build(SCENES, BASE, 'IS', 'iseong_clip.mp4')
