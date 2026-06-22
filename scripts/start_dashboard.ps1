# Start dashboard safely: kill stale Streamlit/python processes, clear temp, then run Streamlit on 127.0.0.1:8501
try {
    Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
} catch {}

# Stop any python processes that include 'streamlit' on the command line
try {
    Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -match 'streamlit' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
} catch {}

# Remove Streamlit temp session files
try { Remove-Item -Path "$env:TEMP\.streamlit" -Recurse -Force -ErrorAction SilentlyContinue } catch {}
Start-Sleep -Milliseconds 500

# Change to workspace folder (assumes script is in scripts/)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $scriptDir "..")

# If a virtualenv in .venv exists, activate it (optional)
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating .venv..."
    & .\.venv\Scripts\Activate.ps1
    Start-Sleep -Milliseconds 300
}

# Start Streamlit in a new PowerShell window so it remains visible
$cmd = "streamlit run app.py --server.address=127.0.0.1 --server.port=8501 --logger.level=info"
Write-Host "Starting Streamlit: $cmd"
Start-Process powershell -ArgumentList "-NoExit","-Command",$cmd

Write-Host "Start command launched. If the app does not load, check the terminal window for errors."