from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

class VehiculoCreate(BaseModel):
    idCliente: int = Field(..., gt=0)
    placa: str = Field(..., min_length=5, max_length=20)
    marca: Optional[str] = Field(None, max_length=50)
    modelo: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=30)
    tipoVehiculo: Literal[
        "AUTOMOVIL",
        "MOTOCICLETA",
        "CAMIONETA",
        "OTRO"
    ] = "AUTOMOVIL"

    @field_validator("placa")
    @classmethod
    def normalizar_placa(cls, valor: str):
        return valor.strip().upper()