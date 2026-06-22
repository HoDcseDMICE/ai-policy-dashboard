# Secure launcher for the AI Policy Dashboard
# Prompts for an access code (or accepts as first argument) and starts Streamlit + opens browser if valid.
param(
    [string]$Code
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$codeFile = Join-Path $scriptDir 'access_code.txt'
if (-Not (Test-Path $codeFile)) {
    Write-Host "Access code file not found: $codeFile" -ForegroundColor Yellow
    exit 1
}

$expected = Get-Content $codeFile -Raw
if (-not $Code) {
    $Code = Read-Host -Prompt 'Enter your dashboard access code'
}

if ($Code.Trim() -ne $expected.Trim()) {
    Write-Host 'Access code invalid. Aborting.' -ForegroundColor Red
    exit 2
}

Write-Host 'Access code verified. Launching dashboard...' -ForegroundColor Green

# Activate venv if present
$root = Join-Path $scriptDir '..'
$venvActivate = Join-Path $root 'venv\Scripts\Activate.ps1'
if (Test-Path $venvActivate) {
    Write-Host 'Activating virtual environment...'
    & $venvActivate
    Start-Sleep -Milliseconds 300
}

# Start Streamlit in a new window
$cmd = "streamlit run app.py --server.address=127.0.0.1 --server.port=8501"
Start-Process powershell -ArgumentList "-NoExit","-Command",$cmd

# Open Microsoft Edge to the dashboard (use Edge explicitly)
Start-Sleep -Seconds 2
try {
    Start-Process msedge "http://localhost:8501"
} catch {
    # Fallback to default browser if Edge isn't available
    Start-Process "http://localhost:8501"
}
