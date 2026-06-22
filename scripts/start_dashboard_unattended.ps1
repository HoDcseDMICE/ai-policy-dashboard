# Start Streamlit unattended (no new window) - suitable for Background tasks or Task Scheduler
try { Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue } catch {}
try { Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -match 'streamlit' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue } } catch {}

# Clean temp
try { Remove-Item -Path "$env:TEMP\.streamlit" -Recurse -Force -ErrorAction SilentlyContinue } catch {}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $scriptDir "..")

# Start Streamlit in background
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = "streamlit"
$startInfo.Arguments = "run app.py --server.address=127.0.0.1 --server.port=8501 --logger.level=info"
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true

$proc = [System.Diagnostics.Process]::Start($startInfo)
Start-Sleep -Seconds 1
if ($proc -and -not $proc.HasExited) { Write-Host "Streamlit started (PID: $($proc.Id))" } else { Write-Host "Failed to start Streamlit. Check permissions and PATH." }