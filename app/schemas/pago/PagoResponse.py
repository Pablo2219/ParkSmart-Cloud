from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PagoResponse(BaseModel):
    idPago: int
    idOcupacion: int
    codigoPago: str
    montoTotal: Decimal
    metodoPago: Optional[str]
    estado: str
    fechaGeneracion: datetime
    fechaLimitePago: datetime
    fechaPago: Optional[datetime]
    referenciaTransaccion: Optional[str]
    observaciones: Optional[str]
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)