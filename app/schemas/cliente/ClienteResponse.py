from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClienteResponse(BaseModel):
    idCliente: int
    identificacion: str
    nombre: str
    primerApellido: str
    segundoApellido: Optional[str]

    telefono: str
    correoElectronico: str
    provincia: Optional[str]
    canton: Optional[str]
    distrito: Optional[str]
    direccionExacta: Optional[str]
    estado: str
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)