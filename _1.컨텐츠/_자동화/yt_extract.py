# -*- coding: utf-8 -*-
r"""유튜브 영상 → 자막 + whisper 두 판독 (마스터 0-11, 2026-10-11).

주제 폴더마다 `_추출.py` 를 복사해 ids 만 바꾸던 방식을 대신하는 공용 도구다.
화면(프레임·컷)까지 봐야 하면 영상분석 스킬(videoscan --whisper both)을 쓰고,
말만 필요하면(인터뷰·해설·회견) 이걸 쓴다 — 영상 전체를 받지 않아 훨씬 빠르다.

사용:
  python yt_extract.py <작업폴더> <영상ID> [<영상ID> ...]
      [--start 1]                 폴더 번호 시작값 (기존 01~14 가 있으면 --start 15)
      [--list _목록.tsv]          목록 파일 이름 (덮어쓰지 않게 바꿔 쓸 수 있다)
      [--whisper both|subs|off]   both = 자막 + whisper(기본), subs = 자막만, off = 둘 다 끄고 메타만
      [--whisper-max-min 60]      자막이 있을 때 whisper 를 전체에 돌릴 최대 길이(분). 넘으면 건너뛰고 알림
      [--section ID=MM:SS-MM:SS]  그 영상은 이 구간만 whisper (긴 영상·라이브, 여러 번 줄 수 있다)
      [--lang ko]                 자막·whisper 언어 (외국 영상은 en 등)

결과 (작업폴더 안):
  NN_<채널_제목>_<ID>\meta.txt · seg\transcript.txt(자막) · seg\whisper_medium.txt/.vtt
  _out_<ID>.txt      자막 판독 — 롤링 겹침 제거, 약 40초마다 타임코드
  _whisper_<ID>.txt  whisper 판독 — 같은 꼴
  _추출.log          진행 기록 ([OK] [SKIP] [NOSUB] [ERROR] [WHISPER_SKIPPED_LONG])

규칙: 순차 실행(병렬 금지 — 유튜브 429). 이미 끝난 단계는 건너뛴다. 원본 음성은 받아 적은 직후 지운다.
인용·숫자·이름은 두 판독이 같을 때만 쓴다. 다르면 영상 [분:초]를 직접 듣는다(마스터 0-11).
"""
import argparse, glob, io, json, os, re, subprocess, sys, time

CLI = os.path.expandvars(r"%USERPROFILE%\tools\whisper\Release\whisper-cli.exe")
MODEL = os.path.expandvars(r"%USERPROFILE%\.claude\models\ggml-medium.bin")
BAD = re.compile(r'[\/:*?"<>|\[\]]'); WS = re.compile(r"\s+")
TS = re.compile(r"(\d+):(\d+):(\d+)\.\d+ -->"); TAG = re.compile(r"<[^>]+>")


def safe(t):
    return WS.sub(" ", BAD.sub("", t)).strip().rstrip(". ")[:58].rstrip()


def vtt2lines(src, offset=0):
    """vtt → ["[m:ss] 문장", ...] (같은 줄 반복 제거). offset 초를 더한다(구간 whisper 용)."""
    out, last, cur = [], None, None
    for line in io.open(src, encoding="utf-8", errors="replace"):   # whisper vtt 에 깨진 바이트가 섞여 작업이 죽었다(2026-10-12)
        line = line.rstrip("\n"); m = TS.match(line)
        if m:
            h, mi, s = map(int, m.groups()); cur = h * 3600 + mi * 60 + s + offset; continue
        if cur is None or not line.strip() or "-->" in line: continue
        t = TAG.sub("", line).strip()
        if not t or t == last: continue
        last = t; h, r = divmod(cur, 3600); mi, s = divmod(r, 60)
        out.append("[%s] %s" % ("%d:%02d:%02d" % (h, mi, s) if h else "%d:%02d" % (mi, s), t))
    return out


