# Evals

A small, manual check of how the flow skills behave in a real session. Run it after changing a skill, before tagging a version: the skills are prose, so the only way to know a change works is to watch an agent follow it.

It is deliberately minimal: three sample tasks ([tasks.md](tasks.md)) and one checklist ([checklist.md](checklist.md)) that you fill in by reading the conversation. Nothing here is installed into projects.

## What you need

- A project configured with `flow-setup`, where creating throwaway tasks and branches is fine. A small app with a test suite is enough.
- The skills under test installed in it. For a project install, re-run `./install.sh --project <repo>` first, so the copies match this checkout.
- The harness you want to check (Claude Code, OpenCode, Codex CLI, Cursor, Gemini CLI). The checklist does not depend on it.

## How to run it

1. Create the three tasks from [tasks.md](tasks.md) in the project's tracker, adapting the names to the project.
2. **Task A**: run `flow-work` on it and follow it to the pull request.
3. **Task B**: run `flow-work` on it. After you approve the plan, close the session, open a new one and run `flow-work` on the same task again. Follow it to the pull request.
4. **Task C**: run `flow-work` on it and stop once it has offered to split the task. Nothing needs to be built.
5. Answer as a user would. Do not help the agent follow the skill: if it skips something, let it.
6. Go through [checklist.md](checklist.md) once per task, reading the conversation and looking at the task, the branch and the notes.
7. Close the pull requests and delete the throwaway tasks and branches yourself.

A full run takes about one working session. To check a small change, run only the task that exercises it (each one lists what it is for).

## Recording a run

Keep one file per run in `evals/runs/`, named `<date>-<harness>.md`, with this shape:

```markdown
# <YYYY-MM-DD> · <harness> · <model>

flow version: <tag or commit>
project: <where it was run>

| Task | Failed items | Not applicable |
|---|---|---|
| A | none | Q1, P3 |
| B | M4, C3 | |
| C | M2 | P1 to P4, T1 to T2, C1 to C4 |

## Failures

- **B · M4**: the research message said "impact map: 3 sites". Quote the line that failed.
- **B · C3**: the state note still had `phase:` and `waiting on:` after the PR was opened.
```

Quote the failing line: it is what tells you which sentence of the skill to change.

## Reading the result

- A failed item points at a rule in a skill. Fix the rule (or its example), then re-run the task that failed.
- The same item failing in two runs means the rule is not enough as written: make it more concrete, or add an example.
- An item that never fails over several versions can be dropped. Keep the checklist short enough to be used.
