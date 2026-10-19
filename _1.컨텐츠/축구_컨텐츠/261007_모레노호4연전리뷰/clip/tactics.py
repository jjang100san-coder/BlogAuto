# 엔진 본체는 _1.컨텐츠\_자동화\clipkit\tactics.py 로 옮겼다(10/7, 마일리지 클립과 같이 쓰려고). 여기는 연결만
import os, importlib.util
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '_자동화', 'clipkit', 'tactics.py')
_s = importlib.util.spec_from_file_location('clipkit_tactics', os.path.normpath(_p))
_m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
globals().update({k: v for k, v in vars(_m).items() if not k.startswith('__')})
