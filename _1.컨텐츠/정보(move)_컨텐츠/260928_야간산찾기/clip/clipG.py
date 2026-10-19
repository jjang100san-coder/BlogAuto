# 퇴근 후 등산 어디 가지 · 경기도 118곳 클립 (발행 9/29, logNo 224424969675) — 정보형 · 지하철역 산 클립의 2편
# 실행: python clipG.py stills / python clipG.py → out\night_mountain_clip.mp4
# 숫자는 발행 본문 표 그대로(조건 5개 · 서울 11곳/경기 118곳/정상 기록만 108곳 · 수암봉 104번째 · 지도 들머리 4곳)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit'))
from tactics import build, still
from dataviz import render, LIGHT, INK, NAVY, RED, PINK, MUTED, SKY

BASE = os.path.dirname(os.path.abspath(__file__))
D = dict(type='data', render=render, bg=LIGHT)
GREEN = (46, 125, 80)
MINT = (226, 242, 232)

s0 = dict(D, dur=3.6, items=[
    ('box', 0.2, 90, 620, 300, 710, MINT), ('label', 0.25, '경기', 195, 665, 36, GREEN),
    ('box', 0.35, 320, 620, 760, 710, MINT), ('label', 0.4, '높이 200~400m', 540, 665, 36, GREEN),
    ('box', 0.5, 780, 620, 990, 710, MINT), ('label', 0.55, '정상 기록만', 885, 665, 32, GREEN),
    ('box', 0.65, 200, 730, 520, 820, MINT), ('label', 0.7, '코스 2.5km 이하', 360, 775, 34, GREEN),
    ('box', 0.8, 560, 730, 880, 820, MINT), ('label', 0.85, '상승 350m 이하', 720, 775, 34, GREEN),
    ('label', 1.2, '서울은 11곳 →', 540, 900, 40, MUTED),
    ('count', 1.4, 0, 118, '{:.0f}곳', 540, 1060, 140, GREEN)],
    texts=[(0.05, 'top', '퇴근 후 등산\n{어디 가지?}')], sfx=[(0.1, 'ding'), (1.4, 'ding')])

s1 = dict(D, dur=3.8, items=[
    ('label', 0.2, '프로그램은 코스 짧은 순으로만 줄 세운다', 540, 680, 38, INK),
    ('label', 0.6, '내가 어디서 출발하는지 모른다', 540, 770, 46, RED),
    ('box', 1.1, 240, 860, 840, 1160, MINT), ('label', 1.15, '잘 아는 수암봉은 목록에서', 540, 920, 36, INK),
    ('count', 1.3, 0, 104, '{:.0f}번째', 540, 1060, 100, GREEN)],
    texts=[(0.05, 'top', '그런데 프로그램이\n{모르는 게 하나}')], sfx=[(0.65, 'ding')])

s2 = dict(D, dur=4.0, items=[
    ('label', 0.1, '기록에 없던 들머리 9곳 · 지도(OpenStreetMap) 등산로', 540, 620, 30, MUTED),
    ('hbar', 0.3, '창박골배수지', 64, 110, 740, (150, 190, 160), '64분'),
    ('hbar', 0.5, '원당어린이공원', 63, 110, 870, GREEN, '63분 ← 여기로'),
    ('hbar', 0.7, '성은침례교회', 69, 110, 1000, (150, 190, 160), '69분'),
    ('hbar', 0.9, '병목안시민공원', 78, 110, 1130, (150, 190, 160), '78분'),
    ('label', 1.6, '원당어린이공원 쪽 1.9km · 상승 346m · 정상까지 편도', 540, 1270, 34, INK)],
    texts=[(0.05, 'top', '수암봉 들머리\n{9곳 더 나왔다}')], sfx=[(0.55, 'ding')])

s3 = dict(D, dur=3.6, items=[
    ('label', 0.2, '조명 · 야간 입산 · 통제 구간은', 540, 700, 42, INK),
    ('label', 0.5, '프로그램이 안 알려준다', 540, 790, 52, RED),
    ('box', 1.0, 90, 880, 990, 1180, PINK),
    ('label', 1.1, '헤드랜턴은 무조건', 540, 950, 44, INK),
    ('label', 1.3, '어두워지면 모르는 길로 안 들어가기', 540, 1030, 38, INK),
    ('label', 1.5, '11월 산불조심기간엔 통제 다시 확인', 540, 1110, 34, MUTED)],
    texts=[(0.05, 'top', '저녁 산행에서\n{제일 중요한 것}')], sfx=[(0.55, 'ding')])

s4 = dict(D, dur=3.6, items=[
    ('label', 0.2, '다음엔 출발 지점에서 가까운 산만 남기기', 540, 740, 40, GREEN),
    ('box', 1.2, 90, 900, 990, 1160, MINT),
    ('label', 1.3, '너는 퇴근하고 가는 산 있어?', 540, 990, 50, GREEN),
    ('label', 1.7, '댓글로 알려줘', 540, 1085, 40, INK)],
    texts=[(0.05, 'top', '고르는 건\n{결국 내 몫}')], sfx=[(1.3, 'ding')])

SCENES = [s0, s1, s2, s3, s4]

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
        build(SCENES, BASE, 'G', 'night_mountain_clip.mp4')
