# SLA, RPO y RTO de ParkSmart

Los siguientes valores son objetivos del proyecto. Deben compararse con resultados reales de pruebas antes de la exposición.

| Indicador | Objetivo |
|---|---:|
| Disponibilidad de la API | >= 99.5% |
| `/health` p95 | < 500 ms |
| Endpoints comunes p95 | < 1000 ms |
| Tasa de errores bajo prueba controlada | < 1% |
| RPO | <= 24 h |
| RTO | <= 2 h |

## Medición

Ejecutar:

```powershell
python .\qa\performance\cloud-load-test.py --url https://URL-APP/api/health --requests 100 --concurrency 10
```

El script reporta promedio, p50, p95, máximo, throughput y tasa de errores.

## Interpretación

- Si p95 supera la meta, documentar tamaño de instancia, carga y posible escalamiento.
- Si existe una tasa de error significativa, revisar logs y métricas antes de aumentar recursos.
- El RTO debe medirse durante el ejercicio de restauración, no estimarse sin evidencia.
