# -*- coding: utf-8 -*-
"""일본 영상 3편의 자막만 받아서 대본으로 만든다.

왜 자막이냐 — ggml-small 로 일본어를 전사하면 고유명사가 뭉개지고 같은 구절이
반복되며 붕괴한다(2026-09-27 실측: 3분 40초 영상이 8줄, 뒤쪽은 같은 문장 반복).
유튜브 일본어 자동자막이 훨씬 정확하다. 한국어 자동번역 트랙도 같이 받아 대조용으로 둔다.

자막 엔드포인트가 429(Too Many Requests)에 걸려 있어 길게 쉬며 재시도한다.
429 는 일시적 오류이므로 유료 경로로 내려가지 않는다(추출 사다리 규칙 ①).
"""
import io
import json
import os
import re
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE, "_자막받기.log")

VIDS = ["ZnzNkA8FT8s", "LM025AtRRHI", "GKb9tZTne8g"]
WAITS = [0, 300, 600, 900, 1200, 1800, 1800, 1800]   # 최대 약 2시간 인내

BAD = re.compile(r'[\\/:*?"<>|]')
CUE = re.compile(r"(\d\d):(\d\d):(\d\d)\.\d+\s*-->")
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def log(msg):
    line = "%s  %s" % (time.strftime("%H:%M:%S"), msg)
    with io.open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)
    sys.stdout.flush()


def safe(title):
    """윈도우 금지문자를 뺀 폴더명. 끝의 점·공백도 떼야 폴더가 만들어진다."""
    out = BAD.sub("", title)
    return WS.sub(" ", out).strip().rstrip(". ")[:110]


def title_of(vid):
    """--print 는 콘솔 인코딩으로 나와 한글·일본어가 깨진다. --dump-json 은 항상 UTF-8."""
    res = subprocess.run(
        ["yt-dlp", "--no-warnings", "--skip-download", "--dump-json",
         "https://www.youtube.com/watch?v=" + vid], capture_output=True)
    try:
        return json.loads(res.stdout.decode("utf-8", "replace"))["title"]
    except Exception:
        return ""


def vtt_to_text(path):
    """VTT 를 [분:초] 줄로 바꾼다. 유튜브 자동자막은 롤링이라 중복을 걷어낸다."""
    raw = io.open(path, encoding="utf-8", errors="replace").read()
    cues = []
    for block in re.split(r"\n\n+", raw):
        hit = CUE.search(block)
        if not hit:
            continue
        sec = int(hit.group(1)) * 3600 + int(hit.group(2)) * 60 + int(hit.group(3))
        body = "\n".join(l for l in block.split("\n")
                         if "-->" not in l and "WEBVTT" not in l)
        body = WS.sub(" ", TAG.sub("", body)).strip()
        if body:
            cues.append((sec, body))

    # 다음 줄이 현재 줄을 통째로 품고 있으면 현재 줄은 버린다
    keep = [c for i, c in enumerate(cues)
            if not (i + 1 < len(cues) and c[1] in cues[i + 1][1])]

    out = []
    prev = ""
    for sec, body in keep:
        add = body
        for k in range(min(len(prev), len(body)), 10, -1):
            if prev.endswith(body[:k]):
                add = body[k:].strip()
                break
        if add:
            out.append("[%02d:%02d] %s" % (sec // 60, sec % 60, add))
        prev = body
    return out


def fetch(vid, seg):
    """ja / ko 자동자막을 seg 에 받는다. 성공한 언어 목록을 돌려준다."""
    got = []
    for lang in ("ja", "ko"):
        base = os.path.join(seg, "sub_" + lang)
        res = subprocess.run(
            ["yt-dlp", "--no-warnings", "--skip-download",
             "--write-auto-subs", "--sub-langs", lang, "--sub-format", "vtt",
             "-o", base + ".%(ext)s",
             "https://www.youtube.com/watch?v=" + vid], capture_output=True)
        err = res.stderr.decode("utf-8", "replace")
        if os.path.exists(base + "." + lang + ".vtt"):
            got.append(lang)
        elif "429" in err:
            log("    %s: 429" % lang)
        else:
            log("    %s: 실패 %s" % (lang, err.strip()[-120:]))
        time.sleep(3)
    return got


def main():
    log("=== 자막 받기 시작 (%d편) ===" % len(VIDS))
    todo = list(VIDS)
    for wait in WAITS:
        if not todo:
            break
        if wait:
            log("%d초 대기 후 재시도 (남은 %d편)" % (wait, len(todo)))
            time.sleep(wait)
        still = []
        for vid in todo:
            title = safe(title_of(vid))
            if not title:
                log("%s 제목 조회 실패" % vid)
                still.append(vid)
                continue
            seg = os.path.join(BASE, title, "seg")
            os.makedirs(seg, exist_ok=True)
            log("--- %s" % title)
            got = fetch(vid, seg)
            if not got:
                still.append(vid)
                continue
            src = "ja" if "ja" in got else got[0]
            lines = vtt_to_text(os.path.join(seg, "sub_%s.vtt" % src))
            head = ("# 유튜브 %s 자동자막에서 옮김 (whisper 아님). 받은 언어: %s"
                    % (src, ",".join(got)))
            io.open(os.path.join(seg, "transcript.txt"), "w",
                    encoding="utf-8").write(head + "\n\n" + "\n".join(lines) + "\n")
            log("    OK %s / 본문 %d줄" % (",".join(got), len(lines)))
        todo = still
    if todo:
        log("=== 끝. 못 받은 %d편: %s ===" % (len(todo), todo))
    else:
        log("=== 끝. 전부 성공 ===")


if __name__ == "__main__":
    main()
