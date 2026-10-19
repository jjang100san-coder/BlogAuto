# 클립 엔진 — 전술판(pitch)·카드(card)·외부 장면(render) + 자막·효과음·조립 (10/7 모레노호 4연전에서 처음, 공용으로 옮김)
# 장면(scene) 목록을 받아 1080x1920 세로 영상으로 만든다. 장면 정의는 ep1.py·ep2.py
#
# 좌표: 경기장 x 0(왼쪽)~1(오른쪽), y 0(위 골라인 = 상대 골문)~1(아래 골라인 = 한국 골문)
# 장면 종류
#   card  : 짙은 바탕 위 글 카드. items=[(t, 'row'|'big'|'text', ...)]
#   pitch : 경기장. view=(y0,y1) 보이는 구간, players={id: (팀, x, y, 이름표)},
#           moves=[(id, t0, t1, (x,y))], ball=[('at', t, id) | ('pass', t0, t1, id_from, id_to)],
#           arrows=[(t_on, t_off, from, to, 색, dashed)], zones=[(t_on, t_off, (x,y), rx, ry, 색, 이름표)],
#           tags=[(t_on, t_off, id 또는 (x,y), 글)]
#   공통  : dur(최소 길이), texts=[(t_on, 'top'|'mid'|'bot'|'small', 글[, t_off])], sfx=[(t, 'ding'|'kick')], dim=(t, 세기)
# 내레이션 narration/<ep>/nXX.mp3 가 있으면 그 길이에 맞춰 장면을 늘리고 마지막 상태로 멈춰 둔다
import os, re, math, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
SS = 2  # 2배로 그려서 줄여 계단 현상 없애기
FONT_B = 'C:/Windows/Fonts/malgunbd.ttf'
BG = (36, 22, 26); PANEL = (52, 36, 40); PANEL2 = (68, 50, 54)
CREAM = (244, 240, 232); MUTED = (190, 170, 172); ACCENT = (150, 220, 200)
KOR = (208, 119, 63); OPP = (92, 134, 200); RED = (232, 108, 100); GREEN = (120, 200, 140); AMBER = (236, 190, 100)
PITCH = (32, 52, 48); LINE = (96, 124, 118); BALL = (250, 250, 250)
YELLOW = (255, 214, 0); WHITE = (255, 255, 255)
TEAM = {'kor': KOR, 'opp': OPP, 'gk': (200, 205, 215)}
PY0, PY1 = 560, 1600   # 경기장이 차지하는 화면 세로 구간
NARR_LEAD = 0.15
XF = 0.12
TEMPO = 1.08
MAX_STRETCH = 1.35  # 움직임은 최대 1.35배까지만 늘린다(더 느리면 늘어져 보임) — 나머지는 끝 상태로 멈춤
SFX_VOL = {'whoosh': 0.32, 'ding': 0.28, 'kick': 0.5}
_fonts = {}


def font(sz):
    if sz not in _fonts:
        _fonts[sz] = ImageFont.truetype(FONT_B, sz)
    return _fonts[sz]


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def pop(u):
    """0→1 로 튀어나오는 비율(조금 넘쳤다 돌아옴)."""
    u = min(1.0, max(0.0, u))
    return 1 + 2.2 * (u - 1) ** 3 + 1.2 * (u - 1) ** 2 if u < 1 else 1.0


# ---------- 자막 (make_clip 과 같은 모양) ----------
def parse(line):
    out = []
    for i, part in enumerate(re.split(r'[{}]', line)):
        if part:
            out.append((part, YELLOW if i % 2 else WHITE))
    return out


