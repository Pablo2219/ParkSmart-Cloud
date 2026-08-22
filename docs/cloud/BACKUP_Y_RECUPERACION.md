# Backup y recuperación

## Principio

Redundancia y respaldo resuelven problemas diferentes. Un nodo standby protege frente a una falla de infraestructura; un backup permite recuperar información eliminada o dañada lógicamente.

## Estrategia

ParkSmart utiliza DigitalOcean Managed MySQL. El servicio administra backups automáticos y permite recuperación a un punto anterior dentro de la ventana disponible del proveedor.

## RPO y RTO propuestos

- **RPO objetivo:** <= 24 horas como mínimo académico; el servicio de Managed MySQL puede ofrecer recuperación más granular dentro de su ventana de PITR.
- **RTO objetivo:** <= 2 horas para una restauración y reconexión controlada en un escenario académico.

Estos valores deben validarse con una prueba real antes de presentarlos como resultados alcanzados.

## Prueba de recuperación recomendada

La prueba no debe destruir el clúster principal.

1. Crear registros identificables de prueba.
2. Anotar la hora UTC.
3. Verificar que los registros existen.
4. Ejecutar una restauración/fork a un clúster temporal desde backup o punto en el tiempo.
5. Conectarse al clúster temporal.
6. comprobar los registros restaurados.
7. documentar duración real del proceso.
8. eliminar el clúster temporal al finalizar para detener costos.

El script `scripts/cloud/08-restore-drill.ps1` muestra el procedimiento y solo crea recursos cuando se usa el parámetro `-Execute`.

## Evidencia para la defensa

Guardar capturas o salidas que muestren:

- backups habilitados;
- fecha/hora del punto restaurado;
- clúster temporal creado;
- consulta de verificación;
- duración total;
- limpieza del recurso temporal.

Nunca incluir passwords ni connection strings completas.
