from typing import Literal, Optional

from pydantic import BaseModel, Field


class DeudaUpdate(BaseModel):
    estado: Optional[
        Literal[
            "PENDIENTE",
            "PAGADA",
            "VENCIDA",
            "ANULADA"
        ]
    ] = None

    observaciones: Optional[str] = Field(None, max_length=250)