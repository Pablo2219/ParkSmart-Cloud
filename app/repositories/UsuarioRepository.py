from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.Usuario import Usuario


class UsuarioRepository:
    def buscar_por_nombre(self, db: Session, nombre_usuario: str):
        return (
            db.query(Usuario)
            .options(joinedload(Usuario.rol))
            .filter(Usuario.nombreUsuario == nombre_usuario)
            .first()
        )

    def obtener_por_id(self, db: Session, idUsuario: int):
        return (
            db.query(Usuario)
            .options(joinedload(Usuario.rol))
            .filter(Usuario.idUsuario == idUsuario)
            .first()
        )

    def actualizar_ultimo_acceso(self, db: Session, usuario: Usuario):
        usuario.ultimoAcceso = datetime.now()
        db.commit()
        db.refresh(usuario)
        return usuario


usuario_repository = UsuarioRepository()
