from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    primerApellido: Optional[str] = Field(None, min_length=2, max_length=50)
    segundoApellido: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, min_length=8, max_length=20)
    correoElectronico: Optional[EmailStr] = None
    provincia: Optional[str] = Field(None, max_length=50)
    canton: Optional[str] = Field(None, max_length=50)
    distrito: Optional[str] = Field(None, max_length=50)
    direccionExacta: Optional[str] = Field(None, max_length=250)

    estado: Optional[Literal["ACTIVO", "INACTIVO", "SUSPENDIDO"]] = None