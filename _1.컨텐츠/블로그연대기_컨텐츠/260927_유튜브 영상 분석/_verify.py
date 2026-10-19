# -*- coding: utf-8 -*-
"""3편에 인용할 대사를 화면(자막 그래픽)으로 대조하기 위한 프레임 추출.
영상은 360p 무음으로 받고, 지정 시각 앞뒤 프레임 3장을 가로로 붙인 뒤 원본은 지운다."""
import os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_검증")
os.makedirs(OUT, exist_ok=True)
JOBS = {
    "H5Vmv1pLdos": ["03:15"],
    "jy2UnH1AWcA": ["00:36"],
    "NBH1qkQxPjs": ["13:43", "13:49"],
}
def sec(t):
    m, s = t.split(":"); return int(m) * 60 + int(s)
for i, (vid, ts) in enumerate(JOBS.items()):
    src = os.path.join(OUT, vid + ".mp4")
    if not os.path.exists(src):
        r = subprocess.run(["yt-dlp", "--no-warnings", "-N", "4", "-f", "bv*[height<=360][ext=mp4]/bv*[height<=360]",
                            "-o", src, "https://www.youtube.com/watch?v=" + vid], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode:
            print("FAIL", vid, r.stderr[-300:]); continue
    for t in ts:
        s = sec(t)
        frames = []
        for k, off in enumerate((0.3, 1.8, 3.3)):
            f = os.path.join(OUT, f"{vid}_{t.replace(':','')}_{k}.jpg")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.1f" % max(0, s + off), "-i", src,
                            "-frames:v", "1", "-vf", "scale=640:-2", f])
            frames.append(f)
        out = os.path.join(OUT, f"{vid}_{t.replace(':','')}.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", f] for f in frames], []) +
                       ["-filter_complex", "hstack=inputs=3", out])
        for f in frames: os.remove(f)
        print("OK", vid, t, out)
    os.remove(src)
    if i < len(JOBS) - 1: time.sleep(30)
print("DONE")
