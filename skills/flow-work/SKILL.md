---
name: flow-work
description: Develop one GitHub issue end to end as an orchestrator with role subagents - research, plan, tests first with a user approval gate, implementation, two-axis review, PR. Takes an issue number, or creates the issue from the current conversation and starts right away. Never commits on its own. Use when the user runs /flow-work, or asks to pick up, start or develop a task.
---

# flow-work

Paths starting with `../` are relative to this skill's folder: they point at sibling skills in the same skills directory.

You are the **orchestrator**. You work **with the user, in the session**: you show what each phase found, ask their questions, and move on only when they agree. This is pair work with the user as the navigator, never a job that runs on its own. Bulky work goes to **role subagents**, so your own context stays small.

## Hard rules

These override anything more permissive elsewhere, including the user's general git instructions:

- **The user is in the loop at every phase.** End each phase by showing its result in a few lines and saying what comes next. Don't chain phases silently. The only exception is autonomous mode, and only when the user asks for it (see "Autonomous mode").
- **Decisions belong to the user.** Anything the issue and the agreed plan don't settle (a design choice, a dependency, a trade-off, a scope question) goes to the user as a question with your recommendation. Never decide it for them.
- **Never commit on your own.** At each commit point, give the user the exact command and wait. Run it only if the user explicitly tells you to.
- **Never merge PRs.** The user reviews and merges every PR on GitHub.
- **Never modify approved tests.** After the test gate, the test files are frozen. If a test looks wrong, stop and tell the user why.
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

- The repo path, issue number and current branch.
- Pointers, not pasted content: the issue (`gh issue view <n>`), `docs/agents/*.md`, and the notes from earlier phases.
- The rule: read only what the role needs; do not spawn agents; artifacts (code, comments, test names) in English unless the repo already uses another language.
- The rule: subagents cannot talk to the user. When something is not settled by the issue, the plan or the brief, stop and return it as a question, with options and a recommendation. Do not guess.
- The hand-back contract: **save the full result as a note under the key given, then return at most 15 lines**: outcome, files touched (as `path:line` links), the note key, and any blocker or question for the user. No pasted logs or file contents.

**Notes.** Keys follow `flow/<repo>/<issue>/<phase>`, for example `flow/my-app/42/research`.

- With the Engram MCP server available: save with `mem_save` (topic key = the note key), read with `mem_search` and `mem_get_observation`, update with `mem_update`.
- Without it: write the note to `.scratch/flow/<issue>/<phase>.md` in the repo and pass that path instead. Make sure `.scratch/` is git-ignored.

Notes are working memory for this session's subagents. The durable record lives on the issue.

## The issue is the source of truth

Anyone must be able to understand the task from the GitHub issue alone, without the notes. Keep the issue lean: **at most two comments per task from this flow** (the plan comment and the closing comment). When something changes, **edit** what exists instead of posting something new.

**Permissions:**

- **Creating** the plan comment or the closing comment needs no confirmation.
- **Editing** the description or a comment, and **deleting** anything, always need the user's OK: show the exact change first and wait.

**The description holds the _what_**: what to build, acceptance criteria, out of scope. When the agreed requirements change, propose an edit of the description (never a new comment) with:

- the requirements rewritten as they now stand, and
- at the bottom, a `## Changes` section (heading in the issue language) with one dated line per change: what changed and why. Keep earlier lines.

Apply it with `gh issue edit <n> --body-file <file>` once the user approves.

**One plan comment holds the _how_**: a short implementation summary, created at the end of Phase 4. Never post a second plan comment: if the plan changes, propose an edit of this one. Find it by its hidden marker:

```sh
gh api repos/{owner}/{repo}/issues/<n>/comments --jq '.[] | select(.body | contains("<!-- flow:plan -->")) | .id'
```

Create it with `gh issue comment <n> --body-file <file>`. Edit it, after the user's OK, with `gh api --method PATCH repos/{owner}/{repo}/issues/comments/<id> -F body=@<file>`.

**The closing comment** is posted once, when the PR is opened (Phase 8), with the marker `<!-- flow:summary -->`. If it already exists (for example, the PR was reopened), propose an edit instead.

To link the description to the plan comment, include `Implementation notes: <comment URL>` in the next description edit the user approves. Don't edit the description only to add this link.

Write both comments in the issue language from `docs/agents/workflow.md`; translate the headings and the note text too.

Plan comment template (10 to 15 lines below the header):

```markdown
<!-- flow:plan -->
> [!NOTE]
> **Implementation notes**: how this task is being built. The requirements are in the issue description; flow-work updates this comment when the plan changes.
> Last update: <YYYY-MM-DD> · branch `<task branch>`

### Seams under test
- `<public interface>`: what it catches

### Scenarios
1. <one line per scenario>

### Steps
1. <implementation outline, no file-level detail>

### Changes to the plan
- <YYYY-MM-DD>: <what changed and why> (omit the section until something changes)
```

