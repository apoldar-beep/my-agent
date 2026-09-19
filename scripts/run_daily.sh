#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Wymusza kalendarzowy dzień Europe/Warsaw w nazwie pliku podsumowania
# i w logach, niezależnie od strefy systemowej serwera i od tego, czy
# cron respektuje CRON_TZ z crontabu.
export TZ="Europe/Warsaw"

if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Uruchamiam inbox-agent"
python -m inbox_agent.main
echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Zakończono"
