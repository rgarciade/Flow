# Changelog

What changed in each version of the flow skills. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The skills are instructions for an agent, so a change here can change what the agent does in your project without any code changing. Each version therefore starts with **Behaviour changes**: what the agent now does differently, asks differently, or is allowed to do. Read that part before updating a project copy.

**Which version do I have?** A project install records it in `.agents/skills/<skill>/.flow-version`. Copies installed before 0.1.0 show a bare commit hash: treat them as older than 0.1.0 and read all of it.

**Version numbers.** While the version is 0.x, a minor version (0.2.0) may change behaviour and a patch version (0.1.1) never does.

## [0.7.1] - 2026-11-11

### Changed

- Autonomous mode says the task branch needs no new stop when `create-branch` also creates it on the remote: the user confirmed it in Phase 1.
- The review in another harness follows the `review` row of the roles table; "Claude with Codex" is now only an example, not a fixed pairing.
- `references/code-review.md` says that, when run from `flow-work`, the fixed point and the spec come in the brief, so the agent never asks for them.

## [0.7.0] - 2026-11-11

### Behaviour changes

- **New setting, Task memory (`repo` or `local`), asked by `flow-setup`.** Without Engram, the closed note of a finished task is written to `.flow/memory/<id>.md`. With `repo` you get a `docs(<commit-ref>): save task memory` command to commit it, so it reaches every machine and teammate; with `local` (also when the setting is missing) the folder is git-ignored and you are told it stays on this machine. The research phase of later tasks reads closed notes from Engram, or from `.flow/memory/` without it. With Engram nothing changes.
- **Turning a task into a parent no longer renames its branch.** If the task branch has no commits, the agent creates the group branch for the parent from the updated base branch, pushes it, switches to it and proposes deleting the old task branch locally and on the remote, with the exact commands, which run only with your OK. With commits it asks you, as before.
- **The test gate is explicit in semi-autonomous mode.** The tests are always recorded with the `approved-tests` manifest at the gate, with or without edge cases; the `test` commit comes in Phase 6 before the `feat` one, and once you confirm it, its hash becomes the approved-tests reference.
- **A role run in another harness gets its notes as files.** If notes live in Engram, the agent exports what that role needs to `.scratch/flow/<id>/` first and passes the paths; the role writes its result there and the agent saves it to Engram afterwards.
- **After the fixes in Phase 7, one short automatic review looks only at the fix diff.** Nothing found: one line to you. Something found: the same numbered table, and the agent asks. At most one pass per fix round.

### Changed

- `flow-work` now says it is not a job that runs on its own unless you choose autonomous mode, and names the **Harnesses** section (not **Agents**) as where the default working mode is set.
- Two blocks of `flow-work/SKILL.md` moved into `references/other-harnesses.md` and `references/state-note.md`, with no other change.
- `evals/README.md` has a "Before a release" section: run the evals and note the result in the CHANGELOG entry. Evals were not run for these changes.

## [0.6.0] - 2026-11-11

### Behaviour changes

- **The task's state note keeps a short line for each finished phase,** not only the last one: what the phase produced or settled (for example "research: 3 places touched, fits one session"). When the task is resumed, the agent reads how it got there, not just where it stands. When the PR is opened the progress lines are deleted, and only what a later task needs (what was built, where, what to watch out for) moves into the closed note.

## [0.5.0] - 2026-11-11

### Behaviour changes

- **When one of your answers drops or changes something in the plan, the agent updates the plan itself.** In the plan round, if an answer takes something out (or changes it), the reply shows what changed (what now stays out and why, the criteria, scenarios or manual checks affected) and asks for the OK again, without being asked. The tests never start on a plan that differs from the last one you saw.
- **The same holds after the plan is approved.** When a later answer (a test question, a review finding, a closing question) drops or changes something the plan record or the task description states, the agent proposes the edit in the same message, with its line under "Changes to the plan", instead of waiting for the end of the implementation. The edit still needs your OK.

## [0.4.2] - 2026-11-11

### Added

- `npx github:rgarciade/Flow --project <repo>` installs or updates a project without cloning, for the public repo. `package.json` carries the version used for `.flow-version` in that case: keep it equal to the tag when releasing. `--user`, `--claude` and `--dir` still need a clone.

## [0.4.1] - 2026-11-11

### Added

- A check in `evals/checklist.md` (M9) for the scannable messages and the light plan message.
- `install.sh --project` warns when the project's `.gitignore` ignores a skill it just installed (a repo that lists its skills one by one needs a `!.agents/skills/<name>/` line for each), so teammates are not left without it.

## [0.4.0] - 2026-11-11

### Behaviour changes

- **`flow-work` writes every message to you in the scannable format of the `i-have-adhd` skill**, when it is installed: the action first, numbered steps, no preamble or recap. Before, only the list of tests in pair mode used it. The flow's own message shape and plain-language rules still win where they differ.
- **The plan message is lighter.** It lists, in a few one-line items, what you will see change; file, function and parameter names stay in the plan on the task, one link away.

### Added

