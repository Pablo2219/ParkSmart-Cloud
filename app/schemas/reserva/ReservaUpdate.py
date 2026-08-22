from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class ReservaUpdate(BaseModel):
    fechaInicioReserva: Optional[datetime] = None
    fechaFinReserva: Optional[datetime] = None

    estado: Optional[
        Literal[
            "PENDIENTE",
            "CONFIRMADA",
            "CANCELADA",
            "VENCIDA",
            "UTILIZADA"
        ]
    ] = None

    observaciones: Optional[str] = Field(None, max_length=250)

    @field_validator("fechaFinReserva")
    @classmethod
    def validar_fechas(cls, fecha_fin, info):
        fecha_inicio = info.data.get("fechaInicioReserva")

        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise ValueError(
                "La fecha final debe ser posterior a la fecha inicial."
            )

        return fecha_fin