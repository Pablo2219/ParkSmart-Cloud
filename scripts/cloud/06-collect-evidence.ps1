$ErrorActionPreference = "Stop"

$evidence = ".\docs\cloud\evidencias"
New-Item -ItemType Directory -Force $evidence | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

terraform -chdir=terraform output | Out-File "$evidence\terraform-output-$timestamp.txt" -Encoding utf8
doctl apps list | Out-File "$evidence\apps-$timestamp.txt" -Encoding utf8
doctl databases list | Out-File "$evidence\databases-$timestamp.txt" -Encoding utf8
doctl registry get | Out-File "$evidence\registry-$timestamp.txt" -Encoding utf8

$apps = @(doctl apps list --output json | ConvertFrom-Json)
$app = $apps | Where-Object { $_.spec.name -eq "parksmart-prod" } | Select-Object -First 1
if ($app) {
    $detail = doctl apps get $app.id --output json | ConvertFrom-Json
    if ($detail -is [array]) { $detail = $detail[0] }
    $url = ($detail.live_url ?? $detail.default_ingress).TrimEnd('/')
    Invoke-WebRequest "$url/api/health" -UseBasicParsing | Select-Object StatusCode, Content | Out-File "$evidence\health-$timestamp.txt" -Encoding utf8
    Invoke-WebRequest "$url/api/health/ready" -UseBasicParsing | Select-Object StatusCode, Content | Out-File "$evidence\readiness-$timestamp.txt" -Encoding utf8
}

$dbId = (terraform -chdir=terraform output -raw database_cluster_id).Trim()
doctl databases firewalls list $dbId | Out-File "$evidence\trusted-sources-$timestamp.txt" -Encoding utf8

Write-Host "Evidencia guardada en $evidence" -ForegroundColor Green
Write-Host "Revisa los archivos antes de subirlos para confirmar que no contienen datos sensibles." -ForegroundColor Yellow
