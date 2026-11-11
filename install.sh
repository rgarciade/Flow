#!/usr/bin/env bash
# Install the flow skills (and the vendored skills they read).
#
#   ./install.sh --project <repo-dir>   copy into <repo>/.agents/skills (every harness) and link
#                                       them from <repo>/.claude/skills (Claude Code)
#   ./install.sh --user                 link into ~/.agents/skills (OpenCode, Codex, Cursor, Gemini CLI)
#   ./install.sh --claude <config-dir>  link into a Claude Code profile, e.g. ~/.claude-personal
#   ./install.sh --dir <skills-dir>     link into any other skills folder
#
# Links point at this repo, so a `git pull` here updates them.
# Project mode uses copies so the project works on any machine and in CI; re-run it to update them.
# Nothing is overwritten unless this script installed it.
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")" && pwd)"
sources=("$repo_dir"/skills/* "$repo_dir"/vendor/mattpocock-skills/*/ "$repo_dir"/vendor/i-have-adhd/*/)

usage() {
  sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 1
}

flow_version() {
  local rev
  # A version tag when HEAD is on one (v0.1.0), the tag plus the distance from it
  # otherwise (v0.1.0-3-gb44f7bd), or the bare commit when there are no tags.
  rev="$(git -C "$repo_dir" describe --tags --always 2>/dev/null || echo "uncommitted")"
  if [[ -n "$(git -C "$repo_dir" status --porcelain 2>/dev/null)" ]]; then
    rev="$rev-dirty"
  fi
  echo "$rev"
}

refuse_default_claude_profile() {
  if [[ "$1" == "$HOME/.claude" || "$1" == "$HOME/.claude/"* ]] && [[ "${FLOW_ALLOW_DEFAULT_PROFILE:-}" != "1" ]]; then
    echo "Refusing to install into the default Claude Code profile ($1)." >&2
    echo "Set FLOW_ALLOW_DEFAULT_PROFILE=1 if that is really what you want." >&2
    exit 1
  fi
}

each_source() {
  for src in "${sources[@]}"; do
    [[ -d "$src" ]] && echo "${src%/}"
  done
}

link_into() {
  local skills_dir="$1" src name dest
  mkdir -p "$skills_dir"
  while read -r src; do
    name="$(basename "$src")"
    dest="$skills_dir/$name"
    if [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]; then
      echo "ok       $name"
    elif [[ -e "$dest" || -L "$dest" ]]; then
      echo "skipped  $name (already exists at $dest; remove it to link this repo's version)"
    else
      ln -s "$src" "$dest"
      echo "linked   $name"
    fi
  done < <(each_source)
  echo "Skills folder: $skills_dir"
}

install_project() {
  local project agents_dir claude_dir version stamp src name dest link
  local ignored=()
  project="$(cd "$1" && pwd)"
  refuse_default_claude_profile "$project"
  if [[ "$project" == "$HOME" ]]; then
    echo "Refusing to install into your home folder; pass a project folder." >&2
    exit 1
  fi
  if ! git -C "$project" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "$project is not a git repository." >&2
    exit 1
  fi

  agents_dir="$project/.agents/skills"
  claude_dir="$project/.claude/skills"
  mkdir -p "$agents_dir" "$claude_dir"
  version="$(flow_version)"
  stamp="$(date +%Y-%m-%d)"

  while read -r src; do
    name="$(basename "$src")"

    # The copy, read by OpenCode, Codex, Cursor and Gemini CLI.
    dest="$agents_dir/$name"
    if [[ -e "$dest" && ! -f "$dest/.flow-version" ]]; then
      echo "skipped  $name (exists in .agents/skills and was not installed by flow)"
      continue
    fi
    local action="copied "
    [[ -e "$dest" ]] && action="updated"
    rm -rf "$dest"
    cp -R "$src" "$dest"
    printf 'flow %s, installed %s\nsource: flow/%s\n' "$version" "$stamp" "${src#"$repo_dir"/}" > "$dest/.flow-version"

    # A relative link for Claude Code, which only reads .claude/skills.
    link="$claude_dir/$name"
    if [[ -L "$link" && "$(readlink "$link")" == "../../.agents/skills/$name" ]]; then
      :
    elif [[ -d "$link" && ! -L "$link" && -f "$link/.flow-version" ]]; then
      rm -rf "$link"
      ln -s "../../.agents/skills/$name" "$link"
    elif [[ -e "$link" || -L "$link" ]]; then
      echo "         $name: .claude/skills/$name exists and was not installed by flow; Claude Code will use that one"
    else
      ln -s "../../.agents/skills/$name" "$link"
    fi
    echo "$action  $name"
    git -C "$project" check-ignore -q "$dest" && ignored+=("$name")
  done < <(each_source)

  if ((${#ignored[@]})); then
    echo
    echo "Warning: your .gitignore ignores these skills in .agents/skills, so they will not be committed: $(IFS=,; echo "${ignored[*]}")."
    echo "Add a line like '!.agents/skills/<name>/' for each one, or teammates will miss them."
  fi

  echo
  echo "Installed flow $version into $agents_dir (linked from $claude_dir)"
  echo "Next: open your agent in $project, run flow-setup, then commit .agents/skills, .claude/skills and docs/agents."
}

case "${1:-}" in
  --project)
    [[ -n "${2:-}" ]] || usage
    install_project "$2"
    ;;
  --user)
    link_into "$HOME/.agents/skills"
    ;;
  --claude)
    [[ -n "${2:-}" ]] || usage
    [[ -d "$2" ]] || { echo "Claude Code config folder not found: $2" >&2; exit 1; }
    target="$(cd "$2" && pwd)"
    refuse_default_claude_profile "$target"
    link_into "$target/skills"
    ;;
  --dir)
    [[ -n "${2:-}" ]] || usage
    mkdir -p "$2"
    target="$(cd "$2" && pwd)"
    refuse_default_claude_profile "$target"
    link_into "$target"
    ;;
  *)
    usage
    ;;
esac
