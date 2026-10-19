# -*- coding: utf-8 -*-
"""영상 폴더 하나의 메타데이터 + 대본을 한 번에 출력한다. 사용: python _brief.py <video_id>"""
import json, os, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
root = os.path.dirname(os.path.abspath(__file__))
vid = sys.argv[1]
d = glob.glob(os.path.join(root, "*_" + vid))[0]
raw = os.path.join(d, "_raw")
info = json.load(open(os.path.join(raw, "source.info.json"), encoding="utf-8"))
m = json.load(open(os.path.join(raw, "manifest.json"), encoding="utf-8"))
print("제목   :", info.get("title"))
print("채널   :", info.get("channel"), "|", info.get("uploader_id"), "|", info.get("channel_url"))
print("구독자 :", info.get("channel_follower_count"), "| 인증:", info.get("channel_is_verified"))
print("업로드 :", info.get("upload_date"), "| 길이:", info.get("duration_string"), "| 조회:", info.get("view_count"), "| 좋아요:", info.get("like_count"), "| 댓글:", info.get("comment_count"))
print("태그   :", ", ".join((info.get("tags") or [])[:15]))
print("모드   :", m.get("mode"), "| 대본:", m.get("transcript_source"), "| degraded:", m.get("degraded"))
print("컷통계 :", m.get("cut_stats"))
print("--- 설명 ---")
print((info.get("description") or "")[:1200])
print("--- 대본 ---")
t = os.path.join(raw, "transcript.txt")
if os.path.exists(t):
    import re
    # 줄마다 붙은 [mm:ss] 를 30초 간격으로만 남기고 한 문단으로 잇는다 (읽기 분량 절반)
    out, last = [], -99
    for l in open(t, encoding="utf-8").read().splitlines():
        m = re.match(r"\[(\d+):(\d+)(?::(\d+))?\]\s*(.*)", l)
        if not m: out.append(l); continue
        a, b, c, s = m.groups()
        sec = (int(a) * 3600 + int(b) * 60 + int(c)) if c else int(a) * 60 + int(b)
        if sec - last >= 30:
            out.append("\n[%s] %s" % (l[1:l.index("]")], s)); last = sec
        else:
            out.append(s)
    txt = " ".join(out)
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
    print(txt[:lim] + ("\n...[+%d자 생략]" % (len(txt) - lim) if len(txt) > lim else ""))
else:
    print("(대본 없음)")
