from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

class VehiculoUpdate(BaseModel):
    placa: Optional[str] = Field(None, min_length=5, max_length=20)
    marca: Optional[str] = Field(None, max_length=50)
    modelo: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=30)

    tipoVehiculo: Optional[
        Literal[
            "AUTOMOVIL",
            "MOTOCICLETA",
            "CAMIONETA",
            "OTRO"
        ]
    ] = None

    estado: Optional[
        Literal[
            "ACTIVO",
            "INACTIVO"
        ]
    ] = None

    @field_validator("placa")
    @classmethod
    def normalizar_placa(cls, valor: Optional[str]):
        if valor is None:
            return valor

        return valor.strip().upper()