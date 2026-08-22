from typing import Literal, Optional

from pydantic import BaseModel, Field


class ProviderSpaceCreate(BaseModel):
    idSector: int = Field(..., gt=0)
    codigoEspacio: str = Field(..., min_length=2, max_length=20)
    tipoEspacio: Literal["REGULAR", "MOTOCICLETA", "DISCAPACIDAD", "ELECTRICO", "VIP"] = "REGULAR"
    descripcion: Optional[str] = Field(None, max_length=250)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
