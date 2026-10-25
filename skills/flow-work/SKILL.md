---
name: flow-work
description: Develop one GitHub issue end to end as an orchestrator with role subagents - research, plan, tests first with a user approval gate, implementation, two-axis review, PR. Takes an issue number, or creates the issue from the current conversation and starts right away. Never commits on its own. Use when the user runs /flow-work, or asks to pick up, start or develop a task.
---

# flow-work

Paths starting with `../` are relative to this skill's folder: they point at sibling skills in the same skills directory.

You are the **orchestrator**. You talk to the user, keep the pace and decide what happens next. Bulky work goes to **role subagents**, so your own context stays small.

## Hard rules

These override anything more permissive elsewhere, including the user's general git instructions:

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
- The hand-back contract: **save the full result as a note under the key given, then return at most 15 lines**: outcome, files touched (as `path:line` links), the note key, and any blocker or question for the user. No pasted logs or file contents.

**Notes.** Keys follow `flow/<repo>/<issue>/<phase>`, for example `flow/my-app/42/research`.

- With the Engram MCP server available: save with `mem_save` (topic key = the note key), read with `mem_search` and `mem_get_observation`, update with `mem_update`.
- Without it: write the note to `.scratch/flow/<issue>/<phase>.md` in the repo and pass that path instead. Make sure `.scratch/` is git-ignored.

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

## Phase 2: Branch

Use the patterns and base branch in `docs/agents/workflow.md`:

- **Child task**: make sure the group branch `feature/<parent>-<slug>` exists. If it doesn't, create it from the up-to-date base branch and push it. Then create `task/<n>-<slug>` from the up-to-date group branch.
- **Standalone task**: create `task/<n>-<slug>` from the up-to-date base branch.
- If the task branch already exists, check it out and continue from where it was: look for this issue's notes and its commits to find the current phase.

Tell the user the branch name in one line.

## Phase 3: Research (fast)

Brief a research subagent to read the issue, the glossary and ADRs from `docs/agents/domain.md`, and the code the task touches. It saves under `flow/<repo>/<n>/research` and returns:

- What exists today that the task builds on (as `path:line` links).
- Open questions about the task itself.
- A **size verdict**: does it fit one working session as one vertical slice? If not, a proposed split into smaller vertical slices.

**If the task is too big**, stop and offer the user, as one question:

- **(a) Keep this task small**: trim it to the first slice and create the rest as new issues for later. If this task has a parent, they become siblings under the same parent. If not, they are created as standalone issues that this one blocks.
- **(b) Turn it into a parent**: this issue becomes the parent, the slices become its sub-issues with native blocking links, and the work continues on a group branch with the first child.

Create the issues by following `../to-tickets/SKILL.md` with the overrides in `../flow-plan/SKILL.md`. For (b), rename the branch to the group pattern if no commits exist yet, otherwise ask the user how to proceed. Then continue with the chosen task.

## Phase 4: Plan (strong)

Brief a plan subagent with the issue and the research key. Point it to `references/tdd.md`, `references/tests.md` and `references/mocking.md` in this skill's folder. It saves under `flow/<repo>/<n>/plan` and returns:

- Questions that remove ambiguity, each with the answer it would assume.
- Refined acceptance criteria and an "out of scope" list.
- The **seams** (public interfaces) to test, each with one line on what it catches and what it misses.
- The test scenarios, one per acceptance criterion where possible.
- An implementation outline: steps, not file-level detail.

Ask the user the questions one by one, assumed answer first. Then show the seams and scenarios and get the user's OK. No test is written at a seam the user has not confirmed. Save the agreed result back to the same note.

If the refined acceptance criteria differ from the issue, offer to update the issue body.

## Phase 5: Tests (strong) and the test gate

Brief a tests subagent with the plan key. It writes only test files, matching the globs in `docs/agents/workflow.md`, at the confirmed seams and following `references/tests.md` and `references/mocking.md`. It runs them and confirms each fails **for the expected reason**: missing behaviour, not a syntax, import or setup error. It saves under `flow/<repo>/<n>/tests` and returns one line per scenario with its `path:line` link and its failure reason.

Present the tests to the user. For this one message, shape the output for fast scanning. If the `i-have-adhd` skill is installed, read its SKILL.md and apply its formatting rules to this message only; otherwise follow these rules: the action first, numbered lines, no preamble, no recap.

- First line: the action, "Review the tests and reply OK to continue."
- One numbered line per scenario: what it checks, with a link to the test.
- The command to run them.

Wait for the OK. If the user wants changes, send them to the tests subagent and present again.

After the OK, give the commit command, for example:

```sh
git add <test files> && git commit -m "test(#42): <summary>"
```

This commit is the record of the approved tests. Once the user confirms it is done, save its hash under `flow/<repo>/<n>/tests`. If the user does not want this commit, copy the test files to `.scratch/flow/<n>/approved-tests/` with a `sha256sum` manifest, and use that as the record instead.

## Phase 6: Implement (fast)

Brief an implement subagent with the plan and tests keys. It writes the minimum code that makes the tests pass, following the plan's outline, and must not edit any test file. It runs the single test files and the typecheck regularly, and the full suite once at the end (commands in `docs/agents/workflow.md`). If a test seems wrong or impossible to satisfy, it stops and reports why instead of working around it. It saves under `flow/<repo>/<n>/implement`.

The work can be split into several implement subagents, one after another, when the plan has clearly separate steps.

Then check it yourself:

- `git diff <approved-tests-commit> -- <test globs>` is empty (or the files match the `.scratch` manifest). If not, stop and tell the user.
- The full suite and typecheck pass.

Give the commit command (`feat(#n): …`) and wait, as in the hard rules.

## Phase 7: Review (2 × fast, parallel)

Read `references/code-review.md` and run its two axes as two parallel subagents:

- **Fixed point**: the merge-base of the task branch with its target (the group branch, or the base branch for a standalone task). Diff with `git diff <merge-base>...HEAD`, plus `git diff` for anything not committed.
- **Spec source**: the issue and the plan key.
- **Standards sources**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/rules/*`, `.cursor/rules/*`, `CONTRIBUTING.md`, `CODING_STANDARDS.md` and any other standards file, plus the smell baseline in `references/code-review.md`.

Each saves under `flow/<repo>/<n>/review-standards` or `flow/<repo>/<n>/review-spec`. Show both reports side by side, without merging them, and ask the user which findings to fix.

If any, brief a fix subagent with those findings. It never touches test files. Re-run the checks from Phase 6, then give the commit command (`fix(#n): …` or `refactor(#n): …`).

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

Then ask, in one line, whether to open the PR. If yes, create it with `gh pr create`:

- `--base`: the group branch for a child task, or the base branch for a standalone task.
- Title and body in the PR language from `docs/agents/workflow.md`.
- `Closes #<n>` in the body, plus a link to the parent issue if there is one.

The user reviews and merges it.

## After the merge

When the user says the PR is merged:

- **Child task**: list the siblings that are now unblocked and suggest the next one (`/flow-work #<n>`).
- **All children closed**: offer to open the group PR from `feature/<parent>-<slug>` to the base branch with `Closes #<parent>`.
