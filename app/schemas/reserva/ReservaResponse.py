from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReservaResponse(BaseModel):
    idReserva: int
    idCliente: int
    idVehiculo: int
    idEspacio: int
    codigoReserva: str
    fechaInicioReserva: datetime
    fechaFinReserva: datetime
    estado: str
    observaciones: Optional[str]
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)