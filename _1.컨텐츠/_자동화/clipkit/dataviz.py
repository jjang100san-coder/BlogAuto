# 숫자 글용 그래프 장면 — 숫자 카운트·막대·범위 점·기준선·쌓은 막대 (10/7 마일리지 클립에서 처음)
# 장면: dict(type='data', render=dataviz.render, bg=LIGHT, dur=..., items=[...], texts=[...], sfx=[...])
# items (모두 첫 값이 나타나는 시각 t, 나타난 뒤 ANIM 초 동안 자라거나 올라간다)
#   ('label', t, 글, x, y, 크기, 색[, 'l'|'m'|'r'])              글자(가운데 정렬 기본)
#   ('count', t, a, b, 형식, x, y, 크기, 색)                    a→b 로 숫자가 올라감. 형식 예 '{:,.0f}원'
#   ('box',   t, x0, y0, x1, y1, 색)                             둥근 바탕 상자
#   ('hbar',  t, 이름, 값, 최대, y, 색, 값글)                     가로 막대(왼쪽 이름, 막대 끝에 값글)
#   ('range', t, 이름, 낮음, 높음, 최대, y, 색[, 바탕색[, 반높이]])  범위 점(블로그 18개 노선 카드와 같은 모양)
#   ('vline', t, 값, 최대, y0, y1, 글, 색)                        기준선(예: 10원) — hbar·range 와 같은 가로 눈금
#   ('stack', t, y, [(이름, 값, 색), ...], 최대, 높이)            쌓은 막대(운임 + 세금 등)
from PIL import Image, ImageDraw
from tactics import font, ease, W, H

LIGHT = (250, 248, 244); INK = (28, 28, 30); NAVY = (30, 50, 95); RED = (190, 45, 60)
PINK = (252, 235, 236); GRAY = (215, 215, 215); MUTED = (125, 125, 130); WHITE = (255, 255, 255)
SKY = (226, 236, 252)
ANIM = 0.55
BAR_X, BAR_W = 360, 560      # hbar·range·vline 공통 가로 눈금


def _text(d, xy, s, sz, col, anchor='m'):
    f = font(sz)
    b = d.textbbox((0, 0), s, font=f)
    w, h = b[2] - b[0], b[3] - b[1]
    x, y = xy
    x = {'l': x, 'm': x - w / 2, 'r': x - w}[anchor] - b[0]
    d.text((x, y - h / 2 - b[1]), s, font=f, fill=col)


def _sx(v, vmax):
    return BAR_X + BAR_W * max(0.0, v) / vmax


def render(sc, t, im):
    d = ImageDraw.Draw(im)
    for it in sc.get('items', []):
        kind, t_on = it[0], it[1]
        if t < t_on:
            continue
        u = ease((t - t_on) / ANIM)
        a = min(1.0, (t - t_on) / 0.18)            # 처음 0.18초 동안 나타남
        if kind == 'label':
            _, _, s, x, y, sz, col = it[:7]
            _text(d, (x, y + (1 - a) * 18), s, sz, col, it[7] if len(it) > 7 else 'm')
        elif kind == 'count':
            _, _, va, vb, fmt, x, y, sz, col = it
            _text(d, (x, y), fmt.format(va + (vb - va) * u), sz, col)
        elif kind == 'box':
            _, _, x0, y0, x1, y1, col = it
            d.rounded_rectangle([x0, y0 + (1 - a) * 20, x1, y1 + (1 - a) * 20], radius=22, fill=col)
        elif kind == 'hbar':
            _, _, name, v, vmax, y, col, vt = it
            _text(d, (90, y), name, 38, INK, 'l')
            d.rounded_rectangle([BAR_X, y - 8, BAR_X + BAR_W, y + 8], radius=8, fill=GRAY)
            x1 = _sx(v * u, vmax)
            d.rounded_rectangle([BAR_X, y - 22, max(BAR_X + 44, x1), y + 22], radius=22, fill=col)
            if u > 0.6:
                _text(d, (max(x1, BAR_X + 44) + 18, y), vt, 40, col, 'l')  # 아주 짧은 막대도 최소 폭 뒤에
        elif kind == 'range':
            _, _, name, lo, hi, vmax, y, col = it[:8]
            bgc = it[8] if len(it) > 8 else None
            hh = it[9] if len(it) > 9 else 34     # 줄 반높이 — 18줄이면 26
            sz = 34 if hh >= 30 else 30
            if bgc:
                d.rounded_rectangle([60, y - hh, W - 60, y + hh], radius=14, fill=bgc)
            _text(d, (90, y), name, sz, INK, 'l')
            d.line([BAR_X, y, BAR_X + BAR_W, y], fill=GRAY, width=4)
            xl, xh = _sx(lo, vmax), _sx(lo + (hi - lo) * u, vmax)
            r = 13 if hh >= 30 else 10
            d.line([xl, y, xh, y], fill=col, width=r - 3)
            for x in (xl, xh):
                d.ellipse([x - r, y - r, x + r, y + r], fill=col)
            if u > 0.6:
                _text(d, (W - 70, y), f'{lo:.1f}' if lo == hi else f'{lo:.1f}~{hi:.1f}', sz - 2, col, 'r')  # 한 값이면 한 번만
        elif kind == 'vline':
            _, _, v, vmax, y0, y1, s, col = it
            x = _sx(v, vmax)
            d.line([x, y0, x, y0 + (y1 - y0) * u], fill=col, width=4)
            if u > 0.8:
                _text(d, (x, y1 + 30), s, 30, col)
        elif kind == 'stack':
            _, _, y, segs, vmax, hh = it
            x = 90.0
            span = W - 180
            for name, v, col in segs:
                w = span * v / vmax * u
                d.rounded_rectangle([x, y, x + max(w, 1), y + hh], radius=14, fill=col)
                if u > 0.7 and w > 120:
                    _text(d, (x + w / 2, y + hh / 2 - 18), name, 30, WHITE)
                    _text(d, (x + w / 2, y + hh / 2 + 22), f'{v:,.0f}원', 34, WHITE)
                x += w + 6


