# 내레이션 여러 번 뽑은 것 중 고르기 — 클립 지침 6-1-1 ② (10/11)
# 사용: python narr_pick.py <장면 스크립트.py>
#   준비: narration\<EP>\takes\nXX_tY.mp3 (줄마다 2~3개). 장면의 cap(화면 자막, 숫자 아라비아)과 받아쓰기를 비교한다
#   점수 = 받아쓰기·자막 글자 일치율 − 0.05 × (문장부호 수보다 많은 0.35초 넘는 끊김)
#   → 가장 높은 것을 narration\<EP>\nXX.mp3 로 복사, 표를 출력
#   일치율 0.92 미만 또는 남는 끊김이 있으면 「확인 필요」 — 그 줄만 삐 소리로 이어 _build\narr_check.mp3 (사용자가 귀로)
import os, re, sys, glob, shutil, subprocess, tempfile, difflib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))

path = os.path.abspath(sys.argv[1]); base = os.path.dirname(path)
sys.path.insert(0, base); sys.path.insert(0, HERE)
import pron_book   # 받아쓰기에서 어긋난 낱말을 발음 장부에 쌓는다(지침 6-1-3, 10/11)
src = open(path, encoding='utf-8').read()
ep = re.findall(r"build\(\w+, BASE, '([^']+)', '([^']+)'\)", src)[-1][0]
spec = importlib.util.spec_from_file_location('scenemod', path)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
caps = {}
for i, sc in enumerate(m.SCENES):
    k = sc.get('narr', i)
    if k is not None and sc.get('cap'):
        caps[k] = sc['cap']
nd = os.path.join(base, 'narration', ep)
td = os.path.join(nd, 'takes')
norm = lambda s: re.sub(r'[\s,.?!·~「」"\'()]', '', s).replace('밀리', 'mm').replace('센티', 'cm')


import stt as _stt   # 엔진(whisper-cli / faster-whisper)은 stt.py 가 고른다(10/19) — 출력 꼴은 예전 그대로


def stt(f):
    return _stt.transcribe(f)


def pauses(f):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', 'silencedetect=n=-35dB:d=0.35', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dur = float(re.search(r'Duration: \d+:\d+:([\d.]+)', r.stderr).group(1))
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    return [s for s in st if 0.3 < s < dur - 0.5], dur


import voice_check   # 같은 voice_id 인데 다른 목소리가 섞여 나오는 것을 고르기 전에 뺀다(10/11 하코다테 n04)
alltakes = sorted(glob.glob(os.path.join(td, 'n*_t*.mp3')))
oddv = dict(voice_check.odd(alltakes)[0])
for f, d in oddv.items():
    print('다른 목소리라 뺌: %s 음색 거리 %.1f' % (os.path.basename(f), d))

flag = []
print('줄  고른것  일치율  끊김(허용)  길이  받아쓰기')
for k in sorted(caps):
    takes = [f for f in sorted(glob.glob(os.path.join(td, 'n%02d_t*.mp3' % k))) if f not in oddv]
    if not takes:
        print('n%02d  뽑은 것 없음' % k); continue
    allow = len(re.findall(r'[,.?!]', caps[k].rstrip('.?!')))
    best = None
    for f in takes:
        t = stt(f); p, d = pauses(f)
        pron_book.log_mismatch(caps[k], t, ep)
        ratio = difflib.SequenceMatcher(None, norm(t), norm(caps[k])).ratio()
        extra = max(0, len(p) - allow)
        sc = ratio - 0.05 * extra
        if best is None or sc > best[0]:
            best = (sc, f, ratio, len(p), allow, d, t)
    sc, f, ratio, np_, allow, d, t = best
    shutil.copy(f, os.path.join(nd, 'n%02d.mp3' % k))
    bad = ratio < 0.92 or np_ > allow
    if bad:
        flag.append((k, f))
    print('n%02d  %s  %.2f  %d(%d)  %.1f초  %s%s' % (k, os.path.basename(f)[-6:-4], ratio, np_, allow, d, t[:60], '  ← 확인 필요' if bad else ''))

if flag:
    out = os.path.join(base, '_build'); os.makedirs(out, exist_ok=True)
    beep = os.path.join(out, '_beep.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=880:duration=0.3', '-ar', '44100', '-ac', '2', beep])
    seq = []
    for k, f in flag:
        w = os.path.join(out, '_chk%02d.wav' % k)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-ar', '44100', '-ac', '2', w])
        seq += [beep, w]
    lst = os.path.join(out, '_chk.txt')
    open(lst, 'w', encoding='utf-8').write(''.join("file '%s'\n" % s.replace('\\', '/') for s in seq))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a', 'libmp3lame', '-q:a', '3',
                    os.path.join(out, 'narr_check.mp3')])
    print('확인 필요 %d줄 → %s' % (len(flag), os.path.join(out, 'narr_check.mp3')))
else:
    print('확인 필요 0줄')
