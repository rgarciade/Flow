# flow

[Leer en español](README-es.md)

**Issue-Driven Development** for AI coding agents.

A small set of [Agent Skills](https://agentskills.io/specification) for planning work as tasks in your tracker and developing it one vertical slice at a time, with the human in the driver's seat.

> [!NOTE]
> **When to use it.** `flow` is not meant to be a standard for every project. It fits when there is uncertainty and things are not clear yet:
>
> - **A personal project** where you don't know exactly what you want to build and you find it out step by step.
> - **A work project with a lot left undefined**, where requirements arrive late or keep changing.
> - **An older project with a task-based workflow**, as many teams worked before specs: work arrives as tasks in a tracker and the code grows task by task.
>
> When the scope is clear and stable up front, a spec-driven approach such as OpenSpec or BMAD may serve you better (see [IDD vs SDD](docs/idd-vs-sdd.md)).

> [!IMPORTANT]
> `flow` is strictly a flow **from tasks**. Spec-driven development starts from a specification; `flow` starts from a task in your tracker (an issue). Nothing is built without one: every branch, test, commit and pull request belongs to an issue, and the issue stays the source of truth for what was asked and how it was built.

<p align="center">
  <img src="docs/diagrams/overview.svg" alt="The three flow skills and the files they read and write" width="900">
</p>

## Why

Spec-driven workflows plan everything up front, build layer by layer and end in huge pull requests that nobody really reviews. Issue-driven development takes the opposite approach (full comparison, and when SDD is the better choice: [IDD vs SDD](docs/idd-vs-sdd.md)):

- **You are in the loop, all the way.** This is not a job you launch and come back to. You work with the agent: it shows you what each phase found, asks you whenever something is not settled, and waits for your OK before moving on. Think pair programming, with you as the navigator. For a simple task you can tell it to work autonomously: it then stops only for what really needs you.
- **Visible from the first minute, not at the PR.** In spec-driven teams nobody knows where a piece of work stands until the pull request lands. Here the branch is linked to the issue from the start, every approved commit is pushed, the plan is on the issue, and its status moves (with your OK) from in progress to in review.
- **Any task tracker.** GitHub Issues, GitLab, Jira, Linear, Azure Boards, or plain files in the repo. `flow-setup` records how each operation is done in your tracker, so tasks and their records always look the same; what the tracker can't do gets an agreed alternative (for example a task folder in the repo, linked from the task).
- **The issue drives everything.** Requirements live in the task description, the implementation plan in one record on it, and the summary in another. When requirements change, the description is updated with a log of what changed and why.
- **Detail just in time.** A spec tries to define everything up front, and much of it is stale by the time someone builds it. An issue gives the big picture, the few outcomes that define "done" and the leads from a preliminary look (libraries, connectors, risks). The detailed criteria, design and tests are worked out in the plan phase, against the code as it is when the task starts. That is how teams worked before specs: no guessing too early, but no empty tickets either.
- **Architecture written as you go.** Small tasks can lose the big picture, so `flow` keeps it explicit: parent issues carry architecture notes, each plan flags its architectural decisions, those become ADRs before the PR, reviews check the code against existing ADRs, and a whole feature gets an architecture review before it reaches the base branch.
- **Docs are part of "done".** Each plan lists the project documents the task affects, they are updated with the implementation, and the review flags any that are stale. Just enough: only what the code cannot easily tell. The issue keeps what was asked, ADRs keep why, docs keep how things work now.
- **Plan small, plan when you want.** Tasks live in your tracker. You create them in a planning session, or right before starting one.
- **One task, one vertical slice.** Each task works end to end when it is done, and fits one working session. Too big? Split it into child tasks.
- **Tests first, approved by you.** The AI writes the tests, you approve them, and from then on they are frozen: the implementation must make them pass without touching them. If one turns out to be wrong, it changes only with your OK, in its own commit.
- **The AI writes, you decide.** It never commits or merges on its own. It gives you the command; you run it, or tell it to.
- **Small context, specialised helpers.** An orchestrator talks to you and delegates research, planning, tests, implementation and review to subagents that share details through notes (Engram, or files when it is not available).

## The skills

- **[`flow-setup`](skills/flow-setup/SKILL.md)** · _Once per repo_  
  Asks which task tracker you use and writes `docs/agents/` (how every task operation is done, domain docs, workflow settings) so the other skills know how this repo works.
- **[`flow-plan`](skills/flow-plan/SKILL.md)** · _Planning sessions_  
  Turns ideas into tasks in your tracker: standalone tasks, or a parent task with children and blocking links. No code.
- **[`flow-work`](skills/flow-work/SKILL.md)** · _Developing a task_  
  Takes one task from branch to PR: research → plan → tests (your OK) → implement + docs → review → ADRs → PR.

`flow-plan` and `flow-work` check for `docs/agents/workflow.md` first, and offer to run `flow-setup` if it is missing.

## How a task flows

<p align="center">
  <a href="docs/flows.md"><img src="docs/diagrams/flow-work-phases.svg" alt="flow-work phases, with the points where you decide and the commit points" width="900"></a>
</p>

Every phase, branch and subagent, step by step: **[docs/flows.md](docs/flows.md)**. Where the requirements, the plan, the ADRs and the project docs live, and when each is written: **[Where knowledge lives](docs/flows.md#where-knowledge-lives)**.

## Quick start

```sh
# 1. Install the skills (see docs/setup.md)
./install.sh --project ~/code/my-app      # into one repo, for every harness (versioned copies)
./install.sh --user                       # or for your user: OpenCode, Codex, Cursor, Gemini CLI
./install.sh --claude ~/.claude-personal  # or into a Claude Code profile

# 2. In the project, open your agent and run:
/flow-setup          # once per repo
/flow-plan           # create tasks
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
