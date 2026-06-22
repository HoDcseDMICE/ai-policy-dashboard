# Kill Streamlit-related processes safely
try {
    Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
} catch {}

try {
    Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -match 'streamlit' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
} catch {}

# Optionally remove temp files
try { Remove-Item -Path "$env:TEMP\.streamlit" -Recurse -Force -ErrorAction SilentlyContinue } catch {}
Write-Host "Streamlit processes and temp files cleaned."