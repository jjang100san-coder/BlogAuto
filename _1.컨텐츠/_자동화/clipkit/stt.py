# -*- coding: utf-8 -*-
# 받아쓰기 한 곳에서 — whisper-cli(ggml medium, 지금 쓰는 것) 또는 faster-whisper(CTranslate2, CPU 에서 2~4배 빠름 · 단어 시각) (2026.10.19)
#   narr_pick.py · check_narration.py · narr_words.py 가 부른다. 호출하는 쪽은 엔진을 모른다.
#
#   엔진 고르기(순서대로):
#     1) 환경변수 CLIP_STT=cli | fw 로 강제
#     2) faster-whisper 모델이 로컬에 있으면 fw  — FW_MODEL 폴더(기본 %USERPROFILE%\.claude\models\faster-whisper-medium)
#        모델 받기(한 번, 데스크톱):  pip install faster-whisper  →  python stt.py pull   (Hugging Face 에서 Systran/faster-whisper-medium)
#     3) 아니면 whisper-cli (WH · MD 경로) — 예전과 똑같은 명령·출력
#
#   python stt.py <소리파일>            받아쓴 글 한 줄
#   python stt.py words <소리파일>      단어마다 시각 [(시작, 끝, 낱말)] — fw 만. cli 면 빈 목록
#   python stt.py pull                  faster-whisper medium 모델 내려받기
#   python stt.py which                 어느 엔진을 쓰는지
import os, sys, json, subprocess, tempfile

WH = os.path.expandvars(r"%USERPROFILE%\tools\whisper\Release\whisper-cli.exe")
MD = os.path.expandvars(r"%USERPROFILE%\.claude\models\ggml-medium.bin")
FW_MODEL = os.environ.get('CLIP_FW_MODEL') or os.path.expandvars(r"%USERPROFILE%\.claude\models\faster-whisper-medium")
FW_NAME = 'Systran/faster-whisper-medium'
_fw = None


def engine():
    e = os.environ.get('CLIP_STT', '').lower()
    if e in ('cli', 'fw'):
        return e
    if os.path.isdir(FW_MODEL) and os.path.exists(os.path.join(FW_MODEL, 'model.bin')):
        try:
            import faster_whisper  # noqa
            return 'fw'
        except ImportError:
            pass
    return 'cli'


def _wav16(f):
    """whisper 입력은 16k mono wav. 이름에 pid 를 넣어 두 클립을 같이 돌려도 안 섞이게(10/14)."""
    w = os.path.join(tempfile.gettempdir(), 'stt_%d_%d.wav' % (os.getpid(), abs(hash(f)) % 10000))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-ar', '16000', '-ac', '1', w], check=True)
    return w


def _fw_model():
    global _fw
    if _fw is None:
        from faster_whisper import WhisperModel
        _fw = WhisperModel(FW_MODEL, device='cpu', compute_type='int8')
    return _fw


def transcribe(f, lang='ko'):
    """받아쓴 글 한 줄(공백으로 이어서). 예전 narr_pick.stt / check_narration 와 같은 꼴."""
    if engine() == 'fw':
        segs, _ = _fw_model().transcribe(f, language=lang, beam_size=5, vad_filter=False)
        return ' '.join(s.text.strip() for s in segs if s.text.strip())
    w = _wav16(f)
    r = subprocess.run([WH, '-m', MD, '-l', lang, '-nt', '-f', w], capture_output=True, text=True, encoding='utf-8', errors='replace')
    os.remove(w)
    return ' '.join(l.strip() for l in r.stdout.splitlines() if l.strip())


def words(f, lang='ko'):
    """단어마다 [(시작초, 끝초, 낱말)]. faster-whisper 만 준다(whisper-cli 는 빈 목록 → 호출하는 쪽이 비례 배분으로)."""
    if engine() != 'fw':
        return []
    segs, _ = _fw_model().transcribe(f, language=lang, beam_size=5, word_timestamps=True, vad_filter=False)
    out = []
    for s in segs:
        for w in (s.words or []):
            if w.word.strip():
                out.append((round(w.start, 3), round(w.end, 3), w.word.strip()))
    return out


def pull():
    from faster_whisper.utils import download_model
    os.makedirs(FW_MODEL, exist_ok=True)
    p = download_model(FW_NAME, output_dir=FW_MODEL)
    print('받음:', p)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'which':
        print('엔진:', engine(), '| fw 모델:', FW_MODEL, '(있음)' if os.path.isdir(FW_MODEL) else '(없음)', '| cli:', WH, '(있음)' if os.path.exists(WH) else '(없음)')
    elif a[0] == 'pull':
        pull()
    elif a[0] == 'words':
        print(json.dumps(words(a[1]), ensure_ascii=False))
    else:
        print(transcribe(a[0]))
