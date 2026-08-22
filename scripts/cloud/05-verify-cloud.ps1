$ErrorActionPreference = "Stop"

$apps = @(doctl apps list --output json | ConvertFrom-Json)
$app = $apps | Where-Object { $_.spec.name -eq "parksmart-prod" } | Select-Object -First 1
if (-not $app) {
    throw "No se encontro la app parksmart-prod."
}

$detail = doctl apps get $app.id --output json | ConvertFrom-Json
if ($detail -is [array]) { $detail = $detail[0] }
$url = ($detail.live_url ?? $detail.default_ingress).TrimEnd('/')

Write-Host "App ID: $($app.id)" -ForegroundColor Cyan
Write-Host "URL: $url" -ForegroundColor Cyan

$checks = @(
    @{ Name = "Frontend"; Url = "$url/" },
    @{ Name = "API liveness"; Url = "$url/api/health" },
    @{ Name = "API readiness"; Url = "$url/api/health/ready" },
    @{ Name = "Swagger"; Url = "$url/api/docs" }
)

foreach ($check in $checks) {
    try {
        $response = Invoke-WebRequest -Uri $check.Url -UseBasicParsing -TimeoutSec 20
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
            Write-Host "[OK] $($check.Name) -> $($response.StatusCode)" -ForegroundColor Green
        } else {
            Write-Host "[FALLO] $($check.Name) -> $($response.StatusCode)" -ForegroundColor Red
        }
    } catch {
        Write-Host "[FALLO] $($check.Name): $($_.Exception.Message)" -ForegroundColor Red
    }
}

$dbId = (terraform -chdir=terraform output -raw database_cluster_id).Trim()
Write-Host "`nTrusted Sources de Managed MySQL:" -ForegroundColor Cyan
doctl databases firewalls list $dbId
