# 「잘 나가는 클립」 틀 — 고정 제목 띠 + 움직이는 장면 + 말 자막 (10/10, 네이버 클립 상위 24편 조사 반영)
# 조사: Blog\_문서\클립잘나가는공통점_2026-10-10\ (clip_serp.py · clip_frames.py)
#   ① 위쪽 검은 띠에 두 줄 제목(흰 줄 + 노란 줄)이 처음부터 끝까지 고정  ② 가운데는 처음부터 움직이는 실제 장면
#   ③ 소리 꺼진 자동재생을 위해 내레이션을 그대로 말 자막으로  ④ 그래프·표 없음, 숫자는 장면 위 큰 글자 하나
#
# 장면 dict (tactics.build 에 그대로 넣는다: type='data', render=shorts.render)
#   media : 사진 경로 또는 'video:파일.mp4'(Higgsfield 움직임 컷 등)   focus=(x,y) z0 z1 : 확대 중심·처음·끝 배율
#   cx    : 사진을 꽉 채울 때 좌우 위치(0~1)                         label : 띠 아래 작은 글(촬영 날짜·「AI 생성 이미지」)
#   call  : [(t, '큰 글', 색)] 장면 위 큰 숫자·말(팝)                 cap : 말 자막 원문(화면용 — 숫자는 아라비아)
#   say   : 내레이션 대본(소리용 — 숫자는 한글). prep() 이 cap 을 내레이션 길이에 맞춰 나눠 띄운다
# 공통: HEAD = ('흰 줄', '노란 줄') — 클립 전체에 같은 제목
import os, re, subprocess
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import tactics as T

W, H = 1080, 1920
TOP = 430            # 제목 띠 높이
BOT = 1500           # 장면 아래 끝(그 아래는 검은 띠 — 네이버 화면 아래 글·버튼이 덮는 자리)
YEL = (255, 214, 0); WHITE = (255, 255, 255); BLACK = (0, 0, 0); GRAY = (170, 170, 170)
HEAD = ('', '')
_cache = {}


def _font(sz):
    return T.font(sz)


def _fit_cover(im, w, h, cx=0.5, cy=0.5):
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(cx, cy))


