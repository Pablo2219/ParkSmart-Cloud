import re
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class RegisterRequest(BaseModel):
    nombreUsuario: str = Field(..., min_length=4, max_length=50)
    correoElectronico: EmailStr
    contrasena: str = Field(..., min_length=8, max_length=128)
    rol: Literal["CLIENTE", "PROVEEDOR"]
    aceptaPrivacidad: bool = Field(..., description="Consentimiento expreso para el tratamiento de datos")
    aceptaTerminos: bool = Field(..., description="Aceptación expresa de términos y condiciones")

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

    @field_validator("contrasena")
    @classmethod
    def validar_contrasena(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value) or not re.search(r"[a-z]", value) or not re.search(r"\d", value) or not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula, número y símbolo.")
        return value

    @model_validator(mode="after")
    def validar_por_rol(self):
        if not self.aceptaPrivacidad:
            raise ValueError("Debes aceptar de forma expresa la política de privacidad y el tratamiento de datos.")
        if not self.aceptaTerminos:
            raise ValueError("Debes aceptar los términos y condiciones para crear la cuenta.")
        if self.rol == "CLIENTE" and (not self.nombre or not self.primerApellido):
            raise ValueError("Para un cliente se requieren nombre y primer apellido.")
        if self.rol == "PROVEEDOR" and not self.nombreComercial:
            raise ValueError("Para un proveedor se requiere el nombre comercial.")
        return self
