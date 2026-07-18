#!/usr/bin/env bash
# Install wrap-recall-hive skills + hive CLI for local agent hosts.
#
# Product law (M17): one surface — plain wrap / recall / hive.
# Grok: ALWAYS loose skills (~/.grok/skills). Never Grok plugin + loose skills.
# Claude: user skills (plain names) OR marketplace plugin (may namespace) — pick one.
#
# Usage:
#   ./scripts/install.sh              # Grok + Claude user skills
#   ./scripts/install.sh --grok       # Grok Build only (plain /wrap /recall /hive)
#   ./scripts/install.sh --claude     # Claude Code user skills only
#   ./scripts/install.sh --home DIR   # override data home
#   ./scripts/install.sh --link       # symlink skills to this repo (dev)
#   ./scripts/install.sh --keep-plugin  # do not uninstall Grok wrap-recall-hive plugin
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WANT_GROK=0
WANT_CLAUDE=0
LINK=0
KEEP_PLUGIN=0
DATA_HOME="${WRAP_RECALL_HIVE_HOME:-$HOME/.local/share/wrap-recall-hive}"
EXPLICIT_HOST=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --grok) WANT_GROK=1; EXPLICIT_HOST=1; shift ;;
    --claude) WANT_CLAUDE=1; EXPLICIT_HOST=1; shift ;;
    --both) WANT_GROK=1; WANT_CLAUDE=1; EXPLICIT_HOST=1; shift ;;
    --link) LINK=1; shift ;;
    --keep-plugin) KEEP_PLUGIN=1; shift ;;
    --home) DATA_HOME="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,16p' "$0"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

# Default: both hosts. If only one of --grok/--claude is passed, install that one only.
if [[ "$EXPLICIT_HOST" -eq 0 ]]; then
  WANT_GROK=1
  WANT_CLAUDE=1
fi

install_data() {
  mkdir -p "$DATA_HOME"
  # Prefer root hive/ (full package); fall back to plugin copy
  if [[ -f "$REPO_ROOT/hive/hive.py" ]]; then
    rsync -a --delete "$REPO_ROOT/hive/" "$DATA_HOME/hive/"
  else
    rsync -a --delete "$REPO_ROOT/plugins/wrap-recall-hive/hive/" "$DATA_HOME/hive/"
  fi
  # Keep example registry if user has no registry yet
  if [[ ! -f "$DATA_HOME/hive/registry.json" && -f "$DATA_HOME/hive/registry.example.json" ]]; then
    echo "Note: copy $DATA_HOME/hive/registry.example.json → registry.json and edit paths for multi-seat hive."
  fi
  # Portable skills (source of truth at repo skills/)
  mkdir -p "$DATA_HOME/skills"
  rsync -a "$REPO_ROOT/skills/" "$DATA_HOME/skills/"
  # Marker for resolution
  printf '%s\n' "$DATA_HOME" > "$DATA_HOME/.install-root"
  cat > "$DATA_HOME/env.sh" <<EOF
# Source from shell profile if you want the env var set globally:
#   source $DATA_HOME/env.sh
export WRAP_RECALL_HIVE_HOME="$DATA_HOME"
EOF
  chmod +x "$DATA_HOME/hive/hive.py" 2>/dev/null || true
  echo "Data home: $DATA_HOME"
}

link_or_copy_skill() {
  local name="$1"
  local dest_root="$2"
  local src="$DATA_HOME/skills/$name"
  local dest="$dest_root/$name"
  mkdir -p "$dest_root"
  if [[ ! -d "$src" ]]; then
    echo "Missing skill source: $src" >&2
    return 1
  fi
  if [[ "$LINK" -eq 1 ]]; then
    # Link to repo skills for live edit
    src="$REPO_ROOT/skills/$name"
    rm -rf "$dest"
    ln -sfn "$src" "$dest"
    echo "  link $dest → $src"
  else
    mkdir -p "$dest"
    rsync -a "$src/" "$dest/"
    echo "  copy $dest"
  fi
}

# Grok plugins namespace skills (wrap-recall-hive:recall). Loose skills use plain names.
# Having both = double UI + confused "which recall" — product law M17 forbids it.
clear_grok_plugin_conflict() {
  if [[ "$KEEP_PLUGIN" -eq 1 ]]; then
    echo "Note: --keep-plugin set; not touching Grok plugin install."
    echo "      If wrap-recall-hive is enabled as a Grok plugin AND loose skills exist,"
    echo "      you will see BOTH /recall and /wrap-recall-hive:recall. Uninstall the plugin."
    return 0
  fi
  if ! command -v grok >/dev/null 2>&1; then
    return 0
  fi
  local listed
  listed="$(grok plugin list 2>/dev/null || true)"
  if echo "$listed" | grep -qi 'wrap-recall-hive'; then
    echo "Found Grok plugin wrap-recall-hive (namespaced skills)."
    echo "Uninstalling so only plain /wrap /recall /hive remain (M17)…"
    if grok plugin uninstall wrap-recall-hive --confirm 2>/dev/null; then
      echo "  uninstalled wrap-recall-hive plugin"
    else
      echo "  WARN: could not auto-uninstall. Run:"
      echo "    grok plugin uninstall wrap-recall-hive --confirm"
      echo "  then re-open Grok so the slash menu drops wrap-recall-hive:* entries."
    fi
  fi
}

install_grok() {
  local root="${GROK_SKILLS:-$HOME/.grok/skills}"
  echo "Grok skills → $root  (plain names: wrap, recall, hive)"
  clear_grok_plugin_conflict
  mkdir -p "$root"
  for s in wrap recall hive; do
    link_or_copy_skill "$s" "$root"
  done
  echo
  echo "  Use: wrap · recall · hive   (not wrap-recall-hive:…)"
  echo "  Pack: ~/.grok/memory/ (or whatever root your skills name)"
  echo "  Do NOT also: grok plugin install wrap-recall-hive"
}

install_claude_skills() {
  local root="${CLAUDE_SKILLS:-$HOME/.claude/skills}"
  echo "Claude user skills → $root  (plain names: wrap, recall, hive)"
  mkdir -p "$root"
  for s in wrap recall hive; do
    link_or_copy_skill "$s" "$root"
  done
  echo
  echo "  Plain-name path: user skills above."
  echo "  Marketplace path (pick ONE, not both):"
  echo "    /plugin marketplace add voardwalker-code/wrap-recall-hive"
  echo "    /plugin install wrap-recall-hive@wrap-recall-hive"
  echo "  Marketplace may show namespaced skills (wrap-recall-hive:wrap)."
  echo "  If you use the marketplace plugin, remove ~/.claude/skills/{wrap,recall,hive}"
  echo "  so you do not get two copies."
}

install_data

if [[ "$WANT_GROK" -eq 1 ]]; then install_grok; fi
if [[ "$WANT_CLAUDE" -eq 1 ]]; then install_claude_skills; fi

echo
echo "Done."
echo "  WRAP_RECALL_HIVE_HOME=$DATA_HOME"
echo "  Hive CLI: python3 $DATA_HOME/hive/hive.py --list-owners"
echo "  Optional: source $DATA_HOME/env.sh"
echo
echo "Create an own pack if needed, e.g.:"
echo "  mkdir -p ~/.agent-memory/primary/{journal,worklog}"
echo "  cp $REPO_ROOT/pack/relationship-spine.example.md ~/.agent-memory/primary/relationship-spine.md"
echo
echo "M17 — one surface: only one install path per host; skills named wrap / recall / hive."
