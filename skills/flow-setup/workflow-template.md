# Workflow

Settings read by the `flow-plan` and `flow-work` skills. Edit this file directly to change them.

## Branches

- **Base branch**: `<base>`. Every feature ends up here.
- **Group branch** (a parent issue with child tasks): `feature/<issue>-<slug>`, created from the base branch. Its PR targets the base branch.
- **Task branch**: `task/<issue>-<slug>`.
  - A child task branches from its group branch, and its PR targets the group branch.
  - A standalone task (no parent) branches from the base branch, and its PR targets the base branch.
- A child task starts only after the PRs of the tasks that block it are merged into the group branch. The user reviews and merges every PR.

## Languages

- **Issues** (titles and bodies): `<language>`
- **Pull requests** (titles and bodies): `<language>`
- **Commit messages**: Conventional Commits, `<language>`

## Commands

| Purpose | Command |
|---|---|
| Full test suite | `<command or none>` |
| Single test file | `<command with {file} placeholder, or none>` |
| Typecheck | `<command or none>` |
| Lint | `<command or none>` |

## Models

Model tiers used by `flow-work`'s subagents. Use the model names your harness accepts (for example `opus` and `sonnet` in Claude Code, or `provider/model-id` in OpenCode). Write `inherit` to use the session model.

- **strong** (plan, tests): `<model>`
- **fast** (research, implement, review, fix): `<model>`

## Status tracking

How `flow-work` moves an issue through its states. It always asks before each move.

- **Status tracking**: `<none | labels | project>`
- If `labels`: in progress `<label>`, in review `<label>`, done `<label, or "closed">`
- If `project`: owner `<owner>`, project number `<n>`, field `<Status>`, options: in progress `<option>`, in review `<option>`, done `<option>`

## Engram sync

Shares this project's Engram memory through git, in the `.engram/` folder. `flow-work` imports new chunks when it creates a branch, and offers to export before opening a PR.

- **Engram sync**: `<ask | always | never>`

## Tests

- **Test file globs**: `<glob>`, `<glob>`
- Approved tests are never edited during implementation. The check is `git diff <approved-tests-commit> -- <globs>`, which must be empty.

## Labels

- Applied when creating issues: `<labels, or none>`

## Notes

<Anything else specific to this repo. Optional.>
