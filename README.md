# ParkSmart Cloud

ParkSmart es una aplicación web con API REST en FastAPI y MySQL. La versión cloud separa aplicación, frontend, base de datos, imágenes de contenedor y respaldos para reducir puntos únicos de falla y permitir una recuperación reproducible.

## Arquitectura objetivo

- **Frontend:** contenedor web desplegado en DigitalOcean App Platform.
- **API:** FastAPI en un contenedor independiente en App Platform.
- **Base de datos:** DigitalOcean Managed MySQL 8.4, separada de la aplicación.
- **Persistencia y recuperación:** backups automáticos del servicio administrado y procedimiento de restauración a un clúster nuevo.
- **Contenedores:** DigitalOcean Container Registry (DOCR).
- **Infraestructura como código:** Terraform.
- **CI:** GitHub Actions para pruebas de Python, Docker/Compose, migraciones y validación de Terraform.
- **Observabilidad:** `/health`, `/health/ready`, métricas/alertas del proveedor y evidencia reproducible.

## Inicio local

1. Copiar `.env.example` como `.env`.
2. Reemplazar todos los valores `CAMBIAR_*` por secretos locales.
3. Ejecutar:

```powershell
docker compose up -d --build --wait
docker compose ps -a
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/health/ready
```

## Despliegue cloud

La guía completa está en [`docs/cloud/DESPLIEGUE_DIGITALOCEAN.md`](docs/cloud/DESPLIEGUE_DIGITALOCEAN.md).

Los scripts se ejecutan desde la raíz del repositorio en este orden:

```powershell
.\scripts\cloud\01-preflight.ps1
.\scripts\cloud\02-provision-infrastructure.ps1
.\scripts\cloud\03-build-push-images.ps1
.\scripts\cloud\04-deploy-app.ps1
.\scripts\cloud\05-verify-cloud.ps1
.\scripts\cloud\06-collect-evidence.ps1
```

## Seguridad

- `.env`, `terraform.tfvars`, certificados privados y estados de Terraform no deben subirse a Git.
- Los secretos de App Platform se generan durante el despliegue y se envían como variables cifradas.
- Managed MySQL se adjunta a App Platform como recurso administrado y la aplicación usa TLS.
- El token de DigitalOcean debe mantenerse fuera del repositorio y cargarse únicamente en la sesión o como secret de GitHub.

## Continuidad

Consultar:

- `docs/cloud/ARQUITECTURA_CLOUD.md`
- `docs/cloud/BACKUP_Y_RECUPERACION.md`
- `docs/cloud/SEGURIDAD_CLOUD.md`
- `docs/cloud/SLA_RPO_RTO.md`
- `docs/cloud/EVIDENCIAS_PARA_DEFENSA.md`
