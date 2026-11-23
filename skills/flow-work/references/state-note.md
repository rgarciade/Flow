# Closing the state note

Read from `SKILL.md` (Phase 8, "Close the state note") when the PR is opened.

Rewrite `flow/<repo>/<id>/state` in its closed form. The progress fields, `done` included, are deleted: move into the closed form only what a later task needs from them: what was built, where, and what to watch out for. This is a note for agents, so keep it exact and ordered, in this shape:

```
<ref> <title> · closed <YYYY-MM-DD>
task: <task link> · PR: <PR link> · branch: <task branch>

does: <what works now, in two or three lines; behaviour, not history>
where:
- <path:line>: <entry point | main logic | data | tests>
decisions:
- <decision>: <why> (<ADR-NNNN> if it has one)
gotchas:
- <what surprised us, or what a later change here must not break>
open:
- <review finding left unfixed | follow-up task | part left out, with its reason>
verify: <the command that runs this task's tests, and any manual step>
detail: <the keys of this task's other notes, only when they live in Engram; omit it otherwise>
```

- **Closing means replacing, never appending.** The result is exactly this closed form: a note with `phase:`, `done:`, `running:`, `waiting on:` or `pending commits:` lines is not closed, whatever it says at the end. If the file already holds the progress note, overwrite it whole. This holds when Engram is blocked or missing too: write the closed note to the repo as "Where it is saved" says, never leave `phase: closed` as a last line of the log.
- **Then clean up.** Without Engram, delete the whole `.flow/work/<id>/` folder (it is git-ignored working material: notes, briefs, the approved-tests copy, whose reference is now the `test` commit). The closed note is all that stays, except when the user chose not to commit the tests: the copy and its manifest are then the only reference, so keep that subfolder (`approved-tests/`). With Engram, leave the phase notes there and keep their keys in `detail:`. If the task is parked or abandoned, the closing rules of `references/park-task.md` apply instead.
- **Write it from the final code**, not from the plan: check each `path:line` and each decision against what was merged into the branch. Drop anything that did not survive.
- **About twenty lines.** No retelling of the phases. Omit a section that has nothing to say.
- It needs no confirmation: tell the user in one line that the task's memory is saved, and where.
- If the PR review later changes the code, update the same note when the user says the PR is merged.
- The closed note keeps the PR link and the branch, so a later session knows the PR exists and can ask `pr-status` whether it is still open. If it is open with changes requested, the task goes on in Phase 9 (`references/pr-review.md`); the closed note stays as it is until the merge.
- `open:` also lists the tests that failed before the task (`failing before`) and any reason the task was abandoned (`references/park-task.md`).

## Where it is saved

- **With Engram**: in Engram, under the state key. Nothing else changes.
- **Without Engram**: write it to `.flow/memory/<id>.md` in the repo. The **Task memory** setting in `docs/agents/workflow.md` says what happens next. A missing setting means `local`.
  - `repo`: `.flow/memory/` must not be git-ignored. Give the user a separate commit command, `git add .flow/memory/<id>.md && git commit -m "docs(<commit-ref>): save task memory" && git push`, and wait, as in the hard rules. The note then travels with the branch and reaches every machine and teammate.
  - `local`: make sure `.flow/memory/` is git-ignored, and tell the user in one line that this memory stays on this machine.
- Progress notes (the state note while the task is open, and the other phase notes) still go to `.flow/work/<id>/` as described in "Notes" in `SKILL.md`.
- Phase 3 research looks for closed notes in Engram, or in `.flow/memory/` without it.
