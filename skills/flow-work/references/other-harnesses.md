# Roles in another harness

Read from `SKILL.md` ("Who runs each role") when a role is set to `<manager>:<harness>` or `<manager>:other` in the **Harnesses** section of `docs/agents/workflow.md`.

For a role set to another harness:

- Read the manager's own skill or guide before using it, and launch the harness in the current worktree, passing the model and effort from the table (for Orca, `agent launch --agent <harness> --model <model> --effort <level>`; Herdr has no model or effort options of its own, so its guide, printed by `hc --skill`, says how to launch a program in a folder, and the model and effort go as that harness's own command-line options). Never create a worktree or a branch for it.
- Give it the same brief and the same hand-back contract as a subagent, written to stand on its own: it starts with none of this session's context. Add that it must not commit, push or open a PR.
- **Notes it cannot read.** That harness may not have the Engram MCP server, so it cannot read notes passed as keys. Before launching it, when notes live in Engram, export the notes this role needs to `.scratch/flow/<id>/<phase>.md` and pass those paths in the brief. Tell it to write its own result to `.scratch/flow/<id>/<role>.md`. When it finishes, you save that result to Engram under the usual key.
- **It will not tell you it is done.** A harness launched through a manager is an interactive session: when it finishes, it prints its answer and sits idle. It does not exit and does not notify you. You must wait for it actively:
  - Launch it so it can be waited on: a terminal, not a chat (for Orca, `--surface terminal`), and keep the handle the launch returns (`launch.outcome.handle`).
  - End its brief with two fixed instructions: write the full result to the note file you named, then print a last line `FLOW-<ROLE>-DONE` (for example `FLOW-REVIEW-DONE`).
  - Wait in a loop with the manager's wait command and a timeout (for Orca, `terminal wait --terminal <handle> --for tui-idle --timeout-ms 600000 --json`). Don't end your turn while it runs, unless your harness re-invokes you when a background command finishes.
  - Each time it goes idle, read its screen (for Orca, `terminal read --terminal <handle> --screen --json`). With the done line and the note file present, it is finished. Idle without the done line means it is waiting for something (a question, a permission prompt, an error): bring it to the user, never answer it yourself.
  - After about 45 minutes with no done line, tell the user what you see on its screen and ask whether to keep waiting.
  - When it is done, read its note, then close only its own terminal (for Orca, `terminal close --terminal <handle> --json`; never `--all`) and tell the user in one line. You launched it, so you close it: never leave it running for the user to clean up.
  - Another manager (Herdr): use the wait, read and close commands its guide gives (`hc --skill`). If it has no way to wait for idle, check every minute whether the note file exists and ends with the done line.
- "One writer at a time" still holds: no other role that edits files starts until it is done.
- Tell the user in one line which harness and model run the role.
- If the launch fails, the harness reports that it has no quota left, or the manager is not available, go on to the role's next harness and say so in one line. When none is usable, run the role as a subagent and say so. Never stop the task for this.
- **A launch the permission system denies is not a failure to work around.** Your own harness may block the launch (for example, Claude Code's auto mode can deny starting another agent with a prompt). Never retry it with a reworded or split command, and never launch it some other way. Tell the user in one line that the launch was blocked and by what, run the role on its next harness or as a subagent, and say how they can allow it next time: approving the command themselves, or the allow rule or mode their harness offers. Don't try again for the rest of the task unless the user says it is now allowed.
- The split is fixed by the tables: don't spread work across harnesses on your own to even out usage, because the harness gives you no usage figures.