def text_layer(text, kind):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    sz = {'top': 84, 'mid': 70, 'bot': 64, 'small': 40}[kind]
    lines = text.split('\n')
    while True:
        f = font(sz)
        widths = [sum(d.textlength(t, font=f) for t, _ in parse(l)) for l in lines]
        if max(widths) <= W - 140 or sz <= 36:
            break
        sz -= 4
    gap = int(sz * 0.32); lh = sz + gap; bh = lh * len(lines) - gap
    y0 = {'top': 270, 'mid': 1300 - bh // 2, 'bot': 1660, 'small': 190}[kind]
    if kind != 'small':
        bw = max(widths)
        d.rounded_rectangle([(W - bw) / 2 - 44, y0 - 28, (W + bw) / 2 + 44, y0 + bh + 38], radius=28, fill=(0, 0, 0, 150))
    for l, lw in zip(lines, widths):
        x = (W - lw) / 2
        for t, c in parse(l):
            d.text((x, y0), t, font=f, fill=c if kind != 'small' else MUTED, stroke_width=5 if kind != 'small' else 0,
                   stroke_fill=(0, 0, 0))
            x += d.textlength(t, font=f)
        y0 += lh
    return img


def paste_pop(base, layer, u):
    """layer(전체 화면 RGBA)를 0.88→1배로 키우며 나타나게."""
    if u >= 1:
        base.alpha_composite(layer); return
    e = 1 - (1 - max(0.0, u)) ** 3
    s = 0.88 + 0.12 * e
    w, h = int(W * s), int(H * s)
    sm = layer.resize((w, h), Image.BILINEAR)
    sm.putalpha(sm.getchannel('A').point(lambda v: int(v * e)))
    base.alpha_composite(sm, ((W - w) // 2, (H - h) // 2))


# ---------- 경기장 ----------
class View:
    def __init__(self, y0, y1):
        self.y0, self.y1 = y0, y1
        self.L = (PY1 - PY0) / (y1 - y0)          # 경기장 길이 1 = 몇 px
        self.Wd = self.L * 68 / 105                # 경기장 폭 1 = 몇 px
        self.x0 = W / 2 - self.Wd / 2

    def p(self, x, y):
        return ((self.x0 + x * self.Wd) * SS, (PY0 + (y - self.y0) * self.L) * SS)


def draw_pitch(d, v):
    lw = 3 * SS
    X = lambda x: (v.x0 + x * v.Wd) * SS
    Y = lambda y: (PY0 + (y - v.y0) * v.L) * SS
    d.rectangle([X(0), Y(0), X(1), Y(1)], fill=PITCH, outline=LINE, width=lw)
    d.line([X(0), Y(0.5), X(1), Y(0.5)], fill=LINE, width=lw)
    r = 9.15 / 68 * v.Wd * SS
    cx, cy = X(0.5), Y(0.5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=lw)
    for top in (True, False):
        for bw, bd in ((40.3 / 68, 16.5 / 105), (18.3 / 68, 5.5 / 105)):
            ya, yb = (0, bd) if top else (1 - bd, 1)
            d.rectangle([X(0.5 - bw / 2), Y(ya), X(0.5 + bw / 2), Y(yb)], outline=LINE, width=lw)
        gy = Y(0) if top else Y(1)
        d.rectangle([X(0.5 - 3.66 / 68), gy - (8 * SS if top else 0), X(0.5 + 3.66 / 68), gy + (0 if top else 8 * SS)],
                    fill=(70, 80, 90))


def tag(d, xy, text, size=26, fill=CREAM, bg=(16, 10, 12)):
    f = font(size * SS)
    x, y = xy
    b = d.textbbox((0, 0), text, font=f); tw, th = b[2] - b[0], b[3] - b[1]
    d.rounded_rectangle([x - tw / 2 - 10 * SS, y - th / 2 - 8 * SS, x + tw / 2 + 10 * SS, y + th / 2 + 10 * SS],
                        radius=9 * SS, fill=bg)
    d.text((x - tw / 2 - b[0], y - th / 2 - b[1]), text, font=f, fill=fill)


def arrow(d, p1, p2, col, dashed=False, w=5, head=18, prog=1.0):
    w *= SS; head *= SS
    x1, y1 = p1; x2, y2 = p2
    x2, y2 = x1 + (x2 - x1) * prog, y1 + (y2 - y1) * prog   # 화살표가 그려지며 늘어난다
    ang = math.atan2(y2 - y1, x2 - x1); L = math.hypot(x2 - x1, y2 - y1)
    if L < head:
        return
    if dashed:
        t = 0
        while t < L - head:
            a, b = t, min(t + 16 * SS, L - head * 0.8)
            d.line([x1 + math.cos(ang) * a, y1 + math.sin(ang) * a, x1 + math.cos(ang) * b, y1 + math.sin(ang) * b], fill=col, width=w)
            t += 28 * SS
    else:
        d.line([x1, y1, x2 - math.cos(ang) * head * 0.8, y2 - math.sin(ang) * head * 0.8], fill=col, width=w)
    d.polygon([(x2, y2), (x2 - math.cos(ang - 0.42) * head, y2 - math.sin(ang - 0.42) * head),
               (x2 - math.cos(ang + 0.42) * head, y2 - math.sin(ang + 0.42) * head)], fill=col)


def _spline(pts, u):
    """경유점들을 지나는 Catmull-Rom 곡선 위 u(0~1) 지점 — 경유점에서 멈추지 않고 이어 달린다(10/10)."""
    if len(pts) == 2:
        (x0, y0), (x1, y1) = pts
        return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    tot = sum(seg) or 1.0
    s = u * tot
    i = 0
    while i < len(seg) - 1 and s > seg[i]:
        s -= seg[i]; i += 1
    v = s / (seg[i] or 1.0)
    p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
    v2, v3 = v * v, v * v * v
    return tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * v + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * v2
                        + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * v3) for k in (0, 1))


def pos_at(sc, pid, t):
    """moves 의 목적지는 (x,y) 하나 또는 [(x,y), (x,y), …] 경유점 목록. 목록이면 곡선으로 한 번에(처음·끝만 감속)."""
    team, x, y, _ = sc['players'][pid]
    for mid, t0, t1, to in sorted([m for m in sc.get('moves', []) if m[0] == pid], key=lambda m: m[1]):
        pts = [(x, y)] + (list(to) if isinstance(to, list) else [to])
        if t >= t1:
            x, y = pts[-1]
        elif t > t0:
            x, y = _spline(pts, ease((t - t0) / (t1 - t0)))
            break
        else:
            break
    return x, y


def ball_at(sc, t):
    holder, pos = None, None
    for ev in sorted(sc.get('ball', []), key=lambda e: e[1]):
        if ev[0] == 'at' and t >= ev[1]:
            holder = ev[2]
        elif ev[0] == 'pass' and t >= ev[1]:
            _, t0, t1, a, b = ev
            if t >= t1:
                holder = b
            else:
                pa = pos_at(sc, a, t0) if isinstance(a, str) else a
                pb = pos_at(sc, b, t) if isinstance(b, str) else b
                e = ease((t - t0) / (t1 - t0))
                return (pa[0] + (pb[0] - pa[0]) * e, pa[1] + (pb[1] - pa[1]) * e)
    if holder is None:
        return None
    return pos_at(sc, holder, t) if isinstance(holder, str) else holder


def resolve(sc, ref, t):
    return pos_at(sc, ref, t) if isinstance(ref, str) else ref


def render_pitch(sc, t, im):
    v = View(*sc['view'])
    big = Image.new('RGBA', (W * SS, H * SS), PITCH + (255,) if sc.get('fill_pitch') else BG + (255,))
    d = ImageDraw.Draw(big)
    draw_pitch(d, v)
    # 구역
    for t_on, t_off, c, rx, ry, col, label in sc.get('zones', []):
        if t_on <= t < t_off:
            u = (t - t_on) / 0.35
            k = pop(u)
            if k < 0.02:
                continue
            pulse = 0.85 + 0.15 * math.sin((t - t_on) * 5) if u >= 1 else 1
            cx, cy = v.p(*resolve(sc, c, t))
            ov = Image.new('RGBA', big.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).ellipse([cx - rx * v.Wd * SS * k, cy - ry * v.L * SS * k, cx + rx * v.Wd * SS * k, cy + ry * v.L * SS * k],
                                       fill=col + (int(95 * pulse),), outline=col + (230,), width=4 * SS)
            big.alpha_composite(ov)
            d = ImageDraw.Draw(big)
    # 화살표
    for t_on, t_off, a, b, col, dashed in sc.get('arrows', []):
        if t_on <= t < t_off:
            arrow(d, v.p(*resolve(sc, a, t_on)), v.p(*resolve(sc, b, t_on)), col, dashed, prog=ease((t - t_on) / 0.35))
    # 선수 — 원을 다 그린 뒤 공, 그다음 이름표(10/10: 뒤에 그린 선수 원이 앞 선수 이름표를 덮던 것 고침)
    r = 22 * SS
    pos = {pid: v.p(*pos_at(sc, pid, t)) for pid in sc['players']}
    for pid, (team, x, y, label) in sc['players'].items():
        px, py = pos[pid]
        d.ellipse([px - r, py - r, px + r, py + r], fill=TEAM[team], outline=CREAM, width=3 * SS)
    # 공
    b = ball_at(sc, t)
    if b:
        bx, by = v.p(*b)
        rb = 11 * SS
        bx += 16 * SS; by -= 16 * SS
        d.ellipse([bx - rb, by - rb, bx + rb, by + rb], fill=BALL, outline=(20, 20, 20), width=2 * SS)
    for pid, (team, x, y, label) in sc['players'].items():
        if label:
            px, py = pos[pid]
            tag(d, (px, py + r + 28 * SS), label, 30)
    # 구역 이름표·글 태그(맨 위)
    for t_on, t_off, c, rx, ry, col, label in sc.get('zones', []):
        if label and t_on + 0.2 <= t < t_off:
            cx, cy = v.p(*resolve(sc, c, t))
            tag(d, (cx, cy + ry * v.L * SS * 0.55), label, 32, fill=col)  # 가운데 선수 이름표와 안 겹치게 아래쪽
    for t_on, t_off, ref, text in sc.get('tags', []):
        if t_on <= t < t_off:
            x, y = resolve(sc, ref, t)
            tag(d, v.p(x, y), text, 28, fill=AMBER)
    small = big.resize((W, H), Image.LANCZOS)
    if tuple(sc['view']) != (0.0, 1.0):   # 일부만 확대한 판은 화면 구간(PY0~PY1) 밖을 잘라 낸다 — 위쪽 제목·아래 말 자막을 덮지 않게(10/11)
        mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).rectangle([0, PY0 - 8, W, PY1 + 8], fill=255)
        small.putalpha(Image.composite(small.getchannel('A'), Image.new('L', (W, H), 0), mask))
    im.alpha_composite(small)