def _fit_contain(im, w, h):
    """카드·캡처를 자르지 않고 통째로 — 위쪽 86% 칸에 맞춰 넣고 남는 곳은 그림 가장자리 색으로 채운다.
    아래 14%는 비워 말자막이 그림 글씨를 덮지 않게(10/12 애드포스트 — 가로로 긴 캡처가 cover 로 양옆이 잘리고 자막이 카드 글씨를 덮었다)."""
    # 10/12 사용자 「글귀가 이미지 자료를 덮어 잘 안 보인다」 → 칸을 셋으로: 위 17% 큰 글 · 가운데 그림 · 아래 18% 말자막
    bg = im.getpixel((2, im.height // 2))   # 왼쪽 가운데 — 맨 위 모서리는 장식 띠(축구 카드 국기 줄)라 파란 바탕이 됐다(10/15 프리뷰)
    y0, y1 = int(h * 0.17), int(h * 0.82)
    k = min(w * 0.96 / im.width, (y1 - y0) / im.height)
    sm = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    cv = Image.new('RGB', (w, h), bg)
    cv.paste(sm, ((w - sm.width) // 2, y0 + (y1 - y0 - sm.height) // 2))
    return cv


def _media(sc):
    """장면 사진(또는 영상 프레임 목록)을 장면 칸 크기의 1.25배로 준비해 둔다(확대 여유)."""
    key = (sc['media'], sc.get('cx', 0.5), sc.get('cy', 0.5), sc.get('fit'))
    if key in _cache:
        return _cache[key]
    w, h = int(W * 1.25), int((BOT - TOP) * 1.25)
    m = sc['media']
    if m.startswith('video:'):
        path = m[6:]
        d = os.path.join(os.path.dirname(path), '_frames_' + os.path.splitext(os.path.basename(path))[0])
        if not os.path.isdir(d) or not os.listdir(d):
            os.makedirs(d, exist_ok=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', 'fps=30', os.path.join(d, 'f%04d.jpg')])
        frames = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith('.jpg'))
        val = ('video', frames, w, h)
    else:
        im = ImageOps.exif_transpose(Image.open(m)).convert('RGB')
        fit = _fit_contain(im, w, h) if sc.get('fit') == 'contain' else _fit_cover(im, w, h, sc.get('cx', 0.5), sc.get('cy', 0.5))
        val = ('img', fit, w, h)
    _cache[key] = val
    return val


def _frame_img(sc, t):
    kind, src, w, h = _media(sc)
    if kind == 'img':
        return src
    i = min(len(src) - 1, int(t * 30))
    k = (src[i], w, h)
    if k not in _cache:
        _cache[k] = _fit_cover(Image.open(src[i]).convert('RGB'), w, h)
    return _cache[k]


def _kenburns(sc, t, base):
    """확대 z0→z1(처음 0.45초는 빠르게 당기는 punch 선택)."""
    u = min(1.0, t / max(sc['dur'], 0.1))
    if sc.get('ease') == 'punch':
        u = min(1.0, t / 0.45) * 0.6 + 0.4 * u if t < 0.45 else 0.6 + 0.4 * u
    z = sc.get('z0', 1.0) + (sc.get('z1', 1.08) - sc.get('z0', 1.0)) * u
    if sc.get('whole'):   # 글이 박힌 카드·표 이미지는 가장자리까지 그대로(z=1 은 가운데 80%만 보여 제목이 잘린다 — 10/11 복귀편 카드)
        z = z / 1.25
    bw, bh = base.size
    cw, ch = W, BOT - TOP
    vw, vh = bw / 1.25 / z * 1.0, bh / 1.25 / z
    fx, fy = sc.get('focus', (0.5, 0.5))
    if sc.get('focus1'):   # 초점이 장면 동안 옮겨 간다 — 두 칸짜리 전술판에서 ① 칸 → ② 칸으로(10/13 정효볼 원리, 정지 도해만 이어지면 액티브함이 떨어진다)
        e = u * u * (3 - 2 * u)
        fx = fx + (sc['focus1'][0] - fx) * e; fy = fy + (sc['focus1'][1] - fy) * e
    x0 = min(max(fx * bw - vw / 2, 0), bw - vw); y0 = min(max(fy * bh - vh / 2, 0), bh - vh)
    return base.resize((cw, ch), Image.LANCZOS, box=(x0, y0, x0 + vw, y0 + vh))


def _text_center(d, y, s, sz, fill, stroke=0, sfill=BLACK, maxw=W - 80):
    f = _font(sz)
    while d.textlength(s, font=f) > maxw and sz > 30:
        sz -= 4; f = _font(sz)
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return sz


def head_layer():
    if 'head' in _cache:
        return _cache['head']
    im = Image.new('RGBA', (W, TOP), BLACK + (255,))
    d = ImageDraw.Draw(im)
    a, b = HEAD
    _text_center(d, 120, a, 92, WHITE)
    _text_center(d, 240, b, 96, YEL)
    _cache['head'] = im
    return im


def render(sc, t, im):
    im.paste(Image.new('RGB', (W, H), BLACK), (0, 0))
    im.paste(_kenburns(sc, t, _frame_img(sc, t)), (0, TOP))
    im.alpha_composite(head_layer(), (0, 0))
    d = ImageDraw.Draw(im)
    if sc.get('label'):
        f = _font(26); w = d.textlength(sc['label'], font=f)
        d.rectangle([W - w - 36, TOP + 14, W - 14, TOP + 56], fill=(0, 0, 0))
        d.text((W - w - 26, TOP + 20), sc['label'], font=f, fill=GRAY)
    # 큰 글(숫자 하나) — 장면 가운데, 튀어나오며
    calls = sorted(sc.get('call', []))
    for n, (t_on, s, col) in enumerate(calls):
        if t >= t_on and (n + 1 == len(calls) or t < calls[n + 1][0]):   # 다음 글이 뜨면 앞 글은 내린다
            k = T.pop((t - t_on) / 0.3)
            top_zone = sc.get('fit') == 'contain' or sc.get('call_top')   # 카드·도해는 그림 위 빈칸에(그림을 덮지 않게) · call_top 은 확대 장면 맨 위에
            sz = int((104 if top_zone else 150) * k)
            if sz > 20:
                f = _font(sz); w = d.textlength(s, font=f)
                while w > W - 60 and sz > 40:
                    sz -= 6; f = _font(sz); w = d.textlength(s, font=f)
                yc = TOP + 112 if top_zone else 700
                d.text(((W - w) / 2, yc - sz / 2), s, font=f, fill=col, stroke_width=10, stroke_fill=BLACK)
    # 말 자막 — 장면 아래쪽, 내레이션에 맞춰 덩어리로
    for t0, t1, s in sc.get('_caps', []):
        if t0 <= t < t1:
            f = _font(52)
            lines = s.split('\n')
            y = BOT - 70 - 66 * (len(lines) - 1)
            for ln in lines:
                w = d.textlength(ln, font=f)
                d.text(((W - w) / 2, y), ln, font=f, fill=WHITE, stroke_width=6, stroke_fill=BLACK)
                y += 66


def stills(scenes, base):
    """장면마다 처음·자막 중간 화면 → _build\\stills\\sheet.jpg."""
    d = os.path.join(base, '_build', 'stills'); os.makedirs(d, exist_ok=True)
    tiles = []
    for i, sc in enumerate(scenes):
        for j, t in enumerate([0.15, sc['dur'] * 0.6]):
            f = os.path.join(d, 's%02d_%d.jpg' % (i, j)); T.still(sc, t, f)
            tiles.append(Image.open(f).resize((216, 384)))
    cols = 8
    sh = Image.new('RGB', (216 * cols, 384 * ((len(tiles) + cols - 1) // cols)))
    for j, im in enumerate(tiles):
        sh.paste(im, ((j % cols) * 216, (j // cols) * 384))
    sh.save(os.path.join(d, 'sheet.jpg'), quality=88)
    print('stills', d)


# ---------- 내레이션 길이에 맞춰 장면 길이·말 자막 시간 잡기 ----------
_gaps = {}


def _narr_len(p, breath=None):
    """tactics.build 와 같은 처리(묵음 줄이기 + TEMPO + breath 쉼) 뒤 길이."""
    q = p + '.tmp.wav'
    T.narr_proc(p, q, breath)
    d = T.media_dur(q); _gaps[p] = T.narr_gaps(q); os.remove(q)
    return d


TAIL = 1.0  # 장면 말이 끝난 뒤 다음 장면까지 쉼(초) — 10/11 사용자: 「말 끝나자마자 넘어가면 속도 따라가기 힘들다」(지침 6-1-2)
UNIT = 15   # 자막 한 줄 = 의미 덩어리 하나(쉼표·마침표 사이) 15자 안 (클립 지침 6-1-2, 10/11)


def units(s):
    """쉼표·마침표·물음표에서 자른 의미 덩어리들."""
    return [p.strip() for p in re.split(r'(?<=[,.?!])\s+', s) if p.strip()]


def _wrap2(p):
    """15자 넘는 덩어리는 가운데에 가장 가까운 띄어쓰기에서 두 줄로(글자 수로 기계적으로 넘기지 않는다 — 10/11 「복귀편을 열린 / 날 밤에」)."""
    if len(p) <= UNIT or ' ' not in p:
        return p
    mid = len(p) / 2

    def score(i):   # 가운데에 가깝고, 조사·어미 뒤에서 끊고, 「설명해 / 줄」「방식 / 문제」처럼 붙은 말은 가르지 않는다(10/11)
        prev, nxt = p[:i].split(' ')[-1], p[i + 1:].split(' ')[0]
        s = abs(i - mid)
        if prev[-1] in END_OK:
            s -= 4
        else:
            s += 3
        if BOUND.match(nxt):
            s += 10
        left, right = p[:i], p[i + 1:]
        if ' ' not in right or (' ' not in left and len(left) <= 2):   # 한 줄에 「들어.」「너는」만 남기지 않는다
            s += 6
        return s
    cut = min((i for i, ch in enumerate(p) if ch == ' '), key=score)
    return p[:cut] + '\n' + p[cut + 1:]


END_OK = set('은는이가을를에엔서고면도만게데야지요며여,')
BOUND = re.compile(r'^(줄|수|것|거|건|게|적|때|듯|뿐|척|만큼|원대|원|만|천|센티|도|석|편|아니라|아니야)(이|은|는|도|야|을|를|에|마다|이야|이었어|였어|으로|로|씩|까지|부터|이면|에서|짜리)?[,.?!]?$')   # 앞말에 붙어야 하는 말 (10/12 「20만 / 원으로」 끊김 → 으로·로 등 추가)


def _chunks(s):
    """자막 덩어리 = 의미 덩어리 하나. 덩어리 안에서 글자 수로 끊지 않는다."""
    return [_wrap2(p) for p in units(s)]


def _caps_from_words(chunks, words, lead, d):
    """단어 시각(narr_words.py → nXX.words.json)으로 자막 덩어리 시작 시각을 잡는다(10/19).
    받아쓰기 글자열과 자막 글자열을 맞춰(SequenceMatcher) 덩어리 첫 글자가 어느 단어에 떨어지는지 본다. 못 맞추면 None → 비례 배분."""
    import difflib
    N = lambda s: re.sub(r'[\s,.?!·~「」"\'()\n]', '', s)
    wtext, starts = '', []
    for a, b, w in words:
        for _ in N(w):
            starts.append(a)
        wtext += N(w)
    cap = N(''.join(chunks))
    if not wtext or not cap:
        return None
    sm = difflib.SequenceMatcher(None, cap, wtext, autojunk=False)
    if sm.ratio() < 0.6:
        return None
    pos2w = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for k in range(i2 - i1):
                pos2w[i1 + k] = j1 + k
    out, off = [], 0
    for c in chunks:
        n = len(N(c)); j = next((pos2w[k] for k in range(off, off + n) if k in pos2w), None)
        t = (starts[j] if j is not None and j < len(starts) else None)
        out.append([t, c]); off += n
    if out[0][0] is None:
        out[0][0] = 0.0
    for k in range(1, len(out)):   # 못 맞춘 덩어리는 앞뒤 사이로
        if out[k][0] is None:
            nxt = next((out[m][0] for m in range(k + 1, len(out)) if out[m][0] is not None), d)
            out[k][0] = (out[k - 1][0] + nxt) / 2
    caps = []
    for k, (t, c) in enumerate(out):
        t1 = out[k + 1][0] if k + 1 < len(out) else d
        caps.append((lead + max(0.0, t - 0.05), lead + t1 + 0.05, c))
    return caps


def prep(scenes, base, ep):
    """장면 길이를 내레이션 + 0.45초 이상으로 늘리고(tactics 의 tscale 늘림을 막아 자막 시간이 맞게), 말 자막을 나눠 단다."""
    for i, sc in enumerate(scenes):
        k = sc.get('narr', i)
        p = os.path.join(base, 'narration', ep, 'n%02d.mp3' % k) if k is not None else ''
        sc['_caps'] = []
        if p and os.path.exists(p):
            d = _narr_len(p, sc.get('breath'))
            sc['dur'] = max(sc['dur'], round(d + T.NARR_LEAD + TAIL, 2))
            if sc.get('cap'):
                ch = _chunks(sc['cap'])
                wj = p[:-4] + '.words.json'   # narr_words.py 가 만든 단어 시각(10/19) — 있으면 그걸로, 없으면 비례 배분
                got = None
                if os.path.exists(wj):
                    try:
                        import json
                        got = _caps_from_words(ch, json.load(open(wj, encoding='utf-8')), T.NARR_LEAD, d)
                    except Exception as e:
                        print('words.json 못 씀(%s) — 비례 배분으로: %s' % (e, wj))
                if got:
                    sc['_caps'] = got
                    continue_prop = False
                else:
                    continue_prop = True
                if continue_prop:
                    tot = sum(len(c) for c in ch) or 1
                    t = T.NARR_LEAD
                    for c in ch:
                        span = d * len(c) / tot
                        sc['_caps'].append((t, t + span + 0.05, c)); t += span
                # 자막 경계를 가까운 말 틈(0.6초 안)으로 당긴다 — 쉼(breath) 뒤 자막이 미리 뜨지 않게(10/11)
                mids = [T.NARR_LEAD + (a + b) / 2 for a, b in _gaps.get(p, [])]
                for j in (range(1, len(sc['_caps'])) if continue_prop else ()):   # 단어 시각으로 잡았으면 틈으로 안 당긴다(10/19)
                    t0 = sc['_caps'][j][0]
                    near = min(mids, key=lambda m: abs(m - t0), default=None)
                    if near is not None and abs(near - t0) < 0.6 and near > sc['_caps'][j - 1][0] + 0.3:
                        a0, _, c0 = sc['_caps'][j - 1]; _, b1, c1 = sc['_caps'][j]
                        sc['_caps'][j - 1] = (a0, near, c0); sc['_caps'][j] = (near, b1, c1)
                t0, _, c = sc['_caps'][-1]
                sc['_caps'][-1] = (t0, sc['dur'], c)   # 쉼 동안 마지막 자막은 남겨 둔다
        sc['qa_strings'] = [HEAD[0], HEAD[1]] + [c[1] for c in sc.get('call', [])] + ([sc['cap']] if sc.get('cap') else []) \
            + ([sc['label']] if sc.get('label') else [])
    return scenes
