# -*- coding: utf-8 -*-
# 사진 한 장에 깊이 패럴랙스 움직임 — Higgsfield 움직임 컷(4크레딧/6초)의 공짜 대안 (2026.10.19)
#   엔진: DepthFlow(AGPL-3.0 — 도구일 뿐, 결과 영상엔 안 붙는다) + Depth Anything V2 깊이 추정(첫 실행 때 Hugging Face 에서 모델 내려받음).
#   pip install depthflow   (torch 가 같이 깔린다 — 1GB 넘음. GPU 없으면 CPU 로 돌아가지만 느리다: 먼저 한 장으로 시간을 잰다)
#   ⚠ 이 스크립트는 클라우드 세션에서 모델을 못 받아 **실행 시험을 못 했다**. 데스크톱 첫 실행 때 오류가 나면 `depthflow --help` 와 비교해 고친다.
#
#   어디에 맞나(클립 지침 5장 그대로): 넓은 풍경·건물 — 카메라가 천천히 들어가는 느낌. 물·풀·깃발의 실제 흔들림은 못 만든다(그건 Higgsfield).
#   주인공이 작은 사진·사람 사진은 금지(깊이가 틀리면 가장자리가 찢긴다). 결과는 make_clip 의 `src='video:…'` 로 넣는다.
#
#   python depth_motion.py <사진> [--preset zoomin|dolly|horizontal|vertical|orbital] [--sec 6] [--amp 0.5] [--out <mp4>]
#     --amp   움직임 세기(0.3 은은 ~ 1.0 과함). 「static camera」 느낌은 0.3~0.5
#   → <사진>_depth.mp4 (1080×1920, 30fps). 입력은 먼저 9:16 으로 자른다(가운데 기준, 지침 5장 「입력은 미리 9:16」)
import os, sys, math, tempfile
from PIL import Image

W, H, FPS = 1080, 1920, 30


def to_916(src, cx=0.5):
    """9:16 으로 자르기(가로 중심 cx 0~1). 세로가 모자라면 위아래 흐린 배경 없이 그냥 가운데 크롭."""
    im = Image.open(src).convert('RGB'); w, h = im.size
    if w / h > W / H:
        nw = int(h * W / H); x0 = int(max(0, min(w - nw, cx * w - nw / 2))); im = im.crop((x0, 0, x0 + nw, h))
    else:
        nh = int(w * H / W); y0 = (h - nh) // 2; im = im.crop((0, y0, w, y0 + nh))
    im = im.resize((W, H), Image.LANCZOS)
    p = os.path.join(tempfile.gettempdir(), 'depth_in_%d.png' % os.getpid()); im.save(p)
    return p


def make(src, preset='zoomin', sec=6.0, amp=0.5, out=None, cx=0.5):
    try:
        from depthflow.scene import DepthScene
    except ImportError:
        raise SystemExit('depthflow 가 없다:  pip install depthflow  (torch 포함, 1GB+)')

    class Scene(DepthScene):
        def update(self):
            u = self.cycle / (2 * math.pi) if hasattr(self, 'cycle') else (self.time / max(sec, 0.01))   # 0→1 진행
            u = min(1.0, max(0.0, u))
            ease = u * u * (3 - 2 * u)   # 처음·끝 천천히(smoothstep — make_clip 줌과 같은 결)
            self.state.steady = 0.30
            self.state.isometric = 0.60
            if preset == 'zoomin':        # 천천히 들어가기 — 후킹·넓은 풍경
                self.state.height = 0.15 + 0.25 * amp * ease
                self.state.zoom = 1.0 - 0.08 * amp * ease
            elif preset == 'dolly':       # 돌리 줌 — 배경이 당겨지는 느낌
                self.state.height = 0.30
                self.state.focus = 0.35
                self.state.zoom = 0.95
                self.state.isometric = 0.5 * (1.0 - math.cos(math.pi * ease)) * amp
            elif preset == 'horizontal':  # 좌우로 살짝
                self.state.offset = (0.6 * amp * math.sin(math.pi * ease), 0.0)
            elif preset == 'vertical':    # 위아래로 살짝
                self.state.offset = (0.0, 0.6 * amp * math.sin(math.pi * ease))
            elif preset == 'orbital':     # 초점 주위를 도는 느낌
                self.state.focus = 0.30
                self.state.zoom = 0.98
                self.state.isometric = 0.5 * math.cos(2 * math.pi * u) * amp + 0.75
                self.state.offset = (0.5 * amp * math.sin(2 * math.pi * u), 0.0)

    out = out or os.path.splitext(src)[0] + '_depth.mp4'
    img = to_916(src, cx)
    scene = Scene(backend='headless')
    scene.input(image=img)
    scene.main(output=out, fps=FPS, time=sec, width=W, height=H, ssaa=1.5, loop=1)
    os.remove(img)
    print('→', out)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    g = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    make(a[0], g('--preset', 'zoomin'), g('--sec', 6.0), g('--amp', 0.5), g('--out', '') or None, g('--cx', 0.5))
