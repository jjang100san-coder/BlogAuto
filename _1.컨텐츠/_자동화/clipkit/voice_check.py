# 목소리 바뀜 찾기 — 같은 voice_id 로 뽑아도 가끔 다른(여자) 목소리가 나온다 (10/11 하코다테 n04 — 사용자 「갑자기 여자 목소리」)
# 음색(소리 난 구간의 평균 로그 스펙트럼 40칸)을 파일마다 재서, 모든 파일의 중앙 음색과 거리가 LIMIT 넘으면 「다른 목소리」
#  · 높이(Hz)만으론 못 가른다 — Kevin 이 127~171Hz 로 출렁이고 섞인 여자 목소리는 184Hz
#  · 음색 거리: Kevin 20개 1.5~4.5 / 여자 목소리 7.4 → 기준 6.0
# 사용: python voice_check.py a.mp3 b.mp3 … / narr_pick(고를 때 뺀다)·qa_clip ⑤(완성 줄 검사)가 부른다
# 파일이 3개 넘어야 중앙값이 뜻이 있다. 줄 대부분이 바뀐 목소리면 못 잡는다(그땐 귀로)
import sys, subprocess
import numpy as np

LIMIT = 6.0
_E = np.logspace(np.log10(80), np.log10(7900), 41)
_IDX = (_E / 16000 * 512).astype(int)


def profile(p):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float)
    fr = []
    for i in range(0, len(x) - 512, 256):
        w = x[i:i + 512]
        if np.abs(w).mean() < 800:
            continue
        s = np.abs(np.fft.rfft(w * np.hanning(512))) ** 2
        fr.append(np.log(np.array([s[_IDX[j]:max(_IDX[j + 1], _IDX[j] + 1)].mean() for j in range(40)]) + 1e-9))
    if len(fr) < 180:   # 소리 난 구간이 3초가 안 되면 음색이 흔들려 판정하지 않는다(10/13 지방 아파트 n08 1.5초 두 개가 6.4·7.8 로 오탐)
        return None
    v = np.mean(fr, 0)
    return v - v.mean()


def odd(files):
    """(다른 목소리 [(파일, 거리)], {파일: 거리})"""
    P = {f: profile(f) for f in files}
    P = {f: v for f, v in P.items() if v is not None}
    if len(P) < 3:
        return [], {}
    med = np.median(np.array(list(P.values())), 0)
    dist = {f: float(np.linalg.norm(v - med)) for f, v in P.items()}
    return [(f, d) for f, d in dist.items() if d > LIMIT], dist


if __name__ == '__main__':
    bad, dist = odd(sys.argv[1:])
    for f, d in dist.items():
        print('%-40s 음색 거리 %.2f%s' % (f, d, '  ← 다른 목소리' if d > LIMIT else ''))
    print('다른 목소리 %d개 (기준 %.1f)' % (len(bad), LIMIT))
