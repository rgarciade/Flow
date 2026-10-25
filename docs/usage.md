# Usage guide

Recipes for day-to-day work. For what happens inside each phase, see [flows.md](flows.md).

## Plan tasks for later

```
/flow-plan
```

Describe what you want. The skill asks one question at a time, always proposing an answer you can accept in one word, and pushes towards the minimum.

- **Separate tasks**: you get a numbered list of drafts (title and one line each). Ask to see any full body, ask for changes, then approve. The issues are created on GitHub.
- **A bigger piece of work**: it proposes a parent issue and child sub-issues, each one a vertical slice, with the blocking links between them. Adjust granularity and dependencies, then approve.

Every issue has: what to build (end to end, from the user's point of view), acceptance criteria, out of scope, and its blockers. No file paths or code: technical detail is decided when the task is picked up.

It ends by telling you which issues can start now, for example `/flow-work #42`.

## Develop an existing task

```
/flow-work #42
```

What you will be asked to do, in order:

1. **Answer a few questions** that remove ambiguity. Each comes with an assumed answer.
2. **Confirm the seams**: the public interfaces that will be tested, each with what it catches and what it misses.
   If the requirements changed, approve the update to the issue description. The plan is then posted as a comment on the issue.
3. **Approve the tests.** You get one line per scenario with a link to the test, and the command to run them. Reply `OK`, or ask for changes.
4. **Run, or authorise, the `test(#42)` commit.** That commit is the record of the approved tests.
5. **Run, or authorise, the `feat(#42)` commit** once the implementation passes.
6. **Choose which review findings to fix**, then the `fix(#42)` or `refactor(#42)` commit.
7. **Read the final report** and review the code in the order it gives you (tests → entry point → logic → data).
8. **Say yes to the PR**, then review and merge it on GitHub.

## Talk about a task and start right away

Discuss the task in the conversation, then:

```
/flow-work
```

Without an issue number, it drafts the issue from the conversation, creates it once you approve, and continues as above.

## When a task turns out to be too big

After research, `flow-work` may report that the task does not fit one session as one vertical slice. It stops and offers:

- **(a) Keep this task small**: trim it to the first slice and create the rest as new issues for later.
- **(b) Turn it into a parent**: the issue becomes the parent, the slices become its sub-issues, and work continues on a group branch with the first child.

## After you merge a PR

Tell `flow-work` it is merged.

- **A child task**: it lists the siblings that are now unblocked and suggests the next one.
- **The last child**: it offers to open the group PR, from `feature/<parent>-<slug>` to the base branch.

## Resume a task

Run `/flow-work #42` again. If the task branch exists, it checks it out and works out where it stopped from its notes (`flow/<repo>/42/*`, in Engram or `.scratch/flow/42/`) and the commits on the branch.

## Commits

`flow-work` never commits or merges on its own. At each commit point it prints the exact command, for example:

```sh
git add tests/profile.test.ts && git commit -m "test(#42): profile endpoint returns the current user"
```

Run it yourself, or tell it to run it. If you would rather not commit the tests, it keeps a copy under `.scratch/flow/<issue>/approved-tests/` with a checksum manifest instead.
