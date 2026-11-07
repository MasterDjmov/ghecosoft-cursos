#!/usr/bin/env python3
"""Recorta una hoja sobre magenta en sus figuras con fondo transparente, ordenadas fila por fila."""
import sys,os
from PIL import Image
def run(src,out,name,target,count=8):
    im=Image.open(src).convert('RGB');w,h=im.size;px=im.load()
    o=Image.new('RGBA',(w,h));op=o.load();fg=bytearray(w*h)
    for y in range(h):
        for x in range(w):
            r,g,b=px[x,y];k=min(r,b)-g
            if k>70: continue
            if k>25:
                a=int(255*(70-k)/45);v=min(r,g+40);op[x,y]=(min(r,v),g,min(b,v),a)
            else: op[x,y]=(r,g,b,255)
            fg[y*w+x]=1
    seen=bytearray(w*h);comps=[]
    for i in range(w*h):
        if fg[i] and not seen[i]:
            st=[i];seen[i]=1;n=0;x0=y0=10**9;x1=y1=-1;pts=[]
            while st:
                j=st.pop();n+=1;pts.append(j);y,x=divmod(j,w);x0=min(x0,x);x1=max(x1,x);y0=min(y0,y);y1=max(y1,y)
                for d in (j-1,j+1,j-w,j+w):
                    if 0<=d<w*h and fg[d] and not seen[d]:seen[d]=1;st.append(d)
            comps.append(dict(n=n,box=[x0,y0,x1,y1],pts=pts))
    comps.sort(key=lambda c:-c['n']);big=comps[:count]
    for c in comps[count:]:
        if c['n']<12: continue
        cx=(c['box'][0]+c['box'][2])/2;cy=(c['box'][1]+c['box'][3])/2
        t=min(big,key=lambda b:abs((b['box'][0]+b['box'][2])/2-cx)+abs((b['box'][1]+b['box'][3])/2-cy))
        b=t['box'];b[0]=min(b[0],c['box'][0]);b[1]=min(b[1],c['box'][1]);b[2]=max(b[2],c['box'][2]);b[3]=max(b[3],c['box'][3]);t['pts']+=c['pts']
    mid=(min(c['box'][1] for c in big)+max(c['box'][3] for c in big))/2
    top=sorted([c for c in big if (c['box'][1]+c['box'][3])/2<mid],key=lambda c:c['box'][0]);bot=sorted([c for c in big if (c['box'][1]+c['box'][3])/2>=mid],key=lambda c:c['box'][0])
    maxh=max(c['box'][3]-c['box'][1] for c in big);f=target/maxh;os.makedirs(out,exist_ok=True)
    for k,c in enumerate(top+bot):
        x0,y0,x1,y1=c['box'];m=Image.new('L',(w,h),0);mp=m.load()
        for j in c['pts']:
            y,x=divmod(j,w);mp[x,y]=255
        fig=Image.composite(o,Image.new('RGBA',(w,h),(0,0,0,0)),m).crop((x0,y0,x1+1,y1+1))
        fig=fig.resize((max(1,round(fig.width*f)),max(1,round(fig.height*f))),Image.LANCZOS);fig.save(f'{out}/{name}-{k}.webp',quality=88)
    print(name,len(top),len(bot),'alto',target)
for a in sys.argv[1:]:
    n,src,t=a.split(':');run(src,os.environ['OUT'],n,int(t))
