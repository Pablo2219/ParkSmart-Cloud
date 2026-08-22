from typing import Literal, Optional

from pydantic import BaseModel, Field


class NotificacionUpdate(BaseModel):
    canal: Optional[
        Literal[
            "EMAIL",
            "SMS",
            "WHATSAPP",
            "PUSH"
        ]
    ] = None

    titulo: Optional[str] = Field(None, min_length=3, max_length=100)
    mensaje: Optional[str] = Field(None, min_length=5, max_length=500)

    estado: Optional[
        Literal[
            "PENDIENTE",
            "ENVIADA",
            "FALLIDA",
            "LEIDA",
            "ANULADA"
        ]
    ] = None