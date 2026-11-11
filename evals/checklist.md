# Checklist

Fill it in once per task, by reading the conversation. Each item is **pass**, **fail** or **not applicable**. An item fails if it fails in any message of the run; note which one.

Each item names the rule it checks, so a failure points at the text to fix.

## Every message between phases

Rule: "Phase messages" in [flow-work](../skills/flow-work/SKILL.md), with the examples in [phase-messages.md](../skills/flow-work/references/phase-messages.md).

| | Check |
|---|---|
| M1 | The first line says which task it is, which phase just ended and which comes next. |
| M2 | It says what is needed from you: an OK, answers, a choice, or nothing. |
| M3 | One line says what the task is about, so the message can be read without remembering the issue. |
| M4 | None of the skill's own words appear: seam, impact map, size verdict, edge case, plan record, summary record, standards axis, spec axis, deep profile, strong or fast tier, a note key, an operation name such as `move-status`. |
| M5 | It is written in full sentences, and a name taken from the code is explained the first time it appears. |
| M6 | It ends by saying what happens once you answer, and what a plain "OK" accepts. |
| M7 | You could understand it after a break, without scrolling up. |
| M8 | Before a long step, one line says what starts and what you will get back. |
| M9 | The message can be scanned: the action or answer needed comes first, there is no preamble or recap, and file, function and parameter names stay out of it. The plan message lists what you will see change in about five one-line items and links to the plan on the task for the technical detail. |

## Questions

Rule: [asking-questions.md](../skills/flow-setup/asking-questions.md).

| | Check |
|---|---|
| Q1 | The questions of a phase arrive together in one message, not one after another. |
| Q2 | Each question has a proposed answer, placed first, with its reason. |
| Q3 | Each question can be answered without reading anything outside that message. |
| Q4 | Nothing is asked that the task or the code already settles. |

## Research

Rule: "Phase 3" in flow-work.

| | Check |
|---|---|
| R1 | Places in the code that the change touches and the issue did not mention are reported, each as something to decide. (Task B) |
| R2 | It says whether the task fits in one session. When it does not, it stops and offers both ways out as one question. (Task C) |
| R3 | A different working mode is proposed as a question and only used after your yes. |

## The plan

Rule: "Phase 4" in flow-work.

| | Check |
|---|---|
| P1 | The plan and its questions arrive in the same message, with the plan already drafted on the assumed answers. |
| P2 | When the criteria changed, the message says that your OK also updates the task description, and no separate stop follows for it. |
| P3 | After an answer that changes the plan, including one that drops something, the reply shows what changed (what is now left out and why) and asks for the OK again, without being asked. The tests do not start on a plan you have not seen. |
| P4 | After the OK, the task has the plan as a comment (or file), and its description holds the criteria as a checklist. |
| P5 | When you answer a later question by dropping or changing something the plan states, the reply proposes the edit to the plan on the task (and to the description if a requirement changed) right away, without being asked. |

## Tests, commits and the task

Rule: "Hard rules" and "Phase 5" to "Phase 7" in flow-work.

| | Check |
|---|---|
| T1 | No commit was run without you saying so, and every commit command ends with `git push`. |
| T2 | The test files did not change after they were approved (`git log --stat` on the branch shows them only in `test` commits). |
| T3 | Review findings come as one numbered table per question ("does it follow the project's rules", "does it do what the task asks"), and each finding can be decided without opening the file. |
| T4 | After fixes, one short review of only the fix diff runs on its own: with nothing found you get one line, otherwise the findings come in the same numbered table. It runs once per fix round. |

## Closing

Rule: "Phase 8" in flow-work.

| | Check |
|---|---|
| C1 | The closing decisions (ticking the criteria, ADRs, memory export, opening the PR) are asked together, right after the report. |
| C2 | The report marks each criterion with the same text the description has. |
| C3 | After the PR is opened, the state note is in its closed form: what the task does, where, decisions and what to watch out for, and no progress fields (`phase:`, `done:`, `waiting on:`, `pending commits:`). Read it in Engram under `flow/<repo>/<id>/state`, or in `.flow/memory/<id>.md` without Engram. |
| C4 | One line tells you that the task's memory was saved, and where. Without Engram: with Task memory `repo` you are given a commit command for `.flow/memory/<id>.md`; with `local` (or no setting) you are told it stays on this machine. |

## The state note and resuming

Rule: "The state note" in flow-work. Checked on Task B, at the restart.

| | Check |
|---|---|
| S1 | Before the restart, the state note exists and names the right phase, mode and pending questions, and keeps one short line for each phase already finished. |
| S2 | In the new session, the first message says where the task stands and what was waiting on you. |
| S3 | Nothing you had already decided is asked again. |
| S4 | If a note could not be saved to Engram, it went to `.scratch/flow/<id>/` and you were told in one line. |
