from typing import Annotated
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.services.AuthService import auth_service, CredencialesInvalidasError
from app.security.Dependencies import obtener_usuario_actual

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
def login(
    request: Request,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    try:
        return auth_service.autenticar(
            db=db,
            nombre_usuario=form.username,
            contrasena=form.password,
            direccion_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    except CredencialesInvalidasError:
        # Devolvemos un 401 uniforme sin revelar si falló el usuario o la contraseña
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me")
def me(usuario=Depends(obtener_usuario_actual)):
    # Devuelve la identidad del usuario sin exponer la contraseña
    return {
        "idUsuario": usuario.idUsuario,
        "nombreUsuario": usuario.nombreUsuario,
        "rol": usuario.rol.nombreRol,
    }