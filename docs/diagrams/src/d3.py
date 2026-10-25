from lib import *
d=D(900,560,"branching","flow branch model","Branch model: task branches merge by pull request into a group branch, the group branch merges into the base branch; standalone tasks go straight to the base branch.")
d.header("BRANCHING","Every PR targets one level up, every branch is linked to its issue")
by,sy,gy,ay,bY=100,190,290,380,470
def lane(y,x0,x1,col=INK,w=2.5): d.line([(x0,y),(x1,y)],col,w)
def dot(x,y,merge=False):
    d.front.append(f'<circle cx="{x}" cy="{y}" r="{6 if merge else 4}" fill="{ACC if merge else INK}" stroke="{BG}" stroke-width="1.5"/>')
lane(by,40,860);lane(sy,120,360);lane(gy,440,840);lane(ay,520,620);lane(bY,700,780)
# branch-off (solid) and PR (accent) connectors
d.path([(120,by),(120,sy),(136,sy)]) if False else None
d.path([(120,by),(120,sy-1)],MUT,mk="a");d.path([(440,by),(440,gy-1)],MUT,mk="a")
d.path([(520,gy),(520,ay-1)],MUT,mk="a");d.path([(700,gy),(700,bY-1)],MUT,mk="a")
d.path([(360,sy),(360,by)],ACC,mk="c");d.path([(840,gy),(840,by)],ACC,mk="c")
d.path([(620,ay),(620,gy)],ACC,mk="c");d.path([(780,bY),(780,gy)],ACC,mk="c")
for x in (160,240,320): dot(x,sy)
for x in (560,590): dot(x,ay)
for x in (730,755): dot(x,bY)
for x in (480,660,810): dot(x,gy)
dot(360,by,True);dot(840,by,True);dot(620,gy,True);dot(780,gy,True)
d.text(48,by-14,"dev  (base branch from workflow.md)",11,700,INK,"start",mono=True)
d.text(132,sy-14,"task/<n>-<slug>   standalone",11,700,INK,"start",mono=True)
d.text(452,gy-14,"feature/<parent>-<slug>   group branch",11,700,INK,"start",mono=True)
d.text(508,ay+4,"task/<n1>-<slug>",11,700,INK,"end",mono=True)
d.text(688,bY+4,"task/<n2>-<slug>",11,700,INK,"end",mono=True)
d.label(348,sy-30,"PR to base","end",ACC)
d.label(828,by+60,"GROUP PR to base","end",ACC)
d.label(608,ay-18,"PR to group","end",ACC)
d.label(792,bY-30,"PR to group","start",ACC)
# note
d.box(40,330,330,120,"Blocked children wait",["task n2 is blocked by n1:","it branches only after n1's PR","is merged into the group branch"],stroke=ACC,fill=ACT,sw=1.6,tsize=12)
d.box(40,468,330,48,"You review and merge every PR",[],tsize=12)
d.legend(540,[("solid","branch from"),("blue","PR (you merge)")])
d.text(330,545,"gh issue develop links each branch to its issue · pull --ff-only first · push every commit",10,400,MUT,"start")
d.save()
