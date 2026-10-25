---
name: flow-work
description: Develop one task end to end, from any task tracker (GitHub Issues, GitLab, Jira, Linear, local files…), as an orchestrator with role subagents - research, plan, tests first with a user approval gate, implementation, two-axis review, PR. Takes a task id, or creates the task from the current conversation and starts right away. Never commits on its own. Use when the user runs /flow-work, or asks to pick up, start or develop a task.
---

# flow-work

Paths starting with `../` are relative to this skill's folder: they point at sibling skills in the same skills directory.

You are the **orchestrator**. You work **with the user, in the session**: you show what each phase found, ask their questions, and move on only when they agree. This is pair work with the user as the navigator, never a job that runs on its own. Bulky work goes to **role subagents**, so your own context stays small.

## Hard rules

These override anything more permissive elsewhere, including the user's general git instructions:

- **The user is in the loop at every phase.** End each phase by showing its result in a few lines and saying what comes next. Don't chain phases silently. The only exception is autonomous mode, and only when the user asks for it (see "Autonomous mode").
- **Decisions belong to the user.** Anything the issue and the agreed plan don't settle (a design choice, a dependency, a trade-off, a scope question) goes to the user as a question with your recommendation. Never decide it for them.
- **Never commit on your own.** At each commit point, give the user the exact command and wait. Run it only if the user explicitly tells you to.
- **Never merge PRs.** The user reviews and merges every PR on the code host.
- **Never modify approved tests on your own.** After the test gate, the test files are frozen. If a test looks wrong, follow "Changing an approved test": stop, explain why, and change it only after the user's OK.
- **One writer at a time.** Subagents that edit files run one after another. Read-only subagents (research, review) may run in parallel.
- **No worktrees, no child branches beyond the ones in `docs/agents/workflow.md`.**
- **Ask one question at a time.** After asking, stop and wait.

## Subagents

Launch each role as a subagent with your harness's own mechanism: the `Agent` tool in Claude Code (`subagent_type: "general-purpose"`), the `Task` tool in OpenCode and Cursor, the subagent support in Codex or Gemini CLI. If the harness cannot spawn subagents, run the phase yourself, keeping the same brief and hand-back discipline.

Each role uses a model **tier**. The **Models** section of `docs/agents/workflow.md` maps each tier to a model for this repo (for example `strong: opus`, `fast: sonnet`). That mapping is the user's choice and overrides any default subagent model. If the harness cannot choose a model per subagent, the subagent inherits the session model. Start each subagent's visible name with the model it runs on, for example `opus: tests #42`.

| Role | Tier | Writes files? |
|---|---|---|
| research | fast | no |
| plan | strong | no |
| tests | strong | yes (test files only) |
| implement | fast | yes (never test files) |
| review-standards, review-spec | fast | no |
| fix | fast | yes (never test files) |

Every subagent brief includes:

- The repo path, task id and current branch.
- Pointers, not pasted content: the task (read it with `view-task`), `docs/agents/*.md` including the tracker file, and the notes from earlier phases.
- The rule: read only what the role needs; do not spawn agents; artifacts (code, comments, test names) in English unless the repo already uses another language.
- The rule: subagents cannot talk to the user. When something is not settled by the issue, the plan or the brief, stop and return it as a question, with options and a recommendation. Do not guess.
- The hand-back contract: **save the full result as a note under the key given, then return at most 15 lines**: outcome, files touched (as `path:line` links), the note key, and any blocker or question for the user. No pasted logs or file contents.

**Notes.** Keys follow `flow/<repo>/<id>/<phase>`, for example `flow/my-app/42/research`.

- With the Engram MCP server available: save with `mem_save` (topic key = the note key), read with `mem_search` and `mem_get_observation`, update with `mem_update`.
- Without it: write the note to `.scratch/flow/<id>/<phase>.md` in the repo and pass that path instead. Make sure `.scratch/` is git-ignored.

Notes are working memory for this session's subagents. The durable record lives with the task.

## The task tracker

This skill works with any task tracker. It never calls one directly: every operation written in backticks, such as `view-task`, `create-record` or `move-status`, is looked up in `docs/agents/tracker.md` (or the shared tracker file named in `workflow.md`), and done exactly as written there. That file also says:

