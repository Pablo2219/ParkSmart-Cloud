from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OcupacionResponse(BaseModel):
    idOcupacion: int
    idReserva: int
    idEspacio: int
    fechaEntrada: datetime
    fechaSalida: Optional[datetime]
    estado: str
    observaciones: Optional[str]
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)