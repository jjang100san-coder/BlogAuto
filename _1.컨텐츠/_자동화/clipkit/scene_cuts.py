# -*- coding: utf-8 -*-
# 내 영상에서 컷 후보 자동으로 — 장면이 바뀌는 곳을 찾아 장면마다 정지 화면 한 장 + 표 (2026.10.19)
#   콘티(클립 지침 3장)를 짤 때 긴 산행·축제 영상을 처음부터 돌려 보지 않아도 된다. 고르는 건 사람이 한다.
#   엔진: PySceneDetect 0.7(ContentDetector — 화면 내용이 확 바뀌는 곳). pip install scenedetect opencv-python-headless
#   남의 영상엔 쓰지 않는다(마스터 6-7) — 내 사진·영상·화면 녹화만(클립 지침 2-2)
#
#   python scene_cuts.py <영상.mp4> [저장폴더] [--th 27] [--min 1.5]
#     → <저장폴더>\scenes.csv (번호·시작·끝·길이)  ·  <저장폴더>\scene_NN_mm-ss.jpg (장면 가운데 프레임, 세로 영상이면 그대로)
#       <저장폴더>\_scenes_sheet.jpg (한눈에 — 번호·시각 박아서)
#     --th   민감도(기본 27. 작을수록 잘게 나뉜다. 산행처럼 화면이 계속 흐르면 35~40)
#     --min  이보다 짧은 장면은 앞 장면에 붙인다(초)
import os, sys, csv, subprocess
from PIL import Image, ImageDraw, ImageFont

FONT = next((p for p in ('C:/Windows/Fonts/malgunbd.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') if os.path.exists(p)), None)


def mmss(t):
    return '%02d-%02d' % (int(t) // 60, int(t) % 60)


def detect_scenes(video, th=27.0, min_len=1.5):
    from scenedetect import detect, ContentDetector
    scenes = detect(video, ContentDetector(threshold=th, min_scene_len=int(min_len * 15)))
    out = []
    for a, b in scenes:
        s, e = (a.seconds if hasattr(a, 'seconds') else a.get_seconds()), (b.seconds if hasattr(b, 'seconds') else b.get_seconds())
        if out and e - s < min_len:
            out[-1] = (out[-1][0], e)
        else:
            out.append((s, e))
    return out


def grab(video, t, out, h=640):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.3f' % t, '-i', video, '-frames:v', '1', '-vf', 'scale=-2:%d' % h, out], check=True)


def sheet(items, out, cols=4):
    ims = [Image.open(p) for _, _, _, p in items]
    if not ims:
        return
    w, h = ims[0].size; rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * w, rows * h), (20, 20, 20)); d = ImageDraw.Draw(S)
    f = ImageFont.truetype(FONT, max(18, h // 18)) if FONT else None
    for i, (n, s, e, p) in enumerate(items):
        im = ims[i].resize((w, h)); x, y = (i % cols) * w, (i // cols) * h
        S.paste(im, (x, y))
        label = '%02d  %s~%s  %.1fs' % (n, mmss(s).replace('-', ':'), mmss(e).replace('-', ':'), e - s)
        d.rectangle([x, y, x + w, y + (h // 12)], fill=(0, 0, 0))
        d.text((x + 8, y + 4), label, font=f, fill=(255, 214, 0))
    S.save(out, quality=85)


def main(video, dest=None, th=27.0, min_len=1.5):
    dest = dest or os.path.join(os.path.dirname(os.path.abspath(video)), '_scenes'); os.makedirs(dest, exist_ok=True)
    sc = detect_scenes(video, th, min_len)
    items = []
    with open(os.path.join(dest, 'scenes.csv'), 'w', newline='', encoding='utf-8-sig') as fp:
        w = csv.writer(fp); w.writerow(['번호', '시작(초)', '끝(초)', '길이(초)', '정지화면'])
        for n, (s, e) in enumerate(sc, 1):
            p = os.path.join(dest, 'scene_%02d_%s.jpg' % (n, mmss(s)))
            grab(video, (s + e) / 2, p); items.append((n, s, e, p))
            w.writerow([n, '%.2f' % s, '%.2f' % e, '%.2f' % (e - s), os.path.basename(p)])
    sheet(items, os.path.join(dest, '_scenes_sheet.jpg'))
    print('장면 %d개 → %s' % (len(sc), dest))
    for n, s, e, p in items:
        print('  %02d  %6.1f ~ %6.1f  (%.1fs)  %s' % (n, s, e, e - s, os.path.basename(p)))
    return items


if __name__ == '__main__':
    a = sys.argv[1:]
    g = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    pos = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or not a[i - 1].startswith('--'))]
    main(pos[0], pos[1] if len(pos) > 1 else None, g('--th', 27.0), g('--min', 1.5))
