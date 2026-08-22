$ErrorActionPreference = "Stop"

Write-Host "== ParkSmart Cloud: preflight ==" -ForegroundColor Cyan

$commands = @("git", "docker", "doctl", "terraform")
foreach ($command in $commands) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Falta instalar '$command'."
    }
    Write-Host "[OK] $command disponible" -ForegroundColor Green
}

if (-not $env:DIGITALOCEAN_TOKEN) {
    Write-Warning "DIGITALOCEAN_TOKEN no existe en esta terminal. Terraform lo necesita."
    Write-Host 'Ejemplo SOLO para la sesion actual: $env:DIGITALOCEAN_TOKEN="TU_TOKEN_NUEVO"'
} else {
    Write-Host "[OK] DIGITALOCEAN_TOKEN cargado en la sesion" -ForegroundColor Green
}

try {
    doctl account get | Out-Null
    Write-Host "[OK] doctl autenticado" -ForegroundColor Green
} catch {
    Write-Warning "doctl no esta autenticado. Ejecuta: doctl auth init"
}

if (-not (Test-Path ".\terraform\terraform.tfvars")) {
    Copy-Item ".\terraform\terraform.tfvars.example" ".\terraform\terraform.tfvars"
    Write-Host "Se creo terraform/terraform.tfvars desde el ejemplo." -ForegroundColor Yellow
    Write-Host "Revisa registry_name antes de continuar; debe ser unico en tu cuenta." -ForegroundColor Yellow
}

Write-Host "Preflight terminado." -ForegroundColor Cyan
