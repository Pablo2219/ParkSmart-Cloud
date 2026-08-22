from typing import Literal, Optional

from pydantic import BaseModel, Field


class NotificacionCreate(BaseModel):
    idCliente: int = Field(..., gt=0)

    idReserva: Optional[int] = Field(None, gt=0)
    idPago: Optional[int] = Field(None, gt=0)
    idDeuda: Optional[int] = Field(None, gt=0)

    tipoNotificacion: Literal[
        "RESERVA",
        "QR",
        "PAGO",
        "DEUDA",
        "SISTEMA"
    ]

    canal: Literal[
        "EMAIL",
        "SMS",
        "WHATSAPP",
        "PUSH"
    ]

    titulo: str = Field(..., min_length=3, max_length=100)
    mensaje: str = Field(..., min_length=5, max_length=500)