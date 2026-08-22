import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config.Settings import settings
from app.models.Pago import Pago

logger = logging.getLogger(__name__)


class FacturacionService:
    """Adaptador aislado para consumir el API de facturación después de un pago confirmado."""

    def emitir_factura(self, pago: Pago, proveedor_id: int | None = None) -> dict:
        payload = {
            "tipoDocumento": "FACTURA_ELECTRONICA",
            "codigoPago": pago.codigoPago,
            "fechaPago": pago.fechaPago.isoformat() if pago.fechaPago else None,
            "montoSubtotal": str(pago.montoSubtotal or 0),
            "montoImpuesto": str(pago.montoImpuesto or 0),
            "montoTotal": str(pago.montoTotal or 0),
            "metodoPago": pago.metodoPago,
            "referenciaTransaccion": pago.referenciaTransaccion,
            "numeroComprobante": pago.numeroComprobante,
            "proveedorId": proveedor_id,
        }

        if settings.BILLING_MODE.upper() == "SIMULATION" or not settings.BILLING_API_URL.strip():
            return {
                "estado": "SIMULADA",
                "numeroFactura": f"FACT-SIM-{pago.codigoPago}",
                "payload": payload,
            }

        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if settings.BILLING_API_KEY:
            headers["Authorization"] = f"Bearer {settings.BILLING_API_KEY}"

        request = Request(settings.BILLING_API_URL.rstrip("/") + "/invoices", data=body, headers=headers, method="POST")
        try:
            with urlopen(request, timeout=settings.BILLING_API_TIMEOUT_SECONDS) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw) if raw else {}
                return {"estado": "EMITIDA", "respuesta": data}
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            logger.exception("No se pudo emitir la factura para el pago %s", pago.codigoPago)
            return {"estado": "PENDIENTE_REINTENTO", "error": str(error), "payload": payload}


facturacion_service = FacturacionService()