- how a task is identified (`<id>`), referenced in text (`<ref>`, for example `#42` or `PROJ-123`), written in branch names (`<id>`) and in commit messages (`<commit-ref>`, as in `feat(<commit-ref>): …`);
- the markup, the **note block** and the **record marker** to use;
- which **alternatives** replace what the tracker can't do, for example a task folder in the repo (`.flow/tasks/<id>/`) instead of comments. When an operation uses an alternative, follow the alternative.

In this skill, "task" means a task in that tracker, and "issue" is used in the same sense. If an operation is missing from the tracker file, ask the user how to do it, propose adding it to the file, and continue.

## The task is the source of truth

Anyone must be able to understand the task from the tracker alone (plus its task folder, if the tracker uses that alternative), without the notes. Keep the task lean: **at most two records per task from this flow**, the plan record and the summary record. A record is a comment on the task, or a file in the task folder, depending on the tracker. When something changes, **edit** what exists instead of adding something new.

**Permissions:**

- **Creating** the plan record or the summary record needs no confirmation.
- **Editing** the description or a record, and **deleting** anything, always need the user's OK: show the exact change first and wait.

**The description holds the _what_**: what to build, acceptance criteria, out of scope. When the agreed requirements change, propose an edit of the description (never a new record) with:

- the requirements rewritten as they now stand, and
- at the bottom, a `## Changes` section (heading in the task language) with one dated line per change: what changed and why. Keep earlier lines.

Apply it with `edit-description` once the user approves.

**The plan record holds the _how_**: a short implementation summary, created with `create-record` at the end of Phase 4. Never create a second plan record: if the plan changes, find it with `find-record` (marker `flow:plan`) and propose an edit with `edit-record`.

**The summary record** is created once, when the PR is opened (Phase 8), with the marker `flow:summary`. If it already exists (for example, the PR was reopened), propose an edit instead.

To link the description to the plan record, include `Implementation notes: <record link>` in the next description edit the user approves. Don't edit the description only to add this link.

Write both records in the task language from `docs/agents/workflow.md`, in the tracker's markup, with its note block and record marker; translate the headings and the note text too. The templates below are in GitHub Markdown; adapt them to the tracker's format.

Plan record template (10 to 15 lines below the header):

```markdown
<!-- flow:plan -->
> [!NOTE]
> **Implementation notes**: how this task is being built. The requirements are in the task description; flow-work updates these notes when the plan changes.
> Last update: <YYYY-MM-DD> · branch `<task branch>`

### Seams under test
- `<public interface>`: what it catches

### Scenarios
1. <one line per scenario>

### Steps
1. <implementation outline, no file-level detail>

### Docs
- <document to create or update>: <what changes> (or "none")

### Architecture decisions
- <decision>: <one line on why> (ADR candidate; omit the section if there are none)

### Changes to the plan
- <YYYY-MM-DD>: <what changed and why> (omit the section until something changes)
```

Summary record template:

```markdown
<!-- flow:summary -->
> [!NOTE]
> **Implementation summary**: what was built for this task. PR: <PR link>

- **Works now**: <one or two lines>
- **Acceptance criteria**: <n>/<n> ✅ (list any ❌)
- **Deviations from the plan**: <none, or one line each>
- **Open review findings**: <none, or one line each>
- **ADRs**: <ADR-NNNN title, or none>
- **Docs**: <documents created or updated, or none>
```

## Team visibility

Task-driven work is visible while it happens, not only when the PR arrives. Anyone looking at the task can see who is on it, in which branch, at which stage, and every commit so far.

