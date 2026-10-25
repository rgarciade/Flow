from lib import *
d=D(900,520,"knowledge","Where knowledge lives and when flow-work writes it","Matrix of the task description, plan record, summary record, ADRs and project docs against the flow-work phases that create, update or check them.")
d.header("KNOWLEDGE","Where each record lives, and when it is written")
X0,LW=30,170
CW,GAP=130,6
cols=["4 Plan","6 Implement","7 Review","8 Report + PR","Group PR"]
cx=[X0+LW+10+i*(CW+GAP) for i in range(len(cols))]
for x,t in zip(cx,cols):
    d.text(x+CW/2,86,t,11,700,INK)
rows=[
 ("Task description",["what was asked"],[
   ["refined criteria,","## Changes (asks)"],["## Changes if a","req. moves (asks)"],None,None,None]),
 ("Plan record",["how it is built"],[
   ["created: seams,","steps, docs, ADRs"],["edited if the","plan changes (asks)"],["edited if a fix","changes it (asks)"],None,None]),
 ("Summary record",["what was built"],[
   None,None,None,["created: works now,","criteria, ADRs, docs"],None]),
 ("ADRs (docs/adr)",["why it was decided"],[
   ["candidates","flagged"],None,["code checked","against ADRs"],["written","(asks)"],["missing ADRs","found"]]),
 ("Project docs",["how it works now"],[
   ["docs to touch","listed"],["updated or created","+ docs README"],["stale or redundant","= finding"],["listed in","the report"],["feature overview","if missing"]]),
]
RH,RG,Y0=64,8,100
for i,(title,sub,cells) in enumerate(rows):
    y=Y0+i*(RH+RG)
    d.box(X0,y,LW,RH,title,sub,tsize=12)
    for x,c in zip(cx,cells):
        if c is None:
            d.text(x+CW/2,y+RH/2+4,"·",14,700,"#c3c7d0")
            continue
        asks=any("(asks)" in l for l in c)
        d.box(x,y,CW,RH,"",[],fill=ACT if asks else "#fff",stroke=ACC if asks else MUT,sw=1.4 if asks else 1)
        for k,l in enumerate(c):
            d.text(x+CW/2,y+RH/2-4+k*15,l,10,400,INK,mono=True)
d.legend(470,[("gate","orange cell: shown to you, done only after your OK")])
d.text(420,481,"·   nothing written in this phase",10,400,MUT,"start")
d.text(30,505,"The issue keeps what and its history, ADRs keep why, docs keep how things work now: just enough, never what the code already says.",10,400,MUT,"start")
d.save()
