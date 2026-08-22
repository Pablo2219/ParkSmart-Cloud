param(
    [switch]$Execute
)

$ErrorActionPreference = "Stop"
$dbId = (terraform -chdir=terraform output -raw database_cluster_id).Trim()
$timestamp = Get-Date -Format "yyyyMMddHHmm"
$name = "parksmart-restore-$timestamp"

Write-Host "Esta prueba crea un clúster MySQL temporal y puede generar costos." -ForegroundColor Yellow
Write-Host "Clúster origen: $dbId"
Write-Host "Clúster temporal: $name"

if (-not $Execute) {
    Write-Host "Modo simulación. No se creó ningún recurso." -ForegroundColor Cyan
    Write-Host "Para ejecutar conscientemente la restauración usa:"
    Write-Host ".\scripts\cloud\08-restore-drill.ps1 -Execute"
    exit 0
}

$confirmation = Read-Host "Escribe RESTAURAR para confirmar el costo temporal"
if ($confirmation -ne "RESTAURAR") {
    throw "Operación cancelada."
}

doctl databases fork $name --restore-from-cluster-id $dbId
Write-Host "Se inició el fork/restauración. Revisa su estado con: doctl databases list" -ForegroundColor Green
Write-Host "Después de recopilar evidencia y validar datos, elimina el recurso temporal desde DigitalOcean para detener costos." -ForegroundColor Yellow
