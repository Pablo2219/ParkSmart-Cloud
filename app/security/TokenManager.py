from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError

from app.config.Settings import settings

def crear_access_token(
    usuario_id: int,
    nombre_usuario: str,
    rol: str,
) -> str:
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario_id),
        "username": nombre_usuario,
        "role": rol,
        "iat": ahora,
        "exp": ahora + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

def decodificar_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except InvalidTokenError as error:
        raise ValueError("Token inválido o vencido") from error