def render_card(sc, t, im):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 10], fill=ACCENT)
    for item in sc.get('items', []):
        t_on, kind = item[0], item[1]
        if t < t_on:
            continue
        u = (t - t_on) / 0.3
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        if kind == 'row':   # ('row', 월, 상대, 점수, 색, 한 줄, y)
            _, _, mon, opp, score, col, line, y = item
            ld.rounded_rectangle([70, y, W - 70, y + 150], radius=22, fill=PANEL)
            ld.text((110, y + 28), mon, font=font(34), fill=MUTED)
            ld.text((220, y + 18), opp, font=font(54), fill=CREAM)
            ld.text((220, y + 92), line, font=font(32), fill=MUTED)
            if score:  # 점수 없는 줄(E조 일정·체크 목록)은 알약을 그리지 않는다
                f = font(46); tw = ld.textlength(score, font=f)
                ld.rounded_rectangle([W - 110 - tw - 36, y + 40, W - 110, y + 110], radius=35, fill=col)
                ld.text((W - 110 - tw - 18, y + 46), score, font=f, fill=(30, 20, 22))
        elif kind == 'big':  # ('big', 글, y, 크기, 색)
            _, _, text, y, sz, col = item
            f = font(sz); tw = ld.textlength(text, font=f)
            ld.text(((W - tw) / 2, y), text, font=f, fill=col)
        paste_pop(im, layer, u)



