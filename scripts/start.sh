#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
uv sync --frozen
export AGENT_MODE="${AGENT_MODE:-fixture}"
exec uv run --no-sync selection "$@"
