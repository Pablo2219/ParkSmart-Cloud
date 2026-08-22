# Seguridad cloud

## Controles implementados en la configuración

### Secretos

- `.env` y `terraform.tfvars` están excluidos del repositorio.
- App Platform recibe `SECRET_KEY` y `JWT_SECRET` como variables `SECRET`.
- GitHub Actions usa Secrets para el token de DigitalOcean.
- No hay contraseñas por defecto en Terraform.

### Base de datos

- MySQL es un servicio administrado independiente de la API.
- La aplicación recibe la conexión mediante variables bindables de App Platform.
- `DATABASE_CA_CERT` habilita validación TLS contra el certificado de la base administrada.
- El usuario de aplicación no es `root` ni el usuario primario del clúster.

### Aplicación

- App Platform entrega tráfico público por HTTPS.
- `/health` se usa para liveness.
- `/health/ready` comprueba la dependencia de base de datos.
- CORS se configura por variable de entorno y no queda atado a una IP de desarrollo.

### Supply chain

- CI compila y prueba el proyecto.
- Docker se ejecuta como usuario sin privilegios en el contenedor de API.
- Las imágenes de producción se guardan en Container Registry.

## Acciones obligatorias en las cuentas

1. Rotar cualquier token que alguna vez haya sido incluido en `terraform.tfvars` o en un commit.
2. Eliminar el archivo sensible del seguimiento de Git si todavía existe.
3. Revisar Network Access de Managed MySQL y confirmar que App Platform figure como trusted source.
4. No habilitar `0.0.0.0/0` para la base de datos.
5. Activar MFA en GitHub y DigitalOcean para las cuentas del equipo que administren infraestructura.
6. Limitar permisos del token de CI al mínimo necesario cuando la plataforma permita scopes personalizados.
