# Roles in another harness

Read from `SKILL.md` ("Who runs each role") when a role is set to `<manager>:<harness>` or `<manager>:other` in the **Harnesses** section of `docs/agents/workflow.md`.

For a role set to another harness:

- Read the manager's own skill or guide before using it, and launch the harness in the current worktree, passing the model and effort from the table (for Orca, `agent launch --agent <harness> --model <model> --effort <level>`; Herdr has no model or effort options of its own, so its guide, printed by `hc --skill`, says how to launch a program in a folder, and the model and effort go as that harness's own command-line options). Never create a worktree or a branch for it.
- Give it the same brief and the same hand-back contract as a subagent, written to stand on its own: it starts with none of this session's context. Add that it must not commit, push or open a PR.
- **Notes it cannot read.** That harness may not have the Engram MCP server, so it cannot read notes passed as keys. Before launching it, when notes live in Engram, export the notes this role needs to `.scratch/flow/<id>/<phase>.md` and pass those paths in the brief. Tell it to write its own result to `.scratch/flow/<id>/<role>.md`. When it finishes, you save that result to Engram under the usual key.
- Wait for it to finish, then read its note. "One writer at a time" still holds: no other role that edits files starts until it is done.
- Tell the user in one line which harness and model run the role.
- If the launch fails, the harness reports that it has no quota left, or the manager is not available, go on to the role's next harness and say so in one line. When none is usable, run the role as a subagent and say so. Never stop the task for this.
- The split is fixed by the tables: don't spread work across harnesses on your own to even out usage, because the harness gives you no usage figures.