def narr_gaps(q):
    """말 사이 틈 [(시작, 끝)] — 앞뒤 묵음은 뺀다. breath 번호·자막 경계 맞추기에 쓴다."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', q, '-af', 'silencedetect=noise=-40dB:d=0.06', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    total = media_dur(q)
    return [(a, b) for a, b in zip(st, en) if a > 0.05 and b < total - 0.05]


def narr_proc(p, q, breath=None):
    """내레이션 처리(긴 묵음 줄이기 + TEMPO) → q(wav). breath=[(n, 초)] : n번째(0부터) 말 사이 틈을 그 길이로 늘린다
    (10/11 사용자: 「반팔이야? 외투야? / 내가 간 나흘은」 사이가 빠르다 → 0.5초 쉼). shorts.prep 도 이걸 써서 자막 시간이 맞는다."""
    run(['ffmpeg', '-y', '-v', 'error', '-i', p, '-af',
         f'silenceremove=stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB:stop_silence=0,atempo={TEMPO}', q])
    if not breath:
        return q
    gaps = narr_gaps(q)
    import wave
    with wave.open(q, 'rb') as w:
        prm = w.getparams(); data = w.readframes(prm.nframes)
    fb = prm.sampwidth * prm.nchannels
    ins = []
    for n, sec in breath:
        if n >= len(gaps):
            print('breath: %d번째 틈 없음(틈 %d개) — %s' % (n, len(gaps), p)); continue
        a, b = gaps[n]
        ins.append((int((a + b) / 2 * prm.framerate), max(0.0, sec - (b - a))))
    for at, add in sorted(ins, reverse=True):
        data = data[:at * fb] + b'\x00' * (int(add * prm.framerate) * fb) + data[at * fb:]
    with wave.open(q, 'wb') as w:
        w.setparams(prm); w.writeframes(data)
    return q


def media_dur(path):
    """미디어 길이(초). ffprobe 가 윈도우 앱 제어 정책에 막혀서(10/7) ffmpeg 출력의 Duration 으로 잰다."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path], capture_output=True, text=True, encoding='utf-8', errors='replace')
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    if not m:
        raise SystemExit('길이를 못 읽음: ' + path)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


