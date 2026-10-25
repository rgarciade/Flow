import html, sys
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + os.sep
INK="#2d3142";MUT="#4f5d75";ACC="#eb6c36";ACT="#fdeee6";LNK="#2e5aa8";BG="#f5f5f5"
SANS="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO="ui-monospace,'SF Mono',Menlo,Consolas,monospace"
e=html.escape
class D:
    def __init__(s,w,h,slug,title,desc):
        s.w,s.h,s.slug,s.title,s.desc=w,h,slug,title,desc;s.back=[];s.front=[]
    def path(s,pts,color=MUT,dash=False,mk="a",start=False,r=8):
        d=f"M{pts[0][0]},{pts[0][1]}"
        for i in range(1,len(pts)-1):
            (x0,y0),(x1,y1),(x2,y2)=pts[i-1],pts[i],pts[i+1]
            def unit(a,b):
                dx,dy=b[0]-a[0],b[1]-a[1];l=(dx*dx+dy*dy)**.5;return dx/l,dy/l
            u=unit((x0,y0),(x1,y1));v=unit((x1,y1),(x2,y2))
            rr=min(r,((x1-x0)**2+(y1-y0)**2)**.5/2,((x2-x1)**2+(y2-y1)**2)**.5/2)
            d+=f" L{x1-u[0]*rr},{y1-u[1]*rr} Q{x1},{y1} {x1+v[0]*rr},{y1+v[1]*rr}"
        d+=f" L{pts[-1][0]},{pts[-1][1]}"
        da=' stroke-dasharray="5,4"' if dash else ''
        ms=f' marker-start="url(#{s.slug}-{mk}s)"' if start else ''
        s.back.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.4"{da} marker-end="url(#{s.slug}-{mk})"{ms}/>')
    def line(s,pts,color=MUT,w=2):
        s.back.append('<polyline points="'+' '.join(f"{x},{y}" for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"/>')
    def label(s,x,y,t,anchor="middle",color=MUT):
        w=6.2*len(t)+8
        x0={"middle":x-w/2,"start":x-4,"end":x-w+4}[anchor]
        s.back.append(f'<rect x="{x0:.1f}" y="{y-9}" width="{w:.1f}" height="13" rx="2" fill="{BG}"/>')
        s.back.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="9" font-family="{MONO}" text-anchor="{anchor}" letter-spacing="0.05em">{e(t)}</text>')
    def text(s,x,y,t,size=12,w=400,color=INK,anchor="middle",mono=False,front=True,italic=False):
        st=' font-style="italic"' if italic else ''
        o=f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{w}" font-family="{MONO if mono else SANS}" text-anchor="{anchor}"{st}>{e(t)}</text>'
        (s.front if front else s.back).append(o)
    def box(s,x,y,w,h,title,sub=(),fill="#fff",stroke=INK,dash=False,sw=1.2,tsize=13):
        da=' stroke-dasharray="4,3"' if dash else ''
        s.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{BG}"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}/>')
        s.text(x+w/2,y+22,title,tsize,700)
        for i,t in enumerate(sub): s.text(x+w/2,y+40+i*15,t,10,400,MUT,mono=True)
    def chip(s,x,y,w,t,fill=ACC,color="#fff",h=15):
        s.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"/>')
        s.text(x+w/2,y+h-4.5,t,9,600,color,mono=True)
    def save(s):
        sl=s.slug
        mk=lambda i,c,st="":f'<marker id="{sl}-{i}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto{st}"><polygon points="0 0,8 3,0 6" fill="{c}"/></marker>'
        defs="<defs>"+mk("a",MUT)+mk("as",MUT,"-start-reverse")+mk("l",LNK)+mk("c",ACC)+"</defs>"
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}" role="img" aria-labelledby="{sl}-title {sl}-desc">'
         f'<title id="{sl}-title">{e(s.title)}</title><desc id="{sl}-desc">{e(s.desc)}</desc>{defs}'
         f'<rect width="100%" height="100%" fill="{BG}"/>'+"".join(s.back)+"".join(s.front)+"</svg>")
        open(OUT+sl+".svg","w").write(svg)
    def header(s,eyebrow,title):
        s.text(30,28,eyebrow,9,600,MUT,"start",mono=True)
        s.text(30,50,title,18,700,INK,"start")
    def legend(s,y,items):
        s.back.append(f'<line x1="30" y1="{y-14}" x2="{s.w-30}" y2="{y-14}" stroke="rgba(45,49,66,0.15)"/>')
        x=30
        for kind,t in items:
            if kind=="gate": s.chip(x,y-5,40,"GATE");x+=48
            elif kind=="commit": s.back.append(f'<rect x="{x}" y="{y-5}" width="40" height="15" rx="3" fill="{INK}"/>');s.text(x+20,y+6,"COMMIT",9,600,"#fff",mono=True);x+=48
            elif kind=="solid": s.back.append(f'<line x1="{x}" y1="{y+2}" x2="{x+28}" y2="{y+2}" stroke="{MUT}" stroke-width="1.4"/>');x+=36
            elif kind=="dash": s.back.append(f'<line x1="{x}" y1="{y+2}" x2="{x+28}" y2="{y+2}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="5,4"/>');x+=36
            elif kind=="blue": s.back.append(f'<line x1="{x}" y1="{y+2}" x2="{x+28}" y2="{y+2}" stroke="{LNK}" stroke-width="1.4"/>');x+=36
            s.text(x,y+6,t,10,400,MUT,"start");x+=len(t)*5.8+24

