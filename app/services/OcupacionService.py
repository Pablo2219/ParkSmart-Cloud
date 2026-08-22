from datetime import datetime

from sqlalchemy.orm import Session

from app.common.utils.billing import (
    calcular_impuesto,
    calcular_subtotal_pago,
    calcular_tiempo_ocupacion,
    calcular_total_pago,
)
from app.repositories.OcupacionRepository import OcupacionRepository
from app.repositories.PagoRepository import PagoRepository
from app.repositories.QrRepository import QrRepository
from app.repositories.ReservaRepository import ReservaRepository
from app.schemas.ocupacion.FinalizarOcupacionRequest import (
    FinalizarOcupacionRequest,
)
from app.schemas.ocupacion.OcupacionCreate import OcupacionCreate
from app.schemas.ocupacion.OcupacionUpdate import OcupacionUpdate


class OcupacionService:

    def __init__(self, db: Session):
        self.db = db
        self.ocupacion_repository = OcupacionRepository(db)
        self.reserva_repository = ReservaRepository(db)
        self.pago_repository = PagoRepository(db)
        self.qr_repository = QrRepository(db)

    def listar_ocupaciones(self):
        return self.ocupacion_repository.listar()

    def listar_ocupaciones_activas(self):
        return self.ocupacion_repository.listar_activas()

    def listar_ocupaciones_por_reserva(self, idReserva: int):
        reserva = self.reserva_repository.obtener_por_id(idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        return self.ocupacion_repository.listar_por_reserva(idReserva)

    def obtener_ocupacion(self, idOcupacion: int):
        ocupacion = self.ocupacion_repository.obtener_por_id(idOcupacion)

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        return ocupacion

    def iniciar_ocupacion(self, datos: OcupacionCreate):
        qr = self.qr_repository.obtener_por_id(datos.idQr)

        if qr is None:
            raise ValueError("El QR no existe.")

        if not self.qr_repository.validar_qr_activo(datos.idQr):
            raise ValueError(
                "El codigo QR no es valido o esta fuera del rango permitido."
            )

        reserva = self.reserva_repository.obtener_por_id(qr.idReserva)

        if reserva is None:
            raise ValueError("La reserva asociada al QR no existe.")

        if reserva.estado != "CONFIRMADA":
            raise ValueError(
                "La reserva asociada al QR no se encuentra confirmada."
            )

        ocupacion_existente = self.ocupacion_repository.obtener_por_qr(
            datos.idQr
        )

        if ocupacion_existente is not None:
            raise ValueError(
                "Ya existe una ocupacion asociada a este QR."
            )

        ocupacion_activa = self.ocupacion_repository.obtener_activa_por_reserva(
            reserva.idReserva
        )

        if ocupacion_activa is not None:
            raise ValueError(
                "Ya existe una ocupacion activa para esta reserva."
            )

        try:
            ocupacion = self.ocupacion_repository.crear(
                idReserva=reserva.idReserva,
                idEspacio=reserva.idEspacio,
                idQr=datos.idQr,
                observaciones=datos.observaciones
            )

            self.db.commit()
            self.db.refresh(ocupacion)

            return ocupacion

        except Exception:
            self.db.rollback()
            raise

    def actualizar_ocupacion(
        self,
        idOcupacion: int,
        datos: OcupacionUpdate
    ):
        ocupacion = self.ocupacion_repository.obtener_por_id(idOcupacion)

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        if ocupacion.estado != "EN_CURSO":
            raise ValueError(
                "Solo se pueden modificar ocupaciones en curso."
            )

        return self.ocupacion_repository.actualizar(
            ocupacion,
            datos
        )

    def finalizar_ocupacion(
        self,
        idOcupacion: int,
        datos: FinalizarOcupacionRequest,
    ):
        ocupacion = self.ocupacion_repository.obtener_por_id(
            idOcupacion
        )

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        if ocupacion.estado != "EN_CURSO":
            raise ValueError(
                "Solo se pueden finalizar ocupaciones en curso."
            )

        pago_existente = self.pago_repository.obtener_activo_por_ocupacion(
            idOcupacion
        )

        if pago_existente is not None:
            raise ValueError(
                "Ya existe un pago registrado para esta ocupacion."
            )

        try:
            fecha_salida = datetime.now()

            tiempo_minutos = calcular_tiempo_ocupacion(
                ocupacion.fechaEntrada,
                fecha_salida
            )

            if tiempo_minutos <= 0:
                tiempo_minutos = 1

            subtotal = calcular_subtotal_pago(
                tiempo_minutos,
                datos.tarifaPorHora
            )

            impuesto = calcular_impuesto(
                subtotal,
                datos.porcentajeImpuesto
            )

            total = calcular_total_pago(
                subtotal,
                impuesto
            )

            codigo_pago = (
                f"PAG-{idOcupacion}-"
                f"{fecha_salida.strftime('%Y%m%d%H%M%S')}"
            )

            ocupacion = self.ocupacion_repository.finalizar(
                ocupacion,
                fecha_salida,
                tiempo_minutos
            )

            self.pago_repository.crear_calculado(
                idOcupacion=idOcupacion,
                codigoPago=codigo_pago,
                tiempoCobradoMinutos=tiempo_minutos,
                tarifaPorHora=datos.tarifaPorHora,
                montoSubtotal=subtotal,
                montoImpuesto=impuesto,
                montoTotal=total,
            )

            self.db.commit()
            self.db.refresh(ocupacion)

            return ocupacion

        except Exception:
            self.db.rollback()
            raise

    def cancelar_ocupacion(self, idOcupacion: int):
        ocupacion = self.ocupacion_repository.obtener_por_id(
            idOcupacion
        )

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        if ocupacion.estado != "EN_CURSO":
            raise ValueError(
                "Solo se pueden cancelar ocupaciones en curso."
            )

        return self.ocupacion_repository.cancelar(
            ocupacion
        )