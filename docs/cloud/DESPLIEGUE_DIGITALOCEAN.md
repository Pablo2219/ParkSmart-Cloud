# Despliegue de ParkSmart en DigitalOcean

## 1. Requisitos de la computadora

- Git
- Docker Desktop
- Terraform >= 1.6
- doctl
- PowerShell

## 2. Seguridad antes de comenzar

Crear o rotar un token de DigitalOcean y no guardarlo en ningún archivo del repositorio.

En PowerShell, para la sesión actual:

```powershell
$env:DIGITALOCEAN_TOKEN="TOKEN_NUEVO"
doctl auth init
```

No enviar el token por chat, correo, capturas ni commits.

## 3. Preparación

```powershell
.\scripts\cloud\01-preflight.ps1
```

El script crea `terraform/terraform.tfvars` a partir del ejemplo si no existe. Ese archivo está ignorado por Git.

Revisar `registry_name`, porque los nombres de registro deben ser válidos para la cuenta.

## 4. Infraestructura base

```powershell
.\scripts\cloud\02-provision-infrastructure.ps1
```

Terraform prepara:

- proyecto lógico;
- VPC;
- DigitalOcean Container Registry;
- Managed MySQL 8.4;
- base `parksmart`;
- usuario normal `parksmart_app`;
- configuración de zona horaria UTC y slow query log.

## 5. Publicar imágenes Docker

```powershell
.\scripts\cloud\03-build-push-images.ps1
```

Se publican:

- `parksmart-api:latest`
- `parksmart-web:latest`

## 6. Desplegar App Platform

```powershell
.\scripts\cloud\04-deploy-app.ps1
```

El script genera secretos criptográficamente aleatorios, crea temporalmente una especificación de App Platform, la envía a DigitalOcean y elimina el archivo temporal.

El despliegue incluye:

- servicio API;
- servicio frontend;
- job `PRE_DEPLOY` para `alembic upgrade head`;
- Managed MySQL adjuntado como base productiva;
- variables de conexión bindables;
- CA de la base cifrada;
- health/readiness checks;
- alertas de CPU, memoria, reinicios y fallos de deployment.

## 7. Verificación

Cuando App Platform indique que el deployment está activo:

```powershell
.\scripts\cloud\05-verify-cloud.ps1
```

Debe responder correctamente:

- frontend `/`
- API `/api/health`
- readiness `/api/health/ready`
- Swagger `/api/docs`

## 8. Evidencias

```powershell
.\scripts\cloud\06-collect-evidence.ps1
```

Revisar los archivos antes de agregarlos al repositorio. No guardar salidas con contraseñas, tokens o cadenas de conexión.

## 9. GitHub Actions para las imágenes

Crear en GitHub > Settings > Secrets and variables > Actions:

- `DIGITALOCEAN_ACCESS_TOKEN`

Luego ejecutar manualmente el workflow **Publicar imagenes cloud**. No usar el token como variable en texto plano dentro de YAML.

## 10. Recomendación para la exposición

Demostrar en vivo:

1. URL pública HTTPS.
2. `/api/health`.
3. `/api/health/ready`.
4. Managed MySQL separado de la API.
5. Container Registry con las dos imágenes.
6. métricas y alertas del proveedor.
7. backups disponibles.
8. procedimiento de recuperación documentado.
