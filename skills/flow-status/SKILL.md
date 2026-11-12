---
name: flow-status
description: Read-only overview of the flow tasks in progress in this repo and its worktrees - which phase each one reached, what is waiting on the user, uncommitted changes, roles that did not finish - with the command to continue each one. Changes nothing. Use when the user runs /flow-status, or asks where they left off, which tasks are in progress or what is pending, for example after the session or the terminals were closed and no task is named.
---

# flow-status

Paths starting with `../` are relative to this skill's folder: they point at sibling skills in the same skills directory.

Show the user, in one message, every `flow-work` task that is still open here, and how to continue each one. This skill **only reads**. It never resumes a task itself: continuing is `flow-work`'s job.

## Hard rules

- **Change nothing.** No file writes, no note saves or updates (Engram or `.scratch/`), no tracker changes, and no git command that changes state: no `fetch`, `pull`, `checkout`, `stash` or `worktree` changes. Use what the local clone already knows, and say so when remote information matters (for example "the PR status comes from the tracker; branches are as of the last fetch").
- **Never fix a note.** If a state note contradicts its branch, report it; `flow-work` fixes it when the task is resumed.
- **Never touch a running worker.** If a role may still be running in another harness, report it and leave it alone.

## 1. Preflight

1. Read `docs/agents/workflow.md`. If it does not exist, tell the user that flow is not set up in this repo, suggest `/flow-setup`, and stop.
2. Read the tracker file (`docs/agents/tracker.md`, or the shared path in `workflow.md`), for `view-task` and `pr-status`.

## 2. Find the tasks

A task can live in any worktree of this repo, and its state note can be in either of two places. Look everywhere, always:

1. **Worktrees**: `git worktree list`. Each one is a place to look in the steps below, including the current one.
2. **State notes in Engram** (if the Engram MCP server is available): `mem_search` for `flow/<repo>/` keys ending in `/state`, then `mem_get_observation` on each.
3. **State notes as files**: `.scratch/flow/*/state.md` in every worktree. A note lands there when Engram is missing or a save to it failed, so check this even when Engram is available. If the same task has a note in both places, use the one updated last and say so.
4. **Task branches**: local branches that match the patterns in `workflow.md` (`git branch --list`), and which worktree has each one checked out.

Leave out:

- Closed state notes (the closed form starts with `<ref> <title> · closed`) whose PR is merged or closed. Keep a closed one whose PR is still open (`pr-status`): show it as "PR open" and mention changes requested, if any.
- Branches already merged into their base branch, unless a state note says the task is still open.

## 3. Check each task

For each task, without changing anything:

- **Where it stands**: `phase`, `next`, `waiting on` and `pending commits` from its state note. A branch with no state note: "no state note; `flow-work` will rebuild where it stands from the commits".
- **Its title**: `view-task`, one call per task. With more than ten tasks, show the ten most recently updated and say how many more there are.
- **Worktree**: match the note's `branch:` (or the task branch) to `git worktree list`. No match: "not checked out", or "worktree unknown" when the branch does not exist locally.
- **Uncommitted changes**: `git --no-optional-locks -C <worktree> status --porcelain`, as a count of files.
- **Commits not pushed**: `git -C <worktree> rev-list --count @{u}..HEAD`, when the branch has an upstream. It is as of the last fetch: say so.
- **A role that did not finish**: a `running:` line other than `none` means a role was started and its result never came back (the session or terminal closed under it). Say which role and where it ran. If it ran in another harness through an agent manager, say it may still be running there and that `flow-work` checks that first.
- **Contradictions**: a note whose `branch:` is not the branch it is on, or a `pending commits` command whose commit is already on the branch. Report them in one line each.

## 4. Report

One message, in the format of `../flow-work/references/phase-messages.md` (plain words, the action first). If the `i-have-adhd` skill is installed, apply its formatting rules too.

1. First line: how many tasks are in progress, and which one needs the user first (something waiting on them, a role that did not finish, or uncommitted changes).
2. A numbered table, the most recently updated task first: task (ref and title), where it stands, what it waits on, and warnings (uncommitted files, unpushed commits, unfinished role, contradiction).
3. For each task, the command to continue it: `/flow-work <ref>`, preceded by `cd <worktree>` when it is checked out in another worktree.
4. If there are no open tasks, say so in one line and suggest `/flow-backlog` to create tasks or `/flow-work <id>` to start one.

Then stop. Continuing is the user's call, through `/flow-work <ref>`: this skill never starts it. If they pick a task checked out in another worktree, remind them to open the agent there, since the task's files and notes live there.
