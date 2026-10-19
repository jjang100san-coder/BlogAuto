from PIL import Image
import os, sys
names=['count','score','grades','ch1','canada','ch2','three','gyeongju','ch3','split','recap']
ims=[]
for n in names:
    fs=sorted(os.listdir('_frames_'+n)); ims.append(Image.open('_frames_'+n+'/'+fs[-1]).resize((450,446)))
sh=Image.new('RGB',(450*4,446*3),(0,0,0))
for i,im in enumerate(ims): sh.paste(im,((i%4)*450,(i//4)*446))
sh.save('_anim_check.jpg',quality=85)
