from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class EspacioUpdate(BaseModel):
    idSector: Optional[int] = Field(None, gt=0)
    codigoEspacio: Optional[str] = Field(None, min_length=2, max_length=20)

    tipoEspacio: Optional[
        Literal[
            "REGULAR",
            "MOTOCICLETA",
            "DISCAPACIDAD",
            "ELECTRICO",
            "VIP"
        ]
    ] = None

    estado: Optional[
        Literal[
            "DISPONIBLE",
            "OCUPADO",
            "RESERVADO",
            "MANTENIMIENTO",
            "INACTIVO"
        ]
    ] = None

    descripcion: Optional[str] = Field(None, max_length=250)

    @field_validator("codigoEspacio")
    @classmethod
    def normalizar_codigo(cls, valor: Optional[str]):
        if valor is None:
            return valor

        return valor.strip().upper()