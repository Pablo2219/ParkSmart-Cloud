$ErrorActionPreference = "Stop"

$registry = (terraform -chdir=terraform output -raw registry_endpoint).Trim()
if (-not $registry) {
    throw "No se pudo obtener registry_endpoint. Ejecuta primero 02-provision-infrastructure.ps1"
}

Write-Host "Registry: $registry" -ForegroundColor Cyan
doctl registry login --expiry-seconds 1200

$apiImage = "$registry/parksmart-api:latest"
$webImage = "$registry/parksmart-web:latest"

docker build -t $apiImage .
docker push $apiImage

docker build -f Dockerfile.frontend -t $webImage .
docker push $webImage

Write-Host "[OK] Imagenes publicadas" -ForegroundColor Green
Write-Host $apiImage
Write-Host $webImage
