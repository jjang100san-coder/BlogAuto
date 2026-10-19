# 캠프라인 밴티지 첫 산행 클립 — v2 (10/7 숏폼 공식 반영: 지침 3-3)
# 실행: python make_clip.py   → out\vantage_clip.mp4   (v1 은 make_clip_v1.py · narration_v1 · out\vantage_clip_v1.mp4)
# v1 과 달라진 것: 확대 지점·배율 지정(focus·z0·z1·ease='punch') · 자막 튀어나오기 · 효과음(휙·딩) · 짧은 전환 · 끝 컷 = 첫 컷(반복 재생)
import os, re, math, subprocess, shutil
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
RAW = os.path.join(ROOT, '')
TMP = os.path.join(BASE, '_build')
OUT = os.path.join(BASE, 'out')
OUT_NAME = 'vantage_clip.mp4'
W, H, FPS = 1080, 1920, 30
FONT_B = 'C:/Windows/Fonts/malgunbd.ttf'
NARR_LEAD = 0.15  # 컷이 바뀌고 내레이션이 시작되기까지(초)
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)
XF = 0.12          # 전환 — 2~3초마다 바뀌는 템포라 짧게
POP = 6            # 자막이 튀어나오는 프레임 수
SFX_VOL = {'whoosh': 0.35, 'ding': 0.30}
TEMPO = 1.08      # 내레이션 1.08배 — 숏폼 템포(10/7)
JUMP_AT = 3.6     # 이보다 긴 컷은 가운데서 한 번 더 확 당긴다(점프 줌) → 2~3초마다 화면이 바뀌게

# 자막: {노란색 강조}, 줄바꿈은 \n
# pos: 'top' 후킹 / 'mid' 본 자막 / 'small' 위쪽 작은 라벨
# focus=(x,y): 확대 중심(화면 비율 0~1) · z0→z1: 처음·끝 배율 · ease='punch' 는 0.45초 만에 확 당기고 나머지는 천천히
# sfx: 컷 시작 후 몇 초에 무슨 소리 — 컷이 바뀌는 '휙'은 자동(첫 컷 제외)
V2 = r'C:\Users\user\Desktop\Blog\_1.컨텐츠\장비_컨텐츠\260922_등산화 구매\260922_vantage\photos'
SEGMENTS = [
    # 0 후킹: 독자가 믿는 「한 치수 크게」를 질문으로 → 손가락 두 개로 확 당김
    dict(src=f'{V2}/1000023064.jpg', dur=2.6, focus=(0.36, 0.38), z0=1.0, z1=1.32, ease='punch',
         sfx=[('ding', 0.45)], texts=[
        ('small', '캠프라인 밴티지 · 사이즈 실측'),
        ('top', '등산화, 한 치수 크게?\n손가락이 {두 개} 들어갔다')]),
    dict(src=f'{RAW}/vantage270_label.jpg', dur=2.2, cx=0.17, focus=(0.30, 0.50), z0=1.0, z1=1.25, ease='punch',
         sfx=[('ding', 0.4)], texts=[
        ('top', '그래서 {270}으로 교환')]),
    dict(src=f'{RAW}/vantage270_heel_finger.jpg', dur=2.4, focus=(0.42, 0.33), z0=1.0, z1=1.3, ease='punch',
         sfx=[('ding', 0.5)], texts=[
        ('top', '끈 꽉 조이고\n손가락 {하나} = 딱 맞음')]),
    dict(src=f'{RAW}/insole_tape_b.jpg', fit=True, dur=2.4, z0=1.0, z1=1.06,
         sfx=[('ding', 0.5)], texts=[
        ('mid', '깔창도 10년 신은 270과\n{27.6cm} 똑같아')]),
    # 4 저장할 정보: 라벨 JPN 칸으로 크게 당김
    dict(src=f'{RAW}/vantage270_label.jpg', dur=2.8, cx=0.17, focus=(0.33, 0.55), z0=1.0, z1=2.1, ease='punch',
         sfx=[('ding', 0.45)], texts=[
        ('small', '275 → JPN 280 · 270 → JPN 275'),
        ('top', '꿀팁: 캠프라인 라벨은\n일본 사이즈가 {5mm 크게}')]),
    dict(src=f'{RAW}/20260929_171644.jpg', dur=2.4, focus=(0.47, 0.84), z0=1.0, z1=1.15, texts=[
        ('top', '그렇게 맞춰서\n첫 산행, {수암봉}')]),
    dict(src=f'{RAW}/vantage270_side.jpg', dur=2.4, focus=(0.40, 0.62), z0=1.0, z1=1.22, ease='punch', texts=[
        ('top', '근데 {끈이 자꾸 풀리고}\n아직 덜 길들여졌고')]),
    dict(src=f'{RAW}/vantage270_heel_finger.jpg', dur=2.4, focus=(0.55, 0.72), z0=1.3, z1=1.0, nojump=True, texts=[
        ('top', '발볼이 넓어서인지\n뒤꿈치가 {살짝 떴어}')]),
    # 8 정리 카드 — 저장 유도
    dict(src=f'{RAW}/insole_tape_a.jpg', fit=True, dur=3.2, dim=True, z0=1.0, z1=1.04,
         sfx=[('ding', 0.4)], texts=[
        ('small', '저장해 두고 살 때 꺼내 보기'),
        ('top', '등산화 사이즈\n{체크 3가지}'),
        ('mid', '① 뒤꿈치에 손가락 하나\n② 깔창 길이\n③ {발볼}까지')]),
    # 9 질문으로 끝 — 첫 컷 사진으로 돌아와 배율 1.0 에서 멈춤 → 다시 재생되면 첫 컷과 이어진다
    dict(src=f'{V2}/1000023064.jpg', dur=2.8, focus=(0.36, 0.38), z0=1.32, z1=1.0, nojump=True, texts=[
        ('top', '발볼 넓은 발,\n등산화 {어떻게} 맞춰 신어?'),
        ('mid', '댓글로 알려줘')]),
]


