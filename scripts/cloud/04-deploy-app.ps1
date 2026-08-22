$ErrorActionPreference = "Stop"

$templatePath = ".\.do\app.template.yaml"
$tempPath = ".\.do\app.generated.yaml"

$dbCluster = (terraform -chdir=terraform output -raw database_cluster_name).Trim()
$dbName = (terraform -chdir=terraform output -raw database_name).Trim()
$dbUser = (terraform -chdir=terraform output -raw database_user).Trim()

if (-not $dbCluster -or -not $dbName -or -not $dbUser) {
    throw "Faltan outputs de Terraform. Provisiona primero la infraestructura."
}

function New-RandomSecret {
    $bytes = New-Object byte[] 48
    [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
    return [Convert]::ToBase64String($bytes)
}

$secretKey = New-RandomSecret
$jwtSecret = New-RandomSecret

$content = Get-Content $templatePath -Raw
$content = $content.Replace("__DATABASE_CLUSTER_NAME__", $dbCluster)
$content = $content.Replace("__DATABASE_NAME__", $dbName)
$content = $content.Replace("__DATABASE_USER__", $dbUser)
$content = $content.Replace("__SECRET_KEY__", $secretKey)
$content = $content.Replace("__JWT_SECRET__", $jwtSecret)

[System.IO.File]::WriteAllText(
    (Join-Path (Get-Location) $tempPath),
    $content,
    [System.Text.UTF8Encoding]::new($false)
)

try {
    $apps = @(doctl apps list --output json | ConvertFrom-Json)
    $existing = $apps | Where-Object { $_.spec.name -eq "parksmart-prod" } | Select-Object -First 1

    if ($existing) {
        Write-Host "Actualizando App Platform: $($existing.id)" -ForegroundColor Cyan
        doctl apps update $existing.id --spec $tempPath
    } else {
        Write-Host "Creando ParkSmart en App Platform..." -ForegroundColor Cyan
        doctl apps create --spec $tempPath
    }
} finally {
    Remove-Item $tempPath -Force -ErrorAction SilentlyContinue
    Remove-Variable secretKey, jwtSecret, content -ErrorAction SilentlyContinue
}

Write-Host "La especificacion temporal con secretos fue eliminada." -ForegroundColor Green
Write-Host "Espera a que el deployment quede ACTIVE antes de ejecutar 05-verify-cloud.ps1." -ForegroundColor Yellow