# ---------- 효과음 ----------
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])


def make_sfx(tmp):
    w = os.path.join(tmp, 'whoosh.wav')
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=0.32:c=pink:a=0.9:r=44100',
         '-af', 'highpass=f=500,lowpass=f=5000,afade=t=in:d=0.16:curve=exp,afade=t=out:st=0.16:d=0.16,aformat=channel_layouts=stereo', w])
    dg = os.path.join(tmp, 'ding.wav')
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', "aevalsrc='0.6*sin(2*PI*1568*t)*exp(-7*t)+0.3*sin(2*PI*3136*t)*exp(-11*t)':d=0.6:s=44100",
         '-af', 'aformat=channel_layouts=stereo', dg])
    k = os.path.join(tmp, 'kick.wav')  # 공 차는 「톡」: 낮은 사인 + 짧은 잡음
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', "aevalsrc='0.9*sin(2*PI*140*t)*exp(-30*t)+0.25*(random(0)-0.5)*exp(-60*t)':d=0.15:s=44100",
         '-af', 'aformat=channel_layouts=stereo', k])
    return {'whoosh': w, 'ding': dg, 'kick': k}


# ---------- 조립 ----------
def frame(sc, t, cache):
    t = t / sc.get('tscale', 1.0)   # 내레이션이 길면 움직임 전체를 늘린다(멈춘 화면 줄이기)
    im = Image.new('RGBA', (W, H), sc.get('bg', BG) + (255,))
    if sc['type'] == 'pitch':
        render_pitch(sc, t, im)
    elif sc['type'] == 'card':
        render_card(sc, t, im)
    else:
        sc['render'](sc, t, im)   # 다른 모듈의 장면(예: dataviz.render)
    if sc.get('dim') and t >= sc['dim'][0]:
        a = int(sc['dim'][1] * ease((t - sc['dim'][0]) / 0.5))
        im.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, a)))
    for tx in sc.get('texts', []):
        t_on, kind, text = tx[:3]
        t_off = tx[3] if len(tx) > 3 else 1e9   # 4번째 값이 있으면 그 시각에 사라진다(자막 갈아 끼우기)
        if t_on <= t < t_off:
            key = (kind, text)
            if key not in cache:
                cache[key] = text_layer(text, kind)
            paste_pop(im, cache[key], (t - t_on) * FPS / 6)
    if getattr(sc.get('render'), '__module__', '') != 'shorts':   # shorts.render 는 자막을 직접 그린다
        draw_caps(sc, t * sc.get('tscale', 1.0), im)
    return im.convert('RGB')


CAP_Y = 1430   # 말 자막 마지막 줄 위치(shorts 와 같은 자리). 축구 카드·전술판은 이 아래 ~1500 을 비워 둔다


def draw_caps(sc, t, im):
    """말 자막(shorts.prep 이 만든 _caps) — 축구 카드·전술판 클립에도 같은 자막을 쓴다(10/11 클립 지침 6-1-2)."""
    caps = [c for c in sc.get('_caps', []) if c[0] <= t < c[1]]
    if not caps:
        return
    d = ImageDraw.Draw(im); f = font(52)
    lines = caps[0][2].split('\n'); y = CAP_Y - 66 * (len(lines) - 1)
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, y), ln, font=f, fill=(255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0)); y += 66


def still(sc, t, path):
    frame(sc, t, {}).save(path, quality=92)


# ---------- 전술판 검수: 글자 가림·이름 오타 (10/10 사용자: 「설명용이니 글씨가 가려지거나 잘못 적히면 안 된다」) ----------
_tbox_cache = {}


def _tag_box(xy, text, size):
    """tag() 가 그리는 이름표 상자(화면 px)."""
    f = font(size * SS)
    b = ImageDraw.Draw(Image.new('L', (1, 1))).textbbox((0, 0), text, font=f)
    tw, th = (b[2] - b[0]) / SS, (b[3] - b[1]) / SS
    x, y = xy[0] / SS, xy[1] / SS
    return (x - tw / 2 - 10, y - th / 2 - 8, x + tw / 2 + 10, y + th / 2 + 10)