def font(sz):
    return ImageFont.truetype(FONT_B, sz)


def parse(line):
    """'{강조}' 를 (글자, 색) 조각으로."""
    out = []
    for i, part in enumerate(re.split(r'[{}]', line)):
        if part:
            out.append((part, YELLOW if i % 2 else WHITE))
    return out


def draw_block(img, text, kind):
    d = ImageDraw.Draw(img)
    sz = {'top': 92, 'mid': 70, 'small': 40}[kind]
    lines = text.split('\n')
    # 가장 긴 줄이 화면 폭(양옆 여백 포함 W-140)을 넘으면 글자 크기를 줄인다
    while True:
        f = font(sz)
        widths = [sum(d.textlength(t, font=f) for t, _ in parse(l)) for l in lines]
        if max(widths) <= W - 140 or sz <= 40:
            break
        sz -= 4
    gap = int(sz * 0.32)
    lh = sz + gap
    bh = lh * len(lines) - gap
    y0 = {'top': 300, 'mid': 1180, 'small': 210}[kind]
    if kind == 'mid':
        y0 = 1300 - bh // 2
    pad_x, pad_y = 44, 30
    bw = max(widths)
    if kind != 'small':
        box = Image.new('RGBA', img.size, (0, 0, 0, 0))
        bd = ImageDraw.Draw(box)
        bd.rounded_rectangle([(W - bw) / 2 - pad_x, y0 - pad_y, (W + bw) / 2 + pad_x, y0 + bh + pad_y + 10],
                             radius=28, fill=(0, 0, 0, 150))
        img.alpha_composite(box)
        d = ImageDraw.Draw(img)
    for l, lw in zip(lines, widths):
        x = (W - lw) / 2
        for t, c in parse(l):
            d.text((x, y0), t, font=f, fill=c, stroke_width=5 if kind != 'small' else 3, stroke_fill=(0, 0, 0))
            x += d.textlength(t, font=f)
        y0 += lh


def overlay_png(seg, path):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if seg.get('dim'):
        img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 90)))
    for kind, text in seg['texts']:
        draw_block(img, text, kind)
    img.save(path)


