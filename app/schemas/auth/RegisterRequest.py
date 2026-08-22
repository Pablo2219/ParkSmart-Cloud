from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class RegisterRequest(BaseModel):
    nombreUsuario: str = Field(..., min_length=4, max_length=50)
    correoElectronico: EmailStr
    contrasena: str = Field(..., min_length=8, max_length=128)
    rol: Literal["CLIENTE", "PROVEEDOR"]
    aceptaPrivacidad: bool = Field(..., description="Consentimiento expreso para el tratamiento de datos")

    identificacion: str = Field(..., min_length=6, max_length=20)
    telefono: str = Field(..., min_length=8, max_length=20)

    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    primerApellido: Optional[str] = Field(None, min_length=2, max_length=50)
    segundoApellido: Optional[str] = Field(None, max_length=50)

    nombreComercial: Optional[str] = Field(None, min_length=2, max_length=120)
    direccion: Optional[str] = Field(None, max_length=250)

    @field_validator("nombreUsuario", "identificacion", "telefono")
    @classmethod
    def limpiar_texto(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def validar_por_rol(self):
        if not self.aceptaPrivacidad:
            raise ValueError("Debes aceptar el tratamiento de datos personales para crear la cuenta.")
        if self.rol == "CLIENTE":
            if not self.nombre or not self.primerApellido:
                raise ValueError("Para un cliente se requieren nombre y primer apellido.")
        if self.rol == "PROVEEDOR" and not self.nombreComercial:
            raise ValueError("Para un proveedor se requiere el nombre comercial.")
        return self
