param(
    [Parameter(Mandatory=$true)]
    [string]$Url
)

$indexPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '..\public\index.html'
if (-Not (Test-Path $indexPath)) {
    Write-Error "index.html not found at $indexPath"
    exit 1
}

$content = Get-Content $indexPath -Raw
# Replace any existing deploy url (http://... or __DEPLOY_URL__)
$content = $content -replace "const deployUrl = \".*\";","const deployUrl = \"$Url\";"
Set-Content -Path $indexPath -Value $content -Force
Write-Host "Updated public/index.html deploy URL to $Url" -ForegroundColor Green
