# -*- coding: utf-8 -*-
"""대본을 ASCII 이름으로 뽑아준다.

폴더명이 중국어라 bash glob 이 전각 문자(：등)를 못 잡고,
콘솔이 cp949 라 print 로 한자를 못 찍는다. 그래서 파일로 떨군다.

사용: python _읽기.py <폴더명 일부>   예) python _읽기.py 0比0
"""
import io
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
key = sys.argv[1] if len(sys.argv) > 1 else ""

hits = [n for n in sorted(os.listdir(BASE))
        if os.path.isdir(os.path.join(BASE, n)) and key in n]
if not hits:
    io.open(os.path.join(BASE, "_out.txt"), "w", encoding="utf-8").write(
        "일치하는 폴더 없음: %r" % key)
    raise SystemExit

parts = []
for n in hits:
    t = os.path.join(BASE, n, "seg", "transcript.txt")
    parts.append("### " + n)
    if os.path.exists(t):
        parts.append(io.open(t, encoding="utf-8").read())
    else:
        parts.append("(대본 없음)")
io.open(os.path.join(BASE, "_out.txt"), "w",
        encoding="utf-8").write("\n\n".join(parts))
