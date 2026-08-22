from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class VehiculoResponse(BaseModel):
    idVehiculo: int
    idCliente: int
    placa: str
    marca: Optional[str]
    modelo: Optional[str]
    color: Optional[str]
    tipoVehiculo: str
    estado: str
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)