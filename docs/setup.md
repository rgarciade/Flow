# Setup

## Requirements

| Tool | Why | |
|---|---|---|
| An agent harness with [Agent Skills](https://agentskills.io/specification) support | Runs the skills | Claude Code, OpenCode, Codex CLI, Cursor, Gemini CLI |
| Access to your task tracker and code host | Reading and updating tasks, opening PRs | A CLI (`gh`, `glab`, `jira`, `az`…), an MCP server or an API token. For the GitHub example: [GitHub CLI](https://cli.github.com) 2.94+, `gh auth status` |
| [Engram](https://github.com/Gentleman-Programming/engram) MCP server and CLI (recommended) | Shared notes between the orchestrator and its subagents; optional memory sync through git (`.engram/`) | Without it, notes go to `.scratch/flow/` in the repo and sync is off |
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) skill (optional) | Formatting rules for the test-approval message | Without it, `flow-work` uses built-in equivalents |

Any task tracker works: `flow-setup` records how to reach it (CLI, API or MCP server). The GitHub example uses the GitHub CLI; on GitHub, native sub-issues and issue dependencies are used when available.

## 1. Install the skills

```sh
git clone <this-repo> flow && cd flow
```

| Command | Installs into | How | Read by |
|---|---|---|---|
| `./install.sh --project <repo>` | `<repo>/.agents/skills/`, with relative links from `<repo>/.claude/skills/` | Copies, with a `.flow-version` file in each skill | Every harness, for anyone who clones the repo |
| `./install.sh --user` | `~/.agents/skills/` | Symlinks to this repo | OpenCode, Codex CLI, Cursor, Gemini CLI |
| `./install.sh --claude <config-dir>` | `<config-dir>/skills/` | Symlinks to this repo | Claude Code (that profile) |
| `./install.sh --dir <skills-dir>` | Any skills folder | Symlinks to this repo | Whatever reads that folder |

- **Symlinked installs** update with a `git pull` here.
- **Project installs** are copies, so the project works on any machine and in CI. Run the command again to update them, then commit. Each skill's `.flow-version` file records the `flow` commit it came from; commit `flow` before installing, or it reads `uncommitted`.
- **Nothing is overwritten** unless this script installed it. A skill of your own with the same name is reported as `skipped`.
- The script refuses `~/.claude` (the default Claude Code profile) unless `FLOW_ALLOW_DEFAULT_PROFILE=1` is set, so a work setup is never touched by accident.

### Claude Code

Claude Code reads skills only from `.claude/skills/` (project) and `<config-dir>/skills/` (user). It does not read `.agents/skills/`, which is why project mode adds links in `.claude/skills/`.

- **Instructions file**: Claude Code reads `CLAUDE.md`. When a project has no `CLAUDE.md`, it loads `AGENTS.md` instead. The `instructionFiles` setting changes this: `claude-md-and-agents-md` loads both.
- **Subagents and models**: the `Agent` tool can pick a model per subagent, so the tiers in `docs/agents/workflow.md` apply as written (default `strong: opus`, `fast: sonnet`).
- **A separate profile**: to keep these skills away from another setup, install them with `--claude` into their own config folder and start Claude Code with `CLAUDE_CONFIG_DIR=<that folder>`. Claude Code still reads `~/.claude/CLAUDE.md` in that case; exclude it from the profile's `settings.json` with `"claudeMdExcludes": ["/Users/<you>/.claude/CLAUDE.md"]` if you don't want it.

### OpenCode

- **Skills**: reads `.agents/skills/`, `.opencode/skills/` and `.claude/skills/` in the project, and `~/.agents/skills/`, `~/.config/opencode/skills/` and `~/.claude/skills/` for the user. Both `--project` and `--user` work.
- **Instructions file**: `AGENTS.md`; `CLAUDE.md` only as a fallback.
- **Subagents and models**: launched with the `Task` tool. A model per subagent comes from agent definitions (`opencode.json` or `.opencode/agents/*.md`, with `model: provider/model-id`); otherwise subagents inherit the main model. Set the tiers in `docs/agents/workflow.md` to the names you use, or `inherit`.
- **Engram**: add it as an MCP server under `mcp` in `opencode.json`.

### Codex CLI, Cursor, Gemini CLI

- **Skills**: all three read `.agents/skills/` and `~/.agents/skills/`. Cursor also reads `.claude/skills/`.
- **Instructions file**: Codex and Cursor read `AGENTS.md`. Gemini CLI reads `GEMINI.md`; set `context.fileName` in its settings to also read `AGENTS.md`.
- **Subagents and models**: each has its own way to define subagents with a model (TOML in `.codex/agents/`, Markdown in `.cursor/agents/` or `.gemini/agents/`). Use `inherit` in the tiers if you don't define them.
- **Engram**: `codex mcp add`, Cursor's MCP settings, or `gemini mcp add`.

These harnesses follow the shared Agent Skills format, but `flow` is developed and tested on Claude Code. Expect small differences elsewhere.

## 2. Configure each repo

### Task trackers

`flow-plan` and `flow-work` never call a tracker directly. They use named operations (`view-task`, `create-task`, `create-child`, `add-blocker`, `create-record`, `edit-description`, `move-status`, `create-branch`, `open-pr`…) and look up how to do each one in the repo's `docs/agents/tracker.md`. `flow-setup` writes that file:

- **GitHub Issues**: from a ready example ([tracker-github.md](../skills/flow-setup/tracker-github.md)); it only confirms labels and status.
- **Any other tracker** (GitLab, Jira, Linear, Azure Boards…): from [tracker-template.md](../skills/flow-setup/tracker-template.md), filling each operation with the tracker's CLI, MCP server or API.
- **What the tracker can't do** gets an agreed alternative, recorded in the same file: for example a task folder in the repo (`.flow/tasks/<id>/plan.md`, linked from the task) instead of comments, a "Blocked by" line instead of native dependencies, or the task id in the branch name instead of a branch link. With no automated access at all, **manual mode** gives you the exact text to paste.
- **Shared trackers**: if several repos use the same tracker (a company Jira), the file can live in one shared place, with its path in each repo's `workflow.md`.

Tasks and pull requests can live in different places (Jira tasks, GitHub PRs): the file records both.

### Run flow-setup

Open your agent inside the project and run `flow-setup` (`/flow-setup` in Claude Code).

It explores the repo, asks its questions in batches (selectors when your agent supports them, otherwise a numbered list) with a proposed answer for each (base branch, branch names, languages, model tiers, test commands, test file globs, labels, Engram sync, status tracking, docs folder) and shows you a draft before writing:

```
docs/agents/tracker.md         how every task operation is done in your tracker
docs/agents/domain.md          where the glossary and ADRs live
docs/agents/workflow.md        base branch, branch names, languages, models, commands, Engram sync, docs
AGENTS.md or CLAUDE.md         a short "## Agent skills" block pointing at the above
<docs>/README.md               a reading guide for the project docs (only if the docs folder already exists)
```

It does not commit. Review the files and commit them yourself; the command is in its last message. To change a setting later, edit `docs/agents/workflow.md` directly, or run `flow-setup` again.

You can skip this step: `flow-plan` and `flow-work` check for `docs/agents/workflow.md` and offer to run `flow-setup` when it is missing.
