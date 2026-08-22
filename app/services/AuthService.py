from sqlalchemy.orm import Session

from app.repositories.UsuarioRepository import usuario_repository
from app.security.PasswordManager import verificar_contrasena
from app.security.TokenManager import crear_access_token
from app.config.Settings import settings


class CredencialesInvalidasError(Exception):
    pass


class AuthService:
    def autenticar(self, db: Session, nombre_usuario: str, contrasena: str, direccion_ip: str = None, user_agent: str = None):
        usuario = usuario_repository.buscar_por_identidad(db, nombre_usuario.strip())

        if usuario is None or usuario.estado != "ACTIVO":
            raise CredencialesInvalidasError("Credenciales inválidas")

        if not verificar_contrasena(contrasena, usuario.contrasenaHash):
            raise CredencialesInvalidasError("Credenciales inválidas")

        usuario_repository.actualizar_ultimo_acceso(db, usuario)

        token = crear_access_token(
            usuario_id=usuario.idUsuario,
            nombre_usuario=usuario.nombreUsuario,
            rol=usuario.rol.nombreRol,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "usuario": {
                "idUsuario": usuario.idUsuario,
                "idCliente": usuario.idCliente,
                "idProveedor": usuario.idProveedor,
                "nombreUsuario": usuario.nombreUsuario,
                "correoElectronico": usuario.correoElectronico,
                "rol": usuario.rol.nombreRol,
            },
        }


auth_service = AuthService()
