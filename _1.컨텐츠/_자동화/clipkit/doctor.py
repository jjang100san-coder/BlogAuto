# -*- coding: utf-8 -*-
# 클립 제작 환경 점검 — 한 번에 뭐가 있고 없는지 (2026.10.19, 클라우드 세션에서 만든 검사들을 데스크톱에 한꺼번에 붙일 때)
#   python doctor.py            표로 보여 준다
#   python doctor.py --install  없는 pip 패키지를 깐다(whisper 모델·글꼴·크롬은 손으로)
import os, sys, shutil, subprocess, importlib

ROWS = [
    # (이름, 종류, 확인, 없을 때 할 것, 어디서 쓰나)
    ('ffmpeg', 'exe', lambda: shutil.which('ffmpeg'), 'ffmpeg 설치 후 PATH', 'tactics·narr_proc·loudnorm·scene_cuts 전부'),
    ('Pillow', 'pip', 'PIL', 'pip install pillow', '모든 장면 그리기'),
    ('numpy', 'pip', 'numpy', 'pip install numpy', 'voice_check·face_boxes'),
    ('playwright', 'pip', 'playwright', 'pip install playwright && python -m playwright install chromium', 'fill_clip·html_anim·clip_frames'),
    ('kiwipiepy', 'pip', 'kiwipiepy', 'pip install kiwipiepy', 'pron_book 소리 검사(품사) · draft_lint 2-7-1 보강 예정'),
    ('g2pkiwi', 'pip', 'g2pkiwi', 'pip install g2pkiwi', 'pron_book 소리 검사(발음형)'),
    ('scenedetect', 'pip', 'scenedetect', 'pip install scenedetect opencv-python-headless', 'scene_cuts 컷 후보'),
    ('deface', 'pip', 'deface', 'pip install deface', 'face_boxes 얼굴 상자'),
    ('faster-whisper', 'pip', 'faster_whisper', 'pip install faster-whisper  (선택 — whisper-cli 대신, 단어 시각)', 'stt'),
    ('whisper-cli', 'exe', lambda: os.path.exists(os.path.expandvars(r"%USERPROFILE%\tools\whisper\Release\whisper-cli.exe")), '지금 쓰는 whisper.cpp — 경로 stt.WH', 'stt(cli)'),
    ('ggml-medium', 'file', lambda: os.path.exists(os.path.expandvars(r"%USERPROFILE%\.claude\models\ggml-medium.bin")), 'stt.MD 경로', 'stt(cli)'),
    ('faster-whisper 모델', 'file', lambda: os.path.exists(os.path.join(os.environ.get('CLIP_FW_MODEL') or os.path.expandvars(r"%USERPROFILE%\.claude\models\faster-whisper-medium"), 'model.bin')), 'python stt.py pull  (선택)', 'stt(fw) · narr_words 단어 시각'),
    ('맑은 고딕 Bold', 'file', lambda: os.path.exists('C:/Windows/Fonts/malgunbd.ttf'), '윈도우 기본 글꼴 — tactics.FONT_B', '자막'),
    ('NotoSansKR-VF', 'file', lambda: os.path.exists(r'C:\Windows\Fonts\NotoSansKR-VF.ttf'), 'Google Noto Sans KR 가변 글꼴 설치', '농구·학군 카드'),
    ('크롬', 'exe', lambda: os.path.exists(r'C:\Program Files\Google\Chrome\Application\chrome.exe'), 'fill_clip.CHROME', 'fill_clip·set_clip_covers'),
]


def check(row):
    name, kind, how, fix, use = row
    if kind == 'pip':
        try:
            m = importlib.import_module(how); ver = getattr(m, '__version__', '')
            return True, ver
        except Exception:
            return False, ''
    return (bool(how()), '')


def main(install=False):
    missing = []
    print('%-22s %-4s %-10s %s' % ('항목', '', '버전', '쓰는 곳'))
    for row in ROWS:
        ok, ver = check(row)
        print('%-22s %-4s %-10s %s' % (row[0], '✅' if ok else '❌', ver, row[4]))
        if not ok:
            missing.append(row)
    if missing:
        print('\n없는 것 %d — 할 것:' % len(missing))
        for r in missing:
            print('  %-22s %s' % (r[0], r[3]))
    if install:
        pk = [r[3].split()[2] for r in missing if r[1] == 'pip' and r[3].startswith('pip install')]
        extra = [w for r in missing if r[1] == 'pip' and r[3].startswith('pip install') for w in r[3].split('(')[0].split()[2:] if not w.startswith('&&')]
        if extra:
            print('\npip install', ' '.join(dict.fromkeys(extra)))
            subprocess.run([sys.executable, '-m', 'pip', 'install', *dict.fromkeys(extra)])
    return missing


if __name__ == '__main__':
    main('--install' in sys.argv)
