$ErrorActionPreference = "Stop"

if (-not $env:DIGITALOCEAN_TOKEN) {
    throw "Define DIGITALOCEAN_TOKEN en esta terminal antes de ejecutar Terraform."
}

Push-Location terraform
try {
    terraform init
    terraform fmt -recursive
    terraform validate
    terraform plan -out parksmart.tfplan
    Write-Host "Revisa el plan anterior. Si es correcto, presiona ENTER para aplicar." -ForegroundColor Yellow
    Read-Host | Out-Null
    terraform apply parksmart.tfplan
    Remove-Item parksmart.tfplan -Force -ErrorAction SilentlyContinue
    terraform output
} finally {
    Pop-Location
}
