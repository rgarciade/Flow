# Flows

`flow` is **Issue-Driven Development**: every piece of work starts from a GitHub issue and stays tied to it, from the branch name to the pull request. This page shows how the pieces fit together. The skills themselves are the source of truth: [flow-setup](../skills/flow-setup/SKILL.md), [flow-plan](../skills/flow-plan/SKILL.md), [flow-work](../skills/flow-work/SKILL.md).

## Overview

<p align="center"><img src="diagrams/overview.svg" alt="The three skills and the files they read and write" width="900"></p>

- `flow-setup` runs once per repo and writes `docs/agents/*.md`.
- `flow-plan` turns ideas into GitHub issues and never writes code.
- `flow-work` takes one issue to a pull request.
- Both `flow-plan` and `flow-work` read `docs/agents/*.md`, and offer to run `flow-setup` when `workflow.md` is missing.

## flow-work phases

<p align="center"><img src="diagrams/flow-work-phases.svg" alt="flow-work phases with user gates and commit points" width="900"></p>

| Phase | Who | Output | Your part |
|---|---|---|---|
| 0. Preflight | orchestrator | Settings loaded, clean tree | Run `flow-setup` if asked |
| 1. Task | orchestrator | The issue (read or created) and its position: parent, blockers, children | Approve the draft if it was created; confirm the task and branch; OK the move to in progress |
| 2. Branch | orchestrator | `task/<n>-<slug>` linked to the issue with `gh issue develop` (and the group branch if needed) | |
| 3. Research | research subagent | What exists, whether the issue's preliminary notes still hold, open questions, size verdict | Read the summary and comment; choose (a) or (b) if it is too big |
| 4. Plan | plan subagent | **The task's detail**: refined criteria, seams, scenarios, outline | Answer questions, confirm seams |
| 5. Tests | tests subagent | Failing tests, each for the expected reason | **Approve the tests**, `test(#n)` commit |
| 6. Implement | implement subagent(s) | Code that passes the frozen tests | Answer any question not settled by the plan; `feat(#n)` commit |
| 7. Review | 2 review subagents, then fix | Standards and spec reports | Choose findings, `fix`/`refactor` commit |
| 8. Report and PR | orchestrator | Report, PR and closing comment | Review the code, OK the move to in review, merge the PR |

**You are in the loop.** Every phase ends by showing you its result and waiting for you before the next one. Anything the issue and the plan don't settle comes to you as a question with a recommendation; subagents return such questions instead of guessing.

**Frozen tests.** After the approval, `git diff <test commit> -- <test globs>` must stay empty. If implementation shows that a test was wrong, the work stops and you decide. When you agree, only the tests subagent changes it, in its own `test(#n): adjust …` commit that becomes the new reference, and the change is logged in the plan comment (and in the description if a requirement changed). Loosening a test only to make the code pass is never accepted.

## Branches

<p align="center"><img src="diagrams/branching.svg" alt="Base branch, group branches and task branches" width="900"></p>

- **Standalone task**: `task/<n>-<slug>` from the base branch, PR to the base branch.
- **Group of tasks** (a parent issue with sub-issues): `feature/<parent>-<slug>` from the base branch. Each child gets `task/<n>-<slug>` from the group branch, with its PR to the group branch. When every child is merged, one PR takes the group branch to the base branch.
- A child starts only after the PRs of its blockers are merged into the group branch, so each child PR shows only its own diff.
- You review and merge every PR.

The base branch and the name patterns live in each repo's `docs/agents/workflow.md`.

## Orchestrator and subagents

<p align="center"><img src="diagrams/orchestrator.svg" alt="Orchestrator, role subagents, models and Engram" width="900"></p>

| Role | Tier | Writes |
|---|---|---|
| Orchestrator | session model | Nothing bulky: talks to you, decides, runs checks |
| research | fast | No |
| plan | strong | No |
| tests | strong | Test files only |
| implement | fast | Code, never tests |
| review-standards, review-spec | fast (in parallel) | No |
| fix | fast | Code, never tests |

- **Model tiers.** Each repo maps `strong` and `fast` to real models in `docs/agents/workflow.md` (in Claude Code, by default `opus` and `sonnet`). Where the harness cannot pick a model per subagent, subagents inherit the session model.
- **Notes as the shared memory.** Each subagent saves its full result under `flow/<repo>/<issue>/<phase>` and returns at most 15 lines. The orchestrator passes note keys between phases, not content, so its context stays small. Notes go to Engram when its MCP server is available, or to `.scratch/flow/<issue>/<phase>.md` otherwise.
- **Harness-neutral subagents.** The orchestrator uses whatever subagent mechanism the harness offers (`Agent` in Claude Code, `Task` in OpenCode and Cursor…). Without one, it runs each phase itself with the same discipline.
- **One writer at a time.** Subagents that edit files run one after another; read-only ones may run in parallel.
- **Visible models.** Every subagent's task name starts with its model, for example `opus: tests #42`.

## Review

Phase 7 follows Matt Pocock's two-axis review ([reference](../skills/flow-work/references/code-review.md)):

- **Standards**: does the diff follow the repo's documented rules (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/*`, `CONTRIBUTING.md`…), plus a baseline of code smells that the repo's own rules can override?
- **Spec**: does it do what the issue and the plan asked for, without missing parts or scope creep?

