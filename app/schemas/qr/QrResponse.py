from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class QrResponse(BaseModel):
    idQr: int
    idReserva: int
    codigoQr: str
    tokenQr: str
    fechaGeneracion: datetime
    fechaValidezInicio: datetime
    fechaValidezFin: datetime
    estado: str
    fechaUso: Optional[datetime]
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)