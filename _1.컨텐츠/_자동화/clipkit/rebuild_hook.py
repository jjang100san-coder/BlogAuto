# 숫자형 클립 앞에 1.6초 후킹 장면(커버와 같은 이미지 + 첫 장면 질문 자막)을 끼워 다시 빌드 (10/10, 클립 지침 2-4 🎬)
# 사용: python rebuild_hook.py <clipXX.py> [...]   → 각 clip\out\<원래이름>_hook.mp4
# 커버 이미지는 make_covers_1010.py 가 만든 clip\_build\cover_full.png(라벨 박힌 꽉 찬 장면). 내레이션은 새로 안 만든다(번호만 한 칸씩 밀어 씀)
import os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tactics import build
from dataviz import render, LIGHT

for path in sys.argv[1:]:
    path = os.path.abspath(path)
    src = open(path, encoding='utf-8').read()
    ep, name = re.findall(r"build\(SCENES, BASE, '([^']+)', '([^']+)'\)", src)[-1]
    spec = importlib.util.spec_from_file_location('clipmod', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = m.BASE
    full = os.path.join(base, '_build', 'cover_full.png')
    if not os.path.exists(full):
        print('커버 장면 없음 — make_covers 먼저:', path); continue
    hook = next(s for _, kind, s in m.SCENES[0]['texts'] if kind == 'top')
    keep = os.path.join(base, 'cover_full_keep.png')   # build 가 _build\<EP> 만 지우지만 안전하게 옮겨 둔다
    if not os.path.exists(keep):
        import shutil; shutil.copy(full, keep)
    h = dict(type='data', render=render, bg=LIGHT, dur=1.6, narr=None,
             items=[('image', 0, keep, 0, 0, 1080, 1920)], texts=[(0.05, 'top', hook)], sfx=[(0.05, 'ding')])
    scenes = [h]
    for i, sc in enumerate(m.SCENES):
        sc = dict(sc); sc['narr'] = i; scenes.append(sc)
    build(scenes, base, ep, name.replace('.mp4', '_hook.mp4'))