def _text_box(text, kind):
    key = (text, kind)
    if key not in _tbox_cache:
        _tbox_cache[key] = text_layer(text, kind).getchannel('A').getbbox()
    return _tbox_cache[key]


def _hit(a, b, pad=4):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def layout(sc, t):
    """t 시각 화면의 글자 상자들과 가리면 안 되는 점(선수·공)."""
    texts, dots = [], []
    for tx in sc.get('texts', []):
        t_on, kind, s = tx[:3]
        if t_on <= t < (tx[3] if len(tx) > 3 else 1e9):
            texts.append(('자막 ' + s.replace('\n', ' ').replace('{', '').replace('}', ''), _text_box(s, kind)))
    if getattr(sc.get('render'), '__module__', '') != 'shorts':   # 축구 카드·전술판의 말 자막 자리(shorts 장면은 사진 위라 제외)
        for c0, c1, s in sc.get('_caps', []):
            if c0 <= t < c1:
                n = s.count('\n')
                texts.append(('말자막 ' + s.replace('\n', ' '), (60, CAP_Y - 66 * n - 6, W - 60, CAP_Y + 62)))
    if sc['type'] == 'data':   # 숫자·카드 장면의 글(label·count) 상자도 본다(10/10 검산 보강)
        dr = ImageDraw.Draw(Image.new('L', (1, 1)))
        for it in sc.get('items', []):
            if it[1] > t or it[0] not in ('label', 'count'):
                continue
            if it[0] == 'label':
                s, x, y, sz = it[2], it[3], it[4], it[5]; al = it[7] if len(it) > 7 else 'm'
            else:
                s, x, y, sz, al = it[4].format(it[3]), it[5], it[6], it[7], 'm'
            b = dr.textbbox((0, 0), s, font=font(sz)); w, h = b[2] - b[0], b[3] - b[1]
            x0 = {'l': x, 'm': x - w / 2, 'r': x - w}[al]
            texts.append(('글 ' + s, (x0, y - h / 2, x0 + w, y + h / 2)))
    if sc['type'] != 'pitch':
        return texts, dots
    v = View(*sc['view'])
    r = 22 * SS
    for pid, (team, x, y, label) in sc['players'].items():
        px, py = v.p(*pos_at(sc, pid, t))
        dots.append(('선수 ' + (label or pid), (px / SS - 22, py / SS - 22, px / SS + 22, py / SS + 22)))
        if label:
            texts.append(('이름표 ' + label, _tag_box((px, py + r + 28 * SS), label, 30)))
    b = ball_at(sc, t)
    if b:
        bx, by = v.p(*b)
        dots.append(('공', (bx / SS + 5, by / SS - 27, bx / SS + 27, by / SS - 5)))
    for t_on, t_off, c, rx, ry, col, label in sc.get('zones', []):
        if label and t_on + 0.2 <= t < t_off:
            cx, cy = v.p(*resolve(sc, c, t))
            texts.append(('구역 ' + label, _tag_box((cx, cy + ry * v.L * SS * 0.55), label, 32)))
    for t_on, t_off, ref, s in sc.get('tags', []):
        if t_on <= t < t_off:
            texts.append(('태그 ' + s, _tag_box(v.p(*resolve(sc, ref, t)), s, 28)))
    return texts, dots


