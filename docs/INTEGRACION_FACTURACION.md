# Integración de facturación de ParkSmart

ParkSmart separa la lógica de negocio de la integración externa mediante `FacturacionService`.

## Funcionamiento local

Con:

```env
BILLING_MODE=SIMULATION
BILLING_API_URL=
```

la confirmación de un pago sigue su flujo normal y el adaptador genera una respuesta simulada. No se necesita ningún proveedor externo para probar Docker.

## Producción

Cuando exista el proveedor de facturación, configurar:

```env
BILLING_MODE=API
BILLING_API_URL=https://dominio-del-proveedor
BILLING_API_KEY=...
BILLING_API_TIMEOUT_SECONDS=10
```

El adaptador realiza un `POST` a:

```text
{BILLING_API_URL}/invoices
```

con un payload equivalente a:

```json
{
  "tipoDocumento": "FACTURA_ELECTRONICA",
  "codigoPago": "PAG-...",
  "fechaPago": "2026-08-22T10:30:00",
  "montoSubtotal": "1000.00",
  "montoImpuesto": "130.00",
  "montoTotal": "1130.00",
  "metodoPago": "TARJETA",
  "referenciaTransaccion": "TX-123",
  "numeroComprobante": "CMP-123",
  "proveedorId": 10
}
```

La confirmación de un pago no se revierte si el API externo falla. El adaptador devuelve `PENDIENTE_REINTENTO` para que posteriormente se pueda incorporar una cola/outbox de reintentos sin modificar la lógica de pagos.

El contrato definitivo debe adaptarse al proveedor fiscal elegido y a los requisitos de facturación electrónica de Costa Rica antes de producción.
