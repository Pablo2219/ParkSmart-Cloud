from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ProviderSpaceInline(BaseModel):
    codigoEspacio: str = Field(..., min_length=2, max_length=20)
    tipoEspacio: Literal["REGULAR", "MOTOCICLETA", "DISCAPACIDAD", "ELECTRICO", "VIP"] = "REGULAR"
    descripcion: Optional[str] = Field(None, max_length=250)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)


class ProviderParkingCreate(BaseModel):
    nombreSector: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=250)
    ubicacion: Optional[str] = Field(None, max_length=100)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    espacios: List[ProviderSpaceInline] = Field(default_factory=list, max_length=200)


class ProviderProfileUpdate(BaseModel):
    nombreComercial: str = Field(..., min_length=2, max_length=120)
    telefono: str = Field(..., min_length=8, max_length=20)
    correoElectronico: str = Field(..., min_length=5, max_length=120)
    direccion: Optional[str] = Field(None, max_length=250)
    latitud: Optional[float] = Field(None, ge=-90, le=90)
    longitud: Optional[float] = Field(None, ge=-180, le=180)
