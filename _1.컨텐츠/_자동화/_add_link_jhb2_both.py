# -*- coding: utf-8 -*-
# 정효볼 2편 링크를 안산 후기 → 화성 프리뷰 순서로 (앞 창을 닫으면 다음 글이 열린다) 2026-10-16
import subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
for no in ("224438297308", "224439601706"):
    subprocess.run(["python", "add_link.py", "_add_link_%s.json" % no], cwd=here)
