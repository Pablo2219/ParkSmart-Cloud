from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Espacio import Espacio
from app.models.Ocupacion import Ocupacion
from app.models.Qr import Qr
from app.models.Reserva import Reserva
from app.schemas.ocupacion.OcupacionUpdate import OcupacionUpdate


class OcupacionRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Ocupacion)
        return self.db.scalars(consulta).all()

    def listar_activas(self):
        consulta = select(Ocupacion).where(
            Ocupacion.estado == "EN_CURSO"
        )

        return self.db.scalars(consulta).all()

    def listar_por_reserva(self, idReserva: int):
        consulta = select(Ocupacion).where(
            Ocupacion.idReserva == idReserva
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idOcupacion: int):
        consulta = select(Ocupacion).where(
            Ocupacion.idOcupacion == idOcupacion
        )

        return self.db.scalar(consulta)

    def obtener_activa_por_reserva(self, idReserva: int):
        consulta = select(Ocupacion).where(
            Ocupacion.idReserva == idReserva,
            Ocupacion.estado == "EN_CURSO"
        )

        return self.db.scalar(consulta)

    def obtener_por_qr(self, idQr: int):
        consulta = select(Ocupacion).where(
            Ocupacion.idQr == idQr
        )

        return self.db.scalar(consulta)

    def crear(
        self,
        idReserva: int,
        idEspacio: int,
        idQr: int,
        observaciones: str | None
    ):
        ocupacion = Ocupacion(
            idReserva=idReserva,
            idEspacio=idEspacio,
            idQr=idQr,
            estado="EN_CURSO",
            observaciones=observaciones
        )

        espacio = self.db.get(Espacio, idEspacio)

        if espacio is not None:
            espacio.estado = "OCUPADO"

        reserva = self.db.get(Reserva, idReserva)

        if reserva is not None:
            reserva.estado = "UTILIZADA"

        qr = self.db.get(Qr, idQr)

        if qr is not None:
            qr.estado = "USADO"
            qr.fechaUso = datetime.now()

        self.db.add(ocupacion)

        # No hacemos commit aqui.
        # OcupacionService controla la transaccion completa.
        self.db.flush()

        return ocupacion

    def actualizar(
        self,
        ocupacion: Ocupacion,
        datos: OcupacionUpdate
    ):
        datos_actualizados = datos.model_dump(
            exclude_unset=True
        )

        for campo, valor in datos_actualizados.items():
            setattr(ocupacion, campo, valor)

        self.db.commit()
        self.db.refresh(ocupacion)

        return ocupacion

    def finalizar(
        self,
        ocupacion: Ocupacion,
        fecha_salida: datetime,
        tiempo_total_minutos: int,
    ):
        ocupacion.estado = "FINALIZADA"
        ocupacion.fechaSalida = fecha_salida
        ocupacion.tiempoTotalMinutos = tiempo_total_minutos

        espacio = self.db.get(
            Espacio,
            ocupacion.idEspacio
        )

        if espacio is not None:
            espacio.estado = "DISPONIBLE"

        self.db.flush()

        return ocupacion

    def cancelar(self, ocupacion: Ocupacion):
        ocupacion.estado = "CANCELADA"

        espacio = self.db.get(
            Espacio,
            ocupacion.idEspacio
        )

        if espacio is not None:
            espacio.estado = "DISPONIBLE"

        self.db.commit()
        self.db.refresh(ocupacion)

        return ocupacion