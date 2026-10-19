# 클립 내레이션 받아쓰기 검사 — MiniMax 가 대본에 없는 소리를 붙이거나(「그리고 나즈게이트」) 같은 소리를 반복하는 걸 잡는다
# 사용: python check_narration.py <글폴더>\clip
#   → narration\n*.mp3 를 whisper(medium, 한국어)로 받아써서 길이와 함께 출력. 끝에 대본에 없는 말이 붙었는지 눈으로 본다
import sys, os, re, glob, subprocess, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clipkit'))
import stt   # 엔진(whisper-cli / faster-whisper)은 clipkit\stt.py 가 고른다(10/19)


def media_dur(path):
    """미디어 길이(초). ffprobe 가 윈도우 앱 제어 정책에 막혀서(10/7) ffmpeg 출력의 Duration 으로 잰다."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path], capture_output=True, text=True, encoding='utf-8', errors='replace')
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    if not m:
        raise SystemExit('길이를 못 읽음: ' + path)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main(clip_dir):
    tmp = tempfile.mkdtemp()
    w = os.path.join(tmp, "x.wav")
    for f in sorted(glob.glob(os.path.join(clip_dir, "narration", "n[0-9][0-9].mp3"))):
        d = media_dur(f)
        lines = [stt.transcribe(f)]
        flag = " !!12초 초과" if d > 12 else ""
        print("%s  %.1f초%s" % (os.path.basename(f), d, flag))
        for l in lines:
            print("    " + l)


if __name__ == "__main__":
    main(sys.argv[1])