def audit(scenes, post_text=None, step=0.1):
    """장면마다 step 초 간격으로 ① 글자끼리 겹침 ② 글자가 선수·공을 덮음 ③ 화면 밖 글자를 찾고,
    post_text(발행본 본문)를 주면 ④ 이름표·구역·태그 글이 발행본에 있는지(띄어쓰기 무시) 본다. 문제 목록을 돌려준다."""
    probs, seen = [], set()
    for i, sc in enumerate(scenes):
        n = int(sc['dur'] / step) + 1
        for k in range(n):
            t = k * step
            texts, dots = layout(sc, t)
            for a in range(len(texts)):
                na, ba = texts[a]
                if ba and (ba[0] < 20 or ba[2] > W - 20 or ba[1] < 20 or ba[3] > H - 20):
                    key = (i, '밖', na)
                    if key not in seen:
                        seen.add(key); probs.append((i, round(t, 1), '화면 밖', na, ''))
                for c in range(a + 1, len(texts)):
                    nb, bb = texts[c]
                    both_sub = na.startswith('자막') and nb.startswith('자막')   # small 라벨과 top 자막은 원래 붙어 있다
                    if ba and bb and _hit(ba, bb, pad=-2 if both_sub else 4):
                        key = (i, '겹침', na, nb)
                        if key not in seen:
                            seen.add(key); probs.append((i, round(t, 1), '글자 겹침', na, nb))
                for nd, bd in dots:
                    if ba and _hit(ba, bd, pad=0) and not (na.startswith('이름표') and na[4:] in nd):
                        key = (i, '가림', na, nd)
                        if key not in seen:
                            seen.add(key); probs.append((i, round(t, 1), '글자가 가림', na, nd))
    if post_text is not None:
        body = re.sub(r'\s', '', post_text)
        for i, sc in enumerate(scenes):
            words = [p[3] for p in sc.get('players', {}).values() if p[3]] + [z[6] for z in sc.get('zones', []) if z[6]] \
                + [g[3] for g in sc.get('tags', [])]
            for w_ in words:
                if re.sub(r'\s|(선수|감독)$', '', w_.strip()) not in body:   # 클립에서 붙이는 호칭은 떼고 대조(10/11)
                    probs.append((i, '-', '발행본에 없는 글', w_, '철자·이름 확인'))
    for p in probs:
        print('장면 %s  %s초  %s: %s %s' % (p[0], p[1], p[2], p[3], ('↔ ' + p[4]) if p[4] else ''))
    print('검수 끝 — 문제 %d건' % len(probs))
    return probs


# ---------- 검산: 화면 글자 모으기 · 숫자 대조 · 호칭 (10/10 「지금 퀄리티 유지」) ----------
def screen_strings(scenes):
    """장면마다 화면에 뜨는 글 전부(자막·라벨·카드 줄·이름표·태그)."""
    out = []
    for i, sc in enumerate(scenes):
        ss = [tx[2] for tx in sc.get('texts', [])]
        for it in sc.get('items', []):
            if isinstance(it[0], str) and it[0] == 'label':
                ss.append(it[2])
            elif isinstance(it[0], (int, float)) and len(it) > 2:   # card 장면 ('row'·'big')
                ss += [x for x in it[2:] if isinstance(x, str) and x and not x.startswith('#')]
        ss += [p[3] for p in sc.get('players', {}).values() if p[3]]
        ss += [z[6] for z in sc.get('zones', []) if z[6]] + [g[3] for g in sc.get('tags', [])]
        ss += sc.get('qa_strings', [])   # shorts.py 장면(제목 띠·큰 글·말 자막·라벨)
        out.append([s.replace('{', '').replace('}', '').replace('\n', ' ') for s in ss])
    return out


def _num_variants(tok):
    """「7/11」→「7월 11일」, 「67%」→「67%」 등 발행본에 적혔을 법한 꼴."""
    v = {tok}
    m = re.fullmatch(r'(\d{1,2})/(\d{1,2})', tok)
    if m:
        v |= {'%s월%s일' % m.groups(), '%s월 %s일' % m.groups()}
    return v


def check_facts(scenes, post_text, extra_ok=()):
    """화면 숫자(1-0·7/11·309·67% …)가 발행본에 있는지. 없으면 사람이 다시 본다(계산값·날짜 꼴이 다를 수 있음)."""
    body = re.sub(r'\s', '', post_text)
    probs = []
    for i, ss in enumerate(screen_strings(scenes)):
        for s in ss:
            for tok in re.findall(r'\d+(?:[.,:\-/~]\d+)*%?', s):
                if tok in extra_ok or any(re.sub(r'\s', '', v) in body for v in _num_variants(tok)):
                    continue
                probs.append((i, tok, s))
    for p in probs:
        print('장면 %s  발행본에 없는 숫자 %s  ← 「%s」' % p)
    print('숫자 대조 끝 — 확인할 것 %d건' % len(probs))
    return probs


def check_honorifics(scenes, players=(), coaches=(), narration=()):
    """선수 이름 뒤엔 「선수」, 감독 이름 뒤엔 「감독」(지침 6-2). 「이건희·강성진·정호연 선수」처럼 · 로 묶은 목록은 끝에 한 번.
    전술판 이름표(점 아래 이름)는 빼고 본다. narration = 내레이션 대본 줄 목록."""
    labels = {p[3] for sc in scenes for p in sc.get('players', {}).values() if p[3]}
    lines = [(i, s) for i, ss in enumerate(screen_strings(scenes)) for s in ss if s not in labels]
    lines += [('대본 %d' % k, s) for k, s in enumerate(narration)]
    probs = []
    for where, s in lines:
        for names, title in ((players, '선수'), (coaches, '감독')):
            for n in names:
                for m in re.finditer(re.escape(n), s):
                    rest = s[m.end():]
                    rest = re.sub(r'^(?:[·,] ?[가-힣]{2,5})*', '', rest)   # 「·강성진·정호연」 건너뛰기
                    if not rest.lstrip().startswith(title):
                        probs.append((where, n, title, s))
    for p in probs:
        print('%s  「%s」 뒤에 「%s」 없음 ← 「%s」' % p)
    print('호칭 검사 끝 — 문제 %d건' % len(probs))
    return probs


