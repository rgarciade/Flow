---
name: flow-setup
description: Configure the current repo for the flow skills (flow-plan, flow-work). Sets up the GitHub issue tracker docs and writes docs/agents/workflow.md with the base branch, branch naming, languages and test commands. Use when the user runs /flow-setup, or when flow-plan or flow-work find docs/agents/workflow.md missing and the user agrees to run it.
---

# flow-setup

Paths starting with `../` are relative to this skill's folder: they point at sibling skills in the same skills directory.

One-time, per-repo configuration for the flow skills. It writes the files that `flow-plan` and `flow-work` read, so those skills stay generic and each repo keeps its own rules.

Output files (all inside the repo):

- `docs/agents/issue-tracker.md`: how issues are created, read, linked and closed (GitHub, via `gh`)
- `docs/agents/domain.md`: where the glossary and ADRs live, and how to use them
- `docs/agents/workflow.md`: our flow settings (template: [workflow-template.md](workflow-template.md))
- an `## Agent skills` block in the repo's `CLAUDE.md` or `AGENTS.md`, pointing at those files

Never commit. When the files are written, give the user the exact `git add` / `git commit` command and stop.

## 1. Explore (no questions yet)

Read, don't assume:

- `git remote -v`: is it a GitHub repo? Which one? Run `gh repo view --json nameWithOwner,defaultBranchRef` to confirm access.
- Branches: `git branch -a`. Which of `dev`, `develop`, `main`, `master` exist?
- `CLAUDE.md` and `AGENTS.md` at the root. If one is a symlink to the other, the real file is the one to edit.
- `docs/agents/`: does any of it exist already? If `workflow.md` exists, this is an update: only ask about fields that are missing or that the user wants to change.
- Test and typecheck commands: `package.json` scripts, `Makefile`, `pyproject.toml`, `deno.json`, CI workflows in `.github/workflows/`.
- Where tests live (folders and file name patterns), so a glob can match every test file.
- The language of recent issues and PRs: `gh issue list --limit 5 --state all`, `gh pr list --limit 5 --state all`.

## 2. Issue tracker and domain docs (Matt Pocock's setup)

Read `../setup-matt-pocock-skills/SKILL.md` and apply its **Section A** (issue tracker) and **Section C** (domain docs), using the seed templates in that folder. Skip **Section B** (triage labels): the `triage` skill is not installed.

Default answers: GitHub for the tracker, single-context for the domain docs. Do not create `GLOSSARY.md` or ADRs.

## 3. Our questions

Ask one question at a time. Lead with the value you detected as the recommended answer, so the user can accept it in one word. Skip any question that exploration already settled beyond doubt, and say what you assumed.

1. Base branch: the branch every finished feature ends up in (for example `dev`).
2. Branch naming for groups and tasks. Default: `feature/<issue>-<slug>` for a group branch (a parent issue) and `task/<issue>-<slug>` for a task branch.
3. Language of issues and PR titles and bodies. Default: the language the repo already uses.
4. Commands: full test suite, a single test file, typecheck, lint. Mark any that don't exist as `none`.
5. Test file glob(s): the patterns that match every test file (used to check that implementation never edits approved tests).
6. Labels to apply when creating issues. Default: none.
7. Models for the two tiers: **strong** (plan, tests) and **fast** (research, implement, review, fix). Default in Claude Code: `opus` and `sonnet`. In another harness, propose its equivalents in the names it accepts, or `inherit`.

## 4. Draft, confirm, write

Show the user a draft of every file you will write or edit, including the `## Agent skills` block. Let them edit it. Then write:

- `docs/agents/issue-tracker.md` and `docs/agents/domain.md` (from Matt's templates)
- `docs/agents/workflow.md` (from [workflow-template.md](workflow-template.md))
- The `## Agent skills` block, following the file-selection rules in Matt's setup (edit the existing `CLAUDE.md` or `AGENTS.md`; never create the other one; update an existing block in place). When neither exists, recommend `AGENTS.md`: OpenCode, Codex and Cursor read it, and Claude Code loads it when the project has no `CLAUDE.md`. Add this sub-block to it:

```markdown
### Workflow

Branches, base branch, languages, model tiers and test commands for the flow skills. See `docs/agents/workflow.md`.
```

## 5. Done

Tell the user which files were written, then give the commit command, for example:

```sh
git add docs/agents AGENTS.md && git commit -m "docs: configure agent workflow"
```

Do not run it. If `flow-setup` was started from `flow-plan` or `flow-work`, go back to that skill and continue where it stopped.
