from sqlalchemy.orm import Session
from app.repositories.UsuarioRepository import usuario_repository
from app.security.PasswordManager import verificar_contrasena
from app.security.TokenManager import crear_access_token
from app.config.Settings import settings

class CredencialesInvalidasError(Exception):
    pass

class AuthService:
    def autenticar(self, db: Session, nombre_usuario: str, contrasena: str, direccion_ip: str = None, user_agent: str = None):
        # 1. Buscar el usuario
        usuario = usuario_repository.buscar_por_nombre(db, nombre_usuario)
        
        # 2. Validar si existe y si su estado es ACTIVO
        if usuario is None or usuario.estado != "ACTIVO":
            # Nota: Usamos el mismo error para no revelar si falló el usuario o la contraseña
            raise CredencialesInvalidasError("Credenciales inválidas")
            
        # 3. Verificar la contraseña con Argon2
        if not verificar_contrasena(contrasena, usuario.contrasenaHash):
            raise CredencialesInvalidasError("Credenciales inválidas")
            
        # 4. Actualizar el último acceso
        usuario_repository.actualizar_ultimo_acceso(db, usuario)

        # 5. Generar el Token JWT
        token = crear_access_token(
            usuario_id=usuario.idUsuario,
            nombre_usuario=usuario.nombreUsuario,
            rol=usuario.rol.nombreRol
        )
        
        # 6. Devolver el formato exacto requerido
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

auth_service = AuthService()