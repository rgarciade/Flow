# flow

[Leer en español](README-es.md)

**Issue-Driven Development** for AI coding agents.

A small set of [Agent Skills](https://agentskills.io/specification) for planning work as tasks in your tracker and developing it one vertical slice at a time, with the human in the driver's seat.

> [!NOTE]
> **When to use it.** `flow` is not meant to be a standard for every project. It fits when there is uncertainty and things are not clear yet:
>
> - **A personal project** where you don't know exactly what you want to build and you find it out step by step.
> - **A work project with a lot left undefined**, where requirements arrive late or keep changing.
> - **An older project with a task-based workflow**: work arrives as tasks in a tracker and the code grows task by task.
>
> When the scope is clear and stable up front, a spec-driven approach such as OpenSpec or BMAD may serve you better (see [IDD vs SDD](docs/idd-vs-sdd.md)).

> [!IMPORTANT]
> `flow` is strictly a flow **from tasks**. Spec-driven development starts from a specification; `flow` starts from a task in your tracker (an issue). Nothing is built without one: every branch, test, commit and pull request belongs to an issue, and the issue stays the source of truth for what was asked and how it was built.

<p align="center">
  <img src="docs/diagrams/overview.svg" alt="The three flow skills and the files they read and write" width="900">
</p>

## The skills

- **[`flow-setup`](skills/flow-setup/SKILL.md)** · _Once per repo_  
  Asks which task tracker you use and writes `docs/agents/` (how every task operation is done, domain docs, workflow settings) so the other skills know how this repo works.
- **[`flow-backlog`](skills/flow-backlog/SKILL.md)** · _Backlog sessions_  
  Turns ideas into tasks in your tracker: standalone tasks, or a parent task with children and blocking links. No code.
- **[`flow-work`](skills/flow-work/SKILL.md)** · _Developing a task_  
  Takes one task from branch to PR: research → plan → tests (your OK) → implement + docs → review → ADRs → PR.

`flow-backlog` and `flow-work` check for `docs/agents/workflow.md` first, and offer to run `flow-setup` if it is missing.

## How a task flows

<p align="center">
  <a href="docs/flows.md"><img src="docs/diagrams/flow-work-phases.svg" alt="flow-work phases, with the points where you decide and the commit points" width="900"></a>
</p>

Every phase, branch and subagent, step by step: **[docs/flows.md](docs/flows.md)**. Where the requirements, the plan, the ADRs and the project docs live, and when each is written: **[Where knowledge lives](docs/flows.md#where-knowledge-lives)**.

## Why

Spec-driven workflows plan everything up front and end in huge pull requests nobody really reviews. `flow` goes task by task instead ([IDD vs SDD](docs/idd-vs-sdd.md)):

- **You stay in the loop.** It shows you each phase, asks when something is not settled, and never commits or merges on its own.
- **The issue drives everything.** Requirements, plan and summary live on the task, in any tracker: GitHub, GitLab, Jira, Linear or plain files.
- **Detail just in time.** The issue gives the big picture; the plan works out criteria, design and tests against the code as it is when the task starts.
- **One task, one vertical slice.** Each one works end to end and fits one working session. Too big? Split it into child tasks.
- **Tests first, then frozen.** The implementation must pass them without touching them; any change needs your OK.
- **Visible from the first minute.** The branch is linked to the issue, every approved commit is pushed, and the status moves with your OK.
- **Architecture and docs as you go.** Architectural decisions become ADRs, and the docs the task affects are updated before the PR.

## Quick start

```sh
# 1. Install the skills (see docs/setup.md)
./install.sh --project ~/code/my-app      # into one repo, for every harness (versioned copies)
./install.sh --user                       # or for your user: OpenCode, Codex, Cursor, Gemini CLI
./install.sh --claude ~/.claude-personal  # or into a Claude Code profile

# 2. In the project, open your agent and run:
/flow-setup          # once per repo
/flow-backlog        # create tasks
/flow-work #42       # develop one
```

Works with any harness that supports Agent Skills: Claude Code, OpenCode, Codex CLI, Cursor, Gemini CLI. It is developed and tested on Claude Code; [setup.md](docs/setup.md) covers the differences.

**Where things live.** The skills are installed once per user, or copied into a repo when it should carry them. Each repo's own rules live in its `docs/agents/`, written by `flow-setup`: how its task tracker works (`tracker.md`) and its branches, languages, models and commands (`workflow.md`). Your general instructions file (`CLAUDE.md`, `AGENTS.md`…) stays yours: `flow-setup` only adds a short `## Agent skills` block that points at `docs/agents/`.

## Documentation

- [IDD vs SDD](docs/idd-vs-sdd.md): how this flow compares with spec-driven development, and when to use each.
- [Setup](docs/setup.md): requirements, installation, configuring a repo.
- [Usage guide](docs/usage.md): day-to-day recipes.
- [Flows](docs/flows.md): how each phase, branch and subagent fits together.

## Credits

- The working method is inspired by a talk on replacing spec-driven development with backlog + user stories + vertical slices + pair programming with AI.
- Some vendored skills and references are adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
