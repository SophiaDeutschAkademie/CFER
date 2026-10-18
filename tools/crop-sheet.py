# 여러 개를 한 장에 그린 시트(2:1)를 잘라 web/assets/img/kXX/ 에 webp로 저장 (SODA 삽화 스킬 규칙: 위쪽 88% 열 합계로 경계)
import sys, numpy as np
from PIL import Image
OUT="/home/user/CFER/web/assets/img/k01/"
def ink(a):  # 흰 배경이 아닌 픽셀
    return (a.min(axis=2) < 215)
def split(path, names, height, pad=0.07):
    im=Image.open(path).convert("RGB"); a=np.asarray(im); H,W,_=a.shape
    m=ink(a)
    col=m[:int(H*0.88)].sum(axis=0).astype(float)
    k=9; col=np.convolve(col,np.ones(k)/k,mode="same")
    n=len(names)
    # 빈 열(잉크 거의 없음)로 나뉜 잉크 구간을 찾고, 가장 큰 n개를 왼쪽부터 사용
    on=col>max(1.0,col.max()*0.03); segs=[]; x=0
    while x<W:
        if on[x]:
            s0=x
            while x<W and on[x]: x+=1
            segs.append([s0,x])
        else: x+=1
    merged=[]
    for sg in segs:   # 아주 좁은 틈은 같은 물체로
        if merged and sg[0]-merged[-1][1] < W*0.012: merged[-1][1]=sg[1]
        else: merged.append(sg)
    merged=sorted(sorted(merged,key=lambda g:-(col[g[0]:g[1]].sum()))[:n])
    cuts=[]
    if len(merged)!=n:   # 맞닿아 있으면: 등분 지점 근처에서 잉크가 가장 적은 열을 경계로
        b=[0]
        for i in range(1,n):
            c=int(W*i/n); lo,hi=c-int(W*0.07),c+int(W*0.07)
            b.append(lo+int(np.argmin(col[lo:hi])))
        b.append(W)
        merged=[[b[i],b[i+1]] for i in range(n)]
        for i in range(n): cuts.append((b[i],b[i+1]))
        merged=None
    for i in range(n if merged else 0):
        lo = 0 if i==0 else (merged[i-1][1]+merged[i][0])//2
        hi = W if i==n-1 else (merged[i][1]+merged[i+1][0])//2
        cuts.append((lo,hi))
    for i,name in enumerate(names):
        x0,x1=cuts[i]
        sub=m[:,x0:x1]; ys=np.where(sub.any(axis=1))[0]; xs=np.where(sub.any(axis=0))[0]
        box=(x0+xs[0], ys[0], x0+xs[-1]+1, ys[-1]+1)
        c=im.crop(box); w,h=c.size; p=int(max(w,h)*pad)
        canvas=Image.new("RGB",(w+2*p,h+2*p),"white"); canvas.paste(c,(p,p))
        r=height/canvas.height; canvas=canvas.resize((max(1,int(canvas.width*r)),height),Image.LANCZOS)
        canvas.save(OUT+name+".webp","WEBP",quality=84); print(name, canvas.size)
def scene(path,name,w=1280):
    im=Image.open(path).convert("RGB"); r=w/im.width
    im.resize((w,int(im.height*r)),Image.LANCZOS).save(OUT+name+".webp","WEBP",quality=82); print(name)
if __name__=="__main__":
    R=sys.argv[2] if len(sys.argv)>2 else "raw/"   # 원본 시트 폴더
    what=sys.argv[1]
    if what=="base":
        for s in ["story-1-bahnhof","story-2-wg","story-3-treppenhaus"]: scene(R+s+".webp",s)
        split(R+"sheet-koffer.webp",["ding-mantel","ding-foto","ding-brief","ding-tabletten","ding-anhaenger"],360)
        split(R+"sheet-kurs.webp",["person-carlos","person-tomasz","person-priya","person-minjun","person-wagner"],560)
    if what=="stimmung":
        split(R+"sheet-stimmung.webp",["stimmung-1-sehr-gut","stimmung-2-gut","stimmung-3-es-geht","stimmung-4-nicht-so-gut","stimmung-5-schlecht"],260)
    if what=="haus":
        split(R+"sheet-haus.webp",["person-jonas","person-lena","person-sujin","person-haeun","person-schulze"],560)
