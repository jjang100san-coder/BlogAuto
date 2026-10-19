import os, json, numpy as np
from PIL import Image
IMG = os.path.join(os.path.dirname(os.getcwd()), 'jhb2', 'images')
COL = {'kor': np.array([208, 119, 63]), 'opp': np.array([46, 156, 192])}
PX = [(75, 504), (575, 1004)]; Y0, Y1 = 230, 929
def blobs(a, col):
    d = np.abs(a[..., :3].astype(int) - col).sum(-1) < 70
    seen = np.zeros_like(d); out = []
    H, W = d.shape
    for y0 in range(Y0, Y1):
        for x0 in np.where(d[y0] & ~seen[y0])[0]:
            st = [(y0, x0)]; seen[y0, x0] = 1; pts = []
            while st:
                y, x = st.pop(); pts.append((y, x))
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    yy, xx = y+dy, x+dx
                    if 0 <= yy < H and 0 <= xx < W and d[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = 1; st.append((yy, xx))
            p = np.array(pts); h = np.ptp(p[:,0])+1; w = np.ptp(p[:,1])+1
            if len(p) > 250 and 18 < h < 40 and 18 < w < 40 and len(p) > 0.55*h*w:
                out.append((p[:,1].mean(), p[:,0].mean()))
    return out
res = {}
for f in ('03_p1_lure.png','05_p3_roles.png','06_p4_switch.png','08_p6_press.png'):
    a = np.array(Image.open(os.path.join(IMG, f)).convert('RGB'))
    r = {'L': [], 'R': []}
    for team, col in COL.items():
        for x, y in blobs(a, col):
            for side, (x0, x1) in zip('LR', PX):
                if x0 <= x <= x1:
                    r[side].append((team, round((x-x0)/(x1-x0), 3), round((y-Y0)/(Y1-Y0), 3)))
    res[f] = r
    print(f, {k: (sum(1 for t in v if t[0]=='kor'), sum(1 for t in v if t[0]=='opp')) for k, v in r.items()})
json.dump(res, open('dots.json', 'w'), indent=1)
