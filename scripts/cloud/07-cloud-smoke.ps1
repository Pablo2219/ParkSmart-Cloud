param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd('/')
$fallos = 0

function Test-Endpoint($Nombre, $Url, $ExpectedStatus) {
    try {
        $r = Invoke-RestMethod -Uri $Url -TimeoutSec 20
        if ($r.status -ne $ExpectedStatus) {
            throw "status=$($r.status), esperado=$ExpectedStatus"
        }
        Write-Host "[OK] $Nombre" -ForegroundColor Green
    } catch {
        $script:fallos++
        Write-Host "[FALLO] $Nombre - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Test-Endpoint "Liveness cloud" "$BaseUrl/api/health" "ok"
Test-Endpoint "Readiness cloud" "$BaseUrl/api/health/ready" "ready"

try {
    $r = Invoke-WebRequest -Uri "$BaseUrl/" -UseBasicParsing -TimeoutSec 20
    if ($r.StatusCode -ne 200) { throw "HTTP $($r.StatusCode)" }
    Write-Host "[OK] Frontend cloud" -ForegroundColor Green
} catch {
    $fallos++
    Write-Host "[FALLO] Frontend cloud - $($_.Exception.Message)" -ForegroundColor Red
}

if ($fallos -gt 0) { exit 1 }
Write-Host "Resultado: smoke cloud correcto" -ForegroundColor Cyan
exit 0
