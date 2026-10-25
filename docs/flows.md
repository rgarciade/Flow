# Flows

How the pieces fit together. The skills themselves are the source of truth: [flow-setup](../skills/flow-setup/SKILL.md), [flow-plan](../skills/flow-plan/SKILL.md), [flow-work](../skills/flow-work/SKILL.md).

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
| 1. Task | orchestrator | The issue (read or created) and its position: parent, blockers, children | Approve the draft if it was created |
| 2. Branch | orchestrator | `task/<n>-<slug>` (and the group branch if needed) | |
| 3. Research | research subagent | What exists, open questions, size verdict | Choose (a) or (b) if it is too big |
| 4. Plan | plan subagent | Refined criteria, seams, scenarios, outline | Answer questions, confirm seams |
| 5. Tests | tests subagent | Failing tests, each for the expected reason | **Approve the tests**, `test(#n)` commit |
| 6. Implement | implement subagent(s) | Code that passes the frozen tests | `feat(#n)` commit |
| 7. Review | 2 review subagents, then fix | Standards and spec reports | Choose findings, `fix`/`refactor` commit |
| 8. Report and PR | orchestrator | Report and PR | Review the code, merge the PR |

**Frozen tests.** After the approval, `git diff <test commit> -- <test globs>` must stay empty. If a test looks wrong during implementation, the work stops and you decide.

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
