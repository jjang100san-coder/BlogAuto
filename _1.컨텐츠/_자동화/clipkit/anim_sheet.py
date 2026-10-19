# python anim_sheet.py <클립 폴더> <이름,...> [끝 프레임 비율 0~1]  → <폴더>\_anim_check.jpg (장면마다 프레임 하나씩 모아 보기)
import os, sys
from PIL import Image
d, names = sys.argv[1], sys.argv[2].split(',')
r = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
ims = []
for n in names:
    fs = sorted(os.listdir(os.path.join(d, '_frames_' + n)))
    ims.append(Image.open(os.path.join(d, '_frames_' + n, fs[min(len(fs) - 1, int(len(fs) * r))])).resize((450, 446)))
c = 4; sh = Image.new('RGB', (450 * c, 446 * ((len(ims) + c - 1) // c)), (0, 0, 0))
for i, im in enumerate(ims): sh.paste(im, ((i % c) * 450, (i // c) * 446))
sh.save(os.path.join(d, '_anim_check.jpg'), quality=85); print('ok')
