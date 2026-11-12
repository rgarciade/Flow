# Usage guide

`flow` is issue-driven: every recipe below starts from a task in your tracker, or creates one first. Examples use GitHub-style references (`#42`); in your tracker they may look like `PROJ-123`. Recipes for day-to-day work. For what happens inside each phase, see [flows.md](flows.md).

## Plan tasks for later

```
/flow-backlog
```

Describe what you want. The skill asks independent questions together, always proposing an answer: as selectors with a free-text option when your agent supports them, otherwise as a numbered list you can answer with "OK" or corrections by number. It asks one alone when its answer changes the rest, and pushes towards the minimum.

- **Separate tasks**: you get a numbered list of drafts (title and one line each). Ask to see any full body, ask for changes, then approve. The tasks are created in your tracker.
- **A bigger piece of work**: it proposes a parent task and child tasks, each one a vertical slice, with the blocking links between them. Adjust granularity and dependencies, then approve.

Every issue has: the big picture (what to build and why), the two to four outcomes that define "done", preliminary notes (candidate libraries, connectors, risks), out of scope, and its blockers. It is deliberately not a full specification: the detail is worked out in `flow-work`'s plan phase, when the task is picked up.

If the work touches something unknown, `flow-backlog` offers a short **preliminary research** pass first: a read-only look at libraries, connectors, existing code and risks, whose findings go into the issues' preliminary notes.

It ends by telling you which issues can start now, for example `/flow-work #42`.

## Develop an existing task

```
/flow-work #42
```

It starts by updating the base or group branch (`git pull --ff-only`), creating the task branch from it and importing any new Engram memory from `.engram/`, so you always start from the latest state.

What you will be asked to do, in order:

