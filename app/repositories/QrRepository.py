from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Qr import Qr
from app.models.Reserva import Reserva


class QrRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Qr)
        return self.db.scalars(consulta).all()

    def listar_por_reserva(self, idReserva: int):
        consulta = select(Qr).where(
            Qr.idReserva == idReserva
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idQr: int):
        consulta = select(Qr).where(
            Qr.idQr == idQr
        )

        return self.db.scalar(consulta)

    def validar_qr_activo(self, idQr: int) -> bool:
        ahora = datetime.now()

        consulta = select(Qr).where(
            Qr.idQr == idQr,
            Qr.estado == "ACTIVO",
            Qr.fechaActivacion <= ahora,
            Qr.fechaExpiracion >= ahora,
        )

        qr = self.db.scalar(consulta)

        return qr is not None

    def obtener_por_codigo(self, codigoQr: str):
        consulta = select(Qr).where(
            Qr.codigoQr == codigoQr
        )

        return self.db.scalar(consulta)

    def obtener_por_reserva_activa(self, idReserva: int):
        consulta = select(Qr).where(
            Qr.idReserva == idReserva,
            Qr.estado == "ACTIVO"
        )

        return self.db.scalar(consulta)

    def crear_activo(
        self,
        idReserva: int,
        codigoQr: str,
        tokenQr: str,
        fechaActivacion,
        fechaExpiracion
    ):
        qr = Qr(
            idReserva=idReserva,
            codigoQr=codigoQr,
            tokenQr=tokenQr,
            fechaValidezInicio=fechaActivacion,
            fechaValidezFin=fechaExpiracion,
            fechaActivacion=fechaActivacion,
            fechaExpiracion=fechaExpiracion,
            estado="ACTIVO"
        )

        self.db.add(qr)
        self.db.commit()
        self.db.refresh(qr)

        return qr

    def marcar_usado(self, qr: Qr):
        qr.estado = "USADO"
        qr.fechaUso = datetime.now()

        reserva = self.db.get(Reserva, qr.idReserva)

        if reserva is not None:
            reserva.estado = "UTILIZADA"

        self.db.commit()
        self.db.refresh(qr)

        return qr

    def marcar_vencido(self, qr: Qr):
        qr.estado = "VENCIDO"

        self.db.commit()
        self.db.refresh(qr)

        return qr

    def anular(self, qr: Qr):
        qr.estado = "CANCELADO"

        self.db.commit()
        self.db.refresh(qr)

        return qr