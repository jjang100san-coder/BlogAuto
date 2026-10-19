# 개념도(두 칸 전술판)에서 경기장 테두리와 점(수원 주황·상대 파랑)을 뽑아 0~1 좌표로 → dots.json
# 전술판 세 원칙 ① 정확한 배치: 손으로 옮겨 적지 않고 그림에서 바로 읽는다
import sys, json, os
import numpy as np
from PIL import Image

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'jhb2', 'images')
OR = np.array([208, 119, 63]); BL = np.array([46, 156, 192])


def pitches(a):
    """경기장 테두리(밝은 회녹색 선) — 세로선이 길게 이어지는 x 와 가로선 y 를 찾는다."""
    g = a.astype(int)
    line = (abs(g[..., 0] - 92) < 30) & (abs(g[..., 1] - 120) < 30) & (abs(g[..., 2] - 118) < 30)
    cols = line.sum(0); rows = line.sum(1)
    xs = [x for x in range(a.shape[1]) if cols[x] > 500]
    ys = [y for y in range(a.shape[0]) if rows[y] > 300]
    # 묶기
    def groups(v):
        out = []
        for x in v:
            if out and x - out[-1][-1] <= 3: out[-1].append(x)
            else: out.append([x])
        return [int(np.mean(o)) for o in out]
    return groups(xs), groups(ys)


def dots(a, col):
    d = np.abs(a[..., :3].astype(int) - col).sum(-1) < 60
    ys, xs = np.where(d)
    cl = []   # [sumx, sumy, n, cx, cy]
    for x, y in zip(xs, ys):
        for c in cl:
            if abs(c[3] - x) < 22 and abs(c[4] - y) < 22:
                c[0] += x; c[1] += y; c[2] += 1; c[3] = c[0] / c[2]; c[4] = c[1] / c[2]; break
        else:
            cl.append([x, y, 1, x, y])
    return [(round(c[3], 1), round(c[4], 1)) for c in cl if 120 < c[2] < 1500]


res = {}
for f in sys.argv[1:]:
    a = np.array(Image.open(os.path.join(IMG, f)).convert('RGB'))
    xs, ys = pitches(a)
    res[f] = {'xs': xs, 'ys': ys, 'orange': dots(a, OR), 'blue': dots(a, BL)}
    print(f, 'xs', xs, 'ys', ys, 'or', len(res[f]['orange']), 'bl', len(res[f]['blue']))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dots_raw.json'), 'w'), indent=1)
