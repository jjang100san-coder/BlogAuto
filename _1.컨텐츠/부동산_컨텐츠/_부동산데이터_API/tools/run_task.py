# -*- coding: utf-8 -*-
"""작업 스케줄러용 실행기 — pythonw 는 화면이 없으니 출력과 오류를 _run.log 에 남긴다.

  pythonw run_task.py rates     금리 스냅샷 (+카톡)
  pythonw run_task.py compare   기흥·영통 경계 4개 구 비교표(10/15 이사지 정정) — 지난달까지 (+카톡)
  pythonw run_task.py track     내 거래 추적 (바뀐 게 있을 때만 카톡)
"""
import contextlib
import datetime as dt
import io
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
JOBS = {"rates": "rates_snapshot", "compare": "compare_suwon", "track": "deal_track"}

name = sys.argv[1] if len(sys.argv) > 1 else ""
buf = io.StringIO()
with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
    try:
        mod = __import__(JOBS[name])
        kakao = name != "compare" or dt.date.today().day <= 7   # 비교표 카톡은 매달 첫 주만
        sys.argv = [mod.__file__] + (["--kakao"] if kakao else [])
        mod.main()
    except BaseException:
        traceback.print_exc()
with open(os.path.join(HERE, "_run.log"), "a", encoding="utf-8") as f:
    f.write(f"===== {dt.datetime.now():%Y-%m-%d %H:%M:%S} {name}\n{buf.getvalue()}\n")
