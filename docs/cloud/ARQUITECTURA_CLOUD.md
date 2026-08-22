# Arquitectura cloud de ParkSmart

## Objetivo

Separar los componentes críticos de ParkSmart para evitar que una falla única afecte simultáneamente al código, la aplicación, la base de datos y los respaldos.

## Componentes

```text
Usuarios
   |
   | HTTPS
   v
Frontend - App Platform
   |
   | HTTPS / API
   v
FastAPI - App Platform
   |
   | TLS
   v
Managed MySQL 8.4
   |
   +--> Backups automáticos / PITR

GitHub --> CI --> Container Registry --> App Platform
```

## Separación de riesgos

| Componente | Ubicación | Riesgo mitigado |
|---|---|---|
| Código fuente | GitHub | Pérdida de una máquina de desarrollo |
| Imágenes | DigitalOcean Container Registry | Reconstrucción y despliegue repetible |
| API | App Platform | Independencia del equipo local y del servidor de BD |
| Frontend | App Platform, servicio separado | Separación de presentación y API |
| Datos | Managed MySQL | Persistencia fuera de los contenedores |
| Backups | Servicio administrado de base de datos | Recuperación ante borrado/corrupción lógica |

## Alta disponibilidad

La configuración académica usa `database_node_count = 1` para controlar costos. Si el presupuesto lo permite, cambiarlo a `2` agrega un nodo standby administrado para alta disponibilidad. La arquitectura mantiene el parámetro explícito para que la decisión de costo sea demostrable y no quede oculta.

La aplicación puede escalar a más de una instancia en App Platform si el plan seleccionado lo permite. Para la defensa se debe distinguir entre:

- **Redundancia:** múltiples instancias/nodos para soportar fallas.
- **Respaldo:** copias recuperables para errores humanos o corrupción lógica.

Una réplica no reemplaza un backup.
