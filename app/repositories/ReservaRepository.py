from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.Reserva import Reserva
from app.models.Espacio import Espacio
from app.schemas.reserva.ReservaCreate import ReservaCreate
from app.schemas.reserva.ReservaUpdate import ReservaUpdate


class ReservaRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Reserva)
        return self.db.scalars(consulta).all()

    def listar_activas(self):
        consulta = select(Reserva).where(
            Reserva.estado.in_(["PENDIENTE", "CONFIRMADA"])
        )

        return self.db.scalars(consulta).all()

    def listar_por_cliente(self, idCliente: int):
        consulta = select(Reserva).where(
            Reserva.idCliente == idCliente
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idReserva: int):
        consulta = select(Reserva).where(
            Reserva.idReserva == idReserva
        )

        return self.db.scalar(consulta)

    def existe_cruce_reserva(
        self,
        idEspacio: int,
        fechaInicioReserva,
        fechaFinReserva,
        idReservaExcluir: int | None = None
    ):
        consulta = select(func.count()).select_from(Reserva).where(
            Reserva.idEspacio == idEspacio,
            Reserva.estado.in_(["PENDIENTE", "CONFIRMADA"]),
            fechaInicioReserva < Reserva.fechaFinReserva,
            fechaFinReserva > Reserva.fechaInicioReserva
        )

        if idReservaExcluir is not None:
            consulta = consulta.where(
                Reserva.idReserva != idReservaExcluir
            )

        cantidad = self.db.scalar(consulta)

        return cantidad > 0

    def crear(self, datos: ReservaCreate, codigoReserva: str):
        reserva = Reserva(
            idCliente=datos.idCliente,
            idVehiculo=datos.idVehiculo,
            idEspacio=datos.idEspacio,
            codigoReserva=codigoReserva,
            fechaInicioReserva=datos.fechaInicioReserva,
            fechaFinReserva=datos.fechaFinReserva,
            estado="CONFIRMADA",
            observaciones=datos.observaciones
        )

        espacio = self.db.get(Espacio, datos.idEspacio)

        if espacio is not None:
            espacio.estado = "RESERVADO"

        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)

        return reserva

    def actualizar(self, reserva: Reserva, datos: ReservaUpdate):
        datos_actualizados = datos.model_dump(exclude_unset=True)

        for campo, valor in datos_actualizados.items():
            setattr(reserva, campo, valor)

        self.db.commit()
        self.db.refresh(reserva)

        return reserva

    def cancelar(self, reserva: Reserva):
        reserva.estado = "CANCELADA"

        espacio = self.db.get(Espacio, reserva.idEspacio)

        if espacio is not None:
            espacio.estado = "DISPONIBLE"

        self.db.commit()
        self.db.refresh(reserva)

        return reserva