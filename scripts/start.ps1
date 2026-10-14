param([switch]$Live, [int]$Port = 8050)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$env:PYTHONUTF8 = '1'
uv sync --frozen
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
if ($Live) { $env:AGENT_MODE = 'live' } else { $env:AGENT_MODE = 'fixture' }
uv run --no-sync selection --port $Port
