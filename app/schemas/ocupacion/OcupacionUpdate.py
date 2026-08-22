from typing import Literal, Optional

from pydantic import BaseModel, Field


class OcupacionUpdate(BaseModel):
    estado: Optional[
        Literal[
            "EN_CURSO",
            "FINALIZADA",
            "CANCELADA"
        ]
    ] = None

    observaciones: Optional[str] = Field(None, max_length=250)