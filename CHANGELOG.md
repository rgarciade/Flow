# Changelog

What changed in each version of the flow skills. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The skills are instructions for an agent, so a change here can change what the agent does in your project without any code changing. Each version therefore starts with **Behaviour changes**: what the agent now does differently, asks differently, or is allowed to do. Read that part before updating a project copy.

**Which version do I have?** A project install records it in `.agents/skills/<skill>/.flow-version`. Copies installed before 0.1.0 show a bare commit hash: treat them as older than 0.1.0 and read all of it.

**Version numbers.** While the version is 0.x, a minor version (0.2.0) may change behaviour and a patch version (0.1.1) never does.

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

[0.1.0]: https://github.com/rgarciade/Flow/releases/tag/v0.1.0
