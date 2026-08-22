from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ClienteCreate(BaseModel):
    identificacion: str = Field(..., min_length=5, max_length=20)
    nombre: str = Field(..., min_length=2, max_length=50)
    primerApellido: str = Field(..., min_length=2, max_length=50)
    segundoApellido: Optional[str] = Field(None, max_length=50)

    telefono: str = Field(..., min_length=8, max_length=20)
    correoElectronico: EmailStr

    provincia: Optional[str] = Field(None, max_length=50)
    canton: Optional[str] = Field(None, max_length=50)
    distrito: Optional[str] = Field(None, max_length=50)
    direccionExacta: Optional[str] = Field(None, max_length=250)