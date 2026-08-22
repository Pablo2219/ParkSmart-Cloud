# Cambios cloud realizados

## Configuración y secretos

- Se completó `.env.example` con las variables requeridas por seguridad y autenticación.
- Se eliminó la necesidad de guardar credenciales reales en Terraform.
- Se agregó soporte para CA de Managed MySQL mediante variable de entorno cifrada.
- Se parametrizó CORS para separar configuración local y producción.

## Contenedores

- Se endureció el Dockerfile de API y se mantuvo el proceso con usuario sin privilegios.
- Se agregó un Dockerfile separado para el frontend.
- Se agregó configuración dinámica del frontend para apuntar a la URL pública de la API.

## Infraestructura

- Terraform ahora define proyecto, VPC, Container Registry y Managed MySQL 8.4.
- Se eliminó la regla de base de datos abierta a `0.0.0.0`.
- Se agregó usuario normal de aplicación y configuración de MySQL.
- Se agregó plantilla de App Platform con API, frontend, migración pre-deploy, health checks y alertas.

## Automatización

- Se corrigió CI para un clon limpio con secretos efímeros de prueba.
- Se agregó validación de Terraform.
- Se agregó workflow manual para publicar imágenes al registry.
- Se agregaron scripts PowerShell para provisionar, publicar, desplegar, verificar y recopilar evidencia.

## Continuidad

- Se documentaron backups, restauración, SLA, RPO y RTO.
- Se agregó prueba de carga reproducible.
- Se agregó checklist de evidencias para la defensa.
