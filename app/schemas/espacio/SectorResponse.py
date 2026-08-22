from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SectorResponse(BaseModel):
    idSector: int
    nombreSector: str
    descripcion: Optional[str]
    ubicacion: Optional[str]
    estado: str
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)