from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ReservaCreate(BaseModel):
    idCliente: int = Field(..., gt=0)
    idVehiculo: int = Field(..., gt=0)
    idEspacio: int = Field(..., gt=0)

    fechaInicioReserva: datetime
    fechaFinReserva: datetime

    observaciones: Optional[str] = Field(None, max_length=250)

    @field_validator("fechaFinReserva")
    @classmethod
    def validar_fechas(cls, fecha_fin, info):
        fecha_inicio = info.data.get("fechaInicioReserva")

        if fecha_inicio and fecha_fin <= fecha_inicio:
            raise ValueError(
                "La fecha final debe ser posterior a la fecha inicial."
            )

        return fecha_fin