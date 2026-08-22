from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Pago import Pago
from app.schemas.pago.PagoCreate import PagoCreate
from app.schemas.pago.PagoUpdate import PagoUpdate


class PagoRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Pago)
        return self.db.scalars(consulta).all()

    def listar_pendientes(self):
        consulta = select(Pago).where(
            Pago.estado == "PENDIENTE"
        )

        return self.db.scalars(consulta).all()

    def listar_por_ocupacion(self, idOcupacion: int):
        consulta = select(Pago).where(
            Pago.idOcupacion == idOcupacion
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idPago: int):
        consulta = select(Pago).where(
            Pago.idPago == idPago
        )

        return self.db.scalar(consulta)

    def obtener_activo_por_ocupacion(self, idOcupacion: int):
        consulta = select(Pago).where(
            Pago.idOcupacion == idOcupacion,
            Pago.estado.in_(
                ["PENDIENTE", "PAGADO", "VENCIDO"]
            )
        )

        return self.db.scalar(consulta)

    def verificar_pago_vencido(self, idPago: int) -> bool:
        ahora = datetime.now()

        consulta = select(Pago).where(
            Pago.idPago == idPago,
            Pago.estado == "PENDIENTE",
            Pago.fechaLimitePago < ahora,
        )

        pago = self.db.scalar(consulta)

        return pago is not None

    def crear(self, datos: PagoCreate, codigoPago: str):
        fecha_limite = datetime.now() + timedelta(hours=24)

        pago = Pago(
            idOcupacion=datos.idOcupacion,
            codigoPago=codigoPago,
            montoTotal=datos.montoTotal,
            estado="PENDIENTE",
            fechaLimitePago=fecha_limite,
            observaciones=datos.observaciones
        )

        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)

        return pago

    def crear_calculado(
        self,
        idOcupacion: int,
        codigoPago: str,
        tiempoCobradoMinutos: int,
        tarifaPorHora,
        montoSubtotal,
        montoImpuesto,
        montoTotal,
    ):
        fecha_limite = datetime.now() + timedelta(hours=24)

        pago = Pago(
            idOcupacion=idOcupacion,
            codigoPago=codigoPago,
            tiempoCobradoMinutos=tiempoCobradoMinutos,
            tarifaPorHora=tarifaPorHora,
            montoSubtotal=montoSubtotal,
            montoImpuesto=montoImpuesto,
            montoTotal=montoTotal,
            estado="PENDIENTE",
            fechaLimitePago=fecha_limite,
        )

        self.db.add(pago)
        self.db.flush()

        return pago

    def actualizar(
        self,
        pago: Pago,
        datos: PagoUpdate
    ):
        datos_actualizados = datos.model_dump(
            exclude_unset=True
        )

        for campo, valor in datos_actualizados.items():
            setattr(pago, campo, valor)

        self.db.commit()
        self.db.refresh(pago)

        return pago

    def confirmar(
        self,
        pago: Pago,
        datos: PagoUpdate
    ):
        pago.estado = "PAGADO"
        pago.fechaPago = datetime.now()
        pago.metodoPago = datos.metodoPago
        pago.referenciaTransaccion = datos.referenciaTransaccion
        pago.numeroComprobante = datos.numeroComprobante

        if datos.observaciones is not None:
            pago.observaciones = datos.observaciones

        self.db.commit()
        self.db.refresh(pago)

        return pago

    def anular(self, pago: Pago):
        pago.estado = "ANULADO"

        self.db.commit()
        self.db.refresh(pago)

        return pago

    def marcar_vencido(self, pago: Pago):
        pago.estado = "VENCIDO"

        self.db.commit()
        self.db.refresh(pago)

        return pago