def paragraphs(lines, gap=40):
    """롤링 자동자막 겹침을 걷어내고 약 40초 단위 문단으로 (`_읽기2.py` 와 같은 규칙)."""
    prev, buf, last_ts, paras = "", [], -999, []
    for line in lines:
        m = re.match(r"\[(\d+):(\d+)(?::(\d+))?\]\s*(.*)", line.strip())
        if not m: continue
        a, b, c, txt = m.groups()
        sec = int(a) * 60 + int(b) if c is None else int(a) * 3600 + int(b) * 60 + int(c)
        k = 0
        for L in range(min(len(prev), len(txt)), 0, -1):
            if prev.endswith(txt[:L]):
                k = L; break
        new = txt[k:].strip() if k >= 4 else txt
        prev = txt
        if not new: continue
        if sec - last_ts >= gap:
            if buf: paras.append("".join(buf))
            buf = ["[%d:%02d] " % (sec // 60, sec % 60)]; last_ts = sec
        buf.append(new + " ")
    if buf: paras.append("".join(buf).rstrip())
    return "\n".join(paras)


def mmss(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work"); ap.add_argument("ids", nargs="+")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--list", default="_목록.tsv")
    ap.add_argument("--whisper", choices=("both", "subs", "off"), default="both")
    ap.add_argument("--whisper-max-min", type=float, default=60.0)
    ap.add_argument("--section", action="append", default=[])
    ap.add_argument("--lang", default="ko")
    a = ap.parse_args()
    work = os.path.abspath(a.work); os.makedirs(work, exist_ok=True)
    LOG = os.path.join(work, "_추출.log")
    sections = {}
    for s in a.section:
        vid, rng = s.split("=", 1); st, en = rng.split("-"); sections[vid] = (mmss(st), mmss(en))

    def log(m):
        line = "%s  %s" % (time.strftime("%H:%M:%S"), m)
        io.open(LOG, "a", encoding="utf-8").write(line + "\n"); print(line); sys.stdout.flush()

    have_whisper = os.path.exists(CLI) and os.path.exists(MODEL)
    if a.whisper == "both" and not have_whisper:
        log("whisper-cli 또는 medium 모델이 없어 자막만 받습니다 [WARN] %s / %s" % (CLI, MODEL))
    log("=== 시작 %d편 (whisper=%s) [START]" % (len(a.ids), a.whisper))
    idx = []
    for n, vid in enumerate(a.ids, a.start):
        r = subprocess.run(["yt-dlp", "--no-warnings", "--skip-download", "--extractor-args",
                            "youtube:lang=%s" % a.lang, "--dump-json", "--", vid], capture_output=True)
        try:
            m = json.loads(r.stdout.decode("utf-8", "replace"))
        except Exception:
            log("%02d %s 메타 실패 [ERROR %s] %s" % (n, vid, vid, r.stderr.decode("utf-8", "replace")[-200:].strip()))
            time.sleep(10); continue
        old = [d for d in os.listdir(work) if d.endswith("_" + vid) and os.path.isdir(os.path.join(work, d))]
        d = os.path.join(work, old[0]) if old else os.path.join(
            work, "%02d_%s_%s" % (n, safe("%s_%s" % (m.get("channel", ""), m["title"])), vid))
        seg = os.path.join(d, "seg"); os.makedirs(seg, exist_ok=True)
        dur = float(m.get("duration") or 0)
        io.open(os.path.join(d, "meta.txt"), "w", encoding="utf-8").write(
            "번호: %02d\n제목: %s\n채널: %s\n주소: https://youtu.be/%s\n길이: %ss\n업로드: %s\n"
            % (n, m["title"], m.get("channel"), vid, m.get("duration"), m.get("upload_date")))
        idx.append((n, vid, m.get("channel"), m["title"], m.get("upload_date"), m.get("duration")))
        if a.whisper == "off":
            continue

        # ① 자막 ----------------------------------------------------------
        tr = os.path.join(seg, "transcript.txt"); has_sub = os.path.exists(tr)
        if not has_sub:
            subs, autos = m.get("subtitles") or {}, m.get("automatic_captions") or {}
            orig = a.lang + "-orig"
            if a.lang in subs:
                args, kind = ["--write-subs", "--sub-langs", a.lang], "사람자막"
            elif orig in autos or a.lang in autos:
                args, kind = ["--write-auto-subs", "--sub-langs", orig if orig in autos else a.lang], "자동자막"
            else:
                args, kind = None, None
            if args:
                subprocess.run(["yt-dlp", "--no-warnings", "--skip-download"] + args +
                               ["--sub-format", "vtt", "-o", os.path.join(seg, "source.%(ext)s"), "--", vid],
                               capture_output=True)
                v = sorted(glob.glob(os.path.join(seg, "source*.vtt")))
                if v:
                    lines = vtt2lines(v[0])
                    io.open(tr, "w", encoding="utf-8").write("\n".join(lines))
                    io.open(os.path.join(work, "_out_%s.txt" % vid), "w", encoding="utf-8").write(
                        "### " + os.path.basename(d) + " (자막: " + kind + ")\n" + paragraphs(lines))
                    has_sub = True
                    log("%02d 자막 %s %d줄 [OK %s]" % (n, kind, len(lines), vid))
                else:
                    log("%02d 자막 받기 실패 [ERROR %s]" % (n, vid)); time.sleep(20)
            else:
                log("%02d 자막 없음 → whisper 가 유일한 판독 [NOSUB %s]" % (n, vid))
        else:
            log("%02d 자막 이미 있음 [SKIP %s]" % (n, vid))

        # ② whisper -------------------------------------------------------
        if a.whisper != "both" or not have_whisper:
            time.sleep(5); continue
        wout = os.path.join(seg, "whisper_medium")
        if os.path.exists(wout + ".txt") and os.path.getsize(wout + ".txt") > 200:
            wtxt = os.path.join(work, "_whisper_%s.txt" % vid)
            if not os.path.exists(wtxt) and os.path.exists(wout + ".vtt"):   # 받아 적기는 끝났는데 정리 전에 죽은 경우
                sec0 = sections.get(vid)
                wl = vtt2lines(wout + ".vtt", offset=sec0[0] if sec0 else 0)
                io.open(wtxt, "w", encoding="utf-8").write("### " + os.path.basename(d) + " (whisper medium)\n" + paragraphs(wl))
                log("%02d whisper 정리만 다시 %d줄 [OK %s]" % (n, len(wl), vid))
            log("%02d whisper 이미 있음 [SKIP %s]" % (n, vid)); time.sleep(3); continue
        sec = sections.get(vid)
        if sec is None and has_sub and a.whisper_max_min and dur > a.whisper_max_min * 60:
            log("%02d %.0f분 — 자막이 있어 전체 whisper 는 건너뜀. 인용 구간을 --section %s=MM:SS-MM:SS 로 다시 [WHISPER_SKIPPED_LONG %s]"
                % (n, dur / 60, vid, vid))
            time.sleep(5); continue
        for f in glob.glob(os.path.join(d, "src.*")): os.remove(f)
        r = subprocess.run(["yt-dlp", "--no-warnings", "-N", "8", "-f", "bestaudio",
                            "-o", os.path.join(d, "src.%(ext)s"), "--", vid], capture_output=True)
        src = glob.glob(os.path.join(d, "src.*"))
        if not src:
            log("%02d 음성 다운로드 실패 [ERROR %s] %s" % (n, vid, r.stderr.decode("utf-8", "replace")[-200:]))
            time.sleep(20); continue
        wav = os.path.join(d, "audio.wav")
        cut = ["-ss", str(sec[0]), "-to", str(sec[1])] if sec else []   # 전체 받고 잘라내기(--download-sections 금지)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + cut +
                       ["-i", src[0], "-ar", "16000", "-ac", "1", wav])
        for f in src: os.remove(f)
        t0 = time.time()
        subprocess.run([CLI, "-m", MODEL, "-l", a.lang, "-t", "8", "-mc", "0", "-bo", "5", "-bs", "5",   # -mc 0: 환각 반복 루프 방지(2026-10-12)
                        "-f", wav, "-otxt", "-ovtt", "-of", wout],
                       capture_output=True)
        if os.path.exists(wout + ".vtt"):
            os.remove(wav)
            wl = vtt2lines(wout + ".vtt", offset=sec[0] if sec else 0)
            io.open(os.path.join(work, "_whisper_%s.txt" % vid), "w", encoding="utf-8").write(
                "### " + os.path.basename(d) + " (whisper medium" +
                (", 구간 %d:%02d~%d:%02d" % (sec[0] // 60, sec[0] % 60, sec[1] // 60, sec[1] % 60) if sec else "") +
                ")\n" + paragraphs(wl))
            log("%02d whisper %d줄 %.0f초 [OK %s]" % (n, len(wl), time.time() - t0, vid))
        else:
            log("%02d whisper 실패 — 음성은 %s 에 남김 [ERROR %s]" % (n, wav, vid))
        time.sleep(5)
    io.open(os.path.join(work, a.list), "w", encoding="utf-8").write(
        "\n".join("\t".join(str(x) for x in r) for r in idx))
    log("=== 끝 [DONE]")


if __name__ == "__main__":
    main()
