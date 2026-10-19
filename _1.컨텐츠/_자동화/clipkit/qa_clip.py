# 클립 검산 한 번에 — python qa_clip.py <장면 스크립트.py> [--stt]
# (10/10 사용자: 「지금 퀄리티 유지할 수 있도록 검산 프로세스」 — 정효볼 3편 기준)
#  ① 글자 겹침·가림·화면 밖(전술판 + 숫자 카드)        tactics.audit
#  ② 이름표·태그 글이 발행본에 있나(오타)               tactics.audit(post)
#  ③ 화면 숫자가 발행본에 있나                          tactics.check_facts
#  ④ 호칭(선수·감독) — 화면 글 + 내레이션 대본          tactics.check_honorifics
#  ⑤ 내레이션: 장면마다 파일·12초 이하·대본 줄 수       파일 검사
#  ⑥ 완성본 길이 90초 이하                               out\*.mp4
#  ⑦ --stt: 받아쓰기를 대본 옆에 나란히(귀 대신 눈으로)  check_narration.py
# 준비물(클립 폴더): pub_<logNo>.txt(발행본 — getpub.py) · narration\<EP>\script.txt(대본, 한 줄 = nXX 하나)
# 장면 스크립트에 PLAYERS = [...] · COACHES = [...] 를 적어 두면 호칭 검사에 쓴다
import os, re, sys, glob, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(sys.argv[1]); base = os.path.dirname(path)
sys.path.insert(0, base); sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location('scenemod', path)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import tactics as T

src = open(path, encoding='utf-8').read()
ep, out_name = (re.findall(r"build\(\w+, BASE, '([^']+)', '([^']+)'\)", src) or [(None, None)])[-1]
fails = []

posts = glob.glob(os.path.join(base, 'pub_*.txt'))
post = open(posts[0], encoding='utf-8').read() if posts else None
if not post:
    fails.append('발행본 pub_*.txt 없음 — 숫자·오타 대조를 못 함(getpub.py <logNo> 로 받기)')

print('\n== ①② 글자 겹침·가림·화면 밖·이름 오타')
if T.audit(m.SCENES, post):
    fails.append('글자 검수')

if post:
    print('\n== ③ 화면 숫자 ↔ 발행본')
    if T.check_facts(m.SCENES, post, getattr(m, 'NUM_OK', ())):
        fails.append('숫자 대조(눈으로 확인 — 계산값·날짜 꼴이면 NUM_OK 에 적기)')

BADCH = '−✕✗✔'   # 글꼴에 없어 □로 나오는 글자(10/11 ✕, 10/13 지방 아파트 「−12.1%」) — 「-」 「x」 로
for i, sc in enumerate(m.SCENES):
    for s in [c[1] for c in sc.get('call', [])] + [sc.get('cap', ''), sc.get('label', '')]:
        bad = [ch for ch in s if ch in BADCH]
        if bad:
            print('장면 %d  □로 나오는 글자 %s ← 「%s」' % (i, ''.join(bad), s)); fails.append('□로 나오는 글자')

caps = [(i, sc['cap']) for i, sc in enumerate(m.SCENES) if sc.get('cap')]
if caps:
    print('\n== ③-2 자막 의미 덩어리 길이(쉼표·마침표 사이 15자 권장, 30자 넘으면 고침 — 지침 6-1-2)')
    long_ = [(i, u) for i, c in caps for u in re.split(r'(?<=[,.?!])\s+', c) if len(u.strip()) > 30]
    warn = [(i, u) for i, c in caps for u in re.split(r'(?<=[,.?!])\s+', c) if 15 < len(u.strip()) <= 30]
    for i, u in long_:
        print('장면 %d  %d자 — 둘로 나눌 것: %s' % (i, len(u), u))
    for i, u in warn:
        print('장면 %d  %d자(두 줄) — 의미가 갈리는 곳에 쉼표를 둘 수 있으면 나누기: %s' % (i, len(u), u))
    print('30자 넘는 덩어리 %d개 · 두 줄 덩어리 %d개' % (len(long_), len(warn)))
    if long_:
        fails.append('자막 의미 덩어리 30자 넘음')