1. **Confirm the task** as the agent understood it, and the branch it will create. If the task is already assigned to someone else or in progress, it warns you first.
2. **Read the research summary** (what exists, the places in the code the change must reach that the issue did not mention, open questions, size) and add anything it missed.
3. **Answer the plan's questions and confirm the plan, in one round.** The plan arrives already drafted with an assumed answer for each question, so you see everything together: the refined acceptance criteria, the docs it will touch, any **manual verification** steps for parts that can't reasonably be tested (configuration, styling, infrastructure…), and the **seams**: the public interfaces that will be tested, each with what it catches and what it misses. If an answer of yours changes the plan, you get only what changed.
4. **Nothing else for the plan.** Your OK also records the plan on the task and, when the criteria changed, updates the task description with the ones you just saw.
5. **Check the test edge cases**, if any (see [Working modes](#working-modes)): one line each, with a link to the test. Reply `OK`, or ask for changes. Without edge cases it just tells you how many tests it wrote and goes on. In pair mode you approve every test here, then run the `test(#42)` commit.
6. **Run, or authorise, the `test(#42)` and `feat(#42)` commits**, in that order, once the implementation passes and the docs it listed are updated. The `test` commit is the record of the approved tests.
7. **Choose which review findings to fix**, by number. They come as one short table per axis, must-fix first, and include stale or redundant docs and code that contradicts an ADR. Then the `fix(#42)` or `refactor(#42)` commit.
8. **Read the final report** and review the code in the order it gives you (tests → entry point → logic → data).
9. **Answer the closing questions, asked together** right after the report: ticking the met criteria, the ADRs (if the plan flagged architectural decisions), exporting Engram memory (if the repo uses Engram sync) and opening the PR.
10. **Run, or authorise, the commits that follow from your answers**: `docs(#42)` for the ADRs and `chore(#42)` for the Engram export.
11. **Review and merge the PR** on your code host. The agent then saves the task's memory for later tasks (what was built, where, decisions and gotchas); it needs nothing from you.

Every message between phases follows the same shape: where the task is, what is needed from you, what the task is about, what the phase found, the questions, and what happens once you answer. It is written in plain words, without the skill's internal vocabulary.

## Talk about a task and start right away

Discuss the task in the conversation, then:

```
/flow-work
```

Without an issue number, it drafts the issue from the conversation, creates it once you approve, and continues as above.

## Working modes

| Mode | When | Where it stops | Tests | Commit commands |
|---|---|---|---|---|
| **Semi-autonomous** | The default | At every phase | Only the edge cases come to you | `test` and `feat` together, after implementing |
| **Pair** | Proposed after research when the task has loose ends or is very complex; switched on only with your yes | At every phase | You approve every test | One per phase |
| **Autonomous** | Small, simple tasks, only with your yes (see below) | Only for what really needs you | No test gate | All together with the final report |

**Edge cases** are the tests the plan did not settle, since you already approved the seams and scenarios there:

- a test that departs from its scenario, or a scenario left without a test;
- a scenario tested at a different seam than the one agreed, or a test that mocks the code it checks;
- an expected value or behaviour the plan didn't settle, which the agent had to choose;
- a test that fails for a reason other than the expected one.

The tests are frozen in every mode: at the test gate they are recorded in `.scratch/flow/<id>/approved-tests/` (in semi-autonomous mode, also after you approve edge cases), and that copy is the reference until the `test` commit exists. Once you confirm that commit, its hash becomes the reference.

Ask for a mode when you start (`/flow-work #42, pair mode`) or at any time ("show me every test", "back to semi-autonomous").

A repo can start its tasks in another mode: set **Default working mode** in the Harnesses section of `docs/agents/workflow.md`. With `autonomous` as the default, only tasks that research finds small and simple run that way; the rest start in semi-autonomous and you are told why.

## Choose the harnesses and models

By default every role is done by subagents of the harness you are using (Claude Code, OpenCode, Codex…). The **Harnesses** section of `docs/agents/workflow.md` lets you pick which harnesses work on the repo and which models each one uses, for example Claude Code for the plan and the tests, and OpenCode for the rest:

```markdown
| Harness | Runs in | Strong model | Fast model | Deep model | Effort |
|---|---|---|---|---|---|
| claude | `subagent` | `sonnet` | `sonnet` | `opus` | |
| opencode | `orca:opencode` | `<model id>` | `<model id>` | | |

| Role | Harnesses, in order | Uses |
|---|---|---|
| plan, tests | claude | strong |
| research, implement, fix | opencode, claude | fast |
| review | opencode, claude | fast |
```

You don't write it by hand: run `/flow-setup` the first time, or run it again and say you want to change the harnesses or models. It asks which harnesses you have, their models and which one takes each role, writes the section and shows it before and after, with no extra approval stop (nothing is committed, so the diff is the review), and touches nothing else except the short `## Agent skills` block in `AGENTS.md` or `CLAUDE.md`, which it brings up to date if its text is out of date.

- **Fallbacks.** Several harnesses on a role are alternatives, in order. If the first has no quota left or is not installed, the next one takes over and you are told in one line.
- **Managers.** `orca:<harness>` uses Orca and `herdr:<harness>` uses Herdr to launch it. On a machine without the manager, the role runs as a subagent and you are told, so teammates don't need it.
- **Models.** Each harness has its own: strong for the plan and the tests, fast for the rest, and an optional deep one used only when `flow-work` proposes the deep profile for a very complex task and you agree.
- The orchestrator is the session you open, so its harness and model are your choice. The split is fixed by role: nothing balances usage across your subscriptions.
- The other harness works in the same checkout, gets the same instructions as a subagent and never commits.

## Let it work on its own (simple tasks)

For a small task, say so when you start (`/flow-work #42, work autonomously`), or accept when `flow-work` suggests it after research. It then chains the phases without the routine confirmations and stops only for:

- a decision the issue and the plan don't settle, where a wrong guess would cost rework;
- a test that looks wrong, or a check it cannot make pass;
- a task bigger than it looked;
- anything that leaves your machine or changes shared state (commits, pushes, status moves, issue edits, the PR, merging the target branch, replies on a PR review);
- parking or abandoning a task.

Tests are still frozen (recorded in `.scratch/flow/42/approved-tests/`), commit commands (each ending with `&& git push`) come together with the final report, and the report lists every assumption it made for you. Say "back to pair mode" at any time.

## When a test turns out to be wrong

Implementation sometimes shows that an approved test was wrong: a misread requirement, a library that behaves differently, a badly chosen seam. `flow-work` stops (also in autonomous mode) and shows you which test, why, the evidence and the change it proposes. It tells you if it thinks the test is actually right and the code is just hard.

If you agree:

1. The tests subagent changes only those tests.
2. You run, or authorise, `test(#42): adjust <what> (<why>) && git push`. That commit becomes the new reference for "tests unchanged".
3. You approve a line in the plan record's "Changes to the plan", and in the description's `## Changes` if a requirement changed.

The PR history then shows what was approved, what changed, when and why.

## When a task turns out to be too big

After research, `flow-work` may report that the task does not fit one session as one vertical slice. It stops and offers:

- **(a) Keep this task small**: trim it to the first slice and create the rest as new issues for later.
- **(b) Turn it into a parent**: the task becomes the parent, the slices become its children, and work continues on a group branch with the first child.

## After you merge a PR

Tell `flow-work` it is merged.

- **A child task**: it lists the siblings that are now unblocked and suggests the next one.
- **The last child**: it runs a group architecture review of the whole feature (coherence, duplication between children, missing ADRs) and shows it to you. Findings become new child issues or follow-ups. Then it offers to open the group PR, from `feature/<parent>-<slug>` to the base branch.

## The PR got review comments

Tell `flow-work` (or run `/flow-work #42` again while the PR is open with changes requested). It reads the comments from the code host and shows them as a numbered table: what each one asks and what it proposes (fix, discuss or decline, with the reason). You choose which to address. Then it fixes them, runs the checks, re-reviews the fix and gives you the `fix` commit command. Replies on the PR are drafted for you and posted only with your OK. A comment that changes a requirement or an approved test goes through the same steps as in the plan phase.

## Park or abandon a task

Say "park", "pause", "drop" or "abandon". To park, it shows `git status` and proposes a WIP commit or a stash, sets the state note to `phase: parked` and proposes moving the status back. Resume with `/flow-work #42`. To abandon, it asks why and proposes, each with your OK, a comment on the task, moving or closing it, unassigning, and deleting the branch with the exact commands. The reason is saved in the task's memory. It always stops for you, also in autonomous mode.

## Tests that already fail, and a moved base branch

After creating the branch, `flow-work` runs the full suite once and tells you if tests already fail; from then on only new failures count, and the final report lists the old ones. Before opening the PR (and before pushing review fixes) it checks whether the target branch has new commits. If so it proposes `git merge origin/<target>`, never a rebase, stops on conflicts, and re-runs the checks after the merge.

## Resume a task

Run `/flow-work #42` again. If the task branch exists, it checks it out (a parked task says why it was parked) and reads the task's **state note** (`flow/<repo>/42/state`, in Engram or `.scratch/flow/42/state.md`): the phase it reached, a short line for each phase finished and what it settled, the working mode and model profile you chose, the questions that were waiting on you and the commits still pending. It checks that against the branch and the task, tells you where things stand and continues once you confirm. The same note keeps a long session on track when the agent's context is summarised.

It looks for the note in both places, Engram and `.scratch/`, since a note goes to `.scratch/` when saving it to Engram fails. The note also records which role is running. If the session or a terminal closed while a role was working, it finds that role unfinished. When the role ran in another harness, it first checks whether that agent is still working. Otherwise it shows you what the role left uncommitted and asks whether to relaunch the role on top of those changes or set them aside in a stash (you run the stash command).

Don't remember which task, or which worktree it was in? Run `/flow-status`. It changes nothing, and lists every task in progress in the repo and its worktrees: the phase each one reached, what it waits on, uncommitted changes, unpushed commits, a role that did not finish, and the command to continue it. `/flow-work` with no task and nothing in the conversation to make one from shows the same list and asks which one to resume, or whether to start a new task.

## Commits

`flow-work` never commits or merges on its own. At each commit point it prints the exact command, for example:

```sh
git add tests/profile.test.ts && git commit -m "test(#42): profile endpoint returns the current user" && git push
```

Run it yourself, or tell it to run it. If you would rather not commit the tests, it keeps a copy under `.scratch/flow/<issue>/approved-tests/` with a checksum manifest instead.
