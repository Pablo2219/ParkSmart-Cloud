from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeudaResponse(BaseModel):
    idDeuda: int
    idPago: int
    codigoDeuda: str
    montoDeuda: Decimal
    fechaGeneracion: datetime
    fechaLimite: datetime
    estado: str
    observaciones: Optional[str]
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)