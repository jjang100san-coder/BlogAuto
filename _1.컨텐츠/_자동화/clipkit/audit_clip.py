# 전술판·숫자 클립 검수 — python audit_clip.py <장면 스크립트.py> [발행본.txt]
# 글자끼리 겹침 · 글자가 선수/공을 덮음 · 화면 밖 글자 · (발행본을 주면) 이름표·구역·태그 글이 발행본에 있는지
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.dirname(path))
spec = importlib.util.spec_from_file_location('scenemod', path)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sys.path.insert(0, HERE)
import importlib
for k in [k for k in sys.modules if k == 'tactics']:
    del sys.modules[k]
spec2 = importlib.util.spec_from_file_location('tactics_kit', os.path.join(HERE, 'tactics.py'))
tk = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(tk)
post = open(sys.argv[2], encoding='utf-8').read() if len(sys.argv) > 2 else None
tk.audit(m.SCENES, post)
