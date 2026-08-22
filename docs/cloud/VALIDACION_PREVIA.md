# Validación previa del paquete cloud

Antes de entregar este paquete se realizaron las siguientes revisiones estructurales:

- compilación de módulos Python de `app/`, `migrations/`, `tests/` y prueba de rendimiento;
- validación de sintaxis JSON de los archivos Postman;
- validación de sintaxis YAML de `.do/app.template.yaml`;
- comprobación de normalización de URL MySQL cloud hacia `mysql+pymysql`;
- comprobación de materialización del CA de base de datos para TLS;
- comprobación del build script del frontend con una URL de API de prueba;
- ejecución de las cuatro pruebas de health/root con dependencias aisladas del entorno;
- búsqueda de `.env`, `terraform.tfvars`, claves privadas y tokens conocidos dentro del paquete final.

## Validaciones que requieren las cuentas del equipo

No pueden completarse de forma estática porque dependen de recursos reales:

- `terraform plan/apply` contra la cuenta de DigitalOcean;
- push real al Container Registry;
- despliegue real en App Platform;
- trusted sources de Managed MySQL;
- health/readiness públicos;
- backup/restore real;
- métricas, alertas y prueba de carga sobre la URL pública.

Los scripts de `scripts/cloud/` están preparados para ejecutar esas verificaciones en orden.
