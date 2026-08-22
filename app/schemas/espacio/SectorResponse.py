from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SectorResponse(BaseModel):
    idSector: int
    idProveedor: Optional[int] = None
    nombreSector: str
    descripcion: Optional[str]
    ubicacion: Optional[str]
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    estado: str
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