script_f = os.path.join(base, 'narration', ep or '', 'script.txt')
script = [l.strip() for l in open(script_f, encoding='utf-8')] if os.path.exists(script_f) else []
if script:
    print('\n== ③-3 같은 말 반복(한 줄 안 · 다음 줄 첫머리 — 지침 6-1-2)')
    import repeat_check
    rep = repeat_check.check([l for l in script if l])
    for kind, n, msg, line in rep:
        print('%s  n%02d  %s\n        %s' % (kind, n, msg, line))
    print('반복 %d건(고칠 것 %d)' % (len(rep), sum(1 for r in rep if r[0] == '고칠 것')))
    if any(r[0] == '고칠 것' for r in rep):
        fails.append('같은 말 반복 — 대사를 바꿔 다시 녹음')

if script:
    print('\n== ③-4 발음 장부(clipkit\\pron_book.json — 지침 6-1-3, 경고만)')
    import pron_book
    pw = pron_book.check([l for l in script if l])
    for n, w, heard, tip in pw:
        print('n%02d  「%s」%s  %s' % (n, w, ('  들린 말: ' + heard) if heard else '', tip))
    print('발음 주의 %d건 — 받아쓰기(⑦)와 귀로 확인' % len(pw))

print('\n== ④ 호칭')
if T.check_honorifics(m.SCENES, getattr(m, 'PLAYERS', ()), getattr(m, 'COACHES', ()), script):
    fails.append('호칭')

print('\n== ⑤ 내레이션 파일')
nd = os.path.join(base, 'narration', ep or '')
need = [sc.get('narr', i) for i, sc in enumerate(m.SCENES)]
need = [k for k in need if k is not None]
for k in need:
    f = os.path.join(nd, 'n%02d.mp3' % k)
    if not os.path.exists(f):
        print('없음: n%02d' % k); fails.append('내레이션 n%02d 없음' % k); continue
    r = subprocess.run(['ffmpeg', '-i', f], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    mm = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    d = int(mm.group(2)) * 60 + float(mm.group(3)) if mm else 0
    flag = '  ← 12초 넘음' if d > 12 else ''
    print('n%02d %.1f초%s  %s' % (k, d, flag, script[k] if k < len(script) else '(대본 없음)'))
    if d > 12:
        fails.append('n%02d 12초 넘음' % k)
import voice_check   # 줄마다 음색 — 한 줄만 다른 목소리면 고침(10/11 하코다테 n04 여자 목소리)
vf = [os.path.join(nd, 'n%02d.mp3' % k) for k in need if os.path.exists(os.path.join(nd, 'n%02d.mp3' % k))]
vbad, _ = voice_check.odd(vf)
print('다른 목소리 %d줄 (음색 거리 기준 %.1f)' % (len(vbad), voice_check.LIMIT))
for f, d in vbad:
    print('  ← %s 음색 거리 %.1f — 다른 목소리, 다시 뽑기' % (os.path.basename(f), d))
    fails.append('%s 다른 목소리' % os.path.basename(f))
if not script:
    fails.append('대본 script.txt 없음 — 호칭·받아쓰기 대조를 못 함')

print('\n== ⑥ 완성본 길이')
mp4 = os.path.join(base, 'out', out_name or '')
if out_name and os.path.exists(mp4):
    r = subprocess.run(['ffmpeg', '-i', mp4], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    mm = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    d = int(mm.group(2)) * 60 + float(mm.group(3))
    print('%s %.1f초' % (out_name, d))
    if d > 90.5:
        fails.append('완성본 %.1f초 — 90초 넘음(지침 5-1)' % d)
else:
    print('아직 빌드 전')

if '--stt' in sys.argv:
    print('\n== ⑦ 받아쓰기(대본과 나란히 — 숫자는 아라비아로 나온다)')
    import tempfile, shutil
    tmp = tempfile.mkdtemp(); os.makedirs(os.path.join(tmp, 'narration'))
    for f in glob.glob(os.path.join(nd, 'n[0-9][0-9].mp3')):
        shutil.copy(f, os.path.join(tmp, 'narration'))
    for k, s in enumerate(script):
        print('대본 n%02d  %s' % (k, s))
    subprocess.run([sys.executable, os.path.join(HERE, '..', 'check_narration.py'), tmp])

print('\n' + ('✅ 검산 통과' if not fails else '❌ 고칠 것:\n - ' + '\n - '.join(fails)))
