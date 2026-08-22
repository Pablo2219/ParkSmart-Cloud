from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Deuda import Deuda
from app.schemas.deuda.DeudaUpdate import DeudaUpdate


class DeudaRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Deuda)
        return self.db.scalars(consulta).all()

    def listar_pendientes(self):
        consulta = select(Deuda).where(
            Deuda.estado == "PENDIENTE"
        )

        return self.db.scalars(consulta).all()

    def listar_vencidas(self):
        consulta = select(Deuda).where(
            Deuda.estado == "VENCIDA"
        )

        return self.db.scalars(consulta).all()

    def listar_por_pago(self, idPago: int):
        consulta = select(Deuda).where(
            Deuda.idPago == idPago
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idDeuda: int):
        consulta = select(Deuda).where(
            Deuda.idDeuda == idDeuda
        )

        return self.db.scalar(consulta)

    def obtener_activa_por_pago(self, idPago: int):
        consulta = select(Deuda).where(
            Deuda.idPago == idPago,
            Deuda.estado.in_(["PENDIENTE", "VENCIDA"])
        )

        return self.db.scalar(consulta)

    def crear_vencida(
        self,
        idPago: int,
        codigoDeuda: str,
        montoDeuda,
        fechaLimite,
        observaciones: str | None
    ):
        deuda = Deuda(
            idPago=idPago,
            codigoDeuda=codigoDeuda,
            montoDeuda=montoDeuda,
            fechaLimite=fechaLimite,
            estado="VENCIDA",
            observaciones=observaciones
        )

        self.db.add(deuda)
        self.db.flush()

        return deuda

    def actualizar(self, deuda: Deuda, datos: DeudaUpdate):
        datos_actualizados = datos.model_dump(exclude_unset=True)

        for campo, valor in datos_actualizados.items():
            setattr(deuda, campo, valor)

        self.db.commit()
        self.db.refresh(deuda)

        return deuda

    def pagar(self, deuda: Deuda):
        deuda.estado = "PAGADA"

        self.db.commit()
        self.db.refresh(deuda)

        return deuda

    def marcar_vencida(self, deuda: Deuda):
        deuda.estado = "VENCIDA"

        self.db.commit()
        self.db.refresh(deuda)

        return deuda

    def anular(self, deuda: Deuda):
        deuda.estado = "ANULADA"

        self.db.commit()
        self.db.refresh(deuda)

        return deuda