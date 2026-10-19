# -*- coding: utf-8 -*-
# 화면 녹화에서 기다리는 구간 자동으로 빼기 — 좌석 오픈·예약 화면처럼 화면이 멈춰 있는 동안을 잘라 낸다 (2026.10.19)
#   엔진: auto-editor(Unlicense). 첫 실행 때 GitHub 에서 실행 파일을 한 번 내려받는다.  pip install auto-editor
#   화면 녹화는 소리가 없으니 기본은 「움직임」 기준. 사람 말이 든 영상이면 --audio
#   결과는 컷 재료일 뿐 — 자막·내레이션은 make_clip/shorts 가 예전처럼 입힌다. 캡처 컷의 6-2·6-4 점검은 그대로(클립 지침 3-2)
#
#   python trim_idle.py <녹화.mp4> [--out <저장.mp4>] [--motion 0.02] [--margin 0.3] [--audio]
#     --motion  움직임 문턱(기본 2%. 커서 깜빡임까지 잡히면 0.04~0.06 으로)
#     --margin  남기는 구간 앞뒤로 더 남길 시간(초)
#     --audio   소리 기준(기본 -20dB 아래를 묵음으로)
#   → 저장 파일 + 남긴 구간 표(원본 시각 기준). 원본은 건드리지 않는다
import os, sys, json, shutil, subprocess

EXE = shutil.which('auto-editor') or os.path.join(os.path.dirname(sys.executable), 'Scripts', 'auto-editor.exe')


def dur(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path], capture_output=True, text=True, encoding='utf-8', errors='replace')
    import re
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def kept_ranges(v3_path):
    """auto-editor v3 내보내기에서 남긴 구간 [(원본 시작, 원본 끝)] — offset·dur 은 timebase(예 "30/1") 단위."""
    d = json.load(open(v3_path, encoding='utf-8'))
    num, den = (d.get('timebase') or '30/1').split('/'); fps = float(num) / float(den)
    out = []
    for clip in d.get('v', [[]])[0]:
        if isinstance(clip, dict) and 'offset' in clip:
            out.append((clip['offset'] / fps, (clip['offset'] + clip['dur']) / fps))
    return out


def main(src, out=None, motion=0.02, margin=0.3, audio=False):
    if not os.path.exists(EXE):
        raise SystemExit('auto-editor 가 없다:  pip install auto-editor')
    out = out or os.path.splitext(src)[0] + '_trim.mp4'
    edit = 'audio:threshold=-20dB' if audio else 'motion:threshold=%s' % motion
    common = [EXE, src, '--edit', edit, '--margin', '%ss' % margin, '--no-open']
    subprocess.run(common + ['-o', out], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    v3 = os.path.splitext(out)[0] + '.v3'
    subprocess.run(common + ['--export', 'v3', '-o', v3], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    a, b = dur(src), dur(out)
    print('%s  %.1f초 → %.1f초 (%.0f%% 뺌)  → %s' % (os.path.basename(src), a, b, 100 * (1 - b / a) if a else 0, out))
    for s, e in kept_ranges(v3):
        print('  남김  %6.2f ~ %6.2f  (%.2fs)' % (s, e, e - s))
    os.remove(v3)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    g = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    main(a[0], g('--out', ''), g('--motion', 0.02), g('--margin', 0.3), '--audio' in a)