The two reports are shown side by side and never merged, so one axis cannot hide the other.

## The issue as the source of truth

Anyone can understand a task from its GitHub issue alone, without the agent's notes:

| Where | What | When it changes |
|---|---|---|
| Issue description | The _what_: what to build, acceptance criteria, out of scope, a link to the plan comment, and a `## Changes` log at the bottom (what changed and why) | Edited whenever the agreed requirements change, after you approve the edit |
| Plan comment (`<!-- flow:plan -->`) | The _how_, in 10 to 15 lines: seams under test, scenarios, steps, and a "Changes to the plan" log | Created after planning; **edited in place**, after you approve, if implementation or review changes the plan |
| Closing comment (`<!-- flow:summary -->`) | What was built, criteria met, deviations, open findings, link to the PR | Posted when the PR is opened |

- **At most two comments per task** from `flow-work`. Changes edit what exists instead of adding more.
- **Creating** these comments needs no confirmation; **editing** the description or a comment, and **deleting** anything, always asks you first.
- Both comments start with a GitHub `[!NOTE]` box saying they are implementation notes, not requirements. A hidden marker lets `flow-work` find the same comment every time.

## Engram sync

When the Engram CLI is installed, a project's memory can travel with the repo in `.engram/`, so another machine or teammate gets the same context. The **Engram sync** setting in `docs/agents/workflow.md` controls it (`ask`, `always` or `never`).

- **In, when a branch is created.** After pulling the base or group branch, `flow-work` runs `engram sync --status` and, if there are new chunks, `engram sync --import`.
- **Out, before the PR.** After the final report, `flow-work` offers to run `engram sync`, which exports the project's memory to `.engram/` (prompts excluded), and gives you the commit command.

The export holds every memory of the project, not only the current task's notes. Check what you share before pushing a public repo.

## Team visibility

Spec-driven teams only see a piece of work when its pull request arrives. Issue-driven work is visible while it happens:

| What the team sees | Where | How |
|---|---|---|
| Who is on it | Issue assignee | Assigned to you when you confirm the task |
| Which branch | Issue → Development panel | Branches are created with `gh issue develop`, linked to the issue |
| Every approved step | Commits on the linked branch | Each commit command ends with `git push` |
| How it is being built | The plan comment on the issue | Posted after planning, edited when the plan changes |
| Which stage | Issue status (labels or a GitHub Project field) | Moved to in progress, in review and done, always after your OK |

Status tracking is configured per repo in `docs/agents/workflow.md` (`none`, `labels` or `project`).

## Autonomous mode

For simple tasks you can let `flow-work` chain the phases on its own. It is never the default and never switched on without your yes. It still stops for decisions the plan doesn't settle, suspicious tests, failing checks, tasks that grow, and anything that leaves your machine. See the [usage guide](usage.md#let-it-work-on-its-own-simple-tasks).

## Architecture and coherence

Small vertical slices are easy to review but can lose the big picture. `flow` keeps it explicit at four points, without specifying everything up front:

| When | What | Where it lands |
|---|---|---|
| Planning a feature (`flow-plan`) | **Architecture notes** on the parent issue: main pieces, data flow, boundaries, decisions taken and open | Parent issue description |
| Phase 4, Plan | **ADR candidates**: decisions that are hard to reverse, span modules, or were chosen between alternatives. Conflicts with existing ADRs go to you as questions | Plan note and the plan comment's "Architecture decisions" |
| Phase 7, Review | The standards reviewer checks the code against the **ADRs, the glossary and the architecture notes**; a contradiction is a finding that cites the ADR | Review report |
| Phase 8, before the PR | Each candidate that held becomes an **ADR** in `docs/adr/`, after your OK, in a `docs(#n)` commit | The repo, with the PR |
| Group PR | A **group architecture review** of the whole feature: coherence, duplication between children, missing ADRs, glossary drift. Findings become new child issues or follow-ups | Report to you before the group PR |

Most tasks produce no ADR at all: only decisions that would be expensive to undo get one. The template is in [`skills/flow-work/references/adr-template.md`](../skills/flow-work/references/adr-template.md).

## Documentation

The project's own documentation (module guides, user guides, the README) is kept current task by task, not in a final catch-up phase:

| When | What |
|---|---|
| Phase 4, Plan | The plan lists the **docs to touch** (or "none"), and they appear in the plan comment. Rules in the project's `AGENTS.md` or `CLAUDE.md` take precedence |
| Phase 6, Implement | With the tests green, those documents are updated or created. The docs folder is created only when a first document needs it |
| Phase 7, Review | The spec reviewer checks that the documents match what the code now does; a stale or missing one is a finding |
| Group PR | The group architecture review checks that the feature as a whole is documented, and proposes an overview if it is missing |

Each kind of record has one job:

| Record | Holds | Changes |
|---|---|---|
| The issue | What was asked, and its history | Edited with a `## Changes` log |
| An ADR | Why a decision was taken | Never edited; superseded by a new ADR |
| The docs | How things work now | Updated whenever the code changes |

The docs folder and the project's own rules are set in the **Docs** section of `docs/agents/workflow.md`.
