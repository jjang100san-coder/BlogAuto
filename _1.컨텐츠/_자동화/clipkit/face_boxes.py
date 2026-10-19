# -*- coding: utf-8 -*-
# 얼굴 상자 자동 검출 → make_clip 의 mosaic=[(x0,y0,x1,y1)] 비율 좌표 (2026.10.19)
#   지금은 얼굴 위치를 눈으로 재서 적는다(클립 지침 3-2·4-1). 이 스크립트가 후보 상자를 찾아 주고, 가리는 건 예전처럼 make_clip 의 굵은 모자이크(6칸)가 한다.
#   검출기: deface 에 들어 있는 CenterFace(onnx, 모델 동봉 — 내려받기 없음). pip install deface
#   ⚠ 검출은 후보일 뿐 — 못 찾은 얼굴(옆얼굴·작은 얼굴·뒷모습)은 여전히 눈으로. 지침 7장 「얼굴·어린이·번호판 없음」 체크는 그대로
#
#   python face_boxes.py <사진 또는 폴더> [--pad 0.25] [--th 0.3] [--preview]
#     → 사진마다  mosaic=[(x0, y0, x1, y1), ...]  한 줄 (SEGMENTS 에 그대로 붙여 넣는다)
#     --pad     상자를 머리카락까지 덮게 위로·옆으로 늘리는 비율(기본 0.25 = 25%)
#     --th      검출 문턱(기본 0.3. 못 찾으면 0.15 까지 내려 본다 — 대신 오검출이 는다)
#     --preview 사진 옆에 _faces.jpg 로 상자·모자이크 미리보기(6칸 블록, make_clip 과 같은 꼴)
import os, sys, glob
import numpy as np
from PIL import Image, ImageDraw

EXT = ('.jpg', '.jpeg', '.png', '.webp')
_cf = None


def _det():
    global _cf
    if _cf is None:
        from deface.centerface import CenterFace
        _cf = CenterFace(backend='auto')
    return _cf


def boxes(path, th=0.3, pad=0.25):
    """[(x0, y0, x1, y1, score)] 비율 좌표. pad 만큼 위·옆으로 넓힌다(머리카락)."""
    im = Image.open(path).convert('RGB')
    W, H = im.size
    arr = np.asarray(im)[:, :, ::-1]   # CenterFace 는 BGR
    dets, _ = _det()(arr, threshold=th)
    out = []
    for x0, y0, x1, y1, sc in dets:
        w, h = x1 - x0, y1 - y0
        x0 -= w * pad; x1 += w * pad; y0 -= h * pad * 1.4; y1 += h * pad * 0.4   # 위를 더(이마·머리), 아래는 턱만
        out.append((round(max(0, x0 / W), 3), round(max(0, y0 / H), 3), round(min(1, x1 / W), 3), round(min(1, y1 / H), 3), round(float(sc), 2)))
    return sorted(out, key=lambda b: (b[0], b[1]))


def preview(path, bx, out):
    """상자 + 6칸 굵은 모자이크 미리보기(make_clip mosaic 과 같은 블록 수)."""
    im = Image.open(path).convert('RGB'); W, H = im.size
    for x0, y0, x1, y1, _ in bx:
        X0, Y0, X1, Y1 = int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)
        if X1 <= X0 or Y1 <= Y0:
            continue
        n = 6; cell = max(1, (X1 - X0) // n)
        crop = im.crop((X0, Y0, X1, Y1))
        small = crop.resize((n, max(1, (Y1 - Y0) // cell)), Image.BOX)
        im.paste(small.resize(crop.size, Image.NEAREST), (X0, Y0))
        ImageDraw.Draw(im).rectangle([X0, Y0, X1, Y1], outline=(255, 214, 0), width=max(2, W // 400))
    im.save(out, quality=88)


def main(target, th=0.3, pad=0.25, prev=False):
    files = sorted(f for f in glob.glob(os.path.join(target, '*')) if f.lower().endswith(EXT)) if os.path.isdir(target) else [target]
    for f in files:
        bx = boxes(f, th, pad)
        s = ', '.join('(%.3f, %.3f, %.3f, %.3f)' % b[:4] for b in bx)
        print('%s  얼굴 %d  mosaic=[%s]%s' % (os.path.basename(f), len(bx), s, '  신뢰도 ' + ' '.join(str(b[4]) for b in bx) if bx else ''))
        if prev and bx:
            o = os.path.splitext(f)[0] + '_faces.jpg'; preview(f, bx, o); print('   미리보기:', o)


if __name__ == '__main__':
    a = sys.argv[1:]
    g = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    main(a[0], g('--th', 0.3), g('--pad', 0.25), '--preview' in a)
