# Changelog

What changed in each version of the flow skills. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The skills are instructions for an agent, so a change here can change what the agent does in your project without any code changing. Each version therefore starts with **Behaviour changes**: what the agent now does differently, asks differently, or is allowed to do. Read that part before updating a project copy.

**Which version do I have?** A project install records it in `.agents/skills/<skill>/.flow-version`. Copies installed before 0.1.0 show a bare commit hash: treat them as older than 0.1.0 and read all of it.

**Version numbers.** While the version is 0.x, a minor version (0.2.0) may change behaviour and a patch version (0.1.1) never does.

## [Unreleased]

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

[0.4.2]: https://github.com/rgarciade/Flow/tree/v0.4.2
[0.4.1]: https://github.com/rgarciade/Flow/tree/v0.4.1
[0.4.0]: https://github.com/rgarciade/Flow/tree/v0.4.0
[0.3.0]: https://github.com/rgarciade/Flow/tree/v0.3.0
[0.2.0]: https://github.com/rgarciade/Flow/tree/v0.2.0
[0.1.0]: https://github.com/rgarciade/Flow/tree/v0.1.0
