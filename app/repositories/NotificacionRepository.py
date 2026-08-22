from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Notificacion import Notificacion
from app.schemas.notificacion.NotificacionCreate import NotificacionCreate
from app.schemas.notificacion.NotificacionUpdate import NotificacionUpdate


class NotificacionRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Notificacion)
        return self.db.scalars(consulta).all()

    def listar_pendientes(self):
        consulta = select(Notificacion).where(
            Notificacion.estado == "PENDIENTE"
        )

        return self.db.scalars(consulta).all()

    def listar_por_cliente(self, idCliente: int):
        consulta = select(Notificacion).where(
            Notificacion.idCliente == idCliente
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idNotificacion: int):
        consulta = select(Notificacion).where(
            Notificacion.idNotificacion == idNotificacion
        )

        return self.db.scalar(consulta)

    def crear(self, datos: NotificacionCreate):
        notificacion = Notificacion(**datos.model_dump())

        self.db.add(notificacion)
        self.db.commit()
        self.db.refresh(notificacion)

        return notificacion

    def actualizar(
        self,
        notificacion: Notificacion,
        datos: NotificacionUpdate
    ):
        datos_actualizados = datos.model_dump(exclude_unset=True)

        for campo, valor in datos_actualizados.items():
            setattr(notificacion, campo, valor)

        self.db.commit()
        self.db.refresh(notificacion)

        return notificacion

    def marcar_enviada(self, notificacion: Notificacion):
        notificacion.estado = "ENVIADA"
        notificacion.fechaEnvio = datetime.now()

        self.db.commit()
        self.db.refresh(notificacion)

        return notificacion

    def marcar_leida(self, notificacion: Notificacion):
        notificacion.estado = "LEIDA"
        notificacion.fechaLectura = datetime.now()

        self.db.commit()
        self.db.refresh(notificacion)

        return notificacion

    def marcar_fallida(self, notificacion: Notificacion):
        notificacion.estado = "FALLIDA"

        self.db.commit()
        self.db.refresh(notificacion)

        return notificacion

    def anular(self, notificacion: Notificacion):
        notificacion.estado = "ANULADA"

        self.db.commit()
        self.db.refresh(notificacion)

        return notificacion