# Usage guide

`flow` is issue-driven: every recipe below starts from a GitHub issue, or creates one first. Recipes for day-to-day work. For what happens inside each phase, see [flows.md](flows.md).

## Plan tasks for later

```
/flow-plan
```

Describe what you want. The skill asks one question at a time, always proposing an answer you can accept in one word, and pushes towards the minimum.

- **Separate tasks**: you get a numbered list of drafts (title and one line each). Ask to see any full body, ask for changes, then approve. The issues are created on GitHub.
- **A bigger piece of work**: it proposes a parent issue and child sub-issues, each one a vertical slice, with the blocking links between them. Adjust granularity and dependencies, then approve.

Every issue has: the big picture (what to build and why), the two to four outcomes that define "done", preliminary notes (candidate libraries, connectors, risks), out of scope, and its blockers. It is deliberately not a full specification: the detail is worked out in `flow-work`'s plan phase, when the task is picked up.

If the work touches something unknown, `flow-plan` offers a short **preliminary research** pass first: a read-only look at libraries, connectors, existing code and risks, whose findings go into the issues' preliminary notes.

It ends by telling you which issues can start now, for example `/flow-work #42`.

## Develop an existing task

```
/flow-work #42
```

It starts by updating the base or group branch (`git pull --ff-only`), creating the task branch from it and importing any new Engram memory from `.engram/`, so you always start from the latest state.

What you will be asked to do, in order:

1. **Confirm the task** as the agent understood it, and the branch it will create.
2. **Read the research summary** (what exists, open questions, size) and add anything it missed.
3. **Answer a few questions** that remove ambiguity. Each comes with an assumed answer.
4. **Confirm the plan**, including the docs it will touch, and the **seams**: the public interfaces that will be tested, each with what it catches and what it misses.
   The plan is then posted as a comment on the issue and, if the requirements changed, you approve the update to the issue description.
5. **Approve the tests.** You get one line per scenario with a link to the test, and the command to run them. Reply `OK`, or ask for changes.
6. **Run, or authorise, the `test(#42)` commit.** That commit is the record of the approved tests.
7. **Run, or authorise, the `feat(#42)` commit** once the implementation passes.
8. **Choose which review findings to fix**, then the `fix(#42)` or `refactor(#42)` commit.
9. **Read the final report** and review the code in the order it gives you (tests → entry point → logic → data).
10. **Approve the ADRs**, if the plan flagged architectural decisions, then the `docs(#42)` commit.
11. **Export Engram memory or not** (if the repo uses Engram sync), then the `chore(#42)` commit.
12. **Say yes to the PR**, then review and merge it on GitHub.

## Talk about a task and start right away

Discuss the task in the conversation, then:

```
/flow-work
```

Without an issue number, it drafts the issue from the conversation, creates it once you approve, and continues as above.

## Let it work on its own (simple tasks)

For a small task, say so when you start (`/flow-work #42, work autonomously`), or accept when `flow-work` suggests it after research. It then chains the phases without the routine confirmations and stops only for:

- a decision the issue and the plan don't settle, where a wrong guess would cost rework;
- a test that looks wrong, or a check it cannot make pass;
- a task bigger than it looked;
- anything that leaves your machine or changes shared state (commits, pushes, status moves, issue edits, the PR).

Tests are still frozen (recorded in `.scratch/flow/42/approved-tests/`), commit commands (each ending with `&& git push`) come together with the final report, and the report lists every assumption it made for you. Say "back to pair mode" at any time.

## When a test turns out to be wrong

Implementation sometimes shows that an approved test was wrong: a misread requirement, a library that behaves differently, a badly chosen seam. `flow-work` stops (also in autonomous mode) and shows you which test, why, the evidence and the change it proposes. It tells you if it thinks the test is actually right and the code is just hard.

If you agree:

1. The tests subagent changes only those tests.
2. You run, or authorise, `test(#42): adjust <what> (<why>) && git push`. That commit becomes the new reference for "tests unchanged".
3. You approve a line in the plan comment's "Changes to the plan", and in the description's `## Changes` if a requirement changed.

The PR history then shows what was approved, what changed, when and why.

## When a task turns out to be too big

After research, `flow-work` may report that the task does not fit one session as one vertical slice. It stops and offers:

- **(a) Keep this task small**: trim it to the first slice and create the rest as new issues for later.
- **(b) Turn it into a parent**: the issue becomes the parent, the slices become its sub-issues, and work continues on a group branch with the first child.

## After you merge a PR

Tell `flow-work` it is merged.

- **A child task**: it lists the siblings that are now unblocked and suggests the next one.
- **The last child**: it runs a group architecture review of the whole feature (coherence, duplication between children, missing ADRs) and shows it to you. Findings become new child issues or follow-ups. Then it offers to open the group PR, from `feature/<parent>-<slug>` to the base branch.

## Resume a task

Run `/flow-work #42` again. If the task branch exists, it checks it out and works out where it stopped from its notes (`flow/<repo>/42/*`, in Engram or `.scratch/flow/42/`) and the commits on the branch.

## Commits

`flow-work` never commits or merges on its own. At each commit point it prints the exact command, for example:

```sh
git add tests/profile.test.ts && git commit -m "test(#42): profile endpoint returns the current user" && git push
```

Run it yourself, or tell it to run it. If you would rather not commit the tests, it keeps a copy under `.scratch/flow/<issue>/approved-tests/` with a checksum manifest instead.
