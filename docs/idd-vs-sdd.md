# Issue-Driven vs Spec-Driven Development

`flow` is **Issue-Driven Development (IDD)**: work starts from a task in your tracker, gets its detail just in time, and is built one vertical slice at a time with you in the loop. **Spec-Driven Development (SDD)**, as in SpecKit, Kiro, BMAD or OpenSpec, starts from a specification written up front and executes it.

Neither is better everywhere. This page compares them honestly and says when to pick each.

## At a glance

| | IDD (`flow`) | SDD |
|---|---|---|
| Starting point | A task: the big picture, a few outcomes, preliminary notes | A specification: requirements, design and tasks up front |
| When detail is decided | In each task's plan, against the code as it is then | Before building, for the whole scope |
| Unit of delivery | One vertical slice per task, one small PR | Often layer by layer, ending in large PRs |
| Human role | Navigator in every phase; approves plan, tests, commits, records | Approves the spec, then reviews the result |
| Visibility while building | Linked branch, pushed commits, plan record and status on the task | Mostly at the PR |
| Architecture | Architecture notes, ADRs as decisions happen, reviews against them, a group review per feature | Designed up front in the spec |
| Documentation | Just-enough living docs, updated in every task | The spec itself, plus whatever is written after |
| Tooling | Your tracker (any, through an adapter) and git | The spec framework's documents and commands |

## Where IDD is stronger

- **Detail that doesn't go stale.** Requirements change between planning and building. IDD decides the detail when the task starts, so the plan matches the code as it is; a spec written weeks earlier often doesn't.
- **Small, reviewable PRs.** One vertical slice per task means each PR shows one working change. You can actually review it.
- **Something works after every task.** Feedback comes in days, not at the end of the whole spec.
- **The team sees progress before the PR.** The branch is linked to the task from the first minute, every approved commit is pushed, the plan is on the task and its status moves. With SDD, the team usually learns where things stand when the PR lands.
- **You stay in control.** You confirm the task, answer the open questions, approve the tests (which are then frozen), and decide every commit. The AI saves you typing, not thinking.
- **Cheap to change your mind.** Changing direction means changing the next task, not rewriting a spec and everything derived from it.
- **Less over-engineering.** Each task builds only what it asks for; the agent isn't preparing the code for the whole spec at once.
- **Fits the tools the team already uses.** Any tracker (GitHub, GitLab, Jira, Linear, files) through `docs/agents/tracker.md`, plus git.

## Where SDD is stronger

- **Thinking the whole system first.** A spec forces a global design before any code. IDD compensates with architecture notes on parent tasks, ADRs written as decisions happen, reviews against them and a group architecture review, but it still designs as it goes. For a greenfield system with many interacting parts, an up-front design pass is valuable.
- **Fire and forget.** SDD lets you hand over a long piece of work and review the result. IDD asks for your attention in every phase; its autonomous mode only covers simple tasks.
- **Large, well-understood work.** A migration or a rewrite with stable, known requirements can be specified once and executed; slicing it into many planned tasks can be slower.
- **Contracts between teams.** An API or integration that several teams depend on needs a stable agreement before anyone builds. The spec is that contract from day one.
- **One document that describes the system.** IDD spreads knowledge on purpose (the task for _what_, ADRs for _why_, docs for _how it works now_). Some teams and auditors want a single specification instead.

## Shared risks

- **Discipline.** A spec nobody updates and a task whose plan record drifts fail in the same way. `flow` reduces the risk with the `## Changes` log on the description, the "Changes to the plan" log, and reviews that check docs and ADRs, but it can't replace the habit.
- **The agent follows instructions, not intentions.** Both approaches depend on the agent doing what the skill or the spec says. Review the code either way.

## When to use which

**Prefer IDD (`flow`) when:**

- it is not yet clear what you are building, so you find it out task by task;
- the project already works from tasks in a tracker;
- the product evolves and requirements change while you build;
- you want small PRs that you or your team actually review;
- teammates need to see where each piece of work stands before the PR;
- developers want to understand and own the code that goes in;
- work comes as a stream of features and fixes rather than one big defined project.

**Prefer SDD when:**

- several teams or systems need a stable contract before building;
- the work is a large, well-defined migration or rewrite;
- you want to delegate a long piece of work and review it at the end;
- a single up-front specification is required (by a client, an auditor, a regulation).

**Combine them** for big features in an evolving product: write a light spec of the architecture or the contract (the parent task's architecture notes, or an ADR in `docs/adr/`), then build it with IDD, one child task at a time. That keeps the global view of SDD and the just-in-time detail, visibility and review of IDD.
