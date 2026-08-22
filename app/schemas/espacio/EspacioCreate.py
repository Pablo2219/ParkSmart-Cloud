from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class EspacioCreate(BaseModel):
    idSector: int = Field(..., gt=0)
    codigoEspacio: str = Field(..., min_length=2, max_length=20)

    tipoEspacio: Literal[
        "REGULAR",
        "MOTOCICLETA",
        "DISCAPACIDAD",
        "ELECTRICO",
        "VIP"
    ] = "REGULAR"

    descripcion: Optional[str] = Field(None, max_length=250)

    @field_validator("codigoEspacio")
    @classmethod
    def normalizar_codigo(cls, valor: str):
        return valor.strip().upper()