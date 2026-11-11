from lib import *
d=D(900,560,"orchestrator","flow-work orchestrator and subagents","The orchestrator talks to the user and briefs the roles with note keys; each role runs as a subagent or in another harness, as set in the Harnesses table, and saves its full result to notes and returns at most 15 lines.")
d.header("ORCHESTRATION","One thin thread, the bulk work goes to the roles")
d.box(40,76,170,64,"You",["decide, commit, merge"],tsize=13)
d.box(330,76,240,64,"Orchestrator",["the session you open"],stroke=ACC,fill=ACT,sw=1.6)
d.box(680,76,190,64,"Hard rules",["one writer at a time","never commits or merges"],dash=True,tsize=12)
d.path([(210,108),(330,108)],start=True);d.label(270,99,"GATES")
# container
d.front.append(f'<rect x="28" y="210" width="844" height="150" rx="8" fill="{BG}"/><rect x="28" y="210" width="844" height="150" rx="8" fill="none" stroke="{MUT}" stroke-width="1" stroke-dasharray="4,3"/>')
d.text(40,228,"ROLES  (subagent or another harness, with its model, per the Harnesses table in workflow.md)",9,600,MUT,"start",mono=True)
roles=[("research","fast","reads code + task",0),("plan","strong","seams + scenarios",0),("tests","strong","test files only",1),("implement","fast","never tests",1),("reviews","fast","standards + spec",0),("fix","fast","never tests",1),("arch review","strong","group, before PR",0)]
cw,gap,x=108,8,40
for i,(n,m,w,wr) in enumerate(roles):
    xx=x+i*(cw+gap)
    d.box(xx,240,cw,108,n,[],stroke=ACC if wr else INK,sw=1.6 if wr else 1.2,tsize=12 if len(n)<14 else 11)
    d.chip(xx+8,254+12,cw-16,m.upper(),fill=INK,h=15)
    d.text(xx+cw/2,308,w,9.5,400,MUT,mono=True)
    d.text(xx+cw/2,326,"WRITES" if wr else "READ-ONLY",9,700,ACC if wr else MUT,mono=True)
# arrows orchestrator<->container
d.path([(430,140),(430,210)]);d.label(420,180,"BRIEF + NOTE KEYS","end")
d.path([(500,210),(500,140)],LNK,mk="l");d.label(510,180,"<=15 LINES + QUESTIONS","start",LNK)
# engram
d.box(28,430,844,70,"Notes: Engram, or .scratch/flow/ files",["flow/<repo>/<id>/<phase>   e.g. flow/my-app/42/research","phases: research, plan, tests, implement, review-standards, review-spec; state"],tsize=13)
d.path([(250,360),(250,430)]);d.label(260,400,"SAVE: FULL RESULT","start")
d.path([(650,430),(650,360)],LNK,mk="l");d.label(640,400,"READ: PRIOR PHASES","end",LNK)
d.save()
