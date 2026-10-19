# -*- coding: utf-8 -*-
"""롤링 자동자막(한 줄 = 앞 줄의 새 부분 + 이번 새 부분)의 겹침을 걷어내고
문단으로 묶어 _out.txt 로 떨군다. 약 40초마다 타임코드를 하나 남긴다.
사용: python _읽기2.py <폴더명 일부>"""
import io, os, re, sys
BASE = os.path.dirname(os.path.abspath(__file__))
key = sys.argv[1] if len(sys.argv) > 1 else ""
hits = [n for n in sorted(os.listdir(BASE)) if os.path.isdir(os.path.join(BASE, n)) and key in n]
out = []
for n in hits:
    t = os.path.join(BASE, n, "seg", "transcript.txt")
    out.append("### " + n)
    if not os.path.exists(t):
        out.append("(대본 없음)"); continue
    prev, buf, last_ts, paras = "", [], -999, []
    for line in io.open(t, encoding="utf-8"):
        m = re.match(r"\[(\d+):(\d+)(?::(\d+))?\]\s*(.*)", line.strip())
        if not m: continue
        a, b, c, txt = m.groups()
        sec = int(a)*60+int(b) if c is None else int(a)*3600+int(b)*60+int(c)
        # 앞 줄 끝부분과 겹치는 가장 긴 접두부를 떼어낸다 (롤링 자막)
        k = 0
        for L in range(min(len(prev), len(txt)), 0, -1):
            if prev.endswith(txt[:L]):
                k = L; break
        new = txt[k:].strip() if k >= 4 else txt
        prev = txt
        if not new: continue
        if sec - last_ts >= 40:
            if buf: paras.append("".join(buf))
            buf = ["[%d:%02d] " % (sec//60, sec%60)]; last_ts = sec
        buf.append(new)
    if buf: paras.append("".join(buf))
    out.append("\n".join(paras))
io.open(os.path.join(BASE, "_out.txt"), "w", encoding="utf-8").write("\n\n".join(out))
