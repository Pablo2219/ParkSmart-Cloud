from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EspacioResponse(BaseModel):
    idEspacio: int
    idSector: int
    codigoEspacio: str
    tipoEspacio: str
    estado: str
    descripcion: Optional[str]
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