def still_2x(seg, path):
    """사진을 2160x3840 으로: 채우기(cx 로 좌우 위치) 또는 흐린 배경 위에 맞추기."""
    im = ImageOps.exif_transpose(Image.open(seg['src'])).convert('RGB')
    W2, H2 = W * 2, H * 2
    if seg.get('fit'):
        bg = ImageOps.fit(im, (W2, H2)).filter(ImageFilter.GaussianBlur(60))
        bg = Image.eval(bg, lambda v: int(v * 0.55))
        r = min(W2 * 0.92 / im.width, H2 * 0.56 / im.height)
        fg = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
        bg.paste(fg, ((W2 - fg.width) // 2, int(H2 * 0.07)))
        im = bg
    else:
        im = ImageOps.fit(im, (W2, H2), Image.LANCZOS, centering=(seg.get('cx', 0.5), 0.5))
    for x0, y0, x1, y1 in seg.get('blur', []):  # 사람 얼굴 가리기
        box = (int(x0 * W2), int(y0 * H2), int(x1 * W2), int(y1 * H2))
        im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(40)), box)
    for x0, y0, x1, y1 in seg.get('mosaic', []):  # 얼굴 모자이크(픽셀 블록)
        box = (int(x0 * W2), int(y0 * H2), int(x1 * W2), int(y1 * H2))
        part = im.crop(box)
        bw = max(1, (box[2] - box[0]) // 6)
        small = part.resize((max(1, part.width // bw), max(1, part.height // bw)), Image.BILINEAR)
        im.paste(small.resize(part.size, Image.NEAREST), box)
    im.save(path, quality=93)


def zoom_at(seg, k, n):
    """k 번째 프레임의 배율. punch: 0.45초 동안 전체 변화의 80% → 나머지 20% 는 끝까지 천천히."""
    z0, z1 = seg.get('z0', 1.0), seg.get('z1', 1.08)
    t = k / max(1, n - 1)
    if seg.get('ease') == 'punch':
        tp = min(1.0, 0.45 * FPS / max(1, n - 1))  # 0.45초가 전체에서 차지하는 비율
        if t < tp:
            u = t / tp
            e = 0.8 * (1 - (1 - u) ** 3)  # ease-out cubic
        else:
            e = 0.8 + 0.2 * (t - tp) / max(1e-6, 1 - tp)
    else:
        e = t * t * (3 - 2 * t)  # smoothstep
    return z0 + (z1 - z0) * e


def pop_overlay(ovl, k):
    """자막이 0.88배에서 1배로 커지며 나타난다(처음 POP 프레임)."""
    if k >= POP:
        return ovl
    u = (k + 1) / POP
    e = 1 - (1 - u) ** 3
    s = 0.88 + 0.12 * e
    w, h = int(W * s), int(H * s)
    sm = ovl.resize((w, h), Image.BILINEAR)
    a = sm.getchannel('A').point(lambda v: int(v * e))
    sm.putalpha(a)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    out.alpha_composite(sm, ((W - w) // 2, (H - h) // 2))
    return out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])


def make_sfx():
    """효과음은 직접 합성(저작권 없음): 휙 = 걸러낸 분홍 잡음, 딩 = 사인파 두 개 감쇠."""
    w = os.path.join(TMP, 'whoosh.wav')
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=0.32:c=pink:a=0.9:r=44100',
         '-af', 'highpass=f=500,lowpass=f=5000,afade=t=in:d=0.16:curve=exp,afade=t=out:st=0.16:d=0.16,aformat=channel_layouts=stereo', w])
    d = os.path.join(TMP, 'ding.wav')
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i',
         "aevalsrc='0.6*sin(2*PI*1568*t)*exp(-7*t)+0.3*sin(2*PI*3136*t)*exp(-11*t)':d=0.6:s=44100",
         '-af', 'aformat=channel_layouts=stereo', d])
    return {'whoosh': w, 'ding': d}


