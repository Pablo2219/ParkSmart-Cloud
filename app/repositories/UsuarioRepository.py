from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.Usuario import Usuario


class UsuarioRepository:
    def buscar_por_identidad(self, db: Session, identidad: str):
        return (
            db.query(Usuario)
            .options(joinedload(Usuario.rol), joinedload(Usuario.proveedor))
            .filter(or_(Usuario.nombreUsuario == identidad, Usuario.correoElectronico == identidad))
            .first()
        )

    def buscar_por_nombre(self, db: Session, nombre_usuario: str):
        return self.buscar_por_identidad(db, nombre_usuario)

    def obtener_por_id(self, db: Session, idUsuario: int):
        return (
            db.query(Usuario)
            .options(joinedload(Usuario.rol), joinedload(Usuario.proveedor))
            .filter(Usuario.idUsuario == idUsuario)
            .first()
        )

    def actualizar_ultimo_acceso(self, db: Session, usuario: Usuario):
        usuario.ultimoAcceso = datetime.now()
        db.commit()
        db.refresh(usuario)
        return usuario


usuario_repository = UsuarioRepository()
