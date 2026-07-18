#!/usr/bin/env bash
# Grok Build only — plain /wrap /recall /hive under ~/.grok/skills (M17).
# Uninstalls Grok wrap-recall-hive plugin if present (avoids namespaced twin UI).
# Pass-through: --link · --home DIR · --keep-plugin
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install.sh" --grok "$@"