def build():
    shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    sfx_files = make_sfx()
    # 내레이션(narration\nXX.mp3)이 있으면 컷 길이를 목소리에 맞춘다
    narr = {}
    for i, seg in enumerate(SEGMENTS):
        p = os.path.join(BASE, 'narration', f'n{i:02d}.mp3')
        if os.path.exists(p):
            # MiniMax 가 문장 사이를 1~1.7초씩 쉬는 버릇 → 0.4초 넘는 빈틈은 0.4초로 묶는다(10/7 사용자 지적)
            q = os.path.join(TMP, f'n{i:02d}.wav')
            run(['ffmpeg', '-y', '-i', p, '-af',
                 f'silenceremove=stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB:stop_silence=0,atempo={TEMPO}', q])
            p = q
            d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                     capture_output=True, text=True).stdout)
            if d > 12:  # MiniMax 가 가끔 같은 소리를 수십 초 반복하는 깨진 파일을 준다(10/7 한정선 n03 51초)
                raise SystemExit('내레이션 n%02d.mp3 가 %.1f초 — 깨진 파일일 수 있음. 문장을 바꿔 다시 생성' % (i, d))
            narr[i] = p
            seg['dur'] = round(max(seg['dur'], d + NARR_LEAD + 0.25), 2)
    parts = []
    for i, seg in enumerate(SEGMENTS):
        ov = os.path.join(TMP, f'ov{i:02d}.png')
        overlay_png(seg, ov)
        out = os.path.join(TMP, f'seg{i:02d}.mp4')
        n = int(seg['dur'] * FPS)
        big = os.path.join(TMP, f'img{i:02d}.jpg')
        still_2x(seg, big)
        # 소수점 단위로 확대(PIL box resize) — zoompan 은 정수 픽셀로 끊겨 덜컥거렸다(10/7 사용자 지적)
        src = Image.open(big).convert('RGB')
        ovl = Image.open(ov).convert('RGBA')
        W2, H2 = src.size
        fx, fy = seg.get('focus', (0.5, 0.5))
        p = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                              '-i', '-', '-frames:v', str(n), '-c:v', 'libx264', '-crf', '19', '-preset', 'medium',
                              '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        for k in range(n):
            z = zoom_at(seg, k, n)
            if seg['dur'] >= JUMP_AT and not seg.get('nojump') and k >= n // 2:
                u = min(1.0, (k - n // 2) / (0.3 * FPS))
                z *= 1 + 0.12 * (1 - (1 - u) ** 3)  # 0.3초 만에 12% 더 당김
            w, h = W2 / z, H2 / z
            x0 = min(max(fx * W2 - w / 2, 0), W2 - w)  # 확대 중심을 focus 로, 화면 밖으로는 안 나가게
            y0 = min(max(fy * H2 - h / 2, 0), H2 - h)
            fr = src.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')
            fr.alpha_composite(pop_overlay(ovl, k))
            p.stdin.write(fr.convert('RGB').tobytes())
        p.stdin.close()
        if p.wait():
            raise SystemExit('ffmpeg 프레임 인코딩 실패: ' + out)
        parts.append(out)
        print('seg', i, seg['dur'], 's')

    inputs, chain, prev, t = [], [], '0:v', 0.0
    for p in parts:
        inputs += ['-i', p]
    starts = [0.0]
    for i in range(1, len(parts)):
        t += SEGMENTS[i - 1]['dur'] - XF
        starts.append(t)
        lab = f'x{i}'
        chain.append(f'[{prev}][{i}:v]xfade=transition=fade:duration={XF}:offset={t:.3f}[{lab}]')
        prev = lab
    total = sum(s['dur'] for s in SEGMENTS) - XF * (len(parts) - 1)
    # 오디오: 무음 바탕 + 내레이션 + 효과음
    k = len(parts)
    inputs += ['-f', 'lavfi', '-t', f'{total:.3f}', '-i', 'anullsrc=r=44100:cl=stereo']
    alabs = [f'[{k}:a]']
    idx = k + 1
    for i, p in sorted(narr.items()):
        inputs += ['-i', p]
        ms = int((starts[i] + NARR_LEAD) * 1000)
        chain.append(f'[{idx}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}]')
        alabs.append(f'[a{i}]')
        idx += 1
    events = []
    for i, seg in enumerate(SEGMENTS):
        if i:
            events.append(('whoosh', max(0.0, starts[i] - 0.12)))
        for name, off in seg.get('sfx', []):
            events.append((name, starts[i] + off))
    for j, (name, at) in enumerate(events):
        inputs += ['-i', sfx_files[name]]
        ms = int(at * 1000)
        chain.append(f'[{idx}:a]volume={SFX_VOL[name]},adelay={ms}|{ms}[s{j}]')
        alabs.append(f'[s{j}]')
        idx += 1
    chain.append(f'{"".join(alabs)}amix=inputs={len(alabs)}:duration=first:normalize=0[aout]')
    final = os.path.join(OUT, OUT_NAME)
    run(['ffmpeg', '-y', *inputs,
         '-filter_complex', ';'.join(chain), '-map', f'[{prev}]', '-map', '[aout]',
         '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-movflags', '+faststart', final])
    print('done', final, f'{total:.1f}s')


if __name__ == '__main__':
    build()