Closing comment template:

```markdown
<!-- flow:summary -->
> [!NOTE]
> **Implementation summary**: what was built for this task. PR: #<pr>

- **Works now**: <one or two lines>
- **Acceptance criteria**: <n>/<n> ✅ (list any ❌)
- **Deviations from the plan**: <none, or one line each>
- **Open review findings**: <none, or one line each>
```

## Team visibility

Issue-driven work is visible while it happens, not only when the PR arrives. Anyone looking at the issue can see who is on it, in which branch, at which stage, and every commit so far.

- **Linked branch.** Create task branches with `gh issue develop` (Phase 2). The branch then appears in the issue's "Development" panel from the first minute.
- **Pushed commits.** Every commit command you give the user ends with `git push`, so each approved step shows up on the linked branch.
- **The plan comment** tells the team how the task is being built (see "The issue is the source of truth").
- **Assignment.** When the user confirms the task (Phase 1), propose assigning the issue to them (`gh issue edit <n> --add-assignee @me`) and do it after their OK. This does not depend on status tracking.
- **Status moves.** If **Status tracking** in `docs/agents/workflow.md` is not `none`, propose moving the issue's status at these points, and move it only after the user's OK (one line, it can share a message with the phase's other question):

  | When | Move to |
  |---|---|
  | The user confirms the task (Phase 1) | in progress |
  | The PR is opened (Phase 8) | in review |
  | The PR is merged | done (usually automatic through `Closes #<n>`; only propose it if it did not happen) |

  How to move it, depending on **Status tracking**:

  - `labels`: `gh issue edit <n> --remove-label "<old>" --add-label "<new>"`, with the label names in `workflow.md`.
  - `project`: `gh project item-edit --owner <owner> <project-number> --url <issue-url> --field "<field>" --value "<option>"`, with the project, field and option names in `workflow.md`. If the issue is not in the project yet, add it first with `gh project item-add`.

## Autonomous mode

For a task that is not complex, the user can ask you to work autonomously ("work on your own", "autonomous mode"). You may also suggest it after research, when the size verdict says the task is small. Never switch to it without the user's explicit yes.

In autonomous mode, chain the phases without stopping for routine confirmations:

- **Skip:** showing each phase's result and waiting, the research summary, the seams confirmation, the test gate and the progress lines. Take the plan's assumed answers when they are clearly safe.
- **Still stop for** what really needs the programmer:
  - a decision the issue and the plan don't settle, where a wrong guess would cost real rework;
  - a test that looks wrong, or a check you cannot make pass;
  - a task that turns out bigger than it looked;
  - anything that leaves the machine or changes shared state: commits, pushes, status moves, issue edits, the PR.
- **Tests stay frozen.** With no test gate, record the tests with the `.scratch/flow/<n>/approved-tests/` manifest right after writing them, and check them against it as usual.
- **Commits come at the end.** Instead of a commit command per phase, give the user the `test`, `feat` and `fix`/`refactor` commands (and `chore` for an Engram export) together with the final report, each ending with `&& git push`.
- **The final report is never skipped.** It also lists every assumption you made on the user's behalf, so they can check them.

The user can leave autonomous mode at any moment ("stop", "back to pair mode"). Go back to stopping at every phase from there.

## Phase 0: Preflight

1. Read `docs/agents/workflow.md`. If it does not exist, tell the user and ask, in one line, whether to run `flow-setup` now. If yes, read `../flow-setup/SKILL.md`, follow it, then come back here. If no, stop. If a field this skill needs is missing, ask only for that field.
2. Read `docs/agents/issue-tracker.md`.
3. Run `git status`. If there are uncommitted changes that are not part of this task, stop and ask the user what to do with them.

## Phase 1: The task

- **Issue number given** (`#42`, `42` or a URL): read it with `gh issue view <n> --json number,title,body,labels,comments,state`. State its title back to the user.
- **No number**: the task comes from the current conversation. Draft the issue with the template in `../flow-plan/SKILL.md`, show it, and create it with `gh issue create` once the user approves. Then continue with that number.

Then check its position:

- **Parent**: `gh api repos/{owner}/{repo}/issues/<n>/parent` (404 means no parent).
- **Open blockers**: `gh api repos/{owner}/{repo}/issues/<n> --jq .issue_dependencies_summary`. If any blocker is still open, or its PR is not merged into the group branch, stop and tell the user which one.
- **Children**: if the issue itself has open sub-issues, it is a group. Ask which child to start, and suggest the first one with no open blockers.

Show the user, in a few lines, the task as you understand it (title, what it asks for, parent and blockers) and the branch you will create. Start once they confirm. In the same message, ask whether to assign the issue to them and, if status tracking is on, move it to "in progress" (see "Team visibility").

## Phase 2: Branch

Use the patterns and base branch in `docs/agents/workflow.md`. Before branching off a branch, bring it up to date: `git fetch origin`, check it out, then `git pull --ff-only`. Pulling with `--ff-only` is part of this flow and needs no confirmation; if it cannot fast-forward, stop and tell the user.

Create branches with `gh issue develop`, so each one is linked to its issue and visible in the issue's "Development" panel:

- **Child task**: make sure the group branch `feature/<parent>-<slug>` exists. If it doesn't, create it linked to the parent issue: `gh issue develop <parent> --name feature/<parent>-<slug> --base <base branch>`. Then update the group branch and create the task branch: `gh issue develop <n> --name task/<n>-<slug> --base feature/<parent>-<slug> --checkout`.
- **Standalone task**: update the base branch and run `gh issue develop <n> --name task/<n>-<slug> --base <base branch> --checkout`.
- `gh issue develop` creates the branch on GitHub and checks it out locally; this is part of the flow and needs no extra confirmation once the user has confirmed the task.
- If the task branch already exists, check it out and continue from where it was: look for this issue's plan comment, its notes and its commits to find the current phase.

**Sync Engram in.** If the Engram CLI is available and the repo has a `.engram/` folder, run `engram sync --status`. If it reports chunks that are not imported yet, run `engram sync --import`, then tell the user in one line what was imported. Skip this when **Engram sync** in `docs/agents/workflow.md` is `never`.

Tell the user, in one line, the branch name (now linked to the issue) and what was imported from Engram, if anything, then go on to research. The user already confirmed the branch in Phase 1, so there is nothing to wait for here.

## Phase 3: Research (fast)

Brief a research subagent to read the issue, the glossary and ADRs from `docs/agents/domain.md`, and the code the task touches. It checks the issue's "Preliminary notes" (libraries, connectors, APIs) against the code and the dependencies as they are today, and flags anything that no longer holds. It saves under `flow/<repo>/<n>/research` and returns:

- What exists today that the task builds on (as `path:line` links).
- Open questions about the task itself.
- A **size verdict**: does it fit one working session as one vertical slice? If not, a proposed split into smaller vertical slices.

Show the user the research in three to five lines: what the task builds on, the open questions, and the size verdict. Go on to planning once they agree; their comments go into the plan brief. If the size verdict says the task is small and simple, you may suggest autonomous mode in the same message (see "Autonomous mode").

**If the task is too big**, stop and offer the user, as one question:

- **(a) Keep this task small**: trim it to the first slice and create the rest as new issues for later. If this task has a parent, they become siblings under the same parent. If not, they are created as standalone issues that this one blocks.
- **(b) Turn it into a parent**: this issue becomes the parent, the slices become its sub-issues with native blocking links, and the work continues on a group branch with the first child.

Create the issues by following `../to-tickets/SKILL.md` with the overrides in `../flow-plan/SKILL.md`. For (b), rename the branch to the group pattern if no commits exist yet, otherwise ask the user how to proceed. Then continue with the chosen task.

## Phase 4: Plan (strong)

This is where the task gets its detail. The issue gives the big picture and some leads; the plan turns them into precise criteria, seams, scenarios and steps against the code as it is now. Expect it to refine or even contradict the issue: that is the point, and the description is then updated with a `## Changes` line.

Brief a plan subagent with the issue and the research key. Point it to `references/tdd.md`, `references/tests.md` and `references/mocking.md` in this skill's folder. It saves under `flow/<repo>/<n>/plan` and returns:

- Questions that remove ambiguity, each with the answer it would assume.
- Refined acceptance criteria and an "out of scope" list.
- The **seams** (public interfaces) to test, each with one line on what it catches and what it misses.
- The test scenarios, one per acceptance criterion where possible.
- An implementation outline: steps, not file-level detail.

Ask the user the questions one by one, assumed answer first. Then show the seams and scenarios and get the user's OK. No test is written at a seam the user has not confirmed. Save the agreed result back to the same note.

Then update the issue (see "The issue is the source of truth"):

1. Post the plan comment with the agreed seams, scenarios and steps.
2. If the refined acceptance criteria or the out-of-scope list differ from the description, propose the description edit (requirements as they now stand, the `## Changes` line, and the link to the plan comment) and apply it once the user approves.

## Phase 5: Tests (strong) and the test gate

Brief a tests subagent with the plan key. It writes only test files, matching the globs in `docs/agents/workflow.md`, at the confirmed seams and following `references/tests.md` and `references/mocking.md`. It runs them and confirms each fails **for the expected reason**: missing behaviour, not a syntax, import or setup error. It saves under `flow/<repo>/<n>/tests` and returns one line per scenario with its `path:line` link and its failure reason.

Present the tests to the user. For this one message, shape the output for fast scanning. If the `i-have-adhd` skill is installed, read its SKILL.md and apply its formatting rules to this message only; otherwise follow these rules: the action first, numbered lines, no preamble, no recap.

- First line: the action, "Review the tests and reply OK to continue."
- One numbered line per scenario: what it checks, with a link to the test.
- The command to run them.

Wait for the OK. If the user wants changes, send them to the tests subagent and present again.

After the OK, give the commit command, for example:

```sh
git add <test files> && git commit -m "test(#42): <summary>" && git push
```

This commit is the record of the approved tests. Once the user confirms it is done, save its hash under `flow/<repo>/<n>/tests`. If the user does not want this commit, copy the test files to `.scratch/flow/<n>/approved-tests/` with a `sha256sum` manifest, and use that as the record instead.

## Phase 6: Implement (fast)

Brief an implement subagent with the plan and tests keys. It writes the minimum code that makes the tests pass, following the plan's outline, and must not edit any test file. It runs the single test files and the typecheck regularly, and the full suite once at the end (commands in `docs/agents/workflow.md`). If a test seems wrong or impossible to satisfy, it stops and reports why instead of working around it. It saves under `flow/<repo>/<n>/implement`.

The work can be split into several implement subagents, one after another, when the plan has clearly separate steps. Between them, tell the user in one line which step is done and which comes next. If a subagent returns a question, bring it to the user before continuing.

Then check it yourself:

- `git diff <approved-tests-commit> -- <test globs>` is empty (or the files match the `.scratch` manifest). If not, stop and tell the user.
- The full suite and typecheck pass.

If the implementation departed from the plan (a step changed, was added or was dropped), propose an edit of the plan comment: the affected section updated, plus a line under "Changes to the plan". Apply it once the user approves. If the requirements changed too, propose the description edit as well.

Give the commit command (`feat(#n): …`, ending with `&& git push`) and wait, as in the hard rules.

## Phase 7: Review (2 × fast, parallel)

Read `references/code-review.md` and run its two axes as two parallel subagents:

- **Fixed point**: the merge-base of the task branch with its target (the group branch, or the base branch for a standalone task). Diff with `git diff <merge-base>...HEAD`, plus `git diff` for anything not committed.
- **Spec source**: the issue and the plan key.
- **Standards sources**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/rules/*`, `.cursor/rules/*`, `CONTRIBUTING.md`, `CODING_STANDARDS.md` and any other standards file, plus the smell baseline in `references/code-review.md`.

Each saves under `flow/<repo>/<n>/review-standards` or `flow/<repo>/<n>/review-spec`. Show both reports side by side, without merging them, and ask the user which findings to fix.

If any, brief a fix subagent with those findings. It never touches test files. Re-run the checks from Phase 6, then give the commit command (`fix(#n): …` or `refactor(#n): …`, ending with `&& git push`). If a fix changes the plan, propose the plan comment edit as in Phase 6.

## Phase 8: Final report and PR

Write the report in this shape:

1. **Detailed summary** at the top:
   - what now works, in concrete terms;
   - each acceptance criterion with ✅ or ❌;
   - test results;
   - review findings fixed and left open;
   - any deviation from the plan.
2. **Files to review, in vertical order**: tests → entry point → logic → data. One `path:line` link per file, with one line on what changed. The user reviews the code; do not ask them to skip it.
3. **Short summary** at the end: three lines at most.

**Sync Engram out**, before the PR. Follow **Engram sync** in `docs/agents/workflow.md`:

- `ask` (default): ask, in one line, whether to export this project's Engram memory to the repo.
- `always`: export without asking.
- `never`: skip.

To export, run `engram sync` from the repo root. It writes this project's memory to `.engram/` as compressed chunks; prompts are excluded. Then give the commit command, for example `git add .engram && git commit -m "chore(#42): sync engram memory" && git push`, and wait, as in the hard rules. The export holds every memory of this project, not only this task's notes: remind the user of that the first time.

Then ask, in one line, whether to open the PR. If yes, create it with `gh pr create`:

- `--base`: the group branch for a child task, or the base branch for a standalone task.
- Title and body in the PR language from `docs/agents/workflow.md`.
- `Closes #<n>` in the body, plus a link to the parent issue if there is one.

Then post the closing comment on the issue, with the PR number. If status tracking is on, ask whether to move the issue to "in review". The user reviews and merges the PR.

## After the merge

When the user says the PR is merged:

- **Child task**: list the siblings that are now unblocked and suggest the next one (`/flow-work #<n>`).
- **All children closed**: offer to open the group PR from `feature/<parent>-<slug>` to the base branch with `Closes #<parent>`.