# ---------- 10/8 추가: 꺾은선 · 양방향 막대 · 쌍 막대 · 이미지 ----------
#   ('line', t, [(라벨, [y값...], 색), ...], (x0, y0, x1, y1), (vmin, vmax), 그리는시간[, 기준선값, 기준선글])
#        → 값 개수만큼 가로로 나눠 왼쪽부터 그려 나간다(원자료 일별값 등). 끝점에 라벨
#   ('dbar', t, 이름, 값, 최대, y, 양수색, 음수색, 값글)          가운데 0 에서 좌우로 뻗는 막대(요일 효과 등)
#   ('pair', t, 이름, a, b, 최대, y, a색, b색[, 단위])              위 a·아래 b 두 줄 막대, 끝에 숫자+단위(기본 「일」)
#   ('image', t, 경로, x0, y0, x1, y1)                               블로그에 쓴 그래프·사진을 상자 안에 맞춰 넣음
from PIL import Image as _Image
_img_cache = {}


def render_more(sc, t, im):
    d = ImageDraw.Draw(im)
    for it in sc.get('items', []):
        kind, t_on = it[0], it[1]
        if t < t_on or kind not in ('line', 'dbar', 'pair', 'image'):
            continue
        if kind == 'line':
            series, (x0, y0, x1, y1), (vmin, vmax), draw_t = it[2], it[3], it[4], it[5]
            u = min(1.0, (t - t_on) / draw_t)
            d.rectangle([x0, y0, x1, y1], outline=GRAY, width=2)
            if len(it) > 6:
                ref, reft = it[6], it[7]
                ry = y1 - (ref - vmin) / (vmax - vmin) * (y1 - y0)
                for xx in range(int(x0), int(x1), 24):
                    d.line([xx, ry, min(xx + 12, x1), ry], fill=RED, width=3)
                _text(d, (x1 - 4, ry - 22), reft, 26, RED, 'r')
            for label, vals, col in series:
                n = len(vals)
                k = max(2, int(round(n * u)))
                pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - (v - vmin) / (vmax - vmin) * (y1 - y0)) for i, v in enumerate(vals[:k])]
                d.line(pts, fill=col, width=6, joint='curve')
                ex, ey = pts[-1]
                d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=col)
                if u >= 1:
                    _text(d, (ex + 14, ey), label, 30, col, 'l')
        elif kind == 'dbar':
            _, _, name, v, vmax, y, cpos, cneg, vt = it
            u = ease((t - t_on) / ANIM)
            cx = BAR_X + BAR_W / 2
            _text(d, (90, y), name, 40, INK, 'l')
            d.line([cx, y - 34, cx, y + 34], fill=GRAY, width=3)
            w = BAR_W / 2 * v / vmax * u
            col = cpos if v >= 0 else cneg
            d.rounded_rectangle([min(cx, cx + w), y - 22, max(cx, cx + w), y + 22], radius=12, fill=col)
            if u > 0.6:
                _text(d, (cx + w + (16 if v >= 0 else -16), y), vt, 36, col, 'l' if v >= 0 else 'r')
        elif kind == 'pair':
            _, _, name, a, b, vmax, y, ca, cb = it[:9]
            unit = it[9] if len(it) > 9 else '일'   # 10/8: 제주 조합 「번」
            u = ease((t - t_on) / ANIM)
            _text(d, (90, y), name, 36, INK, 'l')
            for dy, v, col in ((-15, a, ca), (15, b, cb)):
                d.rounded_rectangle([BAR_X, y + dy - 10, BAR_X + BAR_W, y + dy + 10], radius=10, fill=(236, 236, 236))
                w = BAR_W * v / vmax * u
                if w > 1:
                    d.rounded_rectangle([BAR_X, y + dy - 10, BAR_X + max(w, 20), y + dy + 10], radius=10, fill=col)
                if u > 0.6:
                    _text(d, (BAR_X + max(w, 20) + 12, y + dy), f'{v}{unit}', 26, col, 'l')
        elif kind == 'image':
            _, _, path, x0, y0, x1, y1 = it
            if path not in _img_cache:
                from PIL import ImageOps as _IO
                _img_cache[path] = _IO.exif_transpose(_Image.open(path)).convert('RGB')  # 폰 사진 회전 정보 반영
            src = _img_cache[path]
            r = min((x1 - x0) / src.width, (y1 - y0) / src.height)
            key = (path, r)
            if key not in _img_cache:
                _img_cache[key] = src.resize((int(src.width * r), int(src.height * r)), _Image.LANCZOS)
            pic = _img_cache[key]
            a = min(1.0, (t - t_on) / 0.3)
            px, py = int(x0 + (x1 - x0 - pic.width) / 2), int(y0 + (y1 - y0 - pic.height) / 2 + (1 - a) * 30)
            im.paste(pic, (px, py))


_render_base = render


def render(sc, t, im):   # noqa: F811 — 기존 항목 + 추가 항목
    _render_base(sc, t, im)
    render_more(sc, t, im)
