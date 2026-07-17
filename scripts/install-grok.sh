#!/usr/bin/env bash
# Convenience: install wrap / recall / hive for Grok Build only.
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install.sh" --grok "$@"
