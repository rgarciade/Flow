# Sample tasks

Three tasks, each chosen to make `flow-work` take a different path. They are written as shapes with an example: keep the shape and adapt the names to the project you run them on. Create them with the body below, in the project's task language.

The bodies are deliberately incomplete in the places named under "What it exercises". Do not complete them.

## Task A: small and clear

**Shape.** One obvious change in one place, with nothing to decide.

**Example.**

```markdown
## What to build

Show the app's version number at the bottom of the settings screen, so users can tell support which version they run.

## Acceptance criteria

- [ ] The settings screen shows the version from the project's manifest.
- [ ] The value changes when the manifest version changes, with no other edit.
```

**What it exercises.**

- Messages keep their shape when there is little to say.
- No invented questions: a phase with nothing to ask says so and goes on.
- After research, it suggests working autonomously, as a question, and does not switch on its own.
- The closing decisions arrive together, and the state note is closed.

## Task B: more places than the issue says, and open decisions

**Shape.** A change to something the code does in several places, where the issue names only one, and at least two details are left undecided.

**Example.**

```markdown
## What to build

Durations in the list of items are shown as `65:00`. Show them as `1 h 05 min`, which is easier to read.

## Acceptance criteria

- [ ] The list shows durations in the new format.
```

Pick a value that the project really formats in more than one place (a duration, a date, a file size, a price). The issue must mention only one of them, and must not say what happens to durations under one minute or whether exports keep the old format.

**What it exercises.**

- Research finds the other places by searching the code, and brings each one as a question instead of leaving it out silently.
- The plan arrives in one message with its questions and an assumed answer for each.
- The plan's OK also covers the update of the task description, since the criteria change.
- Questions are asked together, each understandable on its own.
- Resuming in a new session (step 3 of the run): the agent reads its state note and says where the task stands.

## Task C: too big for one session

**Shape.** Several features under one title, each usable on its own.

**Example.**

```markdown
## What to build

Let users tag items: create and rename tags, assign them to items, filter the list by tag, and include the tags in the export.

## Acceptance criteria

- [ ] Tags can be created, renamed and deleted.
- [ ] An item can have several tags.
- [ ] The list can be filtered by one or more tags.
- [ ] The export includes a tags column.
```

**What it exercises.**

- Research says the task does not fit in one session, in plain words.
- It stops and offers the two ways out (keep it small, or turn it into a parent with children) as one question with a recommendation.
- It does not start planning or create any task before the user chooses.

Stop the run here.
