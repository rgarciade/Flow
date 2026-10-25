from lib import *
d=D(900,540,"flow-work-phases","flow-work phases 0 to 8","Flow of flow-work phases 0 to 8 with user gates, commit points and the task-too-big branch after research.")
d.header("FLOW-WORK","Nine phases, you decide at every gate")
W,H=140,100
def ph(x,y,n,t,sub,gate=None,commit=None,model=None):
    g=gate is not None
    d.box(x,y,W,H,f"{n} {t}",sub,stroke=ACC if g else INK,fill=ACT if g else "#fff",sw=1.6 if g else 1.2,tsize=12)
    if gate: d.chip(x+8,y+54 if commit else y+68,W-16,gate,h=15)
    if commit:
        d.front.append(f'<rect x="{x+8}" y="{y+76}" width="{W-16}" height="15" rx="3" fill="{INK}"/>')
        d.text(x+W/2,y+87,commit,9,600,"#fff",mono=True)
A=60;B=190;C=330
ph(30,A,"0","Preflight",["read workflow.md","git status"])
ph(198,A,"1","Task",["task + blockers"],gate="confirm task")
ph(366,A,"2","Branch",["create-branch","linked to the task"])
ph(534,A,"3","Research",["fast, size verdict"],gate="read summary")
ph(366,B,"4","Plan",["strong, docs + ADRs"],gate="confirm plan")
ph(198,B,"5","Tests",["strong, tests only"],gate="approve tests",commit="test(<ref>)")
ph(30,B,"6","Implement",["fast, code + docs"],commit="feat(<ref>)")
ph(30,C,"7","Review",["checks docs + ADRs"],gate="choose findings",commit="fix|refactor(<ref>)")
ph(198,C,"8","Report + PR",["ADRs written"],gate="open PR?")
d.box(366,C,W,H,"You merge the PR",["on the code host,","never the agent"],stroke=ACC,fill=ACT,sw=1.6,tsize=12)
d.chip(374,C+72+4,W-16,"GATE",h=15)
d.box(534,C,W,H,"After merge",["next sibling, or","arch review + group PR"],dash=True,tsize=12)
# decision
cx,cy=604,B+50
d.front.append(f'<polygon points="{cx},{cy-46} {cx+70},{cy} {cx},{cy+46} {cx-70},{cy}" fill="{BG}"/><polygon points="{cx},{cy-46} {cx+70},{cy} {cx},{cy+46} {cx-70},{cy}" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
d.text(cx,cy-2,"Task too big?",12,700);d.text(cx,cy+13,"size verdict",9,400,MUT,mono=True)
d.box(710,B-14,170,152,"Too big: you choose",[],stroke=ACC,fill=ACT,sw=1.6,tsize=12)
d.chip(718,B+14,154,"GATE",h=15)
for i,t in enumerate(["(a) trim to first slice;","new tasks for the rest","(b) become parent;","slices = child tasks","then continue"]):
    d.text(718,B+46+i*15,t,10,400,MUT,"start",mono=True)
# arrows
y1=A+H/2
d.path([(170,y1),(198,y1)]);d.path([(338,y1),(366,y1)]);d.path([(506,y1),(534,y1)])
d.path([(604,A+H),(604,cy-46)])
d.path([(534,cy),(506,cy)]);d.label(520,cy-9,"NO")
d.path([(674,cy),(710,cy)],ACC,mk="c");d.label(692,cy-9,"YES")
d.path([(366,B+H/2),(338,B+H/2)]);d.path([(198,B+H/2),(170,B+H/2)])
d.path([(100,B+H),(100,C)])
d.path([(170,C+H/2),(198,C+H/2)]);d.path([(338,C+H/2),(366,C+H/2)]);d.path([(506,C+H/2),(534,C+H/2)],dash=True)
d.legend(480,[("gate","user decides"),("commit","user runs commit + push; agent never commits"),("dash","after merge")])
d.text(30,530,"Status moves (in progress, in review) and autonomous mode for simple tasks: always on your OK.",10,400,MUT,"start")
d.save()
