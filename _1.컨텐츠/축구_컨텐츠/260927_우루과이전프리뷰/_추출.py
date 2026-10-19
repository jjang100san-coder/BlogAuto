# -*- coding: utf-8 -*-
"""우루과이전(9/28) 프리뷰 영상 추출 드라이버.

영상이 올라오면 VIDS 에 id 만 추가하고 다시 실행한다. 이미 대본이 있는 폴더는 건너뛴다.
폴더 이름은 유튜브 영상 제목으로 만든다(사용자 요청, 2026-09-27).
  - 윈도우 금지문자 \ / : * ? " < > | 를 지우고, 끝의 점·공백도 떼야 폴더가 만들어진다.
    예: "...포를란? 우루과이전 프리뷰!" 의 물음표가 그대로 가면 생성 실패한다.
경로를 PowerShell 인수로 넘기지 않으려고 파이썬으로 직접 돌린다
  (한글 경로가 인수로 가다 _1.컨텐츠 -> _1.而⑦뀗痢? 로 깨진 사례가 있다).
한국 방송이므로 처음부터 한국어 자막·전사를 강제한다.
videoscan 은 순차 실행한다 — 병렬로 띄우면 유튜브 429 가 뜬다.
"""
import io, json, os, re, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
VS   = os.path.join(os.path.expanduser("~"), ".claude", "skills",
                    "claude-watch-kr", "scripts", "videoscan.py")
LOG  = os.path.join(BASE, "_추출.log")

# (id, subs, whisper_lang) — subs 는 videoscan --sub-langs 에 그대로 넘긴다.
# 한국 영상은 "ko,ko-orig". 일본 영상은 한국어 자동번역이 제공되므로 "ko,ja,ja-orig" 로
# 받아서 한국어를 본문으로 쓰고 일본어 원본은 중요한 대목 대조용으로 남긴다
# (일본어 음성 -> 일본어 자막 -> 한국어 번역의 이중 기계 처리라 그대로 믿을 수 없다).
VIDS = [
    ("rgpjU_qCPkY", "ko,ko-orig", "ko"),   # 알유레띠
    ("mLaQ0cmNbrM", "ko,ko-orig", "ko"),   # 로스트의 축구생활
    ("8VT2Pz7BX8M", "ko,ko-orig", "ko"),   # 서형욱의 뽈리TV — 현장인터뷰(기자회견)
    ("mGoDnlxJuuM", "ko,ko-orig", "ko"),   # CHOSUN IMAGE VISION — 기자회견 풀영상
    ("TuclRoGUQKw", "ko,ko-orig", "ko"),   # 서형욱의 뽈리TV — 국대 프리뷰
    ("Q9nv7LO8BSM", "ko,ko-orig", "ko"),   # 새벽의 축구 전문가 — 라이브 2:00:52
    # ↓ 일본 채널 (일본 vs 우루과이전 분석). 우루과이의 직전 경기라 프리뷰 자료로 쓴다
    ("ZnzNkA8FT8s", "ko,ja,ja-orig", "ja"),  # Non:Suke — 우루과이 매체 반응 번역
    ("LM025AtRRHI", "ko,ja,ja-orig", "ja"),  # GOAT理論 — 선수 평가와 과제
    ("GKb9tZTne8g", "ko,ja,ja-orig", "ja"),  # レオザのサッカー塾 — 경기 정리
]

def log(m):
    line = "%s  %s" % (time.strftime("%H:%M:%S"), m)
    with io.open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line); sys.stdout.flush()

BAD = r'[\/:*?"<>|]'
def safe(t):
    t = re.sub(BAD, '', t)
    t = re.sub(r'\s+', ' ', t).strip().rstrip('. ')
    return t[:110]

def title_of(vid):
    """--print 는 콘솔 인코딩(윈도우 cp949)으로 나와서 한글이 깨진다.
    --dump-json 은 항상 UTF-8 이라 이걸 쓴다 (2026-09-27 실측)."""
    o = subprocess.run(["yt-dlp", "--no-warnings", "--skip-download",
                        "--dump-json",
                        "https://www.youtube.com/watch?v=" + vid],
                       capture_output=True)
    try:
        return json.loads(o.stdout.decode("utf-8", "replace"))["title"]
    except Exception:
        return ""

def main():
    log("=== 시작 (%d편) ===" % len(VIDS))
    for vid, subs, wlang in VIDS:
        t = title_of(vid)
        if not t:
            log("%s : 제목 조회 실패, 건너뜀" % vid); continue
        d = os.path.join(BASE, safe(t))
        if os.path.exists(os.path.join(d, "seg", "transcript.txt")):
            log("이미 완료, 건너뜀 — %s" % safe(t)); continue
        os.makedirs(d, exist_ok=True)
        log("--- 시작: %s" % safe(t))
        with io.open(LOG, "a", encoding="utf-8") as f:
            r = subprocess.run([sys.executable, VS,
                                "https://www.youtube.com/watch?v=" + vid,
                                "--out", os.path.join(d, "seg"),
                                "--sub-langs", subs,
                                "--whisper-lang", wlang],
                               stdout=f, stderr=subprocess.STDOUT)
        log("--- 종료 exit=%s" % r.returncode)
        time.sleep(20)
    log("=== 끝 ===")

if __name__ == "__main__":
    main()
