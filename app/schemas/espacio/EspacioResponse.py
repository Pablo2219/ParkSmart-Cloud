from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EspacioResponse(BaseModel):
    idEspacio: int
    idSector: int
    codigoEspacio: str
    tipoEspacio: str
    estado: str
    descripcion: Optional[str]
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)