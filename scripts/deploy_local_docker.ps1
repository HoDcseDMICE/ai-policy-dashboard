# Build and run Docker image locally for the AI Policy Dashboard
param(
    [string]$ImageName = "ai-policy-dashboard:local",
    [int]$Port = 8501
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root\..\

Write-Host "Building Docker image $ImageName..."
docker build -t $ImageName .

Write-Host "Stopping any existing container on port $Port (if present)..."
# Find container using the port and stop it
$existing = docker ps --filter "publish=$Port" --format "{{.ID}}"
if ($existing) {
    docker stop $existing | Out-Null
}

Write-Host "Running container (port $Port -> 8501 inside)"
docker run -d -p $Port:8501 --name ai-policy-dashboard $ImageName

Start-Sleep -Seconds 2
$localIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -ne '127.0.0.1' -and $_.IPAddress -notlike '169.*' } | Select-Object -First 1 -ExpandProperty IPAddress)
if ($localIp) {
    Start-Process msedge "http://$localIp:$Port"
}
else {
    Start-Process msedge "http://localhost:$Port"
}

Write-Host "Dashboard should be accessible at http://localhost:$Port or http://$localIp:$Port" -ForegroundColor Green
