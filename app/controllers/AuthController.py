from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.auth.RegisterRequest import RegisterRequest
from app.services.AuthService import auth_service, CredencialesInvalidasError
from app.services.RegistrationService import registro_service
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(datos: RegisterRequest, db: Session = Depends(get_db)):
    try:
        return registro_service.registrar(db, datos)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No fue posible registrar la cuenta porque uno de los datos ya existe.")


@router.get("/me")
def me(usuario=Depends(obtener_usuario_actual)):
    proveedor = usuario.proveedor
    return {
        "idUsuario": usuario.idUsuario,
        "idCliente": usuario.idCliente,
        "idProveedor": usuario.idProveedor,
        "nombreUsuario": usuario.nombreUsuario,
        "correoElectronico": usuario.correoElectronico,
        "rol": usuario.rol.nombreRol,
        "estado": usuario.estado,
        "aceptaPrivacidad": usuario.aceptaPrivacidad,
        "versionPoliticaPrivacidad": usuario.versionPoliticaPrivacidad,
        "proveedor": {
            "idProveedor": proveedor.idProveedor,
            "nombreComercial": proveedor.nombreComercial,
            "telefono": proveedor.telefono,
            "correoElectronico": proveedor.correoElectronico,
            "direccion": proveedor.direccion,
            "latitud": proveedor.latitud,
            "longitud": proveedor.longitud,
        } if proveedor else None,
    }


@router.get("/mis-datos")
def mis_datos(usuario=Depends(obtener_usuario_actual)):
    """Mecanismo de acceso a los datos personales del titular."""
    return {
        "usuario": {
            "idUsuario": usuario.idUsuario,
            "nombreUsuario": usuario.nombreUsuario,
            "correoElectronico": usuario.correoElectronico,
            "rol": usuario.rol.nombreRol,
            "fechaCreacion": usuario.fechaCreacion,
            "fechaConsentimiento": usuario.fechaConsentimiento,
            "versionPoliticaPrivacidad": usuario.versionPoliticaPrivacidad,
        },
        "idCliente": usuario.idCliente,
        "idProveedor": usuario.idProveedor,
    }


@router.post("/revocar-consentimiento")
def revocar_consentimiento(usuario=Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    """Revoca el consentimiento comercial y desactiva el acceso a la cuenta."""
    usuario.aceptaPrivacidad = False
    usuario.estado = "INACTIVO"
    db.commit()
    return {"mensaje": "Consentimiento revocado. La cuenta fue desactivada.", "estado": usuario.estado}
