# CareDesk Day-1 preflight (Windows PowerShell). Run from the repo root.
$fail = $false
foreach ($tool in 'claude', 'git', 'uv', 'node') {
    if (Get-Command $tool -ErrorAction SilentlyContinue) {
        $v = (& $tool --version 2>&1 | Select-Object -First 1)
        Write-Host "OK   ${tool}: $v"
    } else {
        Write-Host "FAIL $tool not found"; $fail = $true
    }
}
if ($env:ANTHROPIC_API_KEY) {
    Write-Host 'FAIL ANTHROPIC_API_KEY is set: it overrides your seat login and bills the API. Run: Remove-Item Env:ANTHROPIC_API_KEY'
    $fail = $true
} else {
    Write-Host 'OK   ANTHROPIC_API_KEY not set'
}
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host 'OK   created .env from .env.example' }
Push-Location backend
uv run --python 3.12 --group dev pytest -q *> $null
if ($LASTEXITCODE -eq 0) { Write-Host 'OK   backend tests pass' } else { Write-Host 'FAIL backend tests'; $fail = $true }
Pop-Location
if ($fail) { Write-Host 'PREFLIGHT FAILED'; exit 1 } else { Write-Host 'PREFLIGHT PASSED' }
