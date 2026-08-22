from typing import Literal, Optional

from pydantic import BaseModel, Field


class PagoUpdate(BaseModel):
    metodoPago: Optional[
        Literal[
            "EFECTIVO",
            "TARJETA",
            "SINPE",
            "PASARELA"
        ]
    ] = None

    estado: Optional[
        Literal[
            "PENDIENTE",
            "PAGADO",
            "VENCIDO",
            "ANULADO"
        ]
    ] = None

    referenciaTransaccion: Optional[str] = Field(
        None,
        max_length=100
    )

    numeroComprobante: Optional[str] = Field(
        None,
        max_length=100
    )

    observaciones: Optional[str] = Field(
        None,
        max_length=250
    )