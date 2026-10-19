# -*- coding: utf-8 -*-
"""유튜브 분석 원본(_raw·seg 안의 영상·음성)만 집계/삭제. 컷 jpg·자막·transcript 는 남긴다."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
BLOG = r"C:\Users\user\Desktop\Blog"
ROOT = "\\\\?\\" + os.path.join(BLOG, [d for d in os.listdir(BLOG) if d.startswith("_1.")][0])
MEDIA = {".mp4", ".webm", ".mkv", ".m4a", ".wav", ".mp3", ".opus", ".aac", ".mov", ".part"}
RAWDIRS = {"_raw", "seg", "영상", "영상추출"}  # 영상, 영상추출
SKIP_TOP = {"미국체류기_컨텐츠", "여행_컨텐츠", "_자동화", "_템플릿"}
mode = sys.argv[1] if len(sys.argv) > 1 else "list"
allow_file = sys.argv[2] if len(sys.argv) > 2 else None
allow = set()
if allow_file:
    allow = {l.strip() for l in open(allow_file, encoding="utf-8") if l.strip()}
per, files = {}, []
for top in os.listdir(ROOT):
    if top in SKIP_TOP or not os.path.isdir(os.path.join(ROOT, top)):
        continue
    for topic in os.listdir(os.path.join(ROOT, top)):
        tdir = os.path.join(ROOT, top, topic)
        if not os.path.isdir(tdir):
            continue
        key = f"{top}/{topic}"
        for dp, dns, fns in os.walk(tdir):
            parts = dp.replace(ROOT, "").split("\\")
            if not any(p == "_raw" or p.startswith("seg") or p in RAWDIRS for p in parts):
                continue
            if any(p.startswith("clip") for p in parts):
                continue
            for fn in fns:
                if os.path.splitext(fn)[1].lower() in MEDIA:
                    p = os.path.join(dp, fn)
                    sz = os.path.getsize(p)
                    per.setdefault(key, [0, 0])
                    per[key][0] += sz
                    per[key][1] += 1
                    files.append((key, p, sz))
if mode == "list":
    for k, (s, n) in sorted(per.items(), key=lambda x: -x[1][0]):
        print(f"{s/1048576:8.0f} MB  {n:3d}개  {k}")
    print(f"합계 {sum(v[0] for v in per.values())/1048576/1024:.2f} GB")
elif mode == "delete":
    freed = cnt = 0
    for key, p, sz in files:
        if key in allow:
            os.remove(p)
            freed += sz
            cnt += 1
    print(f"삭제 {cnt}개, {freed/1048576/1024:.2f} GB 확보")
    for k in sorted(allow):
        s = per.get(k)
        print(f"  - {k}: {s[0]/1048576:.0f} MB {s[1]}개" if s else f"  - {k}: (미디어 없음)")