- `install.sh` now also installs the `i-have-adhd` skill (MIT, version 0.4.1, copied into `vendor/i-have-adhd/`). A skill of yours with that name is kept, and `flow-work` uses it.
- A worked example of a plan message that is too dense (`skills/flow-work/references/phase-messages.md`).

## [0.3.0] - 2026-11-11

### Behaviour changes

- **Changing only the harnesses or models no longer asks for a second approval.** When you run `flow-setup` just to change them, your answers to its three rounds count as the confirmation: it writes the section and shows the before and after in the same message. Nothing is committed, so the diff is the review.
- **The short `## Agent skills` block in `AGENTS.md` or `CLAUDE.md` is brought up to date on that path too.** It is the one exception to "touch only that section": if its text differs from the current template (a repo set up with 0.1 still says "model tiers"), `flow-setup` updates it in place and shows it. It never creates the other file. `tracker.md`, `domain.md` and the docs `README.md` stay untouched.

## [0.2.0] - 2026-11-11

### Behaviour changes

- **Harnesses and models are defined once per harness, and `flow-setup` walks you through them.** "Harness" is Claude Code, OpenCode, Codex and the like. The section of `docs/agents/workflow.md` is now called **Harnesses** (`flow-work` still reads a section called **Agents**, as in 0.1.0) and has two tables: the harnesses you have (where each runs, `subagent` or `<manager>:<harness>` such as `orca:opencode` or `herdr:claude`, with its strong, fast and optional deep model and its effort) and, per role, an ordered list of harnesses. When the first has no quota left, `flow-work` moves to the next and tells you. The deep profile now means that the strong roles use their harness's deep model. The split is fixed by role: usage is not balanced across subscriptions. `flow-setup` asks for this in a round of its own, and can be run again just to change the harnesses or models, touching only that section. A repo with the older **Models** section keeps working as before.

## [0.1.0] - 2026-11-11

The first tagged version. It gathers everything up to this point; the list below covers what changed for copies installed before 2026-11-11.

### Behaviour changes

- **Your OK on the plan now also authorises editing the task description.** When the plan refined the acceptance criteria, the plan message shows them and says so, and one OK covers the plan and that edit. Before, the edit was a separate stop.
- **The plan arrives in one round.** It comes already drafted on an assumed answer for each question, with the questions in the same message. Before, the questions came first and the plan after.
- **The closing decisions are asked together**, right after the final report: ticking the met criteria, the ADRs, the Engram export, opening the PR and moving the task to "in review". Before, each was its own stop.
- **`flow-work` writes a state note for every task** (`flow/<repo>/<id>/state` in Engram, or `.scratch/flow/<id>/state.md`), reads it when a task is resumed, and rewrites it as the task's memory once the PR is opened. That last step needs no confirmation. The research phase of later tasks reads those notes.
- **A note that cannot be saved to Engram goes to `.scratch/flow/<id>/`** in the repo, and you are told. Make sure `.scratch/` is git-ignored.
- **A repo can say who runs each role and which mode tasks start in.** The new **Agents** section of `docs/agents/workflow.md` sets the default working mode and, per role, whether it runs as a subagent or in another coding agent through an agent manager such as Orca (for example the review in Codex when the flow runs in Claude). Without the section nothing changes: semi-autonomous, and subagents for every role. Run `flow-setup` again, or copy the section from `skills/flow-setup/workflow-template.md`, to use it.
- **Messages between phases have a fixed shape and no line budget**: where the task stands, what is needed from you, what the task is about, what the phase found, the questions, and what happens next, in plain words without the skill's internal vocabulary.

### Added

- Worked examples of cryptic and clear phase messages (`skills/flow-work/references/phase-messages.md`).
- One shared rule for asking questions, read by the three skills (`skills/flow-setup/asking-questions.md`).
- `evals/`: sample tasks and a checklist to check how the skills behave after a change.
- This changelog, version tags, and the version in `.flow-version`.
- CI: a link check for the Markdown files and ShellCheck for `install.sh`.
- An MIT licence.

### Changed

- The rules for the task's records and for team visibility moved from `flow-work`'s `SKILL.md` to its `references/` folder. Their content is the same.
- `install.sh --project` writes the version tag to `.flow-version` instead of a bare commit hash.

[0.7.1]: https://github.com/rgarciade/Flow/tree/v0.7.1
[0.7.0]: https://github.com/rgarciade/Flow/tree/v0.7.0
[0.6.0]: https://github.com/rgarciade/Flow/tree/v0.6.0
[0.5.0]: https://github.com/rgarciade/Flow/tree/v0.5.0
[0.4.2]: https://github.com/rgarciade/Flow/tree/v0.4.2
[0.4.1]: https://github.com/rgarciade/Flow/tree/v0.4.1
[0.4.0]: https://github.com/rgarciade/Flow/tree/v0.4.0
[0.3.0]: https://github.com/rgarciade/Flow/tree/v0.3.0
[0.2.0]: https://github.com/rgarciade/Flow/tree/v0.2.0
[0.1.0]: https://github.com/rgarciade/Flow/tree/v0.1.0
