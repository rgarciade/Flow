# Shape and size of the notes

Read from `SKILL.md` ("Notes") and put in every subagent brief. A note is **working memory for the next role**, not a report and not a log. The user rarely reads it, and the task's records hold what lasts. Write only what the next reader cannot get quickly from the code, the task or the diff.

**Size.** Aim for about 20 lines, and never more than 30. Fewer long lines, no tables of figures.

**Never put in a note:**

- the commands or searches you ran ("Searches: rg …"): the result matters, not how you got it;
- the pros and cons of an option once it is decided, or the options the user rejected;
- the task's description again, or earlier notes again: link them;
- a play-by-play of each change (the diff shows it), or a list of every file read;
- counts and check results the orchestrator re-runs anyway: one line, "checks green" or the failure.

**Shape by role.** Keep these headings, skip one that has nothing to say.

- **research**
  - `Facts that change the plan`: each one line, with `path:line`.
  - `Places the change touches`: one line each, saying whether it is covered.
  - `Decisions needed`: each with its options and a recommendation, in two lines at most.
  - `Size`: fits one session, or why not.
- **plan**: the acceptance criteria, where the tests call the code, the scenarios, what is left out and why, and the manual checks. It is the plan record: it can reach about 40 lines.
- **tests**: the test files and what each covers, in one line each, and the checks that are red as expected.
- **implement, fix**
  - `Outcome`: one line.
  - `Files`: `path:line` and a few words each.
  - `Deviations or questions`: only what departs from the plan or needs the user.
  - `Checks`: one line.
- **review**: the findings table and nothing else.

**Briefs are not notes.** A brief written to a file for another harness is deleted once the role has handed back. Keep nothing of it in the notes.

**The state note is rewritten, not added to.** Each update replaces the whole note, in Engram and in the file. It never grows past about 12 lines: `done` is one short line per finished phase, and `decided`, `waiting on` and `pending commits` are removed as soon as they are settled.
