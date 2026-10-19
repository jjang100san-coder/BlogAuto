# 수암봉 등산코스 클립 — 블로그 글을 9:16 영상으로 (사진 움직임 + 자막 + 내레이션)
# 실행: python make_clip.py   → out\suambong_clip.mp4
import os, re, subprocess, shutil
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
RAW = os.path.join(ROOT, '클로드')
TMP = os.path.join(BASE, '_build')
OUT = os.path.join(BASE, 'out')
OUT_NAME = 'suambong_clip.mp4'
W, H, FPS = 1080, 1920, 30
FONT_B = 'C:/Windows/Fonts/malgunbd.ttf'
NARR_LEAD = 0.15  # 컷이 바뀌고 내레이션이 시작되기까지(초)
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

# 자막: {노란색 강조}, 줄바꿈은 \n
# pos: 'top' 후킹 / 'mid' 본 자막 / 'small' 위쪽 작은 라벨
SEGMENTS = [
    dict(src='video:cut00_정상노을.mp4', dur=3.0, texts=[
        ('small', '수암봉 · 9월 29일 화요일 퇴근길'),
        ('top', '퇴근하고 산 갔다 왔거든?\n정상까지 {38분} 컷')]),
    dict(src=f'{RAW}/20260929_175006.jpg', dur=3.0, texts=[
        ('mid', '수암봉공영주차장\n평일엔 주차비 {안 받음}')]),
    dict(src=f'{RAW}/20260929_175010.jpg', dur=3.0, texts=[
        ('mid', '화장실은 주차장 옆 {하나뿐}\n산에는 없어!')]),
    dict(src=f'{RAW}/finder_conditions.png', fit=True, dur=3.0, texts=[
        ('mid', '내가 만든 프로그램으로\n경기도 {118곳} 중에 골랐어')]),
    dict(src=f'{RAW}/20260929_163938.jpg', dur=3.0, texts=[
        ('mid', '정상까지 {1.36km}\n처음 절반은 거의 산책')]),
    dict(src=f'{RAW}/20260929_165049.jpg', dur=3.0, texts=[
        ('mid', '중간에 {약수터}\n컵은 각자 챙기기!')]),
    dict(src=f'{RAW}/20260929_170339.jpg', dur=3.0, texts=[
        ('mid', '헬기장에 서면\n수암봉이 {눈앞에}')]),
    dict(src=f'{RAW}/20260929_170853.jpg', dur=3.0, texts=[
        ('mid', '마지막 {나무계단}만 오르면…\n끝!')]),
    dict(src=f'{RAW}/20260929_171518.jpg', dur=3.0, texts=[
        ('mid', '수암봉 {398m}\n주차장에서 {38분}')]),
    dict(src=f'{RAW}/suambong_profile.png', fit=True, dur=3.0, texts=[
        ('mid', '프로그램 예상 56분\n실제는 {18분 빨랐어}')]),
    dict(src=f'{RAW}/20260929_171450.jpg', dur=3.0, texts=[
        ('mid', '정상 바위엔 {나비}\n나보다 먼저 왔나 봐')]),
    dict(src=f'{RAW}/20260929_171644.jpg', dur=3.0, texts=[
        ('mid', '새 등산화 {첫 개시}\n아직 길들이는 중')]),
    dict(src=f'{RAW}/20260929_173036.jpg', dur=3.0, texts=[
        ('mid', '하산은 같은 길로 {34분}')]),
    dict(src=f'{RAW}/20260929_171531.jpg', dur=4.0, dim=True, texts=[
        ('top', '평일 저녁 {2시간}이면\n충분한 산'),
        ('mid', '구간별 시간표는 블로그에')]),
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
    """사진을 2160x3840 으로: 채우기(가운데 crop) 또는 흐린 배경 위에 맞추기."""
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
        bw = max(1, (box[2] - box[0]) // 6)  # 블록 6칸 — 28칸이면 얼굴이 그대로 보였다
        small = part.resize((max(1, part.width // bw), max(1, part.height // bw)), Image.BILINEAR)
        im.paste(small.resize(part.size, Image.NEAREST), box)
    im.save(path, quality=93)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])


def build():
    shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    # 내레이션(narration\nXX.mp3)이 있으면 컷 길이를 목소리에 맞춘다
    narr = {}
    for i, seg in enumerate(SEGMENTS):
        p = os.path.join(BASE, 'narration', f'n{i:02d}.mp3')
        if os.path.exists(p):
            # MiniMax 가 문장 사이를 1~1.7초씩 쉬는 버릇 → 0.4초 넘는 빈틈은 0.4초로 묶는다(10/7 사용자 지적)
            q = os.path.join(TMP, f'n{i:02d}.wav')
            run(['ffmpeg', '-y', '-i', p, '-af',
                 'silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-40dB:stop_silence=0', q])
            p = q
            d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                     capture_output=True, text=True).stdout)
            if d > 12:  # MiniMax 가 가끔 같은 소리를 수십 초 반복하는 깨진 파일을 준다(10/7 한정선 n03 51초)
                raise SystemExit('내레이션 n%02d.mp3 가 %.1f초 — 깨진 파일일 수 있음. 문장을 바꿔 다시 생성' % (i, d))
            narr[i] = p
            seg['dur'] = round(max(seg['dur'], d + NARR_LEAD + 0.35), 2)
    parts = []
    for i, seg in enumerate(SEGMENTS):
        ov = os.path.join(TMP, f'ov{i:02d}.png')
        overlay_png(seg, ov)
        out = os.path.join(TMP, f'seg{i:02d}.mp4')
        n = int(seg['dur'] * FPS)
        if seg['src'].startswith('video:'):
            src = os.path.join(BASE, seg['src'][6:])
            vf = (f'[0:v]scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},tpad=stop_mode=clone:stop_duration={seg["dur"]},trim=duration={seg["dur"]},setpts=PTS-STARTPTS[b];'
                  f'[b][1:v]overlay=0:0,format=yuv420p[v]')
            run(['ffmpeg', '-y', '-i', src, '-i', ov, '-filter_complex', vf, '-map', '[v]',
                 '-t', str(seg['dur']), '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', out])
        else:
            big = os.path.join(TMP, f'img{i:02d}.jpg')
            still_2x(seg, big)
            # 소수점 단위로 확대(PIL box resize) + 시작·끝 천천히(이징) — zoompan 은 정수 픽셀로 끊겨 덜컥거렸다(10/7 사용자 지적)
            src = Image.open(big).convert('RGB')
            ovl = Image.open(ov).convert('RGBA')
            W2, H2 = src.size
            zmax = 1.08
            p = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                                  '-i', '-', '-frames:v', str(n), '-c:v', 'libx264', '-crf', '19', '-preset', 'medium',
                                  '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            for k in range(n):
                t = k / max(1, n - 1)
                e = t * t * (3 - 2 * t)  # smoothstep
                z = zmax - (zmax - 1) * e if seg.get('zoom') == 'out' else 1 + (zmax - 1) * e
                w, h = W2 / z, H2 / z
                x0, y0 = (W2 - w) / 2, (H2 - h) / 2
                fr = src.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')
                fr.alpha_composite(ovl)
                p.stdin.write(fr.convert('RGB').tobytes())
            p.stdin.close()
            if p.wait():
                raise SystemExit('ffmpeg 프레임 인코딩 실패: ' + out)
        parts.append(out)
        print('seg', i, seg['dur'], 's')

    # 0.25초 크로스페이드로 이어 붙이기
    xf = 0.25
    inputs, chain, prev, t = [], [], '0:v', 0.0
    for p in parts:
        inputs += ['-i', p]
    starts = [0.0]
    for i in range(1, len(parts)):
        t += SEGMENTS[i - 1]['dur'] - xf
        starts.append(t)
        lab = f'x{i}'
        chain.append(f'[{prev}][{i}:v]xfade=transition=fade:duration={xf}:offset={t:.3f}[{lab}]')
        prev = lab
    total = sum(s['dur'] for s in SEGMENTS) - xf * (len(parts) - 1)
    # 오디오: 무음 바탕 + 컷 시작 시각에 맞춘 내레이션
    k = len(parts)
    inputs += ['-f', 'lavfi', '-t', f'{total:.3f}', '-i', 'anullsrc=r=44100:cl=stereo']
    alabs = [f'[{k}:a]']
    for j, (i, p) in enumerate(sorted(narr.items())):
        inputs += ['-i', p]
        ms = int((starts[i] + NARR_LEAD) * 1000)
        chain.append(f'[{k + 1 + j}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}]')
        alabs.append(f'[a{i}]')
    chain.append(f'{"".join(alabs)}amix=inputs={len(alabs)}:duration=first:normalize=0[aout]')
    final = os.path.join(OUT, OUT_NAME)
    run(['ffmpeg', '-y', *inputs,
         '-filter_complex', ';'.join(chain), '-map', f'[{prev}]', '-map', '[aout]',
         '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-movflags', '+faststart', final])
    print('done', final, f'{total:.1f}s')


if __name__ == '__main__':
    build()
