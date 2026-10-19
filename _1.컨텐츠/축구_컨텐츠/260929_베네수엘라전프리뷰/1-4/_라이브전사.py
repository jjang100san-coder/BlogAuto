# -*- coding: utf-8 -*-
"""아카이브 처리 중(post_live)인 라이브를 오디오만 받아 whisper 로 전사한다.

videoscan 은 영상까지 받고 자막이 없으면 4스레드로 돌려 느리다. 토크 라이브는 화면이 필요 없으니
오디오 전용 DASH 트랙만 받는다. --abort-on-unavailable-fragment 로 조각 누락 시 중단(깨진 파일 방지).
whisper-cli 는 일본어 경로를 못 받으므로 ASCII 임시 폴더에서 돌리고 결과만 가져온다.
로그에는 ASCII 마커를 남긴다(PowerShell/grep 에서 한글 조건이 깨진 전례).
사용: python _라이브전사.py <video_id> [threads]
"""
import io, json, os, re, shutil, subprocess, sys, tempfile, time
BASE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE, "_라이브전사.log")
CLI = os.path.join(os.path.expanduser("~"), "tools", "whisper", "Release", "whisper-cli.exe")
MODEL = os.path.join(os.path.expanduser("~"), ".claude", "models", "ggml-medium.bin")
BAD = re.compile(r'[\/:*?"<>|]'); WS = re.compile(r"\s+")

def log(m):
    line = "%s  %s" % (time.strftime("%H:%M:%S"), m)
    io.open(LOG, "a", encoding="utf-8").write(line + "\n"); print(line); sys.stdout.flush()

def main(vid, threads):
    r = subprocess.run(["yt-dlp", "--no-warnings", "--skip-download", "--dump-json",
                        "https://www.youtube.com/watch?v=" + vid], capture_output=True)
    d = json.loads(r.stdout.decode("utf-8", "replace"))
    title = WS.sub(" ", BAD.sub("", d["title"])).strip().rstrip(". ")[:100]
    seg = os.path.join(BASE, title, "seg"); os.makedirs(seg, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="livews_")
    log("[START %s] %s | status=%s dur=%s" % (vid, title[:40], d.get("live_status"), d.get("duration")))
    r = subprocess.run(["yt-dlp", "--no-warnings", "-f", "140/139/bestaudio", "-N", "4",
                        "--abort-on-unavailable-fragment", "-o", os.path.join(tmp, "a.%(ext)s"),
                        "https://www.youtube.com/watch?v=" + vid], capture_output=True)
    files = [f for f in os.listdir(tmp) if f.startswith("a.")]
    if r.returncode != 0 or not files:
        log("[ERROR %s] download: %s" % (vid, r.stderr.decode("utf-8", "replace")[-300:])); return
    src = os.path.join(tmp, files[0])
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "default=nw=1:nk=1", src], capture_output=True)
    got = float(p.stdout.decode().strip() or 0)
    log("[DOWNLOADED %s] %.0fs (expected %s)" % (vid, got, d.get("duration")))
    if d.get("duration") and got < 0.95 * d["duration"]:
        log("[ERROR %s] audio too short — archive incomplete, stop" % vid); return
    wav = os.path.join(tmp, "a.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-ar", "16000", "-ac", "1",
                    "-c:a", "pcm_s16le", wav], check=True)
    log("[WHISPER %s] medium ja, threads=%d" % (vid, threads))
    t0 = time.time()
    r = subprocess.run([CLI, "-m", MODEL, "-f", wav, "-l", "ja", "-t", str(threads),
                        "-ovtt", "-of", os.path.join(tmp, "whisper")], capture_output=True)
    vtt = os.path.join(tmp, "whisper.vtt")
    if not os.path.exists(vtt):
        log("[ERROR %s] whisper: %s" % (vid, r.stderr.decode("utf-8", "replace")[-300:])); return
    shutil.copy2(vtt, os.path.join(seg, "whisper.vtt"))
    lines, cur = [], None
    for ln in io.open(vtt, encoding="utf-8"):
        ln = ln.strip()
        m = re.match(r"(\d+):(\d+):(\d+)\.\d+\s+-->", ln)
        if m:
            cur = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)); continue
        if cur is not None and ln and not ln.startswith("WEBVTT"):
            lines.append("[%d:%02d] %s" % (cur//60, cur%60, ln)); cur = None
    io.open(os.path.join(seg, "transcript.txt"), "w", encoding="utf-8").write("\n".join(lines))
    log("[DONE %s] %d lines, whisper %.0f min" % (vid, len(lines), (time.time()-t0)/60))
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 12)