- **Linked branch.** Create task branches with `create-branch` (Phase 2), which links the branch to the task, or names it so the tracker links it.
- **Pushed commits.** Every commit command you give the user ends with `git push`, so each approved step shows up on the linked branch.
- **The plan record** tells the team how the task is being built (see "The task is the source of truth").
- **Assignment.** When the user confirms the task (Phase 1), propose assigning the task to them with `assign`, and do it after their OK. Skip it if the tracker file says `assign` is not used.
- **Status moves.** Unless the tracker file says `move-status` is not used, propose moving the task's status at these points with `move-status`, and move it only after the user's OK (one line, it can share a message with the phase's other question):

  | When | Move to |
  |---|---|
  | The user confirms the task (Phase 1) | in progress |
  | The PR is opened (Phase 8) | in review |
  | The PR is merged | done (often automatic through the `closing-reference`; only propose it if it did not happen) |

## Autonomous mode

For a task that is not complex, the user can ask you to work autonomously ("work on your own", "autonomous mode"). You may also suggest it after research, when the size verdict says the task is small. Never switch to it without the user's explicit yes.

In autonomous mode, chain the phases without stopping for routine confirmations:

- **Skip:** showing each phase's result and waiting, the research summary, the seams confirmation, the test gate and the progress lines. Take the plan's assumed answers when they are clearly safe.
- **Still stop for** what really needs the programmer:
  - a decision the issue and the plan don't settle, where a wrong guess would cost real rework;
  - a test that looks wrong (see "Changing an approved test"), or a check you cannot make pass;
  - a task that turns out bigger than it looked;
  - anything that leaves the machine or changes shared state: commits, pushes, status moves, issue edits, the PR.
- **Tests stay frozen.** With no test gate, record the tests with the `.scratch/flow/<id>/approved-tests/` manifest right after writing them, and check them against it as usual.
- **Commits come at the end.** Instead of a commit command per phase, give the user the `test`, `feat` and `fix`/`refactor` commands (and `chore` for an Engram export) together with the final report, each ending with `&& git push`.
- **The final report is never skipped.** It also lists every assumption you made on the user's behalf, so they can check them.

The user can leave autonomous mode at any moment ("stop", "back to pair mode"). Go back to stopping at every phase from there.

## Changing an approved test

Sometimes implementation shows that an approved test was wrong: the requirement was misread, a library behaves differently than assumed, or the seam was badly chosen. That is legitimate. Changing a test because it is inconvenient for the code is not. Approved tests change only through this procedure, in pair and autonomous mode alike:

1. **Detect.** The subagent that hits the problem stops without touching the test, and returns: which test (`path:line`), why it believes the test is wrong, the evidence (the code, the library docs, or the requirement that contradicts it), and the change it proposes.
2. **The user decides.** Show it in a few lines with your recommendation, and say which case it is: the test was wrong, or the requirement changed. If the honest answer is "the test is right and the code is hard", say so and recommend keeping the test.
3. **Change.** After the user's OK, brief the tests subagent (strong tier) to change **only** those tests. Each must again fail for the expected reason, or pass if the implementation already covers it. Never loosen an assertion only to make it pass.
4. **Record.**
   - Give the commit command `git add <test files> && git commit -m "test(<commit-ref>): adjust <what> (<why>)" && git push`. Once the user confirms it, that commit becomes the new approved-tests reference for the checks; save its hash in the tests note. With the `.scratch` record instead, refresh the manifest.
   - Propose a line under "Changes to the plan" in the plan record (an edit, so it needs the user's OK).
   - If a requirement changed, also propose the `## Changes` line in the issue description.
5. **Continue** implementing against the new tests.

## Phase 0: Preflight

1. Read `docs/agents/workflow.md`. If it does not exist, tell the user and ask, in one line, whether to run `flow-setup` now. If yes, read `../flow-setup/SKILL.md`, follow it, then come back here. If no, stop. If a field this skill needs is missing, ask only for that field.
2. Read the tracker file (`docs/agents/tracker.md`, or the shared path in `workflow.md`). If only an old `docs/agents/issue-tracker.md` exists, offer to run `flow-setup` to convert it.
3. Run `git status`. If there are uncommitted changes that are not part of this task, stop and ask the user what to do with them.

## Phase 1: The task

- **Task id given** (`#42`, `PROJ-123` or a URL): read it with `view-task`. State its title back to the user.
- **No id**: the task comes from the current conversation. Draft it with the template in `../flow-plan/SKILL.md`, show it, and create it with `create-task` once the user approves. Then continue with that id.

Then check its position:

- **Parent**: `get-parent`.
- **Open blockers**: `open-blockers`. If any blocker is still open, or `pr-status` shows its PR is not merged into the group branch, stop and tell the user which one.
- **Children**: `list-children`. If the task itself has open children, it is a group. Ask which child to start, and suggest the first one with no open blockers.

Show the user, in a few lines, the task as you understand it (title, what it asks for, parent and blockers) and the branch you will create. Start once they confirm. In the same message, ask whether to assign the issue to them and, unless `move-status` is not used, move it to "in progress" (see "Team visibility").

## Phase 2: Branch

Use the patterns and base branch in `docs/agents/workflow.md`. Before branching off a branch, bring it up to date: `git fetch origin`, check it out, then `git pull --ff-only`. Pulling with `--ff-only` is part of this flow and needs no confirmation; if it cannot fast-forward, stop and tell the user.

Create branches with `create-branch`, so each one is linked to its task:

- **Child task**: make sure the group branch `feature/<parent-id>-<slug>` exists. If it doesn't, create it from the updated base branch with `create-branch` for the parent task, and push it. Then update the group branch and create `task/<id>-<slug>` from it with `create-branch`.
- **Standalone task**: update the base branch and create `task/<id>-<slug>` from it with `create-branch`.
- Creating these branches is part of the flow and needs no extra confirmation once the user has confirmed the task.
- If the task branch already exists, check it out and continue from where it was: look for this task's plan record, its notes and its commits to find the current phase.

**Sync Engram in.** If the Engram CLI is available and the repo has a `.engram/` folder, run `engram sync --status`. If it reports chunks that are not imported yet, run `engram sync --import`, then tell the user in one line what was imported. Skip this when **Engram sync** in `docs/agents/workflow.md` is `never`.

Tell the user, in one line, the branch name (now linked to the task) and what was imported from Engram, if anything, then go on to research. The user already confirmed the branch in Phase 1, so there is nothing to wait for here.

## Phase 3: Research (fast)

Brief a research subagent to read the issue, the parent issue's "Architecture notes" for a child task, the glossary and ADRs from `docs/agents/domain.md`, and the code the task touches. It checks the issue's "Preliminary notes" (libraries, connectors, APIs) against the code and the dependencies as they are today, and flags anything that no longer holds. It saves under `flow/<repo>/<id>/research` and returns:

- What exists today that the task builds on (as `path:line` links).
- Open questions about the task itself.
- A **size verdict**: does it fit one working session as one vertical slice? If not, a proposed split into smaller vertical slices.

Show the user the research in three to five lines: what the task builds on, the open questions, and the size verdict. Go on to planning once they agree; their comments go into the plan brief. If the size verdict says the task is small and simple, you may suggest autonomous mode in the same message (see "Autonomous mode").

**If the task is too big**, stop and offer the user, as one question:

- **(a) Keep this task small**: trim it to the first slice and create the rest as new issues for later. If this task has a parent, they become siblings under the same parent. If not, they are created as standalone issues that this one blocks.
- **(b) Turn it into a parent**: this task becomes the parent, the slices become its children (`create-child`) with blocking links (`add-blocker`), and the work continues on a group branch with the first child. Propose adding "Architecture notes" to its description (see `../flow-plan/SKILL.md`), as an edit the user approves.

Create the issues by following `../to-tickets/SKILL.md` with the overrides in `../flow-plan/SKILL.md`. For (b), rename the branch to the group pattern if no commits exist yet, otherwise ask the user how to proceed. Then continue with the chosen task.

## Phase 4: Plan (strong)

This is where the task gets its detail. The issue gives the big picture and some leads; the plan turns them into precise criteria, seams, scenarios and steps against the code as it is now. Expect it to refine or even contradict the issue: that is the point, and the description is then updated with a `## Changes` line.

Brief a plan subagent with the issue and the research key. Point it to `references/tdd.md`, `references/tests.md` and `references/mocking.md` in this skill's folder. It saves under `flow/<repo>/<id>/plan` and returns:

- Questions that remove ambiguity, each with the answer it would assume.
- Refined acceptance criteria and an "out of scope" list.
- The **seams** (public interfaces) to test, each with one line on what it catches and what it misses.
- The test scenarios, one per acceptance criterion where possible.
- An implementation outline: steps, not file-level detail.
- **Docs to touch**: the project documents this task makes stale or genuinely needs (following "Just enough docs" below) (a module's guide, the README, a user guide), each with what changes, or "none". Use the folder and rules in the **Docs** section of `docs/agents/workflow.md`; rules in the project's `AGENTS.md` or `CLAUDE.md` take precedence.
- **ADR candidates**: the architectural decisions this plan makes (a new dependency, a pattern, a boundary between modules, a data model change), each with one line on why. Only decisions that are hard to reverse, affect more than one module, or were chosen between real alternatives (see `references/adr-template.md`). Most tasks have none. It also flags any conflict with an existing ADR or with the parent's "Architecture notes", which goes to the user as a question.

Ask the user the questions one by one, assumed answer first. Then show the seams and scenarios and get the user's OK. No test is written at a seam the user has not confirmed. Save the agreed result back to the same note.

Then update the task (see "The task is the source of truth"):

1. Create the plan record (`create-record`) with the agreed seams, scenarios and steps.
2. If the refined acceptance criteria or the out-of-scope list differ from the description, propose the description edit (requirements as they now stand, the `## Changes` line, and the link to the plan record) and apply it once the user approves.

## Phase 5: Tests (strong) and the test gate

Brief a tests subagent with the plan key. It writes only test files, matching the globs in `docs/agents/workflow.md`, at the confirmed seams and following `references/tests.md` and `references/mocking.md`. It runs them and confirms each fails **for the expected reason**: missing behaviour, not a syntax, import or setup error. It saves under `flow/<repo>/<id>/tests` and returns one line per scenario with its `path:line` link and its failure reason.

Present the tests to the user. For this one message, shape the output for fast scanning. If the `i-have-adhd` skill is installed, read its SKILL.md and apply its formatting rules to this message only; otherwise follow these rules: the action first, numbered lines, no preamble, no recap.

- First line: the action, "Review the tests and reply OK to continue."
- One numbered line per scenario: what it checks, with a link to the test.
- The command to run them.

Wait for the OK. If the user wants changes, send them to the tests subagent and present again.

After the OK, give the commit command, for example:

```sh
git add <test files> && git commit -m "test(<commit-ref>): <summary>" && git push
```

This commit is the record of the approved tests. Once the user confirms it is done, save its hash under `flow/<repo>/<id>/tests`. If the user does not want this commit, copy the test files to `.scratch/flow/<id>/approved-tests/` with a `sha256sum` manifest, and use that as the record instead.

## Phase 6: Implement (fast)

Brief an implement subagent with the plan and tests keys. It writes the minimum code that makes the tests pass, following the plan's outline, and must not edit any test file. It runs the single test files and the typecheck regularly, and the full suite once at the end (commands in `docs/agents/workflow.md`). If a test seems wrong or impossible to satisfy, it stops and reports it as step 1 of "Changing an approved test", instead of working around it. It saves under `flow/<repo>/<id>/implement`.

The work can be split into several implement subagents, one after another, when the plan has clearly separate steps. Between them, tell the user in one line which step is done and which comes next. If a subagent returns a question, bring it to the user before continuing.

**Just enough docs.** Document only what the code cannot easily tell: what a module or feature is for, how to use, run or configure it, flows that cross several modules, external integrations, and non-obvious constraints or gotchas. Don't restate what reading the code gives quickly (signatures, file-by-file or line-by-line walkthroughs, generated API listings), and don't record history (that lives in the issue and the ADRs). Prefer a few lines in an existing document over a new file. When in doubt, leave it out.

**Docs.** With the tests green, update or create the documents listed in the plan's "Docs to touch" (an implement subagent, fast tier, never touching tests). Describe how things work now, not the history of the change: that lives in the issue and the ADRs. Create the docs folder only when a first document needs it, and then also its `README.md` from `../flow-setup/docs-readme-template.md`, in the language the repo's docs use, with its links adjusted if the docs folder is not `docs/`: it tells readers that these docs are deliberately short and where everything else lives. Keep its "Contents" list current whenever a document is added, renamed or removed. If the folder exists but has no such guide, propose adding it (or its "These docs are deliberately short" note to an existing index) as part of this step. If the plan said "none" but the change clearly makes a document stale, add it and tell the user.

Then check it yourself:

- `git diff <approved-tests-commit> -- <test globs>` is empty, using the latest approved-tests reference (or the files match the `.scratch` manifest). If not, stop and tell the user.
- The full suite and typecheck pass.

If the implementation departed from the plan (a step changed, was added or was dropped), propose an edit of the plan record: the affected section updated, plus a line under "Changes to the plan". Apply it once the user approves. If the requirements changed too, propose the description edit as well.

Give the commit command (`feat(<commit-ref>): …`, ending with `&& git push`) and wait, as in the hard rules.

## Phase 7: Review (2 × fast, parallel)

Read `references/code-review.md` and run its two axes as two parallel subagents:

- **Fixed point**: the merge-base of the task branch with its target (the group branch, or the base branch for a standalone task). Diff with `git diff <merge-base>...HEAD`, plus `git diff` for anything not committed.
- **Spec source**: the issue and the plan key. The spec axis also checks that the documents in "Docs to touch" match what the code now does: a stale or missing document is a finding, and so is a document that only repeats what the code already says ("Just enough docs").
- **Standards sources**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/rules/*`, `.cursor/rules/*`, `CONTRIBUTING.md`, `CODING_STANDARDS.md` and any other standards file, plus the smell baseline in `references/code-review.md`.
- **Architecture sources**, for the standards axis: the ADRs and the glossary from `docs/agents/domain.md`, the parent's "Architecture notes" for a child task, and this task's ADR candidates. Any code that contradicts an ADR is a finding that cites it ("contradicts ADR-0007"); so is a domain term used differently from the glossary.

Each saves under `flow/<repo>/<id>/review-standards` or `flow/<repo>/<id>/review-spec`. Show both reports side by side, without merging them, and ask the user which findings to fix.

If any, brief a fix subagent with those findings. It never touches test files. Re-run the checks from Phase 6, then give the commit command (`fix(<commit-ref>): …` or `refactor(<commit-ref>): …`, ending with `&& git push`). If a fix changes the plan, propose the plan record edit as in Phase 6.

## Phase 8: Final report and PR

Write the report in this shape:

1. **Detailed summary** at the top:
   - what now works, in concrete terms;
   - each acceptance criterion with ✅ or ❌;
   - test results;
   - review findings fixed and left open;
   - any deviation from the plan;
   - the documents created or updated;
   - the ADR candidates, which become ADRs in the next step.
2. **Files to review, in vertical order**: tests → entry point → logic → data. One `path:line` link per file, with one line on what changed. The user reviews the code; do not ask them to skip it.
3. **Short summary** at the end: three lines at most.

**Write the ADRs**, before the PR. For each ADR candidate from the plan that still holds after implementation and review, draft `docs/adr/<NNNN>-<title>.md` from `references/adr-template.md` (location and language as in `docs/agents/domain.md`). Show the drafts to the user and write them once they approve; if an ADR supersedes an older one, propose updating the old one's status too. Give the commit command `git add docs/adr && git commit -m "docs(<commit-ref>): add ADR-<NNNN> <title>" && git push`. Skip this step when there are no candidates.

**Sync Engram out**, before the PR. Follow **Engram sync** in `docs/agents/workflow.md`:

- `ask` (default): ask, in one line, whether to export this project's Engram memory to the repo.
- `always`: export without asking.
- `never`: skip.

To export, run `engram sync` from the repo root. It writes this project's memory to `.engram/` as compressed chunks; prompts are excluded. Then give the commit command, for example `git add .engram && git commit -m "chore(<commit-ref>): sync engram memory" && git push`, and wait, as in the hard rules. The export holds every memory of this project, not only this task's notes: remind the user of that the first time.

Then ask, in one line, whether to open the PR. If yes, create it with `open-pr`:

- `--base`: the group branch for a child task, or the base branch for a standalone task.
- Title and body in the PR language from `docs/agents/workflow.md`.
- The `closing-reference` for this task in the body, plus a link to the parent task if there is one.

Then create the summary record on the task, with the PR link. Unless `move-status` is not used, ask whether to move the task to "in review". The user reviews and merges the PR.

## After the merge

When the user says the PR is merged:

- **Child task**: list the siblings that are now unblocked and suggest the next one (`/flow-work <ref>`).
- **All children closed**: run the group architecture review below, then offer to open the group PR from `feature/<parent-id>-<slug>` to the base branch with the parent's `closing-reference`.

### Group architecture review (strong)

Before the group PR, brief a read-only subagent (strong tier) with the parent issue and its "Architecture notes", its children and their plan records, the ADRs and glossary, and the whole group diff (`git diff <base branch>...feature/<parent-id>-<slug>`). It saves under `flow/<repo>/<parent-id>/architecture-review` and returns, in at most 15 lines:

- whether the feature holds together as a whole, against the parent's "Architecture notes";
- duplication or inconsistencies between children (two helpers doing the same thing, different names for one concept, diverging patterns);
- decisions that were made but have no ADR, and code that contradicts an ADR;
- glossary drift;
- whether the feature as a whole is documented: an overview that no single child writes (what the feature does, its main pieces, how to use it). If it is missing or stale, propose it as a document to write on the group branch, with the user's OK and a `docs(<parent commit-ref>)` commit.

Show it to the user. For each finding they want addressed, propose either a new child issue under the parent (through `flow-plan`'s template, developed with `flow-work` before the group PR) or a follow-up issue for later. Missing ADRs can be written directly on the group branch, with the user's OK and a `docs(<parent commit-ref>)` commit. If the user changed the architecture along the way, propose updating the parent's "Architecture notes" (an edit, so it asks).
