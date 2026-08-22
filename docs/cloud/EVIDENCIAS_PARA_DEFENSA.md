# Evidencias para la defensa

## Infraestructura

- [ ] Terraform `plan` sin secretos visibles.
- [ ] VPC creada.
- [ ] Container Registry creado.
- [ ] Managed MySQL en estado online.
- [ ] API y frontend en App Platform.
- [ ] URL pública HTTPS funcionando.

## Separación de componentes

- [ ] Código en GitHub.
- [ ] Imágenes API/frontend en DOCR.
- [ ] aplicación en App Platform.
- [ ] datos en Managed MySQL.
- [ ] backups administrados disponibles.

## Disponibilidad

- [ ] `/api/health` = `ok`.
- [ ] `/api/health/ready` = `ready`.
- [ ] health checks visibles en App Platform.
- [ ] métricas de CPU/memoria/reinicios.
- [ ] alertas configuradas.

## Seguridad

- [ ] `.env` no rastreado.
- [ ] `terraform.tfvars` no rastreado.
- [ ] token de DigitalOcean rotado si fue expuesto previamente.
- [ ] Managed MySQL sin regla `0.0.0.0/0`.
- [ ] App Platform aparece como trusted source.
- [ ] conexión TLS.

## Continuidad

- [ ] backups/PITR visibles.
- [ ] ejercicio de restore/fork ejecutado.
- [ ] RPO documentado.
- [ ] RTO medido.
- [ ] recurso temporal eliminado después de la prueba.

## Rendimiento

- [ ] prueba de carga ejecutada.
- [ ] p95 registrado.
- [ ] throughput registrado.
- [ ] tasa de errores registrada.
- [ ] comparación contra SLA.
