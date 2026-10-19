import sys, os, re, zipfile, math, json
sys.path.insert(0, r"C:\Users\user\Desktop\자동화\블로그용\Keyword_Reader")
import mountaindata as md
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F=r"C:\Windows\Fonts\malgun.ttf"; fm.fontManager.addfont(F); fm.fontManager.addfont(r"C:\Windows\Fonts\malgunbd.ttf")
plt.rcParams['font.family']=fm.FontProperties(fname=F).get_name()
OUT=r"C:\Users\user\Desktop\Blog\_1.컨텐츠\등산_컨텐츠\261011_오산기준_후보산"
Z=zipfile.ZipFile(os.path.expandvars(r'%LOCALAPPDATA%\ContentTrendRadar\mountain\peaks.zip'))
dem=md.Dem()
def tracks(prefix):
    segs=[]
    for n in Z.namelist():
        if not n.startswith(prefix): continue
        s=Z.read(n).decode('utf-8','replace')
        for seg in re.findall(r'<trkseg>(.*?)</trkseg>',s,re.S):
            pts=[(float(a),float(b)) for a,b in re.findall(r'<trkpt[^>]*lat="([\d.]+)"[^>]*lon="([\d.]+)"',seg)]
            if len(pts)>5: segs.append(pts)
    return segs
def dem_max(lat,lon,r=0.015,step=0.0006):
    best=(-1,lat,lon); la=lat-r
    while la<=lat+r:
        lo=lon-r*1.25
        while lo<=lon+r*1.25:
            e=dem.ele(la,lo) or 0
            if e>best[0]: best=(e,la,lo)
            lo+=step
        la+=step
    return best
M=[
 dict(name='무봉산 (화성 동탄)', summit=None, seed=(37.2093,127.1498), gpx=None, access=[('만의사 (차로 진입)',37.2093,127.1498)], note='GPS 코스 자료 없음 · 정상은 지형 고도 최고점으로 추정'),
 dict(name='건달산 (화성 봉담)', summit=(37.1909,126.9211), gpx='1311010029_건달산/', access=None, note='산림청 335m'),
 dict(name='서봉산 (화성 정남)', summit=(37.1587,126.9448), gpx='1311030108_서봉산/', access=None, note='산림청 250m'),
 dict(name='칠보산 (수원 호매실)', summit=(37.2607,126.9323), gpx=None, access=None, note='GPS 코스 자료 없음 · 238m'),
 dict(name='석성산 (용인 동백)', summit=(37.2726,127.1729), gpx='1311010304_석성산/', access=[('동백제7호나래공원 (동백역 650m)',37.2721,127.1592)], note='산림청 471m — 조건 초과'),
 dict(name='바라산 (의왕)', summit=(37.3687,127.0271), gpx='1311010215_바라산/', access=None, note='산림청 427m · GPS 기록은 450m 봉까지'),
]
for m in M:
    if m['summit'] is None:
        e,la,lo=dem_max(*m['seed']); m['summit']=(la,lo); m['summit_ele']=e
    else:
        m['summit_ele']=dem.ele(*m['summit'])
    la0,lo0=m['summit']; R=0.022; RL=R*1.27; N=110
    lats=[la0-R+2*R*i/(N-1) for i in range(N)]; lons=[lo0-RL+2*RL*j/(N-1) for j in range(N)]
    grid=[[max(0.0,dem.ele(la,lo) or 0) for lo in lons] for la in lats]
    fig,ax=plt.subplots(figsize=(9,8.2),dpi=150)
    zmax=max(max(r) for r in grid); zmin=min(min(r) for r in grid)
    levels=list(range(max(0,int(zmin//25*25)),int(zmax//25*25)+50,25))
    cf=ax.contourf(lons,lats,grid,levels=levels,cmap='YlGn',alpha=0.85)
    cs=ax.contour(lons,lats,grid,levels=levels,colors='#556b2f',linewidths=0.5)
    ax.clabel(cs,levels[::2],fmt='%d',fontsize=7,colors='#2f3f1f')
    fig.colorbar(cf,ax=ax,shrink=0.7,label='고도 m')
    segs=tracks(m['gpx']) if m['gpx'] else []
    for s in segs: ax.plot([p[1] for p in s],[p[0] for p in s],color='#c0392b',lw=1.4,alpha=0.9)
    # lowest trailhead among GPX segment ends (= car access candidate)
    ends=[]
    for s in segs:
        for p in (s[0],s[-1]): ends.append((dem.ele(*p) or 0,p))
    ends.sort()
    if ends:
        e,(pla,plo)=ends[0]; ax.plot(plo,pla,marker='s',ms=9,color='#1f77b4',mec='white')
        ha='right' if plo<lo0 else 'left'; dx=-8 if plo<lo0 else 8
        ax.annotate('가장 낮은 들머리 %dm'%e,(plo,pla),xytext=(dx,-14),textcoords='offset points',ha=ha,fontsize=9,color='#1f77b4',fontweight='bold',bbox=dict(fc='white',ec='none',alpha=.8))
    for lab,ala,alo in (m['access'] or []):
        ax.plot(alo,ala,marker='P',ms=11,color='#1f77b4',mec='white')
        ax.annotate(lab,(alo,ala),xytext=(-8,14),textcoords='offset points',ha='right',fontsize=9,color='#1f77b4',fontweight='bold',bbox=dict(fc='white',ec='none',alpha=.8))
    ax.plot(lo0,la0,marker='^',ms=12,color='#111',mec='white')
    ax.annotate('정상 (지형 %dm)'%(m['summit_ele'] or 0),(lo0,la0),xytext=(8,8),textcoords='offset points',fontsize=10,fontweight='bold',bbox=dict(fc='white',ec='none',alpha=.8))
    # scale bar 1km
    km=1/ (111.32*math.cos(math.radians(la0))); x0=lo0-RL+RL*0.08; y0=la0-R+R*0.08
    ax.plot([x0,x0+km],[y0,y0],color='k',lw=3); ax.text(x0+km/2,y0+R*0.03,'1 km',ha='center',fontsize=9)
    ax.set_xlim(lons[0],lons[-1]); ax.set_ylim(lats[0],lats[-1]); ax.set_aspect(1/math.cos(math.radians(la0))); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('%s — 등고선 25m 간격 · 빨간 선 = GPS 기록 등산로\n%s'%(m['name'],m['note']),fontsize=12)
    fig.text(0.5,0.01,'직접 만든 지도 · 고도: 지형 타일(terrarium z14, ±10m) · 등산로: 공공데이터 봉우리 GPX(개인 기록) · 등고선은 지형이지 등산로가 아님',ha='center',fontsize=7.5,color='#666')
    fn=re.sub(r'[ ()·]','_',m['name'].split(' ')[0])
    fig.savefig(os.path.join(OUT,'contour_%s.png'%fn),bbox_inches='tight',facecolor='white'); plt.close(fig)
    print(m['name'],'summit',m['summit'],m['summit_ele'],'segs',len(segs),'lowest trailhead',ends[0] if ends else None)