def build(scenes, base, ep, out_name):
    tmp = os.path.join(base, '_build', ep)
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    os.makedirs(os.path.join(base, 'out'), exist_ok=True)
    sfx = make_sfx(tmp)
    narr = {}
    for i, sc in enumerate(scenes):
        k = sc.get('narr', i)   # 앞에 후킹 장면을 끼우면 번호가 밀린다 → 장면이 쓸 내레이션 번호(None = 없음, 10/10)
        p = os.path.join(base, 'narration', ep, f'n{k:02d}.mp3') if k is not None else ''
        if p and os.path.exists(p):
            q = os.path.join(tmp, f'n{i:02d}.wav')
            narr_proc(p, q, sc.get('breath'))
            d = media_dur(q)
            if d > 12:
                raise SystemExit('내레이션 %s n%02d 가 %.1f초 — 깨진 파일일 수 있음' % (ep, i, d))
            narr[i] = q
            need = d + NARR_LEAD + 0.3
            if need > sc['dur']:
                sc['tscale'] = min(MAX_STRETCH, need / sc['dur'])
                sc['dur'] = round(need, 2)
    parts = []
    for i, sc in enumerate(scenes):
        out = os.path.join(tmp, f'seg{i:02d}.mp4')
        n = int(sc['dur'] * FPS)
        p = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-frames:v', str(n), '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', out],
                             stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        cache = {}
        for k in range(n):
            p.stdin.write(frame(sc, k / FPS, cache).tobytes())
        p.stdin.close()
        if p.wait():
            raise SystemExit('인코딩 실패 ' + out)
        parts.append(out)
        print('scene', i, sc['dur'], 's')
    inputs, chain, prev, t = [], [], '0:v', 0.0
    for p in parts:
        inputs += ['-i', p]
    starts = [0.0]
    for i in range(1, len(parts)):
        t += scenes[i - 1]['dur'] - XF
        starts.append(t)
        chain.append(f'[{prev}][{i}:v]xfade=transition=fade:duration={XF}:offset={t:.3f}[x{i}]')
        prev = f'x{i}'
    total = sum(s['dur'] for s in scenes) - XF * (len(parts) - 1)
    k = len(parts)
    inputs += ['-f', 'lavfi', '-t', f'{total:.3f}', '-i', 'anullsrc=r=44100:cl=stereo']
    alabs = [f'[{k}:a]']; idx = k + 1
    for i, p in sorted(narr.items()):
        inputs += ['-i', p]; ms = int((starts[i] + NARR_LEAD) * 1000)
        chain.append(f'[{idx}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}]')
        alabs.append(f'[a{i}]'); idx += 1
    events = []
    for i, sc in enumerate(scenes):
        if i:
            events.append(('whoosh', max(0.0, starts[i] - 0.12)))
        ts = sc.get('tscale', 1.0)
        for at, name in sc.get('sfx', []):
            events.append((name, starts[i] + at * ts))
        for ev in sc.get('ball', []):   # 패스마다 「톡」
            if ev[0] == 'pass':
                events.append(('kick', starts[i] + ev[1] * ts))
    for j, (name, at) in enumerate(events):
        inputs += ['-i', sfx[name]]; ms = int(at * 1000)
        chain.append(f'[{idx}:a]volume={SFX_VOL[name]},adelay={ms}|{ms}[s{j}]')
        alabs.append(f'[s{j}]'); idx += 1
    chain.append(f'{"".join(alabs)}amix=inputs={len(alabs)}:duration=first:normalize=0[aout]')
    final = os.path.join(base, 'out', out_name)
    run(['ffmpeg', '-y', *inputs, '-filter_complex', ';'.join(chain), '-map', f'[{prev}]', '-map', '[aout]',
         '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-movflags', '+faststart', final])
    print('done', final, f'{total:.1f}s')
