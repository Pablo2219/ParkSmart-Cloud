from typing import Optional

from pydantic import BaseModel, Field


class ProviderSectorCreate(BaseModel):
    nombreSector: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=250)
    ubicacion: Optional[str] = Field(None, max_length=100)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
