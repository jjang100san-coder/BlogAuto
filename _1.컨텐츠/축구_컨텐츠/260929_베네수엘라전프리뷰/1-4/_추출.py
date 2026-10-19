# -*- coding: utf-8 -*-
"""베네수엘라전(10/2) 프리뷰 자료 — 일본 채널의 일본 vs 베네수엘라(9/28, 2-1) 분석.

베네수엘라의 직전 경기라 프리뷰 자료로 쓴다. 우루과이전 때 일본 vs 우루과이를 쓴 것과 같은 방식.

자막은 일본어 원어 트랙만 받는다 ("ja,ja-orig").
  - 한국어 자동번역(ko)은 음성 -> 일본어 자막 -> 한국어의 이중 기계 처리라 고유명사·전술 용어가
    더 망가지고, 번역 트랙은 레이트리밋이 빡빡해 자막 하나 때문에 통째로 실패하기 쉽다(SKILL.md).
  - 번역은 원어 대본을 읽고 직접 한다.
자막이 없으면 whisper medium 으로 -l ja 전사 (find_whisper 가 medium 을 고른다).

영상을 추가할 때는 VIDS 에 줄만 더한다. 이미 끝난 건은 자동으로 건너뛴다.
폴더 이름은 유튜브 영상 제목(윈도우 금지문자 제거, 끝 점·공백 제거).
videoscan 은 순차 실행한다 — 병렬로 띄우면 429.
"""
import io, json, os, re, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
VS = os.path.join(os.path.expanduser("~"), ".claude", "skills",
                  "claude-watch-kr", "scripts", "videoscan.py")
LOG = os.path.join(BASE, "_추출.log")

VIDS = [
    ("L_qzhLnexQg", "ja,ja-orig", "ja"),   # 1 小澤一郎 — 리뷰 + 전술보드 (18분)
    ("vc67KlCjLSw", "ja,ja-orig", "ja"),   # 2 GOAT理論 — 분석&평가 클립 (16분)
    ("wTNBWN5OPF0", "ja,ja-orig", "ja"),   # 3 レオザ 공인 클립 (21분)
    ("9ShfI37ipok", "ja,ja-orig", "ja"),   # 4 サッカーミムちゃんねる — 승부를 가른 열쇠 (11분)
    # 5 PIVOT 라이브 리뷰 (9/29 09:00, 39분) — 게스트 ミムラユウスケ·垣内一之(스포니치).
    #   종료 직후엔 자동자막이 아직 없어 whisper medium -l ja 로 전사된다 (~45분).
    ("v4NIs1Az0ME", "ja,ja-orig", "ja"),
    # --- 2차 (2026-09-29 16시) — 하루 지나도 새 분석이 없어 기존 후보 중 미추출 양질 자료 ---
    ("9d0hXs2Msjc", "ja,ja-orig", "ja"),   # 6 닛테레 경기 후 기자회견 47분 (베네수엘라 감독 회견 포함 여부 확인)
    ("hKrYAuT12uY", "ja,ja-orig", "ja"),   # 7 교도통신 모리야스 회견 무편집 29분
    ("1i1ELZ9HRTQ", "ja,ja-orig", "ja"),   # 8 蹴球メガネーズ 北條聡·川端暁彦 88분
    ("Pd4s7l7Ajzw", "ja,ja-orig", "ja"),   # 9 城彰二 JOチャンネル 13분
    # --- 3차 (2026-09-30 00시) — 후속 라이브 ---
    ("b-Mc0IyG6DE", "ja,ja-orig", "ja"),   # 10 레오자 다음날 라이브 85분 (W杯明け2戦振り返り 외 잡담 다수)
    # ("395HT1wf7wo", ...)  # 11 뮤라 유스케 긴급 라이브 65분 — 00:17 현재 post_live, 처리 끝나면 추가
]

BAD = re.compile(r'[\/:*?"<>|]')
WS = re.compile(r"\s+")


def log(msg):
    line = "%s  %s" % (time.strftime("%H:%M:%S"), msg)
    with io.open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)
    sys.stdout.flush()


def safe(title):
    return WS.sub(" ", BAD.sub("", title)).strip().rstrip(". ")[:100]


def title_of(vid):
    """--print 는 cp949 로 나와 깨진다. --dump-json 은 항상 UTF-8."""
    res = subprocess.run(["yt-dlp", "--no-warnings", "--skip-download", "--dump-json",
                          "https://www.youtube.com/watch?v=" + vid], capture_output=True)
    try:
        return json.loads(res.stdout.decode("utf-8", "replace"))["title"]
    except Exception:
        return ""


def main():
    log("=== 시작 (%d편, 일본어) === [START]" % len(VIDS))
    for vid, subs, wlang in VIDS:
        title = title_of(vid)
        if not title:
            log("%s 제목 조회 실패, 건너뜀" % vid)
            continue
        d = os.path.join(BASE, safe(title))
        if os.path.exists(os.path.join(d, "seg", "transcript.txt")):
            log("이미 완료, 건너뜀 — %s" % vid)
            continue
        os.makedirs(d, exist_ok=True)
        log("--- 시작: %s [%s]" % (safe(title)[:60], vid))
        with io.open(LOG, "a", encoding="utf-8") as fh:
            r = subprocess.run([sys.executable, VS, "https://www.youtube.com/watch?v=" + vid,
                                "--out", os.path.join(d, "seg"),
                                "--sub-langs", subs, "--whisper-lang", wlang],
                               stdout=fh, stderr=subprocess.STDOUT)
        log("--- 종료 exit=%s [%s]" % (r.returncode, vid))
        time.sleep(20)
    # 한글 조건문은 PowerShell 에서 깨지므로 ASCII 마커를 같이 남긴다 (2026-09-29 교훈)
    log("=== 끝 === [DONE]")


if __name__ == "__main__":
    main()
