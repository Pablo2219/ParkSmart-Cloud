from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import PyJWTError
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.config.Settings import settings
from app.repositories.UsuarioRepository import usuario_repository

# Le decimos a FastAPI dónde está la ruta de login para que lo muestre en la documentación (Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o la sesión expiró",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Descifrar el token usando la llave secreta
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        
        # 2. Extraer el ID del usuario. Ajusta "usuario_id" si en tu TokenManager lo llamaste diferente (a veces se usa "sub")
        usuario_id_raw = payload.get("sub")
        usuario_id = int(usuario_id_raw) if usuario_id_raw is not None else None
        
        if usuario_id is None:
            raise credenciales_exception
            
    except (PyJWTError, ValueError, TypeError):
        # Si el token es inventado, fue alterado o ya caducó, rechazamos la petición
        raise credenciales_exception

    # 3. Buscar al usuario real en la base de datos
    usuario = usuario_repository.obtener_por_id(db, idUsuario=usuario_id)
    
    if usuario is None or usuario.estado != "ACTIVO":
        raise credenciales_exception
        
    return usuario


def exigir_roles(*roles_permitidos):
    """
    Función validadora para proteger endpoints específicos.
    Ejemplo de uso en un controlador: Depends(exigir_roles("ADMINISTRADOR", "OPERADOR"))
    """
    def verificador_roles(usuario = Depends(obtener_usuario_actual)):
        # Verificamos si el nombre del rol del usuario está en la lista de permitidos
        if usuario.rol.nombreRol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para realizar esta acción"
            )
        return usuario
        
    return verificador_roles